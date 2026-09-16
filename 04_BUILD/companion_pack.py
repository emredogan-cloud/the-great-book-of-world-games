#!/usr/bin/env python3
"""
COMPANION PACK — The Great Book of World Games
================================================================================
Builds the free digital companion for the printed paperback: four PDFs and a
manifest, every fact in them read from the manuscript data.

    game-index.pdf              all games in book order, one table
    quick-reference-cards.pdf   one cut-out card per game, four to a sheet
    score-sheets.pdf            general score grid · match record · tailored
                                tally sheets ONLY where the rules count
    boards-pack.pdf             printable boards from the book's own SVGs
    companion-manifest.json     what the website registry needs

Sources (read-only — this script never writes into the book project):

    02_MANUSCRIPT/book.json            rules, spec strings, provenance
    02_MANUSCRIPT/frontmatter.json     contents order and family openers
    06_REPORTS/interior-paperback.json first page of every game in print
    07_ASSETS/diagrams/*.svg           diagrams (drawn through svg_vector.py)
    07_ASSETS/diagrams/*_diagrams.json diagram type and board class

Rules of the build:

  · Nothing about a game is invented here. A card prints the book's own
    `winCondition` sentence as the objective; the index prints the book's
    own `spec` strings; a board is the book's own SVG scaled up. A missing
    field prints "—".
  · Black ink only. US Letter portrait, landscape only when a board earns a
    larger scale that way. Liberation Serif embedded (the paperback's face);
    reportlab's Helvetica base font is replaced so nothing unembedded leaks.
  · Every page carries the footer
        valicepress.com/companion/world-games · The Great Book of World Games

Usage:
    python3 04_BUILD/companion_pack.py --out /path/to/public/companion/world-games
    python3 04_BUILD/companion_pack.py --out DIR --root /path/to/book/project
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import sys

# ── constants ─────────────────────────────────────────────────────────────
IN = 72.0
MM = 72.0 / 25.4
LETTER_W, LETTER_H = 8.5 * IN, 11.0 * IN
MARGIN = 0.5 * IN
FOOTER = "valicepress.com/companion/world-games · The Great Book of World Games"
BOOK_TITLE = "The Great Book of World Games"


def _publisher() -> str:
    """Kurucu değeri: tek doğruluk kaynağı project_config.json (validate_structure.py)."""
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(os.path.dirname(here), "project_config.json"),
              encoding="utf-8") as f:
        return json.load(f)["publisher"]


PUBLISHER = _publisher()
RECON_MARK = "†"
RECON_LEGEND = ("%s  rules the book presents as a scholarly reconstruction"
                % RECON_MARK)

FONT_DIR_CANDIDATES = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/liberation2",
    "/usr/share/fonts/liberation",
    "/usr/share/fonts/liberation-fonts",
]
FONT_FILES = {
    "GBSerif":    "LiberationSerif-Regular.ttf",
    "GBSerif-B":  "LiberationSerif-Bold.ttf",
    "GBSerif-I":  "LiberationSerif-Italic.ttf",
    "GBSerif-BI": "LiberationSerif-BoldItalic.ttf",
}

# Diagram types the book itself prints as "Board Templates" in its back
# matter (see build_backmatter.py). A move-diagram is a rule illustration,
# not a board, and never goes into the boards pack.
BOARD_TYPES = {"board-diagram", "setup-illustration"}

# Tailored score sheets. A family appears here only if book.json gives at
# least one of its games an explicit `scoring` field or a win/end condition
# that tells the players to count. The build asserts that for every game
# listed; the rule text printed on the sheet is always the book's own.
TAILORED_SHEETS = [
    {
        "family": "chance",
        "layout": "running-total",
        "games": ["astragaloi", "set-dilth", "tien-gow"],
        "players": 5,           # astragaloi 2–5 · set-dilth 2–4 · tien-gow 4
        "rows": 16,
        "rowLabel": "Throw / round",
    },
    {
        "family": "race",
        "layout": "patolli",
        "games": ["patolli"],
    },
    {
        "family": "sowing",
        "layout": "seed-count",
        "games": ["olinda-keliya", "oware", "pallanguzhi"],
        "noTally": ["bao-la-kiswahili", "omweso"],
    },
    {
        "family": "territory",
        "layout": "go-count",
        "games": ["go"],
    },
    {
        "family": "boardless",
        "layout": "counts",
        "games": ["gonggi", "jianzi"],
    },
]

# Words that mark a rule as one that counts. Used only to GUARD the list
# above: a game on a tailored sheet must match, otherwise the build stops.
TALLY_RE = re.compile(r"\b(points?|scores?|count(?:ed|ing)?|total|seeds)\b",
                      re.I)


# ── fonts ─────────────────────────────────────────────────────────────────
def register_fonts() -> str:
    """Embed Liberation Serif under the same names the paperback uses."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping
    import reportlab.rl_config as rl_config

    fdir = None
    for d in FONT_DIR_CANDIDATES:
        if os.path.isdir(d) and all(os.path.exists(os.path.join(d, f))
                                    for f in FONT_FILES.values()):
            fdir = d
            break
    if fdir is None:
        raise RuntimeError("Liberation Serif not found; install fonts-liberation")
    for name, fn in FONT_FILES.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(fdir, fn)))
    # reportlab's base font is Helvetica and it enters the page resources
    # even when unused; `pdffonts` would list it as not embedded.
    rl_config.canvas_basefontname = "GBSerif"
    addMapping("GBSerif", 0, 0, "GBSerif")
    addMapping("GBSerif", 1, 0, "GBSerif-B")
    addMapping("GBSerif", 0, 1, "GBSerif-I")
    addMapping("GBSerif", 1, 1, "GBSerif-BI")
    return fdir


def esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def dash(v) -> str:
    """A missing or empty field prints as an em dash, never as a guess."""
    if v is None:
        return "—"
    v = str(v).strip()
    return v if v else "—"


# ── data ──────────────────────────────────────────────────────────────────
class BookData:
    def __init__(self, root: str):
        self.root = root
        mp = os.path.join(root, "02_MANUSCRIPT")
        self.book = json.load(open(os.path.join(mp, "book.json"), encoding="utf-8"))
        self.front = json.load(open(os.path.join(mp, "frontmatter.json"),
                                    encoding="utf-8"))
        rep = json.load(open(os.path.join(root, "06_REPORTS",
                                          "interior-paperback.json"),
                             encoding="utf-8"))
        self.pagemap: dict[str, int] = rep["pagemap"]
        self.paperback_pages = rep.get("pageCount")
        self.games = {g["gameId"]: g for g in self.book["games"]}

        # Book order comes from the contents list, family openers included.
        self.openers = {fo["family"]: fo for fo in self.front["familyOpeners"]}
        self.order: list[dict] = []          # entries in reading order
        seen = set()
        for e in self.front["contents"]:
            if e["kind"] == "family-opener":
                self.order.append({"kind": "opener", "family": e["family"],
                                   "title": e["title"]})
            elif e["kind"] == "game" and e["gameId"] in self.games:
                self.order.append({"kind": "game", "gameId": e["gameId"]})
                seen.add(e["gameId"])
        missing = [gid for gid in self.games if gid not in seen]
        if missing:
            raise SystemExit("games absent from frontmatter contents: %s"
                             % ", ".join(missing))
        self.game_ids_in_order = [e["gameId"] for e in self.order
                                  if e["kind"] == "game"]

        # Diagram metadata: type and board class per diagram id.
        self.diagram_meta: dict[str, dict] = {}
        ddir = os.path.join(root, "07_ASSETS", "diagrams")
        self.diagram_dir = ddir
        for fn in sorted(os.listdir(ddir)):
            if fn.endswith("_diagrams.json"):
                for d in json.load(open(os.path.join(ddir, fn),
                                        encoding="utf-8"))["diagrams"]:
                    self.diagram_meta[d["diagramId"]] = d

        self.problems: list[str] = []
        self._check()

    def _check(self):
        for gid, g in self.games.items():
            if gid not in self.pagemap:
                self.problems.append("%s: no page in interior-paperback.json" % gid)
            for k in ("players", "time", "age", "materials"):
                if not (g.get("spec") or {}).get(k):
                    self.problems.append("%s: spec.%s missing" % (gid, k))
            for k in ("culture", "place", "period", "winCondition"):
                if not g.get(k):
                    self.problems.append("%s: %s missing" % (gid, k))
            for did in g.get("diagrams", []):
                if did not in self.diagram_meta:
                    self.problems.append("%s: diagram %s has no metadata" % (gid, did))
                if not os.path.exists(os.path.join(self.diagram_dir, did + ".svg")):
                    self.problems.append("%s: diagram %s has no SVG" % (gid, did))

    # ── accessors ────────────────────────────────────────────────────────
    def family_label(self, family: str) -> str:
        fo = self.openers.get(family)
        if not fo:
            return dash(family)
        return "Part %s · %s" % (fo.get("numeral") or "—", fo.get("title") or family)

    def page(self, gid: str):
        return self.pagemap.get(gid)

    def spec(self, gid: str, key: str) -> str:
        return dash((self.games[gid].get("spec") or {}).get(key))


# Compact renderings of the book's own spec strings. Each keeps the book's
# words; only the unit is folded into the column header.
_PLAYERS_HEAD = re.compile(
    r"^\s*(\d+(?:\s*[–-]\s*\d+)?(?:\s+or\s+(?:\d+|more))?)\s*[,]?\s*(.*)$")
_TIME_MIN = re.compile(r"^\s*(\d+\s*[–-]\s*\d+)\s+minutes?\s*$", re.I)
_AGE_UP = re.compile(r"^\s*(\d+)\s+and\s+up\s*$", re.I)


def players_parts(s: str) -> tuple[str, str]:
    """'2–4 (four play as two partnerships)' → ('2–4', '(four play …)')."""
    if s == "—":
        return s, ""
    m = _PLAYERS_HEAD.match(s)
    if not m:
        return s, ""
    return m.group(1).replace(" ", ""), m.group(2).strip()


def time_compact(s: str) -> str:
    m = _TIME_MIN.match(s)
    return m.group(1).replace(" ", "") if m else s


def age_compact(s: str) -> str:
    m = _AGE_UP.match(s)
    return m.group(1) + "+" if m else s


# ── page furniture ────────────────────────────────────────────────────────
def draw_footer(c, page_w: float, page_no: int | None = None):
    c.saveState()
    c.setFillColorRGB(0, 0, 0)
    c.setStrokeColorRGB(0, 0, 0)
    c.setFont("GBSerif", 8)
    c.drawCentredString(page_w / 2.0, 0.28 * IN, FOOTER)
    if page_no is not None:
        c.setFont("GBSerif", 8)
        c.drawRightString(page_w - MARGIN, 0.28 * IN, str(page_no))
    c.restoreState()


def styles():
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER

    def S(**kw):
        kw.setdefault("fontName", "GBSerif")
        kw.setdefault("bulletFontName", "GBSerif")
        kw.setdefault("textColor", "black")
        return ParagraphStyle(**kw)

    return {
        "h1":    S(name="h1", fontName="GBSerif-B", fontSize=18, leading=22,
                   spaceAfter=4),
        "h2":    S(name="h2", fontName="GBSerif-B", fontSize=12, leading=15,
                   spaceBefore=8, spaceAfter=3),
        "sub":   S(name="sub", fontName="GBSerif-I", fontSize=9.5, leading=12,
                   spaceAfter=8),
        "body":  S(name="body", fontSize=9.5, leading=12.5, spaceAfter=6),
        "small": S(name="small", fontSize=8, leading=10),
        "cell":  S(name="cell", fontSize=7.5, leading=9.2),
        "cellb": S(name="cellb", fontName="GBSerif-B", fontSize=7.5, leading=9.2),
        "cellc": S(name="cellc", fontSize=7.5, leading=9.2, alignment=TA_CENTER),
        "head":  S(name="head", fontName="GBSerif-B", fontSize=7.5, leading=9.2),
        "headc": S(name="headc", fontName="GBSerif-B", fontSize=7.5, leading=9.2,
                   alignment=TA_CENTER),
        "fam":   S(name="fam", fontName="GBSerif-B", fontSize=9, leading=11),
        "card_title": S(name="ct", fontName="GBSerif-B", fontSize=14, leading=17),
        "card_kick":  S(name="ck", fontName="GBSerif-I", fontSize=8, leading=10),
        "card_body":  S(name="cb", fontSize=9, leading=11.5),
        "card_small": S(name="cs", fontName="GBSerif-I", fontSize=8, leading=10),
    }


def fit_paragraph(text: str, style, width: float, max_h: float,
                  min_size: float = 7.0):
    """Shrink a paragraph until it fits `max_h`; returns (para, h, fits)."""
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    size = style.fontSize
    while True:
        st = ParagraphStyle(name=style.name + "_fit", parent=style,
                            fontSize=size, leading=size * 1.25)
        p = Paragraph(text, st)
        _, h = p.wrap(width, 100000)
        if h <= max_h:
            return p, h, True
        if size <= min_size:
            return p, h, False
        size -= 0.5


def sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


# ══════════════════════════════════════════════════════════════════════════
# 1 · GAME INDEX
# ══════════════════════════════════════════════════════════════════════════
def build_game_index(data: BookData, out_path: str) -> int:
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Table,
                                    TableStyle, Spacer, KeepTogether)
    from reportlab.lib import colors

    st = styles()
    doc = SimpleDocTemplate(out_path, pagesize=(LETTER_W, LETTER_H),
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN + 6, bottomMargin=MARGIN + 6,
                            title="%s — Game Index" % BOOK_TITLE,
                            author=PUBLISHER, creator="companion_pack.py")

    def on_page(c, d):
        draw_footer(c, LETTER_W, d.page)

    n_games = len(data.game_ids_in_order)
    n_fam = len([e for e in data.order if e["kind"] == "opener"])
    n_rec = sum(1 for gid in data.game_ids_in_order
                if data.games[gid].get("reconstructed"))

    story = [
        Paragraph("Game Index", st["h1"]),
        Paragraph("%s · all %d games in the order they appear in the paperback"
                  % (BOOK_TITLE, n_games), st["sub"]),
        Paragraph(
            "<b>How to read this table.</b> The games are listed in book order, "
            "under the %d Parts the book sorts them into, so a row's neighbours "
            "are the games that work the same way. <i>Players</i>, <i>Time</i> and "
            "<i>Age</i> are the figures printed in each game's specification "
            "box: time is in minutes, and an age of 7+ is the book's "
            "“7 and up”. <i>Culture and place</i> and <i>Period</i> are "
            "copied as the book states them, including its hedges "
            "(“recorded 1895” means the source the book used dates "
            "from then, not that the game does). <i>Page</i> is the first page "
            "of the game's rules in the paperback. A dagger (%s) marks the %d "
            "rule sets the book presents as reconstructions, where the "
            "source records the board and pieces but not every rule; the "
            "book says so on the page. A dash means the book gives no figure."
            % (n_fam, RECON_MARK, n_rec), st["body"]),
        Spacer(1, 4),
    ]

    # Column widths sum to the 7.5 in text width.
    widths = [18, 92, 58, 40, 28, 118, 142, 28, 16]
    assert abs(sum(widths) - 540) < 0.01, sum(widths)
    P = Paragraph
    header = [P("#", st["headc"]), P("Game", st["head"]), P("Players", st["head"]),
              P("Time (min)", st["head"]), P("Age", st["head"]),
              P("Culture · place", st["head"]), P("Period", st["head"]),
              P("Page", st["headc"]), P(RECON_MARK, st["headc"])]
    rows = [header]
    fam_rows = []
    n = 0
    for e in data.order:
        if e["kind"] == "opener":
            fam_rows.append(len(rows))
            rows.append([P(esc(data.family_label(e["family"])), st["fam"])]
                        + [""] * (len(widths) - 1))
            continue
        gid = e["gameId"]
        g = data.games[gid]
        n += 1
        head, tail = players_parts(data.spec(gid, "players"))
        players = esc(head) + ("<br/><i>%s</i>" % esc(tail) if tail else "")
        pg = data.page(gid)
        rows.append([
            P(str(n), st["cellc"]),
            P("<b>%s</b>" % esc(g.get("title") or gid), st["cell"]),
            P(players, st["cell"]),
            P(esc(time_compact(data.spec(gid, "time"))), st["cell"]),
            P(esc(age_compact(data.spec(gid, "age"))), st["cell"]),
            P("%s · %s" % (esc(dash(g.get("culture"))), esc(dash(g.get("place")))),
              st["cell"]),
            P(esc(dash(g.get("period"))), st["cell"]),
            P(str(pg) if pg else "—", st["cellc"]),
            P(RECON_MARK if g.get("reconstructed") else "", st["cellc"]),
        ])

    t = Table(rows, colWidths=widths, repeatRows=1)
    ts = [
        ("FONTNAME", (0, 0), (-1, -1), "GBSerif"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.black),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, colors.black),
    ]
    for r in fam_rows:
        ts += [("SPAN", (0, r), (-1, r)),
               ("TOPPADDING", (0, r), (-1, r), 7),
               ("BOTTOMPADDING", (0, r), (-1, r), 3),
               ("LINEBELOW", (0, r), (-1, r), 0.6, colors.black)]
    t.setStyle(TableStyle(ts))
    story.append(t)
    story.append(Spacer(1, 8))
    story.append(KeepTogether([
        Paragraph(esc(RECON_LEGEND), st["small"]),
        Paragraph("Page numbers refer to the paperback edition (%s pages, "
                  "8.5 × 11 in). %d games · %d Parts."
                  % (data.paperback_pages or "—", n_games, n_fam), st["small"]),
    ]))
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return n


# ══════════════════════════════════════════════════════════════════════════
# 2 · QUICK REFERENCE CARDS
# ══════════════════════════════════════════════════════════════════════════
def build_cards(data: BookData, out_path: str) -> int:
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.platypus import Paragraph

    st = styles()
    c = rl_canvas.Canvas(out_path, pagesize=(LETTER_W, LETTER_H))
    c.setTitle("%s — Quick Reference Cards" % BOOK_TITLE)
    c.setAuthor(PUBLISHER)
    c.setCreator("companion_pack.py")

    card_w = (LETTER_W - 2 * MARGIN) / 2.0      # 3.75 in
    card_h = (LETTER_H - 2 * MARGIN) / 2.0      # 5 in
    pad = 14.0
    inner_w = card_w - 2 * pad

    def cut_lines():
        c.saveState()
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.4)
        c.setDash([3, 3])
        mx, my = LETTER_W / 2.0, LETTER_H / 2.0
        c.line(mx, MARGIN, mx, LETTER_H - MARGIN)
        c.line(MARGIN, my, LETTER_W - MARGIN, my)
        c.rect(MARGIN, MARGIN, LETTER_W - 2 * MARGIN, LETTER_H - 2 * MARGIN)
        c.setDash()
        # crop ticks in the margins
        tick = 10
        for x in (MARGIN, mx, LETTER_W - MARGIN):
            c.line(x, MARGIN - tick - 2, x, MARGIN - 2)
            c.line(x, LETTER_H - MARGIN + 2, x, LETTER_H - MARGIN + tick + 2)
        for y in (MARGIN, my, LETTER_H - MARGIN):
            c.line(MARGIN - tick - 2, y, MARGIN - 2, y)
            c.line(LETTER_W - MARGIN + 2, y, LETTER_W - MARGIN + tick + 2, y)
        c.restoreState()

    def draw_card(x0: float, y0: float, gid: str):
        """x0,y0 = lower-left corner of the card."""
        g = data.games[gid]
        top = y0 + card_h - pad
        y = top
        # title (shrinks for the long ones)
        p, h, _ = fit_paragraph("<b>%s</b>" % esc(g.get("title") or gid),
                                st["card_title"], inner_w, 40, 10)
        p.drawOn(c, x0 + pad, y - h)
        y -= h + 2
        kick = "%s — %s" % (data.family_label(g.get("family")),
                            dash(g.get("culture")))
        p = Paragraph(esc(kick), st["card_kick"])
        _, h = p.wrap(inner_w, 100)
        p.drawOn(c, x0 + pad, y - h)
        y -= h + 5
        c.setLineWidth(0.5)
        c.line(x0 + pad, y, x0 + card_w - pad, y)
        y -= 7
        spec = ("<b>Players</b> %s &nbsp;·&nbsp; <b>Time</b> %s &nbsp;·&nbsp; "
                "<b>Age</b> %s" % (esc(data.spec(gid, "players")),
                                   esc(data.spec(gid, "time")),
                                   esc(data.spec(gid, "age"))))
        p = Paragraph(spec, st["card_body"])
        _, h = p.wrap(inner_w, 100)
        p.drawOn(c, x0 + pad, y - h)
        y -= h + 4
        p = Paragraph("<b>Materials</b> %s" % esc(data.spec(gid, "materials")),
                      st["card_body"])
        _, h = p.wrap(inner_w, 200)
        p.drawOn(c, x0 + pad, y - h)
        y -= h + 6

        # bottom block: page line (+ reconstruction note)
        bottom_lines = ["Full rules: page %s of the paperback."
                        % (data.page(gid) or "—")]
        if g.get("reconstructed"):
            bottom_lines.append("%s The book presents these rules as a "
                                "reconstruction." % RECON_MARK)
        bp = Paragraph("<br/>".join(esc(s) for s in bottom_lines),
                       st["card_small"])
        _, bh = bp.wrap(inner_w, 100)
        bp.drawOn(c, x0 + pad, y0 + pad)
        limit = y0 + pad + bh + 8

        # objective — the book's own winCondition sentence(s). Shrunk to
        # fit; if it still does not fit, cut at a sentence boundary.
        avail = y - limit
        sents = sentences(dash(g.get("winCondition")))
        while True:
            text = "<b>Objective</b> " + esc(" ".join(sents))
            p, h, ok = fit_paragraph(text, st["card_body"], inner_w, avail, 7.5)
            if ok or len(sents) <= 1:
                break
            sents = sents[:-1]
        if not ok:
            data.problems.append("%s: objective overflowed the card" % gid)
        p.drawOn(c, x0 + pad, y - h)

    slots = [(MARGIN, MARGIN + card_h), (MARGIN + card_w, MARGIN + card_h),
             (MARGIN, MARGIN), (MARGIN + card_w, MARGIN)]
    ids = data.game_ids_in_order
    n = 0
    for i in range(0, len(ids), 4):
        cut_lines()
        for slot, gid in zip(slots, ids[i:i + 4]):
            draw_card(slot[0], slot[1], gid)
            n += 1
        draw_footer(c, LETTER_W, c.getPageNumber())
        c.showPage()
    c.save()
    return n


# ══════════════════════════════════════════════════════════════════════════
# 3 · SCORE SHEETS
# ══════════════════════════════════════════════════════════════════════════
class Sheet:
    """Small drawing helpers shared by the score-sheet pages."""

    def __init__(self, c, st):
        self.c, self.st = c, st
        self.left = MARGIN
        self.right = LETTER_W - MARGIN
        self.width = self.right - self.left

    def title(self, title: str, sub: str) -> float:
        c = self.c
        c.setFont("GBSerif-B", 16)
        c.drawString(self.left, LETTER_H - MARGIN - 14, title)
        c.setFont("GBSerif-I", 9)
        c.drawString(self.left, LETTER_H - MARGIN - 27, sub)
        c.setLineWidth(0.8)
        c.line(self.left, LETTER_H - MARGIN - 33, self.right, LETTER_H - MARGIN - 33)
        return LETTER_H - MARGIN - 42

    def fill_line(self, y: float, label: str, x: float, w: float) -> None:
        c = self.c
        c.setFont("GBSerif", 9)
        c.drawString(x, y, label)
        lw = c.stringWidth(label, "GBSerif", 9)
        c.setLineWidth(0.4)
        c.line(x + lw + 4, y - 2, x + w, y - 2)

    def para(self, text: str, y: float, style=None, w: float | None = None,
             x: float | None = None) -> float:
        from reportlab.platypus import Paragraph
        p = Paragraph(text, style or self.st["body"])
        _, h = p.wrap(w or self.width, 1000)
        p.drawOn(self.c, x if x is not None else self.left, y - h)
        return y - h

    def grid(self, y_top: float, col_widths: list[float], row_h: float,
             n_rows: int, headers: list[str], first_col_labels=None,
             header_h: float | None = None, x: float | None = None,
             bold_last_row: bool = False, last_row_label: str | None = None) -> float:
        """Draw a ruled grid; returns the y of its bottom edge."""
        c = self.c
        x0 = self.left if x is None else x
        hh = header_h or row_h
        total_w = sum(col_widths)
        total_h = hh + n_rows * row_h
        c.setLineWidth(0.8)
        c.rect(x0, y_top - total_h, total_w, total_h)
        c.setLineWidth(0.8)
        c.line(x0, y_top - hh, x0 + total_w, y_top - hh)
        c.setLineWidth(0.3)
        for r in range(1, n_rows):
            yy = y_top - hh - r * row_h
            c.line(x0, yy, x0 + total_w, yy)
        xx = x0
        for i, w in enumerate(col_widths[:-1]):
            xx += w
            c.setLineWidth(0.8 if i == 0 else 0.3)
            c.line(xx, y_top, xx, y_top - total_h)
        # headers
        c.setFont("GBSerif-B", 8.5)
        xx = x0
        for w, htxt in zip(col_widths, headers):
            if htxt:
                c.drawCentredString(xx + w / 2.0, y_top - hh / 2.0 - 3, htxt)
            xx += w
        # first-column labels
        if first_col_labels:
            c.setFont("GBSerif", 8.5)
            for r, lab in enumerate(first_col_labels[:n_rows]):
                yy = y_top - hh - r * row_h - row_h / 2.0 - 3
                c.drawCentredString(x0 + col_widths[0] / 2.0, yy, str(lab))
        if bold_last_row:
            yy = y_top - hh - (n_rows - 1) * row_h
            c.setLineWidth(0.8)
            c.line(x0, yy, x0 + total_w, yy)
            if last_row_label:
                c.setFont("GBSerif-B", 8.5)
                c.drawCentredString(x0 + col_widths[0] / 2.0,
                                    yy - row_h / 2.0 - 3, last_row_label)
        return y_top - total_h


def build_score_sheets(data: BookData, out_path: str) -> dict:
    from reportlab.pdfgen import canvas as rl_canvas

    st = styles()
    c = rl_canvas.Canvas(out_path, pagesize=(LETTER_W, LETTER_H))
    c.setTitle("%s — Score Sheets" % BOOK_TITLE)
    c.setAuthor(PUBLISHER)
    c.setCreator("companion_pack.py")
    sh = Sheet(c, st)
    made = {"general": 0, "matchRecord": 0, "tailored": []}

    def end_page():
        draw_footer(c, LETTER_W, c.getPageNumber())
        c.showPage()

    # ── (a) general multi-round score grid, 2–6 players, two pages ──────
    for part, (r0, r1) in enumerate([(1, 20), (21, 40)]):
        y = sh.title("Score Sheet — rounds %d to %d" % (r0, r1),
                     "For any game in the book played over several rounds · "
                     "two to six players · %s" % BOOK_TITLE)
        y -= 8
        sh.fill_line(y, "Game", sh.left, sh.width * 0.55)
        sh.fill_line(y, "Date", sh.left + sh.width * 0.60, sh.width * 0.40)
        y -= 20
        name_w = 60
        col = (sh.width - name_w) / 6.0
        widths = [name_w] + [col] * 6
        headers = ["Round"] + ["Player %d" % i for i in range(1, 7)]
        labels = list(range(r0, r1 + 1))
        if part == 1:
            labels = ["Carried"] + labels
        labels = labels + ["Total"]
        y = sh.grid(y, widths, 20, len(labels), headers, labels, header_h=30,
                    bold_last_row=True)
        y -= 10
        note = ("Write each player's name in the header. One row per round; "
                "add the column at the end."
                if part == 0 else
                "Continue from the first sheet: copy each player's total into "
                "the <i>Carried</i> row before round 21.")
        sh.para(note, y, st["small"])
        end_page()
        made["general"] += 1

    # ── (b) match record ─────────────────────────────────────────────────
    y = sh.title("Match Record",
                 "Ten games, whichever they were · %s" % BOOK_TITLE)
    y -= 10
    widths = [118, 62, 150, 90, sh.width - (118 + 62 + 150 + 90)]
    y = sh.grid(y, widths, 46, 10, ["Game", "Date", "Players", "Winner", "Notes"],
                header_h=22)
    y -= 12
    sh.para("Page numbers for every game are in the game index; the full rules "
            "are in the paperback.", y, st["small"])
    end_page()
    made["matchRecord"] = 1

    # ── (c) tailored sheets — only where the rules count ─────────────────
    for spec in TAILORED_SHEETS:
        for gid in spec["games"]:
            g = data.games[gid]
            blob = " ".join(g.get("scoring") or []) + " " + \
                (g.get("winCondition") or "") + " " + (g.get("endCondition") or "")
            if not TALLY_RE.search(blob):
                raise SystemExit("tailored sheet for %s but its rules do not "
                                 "count anything — refusing to invent one" % gid)
        fam_title = data.family_label(spec["family"])
        titles = " · ".join(data.games[g]["title"] for g in spec["games"])
        layout = spec["layout"]

        if layout == "running-total":
            y = sh.title("Running Score — %s" % fam_title,
                         "%s · the book's scoring rules are printed below"
                         % titles)
            y -= 8
            sh.fill_line(y, "Game", sh.left, sh.width * 0.40)
            sh.fill_line(y, "Date", sh.left + sh.width * 0.45, sh.width * 0.25)
            sh.fill_line(y, "Target score", sh.left + sh.width * 0.74,
                         sh.width * 0.26)
            y -= 18
            n_p = spec["players"]
            widths = [64] + [(sh.width - 64) / n_p] * n_p
            headers = [spec["rowLabel"]] + ["Player %d" % i for i in range(1, n_p + 1)]
            labels = list(range(1, spec["rows"] + 1)) + ["Total"]
            y = sh.grid(y, widths, 17, len(labels), headers, labels,
                        header_h=26, bold_last_row=True)
            y -= 8
            sh.para("Each cell holds the running total after that throw or "
                    "round, so the last filled cell is always the score.",
                    y, st["small"])
            y -= 16
            y = _scoring_legend(sh, data, spec["games"], y)

        elif layout == "patolli":
            g = data.games["patolli"]
            y = sh.title("Points — %s" % g["title"],
                         "%s · two players · %s" % (fam_title, BOOK_TITLE))
            y -= 8
            sh.fill_line(y, "Date", sh.left, sh.width * 0.30)
            sh.fill_line(y, "Playing to", sh.left + sh.width * 0.35, sh.width * 0.30)
            y -= 20
            # Two players, twelve numbered point boxes each, plus a column
            # that records how the point was earned (the book gives two
            # ways). The box count follows the book: "First to twelve".
            box = 30
            for pi in range(2):
                sh.fill_line(y, "Player %d" % (pi + 1), sh.left, sh.width * 0.5)
                y -= 10
                c.setLineWidth(0.6)
                for i in range(12):
                    x = sh.left + i * (box + 6)
                    c.rect(x, y - box, box, box)
                    c.setFont("GBSerif", 7)
                    c.drawString(x + 2, y - 8, str(i + 1))
                y -= box + 6
                sh.para("<i>In each box write H for a piece brought home or "
                        "S for a piece you sent back, as the book scores them.</i>",
                        y, st["small"])
                y -= 16
            y -= 6
            widths = [60, 120, 120, sh.width - 300]
            y = sh.grid(y, widths, 20, 8, ["Game", "Player 1 points",
                                           "Player 2 points", "Winner / notes"],
                        list(range(1, 9)), header_h=22)
            y -= 14
            y = _scoring_legend(sh, data, ["patolli"], y, include_win=True)

        elif layout == "seed-count":
            y = sh.title("Seed Count by Round — %s" % fam_title,
                         "%s · two players" % titles)
            y -= 8
            sh.fill_line(y, "Game", sh.left, sh.width * 0.45)
            sh.fill_line(y, "Date", sh.left + sh.width * 0.55, sh.width * 0.45)
            y -= 20
            widths = [50, 130, 130, sh.width - 310]
            labels = list(range(1, 13))
            y = sh.grid(y, widths, 22, len(labels),
                        ["Round", "Player 1 — seeds held", "Player 2 — seeds held",
                         "Who won the round / notes"], labels, header_h=26)
            y -= 8
            sh.para("Count each player's seeds when the book says the round or "
                    "the game ends, and write the totals here. The book's own "
                    "conditions:", y, st["small"])
            y -= 16
            y = _scoring_legend(sh, data, spec["games"], y, include_win=True)
            y -= 6
            for gid in spec.get("noTally", []):
                g = data.games[gid]
                y = sh.para("<b>%s</b> is not on this sheet. The book: "
                            "“%s”" % (esc(g["title"]),
                                                 esc(g.get("endCondition") or
                                                     g.get("winCondition") or "—")),
                            y, st["small"])
                y -= 4

        elif layout == "go-count":
            g = data.games["go"]
            y = sh.title("Territory Count — %s" % g["title"],
                         "%s · two players · %s" % (fam_title, BOOK_TITLE))
            y -= 8
            sh.fill_line(y, "Date", sh.left, sh.width * 0.30)
            sh.fill_line(y, "Board", sh.left + sh.width * 0.35, sh.width * 0.25)
            y -= 20
            widths = [50, 110, 110, 110, sh.width - 380]
            labels = list(range(1, 15))
            y = sh.grid(y, widths, 22, len(labels),
                        ["Game", "Dark — territory", "Light — territory",
                         "Winner", "Margin / notes"], labels, header_h=26)
            y -= 14
            y = _scoring_legend(sh, data, ["go"], y, include_win=True)

        elif layout == "counts":
            y = sh.title("Counts — %s" % fam_title, titles)
            y -= 8
            # Gonggi: players run through five levels to an agreed score.
            gg = data.games["gonggi"]
            y = sh.para("<b>%s</b> — %s" % (esc(gg["title"]),
                                             esc(data.spec("gonggi", "players"))),
                        y, st["body"])
            y -= 2
            sh.fill_line(y, "Agreed score", sh.left, sh.width * 0.35)
            y -= 16
            widths = [90] + [(sh.width - 90) / 6.0] * 6
            y = sh.grid(y, widths, 18, 8,
                        ["Player"] + ["Turn %d" % i for i in range(1, 7)],
                        header_h=22)
            y -= 8
            sh.para("Each turn, write the level reached and the score after the "
                    "final toss. The book:", y, st["small"])
            y -= 14
            y = _scoring_legend(sh, data, ["gonggi"], y, include_win=True,
                                fields=("stages",))
            y -= 12
            # Jianzi: the circle keeps one count and tries to beat it.
            jz = data.games["jianzi"]
            y = sh.para("<b>%s</b> — %s" % (esc(jz["title"]),
                                             esc(data.spec("jianzi", "players"))),
                        y, st["body"])
            y -= 2
            widths = [50, 90, 130, sh.width - 270]
            y = sh.grid(y, widths, 18, 8, ["Rally", "Count", "Players in the circle",
                                           "Best so far / notes"],
                        list(range(1, 9)), header_h=22)
            y -= 8
            y = _scoring_legend(sh, data, ["jianzi"], y, include_win=True)

        end_page()
        made["tailored"].append({"family": spec["family"], "games": spec["games"],
                                 "layout": layout})
    c.save()
    return made


def _scoring_legend(sh: Sheet, data: BookData, gids: list[str], y: float,
                    include_win: bool = False,
                    fields: tuple = ("scoring",)) -> float:
    """Print the book's own scoring lines, verbatim, as the sheet's legend."""
    st = sh.st
    for gid in gids:
        g = data.games[gid]
        lines = []
        for f in fields:
            v = g.get(f)
            if isinstance(v, list):
                lines += [str(x) for x in v]
            elif isinstance(v, str):
                lines.append(v)
        if include_win and g.get("winCondition"):
            lines.append("Win: " + g["winCondition"])
        if not lines:
            lines = ["—"]
        text = "<b>%s</b> (page %s) — %s" % (
            esc(g["title"]), data.page(gid) or "—",
            " ".join(esc(s) for s in lines))
        y = sh.para(text, y, st["small"])
        y -= 5
    return y


# ══════════════════════════════════════════════════════════════════════════
# 4 · BOARDS PACK
# ══════════════════════════════════════════════════════════════════════════
def select_boards(data: BookData, sv) -> tuple[list[dict], list[dict]]:
    """Choose one board diagram per game, the way the book's back matter does.

    Returns (included, excluded). Every exclusion carries a reason a reader
    can check against the book."""
    included, excluded = [], []
    for gid in data.game_ids_in_order:
        g = data.games[gid]
        title = g.get("title") or gid
        dids = g.get("diagrams") or []
        if not dids:
            excluded.append({"gameId": gid, "title": title,
                             "reason": "the book has no diagram for this game"})
            continue
        board = None
        for did in dids:
            meta = data.diagram_meta.get(did)
            if meta and meta.get("type") in BOARD_TYPES:
                board = (did, meta)
                break
        if board is None:
            excluded.append({"gameId": gid, "title": title,
                             "reason": "not a board — the book's diagram is a "
                                       "rule illustration (a move or capture)"})
            continue
        did, meta = board
        if meta.get("boardClass") == "bodily":
            excluded.append({"gameId": gid, "title": title,
                             "reason": "not a board — the diagram shows a "
                                       "layout on the ground or the players "
                                       "themselves"})
            continue
        doc = sv.parse(os.path.join(data.diagram_dir, did + ".svg"))
        colours = set()
        for op in doc["ops"]:
            for k in ("fill", "stroke"):
                v = op.get(k)
                if v:
                    colours.add(v)
        if colours - {(0, 0, 0), (255, 255, 255)}:
            excluded.append({"gameId": gid, "title": title,
                             "reason": "needs colour or grey to read"})
            continue
        # Largest scale on Letter with 0.5 in margins, either orientation.
        best = None
        for orient, (pw, ph) in (("portrait", (LETTER_W, LETTER_H)),
                                 ("landscape", (LETTER_H, LETTER_W))):
            aw = pw - 2 * MARGIN
            ah = ph - 2 * MARGIN - BOARD_TITLE_BLOCK
            s = min(aw / doc["widthPx"], ah / doc["heightPx"])
            if best is None or s > best[1] + 1e-6:
                best = (orient, s)
        orient, s = best
        # The SVG unit is a CSS px (96/in); at s = 0.75 the board prints at
        # the size it has in the book. Smaller than that is "too large".
        if s < 0.75:
            excluded.append({"gameId": gid, "title": title,
                             "reason": "too large for a Letter sheet"})
            continue
        included.append({"gameId": gid, "title": title, "diagramId": did,
                         "type": meta.get("type"), "boardClass": meta.get("boardClass"),
                         "orientation": orient, "scale": s, "doc": doc,
                         "page": data.page(gid),
                         "reconstructed": bool(g.get("reconstructed")),
                         "diagramReconstructed": bool(meta.get("reconstructed"))})
    return included, excluded


BOARD_TITLE_BLOCK = 58.0     # title + two caption lines + gap, in points


def build_boards_pack(data: BookData, out_path: str, sv) -> tuple[list, list]:
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.platypus import Paragraph

    st = styles()
    included, excluded = select_boards(data, sv)
    c = rl_canvas.Canvas(out_path, pagesize=(LETTER_W, LETTER_H))
    c.setTitle("%s — Boards Pack" % BOOK_TITLE)
    c.setAuthor(PUBLISHER)
    c.setCreator("companion_pack.py")

    # ── contents page ────────────────────────────────────────────────────
    sh = Sheet(c, st)
    y = sh.title("Boards Pack",
                 "%d printable boards, drawn from the book's own diagrams · %s"
                 % (len(included), BOOK_TITLE))
    y -= 6
    y = sh.para(
        "Each board is the diagram printed beside its game in the paperback, "
        "scaled up to fill a Letter sheet with half-inch margins, one to a "
        "page. Where the book's diagram shows the starting position, the "
        "pieces are shown here too: set your own counters on top of them. "
        "Print on card, or slip the sheet under glass. The page number after "
        "each title is where the rules are.", y, st["body"])
    y -= 4
    col_w = sh.width / 2.0
    lines = ["%s — page %s%s" % (b["title"], b["page"] or "—",
                                 " " + RECON_MARK if b["reconstructed"] else "")
             for b in included]
    half = (len(lines) + 1) // 2
    for ci, chunk in enumerate((lines[:half], lines[half:])):
        yy = y
        for i, ln in enumerate(chunk):
            c.setFont("GBSerif", 9)
            c.drawString(sh.left + ci * col_w, yy - 11, ln)
            yy -= 12.5
    y -= 12.5 * half + 8
    y = sh.para(esc(RECON_LEGEND), y, st["small"])
    y -= 10
    y = sh.para("<b>Not in this pack, and why.</b>", y, st["body"])
    for ex in excluded:
        y = sh.para("%s — %s." % (esc(ex["title"]), esc(ex["reason"])), y,
                    st["small"])
        y -= 1.5
    draw_footer(c, LETTER_W, c.getPageNumber())
    c.showPage()

    # ── one board per page ───────────────────────────────────────────────
    for b in included:
        pw, ph = ((LETTER_W, LETTER_H) if b["orientation"] == "portrait"
                  else (LETTER_H, LETTER_W))
        c.setPageSize((pw, ph))
        doc = b["doc"]
        c.setFont("GBSerif-B", 16)
        c.drawString(MARGIN, ph - MARGIN - 14, b["title"])
        c.setFont("GBSerif-I", 9)
        cap = "Board diagram from the book, page %s" % (b["page"] or "—")
        if b["type"] == "setup-illustration":
            cap += " · shown with the starting position, as printed in the book"
        if b["reconstructed"]:
            cap += " · %s rules presented as a reconstruction" % RECON_MARK
        c.drawString(MARGIN, ph - MARGIN - 27, cap)
        c.setFont("GBSerif", 8)
        c.drawString(MARGIN, ph - MARGIN - 39,
                     "Scaled ×%.2f from the book's diagram · %s · %s"
                     % (b["scale"] / 0.75, BOOK_TITLE, b["orientation"]))
        c.setLineWidth(0.6)
        c.line(MARGIN, ph - MARGIN - 45, pw - MARGIN, ph - MARGIN - 45)
        aw = pw - 2 * MARGIN
        ah = ph - 2 * MARGIN - BOARD_TITLE_BLOCK
        s = b["scale"]
        w_pt, h_pt = doc["widthPx"] * s, doc["heightPx"] * s
        x = MARGIN + (aw - w_pt) / 2.0
        y_top = MARGIN + (ah - h_pt) / 2.0 + h_pt
        sv.draw_reportlab(c, doc, x, y_top, w_pt, font="GBSerif")
        draw_footer(c, pw, c.getPageNumber())
        c.showPage()
    c.save()
    for b in included:
        b.pop("doc", None)
    return included, excluded


# ══════════════════════════════════════════════════════════════════════════
# manifest + verification
# ══════════════════════════════════════════════════════════════════════════
def pdf_page_count(path: str) -> int | None:
    try:
        out = subprocess.run(["pdfinfo", path], capture_output=True, text=True,
                             check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else None


def pdf_fonts_all_embedded(path: str) -> bool | None:
    try:
        out = subprocess.run(["pdffonts", path], capture_output=True, text=True,
                             check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    rows = [ln for ln in out.splitlines()[2:] if ln.strip()]
    return all(re.search(r"\s(yes)\s+(yes|no)\s+(yes|no)\s", ln) for ln in rows)


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


FILE_DESCRIPTIONS = {
    "game-index": (
        "Game Index",
        "Every game in the book on a few pages: players, time, age, where it "
        "comes from and the page it starts on, in the book's own order. Use it "
        "to pick tonight's game before you open the book."),
    "quick-reference-cards": (
        "Quick Reference Cards",
        "One cut-out card for each of the 56 games, with the players, time, age, "
        "materials and the objective, and the page where the full rules are. "
        "Four to a sheet with cut lines, so nobody has to hold the book open "
        "at the table."),
    "score-sheets": (
        "Score Sheets",
        "A general score grid for two to six players, a match record, and "
        "tally sheets for the games whose rules actually call for a count. "
        "Print as many as you need."),
    "boards-pack": (
        "Boards Pack",
        "Printable boards drawn from the book's own diagrams, one to a page and "
        "scaled up to fill a Letter sheet. Print on card or slip the page under "
        "glass, add counters, and the game is ready to play."),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), help="book project root")
    ap.add_argument("--out", required=True, help="output directory for the PDFs")
    args = ap.parse_args()

    sys.path.insert(0, os.path.join(args.root, "04_BUILD"))
    import svg_vector as sv           # the book's own SVG → vector renderer

    register_fonts()
    data = BookData(args.root)
    os.makedirs(args.out, exist_ok=True)

    print("  games in book order: %d" % len(data.game_ids_in_order))
    results = {}

    p = os.path.join(args.out, "game-index.pdf")
    n_index = build_game_index(data, p)
    results["game-index"] = {"path": p, "games": n_index}
    print("  game-index.pdf · %d games" % n_index)

    p = os.path.join(args.out, "quick-reference-cards.pdf")
    n_cards = build_cards(data, p)
    results["quick-reference-cards"] = {"path": p, "cards": n_cards}
    print("  quick-reference-cards.pdf · %d cards" % n_cards)

    p = os.path.join(args.out, "score-sheets.pdf")
    made = build_score_sheets(data, p)
    results["score-sheets"] = {"path": p, "sheets": made}
    print("  score-sheets.pdf · general %d · match record %d · tailored %d"
          % (made["general"], made["matchRecord"], len(made["tailored"])))

    p = os.path.join(args.out, "boards-pack.pdf")
    included, excluded = build_boards_pack(data, p, sv)
    results["boards-pack"] = {"path": p, "included": included, "excluded": excluded}
    print("  boards-pack.pdf · %d boards · %d excluded"
          % (len(included), len(excluded)))

    if n_index != len(data.games) or n_cards != len(data.games):
        raise SystemExit("count mismatch: %d games, %d index rows, %d cards"
                         % (len(data.games), n_index, n_cards))

    # ── manifest ─────────────────────────────────────────────────────────
    files = []
    ok = True
    for fid in ("game-index", "quick-reference-cards", "score-sheets", "boards-pack"):
        path = results[fid]["path"]
        pages = pdf_page_count(path)
        emb = pdf_fonts_all_embedded(path)
        size = os.path.getsize(path)
        title, desc = FILE_DESCRIPTIONS[fid]
        if pages is None:
            print("  ! pdfinfo unavailable for %s" % fid)
            ok = False
        if emb is False:
            print("  ! %s: a font is not embedded" % fid)
            ok = False
        files.append({
            "id": fid,
            "file": os.path.basename(path),
            "title": title,
            "description": desc,
            "pageCount": pages,
            "sizeBytes": size,
            "sha256": sha256(path),
            "meta": "PDF · US Letter · %s page%s"
                    % (pages if pages is not None else "—",
                       "" if pages == 1 else "s"),
            "fontsEmbedded": emb,
        })
        print("  %-24s %3s pages · %7d bytes · fonts embedded: %s"
              % (fid, pages, size, emb))

    manifest = {
        "$comment": [
            "Generated by 04_BUILD/companion_pack.py in the book project.",
            "Every figure comes from book.json, frontmatter.json and the",
            "measured paperback page map; nothing here is edited by hand.",
        ],
        "book": {
            "title": data.front["titlePage"]["title"],
            "publisher": data.front["titlePage"]["publisher"],
            "author": data.front["titlePage"]["author"],
            "edition": "paperback",
            "trim": "8.5 × 11 in",
            "pageCount": data.paperback_pages,
            "games": len(data.games),
        },
        "generatedAt": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "footer": FOOTER,
        "files": files,
        "gameIndex": {"games": n_index},
        "cards": {"games": n_cards, "perPage": 4},
        "scoreSheets": results["score-sheets"]["sheets"],
        "boards": {
            "count": len(included),
            "gameIds": [b["gameId"] for b in included],
            "boards": [{k: b[k] for k in ("gameId", "title", "diagramId", "type",
                                          "boardClass", "orientation", "page",
                                          "reconstructed")}
                       | {"scale": round(b["scale"] / 0.75, 3)}
                       for b in included],
            "excluded": excluded,
        },
        "dataProblems": data.problems,
    }
    mpath = os.path.join(args.out, "companion-manifest.json")
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("  manifest → %s" % mpath)
    if data.problems:
        print("  data notes (%d):" % len(data.problems))
        for pr in data.problems:
            print("    · " + pr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
