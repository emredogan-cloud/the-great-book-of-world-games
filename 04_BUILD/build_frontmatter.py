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


def build(root: str) -> int:
    cfg = load(os.path.join(root, "project_config.json"))
    mdir = cfg["language"]["commercialManuscriptDir"]
    bpath = os.path.join(root, mdir, "book.json")
    if not os.path.exists(bpath):
        print("  · ticari manuscript bu depoda yok — ön madde ATLANDI "
              "(CI'da beklenen)")
        return 0

    book = load(bpath)
    games = book["games"]
    fam_index = load(os.path.join(root, "01_SOURCE", "family_index.json"))
    families = sorted(fam_index["families"], key=lambda f: f["order"])

    # ── içeriğin gerçek sırası ────────────────────────────────────────────
    # Aile sırası kilitlidir (family_index.order); aile içi sıra BAŞLIĞA göre
    # alfabetiktir. Sıra bir tercih değil bir SÖZLEŞMEDİR: indeksler, sayfa
    # göndermeleri ve içindekiler hepsi bu sıradan türetilir.
    by_family = {f["id"]: [] for f in families}
    for g in games:
        by_family.setdefault(g["family"], []).append(g)
    for k in by_family:
        by_family[k].sort(key=lambda g: g["title"].lower())

    order = []
    for f in families:
        order.append({"kind": "family-opener", "family": f["id"],
                      "title": f["en"], "numeral": None})
        for g in by_family[f["id"]]:
            order.append({"kind": "game", "gameId": g["gameId"],
                          "title": g["title"], "culture": g["culture"],
                          "family": f["id"]})

    cultures = sorted({g["culture"] for g in games})
    bce = oldest_bce(games)
    pub_year = cfg.get("production", {}).get("publicationYear") or 2026
    age = round_hundreds(bce + pub_year) if bce else None

    # ── ALT BAŞLIK — ÖLÇÜLÜR ──────────────────────────────────────────────
    subtitle = ("%d Games from %s Years of Human Play — Rules, Boards and "
                "Stories from %d Cultures, Ready to Play Tonight"
                % (len(games), "{:,}".format(age) if age else "Thousands of",
                   len(cultures)))

    isbn = cfg["founder"]["isbn"]
    isbn_line = {}
    for ed in ("paperback", "hardcover"):
        isbn_line[ed] = isbn.get(ed) or "PENDING — KDP-PROVIDED ISBN"

    try:
        from frontmatter_text import (INTRO, HOWTO, FAMILIES_MAP,
                                      SOURCES_NOTE, FAMILY_OPENERS)
    except ImportError as exc:
        print("  ⛔ ön madde metni yok (04_BUILD/frontmatter_text.py): %s" % exc)
        return 1

    fam_by_id = {f["id"]: f for f in families}
    openers = []
    for o in FAMILY_OPENERS:
        f = fam_by_id[o["family"]]
        openers.append(dict(o, gameCount=len(by_family[o["family"]]),
                            targetGames=f["targetGames"],
                            cultures=sorted({g["culture"]
                                             for g in by_family[o["family"]]})))

    fm = {
        "$comment": [
            "ÖN MADDE — ÜRETİLMİŞ DOSYA (04_BUILD/build_frontmatter.py).",
            "Metin 04_BUILD/frontmatter_text.py içindedir ve ELLE yazılır;",
            "sayılar (oyun · kültür · yaş · içindekiler) BURADA ÖLÇÜLÜR.",
            "",
            "Alt başlık ÖLÇÜMDEN türetilir. Hipotez project_config.json",
            "§ project.subtitleHypothesis içinde DURUR ve silinmez.",
        ],
        "version": "1.0",
        "generatedAtPhase": "phase6",
        "titlePage": {
            "title": cfg["project"]["title"],
            "subtitle": subtitle,
            "author": cfg["founder"]["author"],
            "publisher": cfg["founder"]["publisher"],
            "series": cfg["project"]["series"],
            "volume": cfg["project"]["volume"],
        },
        "imprint": {
            "copyright": "Copyright © %d %s" % (pub_year,
                                                cfg["founder"]["author"]),
            "publisher": cfg["founder"]["publisher"],
            "isbn": isbn_line,
            "isbnStrategy": isbn["strategy"],
            "rights": "All rights reserved. No part of this book may be "
                      "reproduced in any form without written permission from "
                      "the publisher, except brief quotations in a review and "
                      "the board templates at the back of this book, which the "
                      "purchaser may photocopy for personal and classroom use.",
            "edition": "First edition",
            "printedBy": "Printed on demand.",
            "authorBio": cfg["founder"].get("authorBio"),
            "$authorBioNote": "null ise KURUCU EYLEMİ bekliyor (A6). "
                              "Yol haritası Faz 6 § 12: authorBio null → KIRMIZI.",
        },
        "measured": {
            "games": len(games),
            "cultures": len(cultures),
            "families": len(families),
            "reconstructed": sum(1 for g in games if g.get("reconstructed")),
            "oldestGameBCE": bce,
            "oldestGameAgeYears": age,
            "publicationYear": pub_year,
            "subtitleMeasured": subtitle,
            "subtitleHypothesis": cfg["project"].get("subtitleHypothesis"),
        },
        "sections": [INTRO, HOWTO, FAMILIES_MAP, SOURCES_NOTE],
        "contents": order,
        "familyOpeners": openers,
    }
    fm["measured"]["frontMatterWords"] = words(fm["sections"])
    fm["measured"]["familyOpenerWords"] = words(openers)

    dump(os.path.join(root, mdir, "frontmatter.json"), fm)
    dump(os.path.join(root, "06_REPORTS", "frontmatter.json"), {
        "$comment": "PUBLIC KATMAN — yapısal özet. Metin YOKTUR (K12).",
        "generatedAtPhase": "phase6",
        "measured": fm["measured"],
        "sectionIds": [s["id"] for s in fm["sections"]],
        "familyOpeners": [{"family": o["family"], "numeral": o["numeral"],
                           "gameCount": o["gameCount"],
                           "targetGames": o["targetGames"],
                           "cultures": len(o["cultures"]),
                           "words": words(o)} for o in openers],
        "contentsLength": len(order),
        "authorBioPresent": bool(cfg["founder"].get("authorBio")),
    })

    print("  ✓ ön madde üretildi")
    print("    alt başlık : %s" % subtitle)
    print("    ölçülen    : %d oyun · %d kültür · %d aile · en eski ~%s yıl"
          % (len(games), len(cultures), len(families), age))
    print("    kelime     : ön madde %d · aile açılışları %d"
          % (fm["measured"]["frontMatterWords"],
             fm["measured"]["familyOpenerWords"]))
    if not cfg["founder"].get("authorBio"):
        print("    ⚠ authorBio BOŞ — KURUCU EYLEMİ (A6). Faz 6 DoD bunu ister.")
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
