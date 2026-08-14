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

Altı bölüm:
  ①  temiz kurgu BÜTÜN kapılardan geçer          (yanlış pozitif yok)
  ②  her kusurlu kurgu İLGİLİ kapıda yakalanır   (körlük yok)
  ③  kapı seviyeleri gerçekten kilitliyor        (kapsam kapıları)
  ④  her muafiyet en az bir kez DEVREYE GİRİYOR  (ölü kural yok)
  ⑤  FAZ 1 KAPILARI ISIRIYOR                     (Faz 1 kapılarının testi)
  ⑥  FAZ 2 KAPILARI ISIRIYOR                     (Faz 2 kapılarının testi)

④ doğrudan Bestiarium'un üç ölü kuralına ve World Myths'in K14 kararına
cevaptır: takip edilmeyen bir dosya için yazılmış muafiyet ÖLÜ MUAFİYETTİR
ve sessizce yanlış güven verir.

⑤ Faz 1'de doğan sekiz kapıyı denetler. Bu kapıların çoğu Faz 1 verisinde
BOŞ KOŞAR (kilitli oyun yok, oynanabilirlik testi yok) — yani gerçek veriyle
asla ısırmazlar. Körlükleri yalnızca burada kapanır.

⑥ Faz 2'nin kapıları için aynısı, ama DAHA SERT: Faz 2'nin koruma kapıları
tasarımı gereği depoda GÖREMEYECEKLERİ şeyleri korur. Manuscript depoda
yoktur, Türkçe pilot depoda yoktur, test kaydı yoktur, kilitli oyun yoktur.
Yani DÖRT kapı birden gerçek veriyle boş koşar ve dördü de yeşil yanar.
Bir korumanın çalıştığını, koruduğu şey ortada yokken kanıtlamanın tek yolu
budur: kasıtlı fikstürler ve saf fonksiyonlar.

Çıkış kodları:  0 = geçti   1 = KÖRLÜK BULUNDU
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "04_BUILD")

VALIDATE_SPEC = os.path.join(BUILD, "validate_spec.py")
CONFIG = os.path.join(ROOT, "project_config.json")
FAMILY_INDEX = os.path.join(ROOT, "01_SOURCE", "family_index.json")

RC_KNOWN = {"setup": "known", "play": "known", "turnLogic": "known",
            "objective": "known", "endCondition": "known",
            "verdict": "complete", "unknownElements": []}
CLARITY_OK = {"setupPerformable": True, "firstTurnTakeable": True,
              "legalMoveDistinguishable": True, "victoryDeterminable": True,
              "tieDefined": True, "terminationRisk": "finite"}
SCORES_OK = {"source": 4, "playability": 4, "cultural": 4, "access": 4,
             "distinct": 4, "explain": 4, "visual": 4, "play": 4}


# ---------------------------------------------------------------------------
# Kurgu üreteci — GERÇEK envanterden bağımsız, tam kontrollü veri
# ---------------------------------------------------------------------------
def clean_config() -> dict:
    with open(CONFIG, encoding="utf-8") as fh:
        return json.load(fh)


def clean_families() -> dict:
    with open(FAMILY_INDEX, encoding="utf-8") as fh:
        return json.load(fh)


def clean_games(cfg: dict, n: int = 150, status: str = "candidate") -> dict:
    """Şemaya ve BÜTÜN Faz 1 kapılarına uyan kusursuz kurgu envanter."""
    fams = [f["id"] for f in cfg["scope"]["familyTaxonomyHypothesis"]]
    games = []
    for i in range(n):
        games.append({
            "gameId": "fixture-%03d" % i,
            "name": "Fixture Game %03d" % i,
            "culture": "culture-%02d" % (i % 50),
            "region": "region-%d" % (i % 6),
            "period": "documented in the twentieth century",
            "family": fams[i % len(fams)],
            "taxonomyRationale": "Kurgu kayıt: ailenin giriş ölçütü karşılanır.",
            "status": status,
            "restrictionStatus": "open",
            "sourceConfidence": "high",
            "sourceVerification": "bibliographic",
            "sources": [
                {"ref": "Alpha %03d, A Fixture Monograph" % i, "type": "book"},
                {"ref": "Beta %03d, A Second Fixture Record" % i, "type": "museum"},
            ],
            "ruleCompleteness": dict(RC_KNOWN),
            "clarity": dict(CLARITY_OK),
            "playabilityStatus": "rules-complete",
            "players": {"min": 2, "max": 2},
            "durationMinutes": {"min": 10, "max": 20},
            "ageMinEstimate": 8,
            "materialsHint": ["a fixture board"],
            "childSuitable": True,
            "environment": "table",
            "visualNeeds": ["board-diagram"],
            "scores": dict(SCORES_OK),
            "unresolvedQuestions": [],
            "editorialStatus": "inventory",
            "playtestStatus": "not-started",
        })
    return {"games": games}


def clean_rules() -> dict:
    """Kusursuz bir kural bloğu — locked kurgularında kullanılır."""
    return {
        "objective": "Take every enemy piece.",
        "playerCountMin": 2,
        "playerCountMax": 2,
        "materials": ["a fixture board", "twelve pieces each"],
        "setup": "Place six pieces on each side of the fixture board.",
        "turnSequence": ["Move one piece one step.", "Remove any trapped piece."],
        "winCondition": "The player with pieces remaining wins.",
        "durationMinutes": 15,
        "ageMin": 8,
        "edgeCases": {"tie": "Equal pieces is a draw.",
                      "stalemate": "A player unable to move loses.",
                      "illegalMove": "Put the piece back and move again."},
        "simplifiedFirstGame": "Play with six pieces each instead of twelve.",
    }


def clean_playtest() -> dict:
    return {"date": "2026-09-01", "tester": "fixture tester",
            "usedOnlyBookText": True, "result": "playable", "playerCount": 2}


_RUN_SEQ = [0]


def make_root(tmp: str, cfg: dict, games, *, fams=None, gate: str = "phase1",
              shards=None, docs: bool = False) -> str:
    """Kurgu bir PROJE KÖKÜ kurar. Gerçek depo asla değiştirilmez.

    ⚠ HER KOŞU KENDİ KÖKÜNÜ ALIR. Tek bir kök paylaşılırsa önceki testin
    yazdığı game_index.json sonraki testte HÂLÂ ORADA olur ve
    'envantersiz phase1 kırmızı yanmalı' testi sessizce anlamsızlaşır —
    yani testin kendisi kör olur. Bu kusur selftest'in ilk koşusunda
    yakalandı ve bu satır onun düzeltmesidir."""
    _RUN_SEQ[0] += 1
    root = os.path.join(tmp, "root-%03d" % _RUN_SEQ[0])
    os.makedirs(os.path.join(root, "01_SOURCE", "games"), exist_ok=True)
    os.makedirs(os.path.join(root, "04_BUILD"), exist_ok=True)
    os.makedirs(os.path.join(root, "06_REPORTS"), exist_ok=True)

    write_json(os.path.join(root, "project_config.json"), cfg)
    write_json(os.path.join(root, "01_SOURCE", "family_index.json"),
               fams if fams is not None else clean_families())
    if games is not None:
        write_json(os.path.join(root, "01_SOURCE", "game_index.json"), games)
    if shards:
        for name, data in shards.items():
            write_json(os.path.join(root, "01_SOURCE", "games", name), data)
    with open(os.path.join(root, ".gate"), "w", encoding="utf-8") as fh:
        fh.write(gate)
    if docs:
        run_gate("update_docs.py", root)          # belgeleri güncel bırak
    return root


def write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def run_gate(script: str, root: str, *extra: str) -> tuple[int, str]:
    """Faz 1 kapılarını kurgu köke karşı koşturur (--root sözleşmesi)."""
    out = subprocess.run(
        [sys.executable, os.path.join(BUILD, script), "--root", root, *extra],
        capture_output=True, text=True, timeout=180)
    return out.returncode, out.stdout + out.stderr


def run_spec_with(cfg: dict, games, gate: str, tmp: str,
                  fams=None) -> tuple[int, str]:
    """validate_spec kendi konumundan ROOT türetir; kurgu köke KOPYALANIR."""
    root = make_root(tmp, cfg, games, fams=fams, gate=gate)
    shutil.copy2(VALIDATE_SPEC, os.path.join(root, "04_BUILD", "validate_spec.py"))
    schema = os.path.join(ROOT, "01_SOURCE", "game.schema.json")
    if os.path.exists(schema):
        shutil.copy2(schema, os.path.join(root, "01_SOURCE", "game.schema.json"))
    out = subprocess.run(
        [sys.executable, os.path.join(root, "04_BUILD", "validate_spec.py"),
         "--gate", gate], capture_output=True, text=True, timeout=120)
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
    rep.check(code == 0, "temiz kurgu + phase1 → validate_spec geçer", out)

    root = make_root(tmp, cfg, games)
    for script in ("qa_taxonomy.py", "qa_rules.py", "validate_research.py",
                   "score_candidates.py", "page_budget.py", "editions.py"):
        code, out = run_gate(script, root)
        rep.check(code == 0, "temiz kurgu → %s geçer" % script, out)


def part2_flaws_caught(rep: Report, tmp: str) -> None:
    print("\n② her kusurlu kurgu ilgili kapıda yakalanır (körlük yok)")

    base = clean_config()

    # (a) yinelenen oyun kimliği
    g = clean_games(base, n=150)
    g["games"][7]["gameId"] = g["games"][3]["gameId"]
    code, out = run_spec_with(base, g, "phase1", tmp)
    rep.check(code != 0, "yinelenen gameId YAKALANIR", out)

    # (b) tanımsız aile
    g = clean_games(base, n=150)
    g["games"][11]["family"] = "uydurma-aile"
    code, out = run_spec_with(base, g, "phase1", tmp)
    rep.check(code != 0, "tanımsız aile YAKALANIR", out)

    # (c) kısıt taraması yapılmamış oyun
    g = clean_games(base, n=150)
    del g["games"][20]["restrictionStatus"]
    code, out = run_spec_with(base, g, "phase1", tmp)
    rep.check(code != 0, "TARANMAMIŞ kısıt durumu YAKALANIR", out)

    # (d) geçersiz durum alanı
    g = clean_games(base, n=150)
    g["games"][5]["status"] = "belki"
    code, out = run_spec_with(base, g, "phase1", tmp)
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
            ed["list"] = 4.99          # 250 sayfa büyük trim: baskı 5,25 $
    code, out = run_spec_with(cfg, clean_games(base, 150), "phase1", tmp)
    rep.check(code != 0, "NEGATİF TELİF yakalanır (fiyat < baskı maliyeti)", out)

    # (g) Kindle %70 bandı dışında
    cfg = copy.deepcopy(base)
    for ed in cfg["production"]["editionsHypothesis"]:
        if ed["id"] == "kindle":
            ed["list"] = 19.99         # tavan 12,99 $
    code, out = run_spec_with(cfg, clean_games(base, 150), "phase1", tmp)
    rep.check(code != 0, "Kindle %70 bandı ihlali YAKALANIR", out)

    # ── ŞEMA DENETİMİ ──────────────────────────────────────────────────────
    # (h) zorunlu alan eksik
    g = clean_games(base, n=150)
    del g["games"][30]["period"]
    code, out = run_spec_with(base, g, "phase1", tmp)
    rep.check(code != 0, "şema: zorunlu alan eksikliği YAKALANIR", out)

    # (i) tanımsız alan (additionalProperties: false)
    g = clean_games(base, n=150)
    g["games"][31]["uydurmaAlan"] = "x"
    code, out = run_spec_with(base, g, "phase1", tmp)
    rep.check(code != 0, "şema: TANIMSIZ ALAN yakalanır", out)

    # (j) enum ihlali
    g = clean_games(base, n=150)
    g["games"][32]["sourceConfidence"] = "çok-yüksek"
    code, out = run_spec_with(base, g, "phase1", tmp)
    rep.check(code != 0, "şema: enum ihlali YAKALANIR", out)

    # (k) sayı aralığı ihlali
    g = clean_games(base, n=150)
    g["games"][33]["scores"]["source"] = 9
    code, out = run_spec_with(base, g, "phase1", tmp)
    rep.check(code != 0, "şema: aralık dışı puan YAKALANIR", out)


def part3_gates_lock(rep: Report, tmp: str) -> None:
    print("\n③ kapı seviyeleri gerçekten kilitliyor")

    cfg = clean_config()

    code, out = run_spec_with(cfg, None, "phase0", tmp)
    rep.check(code == 0, "phase0 envantersiz geçer", out)

    code, out = run_spec_with(cfg, None, "phase1", tmp)
    rep.check(code != 0, "phase1 envantersiz KIRMIZI", out)

    code, out = run_spec_with(cfg, clean_games(cfg, 100), "phase1", tmp)
    rep.check(code != 0, "phase1 yetersiz adayla KIRMIZI (100 < 140)", out)

    code, out = run_spec_with(cfg, clean_games(cfg, 150, "candidate"),
                              "phase2", tmp)
    rep.check(code != 0, "phase2 kilitli oyun olmadan KIRMIZI", out)

    g = clean_games(cfg, 150, "candidate")
    for i in range(12):
        g["games"][i]["status"] = "written"
    code, out = run_spec_with(cfg, g, "phase2", tmp)
    rep.check(code == 0, "phase2 12 yazılmış oyunla geçer", out)

    code, out = run_spec_with(cfg, g, "phase4", tmp)
    rep.check(code != 0, "phase4 eksik manuscript ile KIRMIZI", out)


def part4_no_dead_exemptions(rep: Report) -> None:
    print("\n④ her muafiyet en az bir kez devreye giriyor (ölü kural yok)")

    sys.path.insert(0, BUILD)
    import validate_structure as vs   # noqa: E402

    for rel in sorted(vs.LEAK_SCAN_SKIP):
        rep.check(os.path.isfile(os.path.join(ROOT, rel)),
                  "sızıntı muafiyeti canlı: %s" % rel)

    for rel in sorted(vs.EMBED_SCAN_SKIP):
        rep.check(os.path.isfile(os.path.join(ROOT, rel)),
                  "gömülü-değer muafiyeti canlı: %s" % rel)

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


# ---------------------------------------------------------------------------
def part5_phase1_gates(rep: Report, tmp: str) -> None:
    print("\n⑤ Faz 1 kapıları gerçekten ısırıyor")
    cfg = clean_config()

    def bite(label: str, mutate, script: str, *extra: str, cfg_mut=None,
             fams_mut=None) -> None:
        """Kurguyu boz, kapıyı koştur, KIRMIZI yanmasını bekle."""
        g = clean_games(cfg, 150)
        c = copy.deepcopy(cfg)
        f = clean_families()
        if mutate:
            mutate(g["games"])
        if cfg_mut:
            cfg_mut(c)
        if fams_mut:
            fams_mut(f)
        root = make_root(tmp, c, g, fams=f)
        code, out = run_gate(script, root, *extra)
        rep.check(code != 0, label, out)

    # ── qa_taxonomy.py ─────────────────────────────────────────────────────
    print("  ▸ qa_taxonomy")
    bite("tasnif gerekçesi eksikliği YAKALANIR",
         lambda gs: gs[4].__setitem__("taxonomyRationale", "kısa"),
         "qa_taxonomy.py")
    bite("gerekçesiz `restricted` YAKALANIR",
         lambda gs: gs[6].update({"restrictionStatus": "restricted",
                                  "editorialStatus": "rejected"}),
         "qa_taxonomy.py")
    bite("kitaba sızan `restricted` YAKALANIR (editoryal durum reddetmiyor)",
         lambda gs: gs[8].update({"restrictionStatus": "restricted",
                                  "restrictionNote": "yaşayan gelenek",
                                  "editorialStatus": "inventory"}),
         "qa_taxonomy.py")
    bite("tanımsız ikincil aile YAKALANIR",
         lambda gs: gs[9].__setitem__("secondaryFamily", "yok-boyle-aile"),
         "qa_taxonomy.py")
    bite("aile tabanının altına düşme YAKALANIR",
         lambda gs: [g.__setitem__("family", "sowing") for g in gs[:140]],
         "qa_taxonomy.py")
    bite("kültür çeşitliliği kaybı YAKALANIR",
         lambda gs: [g.__setitem__("culture", "tek-kultur") for g in gs],
         "qa_taxonomy.py")
    bite("komşusu tanımsız SINIR KURALI yakalanır", None, "qa_taxonomy.py",
         fams_mut=lambda f: f["families"][0]["boundaries"].append(
             {"vs": "yok-boyle-aile", "rule": "x"}))

    # ── qa_rules.py ────────────────────────────────────────────────────────
    print("  ▸ qa_rules")
    bite("KURGUSAL TAMAMLAMA yakalanır (unknown öğe + complete verdict)",
         lambda gs: gs[3]["ruleCompleteness"].update({"turnLogic": "unknown"}),
         "qa_rules.py")
    bite("gerekçesiz eksiklik YAKALANIR (partial ama unknownElements boş)",
         lambda gs: gs[3].update({
             "ruleCompleteness": dict(RC_KNOWN, endCondition="partial",
                                      verdict="partial", unknownElements=[]),
             "playabilityStatus": "unresolved"}),
         "qa_rules.py")
    bite("netlik testinden düşen `rules-complete` YAKALANIR",
         lambda gs: gs[5]["clarity"].__setitem__("tieDefined", False),
         "qa_rules.py")
    bite("BEYANSIZ yeniden kurgulama YAKALANIR (plan yok)",
         lambda gs: gs[7].update({"playabilityStatus": "reconstructed",
                                  "sourceConfidence": "reconstructed",
                                  "clarity": dict(CLARITY_OK, tieDefined=False)}),
         "qa_rules.py")
    bite("yersiz kurgulama planı YAKALANIR (ölü kural)",
         lambda gs: gs[7].__setitem__(
             "reconstructionPlan", "Bu kayıt yeniden kurgulanmadı ama plan taşıyor; "
             "bu bir ölü kuraldır ve kapı bunu reddetmelidir."),
         "qa_rules.py")
    bite("bitiş kuralsız DÖNGÜ RİSKİ yakalanır",
         lambda gs: gs[2]["clarity"].__setitem__("terminationRisk", "loop-possible"),
         "qa_rules.py")
    bite("durum ↔ bütünlük çelişkisi YAKALANIR",
         lambda gs: gs[1].__setitem__("playabilityStatus", "unresolved"),
         "qa_rules.py")
    bite("gerekçesiz `dropped` YAKALANIR",
         lambda gs: gs[10].__setitem__("status", "dropped"),
         "qa_rules.py")
    bite("sessiz yeniden kurgulama YAKALANIR (kaynak güveni söylemiyor)",
         lambda gs: gs[12].__setitem__("playabilityStatus", "reconstructed"),
         "qa_rules.py")

    def with_rules(gs, **over):
        r = clean_rules()
        r.update(over)
        gs[0].update({"rules": r, "status": "researched"})

    bite("eksik edge case YAKALANIR (berabere cevapsız)",
         lambda gs: with_rules(gs, edgeCases={"tie": "", "stalemate": "x",
                                              "illegalMove": "y"}),
         "qa_rules.py")
    bite("eksik zorunlu kural alanı YAKALANIR",
         lambda gs: with_rules(gs, setup=""),
         "qa_rules.py")
    bite("çok uzun kural adımı YAKALANIR",
         lambda gs: with_rules(gs, turnSequence=[" ".join(["word"] * 40)]),
         "qa_rules.py")
    bite("'ilk oyununuz' eksikliği YAKALANIR",
         lambda gs: with_rules(gs, simplifiedFirstGame=""),
         "qa_rules.py")
    bite("kural bloğu ↔ aday kaydı çelişkisi YAKALANIR",
         lambda gs: with_rules(gs, playerCountMax=6),
         "qa_rules.py")
    bite("geçersiz oyuncu aralığı YAKALANIR",
         lambda gs: with_rules(gs, playerCountMin=6, playerCountMax=2),
         "qa_rules.py")

    def locked(gs, **over):
        g = gs[0]
        g.update({"status": "locked", "rules": clean_rules(),
                  "sourceVerification": "page-verified",
                  "playtests": [dict(clean_playtest(), **over)]})
        for s in g["sources"]:
            s["locator"] = "s. 1"

    bite("TESTSİZ locked YAKALANIR",
         lambda gs: gs[0].update({"status": "locked", "rules": clean_rules(),
                                  "sourceVerification": "page-verified",
                                  "playtests": []}) or
                    [s.__setitem__("locator", "s. 1") for s in gs[0]["sources"]],
         "qa_rules.py")
    bite("GEÇERSİZ test YAKALANIR (kitap metni dışında bilgi kullanılmış)",
         lambda gs: locked(gs, usedOnlyBookText=False),
         "qa_rules.py")
    bite("BAŞARISIZ test ile locked YAKALANIR",
         lambda gs: locked(gs, result="unplayable"),
         "qa_rules.py")

    # ── validate_research.py ───────────────────────────────────────────────
    print("  ▸ validate_research")
    bite("wiki künyesi YAKALANIR",
         lambda gs: gs[0]["sources"].append(
             {"ref": "Wikipedia, entry on a fixture game", "type": "book"}),
         "validate_research.py")
    bite("LLM çıktısı künyesi YAKALANIR",
         lambda gs: gs[0]["sources"].append(
             {"ref": "ChatGPT session transcript, 2026", "type": "book"}),
         "validate_research.py")
    bite("geçersiz kaynak tipi YAKALANIR",
         lambda gs: gs[1]["sources"][0].__setitem__("type", "blog"),
         "validate_research.py")
    bite("anlamsız künye YAKALANIR",
         lambda gs: gs[2]["sources"][0].__setitem__("ref", "bkz."),
         "validate_research.py")
    bite("locatorsuz `page-verified` YAKALANIR",
         lambda gs: gs[3].__setitem__("sourceVerification", "page-verified"),
         "validate_research.py")
    bite("tek kaynakla 'high' güven YAKALANIR",
         lambda gs: gs[4].__setitem__("sources", [gs[4]["sources"][0]]),
         "validate_research.py")
    bite("AYNI YAZARIN iki eseri bağımsız sayılmaz (locked)",
         lambda gs: gs[5].update({
             "status": "locked", "sourceVerification": "page-verified",
             "sources": [{"ref": "Alpha, First Fixture Book", "type": "book",
                          "locator": "s. 12"},
                         {"ref": "Alpha, Second Fixture Book", "type": "book",
                          "locator": "s. 44"}]}),
         "validate_research.py")
    bite("türetilmiş kaynak bağımsız sayılmaz (lineage)",
         lambda gs: gs[6].update({
             "status": "locked", "sourceVerification": "page-verified",
             "sources": [{"ref": "Alpha, Fixture Monograph", "type": "book",
                          "locator": "s. 12"},
                         {"ref": "Gamma, A Digest of Alpha", "type": "book",
                          "locator": "s. 3", "lineage": "Alpha"}]}),
         "validate_research.py")
    bite("SAYFA DOĞRULAMASIZ locked YAKALANIR",
         lambda gs: gs[7].__setitem__("status", "locked"),
         "validate_research.py")
    bite("KISITLI oyunun kilitlenmesi YAKALANIR",
         lambda gs: gs[8].update({
             "status": "locked", "restrictionStatus": "restricted",
             "restrictionNote": "yaşayan gelenek",
             "editorialStatus": "rejected",
             "sourceVerification": "page-verified"}) or
             [s.__setitem__("locator", "s. 1") for s in gs[8]["sources"]],
         "validate_research.py")

    # ── score_candidates.py ────────────────────────────────────────────────
    print("  ▸ score_candidates")
    bite("puanlanmamış kayıt YAKALANIR",
         lambda gs: gs[0].pop("scores"),
         "score_candidates.py")
    bite("aralık dışı puan YAKALANIR",
         lambda gs: gs[1]["scores"].__setitem__("play", 0),
         "score_candidates.py")
    bite("kültür hedefinin altına düşme YAKALANIR",
         lambda gs: [g.__setitem__("culture", "tek-kultur") for g in gs],
         "score_candidates.py")

    # ── page_budget.py · editions.py ───────────────────────────────────────
    print("  ▸ page_budget · editions")
    # ⚠ BU FİKSTÜRLER FAZ 2'DE GÜNCELLENDİ VE GÜNCELLENMESİNİ SELFTEST
    # KENDİSİ İSTEDİ. page_budget artık kalibre edildiğinde `pagesPerGame`
    # hipotezini DEĞİL `measured.billedPagesPerGame` ölçümünü kullanıyor;
    # eski fikstür hipotezi bozuyordu ve model onu okumadığı için kapı
    # ısırmıyordu. Yani bir gerçek körlük doğdu ve selftest onu YAKALADI.
    # Ders: bir kapının girdisini değiştirmek, o kapının testini de
    # değiştirmeyi gerektirir — yoksa test başka bir şeyi denetler.
    def uncalibrated(c):
        """Kalibrasyonu kapat: model hipoteze döner."""
        c["production"]["pageModel"]["calibrated"] = False
        c["production"]["pageModel"].pop("acknowledgedDeviation", None)

    bite("sayfa modeli hedeften sapınca YAKALANIR (hipotez modu)",
         None, "page_budget.py",
         cfg_mut=lambda c: (uncalibrated(c),
                            c["production"]["pageModel"].__setitem__("pagesPerGame", 4)))
    bite("ÖLÇÜLMÜŞ sapma da YAKALANIR (kalibre mod)", None, "page_budget.py",
         cfg_mut=lambda c: (c["production"]["pageModel"].pop("acknowledgedDeviation", None),
                            c["production"]["pageModel"]["measured"].__setitem__(
                                "billedPagesPerGame", 4)))
    bite("EKSİK sapma şerhi YAKALANIR", None, "page_budget.py",
         cfg_mut=lambda c: (c["production"]["pageModel"]["measured"].__setitem__(
                                "billedPagesPerGame", 4),
                            c["production"]["pageModel"].__setitem__(
                                "acknowledgedDeviation",
                                {"date": "2026-08-13", "cause": "x",
                                 "measurement": "x", "effect": "x",
                                 "economicImplication": "x",
                                 "recommendedResponse": "x"})))
    bite("KDP sayfa sınırının aşılması YAKALANIR", None, "page_budget.py",
         cfg_mut=lambda c: (uncalibrated(c),
                            c["production"]["pageModel"].__setitem__("pagesPerGame", 9),
                            c["scope"].__setitem__("pageTarget", 950),
                            c["scope"].__setitem__("pageTolerancePct", 90)))
    bite("negatif telif YAKALANIR", None, "editions.py",
         cfg_mut=lambda c: [ed.__setitem__("list", 3.99)
                            for ed in c["production"]["editionsHypothesis"]
                            if ed["id"] == "hardcover"])
    bite("Kindle bandı ihlali YAKALANIR", None, "editions.py",
         cfg_mut=lambda c: [ed.__setitem__("list", 24.99)
                            for ed in c["production"]["editionsHypothesis"]
                            if ed["id"] == "kindle"])

    # ── build_index.py ─────────────────────────────────────────────────────
    print("  ▸ build_index")
    fams = clean_families()
    fam_ids = [f["id"] for f in fams["families"]]

    def shard_set(games: list) -> dict:
        by: dict = {f: [] for f in fam_ids}
        for g in games:
            by[g["family"]].append(g)
        return {"family-%s.json" % f: {"family": f, "games": by[f]}
                for f in fam_ids}

    g = clean_games(cfg, 150)
    shards = shard_set(g["games"])
    root = make_root(tmp, cfg, g, shards=shards)
    code, out = run_gate("build_index.py", root)
    rep.check(code == 0, "parçalardan indeks üretimi çalışır", out)
    code, out = run_gate("build_index.py", root, "--check")
    rep.check(code == 0, "taze indeks --check geçer", out)

    # BAYAT indeks: parçalar değişti, indeks eski kaldı.
    stale = copy.deepcopy(g)
    stale["games"][0]["name"] = "Elle değiştirilmiş kayıt"
    write_json(os.path.join(root, "01_SOURCE", "game_index.json"), stale)
    code, out = run_gate("build_index.py", root, "--check")
    rep.check(code != 0, "BAYAT indeks YAKALANIR (--check)", out)

    g2 = clean_games(cfg, 150)
    sh = shard_set(g2["games"])
    sh["family-sowing.json"]["games"][1]["gameId"] = \
        sh["family-sowing.json"]["games"][0]["gameId"]
    root = make_root(tmp, cfg, None, shards=sh)
    code, out = run_gate("build_index.py", root)
    rep.check(code != 0, "parçalarda yinelenen gameId YAKALANIR", out)

    g3 = clean_games(cfg, 150)
    sh = shard_set(g3["games"])
    sh["family-sowing.json"]["games"][0]["family"] = "race"
    root = make_root(tmp, cfg, None, shards=sh)
    code, out = run_gate("build_index.py", root)
    rep.check(code != 0, "yanlış parçadaki kayıt YAKALANIR", out)

    g4 = clean_games(cfg, 150)
    sh = shard_set(g4["games"])
    del sh["family-chance.json"]
    root = make_root(tmp, cfg, None, shards=sh)
    code, out = run_gate("build_index.py", root)
    rep.check(code != 0, "eksik aile parçası YAKALANIR", out)

    # ── update_docs.py ─────────────────────────────────────────────────────
    print("  ▸ update_docs")
    g5 = clean_games(cfg, 150)
    root = make_root(tmp, cfg, g5, docs=True)
    code, out = run_gate("update_docs.py", root, "--check")
    rep.check(code == 0, "taze üretilen belgeler --check geçer", out)

    with open(os.path.join(root, "BOOK_STATS.md"), "a", encoding="utf-8") as fh:
        fh.write("\nElle eklenmiş bir satır.\n")
    code, out = run_gate("update_docs.py", root, "--check")
    rep.check(code != 0, "BAYAT üretilen belge YAKALANIR", out)

    # Üretilen belge veriyi GERÇEKTEN yansıtıyor mu: envanter değişince
    # belge de değişmelidir; değişmiyorsa --check hiçbir şey korumuyordur.
    g6 = clean_games(cfg, 150)
    root2 = make_root(tmp, cfg, g6, docs=True)
    g6["games"] = g6["games"][:145]
    write_json(os.path.join(root2, "01_SOURCE", "game_index.json"), g6)
    code, out = run_gate("update_docs.py", root2, "--check")
    rep.check(code != 0, "envanter değişince belge BAYAT sayılır", out)


def part6_phase2_gates(rep, tmp: str) -> None:
    """⑥ FAZ 2 KAPILARI GERÇEKTEN ISIRIYOR MU.

    Bu bölüm Faz 2'nin varlık sebebidir. Faz 2'nin kapılarının çoğu GERÇEK
    veriyle BOŞ KOŞAR: manuscript depoda yok, Türkçe pilot depoda yok,
    kilitli oyun yok, test kaydı yok. Boş koşan bir kapı yeşil yanar ve
    yeşil yanan bir kapı korunuyormuş gibi görünür.

    Körlük yalnızca burada kapanır.
    """
    print("\n⑥ Faz 2 kapıları gerçekten ısırıyor")
    root = ROOT

    # ── ① SIZINTI DEDEKTÖRÜ · kasıtlı fikstürler ───────────────────────────
    # Fikstürler depo taramasından muaftır (aksi hâlde CI kalıcı kırmızı
    # olurdu). Muafiyet burada KANITA çevrilir: fonksiyona DOĞRUDAN verilir.
    print("  ▸ manuscript sızıntısı")
    sys.path.insert(0, os.path.join(root, "04_BUILD"))
    import validate_structure as vs  # noqa: E402
    fx = os.path.join(root, "05_TESTS", "fixtures", "leak")
    if not os.path.isdir(fx):
        rep.check(False, "sızıntı fikstürleri var", "05_TESTS/fixtures/leak yok")
    else:
        for fn in sorted(os.listdir(fx)):
            if not fn.endswith(".md") or fn == "README.md":
                continue
            with open(os.path.join(fx, fn), encoding="utf-8") as fh:
                r = vs.scan_for_leak(fh.read())
            if fn == "bad-turkish-pilot.md":
                rep.check(r["pilotMarkers"] > 0,
                          "FİKSTÜR %s → Türkçe pilot işareti YAKALANIR" % fn)
            elif fn.startswith("bad-"):
                rep.check(r["leak"],
                          "FİKSTÜR %s → sızıntı YAKALANIR (%s)"
                          % (fn, " · ".join(r["reasons"]) or "-"))
            else:
                rep.check(not r["leak"],
                          "FİKSTÜR %s → TEMİZ sayılır (yanlış alarm yok)" % fn)
        # Faz 1 dedektörü etiketsiz prozayı KAÇIRIRDI; bunu ayrıca kanıtla.
        with open(os.path.join(fx, "bad-unlabelled.md"), encoding="utf-8") as fh:
            r = vs.scan_for_leak(fh.read())
        rep.check(r["markers"] < vs.LEAK_MIN_HITS and r["leak"],
                  "ETİKETSİZ proza — Faz 1 hattı kaçırırdı, Faz 2 hattı YAKALAR")

    # ── ② DİL AYRIMI ───────────────────────────────────────────────────────
    print("  ▸ dil ayrımı")
    import qa_language_split as qls  # noqa: E402
    cases = [
        ("Slide it in a straight line: up, down, left or right.", False,
         "İngilizce kural cümlesi TEMİZ"),
        ("Toguz Kumalak and Bagh-Chal use a five by five grid.", False,
         "İngilizce metindeki Türkçe OYUN ADI yanlış alarm ÜRETMEZ"),
        ("Kral ortadaki kareye konur ve sekiz savunan taş dizilir.", True,
         "TEK Türkçe kural cümlesi YAKALANIR"),
        ("Bu oyun iki kişiyle oynanır ve her oyuncu taşlarını dizer.", True,
         "Türkçe paragraf YAKALANIR"),
    ]
    for text, expect, label in cases:
        rep.check(qls.turkishness(text)["turkish"] is expect, label)

    # ── ③ KAPSAM KİLİDİ ────────────────────────────────────────────────────
    print("  ▸ kapsam ve pilot kilidi")
    import validate_scope as vsc  # noqa: E402
    lock = json.load(open(os.path.join(root, "01_SOURCE", "scope_lock.json"),
                          encoding="utf-8"))
    ids = [e["gameId"] for e in lock["entries"]]
    rep.check(vsc.digest(ids) == lock["integrity"]["sha256"],
              "kilit özeti gerçek listeyle uyuşuyor")
    rep.check(vsc.digest(ids[:-1]) != lock["integrity"]["sha256"],
              "listeden BİR oyun düşürmek özeti DEĞİŞTİRİR")
    rep.check(vsc.digest(list(reversed(ids))) == lock["integrity"]["sha256"],
              "sıra değişikliği özeti değiştirmez (kitap aynı kitaptır)")
    dropped = {"status": "dropped", "restrictionStatus": "open",
               "playabilityStatus": "rules-complete"}
    rep.check(not vsc.eligible(dropped)[0], "düşmüş oyun UYGUN sayılmaz")
    restricted = {"status": "researched", "restrictionStatus": "restricted",
                  "playabilityStatus": "rules-complete"}
    rep.check(not vsc.eligible(restricted)[0], "kısıtlı oyun UYGUN sayılmaz")

    # ── ④ DİYAGRAM KAPISI ──────────────────────────────────────────────────
    print("  ▸ diyagram dili")
    dpath = os.path.join(root, "07_ASSETS", "diagrams", "pilot_diagrams.json")
    if os.path.exists(dpath):
        with open(dpath, encoding="utf-8") as fh:
            orig = fh.read()
        muts = [
            ("yeniden kurgulama beyanının SİLİNMESİ YAKALANIR",
             lambda d: d["diagrams"][0].__setitem__("reconstructed", False)),
            ("tahta DIŞI koordinat YAKALANIR",
             lambda d: d["diagrams"][0]["pieces"][0].__setitem__("at", "z9")),
            ("efsanedeki ÖLÜ sembol YAKALANIR",
             lambda d: d["diagrams"][2]["legend"].append(
                 {"glyph": "king", "label": "kral"})),
            ("sözlükte OLMAYAN glif YAKALANIR",
             lambda d: d["diagrams"][1]["pieces"][0].__setitem__("glyph", "tiger")),
            ("RENK kullanımı YAKALANIR",
             lambda d: d["diagrams"][3].__setitem__("colour", "#c00")),
            ("uyarlama ALTYAZISININ silinmesi YAKALANIR",
             lambda d: d["diagrams"][3].__setitem__("caption", "")),
        ]
        try:
            for label, mut in muts:
                d = json.loads(orig)
                mut(d)
                with open(dpath, "w", encoding="utf-8") as fh:
                    json.dump(d, fh, ensure_ascii=False, indent=2)
                code, out = run_gate("qa_diagram.py", root)
                rep.check(code != 0, label, out)
        finally:
            with open(dpath, "w", encoding="utf-8") as fh:
                fh.write(orig)
        code, out = run_gate("qa_diagram.py", root)
        rep.check(code == 0, "TEMİZ diyagram kümesi geçer", out)

    # ── ⑤ OYNANABİLİRLİK ───────────────────────────────────────────────────
    # Bu kapı gerçek veriyle TAMAMEN boş koşar: kilitli oyun yok, kayıt yok.
    # Isırdığı yalnızca burada kanıtlanabilir.
    print("  ▸ oynanabilirlik")
    cfg = json.load(open(os.path.join(root, "project_config.json"),
                        encoding="utf-8"))
    import qa_playable as qp  # noqa: E402

    def playable_root(sessions, lock_game=True):
        r = os.path.join(tmp, "pl%d" % len(os.listdir(tmp)))
        os.makedirs(os.path.join(r, "01_SOURCE", "playtests"))
        os.makedirs(os.path.join(r, "06_REPORTS"), exist_ok=True)
        write_json(os.path.join(r, "project_config.json"), cfg)
        g = {"games": [{"gameId": "tablut", "status":
                        "locked" if lock_game else "candidate"}]}
        write_json(os.path.join(r, "01_SOURCE", "game_index.json"), g)
        write_json(os.path.join(r, "01_SOURCE", "playtests", "tablut.json"),
                   {"gameId": "tablut", "sessions": sessions})
        return r

    ok_session = {"gameId": "tablut", "testerId": "T01",
                  "evidenceType": "external", "testedVersion": "v1",
                  "language": "tr", "startedAt": "2026-08-20T19:05",
                  "finishedAt": "2026-08-20T19:47", "playerCount": 2,
                  "result": "playable", "usedOnlyBookText": True,
                  "edgeCasesSeen": {"tie": False, "stalemate": False,
                                    "illegalMove": True}}
    code, out = run_gate("qa_playable.py", playable_root([ok_session]))
    rep.check(code == 0, "geçerli DIŞ test kaydı kapıyı açar", out)

    s = dict(ok_session, evidenceType="internal")
    code, out = run_gate("qa_playable.py", playable_root([s]))
    rep.check(code != 0,
              "İÇ kanıt DIŞ kanıtın yerine GEÇMEZ (kilitli oyun testsiz kalır)",
              out)

    s = dict(ok_session, usedOnlyBookText=False)
    code, out = run_gate("qa_playable.py", playable_root([s]))
    rep.check(code != 0, "kitap dışı bilgiyle oynanan test GEÇERSİZDİR", out)

    s = dict(ok_session); s["email"] = "a@b.c"
    code, out = run_gate("qa_playable.py", playable_root([s]))
    rep.check(code != 0, "KİŞİSEL VERİ taşıyan kayıt REDDEDİLİR", out)

    s = dict(ok_session, testerId="Ahmet")
    code, out = run_gate("qa_playable.py", playable_root([s]))
    rep.check(code != 0, "anonim OLMAYAN testçi kimliği REDDEDİLİR", out)

    s = dict(ok_session); s["edgeCasesSeen"] = {"tie": False}
    code, out = run_gate("qa_playable.py", playable_root([s]))
    rep.check(code != 0, "üç edge case cevapsızken 'playable' YAKALANIR", out)

    code, out = run_gate("qa_playable.py", playable_root([]))
    rep.check(code != 0, "TESTSİZ kilitli oyun YAKALANIR", out)

    # ── ⑥ SAYFA DOĞRULAMA KAYDI ────────────────────────────────────────────
    print("  ▸ sayfa doğrulama")
    import validate_research as vr  # noqa: E402
    svp = os.path.join(root, "01_SOURCE", "source_verification.json")
    if os.path.exists(svp):
        recs = json.load(open(svp, encoding="utf-8"))["records"]
        thin = [r for r in recs if r["status"] == "verified"
                and len(r.get("supportingPassage", "")) < 40]
        rep.check(not thin,
                  "'verified' her kaydın dayanak PASAJI var (%d kayıt)" % len(recs))
        blocked = [r for r in recs if r["status"] == "blocked"]
        rep.check(all(not (r.get("locator") or "").strip("—").strip()
                      for r in blocked),
                  "'blocked' hiçbir kayıt locator taşımıyor (%d kayıt)"
                  % len(blocked))
        rep.check(vr.author_key("Culin, Stewart, Korean Games") ==
                  vr.author_key("Culin, Stewart, Games of the North American Indians"),
                  "aynı yazarın iki eseri BİR kaynak sayılır")


def part7_phase3_gates(rep, tmp: str) -> None:
    """⑦ FAZ 3 KAPILARI GERÇEKTEN ISIRIYOR MU.

    Faz 3 üç yeni koruma getirdi ve üçü de gerçek veriyle YEŞİL koşuyor —
    yani ısırdıkları yalnızca burada kanıtlanabilir:

      · 150 mm diyagram bütçesi (K19) — RENDER ölçümünden
      · graph tahtalarda düğüm sınırı (dil v1.3)
      · uydurulmuş locator — 'verified' kaydı olmayan sayfa numarası
    """
    print("\n⑦ Faz 3 kapıları gerçekten ısırıyor")
    root = ROOT
    sys.path.insert(0, os.path.join(root, "04_BUILD"))

    # ── 150 MM BÜTÇESİ ─────────────────────────────────────────────────────
    print("  ▸ diyagram bütçesi (150 mm)")
    rpath = os.path.join(root, "06_REPORTS", "diagram-render.json")
    if os.path.exists(rpath):
        with open(rpath, encoding="utf-8") as fh:
            orig = fh.read()
        try:
            for label, mut in [
                ("bütçeyi 1 mm aşan diyagram YAKALANIR",
                 lambda d: d["diagrams"][0].__setitem__("heightMm", 151.0)),
                ("RENDER EDİLMEMİŞ diyagram YAKALANIR",
                 lambda d: d.__setitem__("diagrams", d["diagrams"][1:])),
            ]:
                d = json.loads(orig)
                mut(d)
                write_json(rpath, d)
                code, out = run_gate("qa_diagram.py", root)
                rep.check(code != 0, label, out)
        finally:
            with open(rpath, "w", encoding="utf-8") as fh:
                fh.write(orig)
        code, out = run_gate("qa_diagram.py", root)
        rep.check(code == 0, "TEMİZ render ölçümü geçer", out)

    # ── GRAPH TAHTA SINIRI ─────────────────────────────────────────────────
    print("  ▸ graph tahta sınırı")
    dpath = os.path.join(root, "07_ASSETS", "diagrams", "phase3_diagrams.json")
    if os.path.exists(dpath):
        with open(dpath, encoding="utf-8") as fh:
            orig = fh.read()
        try:
            for label, mut in [
                ("TANIMSIZ düğümde duran taş YAKALANIR",
                 lambda d: d["diagrams"][0]["pieces"][0].__setitem__("at", "zz")),
                ("KOPUK kenar YAKALANIR",
                 lambda d: d["diagrams"][0]["edges"].append(["a", "yok"])),
            ]:
                d = json.loads(orig)
                mut(d)
                write_json(dpath, d)
                code, out = run_gate("qa_diagram.py", root)
                rep.check(code != 0, label, out)
        finally:
            with open(dpath, "w", encoding="utf-8") as fh:
                fh.write(orig)

    # ── UYDURULMUŞ LOCATOR ─────────────────────────────────────────────────
    # Bu, Faz 3'ün en önemli dürüstlük kapısıdır: erişilemeyen bir kaynağa
    # sayfa numarası yazmak, doğrulanmamışı doğrulanmış göstermektir.
    print("  ▸ uydurulmuş locator")
    import validate_research as vr  # noqa: E402
    svp = os.path.join(root, "01_SOURCE", "source_verification.json")
    recs = json.load(open(svp, encoding="utf-8"))["records"]
    verified = {(r["gameId"], vr.author_key(r["sourceRef"]))
                for r in recs if r["status"] == "verified"}
    blocked = {(r["gameId"], vr.author_key(r["sourceRef"]))
               for r in recs if r["status"] == "blocked"}
    rep.check(("bao-la-kiswahili", "de voogt") in blocked
              or any(g == "bao-la-kiswahili" for g, _ in blocked),
              "erişilemeyen kaynak 'blocked' olarak kayıtlı")
    games = {g["gameId"]: g for g in
             json.load(open(os.path.join(root, "01_SOURCE", "game_index.json"),
                            encoding="utf-8"))["games"]}
    orphan = [(gid, vr.author_key(s.get("ref", "")))
              for gid, g in games.items() for s in (g.get("sources") or [])
              if (s.get("locator") or "").strip()
              and (gid, vr.author_key(s.get("ref", ""))) not in verified]
    rep.check(not orphan,
              "envanterdeki her locator bir 'verified' kayda dayanıyor "
              "(%d locator tarandı)" % sum(1 for g in games.values()
                                           for s in (g.get("sources") or [])
                                           if (s.get("locator") or "").strip()))

    # ── ÜRETİM KUYRUĞU DÜRÜSTLÜĞÜ ──────────────────────────────────────────
    print("  ▸ üretim kuyruğu")
    qp = os.path.join(root, "01_SOURCE", "production_queue.json")
    if os.path.exists(qp):
        q = json.load(open(qp, encoding="utf-8"))
        drafted_unverified = [g["gameId"] for g in q["games"]
                              if g["manuscriptStatus"] == "draft"
                              and g["verifiedSources"] == 0]
        rep.check(not drafted_unverified,
                  "hiçbir DRAFT oyun sıfır doğrulanmış kaynakla yazılmamış — %s"
                  % (drafted_unverified or "temiz"))
        locked_any = [g["gameId"] for g in q["games"]
                      if g["manuscriptStatus"] == "locked"]
        rep.check(not locked_any,
                  "hiçbir oyun LOCKED değil (dış test yok) — %s"
                  % (locked_any or "temiz"))


def part8_phase4_gates(rep, tmp: str) -> None:
    """⑧ FAZ 4 KAPILARI GERÇEKTEN ISIRIYOR MU.

    Faz 4 dört yeni koruma getirdi ve dördü de gerçek veriyle YEŞİL koşuyor.
    Bir kapının ısırdığı yalnızca KUSURLU bir kurguda görülebilir:

      · kuyruk SIRASI — engelli oyun erişilebilirin önüne geçemez (K22)
      · 150 mm bütçesi OYUN BAŞINA — iki diyagram toplamı da denetlenir
      · efsane, alma çarpısını (×) AÇIKLAMAK zorunda
      · manuscript kapısı — beş öğe · üç soru · beyan · kaynak · dış test
    """
    print("\n⑧ Faz 4 kapıları gerçekten ısırıyor")
    root = ROOT

    # ── ① KUYRUK SIRASI ────────────────────────────────────────────────────
    print("  ▸ üretim kuyruğu sırası")
    qp = os.path.join(root, "01_SOURCE", "production_queue.json")
    if os.path.exists(qp):
        with open(qp, encoding="utf-8") as fh:
            orig = fh.read()

        def swap_blocked_to_front(d):
            """Engelli bir oyunu kuyruğun BAŞINA taşır."""
            i = next(i for i, g in enumerate(d["games"]) if g["priority"] >= 4)
            d["games"].insert(0, d["games"].pop(i))

        def mark_unattempted_as_blocked(d):
            """Denenmemiş bir oyunu 'engelli' gösterir — engeli ABARTIR."""
            g = next(g for g in d["games"]
                     if g["priority"] == 2 and g["sourceStatus"] == "not-attempted")
            g["priority"] = 4
            g["accessibility"] = "deferred"

        def duplicate_game(d):
            d["games"].append(dict(d["games"][0]))

        def write_without_source(d):
            g = next(g for g in d["games"] if g["verifiedSources"] == 0)
            g["manuscriptStatus"] = "draft"

        try:
            for label, mut in [
                ("ENGELLİ oyun erişilebilirin ÖNÜNE geçerse YAKALANIR",
                 swap_blocked_to_front),
                ("DENENMEMİŞ oyunu 'engelli' göstermek YAKALANIR",
                 mark_unattempted_as_blocked),
                ("kuyrukta YİNELENEN oyun YAKALANIR", duplicate_game),
                ("doğrulanmamış kaynakla YAZILMIŞ oyun YAKALANIR",
                 write_without_source),
            ]:
                d = json.loads(orig)
                mut(d)
                write_json(qp, d)
                code, out = run_gate("build_queue.py", root, "--check")
                rep.check(code != 0, label, out)
        finally:
            with open(qp, "w", encoding="utf-8") as fh:
                fh.write(orig)
        code, out = run_gate("build_queue.py", root, "--check")
        rep.check(code == 0, "TEMİZ kuyruk erişilebilir-önce sırayla geçer", out)

    # ── ② OYUN BAŞINA DİYAGRAM BÜTÇESİ ─────────────────────────────────────
    # Faz 4'ün bulduğu KÖRLÜK: bütçenin adı `maxDiagramMmPerGame` ama denetim
    # diyagram başınaydı. İki diyagramı olan bir madde bütçeyi ikiye
    # katlayabiliyordu ve kapı yeşil yanıyordu.
    print("  ▸ oyun başına diyagram bütçesi")
    rpath = os.path.join(root, "06_REPORTS", "diagram-render.json")
    if os.path.exists(rpath):
        with open(rpath, encoding="utf-8") as fh:
            orig = fh.read()

        def split_over_budget(d):
            """Tek tek GEÇEN ama TOPLAMDA aşan iki diyagram."""
            same = [m for m in d["diagrams"] if m["gameId"] == "tablut"]
            for m in same:
                m["heightMm"] = 80.0        # 80 < 150 ✓ ama 80+80 = 160 ⛔

        try:
            d = json.loads(orig)
            split_over_budget(d)
            write_json(rpath, d)
            code, out = run_gate("qa_diagram.py", root)
            rep.check(code != 0,
                      "tek tek geçen ama TOPLAMDA bütçeyi aşan iki diyagram "
                      "YAKALANIR", out)
        finally:
            with open(rpath, "w", encoding="utf-8") as fh:
                fh.write(orig)

    # ── ③ EFSANE ALMA ÇARPISINI AÇIKLAMALI ─────────────────────────────────
    print("  ▸ efsane × sembolünü açıklıyor mu")
    dpath = os.path.join(root, "07_ASSETS", "diagrams", "phase4_diagrams.json")
    if os.path.exists(dpath):
        with open(dpath, encoding="utf-8") as fh:
            orig = fh.read()

        def drop_captured_legend(d):
            x = next(x for x in d["diagrams"]
                     if any(p.get("captured") for p in x.get("pieces", [])))
            x["legend"] = [e for e in x["legend"] if e["glyph"] != "captured"]

        try:
            d = json.loads(orig)
            drop_captured_legend(d)
            write_json(dpath, d)
            code, out = run_gate("qa_diagram.py", root)
            rep.check(code != 0,
                      "efsanesi × işaretini AÇIKLAMAYAN diyagram YAKALANIR",
                      out)
        finally:
            with open(dpath, "w", encoding="utf-8") as fh:
                fh.write(orig)

    # ── ④ MANUSCRIPT KAPISI ────────────────────────────────────────────────
    # Manuscript depoda YOKTUR; kapı orada boş koşar. Isırdığı yalnızca
    # burada, kurgu bir manuscript'le kanıtlanabilir.
    print("  ▸ manuscript kapısı")
    cfg = json.load(open(os.path.join(root, "project_config.json"),
                         encoding="utf-8"))

    def clean_entry():
        return {
            "gameId": "fixture-game", "title": "Fixture", "culture": "Nowhere",
            "place": "Nowhere", "period": "never", "family": "territory",
            "authoring": "written-directly-in-english", "translatedFrom": None,
            "status": "researched", "reconstructed": False,
            "spec": {"players": "2", "time": "10 minutes", "age": "6 and up",
                     "materials": "A board", "difficulty": "Easy"},
            "culturalStory": "A story.",
            "materialsAndSubstitution": "Some things.",
            "setup": ["Draw the board."],
            "turnSequence": ["Move a piece."],
            "winCondition": "Take everything.",
            "endCondition": "Play stops when nothing is left.",
            "edgeCases": {"tie": "A draw.", "stalemate": "A loss.",
                          "illegalMove": "Put it back."},
            "exampleTurn": "A turn.", "firstGame": "A short game.",
            "sources": ["Someone, A Book (Somewhere, 1900)."],
            "englishValidation": {k: "checked" for k in
                                  ("source", "rules", "playability", "clarity",
                                   "terminology", "cultural", "diagram")},
            "diagrams": [],
        }

    def ms_root(entry, *, index=None, playtests=None):
        r = os.path.join(tmp, "ms-%03d" % _RUN_SEQ[0])
        _RUN_SEQ[0] += 1
        os.makedirs(os.path.join(r, "02_MANUSCRIPT"), exist_ok=True)
        os.makedirs(os.path.join(r, "01_SOURCE"), exist_ok=True)
        os.makedirs(os.path.join(r, "04_BUILD"), exist_ok=True)
        os.makedirs(os.path.join(r, "06_REPORTS"), exist_ok=True)
        write_json(os.path.join(r, "project_config.json"), cfg)
        write_json(os.path.join(r, "02_MANUSCRIPT", "book.json"),
                   {"games": [entry]})
        if index is not None:
            write_json(os.path.join(r, "01_SOURCE", "game_index.json"),
                       {"games": index})
        if playtests:
            os.makedirs(os.path.join(r, "01_SOURCE", "playtests"), exist_ok=True)
            for i, pt in enumerate(playtests):
                write_json(os.path.join(r, "01_SOURCE", "playtests",
                                        "t%d.json" % i), pt)
        shutil.copy2(os.path.join(BUILD, "calibrate_pages.py"),
                     os.path.join(r, "04_BUILD", "calibrate_pages.py"))
        return r

    code, out = run_gate("qa_manuscript.py", ms_root(clean_entry()))
    rep.check(code == 0, "TEMİZ manuscript maddesi geçer", out)

    for label, mut in [
        ("BİTİŞ KOŞULU olmayan madde YAKALANIR",
         lambda e: e.__setitem__("endCondition", "")),
        ("KURULUMU olmayan madde YAKALANIR",
         lambda e: e.__setitem__("setup", [])),
        ("HEDEFİ olmayan madde YAKALANIR",
         lambda e: e.__setitem__("winCondition", "")),
        ("hamle bloğu olmayan madde YAKALANIR",
         lambda e: e.__setitem__("turnSequence", [])),
        ("üç sorudan biri cevapsızsa YAKALANIR",
         lambda e: e["edgeCases"].__setitem__("tie", "")),
        ("KAYNAKSIZ madde YAKALANIR", lambda e: e.__setitem__("sources", [])),
        ("BEYANSIZ yeniden kurgulama YAKALANIR",
         lambda e: e.__setitem__("reconstructed", True)),
        ("ÇEVİRİ BEYANI taşıyan ticari madde YAKALANIR",
         lambda e: e.__setitem__("translatedFrom", "tr")),
        ("doğrulama kaydı eksik madde YAKALANIR",
         lambda e: e["englishValidation"].__setitem__("cultural", "")),
        ("DOĞRULANMAMIŞ sayfa numarası veren madde YAKALANIR",
         lambda e: e.__setitem__("sources", ["Someone, A Book, pp. 12–14."])),
        ("ÖLÇÜLMEYEN kural bloğu YAKALANIR",
         lambda e: e.__setitem__("newBlockNobodyMeasures", ["A step."])),
    ]:
        e = clean_entry()
        mut(e)
        # `MOVE_BLOCKS` dışındaki bir blok ölçüm listesinde aranmaz; kusuru
        # gerçekçi kılmak için bilinen bir bloğu ölçüm listesinden SİLİYORUZ.
        r = ms_root(e)
        if "ÖLÇÜLMEYEN" in label:
            cp = os.path.join(r, "04_BUILD", "calibrate_pages.py")
            src = open(cp, encoding="utf-8").read()
            src = src.replace('("On your turn", "turnSequence"),', "")
            with open(cp, "w", encoding="utf-8") as fh:
                fh.write(src)
        code, out = run_gate("qa_manuscript.py", r)
        rep.check(code != 0, label, out)

    e = clean_entry()
    e["status"] = "locked"
    code, out = run_gate("qa_manuscript.py", ms_root(e))
    rep.check(code != 0, "DIŞ TEST KAYDI OLMADAN 'locked' madde YAKALANIR", out)

    e = clean_entry()
    e["reconstructed"] = True
    e["reconstructionNotice"] = "The rules below are reconstructed."
    idx = [{"gameId": "fixture-game", "playabilityStatus": "rules-complete"}]
    code, out = run_gate("qa_manuscript.py", ms_root(e, index=idx))
    rep.check(code != 0,
              "madde 'reconstructed' derken envanter DEMİYORSA YAKALANIR", out)

    e = clean_entry()
    idx = [{"gameId": "fixture-game", "playabilityStatus": "reconstructed"}]
    code, out = run_gate("qa_manuscript.py", ms_root(e, index=idx))
    rep.check(code != 0,
              "envanter 'reconstructed' derken madde DEMİYORSA YAKALANIR", out)


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
        part5_phase1_gates(rep, tmp)
        part6_phase2_gates(rep, tmp)
        part7_phase3_gates(rep, tmp)
        part8_phase4_gates(rep, tmp)

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
