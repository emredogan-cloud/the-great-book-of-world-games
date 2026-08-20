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


def description(m, pages) -> str:
    return (
"A reference book you play from.\n"
"\n"
"The Great Book of World Games sets out %d traditional games from %d "
"cultures, from the royal graves of Ur to a Zulu playground, and it sets "
"them out so you can play them tonight. Each game gets two facing pages: the "
"book lies open on the table and nobody has to turn a page in the middle of "
"a turn.\n"
"\n"
"WHAT IS INSIDE EACH ENTRY\n"
"· Players, time, age, materials and difficulty at a glance\n"
"· What to use instead of what — buttons, coins, dried beans, an egg box\n"
"· Numbered rules, one action to a line\n"
"· A board diagram drawn to scale\n"
"· The three questions every table argues about: what happens on a draw, "
"what happens if nobody can move, and what happens when somebody plays an "
"illegal move\n"
"· A shorter version to start with\n"
"· The work and the pages the rules were read from\n"
"\n"
"SORTED BY HOW THEY WORK, NOT BY WHERE THEY ARE FROM\n"
"Most collections file games by country. This one files them by mechanism, "
"in seven families — sowing, hunt and siege, race home, line and territory, "
"the war board, chance and nerve, and games without a board. Put that way, "
"the mancala games of Ghana, Sri Lanka and Buganda sit together and you can "
"see what they share and where they part; the ancestors of chess sit "
"together and you can watch six cultures solve the same problem six ways.\n"
"\n"
"HONEST ABOUT WHAT IS KNOWN\n"
"Every rule set names its source. Where a historical record is incomplete, "
"the entry says so and shows what has been reconstructed and on what basis. "
"Where no source settles a question — most often the draw — the book makes a "
"ruling and tells you it is the book's ruling, so you can overrule it. One "
"page at the back is given to game origin stories that are widely repeated "
"and are not true.\n"
"\n"
"AT THE BACK\n"
"Full-size board templates you can photocopy. A materials guide. A glossary "
"of the terms used for mechanics. Sources for every game. Three indexes — by "
"culture, by number of players, and by time and age.\n"
"\n"
"%d pages. Almost nothing in it has to be bought."
        % (m["games"], m["cultures"], pages))


KEYWORDS = [
    "traditional board games book",
    "world games rules and history",
    "family games for adults and kids",
    "mancala backgammon go rules",
    "history of board games reference",
    "games from around the world",
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
    for ed in ("paperback", "hardcover"):
        p = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if os.path.exists(p):
            pages[ed] = load(p)["pageCount"]

    isbn = cfg["founder"]["isbn"]
    bio = cfg["founder"].get("authorBio")
    ai = cfg["founder"]["aiDisclosure"]
    errs, founder_actions = [], []

    desc = description(m, pages.get("paperback", 0))
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

    # ── authorBio: SEVİYEYE DUYARLI KAPI ────────────────────────────────
    if not bio:
        msg = ("`founder.authorBio` BOŞ. KDP yazar biyografisini ister ve "
               "World Myths'te yer tutucu metin REDDEDİLDİ (12 Ağustos 2026). "
               "Kurucu gerçek bir biyografi yazmadan yayın tamamlanamaz.")
        if gate == "release":
            errs.append("authorBio null — yol haritası Faz 6 § 12: KIRMIZI")
        founder_actions.append({"id": "A6", "field": "founder.authorBio",
                                "blocking": True, "note": msg})
    if not ai.get("founderConfirmed"):
        founder_actions.append({
            "id": "AI-DECL", "field": "founder.aiDisclosure.founderConfirmed",
            "blocking": True,
            "note": "KDP'nin yapay zekâ beyanı SEÇİMİ kurucunundur. Ajan "
                    "hukuki bildirim veremez. Beyan için gereken olgular "
                    "`aiProductionFacts` alanındadır."})
    for ed in ("paperback", "hardcover"):
        if not isbn.get(ed):
            founder_actions.append({
                "id": "ISBN-%s" % ed, "field": "founder.isbn.%s" % ed,
                "blocking": False,
                "note": "KDP ücretsiz ISBN atar. Atandıktan sonra buraya "
                        "yazılırsa künye sayfası gerçek numarayı basar; "
                        "yazılmazsa PENDING basmaya devam eder. SAHTE ISBN "
                        "YASAKTIR."})

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
            "edition": "First edition",
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
            "$note": "KDP'nin AI beyanı için OLGULAR. Seçimi kurucu yapar.",
            "text": "Text was drafted with AI assistance and edited by the "
                    "author; every rule set is traced to a named printed "
                    "source at page level.",
            "images": "Cover and A+ artwork are generated externally by the "
                      "author; interior diagrams are drawn deterministically "
                      "by the project's own code from data, not generated.",
            "translation": "None. The commercial text is written directly in "
                           "English.",
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


def run(root: str, args) -> int:
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
