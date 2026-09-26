#!/usr/bin/env python3
"""
INTERIOR — The Great Book of World Games (GBK-02), 2026 recovery edition
================================================================================
Builds the print interiors (paperback, hardcover, large print) from the
manuscript (`02_MANUSCRIPT/book.json`, `frontmatter.json`, `backmatter.json`)
and the board engine (`boards.py`).

DESIGN (replaces the 2026-09-23 single-column layout, audit WG-012):
  · paperback and hardcover share ONE text block (6.975 × 9.45 in), so their
    page numbers are identical and one page map serves both — the companion,
    the indexes and the metadata cannot drift apart between them;
  · game pages are set in two columns of Source Serif 4 (10.5/14 pt, ≈ 46
    characters a line); rule headings, the quick-play box, captions and
    diagram labels are Source Sans 3; titles are Cinzel, as on the cover;
  · every game begins on a left-hand page, so its first two pages lie open
    together; a game takes two pages, or four when its rules need them —
    never an odd number, and never a page left blank inside an entry;
  · diagrams are placed at 100 %: no label ever prints below 8 pt;
  · the large-print edition is one column of Atkinson Hyperlegible 16 pt,
    no italics, and makes no spread claims (its front matter says so).

Usage:
    interior.py --edition paperback|hardcover|largeprint
    interior.py --all            (paperback + hardcover + largeprint)
    interior.py --check          (verify the last build against its report)

Exit codes: 0 pass · 1 gate red · 2 dependency missing
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import typo  # noqa: E402

IN = 72.0
MM = 72.0 / 25.4

# KDP inside-margin table (Amazon.com, B&W): minimum gutter by page count.
KDP_GUTTER_IN = [(150, 0.375), (300, 0.500), (500, 0.625), (700, 0.750), (828, 0.875)]
GUTTER_SAFETY_IN = 0.05          # ink of some glyphs overhangs the nominal origin
TEXT_W_IN = 6.975                # shared text-block width (PB and HC)
TEXT_H_IN = 9.45
TOP_IN = 0.75
COL_GAP_IN = 0.25

FONT_DIR = os.path.join(DEFAULT_ROOT, "07_ASSETS", "fonts")
FONT_FILES = {
    "GBSerif": "SourceSerif4-Regular.ttf", "GBSerif-I": "SourceSerif4-It.ttf",
    "GBSerif-SB": "SourceSerif4-Semibold.ttf", "GBSerif-B": "SourceSerif4-Bold.ttf",
    "GBSans": "SourceSans3-Regular.ttf", "GBSans-I": "SourceSans3-It.ttf",
    "GBSans-SB": "SourceSans3-Semibold.ttf", "GBSans-B": "SourceSans3-Bold.ttf",
    "GBTitle": "cinzel-500.ttf",
}
# Large print is set in Source Sans 3. Atkinson Hyperlegible was the first
# choice and was rejected on measurement: its 2020 release has no ō, Ō or İ,
# and this book prints Mū Tōrere, Hōsei and Kōichi. A missing glyph is not
# a style question — it is a word the reader cannot read.
FONT_SHA256 = {}                 # filled on registration, written to the report


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def gutter_in(pages):
    for limit, val in KDP_GUTTER_IN:
        if pages <= limit:
            return val
    return KDP_GUTTER_IN[-1][1]


# ── text markup ──────────────────────────────────────────────────────────
_MD_ITALIC = re.compile(r"\*([^*\n]+)\*")


def rich(s):
    """Manuscript text → Paragraph mini-HTML.

    Escape first, then typographic quotes (typo.xml_text raises on a quote it
    cannot convert), then *italic* → <i>. A literal True/False/None can never
    reach this function: `text_of()` refuses non-strings (audit WG-014)."""
    t = typo.xml_text(s)
    t = _MD_ITALIC.sub(r"<i>\1</i>", t)
    return t


def plain(s):
    return _MD_ITALIC.sub(r"\1", str(s))


class LeakError(ValueError):
    pass


def text_of(v, where=""):
    """Only strings print. Booleans, None and numbers in a prose field are a
    data error — the 2026 'True' leak came from printing a boolean."""
    if isinstance(v, str):
        return v
    raise LeakError("non-string value %r in a printed field (%s)" % (v, where))


def register_fonts(lp=False):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping
    import reportlab.rl_config as rl_config
    for name, fn in FONT_FILES.items():
        path = os.path.join(FONT_DIR, fn)
        if not os.path.exists(path):
            raise RuntimeError("font missing: %s (see 07_ASSETS/fonts/licenses)" % path)
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, path))
        FONT_SHA256[fn] = sha256(path)
    rl_config.canvas_basefontname = "GBSerif"
    addMapping("GBSerif", 0, 0, "GBSerif")
    addMapping("GBSerif", 1, 0, "GBSerif-B")
    addMapping("GBSerif", 0, 1, "GBSerif-I")
    addMapping("GBSerif", 1, 1, "GBSerif-B")
    addMapping("GBSans", 0, 0, "GBSans")
    addMapping("GBSans", 1, 0, "GBSans-B")
    addMapping("GBSans", 0, 1, "GBSans-I")
    addMapping("GBSans", 1, 1, "GBSans-B")



# ── geometry ─────────────────────────────────────────────────────────────
def geometry(cfg, edition, pages_guess):
    prod = cfg["production"]
    trim = prod["trimHardcover" if edition == "hardcover" else "trimPaperback"]
    bare = gutter_in(pages_guess)
    lp = edition == "largeprint"
    if edition == "hardcover":
        gut = bare + GUTTER_SAFETY_IN + 0.125
    else:
        gut = bare + GUTTER_SAFETY_IN
    text_w = TEXT_W_IN
    if edition == "paperback":
        # same text block as the hardcover: the extra 0.25 in of trim is shared
        # between gutter and outer margin
        spare = trim["w"] - text_w - gut
        gut = gut + max(0.0, spare - 0.825)
    outer = trim["w"] - text_w - gut
    if outer < 0.5:
        # keep a safe outer margin; the text block narrows instead
        outer = 0.5
        text_w = trim["w"] - gut - outer
    g = {
        "edition": edition, "largePrint": lp,
        "trimWidthIn": trim["w"], "trimHeightIn": trim["h"],
        "wPt": trim["w"] * IN, "hPt": trim["h"] * IN,
        "gutterIn": round(gut, 4), "outerIn": round(outer, 4),
        "gutterBareMinIn": bare, "gutterSafetyIn": GUTTER_SAFETY_IN,
        "topIn": TOP_IN, "bottomIn": trim["h"] - TOP_IN - TEXT_H_IN,
        "textWIn": round(text_w, 4), "textHIn": TEXT_H_IN,
        "gutterPt": gut * IN, "outerPt": outer * IN, "topPt": TOP_IN * IN,
        "textWPt": text_w * IN, "textHPt": TEXT_H_IN * IN,
        "colGapPt": COL_GAP_IN * IN, "columns": 1 if lp else 2,
        "bleed": False,
    }
    g["colWPt"] = g["textWPt"] if lp else (g["textWPt"] - g["colGapPt"]) / 2
    g["bottomPt"] = g["hPt"] - g["topPt"] - g["textHPt"]
    if lp:
        g.update({"bodyPt": 16.0, "leadPt": 22.0, "font": "Source Sans 3 (SIL OFL 1.1, embedded)",
                  "editionLabel": prod.get("largePrint", {}).get("editionLabel", "Large Print Edition")})
    else:
        g.update({"bodyPt": 10.5, "leadPt": 14.0,
                  "font": "Source Serif 4 / Source Sans 3 / Cinzel (SIL OFL 1.1, embedded)"})
    return g


# ── styles ───────────────────────────────────────────────────────────────
def styles(g):
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    lp = g["largePrint"]
    # large print: one sans family, no italics (ACB large-print guidance)
    serif, serif_i, serif_b = (("GBSans", "GBSans", "GBSans-B") if lp else
                               ("GBSerif", "GBSerif-I", "GBSerif-B"))
    sans, sans_i, sans_b, sans_sb = (("GBSans", "GBSans", "GBSans-B", "GBSans-SB") if lp else
                                     ("GBSans", "GBSans-I", "GBSans-B", "GBSans-SB"))
    title = "GBSans-B" if lp else "GBTitle"
    k = 1.0 if not lp else 16.0 / 10.5
    minpt = 16.0 if lp else 8.0

    def S(name, font, size, lead, **kw):
        size = max(size * k, minpt) if lp else size
        lead = max(lead * k, size * 1.3) if lp else lead
        kw.setdefault("bulletFontName", font)
        # no widows: a paragraph's last line is never carried alone to the next column or page
        kw.setdefault("allowWidows", 0)
        return ParagraphStyle(name=name, fontName=font, fontSize=size, leading=lead, **kw)

    st = {
        "body": S("body", serif, 10.5, 14, spaceAfter=5 * k, alignment=TA_LEFT if lp else TA_JUSTIFY,
                  hyphenationLang=None),
        "story": S("story", serif, 10.5, 14, spaceAfter=5 * k, alignment=TA_LEFT if lp else TA_JUSTIFY),
        "step": S("step", serif, 10.5, 13.8, leftIndent=13 * k, firstLineIndent=-13 * k,
                  spaceAfter=2.6 * k),
        "qa": S("qa", serif, 10.2, 13.4, spaceAfter=3.5 * k),
        "h2": S("h2", sans_b, 8.6, 11, spaceBefore=8 * k, spaceAfter=3 * k, textTransform=None),
        "h3": S("h3", sans_b, 9.2, 12, spaceBefore=5 * k, spaceAfter=1.5 * k),
        "source": S("source", serif, 8.6, 11.0, spaceAfter=2.2 * k, leftIndent=0),
        "caption": S("caption", sans_i, 8.6, 10.8, spaceAfter=6 * k, alignment=TA_CENTER),
        "platecap": S("platecap", sans, 8.0, 10.0, spaceBefore=2.5 * k, alignment=TA_LEFT),
        "notice": S("notice", serif, 9.6, 12.6, spaceAfter=3 * k),
        "qlabel": S("qlabel", sans_b, 8.2, 10.4),
        "qval": S("qval", sans, 9.2, 11.6),
        "qbrief": S("qbrief", sans, 9.2, 12.0),
        "gtitle": S("gtitle", title, 25 if not lp else 26, 29 if not lp else 32, spaceAfter=1),
        "kicker": S("kicker", sans_i, 9.6, 12.4, spaceAfter=0),
        "sect": S("sect", title, 22 if not lp else 24, 27 if not lp else 30, spaceAfter=10 * k),
        "part": S("part", sans_b, 9.5, 12, spaceAfter=4 * k),
        "stand": S("stand", serif_i, 12.5, 16.5, spaceAfter=10 * k),
        "fm": S("fm", serif, 10.8, 15.0, spaceAfter=6.5 * k, alignment=TA_LEFT if lp else TA_JUSTIFY),
        "fmh": S("fmh", sans_b, 9.8, 12.5, spaceBefore=7 * k, spaceAfter=2 * k),
        "toc": S("toc", serif, 9.6, 12.2),
        "tocfam": S("tocfam", sans_b, 9.0, 12.0, spaceBefore=6 * k, spaceAfter=1.5 * k),
        "idx": S("idx", serif, 9.0, 11.4, leftIndent=9 * k, firstLineIndent=-9 * k),
        "idxh": S("idxh", sans_b, 9.0, 11.6, spaceBefore=5 * k, spaceAfter=1 * k),
        "small": S("small", serif, 8.8, 11.6, spaceAfter=4 * k),
        "title": S("title", title, 34 if not lp else 30, 40 if not lp else 36, alignment=TA_CENTER,
                   spaceAfter=10),
        "subtitle": S("subtitle", serif_i, 13, 17.5, alignment=TA_CENTER, spaceAfter=8),
        "author": S("author", title, 16 if not lp else 18, 20 if not lp else 22, alignment=TA_CENTER),
        "tpl": S("tpl", sans, 9.5, 12.5, alignment=TA_LEFT),
        "tplh": S("tplh", title, 18 if not lp else 20, 22 if not lp else 24),
        "cell": S("cell", sans, 8.8, 10.8),
        "cellb": S("cellb", sans_b, 8.8, 10.8),
    }
    st["_k"] = k
    st["_lp"] = lp
    st["_fonts"] = {"serif": serif, "serif_i": serif_i, "serif_b": serif_b,
                    "sans": sans, "sans_i": sans_i, "sans_b": sans_b, "sans_sb": sans_sb,
                    "title": title}
    return st


# ── flowables ────────────────────────────────────────────────────────────
class Flow:
    """Minimal flowable protocol: wrap(w, h) → (w, h); split(w, h) → list;
    drawOn(canvas, x, y_bottom)."""
    keep_next = False

    def split(self, aw, ah):
        return []


class VSpace(Flow):
    def __init__(self, h):
        self.h = h

    def wrap(self, aw, ah):
        return aw, self.h

    def drawOn(self, c, x, y, _sW=0):
        pass


class Rule(Flow):
    def __init__(self, width=0.6, before=3.0, after=5.0, grey=0.0, frac=1.0):
        self.lw, self.before, self.after, self.grey, self.frac = width, before, after, grey, frac

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.before + self.lw + self.after

    def drawOn(self, c, x, y, _sW=0):
        c.saveState()
        c.setLineWidth(self.lw)
        c.setStrokeGray(self.grey)
        yy = y + self.after + self.lw / 2
        c.line(x, yy, x + self.aw * self.frac, yy)
        c.restoreState()


def plate_caption(rec):
    """The line printed under a plate: what kind of picture it is and where it comes from."""
    if rec.get("caption"):
        return rec["caption"]
    if rec.get("kind") == "ai-generated":
        return "AI-generated illustration"
    return rec.get("credit", "")


class Bound(Flow):
    """Items that must stay together (a heading and its first step)."""

    def __init__(self, items):
        self.items = items

    def wrap(self, aw, ah):
        self.aw = aw
        self.hs = [it.wrap(aw, ah)[1] for it in self.items]
        # spaceBefore/After of Paragraphs are handled here explicitly
        self.h = sum(self.hs) + sum(_space(it) for it in self.items)
        return aw, self.h

    def drawOn(self, c, x, y, _sW=0):
        yy = y + self.h
        for it, h in zip(self.items, self.hs):
            sb, sa = _spaces(it)
            yy -= sb + h
            it.drawOn(c, x, yy)
            yy -= sa


def _spaces(fl):
    st = getattr(fl, "style", None)
    if st is None:
        return 0.0, 0.0
    return getattr(st, "spaceBefore", 0.0), getattr(st, "spaceAfter", 0.0)


def _space(fl):
    a, b = _spaces(fl)
    return a + b


class SVGFlow(Flow):
    """A board diagram, drawn as vector at a fixed scale (1.0 = as designed)."""

    def __init__(self, doc, scale=1.0, gap_before=4.0, gap_after=3.0, max_w=None):
        self.doc = doc
        self.scale = scale
        w = doc["widthMm"] * MM * scale
        if max_w and w > max_w:
            self.scale = scale * max_w / w
            w = max_w
        self.w = w
        self.h = doc["heightMm"] * MM * self.scale
        self.gb, self.ga = gap_before, gap_after

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.h + self.gb + self.ga

    def drawOn(self, c, x, y, _sW=0):
        import svg_vector as sv
        cx = x + (getattr(self, "aw", self.w) - self.w) / 2.0
        sv.draw_reportlab(c, self.doc, cx, y + self.ga + self.h, self.w,
                          fonts=_SVG_FONTS)


_SVG_FONTS = dict()


def max_print_width(path, ppi=300.0):
    """Widest a raster may be printed, in points, without falling below `ppi`."""
    from reportlab.lib.utils import ImageReader
    return ImageReader(path).getSize()[0] / ppi * 72.0


class ImageFlow(Flow):
    def __init__(self, path, w, h=None, gap_after=4.0, frame=False):
        from reportlab.lib.utils import ImageReader
        self.reader = ImageReader(path)
        iw, ih = self.reader.getSize()
        self.w = w
        self.h = h if h else w * ih / iw
        self.ga = gap_after
        self.frame = frame

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.h + self.ga

    def drawOn(self, c, x, y, _sW=0):
        c.drawImage(self.reader, x, y + self.ga, self.w, self.h, preserveAspectRatio=True,
                    mask="auto")
        if self.frame:
            c.saveState()
            c.setLineWidth(0.4)
            c.rect(x, y + self.ga, self.w, self.h, stroke=1, fill=0)
            c.restoreState()


class Box(Flow):
    """A framed block of paragraphs (quick play, reconstruction notice).
    Not split: boxes are kept whole (they are short by design)."""

    def __init__(self, items, pad=6.0, rule_top=1.6, gap_after=6.0, title=None,
                 title_style=None, fill=None):
        self.items, self.pad, self.rule_top = items, pad, rule_top
        self.ga = gap_after
        self.title, self.tstyle, self.fill = title, title_style, fill

    def wrap(self, aw, ah):
        self.aw = aw
        iw = aw - 2 * self.pad
        self.hs = []
        tot = 0.0
        for it in self.items:
            h = it.wrap(iw, ah)[1]
            self.hs.append(h)
            tot += h + _space(it)
        self.h = tot + 2 * self.pad + self.rule_top
        return aw, self.h + self.ga

    def drawOn(self, c, x, y, _sW=0):
        y0 = y + self.ga
        c.saveState()
        if self.fill is not None:
            c.setFillGray(self.fill)
            c.rect(x, y0, self.aw, self.h, stroke=0, fill=1)
        c.setLineWidth(0.5)
        c.setStrokeGray(0)
        c.rect(x, y0, self.aw, self.h, stroke=1, fill=0)
        c.setLineWidth(self.rule_top)
        c.line(x, y0 + self.h - self.rule_top / 2, x + self.aw, y0 + self.h - self.rule_top / 2)
        c.restoreState()
        yy = y0 + self.h - self.rule_top - self.pad
        for it, h in zip(self.items, self.hs):
            sb, sa = _spaces(it)
            yy -= sb + h
            it.drawOn(c, x + self.pad, yy)
            yy -= sa


class Row(Flow):
    """Two blocks side by side (plate | quick-play box). Height = taller."""

    def __init__(self, left, right, gap, left_w, gap_after=8.0):
        self.left, self.right, self.gap, self.lw, self.ga = left, right, gap, left_w, gap_after

    def wrap(self, aw, ah):
        self.aw = aw
        rw = aw - self.lw - self.gap
        self.hl = self.left.wrap(self.lw, ah)[1]
        self.hr = self.right.wrap(rw, ah)[1]
        self.h = max(self.hl, self.hr)
        return aw, self.h + self.ga

    def drawOn(self, c, x, y, _sW=0):
        top = y + self.ga + self.h
        self.left.drawOn(c, x, top - self.hl)
        self.right.drawOn(c, x + self.lw + self.gap, top - self.hr)


class Anchor(Flow):
    """Zero-height marker: records the page a target falls on."""

    def __init__(self, key, sink):
        self.key, self.sink = key, sink

    def wrap(self, aw, ah):
        return aw, 0.0

    def drawOn(self, c, x, y, _sW=0):
        pass


class ColumnBreak(Flow):
    def wrap(self, aw, ah):
        return aw, 0.0

    def drawOn(self, c, x, y, _sW=0):
        pass


class PageEnd(ColumnBreak):
    """Ends the page being filled: what follows starts on the next page. Inserted only by
    _flow_even, to bring an entry's closing section onto a last page that would be empty."""


# ── page engine ──────────────────────────────────────────────────────────
class Page:
    __slots__ = ("items", "runHead", "folio", "blank", "kind", "opensSection", "anchors",
                 "bottomLines")

    def __init__(self, kind="body"):
        self.items = []          # (flowable, x, y_bottom, w)
        self.runHead = None
        self.folio = True
        self.blank = False
        self.kind = kind
        self.opensSection = False
        self.anchors = []
        self.bottomLines = []


class Region:
    def __init__(self, page, pno, x, y_top, w, h):
        self.page, self.pno, self.x, self.y_top, self.w, self.h = page, pno, x, y_top, w, h
        self.y = y_top

    @property
    def avail(self):
        return self.y - (self.y_top - self.h)


class Layout:
    def __init__(self, g, st):
        self.g, self.st = g, st
        self.pages = []
        self.anchors = {}

    @property
    def n(self):
        return len(self.pages)

    def new_page(self, kind="body", run_head=None):
        p = Page(kind)
        p.runHead = run_head
        self.pages.append(p)
        return p

    @staticmethod
    def is_verso(pno):
        return pno % 2 == 0

    def pad_to_verso(self):
        if (self.n + 1) % 2 != 0:
            p = self.new_page("blank")
            p.blank, p.folio = True, False

    def pad_to_recto(self):
        if (self.n + 1) % 2 != 1:
            p = self.new_page("blank")
            p.blank, p.folio = True, False

    def block(self, pno):
        """(x, y_top, w, h) of the text block on page `pno` (1-based)."""
        g = self.g
        x = g["outerPt"] if self.is_verso(pno) else g["gutterPt"]
        y_top = g["hPt"] - g["topPt"]
        return x, y_top, g["textWPt"], g["textHPt"]

    def columns(self, pno, top=0.0, bottom=0.0):
        x, y_top, w, h = self.block(pno)
        page = self.pages[pno - 1]
        if self.g["columns"] == 1:
            return [Region(page, pno, x, y_top - top, w, h - top - bottom)]
        cw = self.g["colWPt"]
        gap = self.g["colGapPt"]
        return [Region(page, pno, x, y_top - top, cw, h - top - bottom),
                Region(page, pno, x + cw + gap, y_top - top, cw, h - top - bottom)]

    def full(self, pno, top=0.0, bottom=0.0):
        x, y_top, w, h = self.block(pno)
        return Region(self.pages[pno - 1], pno, x, y_top - top, w, h - top - bottom)

    # -- placing -----------------------------------------------------------
    def place(self, reg, fl, h, w=None, commit=True):
        if commit:
            # nothing is ever set past the foot of its region (and so off the page)
            if h > reg.avail + 0.5:
                raise RuntimeError("placement past the foot of page %d: %s needs %.0f pt, %.0f pt left"
                                   % (reg.pno, type(fl).__name__, h, reg.avail))
            reg.page.items.append((fl, reg.x, reg.y - h, w or reg.w))
        reg.y -= h

    def fill(self, regions, flowables, record=True, commit=True):
        """Pour flowables into regions in order. Returns the leftover list.
        With commit=False nothing is placed: a dry run for balancing."""
        q = list(flowables)
        ri = 0
        while q and ri < len(regions):
            reg = regions[ri]
            fl = q[0]
            if isinstance(fl, PageEnd):
                q.pop(0)
                return q
            if isinstance(fl, ColumnBreak):
                q.pop(0)
                ri += 1
                continue
            if isinstance(fl, Anchor):
                q.pop(0)
                if commit:
                    reg.page.anchors.append(fl.key)
                    if record:
                        fl.sink[fl.key] = reg.pno
                continue
            sb, sa = _spaces(fl)
            at_top = abs(reg.y - reg.y_top) < 0.01
            sb_eff = 0.0 if at_top else sb
            avail = reg.avail - sb_eff
            w, h = fl.wrap(reg.w, max(avail, 1.0))
            need = h + sa
            # keep-with-next: a heading must not end a region
            if getattr(fl, "keep_next", False) and len(q) > 1:
                nxt = q[1]
                _, hn = nxt.wrap(reg.w, max(avail - need, 1.0))
                need_n = min(hn, _first_lines(nxt))
                if need + need_n > avail + 0.01 and not at_top:
                    ri += 1
                    continue
            if h <= avail + 0.01:
                reg.y -= sb_eff
                self.place(reg, fl, h, commit=commit)
                reg.y -= min(sa, max(reg.avail, 0.0))
                q.pop(0)
                continue
            parts = fl.split(reg.w, avail) if avail > 24 else []
            if parts and len(parts) > 1:
                q.pop(0)
                q[0:0] = parts
                continue
            if at_top and h > reg.h + 0.01:
                # a short region (columns under an opener band, or under floats) cannot hold it,
                # but a full column on a later page can. Only a flowable taller than a whole
                # page column can never be placed, and that is an error.
                if h > self.g["textHPt"] + 0.01:
                    raise RuntimeError("flowable taller than a whole page column (%.0f > %.0f pt): %s"
                                       % (h, self.g["textHPt"], type(fl).__name__))
            ri += 1
        return q


def _first_lines(fl, n=2):
    """Height of the first n lines of a paragraph (for keep-with-next)."""
    st = getattr(fl, "style", None)
    if st is not None and hasattr(st, "leading"):
        return st.leading * n + getattr(st, "spaceBefore", 0)
    return 30.0


# ═════════════════════════════════════════════════════════════════════════
# MANUSCRIPT → ENTRY MODEL
# ═════════════════════════════════════════════════════════════════════════
DIFF_LABEL = {1: "Very easy", 2: "Easy", 3: "Moderate", 4: "Demanding", 5: "Expert"}
FAMILY_ORDER = ["sowing", "hunt-siege", "race", "territory", "war-board", "chance", "boardless"]


def entry(g):
    """The one read path from a v2 game record to what is printed.

    Every printed string passes `text_of`, which refuses anything that is not
    a string. Missing mandatory blocks raise: a page must never quietly lose
    its setup or its end condition."""
    e = {}
    gid = g["gameId"]
    for k in ("title", "culture", "place", "period", "family", "objective", "atAGlance",
              "story", "materials", "firstGame"):
        if k not in g or g[k] in (None, ""):
            raise KeyError("%s: missing %s" % (gid, k))
        e[k] = text_of(g[k], "%s.%s" % (gid, k))
    e["gameId"] = gid
    sp = g["spec"]
    e["spec"] = {
        "players": text_of(sp["players"], gid + ".players"),
        "time": text_of(sp["time"], gid + ".time"),
        "age": text_of(sp["age"], gid + ".age"),
        "materials": text_of(sp["materials"], gid + ".materials"),
        "difficulty": int(sp["difficulty"]),
        "difficultyNote": text_of(sp.get("difficultyNote") or "", gid + ".difficultyNote"),
    }
    if not 1 <= e["spec"]["difficulty"] <= 5:
        raise ValueError("%s: difficulty must be 1–5" % gid)
    e["setup"] = [text_of(s, gid + ".setup") for s in g["setup"]]
    e["rules"] = [{"head": text_of(b["head"], gid + ".rules.head"),
                   "steps": [text_of(s, gid + ".rules.step") for s in b["steps"]]}
                  for b in g["rules"]]
    e["ending"] = {"end": text_of(g["ending"]["end"], gid + ".end"),
                   "winner": text_of(g["ending"]["winner"], gid + ".winner")}
    e["special"] = [{"q": text_of(x["q"], gid + ".q"), "a": text_of(x["a"], gid + ".a")}
                    for x in g["special"]]
    wt = g["workedTurn"]
    e["workedTurn"] = {k: (text_of(wt[k], gid + ".worked." + k) if k != "steps" else
                           [text_of(s, gid + ".worked.step") for s in wt.get("steps", [])])
                       for k in ("start", "steps", "result", "next") if wt.get(k)}
    e["workedTurn"]["diagram"] = wt.get("diagram")
    e["variants"] = [{"name": text_of(v["name"], gid + ".variant"),
                      "kind": v.get("kind", "recorded"),
                      "note": text_of(v["note"], gid + ".variant.note")}
                     for v in g.get("variants", [])]
    rc = g.get("reconstruction")
    e["reconstruction"] = ({"sources": text_of(rc["sources"], gid + ".recon"),
                            "book": text_of(rc["book"], gid + ".recon")} if rc else None)
    e["safety"] = text_of(g["safety"], gid + ".safety") if g.get("safety") else None
    e["gamblingNote"] = (text_of(g["gamblingNote"], gid + ".gambling")
                         if g.get("gamblingNote") else None)
    e["sources"] = [s if isinstance(s, dict) else {"work": s} for s in g["sources"]]
    for s in e["sources"]:
        text_of(s["work"], gid + ".source")
    e["rulings"] = [text_of(r, gid + ".ruling") for r in g.get("editorialRulings", [])]
    e["diagrams"] = g.get("diagrams", [])
    e["altNames"] = g.get("altNames", [])
    e["reconstructed"] = bool(g.get("reconstructed"))
    return e


def source_line(s):
    t = s["work"]
    if s.get("pages") and s["pages"] not in t:
        t = "%s, %s" % (t.rstrip("., "), s["pages"])
    return t.rstrip(".") + "."


def diff_dots(n, lp=False):
    return ("●" * n + "○" * (5 - n)) if not lp else "%d of 5" % n


# ═════════════════════════════════════════════════════════════════════════
# GAME ENTRY
# ═════════════════════════════════════════════════════════════════════════
def _P(st):
    from reportlab.platypus import Paragraph

    def P(t, s):
        return Paragraph(t, st[s])
    return P


def heading(st, text):
    from reportlab.platypus import Paragraph
    p = Paragraph(typo.xml_text(text.upper() if not st["_lp"] else text), st["h2"])
    p.keep_next = True
    return p


def numbered(st, items, start=1):
    from reportlab.platypus import Paragraph
    f = st["_fonts"]["sans_sb"]
    out = []
    for i, s in enumerate(items, start):
        out.append(Paragraph('<font name="%s">%d.</font>&nbsp;%s' % (f, i, rich(s)), st["step"]))
    return out


def with_heading(st, head, items):
    """A heading carries keep-with-next: it never ends a column alone."""
    return [heading(st, head)] + list(items)


def quick_box(e, st):
    P = _P(st)
    f = st["_fonts"]
    lab = lambda s: '<font name="%s">%s</font>' % (f["sans_b"], s)  # noqa: E731
    sp = e["spec"]
    lp = st["_lp"]
    d = sp["difficulty"]
    dots = diff_dots(d, lp)
    dnote = (" — %s" % rich(sp["difficultyNote"])) if sp["difficultyNote"] else ""
    items = [
        P(lab("QUICK PLAY" if not lp else "Quick play"), "qlabel"),
        VSpace(2.5),
        P("%s %s &nbsp;·&nbsp; %s %s &nbsp;·&nbsp; %s %s" % (
            lab("Players"), rich(sp["players"]), lab("Time"), rich(sp["time"]),
            lab("Age"), rich(sp["age"])), "qval"),
        VSpace(1.5),
        P("%s %s %s%s" % (lab("Difficulty"), dots, DIFF_LABEL[d], dnote), "qval"),
        VSpace(1.5),
        P("%s %s" % (lab("You need"), rich(sp["materials"])), "qval"),
        VSpace(1.5),
        P("%s %s" % (lab("Goal"), rich(e["objective"])), "qval"),
        VSpace(3.0),
        P(rich(e["atAGlance"]), "qbrief"),
    ]
    return Box(items, pad=6.5 if not lp else 9, rule_top=1.8, gap_after=0)


def opener_band(e, st, g, plate_path, family_label):
    P = _P(st)
    kick = "%s · %s · %s" % (rich(e["culture"]), rich(e["place"]), rich(e["period"]))
    band = [P(rich(e["title"]), "gtitle"), P(kick, "kicker"), Rule(0.6, 4.0, 7.0)]
    qb = quick_box(e, st)
    # every plate says what it is: an AI-generated illustration, a public-domain source, or a drawn board
    cap = e.get("plateCaption")
    if g["columns"] == 2 and plate_path:
        plate = ImageFlow(plate_path, g["colWPt"], gap_after=0)
        left = Bound([plate, P(rich(cap), "platecap")]) if cap else plate
        band.append(Row(left, qb, g["colGapPt"], g["colWPt"], gap_after=9.0))
    else:
        if plate_path:
            # never wider than the file allows at 300 ppi (KDP's print minimum)
            w = min(g["textWPt"] * (0.8 if g["largePrint"] else 1.0), max_print_width(plate_path))
            band.append(ImageFlow(plate_path, w, gap_after=0.0 if cap else 8.0))
            if cap:
                band += [P(rich(cap), "platecap"), VSpace(8.0)]
        band += [qb, VSpace(9.0)]
    return band


def entry_body(e, st, g, diagrams, floats):
    """The two-column body of an entry, in reading order.

    `diagrams`: id → (doc, caption). Diagrams wider than a column go to
    `floats` (placed full-width at the top of the next page); the rest sit
    in the column where the text refers to them."""
    P = _P(st)
    f = st["_fonts"]
    b = []
    colw = g["colWPt"]

    def put_diagram(did):
        if did not in diagrams:
            return
        doc, cap = diagrams.pop(did)
        k = 1.0 if not g["largePrint"] else 1.0
        fl = SVGFlow(doc, scale=k, gap_before=5.0, gap_after=2.0, max_w=g["textWPt"])
        capp = P(rich(cap), "caption") if cap else None
        if fl.w > colw + 0.5 and g["columns"] == 2:
            floats.append((fl, capp))
        else:
            if fl.w > colw:
                fl = SVGFlow(doc, scale=k * colw / fl.w, gap_before=5.0, gap_after=2.0)
            b.append(Bound([fl, capp]) if capp else fl)

    b += with_heading(st, "Background", [P(rich(e["story"]), "story")])
    b += with_heading(st, "What you need", [P(rich(e["materials"]), "body")])
    if e["safety"]:
        b.append(P('<font name="%s">Safety.</font> %s' % (f["sans_b"], rich(e["safety"])),
                   "notice"))
    if e["gamblingNote"]:
        b.append(P('<font name="%s">Stakes.</font> %s' % (f["sans_b"], rich(e["gamblingNote"])),
                   "notice"))
    if e["reconstruction"]:
        rc = e["reconstruction"]
        b.append(Box([P('<font name="%s">%s</font>' % (f["sans_b"], "RECONSTRUCTION" if not st["_lp"]
                                                        else "Reconstruction"), "qlabel"),
                      VSpace(2.0),
                      P('<font name="%s">What the sources give.</font> %s'
                        % (f["sans_b"], rich(rc["sources"])), "notice"),
                      P('<font name="%s">What this book supplies.</font> %s'
                        % (f["sans_b"], rich(rc["book"])), "notice")],
                     pad=6.0, rule_top=1.2, gap_after=7.0))
    b += with_heading(st, "Setup", numbered(st, e["setup"]))
    ids = list(e["diagrams"])
    worked_id = e["workedTurn"].get("diagram")
    main_ids = [d for d in ids if d != worked_id]
    if main_ids:
        put_diagram(main_ids[0])
    for blk in e["rules"]:
        b += with_heading(st, blk["head"], numbered(st, blk["steps"]))
    for d in main_ids[1:]:
        put_diagram(d)
    b += with_heading(st, "Ending and winning",
                      [P('<font name="%s">The end.</font> %s' % (f["sans_b"], rich(e["ending"]["end"])),
                         "body"),
                       P('<font name="%s">The winner.</font> %s' % (f["sans_b"],
                                                                    rich(e["ending"]["winner"])),
                         "body")])
    qa = [P('<font name="%s">%s.</font> %s' % (f["sans_b"], rich(x["q"].rstrip(".?")),
                                                 rich(x["a"])), "qa") for x in e["special"]]
    b += with_heading(st, "Special situations", qa)
    wt = e["workedTurn"]
    wl = []
    if wt.get("start"):
        wl.append(P('<font name="%s">Start.</font> %s' % (f["sans_b"], rich(wt["start"])), "body"))
    wl += numbered(st, wt.get("steps", []))
    if wt.get("result"):
        wl.append(P('<font name="%s">Result.</font> %s' % (f["sans_b"], rich(wt["result"])), "body"))
    if wt.get("next"):
        wl.append(P('<font name="%s">Next.</font> %s' % (f["sans_b"], rich(wt["next"])), "body"))
    b += with_heading(st, "A worked turn", wl)
    if worked_id:
        put_diagram(worked_id)
    b += with_heading(st, "Your first game", [P(rich(e["firstGame"]), "body")])
    if e["variants"]:
        vl = []
        for v in e["variants"]:
            tag = " <i>(house rule)</i>" if v["kind"] == "house rule" and not st["_lp"] else \
                (" (house rule)" if v["kind"] == "house rule" else "")
            vl.append(P('<font name="%s">%s</font>%s. %s' % (f["sans_b"], rich(v["name"]), tag,
                                                             rich(v["note"])), "body"))
        b += with_heading(st, "Variants", vl)
    srcs = [P(rich(source_line(s)), "source") for s in e["sources"]]
    if e["rulings"]:
        srcs.append(P('<font name="%s">†</font> This book’s own rulings, where the sources are '
                      'silent: %s' % (f["sans_b"], " ".join(rich(r) for r in e["rulings"])),
                      "source"))
    b += with_heading(st, "Sources", srcs)
    # any diagram not yet placed (defensive: nothing is ever dropped)
    for d in list(diagrams):
        put_diagram(d)
    return b


def tight_styles(st, f=0.62):
    """The same styles with vertical space reduced — tried before an entry
    is allowed to spill from two pages to four."""
    import copy
    t = dict(st)
    for k, v in st.items():
        if hasattr(v, "spaceBefore"):
            s2 = copy.copy(v)
            s2.spaceBefore = v.spaceBefore * f
            s2.spaceAfter = v.spaceAfter * f
            if k in ("body", "story", "step", "qa"):
                s2.leading = v.leading * 0.975
            t[k] = s2
    return t


def _flow_pages(lay, first_pno, band, body, floats, balance=True, max_pages=None,
                run_heads=("", ""), commit=True):
    """Lay an entry out from page `first_pno` (already created, empty).
    Returns number of pages used, or None if max_pages was exceeded (dry)."""
    pno = first_pno
    full = lay.full(pno)
    lay.fill([full], band, commit=commit)
    used_top = full.y_top - full.y
    q = list(body)
    pages = 1
    fl_q = list(floats)
    top = used_top
    while True:
        # floats go at the top of every page after the first, while they last
        if pages > 1 and fl_q:
            reg = lay.full(pno)
            t = 0.0
            while fl_q:
                fl, cap = fl_q[0]
                h = fl.wrap(reg.w, reg.h)[1] + (cap.wrap(reg.w, reg.h)[1] + _space(cap) if cap else 0)
                if t + h > reg.h * 0.62 and t > 0:
                    break
                fl_q.pop(0)
                reg.y = reg.y_top - t
                lay.place(reg, fl, fl.wrap(reg.w, reg.h)[1], commit=commit)
                if cap:
                    ch = cap.wrap(reg.w, reg.h)[1]
                    lay.place(reg, cap, ch, commit=commit)
                t += h
            top = t + 6.0
        cols = lay.columns(pno, top=top)
        last_try = q
        if balance and g_is_two(lay):
            # would everything that is left fit on this page? then balance
            probe = lay.columns(pno, top=top)
            left = lay.fill(probe, list(q), commit=False)
            if not left and not fl_q:
                cap = _balance_cap(lay, pno, top, q)
                cols = lay.columns(pno, top=top, bottom=max(0.0, probe[0].h - cap))
        q = lay.fill(cols, q, commit=commit)
        if not q and not fl_q:
            return pages
        if max_pages and pages >= max_pages:
            return None
        pages += 1
        if commit:
            lay.new_page("game", run_head=run_heads[(pages - 1) % 2])
        else:
            lay.pages.append(Page("game"))
        pno += 1
        top = 0.0


def g_is_two(lay):
    return lay.g["columns"] == 2


def _balance_cap(lay, pno, top, q):
    """Smallest column height that still holds everything left (binary search)."""
    H0 = lay.columns(pno, top=top)[0].h
    lo, hi = 20.0, H0
    for _ in range(16):
        mid = (lo + hi) / 2
        regs = lay.columns(pno, top=top, bottom=H0 - mid)
        left = lay.fill(regs, list(q), commit=False)
        if left:
            lo = mid
        else:
            hi = mid
    return min(H0, hi + 2.0)


def layout_game(lay, e, st, diagram_docs, plate_path, family_label, anchors):
    """A game entry: starts on a verso; two pages, or four if it must."""
    g = lay.g
    heads = (family_label, e["title"])
    if g["largePrint"]:
        # large print: one column, starts on a new page (either side), no spread
        first = lay.n + 1
        lay.new_page("game", run_head=e["title"])
        anchors["game:" + e["gameId"]] = first
        floats = []
        diags = {d: diagram_docs[d] for d in e["diagrams"] if d in diagram_docs}
        body = opener_band(e, st, g, plate_path, family_label) + entry_body(e, st, g, diags, floats)
        q = body
        pno = first
        while True:
            q = lay.fill(lay.columns(pno), q)
            if not q:
                break
            lay.new_page("game", run_head=e["title"])
            pno += 1
        return lay.n - first + 1, "lp"

    lay.pad_to_verso()
    first = lay.n + 1
    attempts = [("normal", st, True), ("tight", tight_styles(st), True)]
    result = None
    for mode, stx, bal in attempts:
        floats = []
        diags = {d: diagram_docs[d] for d in e["diagrams"] if d in diagram_docs}
        band = opener_band(e, stx, g, plate_path, family_label)
        body = entry_body(e, stx, g, diags, floats)
        # dry run on scratch pages
        n0 = lay.n
        lay.pages.append(Page("game"))
        used = _flow_pages(lay, first, band, body, floats, max_pages=2, commit=False)
        del lay.pages[n0:]
        if used is not None:
            result = (mode, stx)
            break
    if result is None:
        result = ("four", st)
    mode, stx = result
    floats = []
    diags = {d: diagram_docs[d] for d in e["diagrams"] if d in diagram_docs}
    band = opener_band(e, stx, g, plate_path, family_label)
    body = entry_body(e, stx, g, diags, floats)
    lay.new_page("game", run_head=heads[0])
    anchors["game:" + e["gameId"]] = first
    used = _flow_pages(lay, first, band, body, floats, run_heads=heads)
    if used % 2:
        # an entry never ends on a verso with a blank recto beside it: the
        # recto becomes this game's own notes page is NOT done — instead the
        # entry is re-flowed over an even number of pages with balanced text.
        del lay.pages[first - 1:]
        lay.new_page("game", run_head=heads[0])
        floats = []
        diags = {d: diagram_docs[d] for d in e["diagrams"] if d in diagram_docs}
        band = opener_band(e, st, g, plate_path, family_label)
        body = entry_body(e, st, g, diags, floats)
        used = _flow_even(lay, first, band, body, floats, heads, used + 1)
        mode = mode + "+even"
    return used, mode


def _flow_even(lay, first, band, body, floats, heads, target):
    """Flow an entry over exactly `target` pages, spreading the text so the
    last two pages carry it evenly (no blank page, no single orphan page)."""
    # binary search a height cap for all pages after the first spread
    full_h = lay.columns(first)[0].h
    # the target grows by a spread while the entry (its floats included) cannot fit: nothing
    # may be left unplaced, and nothing may be placed past the foot of a page
    for tgt in range(target, target + 8, 2):
        n0 = lay.n
        fits = _try_capped(lay, first, band, body, floats, full_h, tgt, commit=False)
        del lay.pages[n0:]
        if fits:
            target = tgt
            break
    else:
        raise RuntimeError("entry cannot be laid out over %d–%d pages" % (target, target + 6))

    def search(hold, body=body):
        # the smallest cap that still fits: the text of the last pages is shared out evenly
        # (a floor of 30 % once left the last page of some entries with nothing on it)
        lo, hi = full_h * 0.02, full_h
        best = None
        for _ in range(16):
            mid = (lo + hi) / 2
            n0 = lay.n
            ok = _try_capped(lay, first, band, body, floats, mid, target, commit=False,
                             hold_last_float=hold)
            del lay.pages[n0:]
            if ok:
                best, hi = mid, mid
            else:
                lo = mid
        return best

    def fits_at(cap, hold, body=body):
        n0 = lay.n
        ok = _try_capped(lay, first, band, body, floats, cap, target, commit=False,
                         hold_last_float=hold)
        del lay.pages[n0:]
        return ok

    def last_empty(cap, hold, body=body):
        rep = {}
        n0 = lay.n
        _try_capped(lay, first, band, body, floats, cap, target, commit=False, report=rep,
                    hold_last_float=hold)
        del lay.pages[n0:]
        return rep.get("lastEmpty", False)

    hold = False
    best = search(False) or full_h
    if last_empty(best, False) and floats and fits_at(full_h, True):
        # nothing reached the last page: keep the last diagram back for it
        cap2 = search(True)
        if cap2 is not None and not last_empty(cap2, True):
            hold, best = True, cap2
    if last_empty(best, hold):
        # still empty (the diagrams sit in the columns, and a column cannot be cut below a
        # diagram's height): start the entry's closing section on the last page instead
        heads_at = [i for i, fl in enumerate(body)
                    if getattr(getattr(fl, "style", None), "name", "") == "h2"]
        for i in reversed(heads_at[-3:]):
            body2 = body[:i] + [PageEnd()] + body[i:]
            if not fits_at(full_h, hold, body2):
                continue
            cap2 = search(hold, body2)
            if cap2 is not None and not last_empty(cap2, hold, body2):
                body, best = body2, cap2
                break
    # commit with the best cap
    _try_capped(lay, first, band, body, floats, best, target, commit=True, heads=heads,
                hold_last_float=hold)
    return lay.n - first + 1


def _try_capped(lay, first, band, body, floats, cap, target, commit, heads=("", ""), report=None,
                hold_last_float=False):
    # rebuild fresh flowables each time (Paragraph.split state is not shared)
    pno = first
    full = lay.full(pno)
    if not commit:
        lay.pages.append(Page("game"))
    lay.fill([full], band, commit=commit)
    top = full.y_top - full.y
    q = list(body)
    fl_q = list(floats)
    for i in range(target):
        if i > 0:
            if commit:
                lay.new_page("game", run_head=heads[i % 2])
            else:
                lay.pages.append(Page("game"))
            pno += 1
            top = 0.0
            reg = lay.full(pno)
            t = 0.0
            while fl_q:
                if hold_last_float and len(fl_q) == 1 and i < target - 1:
                    break                       # the last diagram waits for the last page
                fl, capp = fl_q[0]
                h = fl.wrap(reg.w, reg.h)[1]
                ch = (capp.wrap(reg.w, reg.h)[1] + _space(capp)) if capp else 0.0
                # the same rule as the normal flow: a second float only while the page keeps
                # room for text; the rest wait for the next page
                if t > 0 and t + h + ch > reg.h * 0.62:
                    break
                fl_q.pop(0)
                reg.y = reg.y_top - t
                lay.place(reg, fl, h, commit=commit)
                t += h
                if capp:
                    lay.place(reg, capp, capp.wrap(reg.w, reg.h)[1], commit=commit)
                    t += ch
            top = t + (6.0 if t else 0.0)
        cols = lay.columns(pno, top=top)
        colh = cols[0].h
        if i >= 2:
            cols = lay.columns(pno, top=top, bottom=max(0.0, colh - cap))
        before = list(q)
        q = lay.fill(cols, q, commit=commit)
        if report is not None and i == target - 1:
            text_here = bool(before) and (len(q) < len(before) or (q and q[0] is not before[0]))
            report["lastEmpty"] = not (text_here or (i > 0 and top > 0.0))
    return not q and not fl_q


# ═════════════════════════════════════════════════════════════════════════
# FRONT MATTER · FAMILY OPENERS · BACK MATTER
# ═════════════════════════════════════════════════════════════════════════
def ed_text(v, edition):
    """Edition-aware text: a string, or {"default": …, "largeprint": …, "kindle": …}."""
    if isinstance(v, dict):
        for k in (edition, "print" if edition in ("paperback", "hardcover", "largeprint") else None,
                  "default"):
            if k and k in v:
                return text_of(v[k], "edition text")
        raise KeyError("no text for edition %s" % edition)
    return text_of(v, "front/back text")


class PageRef:
    """Resolves {page:key} placeholders against the anchor map of pass 1."""

    def __init__(self, anchors):
        self.anchors = anchors or {}

    def __call__(self, s):
        def rep(m):
            v = self.anchors.get(m.group(1))
            return str(v) if v else "000"
        return re.sub(r"\{page:([^}]+)\}", rep, s)


def table_flow(rows, col_w, st, header=None, zebra=False, font_size=None):
    """A simple ruled table (reportlab Table) that splits across regions."""
    from reportlab.platypus import Table, TableStyle, Paragraph
    data = []
    if header:
        data.append([Paragraph(h, st["cellb"]) for h in header])
    for r in rows:
        data.append([c if not isinstance(c, str) else Paragraph(c, st["cell"]) for c in r])
    t = Table(data, colWidths=col_w, repeatRows=1 if header else 0)
    cmds = [("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 2.5), ("RIGHTPADDING", (0, 0), (-1, -1), 2.5),
            ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
            ("LINEBELOW", (0, 0), (-1, -1), 0.3, (0.55, 0.55, 0.55))]
    if header:
        cmds += [("LINEBELOW", (0, 0), (-1, 0), 0.9, (0, 0, 0))]
    t.setStyle(TableStyle(cmds))
    return t


def family_glance(fam, games, st, g, pages):
    P = _P(st)
    rows = []
    for e in games:
        pg = pages.get("game:" + e["gameId"], "000")
        rows.append(["<b>%s</b><br/>%s" % (rich(e["title"]), rich(e["culture"])),
                     rich(e["spec"]["players"]), rich(e["spec"]["time"]),
                     rich(e["spec"]["age"]),
                     diff_dots(e["spec"]["difficulty"], st["_lp"]) if not st["_lp"]
                     else "%d of 5" % e["spec"]["difficulty"],
                     str(pg)])
    W = g["textWPt"]
    cw = [W * 0.34, W * 0.14, W * 0.17, W * 0.12, W * 0.13, W * 0.10]
    return table_flow(rows, cw, st, header=["Game", "Players", "Time", "Age", "Difficulty", "Page"])


def layout_family_opener(lay, o, games, st, anchors, pages, edition):
    P = _P(st)
    g = lay.g
    if not g["largePrint"]:
        lay.pad_to_verso()
    first = lay.n + 1
    p = lay.new_page("opener", run_head=None)
    p.opensSection = True
    anchors["part:" + o["family"]] = first
    band = [P("PART %s" % o["numeral"] if not st["_lp"] else "Part %s" % o["numeral"], "part"),
            P(rich(o["title"]), "sect"), P(rich(o["standfirst"]), "stand"), Rule(0.8, 2.0, 8.0)]
    body = [P(rich(ed_text(para, edition)), "fm") for para in o["paragraphs"]]
    glance = [heading(st, "The family at a glance"),
              P(rich(ed_text(o.get("glanceNote", "Every game in this part, with the page it "
                                   "starts on. Difficulty measures how much there is to learn, "
                                   "not how deep the game goes (see How to Use This Book)."),
                             edition)), "small"),
              family_glance(o["family"], games, st, g, pages)]
    q = lay.fill([lay.full(first)], band)
    top = lay.block(first)[3] - (lay.full(first).h) if False else 0
    full = lay.full(first)
    used = sum(fl.wrap(full.w, full.h)[1] + _space(fl) for fl in band)
    q = lay.fill(lay.columns(first, top=used), body)
    pno = first
    while q:
        lay.new_page("opener", run_head=o["title"])
        pno += 1
        q = lay.fill(lay.columns(pno), q)
    # the at-a-glance table on the facing page (or continuing)
    lay.new_page("opener", run_head=o["title"])
    pno += 1
    q = lay.fill([lay.full(pno)], glance)
    while q:
        lay.new_page("opener", run_head=o["title"])
        pno += 1
        q = lay.fill([lay.full(pno)], q)
    if not g["largePrint"] and (lay.n - first + 1) % 2:
        # openers are spreads: pad inside the part, never with a blank verso later
        pp = lay.new_page("blank")
        pp.blank, pp.folio = True, False


def layout_section(lay, title, flowables, run_head, anchors, key, st, new_page=True,
                   recto=False, columns=1):
    P = _P(st)
    if recto:
        lay.pad_to_recto()
    first = lay.n + 1
    p = lay.new_page("front" if key.startswith("fm:") else "back", run_head=run_head)
    p.opensSection = True
    anchors[key] = first
    band = [P(rich(title), "sect")]
    full = lay.full(first)
    q = lay.fill([full], band)
    used = full.y_top - full.y
    regs = lay.columns(first, top=used) if columns == 2 else [lay.full(first, top=used)]
    q = lay.fill(regs, flowables)
    pno = first
    while q:
        lay.new_page(p.kind, run_head=run_head)
        pno += 1
        regs = lay.columns(pno) if columns == 2 else [lay.full(pno)]
        q = lay.fill(regs, q)
    return first


# ── indexes (built from the manuscript, never typed) ─────────────────────
AGE_BUCKETS = [(4, "Age 4 and up"), (6, "Age 6 and up"), (8, "Age 8 and up"),
               (10, "Age 10 and up"), (12, "Age 12 and up")]
TIME_BUCKETS = [(15, "Up to 15 minutes"), (30, "15 to 30 minutes"), (60, "30 minutes to an hour"),
                (10 ** 6, "More than an hour")]
PLAYER_BUCKETS = [("2", "Two players"), ("3-4", "Three or four"), ("5+", "Five or more")]


def _range(spec, lo_key, hi_key, text_key):
    lo, hi = spec.get(lo_key), spec.get(hi_key)
    if lo is None:
        nums = [int(x) for x in re.findall(r"\d+", spec.get(text_key, ""))]
        lo = nums[0] if nums else 0
        hi = nums[-1] if nums else lo
    if hi is None:
        hi = 99
    return int(lo), int(hi)


def player_buckets(sp):
    lo, hi = _range(sp, "playersMin", "playersMax", "players")
    out = []
    if lo <= 2 <= hi:
        out.append("2")
    if lo <= 4 and hi >= 3:
        out.append("3-4")
    if hi >= 5:
        out.append("5+")
    if lo == 1 and "2" not in out:
        out.append("2")
    return out


def time_bucket_keys(sp):
    lo, hi = _range(sp, "timeMin", "timeMax", "time")
    keys, prev = [], 0
    for lim, lbl in TIME_BUCKETS:
        if lo <= lim and hi > prev:
            keys.append(lbl)
        prev = lim
    return keys or [TIME_BUCKETS[0][1]]


def age_bucket(sp):
    a = sp.get("ageMin")
    if a is None:
        nums = [int(x) for x in re.findall(r"\d+", sp.get("age", ""))]
        a = nums[0] if nums else 8
    best = AGE_BUCKETS[0][1]
    for lim, lbl in AGE_BUCKETS:
        if a >= lim:
            best = lbl
    return best


def a_to_z(games):
    """Titles and every alternate name, alphabetised; names point to titles."""
    rows = []
    for e in games:
        rows.append((plain(e["title"]), e["gameId"], None))
        for a in e.get("altNames") or []:
            nm = a["name"] if isinstance(a, dict) else a
            note = a.get("note") if isinstance(a, dict) else None
            if nm.strip().lower() == e["title"].strip().lower():
                continue
            rows.append((plain(nm), e["gameId"], note))

    def key(r):
        s = r[0].lower()
        s = re.sub(r"^(the|a|an) ", "", s)
        import unicodedata
        return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return sorted(rows, key=key)


def build_index_flow(games, st, pages, titles):
    P = _P(st)
    out = []
    letter = None
    import unicodedata
    for name, gid, note in a_to_z(games):
        base = re.sub(r"^(the|a|an) ", "", name.lower())
        first = unicodedata.normalize("NFD", base)[:1].upper()
        if first != letter:
            letter = first
            h = P(letter, "idxh")
            h.keep_next = True
            out.append(h)
        pg = pages.get("game:" + gid, "000")
        if titles[gid] == name:
            out.append(P("<b>%s</b> &nbsp;%s" % (rich(name), pg), "idx"))
        else:
            out.append(P("%s <i>see</i> %s %s" % (rich(name), rich(titles[gid]), pg), "idx"))
    return out


def bucket_index(games, st, pages, keyfn, order):
    P = _P(st)
    buckets = {k: [] for k in order}
    for e in games:
        for k in keyfn(e):
            buckets.setdefault(k, []).append(e)
    out = []
    for k in order:
        if not buckets.get(k):
            continue
        h = P(rich(k), "idxh")
        h.keep_next = True
        out.append(h)
        for e in sorted(buckets[k], key=lambda x: plain(x["title"]).lower()):
            out.append(P("%s &nbsp;%s" % (rich(e["title"]), pages.get("game:" + e["gameId"], "000")),
                         "idx"))
    return out


def tonight_table(games, st, g, pages):
    """Players × time grid: every game appears in every cell its ranges touch."""
    P = _P(st)
    grid = {}
    for e in games:
        for pb in player_buckets(e["spec"]):
            for tb in time_bucket_keys(e["spec"]):
                grid.setdefault((tb, pb), []).append(e)
    def cell_text(tlbl, pk):
        cell = grid.get((tlbl, pk), [])
        return ", ".join("%s&nbsp;%s" % (rich(e["title"]), pages.get("game:" + e["gameId"], "000"))
                         for e in sorted(cell, key=lambda x: plain(x["title"]).lower())) or "—"
    if g["largePrint"]:
        # at large-print sizes one grid cell can be taller than a page, and a table row
        # cannot split: the same grid is set as headed lists, which flow from page to page
        fl = []
        for _, tlbl in TIME_BUCKETS:
            hh = P(rich(tlbl), "fmh")
            hh.keep_next = True
            fl.append(hh)
            for pk, plbl in PLAYER_BUCKETS:
                fl.append(P("<b>%s:</b> %s" % (rich(plbl), cell_text(tlbl, pk)), "fm"))
        return fl
    rows = []
    for _, tlbl in TIME_BUCKETS:
        rows.append(["<b>%s</b>" % tlbl] + [cell_text(tlbl, pk) for pk, _ in PLAYER_BUCKETS])
    W = g["textWPt"]
    return [table_flow(rows, [W * 0.16, W * 0.36, W * 0.26, W * 0.22], st,
                       header=["", "Two players", "Three or four", "Five or more"])]


# ═════════════════════════════════════════════════════════════════════════
# THE WHOLE BOOK
# ═════════════════════════════════════════════════════════════════════════
def build_layout(ctx, g, st, pages_in=None):
    """One pass over the whole book. `pages_in` = anchors of the previous
    pass (None on the first pass → page numbers print as 000)."""
    P = _P(st)
    edition = g["edition"]
    fm, bm = ctx["fm"], ctx["bm"]
    games = ctx["entries"]
    by_id = {e["gameId"]: e for e in games}
    titles = {e["gameId"]: plain(e["title"]) for e in games}
    pages = pages_in or {}
    ref = PageRef(pages)
    lay = Layout(g, st)
    anchors = {}
    tp, im = fm["titlePage"], fm["imprint"]

    # ① half title
    p = lay.new_page("front")
    p.folio = False
    x, y_top, w, h = lay.block(1)
    reg = Region(p, 1, x, y_top - h * 0.30, w, h * 0.7)
    lay.fill([reg], [P(rich(tp["title"]), "title")])
    if not g["largePrint"]:
        q = lay.new_page("blank")
        q.blank, q.folio = True, False

    # ② title page
    pno = lay.n + 1
    p = lay.new_page("front")
    p.folio = False
    x, y_top, w, h = lay.block(pno)
    reg = Region(p, pno, x, y_top - h * 0.16, w, h * 0.84)
    items = [P(rich(tp["title"]), "title"), P(rich(tp["subtitle"]), "subtitle")]
    if g.get("editionLabel") and g["largePrint"]:
        items.append(P("<b>%s</b>" % rich(g["editionLabel"]), "subtitle"))
    items += [VSpace(30), P(rich(tp["author"]), "author"), VSpace(h * 0.34),
              P(rich(tp["publisher"]), "subtitle")]
    lay.fill([reg], items)

    # ③ imprint
    pno = lay.n + 1
    p = lay.new_page("front")
    p.folio = False
    lines = [rich(tp["title"]), rich(tp["subtitle"]), "", rich(im["copyright"]),
             rich(im["publisher"]), "", "%s · Volume %s" % (rich(tp["series"]), tp["volume"]),
             rich(ed_text(im["edition"], edition)), rich(im["printedBy"]), ""]
    isbn = im["isbn"]
    if edition == "largeprint":
        lines.append("ISBN (large print paperback): %s" % isbn["largeprint"])
    else:
        lines += ["ISBN (paperback): %s" % isbn["paperback"], "ISBN (hardcover): %s" % isbn["hardcover"]]
    lines += ["", rich(ed_text(im["rights"], edition)), "", rich(ed_text(im["aiDisclosure"], edition))]
    for extra in im.get("extra", []):
        lines += ["", rich(ed_text(extra, edition))]
    fl = [P(ln or "&nbsp;", "small") for ln in lines]
    x, y_top, w, h = lay.block(pno)
    reg = Region(p, pno, x, y_top - h * 0.22, w, h * 0.78)
    left = lay.fill([reg], fl)
    while left:
        q = lay.new_page("front")
        q.folio = False
        left = lay.fill([lay.full(lay.n)], left)

    # ④ contents (two columns)
    toc = []
    for s in fm["sections"]:
        if s.get("toc", True):
            toc.append(P("%s &nbsp;<font name='%s'>%s</font>" % (rich(s["title"]), st["_fonts"]["sans"],
                                                               pages.get("fm:" + s["id"], "000")), "toc"))
    for item in fm["contents"]:
        if item["kind"] == "family-opener":
            o = next(x for x in fm["familyOpeners"] if x["family"] == item["family"])
            hh = P("%s &nbsp;%s &nbsp;<font name='%s'>%s</font>" % (
                "Part %s" % o["numeral"], rich(o["title"]), st["_fonts"]["sans"],
                pages.get("part:" + o["family"], "000")), "tocfam")
            hh.keep_next = True
            toc.append(hh)
        else:
            e = by_id[item["gameId"]]
            toc.append(P("%s <font name='%s' size='%s'>· %s</font> &nbsp;<font name='%s'>%s</font>" % (
                rich(e["title"]), st["_fonts"]["sans_i"], 14 if st["_lp"] else 8, rich(e["culture"]),
                st["_fonts"]["sans"], pages.get("game:" + e["gameId"], "000")), "toc"))
    hh = P("At the back", "tocfam")
    hh.keep_next = True
    toc.append(hh)
    for key, label in ctx["backToc"]:
        toc.append(P("%s &nbsp;<font name='%s'>%s</font>" % (rich(label), st["_fonts"]["sans"],
                                                           pages.get(key, "000")), "toc"))
    if not g["largePrint"]:
        lay.pad_to_recto()
    layout_section(lay, "Contents", toc, "Contents", anchors, "fm:contents", st,
                   columns=1 if g["largePrint"] else 2)

    # ⑤ front-matter essays
    for s in fm["sections"]:
        fl = []
        for para in s.get("paragraphs", []):
            fl.append(P(rich(ref(ed_text(para, edition))), "fm"))
        for sub in s.get("sections", []):
            if "heading" not in sub:          # an edition-specific block
                sub = sub.get(edition) or sub.get(
                    "print" if edition in ("paperback", "hardcover", "largeprint") else "kindle")
                if not sub:
                    continue
            hh = P(rich(sub["heading"]), "fmh")
            hh.keep_next = True
            fl += [hh, P(rich(ref(ed_text(sub["text"], edition))), "fm")]
        for row in s.get("table") or []:
            hh = P("%s · %s" % (rich(row["n"]), rich(row["name"])), "fmh")
            hh.keep_next = True
            fl += [hh, P("%s <i>%s</i>" % (rich(row["idea"]), rich(row["test"])), "fm")]
        if s.get("closing"):
            fl.append(P(rich(ref(ed_text(s["closing"], edition))), "fm"))
        if s["id"] == "tonight":
            fl.append(VSpace(4))
            fl += tonight_table(games, st, g, pages)
        layout_section(lay, s["title"], fl, s["title"], anchors, "fm:" + s["id"], st)
    front_pages = lay.n

    # ⑥ body
    spreads, modes = [], {}
    plates = ctx["plates"]
    docs = ctx["diagramDocs"]
    for item in fm["contents"]:
        if item["kind"] == "family-opener":
            o = next(x for x in fm["familyOpeners"] if x["family"] == item["family"])
            fam_games = [by_id[c["gameId"]] for c in fm["contents"]
                         if c["kind"] == "game" and c["family"] == item["family"]]
            layout_family_opener(lay, o, fam_games, st, anchors, pages, edition)
            fam_label = "%s · %s" % (o["numeral"], plain(o["title"]))
            continue
        e = by_id[item["gameId"]]
        first = lay.n + 1
        used, mode = layout_game(lay, e, st, docs, plates.get(e["gameId"]), fam_label, anchors)
        first = anchors["game:" + e["gameId"]]
        spreads.append((e["gameId"], first, lay.n - first + 1))
        modes[e["gameId"]] = mode
    body_end = lay.n

    # ⑦ back matter
    back_start = lay.n + 1
    layout_back(lay, ctx, st, anchors, pages, titles)

    if lay.n % 2:
        q = lay.new_page("blank")
        q.blank, q.folio = True, False
    return lay, {"anchors": anchors, "spreads": spreads, "modes": modes,
                 "frontPages": front_pages, "bodyEnd": body_end, "backStart": back_start}


def layout_back(lay, ctx, st, anchors, pages, titles):
    P = _P(st)
    g = lay.g
    edition = g["edition"]
    bm = ctx["bm"]
    games = ctx["entries"]
    # templates
    tpls = ctx["templates"]
    if tpls:
        intro = [P(rich(ed_text(bm["templatesIntro"], edition)), "fm")]
        rows = [["<b>%s</b>" % rich(t["title"]), ", ".join(rich(titles[x]) for x in t["games"]),
                 "{page:tpl:%s}" % t["id"]] for t in tpls]
        rows = [[r[0], r[1], PageRef(pages)(r[2])] for r in rows]
        W = g["textWPt"]
        intro.append(table_flow(rows, [W * 0.34, W * 0.52, W * 0.14], st,
                                header=["Board", "For", "Page"]))
        if bm.get("kit"):
            hh = heading(st, "Build a games kit")
            intro += [hh, P(rich(ed_text(bm["kitIntro"], edition)), "body")]
            krows = [[rich(k["item"]), rich(k["quantity"]), rich(k["games"])] for k in bm["kit"]]
            intro.append(table_flow(krows, [W * 0.28, W * 0.18, W * 0.54], st,
                                    header=["What", "How many", "Games it opens"]))
        layout_section(lay, bm.get("templatesTitle", "Full-Size Boards"), intro,
                       "Full-size boards", anchors, "bm:templates", st)
        for t in tpls:
            pno = lay.n + 1
            p = lay.new_page("template", run_head="Full-size boards")
            anchors["tpl:" + t["id"]] = pno
            doc = t["doc"]
            reg = lay.full(pno)
            head = [P(rich(t["title"]), "tplh"),
                    P(rich("For %s. %s" % (", ".join(titles[x] for x in t["games"]), t.get("note", ""))),
                      "tpl"), VSpace(6)]
            lay.fill([reg], head)
            availh = reg.avail - 34
            s = min(1.0, reg.w / (doc["widthMm"] * MM), availh / (doc["heightMm"] * MM))
            if s < 0.999:
                # a full-size board printed smaller is not a full-size board
                raise RuntimeError("template %s does not fit the page at 100 %% (needs %.1f %%)"
                                   % (t["id"], 100 * s))
            fl = SVGFlow(doc, scale=1.0, gap_before=2, gap_after=4)
            t["printScale"] = 1.0
            lay.fill([reg], [fl, ScaleBar(100.0, t.get("scaleNote"), size=13.0 if g["largePrint"] else 8.5)])
    # glossary
    if bm.get("glossary"):
        fl = []
        for t in sorted(bm["glossary"], key=lambda x: x["term"].lower()):
            tail = ""
            if t.get("games"):
                tail = " <i>(%s)</i>" % ", ".join(rich(titles.get(x, x)) for x in t["games"])
            fl.append(P("<b>%s</b> &nbsp;%s%s" % (rich(t["term"]), rich(t["definition"]), tail), "idx"))
        layout_section(lay, "Glossary", fl, "Glossary", anchors, "bm:glossary", st,
                       columns=1 if g["largePrint"] else 2)
    # bibliography
    if bm.get("bibliography"):
        fl = [P(rich(ed_text(bm["bibliographyIntro"], edition)), "small")]
        for b in bm["bibliography"]:
            used = ", ".join("%s%s" % (rich(titles.get(x, x)),
                                       (" (%s)" % rich(b["pages"][x])) if b.get("pages", {}).get(x) else "")
                             for x in b["games"])
            fl.append(P("%s. <font name='%s'>%s</font>" % (rich(b["citation"].rstrip(".")),
                                                           st["_fonts"]["sans"], used), "idx"))
        layout_section(lay, "Sources", fl, "Sources", anchors, "bm:sources", st,
                       columns=1 if g["largePrint"] else 2)
    # indexes
    fl = [P(rich(ed_text(bm.get("indexIntro", "Every game under its own name and every other "
                                "name this book gives it."), edition)), "small")]
    fl += build_index_flow(games, st, pages, titles)
    layout_section(lay, "Index of Games and Other Names", fl, "Index", anchors, "bm:index-az", st,
                   columns=1 if g["largePrint"] else 2)
    fl = bucket_index(games, st, pages, lambda e: [e["culture"]],
                      sorted({e["culture"] for e in games}, key=lambda s: plain(s).lower()))
    fl += [heading(st, "By age")] + bucket_index(games, st, pages, lambda e: [age_bucket(e["spec"])],
                                                 [lbl for _, lbl in AGE_BUCKETS])
    fl += [heading(st, "By difficulty")] + bucket_index(
        games, st, pages, lambda e: ["%s %s" % (diff_dots(e["spec"]["difficulty"], st["_lp"]),
                                                DIFF_LABEL[e["spec"]["difficulty"]])],
        ["%s %s" % (diff_dots(i, st["_lp"]), DIFF_LABEL[i]) for i in range(1, 6)])
    fl.append(P(rich(PageRef(pages)("For players and playing time together, see Tonight's Game, "
                                    "page {page:fm:tonight}.")), "small"))
    layout_section(lay, "Index by Culture, Age and Difficulty", fl, "Index", anchors,
                   "bm:index-culture", st, columns=1 if g["largePrint"] else 2)
    # invented traditions
    if bm.get("inventedTraditions"):
        fl = [P(rich(ed_text(bm["inventedIntro"], edition)), "fm")]
        for t in bm["inventedTraditions"]:
            hh = P(rich(t["claim"]), "fmh")
            hh.keep_next = True
            fl += [hh, P("<i>%s</i> %s" % (rich(t["verdict"]), rich(t["detail"])), "body")]
        layout_section(lay, "Invented Traditions", fl, "Invented traditions", anchors,
                       "bm:invented", st)
    # illustrations and credits
    if bm.get("credits"):
        fl = [P(rich(ed_text(c, edition)), "fm") for c in bm["credits"]["paragraphs"]]
        rows = [[rich(r["game"]), rich(r["credit"])] for r in bm["credits"]["plates"]]
        if rows:
            W = g["textWPt"]
            fl.append(table_flow(rows, [W * 0.28, W * 0.72], st, header=["Game", "Illustration"]))
        layout_section(lay, "The Illustrations", fl, "Illustrations", anchors, "bm:credits", st)
    if bm.get("aboutAuthor"):
        layout_section(lay, "About the Author", [P(rich(ed_text(x, edition)), "fm")
                                                 for x in bm["aboutAuthor"]],
                       "About the author", anchors, "bm:author", st)
    comp = ctx.get("companion")
    if comp:
        fl = [P(rich(ed_text(comp["standfirst"], edition)), "fm")]
        for it in comp["items"]:
            fl.append(P("<b>%s</b> &nbsp;%s" % (rich(it["name"]), rich(it.get("detail", ""))), "fm"))
        fl.append(P("<b>%s</b>" % rich(comp["url"]), "fmh"))
        fl.append(P(rich(ed_text(comp.get("note", "Free, and free of conditions: nothing to sign up "
                                           "for, no email asked, no account needed."), edition)), "fm"))
        layout_section(lay, comp["heading"], fl, "Companion", anchors, "bm:companion", st)


class ScaleBar(Flow):
    """A printed length check under every template (photocopy at 100 %)."""

    def __init__(self, mm_len, note=None, size=8.5):
        self.mm = mm_len
        self.note = note
        self.size = size

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, 26.0 + (self.size - 8.5)

    def drawOn(self, c, x, y, _sW=0):
        L = self.mm * MM
        c.saveState()
        c.setLineWidth(0.9)
        yy = y + 16 + (self.size - 8.5)
        c.line(x, yy, x + L, yy)
        for k in range(0, int(self.mm / 10) + 1):
            xx = x + k * 10 * MM * (L / (self.mm * MM))
            c.line(xx, yy - 2.5, xx, yy + 2.5)
        c.setFont("GBSans", self.size)
        txt = self.note or ("This bar measures %d cm when the page is printed or copied at "
                            "full size (100 %%)." % round(self.mm / 10))
        c.drawString(x, y + 3, txt)
        c.restoreState()


# ═════════════════════════════════════════════════════════════════════════
# DRAWING
# ═════════════════════════════════════════════════════════════════════════
def render(lay, path, g, title, author, subject):
    from reportlab.pdfgen import canvas as rl_canvas
    c = rl_canvas.Canvas(path, pagesize=(g["wPt"], g["hPt"]), pageCompression=1)
    c.setTitle(title)
    c.setAuthor(author)
    c.setSubject(subject)
    c.setCreator("04_BUILD/interior.py · The Great Book of World Games")
    for i, p in enumerate(lay.pages, 1):
        c.setFont("GBSerif", 10.5)
        for fl, x, y, w in p.items:
            fl.wrap(w, g["hPt"])
            fl.drawOn(c, x, y)
        if not p.blank:
            furniture(c, lay, i, p, g)
        c.showPage()
    c.save()


def furniture(c, lay, i, p, g):
    verso = lay.is_verso(i)
    x, y_top, w, h = lay.block(i)
    lp = g["largePrint"]
    if not p.opensSection and p.runHead and p.kind not in ("blank",):
        c.saveState()
        c.setFont("GBSans", 12 if lp else 8.0)
        c.setFillGray(0.25)
        head = typo.smart(plain(p.runHead)).upper() if not lp else typo.smart(plain(p.runHead))
        hy = g["hPt"] - g["topPt"] + (14 if not lp else 18)
        if verso:
            c.drawString(x, hy, head)
        else:
            c.drawRightString(x + w, hy, head)
        c.setLineWidth(0.35)
        c.line(x, hy - 4.5, x + w, hy - 4.5)
        c.restoreState()
    if p.folio:
        c.saveState()
        c.setFont("GBSans", 13 if lp else 8.8)
        fy = g["bottomPt"] - (24 if not lp else 30)
        if verso:
            c.drawString(x, fy, str(i))
        else:
            c.drawRightString(x + w, fy, str(i))
        c.restoreState()


# ═════════════════════════════════════════════════════════════════════════
# EDITION BUILD
# ═════════════════════════════════════════════════════════════════════════
def load_context(root, cfg, edition, games_override=None):
    import svg_vector as sv
    mdir = os.path.join(root, cfg["language"]["commercialManuscriptDir"])
    book = load(os.path.join(mdir, "book.json"))
    fm = load(os.path.join(mdir, "frontmatter.json"))
    bm = load(os.path.join(mdir, "backmatter_book.json"))
    raw = games_override or book["games"]
    entries = [entry(gm) for gm in raw]
    # diagrams: rendered SVG files, one per id (boards.py writes them)
    ddir = os.path.join(root, "07_ASSETS", "diagrams" if edition != "largeprint" else "diagrams_lp")
    if edition == "largeprint" and not os.path.isdir(ddir):
        ddir = os.path.join(root, "07_ASSETS", "diagrams")
    captions = {}
    for gm in raw:
        for d in (gm.get("diagramSpecs") or gm.get("diagrams", [])):
            if isinstance(d, dict):
                captions[d["id"]] = d.get("caption", "")
    docs = {}
    for e, gm in zip(entries, raw):
        ids = []
        for d in (gm.get("diagramSpecs") or gm.get("diagrams", [])):
            did = d["id"] if isinstance(d, dict) else d
            ids.append(did)
            f = os.path.join(ddir, did + ".svg")
            if not os.path.exists(f):
                raise FileNotFoundError("diagram not rendered: %s (run boards.py)" % f)
            docs[did] = (sv.parse(f), captions.get(did, ""))
        e["diagrams"] = ids
    # plates: explicit map, duplicate-free (gate enforced in qa_plates.py and here)
    pmap = load(os.path.join(root, "01_SOURCE", "plates.json"))["plates"]
    plates, seen = {}, {}
    for gid, rec in pmap.items():
        f = os.path.join(root, rec["print"])
        if not os.path.exists(f):
            raise FileNotFoundError("plate missing for %s: %s" % (gid, f))
        h = sha256(f)
        if h in seen:
            raise RuntimeError("DUPLICATE PLATE: %s and %s share %s" % (seen[h], gid, rec["print"]))
        seen[h] = gid
        plates[gid] = f
    missing = [e["gameId"] for e in entries if e["gameId"] not in plates]
    if missing:
        raise RuntimeError("games without a plate: %s" % missing)
    for e in entries:
        e["plateCaption"] = plate_caption(pmap[e["gameId"]])
    # templates
    templates = []
    tdir = os.path.join(root, "07_ASSETS", "templates_lp" if edition == "largeprint" else "templates")
    for t in bm.get("templates", []):
        f = os.path.join(tdir, t["id"] + ".svg")
        if not os.path.exists(f):
            raise FileNotFoundError("template not rendered: %s" % f)
        tt = dict(t)
        tt["doc"] = sv.parse(f)
        templates.append(tt)
    back_toc = []
    if templates:
        back_toc.append(("bm:templates", "Full-size boards"))
    for key, label, need in (("bm:glossary", "Glossary", "glossary"),
                             ("bm:sources", "Sources", "bibliography"),
                             ("bm:index-az", "Index of games and other names", None),
                             ("bm:index-culture", "Index by culture, age and difficulty", None),
                             ("bm:invented", "Invented traditions", "inventedTraditions"),
                             ("bm:credits", "The illustrations", "credits"),
                             ("bm:author", "About the author", "aboutAuthor"),
                             ("bm:companion", "The free companion", None)):
        if need is None or bm.get(need):
            back_toc.append((key, label))
    comp = companion_block(root, cfg)
    return {"book": book, "fm": fm, "bm": bm, "entries": entries, "diagramDocs": docs,
            "plates": plates, "templates": templates, "backToc": back_toc, "companion": comp}


def companion_block(root, cfg):
    """The companion page, its counts filled from the companion pack's own manifest.

    The page once promised 'Forty board templates' while the site offered 31; now every number
    on it is measured from 08_OUTPUT/COMPANION/companion-manifest.json."""
    comp = cfg.get("companion")
    if not comp:
        return None
    mp = os.path.join(root, "08_OUTPUT", "COMPANION", "companion-manifest.json")
    if not os.path.exists(mp):
        raise FileNotFoundError("companion manifest missing (%s): build the companion first — "
                                "the printed companion page quotes its counts" % mp)
    import build_frontmatter as bf
    n = load(mp)["counts"]
    w = {"Boards": bf.words_for(n["boards"]).capitalize(), "Cards": bf.words_for(n["cards"]).capitalize(),
         "games": bf.words_for(n["indexGames"]), "tailored": bf.words_for(n["tailoredScoreSheets"])}
    items = [dict(it, name=it["name"].format(**w), detail=it.get("detail", "").format(**w))
             for it in comp["items"]]
    return dict(comp, items=items, counts=n)


def build_edition(root, cfg, edition, out_dir, verbose=True):
    register_fonts()
    import svg_vector
    _SVG_FONTS.update(svg_vector.DEFAULT_FONTS)
    ctx = load_context(root, cfg, edition)
    guess, seen = 220, []
    for _ in range(6):
        g = geometry(cfg, edition, guess)
        st = styles(g)
        lay, meta = build_layout(ctx, g, st, None)              # pass 1: placeholders
        used = meta["anchors"]
        lay2, meta2 = build_layout(ctx, g, st, used)            # pass 2: real numbers
        if meta2["anchors"] != used or lay2.n != lay.n:
            # page numbers changed the layout (e.g. an index line wrapped): one more pass
            used = meta2["anchors"]
            lay2, meta2 = build_layout(ctx, g, st, used)
        # the contents, indexes and cross-references print `used`; they are right only if the
        # layout they produced puts every anchor where `used` says (the old 'contents fit' check)
        settled = meta2["anchors"] == used
        n = lay2.n
        seen.append((guess, n))
        if gutter_in(n) == gutter_in(guess):
            break
        guess = n
    else:
        raise RuntimeError("gutter loop did not converge: %s" % seen)
    lay, meta = lay2, meta2
    check_placeholders(lay)
    os.makedirs(out_dir, exist_ok=True)
    name = "GreatBookOfWorldGames_interior_%s.pdf" % edition
    path = os.path.join(out_dir, name)
    tp = ctx["fm"]["titlePage"]
    render(lay, path, g, "%s — %s" % (tp["title"], tp["subtitle"]), tp["author"],
           "Traditional games of the world — rules, boards and sources")
    spreads = meta["spreads"]
    verso = sum(1 for _, first, _ in spreads if first % 2 == 0)
    per = {gid: n for gid, _, n in spreads}
    odd = [gid for gid, _, n in spreads if n % 2]
    blanks = sum(1 for p in lay.pages if p.blank)
    blank_pages = [i for i, p in enumerate(lay.pages, 1) if p.blank]
    kinds = {}
    for p in lay.pages:
        kinds[p.kind] = kinds.get(p.kind, 0) + 1
    report = {
        "edition": edition, "file": os.path.relpath(path, root), "pageCount": lay.n,
        "sha256": sha256(path), "bytes": os.path.getsize(path),
        "trim": {"widthIn": g["trimWidthIn"], "heightIn": g["trimHeightIn"]},
        "margins": {"gutterIn": g["gutterIn"], "outerIn": g["outerIn"], "topIn": g["topIn"],
                    "bottomIn": round(g["bottomIn"], 4), "gutterBareMinIn": g["gutterBareMinIn"],
                    "gutterSafetyIn": g["gutterSafetyIn"]},
        "textBlockIn": [g["textWIn"], g["textHIn"]],
        "kdpGutterRequiredIn": gutter_in(lay.n), "bleed": False,
        "font": g["font"], "fontSha256": FONT_SHA256, "bodyPt": g["bodyPt"], "leadingPt": g["leadPt"],
        "columns": g["columns"],
        "games": len(ctx["entries"]),
        "spreadsStartingVerso": verso, "spreadsTotal": len(spreads),
        "pagesPerGame": per, "fourPageEntries": [gid for gid, n in per.items() if n >= 4],
        "oddLengthEntries": odd, "layoutModes": meta["modes"],
        "blankPages": blanks, "blankPageList": blank_pages, "pageKinds": kinds,
        "frontMatterPages": meta["frontPages"], "bodyEndPage": meta["bodyEnd"],
        "backMatterStartPage": meta["backStart"],
        "pagemap": {k.split(":", 1)[1]: v for k, v in meta["anchors"].items() if k.startswith("game:")},
        "anchors": meta["anchors"], "gutterIterations": seen,
        "tocFitted": settled, "pageReferencesSettled": settled,
        "templates": [{"id": t["id"], "page": meta["anchors"].get("tpl:" + t["id"]),
                       "printScale": t.get("printScale")} for t in ctx["templates"]],
        "manuscriptSha256": sha256(os.path.join(root, cfg["language"]["commercialManuscriptDir"],
                                                "book.json")),
    }
    if g["largePrint"]:
        report.update({"largePrint": True, "editionLabel": g.get("editionLabel"),
                       "minFontPtSet": min(v.fontSize for k, v in st.items()
                                           if hasattr(v, "fontSize"))})
    dump(os.path.join(root, "06_REPORTS", "interior-%s.json" % edition), report)
    if verbose:
        print("  ✓ %-10s %3d pages · %6.1f KB · gutter %.3f in (KDP min %.3f) · blank %d · "
              "verso starts %d/%d · four-page %d · odd %d"
              % (edition, lay.n, os.path.getsize(path) / 1024.0, g["gutterIn"], gutter_in(lay.n),
                 blanks, verso, len(spreads), len(report["fourPageEntries"]), len(odd)))
    return report


def check_placeholders(lay):
    """No page number may print as a placeholder."""
    bad = []
    for i, p in enumerate(lay.pages, 1):
        for fl, *_ in p.items:
            t = getattr(fl, "text", "") or ""
            if ">000<" in t or re.search(r"(^|[\s;>])000(\s|$|<)", t):
                bad.append(i)
    if bad:
        raise RuntimeError("unresolved page placeholders on pages %s" % sorted(set(bad))[:20])


def run_check(root, cfg):
    errs = []
    for ed in ("paperback", "hardcover", "largeprint"):
        p = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if not os.path.exists(p):
            errs.append("%s interior not built" % ed)
            continue
        r = load(p)
        f = os.path.join(root, r["file"])
        if not os.path.exists(f):
            errs.append("%s PDF missing: %s" % (ed, r["file"]))
            continue
        if sha256(f) != r["sha256"]:
            errs.append("%s PDF checksum does not match its report" % ed)
        if r["margins"]["gutterIn"] < r["kdpGutterRequiredIn"]:
            errs.append("%s: gutter %.3f < KDP %.3f" % (ed, r["margins"]["gutterIn"], r["kdpGutterRequiredIn"]))
        if r["pageCount"] % 2:
            errs.append("%s: odd page count" % ed)
        if not r.get("tocFitted", False):
            errs.append("%s: the contents and page references did not settle — printed page numbers "
                        "may be wrong" % ed)
        if ed != "largeprint":
            if r["spreadsStartingVerso"] != r["spreadsTotal"]:
                errs.append("%s: %d games do not start on a left-hand page"
                            % (ed, r["spreadsTotal"] - r["spreadsStartingVerso"]))
            if r.get("oddLengthEntries"):
                errs.append("%s: games with an odd number of pages: %s" % (ed, r["oddLengthEntries"]))
        if r.get("manuscriptSha256") and r["manuscriptSha256"] != sha256(
                os.path.join(root, cfg["language"]["commercialManuscriptDir"], "book.json")):
            errs.append("%s: built from an older manuscript — rebuild" % ed)
    pb = os.path.join(root, "06_REPORTS", "interior-paperback.json")
    hc = os.path.join(root, "06_REPORTS", "interior-hardcover.json")
    if os.path.exists(pb) and os.path.exists(hc):
        a, b = load(pb), load(hc)
        if a["pagemap"] != b["pagemap"] or a["pageCount"] != b["pageCount"]:
            errs.append("paperback and hardcover page maps differ — one companion cannot serve both")
    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        return 1
    for ed in ("paperback", "hardcover", "largeprint"):
        r = load(os.path.join(root, "06_REPORTS", "interior-%s.json" % ed))
        print("  ✓ %-10s %3d pages · gutter %.3f ≥ %.3f · blank %d" % (
            ed, r["pageCount"], r["margins"]["gutterIn"], r["kdpGutterRequiredIn"], r["blankPages"]))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--edition", choices=["paperback", "hardcover", "largeprint"])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    cfg = load(os.path.join(root, "project_config.json"))
    try:
        import reportlab  # noqa: F401
    except ImportError:
        print("  ⊘ reportlab missing — interior SKIPPED")
        return 2
    if not os.path.exists(os.path.join(root, cfg["language"]["commercialManuscriptDir"], "book.json")):
        print("  · manuscript not in this checkout — interior SKIPPED (expected in CI)")
        return 0
    print("=" * 74)
    print("  INTERIOR")
    print("=" * 74)
    if args.check:
        rc = run_check(root, cfg)
        print("=" * 74)
        return rc
    eds = ["paperback", "hardcover", "largeprint"] if args.all or not args.edition else [args.edition]
    out = {"paperback": "PAPERBACK", "hardcover": "HARDCOVER", "largeprint": "LARGEPRINT"}
    for ed in eds:
        build_edition(root, cfg, ed, os.path.join(root, "08_OUTPUT", out[ed]))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
