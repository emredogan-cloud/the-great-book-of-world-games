#!/usr/bin/env python3
"""
MANUSCRIPT KAPISI — The Great Book of World Games
================================================================================
Ticari manuscript'in KENDİSİNİ denetler. Diğer kapılar veri katmanına
(`01_SOURCE/`) bakar; bu kapı prozanın yazıldığı katmana bakar.

  ⚠ MANUSCRIPT BU DEPODA YOKTUR (A1 · K12). Dosya yoksa kapı BOŞ KOŞAR ve
  0 döner — bu bir muafiyet değil bir olgudur. Körlüğü `selftest.py`
  kapatır: kasıtlı kusurlu manuscript kurguları her koşuda sınanır.

Denetlenen:
  ① BEŞ ÖĞE       — kurulum · ilk hamle · yasal hamleler · hedef · bitiş
  ② ÜÇ SORU       — berabere · kilit · kural dışı, üçü de cevaplı
  ③ BEYAN         — `reconstructed` madde `reconstructionNotice` taşır ve
                    envanterin beyanıyla İKİ YÖNLÜ uyuşur
  ④ KAYNAK        — her maddenin künyesi var; locator taşıyan her künye
                    `verified` bir doğrulama kaydına dayanıyor
  ⑤ DIŞ TEST      — hiçbir madde kaydı olmayan bir dış test iddia etmiyor
  ⑥ ÖLÇÜLEN BLOK  — manuscript'teki her kural bloğu sayfa ölçümünde SAYILIYOR
  ⑦ DİL           — ticari katmanda `translatedFrom` boş (K16)
  ⑧ KAPSAM        — yazılmış her madde KİLİTLİ 100'ün içinde (Faz 5 · K23)

⑧ NEDEN VAR: Faz 5'in kapsam değişikliği iki maddeyi (fivestones · marbles)
kapsamdan ÇIKARDI. İkisi de yazılmıştı ve manuscript'te duruyordu; bu kapı
onları GÖRMEDİ ve yeşil koştu. Yani kitap, kapsamda olmayan bir oyunu
basmaya devam edebiliyordu ve hiçbir mekanizma itiraz etmiyordu. Kurucunun
§ 32 listesindeki *"removed game remains in final scope"* kusuru tam olarak
budur ve artık mekanik olarak yakalanıyor.

⑥ NEDEN VAR: `calibrate_pages.py` ölçtüğü blokların listesini elle taşır.
Yeni bir blok yazılır ve listeye eklenmezse madde OLDUĞUNDAN KISA ölçülür,
sayfa modeli sessizce küçülür ve sayfa modeli bu kitabın fiyat modelidir.
Faz 3 üç blok, Faz 4 üç blok daha ekledi; ikisinde de listeyi güncellemeyi
hatırlamak DİSİPLİNE bağlıydı. Artık mekanizmaya bağlı.

Çıkış kodları:  0 = geçti (ya da manuscript yok)   1 = kapı kırmızı
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

# ① Beş öğe. "İlk hamle" ve "yasal hamleler" birden çok blokla karşılanabilir:
# bir zar oyununda ilk hamle `throwValues`, bir tahta oyununda `turnSequence`
# içinde yaşar. Kapı BLOK ADI değil ÖĞE arar.
MOVE_BLOCKS = ("turnSequence", "movement", "legalMoves", "throwValues",
               "capture", "stages", "figures", "placement", "chain",
               "stackingAndSending", "scoring")
EDGE_KEYS = ("tie", "stalemate", "illegalMove")
VALIDATION_KEYS = ("source", "rules", "playability", "clarity", "terminology",
                   "cultural", "diagram")


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
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


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def brief(items, n: int = 5) -> str:
    if not items:
        return ""
    more = "" if len(items) <= n else " … (+%d)" % (len(items) - n)
    return " — %s%s" % (", ".join(str(i) for i in items[:n]), more)


def measured_block_keys(root: str) -> set:
    """`calibrate_pages.py`nin GERÇEKTEN ölçtüğü blok adları.

    Kaynağı okur, bir listeyi ikinci kez yazmaz: iki liste ayrışırsa denetim
    denetlediğini sanıp başka bir şeyi denetler."""
    p = os.path.join(root, "04_BUILD", "calibrate_pages.py")
    if not os.path.exists(p):
        return set()
    src = open(p, encoding="utf-8").read()
    keys = set()
    for m in re.finditer(r'\(\s*"[^"]+"\s*,\s*"([a-zA-Z]+)"\s*\)', src):
        keys.add(m.group(1))
    return keys


def run(root: str, args) -> int:
    rep = Report(args.verbose)
    cfg = load(os.path.join(root, "project_config.json"))
    mpath = os.path.join(root, cfg["language"]["commercialManuscriptDir"],
                         "book.json")
    if not os.path.exists(mpath):
        print("  · ticari manuscript bu depoda yok — kapı BOŞ KOŞAR "
              "(CI'da beklenen; körlüğü selftest kapatır)")
        return 0

    book = load(mpath)
    games = book.get("games", [])
    rep.check(bool(games), "manuscript en az bir madde taşıyor")

    inv = {}
    ip = os.path.join(root, "01_SOURCE", "game_index.json")
    if os.path.exists(ip):
        inv = {g["gameId"]: g for g in load(ip)["games"]}

    verified = set()
    vp = os.path.join(root, "01_SOURCE", "source_verification.json")
    if os.path.exists(vp):
        verified = {r["gameId"] for r in load(vp)["records"]
                    if r["status"] == "verified"}

    # ⑧ KİLİTLİ KAPSAM. Boşsa denetim boş koşar (kilit henüz yazılmamış
    # olabilir); doluysa manuscript ondan TAŞAMAZ.
    scoped: set = set()
    sp = os.path.join(root, "01_SOURCE", "scope_lock.json")
    if os.path.exists(sp):
        scoped = {e["gameId"] for e in load(sp).get("entries", [])}

    playtested = set()
    pdir = os.path.join(root, "01_SOURCE", "playtests")
    if os.path.isdir(pdir):
        for fn in os.listdir(pdir):
            if fn.endswith(".json"):
                try:
                    playtested.add(load(os.path.join(pdir, fn))["gameId"])
                except Exception:  # noqa
                    pass

    dup = [g["gameId"] for g in games
           if [x["gameId"] for x in games].count(g["gameId"]) > 1]
    rep.check(not dup, "manuscript'te yinelenen madde yok" + brief(sorted(set(dup))))

    no_setup, no_move, no_obj, no_end = [], [], [], []
    no_edge, no_recon, recon_mismatch = [], [], []
    no_source, ghost_source, fake_test, translated, no_valid = [], [], [], [], []
    out_of_scope: list = []
    used_blocks = set()

    for g in games:
        gid = g.get("gameId", "?")
        if not g.get("setup"):
            no_setup.append(gid)
        if not any(g.get(k) for k in MOVE_BLOCKS):
            no_move.append(gid)
        if not (g.get("winCondition") or "").strip():
            no_obj.append(gid)
        if not (g.get("endCondition") or "").strip():
            no_end.append(gid)

        edges = g.get("edgeCases") or {}
        if not all((edges.get(k) or "").strip() for k in EDGE_KEYS):
            no_edge.append(gid)

        # ③ BEYAN — iki yönlü, qa_diagram ⑥ ile aynı disiplin.
        claims = bool(g.get("reconstructed"))
        if claims and not (g.get("reconstructionNotice") or "").strip():
            no_recon.append(gid)
        idx_recon = inv.get(gid, {}).get("playabilityStatus") == "reconstructed"
        if idx_recon and not claims:
            recon_mismatch.append("%s: envanter 'reconstructed', madde DEMİYOR" % gid)
        if claims and gid in inv and not idx_recon:
            recon_mismatch.append("%s: madde 'reconstructed', envanter DEMİYOR" % gid)

        # ④ KAYNAK
        srcs = g.get("sources") or []
        if not srcs:
            no_source.append(gid)
        elif re.search(r"\bpp?\.\s*\d|\bss\.\s*\d", " ".join(srcs)) \
                and gid not in verified:
            ghost_source.append(gid)

        # ⑤ DIŞ TEST — bir maddenin kendi kendini onaylaması imkânsız olmalı.
        st = "%s %s" % (g.get("status", ""), g.get("statusNote", ""))
        if (g.get("externalPlaytest") == "passed" or g.get("status") == "locked") \
                and gid not in playtested:
            fake_test.append(gid)
        del st

        if g.get("translatedFrom"):
            translated.append(gid)

        v = g.get("englishValidation") or {}
        if not all((v.get(k) or "").strip() for k in VALIDATION_KEYS):
            no_valid.append(gid)

        # ⑧ KAPSAM — kapsamdan çıkarılmış bir oyun basılmaya devam edemez.
        if scoped and gid not in scoped:
            out_of_scope.append(gid)

        for k in MOVE_BLOCKS:
            if g.get(k):
                used_blocks.add(k)

    print("\n── ① beş öğe ──")
    rep.check(not no_setup, "her maddede kurulum var" + brief(no_setup))
    rep.check(not no_move, "her maddede en az bir hamle bloğu var" + brief(no_move))
    rep.check(not no_obj, "her maddede hedef (winCondition) var" + brief(no_obj))
    rep.check(not no_end, "her maddede BİTİŞ KOŞULU var" + brief(no_end))

    print("\n── ② üç soru ──")
    rep.check(not no_edge,
              "her maddede berabere · kilit · kural dışı cevaplı" + brief(no_edge))

    print("\n── ③ yeniden kurgulama beyanı ──")
    rep.check(not no_recon,
              "beyansız yeniden kurgulanmış madde yok" + brief(no_recon))
    rep.check(not recon_mismatch,
              "madde ile envanterin beyanı uyuşuyor" + brief(recon_mismatch))

    print("\n── ④ kaynak ──")
    rep.check(not no_source, "her madde künye taşıyor" + brief(no_source))
    rep.check(not ghost_source,
              "sayfa numarası veren her madde DOĞRULANMIŞ bir kayda dayanıyor"
              + brief(ghost_source))

    print("\n── ⑤ dış test ──")
    rep.check(not fake_test,
              "kaydı olmayan dış test iddia eden madde yok" + brief(fake_test))

    print("\n── ⑥ ölçülen bloklar ──")
    measured = measured_block_keys(root)
    unmeasured = sorted(used_blocks - measured) if measured else []
    rep.check(not unmeasured,
              "manuscript'teki her kural bloğu sayfa ölçümünde SAYILIYOR"
              + brief(unmeasured))

    print("\n── ⑦ dil ──")
    rep.check(not translated,
              "hiçbir ticari madde çeviri beyanı taşımıyor (K16)" + brief(translated))
    rep.check(not no_valid,
              "her madde yedi başlıkta doğrulama kaydı taşıyor" + brief(no_valid))

    print("\n── ⑧ kapsam ──")
    if scoped:
        rep.check(not out_of_scope,
                  "yazılmış her madde KİLİTLİ 100'ün içinde (%d kilitli)"
                  % len(scoped) +
                  ("" if not out_of_scope
                   else " — KAPSAM DIŞI BASILIYOR:" + brief(out_of_scope)))
    else:
        print("  · kapsam kilidi yok — bu bölüm boş koşar")

    rep.facts = {
        "games": len(games),
        "outOfScope": sorted(out_of_scope),
        "scopeLocked": len(scoped),
        "blocksUsed": sorted(used_blocks),
        "blocksMeasured": sorted(measured),
        "withDiagrams": sum(1 for g in games if g.get("diagrams")),
        "withoutDiagrams": sum(1 for g in games if not g.get("diagrams")),
        "reconstructed": sum(1 for g in games if g.get("reconstructed")),
        "externalPlaytests": len(playtested),
    }
    return 1 if rep.errors else 0, rep


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    print("=" * 74)
    print("  MANUSCRIPT KAPISI")
    print("=" * 74)
    out = run(root, args)
    if isinstance(out, int):          # manuscript yok — boş koştu
        print("=" * 74)
        if args.json:
            os.makedirs(os.path.dirname(os.path.join(root, args.json)),
                        exist_ok=True)
            with open(os.path.join(root, args.json), "w", encoding="utf-8") as fh:
                json.dump({"status": "skipped",
                           "reason": "manuscript depoda yok"}, fh,
                          ensure_ascii=False, indent=2)
        return 0
    rc, rep = out
    print()
    if rc:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
    else:
        print("  ✅ %d denetim yeşil · %d madde · %d diyagramsız"
              % (rep.checks, rep.facts["games"], rep.facts["withoutDiagrams"]))
    print("=" * 74)
    if args.json:
        p = os.path.join(root, args.json)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump({"status": "fail" if rc else "pass",
                       "checks": rep.checks, "errors": rep.errors,
                       **rep.facts}, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
