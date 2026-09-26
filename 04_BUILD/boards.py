#!/usr/bin/env python3
"""
BOARDS — the single source of truth for every board, diagram and template
================================================================================
The Great Book of World Games (GBK-02).

Every picture of a board in the book is drawn here, from the game record's
own diagram spec (`book.json → games[].diagrams[]`). The same geometry is
drawn three ways:

  · as an in-entry diagram (`07_ASSETS/diagrams/<id>.svg`, vector, placed by
    interior.py at 100 % so that no label ever falls below 8 pt);
  · as a full-size photocopiable template (`07_ASSETS/templates/<id>.svg`);
  · in the Kindle EPUB and the free companion pack (same SVG files).

WHY ONE ENGINE. The 2026-09-25 audit found seventeen wrong diagrams. Their
common cause was a renderer with a handful of fixed board shapes: a
twenty-circle square ring stood in for three different race tracks, pit
boards had no stores, and graph boards were approximated by grids. A board
that is approximated is a board that cannot be played. Here every board is
built from its own geometry, and every drawing reports what it drew
(points, squares, pieces per side) so that `qa_boards.py` can check the
picture against the numbers the rules print.

Units: millimetres, origin top-left, y downward (SVG convention). The SVG
user unit is the CSS pixel (96 dpi) so that `svg_vector.py` keeps working.

Standard library only.
"""

from __future__ import annotations

import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

PX = 96.0 / 25.4                   # SVG px per mm
PT_PX = 96.0 / 72.0                # SVG px per pt
MM_PT = 72.0 / 25.4

# ── visual language (DIAGRAM_LANGUAGE.md, raised to the 2026 standard) ─────
INK = "#000000"
GREY = {0: "#ffffff", 12: "#e0e0e0", 25: "#bfbfbf", 55: "#737373", 100: "#000000"}
STROKE = 0.75                      # pt — thinnest line allowed in print
LINE = 0.9                         # pt — board lines
FRAME = 1.3                        # pt — board frames
ARROW = 1.15                       # pt
# a capture must read as a different arrow from a plain move at print size: 1.5 pt beside 1.15 pt
# could not be told apart, and the key drew both at 1.15 (seven keys paired "move" and
# "capturing move" under one symbol; found 2026-09-26)
CAPTURE_PT = 1.9                   # pt
LABEL_PT = 8.5                     # every label at 100 % placement
SMALL_PT = 8.0                     # absolute floor (coordinates, route numbers)
FONT_SANS = "sans"
FONT_SERIF = "serif"


def pt(v):
    """points → millimetres."""
    return v / MM_PT


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


class Scene:
    """A flat list of vector operations in millimetres."""

    def __init__(self, w=10.0, h=10.0):
        self.w, self.h = w, h
        self.ops = []
        self.facts = {"points": 0, "squares": 0, "pits": 0, "stations": 0,
                      "pieces": {}, "texts": [], "minTextPt": 99.0,
                      "minStrokePt": 99.0}

    # -- bookkeeping ---------------------------------------------------
    def _stroke(self, w):
        self.facts["minStrokePt"] = min(self.facts["minStrokePt"], w)

    def count_piece(self, side):
        p = self.facts["pieces"]
        p[side] = p.get(side, 0) + 1

    # -- primitives ----------------------------------------------------
    def line(self, x1, y1, x2, y2, w=LINE, dash=None, grey=100, cap="round"):
        self._stroke(w)
        self.ops.append(("line", x1, y1, x2, y2, w, dash, grey, cap))

    def polyline(self, pts, w=LINE, closed=False, fill=None, grey=100, dash=None):
        self._stroke(w)
        self.ops.append(("poly", list(pts), w, closed, fill, grey, dash))

    def circle(self, cx, cy, r, fill=None, w=STROKE, grey=100):
        if w:
            self._stroke(w)
        self.ops.append(("circle", cx, cy, r, fill, w, grey))

    def ellipse(self, cx, cy, rx, ry, fill=None, w=STROKE, grey=100):
        if w:
            self._stroke(w)
        self.ops.append(("ellipse", cx, cy, rx, ry, fill, w, grey))

    def rect(self, x, y, w_, h_, fill=None, w=STROKE, grey=100, r=0.0, dash=None):
        if w:
            self._stroke(w)
        self.ops.append(("rect", x, y, w_, h_, fill, w, grey, r, dash))

    def path(self, d, fill=None, w=STROKE, grey=100, dash=None):
        """`d` is a list of ('M'|'L'|'C'|'Z', coords…) in mm."""
        if w:
            self._stroke(w)
        self.ops.append(("path", d, fill, w, grey, dash))

    def text(self, x, y, s, size=None, anchor="middle", weight="normal",
             style="normal", family=FONT_SANS, grey=100):
        s = str(s)
        if size is None:
            size = LABEL_PT
        self.facts["minTextPt"] = min(self.facts["minTextPt"], size)
        self.facts["texts"].append(s)
        self.ops.append(("text", x, y, s, size, anchor, weight, style, family, grey))

    def image(self, x, y, w_, h_, png_b64):
        """A raster picture (a public-domain figure), embedded as PNG data."""
        self.ops.append(("image", x, y, w_, h_, png_b64))

    # -- composites ----------------------------------------------------
    def arrow(self, x1, y1, x2, y2, w=ARROW, head=2.4, dash=None, gap0=0.0,
              gap1=0.0, grey=100):
        """Straight arrow with a filled head. `gap0/gap1` shorten the ends."""
        ang = math.atan2(y2 - y1, x2 - x1)
        L = math.hypot(x2 - x1, y2 - y1)
        if L < 1e-6:
            return
        ux, uy = math.cos(ang), math.sin(ang)
        sx, sy = x1 + ux * gap0, y1 + uy * gap0
        ex, ey = x2 - ux * gap1, y2 - uy * gap1
        bx, by = ex - ux * head * 0.9, ey - uy * head * 0.9
        self.line(sx, sy, bx, by, w, dash, grey)
        self._head(ex, ey, ang, head, grey)

    def _head(self, ex, ey, ang, head, grey=100):
        a1, a2 = ang + math.pi - 0.42, ang + math.pi + 0.42
        pts = [(ex, ey), (ex + head * math.cos(a1), ey + head * math.sin(a1)),
               (ex + head * math.cos(a2), ey + head * math.sin(a2))]
        self.polyline(pts, w=STROKE, closed=True, fill=grey, grey=grey)

    def curve_arrow(self, x1, y1, x2, y2, bend=0.25, w=ARROW, head=2.4,
                    dash=None, gap0=0.0, gap1=0.0, grey=100):
        """Quadratic-looking arc (drawn as a cubic) bent to the left of travel."""
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        if L < 1e-6:
            return
        nx, ny = -dy / L, dx / L
        cx, cy = mx + nx * L * bend, my + ny * L * bend
        # shorten along the tangents
        def along(px, py, qx, qy, d):
            l = math.hypot(qx - px, qy - py) or 1
            return px + (qx - px) / l * d, py + (qy - py) / l * d
        sx, sy = along(x1, y1, cx, cy, gap0)
        ex, ey = along(x2, y2, cx, cy, gap1)
        ang = math.atan2(ey - cy, ex - cx)
        bx, by = ex - math.cos(ang) * head * 0.9, ey - math.sin(ang) * head * 0.9
        c1 = (sx + (cx - sx) * 2 / 3, sy + (cy - sy) * 2 / 3)
        c2 = (bx + (cx - bx) * 2 / 3, by + (cy - by) * 2 / 3)
        self.path([("M", sx, sy), ("C", c1[0], c1[1], c2[0], c2[1], bx, by)],
                  fill=None, w=w, grey=grey, dash=dash)
        self._head(ex, ey, ang, head, grey)

    # -- composition ---------------------------------------------------
    def bounds(self):
        """Extent of everything drawn, in mm — text measured at its print width."""
        xs, ys = [], []
        for op in self.ops:
            k = op[0]
            if k == "line":
                h = pt(op[5]) / 2.0
                xs += [op[1] - h, op[3] + h, op[1] + h, op[3] - h]
                ys += [op[2] - h, op[4] + h, op[2] + h, op[4] - h]
            elif k == "poly":
                xs += [x for x, _ in op[1]]
                ys += [y for _, y in op[1]]
            elif k == "circle":
                xs += [op[1] - op[3], op[1] + op[3]]
                ys += [op[2] - op[3], op[2] + op[3]]
            elif k == "ellipse":
                xs += [op[1] - op[3], op[1] + op[3]]
                ys += [op[2] - op[4], op[2] + op[4]]
            elif k in ("rect", "image"):
                xs += [op[1], op[1] + op[3]]
                ys += [op[2], op[2] + op[4]]
            elif k == "path":
                for c in op[1]:
                    xs += list(c[1::2])
                    ys += list(c[2::2])
            elif k == "text":
                _, x, y, t, size, anchor, weight, style, fam, _g = op
                tw = text_width(t, size, weight, fam)
                x0 = {"start": x, "middle": x - tw / 2.0, "end": x - tw}.get(anchor, x - tw / 2.0)
                xs += [x0, x0 + tw]
                ys += [y - pt(size) * 0.78, y + pt(size) * 0.25]
        if not xs:
            return 0.0, 0.0, self.w, self.h
        return min(xs), min(ys), max(xs), max(ys)

    def fit_to_content(self, pad=0.4, tol=0.05):
        """Grow the canvas (and shift the drawing) when anything spills past its edge.

        A label placed near an edge at book size can outgrow the canvas at large-print size
        (2× labels); the SVG does not clip, so the overflow printed into the margin."""
        x0, y0, x1, y1 = self.bounds()
        dx = (pad - x0) if x0 < -tol else 0.0
        dy = (pad - y0) if y0 < -tol else 0.0
        gw = (x1 + pad - self.w) if x1 > self.w + tol else 0.0
        gh = (y1 + pad - self.h) if y1 > self.h + tol else 0.0
        if not (dx or dy or gw or gh):
            return False
        ops, self.ops = self.ops, []
        tmp = Scene(self.w, self.h)
        tmp.ops = ops
        self.place(tmp, dx, dy)
        self.w += dx + gw
        self.h += dy + gh
        return True

    def place(self, other, dx, dy, scale=1.0):
        """Copy another scene's ops, translated (and scaled)."""
        s = scale
        for op in other.ops:
            k = op[0]
            if k == "line":
                _, x1, y1, x2, y2, w, dash, grey, cap = op
                self.ops.append(("line", dx + x1 * s, dy + y1 * s, dx + x2 * s,
                                 dy + y2 * s, w, dash, grey, cap))
            elif k == "poly":
                _, pts, w, closed, fill, grey, dash = op
                self.ops.append(("poly", [(dx + x * s, dy + y * s) for x, y in pts],
                                 w, closed, fill, grey, dash))
            elif k == "circle":
                _, cx, cy, r, fill, w, grey = op
                self.ops.append(("circle", dx + cx * s, dy + cy * s, r * s, fill, w, grey))
            elif k == "ellipse":
                _, cx, cy, rx, ry, fill, w, grey = op
                self.ops.append(("ellipse", dx + cx * s, dy + cy * s, rx * s, ry * s,
                                 fill, w, grey))
            elif k == "rect":
                _, x, y, w_, h_, fill, w, grey, r, dash = op
                self.ops.append(("rect", dx + x * s, dy + y * s, w_ * s, h_ * s,
                                 fill, w, grey, r * s, dash))
            elif k == "path":
                _, d, fill, w, grey, dash = op
                nd = []
                for c in d:
                    if c[0] == "Z":
                        nd.append(("Z",))
                    else:
                        vals = c[1:]
                        nd.append((c[0],) + tuple(
                            (dx + v * s) if i % 2 == 0 else (dy + v * s)
                            for i, v in enumerate(vals)))
                self.ops.append(("path", nd, fill, w, grey, dash))
            elif k == "text":
                _, x, y, t, size, anchor, weight, style, fam, grey = op
                self.ops.append(("text", dx + x * s, dy + y * s, t, size * s,
                                 anchor, weight, style, fam, grey))
            elif k == "image":
                _, x, y, w_, h_, data = op
                self.ops.append(("image", dx + x * s, dy + y * s, w_ * s, h_ * s, data))
        f = other.facts
        for key in ("points", "squares", "pits", "stations"):
            self.facts[key] += f[key]
        for side, n in f["pieces"].items():
            self.facts["pieces"][side] = self.facts["pieces"].get(side, 0) + n
        self.facts["texts"] += f["texts"]
        self.facts["minTextPt"] = min(self.facts["minTextPt"], f["minTextPt"] * s)
        self.facts["minStrokePt"] = min(self.facts["minStrokePt"], f["minStrokePt"])

    # -- output --------------------------------------------------------
    def svg(self, title="", family_map=None):
        fam = family_map or {FONT_SANS: "Source Sans 3, Helvetica, Arial, sans-serif",
                             FONT_SERIF: "Source Serif 4, Georgia, serif"}
        W, H = self.w * PX, self.h * PX
        out = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
               'width="%.2f" height="%.2f" viewBox="0 0 %.2f %.2f">' % (W, H, W, H),
               "<title>%s</title>" % esc(title),
               '<rect x="0" y="0" width="%.2f" height="%.2f" fill="#ffffff"/>' % (W, H)]
        P = lambda v: v * PX  # noqa: E731

        def stroke_attrs(w, grey, dash=None):
            if not w:
                return 'stroke="none"'
            a = 'stroke="%s" stroke-width="%.3f"' % (GREY.get(grey, INK), w * PT_PX)
            if dash:
                a += ' stroke-dasharray="%s"' % ",".join("%.2f" % (v * PX) for v in dash)
            return a

        def fill_attr(fill):
            return 'fill="%s"' % (GREY[fill] if fill is not None else "none")

        for op in self.ops:
            k = op[0]
            if k == "line":
                _, x1, y1, x2, y2, w, dash, grey, cap = op
                out.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" %s '
                           'stroke-linecap="%s"/>'
                           % (P(x1), P(y1), P(x2), P(y2), stroke_attrs(w, grey, dash), cap))
            elif k == "poly":
                _, pts, w, closed, fill, grey, dash = op
                tag = "polygon" if closed else "polyline"
                out.append('<%s points="%s" %s %s stroke-linejoin="round"/>'
                           % (tag, " ".join("%.2f,%.2f" % (P(x), P(y)) for x, y in pts),
                              fill_attr(fill), stroke_attrs(w, grey, dash)))
            elif k == "circle":
                _, cx, cy, r, fill, w, grey = op
                out.append('<circle cx="%.2f" cy="%.2f" r="%.2f" %s %s/>'
                           % (P(cx), P(cy), P(r), fill_attr(fill), stroke_attrs(w, grey)))
            elif k == "ellipse":
                _, cx, cy, rx, ry, fill, w, grey = op
                out.append('<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" %s %s/>'
                           % (P(cx), P(cy), P(rx), P(ry), fill_attr(fill),
                              stroke_attrs(w, grey)))
            elif k == "rect":
                _, x, y, w_, h_, fill, w, grey, r, dash = op
                rr = ' rx="%.2f" ry="%.2f"' % (P(r), P(r)) if r else ""
                out.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"%s %s %s/>'
                           % (P(x), P(y), P(w_), P(h_), rr, fill_attr(fill),
                              stroke_attrs(w, grey, dash)))
            elif k == "path":
                _, d, fill, w, grey, dash = op
                parts = []
                for c in d:
                    if c[0] == "Z":
                        parts.append("Z")
                    else:
                        parts.append(c[0] + " " + " ".join("%.2f" % P(v) for v in c[1:]))
                out.append('<path d="%s" %s %s stroke-linejoin="round" stroke-linecap="round"/>'
                           % (" ".join(parts), fill_attr(fill), stroke_attrs(w, grey, dash)))
            elif k == "text":
                _, x, y, t, size, anchor, weight, style, family, grey = op
                out.append('<text x="%.2f" y="%.2f" font-family="%s" font-size="%.2f" '
                           'font-weight="%s" font-style="%s" text-anchor="%s" fill="%s">%s</text>'
                           % (P(x), P(y), esc(fam.get(family, family)), size * PT_PX,
                              weight, style, anchor, GREY.get(grey, INK), esc(smart(t))))
            elif k == "image":
                _, x, y, w_, h_, data = op
                out.append('<image x="%.2f" y="%.2f" width="%.2f" height="%.2f" '
                           'preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,%s"/>'
                           % (P(x), P(y), P(w_), P(h_), data))
        out.append("</svg>")
        return "\n".join(out) + "\n"


def smart(t):
    """Typographic quotes for labels (straight apostrophes stay in data)."""
    try:
        import typo
        return typo.smart(t)
    except Exception:           # pragma: no cover — typo is always present in the build
        return t


_FONTS_READY = None
PRINT_FONTS = {"GBSans": "SourceSans3-Regular.ttf", "GBSans-B": "SourceSans3-Bold.ttf",
               "GBSans-SB": "SourceSans3-Semibold.ttf", "GBSans-I": "SourceSans3-It.ttf",
               "GBSerif": "SourceSerif4-Regular.ttf", "GBSerif-B": "SourceSerif4-Bold.ttf",
               "GBSerif-I": "SourceSerif4-It.ttf"}


def _ensure_fonts():
    """Register the fonts the diagrams are printed in, once. Without them every measurement
    fell back to an average-width guess — after ReportLab searched the disk for an unknown
    font on every single call."""
    global _FONTS_READY
    if _FONTS_READY is None:
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            fdir = os.path.join(ROOT, "07_ASSETS", "fonts")
            for name, fn in PRINT_FONTS.items():
                if name not in pdfmetrics.getRegisteredFontNames():
                    pdfmetrics.registerFont(TTFont(name, os.path.join(fdir, fn)))
            _FONTS_READY = True
        except Exception:  # noqa: BLE001
            _FONTS_READY = False
    return _FONTS_READY


def text_width(s, size, weight="normal", family=FONT_SANS):
    """Advance width in mm (used for layout inside diagrams), in the print font.

    Falls back to a conservative average of 0.52 em only when the fonts are missing."""
    if _ensure_fonts():
        from reportlab.pdfbase.pdfmetrics import stringWidth
        return stringWidth(smart(s), font_name(family, weight, "normal"), size) / MM_PT
    return len(s) * size * 0.52 / MM_PT


def font_name(family, weight, style):
    if family == FONT_SERIF:
        if weight == "bold":
            return "GBSerif-B"
        return "GBSerif-I" if style == "italic" else "GBSerif"
    if weight == "bold":
        return "GBSans-B"
    if weight == "semibold":
        return "GBSans-SB"
    return "GBSans-I" if style == "italic" else "GBSans"


# ── pieces and marks ─────────────────────────────────────────────────────
SIDE_FILL = {"black": 100, "white": 0, "red": 0, "blue": 100, "grey": 25,
             "green": 25, "yellow": 55, "neutral": 0}


def piece(sc, x, y, r, side="white", kind="piece", label=None, captured=False,
          count=True, label_pt=None):
    """One playing piece. Black = filled, White = open; kings get an inner ring;
    labelled pieces (chess family) carry a letter in contrast ink."""
    fill = SIDE_FILL.get(side, 0)
    if kind in ("seed", "bean"):
        sc.circle(x, y, r * 0.55, fill=55, w=STROKE)
        if count:
            sc.count_piece(side)
        return
    if kind == "square":
        sc.rect(x - r, y - r, 2 * r, 2 * r, fill=fill, w=STROKE)
    elif kind == "triangle":
        pts = [(x, y - r * 1.1), (x + r * 1.0, y + r * 0.75), (x - r * 1.0, y + r * 0.75)]
        sc.polyline(pts, closed=True, fill=fill, w=STROKE)
    else:
        sc.circle(x, y, r, fill=fill, w=STROKE)
    if kind in ("king", "general", "special", "leader", "tiger", "fox", "hare",
                "leopard", "hyena"):
        sc.circle(x, y, r * 0.55, fill=None, w=STROKE, grey=0 if fill == 100 else 100)
        if fill != 100:
            sc.circle(x, y, r * 0.22, fill=100, w=0)
    if side == "red" and not label:
        # red is drawn open with a dotted inner ring so it never reads as white
        sc.circle(x, y, r * 0.62, fill=None, w=STROKE, grey=55)
    if label:
        if label_pt:
            size = label_pt
        elif LABEL_PT > 8.5:
            # large print: a letter forced to the full 16 pt overflowed a small piece (the Tablut
            # king in the four-panel capture diagram; 2026-09-26). It shrinks to its piece, never
            # below 1.5× the book size; bigger pieces keep 16 pt.
            size = max(0.75 * SMALL_PT, min(SMALL_PT, r * MM_PT * 1.05))
        else:
            size = max(SMALL_PT, min(9.0, r * MM_PT * 1.05))
        sc.text(x, y + pt(size) * 0.35, label, size=size, weight="bold",
                grey=0 if fill >= 55 else 100)
    if captured:
        k = r * 0.95
        sc.line(x - k, y - k, x + k, y + k, w=1.3, grey=0 if fill == 100 else 100)
        sc.line(x - k, y + k, x + k, y - k, w=1.3, grey=0 if fill == 100 else 100)
    if count:
        sc.count_piece(side)


def rosette(sc, x, y, r):
    sc.circle(x, y, r, fill=None, w=STROKE)
    for i in range(8):
        a = i * math.pi / 4
        px, py = x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.55
        sc.circle(px, py, r * 0.28, fill=None, w=STROKE)
    sc.circle(x, y, r * 0.22, fill=100, w=0)


def mark(sc, x, y, r, kind):
    """Board marks: special squares, starts, safe points."""
    if kind == "rosette":
        rosette(sc, x, y, r)
    elif kind in ("castle", "safe"):
        # a crossed square: the traditional mark of a safe square
        k = r * 0.75
        sc.line(x - k, y - k, x + k, y + k, w=STROKE)
        sc.line(x - k, y + k, x + k, y - k, w=STROKE)
    elif kind == "throne":
        sc.rect(x - r * 0.8, y - r * 0.8, r * 1.6, r * 1.6, fill=25, w=STROKE)
    elif kind == "corner":
        sc.rect(x - r * 0.8, y - r * 0.8, r * 1.6, r * 1.6, fill=25, w=STROKE)
    elif kind == "star":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r * (0.9 if i % 2 == 0 else 0.38)
            pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
        sc.polyline(pts, closed=True, fill=100, w=STROKE)
    elif kind == "x" or kind == "captured":
        k = r * 0.7
        sc.line(x - k, y - k, x + k, y + k, w=1.3)
        sc.line(x - k, y + k, x + k, y - k, w=1.3)
    elif kind == "dot":
        sc.circle(x, y, r * 0.3, fill=100, w=0)
    elif kind == "start":
        pts = [(x - r * 0.6, y - r * 0.7), (x + r * 0.8, y), (x - r * 0.6, y + r * 0.7)]
        sc.polyline(pts, closed=True, fill=100, w=STROKE)
    elif kind == "home":
        sc.circle(x, y, r * 0.8, fill=None, w=STROKE)
        sc.circle(x, y, r * 0.45, fill=100, w=0)
    elif kind == "water":
        for k in (-0.35, 0.05, 0.45):
            sc.path([("M", x - r * 0.7, y + r * k),
                     ("C", x - r * 0.35, y + r * (k - 0.25), x, y + r * (k + 0.25),
                      x + r * 0.7, y + r * k)], w=STROKE)
    elif kind == "ring":
        # Only the key reaches this branch: the board draws its rings in _overlay, bold and round
        # a point or a piece. A thin circle here was the White piece's own symbol in the same key
        # (Dara, Go, Gebeta, Shogi, Xiangqi; seen on the printed page 2026-09-26), so the sample
        # shows what the board shows: the bold ring, round a small grey point.
        sc.circle(x, y, r * 0.8, fill=None, w=1.2)
        sc.circle(x, y, r * 0.3, fill=55, w=0)
    else:
        sc.circle(x, y, r * 0.3, fill=55, w=0)


LEGEND_NAMES = {
    "black": "Black", "white": "White", "red": "Red", "blue": "Blue",
    "green": "Green", "yellow": "Yellow",
}


def legend(entries, width, cols=None, size=None):
    """Legend block. `entries` = [(drawer, label)], drawer(sc, x, y, r)."""
    if size is None:
        size = LABEL_PT
    if not entries:
        return Scene(width, 0)
    r = 1.9 * size / 8.5
    lead = r * 1.3 + 0.5            # the arrow sample reaches 1.3 r left of its anchor
    widths = [lead + r + 1.8 + text_width(lbl, size) for _, lbl in entries]
    if cols is None:
        cols = max(1, min(len(entries), int((width + 4) // (max(widths) + 5))))
    rows = int(math.ceil(len(entries) / cols))
    lh = pt(size) * 1.75
    sc = Scene(width, rows * lh + 1.0)
    colw = width / cols
    for i, (drawer, lbl) in enumerate(entries):
        c, rr = i % cols, i // cols
        x = c * colw + lead
        y = rr * lh + lh * 0.55
        drawer(sc, x, y, r)
        sc.text(x + r + 1.8, y + pt(size) * 0.34, lbl, size=size, anchor="start")
    return sc


# ── helpers for specs ────────────────────────────────────────────────────
def coord(c):
    """'e5' → (col, row) zero-based; row 0 = bottom. Also 'aa12' style."""
    m = re.match(r"^([a-z]+)(\d+)$", str(c).strip().lower())
    if not m:
        return None
    letters, num = m.groups()
    col = 0
    for ch in letters:
        col = col * 26 + (ord(ch) - 96)
    return col - 1, int(num) - 1


def piece_drawer(side, kind="piece", label=None):
    return lambda sc, x, y, r: piece(sc, x, y, r, side, kind, label, count=False)


def mark_drawer(kind):
    return lambda sc, x, y, r: mark(sc, x, y, r * 1.2, kind)


def arrow_drawer(style="move"):
    # the key draws each arrow as the board draws it: weight, dash and grey (see _overlay)
    def d(sc, x, y, r):
        dash = (1.2, 0.9) if style in ("route", "alternate") else None
        sc.arrow(x - r * 1.3, y, x + r * 1.5, y, w=CAPTURE_PT if style == "capture" else ARROW,
                 head=1.9, dash=dash, grey=55 if style == "route" else 100)
    return d


def _key_symbol(drawer):
    """What a key entry draws, as data: two entries that draw the same thing cannot be told apart."""
    sc = Scene(20.0, 20.0)
    drawer(sc, 10.0, 10.0, 2.0)
    return repr([tuple(round(v, 3) if isinstance(v, float) else v for v in op) for op in sc.ops])


def key_clashes(entries):
    """Pairs of different labels that the key draws with the same symbol."""
    seen, out = {}, []
    for d, lbl in entries:
        k = _key_symbol(d)
        if k in seen and seen[k] != lbl:
            out.append([seen[k], lbl])
        seen.setdefault(k, lbl)
    return out


def captured_drawer():
    return lambda sc, x, y, r: (piece(sc, x, y, r, "white", count=False),
                                mark(sc, x, y, r * 1.1, "x"))


# ═════════════════════════════════════════════════════════════════════════
# BOARD RENDERERS
# Each returns (scene, locate) where locate(key) → (x, y, r) in mm, r being
# the natural piece radius at that place. Overlays (pieces, marks, arrows,
# labels) are drawn afterwards by `render_spec` through `locate`.
# ═════════════════════════════════════════════════════════════════════════

def board_grid(b, width):
    cols, rows = int(b["cols"]), int(b["rows"])
    mode = b.get("mode", "cells")
    n_x = cols if mode == "cells" else cols - 1
    n_y = rows if mode == "cells" else rows - 1
    river = b.get("river")              # {"afterRow": 5} → gap between rank 5 and 6
    gap_units = 1 if river else 0
    coords = b.get("coords", True)
    lab = pt(SMALL_PT) + 1.6 if coords else 0.0
    pad = 2.2
    step = b.get("stepMm") or min(14.0, (width - 2 * pad - lab) / max(n_x, 1))
    if mode == "points":
        # a piece on an edge point must not be clipped: pad ≥ piece radius
        pad = max(pad, step * 0.36 + 0.8)
        step = b.get("stepMm") or min(14.0, (width - 2 * pad - lab) / max(n_x, 1))
        pad = max(2.2, step * 0.36 + 0.8)
    W = pad * 2 + lab + n_x * step
    H = pad * 2 + lab + (n_y + gap_units * (0 if mode == "cells" else 0)) * step
    sc = Scene(W, H)
    x0 = pad + lab
    y0 = pad
    omit = set(b.get("omit") or [])

    def rank_y(r):          # r zero-based from bottom
        if mode == "cells":
            return y0 + (rows - 1 - r) * step + step / 2
        return y0 + (rows - 1 - r) * step

    def file_x(c):
        if mode == "cells":
            return x0 + c * step + step / 2
        return x0 + c * step

    if mode == "cells":
        checker = b.get("checkered")
        shaded = set(b.get("shade") or [])
        for c in range(cols):
            for r in range(rows):
                key = "%s%d" % (chr(97 + c), r + 1)
                if key in omit:
                    continue
                x, y = x0 + c * step, y0 + (rows - 1 - r) * step
                shade = None
                if checker and (c + r) % 2 == (0 if checker == "a1dark" else 1):
                    shade = 25
                if key in shaded:
                    # the print palette is 0/25/55/100 %: a 12 % tint can vanish on B&W stock
                    shade = 55 if checker else 25
                sc.rect(x, y, step, step, fill=shade, w=LINE)
                sc.facts["squares"] += 1
        # thick frame round the whole board if rectangular
        if not omit:
            sc.rect(x0, y0, cols * step, rows * step, fill=None, w=FRAME)
        # Burmese boards: the two long diagonals, corner to corner
        if b.get("cornerDiagonals"):
            sc.line(x0, y0, x0 + cols * step, y0 + rows * step, w=LINE)
            sc.line(x0 + cols * step, y0, x0, y0 + rows * step, w=LINE)
    else:
        pts = [(c, r) for c in range(cols) for r in range(rows)
               if "%s%d" % (chr(97 + c), r + 1) not in omit]
        ptset = set(pts)
        riv = river.get("afterRow") if river else None
        # orthogonal lines between neighbouring points
        for c, r in pts:
            if (c + 1, r) in ptset:
                sc.line(file_x(c), rank_y(r), file_x(c + 1), rank_y(r), w=LINE)
            if (c, r + 1) in ptset:
                if riv is not None and r == riv - 1 and 0 < c < cols - 1:
                    pass            # the river: no inner verticals across it
                else:
                    sc.line(file_x(c), rank_y(r), file_x(c), rank_y(r + 1), w=LINE)
        diag = b.get("diagonals", "none")
        if diag in ("all", "alquerque", "fanorona"):
            for c, r in pts:
                if (c + 1, r + 1) in ptset and (c + 1, r) in ptset and (c, r + 1) in ptset:
                    if diag == "all":
                        sc.line(file_x(c), rank_y(r), file_x(c + 1), rank_y(r + 1), w=LINE)
                        sc.line(file_x(c + 1), rank_y(r), file_x(c), rank_y(r + 1), w=LINE)
                    elif (c + r) % 2 == 0:
                        sc.line(file_x(c), rank_y(r), file_x(c + 1), rank_y(r + 1), w=LINE)
                    else:
                        sc.line(file_x(c + 1), rank_y(r), file_x(c), rank_y(r + 1), w=LINE)
        sc.facts["points"] += len(pts)
        for c, r in pts:
            sc.circle(file_x(c), rank_y(r), 0.55, fill=100, w=0)
        if riv is not None and b.get("riverLabel"):
            ymid = (rank_y(riv - 1) + rank_y(riv)) / 2
            sc.text((file_x(0) + file_x(cols - 1)) / 2, ymid + pt(LABEL_PT) * 0.35,
                    b["riverLabel"], size=LABEL_PT, style="italic")
    for ln in b.get("extraLines") or []:
        a, z = coord(ln[0]), coord(ln[1])
        if a and z:
            sc.line(file_x(a[0]), rank_y(a[1]), file_x(z[0]), rank_y(z[1]), w=LINE)
    rad = min(step * (0.34 if mode == "cells" else 0.36), b.get("pieceMaxMm", 99.0))
    if coords:
        if mode == "cells":
            ly = y0 + rows * step + lab - 0.3
        else:
            # below the bottom row of points AND clear of any piece standing there
            ly = y0 + (rows - 1) * step + rad + pt(SMALL_PT) * 0.95 + 0.4
            sc.h = max(sc.h, ly + 1.2)
        for c in range(cols):
            sc.text(file_x(c), ly, chr(97 + c), size=SMALL_PT, grey=55)
        for r in range(rows):
            lx = pad + lab * 0.45 if mode == "cells" else x0 - rad - 1.4
            sc.text(lx, rank_y(r) + pt(SMALL_PT) * 0.35, str(r + 1),
                    size=SMALL_PT, grey=55, anchor="middle" if mode == "cells" else "end")

    def locate(key):
        cr = coord(key)
        if cr is None:
            return None
        return file_x(cr[0]), rank_y(cr[1]), rad
    return sc, locate


def board_mancala(b, width):
    rows = int(b.get("rows", 2))
    n = int(b.get("pits", 6))
    stores = b.get("stores", "both")
    has_st = stores not in ("none", None, False)
    pad = 2.0
    numlab = pt(SMALL_PT) + 1.4
    avail = width - 2 * pad
    units = n + (2 * 1.25 if has_st else 0)
    d = min(15.0, avail / units)             # pit pitch
    r = d * 0.40
    bw = n * d + (2 * 1.25 * d if has_st else 0)
    bh = rows * d + d * 0.25
    W = bw + 2 * pad
    arrow_h = 5.0 if b.get("direction") else 0.0
    H = bh + 2 * pad + 2 * numlab + arrow_h
    sc = Scene(W, H)
    bx, by = pad, pad + numlab
    sc.rect(bx, by, bw, bh, fill=None, w=FRAME, r=d * 0.45)
    px0 = bx + (1.25 * d if has_st else 0)
    counts = b.get("counts") or {}
    hl = set(b.get("highlight") or [])
    square = set(b.get("squarePits") or [])
    order = (["N", "S"] if rows == 2 else ["NO", "NI", "SI", "SO"])
    centres = {}
    for ri, rk in enumerate(order):
        cy = by + d * 0.125 + ri * d + d / 2
        for i in range(n):
            cx = px0 + i * d + d / 2
            # numbering from the owner's left: South left→right, North right→left
            num = (i + 1) if rk.startswith("S") else (n - i)
            key = "%s%d" % (rk, num)
            centres[key] = (cx, cy)
            if key in square:
                # a square pit: the Bao nyumba
                sc.rect(cx - r, cy - r, 2 * r, 2 * r, fill=25 if key in hl else None,
                        w=1.4 if key in hl else LINE)
            else:
                sc.circle(cx, cy, r, fill=25 if key in hl else None,
                          w=1.4 if key in hl else LINE)
            sc.facts["pits"] += 1
            v = counts.get(key)
            if v not in (None, "") and not (v == 0 and not b.get("showZero", True)):
                cp = count_pt()
                sc.text(cx, cy + pt(cp) * 0.36, str(v), size=cp,
                        weight="bold" if key in hl else "normal", family=FONT_SANS)
            if b.get("pitNumbers", True):
                if rk in ("N", "NO"):
                    sc.text(cx, by - 0.9, str(num), size=SMALL_PT, grey=55)
                if rk in ("S", "SO"):
                    sc.text(cx, by + bh + numlab - 0.4, str(num), size=SMALL_PT, grey=55)
    if has_st:
        # by default South's store is at South's right (anticlockwise games);
        # "southStore": "left" puts it at South's left (congkak: each house on its owner's left)
        left_first = (("SS", bx + 0.625 * d), ("NS", bx + bw - 0.625 * d))
        right_first = (("NS", bx + 0.625 * d), ("SS", bx + bw - 0.625 * d))
        for key, cx in (left_first if b.get("southStore") == "left" else right_first):
            cy = by + bh / 2
            sc.ellipse(cx, cy, d * 0.42, bh / 2 - d * 0.22, fill=25 if key in hl else None,
                       w=LINE)
            centres[key] = (cx, cy)
            v = counts.get(key)
            if v not in (None, ""):
                cp = count_pt()
                sc.text(cx, cy + pt(cp) * 0.36, str(v), size=cp, weight="bold")
    if b.get("direction"):
        # sowing direction shown as a loop outside the board
        yb = by + bh + numlab + 2.8
        x1, x2 = px0 + d * 0.5, px0 + n * d - d * 0.5
        if b["direction"] == "anticlockwise":
            sc.arrow(x1, yb, x2, yb, w=ARROW, head=2.2)
        else:
            sc.arrow(x2, yb, x1, yb, w=ARROW, head=2.2)
        lbl = b.get("directionLabel") or ("sowing runs anticlockwise"
                                           if b["direction"] == "anticlockwise"
                                           else "sowing runs clockwise")
        sc.h = max(sc.h, yb + pt(LABEL_PT) * 1.6)
        sc.text((x1 + x2) / 2, yb + pt(LABEL_PT) * 1.3, lbl, size=LABEL_PT, style="italic")
    rr = r * 0.8

    def locate(key):
        c = centres.get(key)
        if not c:
            return None
        return c[0], c[1], rr
    locate.board = "mancala"
    locate.rows = rows
    locate.pit_r = r
    locate.centre_y = by + bh / 2
    return sc, locate


def _lattice_axes(nodes, axes):
    """{"files": [...], "ranks": [...]} → {"x": [[x, file]], "y": [[y, rank]]}, read off the node
    ids (file letter + rank number). A file or rank is labelled only where every node carrying it
    lies on one line; the positions come from the nodes, so a label cannot drift from its points."""
    fx, ry = {}, {}
    for k, (x, y) in nodes.items():
        m = re.match(r"^([a-z])(\d+)$", k)
        if m:
            fx.setdefault(m.group(1), set()).add(round(x, 4))
            ry.setdefault(int(m.group(2)), set()).add(round(y, 4))
    return {"x": [[next(iter(fx[f])), f] for f in axes.get("files", []) if len(fx.get(f, ())) == 1],
            "y": [[next(iter(ry[int(r)])), str(r)] for r in axes.get("ranks", [])
                  if len(ry.get(int(r), ())) == 1]}


def board_graph(b, width):
    nodes = b["nodes"]
    edges = b.get("edges", [])
    aspect = b.get("aspect")
    xs = [v[0] for v in nodes.values()]
    ys = [v[1] for v in nodes.values()]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    spanx = (maxx - minx) or 1.0
    spany = (maxy - miny) or 1.0
    axes = b.get("axes")
    if axes and ("files" in axes or "ranks" in axes):
        axes = _lattice_axes(nodes, axes)
    lab = (pt(SMALL_PT) + 1.6) if axes else 0.0
    span = b.get("spanMm") or min(width - 12.0 - lab, 150.0)
    sx = span / spanx
    sy = sx if aspect is None else sx * aspect
    # piece radius: a fraction of the shortest line, never larger than 3.4 mm
    def raw(k):
        x, y = nodes[k]
        return (x - minx) * sx, (y - miny) * sy
    dmin0 = min((math.hypot(raw(e[0])[0] - raw(e[1])[0], raw(e[0])[1] - raw(e[1])[1])
                 for e in edges if e[0] in nodes and e[1] in nodes), default=8.0)
    rad = max(1.8, min(b.get("pieceMaxMm", 3.4), dmin0 * 0.34))
    pad = rad + 1.2
    W = spanx * sx + 2 * pad + lab
    H = spany * sy + 2 * pad + lab
    sc = Scene(W, H)

    def P(k):
        x, y = nodes[k]
        return lab + pad + (x - minx) * sx, pad + (y - miny) * sy
    for e in edges:
        if e[0] in nodes and e[1] in nodes:
            a, z = P(e[0]), P(e[1])
            if len(e) > 2 and e[2] == "curve":
                sc.path([("M", a[0], a[1]), ("C", a[0], (a[1] + z[1]) / 2, z[0],
                                             (a[1] + z[1]) / 2, z[0], z[1])], w=LINE)
            else:
                sc.line(a[0], a[1], z[0], z[1], w=LINE)
    for k in nodes:
        x, y = P(k)
        sc.circle(x, y, 0.75, fill=100, w=0)
    sc.facts["points"] += len(nodes)
    if b.get("pointLabels"):
        for k, lbl in b["pointLabels"].items():
            if k in nodes:
                x, y = P(k)
                sc.text(x + rad + 1.2, y - rad - 0.4, lbl, size=SMALL_PT, grey=55,
                        anchor="start")
    if axes:
        # file letters under the board and rank numbers to its left, clear of edge pieces
        by = pad + spany * sy + rad + pt(SMALL_PT) * 0.95 + 0.4
        for xn, lbl in axes.get("x", []):
            sc.text(lab + pad + (xn - minx) * sx, by, lbl, size=SMALL_PT, grey=55)
        for yn, lbl in axes.get("y", []):
            sc.text(lab + pad - rad - 1.4, pad + (yn - miny) * sy + pt(SMALL_PT) * 0.35, lbl,
                    size=SMALL_PT, grey=55, anchor="end")
        sc.h = max(sc.h, by + 1.2)

    def locate(key):
        if key not in nodes:
            return None
        x, y = P(key)
        return x, y, rad
    return sc, locate


def board_track(b, width):
    st = b["stations"]
    xs = [s["xy"][0] for s in st]
    ys = [s["xy"][1] for s in st]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    spanx = (maxx - minx) or 1.0
    spany = (maxy - miny) or 1.0
    cell = b.get("cells", False)
    span = b.get("spanMm") or min(width - 2 * 5.0, 160.0)
    ids = {s["id"]: s for s in st}

    def lay(span_):
        sx_ = span_ / spanx
        sy_ = sx_ * b.get("aspect", 1.0)
        # station size from nearest-neighbour spacing
        pts = [((s["xy"][0] - minx) * sx_, (s["xy"][1] - miny) * sy_) for s in st]
        nn = []
        for i, (x, y) in enumerate(pts):
            dm = min((math.hypot(x - u, y - v) for j, (u, v) in enumerate(pts) if j != i),
                     default=10.0)
            nn.append(dm)
        unit = sorted(nn)[len(nn) // 2] if nn else 8.0
        # a station size given in the spec grows with the span (large print), like everything else
        size_ = (b["stationMm"] * span_ / base) if b.get("stationMm") else unit * (0.92 if cell else 0.5)
        # the margin must hold the largest station drawn at the edge (big stations at full size)
        reach = size_ / 2 * (1.415 if cell else 1.25)
        pad_ = max(5.0, reach + 1.2)
        return sx_, sy_, size_, pad_, spanx * sx_ + 2 * pad_

    # large print: a track kept at its book span drew 16 pt station numbers in 3 mm stations
    # (Puluc, Zohn; 2026-09-26). It grows with its labels, as board_prims does — but the whole
    # drawing, margins included, stays within the width it is given (a full-size template is
    # already as wide as the page).
    base = span
    grow = LABEL_PT > 8.5 and bool(b.get("spanMm"))
    if grow:
        span = max(span, min(span * LABEL_PT / 8.5, width - 2 * 5.0))
    sx, sy, size, pad, W = lay(span)
    while grow and W > width + 1e-6 and span > base:
        span = max(base, span - 2.0)
        sx, sy, size, pad, W = lay(span)

    def P0(i):
        x, y = ids[i]["xy"]
        return (x - minx) * sx, (y - miny) * sy
    H = spany * sy + 2 * pad
    sc = Scene(W, H)

    def P(i):
        x, y = P0(i)
        return pad + x, pad + y
    for s in st:
        x, y = P(s["id"])
        if s.get("hidden"):
            continue
        if cell:
            sc.rect(x - size / 2, y - size / 2, size, size, fill=s.get("fill"), w=LINE)
            sc.facts["squares"] += 1
        else:
            rr = size / 2 * (1.25 if s.get("big") else 1.0)
            sc.circle(x, y, rr, fill=s.get("fill"), w=LINE)
            sc.facts["stations"] += 1
        if s.get("mark"):
            mark(sc, x, y, size * 0.38, s["mark"])
        if s.get("label"):
            sc.text(x, y + pt(SMALL_PT) * 0.35, s["label"], size=SMALL_PT,
                    grey=55 if not s.get("labelDark") else 100)
    for ln in b.get("lines") or []:
        a, z = P(ln[0]), P(ln[1])
        sc.line(a[0], a[1], z[0], z[1], w=LINE, dash=ln[2] if len(ln) > 2 else None)
    for route in b.get("route") or []:
        style = b.get("routeStyle", "arrows")
        for a, z in zip(route, route[1:]):
            if style == "none":
                break
            (x1, y1), (x2, y2) = P(a), P(z)
            if style == "arrows":
                sc.arrow(x1, y1, x2, y2, w=0.8, head=1.6, gap0=size * 0.55,
                         gap1=size * 0.55, grey=55)
    rad = size * (0.36 if cell else 0.42)

    def locate(key):
        if key not in ids:
            return None
        x, y = P(key)
        return x, y, rad
    return sc, locate


GENERATORS = {}


def generator(name):
    def deco(fn):
        GENERATORS[name] = fn
        return fn
    return deco


@generator("morris")
def gen_morris(b):
    rings = int(b.get("rings", 3))
    if b.get("notation") == "grid":
        return _morris_grid(b, rings)
    nodes, edges = {}, []
    for k in range(rings):
        a = k / (2.0 * rings) if rings > 1 else 0.0   # 0, 1/6, 1/3 for three rings
        lo, hi = a, 1 - a
        mid = 0.5
        pts = {"tl": (lo, lo), "tm": (mid, lo), "tr": (hi, lo), "mr": (hi, mid),
               "br": (hi, hi), "bm": (mid, hi), "bl": (lo, hi), "ml": (lo, mid)}
        for key, xy in pts.items():
            nodes["%d%s" % (k, key)] = list(xy)
        ring = ["tl", "tm", "tr", "mr", "br", "bm", "bl", "ml"]
        for i in range(8):
            edges.append(["%d%s" % (k, ring[i]), "%d%s" % (k, ring[(i + 1) % 8])])
    for k in range(rings - 1):
        for m in ("tm", "mr", "bm", "ml"):
            edges.append(["%d%s" % (k, m), "%d%s" % (k + 1, m)])
        if b.get("diagonals"):
            for m in ("tl", "tr", "br", "bl"):
                edges.append(["%d%s" % (k, m), "%d%s" % (k + 1, m)])
    if b.get("centre"):
        nodes["c"] = [0.5, 0.5]
        if b.get("centreLines"):
            for m in ("tm", "mr", "bm", "ml"):
                edges.append(["%d%s" % (rings - 1, m), "c"])
    return {"nodes": nodes, "edges": edges}


def _morris_grid(b, rings):
    """Merels boards named by grid coordinates: three rings give the a1–g7 points of the
    nine men's morris board, two rings the a1–e5 points of the six men's morris board."""
    n = 2 * rings + 1
    mid = rings
    key = lambda c, r: "%s%d" % (chr(97 + c), r + 1)  # noqa: E731
    nodes, edges = {}, []
    for k in range(rings):
        lo, hi = k, n - 1 - k
        ring = [(lo, lo), (mid, lo), (hi, lo), (hi, mid), (hi, hi), (mid, hi), (lo, hi), (lo, mid)]
        for c, r in ring:
            nodes[key(c, r)] = [c / (n - 1.0), (n - 1 - r) / (n - 1.0)]
        for i in range(8):
            edges.append([key(*ring[i]), key(*ring[(i + 1) % 8])])
    for k in range(rings - 1):
        lo, hi, lo2, hi2 = k, n - 1 - k, k + 1, n - 2 - k
        edges += [[key(mid, lo), key(mid, lo2)], [key(hi, mid), key(hi2, mid)],
                  [key(mid, hi), key(mid, hi2)], [key(lo, mid), key(lo2, mid)]]
        if b.get("diagonals"):
            edges += [[key(lo, lo), key(lo2, lo2)], [key(hi, lo), key(hi2, lo2)],
                      [key(hi, hi), key(hi2, hi2)], [key(lo, hi), key(lo2, hi2)]]
    axes = {"x": [[c / (n - 1.0), chr(97 + c)] for c in range(n)],
            "y": [[(n - 1 - r) / (n - 1.0), str(r + 1)] for r in range(n)]}
    return {"nodes": nodes, "edges": edges, "axes": axes if b.get("coords", True) else None}


@generator("cross33")
def gen_cross33(b):
    """Fox-and-geese cross: 7 × 7 points without the 2 × 2 corners."""
    nodes, edges = {}, []
    ok = lambda c, r: (2 <= c <= 4) or (2 <= r <= 4)  # noqa: E731
    for c in range(7):
        for r in range(7):
            if ok(c, r):
                nodes["%s%d" % (chr(97 + c), r + 1)] = [c / 6.0, (6 - r) / 6.0]
    for c in range(7):
        for r in range(7):
            if not ok(c, r):
                continue
            k = "%s%d" % (chr(97 + c), r + 1)
            if c + 1 < 7 and ok(c + 1, r):
                edges.append([k, "%s%d" % (chr(98 + c), r + 1)])
            if r + 1 < 7 and ok(c, r + 1):
                edges.append([k, "%s%d" % (chr(97 + c), r + 2)])
            if b.get("diagonals"):
                if (c + r) % 2 == 0:
                    for dc, dr in ((1, 1), (-1, 1)):
                        c2, r2 = c + dc, r + dr
                        if 0 <= c2 < 7 and r2 < 7 and ok(c2, r2) and ok(c + dc, r) and ok(c, r + dr):
                            edges.append([k, "%s%d" % (chr(97 + c2), r2 + 1)])
    return {"nodes": nodes, "edges": edges}


@generator("alquerque")
def gen_alquerque(b):
    cols, rows = int(b.get("cols", 5)), int(b.get("rows", 5))
    nodes, edges = {}, []
    for c in range(cols):
        for r in range(rows):
            nodes["%s%d" % (chr(97 + c), r + 1)] = [c / (cols - 1), (rows - 1 - r) / (rows - 1)]
    for c in range(cols):
        for r in range(rows):
            k = "%s%d" % (chr(97 + c), r + 1)
            if c + 1 < cols:
                edges.append([k, "%s%d" % (chr(98 + c), r + 1)])
            if r + 1 < rows:
                edges.append([k, "%s%d" % (chr(97 + c), r + 2)])
            if (c + r) % 2 == 0:
                if c + 1 < cols and r + 1 < rows:
                    edges.append([k, "%s%d" % (chr(98 + c), r + 2)])
                if c - 1 >= 0 and r + 1 < rows:
                    edges.append([k, "%s%d" % (chr(96 + c), r + 2)])
    return {"nodes": nodes, "edges": edges}


# ── primitive drawings (charts, figures, anything the board types do not cover)
def draw_prims(prims, W, H, sc, ox=0.0, oy=0.0):
    """Primitives in normalised coordinates (0–1 of W × H), y downward.

    {"op": "line", "a": [x, y], "b": [x, y], "w": 0.9, "dash": true}
    {"op": "poly", "pts": [[x, y], …], "closed": false, "fill": null|0|25|55|100}
    {"op": "circle", "c": [x, y], "r": 0.02, "fill": 100}     (r in units of W)
    {"op": "rect", "a": [x, y], "b": [x, y], "fill": null, "r": 0.01}
    {"op": "arrow", "a": [x, y], "b": [x, y], "bend": 0.0, "dash": false}
    {"op": "text", "at": [x, y], "text": "…", "size": 8.5, "anchor": "middle",
     "weight": "normal", "style": "normal"}
    {"op": "hand", "at": [x, y], "s": 0.1, "fingers": [0, 0, 0, 0, 0]}
     (the jan-ken hand drawing; `at` is the top-left of its box, s in units of W)
    """
    X = lambda v: ox + v * W  # noqa: E731
    Y = lambda v: oy + v * H  # noqa: E731
    for p in prims:
        op = p.get("op")
        w = p.get("w", LINE)
        dash = (1.4, 1.0) if p.get("dash") else None
        if op == "line":
            sc.line(X(p["a"][0]), Y(p["a"][1]), X(p["b"][0]), Y(p["b"][1]), w=w, dash=dash,
                    grey=p.get("grey", 100))
        elif op == "poly":
            sc.polyline([(X(x), Y(y)) for x, y in p["pts"]], w=w,
                        closed=p.get("closed", False), fill=p.get("fill"), dash=dash,
                        grey=p.get("grey", 100))
        elif op == "curve":
            pts = [(X(x), Y(y)) for x, y in p["pts"]]
            d = [("M",) + pts[0]]
            for i in range(1, len(pts) - 2, 3):
                d.append(("C",) + pts[i] + pts[i + 1] + pts[i + 2])
            sc.path(d, fill=p.get("fill"), w=w, dash=dash, grey=p.get("grey", 100))
        elif op == "circle":
            sc.circle(X(p["c"][0]), Y(p["c"][1]), p["r"] * W, fill=p.get("fill"),
                      w=p.get("w", STROKE))
        elif op == "rect":
            x1, y1 = X(p["a"][0]), Y(p["a"][1])
            x2, y2 = X(p["b"][0]), Y(p["b"][1])
            sc.rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1),
                    fill=p.get("fill"), w=w, r=p.get("r", 0) * W, dash=dash)
        elif op == "arrow":
            if p.get("bend"):
                sc.curve_arrow(X(p["a"][0]), Y(p["a"][1]), X(p["b"][0]), Y(p["b"][1]),
                               bend=p["bend"], w=p.get("w", ARROW), dash=dash)
            else:
                sc.arrow(X(p["a"][0]), Y(p["a"][1]), X(p["b"][0]), Y(p["b"][1]),
                         w=p.get("w", ARROW), dash=dash)
        elif op == "text":
            sc.text(X(p["at"][0]), Y(p["at"][1]), p["text"], size=max(p.get("size", LABEL_PT),
                                                                        SMALL_PT),
                    anchor=p.get("anchor", "middle"), weight=p.get("weight", "normal"),
                    style=p.get("style", "normal"))
        elif op == "piece":
            piece(sc, X(p["c"][0]), Y(p["c"][1]), p.get("r", 0.03) * W, p.get("side", "white"),
                  p.get("kind", "piece"), p.get("label"))
        elif op == "mark":
            mark(sc, X(p["c"][0]), Y(p["c"][1]), p.get("r", 0.03) * W, p.get("kind", "dot"))
        elif op == "hand":
            hand(sc, X(p["at"][0]), Y(p["at"][1]), p.get("s", 0.1) * W, p.get("fingers", [0, 0, 0, 0, 0]))


def board_prims(b, width):
    W = b.get("widthMm") or width
    # Large print sets every label at twice the size (set_label_scale). A picture kept at its book
    # width then carried 16 pt words in a 72 mm drawing and they ran together (Conkers,
    # 2026-09-26). The drawing grows with its labels, up to the width it is given.
    k = LABEL_PT / 8.5
    if k > 1.0 and b.get("widthMm"):
        W = max(W, min(W * k, width))
    H = W * b.get("aspect", 0.6)
    sc = Scene(W, H)
    draw_prims(b.get("prims", []), W, H, sc)
    anchors = b.get("anchors", {})

    def locate(key):
        if key not in anchors:
            return None
        x, y = anchors[key]
        return x * W, y * H, b.get("pieceR", 0.025) * W
    return sc, locate


# ── charts ────────────────────────────────────────────────────────────────
PIPS = {0: [], 1: [(0.5, 0.5)], 2: [(0.25, 0.25), (0.75, 0.75)],
        3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
        4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
        5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
        6: [(0.25, 0.2), (0.75, 0.2), (0.25, 0.5), (0.75, 0.5), (0.25, 0.8), (0.75, 0.8)]}


def domino(sc, x, y, w, top, bottom, open_pips=()):
    """A tile w wide, 2w high, pips drawn; pips listed in open_pips drawn open."""
    h = 2 * w
    sc.rect(x, y, w, h, fill=None, w=1.0, r=w * 0.12)
    sc.line(x + w * 0.12, y + w, x + w * 0.88, y + w, w=STROKE)
    for half, n in ((0, top), (1, bottom)):
        for (px, py) in PIPS.get(int(n), []):
            cx, cy = x + px * w, y + half * w + py * w
            is_open = ((half, int(n)) in open_pips or ("all", int(n)) in open_pips
                       or (("half6", 6) in open_pips and int(n) == 6 and px < 0.5))
            sc.circle(cx, cy, w * 0.085, fill=None if is_open else 100,
                      w=STROKE if is_open else 0)


def chart_tiles(b, width):
    items = b["items"]
    per_row = b.get("perRow") or min(8, len(items))
    lines_of = [str(it.get("label", "")).split("\n") for it in items]
    # the widest label line, in the weight it prints in (the first line is bold)
    need = max([text_width(ln, SMALL_PT, "bold" if j == 0 else "normal")
                for ls in lines_of for j, ln in enumerate(ls) if ln] or [0.0]) + 1.5
    # A label wider than its cell ran into the next one ('1 Heaven2 Earth…' in large print,
    # found 2026-09-26). Fewer tiles go to a row instead, but each of the spec's own rows — a
    # suit, a player's pieces — is wrapped on its own, so a caption's 'top row' / 'bottom row'
    # stays true.
    fit = max(1, min(per_row, int((width - 2.0) // need)))
    rows_idx = []
    for g0 in range(0, len(items), per_row):
        grp = list(range(g0, min(g0 + per_row, len(items))))
        rows_idx += [grp[k:k + fit] for k in range(0, len(grp), fit)]
    cols = max(len(r_) for r_ in rows_idx)
    tw = min(9.5, (width - 4) / (cols * 1.45))
    cellw = max(tw * 1.45, need)
    label_lines = max((len(ls) for ls in lines_of), default=1)
    cellh = tw * 2 + pt(SMALL_PT) * 1.35 * (label_lines + 0.6) + 2.0
    W = cols * cellw + 2
    H = len(rows_idx) * cellh + 2
    sc = Scene(W, H)
    # Chinese sets: the 1s and 4s are red, and half of each 6 on the double six
    open_red = {("all", 1), ("all", 4)} if b.get("redPipsOpen") else set()
    place = {i: (c, r) for r, row in enumerate(rows_idx) for c, i in enumerate(row)}
    for i, it in enumerate(items):
        c, r = place[i]
        x = 1 + c * cellw + (cellw - tw) / 2
        y = 1 + r * cellh
        extra = {("half6", 6)} if (b.get("redPipsOpen") and it["top"] == 6 and it["bottom"] == 6) else set()
        domino(sc, x, y, tw, it["top"], it["bottom"], open_red | extra)
        for j, ln in enumerate(str(it.get("label", "")).split("\n")):
            if ln:
                sc.text(x + tw / 2, y + 2 * tw + pt(SMALL_PT) * 1.3 * (j + 1), ln,
                        size=SMALL_PT, weight="bold" if j == 0 else "normal")
    return sc, (lambda k: None)


# ── hand signs (jan-ken, morra) ─────────────────────────────────────────────
HAND_SHAPES = {"stone": [0, 0, 0, 0, 0], "paper": [1, 1, 1, 1, 1],
               "scissors": [0, 1, 1, 0, 0], "scissors-thumb": [1, 1, 0, 0, 0],
               "frog": [1, 0, 0, 0, 0], "snake": [0, 1, 0, 0, 0], "slug": [0, 0, 0, 0, 1]}


def capsule(sc, x1, y1, x2, y2, r, fill=0):
    """A finger-like capsule from (x1, y1) to (x2, y2), radius r, drawn as one closed outline."""
    ang = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(ang), math.cos(ang)
    pts = []
    for k in range(9):              # half circle round the far end
        a = ang - math.pi / 2 + math.pi * k / 8.0
        pts.append((x2 + r * math.cos(a), y2 + r * math.sin(a)))
    # the arc ends on the +normal side: return along that side, then back along the other
    pts.append((x1 + nx * r, y1 + ny * r))
    pts.append((x1 - nx * r, y1 - ny * r))
    sc.polyline(pts, closed=True, fill=fill, w=STROKE)


def hand(sc, x, y, s, fingers):
    """A right hand seen from the back, fingers up, at (x, y) = top-left of a box s wide, 1.9 s high.
    `fingers` = [thumb, index, middle, ring, little], 1 = extended."""
    palm_w, palm_h = s * 0.62, s * 0.62
    px, py = x + s * 0.22, y + s * 1.05
    fw = palm_w / 4.0
    # fingers: little … index from left to right on a right hand seen from the back
    order = [4, 3, 2, 1]
    for k, fi in enumerate(order):
        fx = px + k * fw + fw * 0.08
        ext = fingers[fi]
        length = s * (0.72 if fi == 2 else 0.64 if fi in (1, 3) else 0.5) if ext else s * 0.16
        sc.rect(fx, py - length + fw * 0.35, fw * 0.84, length, fill=None, w=STROKE, r=fw * 0.42)
    # palm drawn over the finger roots
    sc.rect(px, py, palm_w, palm_h, fill=0, w=STROKE, r=s * 0.12)
    if not any(fingers[1:]):
        # a fist: the knuckle line
        for k in range(4):
            fx = px + k * fw + fw * 0.5
            sc.line(fx, py + s * 0.02, fx, py + s * 0.14, w=STROKE)
    # thumb on the right side (right hand, palm towards the reader)
    tx, ty = px + palm_w, py + palm_h * 0.55
    if fingers[0]:
        capsule(sc, tx - s * 0.06, ty + s * 0.06, tx + s * 0.3, ty - s * 0.36, fw * 0.42)
    else:
        sc.rect(tx - s * 0.06, ty - s * 0.02, s * 0.16, s * 0.3, fill=0, w=STROKE, r=s * 0.07)


def chart_hands(b, width):
    items = b["items"]
    layout = b.get("layout", "row")
    s = b.get("handMm", 16.0)
    lab_lines = max(len(str(it.get("label", "")).split("\n")) for it in items)
    cell_w = max(s * 1.6, 26.0)
    cell_h = s * 1.95 + pt(SMALL_PT) * 1.35 * (lab_lines + 0.4)
    if layout == "triangle" and len(items) == 3:
        W = min(width, cell_w * 3.2)
        H = cell_h * 2.05
        centres = [(W / 2, 0.0), (cell_w * 0.55, cell_h * 1.05), (W - cell_w * 0.55, cell_h * 1.05)]
    else:
        per = b.get("perRow") or len(items)
        rows = int(math.ceil(len(items) / float(per)))
        W = min(width, per * cell_w)
        cw = W / per
        # shrink the hands, never the text, when the row is too long for the width
        s = min(s, cw / 1.25)
        cell_h = s * 1.95 + pt(SMALL_PT) * 1.35 * (lab_lines + 0.4)
        H = rows * cell_h
        centres = [((i % per) * cw + cw / 2, (i // per) * cell_h) for i in range(len(items))]
    sc = Scene(W, H)
    for (cx, cy), it in zip(centres, items):
        shape = it.get("fingers") or HAND_SHAPES.get(it.get("shape", "stone"))
        hand(sc, cx - s * 0.5, cy + 0.5, s, shape)
        for j, ln in enumerate(str(it.get("label", "")).split("\n")):
            if ln:
                sc.text(cx, cy + s * 1.95 + pt(SMALL_PT) * 1.3 * (j + 0.6), ln, size=SMALL_PT,
                        weight="bold" if j == 0 else "normal")
    for a, z in b.get("beats") or []:
        (x1, y1), (x2, y2) = centres[a], centres[z]
        y1 += s * 1.0
        y2 += s * 1.0
        sc.curve_arrow(x1, y1, x2, y2, bend=b.get("beatBend", 0.0) or 0.001, w=ARROW, head=2.2,
                       gap0=s * 0.75, gap1=s * 0.75)
    return sc, (lambda k: None)


# ── knucklebone faces (astragaloi) ──────────────────────────────────────────
ASTRAGAL_FACE = {4: ("broad", "bulging"), 3: ("broad", "hollow"), 1: ("narrow", "flat"),
                 6: ("narrow", "grooved")}


def astragal(sc, x, y, s, value):
    """A knucklebone seen from above with face `value` up: broad faces wide, narrow faces slim."""
    kind, shape = ASTRAGAL_FACE[int(value)]
    w = s * (0.72 if kind == "broad" else 0.4)
    h = s * 0.9
    cx = x + s / 2
    sc.rect(cx - w / 2, y, w, h, fill=0, w=STROKE, r=w * 0.45)
    if shape == "bulging":
        sc.path([("M", cx - w * 0.3, y + h * 0.62), ("C", cx - w * 0.15, y + h * 0.35, cx + w * 0.15,
                  y + h * 0.35, cx + w * 0.3, y + h * 0.62)], w=STROKE)
    elif shape == "hollow":
        sc.ellipse(cx, y + h * 0.5, w * 0.26, h * 0.24, fill=25, w=STROKE)
    elif shape == "grooved":
        sc.line(cx, y + h * 0.2, cx, y + h * 0.8, w=STROKE)
        sc.line(cx - w * 0.14, y + h * 0.28, cx - w * 0.14, y + h * 0.72, w=STROKE)
    # flat: plain outline


def chart_faces(b, width):
    items = b["items"]
    if items and "faces" in items[0]:
        # rows of throws: name, four bones with values, total
        s = b.get("boneMm", 10.0)
        # the row names' column fits its widest name ('Opponent' ran into the first bone in
        # large print; 2026-09-26)
        name_w = max(20.0, max(text_width(it.get("row", ""), SMALL_PT, "bold") for it in items) + 2.5)
        n = max(len(it["faces"]) for it in items)
        row_h = s * 0.9 + pt(SMALL_PT) * 2.6
        W = min(width, name_w + n * (s + 3.0) + 24.0)
        H = len(items) * row_h + 1.0
        sc = Scene(W, H)
        for r, it in enumerate(items):
            y = r * row_h + 1.0
            sc.text(0.5, y + s * 0.55, it.get("row", ""), size=SMALL_PT, weight="bold", anchor="start")
            for k, v in enumerate(it["faces"]):
                x = name_w + k * (s + 3.0)
                astragal(sc, x, y, s, v)
                sc.text(x + s / 2, y + s * 0.9 + pt(SMALL_PT) * 1.1, str(v), size=SMALL_PT, weight="bold")
            tx = name_w + n * (s + 3.0) + 1.0
            sc.text(tx, y + s * 0.55, "= %s" % it.get("total", sum(it["faces"])), size=LABEL_PT,
                    weight="bold", anchor="start")
            if it.get("name"):
                sc.text(tx, y + s * 0.55 + pt(SMALL_PT) * 1.25, it["name"], size=SMALL_PT, anchor="start",
                        style="italic")
        return sc, (lambda k: None)
    s = b.get("boneMm", 14.0)
    cell_w = max(s * 1.25, (width - 2.0) / len(items))

    def wrap(text, maxw):
        # a label wider than its column ran into the next one (large print, p. 385)
        words, out, cur = str(text).split(), [], ""
        for w_ in words:
            t_ = (cur + " " + w_).strip()
            if cur and text_width(t_, SMALL_PT) > maxw:
                out.append(cur)
                cur = w_
            else:
                cur = t_
        if cur:
            out.append(cur)
        return out

    wrapped = [[l_ for ln in it.get("lines", []) for l_ in wrap(ln, cell_w - 2.0)] for it in items]
    lines = max(len(w_) for w_ in wrapped)
    cell_h = s * 0.9 + pt(LABEL_PT) * 1.6 + pt(SMALL_PT) * 1.3 * lines + 1.0
    W = cell_w * len(items)
    sc = Scene(W, cell_h)
    for i, it in enumerate(items):
        x = i * cell_w + (cell_w - s) / 2
        astragal(sc, x, 0.5, s, it["value"])
        cx = i * cell_w + cell_w / 2
        sc.text(cx, s * 0.9 + pt(LABEL_PT) * 1.3, str(it["value"]), size=LABEL_PT, weight="bold")
        for j, ln in enumerate(wrapped[i]):
            sc.text(cx, s * 0.9 + pt(LABEL_PT) * 1.4 + pt(SMALL_PT) * 1.3 * (j + 1), ln, size=SMALL_PT)
    return sc, (lambda k: None)


def _png_for_print(path, max_px=1400):
    """Load a scanned figure, lift the grey paper to white, cut away any caption fragment
    left under the drawing, trim, and return base64 PNG + aspect (height / width)."""
    import base64, io
    from PIL import Image, ImageOps
    im = Image.open(path).convert("L")
    lo, hi = 70, 165
    im = im.point(lambda v: 0 if v < lo else (255 if v > hi else int((v - lo) * 255 / (hi - lo))))
    # rows holding ink
    w, h = im.size
    px = im.load()
    ink = [sum(1 for x in range(0, w, 2) if px[x, y] < 128) for y in range(h)]
    # a caption fragment: a thin band of ink at the bottom, separated from the drawing by a gap
    y = h - 1
    while y > 0 and ink[y] == 0:
        y -= 1
    band_end = y
    while y > 0 and ink[y] > 0:
        y -= 1
    band_start = y
    gap = 0
    while y > 0 and ink[y] == 0:
        y -= 1
        gap += 1
    if band_end - band_start < h * 0.09 and gap >= 4 and y > h * 0.5:
        im = im.crop((0, 0, w, band_start - gap // 2))
    box = ImageOps.invert(im).getbbox()
    if box:
        im = im.crop(box)
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii"), im.height / float(im.width), im.width


def chart_figures(b, width):
    """Rows of pictures (e.g. Jayne's string figures), each with a caption under it."""
    items = b["items"]
    per = b.get("perRow") or 4
    gap = 3.0
    cw = (width - gap * (per - 1)) / per
    lines = max(len(str(it.get("label", "")).split("\n")) for it in items)
    pics = []
    for it in items:
        src = it["src"] if os.path.isabs(it["src"]) else os.path.join(ROOT, it["src"])
        data, aspect, px_w = _png_for_print(src)
        pics.append((data, aspect, px_w / 300.0 * 25.4))   # widest it may print at 300 ppi, mm
    ph = max(min(a * cw, cw * 0.75, a * wmax) for _, a, wmax in pics)
    cell_h = ph + pt(SMALL_PT) * 1.35 * (lines + 0.5) + 1.0
    rows = int(math.ceil(len(items) / float(per)))
    sc = Scene(width, rows * cell_h)
    for i, (it, (data, aspect, wmax)) in enumerate(zip(items, pics)):
        c, r = i % per, i // per
        x = c * (cw + gap)
        y = r * cell_h
        h = min(aspect * cw, ph, aspect * wmax)
        w_ = h / aspect
        sc.image(x + (cw - w_) / 2, y + (ph - h), w_, h, data)
        for j, ln in enumerate(str(it.get("label", "")).split("\n")):
            if ln:
                sc.text(x + cw / 2, y + ph + pt(SMALL_PT) * 1.3 * (j + 1), ln, size=SMALL_PT,
                        weight="bold" if j == 0 else "normal")
    return sc, (lambda k: None)


def chart_bed(b, width):
    """A chalked bed. Divisions and `anchors` use coordinates normalised to the bed
    (0–1 across, 0–1 down); `marginMm` leaves room round the bed for labels and paths."""
    divs = b["divisions"]
    span = b.get("spanMm") or min(width * 0.6, 60.0)
    aspect = b.get("aspect", 1.6)
    m = b.get("marginMm", 4.0)
    W, H = span + 2 * m, span * aspect + 2 * m
    sc = Scene(W, H)
    for d in divs:
        x, y = m + d["x"] * span, m + d["y"] * span * aspect
        w_, h_ = d["w"] * span, d["h"] * span * aspect
        if d.get("shape") == "arc":
            sc.path([("M", x, y + h_), ("C", x, y - h_ * 0.3, x + w_, y - h_ * 0.3, x + w_, y + h_),
                     ("Z",)], w=LINE)
        else:
            sc.rect(x, y, w_, h_, fill=d.get("fill"), w=LINE)
        if d.get("label") not in (None, ""):
            sc.text(x + w_ / 2, y + h_ / 2 + pt(LABEL_PT) * 0.35, d["label"], size=LABEL_PT)
    ids = {d["id"]: d for d in divs if "id" in d}
    anchors = b.get("anchors", {})

    def locate(key):
        if key in anchors:
            ax, ay = anchors[key]
            return m + ax * span, m + ay * span * aspect, 2.0
        d = ids.get(key)
        if not d:
            return None
        return (m + (d["x"] + d["w"] * 0.25) * span, m + (d["y"] + d["h"] * 0.5) * span * aspect,
                2.0)
    return sc, locate


BOARD_TYPES = {"grid": board_grid, "mancala": board_mancala, "graph": board_graph,
               "track": board_track, "prims": board_prims, "tiles": chart_tiles,
               "bed": chart_bed, "hands": chart_hands, "faces": chart_faces,
               "figures": chart_figures}


# ═════════════════════════════════════════════════════════════════════════
# SPEC → SCENE
# ═════════════════════════════════════════════════════════════════════════
def _expand_board(b):
    b = dict(b)
    t = b.get("type")
    if t in GENERATORS:
        g = GENERATORS[t](b)
        b.update(g)
        b["type"] = "graph"
    if b.get("noAxes"):
        b.pop("axes", None)
    if t == "chart":
        kind = b.get("kind")
        b["type"] = {"tiles": "tiles", "bed": "bed", "hands": "hands", "faces": "faces",
                     "figures": "figures"}.get(kind, "prims")
    return b


DEFAULT_LABELS = {"black": "Black", "white": "White", "red": "Red", "blue": "Blue",
                  "green": "Green", "yellow": "Yellow"}
MARK_LABELS = {"rosette": "rosette", "castle": "safe square", "safe": "safe square",
               "throne": "throne", "corner": "corner square", "star": "special square",
               "start": "start", "home": "home", "x": "captured", "captured": "captured",
               "water": "water"}


def _knockout(sc, x, y, text, size, anchor="middle", weight="normal"):
    """A white box under a word set on the board, so the board's lines stop at the word instead
    of running through its letters (Alquerque 'empty', Diviyan Keliya 'centre', the Ludus zone
    letters on the grid lines — seen on the printed pages 2026-09-26). Sized from the print
    font: cap/ascender height 0.72 em above the baseline, descender 0.24 em below."""
    w = text_width(text, size, weight)
    x0 = {"start": x, "middle": x - w / 2.0, "end": x - w}[anchor]
    em, pad = pt(size), 0.35
    sc.rect(x0 - pad, y - 0.72 * em - pad, w + 2 * pad, 0.96 * em + 2 * pad, fill=0, w=0)


def _label_place(l, x, y, r):
    """Where and how large a free (non-corner) label is set: (x, y, size, anchor)."""
    dx, dy = {"above": (0, -r - 1.2), "below": (0, r + pt(LABEL_PT) + 0.6),
              "left": (-r - 1.0, pt(LABEL_PT) * 0.35),
              "right": (r + 1.0, pt(LABEL_PT) * 0.35),
              "on": (0, pt(LABEL_PT) * 0.35)}.get(l.get("pos", "below"))
    anchor = {"left": "end", "right": "start"}.get(l.get("pos", "below"), "middle")
    size = max(l.get("size", LABEL_PT), SMALL_PT)
    if l.get("pos") == "on" and LABEL_PT > 8.5:
        # large print: a word set on a cell at twice the size ran out of the cell and over
        # the frame ('village', Li'b el-merafib). It may shrink to fit its cell, but not
        # below 1.5× the book size — the large-print floor.
        room = 2 * r * 1.47 - 1.0
        tw_ = text_width(l["text"], size, l.get("weight", "normal"))
        if tw_ > room:
            size = max(size * room / tw_, 0.75 * size)
    return x + dx, y + dy, size, anchor


def _overlay(sc, locate, spec, facts_only=False):
    """Draw marks, pieces, arrows and labels onto `sc` through `locate`."""
    missing = []
    rings = []
    # the knockouts go down first, straight onto the board: they hide the board's lines under a
    # word, and never a mark, a piece or an arrow, which are all drawn after them
    for l in spec.get("labels") or []:
        at = locate(l["at"])
        if at and l.get("pos") != "corner":
            lx, ly, size, anchor = _label_place(l, *at)
            _knockout(sc, lx, ly, l["text"], size, anchor, l.get("weight", "normal"))
    for m in spec.get("marks") or []:
        at = locate(m["at"])
        if not at:
            missing.append(m["at"])
            continue
        x, y, r = at
        if m.get("mark") == "ring":
            rings.append((x, y, r))
            continue
        mark(sc, x, y, r * 1.05, m.get("mark", "dot"))
    for p in spec.get("pieces") or []:
        n = int(p.get("count", 1))
        at = locate(p["at"])
        if not at:
            missing.append(p["at"])
            continue
        x, y, r = at
        if n > 1 and p.get("kind") in ("seed", "bean"):
            continue
        for k in range(n):
            off = (k - (n - 1) / 2) * r * 0.5
            piece(sc, x + off, y - off, r, p.get("side", "white"), p.get("kind", "piece"),
                  p.get("label"), p.get("captured", False))
    for a in spec.get("arrows") or []:
        chain = a.get("path") or [a.get("from"), a.get("to")]
        pts = [locate(k) for k in chain]
        if any(q is None for q in pts):
            missing += [k for k, q in zip(chain, pts) if q is None]
            continue
        style = a.get("style", "move")
        dash = (1.5, 1.1) if style in ("route", "alternate") else None
        w = CAPTURE_PT if style == "capture" else ARROW
        grey = 55 if style == "route" else 100
        if style == "sow" and getattr(locate, "board", "") == "mancala":
            _sow_path(sc, locate, chain, pts)
            continue
        for k, ((x1, y1, r1), (x2, y2, r2)) in enumerate(zip(pts, pts[1:])):
            # "tail": "centre" starts the arrow at the centre of an emptied point
            g0 = 0.9 if (k == 0 and a.get("tail") == "centre") else None
            if style == "sow" or a.get("bend"):
                sc.curve_arrow(x1, y1, x2, y2, bend=a.get("bend", -0.35), w=w, head=2.0,
                               gap0=r1 * 0.9 if g0 is None else g0, gap1=r2 * 1.05, dash=dash, grey=grey)
            else:
                sc.arrow(x1, y1, x2, y2, w=w, head=2.3, gap0=r1 * 1.05 if g0 is None else g0,
                         gap1=r2 * 1.1, dash=dash, grey=grey)
    ring_k = 1.55 if getattr(locate, "board", "") == "mancala" else 1.32
    for (x, y, r) in rings:
        sc.circle(x, y, r * ring_k, fill=None, w=1.2)
    for l in spec.get("labels") or []:
        at = locate(l["at"])
        if not at:
            missing.append(l["at"])
            continue
        x, y, r = at
        if l.get("pos") == "corner":
            # route numbers: small, in the top-left corner inside the cell
            half = r * 1.47
            size = max(l.get("size", SMALL_PT), SMALL_PT)
            if LABEL_PT > 8.5:
                # large print: at twice the size a corner number ran into the star or cross drawn
                # in its own cell (Senet, Sugoroku, Ashta Kashte; 2026-09-26). It keeps the
                # large-print floor, 1.5× the book size.
                size = min(size, 0.75 * SMALL_PT)
            sc.text(x - half + 0.7, y - half + pt(size) * 0.9, l["text"], size=size,
                    anchor="start", weight=l.get("weight", "normal"), grey=55)
            continue
        lx, ly, size, anchor = _label_place(l, x, y, r)
        sc.text(lx, ly, l["text"], size=size,
                anchor=anchor, weight=l.get("weight", "normal"), style=l.get("style", "normal"))
    return missing


def _sow_path(sc, locate, chain, pts):
    """A sowing lap drawn as one smooth line just outside the pits it passes,
    ending in an arrowhead on the pit that receives the last seed."""
    r = locate.pit_r
    cy = locate.centre_y
    way = []
    four = getattr(locate, "rows", 2) == 4
    for key, (x, y, _) in zip(chain, pts):
        if key in ("SS", "NS"):
            way.append((x, y))
            continue
        out = 1.0 if y > cy else -1.0
        if four and len(key) > 1 and key[1] == "I":
            # inner rows: run the line in the gap between the two players' inner rows
            out = -out
            way.append((x, y + out * r * 1.25))
            continue
        way.append((x, y + out * r * 1.38))
    if len(way) < 2:
        return
    # Catmull-Rom through the waypoints → cubic Béziers
    d = [("M",) + way[0]]
    P = [way[0]] + way + [way[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d.append(("C",) + c1 + c2 + p2)
    sc.path(d, fill=None, w=ARROW)
    # small drop marks, one per seed sown
    for (x, y) in way[1:]:
        sc.circle(x, y, 0.55, fill=100, w=0)
    ex, ey = way[-1]
    px, py = way[-2]
    ang = math.atan2(ey - py, ex - px)
    sc._head(ex, ey, ang, 2.1)


def _auto_legend(spec, panels):
    if spec.get("legend") is not None:
        out = []
        for e in spec["legend"]:
            g = e.get("glyph") or e.get("side")
            if e.get("mark"):
                out.append((mark_drawer(e["mark"]), e["label"]))
            elif e.get("arrow"):
                out.append((arrow_drawer(e["arrow"]), e["label"]))
            elif g:
                out.append((piece_drawer(g if g in SIDE_FILL else "white",
                                         e.get("kind", "piece"), e.get("pieceLabel")),
                            e["label"]))
        return out
    seen, out = set(), []
    layers = [spec] + list(panels or [])
    for L in layers:
        for p in L.get("pieces") or []:
            key = (p.get("side", "white"), p.get("kind", "piece"), p.get("label"))
            if key in seen or p.get("kind") in ("seed", "bean"):
                continue
            seen.add(key)
            lbl = p.get("legend") or DEFAULT_LABELS.get(p.get("side"), p.get("side", ""))
            if p.get("kind") not in (None, "piece"):
                lbl = p.get("legend") or "%s %s" % (lbl, p["kind"])
            out.append((piece_drawer(*key), lbl))
        for m in L.get("marks") or []:
            k = m.get("mark")
            if ("m", k) in seen or (k == "dot" and not m.get("legend")):
                continue
            seen.add(("m", k))
            out.append((mark_drawer(k), m.get("legend") or MARK_LABELS.get(k, k)))
        for a in L.get("arrows") or []:
            k = a.get("style", "move")
            if ("a", k) in seen:
                continue
            seen.add(("a", k))
            out.append((arrow_drawer(k), a.get("legend") or
                        {"move": "move", "capture": "capturing move", "route": "route",
                         "sow": "sowing", "alternate": "other possible move"}.get(k, k)))
    # collapse identical labels (kings etc. keep their own)
    uniq, lbls = [], set()
    for d, l in out:
        if l in lbls:
            continue
        lbls.add(l)
        uniq.append((d, l))
    return uniq


def render_spec(spec, width=84.0, legend_on=True):
    """Render one diagram spec. Returns (scene, report)."""
    b = _expand_board(spec.get("board") or {"type": "prims", "prims": []})
    t = b.get("type")
    if t not in BOARD_TYPES:
        raise ValueError("%s: unknown board type %r" % (spec.get("id"), t))
    panels = spec.get("panels") or []
    missing = []
    if panels:
        n = len(panels)
        # side by side if they fit; else two across (three or more panels); else stacked
        min_p = b.get("minPanelMm", 55.0)
        cols = spec.get("panelCols")
        if cols is None:
            if (width - 6.0 * (n - 1)) / n >= min_p:
                cols = n
            elif n >= 3 and (width - 6.0) / 2 >= min_p:
                cols = 2
            else:
                cols = 1
        cols = max(1, min(int(cols), n))
        stacked = cols == 1
        sub_w = (width - 6.0 * (cols - 1)) / cols
        subs = []
        for pnl in panels:
            bb = dict(b)
            if pnl.get("board"):
                bb.update(_expand_board(pnl["board"]))
            sc_b, loc = BOARD_TYPES[bb["type"]](bb, sub_w)
            merged = dict(pnl)
            missing += _overlay(sc_b, loc, merged)
            subs.append((pnl, sc_b))
        # panel captions wrap to the panel's own width (a caption wider than its panel ran off
        # the drawing, and at large-print size off the page); a row makes room for its longest
        lead = pt(LABEL_PT) * 1.25

        def cap_lines(text, width):
            words, lines, cur = str(text or "").split(), [], ""
            for w_ in words:
                t_ = (cur + " " + w_).strip()
                if cur and text_width(t_, LABEL_PT, "bold") > width:
                    lines.append(cur)
                    cur = w_
                else:
                    cur = t_
            if cur:
                lines.append(cur)
            return lines

        def cap_height(k):
            return lead * max(k, 1) + pt(LABEL_PT) * 0.45

        def draw_cap(lines, cx, y0):
            for j, ln in enumerate(lines):
                sc.text(cx, y0 + pt(LABEL_PT) * 1.1 + j * lead, ln, size=LABEL_PT, weight="bold")

        caps = [cap_lines(pnl.get("caption", ""), s.w) for pnl, s in subs]
        if cols == n:
            cap_h = cap_height(max(len(c) for c in caps))
            W = sum(s.w for _, s in subs) + 6.0 * (n - 1)
            H = max(s.h for _, s in subs) + cap_h
            sc = Scene(W, H)
            x = 0.0
            for (pnl, s), cl in zip(subs, caps):
                draw_cap(cl, x + s.w / 2, 0.0)
                sc.place(s, x, cap_h)
                x += s.w + 6.0
        else:
            cell_w = max(s.w for _, s in subs)
            idx = list(range(n))
            rows = [idx[i:i + cols] for i in range(0, n, cols)]
            row_cap = [cap_height(max(len(caps[i]) for i in r)) for r in rows]
            row_h = [max(subs[i][1].h for i in r) + ch + 2.0 for r, ch in zip(rows, row_cap)]
            W = cols * cell_w + 6.0 * (cols - 1)
            H = sum(row_h) - 2.0
            sc = Scene(W, H)
            y = 0.0
            for r, rh, ch in zip(rows, row_h, row_cap):
                for c, i in enumerate(r):
                    pnl, s = subs[i]
                    ox = c * (cell_w + 6.0) + (cell_w - s.w) / 2
                    draw_cap(caps[i], ox + s.w / 2, y)
                    sc.place(s, ox, y + ch)
                y += rh
    else:
        sc, loc = BOARD_TYPES[t](b, width)
        missing += _overlay(sc, loc, spec)
    clashes = []
    if legend_on:
        ent = _auto_legend(spec, panels)
        clashes = key_clashes(ent)
        if ent:
            lg = legend(ent, max(sc.w, 40.0))
            out = Scene(max(sc.w, lg.w), sc.h + 2.5 + lg.h)
            out.place(sc, (out.w - sc.w) / 2, 0)
            out.place(lg, (out.w - lg.w) / 2 if lg.w < out.w else 0, sc.h + 2.5)
            sc = out
    refit = sc.fit_to_content()
    rep = {"id": spec.get("id"), "widthMm": round(sc.w, 2), "heightMm": round(sc.h, 2),
           "refitToContent": refit,
           "points": sc.facts["points"], "squares": sc.facts["squares"],
           "pits": sc.facts["pits"], "stations": sc.facts["stations"],
           "pieces": sc.facts["pieces"], "minTextPt": round(sc.facts["minTextPt"], 2),
           "minStrokePt": round(sc.facts["minStrokePt"], 2), "missingRefs": missing,
           "keyClashes": clashes}
    return sc, rep


def verify(spec, rep):
    """Compare what was drawn with what the spec says must be drawn."""
    errs = []
    v = spec.get("verify") or {}
    for k in ("points", "squares", "pits", "stations"):
        if k in v and rep.get(k) != v[k] and not spec.get("panels"):
            errs.append("%s: %s drawn %s, rules say %s" % (spec["id"], k, rep.get(k), v[k]))
    for side in ("black", "white", "red", "blue", "green", "yellow"):
        if side in v and not spec.get("panels"):
            got = rep["pieces"].get(side, 0)
            if got != v[side]:
                errs.append("%s: %s pieces drawn %d, rules say %d" % (spec["id"], side, got, v[side]))
    if rep["missingRefs"]:
        errs.append("%s: references to points that do not exist: %s"
                    % (spec["id"], sorted(set(rep["missingRefs"]))))
    if rep["minTextPt"] < SMALL_PT - 1e-6:
        errs.append("%s: text at %.2f pt (< %.1f)" % (spec["id"], rep["minTextPt"], SMALL_PT))
    if rep["minStrokePt"] < STROKE - 1e-6:
        errs.append("%s: stroke %.2f pt (< %.2f)" % (spec["id"], rep["minStrokePt"], STROKE))
    for a, b in rep.get("keyClashes") or []:
        errs.append("%s: the key draws %r and %r with the same symbol" % (spec["id"], a, b))
    return errs


def write_svg(spec, out_dir, width=84.0, legend_on=True, suffix=""):
    sc, rep = render_spec(spec, width, legend_on)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "%s%s.svg" % (spec["id"], suffix))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(sc.svg(spec.get("caption") or spec["id"]))
    rep["file"] = os.path.relpath(path, ROOT)
    return rep


# ═════════════════════════════════════════════════════════════════════════
# COMMAND LINE — render every diagram and template from the manuscript
# ═════════════════════════════════════════════════════════════════════════
COLUMN_MM = 85.0          # one column of the print text block (6.975 in / 2 − gutter)
WIDE_MM = 177.0           # the whole print text block
TEMPLATE_MM = 177.0
LP_MAX_H_MM = 200.0         # large print: tallest diagram, leaving room for its caption in a 240 mm column
LP_SCALE = 2.0            # large print: labels twice the size (8.5 → 17 pt)


def set_label_scale(k):
    global LABEL_PT, SMALL_PT
    LABEL_PT = 8.5 * k
    SMALL_PT = 8.0 * k


def count_pt():
    """Seed counts in a sowing pit: 10.5 pt at book scale; scaled with the labels when they are
    enlarged (large print), but kept small enough for a two-digit count to sit inside a Hus pit."""
    return 10.5 if LABEL_PT < 12 else max(12.5, LABEL_PT * 0.8)


def spec_width(spec):
    w = spec.get("widthMm")
    if w:
        return float(w)
    if spec.get("size") == "wide":
        return WIDE_MM
    if spec.get("size") == "column":
        return COLUMN_MM
    # before/after panels sit side by side across the page, never stacked
    # into a column-high strip
    if len(spec.get("panels") or []) >= 2:
        return WIDE_MM
    return COLUMN_MM


def render_all(root, lp=False, quiet=False):
    """Render every diagram spec in book.json. Returns (reports, errors)."""
    book = json.load(open(os.path.join(root, "02_MANUSCRIPT", "book.json"), encoding="utf-8"))
    out = os.path.join(root, "07_ASSETS", "diagrams_lp" if lp else "diagrams")
    os.makedirs(out, exist_ok=True)
    if lp:
        set_label_scale(LP_SCALE)
    else:
        set_label_scale(1.0)
    reps, errs, ids = [], [], set()
    for g in book["games"]:
        for spec in specs_of(g):
            if not isinstance(spec, dict):
                errs.append("%s: diagram %r is not a spec" % (g["gameId"], spec))
                continue
            if spec["id"] in ids:
                errs.append("%s: duplicate diagram id %s" % (g["gameId"], spec["id"]))
            ids.add(spec["id"])
            w = spec_width(spec)
            if lp:
                w = min(WIDE_MM, w * 2.0)
            try:
                rep = write_svg(spec, out, w)
                # large print: a tall board drawn the full text width can outgrow the page;
                # draw it narrower instead (labels keep their large-print size)
                # (height does not fall in proportion: captions re-wrap, and a panelled
                # board restacks when narrow, so step down to the widest width that fits)
                if lp and rep["heightMm"] > LP_MAX_H_MM:
                    best, cand = (rep, w), w
                    while cand > COLUMN_MM:
                        cand = max(COLUMN_MM, cand - 4.0)
                        r = write_svg(spec, out, cand)
                        if r["heightMm"] < best[0]["heightMm"]:
                            best = (r, cand)
                        if r["heightMm"] <= LP_MAX_H_MM:
                            break
                    w = best[1]
                    rep = write_svg(spec, out, w)
            except Exception as exc:  # a broken spec must be loud
                errs.append("%s: %s: %s" % (g["gameId"], spec.get("id"), exc))
                continue
            rep["gameId"] = g["gameId"]
            rep["targetWidthMm"] = w
            e = verify(spec, rep)
            rep["errors"] = e
            errs += e
            reps.append(rep)
    set_label_scale(1.0)
    return reps, errs


def specs_of(g):
    """A game's diagram specs: `diagramSpecs` (merged manuscript) or dicts in `diagrams`."""
    if g.get("diagramSpecs"):
        return g["diagramSpecs"]
    return [d for d in g.get("diagrams", []) if isinstance(d, dict)]


def _diagram_index(book):
    idx = {}
    for g in book["games"]:
        for d in specs_of(g):
            idx[d["id"]] = (g["gameId"], d)
    return idx


def template_spec(item, didx):
    """A full-size board derived from a game's own diagram spec: the same
    board, marks and fixed labels, without pieces or arrows, at playing size."""
    if "fromDiagram" in item:
        gid, d = didx[item["fromDiagram"]]
        panel0 = (d.get("panels") or [{}])[0]
        board = dict(d.get("board") or panel0.get("board") or {})
        spec = {"id": item.get("id", d["id"]), "board": board,
                "marks": d.get("marks") or panel0.get("marks") or [],
                "labels": [l for l in (d.get("labels") or []) if l.get("fixed")]}
    else:
        spec = {"id": item["id"], "board": dict(item["board"]), "marks": item.get("marks", []),
                "labels": item.get("labels", [])}
    for k in ("stepMm", "spanMm", "stationMm", "coords", "aspect"):
        if k in item:
            spec["board"][k] = item[k]
    if "verify" in item:
        spec["verify"] = item["verify"]
    return spec


def render_templates(root, quiet=False, lp=False):
    bm_path = os.path.join(root, "02_MANUSCRIPT", "backmatter_book.json")
    if not os.path.exists(bm_path):
        return [], []
    bm = json.load(open(bm_path, encoding="utf-8"))
    book = json.load(open(os.path.join(root, "02_MANUSCRIPT", "book.json"), encoding="utf-8"))
    didx = _diagram_index(book)
    # large print gets its own set: the same boards at the same size, with labels of at least 12 pt
    out = os.path.join(root, "07_ASSETS", "templates_lp" if lp else "templates")
    os.makedirs(out, exist_ok=True)
    reps, errs = [], []
    set_label_scale(1.5 if lp else 1.15)
    for t in bm.get("templates", []):
        items = t.get("items") or [t]
        page = Scene(TEMPLATE_MM, 1.0)
        y = 0.0
        facts = []
        try:
            for it in items:
                spec = template_spec(it, didx)
                target = it.get("widthMm", TEMPLATE_MM)
                sc, rep = render_spec(spec, target, legend_on=it.get("legend", False))
                # a template prints at 100 % on a fixed page: if its labels made the drawing
                # wider than the page allows, draw the board a little narrower instead
                w_try = target
                for _ in range(4):
                    if sc.w <= target + 0.05:
                        break
                    over = (sc.w - target) + 0.3
                    if spec["board"].get("spanMm"):      # a fixed span ignores the width
                        spec["board"]["spanMm"] = spec["board"]["spanMm"] - over
                    else:
                        w_try -= over
                    sc, rep = render_spec(spec, w_try, legend_on=it.get("legend", False))
                if sc.w > target + 0.05:
                    errs.append("template %s: %s is %.1f mm wide, wider than the %.0f mm page"
                                % (t["id"], spec["id"], sc.w, target))
                e = verify(spec, rep)
                errs += ["template %s: %s" % (t["id"], x) for x in e]
                if len(items) > 1 and it.get("caption"):
                    page.text(0, y + pt(LABEL_PT * 1.2), it["caption"], size=LABEL_PT * 1.2,
                              anchor="start", weight="bold")
                    y += pt(LABEL_PT * 1.2) * 1.6
                page.place(sc, (TEMPLATE_MM - sc.w) / 2, y)
                y += sc.h + 8.0
                facts.append(rep)
        except Exception as exc:
            errs.append("template %s: %s" % (t["id"], exc))
            continue
        page.h = y - 8.0
        path = os.path.join(out, t["id"] + ".svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(page.svg(t.get("title", t["id"])))
        rep = {"id": t["id"], "widthMm": round(page.w, 1), "heightMm": round(page.h, 1),
               "parts": facts, "file": os.path.relpath(path, ROOT)}
        # a template is printed at exactly 100 %: it must fit the text block
        if page.h > 200.0:
            errs.append("template %s is %.0f mm tall — larger than the printable page" % (t["id"], page.h))
        reps.append(rep)
    set_label_scale(1.0)
    return reps, errs


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--check", action="store_true", help="render to a temp dir and report only")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    if not os.path.exists(os.path.join(root, "02_MANUSCRIPT", "book.json")):
        print("  · manuscript not in this checkout — boards SKIPPED (expected in CI)")
        return 0
    print("=" * 74)
    print("  BOARDS · diagrams and full-size templates")
    print("=" * 74)
    reps, errs = render_all(root)
    lp_reps, lp_errs = render_all(root, lp=True)
    t_reps, t_errs = render_templates(root)
    lpt_reps, lpt_errs = render_templates(root, lp=True)
    errs += [e for e in lp_errs if "text at" not in e] + t_errs + ["large print: " + e for e in lpt_errs]
    report = {"diagrams": reps, "diagramsLargePrint": [
        {"id": r["id"], "widthMm": r["widthMm"], "heightMm": r["heightMm"], "minTextPt": r["minTextPt"]}
        for r in lp_reps], "templates": t_reps, "templatesLargePrint": lpt_reps, "errors": errs}
    os.makedirs(os.path.join(root, "06_REPORTS"), exist_ok=True)
    with open(os.path.join(root, "06_REPORTS", "boards.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
    print("  %d diagrams · %d large-print diagrams · %d templates (+%d large print)"
          % (len(reps), len(lp_reps), len(t_reps), len(lpt_reps)))
    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        return 1
    print("  ✅ every drawing matches the counts its rules print")
    return 0


if __name__ == "__main__":
    sys.exit(main())
