#!/usr/bin/env python3
"""
KINDLE EPUB — The Great Book of World Games (GBK-02), 2026 recovery edition
================================================================================
EPUB 3, reflowable. Built from the same read path as the print interior
(`interior.entry()`), so a printed page and a Kindle chapter cannot say
different things, and a non-string value can never be printed (WG-014).

Why reflowable: the print book's promise is a spread you can lay open on a
table. A scrolling screen has no spread to break, so each game is simply one
continuous chapter; a fixed-layout file would shrink an 8.5 × 11 in page onto
a phone and lock the reader's font and size settings.

Kindle-specific text: every paragraph that is true only of print is given a
"kindle" variant in the manuscript (see frontmatter_text.py). Page numbers
never appear; cross-references are links. The full-size boards are not
reproduced (they are for photocopying): the text points to the free companion
pack, which carries them.

Diagrams are inline SVG (vector, sharp at any size). Plates are colour JPEGs
from 07_ASSETS/plates_kindle/, sized to keep the file small — KDP charges a
delivery fee per megabyte on the 70 % royalty plan.

Exit codes: 0 pass · 1 gate red · 2 dependency missing
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import typo  # noqa: E402

for _p in (os.path.join(os.path.dirname(os.path.dirname(DEFAULT_ROOT)), "COMMON-AREA", "isbn"),
           "/home/emre/Downloads/MY-DİGİTAL-BOOK/COMMON-AREA/isbn"):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)
try:
    import registry as isbn_registry  # noqa: E402  (raises if the EPUB is not registered)
except ImportError:
    # A checkout without COMMON-AREA/isbn (the public CI runner). Only BUILDING needs the
    # registry, and build() refuses to run without it; the check and the CI skip path do not.
    # There is deliberately no stand-in identifier: a hard-coded ISBN is how the book's ISBN
    # was lost once before (see below).
    isbn_registry = None


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


_MD_I = re.compile(r"\*([^*\n]+)\*")


def E(s):
    """XHTML escape + typographic quotes + *italic* → <em>."""
    if not isinstance(s, str):
        raise ValueError("non-string value in printed text: %r" % (s,))
    if "{page:" in s:
        raise ValueError("a page reference reached the Kindle text: %r" % s[:120])
    return _MD_I.sub(r"<em>\1</em>", typo.xml_text(s))


CSS = """@charset "utf-8";
html{font-size:100%}
body{font-family:serif;line-height:1.45;margin:0 4%;text-align:left}
h1{font-size:1.55em;line-height:1.2;margin:1em 0 .15em;page-break-before:always}
h2{font-size:1.05em;margin:1.3em 0 .25em;text-transform:uppercase;letter-spacing:.04em;font-family:sans-serif}
h3{font-size:1em;margin:1em 0 .2em;font-family:sans-serif}
p{margin:.45em 0;text-indent:0}
.kicker{font-style:italic;font-size:.9em;margin:.1em 0 .8em}
table.quick{border-collapse:collapse;width:100%;margin:.6em 0 1em;font-family:sans-serif;font-size:.9em}
table.quick th{text-align:left;vertical-align:top;padding:.2em .6em .2em 0;white-space:nowrap}
table.quick td{vertical-align:top;padding:.2em 0}
table.quick{border-top:2px solid #000;border-bottom:1px solid #000}
.brief{font-family:sans-serif;font-size:.95em;margin:.4em 0 1em}
.box{border:1px solid #000;padding:.4em .7em;margin:.8em 0}
ol{margin:.3em 0 .8em 1.4em;padding:0}
ol li{margin:.25em 0}
.sources p{font-size:.85em;margin:.3em 0}
figure{margin:1em 0;text-align:center;page-break-inside:avoid}
figure svg{max-width:100%;height:auto}
figcaption{font-style:italic;font-size:.85em;margin-top:.3em}
.plate{text-align:center;margin:.6em 0;page-break-inside:avoid}
.plate img{max-width:100%;height:auto}
.platecap{font-size:.8em;text-align:left;margin:.2em 0 0 0;text-indent:0}
.standfirst{font-style:italic;font-size:1.05em;margin:.3em 0 1em}
table.list{border-collapse:collapse;width:100%;font-size:.88em;margin:.6em 0}
table.list th,table.list td{text-align:left;vertical-align:top;padding:.25em .4em;border-bottom:1px solid #999}
nav ol{list-style:none;margin-left:0}
nav ol ol{margin-left:1.2em}
.front h1{page-break-before:auto}
.idx p{margin:.15em 0}
"""

DIFF = {1: "Very easy", 2: "Easy", 3: "Moderate", 4: "Demanding", 5: "Expert"}


def xhtml(title, body, cls=""):
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
            'lang="en" xml:lang="en">\n<head><title>%s</title><meta charset="utf-8"/>'
            '<link rel="stylesheet" type="text/css" href="../style.css"/></head>\n'
            '<body%s>\n%s\n</body></html>\n'
            % (E(title), ' class="%s"' % cls if cls else "", body))


def svg_inline(path, max_w="30em"):
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    s = re.sub(r"<\?xml[^>]*\?>\s*", "", s)
    return s.replace("<svg ", '<svg role="img" style="max-width:%s" ' % max_w, 1)


def game_doc(e, ddir, plate, plate_alt, captions, plate_cap=""):
    import interior as I
    o = ['<h1 id="top">%s</h1>' % E(e["title"]),
         '<p class="kicker">%s · %s · %s</p>' % (E(e["culture"]), E(e["place"]), E(e["period"]))]
    if plate:
        cap = '<p class="platecap">%s</p>' % E(plate_cap) if plate_cap else ""
        o.append('<div class="plate"><img src="../images/%s" alt="%s"/>%s</div>' % (plate, E(plate_alt), cap))
    sp = e["spec"]
    rows = [("Players", sp["players"]), ("Time", sp["time"]), ("Age", sp["age"]),
            ("Difficulty", "%s (%d of 5)%s" % (DIFF[sp["difficulty"]], sp["difficulty"],
                                                (" — " + sp["difficultyNote"]) if sp["difficultyNote"] else "")),
            ("You need", sp["materials"]), ("Goal", e["objective"])]
    o.append('<table class="quick">%s</table>'
             % "".join("<tr><th>%s</th><td>%s</td></tr>" % (E(k), E(v)) for k, v in rows))
    o.append('<p class="brief">%s</p>' % E(e["atAGlance"]))
    o.append("<h2>Background</h2><p>%s</p>" % E(e["story"]))
    o.append("<h2>What you need</h2><p>%s</p>" % E(e["materials"]))
    if e["safety"]:
        o.append('<p class="box"><b>Safety.</b> %s</p>' % E(e["safety"]))
    if e["gamblingNote"]:
        o.append('<p class="box"><b>Stakes.</b> %s</p>' % E(e["gamblingNote"]))
    if e["reconstruction"]:
        rc = e["reconstruction"]
        o.append('<div class="box"><h3>Reconstruction</h3><p><b>What the sources give.</b> %s</p>'
                 '<p><b>What this book supplies.</b> %s</p></div>' % (E(rc["sources"]), E(rc["book"])))
    o.append("<h2>Setup</h2><ol>%s</ol>" % "".join("<li>%s</li>" % E(s) for s in e["setup"]))
    worked = e["workedTurn"].get("diagram")
    main = [d for d in e["diagrams"] if d != worked]

    def fig(did):
        p = os.path.join(ddir, did + ".svg")
        if not os.path.exists(p):
            raise FileNotFoundError(p)
        cap = captions.get(did, "")
        return "<figure>%s%s</figure>" % (svg_inline(p),
                                          "<figcaption>%s</figcaption>" % E(cap) if cap else "")
    if main:
        o.append(fig(main[0]))
    for b in e["rules"]:
        o.append("<h2>%s</h2><ol>%s</ol>" % (E(b["head"]), "".join("<li>%s</li>" % E(s)
                                                                    for s in b["steps"])))
    for d in main[1:]:
        o.append(fig(d))
    o.append("<h2>Ending and winning</h2><p><b>The end.</b> %s</p><p><b>The winner.</b> %s</p>"
             % (E(e["ending"]["end"]), E(e["ending"]["winner"])))
    o.append("<h2>Special situations</h2>" + "".join(
        "<p><b>%s.</b> %s</p>" % (E(x["q"].rstrip(".?")), E(x["a"])) for x in e["special"]))
    wt = e["workedTurn"]
    o.append("<h2>A worked turn</h2>")
    if wt.get("start"):
        o.append("<p><b>Start.</b> %s</p>" % E(wt["start"]))
    if wt.get("steps"):
        o.append("<ol>%s</ol>" % "".join("<li>%s</li>" % E(s) for s in wt["steps"]))
    if wt.get("result"):
        o.append("<p><b>Result.</b> %s</p>" % E(wt["result"]))
    if wt.get("next"):
        o.append("<p><b>Next.</b> %s</p>" % E(wt["next"]))
    if worked:
        o.append(fig(worked))
    o.append("<h2>Your first game</h2><p>%s</p>" % E(e["firstGame"]))
    if e["variants"]:
        o.append("<h2>Variants</h2>" + "".join(
            "<p><b>%s</b>%s. %s</p>" % (E(v["name"]), " (house rule)" if v["kind"] == "house rule" else "",
                                        E(v["note"])) for v in e["variants"]))
    src = "".join("<p>%s</p>" % E(I.source_line(s)) for s in e["sources"])
    if e["rulings"]:
        src += "<p><b>†</b> This book’s own rulings, where the sources are silent: %s</p>" % " ".join(
            E(r) for r in e["rulings"])
    o.append('<div class="sources"><h2>Sources</h2>%s</div>' % src)
    return "\n".join(o)


def build(root):
    import interior as I
    cfg = load(os.path.join(root, "project_config.json"))
    mdir = cfg["language"]["commercialManuscriptDir"]
    if not os.path.exists(os.path.join(root, mdir, "book.json")):
        print("  · manuscript not in this checkout — EPUB SKIPPED (expected in CI)")
        return 0
    if isbn_registry is None:
        print("  ✗ ISBN registry (COMMON-AREA/isbn/registry.py) not found — the EPUB is not built "
              "without the book's registered identifier")
        return 1
    book = load(os.path.join(root, mdir, "book.json"))
    fm = load(os.path.join(root, mdir, "frontmatter.json"))
    bm = load(os.path.join(root, mdir, "backmatter_book.json"))
    entries = [I.entry(g) for g in book["games"]]
    by_id = {e["gameId"]: e for e in entries}
    titles = {e["gameId"]: I.plain(e["title"]) for e in entries}
    captions = {}
    for g, e in zip(book["games"], entries):
        specs = g.get("diagramSpecs") or g.get("diagrams", [])
        e["diagrams"] = [d["id"] if isinstance(d, dict) else d for d in specs]
        for d in specs:
            if isinstance(d, dict):
                captions[d["id"]] = d.get("caption", "")
    ddir = os.path.join(root, "07_ASSETS", "diagrams")
    pmap = load(os.path.join(root, "01_SOURCE", "plates.json"))["plates"]
    tp, im = fm["titlePage"], fm["imprint"]
    ed = "kindle"
    files, spine, nav = [], [], []
    images = {}

    def add(name, title, body, cls="", level=None, label=None):
        files.append(("OEBPS/text/%s" % name, xhtml(title, body, cls)))
        spine.append(name)
        if level is not None:
            nav.append((name, label or title, level))

    def link(gid):
        return '<a href="game-%s.xhtml">%s</a>' % (gid, E(titles[gid]))

    # cover
    cover = os.path.join(root, "08_OUTPUT", "KINDLE", "GreatBookOfWorldGames_cover_kindle.jpg")
    if not os.path.exists(cover):
        raise FileNotFoundError("Kindle cover missing: %s (build the covers first)" % cover)
    images["cover.jpg"] = cover
    add("cover.xhtml", "Cover", '<div style="text-align:center"><img src="../images/cover.jpg" '
        'alt="%s" style="max-width:100%%;height:auto"/></div>' % E(tp["title"]), "front", 0, "Cover")
    add("title.xhtml", tp["title"], '<h1>%s</h1><p class="standfirst">%s</p><p>%s</p><p>%s</p>'
        % (E(tp["title"]), E(tp["subtitle"]), E(tp["author"]), E(tp["publisher"])), "front", 0,
        "Title page")
    isbn_e = isbn_registry.require(os.path.join(root, "08_OUTPUT", "KINDLE", "GreatBookOfWorldGames.epub"))
    isbn_e = "%s-%s-%s-%s-%s" % (isbn_e[:3], isbn_e[3:6], isbn_e[6:8], isbn_e[8:12], isbn_e[12]) \
        if isbn_e.isdigit() and isbn_e.startswith("978625") else isbn_e
    imp = ["<h1>Copyright</h1>", "<p>%s</p>" % E(im["copyright"]), "<p>%s</p>" % E(im["publisher"]),
           "<p>%s · Volume %s</p>" % (E(tp["series"]), tp["volume"]),
           "<p>%s</p>" % E(I.ed_text(im["edition"], ed))]
    if isbn_e:
        imp.append("<p>ISBN (electronic edition): %s</p>" % E(str(isbn_e)))
    imp += ["<p>%s</p>" % E(I.ed_text(im["rights"], ed)), "<p>%s</p>" % E(I.ed_text(im["aiDisclosure"], ed))]
    add("imprint.xhtml", "Copyright", "\n".join(imp), "front", 0, "Copyright")
    for s in fm["sections"]:
        b = ["<h1>%s</h1>" % E(s["title"])]
        for para in s.get("paragraphs", []):
            b.append("<p>%s</p>" % E(I.ed_text(para, ed)))
        for sub in s.get("sections", []):
            if isinstance(sub, dict) and "heading" not in sub:
                sub = sub.get(ed) or sub.get("kindle") or sub.get("default")
            b.append("<h2>%s</h2><p>%s</p>" % (E(sub["heading"]), E(I.ed_text(sub["text"], ed))))
        for row in s.get("table") or []:
            b.append("<h2>%s · %s</h2><p>%s <em>%s</em></p>" % (E(row["n"]), E(row["name"]),
                                                                E(row["idea"]), E(row["test"])))
        if s.get("closing"):
            b.append("<p>%s</p>" % E(I.ed_text(s["closing"], ed)))
        if s["id"] == "tonight":
            b.append(tonight_table(entries, link))
        add("%s.xhtml" % s["id"], s["title"], "\n".join(b), "front", 0, s["title"])
    openers = {o["family"]: o for o in fm["familyOpeners"]}
    for item in fm["contents"]:
        if item["kind"] == "family-opener":
            o = openers[item["family"]]
            fam = [by_id[c["gameId"]] for c in fm["contents"]
                   if c["kind"] == "game" and c["family"] == item["family"]]
            b = ['<p class="kicker">Part %s</p><h1>%s</h1>' % (E(o["numeral"]), E(o["title"])),
                 '<p class="standfirst">%s</p>' % E(o["standfirst"])]
            b += ["<p>%s</p>" % E(I.ed_text(p, ed)) for p in o["paragraphs"]]
            b.append("<h2>The family at a glance</h2><table class=\"list\"><tr><th>Game</th>"
                     "<th>Players</th><th>Time</th><th>Age</th><th>Difficulty</th></tr>%s</table>"
                     % "".join("<tr><td>%s<br/>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                               % (link(x["gameId"]), E(x["culture"]), E(x["spec"]["players"]),
                                  E(x["spec"]["time"]), E(x["spec"]["age"]),
                                  "%s (%d of 5)" % (DIFF[x["spec"]["difficulty"]], x["spec"]["difficulty"]))
                               for x in fam))
            add("part-%s.xhtml" % o["family"], o["title"], "\n".join(b), "", 0, "Part %s · %s" % (
                o["numeral"], o["title"]))
            continue
        e = by_id[item["gameId"]]
        rec = pmap[e["gameId"]]
        fn = os.path.basename(rec["kindle"])
        images[fn] = os.path.join(root, rec["kindle"])
        add("game-%s.xhtml" % e["gameId"], e["title"],
            game_doc(e, ddir, fn, rec.get("alt") or ("Illustration for " + titles[e["gameId"]]), captions,
                     I.plate_caption(rec)),
            "", 1, e["title"])
    # back matter
    if bm.get("glossary"):
        g = ["<h1>Glossary</h1>"] + ["<p><b>%s</b> %s%s</p>" % (
            E(t["term"]), E(t["definition"]),
            (" (%s)" % ", ".join(link(x) for x in t["games"])) if t.get("games") else "")
            for t in sorted(bm["glossary"], key=lambda x: x["term"].lower())]
        add("glossary.xhtml", "Glossary", "\n".join(g), "front idx", 0, "Glossary")
    if bm.get("bibliography"):
        b = ["<h1>Sources</h1><p>%s</p>" % E(I.ed_text(bm["bibliographyIntro"], ed))]
        for w in bm["bibliography"]:
            b.append("<p>%s. %s</p>" % (E(w["citation"].rstrip(".")), ", ".join(
                link(x) + ((" (%s)" % E(w["pages"][x])) if w.get("pages", {}).get(x) else "")
                for x in w["games"])))
        add("sources.xhtml", "Sources", "\n".join(b), "front idx", 0, "Sources")
    rows = []
    for name, gid, note in I.a_to_z(entries):
        if titles[gid] == name:
            rows.append("<p><b>%s</b></p>" % link(gid))
        else:
            rows.append("<p>%s <em>see</em> %s</p>" % (E(name), link(gid)))
    add("index-az.xhtml", "Index of Games and Other Names", "<h1>Index of Games and Other Names</h1>"
        + "\n".join(rows), "front idx", 0, "Index of games and other names")
    ix = ["<h1>Index by Culture, Age and Difficulty</h1>", "<h2>By culture</h2>"]
    for cul in sorted({e["culture"] for e in entries}, key=lambda s: I.plain(s).lower()):
        ix.append("<p><b>%s</b>: %s</p>" % (E(cul), ", ".join(
            link(e["gameId"]) for e in sorted(entries, key=lambda x: I.plain(x["title"]).lower())
            if e["culture"] == cul)))
    ix.append("<h2>By age</h2>")
    for _, lbl in I.AGE_BUCKETS:
        gs = [e for e in entries if I.age_bucket(e["spec"]) == lbl]
        if gs:
            ix.append("<p><b>%s</b>: %s</p>" % (E(lbl), ", ".join(link(e["gameId"]) for e in gs)))
    ix.append("<h2>By difficulty</h2>")
    for k in range(1, 6):
        gs = [e for e in entries if e["spec"]["difficulty"] == k]
        if gs:
            ix.append("<p><b>%s (%d of 5)</b>: %s</p>" % (DIFF[k], k, ", ".join(link(e["gameId"]) for e in gs)))
    add("index-culture.xhtml", "Index by Culture, Age and Difficulty", "\n".join(ix), "front idx", 0,
        "Index by culture, age and difficulty")
    if bm.get("inventedTraditions"):
        b = ["<h1>Invented Traditions</h1><p>%s</p>" % E(I.ed_text(bm["inventedIntro"], ed))]
        for t in bm["inventedTraditions"]:
            b.append("<h2>%s</h2><p><em>%s</em> %s</p>" % (E(t["claim"]), E(t["verdict"]), E(t["detail"])))
        add("invented.xhtml", "Invented Traditions", "\n".join(b), "front", 0, "Invented traditions")
    if bm.get("credits"):
        b = ["<h1>The Illustrations</h1>"] + ["<p>%s</p>" % E(I.ed_text(p, ed))
                                              for p in bm["credits"]["paragraphs"]]
        b.append('<table class="list"><tr><th>Game</th><th>Illustration</th></tr>%s</table>' % "".join(
            "<tr><td>%s</td><td>%s</td></tr>" % (E(r["game"]), E(r["credit"])) for r in bm["credits"]["plates"]))
        add("illustrations.xhtml", "The Illustrations", "\n".join(b), "front", 0, "The illustrations")
    if bm.get("aboutAuthor"):
        add("author.xhtml", "About the Author", "<h1>About the Author</h1>" + "".join(
            "<p>%s</p>" % E(I.ed_text(p, ed)) for p in bm["aboutAuthor"]), "front", 0, "About the author")
    comp = I.companion_block(root, cfg) or {}
    if comp.get("url"):
        b = ["<h1>%s</h1>" % E(comp["heading"]), '<p class="standfirst">%s</p>' % E(I.ed_text(comp["standfirst"], ed))]
        b += ["<p><b>%s.</b> %s</p>" % (E(it["name"]), E(it.get("detail", ""))) for it in comp["items"]]
        b.append('<p><b><a href="https://%s">%s</a></b></p>' % (E(comp["url"]), E(comp["url"])))
        b.append("<p>%s</p>" % E(I.ed_text(comp.get("note", "Free, and free of conditions: nothing to "
                                              "sign up for, no email asked, no account needed."), ed)))
        add("companion.xhtml", comp["heading"], "\n".join(b), "front", 0, "The free companion")
    return write_epub(root, cfg, tp, files, spine, nav, images, entries)


def tonight_table(entries, link):
    import interior as I
    grid = {}
    for e in entries:
        for pb in I.player_buckets(e["spec"]):
            for tb in I.time_bucket_keys(e["spec"]):
                grid.setdefault((tb, pb), []).append(e)
    rows = []
    for _, tl in I.TIME_BUCKETS:
        cells = []
        for pk, _ in I.PLAYER_BUCKETS:
            gs = sorted(grid.get((tl, pk), []), key=lambda x: I.plain(x["title"]).lower())
            cells.append(", ".join(link(e["gameId"]) for e in gs) or "—")
        rows.append("<tr><th>%s</th>%s</tr>" % (E(tl), "".join("<td>%s</td>" % c for c in cells)))
    return ('<table class="list"><tr><th></th><th>Two players</th><th>Three or four</th>'
            '<th>Five or more</th></tr>%s</table>' % "".join(rows))


def write_epub(root, cfg, tp, files, spine, nav, images, entries):
    out_dir = os.path.join(root, "08_OUTPUT", "KINDLE")
    path = os.path.join(out_dir, "GreatBookOfWorldGames.epub")
    uid = isbn_registry.identifier(path)
    svg_docs = {name.split("/")[-1] for name, data in files if "<svg" in data}
    manifest = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
                '<item id="css" href="style.css" media-type="text/css"/>']
    for i, fn in enumerate(sorted(images)):
        props = ' properties="cover-image"' if fn == "cover.jpg" else ""
        manifest.append('<item id="img%d" href="images/%s" media-type="image/jpeg"%s/>' % (i, fn, props))
    for i, n in enumerate(spine):
        props = ' properties="svg"' if n in svg_docs else ""
        manifest.append('<item id="s%d" href="text/%s" media-type="application/xhtml+xml"%s/>' % (i, n, props))
    # nav: two levels
    navh = ['<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>']
    i = 0
    while i < len(nav):
        name, label, lvl = nav[i]
        navh.append('<li><a href="text/%s">%s</a>' % (name, E(label)))
        j = i + 1
        kids = []
        while j < len(nav) and nav[j][2] > lvl:
            kids.append(nav[j])
            j += 1
        if kids:
            navh.append("<ol>" + "".join('<li><a href="text/%s">%s</a></li>' % (k[0], E(k[1])) for k in kids) + "</ol>")
        navh.append("</li>")
        i = j
    navh.append('</ol></nav><nav epub:type="landmarks" hidden=""><ol>'
                '<li><a epub:type="cover" href="text/cover.xhtml">Cover</a></li>'
                '<li><a epub:type="toc" href="nav.xhtml">Contents</a></li>'
                '<li><a epub:type="bodymatter" href="text/introduction.xhtml">Start</a></li></ol></nav>')
    nav_doc = ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" '
               'xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en"><head><title>Contents</title>'
               '<meta charset="utf-8"/><link rel="stylesheet" type="text/css" href="style.css"/></head><body>%s'
               '</body></html>\n' % "".join(navh))
    modified = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # the navigation document is also the book's inline table of contents (Kindle asks for one):
    # it is read after the copyright page, so the "Contents" landmark points at a spine item
    itemrefs = ['<itemref idref="s%d"/>' % i for i in range(len(spine))]
    itemrefs.insert(spine.index("imprint.xhtml") + 1, '<itemref idref="nav"/>')
    desc = cfg["metadata"].get("descriptionShort") or tp["subtitle"]
    opf = ('<?xml version="1.0" encoding="utf-8"?>\n<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
           'unique-identifier="bookid" xml:lang="en">\n<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
           '<dc:identifier id="bookid">%s</dc:identifier>\n'
           '<dc:title id="t-main">%s</dc:title>\n<meta refines="#t-main" property="title-type">main</meta>\n'
           '<dc:title id="t-sub">%s</dc:title>\n<meta refines="#t-sub" property="title-type">subtitle</meta>\n'
           '<dc:creator>%s</dc:creator>\n<dc:publisher>%s</dc:publisher>\n<dc:language>en</dc:language>\n'
           '<dc:description>%s</dc:description>\n<meta property="dcterms:modified">%s</meta>\n'
           '<meta property="schema:accessMode">textual</meta>\n<meta property="schema:accessMode">visual</meta>\n'
           '<meta property="schema:accessModeSufficient">textual,visual</meta>\n'
           '<meta property="schema:accessibilityFeature">structuralNavigation</meta>\n'
           '<meta property="schema:accessibilityFeature">alternativeText</meta>\n'
           '<meta property="schema:accessibilityFeature">tableOfContents</meta>\n'
           '<meta property="schema:accessibilityHazard">none</meta>\n'
           '<meta property="schema:accessibilitySummary">Reflowable text with a navigable table of contents; '
           'every illustration has a text description; board diagrams are vector drawings whose content is '
           'also given in the text of the rules.</meta>\n'
           '<meta name="cover" content="img%d"/>\n</metadata>\n<manifest>\n%s\n</manifest>\n<spine>\n%s\n</spine>\n'
           '</package>\n'
           % (uid, E(tp["title"]), E(tp["subtitle"]), E(tp["author"]), E(isbn_registry.IMPRINT_ASCII), E(desc),
              modified, sorted(images).index("cover.jpg"), "\n".join(manifest),
              "\n".join(itemrefs)))
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0" encoding="utf-8"?>\n<container version="1.0" '
                   'xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
                   '<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                   '</rootfiles></container>\n', zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav_doc, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, zipfile.ZIP_DEFLATED)
        for name, data in files:
            z.writestr(name, data, zipfile.ZIP_DEFLATED)
        for fn, src in sorted(images.items()):
            with open(src, "rb") as fh:
                data = fh.read()
            if fn == "cover.jpg":
                # the marketplace cover is uploaded to KDP separately; the copy inside the book only
                # has to fill a reading screen, and KDP charges Kindle delivery by the megabyte
                import io
                from PIL import Image
                im = Image.open(io.BytesIO(data)).convert("RGB")
                if im.height > 1600:
                    im = im.resize((round(im.width * 1600 / im.height), 1600), Image.LANCZOS)
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=85, optimize=True, progressive=True)
                data = buf.getvalue()
            z.writestr("OEBPS/images/%s" % fn, data, zipfile.ZIP_DEFLATED)
    rep = {"format": "EPUB 3, reflowable", "file": os.path.relpath(path, root), "sha256": sha256(path),
           "bytes": os.path.getsize(path), "documents": len(files), "spineItems": len(spine),
           "games": len(entries), "platesEmbedded": len(images) - 1,
           "diagramsEmbedded": sum(len(e["diagrams"]) for e in entries),
           "identifier": uid, "modified": modified, "fixedLayout": False,
           "manuscriptSha256": sha256(os.path.join(root, "02_MANUSCRIPT", "book.json"))}
    dump(os.path.join(root, "06_REPORTS", "epub.json"), rep)
    print("  ✓ EPUB 3 · %d documents · %d games · %d diagrams · %d plates · %.1f MB"
          % (len(files), len(entries), rep["diagramsEmbedded"], rep["platesEmbedded"], rep["bytes"] / 1e6))
    return 0


def run_check(root):
    p = os.path.join(root, "06_REPORTS", "epub.json")
    if not os.path.exists(os.path.join(root, "02_MANUSCRIPT", "book.json")):
        print("  · manuscript not in this checkout — EPUB check SKIPPED (expected in CI)")
        return 0
    if not os.path.exists(p):
        print("  ✗ EPUB not built")
        return 1
    r = load(p)
    f = os.path.join(root, r["file"])
    if not os.path.exists(f) or sha256(f) != r["sha256"]:
        print("  ✗ EPUB missing or changed since its report")
        return 1
    if r.get("manuscriptSha256") != sha256(os.path.join(root, "02_MANUSCRIPT", "book.json")):
        print("  ✗ EPUB built from an older manuscript — rebuild")
        return 1
    with zipfile.ZipFile(f) as z:
        if z.namelist()[0] != "mimetype" or z.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
            print("  ✗ mimetype entry wrong")
            return 1
        import xml.etree.ElementTree as ET
        for n in z.namelist():
            if n.endswith((".xhtml", ".opf", ".xml")):
                data = z.read(n).decode("utf-8")
                ET.fromstring(data.encode("utf-8"))
                for bad in (">True<", ">False<", ">None<", "{page:", "000</"):
                    if bad in data:
                        print("  ✗ %s contains %r" % (n, bad))
                        return 1
    ep = shutil.which("epubcheck") or "/usr/local/bin/epubcheck"
    if os.path.exists(ep):
        res = subprocess.run([ep, f], capture_output=True, text=True)
        out = (res.stdout or "") + (res.stderr or "")
        if res.returncode != 0 or re.search(r"(\d+) (errors|fatal)", out) and not re.search(
                r"No errors or warnings detected", out):
            print("  ✗ EPUBCheck failed:\n%s" % out[-3000:])
            return 1
        print("  ✓ EPUBCheck: no errors or warnings")
    print("  ✓ EPUB valid · %d documents · %.1f MB" % (r["documents"], r["bytes"] / 1e6))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  KINDLE EPUB")
    print("=" * 74)
    rc = run_check(root) if args.check else build(root)
    print("=" * 74)
    return rc


if __name__ == "__main__":
    sys.exit(main())
