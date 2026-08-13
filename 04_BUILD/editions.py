#!/usr/bin/env python3
"""
SÜRÜM VE TELİF MODELİ — The Great Book of World Games
================================================================================
Her sürüm için birim telifi ve başabaş ACOS'u KDP'nin yayımlanmış formülüyle
hesaplar. Girdi tek yerdedir: `project_config.json § production`.

  baskı maliyeti = sabit + sayfa × sayfa başına
  telif          = liste × oran − baskı maliyeti
  başabaş ACOS   = telif ÷ liste

BAŞABAŞ ACOS NEDEN ÖNEMLİ: reklamın hata payı doğrudan birim teliftir.
10,99 $ telifli ciltli sürümde %31 ACOS'a kadar dayanılır; 4,00 $ telifli bir
sürümde aynı reklam zarar yazar. Bu yüzden sayfa sayısı bir fiyat kararıdır.

Sayfa sayısı `page_budget.py`'nin modelinden okunur — iki betiğin AYRI sayfa
sayısı kullanması, World Myths'te kapak sırtının iç bloktan farklı sayfa
sayısıyla hesaplanmasına yol açan kusurun aynısıdır.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

BANDS = {"paperback": "paperbackLargeTrimBW", "hardcover": "hardcoverLargeTrimBW"}


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def modelled_pages(cfg: dict) -> int:
    """page_budget.py ile AYNI formül. İki betik tek bir sayfa sayısı kullanır."""
    scope, pm = cfg["scope"], cfg["production"]["pageModel"]
    raw = (scope["games"] * pm["pagesPerGame"]
           + scope["families"] * pm["familyOpenerPages"]
           + pm["frontMatterPages"] + pm["backMatterPages"])
    mult = max(1, pm.get("signatureMultiple", 1))
    return int(math.ceil(raw / mult) * mult)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  SÜRÜM VE TELİF MODELİ")
    print("=" * 74)

    try:
        cfg = load(os.path.join(root, "project_config.json"))
    except (OSError, json.JSONDecodeError) as exc:
        print("  ⛔ project_config.json okunamadı: %s" % exc)
        return 1

    prod = cfg.get("production", {})
    pc = prod.get("kdpPrintCost", {})
    pages = modelled_pages(cfg)
    errors: list[str] = []
    rows: list[dict] = []

    print("\n  modellenen sayfa sayısı: %d\n" % pages)
    print("  %-11s %8s %8s %8s %9s  %s"
          % ("sürüm", "liste", "baskı", "telif", "b.e.ACOS", "durum"))
    print("  " + "-" * 62)

    for ed in prod.get("editionsHypothesis", []):
        eid = ed.get("id")
        if not ed.get("enabled"):
            print("  %-11s %8s %8s %8s %9s  devre dışı" % (eid, "—", "—", "—", "—"))
            continue
        lst = ed.get("list")
        if lst is None:
            errors.append("%s etkin ama fiyatı yok" % eid)
            continue

        if eid in BANDS:
            b = pc.get(BANDS[eid], {})
            cost = b.get("fixed", 0) + pages * b.get("perPage", 0)
            rate = (pc.get("royaltyRateAtOrAbove999", 0.6) if lst >= 9.99
                    else pc.get("royaltyRateBelow999", 0.5))
            if not (b.get("minPages", 0) <= pages <= b.get("maxPages", 10 ** 6)):
                errors.append("%s: %d sayfa KDP sınırları dışında" % (eid, pages))
        elif eid == "kindle":
            rate = pc.get("kindleRoyaltyRate70", 0.70)
            cost = pc.get("kindleDeliveryPerMB", 0.15) * pc.get(
                "kindleFileSizeMBHypothesis", 0)
            lo, hi = pc.get("kindle70BandMin", 2.99), pc.get("kindle70BandMax", 12.99)
            if not lo <= lst <= hi:
                errors.append("kindle fiyatı %%70 bandı dışında: %.2f ∉ [%.2f, %.2f]"
                              % (lst, lo, hi))
        else:
            continue

        royalty = lst * rate - cost
        acos = (royalty / lst * 100.0) if lst else 0.0
        ok = royalty > 0
        if not ok:
            errors.append("%s telifi pozitif değil: %.2f $" % (eid, royalty))

        print("  %-11s %8.2f %8.2f %8.2f %8.1f%%  %s"
              % (eid, lst, cost, royalty, acos, "✓" if ok else "✗ NEGATİF"))
        rows.append({"id": eid, "list": lst, "printCost": round(cost, 2),
                     "royalty": round(royalty, 2), "breakEvenAcosPct": round(acos, 1),
                     "royaltyRate": rate})

    # KDP Select kararı bir hesaptır, bir tercih değildir (karar K6).
    if not prod.get("kdpSelect", False) and rows:
        pb = next((r for r in rows if r["id"] == "paperback"), None)
        if pb:
            kenp_full = pages * 0.00482
            ratio = pb["royalty"] / kenp_full if kenp_full else 0
            print("\n── KDP Select / KU kontrolü (karar K6) ──")
            print("  %d sayfalık tam okuma ≈ %.2f $ · ciltsiz telif %.2f $ → %.1f kat kayıp"
                  % (pages, kenp_full, pb["royalty"], ratio))
            if ratio < 1:
                print("  ! HESAP TERSİNE DÖNDÜ: KU bu sayfa sayısında daha kârlı olabilir.")
                print("    K6 kararı yeniden değerlendirilmelidir.")

    print("\n" + "=" * 74)
    if errors:
        for e in errors:
            print("  ✗ %s" % e)
        print("  ⛔ SÜRÜM MODELİ KIRMIZI")
        status = "fail"
    else:
        print("  ✅ bütün etkin sürümler pozitif telif üretiyor · %d sayfa" % pages)
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "pages": pages, "editions": rows,
                       "errors": errors}, fh, ensure_ascii=False, indent=2)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
