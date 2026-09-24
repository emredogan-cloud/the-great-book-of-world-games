#!/usr/bin/env python3
"""
upscale_master_covers.py — Slice and upscale corrected master covers with Real-ESRGAN x4.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

TOOL = Path("/tmp/claude-1000/-home-emre-Downloads-MY-D-G-TAL-BOOK/9f27e6b0-3cdb-4f66-9d88-e85fcf9e351e/scratchpad/tools/realesrgan-ncnn-vulkan")
MODELS = TOOL.parent / "models"

SRC_DIR = ROOT / "07_ASSETS" / "processed" / "cover"
STD_PNG = SRC_DIR / "print_master_standard_corrected.png"
LP_PNG = SRC_DIR / "print_master_largeprint_corrected.png"
KM_PNG = SRC_DIR / "kindle_master_corrected.png"

OUT_DIR = SRC_DIR / "x4"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TMP_DIR = Path("/tmp/cover_slices")
TMP_DIR.mkdir(parents=True, exist_ok=True)

SC_X4 = Path("/tmp/claude-1000/-home-emre-Downloads-MY-D-G-TAL-BOOK/9f27e6b0-3cdb-4f66-9d88-e85fcf9e351e/scratchpad/x4")


def slice_panels():
    print("=== Slicing corrected master covers ===")
    im_std = Image.open(STD_PNG).convert("RGB")
    assert im_std.size == (1536, 1024), f"Unexpected std size {im_std.size}"
    
    # Front: x 815..1536 (width 721, height 1024)
    front = im_std.crop((815, 0, 1536, 1024))
    front_path = TMP_DIR / "front.png"
    front.save(front_path)
    print(f"  ✓ Saved front slice: {front_path} ({front.size})")

    # Back Std: x 0..700 (width 700, height 1024)
    back_std = im_std.crop((0, 0, 700, 1024))
    back_std_path = TMP_DIR / "back_std.png"
    back_std.save(back_std_path)
    print(f"  ✓ Saved back_std slice: {back_std_path} ({back_std.size})")

    # Back LP: x 0..700 (width 700, height 1024)
    im_lp = Image.open(LP_PNG).convert("RGB")
    assert im_lp.size == (1536, 1024), f"Unexpected lp size {im_lp.size}"
    back_lp = im_lp.crop((0, 0, 700, 1024))
    back_lp_path = TMP_DIR / "back_lp.png"
    back_lp.save(back_lp_path)
    print(f"  ✓ Saved back_lp slice: {back_lp_path} ({back_lp.size})")

    return front_path, back_std_path, back_lp_path


def run_upscale(inp: Path, out: Path):
    print(f"--- Upscaling {inp.name} -> {out.name} ---")
    cmd = [
        str(TOOL),
        "-i", str(inp),
        "-o", str(out),
        "-s", "4",
        "-n", "realesrgan-x4plus",
        "-m", str(MODELS),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("STDERR:", res.stderr)
        raise RuntimeError(f"Upscaling failed for {inp}: {res.stderr}")
    im = Image.open(out)
    print(f"  ✓ Upscaled successfully: {out.name} ({im.size})")


def main():
    if not TOOL.exists():
        sys.exit(f"Tool not found: {TOOL}")
    
    front_p, back_std_p, back_lp_p = slice_panels()

    tasks = [
        (front_p, OUT_DIR / "GAMES-front-x4.png"),
        (back_std_p, OUT_DIR / "GAMES-back-std-x4.png"),
        (back_lp_p, OUT_DIR / "GAMES-back-lp-x4.png"),
        (KM_PNG, OUT_DIR / "GAMES-kindle-x4.png"),
    ]

    for inp, out in tasks:
        run_upscale(inp, out)

    # Also update scratchpad x4 directory
    if SC_X4.exists():
        shutil.copy2(OUT_DIR / "GAMES-front-x4.png", SC_X4 / "GAMES-front-x4.png")
        shutil.copy2(OUT_DIR / "GAMES-back-std-x4.png", SC_X4 / "GAMES-back-x4.png")
        shutil.copy2(OUT_DIR / "GAMES-back-lp-x4.png", SC_X4 / "GAMES-back-lp-x4.png")
        shutil.copy2(OUT_DIR / "GAMES-kindle-x4.png", SC_X4 / "GAMES-kindle-x4.png")
        print("  ✓ Mirrored upscaled panels to scratchpad/x4")


if __name__ == "__main__":
    main()
