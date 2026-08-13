#!/usr/bin/env python3
"""
DİL AYRIMI KAPISI — The Great Book of World Games
================================================================================
Karar K16'nın mekanizması.

  TİCARİ ÜRÜNÜN DİLİ İNGİLİZCEDİR VE İSTİSNASI YOKTUR.
  TÜRKÇE yalnızca DIŞ İNSAN TESTİ için geçici bir malzemedir.

Bu kapı üç şeyi ayrı ayrı denetler:

  ① TİCARİ KATMANDA TÜRKÇE YOK      — 02_MANUSCRIPT/ İngilizce kalır
  ② TEST KATMANI İŞARETLİ           — her Türkçe pilot dosyası TEST-ONLY der
  ③ ÇEVİRİ BEYANI VE BAĞIMSIZ DOĞRULAMA
                                    — İngilizce sürüm çeviri DEĞİLDİR ve
                                      bunu beyan eder; ayrıca bağımsız
                                      doğrulama kaydı taşır

── ③ NEDEN BÖYLE KURULDU ─────────────────────────────────────────────────
Makine çevirisini metne bakarak kanıtlamak MÜMKÜN DEĞİLDİR: iyi bir çeviri
ile iyi bir yeniden yazım aynı görünür. Bu kapı o iddiada bulunmaz.

Bunun yerine ölçebildiğini ölçer ve ölçemediğini BEYANA bağlar:

  · ölçülebilir → ticari katmanda Türkçe var mı            (mekanik)
  · ölçülebilir → İngilizce sürüm bağımsız doğrulandı mı   (mekanik)
  · ölçülemez   → metin çeviri mi                          (BEYAN + insan testi)

Beyanı denetlenebilir kılan şey şudur: `translatedFrom` alanı Türkçe pilot
dosyasını gösteriyorsa kapı kırmızı yanar. Yani "çevirdim" demek serbesttir
ama sonucu kilitlemek DEĞİLDİR.

⚠ TÜRKÇE PİLOTUN GEÇMESİ, İNGİLİZCE SÜRÜMÜN GEÇTİĞİ ANLAMINA GELMEZ.
Bir kuralın belirsizliği dilin İÇİNDE yaşar. İki sürüm ayrı ayrı test edilir.

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

# ① Türkçe imzası. Tek bir işaret yetmez — bir İngilizce metin bir Türkçe
# oyun adı taşıyabilir (Yut Nori, Toguz Kumalak) ve bu bir ihlal DEĞİLDİR.
# Bu yüzden ölçüt iki katmanlıdır: TÜRKÇE HARF + TÜRKÇE İŞLEV SÖZCÜĞÜ.
TURKISH_CHARS = "ışğüöçİIŞĞÜÖÇ"
TURKISH_FUNCTION_WORDS = [
    r"\bve\b", r"\bbir\b", r"\biçin\b", r"\bolarak\b", r"\bbu\b", r"\bile\b",
    r"\bdeğil\b", r"\bdaha\b", r"\bsonra\b", r"\bkadar\b", r"\bher\b",
    r"\byapar\b", r"\boyuncu\b", r"\btahta\b", r"\bkural\b", r"\btaş\b",
    r"\bhamle\b", r"\bkazanır\b", r"\bberabere\b", r"\bsıra\b",
]
# İKİ EŞİKLİ ÖLÇÜT — ve neden iki tane olduğu.
#
# İlk sürüm tek eşikliydi (≥4 işlev sözcüğü) ve KENDİ FİKSTÜRÜNÜ KAÇIRDI:
# ticari metne sokulan TEK BİR Türkçe kural cümlesi üç işlev sözcüğü taşıyor
# ve eşiğin altında kalıyordu. Bir paragraf için doğru olan eşik, bir cümle
# için yanlıştı.
#
#   · uzun metin → çok sözcük, düşük harf oranı yeter
#   · tek cümle  → az sözcük, ama Türkçe harf YOĞUNLUĞU yüksek
#
# İkisi de yakalanır. İngilizce bir dize Türkçe harf taşımadığı için oran
# sıfıra yakındır ve ikinci eşiği ASLA tetikleyemez — yani yanlış alarm
# üretmez. Bir oyun adı ('Toguz Kumalak') da tetiklemez: işlev sözcüğü yok.
TR_WORD_MIN = 4              # uzun metin eşiği
TR_CHAR_RATIO_MIN = 0.004
TR_SENTENCE_WORD_MIN = 2     # tek cümle eşiği
TR_SENTENCE_RATIO_MIN = 0.012

PILOT_MARKER = "TEST-ONLY / TURKISH PILOT"


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


def turkishness(text: str) -> dict:
    """Bir metnin Türkçe olup olmadığını ölçer.

    SAF FONKSİYONDUR — selftest onu fikstürlere doğrudan verir.

    İki katmanlı ölçüt kasıtlıdır. Tek başına Türkçe harf yetmez: İngilizce
    bir metin 'Toguz Kumalak' ya da 'Bagh-Chal' yazabilir ve bu bir ihlal
    değildir. Türkçeyi Türkçe yapan şey İŞLEV SÖZCÜKLERİDİR — 've', 'bir',
    'için' — çünkü onlar çevrilmemiş bir cümlenin iskeletidir.
    """
    if not text.strip():
        return {"turkish": False, "chars": 0, "ratio": 0.0, "words": 0}
    chars = sum(1 for c in text if c in TURKISH_CHARS)
    ratio = chars / max(1, len(text))
    words = sum(len(re.findall(p, text, flags=re.IGNORECASE))
                for p in TURKISH_FUNCTION_WORDS)
    turkish = (words >= TR_WORD_MIN and ratio >= TR_CHAR_RATIO_MIN) or \
              (words >= TR_SENTENCE_WORD_MIN and ratio >= TR_SENTENCE_RATIO_MIN)
    return {"turkish": turkish, "chars": chars,
            "ratio": round(ratio, 5), "words": words}


# Mühendislik alanları — DENETİM KAYDIDIR, ticari proza DEĞİLDİR ve projenin
# belge dilinde (Türkçe) yazılır. Liste KISA ve ADLIDIR.
#
# ⚠ MANTIK KASITLI OLARAK BU YÖNDEDİR: her şey taranır, bu birkaç alan
# HARİÇ. Tersi — "yalnızca şu alanlar taranır" — kırılgandır: şemaya yarın
# eklenen yeni bir proza alanı sessizce taranmadan kalırdı. Varsayılan
# TARANMAKTIR; muafiyet gerekçesiyle yazılır.
ENGINEERING_KEYS = {
    "englishValidation",   # bağımsız İngilizce doğrulamanın denetim kaydı
    "statusNote",          # bir oyunun neden locked OLAMADIĞININ gerekçesi
}


def strings_of(obj, path="") -> list:
    """JSON ağacındaki bütün dizeleri yolu ile birlikte toplar.

    `$`-önekli ve ENGINEERING_KEYS altındaki alt ağaçlar atlanır: bunlar
    okura değil denetçiye yazılmıştır ve kitaba basılmaz."""
    out = []
    if isinstance(obj, str):
        out.append((path, obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).startswith("$") or k in ENGINEERING_KEYS:
                continue
            out += strings_of(v, "%s.%s" % (path, k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += strings_of(v, "%s[%d]" % (path, i))
    return out


def check_commercial(root: str, cfg: dict, rep: Report) -> None:
    """① Ticari katmanda Türkçe olamaz."""
    d = os.path.join(root, cfg["language"]["commercialManuscriptDir"])
    print("\n── ① ticari katman (%s) ──"
          % cfg["language"]["commercialManuscriptDir"])
    files = []
    if os.path.isdir(d):
        for dirpath, _, names in os.walk(d):
            for n in names:
                if n.endswith((".json", ".md")) and n != "README.md":
                    files.append(os.path.join(dirpath, n))
    rep.facts["commercialFiles"] = len(files)
    if not files:
        print("  · ticari manuscript bu depoda yok — kapı boş koşar "
              "(CI'da beklenen; körlüğü selftest kapatır)")
        return

    tr_hits, marker_hits, undeclared, unvalidated, translated = [], [], [], [], []
    for p in files:
        rel = os.path.relpath(p, root)
        try:
            with open(p, encoding="utf-8") as fh:
                raw = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        if PILOT_MARKER.lower() in raw.lower():
            marker_hits.append(rel)
        if p.endswith(".json"):
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                rep.check(False, "ticari dosya bozuk: %s — %s" % (rel, exc))
                continue
            for path, s in strings_of(data):
                t = turkishness(s)
                if t["turkish"]:
                    tr_hits.append("%s%s (%d işlev sözcüğü)" % (rel, path, t["words"]))
            for entry in (data.get("games") or []):
                gid = entry.get("gameId", "?")
                if entry.get("translatedFrom"):
                    translated.append("%s → %s" % (gid, entry["translatedFrom"]))
                if entry.get("authoring") != "written-directly-in-english":
                    undeclared.append(gid)
                ev = entry.get("englishValidation") or {}
                need = ["source", "rules", "playability", "clarity",
                        "terminology", "cultural", "diagram"]
                missing = [k for k in need if not ev.get(k)]
                if missing:
                    unvalidated.append("%s → %s" % (gid, ",".join(missing)))
        else:
            t = turkishness(raw)
            if t["turkish"]:
                tr_hits.append("%s (%d işlev sözcüğü)" % (rel, t["words"]))

    rep.check(not tr_hits,
              "ticari manuscript'te Türkçe metin YOK (%d dosya)" % len(files)
              + brief(tr_hits))
    rep.check(not marker_hits,
              "ticari manuscript'te Türkçe pilot işareti YOK" + brief(marker_hits))
    rep.check(not translated,
              "hiçbir ticari kayıt Türkçe pilottan ÇEVRİLDİĞİNİ beyan etmiyor"
              + brief(translated))
    rep.check(not undeclared,
              "her ticari kayıt 'doğrudan İngilizce yazıldı' beyanını taşıyor"
              + brief(undeclared))
    rep.check(not unvalidated,
              "her ticari kayıt BAĞIMSIZ İngilizce doğrulama kaydı taşıyor"
              + brief(unvalidated))


def check_pilot(root: str, cfg: dict, rep: Report) -> None:
    """② Test katmanı işaretli ve YALNIZCA test katmanında."""
    d = os.path.join(root, cfg["language"]["pilotTestDir"])
    print("\n── ② test katmanı (%s) ──" % cfg["language"]["pilotTestDir"])
    if not os.path.isdir(d):
        print("  · Türkçe pilot dizini yok — kapı boş koşar")
        rep.facts["pilotFiles"] = 0
        return

    files = [os.path.join(d, n) for n in sorted(os.listdir(d))
             if n.endswith((".json", ".md"))]
    rep.facts["pilotFiles"] = len(files)
    unmarked, not_turkish = [], []
    for p in files:
        rel = os.path.relpath(p, root)
        try:
            with open(p, encoding="utf-8") as fh:
                raw = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        if PILOT_MARKER.lower() not in raw.lower():
            unmarked.append(rel)
        # Bir "Türkçe pilot" dosyası Türkçe DEĞİLSE, ya yanlış yere konmuştur
        # ya da testçiye İngilizce metin gidiyordur — ikisi de kusurdur.
        if os.path.basename(p) != "README.md" and not turkishness(raw)["turkish"]:
            not_turkish.append(rel)

    rep.check(not unmarked,
              "her Türkçe pilot dosyası '%s' işaretini taşıyor" % PILOT_MARKER
              + brief(unmarked))
    rep.check(not not_turkish,
              "Türkçe pilot dosyalarının hepsi gerçekten Türkçe" + brief(not_turkish))

    # Test malzemesi de yayımlanmamış prozadır: takip EDİLMEMELİDİR.
    import subprocess
    try:
        out = subprocess.run(["git", "ls-files", cfg["language"]["pilotTestDir"]],
                             cwd=root, capture_output=True, text=True, timeout=20)
        tracked = [l for l in out.stdout.splitlines() if l.strip()
                   and not l.endswith("README.md")]
    except (OSError, subprocess.SubprocessError):
        tracked = []
    rep.check(not tracked,
              "Türkçe pilot metni depoda TAKİP EDİLMİYOR" + brief(tracked))


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  DİL AYRIMI · ticari dil = İNGİLİZCE · test dili = Türkçe")
    print("=" * 74)

    rep = Report(args.verbose)
    try:
        cfg = load(os.path.join(root, "project_config.json"))
    except (OSError, json.JSONDecodeError) as exc:
        print("  ⛔ project_config.json okunamadı: %s" % exc)
        return 1

    lang = cfg.get("language") or {}
    rep.check(lang.get("commercial") == "en", "ticari dil yapılandırmada 'en'")
    rep.check(lang.get("pilotTestLanguageIsCommercial") is False,
              "test dili ticari SAYILMIYOR")
    rep.check(lang.get("machineTranslationForbidden") is True,
              "makine çevirisi yapılandırmada YASAK")
    rep.check(lang.get("englishRequiresIndependentValidation") is True,
              "İngilizce sürüm bağımsız doğrulama şartına bağlı")
    rep.check(not lang.get("commercialExceptions"),
              "ticari dilin istisnası YOK")

    check_commercial(root, cfg, rep)
    check_pilot(root, cfg, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · dil ayrımı korunuyor" % rep.checks)
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
