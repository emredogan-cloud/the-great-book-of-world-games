#!/usr/bin/env python3
"""
KÜTÜPHANECİ ALIMI — The Great Book of World Games
================================================================================
Kurucunun sağladığı kural özetlerini YAPISAL kanonik kayda çevirir.

  ⚠ KURUCU ÖZETİ, BAĞIMSIZ DOĞRULANMIŞ KAYNAK DEĞİLDİR.

Bu ayrım bu betiğin varlık sebebidir. Kurucu malzemesi üretim için
YETERLİDİR (kurucu onayı K28) ama `page-verified` bir künye ile aynı şey
değildir. Her kayıt ikisini de ayrı ayrı taşır:

    founderSupplied         = true
    independentVerification = true / false
    bibliographyStatus      = complete / incomplete

⚠ SAYFA NUMARASI UYDURULMAZ. Kurucu malzemesi URL veriyor ama baskı ve
sayfa vermiyorsa, `sourcePages` BOŞ kalır ve `bibliographyStatus`
`incomplete` yazılır. Doğrulayıcıyı yeşile boyamak için bir künye
uydurmak, kitabın tek denetlenebilir iddiasını yıkar.

Çıktı:
  01_SOURCE/rules/librarian_delivery.json   korumalı · tam kural özeti
  06_REPORTS/librarian-ingest.json          public   · yalnızca sayı ve bayrak

Çıkış kodları:  0 = alındı   1 = hata
"""
from __future__ import annotations
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

REQUIRED = ("gameId", "title", "culture", "family", "players", "setup",
            "firstMove", "legalMoves", "ending", "sourceSummary",
            "founderSupplied", "independentVerification",
            "bibliographyStatus", "restrictionScreened",
            "reconstructionStatus")

DELIVERY_FILE = "games-lib-screenshots/Tien gow Tin Kau 天九 ve.txt"


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def check(root, records, rep):
    """Kayıtların dürüstlüğünü denetler."""
    errs = []
    seen = set()
    for r in records:
        gid = r.get("gameId", "?")
        miss = [f for f in REQUIRED if f not in r or r[f] in (None, "", [])]
        if miss:
            errs.append("%s → eksik alan: %s" % (gid, ",".join(miss)))
        if gid in seen:
            errs.append("%s → yinelenen kayıt" % gid)
        seen.add(gid)
        # ⚠ EN ÖNEMLİ DENETİM: sayfa iddiası ile künye durumu çelişemez.
        if r.get("sourcePages") and r.get("bibliographyStatus") != "complete":
            errs.append("%s → sayfa veriyor ama künye 'incomplete'" % gid)
        if r.get("independentVerification") and not r.get("sourcePages"):
            errs.append("%s → 'bağımsız doğrulanmış' diyor ama sayfa YOK" % gid)
        if not r.get("founderSupplied"):
            errs.append("%s → kütüphaneci kaydı 'founderSupplied' değil" % gid)
    return errs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    print("=" * 74)
    print("  KÜTÜPHANECİ ALIMI%s" % (" (--check)" if args.check else ""))
    print("=" * 74)

    cpath = os.path.join(root, "01_SOURCE", "rules", "librarian_delivery.json")
    if not os.path.exists(cpath):
        print("  · kütüphaneci kaydı yok — kapı BOŞ KOŞAR (public katman)")
        ppath = os.path.join(root, "06_REPORTS", "librarian-ingest.json")
        if os.path.exists(ppath):
            pub = load(ppath)
            print("  · public özet: %d oyun · %d bağımsız doğrulanmış"
                  % (pub.get("records", 0), pub.get("independentlyVerified", 0)))
        print("=" * 74)
        return 0

    data = load(cpath)
    records = data.get("records", [])
    errs = check(root, records, None)

    src = os.path.join(root, DELIVERY_FILE)
    if not os.path.exists(src):
        print("  ! kaynak teslim dosyası bulunamadı: %s" % DELIVERY_FILE)

    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        print("\n  ⛔ %d KAYIT KUSURU" % len(errs))
        print("=" * 74)
        return 1

    iv = sum(1 for r in records if r.get("independentVerification"))
    bc = sum(1 for r in records if r.get("bibliographyStatus") == "complete")
    pub = {
        "$comment": [
            "KÜTÜPHANECİ ALIMI — public yapısal özet.",
            "Kural metni BURADA DURMAZ; yalnızca sayı ve dürüstlük bayrakları.",
            "Tam kayıt korumalı katmandadır (01_SOURCE/rules/).",
        ],
        "generatedAtPhase": data.get("phase", "phase5"),
        "deliveryFile": DELIVERY_FILE,
        "records": len(records),
        "founderSupplied": sum(1 for r in records if r.get("founderSupplied")),
        "independentlyVerified": iv,
        "bibliographyComplete": bc,
        "bibliographyIncomplete": len(records) - bc,
        "games": sorted(r["gameId"] for r in records),
    }
    dump(os.path.join(root, "06_REPORTS", "librarian-ingest.json"), pub)

    print("  ✓ %d kayıt alındı" % len(records))
    print("      kurucu tarafından sağlanan : %d" % pub["founderSupplied"])
    print("      BAĞIMSIZ doğrulanmış       : %d" % iv)
    print("      künyesi TAM                : %d" % bc)
    print("      künyesi EKSİK              : %d" % (len(records) - bc))
    if iv == 0:
        print("  · hiçbiri bağımsız doğrulanmamıştır ve kayıt bunu SÖYLÜYOR")
    print("=" * 74)
    if args.json:
        dump(os.path.join(root, args.json), pub)
    return 0


if __name__ == "__main__":
    sys.exit(main())
