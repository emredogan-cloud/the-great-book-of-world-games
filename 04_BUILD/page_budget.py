#!/usr/bin/env python3
"""
SAYFA BÜTÇESİ — The Great Book of World Games
================================================================================
SAYFA SAYISI BİR TASARIM TERCİHİ DEĞİL, FİYAT MODELİNİN KENDİSİDİR.
KDP büyük trim siyah-beyaz baskı sayfa başına 0,017 $'dır: 256 yerine 300
sayfa, her satılan kopyada telifi 0,75 $ düşürür ve reklamın hata payını
doğrudan yer.

Bu betik modeli HESAPLAR ve hedefle karşılaştırır. Hiçbir sabit değer taşımaz;
hepsi `project_config.json § production.pageModel` içindedir.

  gövde   = önerilen oyun sayısı × sayfa/oyun
  açılış  = aile sayısı × aile açılış sayfası
  ön/arka = ön madde + arka madde
  toplam  = yukarıdakiler, forma katına yuvarlanmış

⚠ MODEL KALİBRE EDİLMEMİŞTİR. `pageModel.calibrated` false olduğu sürece
çıktı bir HİPOTEZDİR ve bu rapor bunu her koşuda söyler. Gerçek ölçüm
Faz 2'nin işidir (12 oyunluk pilotun dizilmiş sayfa sayısı).

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


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  SAYFA BÜTÇESİ")
    print("=" * 74)

    try:
        cfg = load(os.path.join(root, "project_config.json"))
    except (OSError, json.JSONDecodeError) as exc:
        print("  ⛔ project_config.json okunamadı: %s" % exc)
        return 1

    scope = cfg.get("scope", {})
    prod = cfg.get("production", {})
    pm = prod.get("pageModel")
    if not pm:
        print("  ✗ production.pageModel tanımsız — model hesaplanamaz")
        return 1

    games = scope.get("games", 0)
    families = scope.get("families", 0)
    target = scope.get("pageTarget", 0)
    tol_pct = scope.get("pageTolerancePct", 6)

    body = games * pm["pagesPerGame"]
    openers = families * pm["familyOpenerPages"]
    front = pm["frontMatterPages"]
    back = pm["backMatterPages"]
    raw = body + openers + front + back

    mult = max(1, pm.get("signatureMultiple", 1))
    total = int(math.ceil(raw / mult) * mult)

    lo = target * (1 - tol_pct / 100.0)
    hi = target * (1 + tol_pct / 100.0)
    deviation = (total - target) / target * 100.0 if target else 0.0
    within = lo <= total <= hi

    words = games * scope.get("gameWordTarget", 0)
    wpp = pm.get("wordsPerTypesetPageHypothesis", 0)
    implied_body_pages = round(words / wpp, 1) if wpp else 0

    print("\n── model ──")
    print("  gövde        %3d oyun × %d sayfa      = %4d" % (games, pm["pagesPerGame"], body))
    print("  aile açılışı %3d aile × %d sayfa      = %4d" % (families, pm["familyOpenerPages"], openers))
    print("  ön madde                             = %4d" % front)
    print("  arka madde                           = %4d" % back)
    print("  " + "-" * 52)
    print("  ham toplam                           = %4d" % raw)
    print("  forma katına yuvarlanmış (×%d)        = %4d" % (mult, total))

    print("\n── hedefle karşılaştırma ──")
    print("  hedef        %d ± %%%d  (%.0f – %.0f)" % (target, tol_pct, lo, hi))
    print("  model        %d" % total)
    print("  sapma        %+.1f%%" % deviation)

    print("\n── çapraz denetim: kelime bütçesi ne diyor ──")
    print("  %d oyun × %d kelime = %d kelime" % (games, scope.get("gameWordTarget", 0), words))
    print("  %d kelime/sayfa varsayımıyla gövde ≈ %.1f sayfa (model %d)"
          % (wpp, implied_body_pages, body))
    if implied_body_pages and body:
        gap = abs(implied_body_pages - body) / body * 100.0
        print("  iki tahmin arası fark: %%%.0f" % gap)
        if gap > 25:
            print("  ! İKİ TAHMİN AYRIŞIYOR. Sayfa/oyun ile kelime/oyun aynı kitabı")
            print("    tarif etmiyor; biri diyagram alanını hesaba katmıyor olabilir.")
            print("    Faz 2 gerçek dizgisi hangisinin doğru olduğunu söyleyecek.")

    calibrated = bool(pm.get("calibrated"))
    print("\n── kalibrasyon ──")
    if calibrated:
        print("  ✓ model gerçek dizgiyle kalibre edilmiş")
    else:
        print("  ⚠ MODEL KALİBRE EDİLMEDİ — bu sayılar HİPOTEZDİR.")
        print("    Gerçek ölçüm %s fazında yapılır (12 oyunluk pilot dizgisi)."
              % pm.get("calibratedAtPhase", "phase2"))

    errors = []
    if not within:
        errors.append("model hedeften %%%d'den fazla sapıyor (%+.1f%%)"
                      % (tol_pct, deviation))

    # KDP sayfa sınırları: modelin basılabilir olması gerekir.
    pc = prod.get("kdpPrintCost", {})
    for ed in prod.get("editionsHypothesis", []):
        if not ed.get("enabled"):
            continue
        band = {"paperback": "paperbackLargeTrimBW",
                "hardcover": "hardcoverLargeTrimBW"}.get(ed["id"])
        if not band or band not in pc:
            continue
        b = pc[band]
        if not (b.get("minPages", 0) <= total <= b.get("maxPages", 10 ** 6)):
            errors.append("%s sayfa sınırları dışında: %d ∉ [%d, %d]"
                          % (ed["id"], total, b.get("minPages"), b.get("maxPages")))

    print("\n" + "=" * 74)
    if errors:
        for e in errors:
            print("  ✗ %s" % e)
        print("  ⛔ SAYFA MODELİ KIRMIZI")
        status = "fail"
    else:
        print("  ✅ sayfa modeli hedef bandında · %d sayfa (hedef %d, %+.1f%%)"
              % (total, target, deviation))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({
                "status": status,
                "calibrated": calibrated,
                "hypothesis": not calibrated,
                "model": {"games": games, "families": families,
                          "bodyPages": body, "openerPages": openers,
                          "frontMatterPages": front, "backMatterPages": back,
                          "rawTotal": raw, "total": total},
                "target": target, "tolerancePct": tol_pct,
                "deviationPct": round(deviation, 2), "withinTolerance": within,
                "wordCrossCheck": {"words": words, "wordsPerPage": wpp,
                                   "impliedBodyPages": implied_body_pages},
                "errors": errors,
            }, fh, ensure_ascii=False, indent=2)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
