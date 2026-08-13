#!/usr/bin/env python3
"""
OYNANABİLİRLİK KAPISI — The Great Book of World Games
================================================================================
`00_CONTEXT/PLAYABILITY_STANDARD.md` bir sözleşmedir; bu betik onun
mekanizmasıdır. Kitabın tek vaadi — *Ready to Play Tonight* — burada
denetlenir.

Denetlenen:
  ① KANIT TÜRÜ AYRIMI   — internal kanıt, external kanıtın yerine GEÇMEZ
  ② Kayıt bütünlüğü     — testçi kimliği · sürüm · süre · sonuç
  ③ KİŞİSEL VERİ        — testçiyi tanımlayan alan var mı
  ④ Yalnızca kitap metni — `usedOnlyBookText: false` kayıt GEÇERSİZDİR
  ⑤ Üç edge case        — berabere · kilit · kural dışı
  ⑥ locked kapısı       — her kilitli oyunun ≥1 GEÇMİŞ DIŞ testi var mı

── ① NEDEN EN ÖNEMLİ DENETİM ─────────────────────────────────────────────
Bir kural metnini yazan zihin, o metni okuyup ANLAMADIĞINI keşfedemez.
Ajanın, alt-ajanın ve doğrulayıcının ürettiği her şey `internal`dır ve bu
bir aşağılama değil bir TANIMDIR. Yalnızca `external` kayıt kapı sayılır.

İki tür aynı toplamda GÖSTERİLMEZ: "12 test yapıldı" cümlesi, onunun ajan
tarafından yapıldığı bir dünyada bir yalandır.

── SAHTE KAYIT ───────────────────────────────────────────────────────────
Bu kapı sahte bir kaydı metinden ayırt EDEMEZ ve bunu iddia etmez. Yaptığı
şey, sahte kaydı üretmeyi ZORLAŞTIRMAK ve kayıtsız ilerlemeyi İMKÂNSIZ
kılmaktır: test kaydı yoksa `locked` yoktur, ve `locked` yoksa kitap yoktur.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

REQUIRED_FIELDS = ("gameId", "testerId", "evidenceType", "testedVersion",
                   "language", "startedAt", "finishedAt", "playerCount",
                   "result", "usedOnlyBookText")
VALID_RESULTS = ("playable", "ambiguous", "unplayable")
REQUIRED_EDGE = ("tie", "stalemate", "illegalMove")
# Testçiyi tanımlayabilecek alanlar. Testçiyi korumak da bir kapıdır.
FORBIDDEN_PERSONAL = ("name", "surname", "fullName", "email", "phone",
                      "address", "birthDate", "age", "photo", "socialHandle",
                      "ip", "location")


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
        return bool(cond)

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def brief(items: list, n: int = 5) -> str:
    if not items:
        return ""
    more = "" if len(items) <= n else " … (+%d)" % (len(items) - n)
    return " — %s%s" % (", ".join(str(i) for i in items[:n]), more)


def collect(root: str, cfg: dict, rep: Report) -> list:
    d = os.path.join(root, cfg["playtest"]["recordDir"])
    if not os.path.isdir(d):
        return []
    out = []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".json"):
            continue
        try:
            data = load(os.path.join(d, fn))
        except json.JSONDecodeError as exc:
            rep.check(False, "test kaydı bozuk: %s — %s" % (fn, exc))
            continue
        recs = data.get("sessions", data) if isinstance(data, dict) else data
        for r in (recs if isinstance(recs, list) else []):
            r.setdefault("_file", fn)
            out.append(r)
    return out


def check_records(records: list, cfg: dict, rep: Report) -> None:
    pcfg = cfg["playtest"]
    print("\n── ①–⑤ test kayıtları (%d) ──" % len(records))

    ext = [r for r in records if r.get("evidenceType") == "external"]
    internal = [r for r in records if r.get("evidenceType") == "internal"]
    rep.facts["external"] = len(ext)
    rep.facts["internal"] = len(internal)
    print("  · DIŞ (insan) kanıt : %d" % len(ext))
    print("  · İÇ (ajan) kanıt   : %d" % len(internal))

    if not records:
        rep.warn("hiç test kaydı yok — dış test HENÜZ YAPILMADI. "
                 "Bu bir kusur değil bir DURUMDUR ve locked'ı bloklar.")
        return

    bad_type = [r.get("_file") for r in records
                if r.get("evidenceType") not in pcfg["evidenceTypes"]]
    rep.check(not bad_type, "her kaydın kanıt türü beyanlı" + brief(bad_type))

    incomplete, bad_result, bad_id, personal, notbook, no_edge = [], [], [], [], [], []
    pat = re.compile(pcfg["testerIdPattern"])
    for r in records:
        tag = "%s/%s" % (r.get("gameId", "?"), r.get("testerId", "?"))
        if [f for f in REQUIRED_FIELDS if f not in r]:
            incomplete.append(tag)
        if r.get("result") not in VALID_RESULTS:
            bad_result.append("%s → %s" % (tag, r.get("result")))
        if not pat.match(str(r.get("testerId", ""))):
            bad_id.append(tag)
        for f in FORBIDDEN_PERSONAL:
            if f in r:
                personal.append("%s → %s" % (tag, f))
        # ④ Yarım bilgiyle oynanan oyun KANIT DEĞİLDİR.
        if r.get("evidenceType") == "external" and r.get("usedOnlyBookText") is not True:
            notbook.append(tag)
        ec = r.get("edgeCasesSeen") or {}
        if r.get("result") == "playable" and \
                [k for k in REQUIRED_EDGE if k not in ec]:
            no_edge.append(tag)

    rep.check(not incomplete, "her kayıt zorunlu alanları taşıyor" + brief(incomplete))
    rep.check(not bad_result, "sonuç değerleri geçerli" + brief(bad_result))
    rep.check(not bad_id,
              "testçi kimlikleri anonim kalıba uyuyor (%s)" % pcfg["testerIdPattern"]
              + brief(bad_id))
    rep.check(not personal,
              "hiçbir kayıt kişisel veri taşımıyor" + brief(personal))
    rep.check(not notbook,
              "her DIŞ test yalnızca kitap metniyle yapılmış" + brief(notbook))
    rep.check(not no_edge,
              "'playable' her kayıt üç edge case'i de cevaplıyor" + brief(no_edge))

    # ② Ölçüm gerçekten yapılmış mı — süre ve oyuncu sayısı
    unmeasured = [("%s/%s" % (r.get("gameId"), r.get("testerId")))
                  for r in ext
                  if not r.get("startedAt") or not r.get("finishedAt")
                  or not isinstance(r.get("playerCount"), int)]
    rep.check(not unmeasured,
              "her dış testte süre ve oyuncu sayısı ÖLÇÜLMÜŞ" + brief(unmeasured))


def check_locked(root: str, records: list, cfg: dict, rep: Report) -> None:
    """⑥ locked kapısı — kanıtsız kilit yoktur."""
    idx = load(os.path.join(root, "01_SOURCE", "game_index.json"))
    games = idx.get("games", [])
    locked = [g for g in games if g.get("status") in ("locked", "written")]
    print("\n── ⑥ locked kapısı (%d kilitli oyun) ──" % len(locked))
    rep.facts["locked"] = len(locked)
    if not locked:
        print("  · kilitli oyun yok — kapı boş koşar (körlüğü selftest kapatır)")
        return

    minext = cfg["playtest"]["minExternalPlaytestsPerGame"]
    passed: dict = {}
    for r in records:
        if r.get("evidenceType") == "external" and r.get("result") == "playable" \
                and r.get("usedOnlyBookText") is True:
            passed[r["gameId"]] = passed.get(r["gameId"], 0) + 1

    thin = ["%s (%d/%d)" % (g["gameId"], passed.get(g["gameId"], 0), minext)
            for g in locked if passed.get(g["gameId"], 0) < minext]
    rep.check(not thin,
              "her kilitli oyunun ≥%d GEÇMİŞ DIŞ testi var" % minext + brief(thin))


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  OYNANABİLİRLİK — dış insan kanıtı")
    print("=" * 74)

    rep = Report(args.verbose)
    try:
        cfg = load(os.path.join(root, "project_config.json"))
    except (OSError, json.JSONDecodeError) as exc:
        print("  ⛔ project_config.json okunamadı: %s" % exc)
        return 1

    rep.check(cfg["playtest"]["externalRequiredForStatus"] == "locked",
              "dış test 'locked' için şart koşuluyor")
    rep.check(cfg["playtest"].get("fabricationIsProjectEndingOffence") is True,
              "sahte kayıt yapılandırmada iş bitiren ihlal olarak tanımlı")

    records = collect(root, cfg, rep)
    check_records(records, cfg, rep)
    check_locked(root, records, cfg, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
        for w in rep.warnings:
            print("     ! %s" % w)
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · dış kanıt %d · iç kanıt %d"
              % (rep.checks, rep.facts.get("external", 0),
                 rep.facts.get("internal", 0)))
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
