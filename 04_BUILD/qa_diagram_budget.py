#!/usr/bin/env python3
"""
BASILAN DİYAGRAM KAPISI — The Great Book of World Games
================================================================================
`qa_diagram.py` v1 TANIMLAYICILARINI denetler (sözlük, efsane, koordinat).
GBK-02 kurtarmasında kitaptaki her diyagram maddenin kendi `diagramSpecs`
kaydından boards.py ile yeniden çizildi; v1 kümesinin 60 tanımından 45'i
emekli oldu ve kalan 15'i de artık v1 çizimini tarif ediyor. Yani K19
bütçesini v1 ölçümünden hesaplayan bir kapı, BASILMAYAN diyagramları
denetleyip yeşil yanar.

Bu kapı BASILAN kümeyi denetler:
  ① her `diagramSpecs` kaydı render edilmiş ve ÖLÇÜLMÜŞ (06_REPORTS/boards.json)
  ② render ölçümünde TANIMI OLMAYAN diyagram yok (bayat ölçüm)
  ③ her diyagram kendi sayım doğrulamasını geçmiş (boards.py `verify`)
  ④ her diyagramın altyazısı var
  ⑤ K19 — OYUN BAŞINA toplam yükseklik ≤ `maxDiagramMmPerGame`
     (K24 kimlik eşlemesi `diagramBudgetOverrides` burada da geçerli)

⑤ bir KURUCU KARARIDIR. Kapı onu değiştirmez ve yorumlamaz: aşan her oyun
kırmızıdır, ta ki kurucu kararı değişene ya da diyagram küçülene dek.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def brief(items: list, n: int = 5) -> str:
    if not items:
        return ""
    more = "" if len(items) <= n else " … (+%d)" % (len(items) - n)
    return " — %s%s" % (", ".join(str(i) for i in items[:n]), more)


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list = []
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
        return bool(cond)


def run(root: str, rep: Report) -> None:
    cfg = load(os.path.join(root, "project_config.json"))
    bpath = os.path.join(root, "02_MANUSCRIPT", "book.json")
    if not os.path.exists(bpath):
        print("  · manuscript bu depoda yok — kapı BOŞ KOŞAR (CI'da beklenen; "
              "körlüğü selftest kapatır)")
        return
    specs = [(g["gameId"], s) for g in load(bpath).get("games", [])
             for s in (g.get("diagramSpecs") or [])]
    rep.check(bool(specs), "manuscript en az bir basılan diyagram taşıyor")
    rpath = os.path.join(root, "06_REPORTS", "boards.json")
    if not rep.check(os.path.exists(rpath),
                     "render ölçümü var (06_REPORTS/boards.json — önce boards.py)"):
        return
    measured = {m["id"]: m for m in load(rpath).get("diagrams", [])}
    ids = {s["id"] for _, s in specs}

    print("\n── ①–④ basılan diyagramlar (%d) ──" % len(specs))
    unrendered = sorted(i for i in ids if i not in measured)
    rep.check(not unrendered, "her diyagram render edilmiş ve ÖLÇÜLMÜŞ" + brief(unrendered))
    ghost = sorted(set(measured) - ids)
    rep.check(not ghost, "ölçümde TANIMI OLMAYAN diyagram yok (bayat ölçüm)" + brief(ghost))
    failed = sorted("%s → %s" % (i, "; ".join(measured[i]["errors"]))
                    for i in ids if i in measured and measured[i].get("errors"))
    rep.check(not failed, "her diyagram kendi sayım doğrulamasını geçiyor" + brief(failed))
    nocap = sorted(s["id"] for _, s in specs if not (s.get("caption") or "").strip())
    rep.check(not nocap, "her diyagramın altyazısı var" + brief(nocap))

    limit = float(cfg["diagram"]["maxDiagramMmPerGame"])
    overrides = cfg["diagram"].get("diagramBudgetOverrides") or {}
    print("\n── ⑤ K19 · oyun başına diyagram tavanı (%d mm · render ölçümü) ──" % limit)
    per_game: dict = {}
    for gid, s in specs:
        m = measured.get(s["id"])
        if m:
            per_game.setdefault(gid, []).append(float(m["heightMm"]))
    over = []
    for gid, hs in sorted(per_game.items(), key=lambda kv: -sum(kv[1])):
        ov = overrides.get(gid)
        cap = float(ov["maxMm"]) if isinstance(ov, dict) and ov.get("maxMm") else limit
        if sum(hs) > cap:
            over.append("%s %.0f mm (%d diyagram, tavan %.0f)" % (gid, sum(hs), len(hs), cap))
    totals = [sum(hs) for hs in per_game.values()]
    rep.facts = {"printedDiagrams": len(specs), "games": len(per_game),
                 "overBudgetGames": len(over), "limitMm": limit,
                 "maxGameMm": round(max(totals), 1) if totals else 0,
                 "overBudget": over}
    rep.check(not over, "hiçbir OYUN K19 tavanını aşmıyor — %d/%d oyun aşıyor"
              % (len(over), len(per_game)) + brief(over))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  BASILAN DİYAGRAM KAPISI (v2 · K19)")
    print("=" * 74)
    rep = Report(args.verbose)
    try:
        run(root, rep)
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        print("  ⛔ kaynak dosya okunamadı: %s" % exc)
        return 2
    print("\n" + "=" * 74)
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil" % rep.checks)
        status = "pass"
    print("=" * 74)
    if args.json:
        os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks, "errors": rep.errors,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
