#!/usr/bin/env bash
# ÇIKIŞ 2 = "ATLANDI" konvansiyonu — TEK YERDE.
#
# Bu depodaki kapılar üç şey söyleyebilir:
#   0  yeşil
#   1  KIRMIZI — gerçek kusur
#   2  ATLANDI — koşacak bir şey yoktu (bağımlılık kurulu değil, ya da
#      ticari manuscript bu depoda yok; bkz. .gitignore § ①)
#
# İş akışı bu üçlüyü baştan bilmiyordu ve `|| exit 1` yazıyordu. Sonuç:
# reportlab'sız bir runner'da qa_visual DOĞRU davranıp 2 döndürdü, iş yine
# de kırmızı yandı — CI, KURULU OLMAYAN bir bağımlılığın yokluğuna kızdı.
# Aynı kusur iş akışında ALTI ayrı yerde ayrı ayrı yaşıyordu; her birine
# ayrı `case` bloğu yazmak onu altıya katlamak olurdu.
#
#   bash 04_BUILD/ci_run.sh python3 04_BUILD/qa_visual.py --json out.json
set -u
"$@"
rc=$?
case $rc in
  0) exit 0 ;;
  2) echo "::notice::ATLANDI (bağımlılık/çıktı yok — beklenen): $*"; exit 0 ;;
  *) echo "::error::KIRMIZI (çıkış $rc): $*"; exit "$rc" ;;
esac
