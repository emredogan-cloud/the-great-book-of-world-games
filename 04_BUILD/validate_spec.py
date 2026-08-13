#!/usr/bin/env python3
"""
VERİ BÜTÜNLÜĞÜ VE KAPSAM KAPISI — The Great Book of World Games
================================================================================
Bu kapı üç soruyu sorar:

  ① project_config.json kendi içinde tutarlı mı
  ② game_index.json şemaya uyuyor mu, kimlikler tekil mi
  ③ .gate seviyesinin GEREKTİRDİĞİ kapsam sağlanmış mı

Üçüncüsü kritiktir: `.gate` = phase2 ise 12 kilitli oyun ZORUNLUDUR.
Kapıyı yükseltip kapsamı sağlamamak sessizce geçemez.

TASARIM: yalnızca Python standart kütüphanesi. Üçüncü taraf paket YOK —
yazım fazlarında günde onlarca push olur ve iki dakikalık kurulum beklemek
disiplini öldürür. (World Myths kararı K7.)

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
GAME_INDEX = os.path.join(ROOT, "01_SOURCE", "game_index.json")
FAMILY_INDEX = os.path.join(ROOT, "01_SOURCE", "family_index.json")
GAME_SCHEMA = os.path.join(ROOT, "01_SOURCE", "game.schema.json")

VALID_GATES = ["phase0", "phase1", "phase2", "phase3", "phase4", "phase5", "release"]
VALID_STATUS = ["candidate", "researched", "locked", "written", "dropped"]
VALID_CONFIDENCE = ["high", "medium", "low", "reconstructed"]
VALID_RESTRICTION = ["open", "attributed", "restricted", "excluded"]


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.facts: dict = {}

    def ok(self, label: str) -> None:
        self.checks += 1
        if self.verbose:
            print("  ✓ %s" % label)

    def fail(self, label: str) -> None:
        self.checks += 1
        self.errors.append(label)
        print("  ✗ %s" % label)

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)

    def check(self, cond: bool, label: str) -> bool:
        if cond:
            self.ok(label)
        else:
            self.fail(label)
        return cond


def load_json(path: str, rep: Report, required: bool = True):
    if not os.path.exists(path):
        if required:
            rep.fail("dosya yok: %s" % os.path.relpath(path, ROOT))
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        rep.fail("JSON bozuk: %s — %s" % (os.path.relpath(path, ROOT), exc))
        return None


def read_gate() -> str:
    path = os.path.join(ROOT, ".gate")
    if not os.path.exists(path):
        return "phase0"
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip()


# ---------------------------------------------------------------------------
# JSON SCHEMA ALT KÜMESİ DOĞRULAYICI
# ---------------------------------------------------------------------------
# Karar K7 üçüncü taraf paket yasaklar; `jsonschema` kurulamaz. Bu yüzden
# şemanın KULLANDIĞIMIZ alt kümesi burada elle uygulanır:
#   type · required · properties · additionalProperties · enum · pattern
#   minLength · minItems · minimum · maximum · items
#
# Desteklenmeyen bir anahtar şemaya girerse SESSİZCE YOK SAYILIR ve bu,
# doğrulanmadığı hâlde doğrulanmış sanılan bir alan üretir. Bu riski
# kapatmak için `unsupported_keywords()` şemayı tarar ve bilinmeyen bir
# anahtar bulursa kapıyı kırmızı yakar.
SUPPORTED = {
    "$schema", "$id", "$comment", "title", "description", "type", "required",
    "properties", "additionalProperties", "enum", "pattern", "minLength",
    "minItems", "minimum", "maximum", "items", "format",
}
TYPES = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "integer": int, "number": (int, float),
}


def unsupported_keywords(schema, path: str = "#") -> list[str]:
    found: list[str] = []
    if isinstance(schema, dict):
        for k, v in schema.items():
            if k in ("properties", "items"):
                if k == "properties" and isinstance(v, dict):
                    for pk, pv in v.items():
                        found += unsupported_keywords(pv, "%s/%s" % (path, pk))
                elif k == "items":
                    found += unsupported_keywords(v, path + "/items")
                continue
            if k not in SUPPORTED:
                found.append("%s → %s" % (path, k))
    return found


def validate_node(value, schema: dict, path: str) -> list[str]:
    errs: list[str] = []
    t = schema.get("type")
    if t:
        py = TYPES.get(t)
        # JSON'da bool int'in alt tipidir; integer beklenen yerde True geçmemeli.
        if py is None:
            pass
        elif t == "integer" and isinstance(value, bool):
            errs.append("%s: integer bekleniyor, boolean geldi" % path)
            return errs
        elif not isinstance(value, py):
            errs.append("%s: %s bekleniyor, %s geldi"
                        % (path, t, type(value).__name__))
            return errs

    if "enum" in schema and value not in schema["enum"]:
        errs.append("%s: '%s' izinli değerler dışında" % (path, value))
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errs.append("%s: en az %d karakter olmalı" % (path, schema["minLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errs.append("%s: '%s' kalıba uymuyor" % (path, value))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append("%s: %s < %s" % (path, value, schema["minimum"]))
        if "maximum" in schema and value > schema["maximum"]:
            errs.append("%s: %s > %s" % (path, value, schema["maximum"]))
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append("%s: en az %d öğe olmalı" % (path, schema["minItems"]))
        if isinstance(schema.get("items"), dict):
            for i, item in enumerate(value):
                errs += validate_node(item, schema["items"], "%s[%d]" % (path, i))
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for req in schema.get("required", []):
            if req not in value:
                errs.append("%s: zorunlu alan eksik → %s" % (path, req))
        if schema.get("additionalProperties") is False:
            for k in value:
                if k not in props:
                    errs.append("%s: tanımsız alan → %s" % (path, k))
        for k, v in value.items():
            if k in props and isinstance(props[k], dict):
                errs += validate_node(v, props[k], "%s.%s" % (path, k))
    return errs


def check_schema(games, rep: Report) -> None:
    print("\n── şema uyumu ──")
    schema = load_json(GAME_SCHEMA, rep, required=False)
    if schema is None:
        rep.warn("game.schema.json yok — şema denetimi atlandı")
        return

    unsupported = unsupported_keywords(schema)
    rep.check(not unsupported,
              "şema yalnızca desteklenen anahtarları kullanıyor"
              + ("" if not unsupported else " — DOĞRULANMAYAN: %s" % unsupported[:5]))

    if games is None:
        return
    entries = games.get("games", []) if isinstance(games, dict) else games
    failures: list[str] = []
    for g in entries:
        errs = validate_node(g, schema, g.get("gameId", "?"))
        if errs:
            failures.extend(errs)
    rep.facts["schema_errors"] = len(failures)
    rep.check(not failures,
              "her oyun kaydı şemaya uyuyor (%d kayıt)" % len(entries)
              + ("" if not failures else " — %s" % failures[:5]))


# ---------------------------------------------------------------------------
def check_config(cfg: dict, rep: Report) -> None:
    print("\n── yapılandırma bütünlüğü ──")

    for key in ("project", "founder", "audience", "scope", "playability",
                "sourcing", "production", "gates", "style"):
        rep.check(key in cfg, "config bloğu var: %s" % key)

    scope = cfg.get("scope", {})
    fams = scope.get("familyTaxonomyHypothesis", [])
    rep.check(len(fams) == scope.get("families", -1),
              "aile sayısı taksonomiyle uyuşuyor (%d)" % len(fams))

    total = sum(f.get("targetGames", 0) for f in fams)
    games = scope.get("games", 0)
    # Aile hedefleri toplamı oyun hedefine yakın olmalı; tam eşitlik zorunlu değil
    # çünkü aile hedefleri Faz 1'de yeniden dengelenir.
    rep.check(abs(total - games) <= max(3, games * 0.05),
              "aile hedefleri toplamı (%d) oyun hedefine (%d) yakın" % (total, games))

    ids = [f.get("id") for f in fams]
    rep.check(len(ids) == len(set(ids)), "aile kimlikleri tekil")

    # Üretim ekonomisi: KDP formülünün kendisi burada doğrulanır.
    prod = cfg.get("production", {})
    pc = prod.get("kdpPrintCost", {})
    pages = scope.get("pageTarget", 0)
    for ed in prod.get("editionsHypothesis", []):
        if not ed.get("enabled") or ed.get("list") is None:
            continue
        eid, lst = ed["id"], ed["list"]
        if eid == "paperback":
            band = pc.get("paperbackLargeTrimBW", {})
        elif eid == "hardcover":
            band = pc.get("hardcoverLargeTrimBW", {})
        else:
            continue
        cost = band.get("fixed", 0) + pages * band.get("perPage", 0)
        rate = (pc.get("royaltyRateAtOrAbove999", 0.6) if lst >= 9.99
                else pc.get("royaltyRateBelow999", 0.5))
        royalty = lst * rate - cost
        rep.facts["royalty_%s" % eid] = round(royalty, 2)
        rep.facts["printcost_%s" % eid] = round(cost, 2)
        rep.check(royalty > 0,
                  "%s telifi pozitif: %.2f $ (baskı %.2f $ @ %d sayfa)"
                  % (eid, royalty, cost, pages))

    # Kindle %70 bandı
    for ed in prod.get("editionsHypothesis", []):
        if ed.get("id") == "kindle" and ed.get("enabled") and ed.get("list"):
            lo = pc.get("kindle70BandMin", 2.99)
            hi = pc.get("kindle70BandMax", 12.99)
            rep.check(lo <= ed["list"] <= hi,
                      "Kindle fiyatı %%70 bandında (%.2f–%.2f $)" % (lo, hi))

    fnd = cfg.get("founder", {})
    isbn = fnd.get("isbn", {})
    rep.check(isbn.get("strategy") in ("kdp-free", "own"),
              "ISBN stratejisi geçerli")


def check_games(cfg: dict, games, fams, gate: str, rep: Report) -> None:
    print("\n── oyun envanteri ──")

    if games is None:
        if gate == "phase0":
            rep.warn("game_index.json yok — phase0'da beklenen (Faz 1 üretir)")
            rep.facts["games_total"] = 0
            return
        rep.fail("game_index.json yok ama kapı %s" % gate)
        return

    entries = games.get("games", []) if isinstance(games, dict) else games
    rep.facts["games_total"] = len(entries)

    ids = [g.get("gameId") for g in entries]
    rep.check(len(ids) == len(set(ids)), "oyun kimlikleri tekil (%d)" % len(ids))
    rep.check(all(ids), "her oyunun gameId'si var")

    fam_ids = set()
    if fams:
        fam_entries = fams.get("families", []) if isinstance(fams, dict) else fams
        fam_ids = {f.get("id") for f in fam_entries}
    else:
        fam_ids = {f["id"] for f in cfg["scope"]["familyTaxonomyHypothesis"]}

    bad_family = [g["gameId"] for g in entries if g.get("family") not in fam_ids]
    rep.check(not bad_family,
              "her oyun tanımlı bir aileye ait" +
              ("" if not bad_family else " — ihlal: %s" % bad_family[:5]))

    bad_status = [g["gameId"] for g in entries
                  if g.get("status") not in VALID_STATUS]
    rep.check(not bad_status,
              "durum alanları geçerli" +
              ("" if not bad_status else " — ihlal: %s" % bad_status[:5]))

    bad_restr = [g["gameId"] for g in entries
                 if g.get("restrictionStatus") not in VALID_RESTRICTION]
    rep.check(not bad_restr,
              "kısıt taraması alanları geçerli" +
              ("" if not bad_restr else " — TARANMAMIŞ: %s" % bad_restr[:5]))

    cultures = {g.get("culture") for g in entries if g.get("culture")}
    rep.facts["cultures_total"] = len(cultures)

    for st in VALID_STATUS:
        rep.facts["games_%s" % st] = sum(1 for g in entries
                                         if g.get("status") == st)


def check_gate_scope(cfg: dict, gate: str, rep: Report) -> None:
    print("\n── kapı seviyesi kapsam denetimi (%s) ──" % gate)

    req = cfg.get("gates", {}).get("requirements", {}).get(gate)
    if req is None:
        rep.fail("kapı seviyesi config'de tanımsız: %s" % gate)
        return

    total = rep.facts.get("games_total", 0)
    locked = (rep.facts.get("games_locked", 0)
              + rep.facts.get("games_written", 0))
    written = rep.facts.get("games_written", 0)

    rep.check(total >= req["gamesCandidate"],
              "aday oyun ≥ %d (ölçülen %d)" % (req["gamesCandidate"], total))
    rep.check(locked >= req["gamesLocked"],
              "kilitli oyun ≥ %d (ölçülen %d)" % (req["gamesLocked"], locked))
    rep.check(written >= req["gamesWritten"],
              "yazılmış oyun ≥ %d (ölçülen %d)" % (req["gamesWritten"], written))

    if cfg["scope"].get("locked"):
        if gate in ("phase4", "phase5", "release"):
            rep.check(total >= cfg["scope"]["games"],
                      "kilitli kapsam sağlanıyor")
            rep.check(rep.facts.get("cultures_total", 0)
                      >= cfg["scope"]["cultures"],
                      "kültür sayısı alt başlığı doğruluyor (≥ %d)"
                      % cfg["scope"]["cultures"])


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None, help="kapı seviyesi (yoksa .gate okunur)")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None, help="rapor çıktısı")
    args = ap.parse_args()

    gate = args.gate or read_gate()
    if gate not in VALID_GATES:
        print("HATA: geçersiz kapı seviyesi: %s" % gate, file=sys.stderr)
        return 2

    print("=" * 74)
    print("  VERİ BÜTÜNLÜĞÜ VE KAPSAM · kapı: %s" % gate)
    print("=" * 74)

    rep = Report(args.verbose)

    cfg = load_json(CONFIG, rep)
    if cfg is None:
        print("\n⛔ project_config.json okunamadı — başka hiçbir şey denetlenemez")
        return 1

    check_config(cfg, rep)
    games = load_json(GAME_INDEX, rep, required=(gate != "phase0"))
    fams = load_json(FAMILY_INDEX, rep, required=False)
    check_schema(games, rep)
    check_games(cfg, games, fams, gate, rep)
    check_gate_scope(cfg, gate, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · kapı: %s" % (rep.checks, gate))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "gate": gate, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
