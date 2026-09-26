#!/usr/bin/env python3
"""
SVG → VEKTÖR ÇEVİRİCİ — The Great Book of World Games
================================================================================
Reads the SVG written by `boards.py` and turns it into drawing operations:

  · `interior.py`  → reportlab · real vector inside the print PDF
  · `qa_visual.py` → PIL · raster preview for inspection

Why our own converter: the diagrams are line drawings in black ink; they must
stay vector so a 0.75 pt line prints at press resolution and survives a 71 %
photocopy — the whole point of the full-size templates at the back.

Supported vocabulary — exactly what `boards.py` writes, nothing else:

    <svg> <title> <rect> <line> <circle> <ellipse> <polygon> <polyline>
    <path d="M/L/C/Z, absolute"> <text font-family font-weight font-style>
    <image> with an embedded PNG (public-domain figures only; drawn as a picture)

`--check-vocabulary` scans every SVG and fails on any other element: an
element that is silently skipped is a board drawn incompletely.

Exit codes: 0 pass · 1 gate red · 2 dependency missing
"""

from __future__ import annotations

import os
import re
import sys
import xml.etree.ElementTree as ET

SVG_NS = "{http://www.w3.org/2000/svg}"
PX_PER_MM = 96.0 / 25.4
KNOWN_TAGS = {"svg", "title", "rect", "line", "circle", "ellipse", "polygon",
              "polyline", "path", "text", "image"}
XLINK = "{http://www.w3.org/1999/xlink}"


class UnknownElement(Exception):
    """An SVG element outside the vocabulary. Never skipped silently."""


def _f(el, name, default=0.0):
    v = el.get(name)
    if v is None:
        return default
    return float(str(v).replace("%", "").replace("px", "").strip())


def _colour(v, default=(0, 0, 0)):
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


def _dash(v):
    if not v:
        return None
    return [float(x) for x in re.split(r"[ ,]+", v.strip()) if x]


def _points(v):
    nums = [float(x) for x in re.split(r"[ ,]+", (v or "").strip()) if x]
    return list(zip(nums[0::2], nums[1::2]))


def _path(d):
    toks = re.findall(r"[MLCZmlcz]|-?\d*\.?\d+(?:e-?\d+)?", d)
    out, i, cmd = [], 0, None
    while i < len(toks):
        t = toks[i]
        if t in "MLCZmlcz":
            cmd = t.upper()
            if cmd == "Z":
                out.append(("Z",))
            i += 1
            continue
        n = {"M": 2, "L": 2, "C": 6}[cmd]
        vals = [float(x) for x in toks[i:i + n]]
        out.append((cmd,) + tuple(vals))
        i += n
        if cmd == "M":
            cmd = "L"
    return out


def parse(path: str) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    if root.tag.replace(SVG_NS, "") != "svg":
        raise UnknownElement("root is not <svg>")
    w = _f(root, "width")
    h = _f(root, "height")
    ops, title = [], ""
    for el in root:
        t = el.tag.replace(SVG_NS, "")
        if t not in KNOWN_TAGS:
            raise UnknownElement("%s: unknown element <%s>" % (os.path.basename(path), t))
        base = {"fill": _colour(el.get("fill"), (0, 0, 0)),
                "stroke": _colour(el.get("stroke"), None),
                "strokeWidth": _f(el, "stroke-width", 1.0),
                "dash": _dash(el.get("stroke-dasharray"))}
        if t == "title":
            title = (el.text or "").strip()
        elif t == "rect":
            rw, rh = el.get("width", "0"), el.get("height", "0")
            ops.append(dict(base, op="rect", x=_f(el, "x"), y=_f(el, "y"),
                            w=w if str(rw).endswith("%") else float(rw),
                            h=h if str(rh).endswith("%") else float(rh),
                            r=_f(el, "rx", 0.0)))
        elif t == "line":
            ops.append(dict(base, op="line", x1=_f(el, "x1"), y1=_f(el, "y1"),
                            x2=_f(el, "x2"), y2=_f(el, "y2"),
                            stroke=_colour(el.get("stroke"))))
        elif t == "circle":
            ops.append(dict(base, op="circle", cx=_f(el, "cx"), cy=_f(el, "cy"),
                            r=_f(el, "r")))
        elif t == "ellipse":
            ops.append(dict(base, op="ellipse", cx=_f(el, "cx"), cy=_f(el, "cy"),
                            rx=_f(el, "rx"), ry=_f(el, "ry")))
        elif t in ("polygon", "polyline"):
            ops.append(dict(base, op="poly", pts=_points(el.get("points")),
                            closed=(t == "polygon")))
        elif t == "path":
            ops.append(dict(base, op="path", d=_path(el.get("d", ""))))
        elif t == "image":
            import base64
            href = el.get(XLINK + "href") or el.get("href") or ""
            if not href.startswith("data:image/png;base64,"):
                raise UnknownElement("%s: <image> must embed PNG data" % os.path.basename(path))
            ops.append({"op": "image", "x": _f(el, "x"), "y": _f(el, "y"), "w": _f(el, "width"),
                        "h": _f(el, "height"), "png": base64.b64decode(href.split(",", 1)[1])})
        elif t == "text":
            ops.append({"op": "text", "x": _f(el, "x"), "y": _f(el, "y"),
                        "size": _f(el, "font-size", 9.0),
                        "anchor": el.get("text-anchor", "start"),
                        "fill": _colour(el.get("fill")),
                        "family": el.get("font-family", "sans"),
                        "weight": el.get("font-weight", "normal"),
                        "style": el.get("font-style", "normal"),
                        "text": (el.text or "")})
    return {"widthPx": w, "heightPx": h, "widthMm": w / PX_PER_MM,
            "heightMm": h / PX_PER_MM, "title": title, "ops": ops}


def _font_for(family: str, weight: str, style: str, fonts: dict) -> str:
    fam = (family or "").lower()
    serif = "serif" in fam and "sans" not in fam
    key = ("serif" if serif else "sans",
           "bold" if weight in ("bold", "700", "semibold", "600") else "normal",
           "italic" if style == "italic" else "normal")
    return fonts.get(key) or fonts.get(("sans", "normal", "normal"))


DEFAULT_FONTS = {
    ("sans", "normal", "normal"): "GBSans", ("sans", "bold", "normal"): "GBSans-B",
    ("sans", "normal", "italic"): "GBSans-I", ("sans", "bold", "italic"): "GBSans-B",
    ("serif", "normal", "normal"): "GBSerif", ("serif", "bold", "normal"): "GBSerif-B",
    ("serif", "normal", "italic"): "GBSerif-I", ("serif", "bold", "italic"): "GBSerif-B",
}


def draw_reportlab(canvas, doc_ops: dict, x_pt: float, y_pt: float, width_pt: float,
                   skip_background: bool = True, font=None, fonts=None) -> float:
    """Draw at (x_pt, y_pt) = TOP-LEFT corner, scaled to `width_pt`.
    Returns the height used. `fonts` maps (family, weight, style) → font name;
    the fonts must be registered (and are embedded)."""
    fonts = fonts or DEFAULT_FONTS
    s = width_pt / doc_ops["widthPx"]
    height_pt = doc_ops["heightPx"] * s

    def X(v):
        return x_pt + v * s

    def Y(v):
        return y_pt - v * s

    def set_stroke(o):
        if o.get("stroke"):
            canvas.setStrokeColorRGB(*[c / 255.0 for c in o["stroke"]])
            canvas.setLineWidth(max(o["strokeWidth"] * s, 0.25))
            if o.get("dash"):
                canvas.setDash([v * s for v in o["dash"]])
            else:
                canvas.setDash()
            return 1
        return 0

    def set_fill(o):
        if o.get("fill"):
            canvas.setFillColorRGB(*[c / 255.0 for c in o["fill"]])
            return 1
        return 0

    canvas.saveState()
    canvas.setLineCap(1)
    canvas.setLineJoin(1)
    for o in doc_ops["ops"]:
        op = o["op"]
        if op == "rect":
            if skip_background and o["w"] >= doc_ops["widthPx"] - 0.01 \
               and o["h"] >= doc_ops["heightPx"] - 0.01:
                continue
            st, fi = set_stroke(o), set_fill(o)
            if o.get("r"):
                canvas.roundRect(X(o["x"]), Y(o["y"] + o["h"]), o["w"] * s, o["h"] * s,
                                 o["r"] * s, stroke=st, fill=fi)
            else:
                canvas.rect(X(o["x"]), Y(o["y"] + o["h"]), o["w"] * s, o["h"] * s,
                            stroke=st, fill=fi)
        elif op == "line":
            if set_stroke(o):
                canvas.line(X(o["x1"]), Y(o["y1"]), X(o["x2"]), Y(o["y2"]))
        elif op in ("circle", "ellipse"):
            st, fi = set_stroke(o), set_fill(o)
            if op == "circle":
                canvas.circle(X(o["cx"]), Y(o["cy"]), o["r"] * s, stroke=st, fill=fi)
            else:
                canvas.ellipse(X(o["cx"] - o["rx"]), Y(o["cy"] + o["ry"]),
                               X(o["cx"] + o["rx"]), Y(o["cy"] - o["ry"]), stroke=st, fill=fi)
        elif op == "poly":
            st, fi = set_stroke(o), set_fill(o)
            p = canvas.beginPath()
            for i, (px, py) in enumerate(o["pts"]):
                (p.moveTo if i == 0 else p.lineTo)(X(px), Y(py))
            if o["closed"]:
                p.close()
            canvas.drawPath(p, stroke=st, fill=fi if o["closed"] else 0)
        elif op == "path":
            st, fi = set_stroke(o), set_fill(o)
            p = canvas.beginPath()
            closed = False
            for c in o["d"]:
                if c[0] == "M":
                    p.moveTo(X(c[1]), Y(c[2]))
                elif c[0] == "L":
                    p.lineTo(X(c[1]), Y(c[2]))
                elif c[0] == "C":
                    p.curveTo(X(c[1]), Y(c[2]), X(c[3]), Y(c[4]), X(c[5]), Y(c[6]))
                elif c[0] == "Z":
                    p.close()
                    closed = True
            canvas.drawPath(p, stroke=st, fill=fi if closed else 0)
        elif op == "image":
            import io
            from reportlab.lib.utils import ImageReader
            canvas.drawImage(ImageReader(io.BytesIO(o["png"])), X(o["x"]), Y(o["y"] + o["h"]),
                             o["w"] * s, o["h"] * s, preserveAspectRatio=True, mask="auto")
        elif op == "text":
            canvas.setDash()
            canvas.setFillColorRGB(*[c / 255.0 for c in (o["fill"] or (0, 0, 0))])
            fname = font or _font_for(o["family"], o["weight"], o["style"], fonts)
            canvas.setFont(fname, o["size"] * s)
            draw = {"start": canvas.drawString, "middle": canvas.drawCentredString,
                    "end": canvas.drawRightString}[o["anchor"]]
            draw(X(o["x"]), Y(o["y"]), o["text"])
    canvas.restoreState()
    return height_pt


def draw_pil(doc_ops: dict, scale: float = 3.0):
    """Raster preview for inspection only (not a production output)."""
    from PIL import Image, ImageDraw, ImageFont
    W = int(doc_ops["widthPx"] * scale)
    H = int(doc_ops["heightPx"] * scale)
    im = Image.new("RGB", (max(W, 1), max(H, 1)), "white")
    dr = ImageDraw.Draw(im)
    fontpath = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    for o in doc_ops["ops"]:
        op = o["op"]
        sw = max(int(round(o.get("strokeWidth", 1) * scale)), 1)
        if op == "rect":
            dr.rectangle([o["x"] * scale, o["y"] * scale, (o["x"] + o["w"]) * scale,
                          (o["y"] + o["h"]) * scale], fill=o.get("fill"),
                         outline=o.get("stroke"), width=sw if o.get("stroke") else 0)
        elif op == "line":
            dr.line([o["x1"] * scale, o["y1"] * scale, o["x2"] * scale, o["y2"] * scale],
                    fill=o["stroke"], width=sw)
        elif op in ("circle", "ellipse"):
            rx = o.get("r", o.get("rx", 0)) * scale
            ry = o.get("r", o.get("ry", 0)) * scale
            dr.ellipse([o["cx"] * scale - rx, o["cy"] * scale - ry, o["cx"] * scale + rx,
                        o["cy"] * scale + ry], fill=o.get("fill"), outline=o.get("stroke"),
                       width=sw if o.get("stroke") else 0)
        elif op == "poly":
            pts = [(x * scale, y * scale) for x, y in o["pts"]]
            if o["closed"]:
                dr.polygon(pts, fill=o.get("fill"), outline=o.get("stroke"))
            else:
                dr.line(pts, fill=o.get("stroke"), width=sw)
        elif op == "path":
            pts = []
            for c in o["d"]:
                if c[0] in "ML":
                    pts.append((c[1] * scale, c[2] * scale))
                elif c[0] == "C":
                    pts.append((c[5] * scale, c[6] * scale))
            if len(pts) > 1:
                dr.line(pts, fill=o.get("stroke") or (0, 0, 0), width=sw)
        elif op == "image":
            import io
            pic = Image.open(io.BytesIO(o["png"])).convert("RGB")
            pic = pic.resize((max(int(o["w"] * scale), 1), max(int(o["h"] * scale), 1)))
            im.paste(pic, (int(o["x"] * scale), int(o["y"] * scale)))
        elif op == "text":
            f = ImageFont.truetype(fontpath, max(int(o["size"] * scale), 6)) \
                if os.path.exists(fontpath) else None
            anchor = {"start": "ls", "middle": "ms", "end": "rs"}[o["anchor"]]
            dr.text((o["x"] * scale, o["y"] * scale), o["text"], fill=o["fill"], font=f,
                    anchor=anchor if f else None)
    return im


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--check-vocabulary", action="store_true")
    args = ap.parse_args()
    bad, n = [], 0
    for sub in ("diagrams", "templates"):
        ddir = os.path.join(args.root, "07_ASSETS", sub)
        if not os.path.isdir(ddir):
            continue
        for fn in sorted(os.listdir(ddir)):
            if not fn.endswith(".svg"):
                continue
            n += 1
            try:
                parse(os.path.join(ddir, fn))
            except UnknownElement as e:
                bad.append(str(e))
    print("  %d SVG files scanned · vocabulary: %s" % (n, ", ".join(sorted(KNOWN_TAGS))))
    if bad:
        for b in bad:
            print("  ✗ %s" % b)
        return 1
    print("  ✅ every SVG is inside the known vocabulary")
    return 0


if __name__ == "__main__":
    sys.exit(main())
