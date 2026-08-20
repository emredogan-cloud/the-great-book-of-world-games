#!/usr/bin/env python3
"""
SVG → VEKTÖR ÇEVİRİCİ — The Great Book of World Games
================================================================================
`render_diagrams.py`ın ürettiği SVG'yi okur ve onu **çizim emirlerine**
çevirir. Emirler iki yere gider:

  · `interior.py`  → reportlab · PDF içine GERÇEK VEKTÖR olarak
  · `qa_visual.py` → PIL · gözle denetim için raster

⚠ NEDEN KENDİ ÇEVİRİCİMİZ. Sistemde `rsvg-convert` yoktur ve ImageMagick'in
iç SVG çizicisi bu dosyaları YANLIŞ çiziyor: `morris-mill.svg`ın dolu siyah
taşları beyaz çıktı. Yanlış dolgu bir estetik kusur değildir — bu kitapta
taşın rengi HANGİ OYUNCUYA ait olduğudur ve yanlış dolgu diyagramı yalancı
yapar.

⚠ NEDEN RASTER DEĞİL. Diyagram bir çizgi çizimidir; 300 dpi'da rasterleştirmek
hem dosyayı şişirir hem POD baskıda 0,75 pt çizgiyi kırar. Vektör kalırsa
çizgi baskı çözünürlüğünde basılır ve fotokopi ölçeğinde (%71) de ayakta
kalır — arka maddedeki tahta şablonlarının bütün amacı budur.

Desteklenen sözlük — `render_diagrams.py`ın ÜRETTİĞİNİN TAMAMI:

    <svg width height viewBox>  <rect>  <line>  <circle>  <text>  <title>

Bu liste bir varsayım değildir: `qa_visual.py --check-vocabulary` bütün
SVG'leri tarar ve burada olmayan bir eleman görürse KIRMIZI yanar. Sessizce
atlanan bir eleman, eksik çizilmiş bir tahtadır.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
"""

from __future__ import annotations

import os
import re
import sys
import xml.etree.ElementTree as ET

SVG_NS = "{http://www.w3.org/2000/svg}"
PX_PER_MM = 3.7795275591          # render_diagrams.py ile AYNI sabit
KNOWN_TAGS = {"svg", "title", "rect", "line", "circle", "text"}


class UnknownElement(Exception):
    """Sözlükte olmayan bir SVG elemanı. Sessizce atlanmaz."""


def _f(el, name, default=0.0):
    v = el.get(name)
    if v is None:
        return default
    return float(str(v).replace("%", "").strip())


def _colour(v, default=(0, 0, 0)):
    """`#rgb` / `#rrggbb` / `none` → (r,g,b) 0–255 ya da None."""
    if v is None:
        return default
    v = v.strip().lower()
    if v in ("none", "transparent"):
        return None
    if v.startswith("#"):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) == 6:
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    return default


def parse(path: str) -> dict:
    """SVG dosyasını çizim emirlerine çevirir.

    Döndürür: {"widthPx","heightPx","widthMm","heightMm","title","ops":[…]}
    Emirler kaynaktaki SIRAYLA durur; z-sırası budur ve korunur.
    """
    tree = ET.parse(path)
    root = tree.getroot()
    tag = root.tag.replace(SVG_NS, "")
    if tag != "svg":
        raise UnknownElement("kök eleman <svg> değil: <%s>" % tag)

    w = _f(root, "width")
    h = _f(root, "height")
    ops: list[dict] = []
    title = ""

    for el in root:
        t = el.tag.replace(SVG_NS, "")
        if t not in KNOWN_TAGS:
            raise UnknownElement("%s: bilinmeyen eleman <%s>"
                                 % (os.path.basename(path), t))
        if t == "title":
            title = (el.text or "").strip()
        elif t == "rect":
            rw = el.get("width", "0")
            rh = el.get("height", "0")
            ops.append({
                "op": "rect",
                "x": _f(el, "x"), "y": _f(el, "y"),
                # width="100%" → tuvalin tamamı
                "w": w if str(rw).endswith("%") else float(rw),
                "h": h if str(rh).endswith("%") else float(rh),
                "fill": _colour(el.get("fill")),
                "stroke": _colour(el.get("stroke"), None),
                "strokeWidth": _f(el, "stroke-width", 0.0),
            })
        elif t == "line":
            ops.append({
                "op": "line",
                "x1": _f(el, "x1"), "y1": _f(el, "y1"),
                "x2": _f(el, "x2"), "y2": _f(el, "y2"),
                "stroke": _colour(el.get("stroke")),
                "strokeWidth": _f(el, "stroke-width", 1.0),
                "dash": el.get("stroke-dasharray"),
            })
        elif t == "circle":
            ops.append({
                "op": "circle",
                "cx": _f(el, "cx"), "cy": _f(el, "cy"), "r": _f(el, "r"),
                "fill": _colour(el.get("fill")),
                "stroke": _colour(el.get("stroke")),
                "strokeWidth": _f(el, "stroke-width", 1.0),
            })
        elif t == "text":
            ops.append({
                "op": "text",
                "x": _f(el, "x"), "y": _f(el, "y"),
                "size": _f(el, "font-size", 9.0),
                "anchor": el.get("text-anchor", "start"),
                "fill": _colour(el.get("fill")),
                "text": (el.text or ""),
            })

    return {"widthPx": w, "heightPx": h,
            "widthMm": w / PX_PER_MM, "heightMm": h / PX_PER_MM,
            "title": title, "ops": ops}


# ── REPORTLAB ────────────────────────────────────────────────────────────
def draw_reportlab(canvas, doc_ops: dict, x_pt: float, y_pt: float,
                   width_pt: float, skip_background: bool = True) -> float:
    """Emirleri bir reportlab canvas'ına çizer ve KULLANILAN YÜKSEKLİĞİ döner.

    `x_pt`,`y_pt` diyagramın SOL ÜST köşesidir (PDF'in alt-sol origin'inde
    y aşağı doğru sayılmaz; burada dönüşüm yapılır). `width_pt` verilen
    genişliğe ORANTILI ölçeklenir.

    `skip_background=True` beyaz tam-tuval dikdörtgenini atlar: PDF'te beyaz
    bir kutu basmanın anlamı yoktur ve sayfa arkaplanını gizlerse dizgi
    hatalarını da gizler.
    """
    s = width_pt / doc_ops["widthPx"]
    height_pt = doc_ops["heightPx"] * s

    def X(v):
        return x_pt + v * s

    def Y(v):                       # SVG y aşağı · PDF y yukarı
        return y_pt - v * s

    canvas.saveState()
    for o in doc_ops["ops"]:
        if o["op"] == "rect":
            if skip_background and o["w"] >= doc_ops["widthPx"] - 0.01 \
               and o["h"] >= doc_ops["heightPx"] - 0.01:
                continue
            if o["fill"]:
                canvas.setFillColorRGB(*[c / 255.0 for c in o["fill"]])
            if o["stroke"]:
                canvas.setStrokeColorRGB(*[c / 255.0 for c in o["stroke"]])
                canvas.setLineWidth(max(o["strokeWidth"] * s, 0.25))
            canvas.rect(X(o["x"]), Y(o["y"] + o["h"]), o["w"] * s, o["h"] * s,
                        stroke=1 if o["stroke"] else 0,
                        fill=1 if o["fill"] else 0)
        elif o["op"] == "line":
            canvas.setStrokeColorRGB(*[c / 255.0 for c in (o["stroke"] or (0, 0, 0))])
            canvas.setLineWidth(max(o["strokeWidth"] * s, 0.25))
            if o.get("dash"):
                canvas.setDash([float(v) * s for v in re.split(r"[ ,]+", o["dash"])])
            else:
                canvas.setDash()
            canvas.line(X(o["x1"]), Y(o["y1"]), X(o["x2"]), Y(o["y2"]))
        elif o["op"] == "circle":
            canvas.setDash()
            if o["fill"]:
                canvas.setFillColorRGB(*[c / 255.0 for c in o["fill"]])
            canvas.setStrokeColorRGB(*[c / 255.0 for c in (o["stroke"] or (0, 0, 0))])
            canvas.setLineWidth(max(o["strokeWidth"] * s, 0.25))
            canvas.circle(X(o["cx"]), Y(o["cy"]), o["r"] * s,
                          stroke=1, fill=1 if o["fill"] else 0)
        elif o["op"] == "text":
            canvas.setDash()
            canvas.setFillColorRGB(*[c / 255.0 for c in (o["fill"] or (0, 0, 0))])
            canvas.setFont("Times-Roman", o["size"] * s)
            draw = {"start": canvas.drawString,
                    "middle": canvas.drawCentredString,
                    "end": canvas.drawRightString}[o["anchor"]]
            draw(X(o["x"]), Y(o["y"]), o["text"])
    canvas.restoreState()
    return height_pt


# ── PIL (yalnız gözle denetim) ───────────────────────────────────────────
def draw_pil(doc_ops: dict, scale: float = 3.0):
    """Emirleri bir PIL görüntüsüne çizer. ÜRETİM ÇIKTISI DEĞİLDİR."""
    from PIL import Image, ImageDraw, ImageFont
    W = int(doc_ops["widthPx"] * scale)
    H = int(doc_ops["heightPx"] * scale)
    im = Image.new("RGB", (max(W, 1), max(H, 1)), "white")
    dr = ImageDraw.Draw(im)
    try:
        fontpath = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
        have_font = os.path.exists(fontpath)
    except Exception:
        have_font = False

    for o in doc_ops["ops"]:
        if o["op"] == "rect":
            xy = [o["x"] * scale, o["y"] * scale,
                  (o["x"] + o["w"]) * scale, (o["y"] + o["h"]) * scale]
            dr.rectangle(xy, fill=o["fill"], outline=o["stroke"],
                         width=max(int(o["strokeWidth"] * scale), 1)
                         if o["stroke"] else 0)
        elif o["op"] == "line":
            dr.line([o["x1"] * scale, o["y1"] * scale,
                     o["x2"] * scale, o["y2"] * scale],
                    fill=o["stroke"], width=max(int(round(o["strokeWidth"] * scale)), 1))
        elif o["op"] == "circle":
            r = o["r"] * scale
            xy = [o["cx"] * scale - r, o["cy"] * scale - r,
                  o["cx"] * scale + r, o["cy"] * scale + r]
            dr.ellipse(xy, fill=o["fill"], outline=o["stroke"],
                       width=max(int(round(o["strokeWidth"] * scale)), 1))
        elif o["op"] == "text":
            f = None
            if have_font:
                f = ImageFont.truetype(fontpath, max(int(o["size"] * scale), 6))
            anchor = {"start": "ls", "middle": "ms", "end": "rs"}[o["anchor"]]
            dr.text((o["x"] * scale, o["y"] * scale), o["text"], fill=o["fill"],
                    font=f, anchor=anchor if f else None)
    return im


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    ap.add_argument("--check-vocabulary", action="store_true")
    args = ap.parse_args()
    ddir = os.path.join(args.root, "07_ASSETS", "diagrams")
    if not os.path.isdir(ddir):
        print("  · diyagram dizini yok — ATLANDI")
        return 0
    bad, n = [], 0
    for fn in sorted(os.listdir(ddir)):
        if not fn.endswith(".svg"):
            continue
        n += 1
        try:
            parse(os.path.join(ddir, fn))
        except UnknownElement as e:
            bad.append(str(e))
    print("  %d SVG tarandı · sözlük: %s" % (n, ", ".join(sorted(KNOWN_TAGS))))
    if bad:
        for b in bad:
            print("  ✗ %s" % b)
        return 1
    print("  ✅ bütün SVG'ler bilinen sözlükte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
