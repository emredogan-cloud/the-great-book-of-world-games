#!/usr/bin/env python3
"""
ADAY SEÇİM MODELİ — The Great Book of World Games
================================================================================
Faz 1'in çıktısı bir liste değil, bir KARAR YORDAMIDIR. Bu betik 150 adayı
sekiz tanımlı ölçütle sıralar ve kitabın hipotez kapsamına bir ÖNERİ üretir.

  ⚠ Bu betik KARAR VERMEZ. Öneri üretir; nihai liste kurucu kararıdır (A3).

Sekiz ölçüt ve ağırlıkları (toplam 1,00). Ağırlıklar yol haritasının öncelik
sırasından türetilmiştir — keyfî değildir:

  playability 0,22  · oynanabilirlik önceliği 1'dir; kural eksikse gerisi boştur
  source      0,18  · kaynak izlenebilirliği önceliği 3'tür ve locked kapısıdır
  cultural    0,12  · kitabın tezi kültürel derinlikse ölçülmelidir
  distinct    0,12  · aynı mekaniğin dokuzuncu tekrarı kitabı zayıflatır
  access      0,10  · malzeme evde yoksa 'bu akşam' vaadi düşer
  explain     0,10  · 650 kelimede anlatılamayan oyun sayfaya sığmaz
  play        0,10  · masada iyi olmayan oyun iyi yorum getirmez
  visual      0,06  · gravür dili değerlidir ama oyunu kurtarmaz

ÇEŞİTLİLİK BONUSU: aynı ailede henüz temsil edilmemiş bir kültür +0,15 alır.
Gerekçe: alt başlık 45 kültür vaat eder ve bu vaat bir kapıdır, süs değildir.
Bonus seçim SIRASINI etkiler, ham puanı DEĞİŞTİRMEZ — ikisi ayrı raporlanır.

Uygunluk (eligibility) filtresi puandan ÖNCE çalışır:
  · status `dropped` değil
  · restrictionStatus `open` ya da `attributed`
  · playabilityStatus `rules-complete` ya da `reconstructed`
Bir oyun ne kadar yüksek puan alırsa alsın, bu üç şartı geçmeden öneriye giremez.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

WEIGHTS = {
    "playability": 0.22,
    "source":      0.18,
    "cultural":    0.12,
    "distinct":    0.12,
    "access":      0.10,
    "explain":     0.10,
    "play":        0.10,
    "visual":      0.06,
}
DIVERSITY_BONUS = 0.15
ELIGIBLE_RESTRICTION = ("open", "attributed")
ELIGIBLE_PLAYABILITY = ("rules-complete", "reconstructed")


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def raw_score(game: dict) -> float:
    s = game.get("scores") or {}
    return round(sum(WEIGHTS[k] * s.get(k, 0) for k in WEIGHTS), 4)


def eligible(game: dict) -> tuple[bool, str]:
    if game.get("status") == "dropped":
        return False, "dropped"
    if game.get("restrictionStatus") not in ELIGIBLE_RESTRICTION:
        return False, "kısıt: %s" % game.get("restrictionStatus")
    if game.get("playabilityStatus") not in ELIGIBLE_PLAYABILITY:
        return False, "oynanabilirlik: %s" % game.get("playabilityStatus")
    return True, ""


def select(games: list, families: list) -> tuple[list, dict]:
    """Aile hedeflerine göre öneri listesi üretir.

    Sıralama deterministiktir: eşit puanda gameId alfabetik sırayı belirler.
    Aynı girdi her makinede AYNI öneriyi üretmelidir."""
    chosen: list = []
    per_family: dict = {}
    for fam in sorted(families, key=lambda f: f.get("order", 99)):
        fid, target = fam["id"], fam.get("targetGames", 0)
        pool = [g for g in games if g.get("family") == fid and eligible(g)[0]]
        pool.sort(key=lambda g: (-raw_score(g), g.get("gameId", "")))

        picked, seen_cultures = [], set()
        while pool and len(picked) < target:
            best, best_eff = None, None
            for g in pool:
                eff = raw_score(g) + (DIVERSITY_BONUS
                                      if g.get("culture") not in seen_cultures else 0.0)
                key = (-eff, g.get("gameId", ""))
                if best_eff is None or key < best_eff:
                    best, best_eff = g, key
            pool.remove(best)
            seen_cultures.add(best.get("culture"))
            picked.append(best)

        per_family[fid] = {"target": target, "eligible": len(
            [g for g in games if g.get("family") == fid and eligible(g)[0]]),
            "selected": len(picked), "cultures": len(seen_cultures)}
        chosen.extend(picked)
    return chosen, per_family


def propose_rebalance(families: list, per_family: dict, short: int) -> dict:
    """Açığı, uygun adayı ARTAN ailelere dağıtan bir hedef önerisi üretir.

    Toplam oyun sayısı korunur: bir ailenin hedefi düşerse bir başkasınınki
    yükselir. Dağıtım deterministiktir — en çok yedeği olan aile önce alır,
    eşitlikte aile sırası (order) belirler.

    ⚠ Bu bir ÖNERİDİR. Aile hedefi taksonomi tezinin parçasıdır ve
    değiştirilmesi kurucu kararıdır (A2/A3)."""
    proposal: dict = {}
    surplus: list = []
    for fam in sorted(families, key=lambda f: f.get("order", 99)):
        fid = fam["id"]
        st = per_family.get(fid, {})
        target, avail = st.get("target", 0), st.get("eligible", 0)
        if avail < target:
            proposal[fid] = (target, avail)
        elif avail > target:
            surplus.append([fid, target, avail - target])

    remaining = short
    while remaining > 0 and surplus:
        surplus.sort(key=lambda s: (-s[2], s[0]))
        head = surplus[0]
        take = min(remaining, head[2])
        old = proposal.get(head[0], (head[1], head[1]))[0]
        proposal[head[0]] = (old, proposal.get(head[0], (head[1], head[1]))[1] + take
                             if head[0] in proposal else head[1] + take)
        head[2] -= take
        remaining -= take
        if head[2] == 0:
            surplus.pop(0)
    return proposal


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  ADAY SEÇİM MODELİ")
    print("=" * 74)

    try:
        cfg = load(os.path.join(root, "project_config.json"))
        fams = load(os.path.join(root, "01_SOURCE", "family_index.json"))
        idx = load(os.path.join(root, "01_SOURCE", "game_index.json"))
    except (OSError, json.JSONDecodeError) as exc:
        print("  ⛔ kaynak dosya okunamadı: %s" % exc)
        return 1

    games = idx.get("games", []) if isinstance(idx, dict) else idx
    families = fams.get("families", [])
    errors: list[str] = []

    # Ağırlıklar toplamı 1,00 olmalıdır; olmazsa puanlar karşılaştırılamaz.
    total_w = round(sum(WEIGHTS.values()), 6)
    if total_w != 1.0:
        errors.append("ağırlıklar toplamı 1,00 değil: %.6f" % total_w)

    missing_scores = [g.get("gameId") for g in games
                      if not isinstance(g.get("scores"), dict)
                      or any(k not in g["scores"] for k in WEIGHTS)]
    if missing_scores:
        errors.append("puanlanmamış kayıt: %s" % ", ".join(missing_scores[:5]))

    out_of_range = [g.get("gameId") for g in games
                    if isinstance(g.get("scores"), dict)
                    and any(not isinstance(g["scores"].get(k), int)
                            or not 1 <= g["scores"][k] <= 5 for k in WEIGHTS)]
    if out_of_range:
        errors.append("1–5 aralığı dışında puan: %s" % ", ".join(out_of_range[:5]))

    if errors:
        for e in errors:
            print("  ✗ %s" % e)
        print("\n  ⛔ seçim modeli koşamadı")
        return 1

    elig = [g for g in games if eligible(g)[0]]
    print("\n── uygunluk ──")
    print("  · %d kayıt · %d uygun · %d elendi" % (len(games), len(elig),
                                                   len(games) - len(elig)))
    reasons: dict[str, int] = {}
    for g in games:
        ok, why = eligible(g)
        if not ok:
            reasons[why] = reasons.get(why, 0) + 1
    for why, n in sorted(reasons.items(), key=lambda kv: -kv[1]):
        print("     %-32s %3d" % (why, n))

    chosen, per_family = select(games, families)
    chosen_ids = {g["gameId"] for g in chosen}
    cultures = {g.get("culture") for g in chosen}

    print("\n── aile başına öneri ──")
    short = 0
    for fam in sorted(families, key=lambda f: f.get("order", 99)):
        st = per_family[fam["id"]]
        flag = "" if st["selected"] >= st["target"] else "  ← HEDEF DOLMUYOR"
        if st["selected"] < st["target"]:
            short += st["target"] - st["selected"]
        print("  %-12s hedef %2d · uygun %2d · seçilen %2d · kültür %2d%s"
              % (fam["id"], st["target"], st["eligible"], st["selected"],
                 st["cultures"], flag))

    print("\n── öneri özeti ──")
    print("  · önerilen oyun : %d (hedef %d)" % (len(chosen), cfg["scope"]["games"]))
    print("  · farklı kültür : %d (hedef %d)" % (len(cultures), cfg["scope"]["cultures"]))
    print("  · yedek havuzu  : %d uygun oyun öneri dışında"
          % (len(elig) - len(chosen)))

    if args.verbose:
        print("\n── ilk 15 (ham puan) ──")
        for g in sorted(elig, key=lambda g: (-raw_score(g), g["gameId"]))[:15]:
            print("  %5.3f  %-24s %-12s %s"
                  % (raw_score(g), g["gameId"], g["family"], g.get("culture")))

    rebalance: dict = {}
    ok = True
    print("\n── kapı ──")
    if short:
        print("  ! %d oyunluk açık var — uygun aday sayısı hedefi doldurmuyor" % short)
        print("    Bu bir VERİ hatası değil, bir KAPSAM bulgusudur: ya hedef")
        print("    düşürülür ya araştırma sürer (yol haritası § FAIL).")
        rebalance = propose_rebalance(families, per_family, short)
        if rebalance:
            print("\n  ÖNERİLEN YENİDEN DENGELEME (kurucu kararı A2/A3):")
            for fid, (old, new) in sorted(rebalance.items()):
                arrow = "↓" if new < old else "↑"
                print("     %-12s %2d %s %2d" % (fid, old, arrow, new))
            print("     Açık, uygun adayı ARTAN ailelere dağıtılır; toplam %d korunur."
                  % cfg["scope"]["games"])
            print("     ⚠ Bu bir ÖNERİDİR. Aile hedeflerini değiştirmek taksonomi")
            print("       tezini değiştirir ve kurucu onayı gerektirir.")
    else:
        print("  ✓ bütün aile hedefleri uygun adaylarla doluyor")

    if len(cultures) < cfg["scope"]["cultures"]:
        print("  ✗ öneri listesi kültür hedefini tutmuyor: %d < %d"
              % (len(cultures), cfg["scope"]["cultures"]))
        ok = False
    else:
        print("  ✓ öneri listesi kültür hedefini tutuyor")

    print("\n" + "=" * 74)
    print("  %s" % ("✅ seçim modeli koştu" if ok else "⛔ SEÇİM MODELİ KIRMIZI"))
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        payload = {
            "status": "pass" if ok else "fail",
            "weights": WEIGHTS,
            "diversityBonus": DIVERSITY_BONUS,
            "eligible": len(elig),
            "proposed": len(chosen),
            "proposedCultures": sorted(c for c in cultures if c),
            "perFamily": per_family,
            "shortfall": short,
            "proposedRebalance": {k: {"current": v[0], "proposed": v[1]}
                                  for k, v in sorted(rebalance.items())},
            "proposal": [
                {"gameId": g["gameId"], "family": g["family"],
                 "culture": g.get("culture"), "score": raw_score(g)}
                for g in sorted(chosen, key=lambda g: (g["family"], -raw_score(g),
                                                       g["gameId"]))],
            "reserve": sorted(g["gameId"] for g in elig
                              if g["gameId"] not in chosen_ids),
        }
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
