#!/usr/bin/env python3
"""
TASNİF KAPISI — The Great Book of World Games
================================================================================
Bu kitabın tezi şudur: oyunlar bölgeye göre değil MEKANİĞE göre dizilir.
Tez bir iddiadır; bu kapı onu bir kurala çevirir.

Denetlenen:
  ① Her aile tanımlı mı — tanım · giriş kuralı · dışlama kuralı · SINIR kuralı
  ② Her oyun TAM BİR aileye ait mi
  ③ Her oyunun tasnif GEREKÇESİ yazılı mı (taxonomyRationale)
  ④ İkincil aile, birincil aileden farklı ve tanımlı mı
  ⑤ Aile dengesi: her aile candidateFloor'u taşıyor mu
  ⑥ Kısıt taraması TAM mı — ve attributed/restricted/excluded GEREKÇELİ mi
  ⑦ Kültür sayısı alt başlığın vaadini karşılıyor mu

⑥ NEDEN BURADA: kısıt taraması bir tasnif işidir. Bir oyunun hangi aileye
ait olduğunu bilmek yetmez; KİME ait olduğunu da bilmek gerekir. Gerekçesiz
bir `restricted` etiketi, hiç taranmamış bir kayıt kadar değersizdir.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

# Gerekçe zorunlu olan kısıt durumları. `open` gerekçe istemez: serbestlik
# varsayılan değil, TARANMIŞ bir sonuçtur ve ayrıca açıklanmasına gerek yoktur.
RESTRICTION_NEEDS_NOTE = ("attributed", "restricted", "excluded")
RATIONALE_MIN = 10


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.facts: dict = {}

    def check(self, cond: bool, label: str) -> bool:
        self.checks += 1
        if cond:
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return cond

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def brief(items: list, n: int = 5) -> str:
    if not items:
        return ""
    shown = ", ".join(str(i) for i in items[:n])
    more = "" if len(items) <= n else " … (+%d)" % (len(items) - n)
    return " — %s%s" % (shown, more)


def check_families(fams: dict, rep: Report) -> dict:
    print("\n── aile tanımları ──")
    entries = fams.get("families", [])
    rep.check(bool(entries), "family_index.json aile taşıyor")

    required = ("id", "definition", "inclusionRule", "exclusionRule",
                "boundaries", "rationale", "targetGames", "candidateFloor")
    incomplete = [f.get("id", "?") for f in entries
                  if any(not f.get(k) for k in required)]
    rep.check(not incomplete,
              "her ailenin tanım · giriş · dışlama · SINIR kuralı var"
              + brief(incomplete))

    # Sınır kuralı bir komşuya işaret etmelidir; kime karşı çizildiği
    # yazılmamış bir sınır, sınır değildir.
    fam_ids = {f["id"] for f in entries}
    bad_bounds = []
    for f in entries:
        for b in f.get("boundaries", []):
            if b.get("vs") not in fam_ids or not b.get("rule"):
                bad_bounds.append("%s → %s" % (f.get("id"), b.get("vs")))
    rep.check(not bad_bounds,
              "her sınır kuralı tanımlı bir komşu aileye bakıyor" + brief(bad_bounds))

    rep.check(bool(fams.get("classificationProcedure")),
              "tasnif yordamı yazılı (deterministik atama)")

    rep.facts["families"] = len(entries)
    return {f["id"]: f for f in entries}


def check_games(games: list, fam_map: dict, rep: Report) -> None:
    print("\n── oyun tasnifi ──")

    no_family = [g.get("gameId") for g in games if g.get("family") not in fam_map]
    rep.check(not no_family, "her oyun tanımlı bir aileye ait" + brief(no_family))

    thin = [g.get("gameId") for g in games
            if len((g.get("taxonomyRationale") or "").strip()) < RATIONALE_MIN]
    rep.check(not thin,
              "her oyunun tasnif gerekçesi yazılı (≥%d karakter)" % RATIONALE_MIN
              + brief(thin))

    bad_secondary = [g.get("gameId") for g in games
                     if g.get("secondaryFamily")
                     and (g["secondaryFamily"] not in fam_map
                          or g["secondaryFamily"] == g.get("family"))]
    rep.check(not bad_secondary,
              "ikincil aile tanımlı ve birincilden farklı" + brief(bad_secondary))

    print("\n── kısıt taraması ──")
    unscreened = [g.get("gameId") for g in games if not g.get("restrictionStatus")]
    rep.check(not unscreened, "kısıt taraması TAM — taranmamış kayıt yok"
              + brief(unscreened))

    ungrounded = [g.get("gameId") for g in games
                  if g.get("restrictionStatus") in RESTRICTION_NEEDS_NOTE
                  and not (g.get("restrictionNote") or "").strip()]
    rep.check(not ungrounded,
              "attributed / restricted / excluded kayıtların GEREKÇESİ var"
              + brief(ungrounded))

    # Bir oyun kitaba giremiyorsa envanter bunu İKİ yerde birden söylemelidir:
    # kısıt durumunda ve editoryal durumda. Tek yerde söylenen bir eleme,
    # ikinci bir betiğin onu sessizce kitaba almasına izin verir.
    leaky = [g.get("gameId") for g in games
             if g.get("restrictionStatus") in ("restricted", "excluded")
             and g.get("editorialStatus") != "rejected"]
    rep.check(not leaky,
              "restricted / excluded oyunlar editoryal olarak da reddedilmiş"
              + brief(leaky))

    for st in ("open", "attributed", "restricted", "excluded"):
        rep.facts["restriction_%s" % st] = sum(
            1 for g in games if g.get("restrictionStatus") == st)

    print("\n── aile dengesi ──")
    counts: dict[str, int] = {}
    for g in games:
        if g.get("status") == "dropped":
            continue
        counts[g.get("family")] = counts.get(g.get("family"), 0) + 1
    rep.facts["family_counts"] = counts

    for fid, fam in sorted(fam_map.items(), key=lambda kv: kv[1].get("order", 99)):
        floor = fam.get("candidateFloor", 0)
        have = counts.get(fid, 0)
        rep.check(have >= floor,
                  "%-12s %3d aday ≥ %d taban" % (fid, have, floor))

    print("\n── kültür çeşitliliği ──")
    cultures = {g.get("culture") for g in games
                if g.get("culture") and g.get("status") != "dropped"
                and g.get("restrictionStatus") not in ("restricted", "excluded")}
    rep.facts["cultures"] = len(cultures)
    rep.facts["candidates"] = sum(1 for g in games if g.get("status") != "dropped")
    rep.facts["dropped"] = sum(1 for g in games if g.get("status") == "dropped")
    print("  · yayımlanabilir kayıtlarda %d farklı kültür" % len(cultures))
    print("  · %d aday · %d düşen" % (rep.facts["candidates"], rep.facts["dropped"]))


def check_scope(cfg: dict, rep: Report) -> None:
    scope = cfg.get("scope", {})
    rep.check(rep.facts.get("families", 0) == scope.get("families"),
              "aile sayısı yapılandırmayla uyuşuyor (%d)" % rep.facts.get("families", 0))
    rep.check(rep.facts.get("cultures", 0) >= scope.get("cultures", 0),
              "kültür sayısı alt başlığın vaadini karşılıyor (≥%d · ölçülen %d)"
              % (scope.get("cultures", 0), rep.facts.get("cultures", 0)))
    rep.check(rep.facts.get("candidates", 0) >= scope.get("gamesCandidateMin", 0),
              "aday sayısı hedefi karşılıyor (≥%d · ölçülen %d)"
              % (scope.get("gamesCandidateMin", 0), rep.facts.get("candidates", 0)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  TASNİF BÜTÜNLÜĞÜ")
    print("=" * 74)

    rep = Report(args.verbose)
    try:
        cfg = load(os.path.join(root, "project_config.json"))
        fams = load(os.path.join(root, "01_SOURCE", "family_index.json"))
        idx = load(os.path.join(root, "01_SOURCE", "game_index.json"))
    except (OSError, json.JSONDecodeError) as exc:
        print("  ⛔ kaynak dosya okunamadı: %s" % exc)
        return 1

    games = idx.get("games", []) if isinstance(idx, dict) else idx
    fam_map = check_families(fams, rep)
    check_games(games, fam_map, rep)
    print("\n── kapsam ──")
    check_scope(cfg, rep)

    print("\n" + "=" * 74)
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil" % rep.checks)
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
