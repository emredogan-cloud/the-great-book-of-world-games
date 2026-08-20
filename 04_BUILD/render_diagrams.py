#!/usr/bin/env python3
"""
DİYAGRAM RENDER — The Great Book of World Games
================================================================================
Tanımlayıcıları (`07_ASSETS/diagrams/*.json`) gerçek SVG'ye çevirir.

  ⚠ ÜRETİM VARLIĞI DEĞİLDİR. Nihai gravür levhalar Faz 5'te üretilir.
  Buradaki çıktı DOĞRULAMA ve ÖLÇÜM içindir: dizgi, diyagramın kapladığı
  gerçek alanı tahmin etmek yerine ÖLÇEBİLSİN diye.

TASARIM: yalnızca standart kütüphane. SVG bir metin biçimidir; onu yazmak
için bir grafik kütüphanesine ihtiyaç yoktur. Çıktı DETERMİNİSTİKTİR —
aynı girdi her makinede byte-byte aynı dosyayı üretir, yani bir diyagramın
değişip değişmediği `git diff` ile görülür.

Bütün ölçüler `DIAGRAM_LANGUAGE.md § 7`den okunur; hiçbiri buraya gömülü
değildir.

Çıkış kodları:  0 = üretildi   1 = hata   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import math

import typo
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

MM = 3.7795275591  # 1 mm = 3.7795 px @96dpi — SVG kullanıcı birimi


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def grey(level: int) -> str:
    """Yalnızca izinli gri seviyeleri (D2). Ara ton YOKTUR."""
    v = int(round(255 * (100 - level) / 100.0))
    return "#%02x%02x%02x" % (v, v, v)


class Canvas:
    def __init__(self, w_mm: float, h_mm: float, stroke_pt: float):
        self.w, self.h = w_mm * MM, h_mm * MM
        self.sw = stroke_pt * 96.0 / 72.0
        self.parts: list[str] = []

    def line(self, x1, y1, x2, y2, w=None, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.parts.append(
            '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#000" '
            'stroke-width="%.2f"%s/>' % (x1, y1, x2, y2, w or self.sw, d))

    def circle(self, cx, cy, r, fill=0, ring=False):
        self.parts.append(
            '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" stroke="#000" '
            'stroke-width="%.2f"/>' % (cx, cy, r, grey(fill), self.sw))
        if ring:
            self.parts.append(
                '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" '
                'stroke-width="%.2f"/>'
                % (cx, cy, r * 0.55, grey(0) if fill == 100 else "#000", self.sw))

    def text(self, x, y, s, pt, anchor="middle"):
        # XML kaçışı + dizgi tırnağı. Bu satır uzun süre kaçışsızdı:
        # etiketteki bir `&` geçersiz SVG üretirdi ve etiketteki düz kesme
        # işareti — iç metin düzeltildikten SONRA bile — daktilo kalırdı.
        self.parts.append(
            '<text x="%.2f" y="%.2f" font-family="serif" font-size="%.2f" '
            'text-anchor="%s" fill="#000">%s</text>'
            % (x, y, pt * 96.0 / 72.0, anchor, typo.xml_text(s)))

    def arrow(self, x1, y1, x2, y2, w, dash=None):
        self.line(x1, y1, x2, y2, w, dash)
        ang = math.atan2(y2 - y1, x2 - x1)
        h = 3.0 * MM
        for s in (0.4, -0.4):
            self.parts.append(
                '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#000" '
                'stroke-width="%.2f"/>'
                % (x2, y2, x2 - h * math.cos(ang - s), y2 - h * math.sin(ang - s), w))

    def cross(self, cx, cy, r, ink="#000"):
        for x1, y1, x2, y2 in ((cx - r, cy - r, cx + r, cy + r),
                               (cx - r, cy + r, cx + r, cy - r)):
            self.parts.append(
                '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
                'stroke-width="%.2f"/>' % (x1, y1, x2, y2, ink, self.sw * 1.4))

    def rect(self, x, y, w, h, ink="#000"):
        """Dolgusuz dikdörtgen — `bodily/bed` bölmeleri (v1.4) ve v1.5'te
        haç tahtasının VAR OLAN kareleri. Izgara çizgileri bir haçın
        köşelerini de doldururdu; kare kare çizim doldurmaz."""
        self.parts.append(
            '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" '
            'stroke="%s" stroke-width="%.2f"/>' % (x, y, w, h, ink, self.sw))

    def svg(self, title: str) -> str:
        return ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<svg xmlns="http://www.w3.org/2000/svg" width="%.2f" '
                'height="%.2f" viewBox="0 0 %.2f %.2f">\n'
                '<title>%s</title>\n'
                '<rect width="100%%" height="100%%" fill="#fff"/>\n%s\n</svg>\n'
                % (self.w, self.h, self.w, self.h, title,
                   "\n".join(self.parts)))


def coord_xy(coord: str, cls: str, size: dict, x0, y0, step, ry=None):
    """Koordinat → piksel. `ry` verilirse satır y'si ondan alınır.

    v1.5: `gapAfterRow` (nehir) satır konumlarını kaydırır ve bu kaydırmayı
    TEK bir yerde tutmak zorundayız; iki ayrı hesap ayrışırsa taşlar
    tahtanın yanına düşer."""
    if cls in ("cell", "point"):
        try:
            col = ord(coord[0]) - ord("a")
            row = int(coord[1:]) - 1
        except (ValueError, IndexError):
            return None
        rows = size.get("rows", 1)
        off = step / 2.0 if cls == "cell" else 0.0
        y = ry(row) if ry else y0 + (rows - 1 - row) * step
        if cls == "cell":
            y = y + off          # üst kenar + yarım adım = hücre merkezi
        return x0 + col * step + off, y
    return None


def render(d: dict, lang: dict, out_dir: str) -> dict:
    """Bir tanımlayıcıyı SVG'ye çevirir ve ÖLÇÜLERİNİ döndürür."""
    pr = lang["print"]
    cls = d["boardClass"]
    size = d.get("size", {})
    sw = pr["minStrokePt"]
    ratio = (pr["pieceDiameterRatioMin"] + pr["pieceDiameterRatioMax"]) / 2.0
    step_mm = 7.0
    pad = 6.0
    legend_h = 4.5 * max(1, len(d.get("legend", [])))

    if cls == "point" and d.get("nodes"):
        # DÜZENSİZ NOKTA TAHTASI (v1.3). Izgara yok: düğümler ve kenarlar
        # açıkça verilir. Yaklaşık bir ızgarayla idare etmek YASAKTIR —
        # yanlış çizilmiş bir tahta oyunu oynanamaz yapar.
        nodes = d["nodes"]
        span = size.get("spanMm", 60.0)
        aspect = size.get("aspect", 1.0)
        w = pad * 2 + span
        h = pad * 2 + span * aspect + legend_h
        c = Canvas(w, h, sw)
        x0, y0 = pad * MM, pad * MM
        def nxy(k):
            x, y = nodes[k]
            return x0 + x * span * MM, y0 + y * span * aspect * MM
        for a, b in d.get("edges", []):
            ax, ay = nxy(a); bx, by = nxy(b)
            c.line(ax, ay, bx, by)
        r = min(span * MM * 0.045, 2.6 * MM)
        placed = {p["at"]: p for p in d.get("pieces", [])}
        for k in nodes:
            if k in placed:
                g = lang["glyphs"][placed[k]["glyph"]]
                c.circle(*nxy(k), r, g["fill"],
                         ring=placed[k]["glyph"] in ("king", "lightSpecial",
                                                     "darkSpecial"))
                if placed[k].get("captured"):
                    c.cross(*nxy(k), r * 0.8,
                            "#fff" if g["fill"] >= 55 else "#000")
            else:
                c.circle(*nxy(k), r * 0.42, 0)
        for a in d.get("arrows", []):
            if a.get("from") in nodes and a.get("to") in nodes:
                spec = lang["arrows"][a["kind"]]
                fx, fy = nxy(a["from"]); tx, ty = nxy(a["to"])
                c.arrow(fx, fy, tx, ty, spec["widthPt"] * 96 / 72,
                        "3,2" if spec["style"] == "dotted" else None)

    elif cls in ("cell", "point"):
        cols, rows = size.get("cols", 1), size.get("rows", 1)
        # v1.5 ① OMITTED CELLS — tahtada BULUNMAYAN kareler (haç tahtası).
        # v1.5 ③ GAP AFTER ROW — nehir: bir sıradan sonra bir sıra boşluk.
        omit = set(d.get("omitCells") or [])
        gap_after = d.get("gapAfterRow")
        gap_mm = step_mm if gap_after else 0.0
        w = pad * 2 + (cols - (0 if cls == "cell" else 1)) * step_mm
        h = (pad * 2 + (rows - (0 if cls == "cell" else 1)) * step_mm
             + gap_mm + legend_h)
        c = Canvas(w, h, sw)
        x0, y0 = pad * MM, pad * MM
        step = step_mm * MM
        gap = gap_mm * MM

        def ry(row):
            """Satırın y'si. `gapAfterRow` verilmişse ALT bölge aşağı kayar.

            Nehir bir boşluk değil bir KURALDIR (fil geçemez); bu yüzden
            çizimde de gerçek bir boşluk olarak durur, bir çizgi olarak
            değil."""
            y = y0 + (rows - 1 - row) * step
            if gap_after and row <= gap_after - 1:
                y += gap
            return y

        # `ry(row)` bir hücrenin ÜST kenarıdır; hücre oradan bir adım
        # aşağı iner. (v1.5'in ilk sürümü bunu bir adım YUKARI çiziyordu
        # ve her cell tahtasının en üst sırası tuvalin dışına taşıyordu —
        # görsel denetimde Ur tahtasında yakalandı.)
        if cls == "cell":
            top, bot = ry(rows - 1), ry(0) + step
            if omit:
                # VAR OLAN kareleri tek tek çiz. Izgara çizgileri bir haçın
                # köşelerini de doldurur; kare kare çizim doldurmaz.
                for col in range(cols):
                    for row in range(rows):
                        coord = "%s%d" % (chr(ord("a") + col), row + 1)
                        if coord in omit:
                            continue
                        c.rect(x0 + col * step, ry(row), step, step)
            else:
                for i in range(cols + 1):
                    c.line(x0 + i * step, top, x0 + i * step, bot)
                for j in range(rows):
                    c.line(x0, ry(j), x0 + cols * step, ry(j))
                c.line(x0, bot, x0 + cols * step, bot)
        else:
            for i in range(cols):
                if gap_after:
                    c.line(x0 + i * step, ry(rows - 1),
                           x0 + i * step, ry(gap_after))
                    c.line(x0 + i * step, ry(gap_after - 1),
                           x0 + i * step, ry(0))
                else:
                    c.line(x0 + i * step, ry(rows - 1), x0 + i * step, ry(0))
            for j in range(rows):
                c.line(x0, ry(j), x0 + (cols - 1) * step, ry(j))

        # v1.5 ② LINES — hisar köşegeni, terfi köşegeni, bölge sınırı.
        for ln in d.get("lines") or []:
            f = coord_xy(ln.get("from", ""), cls, size, x0, y0, step, ry)
            t = coord_xy(ln.get("to", ""), cls, size, x0, y0, step, ry)
            if f and t:
                c.line(f[0], f[1], t[0], t[1])

        r = step * ratio / 2.0
        for p in d.get("pieces", []):
            xy = coord_xy(p["at"], cls, size, x0, y0, step, ry)
            if not xy:
                continue
            g = lang["glyphs"][p["glyph"]]
            c.circle(xy[0], xy[1], r, g["fill"],
                     ring=p["glyph"] in ("king", "lightSpecial", "darkSpecial"))
            if p.get("captured"):
                c.cross(xy[0], xy[1], r * 0.8,
                        "#fff" if g["fill"] >= 55 else "#000")
        for a in d.get("arrows", []):
            f = coord_xy(a.get("from", ""), cls, size, x0, y0, step, ry)
            t = coord_xy(a.get("to", ""), cls, size, x0, y0, step, ry)
            if f and t:
                spec = lang["arrows"][a["kind"]]
                c.arrow(f[0], f[1], t[0], t[1], spec["widthPt"] * 96 / 72,
                        "3,2" if spec["style"] == "dotted" else None)

    elif cls == "pit":
        pits, rows = size.get("pitsPerRow", 6), size.get("rows", 2)
        w = pad * 2 + pits * step_mm * 1.4
        h = pad * 2 + rows * step_mm * 1.4 + legend_h
        c = Canvas(w, h, sw)
        x0, y0 = pad * MM, pad * MM
        step = step_mm * 1.4 * MM
        for r_i in range(rows):
            for p_i in range(pits):
                c.circle(x0 + p_i * step + step / 2, y0 + r_i * step + step / 2,
                         step * 0.36, 0)
        by = {p["at"]: p for p in d.get("pieces", [])}
        rowmap = ["A", "A'", "B'", "B"][:rows] if rows == 4 else ["A", "B"]
        for r_i, rk in enumerate(rowmap):
            for p_i in range(pits):
                key = "%s%d" % (rk, p_i + 1)
                if key in by:
                    c.text(x0 + p_i * step + step / 2,
                           y0 + r_i * step + step / 2 + 1.2 * MM,
                           str(by[key].get("value", "")), pr["minGlyphPt"] + 1)

    elif cls == "track":
        n = 20
        w = h = pad * 2 + 6 * step_mm
        h += legend_h
        c = Canvas(w, h, sw)
        side = 6 * step_mm * MM
        x0, y0 = pad * MM, pad * MM
        step = side / 5.0
        pts = []
        for i in range(5):
            pts.append((x0 + i * step, y0))
        for i in range(5):
            pts.append((x0 + side, y0 + i * step))
        for i in range(5):
            pts.append((x0 + side - i * step, y0 + side))
        for i in range(5):
            pts.append((x0, y0 + side - i * step))
        for i, (px, py) in enumerate(pts):
            big = i % 5 == 0
            c.circle(px, py, step * (0.30 if big else 0.20), 0)
        c.line(x0, y0, x0 + side, y0 + side, sw * 96 / 72, "4,3")
        c.line(x0 + side, y0, x0, y0 + side, sw * 96 / 72, "4,3")
        c.circle(x0 + side / 2, y0 + side / 2, step * 0.30, 0)

    elif cls == "bodily" and d.get("frame") == "figure":
        # `figure` (v1.5) — İP FİGÜRÜ. `hands` çerçevesi soyut bir şema
        # çizer ve iki figürü BİRBİRİNDEN AYIRT EDEMEZ: Beşik ile Asker
        # Yatağı aynı görünür. Faz 5 bunu görsel denetimde ölçtü.
        #
        # Burada ipin GERÇEK YOLU taşınır: adlandırılmış düğümler (parmaklar
        # ve çaprazlama noktaları, 0–1 normalize) ve `strings` — düğümden
        # düğüme geçen polilinler. Sınır denetimi tanımlı düğüm kümesidir.
        nodes = d.get("nodes", {})
        span = size.get("spanMm", 58.0)
        aspect = size.get("aspect", 0.72)
        w = pad * 2 + span
        h = pad * 2 + span * aspect + legend_h
        c = Canvas(w, h, sw)
        x0, y0 = pad * MM, pad * MM

        def fxy(k):
            x, y = nodes[k]
            return x0 + x * span * MM, y0 + y * span * aspect * MM

        # İpin kendisi ÖNCE çizilir; parmaklar üstüne biner, çünkü ip
        # parmağın ARKASINDAN geçer ve okur bunu görmek zorundadır.
        for path in d.get("strings", []):
            pts = [k for k in path if k in nodes]
            for a, b in zip(pts, pts[1:]):
                ax, ay = fxy(a)
                bx, by = fxy(b)
                c.line(ax, ay, bx, by)
        placed = {p["at"]: p for p in d.get("pieces", [])}
        for k in nodes:
            gk = placed.get(k, {}).get("glyph")
            if gk:
                g = lang["glyphs"][gk]
                c.circle(*fxy(k), 2.0 * MM, g["fill"],
                         ring=gk in ("king", "lightSpecial", "darkSpecial"))
        for a in d.get("arrows", []):
            if a.get("from") in nodes and a.get("to") in nodes:
                spec = lang["arrows"][a["kind"]]
                fx, fy = fxy(a["from"])
                tx, ty = fxy(a["to"])
                c.arrow(fx, fy, tx, ty, spec["widthPt"] * 96 / 72,
                        "3,2" if spec["style"] == "dotted" else None)

    elif cls == "bodily" and d.get("frame") == "bed":
        # `bed` (v1.4) — ZEMİNE ÇİZİLEN BÖLMELER. Bölmeler AÇIKÇA verilir;
        # bir ızgara varsayılmaz, çünkü seksek yatağı ızgara değildir.
        # Ölçüler 0–1 normalize; en/boy oranı `size.aspect` ile verilir.
        divs = d.get("divisions", [])
        span = size.get("spanMm", 46.0)
        aspect = size.get("aspect", 1.6)
        w = pad * 2 + span
        h = pad * 2 + span * aspect + legend_h
        c = Canvas(w, h, sw)
        x0, y0 = pad * MM, pad * MM
        for r in divs:
            rx, ry = x0 + r["x"] * span * MM, y0 + r["y"] * span * aspect * MM
            rw, rh = r["w"] * span * MM, r["h"] * span * aspect * MM
            c.rect(rx, ry, rw, rh)
            c.text(rx + rw / 2, ry + rh / 2 + pr["minGlyphPt"] * 0.35,
                   str(r.get("label", "")), pr["minGlyphPt"])
        ids = {r["id"] for r in divs}
        for p in d.get("pieces", []):
            r = next((x for x in divs if x["id"] == p["at"]), None)
            if not r:
                continue
            g = lang["glyphs"][p["glyph"]]
            # Taş bölmenin SOL yarısına konur: ortaya konursa bölme
            # numarasının üstüne biner ve ikisi birden okunmaz olur.
            c.circle(x0 + (r["x"] + r["w"] * 0.22) * span * MM,
                     y0 + (r["y"] + r["h"] * 0.5) * span * aspect * MM,
                     1.7 * MM, g["fill"])
        del ids

    else:  # bodily · hands | formation
        # `hands` gövdesi KOMPAKT: ip figürü ±10 mm'lik bir alanda yaşar ve
        # 46 mm'lik gövde bunun iki katıydı. Faz 3 bütçesi (150 mm) bu boş
        # payı taşımıyor. Kalınlık ve glif boyu korunur; giden şey KENAR PAYI.
        body_h = 30.0 if d.get("frame") == "hands" else 46.0
        w, h = 70.0, body_h + legend_h
        c = Canvas(w, h, sw)
        cx, cy = w * MM / 2, 22.0 * MM
        if d.get("frame") == "formation":
            for i in range(12):
                a = 2 * math.pi * i / 12
                c.circle(cx + 22 * MM * math.cos(a), cy + 16 * MM * math.sin(a),
                         2.0 * MM, 0)
            c.circle(cx, cy, 2.6 * MM, 25)
            c.circle(cx - 8 * MM, cy, 2.6 * MM, 25)
        else:
            cy = body_h / 2 * MM
            for x in (-18, 18):
                for y in (-8, 8):
                    c.circle(cx + x * MM, cy + y * MM, 1.6 * MM, 0)
            c.line(cx - 18 * MM, cy - 8 * MM, cx + 18 * MM, cy + 8 * MM)
            c.line(cx - 18 * MM, cy + 8 * MM, cx + 18 * MM, cy - 8 * MM)
            c.line(cx - 18 * MM, cy - 8 * MM, cx - 18 * MM, cy + 8 * MM)
            c.line(cx + 18 * MM, cy - 8 * MM, cx + 18 * MM, cy + 8 * MM)

    # Efsane — her diyagramın kendi içinde (D7)
    #
    # ⚠ SEMBOL YAZILMAZ, ÇİZİLİR. v1.3'e kadar efsane sembolü bir METİN
    # karakteriydi (◉, ◎, ⤳ …) ve font o karakteri taşımıyorsa YER BOŞ
    # KALIYORDU. Faz 4 render denetimi bunu üç diyagramda gördü: tilki
    # efsanede sembolsüz duruyordu ve okur hangi taşın tilki olduğunu
    # efsaneden ÖĞRENEMİYORDU. Artık efsane, tahtadaki gliflerin AYNI
    # çizim yoluyla üretilir; font bağımlılığı yoktur.
    ly = c.h - legend_h * MM + 3 * MM
    sym_x = pad * MM + 1.6 * MM
    for e in d.get("legend", []):
        key = e.get("glyph")
        gl, ar = lang["glyphs"].get(key), lang["arrows"].get(key)
        if gl:
            c.circle(sym_x, ly - 0.9 * MM, 1.5 * MM, gl["fill"],
                     ring=key in ("king", "lightSpecial", "darkSpecial"))
            # `captured` bir TAŞ DEĞİL, taşın üstündeki işarettir. Efsanede
            # düz bir çember olarak çizilirse "savunan"dan ayırt edilemez ve
            # okur ×'i yine öğrenemez.
            if key == "captured":
                c.cross(sym_x, ly - 0.9 * MM, 1.2 * MM)
        elif ar:
            c.arrow(sym_x - 1.5 * MM, ly - 0.9 * MM, sym_x + 1.6 * MM,
                    ly - 0.9 * MM, ar["widthPt"] * 96 / 72,
                    "3,2" if ar["style"] == "dotted" else None)
        else:
            # ⚠ MARKER SEMBOLÜ DE ÇİZİLİR, YAZILMAZ.
            # v1.3 bu dersi GLİFLER için öğrendi ve yazdı: "SEMBOL
            # YAZILMAZ, ÇİZİLİR; font o karakteri taşımıyorsa YER BOŞ
            # KALIR." Ama MARKER yolu metin yazmaya devam etti. Faz 6
            # ölçtü: üç marker sembolünün (↺ ⟦⟧ ⌒) ÜÇÜ DE baskı fontunda
            # (Liberation Serif) YOK. `mbube-formation` efsanesindeki
            # 'ring' satırı basılı sayfada SEMBOLSÜZ çıkacaktı ve okur
            # çemberin ne olduğunu efsaneden öğrenemeyecekti.
            r = 1.5 * MM
            if key == "ring":
                c.parts.append(
                    '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" '
                    'stroke="#000" stroke-width="%.2f"/>'
                    % (sym_x, ly - 0.9 * MM, r, c.sw))
            elif key == "repeat":
                c.parts.append(
                    '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" '
                    'stroke="#000" stroke-width="%.2f"/>'
                    % (sym_x, ly - 0.9 * MM, r * 0.85, c.sw))
                c.line(sym_x + r * 0.5, ly - 1.9 * MM,
                       sym_x + r * 1.2, ly - 0.9 * MM)
            elif key == "score":
                for dx in (-r, r):
                    c.line(sym_x + dx, ly - 2.0 * MM, sym_x + dx, ly)
                    c.line(sym_x + dx, ly - 2.0 * MM,
                           sym_x + dx * 0.45, ly - 2.0 * MM)
                    c.line(sym_x + dx, ly, sym_x + dx * 0.45, ly)
            else:
                c.circle(sym_x, ly - 0.9 * MM, r * 0.5, 0)
        c.text(pad * MM + 4.6 * MM, ly, e.get("label", ""),
               pr["minGlyphPt"], anchor="start")
        ly += 4.5 * MM

    path = os.path.join(out_dir, "%s.svg" % d["diagramId"])
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(c.svg(d["diagramId"]))
    return {"diagramId": d["diagramId"], "gameId": d["gameId"],
            "widthMm": round(c.w / MM, 2), "heightMm": round(c.h / MM, 2),
            "legendMm": round(legend_h, 2),
            "boardClass": cls, "panels": d.get("panels", 1),
            "file": os.path.relpath(path, DEFAULT_ROOT)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    print("=" * 74)
    print("  DİYAGRAM RENDER (doğrulama amaçlı)")
    print("=" * 74)

    cfg = load(os.path.join(root, "project_config.json"))
    lang = load(os.path.join(root, cfg["diagram"]["specData"]))
    ddir = os.path.join(root, "07_ASSETS", "diagrams")

    out: list = []
    for fn in sorted(os.listdir(ddir)):
        if not fn.endswith(".json") or fn == "diagram_language.json":
            continue
        for d in load(os.path.join(ddir, fn)).get("diagrams", []):
            m = render(d, lang, ddir)
            # PANEL DİZİLİMİ — v1.1. Yatay dizilim genişliği çarpar; ip
            # figürünün üç paneli yan yana 180 mm sınırını aşıyordu, bu
            # yüzden `bodily/hands` DİKEY dizilir ve yüksekliği çarpar.
            layout = lang["panelRules"]["panelLayout"]
            key = "%s/%s" % (m["boardClass"], d.get("frame", ""))
            vertical = layout.get(key, layout["default"]) == "vertical"
            gap = 4 if m["panels"] > 1 else 0
            if vertical:
                m["renderedWidthMm"] = m["widthMm"]
                body = m["heightMm"] - m["legendMm"]
                m["heightMm"] = round(body * m["panels"]
                                      + gap * (m["panels"] - 1)
                                      + m["legendMm"], 2)
            else:
                m["renderedWidthMm"] = round(m["widthMm"] * m["panels"] + gap, 2)
            m["panelLayout"] = "vertical" if vertical else "horizontal"
            fits = m["renderedWidthMm"] <= lang["print"]["maxWidthFullMm"]
            m["fitsFullWidth"] = fits
            m["withinDiagramBudget"] = (
                m["heightMm"] <= lang["print"]["maxDiagramColumnHeightMm"])
            out.append(m)
            flags = []
            if not fits:
                flags.append("⚠ GENİŞLİK SINIRINI AŞIYOR")
            if not m["withinDiagramBudget"]:
                flags.append("⚠ DİYAGRAM BÜTÇESİNİ AŞIYOR → madde 4 sayfa")
            print("  %-24s %-9s %d panel %-10s %6.1f × %5.1f mm  %s"
                  % (d["diagramId"], d["boardClass"], m["panels"],
                     m["panelLayout"], m["renderedWidthMm"], m["heightMm"],
                     " · ".join(flags) if flags else "✓"))

    print("\n  %d diyagram üretildi" % len(out))
    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"diagrams": out}, fh, ensure_ascii=False, indent=2)
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
