#!/usr/bin/env python3
"""
KAYNAK KÜNYESİ KAPISI — The Great Book of World Games
================================================================================
`00_CONTEXT/SOURCING_STANDARD.md` bir sözleşmedir; bu betik onun mekanizmasıdır.

Denetlenen:
  ① Her oyunun ≥1 kaynağı var mı, tipi geçerli mi, künye anlamlı mı
  ② YASAKLI KAYNAK taraması — wiki · blog · LLM çıktısı · yayıncı tanıtımı
  ③ Bağımsızlık sayımı — aynı yazarın iki eseri BİR kaynaktır
  ④ Doğrulama seviyesi — bibliographic ↔ page-verified ayrımı tutarlı mı
  ⑤ ARAŞTIRMA → YAZIM KİLİDİ — locked/written için ≥2 bağımsız + sayfa doğrulaması
  ⑥ Güven seviyesi ile kaynak sayısı çelişiyor mu

② NEDEN MEKANİZMA: "LLM çıktısı hiçbir koşulda kaynak değildir" bir disiplin
cümlesidir ve disiplin unutulur. Bu tarama onu bir kapıya bağlar.

④ NEDEN AYRI BİR ALAN: bir eserin adını yazmak, o eseri açıp sayfayı görmekle
AYNI ŞEY DEĞİLDİR. Faz 1 künye seviyesinde çalışır ve bunu gizlemez;
`page-verified` Faz 2'nin `locked` kapısıdır. Ayrımı alana bağlamak,
doğrulanmamış bir künyenin doğrulanmış gibi görünmesini imkânsız kılar.

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

VALID_TYPES = ("book", "journal", "museum", "ethnography", "archive", "field-record")
VALID_VERIFICATION = ("bibliographic", "page-verified")
REF_MIN = 12

# ② Kaynak SAYILMAYANLAR. Künyede geçmeleri kapıyı kırmızı yakar.
FORBIDDEN_SOURCE_PATTERNS = [
    (r"\bwikipedia\b", "wiki maddesi"),
    (r"\bwikipedi\b", "wiki maddesi"),
    (r"\bvikipedi\b", "wiki maddesi"),
    (r"\bfandom\b", "wiki maddesi"),
    (r"\bchatgpt\b", "LLM çıktısı"),
    (r"\bgpt-?[0-9]", "LLM çıktısı"),
    (r"\bclaude\b", "LLM çıktısı"),
    (r"\bgemini\b", "LLM çıktısı"),
    (r"\bllm\b", "LLM çıktısı"),
    (r"\byapay zek", "LLM çıktısı"),
    (r"\bblogspot\b", "blog"),
    (r"\bmedium\.com\b", "blog"),
    (r"\breddit\b", "forum"),
    (r"\byoutube\b", "video paylaşımı"),
]

# ③ Bağımsızlık: künyenin ilk virgülüne kadar olan bölüm yazar anahtarıdır.
# "Murray, H. J. R., A History of Chess" → "murray"
AUTHOR_KEY = re.compile(r"^\s*([^,(]+)")


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


def author_key(ref: str) -> str:
    m = AUTHOR_KEY.match(ref or "")
    return (m.group(1).strip().lower() if m else (ref or "").strip().lower())


def independent_count(sources: list) -> int:
    """Bağımsız kaynak sayısı.

    İki kaynak şu iki durumda AYNI sayılır:
      · aynı yazar anahtarını paylaşıyorlarsa (aynı yazarın iki kitabı bir kaynaktır)
      · biri `lineage` ile diğerine dayandığını söylüyorsa
    """
    keys: set[str] = set()
    derived: set[str] = set()
    for s in sources or []:
        k = author_key(s.get("ref", ""))
        if s.get("lineage"):
            derived.add(k)
            continue
        keys.add(k)
    return len(keys - derived) if keys else 0


def check_sources(games: list, rep: Report) -> None:
    print("\n── ① künye bütünlüğü ──")

    none_at_all = [g.get("gameId") for g in games if not g.get("sources")]
    rep.check(not none_at_all, "her oyunun en az bir kaynağı var" + brief(none_at_all))

    bad_type, thin_ref = [], []
    for g in games:
        for s in g.get("sources") or []:
            if s.get("type") not in VALID_TYPES:
                bad_type.append("%s → %s" % (g.get("gameId"), s.get("type")))
            if len((s.get("ref") or "").strip()) < REF_MIN:
                thin_ref.append("%s → '%s'" % (g.get("gameId"), s.get("ref")))
    rep.check(not bad_type, "kaynak tipleri geçerli" + brief(bad_type))
    rep.check(not thin_ref,
              "künyeler anlamlı (≥%d karakter)" % REF_MIN + brief(thin_ref))

    print("\n── ② yasaklı kaynak taraması ──")
    banned = []
    for g in games:
        for s in g.get("sources") or []:
            low = (s.get("ref") or "").lower()
            for pat, name in FORBIDDEN_SOURCE_PATTERNS:
                if re.search(pat, low):
                    banned.append("%s → %s" % (g.get("gameId"), name))
    rep.check(not banned,
              "kaynak sayılmayan hiçbir künye yok (wiki · blog · LLM · forum)"
              + brief(banned))


def check_independence(games: list, cfg: dict, rep: Report) -> None:
    print("\n── ③ bağımsızlık ve ④ doğrulama seviyesi ──")

    min_ind = cfg.get("sourcing", {}).get("minIndependentSourcesPerGame", 2)

    bad_verif = [g.get("gameId") for g in games
                 if g.get("sourceVerification") not in VALID_VERIFICATION]
    rep.check(not bad_verif, "doğrulama seviyesi geçerli" + brief(bad_verif))

    # page-verified iddiası, künyede bir locator ile DESTEKLENMEK zorundadır.
    # Desteksiz bir 'sayfayı gördüm' iddiası, bu kitabın en pahalı yalanıdır.
    unlocated = []
    for g in games:
        if g.get("sourceVerification") != "page-verified":
            continue
        for s in g.get("sources") or []:
            if not (s.get("locator") or "").strip():
                unlocated.append("%s → %s" % (g.get("gameId"), author_key(s.get("ref", ""))))
    rep.check(not unlocated,
              "page-verified sayılan her künyede locator var" + brief(unlocated))

    counts = {g.get("gameId"): independent_count(g.get("sources")) for g in games}
    rep.facts["independent_ge2"] = sum(1 for v in counts.values() if v >= min_ind)
    rep.facts["single_source"] = sum(1 for v in counts.values() if v == 1)

    # ⑥ Güven seviyesi kaynak sayısıyla çelişemez: tek kaynaklı bir oyun
    # `high` güven taşıyamaz.
    overclaim = [gid for gid, n in counts.items()
                 if n < min_ind and next(
                     (g.get("sourceConfidence") for g in games if g.get("gameId") == gid),
                     None) == "high"]
    rep.check(not overclaim,
              "tek kaynaklı hiçbir oyun 'high' güven taşımıyor" + brief(overclaim))

    print("  · ≥%d bağımsız kaynak: %d oyun" % (min_ind, rep.facts["independent_ge2"]))
    print("  · tek kaynak: %d oyun (aday aşamasında serbest, locked'da DEĞİL)"
          % rep.facts["single_source"])
    if rep.facts["single_source"]:
        rep.warn("%d oyun tek kaynaklı — locked olabilmeleri için ikinci "
                 "bağımsız künye gerekir" % rep.facts["single_source"])


def check_write_lock(games: list, cfg: dict, rep: Report) -> None:
    """⑤ ARAŞTIRMA → YAZIM KİLİDİ.

    Faz 1'de kilitli oyun yoktur ve bu bölüm boş koşar. Körlüğü selftest
    kapatır: kusurlu bir `locked` kurguya karşı ısırdığı ayrıca kanıtlanır."""
    min_ind = cfg.get("sourcing", {}).get("minIndependentSourcesPerGame", 2)
    locked = [g for g in games if g.get("status") in ("locked", "written")]
    print("\n── ⑤ araştırma → yazım kilidi (%d kilitli oyun) ──" % len(locked))
    rep.facts["locked"] = len(locked)
    if not locked:
        print("  · Faz 1'de kilitli oyun yok — kilit boş koşar (selftest kapsar)")
        return

    thin = [g.get("gameId") for g in locked
            if independent_count(g.get("sources")) < min_ind]
    rep.check(not thin,
              "her kilitli oyunun ≥%d bağımsız kaynağı var" % min_ind + brief(thin))

    unverified = [g.get("gameId") for g in locked
                  if g.get("sourceVerification") != "page-verified"]
    rep.check(not unverified,
              "her kilitli oyunun kaynağı SAYFA seviyesinde doğrulanmış"
              + brief(unverified))

    unscreened = [g.get("gameId") for g in locked if not g.get("restrictionStatus")]
    rep.check(not unscreened, "her kilitli oyun kısıt taramasından geçmiş"
              + brief(unscreened))

    forbidden = [g.get("gameId") for g in locked
                 if g.get("restrictionStatus") in ("restricted", "excluded")]
    rep.check(not forbidden,
              "kısıtlı / elenmiş hiçbir oyun kilitlenmemiş" + brief(forbidden))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  KAYNAK KÜNYESİ VE ARAŞTIRMA KİLİDİ")
    print("=" * 74)

    rep = Report(args.verbose)
    try:
        cfg = load(os.path.join(root, "project_config.json"))
        idx = load(os.path.join(root, "01_SOURCE", "game_index.json"))
    except (OSError, json.JSONDecodeError) as exc:
        print("  ⛔ kaynak dosya okunamadı: %s" % exc)
        return 1

    games = idx.get("games", []) if isinstance(idx, dict) else idx
    rep.facts["games"] = len(games)
    rep.facts["source_records"] = sum(len(g.get("sources") or []) for g in games)

    check_sources(games, rep)
    check_independence(games, cfg, rep)
    check_write_lock(games, cfg, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d oyun · %d künye"
              % (rep.checks, rep.facts["games"], rep.facts["source_records"]))
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
