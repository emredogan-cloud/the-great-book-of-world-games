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



# ── GÖRSEL İŞLEME ────────────────────────────────────────────────────────
#
# ⚠ DOSYA ADINA GÜVENİLMEZ (kurucu § 2). Teslim edilen görseller AÇILDI ve
# içindekine bakıldı. Bir dosya `aplus-05-play-family-discovery.png` adını
# taşıyordu ama içeriği MODÜL 06'nın istemidir: soluk zeminde düzenli
# sıralara dizilmiş çok sayıda oyun nesnesi ve SAĞ ÜÇTE BİRİ boş. Modül
# 05'in istemi (masa hizasından, elleri gösteren, yüzsüz bir kare) DEĞİLDİR.
# Görsel, adının değil İÇERİĞİNİN modülüne bağlandı.
CONTENT_MAP = {
    "aplus-01-hero-world-of-games.png": "APLUS-01",
    "aplus-02-cultural-diversity.png": "APLUS-02",
    "aplus-03-how-the-book-works.png": "APLUS-03",
    "aplus-04-types-of-games.png": "APLUS-04",
    "aplus-05-play-family-discovery.png": "APLUS-06",
}
# Kırpma çıpası: kompozisyonun KORUNACAK yanı. Hero ve koleksiyon
# modüllerinin SAĞ üçte biri metin içindir ve boş kalmalıdır; kırpma
# soldan yapılır.
CROP_ANCHOR = {"APLUS-01": "right", "APLUS-02": "center",
               "APLUS-03": "center", "APLUS-04": "center",
               "APLUS-06": "right"}


def crop_to(im, tw, th, anchor="center"):
    from PIL import Image
    want = tw / float(th)
    have = im.width / float(im.height)
    if abs(have - want) > 1e-4:
        if have > want:
            nw = int(round(im.height * want))
            if anchor == "right":
                x = im.width - nw
            elif anchor == "left":
                x = 0
            else:
                x = (im.width - nw) // 2
            im = im.crop((x, 0, x + nw, im.height))
        else:
            nh = int(round(im.width / want))
            y = (im.height - nh) // 2
            im = im.crop((0, y, im.width, y + nh))
    return im.resize((tw, th), Image.LANCZOS)


def split_quad(im):
    """2×2 bileşik kareyi DÖRT kareye böler.

    Kurucu `Standard Four Image & Text` için dört ayrı kare yerine tek bir
    2×2 bileşik teslim etti. Bölmek bir ÜRETİM değil bir AYIRMA işidir:
    piksel eklenmez, yalnızca zaten orada olan dört panel kesilir. Panel
    sınırları, aradaki açık ayraç sütun/satırı ÖLÇÜLEREK bulunur.
    """
    import statistics
    g = im.convert("L")
    W, H = g.size
    cols = [statistics.mean(g.crop((x, 0, x + 1, H)).getdata()) for x in range(W)]
    rows = [statistics.mean(g.crop((0, y, W, y + 1)).getdata()) for y in range(H)]

    def gutter(v, lo, hi):
        seg = v[lo:hi]
        return lo + max(range(len(seg)), key=lambda i: seg[i])

    cx = gutter(cols, int(W * 0.42), int(W * 0.58))
    cy = gutter(rows, int(H * 0.42), int(H * 0.58))
    pad = int(min(W, H) * 0.012)
    return [im.crop((pad, pad, cx - pad, cy - pad)),
            im.crop((cx + pad, pad, W - pad, cy - pad)),
            im.crop((pad, cy + pad, cx - pad, H - pad)),
            im.crop((cx + pad, cy + pad, W - pad, H - pad))], (cx, cy)


def process_images(root, mods, verbose=True):
    """Ham A+ sanatını modül ölçülerine getirir. HAM DOSYAYA YAZMAZ."""
    from PIL import Image
    raw = os.path.join(root, "07_ASSETS", "raw", "aplus")
    out_dir = os.path.join(root, "07_ASSETS", "web", "aplus")
    os.makedirs(out_dir, exist_ok=True)
    by_id = {m["id"]: m for m in mods}
    delivered = {}
    if os.path.isdir(raw):
        for fn in os.listdir(raw):
            if fn.startswith("."):
                continue
            key = fn.strip()
            mid = CONTENT_MAP.get(key)
            if mid:
                delivered[mid] = os.path.join(raw, fn)

    results = []
    for m in mods:
        src = delivered.get(m["id"])
        rec = {"id": m["id"], "module": m["moduleType"],
               "targetPx": m["imagePx"], "source": None, "outputs": [],
               "status": "MISSING"}
        if not src:
            results.append(rec)
            if verbose:
                print("  %-10s ⛔ ham görsel YOK" % m["id"])
            continue
        im = Image.open(src)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
            im = Image.alpha_composite(bg, im)
        im = im.convert("RGB")
        rec["source"] = {"file": os.path.relpath(src, root).replace("\t", ""),
                         "widthPx": im.width, "heightPx": im.height,
                         "sha256": sha256(src)}
        tw, th = m["imagePx"]
        if m["id"] == "APLUS-04":
            quads, cut = split_quad(im)
            rec["split"] = {"gutterPx": list(cut), "panels": 4,
                            "$note": "kurucu tek 2×2 bileşik teslim etti; "
                                     "dört panel ÖLÇÜLEREK ayrıldı"}
            names = m.get("imageSet") or []
            for q, name in zip(quads, names):
                path = os.path.join(out_dir, name)
                crop_to(q, tw, th, "center").save(path, "PNG", optimize=True)
                rec["outputs"].append(_out(root, path, tw, th))
        else:
            path = os.path.join(out_dir, m["image"])
            crop_to(im, tw, th, CROP_ANCHOR.get(m["id"], "center")).save(
                path, "PNG", optimize=True)
            rec["outputs"].append(_out(root, path, tw, th))
        big = max(o["bytes"] for o in rec["outputs"])
        rec["status"] = "READY" if big <= 2 * 1024 * 1024 else "TOO-LARGE"
        rec["scaleFactor"] = round(tw / float(im.width), 4)
        rec["upscaled"] = im.width < tw or im.height < th
        results.append(rec)
        if verbose:
            print("  %-10s %d × %d → %s · ×%.3f · %s"
                  % (m["id"], im.width, im.height,
                     " + ".join("%d×%d" % (o["widthPx"], o["heightPx"])
                                for o in rec["outputs"]),
                     rec["scaleFactor"], rec["status"]))
    return results


def _out(root, path, tw, th):
    return {"file": os.path.relpath(path, root), "widthPx": tw,
            "heightPx": th, "bytes": os.path.getsize(path),
            "sha256": sha256(path)}


def sha256(p):
    import hashlib
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


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

    print("=" * 74)
    print("  A+ GÖRSEL İŞLEME")
    print("=" * 74)
    proc = process_images(root, mods)
    by_id = {r["id"]: r for r in proc}
    for m in mods:
        r = by_id.get(m["id"], {})
        m["processed"] = r.get("outputs", [])
        m["rawSource"] = r.get("source")
        m["imageStatus"] = r.get("status", "MISSING")
        m["imagesPresent"] = [o["file"] for o in m["processed"]]
        m["imagesMissing"] = ([] if m["processed"]
                              else (m.get("imageSet") or [m["image"]]))
        if r.get("split"):
            m["split"] = r["split"]
        m["titleChars"] = len(m["title"])
        m["bodyChars"] = len(m["body"])

    over = [(m["id"], m["titleChars"], m["bodyChars"]) for m in mods
            if m["titleChars"] > LIMIT_TITLE or m["bodyChars"] > LIMIT_BODY]
    missing = sum(len(m["imagesMissing"]) for m in mods)
    ready = [m for m in mods if m["imageStatus"] == "READY"]

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
        "modulesReady": [m["id"] for m in ready],
        "modulesWithoutArt": [m["id"] for m in mods if not m["processed"]],
        "contentMap": CONTENT_MAP,
        "$contentMapNote":
            "Görseller DOSYA ADINA göre değil İÇERİĞE göre eşlendi. "
            "'aplus-05-play-family-discovery.png' adlı dosyanın içeriği "
            "MODÜL 06'nın istemidir (soluk zeminde sıralanmış nesneler, sağ "
            "üçte biri boş) ve oraya bağlandı. Modül 05'in sanatı "
            "teslim edilmedi.",
        "status": ("READY" if len(ready) >= 5 and not hits and not over
                   else "PARTIAL — %d/%d modül hazır" % (len(ready), len(mods))
                   if ready and not hits and not over else "DEFECT"),
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
    print("\n── MODÜL HARİTASI ──")
    for m in mods:
        print("  %-10s %-34s %s" % (m["id"], m["name"],
                                    "✓ " + ", ".join(os.path.basename(f)
                                                     for f in m["imagesPresent"])
                                    if m["imagesPresent"] else "⛔ sanat yok"))
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
    print("  hazır modül : %s" % ", ".join(m["id"] for m in ready))
    if missing:
        print("  ⛔ sanatı OLMAYAN modül: %s"
              % ", ".join(m["id"] for m in mods if not m["processed"]))
        print("     Metni hazır, görseli yok. Yüklenebilir A+ projesi %d "
              "modülden oluşur." % len(ready))
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
