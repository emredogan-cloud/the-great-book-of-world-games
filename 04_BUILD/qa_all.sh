#!/usr/bin/env bash
# =============================================================================
# THE GREAT BOOK OF WORLD GAMES — BÜTÜN KALİTE KAPILARI
# =============================================================================
# CI'ın çalıştırdığı komutların BİREBİR AYNISI. Push etmeden önce yerelde
# koşturun; yeşilse CI de yeşil olur.
#
#   ./04_BUILD/qa_all.sh              mevcut kapı seviyesiyle (.gate)
#   ./04_BUILD/qa_all.sh phase1       kapıyı yükselterek dene
#   ./04_BUILD/qa_all.sh --fix        üretilen belgeleri tazeleyerek
#
# Hafif kapıların hiçbiri venv gerektirmez; hepsi Python standart
# kütüphanesiyle koşar. Görsel/dizgi işleri Pillow ve reportlab ister ve
# yoksa ATLANIR (çıkış 2) — bu bir kalite düşüşü DEĞİLDİR.
# =============================================================================
set -uo pipefail

BUILD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$BUILD")"
TESTS="$ROOT/05_TESTS"
cd "$ROOT"

GATE=""
FIX=0
for arg in "$@"; do
  case "$arg" in
    --fix) FIX=1 ;;
    phase0|phase1|phase2|phase3|phase4|phase5|release) GATE="$arg" ;;
    *) echo "bilinmeyen argüman: $arg" >&2; exit 2 ;;
  esac
done

# Kapı seviyesi .gate dosyasındadır; yalnızca AÇIKÇA verilirse o kazanır.
# (Bestiarium'da --fix kapıyı draft'a düşürüyordu — yani belgeleri tazeleyen
# koşu açılmış kapıları HİÇ denetlemiyordu.)
if [ -z "$GATE" ]; then
  GATE="$( [ -f .gate ] && tr -d '[:space:]' < .gate || echo phase0 )"
fi

PY="${PYTHON:-python3}"
VENV_PY="$PY"
[ -x "$BUILD/.venv/bin/python" ] && VENV_PY="$BUILD/.venv/bin/python"

FAILED=()
SKIPPED=()

run () {
  local name="$1"; shift
  echo
  echo "──────────────────────────────────────────────────────────────────────"
  echo "▸ $name"
  echo "──────────────────────────────────────────────────────────────────────"
  if "$@"; then return 0; else FAILED+=("$name"); return 1; fi
}

run_optional () {
  local name="$1"; shift
  echo
  echo "──────────────────────────────────────────────────────────────────────"
  echo "▸ $name"
  echo "──────────────────────────────────────────────────────────────────────"
  "$@"
  case $? in
    0) ;;
    2) echo "ATLANDI: bağımlılık yok — pip install -r 04_BUILD/requirements.txt"
       SKIPPED+=("$name") ;;
    *) FAILED+=("$name") ;;
  esac
}

echo "════════════════════════════════════════════════════════════════════════"
echo "  THE GREAT BOOK OF WORLD GAMES · KALİTE KAPILARI · kapı: $GATE"
echo "════════════════════════════════════════════════════════════════════════"

if [ "$FIX" = "1" ]; then
  echo "▸ üretilen belgeler tazeleniyor…"
  [ -f 04_BUILD/update_docs.py ] && $PY 04_BUILD/update_docs.py >/dev/null || true
fi

# ── ÜRETİLEN ENVANTER ───────────────────────────────────────────────────────
# Bu EN BAŞTA koşar: bayat bir indeksle koşan bütün kapılar yanlış veriyi
# denetler ve yeşil yanabilir. Kaynak parçalardır, indeks türetilmiştir.
[ -f 04_BUILD/build_index.py ] && \
  run "envanter güncel"         $PY 04_BUILD/build_index.py --check

# ── YAPILANDIRMA VE VERİ ────────────────────────────────────────────────────
run "veri bütünlüğü ve kapsam"  $PY 04_BUILD/validate_spec.py --gate "$GATE" \
                                   --json 06_REPORTS/spec-validation.json
run "depo ve belge bütünlüğü"   $PY 04_BUILD/validate_structure.py \
                                   --json 06_REPORTS/structure.json

# ── KAPILARIN KENDİ TESTİ — en önemlisi ────────────────────────────────────
run "KAPILARIN KENDİ TESTİ"     $PY 05_TESTS/selftest.py

# ── FAZ 1'DE DOĞACAK KAPILAR ───────────────────────────────────────────────
# Bu betikler henüz yok. Var olduklarında bu satırlar canlanır.
# Bir kapının VARLIĞI yetmez, KOŞMASI gerekir (World Myths K18).
[ -f 04_BUILD/validate_research.py ] && \
  run "araştırma kayıtları"     $PY 04_BUILD/validate_research.py \
                                   --json 06_REPORTS/research.json
[ -f 04_BUILD/qa_taxonomy.py ] && \
  run "tasnif bütünlüğü"        $PY 04_BUILD/qa_taxonomy.py \
                                   --json 06_REPORTS/qa-taxonomy.json
[ -f 04_BUILD/qa_rules.py ] && \
  run "KURAL BÜTÜNLÜĞÜ"         $PY 04_BUILD/qa_rules.py \
                                   --json 06_REPORTS/qa-rules.json
[ -f 04_BUILD/score_candidates.py ] && \
  run "aday seçim modeli"       $PY 04_BUILD/score_candidates.py \
                                   --json 06_REPORTS/candidate-scores.json
[ -f 04_BUILD/validate_scope.py ] && \
  run "KAPSAM VE PİLOT KİLİDİ"  $PY 04_BUILD/validate_scope.py \
                                   --json 06_REPORTS/scope-lock.json

# ── FAZ 2'DE DOĞACAK KAPILAR ───────────────────────────────────────────────
[ -f 04_BUILD/qa_playable.py ] && \
  run "OYNANABİLİRLİK"          $PY 04_BUILD/qa_playable.py \
                                   --json 06_REPORTS/qa-playable.json
[ -f 04_BUILD/qa_length.py ] && \
  run "kelime bandı"            $PY 04_BUILD/qa_length.py \
                                   --json 06_REPORTS/qa-length.json
[ -f 04_BUILD/qa_voice.py ] && \
  run "ses ve yasak kalıp"      $PY 04_BUILD/qa_voice.py \
                                   --json 06_REPORTS/qa-voice.json
[ -f 04_BUILD/qa_echo.py ] && \
  run "tekrar taraması"         $PY 04_BUILD/qa_echo.py \
                                   --json 06_REPORTS/qa-echo.json
[ -f 04_BUILD/qa_drift.py ] && \
  run "üslup sürüklenmesi"      $PY 04_BUILD/qa_drift.py \
                                   --json 06_REPORTS/qa-drift.json
[ -f 04_BUILD/qa_language_split.py ] && \
  run "DİL AYRIMI (TR ↛ EN)"    $PY 04_BUILD/qa_language_split.py \
                                   --json 06_REPORTS/qa-language-split.json
# Dizgi ölçümü reportlab ister ve `run_optional` sözleşmesine uyar:
# çıkış 2 = bağımlılık yok = ATLANDI, kusur DEĞİL (karar K7).
[ -f 04_BUILD/calibrate_pages.py ] && \
  run_optional "gerçek dizgi ölçümü" $PY 04_BUILD/calibrate_pages.py --check

# ── FAZ 3+ KAPILARI ────────────────────────────────────────────────────────
[ -f 04_BUILD/qa_crossref.py ] && \
  run "çapraz referans"         $PY 04_BUILD/qa_crossref.py \
                                   --json 06_REPORTS/qa-crossref.json
[ -f 04_BUILD/qa_diagram.py ] && \
  run "diyagram ↔ kural uyumu"  $PY 04_BUILD/qa_diagram.py \
                                   --json 06_REPORTS/qa-diagram.json

# ── FAZ 4 KAPILARI ─────────────────────────────────────────────────────────
# Kuyruk SIRASI bir kapıdır: engelli bir oyun erişilebilir bir oyunun önüne
# geçemez (kurucu § 4). Manuscript depoda yok, kuyruğun kendisi var.
[ -f 04_BUILD/build_queue.py ] && \
  run "ÜRETİM KUYRUĞU SIRASI"   $PY 04_BUILD/build_queue.py --check
# Manuscript depoda YOKTUR; bu kapı orada BOŞ KOŞAR ve 0 döner. Yerelde ise
# prozanın kendisini denetler — beş öğe, üç soru, beyan, kaynak, dış test.
[ -f 04_BUILD/qa_manuscript.py ] && \
  run "MANUSCRIPT BÜTÜNLÜĞÜ"    $PY 04_BUILD/qa_manuscript.py \
                                   --json 06_REPORTS/qa-manuscript.json

# ── KURUCU ARAŞTIRMA KAYDI ─────────────────────────────────────────────────
# Kayıt ÜRETİLİR ve burada BAYAT MI diye denetlenir. Bayat bir boşluk kaydı,
# kurucuyu ÇÖZÜLMÜŞ bir engeli araştırmaya gönderir — yani yanlış olmakla
# kalmaz, insan emeğini çöpe atar.
#
# Kapı ayrıca bir ÖRTÜŞME denetimi yapar: kapsam = yazılmış + yazılabilir +
# engelli. Bir oyun yazıldığı hâlde kayıttan düşmezse burası kırmızı yanar.
[ -f 04_BUILD/build_gap_register.py ] && \
  run "KURUCU BOŞLUK KAYDI"     $PY 04_BUILD/build_gap_register.py --check
# Teslim dizini yoksa BOŞ KOŞAR ve 0 döner (§ 17: teslim gelmeden sonraki
# aşamalar çalıştırılmaz).
[ -f 04_BUILD/founder_delivery_ingest.py ] && \
  run "kurucu teslim alımı"     $PY 04_BUILD/founder_delivery_ingest.py --check

# ── FAZ 5 KAPILARI ─────────────────────────────────────────────────────────
# Arka madde ÜRETİLİR (build_backmatter.py) ve burada DENETLENİR. Üretilmiş
# bir dosya, denetlenmedikçe elle yazılmış bir dosyadan güvenli değildir:
# üreteç yanlış kova hesaplarsa çıktı kendi içinde TUTARLI görünür.
[ -f 04_BUILD/build_backmatter.py ] && \
  run "arka madde üretimi"      $PY 04_BUILD/build_backmatter.py
[ -f 04_BUILD/qa_index.py ] && \
  run "ARKA MADDE VE ÜÇ İNDEKS" $PY 04_BUILD/qa_index.py \
                                   --json 06_REPORTS/qa-index.json

# ── ÜRETİM MODELİ ──────────────────────────────────────────────────────────
[ -f 04_BUILD/page_budget.py ] && \
  run "sayfa bütçesi"           $PY 04_BUILD/page_budget.py \
                                   --json 06_REPORTS/page-budget.json
[ -f 04_BUILD/editions.py ] && \
  run "sürüm ve telif modeli"   $PY 04_BUILD/editions.py \
                                   --json 06_REPORTS/editions.json

# ── GÖRSEL VE ÜRETİM HATTI (Pillow / reportlab ister) ──────────────────────
[ -f 04_BUILD/asset_inventory.py ] && \
  run_optional "ham varlık envanteri"   $VENV_PY 04_BUILD/asset_inventory.py --check
[ -f 04_BUILD/interior.py ] && \
  run_optional "iç blok güncel"         $VENV_PY 04_BUILD/interior.py --check
[ -f 04_BUILD/epub.py ] && \
  run_optional "Kindle EPUB güncel"     $VENV_PY 04_BUILD/epub.py --check
[ -f 04_BUILD/covers.py ] && \
  run_optional "kapak üretimi güncel"   $VENV_PY 04_BUILD/covers.py --check
[ -f 04_BUILD/metadata.py ] && \
  run "KDP metadata paketi"     $PY 04_BUILD/metadata.py --check

# ── ÜRETİLEN BELGELER BAYAT MI ─────────────────────────────────────────────
[ -f 04_BUILD/update_docs.py ] && \
  run "üretilen belgeler güncel" $PY 04_BUILD/update_docs.py --check

# ── ÖZET ───────────────────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════════════════"
if [ ${#SKIPPED[@]} -gt 0 ]; then
  echo "  ⊘ ${#SKIPPED[@]} kapı atlandı (bağımlılık yok):"
  for s in "${SKIPPED[@]}"; do echo "     · $s"; done
fi
if [ ${#FAILED[@]} -eq 0 ]; then
  echo "  ✅ BÜTÜN KAPILAR YEŞİL · kapı seviyesi: $GATE"
  echo "════════════════════════════════════════════════════════════════════════"
  exit 0
fi
echo "  ⛔ ${#FAILED[@]} KAPI KIRMIZI"
for f in "${FAILED[@]}"; do echo "     · $f"; done
echo "════════════════════════════════════════════════════════════════════════"
echo
echo "  Kalite düştü. Düzeltilmeden ilerleme yok."
exit 1
