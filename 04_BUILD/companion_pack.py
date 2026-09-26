#!/usr/bin/env python3
"""
COMPANION PACK — The Great Book of World Games (GBK-02), recovery edition
================================================================================
Builds the free companion from the FINAL book build. Nothing is typed by hand:
page numbers come from the interior reports of the build being released
(06_REPORTS/interior-{paperback,largeprint}.json), boards come from the same
board engine and the same specs as the book's diagrams, and card text is the
book's own quick-play text.

    boards-pack.pdf            one printable board per page, for every game that
                               is played on a board (not only those at the back)
    game-index.pdf             all games with players, time, age, difficulty,
                               and the page in the paperback/hardcover and in
                               the large print
    quick-reference-cards.pdf  one card per game, four to a US Letter sheet
    score-sheets.pdf           a general score grid, a match record, and tally
                               sheets for the games whose rules keep a score
    companion-manifest.json    counts, pages, checksums, and the build it serves

The companion refuses to build from a paperback report whose manuscript hash
differs from the current manuscript: a companion cut from a stale page map is
the 2026 defect this replaces (live site: 31 boards, 56 cards, 182-page map).

Usage:  python3 04_BUILD/companion_pack.py --out DIR [--root BOOK_ROOT]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

IN = 72.0
MM = 72.0 / 25.4
LW, LH = 8.5 * IN, 11.0 * IN
MARGIN = 0.55 * IN
URL = "valicepress.com/companion/world-games"
BOARD_TYPES = {"grid", "mancala", "graph", "track", "morris", "cross33", "alquerque"}


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def footer(c, n=None):
    c.saveState()
    c.setFont("GBSans", 8.5)
    c.setFillGray(0.3)
    c.drawString(MARGIN, 0.38 * IN, "%s · The Great Book of World Games" % URL)
    if n:
        c.drawRightString(LW - MARGIN, 0.38 * IN, str(n))
    c.restoreState()


class Ctx:
    def __init__(self, root):
        import interior as I
        self.I = I
        self.root = root
        self.cfg = load(os.path.join(root, "project_config.json"))
        self.book = load(os.path.join(root, "02_MANUSCRIPT", "book.json"))
        self.fm = load(os.path.join(root, "02_MANUSCRIPT", "frontmatter.json"))
        self.raw = {g["gameId"]: g for g in self.book["games"]}
        self.entries = {g["gameId"]: I.entry(g) for g in self.book["games"]}
        self.order = [c["gameId"] for c in self.fm["contents"] if c["kind"] == "game"]
        self.fam = {o["family"]: o for o in self.fm["familyOpeners"]}
        pb = load(os.path.join(root, "06_REPORTS", "interior-paperback.json"))
        lp = load(os.path.join(root, "06_REPORTS", "interior-largeprint.json"))
        hc = load(os.path.join(root, "06_REPORTS", "interior-hardcover.json"))
        msha = sha256(os.path.join(root, "02_MANUSCRIPT", "book.json"))
        for r, name in ((pb, "paperback"), (lp, "large print"), (hc, "hardcover")):
            if r.get("manuscriptSha256") != msha:
                raise RuntimeError("the %s build is older than the manuscript — build the book first" % name)
        if pb["pagemap"] != hc["pagemap"]:
            raise RuntimeError("paperback and hardcover page maps differ; the companion cannot serve both")
        self.pb, self.lp = pb, lp
        self.pages_pb = pb["pagemap"]
        self.pages_lp = lp["pagemap"]


def P(text, style):
    from reportlab.platypus import Paragraph
    return Paragraph(text, style)


def styles():
    from reportlab.lib.styles import ParagraphStyle
    return {
        "h": ParagraphStyle("h", fontName="GBTitle", fontSize=20, leading=24, spaceAfter=6),
        "t": ParagraphStyle("t", fontName="GBSans-B", fontSize=12, leading=14.5),
        "s": ParagraphStyle("s", fontName="GBSans", fontSize=9.4, leading=11.8),
        "si": ParagraphStyle("si", fontName="GBSans-I", fontSize=9, leading=11.5),
        "b": ParagraphStyle("b", fontName="GBSerif", fontSize=9.6, leading=12.2),
        "cell": ParagraphStyle("cell", fontName="GBSans", fontSize=8.6, leading=10.4),
        "cellb": ParagraphStyle("cellb", fontName="GBSans-B", fontSize=8.6, leading=10.4),
    }


def board_spec(raw):
    """The first board-type diagram of a game, stripped to the board and its fixed marks."""
    for d in (raw.get("diagramSpecs") or raw.get("diagrams", [])):
        if not isinstance(d, dict):
            continue
        b = d.get("board") or {}
        if b.get("type") in BOARD_TYPES:
            return {"id": d["id"] + "-board", "board": dict(b), "marks": d.get("marks") or [],
                    "labels": [l for l in (d.get("labels") or []) if l.get("fixed")]}
    return None


def build_boards(ctx, out, st):
    import boards as B
    import svg_vector as sv
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(out, pagesize=(LW, LH))
    c.setTitle("Boards pack — The Great Book of World Games")
    made = []
    tmp = os.path.join(ctx.root, "07_ASSETS", "companion_boards")
    os.makedirs(tmp, exist_ok=True)
    n = 0
    for gid in ctx.order:
        spec = board_spec(ctx.raw[gid])
        if not spec:
            continue
        e = ctx.entries[gid]
        B.set_label_scale(1.2)
        sc, rep = B.render_spec(spec, width=(LW - 2 * MARGIN) / MM, legend_on=bool(spec["marks"]))
        B.set_label_scale(1.0)
        path = os.path.join(tmp, spec["id"] + ".svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(sc.svg(e["title"]))
        doc = sv.parse(path)
        n += 1
        top = LH - MARGIN
        c.setFont("GBTitle", 20)
        c.drawString(MARGIN, top - 20, ctx.I.plain(e["title"]))
        c.setFont("GBSans", 9.5)
        c.drawString(MARGIN, top - 36, "%s · setup and rules: paperback and hardcover p. %s · large print p. %s"
                     % (ctx.I.plain(e["culture"]), ctx.pages_pb[gid], ctx.pages_lp[gid]))
        availw, availh = LW - 2 * MARGIN, LH - 2 * MARGIN - 60
        s = min(availw / (doc["widthMm"] * MM), availh / (doc["heightMm"] * MM))
        w = doc["widthMm"] * MM * s
        h = doc["heightMm"] * MM * s
        x = (LW - w) / 2
        y = top - 50
        sv.draw_reportlab(c, doc, x, y, w)
        footer(c, n)
        c.showPage()
        made.append({"gameId": gid, "page": n, "scale": round(s, 3)})
    c.save()
    return made


def build_index(ctx, out, st):
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
    doc = SimpleDocTemplate(out, pagesize=(LW, LH), leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=0.7 * IN,
                            title="Game index — The Great Book of World Games")
    I = ctx.I
    rows = [[P("<b>%s</b>" % h, st["cellb"]) for h in
             ("Game", "Culture", "Players", "Time", "Age", "Difficulty", "Page (PB/HC)", "Page (LP)")]]
    for gid in ctx.order:
        e = ctx.entries[gid]
        alt = ", ".join((a["name"] if isinstance(a, dict) else a) for a in (e.get("altNames") or [])[:3])
        rows.append([P("<b>%s</b>%s" % (I.rich(e["title"]), ("<br/><font size=7.5>%s</font>" % I.rich(alt)) if alt else ""),
                       st["cell"]),
                     P(I.rich(e["culture"]), st["cell"]), P(I.rich(e["spec"]["players"]), st["cell"]),
                     P(I.rich(e["spec"]["time"]), st["cell"]), P(I.rich(e["spec"]["age"]), st["cell"]),
                     P("%s %d/5" % (I.DIFF_LABEL[e["spec"]["difficulty"]], e["spec"]["difficulty"]), st["cell"]),
                     P(str(ctx.pages_pb[gid]), st["cell"]), P(str(ctx.pages_lp[gid]), st["cell"])])
    W = LW - 2 * MARGIN
    t = Table(rows, colWidths=[W * .25, W * .15, W * .11, W * .13, W * .08, W * .12, W * .08, W * .08],
              repeatRows=1)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.9, (0, 0, 0)),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.3, (0.6, 0.6, 0.6)),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    story = [P("Game index", st["h"]),
             P("Every game in the book, in the book's order, with the page it starts on in the paperback "
               "and hardcover (the same pages) and in the large print edition.", st["b"]), Spacer(1, 8), t]
    doc.build(story, onFirstPage=lambda c, d: footer(c), onLaterPages=lambda c, d: footer(c))
    return len(rows) - 1


def build_cards(ctx, out, st):
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Frame, KeepInFrame
    I = ctx.I
    c = canvas.Canvas(out, pagesize=(LW, LH))
    c.setTitle("Quick-reference cards — The Great Book of World Games")
    cw, ch = (LW - 2 * MARGIN) / 2, (LH - 2 * MARGIN) / 2
    n = 0
    for k, gid in enumerate(ctx.order):
        e = ctx.entries[gid]
        pos = k % 4
        x = MARGIN + (pos % 2) * cw
        y = LH - MARGIN - (pos // 2 + 1) * ch
        c.setDash(3, 3)
        c.setLineWidth(0.4)
        c.rect(x, y, cw, ch)
        c.setDash()
        sp = e["spec"]
        body = [P(I.rich(e["title"]), st["t"]),
                P("%s · %s" % (I.rich(e["culture"]), I.rich(e["place"])), st["si"]),
                P("<b>Players</b> %s · <b>Time</b> %s · <b>Age</b> %s" % (I.rich(sp["players"]), I.rich(sp["time"]),
                                                                        I.rich(sp["age"])), st["s"]),
                P("<b>Difficulty</b> %s (%d of 5)" % (I.DIFF_LABEL[sp["difficulty"]], sp["difficulty"]), st["s"]),
                P("<b>You need</b> %s" % I.rich(sp["materials"]), st["s"]),
                P("<b>Goal</b> %s" % I.rich(e["objective"]), st["s"]),
                P(I.rich(e["atAGlance"]), st["b"]),
                P("<b>Setup</b> " + " ".join("%d. %s" % (i, I.rich(s)) for i, s in enumerate(e["setup"], 1)), st["s"]),
                P("<i>Full rules, worked turn and sources: paperback and hardcover p. %s · large print p. %s</i>"
                  % (ctx.pages_pb[gid], ctx.pages_lp[gid]), st["si"])]
        f = Frame(x + 10, y + 10, cw - 20, ch - 20, showBoundary=0)
        f.addFromList([KeepInFrame(cw - 20, ch - 20, body, mode="shrink")], c)
        if pos == 3 or k == len(ctx.order) - 1:
            footer(c, k // 4 + 1)
            c.showPage()
        n += 1
    c.save()
    return n


SCORING_WORDS = re.compile(r"\b(score[sd]?|points?|tally|counters? won|tricks?)\b", re.I)


def build_scores(ctx, out, st):
    from reportlab.pdfgen import canvas
    I = ctx.I
    c = canvas.Canvas(out, pagesize=(LW, LH))
    c.setTitle("Score sheets — The Great Book of World Games")
    pages = 0

    def grid(title, sub, cols, rows, first_col="Round"):
        nonlocal pages
        pages += 1
        c.setFont("GBTitle", 18)
        c.drawString(MARGIN, LH - MARGIN - 18, title)
        c.setFont("GBSans", 9.5)
        c.drawString(MARGIN, LH - MARGIN - 34, sub)
        top = LH - MARGIN - 50
        W = LW - 2 * MARGIN
        rh = (top - 0.9 * IN) / (rows + 1)
        c.setLineWidth(0.6)
        cws = [W * 0.16] + [W * 0.84 / cols] * cols
        xs = [MARGIN]
        for w in cws:
            xs.append(xs[-1] + w)
        for r in range(rows + 2):
            y = top - r * rh
            c.line(MARGIN, y, MARGIN + W, y)
        for xx in xs:
            c.line(xx, top, xx, top - (rows + 1) * rh)
        c.setFont("GBSans-B", 9)
        c.drawString(MARGIN + 4, top - rh + 6, first_col)
        for i in range(cols):
            c.drawString(xs[i + 1] + 4, top - rh + 6, "Player %d" % (i + 1))
        c.setFont("GBSans", 9)
        for r in range(rows):
            c.drawString(MARGIN + 4, top - (r + 2) * rh + 6, str(r + 1) if r < rows - 1 else "Total")
        footer(c, pages)
        c.showPage()

    grid("Score sheet", "For any game in the book that keeps a score. Write names in the top row.", 4, 20)
    grid("Score sheet — six players", "For the games that seat more players.", 6, 20)
    grid("Match record", "Games in a match, who played which side, and who won each game.", 3, 20, "Game")
    tailored = []
    for gid in ctx.order:
        e = ctx.entries[gid]
        blob = " ".join(s for b in e["rules"] for s in b["steps"]) + " " + e["ending"]["winner"]
        if SCORING_WORDS.search(blob):
            tailored.append(gid)
    for gid in tailored:
        e = ctx.entries[gid]
        grid("%s — score sheet" % I.plain(e["title"]),
             "Rules: paperback and hardcover p. %s · large print p. %s. %s"
             % (ctx.pages_pb[gid], ctx.pages_lp[gid], I.plain(e["ending"]["winner"])[:95]), 4, 18)
    c.save()
    return pages, tailored


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    import interior as I
    I.register_fonts()
    import svg_vector
    I._SVG_FONTS.update(svg_vector.DEFAULT_FONTS)
    ctx = Ctx(root)
    os.makedirs(a.out, exist_ok=True)
    st = styles()
    files = {}
    boards = build_boards(ctx, os.path.join(a.out, "boards-pack.pdf"), st)
    n_index = build_index(ctx, os.path.join(a.out, "game-index.pdf"), st)
    n_cards = build_cards(ctx, os.path.join(a.out, "quick-reference-cards.pdf"), st)
    n_score, tailored = build_scores(ctx, os.path.join(a.out, "score-sheets.pdf"), st)
    import fitz
    for fn in ("boards-pack.pdf", "game-index.pdf", "quick-reference-cards.pdf", "score-sheets.pdf"):
        p = os.path.join(a.out, fn)
        files[fn] = {"pages": fitz.open(p).page_count, "bytes": os.path.getsize(p), "sha256": sha256(p)}
    man = {"$comment": ["Generated by 04_BUILD/companion_pack.py from the released build of the book.",
                        "Every count and page number is measured; nothing here is edited by hand."],
           "book": {"title": "The Great Book of World Games", "publisher": ctx.cfg["founder"]["publisher"],
                    "author": ctx.cfg["founder"]["author"], "games": len(ctx.order),
                    "pageCountPaperbackHardcover": ctx.pb["pageCount"],
                    "pageCountLargePrint": ctx.lp["pageCount"]},
           "builtFrom": {"paperbackSha256": ctx.pb["sha256"], "largePrintSha256": ctx.lp["sha256"],
                         "manuscriptSha256": ctx.pb["manuscriptSha256"]},
           "generatedAt": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
           "counts": {"boards": len(boards), "cards": n_cards, "indexGames": n_index,
                      "scoreSheetPages": n_score, "tailoredScoreSheets": len(tailored)},
           "boards": boards, "tailoredScoreSheets": tailored, "files": files}
    with open(os.path.join(a.out, "companion-manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=1)
    rep = dict(man["counts"], paperbackSha256=ctx.pb["sha256"], out=a.out, files=files)
    with open(os.path.join(root, "06_REPORTS", "companion.json"), "w", encoding="utf-8") as fh:
        json.dump(rep, fh, ensure_ascii=False, indent=1)
    print("  ✓ companion: %d boards · %d cards · index of %d · %d score-sheet pages (%d tailored)"
          % (len(boards), n_cards, n_index, n_score, len(tailored)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
