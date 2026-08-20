#!/usr/bin/env python3
"""
KDP ÖN DENETİMİ — The Great Book of World Games
================================================================================
Amazon'un yükleme sırasında yaptığı denetimlerin **yerelde koşan** karşılığı.
Ajan gerçek KDP Previewer'ın yerine geçemez ve geçtiğini iddia etmez; ama
Previewer'ın reddedeceği şeylerin çoğu burada, yüklemeden ÖNCE bulunabilir.

Denetimler:

  ① FONT        — her font GÖMÜLÜ mü. Gömülmemiş tek font dosyayı reddettirir.
                  (İlk koşuda ÜÇ tane bulundu: reportlab'ın Helvetica taban
                  fontu, diyagram efsanesinin Times-Roman'ı ve ZapfDingbats.)
  ② SAYFA ÖLÇÜSÜ— her sayfa trim ölçüsünde ve HEPSİ aynı ölçüde mi.
  ③ MÜREKKEP    — hiçbir mürekkep güvenli alanın dışına taşmıyor mu.
                  Sayfa RASTERLENİR ve gerçek mürekkep kutusu ÖLÇÜLÜR;
                  bir çerçeve hesabına güvenilmez.
  ④ DİL         — basılan metinde belge dili (Türkçe) var mı.
  ⑤ SAYFA SAYISI— KDP bandında mı, çift mi.
  ⑥ GÖRSEL      — raster görsel varsa çözünürlüğü yeterli mi (bu kitapta
                  diyagramlar VEKTÖRDÜR ve raster yoktur).
  ⑦ BOŞ SAYFA   — beklenmedik boş sayfa (art arda ikiden fazla) var mı.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
IN = 72.0
SAFE_IN = 0.25          # bleed yoksa mürekkebin trim'e en yakın olabileceği
# ⚠ TÜRKÇEYE ÖZGÜ harfler. ü · ö · ç Almanca ve Fransızcada da vardır ve
# kitabın künyelerinde MEŞRU olarak geçer ("Internationales Archiv für
# Ethnographie"). İlk sürüm onları da işaretledi ve tek bir Alman dergi
# adı yüzünden kapıyı kırmızı yaktı. Bir kapı yanlış yerde ısırırsa,
# gerçek bir sızıntıyı bulduğunda da inanılmaz.
TR_CHARS = set("ışğİŞĞ")
TR_WORDS = {"ve", "bir", "bu", "için", "ile", "olan", "oyuncu", "kural",
            "sayfa", "kaynak", "doğrulanmış", "yazılmış", "değil", "kayıt"}
# Ticari metinde MEŞRU olarak geçen özel adlar — dil taramasının dışında.
TR_ALLOW = {"doğan", "vâliçe"}


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


class Report:
    def __init__(self):
        self.fail, self.warn, self.n = [], [], 0

    def check(self, cond, label):
        self.n += 1
        if cond:
            return True
        self.fail.append(label)
        print("  ✗ %s" % label)
        return False


def brief(items, k=5):
    items = list(items)
    if not items:
        return ""
    return " — %s%s" % (", ".join(str(x) for x in items[:k]),
                        " …(+%d)" % (len(items) - k) if len(items) > k else "")


def looks_turkish(word: str) -> bool:
    w = word.strip(".,;:()[]\"'—·").lower()
    if not w or w in TR_ALLOW:
        return False
    if any(ch in TR_CHARS for ch in w):
        return True
    return w in TR_WORDS


def check_fonts(pdf: str, rep: Report) -> list:
    if not shutil.which("pdffonts"):
        rep.warn.append("pdffonts yok — font gömme denetimi ATLANDI")
        print("  ⚠ pdffonts yok — font gömme denetimi ATLANDI")
        return []
    out = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
    rows, bad = [], []
    for line in out.splitlines()[2:]:
        if not line.strip():
            continue
        cols = line.split()
        if len(cols) < 5:
            continue
        name, emb = cols[0], cols[-4]
        rows.append({"name": name, "embedded": emb == "yes"})
        if emb != "yes":
            bad.append(name)
    rep.check(not bad, "her font GÖMÜLÜ (%d font)" % len(rows) + brief(bad))
    return rows


def check_geometry(pdf: str, trim_w_in, trim_h_in, rep: Report) -> dict:
    out = subprocess.run(["pdfinfo", "-l", "100000", pdf],
                         capture_output=True, text=True).stdout
    sizes = set(re.findall(r"Page\s+\d+\s+size:\s+([\d.]+) x ([\d.]+) pts", out))
    if not sizes:
        m = re.search(r"Page size:\s+([\d.]+) x ([\d.]+) pts", out)
        if m:
            sizes = {(m.group(1), m.group(2))}
    want = (round(trim_w_in * IN, 2), round(trim_h_in * IN, 2))
    got = {(round(float(a), 2), round(float(b), 2)) for a, b in sizes}
    rep.check(len(got) == 1, "bütün sayfalar AYNI ölçüde" + brief(sorted(got)))
    rep.check(got == {want}, "sayfa ölçüsü trim ile aynı (istenen %.2f × %.2f pt)"
              % want + brief(sorted(got)))
    m = re.search(r"Pages:\s+(\d+)", out)
    return {"pages": int(m.group(1)) if m else 0, "sizes": sorted(got)}


def check_ink(pdf: str, pages: int, trim_w_in, trim_h_in, rep: Report,
              dpi: int = 72) -> dict:
    """Her sayfayı rasterler ve GERÇEK mürekkep kutusunu ölçer."""
    try:
        from PIL import Image, ImageChops
    except ImportError:
        print("  ⚠ Pillow yok — mürekkep kutusu ATLANDI")
        rep.warn.append("Pillow yok")
        return {}
    import tempfile
    worst = {"leftIn": 99.0, "rightIn": 99.0, "topIn": 99.0, "bottomIn": 99.0}
    offenders, blanks = [], []
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-gray", "-png", pdf,
                        os.path.join(td, "p")], check=True,
                       capture_output=True)
        files = sorted(os.listdir(td))
        for fn in files:
            n = int(re.search(r"(\d+)\.png$", fn).group(1))
            im = Image.open(os.path.join(td, fn)).convert("L")
            bbox = ImageChops.invert(im).getbbox()
            if bbox is None:
                blanks.append(n)
                continue
            W, H = im.size
            left = bbox[0] / dpi
            top = bbox[1] / dpi
            right = (W - bbox[2]) / dpi
            bottom = (H - bbox[3]) / dpi
            worst["leftIn"] = min(worst["leftIn"], left)
            worst["rightIn"] = min(worst["rightIn"], right)
            worst["topIn"] = min(worst["topIn"], top)
            worst["bottomIn"] = min(worst["bottomIn"], bottom)
            if min(left, right, top, bottom) < SAFE_IN - 1.0 / dpi:
                offenders.append("s.%d (%.3f in)"
                                 % (n, min(left, right, top, bottom)))
    rep.check(not offenders,
              "mürekkep güvenli alanda (trim'e ≥ %.2f in)" % SAFE_IN
              + brief(offenders))
    runs, run = [], []
    for n in blanks:
        if run and n == run[-1] + 1:
            run.append(n)
        else:
            if len(run) > 2:
                runs.append("%d–%d" % (run[0], run[-1]))
            run = [n]
    if len(run) > 2:
        runs.append("%d–%d" % (run[0], run[-1]))
    rep.check(not runs, "art arda ikiden fazla boş sayfa yok" + brief(runs))
    return {"worstMarginIn": {k: round(v, 3) for k, v in worst.items()},
            "blankPages": blanks}


def check_language(pdf: str, rep: Report) -> dict:
    out = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                         capture_output=True, text=True).stdout
    hits = sorted({w for w in re.findall(r"[^\s]+", out) if looks_turkish(w)})
    rep.check(not hits, "basılan metinde belge dili YOK" + brief(hits))
    words = len(re.findall(r"\S+", out))
    return {"extractedWords": words, "turkishHits": hits}


def check_images(pdf: str, rep: Report) -> dict:
    if not shutil.which("pdfimages"):
        return {}
    out = subprocess.run(["pdfimages", "-list", pdf],
                         capture_output=True, text=True).stdout
    rows = [l for l in out.splitlines()[2:] if l.strip()]
    low = []
    for l in rows:
        c = l.split()
        try:
            xppi, yppi = int(c[12]), int(c[13])
        except (IndexError, ValueError):
            continue
        if min(xppi, yppi) < 300:
            low.append("%s (%d ppi)" % (c[0], min(xppi, yppi)))
    rep.check(not low, "raster görsel ≥300 ppi (%d görsel)" % len(rows)
              + brief(low))
    return {"rasterImages": len(rows)}



def manuscript_absent(root: str) -> bool:
    """Ticari manuscript depoda YOKTUR (karar K12).

    CI taze bir klonda koşar ve orada `02_MANUSCRIPT/book.json` bulunmaz.
    Bu bir kusur DEĞİLDİR ve kapı orada BOŞ KOŞAR. Bir kapının CI'da
    kırmızı yanması, kusuru olduğu için olmalıdır; verinin orada olmaması
    için değil."""
    return not os.path.exists(os.path.join(root, "02_MANUSCRIPT", "book.json"))


def run(root: str, args) -> int:
    if manuscript_absent(root):
        print("  · ticari manuscript bu depoda yok — KDP ön denetimi ATLANDI "
              "(CI'da beklenen)")
        return 0
    cfg = load(os.path.join(root, "project_config.json"))
    editions = []
    for ed in ("paperback", "hardcover"):
        p = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if os.path.exists(p):
            editions.append((ed, load(p)))
    if not editions:
        print("  · iç blok üretilmemiş — ön denetim ATLANDI")
        return 0

    rep = Report()
    out = {}
    print("=" * 74)
    print("  KDP ÖN DENETİMİ")
    print("=" * 74)
    for ed, meta in editions:
        pdf = os.path.join(root, meta["file"])
        if not os.path.exists(pdf):
            rep.check(False, "%s PDF yok" % ed)
            continue
        print("\n── %s ── %s" % (ed.upper(), os.path.basename(pdf)))
        r = {}
        r["fonts"] = check_fonts(pdf, rep)
        geo = check_geometry(pdf, meta["trim"]["widthIn"],
                             meta["trim"]["heightIn"], rep)
        r["geometry"] = geo
        r["ink"] = check_ink(pdf, geo["pages"], meta["trim"]["widthIn"],
                             meta["trim"]["heightIn"], rep)
        r["language"] = check_language(pdf, rep)
        r["images"] = check_images(pdf, rep)

        cost = cfg["production"]["kdpPrintCost"][
            "paperbackLargeTrimBW" if ed == "paperback"
            else "hardcoverLargeTrimBW"]
        n = geo["pages"]
        rep.check(cost["minPages"] <= n <= cost["maxPages"],
                  "%s sayfa sayısı KDP bandında (%d ∈ [%d, %d])"
                  % (ed, n, cost["minPages"], cost["maxPages"]))
        rep.check(n % 2 == 0, "%s sayfa sayısı ÇİFT (%d)" % (ed, n))
        r["pageCount"] = n
        w = r["ink"].get("worstMarginIn", {})
        if w:
            print("  · en dar mürekkep payı: sol %.3f · sağ %.3f · üst %.3f "
                  "· alt %.3f in" % (w["leftIn"], w["rightIn"], w["topIn"],
                                     w["bottomIn"]))
        print("  · çıkarılan kelime: %d · raster görsel: %d"
              % (r["language"]["extractedWords"], r["images"].get("rasterImages", 0)))
        out[ed] = r

    print("\n" + "=" * 74)
    if rep.fail:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.fail), rep.n))
        for f in rep.fail:
            print("     · %s" % f)
    else:
        print("  ✅ %d denetim yeşil · KDP ön denetimi geçti" % rep.n)
        print("     ⚠ Bu, Amazon KDP Previewer'ın YERİNE GEÇMEZ. Previewer "
              "kurucu tarafından açılır.")
    print("=" * 74)
    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"checks": rep.n, "failed": rep.fail,
                       "warnings": rep.warn, "editions": out},
                      fh, ensure_ascii=False, indent=1)
    return 1 if rep.fail else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    for tool in ("pdfinfo", "pdftoppm", "pdftotext"):
        if not shutil.which(tool):
            print("  ⊘ %s yok — KDP ön denetimi ATLANDI" % tool)
            return 2
    return run(os.path.abspath(args.root), args)


if __name__ == "__main__":
    sys.exit(main())
