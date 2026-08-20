#!/usr/bin/env python3
"""
KAPAK ÜRETECİ — The Great Book of World Games
================================================================================
Sırt genişliğini, tam sarım geometrisini ve güvenli alanları **ölçülen sayfa
sayısından** hesaplar; kurucu sanatı geldiğinde tam sarım kapağı basar.

── SIRT SAYFA SAYISINDAN GELİR ─────────────────────────────────────────
Yol haritası Faz 6 § 8 bunu bir SIRA kuralı yapar:

    Kapak kapısı iç blok kapısından SONRA koşar: sayfa sayısı değişirse
    sırt kayar ve eski kapak GEÇERSİZ olur.

Bu yüzden burada hiçbir sayfa sayısı gömülü DEĞİLDİR. Kaynak tek:
`06_REPORTS/interior-<edition>.json § pageCount` — ki o da `interior.py`ın
SAYDIĞI değerdir, modelin tahmin ettiği değil.

── VARLIK KAPISI ───────────────────────────────────────────────────────
Kapak SANATI kurucu tarafından üretilir (§ 11). Bu betik sanat yokken de
koşar ve GEOMETRİYİ üretir; kompozisyonu YAPMAZ ve yaptığını iddia etmez.
Sanat `07_ASSETS/raw/cover/` altına düştüğünde `--build` devreye girer.

── TİPOGRAFİ ───────────────────────────────────────────────────────────
Kapak yazısı DETERMİNİSTİK ve VEKTÖRDÜR (§ 14): sanatın üstüne beyaz kutu
konmaz, yazı rasterlenmez. Aynı girdi her koşuda byte-byte aynı PDF verir.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
IN = 72.0

# ── KDP GEOMETRİ SABİTLERİ ───────────────────────────────────────────────
# Amazon.com · KDP yardım sayfalarının yayımladığı değerler.
#
# ⚠ CİLTSİZ değerleri KDP'nin kendi formülüdür ve yıllardır sabittir.
# ⚠ CİLTLİ değerleri HİPOTEZDİR ve KURUCU DOĞRULAMASI BEKLER: KDP ciltli
#   kapak şablonunu bir üreteçle verir (kalıp payı, menteşe ve tahta
#   kalınlığı dahil) ve o şablon indirilmeden ciltli kapak BASILMAZ.
#   Bu betik ciltli geometriyi HESAPLAR ama `founderConfirmedTemplate`
#   false olduğu sürece çıktıyı "TEMPLATE PENDING" diye işaretler.
SPINE_PER_PAGE_IN = {
    "paperback": 0.002252,      # beyaz kâğıt · siyah-beyaz mürekkep
    "hardcover": 0.0025,        # HİPOTEZ — şablonla doğrulanacak
}
HARDCOVER_BOARD_IN = 0.06       # HİPOTEZ — tahta payı
BLEED_IN = 0.125
COVER_SAFE_IN = 0.25            # trim kenarından metin/logo uzaklığı
SPINE_TEXT_MIN_PAGES = 79       # KDP: sırta yazı ancak bu sayfadan sonra
BARCODE_W_IN, BARCODE_H_IN = 2.0, 1.2
BARCODE_CLEAR_IN = 0.25


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def geometry(cfg, edition: str, pages: int) -> dict:
    trim = cfg["production"]["trimPaperback" if edition == "paperback"
                             else "trimHardcover"]
    tw, th = trim["w"], trim["h"]
    spine = pages * SPINE_PER_PAGE_IN[edition]
    if edition == "hardcover":
        spine += HARDCOVER_BOARD_IN
    wrap_w = tw * 2 + spine + BLEED_IN * 2
    wrap_h = th + BLEED_IN * 2

    # Sarımın sol kenarından ölçülen bölge sınırları
    back_x0 = BLEED_IN
    spine_x0 = back_x0 + tw
    front_x0 = spine_x0 + spine
    front_x1 = front_x0 + tw

    g = {
        "edition": edition,
        "pageCount": pages,
        "trimWidthIn": tw, "trimHeightIn": th,
        "bleedIn": BLEED_IN, "safeIn": COVER_SAFE_IN,
        "spineWidthIn": round(spine, 4),
        "spinePerPageIn": SPINE_PER_PAGE_IN[edition],
        "spineTextAllowed": pages >= SPINE_TEXT_MIN_PAGES,
        "spineTextMinPages": SPINE_TEXT_MIN_PAGES,
        "wrapWidthIn": round(wrap_w, 4), "wrapHeightIn": round(wrap_h, 4),
        "wrapWidthPt": round(wrap_w * IN, 2),
        "wrapHeightPt": round(wrap_h * IN, 2),
        "zones": {
            "backCover": {"x0": round(back_x0, 4), "x1": round(spine_x0, 4)},
            "spine":     {"x0": round(spine_x0, 4), "x1": round(front_x0, 4)},
            "frontCover": {"x0": round(front_x0, 4), "x1": round(front_x1, 4)},
        },
        "safeZones": {
            "backCopy": {
                "x0": round(back_x0 + COVER_SAFE_IN, 4),
                "x1": round(spine_x0 - COVER_SAFE_IN, 4),
                "y0": round(BLEED_IN + COVER_SAFE_IN, 4),
                "y1": round(BLEED_IN + th - COVER_SAFE_IN, 4)},
            "spineText": {
                "x0": round(spine_x0 + 0.0625, 4),
                "x1": round(front_x0 - 0.0625, 4),
                "y0": round(BLEED_IN + 0.5, 4),
                "y1": round(BLEED_IN + th - 0.5, 4)},
            "frontTitle": {
                "x0": round(front_x0 + COVER_SAFE_IN, 4),
                "x1": round(front_x1 - COVER_SAFE_IN, 4),
                "y0": round(BLEED_IN + th * 0.60, 4),
                "y1": round(BLEED_IN + th - COVER_SAFE_IN, 4)},
            "frontAuthor": {
                "x0": round(front_x0 + COVER_SAFE_IN, 4),
                "x1": round(front_x1 - COVER_SAFE_IN, 4),
                "y0": round(BLEED_IN + COVER_SAFE_IN, 4),
                "y1": round(BLEED_IN + th * 0.18, 4)},
            "barcode": {
                "x0": round(spine_x0 - BARCODE_CLEAR_IN - BARCODE_W_IN, 4),
                "x1": round(spine_x0 - BARCODE_CLEAR_IN, 4),
                "y0": round(BLEED_IN + BARCODE_CLEAR_IN, 4),
                "y1": round(BLEED_IN + BARCODE_CLEAR_IN + BARCODE_H_IN, 4),
                "$note": "KDP barkodu KENDİSİ basar. Bu alan BOŞ ve sade "
                         "bırakılır; sahte barkod çizilmez."},
        },
        "artworkTarget": {
            "$note": "Kurucu sanatının HAM hedefi. 300 ppi baskı standardıdır; "
                     "daha yüksek çözünürlük zarar vermez, düşüğü POD'da "
                     "görünür.",
            "ppi": 300,
            "widthPx": int(round(wrap_w * 300)),
            "heightPx": int(round(wrap_h * 300)),
            "frontOnlyWidthPx": int(round((tw + BLEED_IN) * 300)),
            "frontOnlyHeightPx": int(round(wrap_h * 300)),
        },
    }
    if edition == "hardcover":
        g["$hardcoverWarning"] = (
            "CİLTLİ GEOMETRİ HİPOTEZDİR. KDP ciltli kapak şablonunu bir "
            "üreteçle verir; kalıp payı, menteşe ve tahta kalınlığı oradan "
            "okunur. KURUCU EYLEMİ: şablonu indir, buradaki sırt ve sarım "
            "ölçüleriyle KARŞILAŞTIR, farklıysa project_config.json içine "
            "gerçek değerleri yaz.")
        g["founderConfirmedTemplate"] = bool(
            cfg.get("production", {}).get("hardcoverTemplateConfirmed"))
    return g


def raw_assets(root: str) -> dict:
    d = os.path.join(root, "07_ASSETS", "raw", "cover")
    if not os.path.isdir(d):
        return {"dir": os.path.relpath(d, root), "files": []}
    files = []
    for fn in sorted(os.listdir(d)):
        if fn.startswith("."):
            continue
        p = os.path.join(d, fn)
        if not os.path.isfile(p):
            continue
        rec = {"file": fn, "bytes": os.path.getsize(p), "sha256": sha256(p)}
        try:
            from PIL import Image
            with Image.open(p) as im:
                rec["widthPx"], rec["heightPx"] = im.size
                rec["mode"] = im.mode
                rec["format"] = im.format
        except Exception as exc:
            rec["imageError"] = str(exc)
        files.append(rec)
    return {"dir": os.path.relpath(d, root), "files": files}


def run(root: str, args) -> int:
    cfg = load(os.path.join(root, "project_config.json"))
    out, errs = {}, []
    for ed in ("paperback", "hardcover"):
        p = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if not os.path.exists(p):
            errs.append("%s iç bloğu YOK — sırt hesaplanamaz" % ed)
            continue
        r = load(p)
        g = geometry(cfg, ed, r["pageCount"])
        g["interiorSha256"] = r["sha256"]
        g["interiorFile"] = r["file"]
        out[ed] = g

    assets = raw_assets(root)
    payload = {
        "$comment": [
            "KAPAK GEOMETRİSİ — ÜRETİLMİŞ DOSYA (04_BUILD/covers.py).",
            "Sırt genişliği ÖLÇÜLEN sayfa sayısından gelir; hiçbir sayfa",
            "sayısı gömülü değildir. İç blok değişirse bu dosya BAYATLAR",
            "ve --check kırmızı yanar.",
        ],
        "generatedAtPhase": "phase6",
        "editions": out,
        "rawArtwork": assets,
        "artworkPresent": bool(assets["files"]),
        "compositionStatus": ("BLOCKED — kurucu sanatı yok"
                              if not assets["files"] else "READY"),
    }
    dump(os.path.join(root, "06_REPORTS", "cover-geometry.json"), payload)

    print("=" * 74)
    print("  KAPAK GEOMETRİSİ")
    print("=" * 74)
    for ed, g in out.items():
        print("\n── %s ──" % ed.upper())
        print("  sayfa sayısı        %d  (ÖLÇÜLDÜ, tahmin değil)"
              % g["pageCount"])
        print("  sırt                %.4f in  (%.4f in/sayfa%s)"
              % (g["spineWidthIn"], g["spinePerPageIn"],
                 " + %.2f in tahta" % HARDCOVER_BOARD_IN
                 if ed == "hardcover" else ""))
        print("  tam sarım           %.4f × %.4f in  (%.0f × %.0f px @300 ppi)"
              % (g["wrapWidthIn"], g["wrapHeightIn"],
                 g["artworkTarget"]["widthPx"], g["artworkTarget"]["heightPx"]))
        print("  sırta yazı          %s (KDP eşiği %d sayfa)"
              % ("EVET" if g["spineTextAllowed"] else "HAYIR",
                 g["spineTextMinPages"]))
        z = g["zones"]
        print("  bölgeler (in)       arka %.3f–%.3f · sırt %.3f–%.3f · "
              "ön %.3f–%.3f"
              % (z["backCover"]["x0"], z["backCover"]["x1"],
                 z["spine"]["x0"], z["spine"]["x1"],
                 z["frontCover"]["x0"], z["frontCover"]["x1"]))
        if ed == "hardcover" and not g.get("founderConfirmedTemplate"):
            print("  ⚠ CİLTLİ ŞABLON DOĞRULANMADI — KURUCU EYLEMİ")

    print("\n── HAM KAPAK SANATI ──")
    print("  dizin: %s" % assets["dir"])
    if not assets["files"]:
        print("  ⛔ VARLIK KAPISI: kurucu sanatı YOK.")
        print("     Kapak KOMPOZİSYONU yapılmadı ve yapıldığı İDDİA EDİLMİYOR.")
        print("     İstemler: 07_ASSETS/IMAGE_PROMPT_LIBRARY.html")
    else:
        for f in assets["files"]:
            px = ("%d × %d px" % (f.get("widthPx", 0), f.get("heightPx", 0))
                  if "widthPx" in f else "OKUNAMADI")
            print("  · %-40s %10s  %s" % (f["file"], px, f["sha256"][:12]))

    for e in errs:
        print("  ✗ %s" % e)
    print("=" * 74)
    return 1 if errs else 0


def run_check(root: str) -> int:
    p = os.path.join(root, "06_REPORTS", "cover-geometry.json")
    if not os.path.exists(p):
        print("  · kapak geometrisi üretilmemiş — ATLANDI")
        return 0
    g = load(p)
    errs = []
    for ed, blk in g["editions"].items():
        ip = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if not os.path.exists(ip):
            errs.append("%s iç bloğu kayboldu" % ed)
            continue
        r = load(ip)
        if r["pageCount"] != blk["pageCount"]:
            errs.append("%s: SIRT BAYAT — kapak %d sayfaya göre, iç blok %d "
                        "sayfa (sırt kaydı, kapak GEÇERSİZ)"
                        % (ed, blk["pageCount"], r["pageCount"]))
        if r["sha256"] != blk.get("interiorSha256"):
            errs.append("%s: iç blok DEĞİŞMİŞ — kapak yeniden hesaplanmalı"
                        % ed)
    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        return 1
    print("  ✓ kapak geometrisi iç blokla senkron (%s)"
          % " · ".join("%s %d s. → sırt %.4f in"
                       % (e, b["pageCount"], b["spineWidthIn"])
                       for e, b in g["editions"].items()))
    if not g["artworkPresent"]:
        print("  · VARLIK KAPISI AÇIK: kurucu kapak sanatı bekleniyor "
              "(kompozisyon YAPILMADI)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    if args.check:
        return run_check(root)
    return run(root, args)


if __name__ == "__main__":
    sys.exit(main())
