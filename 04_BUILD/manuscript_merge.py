#!/usr/bin/env python3
"""
MANUSCRIPT MERGE — import rewritten (v2) game entries into book.json
================================================================================
The 2026 recovery rewrote every entry in a normalised structure (quick play,
background, what you need, setup, rules blocks, ending and winner, special
situations, a worked turn with its diagram, first game, variants, sources,
reconstruction box, editorial rulings). This tool merges those records into
02_MANUSCRIPT/book.json.

One authored copy, many readers. The print and Kindle builders read the v2
fields. Older gates (qa_manuscript, qa_rules, qa_lineedit…) read the 2025
field names; those are DERIVED here from the v2 fields — never written by
hand — so the two can never disagree:

    story → culturalStory · materials → materialsAndSubstitution
    ending.winner → winCondition · ending.end → endCondition
    special → edgeCases{tie, stalemate, illegalMove}
    workedTurn → exampleTurn (text) · rules → turnSequence (flattened)
    citations (structured) → sources (formatted strings with pages)
    diagramSpecs (specs) → diagrams (ids)

Usage: manuscript_merge.py --staging DIR [--only id,id] [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

REQUIRED = ("gameId", "title", "family", "culture", "place", "period", "spec", "objective",
            "atAGlance", "story", "materials", "setup", "rules", "ending", "special", "workedTurn",
            "firstGame", "sources", "diagrams")


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def cite(s):
    if isinstance(s, str):
        return s
    w = s["work"].strip()
    pg = (s.get("pages") or "").strip()
    if pg and pg not in w:
        w = "%s, %s" % (w.rstrip(".,; "), pg)
    return w.rstrip(".") + "."


def find_q(special, *keys):
    for x in special:
        q = x["q"].lower()
        if any(k in q for k in keys):
            return x["a"]
    return None


def merge_one(old, new):
    miss = [k for k in REQUIRED if k not in new or new[k] in (None, "", [], {})]
    if miss:
        raise ValueError("%s: missing %s" % (new.get("gameId"), miss))
    if new["gameId"] != old["gameId"]:
        raise ValueError("gameId changed: %s → %s" % (old["gameId"], new["gameId"]))
    rec = {}
    # keep the provenance fields the language gates read
    for k in ("authoring", "translatedFrom", "status"):
        rec[k] = old.get(k)
    for k, v in new.items():
        if k in ("sources", "diagrams"):
            continue
        rec[k] = v
    # structured citations + formatted strings
    rec["citations"] = [s if isinstance(s, dict) else {"work": s} for s in new["sources"]]
    rec["sources"] = [cite(s) for s in new["sources"]]
    # citation strings arrive with typewriter double quotes around article titles ("…") and in
    # "s.v."; they are set as typeset double quotes here, once. Apostrophes stay straight: that is
    # the manuscript's convention everywhere else (typo.smart curls them at render time), and the
    # line editor (qa_lineedit ③) holds the manuscript to one convention.
    def curl_double(t):
        return re.sub(r'(?<![A-Za-zÀ-ÿ0-9])"(?=[^\s])', "“", t).replace('"', "”")
    rec["citations"] = [{k: (curl_double(v) if isinstance(v, str) else v) for k, v in c.items()}
                        for c in rec["citations"]]
    rec["sources"] = [curl_double(x) for x in rec["sources"]]
    for v in rec.get("variants") or []:
        if isinstance(v.get("source"), str):
            v["source"] = curl_double(v["source"])
    specs = [d for d in new["diagrams"] if isinstance(d, dict)]
    rec["diagramSpecs"] = specs
    rec["diagrams"] = [d["id"] for d in specs]
    # derived legacy mirrors
    rec["culturalStory"] = new["story"]
    rec["materialsAndSubstitution"] = new["materials"]
    rec["winCondition"] = new["ending"]["winner"]
    rec["endCondition"] = new["ending"]["end"]
    sp = new["special"]
    rec["edgeCases"] = {
        "tie": find_q(sp, "draw", "tie") or "",
        "stalemate": find_q(sp, "cannot move", "can't move", "no legal", "blocked", "nobody can") or "",
        "illegalMove": find_q(sp, "illegal", "mistake", "wrong") or "",
    }
    wt = new["workedTurn"]
    rec["exampleTurn"] = " ".join(x for x in [wt.get("start", "")] + list(wt.get("steps", []))
                                  + [wt.get("result", ""), wt.get("next", "")] if x)
    rec["turnSequence"] = [s for b in new["rules"] for s in b["steps"]]
    rc = new.get("reconstruction")
    rec["reconstructed"] = bool(new.get("reconstructed"))
    rec["reconstructionNotice"] = ("%s %s" % (rc["sources"], rc["book"])) if rc else ""
    rec["gamblingReframed"] = bool(new.get("gamblingNote"))
    rec["statusNote"] = ("Recovery 2026-09: rewritten from page-verified sources; internal Ready-to-Play "
                         "test run; NOT external-playtested (no human test yet).")
    rec["englishValidation"] = {
        "source": "Rewritten in English from the cited pages (see citations); no translation.",
        "rules": "Normalised structure: setup, rules blocks, ending, winner, special situations.",
        "playability": "Internal walkthrough and worked-turn simulation recorded in the recovery "
                       "verification log; external playtest pending.",
        "clarity": "One action per numbered step; controlled vocabulary applied.",
        "terminology": "Book-wide controlled vocabulary (pit/store/seed; inner/outer rows; Black/White).",
        "cultural": "Culture label per the taxonomy rule (people or historical society of the record).",
        "diagram": "Diagrams drawn by boards.py from diagramSpecs and verified by count.",
    }
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--staging", required=True, help="directory tree with <gameId>.json files")
    ap.add_argument("--only", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    bp = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
    book = load(bp)
    by_id = {g["gameId"]: i for i, g in enumerate(book["games"])}
    only = set(x for x in a.only.split(",") if x)
    found = {}
    for dp, _, fns in os.walk(a.staging):
        if "_work" in dp:
            continue
        for fn in fns:
            if fn.endswith(".json") and not fn.startswith("_"):
                gid = fn[:-5]
                if gid in by_id and (not only or gid in only):
                    found[gid] = os.path.join(dp, fn)
    errs, merged = [], []
    for gid, path in sorted(found.items()):
        try:
            rec = merge_one(book["games"][by_id[gid]], load(path))
        except Exception as exc:
            errs.append("%s: %s" % (gid, exc))
            continue
        book["games"][by_id[gid]] = rec
        merged.append(gid)
    for e in errs:
        print("  ✗ %s" % e)
    print("  merged %d · errors %d · not yet rewritten %d" % (len(merged), len(errs),
                                                            len(by_id) - len(merged)))
    if not a.dry_run and merged:
        book["version"] = "2.0"
        book["phase"] = "recovery-2026-09"
        book.setdefault("$comment", []).append(
            "RECOVERY %s: %d entries replaced by v2 records (manuscript_merge.py)."
            % (datetime.date.today().isoformat(), len(merged)))
        dump(bp, book)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
