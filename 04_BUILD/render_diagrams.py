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
        self.parts.append(
            '<text x="%.2f" y="%.2f" font-family="serif" font-size="%.2f" '
            'text-anchor="%s" fill="#000">%s</text>'
            % (x, y, pt * 96.0 / 72.0, anchor, s))

    def arrow(self, x1, y1, x2, y2, w, dash=None):
        self.line(x1, y1, x2, y2, w, dash)
        ang = math.atan2(y2 - y1, x2 - x1)
        h = 3.0 * MM
        for s in (0.4, -0.4):
            self.parts.append(
                '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#000" '
                'stroke-width="%.2f"/>'
                % (x2, y2, x2 - h * math.cos(ang - s), y2 - h * math.sin(ang - s), w))

    def cross(self, cx, cy, r):
        self.line(cx - r, cy - r, cx + r, cy + r)
        self.line(cx - r, cy + r, cx + r, cy - r)

    def svg(self, title: str) -> str:
        return ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<svg xmlns="http://www.w3.org/2000/svg" width="%.2f" '
                'height="%.2f" viewBox="0 0 %.2f %.2f">\n'
                '<title>%s</title>\n'
                '<rect width="100%%" height="100%%" fill="#fff"/>\n%s\n</svg>\n'
                % (self.w, self.h, self.w, self.h, title,
                   "\n".join(self.parts)))


def coord_xy(coord: str, cls: str, size: dict, x0, y0, step):
    if cls in ("cell", "point"):
        col = ord(coord[0]) - ord("a")
        row = int(coord[1:]) - 1
        rows = size.get("rows", 1)
        off = step / 2.0 if cls == "cell" else 0.0
        return x0 + col * step + off, y0 + (rows - 1 - row) * step + off
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

    if cls in ("cell", "point"):
        cols, rows = size.get("cols", 1), size.get("rows", 1)
        n = cols if cls == "point" else cols
        w = pad * 2 + (cols - (0 if cls == "cell" else 1)) * step_mm
        h = pad * 2 + (rows - (0 if cls == "cell" else 1)) * step_mm + legend_h
        c = Canvas(w, h, sw)
        x0, y0 = pad * MM, pad * MM
        step = step_mm * MM
        if cls == "cell":
            for i in range(cols + 1):
                c.line(x0 + i * step, y0, x0 + i * step, y0 + rows * step)
            for j in range(rows + 1):
                c.line(x0, y0 + j * step, x0 + cols * step, y0 + j * step)
        else:
            for i in range(cols):
                c.line(x0 + i * step, y0, x0 + i * step, y0 + (rows - 1) * step)
            for j in range(rows):
                c.line(x0, y0 + j * step, x0 + (cols - 1) * step, y0 + j * step)
        r = step * ratio / 2.0
        for p in d.get("pieces", []):
            xy = coord_xy(p["at"], cls, size, x0, y0, step)
            if not xy:
                continue
            g = lang["glyphs"][p["glyph"]]
            c.circle(xy[0], xy[1], r, g["fill"],
                     ring=p["glyph"] in ("king", "lightSpecial", "darkSpecial"))
            if p.get("captured"):
                c.cross(xy[0], xy[1], r * 0.8)
        for a in d.get("arrows", []):
            f = coord_xy(a.get("from", ""), cls, size, x0, y0, step)
            t = coord_xy(a.get("to", ""), cls, size, x0, y0, step)
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

    else:  # bodily
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
    ly = c.h - legend_h * MM + 3 * MM
    for e in d.get("legend", []):
        g = lang["glyphs"].get(e.get("glyph")) or lang["arrows"].get(e.get("glyph")) \
            or lang["markers"].get(e.get("glyph")) or {}
        c.text(pad * MM, ly, "%s  %s" % (g.get("symbol", "·"), e.get("label", "")),
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
