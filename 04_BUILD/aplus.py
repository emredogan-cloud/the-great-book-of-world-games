#!/usr/bin/env python3
"""
A+ İÇERİK PAKETİ — The Great Book of World Games
================================================================================
Altı A+ modülünün **MODÜL → GÖRSEL → BAŞLIK → GÖVDE** haritasını üretir ve
metnin her cümlesini bir **iddia taramasından** geçirir.

── İDDİA TARAMASI ──────────────────────────────────────────────────────
Kurucu § 17 dört iddiayı açıkça yasaklar: *bestseller · award winner ·
child-tested · guaranteed educational outcome*. Bunlar yasak çünkü hiçbiri
için bu projede **kanıt yoktur** — ve A+ içeriği Amazon'un moderasyonundan
geçer. Reddedilen bir A+ gönderimi yalnızca zaman kaybettirmez; hesabın
işaretlenmesine yol açabilir.

Tarama daha geniştir: sayı içeren her cümle, projenin ÖLÇTÜĞÜ sayılarla
karşılaştırılır. "56 games" geçer; "100 games" GEÇMEZ. Kitabın kendi
içindeki sayıyla pazarlama metnindeki sayı ayrışırsa, ayrışmayı okur bulur.

── GÖRSEL KAPISI ───────────────────────────────────────────────────────
Görseller kurucu tarafından üretilir. Bu betik metni ve haritayı ÜRETİR;
görseller gelmeden paketi TAM ilan ETMEZ.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
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

# Amazon A+ alan sınırları (kaydedilen değerler; kurucu panelde doğrular).
LIMIT_TITLE = 160
LIMIT_BODY = 1000

FORBIDDEN = [
    (r"\bbest[- ]?sell(er|ing)\b", "bestseller iddiası — kanıt yok"),
    (r"\baward[- ]winning\b|\bprize[- ]winning\b|\bwinner of\b",
     "ödül iddiası — kanıt yok"),
    (r"\bchild[- ]tested\b|\bkid[- ]tested\b|\bplaytested\b|\btested by\b",
     "test iddiası — DIŞ OYNANABİLİRLİK TESTİ 0 OTURUM"),
    (r"\bguarantee\w*\b|\bproven to\b|\bwill improve\b|\bboosts?\b|"
     r"\bdevelops? (their|your) \w+ skills\b",
     "garanti edilmiş eğitsel sonuç iddiası — kanıt yok"),
    (r"\b#\s?1\b|\bnumber one\b|\bworld'?s (best|leading)\b",
     "sıralama iddiası — kanıt yok"),
    (r"\bcomplete (guide|collection) to (all|every)\b",
     "bütünlük iddiası — kitap 56/100 kapsamda"),
    (r"\bevery (game|culture) (in the world|ever)\b", "bütünlük iddiası"),
]


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def modules(m):
    """MODÜL → GÖRSEL → BAŞLIK → GÖVDE. Sayılar ÖLÇÜMDEN gelir."""
    g, c, f = m["games"], m["cultures"], m["families"]
    return [
        {"id": "APLUS-01", "n": "01", "name": "HERO / WORLD OF GAMES",
         "moduleType": "Standard Image Header with Text",
         "image": "aplus-01-hero-world-of-games.png",
         "imagePx": [970, 600],
         "title": "%d games. %d cultures. One table." % (g, c),
         "body":
             "This is a reference book you play from, not one you only read. "
             "Every game is set out across two facing pages so the book lies "
             "open on the table and nobody turns a page mid-turn. Every rule "
             "set names the work and the pages it was read from, and where a "
             "record is incomplete the book says so on the page instead of "
             "filling the gap quietly."},

        {"id": "APLUS-02", "n": "02", "name": "CULTURAL DIVERSITY",
         "moduleType": "Standard Image & Text Overlay",
         "image": "aplus-02-cultural-diversity.png",
         "imagePx": [970, 600],
         "title": "Sorted by how they work, not by where they are from",
         "body":
             "Most collections file games by country, which teaches geography "
             "and hides the interesting part. This one files them by "
             "mechanism, so the sowing games of Ghana, Sri Lanka and Buganda "
             "sit together and you can see what they share and where they "
             "part. %d cultures are represented, from Sumer to the Sámi, and "
             "each entry names the culture precisely rather than a continent."
             % c},

        {"id": "APLUS-03", "n": "03", "name": "HOW THE BOOK WORKS",
         "moduleType": "Standard Single Image & Sidebar",
         "image": "aplus-03-how-the-book-works.png",
         "imagePx": [300, 400],
         "title": "Everything you need for one game, on one opening",
         "body":
             "Players, time, age, materials and difficulty at the top. What "
             "to use instead of what — buttons, coins, dried beans, an egg "
             "box. Numbered rules, one action to a line. A board diagram "
             "drawn to scale. Then three questions every table actually "
             "argues about: what happens on a draw, what happens if nobody "
             "can move, and what happens when somebody plays an illegal "
             "move. Almost nothing in this book has to be bought."},

        {"id": "APLUS-04", "n": "04", "name": "TYPES OF GAMES",
         "moduleType": "Standard Four Image & Text",
         "image": "aplus-04-types-of-games.png",
         "imagePx": [220, 220],
         "imageSet": ["aplus-04-types-of-games-a.png",
                      "aplus-04-types-of-games-b.png",
                      "aplus-04-types-of-games-c.png",
                      "aplus-04-types-of-games-d.png"],
         "title": "%d families of play" % f,
         "body":
             "Sowing · Hunt and siege · Race home · Line and territory · War "
             "board · Chance and nerve · Games without a board. Each family "
             "opens with a portrait of the idea behind it, and each has a "
             "written rule for what belongs in it and what does not. The "
             "boundaries are argued, not assumed."},

        {"id": "APLUS-05", "n": "05", "name": "PLAY / FAMILY / DISCOVERY",
         "moduleType": "Standard Image & Light Text Overlay",
         "image": "aplus-05-play-family-discovery.png",
         "imagePx": [970, 300],
         "title": "For a table with an adult and a child at it",
         "body":
             "Ages are given per game and they mean something: the age at "
             "which a player can hold the whole game in their head. Every "
             "entry ends with a shorter version to start with — a smaller "
             "board, fewer pieces — which is the fastest way to teach a game "
             "to somebody who has not read the page."},

        {"id": "APLUS-06", "n": "06", "name": "THE COMPLETE COLLECTION",
         "moduleType": "Standard Image Header with Text",
         "image": "aplus-06-complete-collection.png",
         "imagePx": [970, 600],
         "title": "Board templates, a glossary and three indexes",
         "body":
             "The back of the book is the part that gets used. Full-size "
             "board templates you can photocopy — the page size was chosen "
             "for exactly that. A materials guide. A glossary of the terms "
             "the book uses for mechanics. Sources for every game. Three "
             "indexes, by culture, by number of players, and by time and "
             "age. And one page listing the game origin stories that are "
             "widely repeated and are not true."},
    ]


def claim_scan(mods, measured) -> list:
    """Yasak iddia + ÖLÇÜLMEMİŞ SAYI taraması."""
    hits = []
    allowed_numbers = {str(measured["games"]), str(measured["cultures"]),
                       str(measured["families"]),
                       "{:,}".format(measured.get("oldestGameAgeYears") or 0),
                       str(measured.get("oldestGameAgeYears") or 0),
                       "two", "three", "one"}
    for m in mods:
        for field in ("title", "body"):
            txt = m[field]
            for pat, why in FORBIDDEN:
                for mt in re.finditer(pat, txt, re.I):
                    hits.append({"module": m["id"], "field": field,
                                 "match": mt.group(0), "reason": why})
            for num in re.findall(r"\b\d[\d,]*\b", txt):
                if num not in allowed_numbers:
                    hits.append({"module": m["id"], "field": field,
                                 "match": num,
                                 "reason": "ÖLÇÜLMEMİŞ SAYI — projenin "
                                           "ölçtüğü değerler: %s"
                                           % ", ".join(sorted(allowed_numbers
                                                              - {"one", "two",
                                                                 "three"}))})
    return hits


def run(root: str, args) -> int:
    mdir = "02_MANUSCRIPT"
    fp = os.path.join(root, mdir, "frontmatter.json")
    if not os.path.exists(fp):
        print("  · ön madde yok — A+ paketi ATLANDI")
        return 0
    fm = load(fp)
    measured = fm["measured"]
    mods = modules(measured)
    hits = claim_scan(mods, measured)

    raw = os.path.join(root, "07_ASSETS", "raw", "aplus")
    have = set(os.listdir(raw)) if os.path.isdir(raw) else set()
    for m in mods:
        wanted = m.get("imageSet") or [m["image"]]
        m["imagesPresent"] = [w for w in wanted if w in have]
        m["imagesMissing"] = [w for w in wanted if w not in have]
        m["titleChars"] = len(m["title"])
        m["bodyChars"] = len(m["body"])

    over = [(m["id"], m["titleChars"], m["bodyChars"]) for m in mods
            if m["titleChars"] > LIMIT_TITLE or m["bodyChars"] > LIMIT_BODY]
    missing = sum(len(m["imagesMissing"]) for m in mods)

    payload = {
        "$comment": [
            "A+ İÇERİK PAKETİ — ÜRETİLMİŞ DOSYA (04_BUILD/aplus.py).",
            "MODÜL → GÖRSEL → BAŞLIK → GÖVDE.",
            "Metindeki her sayı projenin ÖLÇTÜĞÜ değerlerden gelir.",
            "Görseller kurucu tarafından üretilir; yokken paket TAM DEĞİLDİR.",
        ],
        "generatedAtPhase": "phase6",
        "measured": measured,
        "limits": {"titleChars": LIMIT_TITLE, "bodyChars": LIMIT_BODY,
                   "$note": "Amazon alan sınırları kaydedilen değerlerdir; "
                            "kurucu A+ editöründe doğrular."},
        "modules": mods,
        "claimScan": {"forbiddenPatterns": len(FORBIDDEN), "hits": hits},
        "imagesMissing": missing,
        "status": ("READY" if not missing and not hits and not over
                   else "BLOCKED — kurucu görselleri bekleniyor"
                   if missing and not hits and not over else "DEFECT"),
    }
    dump(os.path.join(root, "03_APLUS", "aplus_content.json"), payload)
    dump(os.path.join(root, "06_REPORTS", "aplus.json"),
         {k: v for k, v in payload.items() if k != "modules"} |
         {"moduleSummary": [{"id": m["id"], "type": m["moduleType"],
                             "titleChars": m["titleChars"],
                             "bodyChars": m["bodyChars"],
                             "imagesMissing": m["imagesMissing"]}
                            for m in mods]})

    print("=" * 74)
    print("  A+ İÇERİK PAKETİ")
    print("=" * 74)
    for m in mods:
        print("\n  %s · %s" % (m["id"], m["name"]))
        print("     modül   %s · %s px" % (m["moduleType"],
                                           "×".join(map(str, m["imagePx"]))))
        print("     görsel  %s" % (", ".join(m["imagesMissing"]) + "  ⛔ YOK"
                                   if m["imagesMissing"] else "hazır ✓"))
        print("     başlık  (%d/%d) %s" % (m["titleChars"], LIMIT_TITLE,
                                           m["title"]))
        print("     gövde   (%d/%d)" % (m["bodyChars"], LIMIT_BODY))
    print("\n── İDDİA TARAMASI ── %d kalıp" % len(FORBIDDEN))
    if hits:
        for h in hits:
            print("  ✗ %s.%s '%s' — %s" % (h["module"], h["field"],
                                           h["match"], h["reason"]))
    else:
        print("  ✓ yasak iddia YOK · her sayı ölçümle eşleşiyor "
              "(%d oyun · %d kültür · %d aile)"
              % (measured["games"], measured["cultures"],
                 measured["families"]))
    for mid, t, b in over:
        print("  ✗ %s alan sınırını aşıyor (başlık %d · gövde %d)"
              % (mid, t, b))
    print("\n" + "=" * 74)
    if missing:
        print("  ⛔ VARLIK KAPISI: %d A+ görseli eksik." % missing)
        print("     Metin ve harita HAZIR; paket TAM DEĞİL ve tam olduğu")
        print("     İDDİA EDİLMİYOR. İstemler: 07_ASSETS/IMAGE_PROMPT_LIBRARY.html")
    print("  durum: %s" % payload["status"])
    print("=" * 74)
    return 1 if (hits or over) else 0


def run_check(root: str) -> int:
    p = os.path.join(root, "03_APLUS", "aplus_content.json")
    if not os.path.exists(p):
        print("  · A+ paketi üretilmemiş — ATLANDI")
        return 0
    d = load(p)
    fm = os.path.join(root, "02_MANUSCRIPT", "frontmatter.json")
    errs = []
    if d["claimScan"]["hits"]:
        errs.append("iddia taraması %d isabet" % len(d["claimScan"]["hits"]))
    if os.path.exists(fm):
        m = load(fm)["measured"]
        if m["games"] != d["measured"]["games"] or \
           m["cultures"] != d["measured"]["cultures"]:
            errs.append("A+ metni BAYAT — kitap %d oyun/%d kültür, A+ %d/%d"
                        % (m["games"], m["cultures"],
                           d["measured"]["games"], d["measured"]["cultures"]))
    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        return 1
    print("  ✓ A+ paketi güncel · 6 modül · %s" % d["status"])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    return run_check(root) if args.check else run(root, args)


if __name__ == "__main__":
    sys.exit(main())
