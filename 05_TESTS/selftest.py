#!/usr/bin/env python3
"""
KAPILARIN KENDİ TESTİ — bu hattın EN ÖNEMLİ testi
================================================================================
Metin yokken yeşil kalan bir hat, KUSUR GELDİĞİNDE DE YEŞİL KALABİLİR.

Bu test o riski kapatır: her kapı için TAM BİR KUSUR taşıyan kurgu bir veri
seti çalıştırılır ve kapının o kusuru YAKALADIĞI kanıtlanır.

Bu projede özellikle kritiktir çünkü `validate_spec.py` bir kitabın kapsam
vaadini (100 oyun · 45 kültür · 7 aile) otomatik reddetme yetkisine sahiptir
ve o yetki, doğru çalıştığı KANITLANMADAN kullanılamaz.

Dört bölüm:
  ①  temiz kurgu BÜTÜN kapılardan geçer          (yanlış pozitif yok)
  ②  her kusurlu kurgu İLGİLİ kapıda yakalanır   (körlük yok)
  ③  kapı seviyeleri gerçekten kilitliyor        (kapsam kapıları)
  ④  her muafiyet en az bir kez DEVREYE GİRİYOR  (ölü kural yok)

④ doğrudan Bestiarium'un üç ölü kuralına ve World Myths'in K14 kararına
cevaptır: takip edilmeyen bir dosya için yazılmış muafiyet ÖLÜ MUAFİYETTİR
ve sessizce yanlış güven verir.

Çıkış kodları:  0 = geçti   1 = KÖRLÜK BULUNDU
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "04_BUILD")

VALIDATE_SPEC = os.path.join(BUILD, "validate_spec.py")
VALIDATE_STRUCTURE = os.path.join(BUILD, "validate_structure.py")
CONFIG = os.path.join(ROOT, "project_config.json")


# ---------------------------------------------------------------------------
# Kurgu üreteci — GERÇEK envanterden bağımsız, tam kontrollü veri
# ---------------------------------------------------------------------------
def clean_config() -> dict:
    with open(CONFIG, encoding="utf-8") as fh:
        return json.load(fh)


def clean_games(cfg: dict, n: int = 150, status: str = "candidate") -> dict:
    """Şemaya uyan, kusursuz kurgu envanter."""
    fams = [f["id"] for f in cfg["scope"]["familyTaxonomyHypothesis"]]
    games = []
    for i in range(n):
        games.append({
            "gameId": "fixture-%03d" % i,
            "name": "Fixture Game %03d" % i,
            "culture": "culture-%02d" % (i % 50),
            "region": "region-%d" % (i % 6),
            "family": fams[i % len(fams)],
            "status": status,
            "restrictionStatus": "open",
            "sourceConfidence": "high",
            "sources": [{"ref": "Source A %d" % i, "type": "book"},
                        {"ref": "Source B %d" % i, "type": "museum"}],
        })
    return {"games": games}


def run(script: str, *extra: str, gate: str | None = None,
        index: str | None = None) -> tuple[int, str]:
    cmd = [sys.executable, script, *extra]
    if gate:
        cmd += ["--gate", gate]
    env = dict(os.environ)
    if index:
        env["WORLDGAMES_GAME_INDEX"] = index
    out = subprocess.run(cmd, capture_output=True, text=True, env=env,
                         timeout=120, cwd=ROOT)
    return out.returncode, out.stdout + out.stderr


_RUN_SEQ = [0]


def run_spec_with(cfg: dict, games: dict | None, gate: str,
                  tmp: str) -> tuple[int, str]:
    """validate_spec'i kurgu dosyalarla koşturur.

    Betik yolları sabit okuduğu için kurgu bir PROJE KÖKÜ kurulur:
    gerçek depo asla değiştirilmez.

    ⚠ HER KOŞU KENDİ KÖKÜNÜ ALIR. Tek bir kök paylaşılırsa önceki testin
    yazdığı game_index.json sonraki testte HÂLÂ ORADA olur ve
    "envantersiz phase1 kırmızı yanmalı" testi sessizce anlamsızlaşır —
    yani testin kendisi kör olur. Bu kusur selftest'in ilk koşusunda
    yakalandı ve bu satır onun düzeltmesidir."""
    _RUN_SEQ[0] += 1
    fake_root = os.path.join(tmp, "root-%03d" % _RUN_SEQ[0])
    os.makedirs(os.path.join(fake_root, "01_SOURCE"), exist_ok=True)
    os.makedirs(os.path.join(fake_root, "04_BUILD"), exist_ok=True)

    with open(os.path.join(fake_root, "project_config.json"), "w",
              encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False)
    if games is not None:
        with open(os.path.join(fake_root, "01_SOURCE", "game_index.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(games, fh, ensure_ascii=False)
    with open(os.path.join(fake_root, ".gate"), "w", encoding="utf-8") as fh:
        fh.write(gate)

    # Betiği kurgu köke kopyala: ROOT'u kendi konumundan türetiyor.
    import shutil
    shutil.copy2(VALIDATE_SPEC, os.path.join(fake_root, "04_BUILD",
                                             "validate_spec.py"))
    out = subprocess.run(
        [sys.executable, os.path.join(fake_root, "04_BUILD", "validate_spec.py"),
         "--gate", gate],
        capture_output=True, text=True, timeout=120)
    return out.returncode, out.stdout + out.stderr


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.failed: list[str] = []
        self.passed = 0

    def check(self, ok: bool, label: str, detail: str = "") -> None:
        if ok:
            self.passed += 1
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.failed.append(label)
            print("  ✗ %s" % label)
            if detail:
                print("      %s" % detail.strip()[:400])


# ---------------------------------------------------------------------------
def part1_clean_passes(rep: Report, tmp: str) -> None:
    print("\n① temiz kurgu bütün kapılardan geçer (yanlış pozitif yok)")
    cfg = clean_config()
    games = clean_games(cfg, n=150)
    code, out = run_spec_with(cfg, games, "phase1", tmp)
    rep.check(code == 0, "temiz kurgu + phase1 → geçer", out)


def part2_flaws_caught(rep: Report, tmp: str) -> None:
    print("\n② her kusurlu kurgu ilgili kapıda yakalanır (körlük yok)")

    base = clean_config()

    # (a) yinelenen oyun kimliği
    cfg = copy.deepcopy(base)
    g = clean_games(cfg, n=150)
    g["games"][7]["gameId"] = g["games"][3]["gameId"]
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "yinelenen gameId YAKALANIR", out)

    # (b) tanımsız aile
    cfg = copy.deepcopy(base)
    g = clean_games(cfg, n=150)
    g["games"][11]["family"] = "uydurma-aile"
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "tanımsız aile YAKALANIR", out)

    # (c) kısıt taraması yapılmamış oyun
    cfg = copy.deepcopy(base)
    g = clean_games(cfg, n=150)
    del g["games"][20]["restrictionStatus"]
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "TARANMAMIŞ kısıt durumu YAKALANIR", out)

    # (d) geçersiz durum alanı
    cfg = copy.deepcopy(base)
    g = clean_games(cfg, n=150)
    g["games"][5]["status"] = "belki"
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "geçersiz status YAKALANIR", out)

    # (e) aile sayısı taksonomiyle çelişiyor
    cfg = copy.deepcopy(base)
    cfg["scope"]["families"] = 99
    code, out = run_spec_with(cfg, clean_games(base, 150), "phase1", tmp)
    rep.check(code != 0, "aile sayısı çelişkisi YAKALANIR", out)

    # (f) ekonomik olarak imkânsız fiyat → negatif telif
    cfg = copy.deepcopy(base)
    for ed in cfg["production"]["editionsHypothesis"]:
        if ed["id"] == "paperback":
            ed["list"] = 4.99          # 256 sayfa büyük trim: baskı 5,35 $
    code, out = run_spec_with(cfg, clean_games(base, 150), "phase1", tmp)
    rep.check(code != 0, "NEGATİF TELİF yakalanır (fiyat < baskı maliyeti)", out)

    # (g) Kindle %70 bandı dışında
    cfg = copy.deepcopy(base)
    for ed in cfg["production"]["editionsHypothesis"]:
        if ed["id"] == "kindle":
            ed["list"] = 19.99         # tavan 12,99 $
    code, out = run_spec_with(cfg, clean_games(base, 150), "phase1", tmp)
    rep.check(code != 0, "Kindle %70 bandı ihlali YAKALANIR", out)


def part3_gates_lock(rep: Report, tmp: str) -> None:
    print("\n③ kapı seviyeleri gerçekten kilitliyor")

    cfg = clean_config()

    # phase0: envanter yokken geçmeli (Faz 1 henüz üretmedi)
    code, out = run_spec_with(cfg, None, "phase0", tmp)
    rep.check(code == 0, "phase0 envantersiz geçer", out)

    # phase1: envanter yoksa KIRMIZI
    code, out = run_spec_with(cfg, None, "phase1", tmp)
    rep.check(code != 0, "phase1 envantersiz KIRMIZI", out)

    # phase1: 140'ın altında aday → KIRMIZI
    code, out = run_spec_with(cfg, clean_games(cfg, 100), "phase1", tmp)
    rep.check(code != 0, "phase1 yetersiz adayla KIRMIZI (100 < 140)", out)

    # phase2: 12 kilitli oyun yoksa KIRMIZI
    code, out = run_spec_with(cfg, clean_games(cfg, 150, "candidate"),
                              "phase2", tmp)
    rep.check(code != 0, "phase2 kilitli oyun olmadan KIRMIZI", out)

    # phase2: 12 kilitli + 12 yazılmış varsa geçer
    g = clean_games(cfg, 150, "candidate")
    for i in range(12):
        g["games"][i]["status"] = "written"
    code, out = run_spec_with(cfg, g, "phase2", tmp)
    rep.check(code == 0, "phase2 12 yazılmış oyunla geçer", out)

    # phase4: 100 yazılmış oyun yoksa KIRMIZI
    code, out = run_spec_with(cfg, g, "phase4", tmp)
    rep.check(code != 0, "phase4 eksik manuscript ile KIRMIZI", out)


def part4_no_dead_exemptions(rep: Report) -> None:
    print("\n④ her muafiyet en az bir kez devreye giriyor (ölü kural yok)")

    sys.path.insert(0, BUILD)
    import validate_structure as vs   # noqa: E402

    # Sızıntı taraması muafiyetleri: muaf tutulan dosya GERÇEKTEN VAR OLMALI.
    # Var olmayan bir dosya için yazılmış muafiyet ÖLÜ MUAFİYETTİR ve
    # sessizce yanlış güven verir (World Myths K14 · Bestiarium D28).
    for rel in sorted(vs.LEAK_SCAN_SKIP):
        rep.check(os.path.isfile(os.path.join(ROOT, rel)),
                  "sızıntı muafiyeti canlı: %s" % rel)

    for rel in sorted(vs.EMBED_SCAN_SKIP):
        rep.check(os.path.isfile(os.path.join(ROOT, rel)),
                  "gömülü-değer muafiyeti canlı: %s" % rel)

    # Muafiyet listesi gerçekten GEREKLİ mi: muaf dosya, muaf olmasaydı
    # yakalanacak mıydı? Değilse muafiyet gereksizdir ve kaldırılmalıdır.
    import re
    for rel in sorted(vs.LEAK_SCAN_SKIP):
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as fh:
            body = fh.read()
        hits = sum(1 for pat in vs.LEAK_MARKERS if re.search(pat, body))
        rep.check(hits >= vs.LEAK_MIN_HITS,
                  "muafiyet GEREKLİ (yoksa yakalanırdı): %s [%d işaret]"
                  % (rel, hits))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  KAPILARIN KENDİ TESTİ · The Great Book of World Games")
    print("=" * 74)

    rep = Report(args.verbose)
    with tempfile.TemporaryDirectory() as tmp:
        part1_clean_passes(rep, tmp)
        part2_flaws_caught(rep, tmp)
        part3_gates_lock(rep, tmp)
    part4_no_dead_exemptions(rep)

    print("\n" + "=" * 74)
    if rep.failed:
        print("  ⛔ %d KÖRLÜK BULUNDU (%d denetim geçti)"
              % (len(rep.failed), rep.passed))
        for f in rep.failed:
            print("     · %s" % f)
        print("=" * 74)
        print("\n  Bir kapı kusuru yakalamıyorsa, o kapı YOK demektir.")
        return 1
    print("  ✅ %d denetim yeşil — bütün kapılar ısırıyor" % rep.passed)
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
