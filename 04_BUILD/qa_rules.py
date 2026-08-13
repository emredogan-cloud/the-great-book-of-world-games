#!/usr/bin/env python3
"""
KURAL BÜTÜNLÜĞÜ VE OYNANABİLİRLİK KAPISI — The Great Book of World Games
================================================================================
BU KİTABIN ÖLÜM BİÇİMİ: OYUN ÇALIŞMIYOR.
Bu kapı, o ölümü veri katmanında engellemeye çalışan mekanizmadır.

Üç ayrı denetim yapar ve üçü de FARKLI bir yalanı yakalar:

  ① KURAL BÜTÜNLÜĞÜ — beş öğe (setup · play · turn logic · objective ·
     end condition) biliniyor mu; ve 'biliniyor' denen şey gerçekten
     tutarlı mı. Bir öğe `unknown` iken verdict `complete` OLAMAZ.
     Bu, kurgusal tamamlamanın önündeki tek mekanik engeldir.

  ② NETLİK (taze okur testi) — kurulum yapılabiliyor, ilk hamle atılabiliyor,
     yasal hamle yasadışıdan ayrılabiliyor, kazanan belirlenebiliyor,
     berabere tanımlı. Beşi de doğru değilse oyun ÜRETİME HAZIR DEĞİLDİR.

  ③ DURUM TUTARLILIĞI — playabilityStatus, ① ve ②'nin söylediğiyle
     çelişemez. Eksik kurallı bir oyun `rules-complete` etiketi taşıyamaz.

`locked` durumundaki oyunlar için ayrıca tam `rules` bloğu, üç edge case ve
en az bir GEÇMİŞ oynanabilirlik testi aranır (Faz 2'den itibaren ısırır).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

RC_ELEMENTS = ("setup", "play", "turnLogic", "objective", "endCondition")
CLARITY_KEYS = ("setupPerformable", "firstTurnTakeable",
                "legalMoveDistinguishable", "victoryDeterminable", "tieDefined")

# ③ Hangi playabilityStatus hangi verdict ile bir arada durabilir.
STATUS_ALLOWS_VERDICT = {
    "rules-complete":       {"complete"},
    "reconstructed":        {"complete", "partial"},
    "unresolved":           {"partial", "incomplete"},
    "not-production-ready": {"complete", "partial", "incomplete"},
    "excluded":             {"complete", "partial", "incomplete"},
}
# Faz 2 testine aday sayılan durumlar — kitaba giriş kapısı budur.
PRODUCTION_READY = ("rules-complete", "reconstructed")


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


def expected_verdict(rc: dict) -> str:
    vals = [rc.get(k) for k in RC_ELEMENTS]
    if any(v == "unknown" for v in vals):
        return "incomplete"
    if any(v == "partial" for v in vals):
        return "partial"
    return "complete"


def check_completeness(games: list, rep: Report) -> None:
    print("\n── ① kural bütünlüğü (setup → play → turn → objective → end) ──")

    missing = [g.get("gameId") for g in games if not isinstance(g.get("ruleCompleteness"), dict)]
    rep.check(not missing, "her kayıtta kural bütünlüğü bloğu var" + brief(missing))

    partial_fields = [g.get("gameId") for g in games
                      if isinstance(g.get("ruleCompleteness"), dict)
                      and any(g["ruleCompleteness"].get(k) is None for k in RC_ELEMENTS)]
    rep.check(not partial_fields,
              "beş öğenin beşi de değerlendirilmiş" + brief(partial_fields))

    # ASIL KAPI: verdict, öğelerin söylediğinden DAHA İYİMSER olamaz.
    # (Daha kötümser olabilir — editör bir oyunu ihtiyatla 'partial' sayabilir.)
    rank = {"complete": 0, "partial": 1, "incomplete": 2}
    optimistic = []
    for g in games:
        rc = g.get("ruleCompleteness")
        if not isinstance(rc, dict):
            continue
        exp, got = expected_verdict(rc), rc.get("verdict")
        if got not in rank or rank[got] < rank[exp]:
            optimistic.append("%s (%s → %s beklenir)" % (g.get("gameId"), got, exp))
    rep.check(not optimistic,
              "hiçbir verdict öğelerden daha iyimser değil (kurgusal tamamlama yok)"
              + brief(optimistic))

    # Eksik denen şeyin NE olduğu yazılmalıdır. 'Eksik ama ne eksik bilmiyorum'
    # bir araştırma sonucu değil, bir araştırma boşluğudur.
    silent = [g.get("gameId") for g in games
              if isinstance(g.get("ruleCompleteness"), dict)
              and g["ruleCompleteness"].get("verdict") in ("partial", "incomplete")
              and not g["ruleCompleteness"].get("unknownElements")]
    rep.check(not silent,
              "eksik kurallı her oyun NEYİN eksik olduğunu yazıyor" + brief(silent))

    for v in ("complete", "partial", "incomplete"):
        rep.facts["verdict_%s" % v] = sum(
            1 for g in games
            if isinstance(g.get("ruleCompleteness"), dict)
            and g["ruleCompleteness"].get("verdict") == v)


def check_clarity(games: list, rep: Report) -> None:
    print("\n── ② netlik: taze okur kural uzmanı olmadan oynayabilir mi ──")

    missing = [g.get("gameId") for g in games if not isinstance(g.get("clarity"), dict)]
    rep.check(not missing, "her kayıtta netlik bloğu var" + brief(missing))

    incomplete = [g.get("gameId") for g in games
                  if isinstance(g.get("clarity"), dict)
                  and any(g["clarity"].get(k) is None for k in CLARITY_KEYS)]
    rep.check(not incomplete, "beş netlik sorusunun beşi de cevaplı" + brief(incomplete))

    # `rules-complete` bir oyun beş sorunun beşini de geçmek ZORUNDADIR.
    # İstisna yoktur: kaydın kendisi 'kural tam' diyorsa, tam olmalıdır.
    failing = []
    for g in games:
        if g.get("playabilityStatus") != "rules-complete":
            continue
        cl = g.get("clarity") or {}
        bad = [k for k in CLARITY_KEYS if cl.get(k) is not True]
        if bad:
            failing.append("%s (%s)" % (g.get("gameId"), ", ".join(bad)))
    rep.check(not failing,
              "rules-complete her oyun beş netlik sorusunu da geçiyor" + brief(failing))

    # `reconstructed` bir oyunda TARİHSEL KAYIT netlik testinden düşebilir —
    # zaten bu yüzden yeniden kurgulanmaktadır. Ama boşluk BEYAN EDİLMEK
    # zorundadır: kitabın hangi boşluğu neye dayanarak kapattığı yazılmazsa,
    # uydurma ile yeniden kurgulama arasında mekanik bir fark kalmaz.
    undeclared = []
    for g in games:
        if g.get("playabilityStatus") != "reconstructed":
            continue
        cl = g.get("clarity") or {}
        bad = [k for k in CLARITY_KEYS if cl.get(k) is not True]
        if bad and len((g.get("reconstructionPlan") or "").strip()) < 40:
            undeclared.append("%s (%s)" % (g.get("gameId"), ", ".join(bad)))
    rep.check(not undeclared,
              "netlik boşluğu olan her reconstructed oyunun kurgulama planı yazılı"
              + brief(undeclared))
    rep.facts["reconstruction_plans"] = sum(
        1 for g in games if (g.get("reconstructionPlan") or "").strip())

    # Plan yalnızca yeniden kurgulanan oyunlara aittir; başka bir durumda
    # duran bir plan, ölü kural üretir ve yanlış güven verir.
    stray = [g.get("gameId") for g in games
             if (g.get("reconstructionPlan") or "").strip()
             and g.get("playabilityStatus") != "reconstructed"]
    rep.check(not stray,
              "kurgulama planı yalnızca reconstructed kayıtlarda" + brief(stray))

    # SONSUZ OYUN SORUNU: döngü mümkünse kitabın basacağı bitiş kuralı
    # şimdiden kayıtta durmalıdır. Masada 'e şimdi ne olacak?' sorusunun
    # cevabı Faz 4'te aranmaz. Yeniden kurgulanan oyunlarda bu kural
    # kurgulama planının içinde de durabilir.
    loopless = []
    for g in games:
        if g.get("playabilityStatus") not in PRODUCTION_READY:
            continue
        cl = g.get("clarity") or {}
        if cl.get("terminationRisk") not in ("loop-possible", "unbounded"):
            continue
        has_rule = bool((cl.get("terminationRule") or "").strip())
        has_plan = (g.get("playabilityStatus") == "reconstructed"
                    and len((g.get("reconstructionPlan") or "").strip()) >= 40)
        if not (has_rule or has_plan):
            loopless.append(g.get("gameId"))
    rep.check(not loopless,
              "döngü riski taşıyan her üretim adayının bitiş kuralı yazılı"
              + brief(loopless))

    rep.facts["production_ready"] = sum(
        1 for g in games if g.get("playabilityStatus") in PRODUCTION_READY)
    for st in ("rules-complete", "reconstructed", "unresolved",
               "not-production-ready", "excluded"):
        rep.facts["playability_%s" % st] = sum(
            1 for g in games if g.get("playabilityStatus") == st)


def check_status_consistency(games: list, rep: Report) -> None:
    print("\n── ③ durum tutarlılığı ──")

    unknown = [g.get("gameId") for g in games
               if g.get("playabilityStatus") not in STATUS_ALLOWS_VERDICT]
    rep.check(not unknown, "playabilityStatus geçerli" + brief(unknown))

    clashes = []
    for g in games:
        st = g.get("playabilityStatus")
        rc = g.get("ruleCompleteness")
        if st not in STATUS_ALLOWS_VERDICT or not isinstance(rc, dict):
            continue
        if rc.get("verdict") not in STATUS_ALLOWS_VERDICT[st]:
            clashes.append("%s (%s ↔ %s)" % (g.get("gameId"), st, rc.get("verdict")))
    rep.check(not clashes,
              "playabilityStatus kural bütünlüğüyle çelişmiyor" + brief(clashes))

    # `reconstructed` bir ETİKETTİR ve prozada görünür olmak zorundadır;
    # kaynağı da bunu söylemelidir. Sessiz yeniden kurgulama, bu kitabın
    # en tehlikeli sessiz hatasıdır.
    silent_recon = [g.get("gameId") for g in games
                    if g.get("playabilityStatus") == "reconstructed"
                    and g.get("sourceConfidence") != "reconstructed"]
    rep.check(not silent_recon,
              "yeniden kurgulanmış her oyun kaynak güveninde de bunu söylüyor"
              + brief(silent_recon))

    # Düşen bir oyunun gerekçesi kayıtta durur — yoksa neden düştüğü unutulur
    # ve altı ay sonra aynı araştırma tekrar yapılır.
    silent_drop = [g.get("gameId") for g in games
                   if g.get("status") == "dropped"
                   and not (g.get("droppedReason") or "").strip()]
    rep.check(not silent_drop, "düşen her oyunun gerekçesi yazılı" + brief(silent_drop))


def check_rule_blocks(games: list, cfg: dict, rep: Report) -> None:
    """Bir `rules` bloğu TAŞIYAN her kayıt tam denetlenir — `locked` olmasa bile.

    NEDEN LOCKED'A BAĞLI DEĞİL: yarım yazılmış bir kural bloğu, hiç yazılmamış
    bir bloktan daha tehlikelidir; 'bu oyun hazır' izlenimi verir ve Faz 3'te
    kimse geri dönüp bakmaz. Blok varsa tamdır, yoksa yoktur."""
    withrules = [g for g in games if isinstance(g.get("rules"), dict)]
    print("\n── kural bloğu taşıyan kayıtlar (%d) ──" % len(withrules))
    rep.facts["rule_blocks"] = len(withrules)
    if not withrules:
        print("  · kural bloğu taşıyan kayıt yok — bu bölüm boş koşar (selftest kapsar)")
        return

    play = cfg.get("playability", {})
    req_fields = play.get("requiredRuleFields", [])
    req_edges = play.get("requiredEdgeCases", [])
    style = cfg.get("style", {})
    max_words = style.get("ruleTextMaxSentenceWords", 22)

    missing_fields = []
    for g in withrules:
        r = g["rules"]
        gaps = [f for f in req_fields if r.get(f) in (None, "", [], {})]
        if gaps:
            missing_fields.append("%s (%s)" % (g.get("gameId"), ", ".join(gaps)))
    rep.check(not missing_fields,
              "zorunlu kural alanlarının hepsi dolu" + brief(missing_fields))

    missing_edges = []
    for g in withrules:
        ec = g["rules"].get("edgeCases") or {}
        gaps = [e for e in req_edges if not (ec.get(e) or "").strip()]
        if gaps:
            missing_edges.append("%s (%s)" % (g.get("gameId"), ", ".join(gaps)))
    rep.check(not missing_edges,
              "üç edge case (berabere · kilit · kural dışı) cevaplı"
              + brief(missing_edges))

    bad_players = [g.get("gameId") for g in withrules
                   if isinstance(g["rules"].get("playerCountMin"), int)
                   and isinstance(g["rules"].get("playerCountMax"), int)
                   and g["rules"]["playerCountMin"] > g["rules"]["playerCountMax"]]
    rep.check(not bad_players, "oyuncu sayısı aralığı geçerli" + brief(bad_players))

    # Aday kaydındaki tahminle kural bloğundaki kesin değer çelişemez;
    # çelişirse indeksler (oyuncu sayısına göre arama) yanlış çalışır.
    clash = []
    for g in withrules:
        r, p = g["rules"], g.get("players") or {}
        if p and (r.get("playerCountMin") != p.get("min")
                  or r.get("playerCountMax") != p.get("max")):
            clash.append(g.get("gameId"))
        if g.get("ageMinEstimate") is not None and r.get("ageMin") != g["ageMinEstimate"]:
            clash.append(g.get("gameId"))
    rep.check(not clash,
              "kural bloğu aday kaydıyla çelişmiyor (oyuncu · yaş)"
              + brief(sorted(set(clash))))

    # Kural adımı TEK EYLEM olmalıdır ve STYLE.md cümle azamisini aşmamalıdır.
    # Uzun bir adım masada iki kez okunur; iki kez okunan adım tartışılır.
    long_steps = []
    for g in withrules:
        for i, step in enumerate(g["rules"].get("turnSequence") or [], 1):
            if len(step.split()) > max_words:
                long_steps.append("%s adım %d (%d kelime)"
                                  % (g.get("gameId"), i, len(step.split())))
    rep.check(not long_steps,
              "kural adımları en fazla %d kelime" % max_words + brief(long_steps))

    # Basitleştirilmiş ilk oyun, oynanabilirlik sözleşmesinin parçasıdır.
    no_simple = [g.get("gameId") for g in withrules
                 if not (g["rules"].get("simplifiedFirstGame") or "").strip()]
    rep.check(not no_simple,
              "her kural bloğunda 'ilk oyununuz' sürümü var" + brief(no_simple))


def check_locked(games: list, cfg: dict, rep: Report) -> None:
    """Faz 2'den itibaren ısırır. Faz 1'de `locked` oyun yoktur ve bu bölüm
    boş koşar — ama KÖRLÜĞÜ selftest kapatır: kusurlu bir `locked` kurgu
    verildiğinde bu denetimlerin ısırdığı ayrıca kanıtlanır."""
    locked = [g for g in games if g.get("status") in ("locked", "written")]
    print("\n── locked oyunlar (%d) ──" % len(locked))
    rep.facts["locked"] = len(locked)
    if not locked:
        print("  · Faz 1'de kilitli oyun yok — bu bölüm boş koşar (selftest kapsar)")
        return

    min_tests = cfg.get("playability", {}).get("minPlaytestsPerGame", 1)

    no_rules = [g.get("gameId") for g in locked if not isinstance(g.get("rules"), dict)]
    rep.check(not no_rules, "her kilitli oyunda rules bloğu var" + brief(no_rules))

    untested = []
    for g in locked:
        passed = [p for p in (g.get("playtests") or [])
                  if p.get("result") == "playable" and p.get("usedOnlyBookText") is True]
        if len(passed) < min_tests:
            untested.append(g.get("gameId"))
    rep.check(not untested,
              "her kilitli oyunun ≥%d geçmiş oynanabilirlik testi var "
              "(yalnızca kitap metniyle)" % min_tests + brief(untested))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  KURAL BÜTÜNLÜĞÜ VE OYNANABİLİRLİK")
    print("=" * 74)

    rep = Report(args.verbose)
    try:
        cfg = load(os.path.join(root, "project_config.json"))
        idx = load(os.path.join(root, "01_SOURCE", "game_index.json"))
    except (OSError, json.JSONDecodeError) as exc:
        print("  ⛔ kaynak dosya okunamadı: %s" % exc)
        return 1

    games = idx.get("games", []) if isinstance(idx, dict) else idx
    check_completeness(games, rep)
    check_clarity(games, rep)
    check_status_consistency(games, rep)
    check_rule_blocks(games, cfg, rep)
    check_locked(games, cfg, rep)

    print("\n" + "=" * 74)
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d oyun üretime hazır"
              % (rep.checks, rep.facts.get("production_ready", 0)))
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
