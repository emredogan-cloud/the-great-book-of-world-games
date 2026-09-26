#!/usr/bin/env python3
"""
ÖN MADDE ÜRETECİ — The Great Book of World Games
================================================================================
`EDITORIAL_ARCHITECTURE § 1` ön maddeyi **14 sayfa** diye modeller ve içeriğini
sayar: başlık · künye · içindekiler · giriş denemesi · bu kitap nasıl kullanılır
· yedi ailenin haritası. Faz 5 kapanışı ikisini de **YAZILMAMIŞ** devretti
(§ 17: *"Ön madde ve giriş denemesi"* — hazır DEĞİL sütununda).

Bu betik ön maddeyi ve **yedi aile açılışını** üretir.

⚠ ALT BAŞLIK ÖLÇÜMDEN TÜRETİLİR, YAZILMAZ.
`project_config.json` alt başlık HİPOTEZİ *"100 Games … 45 Cultures"* der.
Kitapta 56 oyun ve 39 kültür vardır. Bir alt başlık pazarlama süsü değil,
kapakta duran bir İDDİADIR; ölçümden ayrıldığı anda kitabın en görünür
yerinde yanlış bir sayı basılır. Bu yüzden burada SAYILIR:

    subtitleMeasured = f(oyun sayısı, kültür sayısı, en eski oyunun yaşı)

Hipotez `subtitleHypothesis` alanında KALIR — silinmez, çünkü neyin
değiştiğini görmek gerekir.

⚠ ISBN UYDURULMAZ. `founder.isbn.strategy = kdp-free` olduğu ve alanlar
`null` durduğu sürece künye sayfası **PENDING — KDP-PROVIDED ISBN** basar.

Çıkış:
    02_MANUSCRIPT/frontmatter.json   (korumalı · tam metin)
    06_REPORTS/frontmatter.json      (public · yapısal özet)

Çıkış kodları:  0 = üretildi   1 = üretilemedi   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def words(*chunks) -> int:
    n = 0
    for c in chunks:
        if isinstance(c, str):
            n += len(re.findall(r"\S+", c))
        elif isinstance(c, list):
            n += words(*c)
        elif isinstance(c, dict):
            n += words(*c.values())
    return n


def oldest_bce(games: list) -> int | None:
    """En eski oyunun tarihi — künyelerden SAYILIR, yazılmaz."""
    best = None
    for g in games:
        for m in re.finditer(r"(\d{3,4})\s*BC", g.get("period", "")):
            v = int(m.group(1))
            best = v if best is None or v > best else best
    return best


def round_hundreds(n: int) -> int:
    return int(round(n / 100.0)) * 100


NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
       "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
       "nineteen"]
TENS = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy",
        80: "eighty", 90: "ninety"}


def words_for(n: int) -> str:
    """Numbers as words, as the book's prose prints them (0–99)."""
    if n < 20:
        return NUM[n]
    t, u = n - n % 10, n % 10
    return TENS[t] + ("" if u == 0 else "-" + NUM[u])


def fill(obj, values):
    """Substitute «key» placeholders everywhere in a text structure."""
    if isinstance(obj, str):
        def rep(m):
            k = m.group(1)
            if k not in values:
                raise KeyError("front matter placeholder «%s» has no measured value" % k)
            return str(values[k])
        return re.sub(r"\u00ab([a-z_]+)\u00bb", rep, obj)
    if isinstance(obj, list):
        return [fill(x, values) for x in obj]
    if isinstance(obj, dict):
        return {k: fill(v, values) for k, v in obj.items()}
    return obj


def codified_source(s) -> bool:
    w = s.get("work", "") if isinstance(s, dict) else str(s)
    return bool(re.search(r"https?://|www\.", w)) or (isinstance(s, dict) and s.get("kind") == "codified")


def build(root: str) -> int:
    cfg = load(os.path.join(root, "project_config.json"))
    mdir = cfg["language"]["commercialManuscriptDir"]
    bpath = os.path.join(root, mdir, "book.json")
    if not os.path.exists(bpath):
        print("  · commercial manuscript not in this checkout — front matter SKIPPED (expected in CI)")
        return 0

    book = load(bpath)
    games = book["games"]
    fam_index = load(os.path.join(root, "01_SOURCE", "family_index.json"))
    families = sorted(fam_index["families"], key=lambda f: f["order"])

    # Contents order: families in their locked order; within a family, by title.
    by_family = {f["id"]: [] for f in families}
    for g in games:
        by_family.setdefault(g["family"], []).append(g)
    for k in by_family:
        by_family[k].sort(key=lambda g: g["title"].lower())
    order = []
    for f in families:
        order.append({"kind": "family-opener", "family": f["id"], "title": f["en"], "numeral": None})
        for g in by_family[f["id"]]:
            order.append({"kind": "game", "gameId": g["gameId"], "title": g["title"],
                          "culture": g["culture"], "family": f["id"]})

    cultures = sorted({g["culture"] for g in games})
    bce = oldest_bce(games)
    pub_year = cfg.get("production", {}).get("publicationYear") or 2026
    # The span is stated as a round figure, to the nearest five hundred years: the
    # earliest boards are dated to within a century or two, not to a year
    # (senet: First Dynasty, c. 3100–2900 BC → "5,000 years").
    age = int(round((bce + pub_year) / 500.0)) * 500 if bce else None
    recon = sum(1 for g in games if g.get("reconstructed"))
    codified = sum(1 for g in games if any(codified_source(s) for s in g.get("sources", [])))
    from backmatter_text import TEMPLATES
    tpl_games = set()
    for t in TEMPLATES:
        tpl_games.update(t.get("games", []))

    subtitle = ("%d Games from %s Years of Human Play — Rules, Boards and Stories from %d "
                "Cultures, Ready to Play Tonight"
                % (len(games), "{:,}".format(age) if age else "Thousands of", len(cultures)))

    values = {"games": len(games), "games_word": words_for(len(games)),
              "games_word_cap": words_for(len(games)).capitalize(),
              "cultures": len(cultures), "cultures_word": words_for(len(cultures)),
              "recon_word": words_for(recon), "recon_word_cap": words_for(recon).capitalize(),
              "codified_word": words_for(codified),
              "tpl_games_word": words_for(len(tpl_games)),
              "chance_word": words_for(len(by_family.get("chance", [])))}

    isbn = cfg["founder"]["isbn"]
    isbn_line = {ed: (isbn.get(ed) or "PENDING — KDP-PROVIDED ISBN")
                 for ed in ("paperback", "hardcover", "largeprint")}

    from frontmatter_text import (INTRO, HOWTO, FAMILIES_MAP, SOURCES_NOTE, TONIGHT,
                                  FAMILY_OPENERS)
    fam_by_id = {f["id"]: f for f in families}
    openers = []
    for o in FAMILY_OPENERS:
        f = fam_by_id[o["family"]]
        n = len(by_family[o["family"]])
        v = dict(values, fam_count_word=words_for(n), fam_count_word_cap=words_for(n).capitalize())
        openers.append(dict(fill(o, v), gameCount=n, targetGames=f["targetGames"],
                            cultures=sorted({g["culture"] for g in by_family[o["family"]]})))

    ai = cfg["founder"]["aiDisclosure"]
    plates_path = os.path.join(root, "01_SOURCE", "plates.json")
    n_ai = n_pd = n_drawn = 0
    if os.path.exists(plates_path):
        for rec in load(plates_path)["plates"].values():
            if rec.get("kind") == "ai-generated":
                n_ai += 1
            elif rec.get("kind") == "drawn":
                n_drawn += 1
            else:
                n_pd += 1
    values.update({"ai_plates_word": words_for(n_ai), "pd_plates_word": words_for(n_pd),
                   "drawn_plates_word": words_for(n_drawn)})

    fm = {
        "$comment": [
            "FRONT MATTER — GENERATED FILE (04_BUILD/build_frontmatter.py).",
            "Text is hand-written in 04_BUILD/frontmatter_text.py; every number",
            "(games · cultures · reconstructions · years · templates) is MEASURED here.",
        ],
        "version": "2.0",
        "generatedAtPhase": "recovery-2026-09",
        "titlePage": {
            "title": cfg["project"]["title"],
            "subtitle": subtitle,
            "author": cfg["founder"]["author"],
            "publisher": cfg["founder"]["publisher"],
            "series": cfg["project"]["series"],
            "volume": cfg["project"]["volume"],
        },
        "imprint": {
            "copyright": "Copyright © %d %s" % (pub_year, cfg["founder"]["author"]),
            "publisher": cfg["founder"]["publisher"],
            "isbn": isbn_line,
            "isbnStrategy": isbn["strategy"],
            "rights": {
                "print": "All rights reserved. No part of this book may be reproduced in any form "
                         "without written permission from the publisher, except brief quotations in "
                         "a review and the full-size boards at the back of this book, which the "
                         "purchaser may photocopy for personal and classroom use.",
                "kindle": "All rights reserved. No part of this book may be reproduced in any form "
                          "without written permission from the publisher, except brief quotations "
                          "in a review."},
            "edition": {"print": "Revised edition, 2026", "kindle": "Revised edition, 2026"},
            "printedBy": "Printed on demand.",
            "aiDisclosure": fill(ai["printed"], values),
        },
        "measured": {
            "games": len(games), "cultures": len(cultures), "cultureLabels": cultures,
            "families": len(families), "reconstructed": recon, "codifiedRulesets": codified,
            "templateGames": sorted(tpl_games),
            "oldestGameBCE": bce, "oldestGameAgeYears": age, "publicationYear": pub_year,
            "subtitleMeasured": subtitle,
            "aiPlates": n_ai, "publicDomainPlates": n_pd,
        },
        "sections": fill([INTRO, HOWTO, FAMILIES_MAP, SOURCES_NOTE, TONIGHT], values),
        "contents": order,
        "familyOpeners": openers,
    }
    fm["measured"]["frontMatterWords"] = words(fm["sections"])
    fm["measured"]["familyOpenerWords"] = words(openers)
    dump(os.path.join(root, mdir, "frontmatter.json"), fm)
    dump(os.path.join(root, "06_REPORTS", "frontmatter.json"), {
        "$comment": "PUBLIC LAYER — structural summary only; no prose (K12).",
        "generatedAtPhase": fm["generatedAtPhase"],
        "measured": fm["measured"],
        "sectionIds": [s["id"] for s in fm["sections"]],
        "familyOpeners": [{"family": o["family"], "numeral": o["numeral"],
                           "gameCount": o["gameCount"], "cultures": len(o["cultures"]),
                           "words": words(o)} for o in openers],
        "contentsLength": len(order),
    })
    print("  ✓ front matter built")
    print("    subtitle (measured): %s" % subtitle)
    reg = cfg["metadata"].get("subtitleRegisteredOnKdp")
    if reg and reg != subtitle:
        print("    ⚠ differs from the subtitle registered on KDP: %s" % reg)
    print("    measured: %d games · %d cultures · %d reconstructed · %d codified · oldest ~%s years"
          % (len(games), len(cultures), recon, codified, age))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    args = ap.parse_args()
    print("=" * 74)
    print("  ÖN MADDE ÜRETECİ")
    print("=" * 74)
    rc = build(os.path.abspath(args.root))
    print("=" * 74)
    return rc


if __name__ == "__main__":
    sys.exit(main())
