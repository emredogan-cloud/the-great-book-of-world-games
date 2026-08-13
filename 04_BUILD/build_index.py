#!/usr/bin/env python3
"""
ENVANTER BİRLEŞTİRİCİ — The Great Book of World Games
================================================================================
Yedi aile parçasını (01_SOURCE/games/family-*.json) tek bir envantere
(01_SOURCE/game_index.json) birleştirir.

NEDEN İKİ KATMAN:
  · Parçalar ELLE yazılır — 150 kayıt tek dosyada yönetilemez, çakışır, bozulur.
  · İndeks MAKİNEYLE üretilir — tek doğruluk kaynağı parçalardır.

`--check` ÜRETİLEN ARTEFAKT TUTARLILIĞINI denetler: diskteki indeks,
parçalardan şu anda üretilecek olanla BİREBİR aynı mı? Değilse biri elle
düzenlenmiş ya da yeniden üretilmeyi unutmuştur — ikisi de sessiz veri
kaymasıdır ve CI'ı kırmızı yakar.

  ./04_BUILD/build_index.py            # üret
  ./04_BUILD/build_index.py --check    # bayat mı

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

# --root ile değiştirilir. Bir kapı test edilemiyorsa kapı değildir:
# selftest bu betiği kurgu bir depo köküne karşı koşturur.
ROOT = DEFAULT_ROOT
SHARD_GLOB = FAMILY_INDEX = GAME_INDEX = ""


def set_root(root: str) -> None:
    global ROOT, SHARD_GLOB, GAME_INDEX, FAMILY_INDEX
    ROOT = os.path.abspath(root)
    SHARD_GLOB = os.path.join(ROOT, "01_SOURCE", "games", "family-*.json")
    GAME_INDEX = os.path.join(ROOT, "01_SOURCE", "game_index.json")
    FAMILY_INDEX = os.path.join(ROOT, "01_SOURCE", "family_index.json")


set_root(DEFAULT_ROOT)

HEADER = [
    "ÜRETİLMİŞ DOSYA — ELLE DÜZENLEMEYİN.",
    "Kaynak: 01_SOURCE/games/family-*.json",
    "Üretici: 04_BUILD/build_index.py",
    "Bu dosyayı elle değiştirirseniz build_index.py --check CI'ı kırmızı yakar.",
]


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def families_in_order() -> list[str]:
    """Aile sırası family_index.json'dan gelir; alfabetik değil EDİTORYAL sıradır."""
    fam = load(FAMILY_INDEX)
    return [f["id"] for f in sorted(fam["families"], key=lambda f: f.get("order", 99))]


def build() -> tuple[dict, list[str]]:
    problems: list[str] = []
    order = families_in_order()
    shards = sorted(glob.glob(SHARD_GLOB))
    if not shards:
        problems.append("hiç parça bulunamadı: 01_SOURCE/games/family-*.json")
        return {}, problems

    by_family: dict[str, list] = {}
    for path in shards:
        rel = os.path.relpath(path, ROOT)
        try:
            data = load(path)
        except json.JSONDecodeError as exc:
            problems.append("JSON bozuk: %s — %s" % (rel, exc))
            continue
        fam = data.get("family")
        if fam is None:
            problems.append("parçada 'family' alanı yok: %s" % rel)
            continue
        if fam not in order:
            problems.append("parça tanımsız aile taşıyor: %s → %s" % (rel, fam))
            continue
        if fam in by_family:
            problems.append("aynı aile iki parçada: %s" % fam)
            continue
        games = data.get("games", [])
        for g in games:
            # Parça dosyası ile kayıt AYNI aileyi söylemek zorundadır.
            if g.get("family") != fam:
                problems.append("kayıt yanlış parçada: %s (%s ≠ %s)"
                                % (g.get("gameId"), g.get("family"), fam))
        by_family[fam] = games

    missing = [f for f in order if f not in by_family]
    if missing:
        problems.append("parçası olmayan aile(ler): %s" % ", ".join(missing))

    merged: list = []
    for fam in order:
        # Aile içinde kimliğe göre sırala: sıralama deterministik olmalı ki
        # --check her makinede aynı sonucu versin.
        merged.extend(sorted(by_family.get(fam, []),
                             key=lambda g: g.get("gameId", "")))

    ids = [g.get("gameId") for g in merged]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        problems.append("yinelenen gameId: %s" % ", ".join(dupes))

    index = {"$comment": HEADER, "games": merged}
    return index, problems


def dump(index: dict) -> str:
    return json.dumps(index, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true",
                    help="üretmeden yalnızca bayatlık denetimi")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    set_root(args.root)

    print("=" * 74)
    print("  ENVANTER BİRLEŞTİRİCİ%s" % ("  ·  --check" if args.check else ""))
    print("=" * 74)

    index, problems = build()
    if problems:
        for p in problems:
            print("  ✗ %s" % p)
        print("\n  ⛔ parçalar birleştirilemedi")
        return 1

    text = dump(index)
    total = len(index["games"])

    if args.check:
        if not os.path.exists(GAME_INDEX):
            print("  ✗ game_index.json yok — build_index.py çalıştırın")
            return 1
        with open(GAME_INDEX, encoding="utf-8") as fh:
            current = fh.read()
        if current != text:
            print("  ✗ game_index.json BAYAT — parçalarla uyuşmuyor")
            print("     düzeltme: ./04_BUILD/build_index.py")
            return 1
        print("  ✅ game_index.json güncel · %d kayıt" % total)
    else:
        with open(GAME_INDEX, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("  ✅ game_index.json üretildi · %d kayıt" % total)

    if args.verbose:
        counts: dict[str, int] = {}
        for g in index["games"]:
            counts[g["family"]] = counts.get(g["family"], 0) + 1
        for fam in families_in_order():
            print("     %-12s %3d" % (fam, counts.get(fam, 0)))

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": "pass", "records": total},
                      fh, ensure_ascii=False, indent=2)
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
