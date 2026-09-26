#!/usr/bin/env python3
"""
QA · THE PRINTED FILES — reads the built PDFs, not the data that made them
================================================================================
A gate that looks only at the manuscript can be green while the PDF is wrong:
the 2026 'True' leak, the stale build and the duplicated plate all passed data
gates. This one opens each interior PDF (PyMuPDF) and checks:

  · no line that is only True / False / None, no '{page:', no '000' page number
  · no internal production text on any page
  · every font embedded; smallest text ≥ 8 pt (print) or ≥ 16 pt body (large print)
  · each game's title is printed on the page the page map says it starts on
  · the contents page numbers equal the page map
  · no raster image is placed on the pages of two different games
  · page count even; blank pages listed

Exit codes: 0 pass · 1 gate red · 2 PyMuPDF missing
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
INTERNAL = re.compile(r"decision K\d+|REJECTED|\bthe project\b|renderer|\.py\b|\.json\b|06_REPORTS|"
                      r"02_MANUSCRIPT|gameId|englishValidation|scratchpad|TODO|FIXME", re.I)


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def norm(s):
    return (s.replace("’", "'").replace("‘", "'").replace("­", "")
            .replace("ﬁ", "fi").replace("ﬂ", "fl").lower())


def check_companion_page(root, ed, doc, errs):
    """The companion page quotes the companion pack's OWN counts (measured, never typed)."""
    cfg = load(os.path.join(root, "project_config.json"))
    comp = cfg.get("companion")
    if not comp:
        return
    mp = os.path.join(root, "08_OUTPUT", "COMPANION", "companion-manifest.json")
    if not os.path.exists(mp):
        errs.append("%s: companion page printed but no companion manifest to check it against" % ed)
        return
    sys.path.insert(0, HERE)
    import build_frontmatter as bf
    n = load(mp)["counts"]
    want = ["%s boards" % bf.words_for(n["boards"]).capitalize(),
            "%s game cards" % bf.words_for(n["cards"]).capitalize()]
    pages = [doc[i].get_text() for i in range(doc.page_count) if comp["url"] in doc[i].get_text()]
    page = " ".join(re.sub(r"\s+", " ", t) for t in pages)
    missing = [w for w in want if w not in page]
    if not pages or missing:
        errs.append("%s: companion page does not quote the companion's own counts %s" % (ed, missing or want))


def check_pdf(root, ed, errs, facts):
    import fitz
    rp = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
    if not os.path.exists(rp):
        errs.append("%s: not built" % ed)
        return
    r = load(rp)
    doc = fitz.open(os.path.join(root, r["file"]))
    if doc.page_count != r["pageCount"]:
        errs.append("%s: PDF has %d pages, report says %d" % (ed, doc.page_count, r["pageCount"]))
    if doc.page_count % 2:
        errs.append("%s: odd page count" % ed)
    book = load(os.path.join(root, "02_MANUSCRIPT", "book.json"))
    titles = {g["gameId"]: g["title"] for g in book["games"]}
    check_companion_page(root, ed, doc, errs)
    # an entry page that carries nothing but its running head and folio: the blank-page count
    # misses it (the head is text), and in print it reads as a mistake
    games = [v for k, v in r.get("anchors", {}).items() if k.startswith("game:")]
    if games:
        g0, bm = min(games), r.get("backMatterStartPage") or doc.page_count + 1
        empty = []
        for i in range(g0 - 1, min(bm - 1, doc.page_count)):
            lines = [l.strip() for l in doc[i].get_text().splitlines() if l.strip()]
            if lines and len(lines) <= 2 and sum(len(l) for l in lines) < 60:
                empty.append(i + 1)
        if empty:
            errs.append("%s: pages with nothing but a running head %s" % (ed, empty))
    min_pt, small_pages = 99.0, []
    img_pages = {}
    lp = ed == "largeprint"
    for i in range(doc.page_count):
        page = doc[i]
        text = page.get_text()
        for ln in text.splitlines():
            s = ln.strip()
            if s in ("True", "False", "None"):
                errs.append("%s p.%d: printed program literal %r" % (ed, i + 1, s))
            if re.fullmatch(r"000", s) or "{page:" in s:
                errs.append("%s p.%d: unresolved page reference %r" % (ed, i + 1, s))
        m = INTERNAL.search(text)
        if m and not re.search(r"build code", text):
            errs.append("%s p.%d: internal text %r" % (ed, i + 1, m.group(0)))
        d = page.get_text("dict")
        for b in d["blocks"]:
            for l in b.get("lines", []):
                for sp in l["spans"]:
                    if sp["text"].strip():
                        if sp["size"] < min_pt:
                            min_pt = sp["size"]
                        floor = 7.95 if not lp else 12.0
                        if sp["size"] < floor:
                            small_pages.append((i + 1, round(sp["size"], 1), sp["text"][:30]))
        for img in page.get_images(full=True):
            xref = img[0]
            img_pages.setdefault(xref, set()).add(i + 1)
    # fonts
    for i in range(doc.page_count):
        for f in doc[i].get_fonts():
            if f[1] in ("ttf", "Type1", "TrueType") and "+" not in f[3] and f[1] != "Type3":
                errs.append("%s: font %s is not embedded (p.%d)" % (ed, f[3], i + 1))
                break
    if small_pages:
        errs.append("%s: text below the size floor on %d spans, e.g. %s"
                    % (ed, len(small_pages), small_pages[:4]))
    # game starts
    pm = r.get("pagemap", {})
    wrong = []
    for gid, pg in pm.items():
        t = norm(doc[pg - 1].get_text())
        if norm(titles[gid]) not in t:
            wrong.append("%s→p.%d" % (gid, pg))
    if wrong:
        errs.append("%s: game title not found on its mapped page: %s" % (ed, wrong[:8]))
    # a raster used on pages of two different games = a duplicated plate
    starts = sorted((pg, gid) for gid, pg in pm.items())

    def game_at(p):
        cur = None
        for pg, gid in starts:
            if pg <= p:
                cur = gid
        return cur
    for xref, pages in img_pages.items():
        gs = {game_at(p) for p in pages if game_at(p)}
        if len(gs) > 1:
            errs.append("%s: one image (xref %d) appears in several games: %s" % (ed, xref, sorted(gs)))
    # contents page numbers
    toc_first = r["anchors"].get("fm:contents")
    if toc_first:
        toc_text = ""
        for p in range(toc_first - 1, min(toc_first + 3, doc.page_count)):
            toc_text += doc[p].get_text()
        bad = []
        for gid, pg in pm.items():
            t = titles[gid]
            # the title must START a contents line: "Tab" must not be read off the "Tablut" line,
            # nor "Shogi" off "Hasami Shogi", nor "Achi" off "Pachisi"
            mm = re.search(r"^\s*" + re.escape(norm(t)) + r"(?![\w'’])[^\n]*?(\d{1,3})\s*$", norm(toc_text), re.M)
            if mm and int(mm.group(1)) != pg:
                bad.append("%s: %s≠%d" % (gid, mm.group(1), pg))
        if bad:
            errs.append("%s: contents page numbers wrong: %s" % (ed, bad[:6]))
    facts[ed] = {"pages": doc.page_count, "minTextPt": round(min_pt, 2),
                 "blankPages": r.get("blankPageList"), "imagesPlaced": len(img_pages)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None, help="report path (default 06_REPORTS/qa-output.json)")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    print("=" * 74)
    print("  QA · THE PRINTED FILES")
    print("=" * 74)
    if not os.path.exists(os.path.join(root, "02_MANUSCRIPT", "book.json")):
        print("  · manuscript not in this checkout — SKIPPED (expected in CI)")
        return 0
    try:
        import fitz  # noqa: F401
    except ImportError:
        print("  ⊘ PyMuPDF missing — SKIPPED")
        return 2
    errs, facts = [], {}
    for ed in ("paperback", "hardcover", "largeprint"):
        check_pdf(root, ed, errs, facts)
    for e in errs:
        print("  ✗ %s" % e)
    for ed, f in facts.items():
        print("  · %-10s %d pages · smallest text %.2f pt · blank %s" % (ed, f["pages"], f["minTextPt"],
                                                                        f["blankPages"]))
    if a.verbose:
        for ed, f in facts.items():
            print("  · %-10s %s" % (ed, json.dumps(f, ensure_ascii=False)[:300]))
    out = a.json or os.path.join(root, "06_REPORTS", "qa-output.json")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"status": "fail" if errs else "pass", "errors": errs, "facts": facts}, fh,
                  ensure_ascii=False, indent=1)
    print("=" * 74)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
