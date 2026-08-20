#!/usr/bin/env python3
"""
KAPAK SANATI ALIM HATTI — The Great Book of World Games
================================================================================
Kurucunun ürettiği HAM görselleri alır, ölçer, doğrular ve baskıya hazır hâle
getirir. Sanat gelmediyse hattı BOŞ koşar ve öyle söyler.

    HAM → sağlama → inceleme → doğrulama → istemle karşılaştırma
        → yükseltme → normalizasyon → kırpma → terfi

── EFEKTİF DPI GERÇEK BİR SAYIDIR ──────────────────────────────────────
`ASSET_UPSCALING_REPORT.md § 3.1` bu projenin en pahalı yanlış anlamasını
kayda geçirmiştir ve burada mekanikleştirilir:

    Bir dosyaya "300 DPI" etiketi yazmak HİÇBİR ŞEY değiştirmez.
    Basılan şey PİKSEL SAYISIDIR.

    efektif DPI = piksel / fiziksel inç

1024 piksel genişliğindeki bir görsel 8,5 inçlik bir kapakta 120 DPI basar,
üstünde ne yazarsa yazsın. Bu betik etiketi DEĞİL o bölmeyi denetler.

── YÜKSELTME PROJENİN ONAYLI YOLUYLA YAPILIR ───────────────────────────
`ASSET_UPSCALING_REPORT.md § 4.1` — kurulu motor:
    ~/Applications/upscayl-cli/upscayl-bin   (Real-ESRGAN ncnn-vulkan)
İllüstrasyon kapaklar için önerilen model: `digital-art-4x` (§ 6.4).
Yeniden örnekleme (Lanczos vb.) BÜYÜTME SAYILMAZ ve kullanılmaz: piksel
üretmez, var olanı yayar.

── HAM DOSYAYA ASLA YAZILMAZ ───────────────────────────────────────────
Yol haritası § 3 "Görsel hattı": `07_ASSETS/raw/` DEĞİŞMEZ. Bütün çıktılar
`processed/` ve `print/` altına yazılır.

Kullanım:
    cover_artwork.py                 → alım + rapor (yükseltme YAPMAZ)
    cover_artwork.py --upscale       → gerekenleri onaylı hatla yükseltir
    cover_artwork.py --check         → alım raporu güncel mi

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

ENGINE_SYMBOLIC = "~/Applications/upscayl-cli/upscayl-bin"
UPSCAYL = os.path.expanduser(ENGINE_SYMBOLIC)
UPSCAYL_MODEL = "digital-art-4x"     # ASSET_UPSCALING_REPORT § 6.4
UPSCAYL_SCALE = 4
TARGET_PPI = 300
MIN_ACCEPTABLE_PPI = 300
UPSCALED_SUFFIX = "-4x-300dpi"


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def classify(name: str) -> str:
    n = name.lower()
    if "wrap" in n:
        return "wrap"
    if "front" in n:
        return "front"
    if "back" in n:
        return "back"
    return "unknown"


def inspect(path: str) -> dict:
    """Dosyayı AÇAR ve gerçekten ne olduğunu söyler. Ada güvenilmez."""
    rec = {"file": os.path.basename(path), "bytes": os.path.getsize(path),
           "sha256": sha256(path)}
    try:
        from PIL import Image
        with Image.open(path) as im:
            rec["format"] = im.format
            rec["mode"] = im.mode
            rec["widthPx"], rec["heightPx"] = im.size
            rec["aspect"] = round(im.size[0] / im.size[1], 4)
            rec["dpiTag"] = list(im.info.get("dpi", ())) or None
            rec["hasAlpha"] = im.mode in ("RGBA", "LA") or (
                im.mode == "P" and "transparency" in im.info)
    except Exception as exc:
        rec["error"] = "%s: %s" % (type(exc).__name__, exc)
    return rec


def evaluate(rec: dict, geo_pb: dict) -> dict:
    """İstemin sözleşmesiyle KARŞILAŞTIRIR ve efektif DPI'yi HESAPLAR."""
    if "widthPx" not in rec:
        return dict(rec, verdict="UNREADABLE")
    kind = classify(rec["file"])
    a = geo_pb["artworkTarget"]
    if kind == "wrap":
        want_w_in = geo_pb["wrapWidthIn"]
        want_h_in = geo_pb["wrapHeightIn"]
        want_px = (a["widthPx"], a["heightPx"])
    elif kind in ("front", "back"):
        want_w_in = geo_pb["trimWidthIn"] + geo_pb["bleedIn"]
        want_h_in = geo_pb["wrapHeightIn"]
        want_px = (a["frontOnlyWidthPx"], a["frontOnlyHeightPx"])
    else:
        return dict(rec, kind=kind, verdict="UNCLASSIFIED",
                    note="Dosya adı wrap/front/back içermiyor; istem "
                         "sözleşmesindeki adlardan biri kullanılmalı.")

    eff_x = rec["widthPx"] / want_w_in
    eff_y = rec["heightPx"] / want_h_in
    eff = min(eff_x, eff_y)
    want_ratio = want_w_in / want_h_in
    ratio_err = abs(rec["aspect"] - want_ratio) / want_ratio

    problems = []
    if eff < MIN_ACCEPTABLE_PPI:
        problems.append("efektif DPI %.1f < %d" % (eff, MIN_ACCEPTABLE_PPI))
    if ratio_err > 0.02:
        problems.append("en-boy oranı %.4f, istenen %.4f (sapma %.1f%%)"
                        % (rec["aspect"], want_ratio, ratio_err * 100))
    if rec.get("hasAlpha"):
        problems.append("ALFA KANALI VAR — baskı için düzleştirilmeli")
    if rec.get("mode") not in ("RGB", "L", "P", None):
        problems.append("renk kipi %s — sRGB/RGB olmalı" % rec.get("mode"))

    scale_needed = MIN_ACCEPTABLE_PPI / eff if eff else 99
    return dict(rec, kind=kind,
                targetInches=[round(want_w_in, 4), round(want_h_in, 4)],
                targetPx=list(want_px),
                targetAspect=round(want_ratio, 4),
                effectiveDpiX=round(eff_x, 1), effectiveDpiY=round(eff_y, 1),
                effectiveDpi=round(eff, 1),
                scaleFactorNeeded=round(scale_needed, 3),
                upscaleRecommended=eff < MIN_ACCEPTABLE_PPI,
                alreadyUpscaled=UPSCALED_SUFFIX in rec["file"],
                problems=problems,
                verdict="PASS" if not problems else "NEEDS-WORK")


def do_upscale(root, src, ev, verbose=True) -> dict:
    """Onaylı hatla YÜKSELTİR. Ham dosyaya DOKUNMAZ."""
    out_dir = os.path.join(root, "07_ASSETS", "processed", "cover")
    os.makedirs(out_dir, exist_ok=True)
    stem, ext = os.path.splitext(os.path.basename(src))
    dst = os.path.join(out_dir, stem + UPSCALED_SUFFIX + ".png")
    if ev.get("alreadyUpscaled"):
        return {"skipped": "dosya adı zaten -4x-300dpi taşıyor "
                           "(ASSET_UPSCALING_REPORT § 6.2/1)"}
    if not os.path.exists(UPSCAYL):
        return {"error": "yükseltme motoru yok: %s "
                         "(ASSET_UPSCALING_REPORT § 2.2)" % ENGINE_SYMBOLIC}
    cmd = [UPSCAYL, "-i", src, "-o", dst, "-n", UPSCAYL_MODEL,
           "-s", str(UPSCALE_SCALE_ARG), "-g", "0", "-f", "png"]
    if verbose:
        print("     → %s -i <raw> -o <processed> -n %s -s %d -g 0 -f png"
              % (ENGINE_SYMBOLIC, UPSCAYL_MODEL, UPSCALE_SCALE_ARG))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(dst):
        return {"error": (r.stderr or r.stdout or "bilinmeyen hata")[-400:]}
    from PIL import Image
    with Image.open(dst) as im:
        w, h = im.size
        im.save(dst, dpi=(TARGET_PPI, TARGET_PPI))
    tw, th = ev["targetInches"]
    return {"file": os.path.relpath(dst, root),
            "model": UPSCAYL_MODEL, "scale": UPSCALE_SCALE_ARG,
            "originalPx": [ev["widthPx"], ev["heightPx"]],
            "processedPx": [w, h],
            "originalEffectiveDpi": ev["effectiveDpi"],
            "finalEffectiveDpi": round(min(w / tw, h / th), 1),
            "scalingFactor": round(w / ev["widthPx"], 3),
            "method": "Real-ESRGAN ncnn-vulkan (upscayl-bin) + Pillow pHYs "
                      "300 dpi — ASSET_UPSCALING_REPORT § 4.1",
            "sha256": sha256(dst), "bytes": os.path.getsize(dst)}


UPSCALE_SCALE_ARG = UPSCAYL_SCALE


def run(root: str, args) -> int:
    gp = os.path.join(root, "06_REPORTS", "cover-geometry.json")
    if not os.path.exists(gp):
        print("  ⛔ kapak geometrisi yok — önce 04_BUILD/covers.py koşun")
        return 1
    geo = load(gp)
    pb = geo["editions"]["paperback"]

    print("=" * 74)
    print("  KAPAK SANATI ALIM HATTI")
    print("=" * 74)
    print("  hedef  : tam sarım %.4f × %.4f in → %d × %d px @ %d ppi"
          % (pb["wrapWidthIn"], pb["wrapHeightIn"],
             pb["artworkTarget"]["widthPx"], pb["artworkTarget"]["heightPx"],
             TARGET_PPI))
    print("  yöntem : %s · model %s · ölçek %dx"
          % ("upscayl-bin (Real-ESRGAN ncnn-vulkan)", UPSCAYL_MODEL,
             UPSCAYL_SCALE))
    print("  motor  : %s" % ("KURULU ✓ " + ENGINE_SYMBOLIC
                             if os.path.exists(UPSCAYL)
                             else "YOK ⛔ " + ENGINE_SYMBOLIC))

    results = {}
    for area in ("cover", "aplus"):
        d = os.path.join(root, "07_ASSETS", "raw", area)
        os.makedirs(d, exist_ok=True)
        files = [f for f in sorted(os.listdir(d))
                 if not f.startswith(".") and os.path.isfile(os.path.join(d, f))]
        print("\n── 07_ASSETS/raw/%s ── %d dosya" % (area, len(files)))
        recs = []
        for fn in files:
            p = os.path.join(d, fn)
            rec = inspect(p)
            if area == "cover":
                ev = evaluate(rec, pb)
            else:
                ev = dict(rec, kind="aplus", verdict="PASS" if "widthPx" in rec
                          else "UNREADABLE",
                          note="A+ görselleri YÜKSELTİLMEZ: en büyüğü 970 px "
                               "ve her model bundan fazlasını üretir; "
                               "küçültülür.")
            recs.append(ev)
            print("  · %-44s %s" % (fn, ev["verdict"]))
            if "widthPx" in ev:
                print("      %d × %d px · %s · efektif DPI %s"
                      % (ev["widthPx"], ev["heightPx"], ev.get("mode", "?"),
                         ev.get("effectiveDpi", "—")))
            for pr in ev.get("problems", []):
                print("      ⚠ %s" % pr)
            if args.upscale and ev.get("upscaleRecommended"):
                res = do_upscale(root, p, ev)
                ev["upscale"] = res
                if "error" in res:
                    print("      ⛔ yükseltme başarısız: %s" % res["error"])
                elif "skipped" in res:
                    print("      · atlandı: %s" % res["skipped"])
                else:
                    print("      ✓ %d × %d px → efektif DPI %.1f (×%.2f)"
                          % (res["processedPx"][0], res["processedPx"][1],
                             res["finalEffectiveDpi"], res["scalingFactor"]))
        results[area] = recs

    total = sum(len(v) for v in results.values())
    payload = {
        "$comment": [
            "KAPAK/A+ HAM VARLIK ALIMI — ÜRETİLMİŞ DOSYA.",
            "Efektif DPI = piksel / fiziksel inç. Etiket DEĞİL, BÖLME.",
            "Ham dosyalara yazılmaz; çıktı 07_ASSETS/processed/ altındadır.",
        ],
        "generatedAtPhase": "phase6",
        # ⚠ MUTLAK YOL YAZILMAZ. Bu dosya PUBLIC depoda durur ve genişletilmiş
        # bir ev dizini yolu, kurucunun kullanıcı adını depoya koyar. Yol
        # SEMBOLİK biçimde saklanır; araç aynı araçtır.
        "engine": {"path": ENGINE_SYMBOLIC, "present": os.path.exists(UPSCAYL),
                   "model": UPSCAYL_MODEL, "scale": UPSCAYL_SCALE,
                   "authority": "ASSET_UPSCALING_REPORT.md"},
        "targetPpi": TARGET_PPI,
        "geometry": {"wrapIn": [pb["wrapWidthIn"], pb["wrapHeightIn"]],
                     "wrapPx": [pb["artworkTarget"]["widthPx"],
                                pb["artworkTarget"]["heightPx"]],
                     "pageCount": pb["pageCount"],
                     "spineIn": pb["spineWidthIn"]},
        "assets": results,
        "assetCount": total,
        "gate": "OPEN — kurucu sanatı bekleniyor" if total == 0 else "INTAKE",
    }
    dump(os.path.join(root, "06_REPORTS", "cover-artwork-intake.json"), payload)

    print("\n" + "=" * 74)
    if total == 0:
        print("  ⛔ VARLIK KAPISI AÇIK — hiç ham görsel yok.")
        print("     Hat BOŞ koştu. Hiçbir görsel işlenmedi ve işlendiği")
        print("     İDDİA EDİLMİYOR. İstemler:")
        print("       07_ASSETS/IMAGE_PROMPT_LIBRARY.html")
        print("     Kurucu dosyaları şuraya bırakır:")
        print("       07_ASSETS/raw/cover/   ·   07_ASSETS/raw/aplus/")
    else:
        bad = [r["file"] for v in results.values() for r in v
               if r["verdict"] != "PASS"]
        print("  %d varlık alındı · %d tanesi işlem bekliyor"
              % (total, len(bad)))
    print("=" * 74)
    return 0


def run_check(root: str) -> int:
    p = os.path.join(root, "06_REPORTS", "cover-artwork-intake.json")
    if not os.path.exists(p):
        print("  · alım raporu yok — ATLANDI")
        return 0
    rep = load(p)
    errs = []
    for area in ("cover", "aplus"):
        d = os.path.join(root, "07_ASSETS", "raw", area)
        on_disk = {f for f in os.listdir(d)
                   if not f.startswith(".")
                   and os.path.isfile(os.path.join(d, f))} \
            if os.path.isdir(d) else set()
        known = {r["file"] for r in rep["assets"].get(area, [])}
        if on_disk != known:
            errs.append("%s: alım raporu BAYAT (diskte %d, raporda %d)"
                        % (area, len(on_disk), len(known)))
    gp = os.path.join(root, "06_REPORTS", "cover-geometry.json")
    if os.path.exists(gp):
        g = load(gp)["editions"]["paperback"]
        if g["pageCount"] != rep["geometry"]["pageCount"]:
            errs.append("alım raporu %d sayfaya göre, geometri %d sayfa diyor"
                        % (rep["geometry"]["pageCount"], g["pageCount"]))
    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        return 1
    print("  ✓ alım raporu güncel (%d varlık · %s)"
          % (rep["assetCount"], rep["gate"]))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--upscale", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("  ⊘ Pillow yok — varlık alımı ATLANDI")
        return 2
    if args.check:
        return run_check(root)
    return run(root, args)


if __name__ == "__main__":
    sys.exit(main())
