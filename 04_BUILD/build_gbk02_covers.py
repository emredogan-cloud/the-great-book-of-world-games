#!/usr/bin/env python3
"""
build_gbk02_covers.py — Build the complete canonical covers for GBK-02.

Produces:
  1. Paperback wrap PDF & JPG (8.5 x 11 in, 172 pp, spine 0.3873 in, wrap 17.6373 x 11.25 in)
  2. Hardcover wrap PDF & JPG (8.25 x 11 in, 172 pp, spine 0.6080 in, wrap 18.6830 x 12.4170 in)
  3. Large Print wrap PDF & JPG (8.5 x 11 in, 272 pp, spine 0.6125 in, wrap 17.8625 x 11.25 in)
  4. Kindle front cover JPG (1600 x 2560 px, RGB, 300 DPI)

Features:
  - Preserves Founder artwork composition, textures, compass, olive branches, and border.
  - Sourced from surgically corrected master covers (63 games, 45 cultures, VALICE PRESS).
  - Large Print back cover features 16pt blurb.
  - Safe margins: PB safe box (0.375 in + tol), HC safe box (0.716 in outer, 0.844 in hinge).
  - Spine ground extracted from comp's luminance percentile with typography cleanly set.
  - Barcode plates (#F6F3EC / #B08F4E frame) applied via barcode_plate.py (verified minLum >= 240).
  - PDFs font-stripped (zero unembedded Base-14 fonts) to guarantee 100% KDP compliance.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMMON = ROOT.parent.parent / "COMMON-AREA" / "covers"
if not COMMON.exists():
    COMMON = Path("/home/emre/Downloads/MY-DİGİTAL-BOOK/COMMON-AREA/covers")
sys.path.insert(0, str(COMMON))

import barcode_plate
from founder_wrap_2026_09_12 import (
    DPI, BLEED, HC_BOARD, HC_SAFE_IN,
    flatten, place, wrap_safe, build_spine, barcode_zone, save_pdf, srgb
)

# Colors and fonts
CREAMY, GOLD = (238, 233, 222), (198, 166, 100)
INKD, INKA = (54, 38, 24), (122, 86, 42)

PB_SAFE_IN = 0.125 + 0.250            # 0.375 in
PB_FRONT_SPINE_IN = 0.400             # front text off spine
PB_TOL_IN = 0.030
PB_BACK_SPINE_IN = 0.062 + PB_TOL_IN  # 0.092 in
HINGE_PAD_GAMES = 0.394 + 0.450       # 0.844 in

# Source paths
SRC_DIR = ROOT / "07_ASSETS" / "processed" / "cover"
X4_DIR = SRC_DIR / "x4"

COMP_STD = SRC_DIR / "print_master_standard_corrected.png"
COMP_LP = SRC_DIR / "print_master_largeprint_corrected.png"
COMP_KM = SRC_DIR / "kindle_master_corrected.png"

BAND_A, BAND_B = 700, 815
TITLE = "THE GREAT BOOK OF WORLD GAMES"
AUTHOR = "EMRE DOĞAN"
META_TITLE = "The Great Book of World Games — 63 Games from 4,600 Years of Human Play"
META_AUTHOR = "Emre Doğan"


def build_kindle() -> dict:
    print("=== Building Kindle Cover ===")
    src_k = Image.open(COMP_KM)
    k4 = Image.open(X4_DIR / "GAMES-kindle-x4.png")
    kim, kcrop = place(flatten(k4), 1600, 2560, 0.5, max_crop_in=2.0)
    
    out_dir = ROOT / "08_OUTPUT" / "KINDLE"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_jpg = out_dir / "GreatBookOfWorldGames_cover_kindle.jpg"
    kim.save(out_jpg, "JPEG", quality=95, subsampling=0, dpi=(DPI, DPI), icc_profile=srgb())
    print(f"  ✓ Saved Kindle cover: {out_jpg} ({out_jpg.stat().st_size} bytes)")

    return {
        "file": str(out_jpg.relative_to(ROOT)),
        "px": [1600, 2560],
        "bytes": out_jpg.stat().st_size,
        "suppliedPx": list(src_k.size),
        "realUpscale": round(1600 / src_k.size[0], 3),
        "crop": kcrop,
    }


def build_print_wraps() -> dict:
    print("=== Building Print Wraps ===")
    comp_std = flatten(Image.open(COMP_STD))
    comp_lp = flatten(Image.open(COMP_LP))

    KF = Image.open(X4_DIR / "GAMES-front-x4.png")
    KB_std = Image.open(X4_DIR / "GAMES-back-std-x4.png")
    KB_lp = Image.open(X4_DIR / "GAMES-back-lp-x4.png")

    ay = 0.72
    mc = 0.25
    ink, accent = INKD, INKA
    dark = False

    specs = {
        "PAPERBACK": {
            "trim": (8.5, 11.0),
            "pages": 172,
            "cal": 0.002252,
            "wrap": (17.6373, 11.25),
            "hc": False,
            "spine_in": 0.3873,
            "back_src": KB_std,
            "comp_spine": comp_std,
            "out_pdf": ROOT / "08_OUTPUT" / "PAPERBACK" / "GreatBookOfWorldGames_cover_paperback.pdf",
            "out_jpg": ROOT / "08_OUTPUT" / "PAPERBACK" / "GreatBookOfWorldGames_cover_paperback.jpg",
        },
        "HARDCOVER": {
            "trim": (8.25, 11.0),
            "pages": 172,
            "cal": 0.0025,
            "wrap": (18.6830, 12.4170),
            "hc": True,
            "spine_in": 0.6080,
            "back_src": KB_std,
            "comp_spine": comp_std,
            "out_pdf": ROOT / "08_OUTPUT" / "HARDCOVER" / "GreatBookOfWorldGames_cover_hardcover.pdf",
            "out_jpg": ROOT / "08_OUTPUT" / "HARDCOVER" / "GreatBookOfWorldGames_cover_hardcover.jpg",
        },
        "LARGEPRINT": {
            "trim": (8.5, 11.0),
            "pages": 272,
            "cal": 0.002252,
            "wrap": (17.8625, 11.25),
            "hc": False,
            "spine_in": 0.6125,
            "back_src": KB_lp,
            "comp_spine": comp_lp,
            "out_pdf": ROOT / "08_OUTPUT" / "LARGEPRINT" / "GreatBookOfWorldGames_cover_largeprint.pdf",
            "out_jpg": ROOT / "08_OUTPUT" / "LARGEPRINT" / "GreatBookOfWorldGames_cover_largeprint.jpg",
        },
    }

    results = {}

    for fmt, f in specs.items():
        print(f"\n--- Processing {fmt} ---")
        pages = f["pages"]
        W, H = f["wrap"]
        spine_in = f["spine_in"]
        pw, ph = int(round(W * DPI)), int(round(H * DPI))
        sp_px = int(round(spine_in * DPI))
        panel_w = (pw - sp_px) // 2
        panel_w_f = pw - sp_px - panel_w

        KB = f["back_src"]
        comp = f["comp_spine"]

        wrap = Image.new("RGB", (pw, ph), (0, 0, 0))

        if f["hc"]:
            pad = int(round(HC_SAFE_IN * DPI))
            pad_i = int(round(HINGE_PAD_GAMES * DPI))
            back, bcrop = wrap_safe(KB, panel_w, ph, pad, pad_i, pad, ay, mc, "left", dark)
            front, fcrop = wrap_safe(KF, panel_w_f, ph, pad, pad_i, pad, ay, mc, "right", dark)
        else:
            pad = int(round((PB_SAFE_IN + PB_TOL_IN) * DPI))
            pad_b = int(round(PB_BACK_SPINE_IN * DPI))
            pad_f = int(round((PB_FRONT_SPINE_IN + PB_TOL_IN) * DPI))
            back, bcrop = wrap_safe(KB, panel_w, ph, pad, pad_b, pad, ay, mc, "left", dark)
            front, fcrop = wrap_safe(KF, panel_w_f, ph, pad, pad_f, pad, ay, mc, "right", dark)

        wrap.paste(back, (0, 0))
        wrap.paste(front, (pw - panel_w_f, 0))

        spine, snote = build_spine(
            comp, BAND_A, BAND_B, sp_px, ph, pages, spine_in,
            TITLE, AUTHOR, ink, accent, dark,
            HC_SAFE_IN if f["hc"] else 0.55
        )
        wrap.paste(spine, (panel_w, 0))

        # Apply barcode plate
        fmt_key = "hardcover" if f["hc"] else "paperback"
        trim_w = f["trim"][0]
        wrap_with_plate, plate_rec = barcode_plate.apply_plate(wrap, fmt_key, trim_w, DPI)
        print(f"  ✓ Barcode plate applied: minLum={plate_rec['minLuminance']}, meanLum={plate_rec['meanLuminance']}, std={plate_rec['stdLuminance']}")

        # Save files
        f["out_pdf"].parent.mkdir(parents=True, exist_ok=True)
        save_pdf(wrap_with_plate, f["out_pdf"], W, H, META_TITLE, META_AUTHOR)
        wrap_with_plate.save(f["out_jpg"], "JPEG", quality=94, subsampling=0, dpi=(DPI, DPI), icc_profile=srgb())
        print(f"  ✓ Saved PDF: {f['out_pdf']} ({f['out_pdf'].stat().st_size} bytes)")
        print(f"  ✓ Saved JPG: {f['out_jpg']} ({f['out_jpg'].stat().st_size} bytes)")

        results[fmt] = {
            "file": str(f["out_pdf"].relative_to(ROOT)),
            "jpg": str(f["out_jpg"].relative_to(ROOT)),
            "pages": pages,
            "trimIn": list(f["trim"]),
            "wrapIn": [W, H],
            "wrapPx": [pw, ph],
            "spineIn": spine_in,
            "spinePx": sp_px,
            "spine": snote,
            "backCrop": bcrop,
            "frontCrop": fcrop,
            "barcodePlate": plate_rec,
            "bytes": f["out_pdf"].stat().st_size,
        }

    return results


def main():
    rec = {
        "book": "GBK-02",
        "slug": "the-great-book-of-world-games",
        "canon": {"games": 63, "cultures": 45, "years": 4600, "brand": "VALICE PRESS"},
        "formats": {},
    }
    rec["formats"]["KINDLE"] = build_kindle()
    rec["formats"].update(build_print_wraps())

    qa_dir = ROOT / "06_REPORTS"
    qa_dir.mkdir(parents=True, exist_ok=True)
    qa_file = qa_dir / "cover-build-canonical.json"
    qa_file.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    print(f"\n✓ Cover build complete. QA record written to {qa_file}")


if __name__ == "__main__":
    main()
