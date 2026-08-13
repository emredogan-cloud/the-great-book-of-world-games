#!/usr/bin/env python3
"""
ÜRETİLEN BELGELER — The Great Book of World Games
================================================================================
`BOOK_STATS.md` ve `ROADMAP_PROGRESS.md` bu betikten ÜRETİLİR. İkisi de elle
yazılmaz; içlerindeki her sayı ölçülmüş bir değerdir.

NEDEN: World Myths'te ilerleme tablosu elle güncelleniyordu ve üç fazda bir
gerçekle ayrışıyordu. Belge yalan söylediğinde okuyan ajan yanlış karar verir.
`--check` bayatlığı CI'da kırmızı yakar — disiplin unutulur, mekanizma unutmaz.

  ./04_BUILD/update_docs.py            # üret
  ./04_BUILD/update_docs.py --check    # bayat mı

Çıktı DETERMİNİSTİKTİR: tarih damgası yoktur. İki koşu aynı girdiyle aynı
baytı üretir; yoksa `--check` her koşuda kırmızı yanardı.

Çıkış kodları:  0 = geçti   1 = bayat/kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

PHASES = [
    ("0", "Bootstrap", "phase0", "main", "—"),
    ("1", "Envanter, tasnif ve oynanabilirlik mimarisi", "phase1", "faz/1-envanter", "v0.1.0"),
    ("2", "Pilot: 12 oyun + kalibrasyon", "phase2", "faz/2-pilot", "v0.2.0"),
    ("3", "Üretim bloğu I — Aileler I–IV", "phase3", "faz/3-blok-1", "v0.3.0"),
    ("4", "Üretim bloğu II — Aileler V–VII", "phase4", "faz/4-blok-2", "v0.4.0"),
    ("5", "Editoryal yakınsama + görsel üretim", "phase5", "faz/5-yakinsama", "v0.5.0"),
    ("6", "Nihai üretim + KDP paketi", "release", "faz/6-uretim", "v1.0.0"),
]
GATE_ORDER = [p[2] for p in PHASES]


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def read_gate(root: str) -> str:
    p = os.path.join(root, ".gate")
    if not os.path.exists(p):
        return "phase0"
    with open(p, encoding="utf-8") as fh:
        return fh.read().strip()


def modelled_pages(cfg: dict) -> int:
    scope, pm = cfg["scope"], cfg["production"]["pageModel"]
    raw = (scope["games"] * pm["pagesPerGame"]
           + scope["families"] * pm["familyOpenerPages"]
           + pm["frontMatterPages"] + pm["backMatterPages"])
    mult = max(1, pm.get("signatureMultiple", 1))
    return int(math.ceil(raw / mult) * mult)


def measure(root: str) -> dict:
    cfg = load(os.path.join(root, "project_config.json"))
    fams = load(os.path.join(root, "01_SOURCE", "family_index.json"))
    ipath = os.path.join(root, "01_SOURCE", "game_index.json")
    games = []
    if os.path.exists(ipath):
        idx = load(ipath)
        games = idx.get("games", []) if isinstance(idx, dict) else idx

    live = [g for g in games if g.get("status") != "dropped"]
    publishable = [g for g in live
                   if g.get("restrictionStatus") in ("open", "attributed")]

    m = {
        "cfg": cfg,
        "families": fams.get("families", []),
        "gate": read_gate(root),
        "records": len(games),
        "candidates": len(live),
        "dropped": len(games) - len(live),
        "publishable": len(publishable),
        "locked": sum(1 for g in games if g.get("status") in ("locked", "written")),
        "written": sum(1 for g in games if g.get("status") == "written"),
        "cultures": len({g.get("culture") for g in publishable if g.get("culture")}),
        "regions": len({g.get("region") for g in publishable if g.get("region")}),
        "screened": sum(1 for g in games if g.get("restrictionStatus")),
        "playtestsPassed": sum(
            1 for g in games
            if any(p.get("result") == "playable" and p.get("usedOnlyBookText")
                   for p in (g.get("playtests") or []))),
        "pages": modelled_pages(cfg),
    }
    for st in ("open", "attributed", "restricted", "excluded"):
        m["restriction_" + st] = sum(1 for g in games
                                     if g.get("restrictionStatus") == st)
    for st in ("rules-complete", "reconstructed", "unresolved",
               "not-production-ready", "excluded"):
        m["play_" + st] = sum(1 for g in games if g.get("playabilityStatus") == st)
    m["productionReady"] = m["play_rules-complete"] + m["play_reconstructed"]

    counts: dict[str, int] = {}
    for g in live:
        counts[g.get("family")] = counts.get(g.get("family"), 0) + 1
    m["familyCounts"] = counts

    visual = sum(1 for g in publishable
                 if g.get("visualNeeds") and g["visualNeeds"] != ["none"])
    m["needVisual"] = visual
    return m


def bar(n: int, target: int, width: int = 20) -> str:
    if target <= 0:
        return ""
    filled = min(width, int(round(width * n / target)))
    return "`" + "█" * filled + "·" * (width - filled) + "`"


def render_stats(m: dict) -> str:
    cfg, scope = m["cfg"], m["cfg"]["scope"]
    prod = cfg["production"]
    pc = prod["kdpPrintCost"]
    pages = m["pages"]
    L: list[str] = []
    a = L.append

    a("# BOOK STATS — The Great Book of World Games")
    a("")
    a("<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/update_docs.py · ELLE DÜZENLEMEYİN -->")
    a("")
    a("> Kapı: `%s` · Buradaki her sayı **ölçülmüştür**." % m["gate"])
    a("> Yeniden üretmek için: `./04_BUILD/update_docs.py`")
    a("")
    a("## 1. Tek bakışta")
    a("")
    a("| | Ölçülen | Hedef | |")
    a("|---|---:|---:|---|")
    a("| Envanter kaydı | **%d** | — | |" % m["records"])
    a("| Aday oyun | **%d** | ≥%d | %s |"
      % (m["candidates"], scope["gamesCandidateMin"], bar(m["candidates"], scope["gamesCandidateMin"])))
    a("| Yayımlanabilir aday | **%d** | — | |" % m["publishable"])
    a("| Üretime hazır kural | **%d** | — | |" % m["productionReady"])
    a("| Kilitli oyun | **%d** | %d | %s |"
      % (m["locked"], scope["games"], bar(m["locked"], scope["games"])))
    a("| Yazılmış oyun | **%d** | %d | %s |"
      % (m["written"], scope["games"], bar(m["written"], scope["games"])))
    a("| Oynanabilirlik testi geçen | **%d** | %d | %s |"
      % (m["playtestsPassed"], scope["games"], bar(m["playtestsPassed"], scope["games"])))
    a("| Kültür | **%d** | ≥%d | %s |"
      % (m["cultures"], scope["cultures"], bar(m["cultures"], scope["cultures"])))
    a("| Bölge | **%d** | — | |" % m["regions"])
    a("| Aile | **%d** | %d | |" % (len(m["families"]), scope["families"]))
    a("| Kısıt taraması | **%d/%d** | %d/%d | %s |"
      % (m["screened"], m["records"], m["records"], m["records"],
         bar(m["screened"], max(1, m["records"]))))
    a("| Görsel gerektiren madde | **%d** | — | |" % m["needVisual"])
    a("")
    a("## 2. Kural bütünlüğü ve kısıt taraması")
    a("")
    a("| Oynanabilirlik durumu | Sayı | | Kısıt durumu | Sayı |")
    a("|---|---:|---|---|---:|")
    a("| `rules-complete` | %d | | `open` | %d |"
      % (m["play_rules-complete"], m["restriction_open"]))
    a("| `reconstructed` | %d | | `attributed` | %d |"
      % (m["play_reconstructed"], m["restriction_attributed"]))
    a("| `unresolved` | %d | | `restricted` | %d |"
      % (m["play_unresolved"], m["restriction_restricted"]))
    a("| `not-production-ready` | %d | | `excluded` | %d |"
      % (m["play_not-production-ready"], m["restriction_excluded"]))
    a("| `excluded` | %d | | — | — |" % m["play_excluded"])
    a("")
    a("## 3. Sayfa ve fiyat modeli")
    a("")
    pm = prod["pageModel"]
    if not pm.get("calibrated"):
        a("> ⚠ Model **HENÜZ KALİBRE EDİLMEDİ**. Aşağıdaki her sayı bir")
        a("> hipotezdir; gerçek dizgi ölçümü **%s** fazında yapılır."
          % pm.get("calibratedAtPhase", "phase2"))
        a("")
    a("| | |")
    a("|---|---:|")
    a("| Oyun başına faturalanan sayfa | %d |" % pm["pagesPerGame"])
    a("| Gövde | %d |" % (scope["games"] * pm["pagesPerGame"]))
    a("| Aile açılışları | %d |" % (scope["families"] * pm["familyOpenerPages"]))
    a("| Ön madde | %d |" % pm["frontMatterPages"])
    a("| Arka madde | %d |" % pm["backMatterPages"])
    a("| **Modelin sayfa sayısı** | **%d** |" % pages)
    a("| Yol haritası hedefi | %d |" % scope["pageTarget"])
    a("| Sapma | %+.1f%% |" % ((pages - scope["pageTarget"]) / scope["pageTarget"] * 100))
    a("")
    a("## 4. Sürümler")
    a("")
    a("| Sürüm | Durum | Liste | Baskı | Telif | Başabaş ACOS |")
    a("|---|---|---:|---:|---:|---:|")
    for ed in prod["editionsHypothesis"]:
        eid, lst = ed["id"], ed.get("list")
        if not ed.get("enabled") or lst is None:
            a("| %s | devre dışı | — | — | — | — |" % eid)
            continue
        if eid in ("paperback", "hardcover"):
            band = pc["paperbackLargeTrimBW"] if eid == "paperback" else pc["hardcoverLargeTrimBW"]
            cost = band["fixed"] + pages * band["perPage"]
            rate = pc["royaltyRateAtOrAbove999"] if lst >= 9.99 else pc["royaltyRateBelow999"]
        else:
            cost = pc["kindleDeliveryPerMB"] * pc["kindleFileSizeMBHypothesis"]
            rate = pc["kindleRoyaltyRate70"]
        roy = lst * rate - cost
        a("| %s | hipotez | %.2f $ | %.2f $ | **%.2f $** | %%%.1f |"
          % (eid, lst, cost, roy, roy / lst * 100))
    a("")
    a("## 5. Aile dağılımı")
    a("")
    a("| Aile | Aday | Taban | Hedef | |")
    a("|---|---:|---:|---:|---|")
    for f in sorted(m["families"], key=lambda f: f.get("order", 99)):
        n = m["familyCounts"].get(f["id"], 0)
        a("| %s | **%d** | %d | %d | %s |"
          % (f["en"], n, f.get("candidateFloor", 0), f.get("targetGames", 0),
             bar(n, f.get("candidateFloor", 1), 12)))
    a("")
    return "\n".join(L) + "\n"


def render_progress(m: dict) -> str:
    scope = m["cfg"]["scope"]
    gate = m["gate"]
    gi = GATE_ORDER.index(gate) if gate in GATE_ORDER else 0
    L: list[str] = []
    a = L.append

    a("# ROADMAP PROGRESS — The Great Book of World Games")
    a("")
    a("<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/update_docs.py · ELLE DÜZENLEMEYİN -->")
    a("")
    a("> Kapı: `%s` · Buradaki her sayı **ölçülmüştür**." % gate)
    a("")
    a("---")
    a("")
    a("## Faz durumu")
    a("")
    a("| Faz | Ad | Durum | Kapı | Dal | Etiket |")
    a("|---|---|---|---|---|---|")
    for i, (num, name, g, branch, tag) in enumerate(PHASES):
        if i < gi:
            state = "✅ **TAMAM**"
        elif i == gi:
            state = "✅ **TAMAM**" if i == 0 and gi == 0 else "🟢 **AÇIK**"
        elif i == gi + 1:
            state = "⏭ sıradaki"
        else:
            state = "⏸ beklemede"
        a("| **%s** | %s | %s | `%s` | `%s` | %s |"
          % (num, name, state, g, branch, tag))
    a("")
    a("---")
    a("")
    a("## Ölçülen ilerleme")
    a("")
    a("| | Ölçülen | Hedef |")
    a("|---|---:|---:|")
    a("| Envanter kaydı | **%d** | — |" % m["records"])
    a("| Aday oyun | **%d** | ≥%d |" % (m["candidates"], scope["gamesCandidateMin"]))
    a("| Üretime hazır kural | **%d** | — |" % m["productionReady"])
    a("| Kilitli oyun | **%d** | %d |" % (m["locked"], scope["games"]))
    a("| Yazılmış oyun | **%d** | %d |" % (m["written"], scope["games"]))
    a("| Oynanabilirlik testi geçen | **%d** | %d |"
      % (m["playtestsPassed"], scope["games"]))
    a("| Kültür | **%d** | ≥%d |" % (m["cultures"], scope["cultures"]))
    a("| Aile | **%d** | %d |" % (len(m["families"]), scope["families"]))
    a("| Kısıt taraması | **%d/%d** | %d/%d |"
      % (m["screened"], m["records"], m["records"], m["records"]))
    a("| Modellenen sayfa | **%d** | %d |" % (m["pages"], scope["pageTarget"]))
    a("")
    a("---")
    a("")
    a("## Sonraki izinli eylem")
    a("")
    if gi + 1 < len(PHASES):
        nxt = PHASES[gi + 1]
        a("> **Faz %s — %s**" % (nxt[0], nxt[1]))
        a(">")
        a("> Dal: `%s` · Kapı: `%s` · Etiket: %s" % (nxt[3], nxt[2], nxt[4]))
        a(">")
        a("> ⛔ Kurucu onayı olmadan başlamaz. Açık kararlar için")
        a("> [`DECISIONS.md`](DECISIONS.md) § AÇIK KARARLAR.")
    else:
        a("> **PROJE TAMAMLANDI.** Sonraki adım kurucunundur.")
    a("")
    return "\n".join(L) + "\n"


TARGETS = [("BOOK_STATS.md", render_stats), ("ROADMAP_PROGRESS.md", render_progress)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  ÜRETİLEN BELGELER%s" % ("  ·  --check" if args.check else ""))
    print("=" * 74)

    try:
        m = measure(root)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print("  ⛔ ölçüm yapılamadı: %s" % exc)
        return 1

    stale: list[str] = []
    for name, render in TARGETS:
        path = os.path.join(root, name)
        text = render(m)
        if args.check:
            current = ""
            if os.path.exists(path):
                with open(path, encoding="utf-8") as fh:
                    current = fh.read()
            if current != text:
                stale.append(name)
                print("  ✗ BAYAT: %s" % name)
            elif args.verbose:
                print("  ✓ güncel: %s" % name)
        else:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            print("  ✓ üretildi: %s" % name)

    print("\n" + "=" * 74)
    if stale:
        print("  ⛔ %d ÜRETİLEN BELGE BAYAT" % len(stale))
        print("     düzeltme: ./04_BUILD/update_docs.py")
        print("=" * 74)
        return 1
    print("  ✅ üretilen belgeler güncel")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
