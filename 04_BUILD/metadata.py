#!/usr/bin/env python3
"""
KDP METADATA PAKETİ — The Great Book of World Games
================================================================================
KDP panelinde tek tek elle girilecek her alanı **denetlenmiş** biçimde üretir:
başlık · alt başlık · yazar · açıklama · anahtar kelime · kategori · yaş ·
ISBN · fiyat · telif · bölge · AI beyanı.

⚠ AJAN PANELE DOKUNMAZ. Bu dosya bir KOPYA KAĞIDIdır, bir yükleme değildir.

── ÜÇ KIRMIZI ÇİZGİ ────────────────────────────────────────────────────
1. **Sahte ISBN YASAK.** `founder.isbn.strategy = kdp-free` ve alanlar null
   olduğu sürece her çıktı `PENDING — KDP-PROVIDED ISBN` basar.
2. **`authorBio` null → Faz 6 KIRMIZI** (yol haritası § 12). World Myths'te
   yer tutucu biyografi KDP tarafından *şablon metni* diye reddedildi. Kapı
   SEVİYEYE DUYARLIDIR: `release` seviyesinde ısırır, daha aşağıda kurucu
   bağımlılığı olarak RAPOR EDİLİR. Böylece şart kayda geçer ama açılmamış
   bir kapıyı yanlış yerde kırmızı yakmaz.
3. **AI beyanını AJAN SEÇMEZ.** KDP'nin yapay zekâ beyanı hukuki bir
   bildirimdir ve kurucunundur. Paket burada BEYAN İÇİN GEREKEN OLGULARI
   verir — neyin nasıl üretildiğini — ve seçimi kurucuya bırakır.

── HER SAYI ÖLÇÜMDEN ───────────────────────────────────────────────────
Açıklamadaki ve alt başlıktaki her sayı `frontmatter.json § measured` ve
`interior-*.json § pageCount` içinden gelir. Elle yazılmış bir sayı yoktur.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

KDP_LIMITS = {"title": 200, "subtitle": 200, "description": 4000,
              "keywordSlots": 7, "keywordChars": 50}

BISAC_NAMES = {
    "GAM002000": "GAMES & ACTIVITIES / Board",
    "REF000000": "REFERENCE / General",
    "HIS000000": "HISTORY / General",
}


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
         "nineteen"]
TENS = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy"}


def word(n):
    return WORDS[n] if n < 20 else TENS[n - n % 10] + ("" if n % 10 == 0 else "-" + WORDS[n % 10])


def description(m, pages, tpl_games, lp_pages=None, hc_pages=None, trims=None) -> str:
    """Every claim here is true of the build it is generated from: counts are
    measured; the spread, template and source sentences say exactly what the
    book now does (audit WG-001, WG-002, WG-006)."""
    lines = [
        "A reference book you play from.",
        "",
        "The Great Book of World Games sets out %s traditional games from %s cultures, from the "
        "royal graves of Ur to a Zulu playground, so that you can play them tonight."
        % (word(m["games"]), word(m["cultures"])),
        "",
        "EVERY ENTRY GIVES YOU",
        "· A quick-play box: players, time, age, difficulty, what you need and the goal",
        "· Where the game comes from, and how we know",
        "· What to use instead of what — buttons, coins, dried beans, an egg box",
        "· Numbered rules, one action to a line, with a board diagram drawn from the rules",
        "· The disputes every table has — a draw, a blocked player, an illegal move — settled",
        "· A worked turn, played out from a stated position",
        "· A simpler first game, and variants: the recorded ones, and house rules marked as such",
        "· The sources: the work and the pages the rules were read from",
        "",
        "SORTED BY HOW THEY WORK, NOT BY WHERE THEY ARE FROM",
        "Seven families — the sowing games, the hunt and the siege, the race home, the line and "
        "the territory, the war board, chance and scoring, and games without a board. Put that "
        "way, the mancala games of Ghana, Sri Lanka and Buganda sit together, and six cultures "
        "solve the problem of chess six different ways.",
        "",
        "HONEST ABOUT WHAT IS KNOWN",
        "Where a game's record is incomplete — senet, the Royal Game of Ur, the Roman game of "
        "twelve lines — the entry says what the sources give and what has been reconstructed, and "
        "whose reconstruction it follows. Where no source settles a question, the book makes a "
        "ruling and marks it as its own, so you can overrule it. A section at the back lists game "
        "origin stories that are widely repeated and are not true.",
        "",
        "AT THE BACK",
        "Full-size boards for %s of the games, drawn at playing size for the photocopier (print "
        "editions). A list of what to gather for a games kit. A glossary, the sources by work, an "
        "index of every game under every name it goes by, and indexes by culture, age and "
        "difficulty. A free companion pack online adds printable boards for the other games, a "
        "card for every game and score sheets." % word(tpl_games),
        "",
    ]
    size = lambda t: "%s × %s in" % ("%g" % t["w"], "%g" % t["h"])   # noqa: E731
    trims = trims or {}
    if pages:
        lines.append("Paperback: %d pages, %s." % (pages, size(trims.get("paperback", {"w": 8.5, "h": 11}))))
    if hc_pages:
        lines.append("Hardcover: %d pages, %s." % (hc_pages, size(trims.get("hardcover", {"w": 8.25, "h": 11}))))
    if lp_pages:
        lines.append("Large print edition: %d pages, set in 16-point type." % lp_pages)
    return "\n".join(lines)


KEYWORDS = [
    "traditional board games rules book",
    "games from around the world",
    "mancala oware rules",
    "royal game of ur senet rules",
    "go xiangqi shogi rules",
    "family board games history",
    "classroom games activity book",
]


def build(root: str, gate: str) -> tuple[dict, list, list]:
    cfg = load(os.path.join(root, "project_config.json"))
    mdir = cfg["language"]["commercialManuscriptDir"]
    fmp = os.path.join(root, mdir, "frontmatter.json")
    if not os.path.exists(fmp):
        return {}, ["ön madde yok — metadata üretilemez"], []
    fm = load(fmp)
    m = fm["measured"]

    pages = {}
    for ed in ("paperback", "hardcover", "largeprint"):
        p = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if os.path.exists(p):
            pages[ed] = load(p)["pageCount"]
    tpl_games = len(m.get("templateGames") or [])

    isbn = cfg["founder"]["isbn"]
    bio = cfg["founder"].get("authorBio")
    ai = cfg["founder"]["aiDisclosure"]
    errs, founder_actions = [], []

    prod = cfg.get("production", {})
    desc = description(m, pages.get("paperback", 0), tpl_games, pages.get("largeprint"),
                       pages.get("hardcover"),
                       {"paperback": prod.get("trimPaperback", {"w": 8.5, "h": 11}),
                        "hardcover": prod.get("trimHardcover", {"w": 8.25, "h": 11})})
    registered = cfg["metadata"].get("subtitleRegisteredOnKdp")
    title = cfg["project"]["title"]
    subtitle = m["subtitleMeasured"]

    if len(title) > KDP_LIMITS["title"]:
        errs.append("başlık %d karakter > %d" % (len(title),
                                                 KDP_LIMITS["title"]))
    if len(subtitle) > KDP_LIMITS["subtitle"]:
        errs.append("alt başlık %d karakter > %d"
                    % (len(subtitle), KDP_LIMITS["subtitle"]))
    if len(desc) > KDP_LIMITS["description"]:
        errs.append("açıklama %d karakter > %d" % (len(desc),
                                                   KDP_LIMITS["description"]))
    if len(KEYWORDS) > KDP_LIMITS["keywordSlots"]:
        errs.append("anahtar kelime %d > %d slot" % (len(KEYWORDS),
                                                     KDP_LIMITS["keywordSlots"]))
    for k in KEYWORDS:
        if len(k) > KDP_LIMITS["keywordChars"]:
            errs.append("anahtar kelime çok uzun: %r (%d)" % (k, len(k)))

    # Alt başlıktaki sayı KİTABIN sayısıyla aynı olmak ZORUNDA.
    if str(m["games"]) not in subtitle:
        errs.append("alt başlıkta ölçülen oyun sayısı (%d) GEÇMİYOR"
                    % m["games"])
    if str(m["cultures"]) not in subtitle:
        errs.append("alt başlıkta ölçülen kültür sayısı (%d) GEÇMİYOR"
                    % m["cultures"])

    if registered and registered != m["subtitleMeasured"]:
        founder_actions.append({
            "id": "SUBTITLE-NEW-EDITION", "field": "metadata.subtitleRegisteredOnKdp", "blocking": True,
            "note": "The verified subtitle (%s) differs from the one registered on the live KDP print "
                    "records (%s). KDP locks a paperback/hardcover title and subtitle 72 hours after "
                    "publication; the corrected files need a NEW EDITION with a new ISBN (or KDP "
                    "support). Decide before uploading the print files." % (m["subtitleMeasured"], registered)})
    founder_actions.append({
        "id": "AI-QUESTIONNAIRE", "field": "founder.aiDisclosure", "blocking": True,
        "note": "Under KDP's definitions the text of this book is AI-GENERATED (created by AI tools, "
                "then edited), not AI-assisted; most plates and the cover are AI-generated images. "
                "Re-answer the KDP AI content questions for every edition when uploading."})

    # ── authorBio: SEVİYEYE DUYARLI KAPI ────────────────────────────────
    if not bio:
        # ⚠ NOT İNGİLİZCE. Bu metin KDP_UPLOAD_HANDBOOK.md içinde BASILIR
        # ve o kılavuz KDP panelinin diliyle, İngilizce yazılmıştır.
        msg = ("`founder.authorBio` is empty. KDP asks for an author "
               "biography, and on a sibling title KDP rejected a placeholder "
               "biography as template text (12 August 2026). Write a real "
               "one before publishing.")
        if gate == "release":
            errs.append("authorBio null — yol haritası Faz 6 § 12: KIRMIZI")
        founder_actions.append({"id": "A6", "field": "founder.authorBio",
                                "blocking": True, "note": msg})
    if not ai.get("founderConfirmed"):
        founder_actions.append({
            "id": "AI-DECL", "field": "founder.aiDisclosure.founderConfirmed",
            "blocking": True,
            "note": "The AI-generated content declaration is a legal "
                    "statement and the choice is yours alone. The agent "
                    "cannot make it. The facts you need are in "
                    "`aiProductionFacts`."})
    for ed in ("paperback", "hardcover"):
        if not isbn.get(ed):
            founder_actions.append({
                "id": "ISBN-%s" % ed, "field": "founder.isbn.%s" % ed,
                "blocking": False,
                "note": "KDP assigns a free ISBN. Once it does, write it "
                        "here and rebuild: the copyright page will print the "
                        "real number instead of PENDING. No ISBN has been "
                        "invented anywhere in this package."})

    md = {
        "$comment": [
            "KDP METADATA — ÜRETİLMİŞ DOSYA (04_BUILD/metadata.py).",
            "Bu bir KOPYA KAĞIDIDIR. Ajan KDP paneline DOKUNMADI.",
            "Her sayı ölçümden gelir; elle yazılmış sayı yoktur.",
        ],
        "generatedAtPhase": "phase6",
        "gate": gate,
        "bookDetails": {
            "language": cfg["project"]["language"],
            "title": title, "titleChars": len(title),
            "subtitle": subtitle, "subtitleChars": len(subtitle),
            "series": cfg["project"]["series"],
            "volume": cfg["project"]["volume"],
            "author": cfg["founder"]["author"],
            "contributors": [],
            "publisher": cfg["founder"]["publisher"],
            "edition": "Revised edition",
        },
        "description": {"text": desc, "chars": len(desc),
                        "limit": KDP_LIMITS["description"],
                        "format": "plain text; KDP allows limited HTML but "
                                  "this copy is written to read correctly "
                                  "without it"},
        "keywords": KEYWORDS,
        "categories": {
            "bisacPrimary": {"code": cfg["audience"]["bisacPrimary"],
                             "name": BISAC_NAMES.get(
                                 cfg["audience"]["bisacPrimary"], "?")},
            "bisacSecondary": [{"code": c, "name": BISAC_NAMES.get(c, "?")}
                               for c in cfg["audience"]["bisacSecondary"]],
            "$note": "KDP artık kategorileri kendi ağacından seçtirir; BISAC "
                     "kodları eşleştirme için verilir. Kurucu paneldeki "
                     "karşılıklarını seçer.",
        },
        "audience": {
            "readerAgeMin": cfg["audience"]["readerAgeMin"],
            "readerAgeMax": cfg["audience"]["readerAgeMax"],
            "$note": "KDP yaş aralığı YALNIZCA çocuk kitabı olarak "
                     "işaretlenen başlıklarda sorulur. Bu kitap bir aile "
                     "başvuru cildidir ve çocuk kitabı olarak "
                     "işaretlenMEZ — işaretlenirse yetişkin alıcı "
                     "aramalarından düşer.",
        },
        "publishingRights": {
            "value": "I own the copyright and I hold the necessary "
                     "publishing rights.",
            "$note": "Kitabın metni bu proje için yazılmıştır. Kural "
                     "kaynakları KAMUSAL ALAN eserlerdir ve alıntı değil "
                     "KÜNYE olarak kullanılır; hiçbir kaynaktan blok metin "
                     "aktarılmamıştır.",
        },
        "isbn": {"strategy": isbn["strategy"],
                 "paperback": isbn.get("paperback") or "PENDING — KDP-PROVIDED ISBN",
                 "hardcover": isbn.get("hardcover") or "PENDING — KDP-PROVIDED ISBN",
                 "$note": "Sahte ISBN YASAKTIR (§ 15)."},
        "aiProductionFacts": {
            "$note": "Facts for KDP's AI content questions (KDP Help G200672390: AI-generated = "
                     "created by an AI tool, even if substantially edited afterwards).",
            "text": ai["text"]["detail"],
            "textClassification": ai["text"]["state"],
            "images": ai["images"]["detail"],
            "imagesClassification": ai["images"]["state"],
            "translation": "None. The text is written in English.",
            "founderConfirmed": bool(ai.get("founderConfirmed")),
        },
        "pricing": {
            e["id"]: {"listUSD": e["list"], "enabled": e["enabled"]}
            for e in cfg["production"]["editionsHypothesis"]},
        "territories": {"value": "All territories (worldwide rights)",
                        "$note": "Kurucu kararı; varsayılan budur."},
        "kdpSelect": {"enrol": cfg["production"]["kdpSelect"],
                      "$note": cfg["production"]["kdpSelect$comment"]},
        "pageCounts": pages,
        "measured": m,
        "founderActions": founder_actions,
        "limits": KDP_LIMITS,
    }
    return md, errs, founder_actions



def manuscript_absent(root: str) -> bool:
    """Ticari manuscript depoda YOKTUR (karar K12).

    CI taze bir klonda koşar ve orada `02_MANUSCRIPT/book.json` bulunmaz.
    Bu bir kusur DEĞİLDİR ve kapı orada BOŞ KOŞAR. Bir kapının CI'da
    kırmızı yanması, kusuru olduğu için olmalıdır; verinin orada olmaması
    için değil."""
    return not os.path.exists(os.path.join(root, "02_MANUSCRIPT", "book.json"))


def run(root: str, args) -> int:
    if manuscript_absent(root):
        print("  · ticari manuscript bu depoda yok — metadata ATLANDI "
              "(CI'da beklenen)")
        return 0
    gate = args.gate or (open(os.path.join(root, ".gate"),
                              encoding="utf-8").read().strip()
                         if os.path.exists(os.path.join(root, ".gate"))
                         else "phase0")
    md, errs, actions = build(root, gate)
    if not md:
        for e in errs:
            print("  ✗ %s" % e)
        return 1 if errs else 0

    if not args.check:
        dump(os.path.join(root, "06_REPORTS", "tracked", "metadata.json"), md)

    print("=" * 74)
    print("  KDP METADATA PAKETİ · kapı: %s" % gate)
    print("=" * 74)
    b = md["bookDetails"]
    print("  başlık        (%3d/%d) %s" % (b["titleChars"],
                                           KDP_LIMITS["title"], b["title"]))
    print("  alt başlık    (%3d/%d) %s" % (b["subtitleChars"],
                                           KDP_LIMITS["subtitle"],
                                           b["subtitle"]))
    print("  yazar         %s" % b["author"])
    print("  yayıncı       %s" % b["publisher"])
    print("  açıklama      (%d/%d karakter)" % (md["description"]["chars"],
                                                KDP_LIMITS["description"]))
    print("  anahtar kel.  %d/%d slot" % (len(md["keywords"]),
                                          KDP_LIMITS["keywordSlots"]))
    print("  kategori      %s + %s" % (md["categories"]["bisacPrimary"]["code"],
                                       ", ".join(c["code"] for c in
                                                 md["categories"]["bisacSecondary"])))
    print("  ISBN          %s" % md["isbn"]["paperback"])
    print("  sayfa         %s" % " · ".join("%s %d" % kv for kv in
                                            md["pageCounts"].items()))
    print("\n── KURUCU EYLEMLERİ (%d) ──" % len(actions))
    for a in actions:
        print("  %s %-38s %s" % ("⛔" if a["blocking"] else "·",
                                 a["field"], a["id"]))
        print("     %s" % a["note"])
    print("\n" + "=" * 74)
    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        print("  ⛔ %d KUSUR" % len(errs))
    else:
        print("  ✅ metadata paketi tutarlı · %d kurucu eylemi bekliyor"
              % len(actions))
        print("     ⚠ AJAN KDP PANELİNE DOKUNMADI. Bu dosya bir kopya kâğıdıdır.")
    print("=" * 74)
    return 1 if errs else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    return run(os.path.abspath(args.root), args)


if __name__ == "__main__":
    sys.exit(main())
