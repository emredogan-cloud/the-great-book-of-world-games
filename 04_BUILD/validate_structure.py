#!/usr/bin/env python3
"""
DEPO, BELGE VE MANUSCRIPT KORUMASI — The Great Book of World Games
================================================================================
Dört ayrı denetim, dördü de bir kusurun GERİ GELMESİNİ engellemek için var:

  ① ZORUNLU DOSYALAR       — yol haritasının söz verdiği belgeler gerçekten var mı
  ② GÖMÜLÜ SABİT DEĞER     — yazar/yayıncı adı bir betiğe gömülmüş mü
  ③ MANUSCRIPT SIZINTISI   — kural prozası takip edilen bir dosyaya sızmış mı
  ④ SIR SIZINTISI          — .env veya anahtar benzeri dize depoya girmiş mi

② NEDEN VAR: World Myths Faz 6'da yazar adı ÜÇ betikte ayrı ayrı gömülüydü
(covers.py, epub.py, handoff.py) ve metadata.py yer tutucu basıyordu — aynı
kitabın KAPAĞI ile METADATASI farklı yazar taşıyordu. Kusur Bestiarium D17'de
de vardı. Tek doğruluk kaynağı project_config.json'dur ve bu kapı onu korur.

③ NEDEN VAR: .gitignore YOL kalıplarıyla çalışır ve yeni bir ada konan dosyayı
YAKALAMAZ. Bu yüzden ikinci bir hat gerekir: takip edilen dosyaların İÇERİĞİNE
bakan bir tarayıcı. Politikayı disipline değil MEKANİZMAYA bağlarız.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

REQUIRED_FILES = [
    "README.md",
    "PROJECT_CONTEXT.md",
    "BRIEF.md",
    "DECISIONS.md",
    "CHANGELOG.md",
    "ROADMAP_PROGRESS.md",
    "BOOK_STATS.md",
    "project_config.json",
    ".gate",
    ".gitignore",
    "THE_GREAT_BOOK_OF_WORLD_GAMES_IMPLEMENTATION_ROADMAP.md",
    "00_CONTEXT/STYLE.md",
    "00_CONTEXT/SOURCING_STANDARD.md",
    "00_CONTEXT/PLAYABILITY_STANDARD.md",
    "00_CONTEXT/LESSONS_FROM_CODEX.md",
    "00_CONTEXT/EDITORIAL_ARCHITECTURE.md",
    "01_SOURCE/game.schema.json",
    "01_SOURCE/game_index.json",
    "01_SOURCE/family_index.json",
    "04_BUILD/qa_all.sh",
    "04_BUILD/validate_spec.py",
    "04_BUILD/build_index.py",
    "04_BUILD/validate_research.py",
    "04_BUILD/qa_taxonomy.py",
    "04_BUILD/qa_rules.py",
    "04_BUILD/score_candidates.py",
    "04_BUILD/page_budget.py",
    "04_BUILD/editions.py",
    "04_BUILD/update_docs.py",
    "05_TESTS/selftest.py",
    "05_TESTS/fixtures/leak/README.md",
    "05_TESTS/fixtures/leak/bad-labelled.md",
    "05_TESTS/fixtures/leak/bad-unlabelled.md",
    "05_TESTS/fixtures/leak/bad-turkish-pilot.md",
    "05_TESTS/fixtures/leak/clean-documentation.md",
    "05_TESTS/fixtures/leak/clean-data-record.md",
    "00_CONTEXT/DIAGRAM_LANGUAGE.md",
    "01_SOURCE/scope_lock.json",
    "01_SOURCE/pilot_lock.json",
    "01_SOURCE/source_verification.json",
    "01_SOURCE/playtests/README.md",
    "01_SOURCE/pilot_tr/README.md",
    "07_ASSETS/diagrams/diagram_language.json",
    "07_ASSETS/diagrams/pilot_diagrams.json",
    "04_BUILD/validate_scope.py",
    "04_BUILD/qa_diagram.py",
    "04_BUILD/qa_playable.py",
    "04_BUILD/qa_language_split.py",
    "04_BUILD/calibrate_pages.py",
    "04_BUILD/render_diagrams.py",
    "06_REPORTS/PHASE_1_REPORT.md",
    ".github/workflows/validate.yml",
]

REQUIRED_DIRS = [
    "05_TESTS/fixtures/leak", "01_SOURCE/pilot_tr",
    "00_CONTEXT", "01_SOURCE", "02_MANUSCRIPT", "03_COVER", "04_BUILD",
    "05_TESTS", "06_REPORTS", "07_ASSETS", "08_OUTPUT", "09_ARCHIVE",
    "01_SOURCE/games", "01_SOURCE/playtests", "01_SOURCE/research",
    "07_ASSETS/raw", "07_ASSETS/processed", "07_ASSETS/diagrams",
]

# ② Gömülü sabit değer taraması ------------------------------------------------
# Bu dizeler YALNIZCA project_config.json içinde geçebilir.
SINGLE_SOURCE_VALUES = ["Emre Doğan", "Vâliçe Press"]
SCAN_CODE_EXT = (".py", ".sh", ".yml", ".yaml")
# Bu dosyalar muaf: config'in kendisi ve onu ANLATAN belgeler.
EMBED_SCAN_SKIP = {
    "project_config.json",
    "04_BUILD/validate_structure.py",   # tarayıcının kendisi dizeleri taşır
}

# ③ Manuscript sızıntısı -------------------------------------------------------
#
# ⚠ FAZ 2'DE GÜÇLENDİRİLDİ (karar K12).
#
# Faz 1'in dedektörü yalnızca aşağıdaki BEŞ YAPISAL ETİKETE bakıyordu ve
# bu yeterli değildi. Gerekçe tek cümledir:
#
#       ETİKETLERİ SİLMEK, PROZAYI SİLMEZ.
#
# Etiketsiz yazılmış bir kural metni — "Place the board between you. Each
# player takes twelve seeds. On a turn you lift every seed from one hollow…" —
# beş etiketin hiçbirini taşımaz ve eski dedektörden TEMİZ GEÇERDİ.
#
# Artık dört hat vardır ve üçü içeriğe bakar:
#
#   ① structural-marker  → sekiz bloğun etiketleri            (Faz 1'den)
#   ② content-signature  → ikinci tekil TALİMAT DİLİ           (yeni)
#   ③ density            → kural cümlesi YOĞUNLUĞU             (yeni)
#   ④ pilot-marker       → Türkçe test malzemesi işareti       (yeni)
#
# ③ NEDEN GEREKLİ: bir belge kural dilini ÖRNEK olarak anabilir; bu
# sızıntı değildir. Ayrımı YOĞUNLUK yapar. Bu belgenin kendisi ② kalıplarının
# birçoğunu taşır ve taşımak zorundadır — ama bir manuscript'in aksine,
# çevresi kural değil AÇIKLAMADIR. Yoğunluk eşiği tam olarak bu farkı ölçer
# ve muafiyet listesini kısa tutar: muafiyet ne kadar uzarsa koruma o kadar
# zayıflar.
LEAK_MARKERS = [
    r"\bSetup:\s",
    r"\bTurn sequence:\s",
    r"\bWin condition:\s",
    r"\bOn your turn,\s",
    r"\bThe game ends when\b",
]
LEAK_MIN_HITS = 2

# ② İçerik imzası — kural prozasının ETİKETSİZ parmak izleri.
# İkinci tekil şahıs + oyun eylemi + oyun nesnesi.
LEAK_SIGNATURES = [
    r"\b(?:Place|Put|Set|Take|Move|Slide|Drop|Sow|Throw|Roll|Deal|Remove|"
    r"Capture|Jump|Stand|Lift|Scatter|Count) (?:the|your|one|each|a|an|all|"
    r"any|two|three|four|five|six|twelve) \w+",
    r"\bOn (?:your|a|each) turn\b",
    r"\byour opponent(?:'s)?\b",
    r"\bthe player (?:who|with|to|on)\b",
    r"\bIf (?:you|a player|neither player|both players) (?:cannot|can|may|has|have)\b",
    r"\bwins the game\b",
    r"\bthe game is a draw\b",
    r"\byou may (?:move|take|capture|place|jump|sow|pass|throw)\b",
    r"\b(?:clockwise|anticlockwise|anti-clockwise) around the\b",
    r"\bhand the turn\b",
    r"\bplay passes to\b",
    r"\bat the start of the game\b",
]
LEAK_SIG_MIN_HITS = 6          # tek bir örnek cümle sızıntı değildir
LEAK_DENSITY_MIN = 0.10        # kural cümlesi / toplam cümle

# ④ Türkçe pilot işareti — TEST malzemesi ticari metne giremez (K16)
LEAK_PILOT_MARKERS = [
    r"TEST-ONLY\s*/\s*TURKISH PILOT",
    r"SADECE TEST\b",
]

LEAK_SCAN_EXT = (".md", ".json", ".txt", ".html")
# Muafiyet = yalnızca bu dosyalar kural dilini ÖRNEK olarak taşıyabilir.
#
# ⚠ HER MUAFİYET selftest § ④ TARAFINDAN İKİ KEZ DENETLENİR:
#   (a) dosya gerçekten var mı        → yoksa ÖLÜ MUAFİYET
#   (b) muafiyet olmasaydı yakalanır mıydı → hayırsa GEREKSİZ MUAFİYET
#
# Bu yüzden listeye "ihtimale karşı" dosya eklenmez. Bir dosya ancak kural
# dilini GERÇEKTEN taşıdığı için buraya girer.
# (World Myths K14 · Bestiarium D28: ölü kural sessizce yanlış güven verir.)
LEAK_SCAN_SKIP = {
    "00_CONTEXT/PLAYABILITY_STANDARD.md",
    "00_CONTEXT/STYLE.md",
    "01_SOURCE/game.schema.json",
}

# Fikstürler ayrı bir muafiyettir ve gerekçesi ötekilerden FARKLIDIR:
# bunlar KASITLI sızıntılardır ve dedektörün onları YAKALAMASI beklenir.
# Depo taramasından çıkarılırlar çünkü aksi hâlde CI kalıcı kırmızı olurdu;
# ama selftest § 6 onları doğrudan `scan_for_leak()`e verir ve
# BAD → sızıntı VAR / CLEAN → sızıntı YOK ispatını her koşuda tekrarlar.
# Yani muafiyet korumayı zayıflatmaz: korumanın KANITINI üretir.
LEAK_FIXTURE_PREFIX = "05_TESTS/fixtures/"

# Türkçe pilot malzemesinin yaşadığı TEK yer.
PILOT_TR_PREFIX = "01_SOURCE/pilot_tr/"
# İşareti TANIMLAYAN dosyalar — tanımlamak kullanmak değildir.
PILOT_MARKER_DEFINERS = {
    "project_config.json",
    "04_BUILD/validate_structure.py",
    "04_BUILD/qa_language_split.py",
    "DECISIONS.md",
}

# ④ Sır taraması ---------------------------------------------------------------
SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI benzeri anahtar"),
    (r"gh[pousr]_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"AKIA[0-9A-Z]{16}", "AWS anahtar kimliği"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "özel anahtar"),
]

FAKE_ISBN = re.compile(r"\b97[89][- ]?\d{1,5}[- ]?\d{1,7}[- ]?\d{1,7}[- ]?\d\b")


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0

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


def tracked_files() -> list[str]:
    """git ls-files — TAKİP EDİLEN dosyalar. Sızıntı denetimi yalnızca
    bunlara bakar: takip edilmeyen dosya zaten public değildir."""
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT,
                             capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            return []
        return [p for p in out.stdout.splitlines() if p.strip()]
    except (OSError, subprocess.SubprocessError):
        return []


def check_files(rep: Report) -> None:
    print("\n── zorunlu dosya ve dizinler ──")
    for rel in REQUIRED_DIRS:
        rep.check(os.path.isdir(os.path.join(ROOT, rel)), "dizin: %s" % rel)
    for rel in REQUIRED_FILES:
        rep.check(os.path.isfile(os.path.join(ROOT, rel)), "dosya: %s" % rel)


def check_gate_file(rep: Report) -> None:
    print("\n── .gate ──")
    path = os.path.join(ROOT, ".gate")
    if not os.path.exists(path):
        rep.check(False, ".gate dosyası var")
        return
    with open(path, encoding="utf-8") as fh:
        lvl = fh.read().strip()
    rep.check(lvl in ("phase0", "phase1", "phase2", "phase3", "phase4",
                      "phase5", "release"),
              ".gate geçerli bir seviye taşıyor: '%s'" % lvl)


def check_embedded(rep: Report, files: list[str]) -> None:
    print("\n── gömülü sabit değer (tek doğruluk kaynağı) ──")
    hits: list[str] = []
    for rel in files:
        if rel in EMBED_SCAN_SKIP or not rel.endswith(SCAN_CODE_EXT):
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        for val in SINGLE_SOURCE_VALUES:
            if val in body:
                hits.append("%s → '%s'" % (rel, val))
    rep.check(not hits,
              "kurucu değerleri yalnızca project_config.json'da" +
              ("" if not hits else " — GÖMÜLÜ: %s" % hits[:5]))


def scan_for_leak(body: str) -> dict:
    """Bir metnin kural prozası taşıyıp taşımadığını ölçer.

    SAF FONKSİYONDUR ve dosya sistemine bakmaz. Böyle olması kasıtlıdır:
    `05_TESTS/selftest.py` onu kasıtlı sızıntı fikstürlerine DOĞRUDAN
    verebilir ve BAD → KIRMIZI / TEMİZ → YEŞİL ispatı, depoyu gerçekten
    kirletmeden üretilir.

    Döndürdüğü sözlük bir KARAR değil bir ÖLÇÜMDÜR; `leak` alanı kararı
    taşır, ötekiler kararın NEDEN verildiğini taşır.
    """
    markers = sum(1 for pat in LEAK_MARKERS if re.search(pat, body))

    sig_hits = 0
    for pat in LEAK_SIGNATURES:
        sig_hits += len(re.findall(pat, body, flags=re.IGNORECASE))

    # Cümle sayımı kabadır ve kaba olması yeterlidir: aradığımız şey bir
    # ORAN, mutlak bir sayı değil.
    sentences = max(1, len(re.findall(r"[.!?](?:\s|$)", body)))
    density = sig_hits / sentences

    pilot = sum(1 for pat in LEAK_PILOT_MARKERS
                if re.search(pat, body, flags=re.IGNORECASE))

    # KARAR: etiketler tek başına yeter (Faz 1 hattı), YA DA imza sayısı ve
    # yoğunluk BİRLİKTE eşiği geçer. "Birlikte" şarttır — bir belge kural
    # dilini örnek olarak anabilir; onu manuscript yapan şey ORANDIR.
    leak = (markers >= LEAK_MIN_HITS) or \
           (sig_hits >= LEAK_SIG_MIN_HITS and density >= LEAK_DENSITY_MIN)

    reasons = []
    if markers >= LEAK_MIN_HITS:
        reasons.append("%d yapısal etiket" % markers)
    if sig_hits >= LEAK_SIG_MIN_HITS and density >= LEAK_DENSITY_MIN:
        reasons.append("%d içerik imzası · yoğunluk %.2f" % (sig_hits, density))
    return {"leak": leak, "markers": markers, "signatures": sig_hits,
            "density": round(density, 3), "pilotMarkers": pilot,
            "reasons": reasons}


def check_manuscript_leak(rep: Report, files: list[str]) -> None:
    print("\n── manuscript sızıntısı (4 hat) ──")
    leaked: list[str] = []
    pilot_leak: list[str] = []
    scanned = 0
    for rel in files:
        if rel in LEAK_SCAN_SKIP or not rel.endswith(LEAK_SCAN_EXT):
            continue
        if rel.startswith(LEAK_FIXTURE_PREFIX):
            continue  # kasıtlı fikstür — selftest doğrudan sınar
        if rel.startswith("02_MANUSCRIPT/"):
            # Manuscript dizinindeki TAKİP EDİLEN her dosya zaten ihlaldir.
            if os.path.basename(rel) not in (".gitkeep", "README.md"):
                leaked.append("%s (manuscript dizini takip ediliyor)" % rel)
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        scanned += 1
        r = scan_for_leak(body)
        if r["leak"]:
            leaked.append("%s (%s)" % (rel, " · ".join(r["reasons"])))
        # ④ Türkçe pilot işareti YALNIZCA pilot dizininde durabilir.
        # İki dosya işareti TANIMLAR ve bu bir sızıntı değildir: onu
        # tanımlayan yer ile onu KULLANAN yer farklı şeylerdir.
        if r["pilotMarkers"] and not rel.startswith(PILOT_TR_PREFIX) \
                and rel not in PILOT_MARKER_DEFINERS:
            pilot_leak.append(rel)

    rep.check(not leaked,
              "kural prozası depoya sızmamış (%d dosya tarandı)" % scanned +
              ("" if not leaked else " — SIZINTI: %s" % leaked[:5]))
    rep.check(not pilot_leak,
              "Türkçe pilot işareti yalnızca pilot dizininde" +
              ("" if not pilot_leak else " — SIZINTI: %s" % pilot_leak[:5]))

    # KORUMALI KATMAN TAKİP EDİLİYOR MU (karar K12).
    # `.gitignore` bir NİYETTİR; bu denetim bir OLGUDUR. Bir dosya bir kez
    # `git add -f` ile eklenirse .gitignore onu geri çıkarmaz ve kimse
    # fark etmez.
    tracked_protected = [rel for rel in files
                         if rel.startswith("01_SOURCE/rules/")
                         or (rel.startswith("02_MANUSCRIPT/")
                             and os.path.basename(rel) not in (".gitkeep", "README.md"))]
    rep.check(not tracked_protected,
              "korumalı katman (kural prozası · manuscript) takip EDİLMİYOR" +
              ("" if not tracked_protected
               else " — TAKİP EDİLİYOR: %s" % tracked_protected[:5]))


def check_secrets(rep: Report, files: list[str]) -> None:
    print("\n── sır ve sahte ISBN taraması ──")
    rep.check(".env" not in files, ".env takip edilmiyor")

    found: list[str] = []
    for rel in files:
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p) or os.path.getsize(p) > 2_000_000:
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        for pat, name in SECRET_PATTERNS:
            if re.search(pat, body):
                found.append("%s → %s" % (rel, name))
    rep.check(not found,
              "sır benzeri dize yok" + ("" if not found else " — %s" % found[:3]))

    # Sahte ISBN: kurucu kararı KDP ücretsiz ISBN. Uydurulmuş numara YASAK.
    cfgp = os.path.join(ROOT, "project_config.json")
    strategy = "kdp-free"
    if os.path.exists(cfgp):
        try:
            with open(cfgp, encoding="utf-8") as fh:
                strategy = json.load(fh).get("founder", {}).get(
                    "isbn", {}).get("strategy", "kdp-free")
        except (OSError, json.JSONDecodeError):
            pass
    if strategy == "kdp-free":
        isbn_hits: list[str] = []
        for rel in files:
            if not rel.endswith((".md", ".json", ".py")):
                continue
            if rel in ("04_BUILD/validate_structure.py",):
                continue
            p = os.path.join(ROOT, rel)
            if not os.path.isfile(p):
                continue
            try:
                with open(p, encoding="utf-8") as fh:
                    body = fh.read()
            except (OSError, UnicodeDecodeError):
                continue
            if FAKE_ISBN.search(body):
                isbn_hits.append(rel)
        rep.check(not isbn_hits,
                  "uydurulmuş ISBN yok (strateji: kdp-free)" +
                  ("" if not isbn_hits else " — %s" % isbn_hits[:3]))


def check_doc_links(rep: Report) -> None:
    """Belge bağları — iki ayrı denetim.

    ① KIRIK BAĞ      — hedef dosya var mı
    ② DEPO SINIRI    — bağ deponun DIŞINA çıkıyor mu

    ② NEDEN AYRI BİR DENETİM: bir bağ yerel makinede çözülüp CI'da
    kırılabilir. `../PAZAR-RAPORU.html` kurucunun çalışma dizininde
    VARDIR ama depoyu klonlayan kimsede YOKTUR — yani yerelde yeşil,
    CI'da kırmızı. Bu tam olarak bootstrap sırasında yaşandı.

    Depo sınırı denetimi bu ayrışmayı ortadan kaldırır: dosyanın var olup
    olmadığına bakmadan, deponun dışına çıkan her bağ REDDEDİLİR. Böylece
    yerel sonuç ile CI sonucu AYNI OLMAK ZORUNDADIR.

    Kural: depo dışındaki bir kaynağa **künyeyle** atıf yapılır, bağ verilmez.
    """
    print("\n── belge bağları ──")
    broken: list[str] = []
    escaped: list[str] = []
    root_abs = os.path.realpath(ROOT)

    scan = list(REQUIRED_FILES)
    for extra in ("02_MANUSCRIPT/README.md", "01_SOURCE/solutions/README.md"):
        if os.path.isfile(os.path.join(ROOT, extra)):
            scan.append(extra)

    for rel in scan:
        if not rel.endswith(".md"):
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as fh:
            body = fh.read()
        for m in re.finditer(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)", body):
            target = m.group(1).split("#")[0]
            if not target:
                continue
            base = os.path.dirname(p)
            resolved = os.path.realpath(os.path.join(base, target))
            # ② depo sınırı — dosyanın varlığından BAĞIMSIZ
            if not (resolved == root_abs or resolved.startswith(root_abs + os.sep)):
                escaped.append("%s → %s" % (rel, target))
                continue
            # ① kırık bağ
            if not os.path.exists(resolved):
                broken.append("%s → %s" % (rel, target))

    rep.check(not escaped,
              "hiçbir bağ deponun dışına çıkmıyor" +
              ("" if not escaped else
               " — SINIR İHLALİ (künyeye çevirin): %s" % escaped[:5]))
    rep.check(not broken,
              "belge içi bağlar çözülüyor" +
              ("" if not broken else " — KIRIK: %s" % broken[:5]))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  DEPO, BELGE VE MANUSCRIPT KORUMASI")
    print("=" * 74)

    rep = Report(args.verbose)
    files = tracked_files()
    if not files:
        rep.warn("git takip listesi boş — depo henüz init edilmemiş olabilir; "
                 "sızıntı denetimleri boş koşuyor")

    check_files(rep)
    check_gate_file(rep)
    check_embedded(rep, files)
    check_manuscript_leak(rep, files)
    check_secrets(rep, files)
    check_doc_links(rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil" % rep.checks)
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "trackedFiles": len(files)},
                      fh, ensure_ascii=False, indent=2)

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
