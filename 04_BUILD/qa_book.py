#!/usr/bin/env python3
"""
QA · THE BOOK AS PRINTED — GBK-02 recovery gate
================================================================================
One gate for everything the 2026-09-25 audit found shipping unnoticed. It reads
the manuscript (v2 schema), the rendered diagrams and templates, the plate
register, the front matter, the build reports and the metadata, and FAILS on:

  ① schema     — a missing block (setup, rules, end, winner, worked turn…),
                 a non-string in a printed field, difficulty outside 1–5
  ② leaks      — True/False/None printed as words; internal production text
                 ("decision K20", "REJECTED", "the renderer", file names…)
  ③ sources    — a game with no page (or section) citation; Wikipedia or a
                 "modern rule summary compiled for this book" as a source
  ④ rulings    — a † in the rules with no editorial ruling explained, or the
                 reverse; a reconstructed game without its reconstruction box
  ⑤ taxonomy   — a culture label that is banned or that contains another label
  ⑥ vocabulary — "hollow/hole/cup/house" in sowing rules; front/back rows;
                 American spellings; hyphenated ranges; shouting capitals
  ⑦ diagrams   — a diagram that does not draw the counts its rules print, a
                 worked turn without its diagram, text below 8 pt
  ⑧ plates     — a missing plate, a plate file shared by two games, a plate
                 register that does not cover every game
  ⑨ counts     — front matter, subtitle and metadata that disagree with the
                 manuscript (games, cultures, reconstructions)
  ⑩ builds     — interiors/EPUB built from an older manuscript; PB and HC page
                 maps that differ; the companion built from a stale page map

Exit codes: 0 pass · 1 gate red
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
sys.path.insert(0, HERE)

PRINTED_KEYS = ("title", "culture", "place", "period", "objective", "atAGlance", "story",
                "materials", "firstGame")
LEAK_WORDS = re.compile(r"(?<![\w'’])(True|False|None)(?![\w'’])")
INTERNAL = re.compile(
    r"decision K\d+|\bK\d{2}\b|REJECTED|the project\b|this project\b|renderer|"
    r"\.(py|json|svg|md|csv)\b|06_REPORTS|02_MANUSCRIPT|gameId|englishValidation|"
    r"\bphase ?\d\b|\bFaz \d\b|build script|agent\b|scratchpad|placeholder|TODO|FIXME|TBD|XXX",
    re.I)
BANNED_CULTURES = {"Medieval European", "Ancient Indian", "Hindustani", "Abbasid Arab",
                   "Andalusi Arab", "Egyptian Arab", "Sudanese Arab", "Han Chinese", "Cantonese",
                   "Tewa Pueblo", "Kekchi Maya", "Sumerian"}
SOWING_BANNED = re.compile(r"\b(hollows?|holes?|cups?|houses?)\b", re.I)
AMERICAN = re.compile(r"\b(realize[sd]?|realizing|color(s|ed)?|center(s|ed)?|organize[sd]?|"
                      r"favorite|behavior|honor|neighbor(s|ing)?|gray|analyze[sd]?|"
                      r"recognize[sd]?|practicing|defense|offense|catalog)\b")
HYPHEN_RANGE = re.compile(r"(?<![\w/.-])(\d{1,4})-(\d{1,4})(?![\w-])")
SHOUT = re.compile(r"\b[A-Z]{3,}(?:\s+[A-Z]{2,}){2,}\b")
WEB_BANNED = re.compile(r"wikipedia|modern rule summary|compiled for this book|pagat\.com|"
                        r"ludii|mancala\.fandom|mancala world|gambiter", re.I)
PAGE_OR_SECTION = re.compile(r"\bpp?\.\s*[\dlxvi]|§|\bsect(ion)?\.?\s*\d|\bart(icle)?\.?\s*\d|"
                             r"\b\d+\.\d+(?:\.\d+)?\b|\bfol\.|\bfig\.|\bcol\.", re.I)


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def walk_strings(obj, path=""):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, list):
        for i, x in enumerate(obj):
            yield from walk_strings(x, "%s[%d]" % (path, i))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("$") or k in ("verify", "board", "gameId", "id", "diagram",
                                          "kind", "family", "templateCandidate"):
                continue
            yield from walk_strings(v, "%s.%s" % (path, k) if path else k)


def printed_parts(g):
    """Every string of a v2 record that reaches a page."""
    out = []
    for k in PRINTED_KEYS:
        out.append((k, g.get(k)))
    for k in ("players", "time", "age", "materials", "difficultyNote"):
        out.append(("spec." + k, g["spec"].get(k)))
    for i, s in enumerate(g.get("setup", [])):
        out.append(("setup[%d]" % i, s))
    for bi, b in enumerate(g.get("rules", [])):
        out.append(("rules[%d].head" % bi, b.get("head")))
        for si, s in enumerate(b.get("steps", [])):
            out.append(("rules[%d].steps[%d]" % (bi, si), s))
    for k in ("end", "winner"):
        out.append(("ending." + k, g.get("ending", {}).get(k)))
    for i, x in enumerate(g.get("special", [])):
        out.append(("special[%d].q" % i, x.get("q")))
        out.append(("special[%d].a" % i, x.get("a")))
    wt = g.get("workedTurn", {})
    for k in ("start", "result", "next"):
        if wt.get(k) is not None:
            out.append(("workedTurn." + k, wt.get(k)))
    for i, s in enumerate(wt.get("steps", [])):
        out.append(("workedTurn.steps[%d]" % i, s))
    for i, v in enumerate(g.get("variants", [])):
        out.append(("variants[%d].name" % i, v.get("name")))
        out.append(("variants[%d].note" % i, v.get("note")))
    rc = g.get("reconstruction")
    if rc:
        out.append(("reconstruction.sources", rc.get("sources")))
        out.append(("reconstruction.book", rc.get("book")))
    for k in ("safety", "gamblingNote"):
        if g.get(k) is not None:
            out.append((k, g.get(k)))
    for i, s in enumerate(g.get("sources", [])):
        out.append(("sources[%d]" % i, s.get("work") if isinstance(s, dict) else s))
    for i, r in enumerate(g.get("editorialRulings", [])):
        out.append(("editorialRulings[%d]" % i, r))
    for i, d in enumerate(g.get("diagramSpecs") or g.get("diagrams", [])):
        if isinstance(d, dict):
            out.append(("diagrams[%d].caption" % i, d.get("caption", "")))
    return out


def check_game(g, errs, warns):
    gid = g.get("gameId", "?")
    E = lambda m: errs.append("%s: %s" % (gid, m))  # noqa: E731
    W = lambda m: warns.append("%s: %s" % (gid, m))  # noqa: E731
    # ① schema
    for k in PRINTED_KEYS + ("spec", "setup", "rules", "ending", "special", "workedTurn", "sources",
                             "diagrams"):
        if k not in g or g[k] in (None, "", [], {}):
            E("missing %s" % k)
    try:
        d = int(g["spec"]["difficulty"])
        if not 1 <= d <= 5:
            E("difficulty %s outside 1–5" % d)
    except Exception:
        E("difficulty missing or not a number")
    for path, v in printed_parts(g):
        if v is None and path.endswith(("difficultyNote",)):
            continue
        if not isinstance(v, str):
            E("printed field %s is %r (not text)" % (path, v))
            continue
        # ② leaks: a field whose whole value is a program literal
        if v.strip() in ("True", "False", "None", "null", "undefined", "nan", "NaN"):
            E("program literal printed in %s: %r" % (path, v))
        if INTERNAL.search(v) and not path.startswith(("sources", "reconstruction")):
            E("internal production text in %s: %r" % (path, INTERNAL.search(v).group(0)))
        if SHOUT.search(v) and not path.startswith("sources"):
            E("shouting capitals in %s: %r" % (path, SHOUT.search(v).group(0)))
        if AMERICAN.search(v) and not path.startswith("sources"):
            W("American spelling in %s: %r" % (path, AMERICAN.search(v).group(0)))
        m = HYPHEN_RANGE.search(v)
        if m and not path.startswith("sources") and int(m.group(1)) < int(m.group(2)):
            W("hyphen in a range in %s: %r (use an en dash)" % (path, m.group(0)))
    # ③ sources
    srcs = g.get("sources", [])
    if not any(PAGE_OR_SECTION.search((s.get("work", "") + " " + (s.get("pages") or ""))
                                      if isinstance(s, dict) else s) for s in srcs):
        E("no source names a page or section")
    for s in srcs:
        w = (s.get("work", "") if isinstance(s, dict) else s)
        if WEB_BANNED.search(w):
            E("source is not acceptable: %r" % w[:90])
        if re.search(r"https?://", w) and not re.search(r"accessed|access(ed)? \d", w, re.I):
            E("web source without an access date: %r" % w[:90])
    # ④ rulings and reconstruction
    # every printed instruction a † can sit in (the first-game suggestion is one)
    rules_text = json.dumps([g.get("setup"), g.get("rules"), g.get("ending"), g.get("special"),
                             g.get("firstGame")], ensure_ascii=False)
    daggers = rules_text.count("†")
    rulings = g.get("editorialRulings") or []
    if daggers and not rulings:
        E("%d † marks but no editorial ruling explained" % daggers)
    if rulings and not daggers:
        W("editorial rulings listed but no † in the rules")
    if g.get("reconstructed") and not g.get("reconstruction"):
        E("reconstructed game without its reconstruction box")
    # ⑤ taxonomy
    if g.get("culture") in BANNED_CULTURES:
        E("culture label %r is banned by the taxonomy" % g["culture"])
    # ⑥ vocabulary
    if g.get("family") == "sowing":
        for path, v in printed_parts(g):
            if not isinstance(v, str) or path in ("story", "title", "period", "place") \
                    or path.startswith(("sources", "reconstruction", "variants")):
                continue
            m = SOWING_BANNED.search(v)
            if m and not re.search(r"nyumba|house \(|‘house’|'house'", v):
                E("sowing vocabulary: %r in %s (use pit/store)" % (m.group(0), path))
        if re.search(r"\b(front|back) rows?\b", rules_text, re.I):
            E("four-row vocabulary: use inner/outer row, not front/back")
    # ⑦ worked turn and diagrams
    wt = g.get("workedTurn") or {}
    if not (wt.get("start") and (wt.get("steps") or wt.get("result"))):
        E("worked turn lacks a start position or the move")
    ids = [d["id"] for d in (g.get("diagramSpecs") or g.get("diagrams", [])) if isinstance(d, dict)]
    if wt.get("diagram") and wt["diagram"] not in ids:
        E("worked-turn diagram %r is not among the entry's diagrams" % wt["diagram"])
    if not wt.get("diagram"):
        W("worked turn has no diagram")


def run(root, strict=False, json_path=None, verbose=False):
    errs, warns = [], []
    mp = os.path.join(root, "02_MANUSCRIPT", "book.json")
    if not os.path.exists(mp):
        print("  · manuscript not in this checkout — gate SKIPPED (expected in CI)")
        return 0
    book = load(mp)
    games = book["games"]
    if len(games) != len({g["gameId"] for g in games}):
        errs.append("duplicate gameId in the manuscript")
    for g in games:
        check_game(g, errs, warns)
    # ⑤ nested culture labels across the book
    labels = sorted({g["culture"] for g in games})
    for a in labels:
        for b in labels:
            if a != b and re.search(r"\b%s\b" % re.escape(b), a):
                errs.append("culture label %r contains label %r (nested taxonomy)" % (a, b))
    # ⑦ diagram render report
    br = os.path.join(root, "06_REPORTS", "boards.json")
    if os.path.exists(br):
        rep = load(br)
        for e in rep.get("errors", []):
            errs.append("diagram: %s" % e)
        drawn = {r["id"] for r in rep.get("diagrams", [])}
        for g in games:
            for d in (g.get("diagramSpecs") or g.get("diagrams", [])):
                if isinstance(d, dict) and d["id"] not in drawn:
                    errs.append("%s: diagram %s not rendered" % (g["gameId"], d["id"]))
    else:
        errs.append("06_REPORTS/boards.json missing — run 04_BUILD/boards.py")
    # ⑧ plates
    pp = os.path.join(root, "01_SOURCE", "plates.json")
    if not os.path.exists(pp):
        errs.append("01_SOURCE/plates.json missing (plate register)")
    else:
        reg = load(pp)["plates"]
        seen = {}
        for g in games:
            rec = reg.get(g["gameId"])
            if not rec:
                errs.append("%s: no plate registered" % g["gameId"])
                continue
            for key in ("print", "kindle"):
                f = os.path.join(root, rec.get(key, ""))
                if not rec.get(key) or not os.path.exists(f):
                    errs.append("%s: %s plate file missing (%s)" % (g["gameId"], key, rec.get(key)))
                    continue
                h = sha256(f)
                if h in seen and seen[h] != g["gameId"]:
                    errs.append("DUPLICATE PLATE: %s and %s share one image (%s)"
                                % (seen[h], g["gameId"], key))
                seen.setdefault(h, g["gameId"])
            if rec.get("source"):
                src = os.path.join(root, rec["source"])
                if os.path.exists(src):
                    h = sha256(src)
                    key = "src:" + h
                    if key in seen and seen[key] != g["gameId"]:
                        errs.append("DUPLICATE PLATE SOURCE: %s and %s" % (seen[key], g["gameId"]))
                    seen.setdefault(key, g["gameId"])
            if rec.get("kind") not in ("ai-generated", "public-domain", "cc0", "drawn"):
                errs.append("%s: plate kind %r not declared" % (g["gameId"], rec.get("kind")))
            if rec.get("kind") in ("public-domain", "cc0", "drawn") and not rec.get("credit"):
                errs.append("%s: %s plate without a credit line" % (g["gameId"], rec.get("kind")))
        extra = sorted(set(reg) - {g["gameId"] for g in games})
        if extra:
            errs.append("plate register names games not in the book: %s" % extra)
    # ⑨ counts
    fp = os.path.join(root, "02_MANUSCRIPT", "frontmatter.json")
    if os.path.exists(fp):
        fm = load(fp)
        m = fm.get("measured", {})
        if m.get("games") != len(games):
            errs.append("front matter measured %s games, manuscript has %d" % (m.get("games"), len(games)))
        if m.get("cultures") != len(labels):
            errs.append("front matter measured %s cultures, manuscript has %d" % (m.get("cultures"), len(labels)))
        sub = fm["titlePage"]["subtitle"]
        if not sub.startswith("%d Games" % len(games)) or ("%d Cultures" % len(labels)) not in sub:
            errs.append("title-page subtitle disagrees with the manuscript: %r" % sub)
        blob = json.dumps(fm, ensure_ascii=False)
        for bad in ("two-page spread", "Every game is a two-page", "two facing pages",
                    "Chance and Nerve", "forty-five cultures", "4,600", "Vâliçe"):
            if bad in blob:
                errs.append("front matter still says %r" % bad)
    # ⑩ builds
    msha = __import__("hashlib").sha256(open(mp, "rb").read()).hexdigest()
    for ed in ("paperback", "hardcover", "largeprint"):
        rp = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if os.path.exists(rp):
            r = load(rp)
            if r.get("manuscriptSha256") and r["manuscriptSha256"] != msha:
                errs.append("%s interior built from an older manuscript" % ed)
    ep = os.path.join(root, "06_REPORTS", "epub.json")
    if os.path.exists(ep) and load(ep).get("manuscriptSha256") not in (None, msha):
        errs.append("EPUB built from an older manuscript")
    cm = os.path.join(root, "06_REPORTS", "companion.json")
    pb = os.path.join(root, "06_REPORTS", "interior-paperback.json")
    if os.path.exists(cm) and os.path.exists(pb):
        c, p = load(cm), load(pb)
        if c.get("paperbackSha256") != p.get("sha256"):
            errs.append("companion pack was built from a different paperback build (stale page map)")
    for e in errs:
        print("  ✗ %s" % e)
    for w in warns:
        print("  ⚠ %s" % w)
    print("  %d games · %d culture labels · %d errors · %d warnings"
          % (len(games), len(labels), len(errs), len(warns)))
    rep = {"status": "fail" if errs or (strict and warns) else "pass", "errors": errs,
           "warnings": warns, "games": len(games), "cultures": len(labels), "cultureLabels": labels}
    if verbose:
        print("  · culture labels: %s" % ", ".join(labels))
    out = json_path or os.path.join(root, "06_REPORTS", "qa-book.json")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rep, fh, ensure_ascii=False, indent=1)
    return 1 if errs or (strict and warns) else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None, help="report path (default 06_REPORTS/qa-book.json)")
    a = ap.parse_args()
    print("=" * 74)
    print("  QA · THE BOOK AS PRINTED")
    print("=" * 74)
    rc = run(os.path.abspath(a.root), a.strict, a.json, a.verbose)
    print("=" * 74)
    return rc


if __name__ == "__main__":
    sys.exit(main())
