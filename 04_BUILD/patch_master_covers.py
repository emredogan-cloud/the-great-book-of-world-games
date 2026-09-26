#!/usr/bin/env python3
"""
patch_master_covers.py — Surgical text correction of Founder-provided master covers.

Replaces obsolete claims ("56 games", "39 cultures", "VÂLİÇE PRESS") with
canonical metadata ("63 games", "45 cultures", "VALICE PRESS") while
preserving 100% of the underlying artwork, background texture, and ornaments.
"""
from __future__ import annotations

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PM_SRC = os.path.join(ROOT, "08_OUTPUT", "last-cover-paperback-hardcover-largeprint.png")
KM_SRC = os.path.join(ROOT, "08_OUTPUT", "last-kindle-cover.png")
OUT_DIR = os.path.join(ROOT, "07_ASSETS", "processed", "cover")
os.makedirs(OUT_DIR, exist_ok=True)

CINZEL = "/home/emre/Downloads/MY-DİGİTAL-BOOK/ROADMAP-BOOKS/CODEX-MYTHOLOGICA/07_ASSETS/fonts/static/cinzel-500.ttf"
LIBERATION = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
INK = (26, 21, 16)


def patch_print_master() -> tuple[str, str]:
    """Surgically correct print master for standard and large print editions."""
    im = Image.open(PM_SRC).convert("RGB")
    arr = np.array(im)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)

    # 1. Front Subtitle: '56' at (1000..1023, 202..218)
    b56 = gray[200:220, 998:1025]
    mask[200:220, 998:1025] = cv2.dilate((b56 < 185).astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=2)

    # 2. Front Subtitle: '39' at (1280..1302, 228..244)
    b39 = gray[226:247, 1278:1304]
    mask[226:247, 1278:1304] = cv2.dilate((b39 < 185).astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=2)

    # 3. Front Imprint: 'VÂLİÇE PRESS' at (1080..1320, 961..983)
    bfimp = gray[961:984, 1080:1320]
    mask[961:984, 1080:1320] = cv2.dilate((bfimp < 185).astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=2)

    # 4. Back P1: '56' at (64..85, 179..196) and '39' at (250..271, 179..196)
    bb56 = gray[179:196, 64:85]
    mask[179:196, 64:85] = cv2.dilate((bb56 < 185).astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=2)
    bb39 = gray[179:196, 250:271]
    mask[179:196, 250:271] = cv2.dilate((bb39 < 185).astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=2)

    # 5. Back imprint: the old accented spelling of the imprint name at (60..160, 773..798)
    bbimp = gray[773:798, 60:160]
    mask[773:798, 60:160] = cv2.dilate((bbimp < 185).astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=2)

    # Inpaint all target regions seamlessly with Telea
    inp = cv2.inpaint(arr, mask, 3, cv2.INPAINT_TELEA)
    pm_std = Image.fromarray(inp)
    d = ImageDraw.Draw(pm_std)

    # Draw replacement front subtitle
    f_sub = ImageFont.truetype(LIBERATION, 20)
    d.text((1000, 200), "63", font=f_sub, fill=INK)
    d.text((1280, 227), "45", font=f_sub, fill=INK)

    # Draw replacement front imprint: VALICE PRESS
    f_fimp = ImageFont.truetype(CINZEL, 15)
    fimp_txt = "V A L I C E   P R E S S"
    w_fimp = f_fimp.getlength(fimp_txt)
    d.text((1198 - w_fimp / 2, 965), fimp_txt, font=f_fimp, fill=INK)

    # Draw replacement back p1 numbers
    f_bp1 = ImageFont.truetype(LIBERATION, 15)
    d.text((65, 179), "63", font=f_bp1, fill=INK)
    d.text((251, 179), "45", font=f_bp1, fill=INK)

    # Draw replacement back imprint
    f_bimp = ImageFont.truetype(LIBERATION, 14)
    d.text((64, 775), "Valice Press", font=f_bimp, fill=INK)

    out_std = os.path.join(OUT_DIR, "print_master_standard_corrected.png")
    pm_std.save(out_std, "PNG")

    # Now create Large Print variant (inpaint the 2-page spread sentence and replace with 16pt sentence)
    # Paragraph 1 sentence: "Each game gets two facing pages, so the book lies open on the table and nobody turns a page in the middle of a turn."
    # Located in lines 2-4: y in [200, 268], x in [40, 680]
    arr_lp = np.array(pm_std)
    mask_lp = np.zeros(arr_lp.shape[:2], dtype=np.uint8)
    g_lp = cv2.cvtColor(arr_lp, cv2.COLOR_RGB2GRAY)
    regions = [
        (420, 200, 675, 223),
        (40, 224, 675, 248),
        (40, 249, 130, 268)
    ]
    for (x0, y0, x1, y1) in regions:
        box = g_lp[y0:y1, x0:x1]
        m = (box < 195).astype(np.uint8) * 255
        m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=2)
        mask_lp[y0:y1, x0:x1] = m

    inp_lp = cv2.inpaint(arr_lp, mask_lp, 5, cv2.INPAINT_TELEA)
    pm_lp = Image.fromarray(inp_lp)
    d_lp = ImageDraw.Draw(pm_lp)
    f_lp_body = ImageFont.truetype(LIBERATION, 15)
    lp_s2_l1 = "Set in 16 pt type with"
    lp_s2_l2 = "oversized board diagrams and high-contrast typography, so the rules can be"
    lp_s2_l3 = "read clearly from across the table."
    d_lp.text((425, 203), lp_s2_l1, font=f_lp_body, fill=INK)
    d_lp.text((64, 226), lp_s2_l2, font=f_lp_body, fill=INK)
    d_lp.text((64, 249), lp_s2_l3, font=f_lp_body, fill=INK)

    out_lp = os.path.join(OUT_DIR, "print_master_largeprint_corrected.png")
    pm_lp.save(out_lp, "PNG")

    return out_std, out_lp


def patch_kindle_master() -> str:
    """Surgically correct Kindle master."""
    km = Image.open(KM_SRC).convert("RGB")
    arr = np.array(km)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)

    # 1. Subtitle: '56' at (276..308, 287..310)
    b56 = gray[287:310, 276:308]
    mask[287:310, 276:308] = cv2.dilate((b56 < 185).astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=2)

    # 2. Subtitle: '39' at (603..632, 320..343)
    b39 = gray[320:343, 603:632]
    mask[320:343, 603:632] = cv2.dilate((b39 < 185).astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=2)

    # 3. Imprint: 'VÂLİÇE PRESS' at (375..620, 1442..1467)
    bimp = gray[1442:1467, 375:620]
    mask[1442:1467, 375:620] = cv2.dilate((bimp < 185).astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=2)

    inp = cv2.inpaint(arr, mask, 3, cv2.INPAINT_TELEA)
    km_corr = Image.fromarray(inp)
    d = ImageDraw.Draw(km_corr)

    # Draw replacement subtitle numbers
    f_sub = ImageFont.truetype(LIBERATION, 25)
    d.text((278, 287), "63", font=f_sub, fill=INK)
    d.text((604, 321), "45", font=f_sub, fill=INK)

    # Draw replacement imprint
    f_imp = ImageFont.truetype(CINZEL, 19)
    txt_imp = "V A L I C E   P R E S S"
    w_imp = f_imp.getlength(txt_imp)
    d.text((494 - w_imp / 2, 1445), txt_imp, font=f_imp, fill=INK)

    out_km = os.path.join(OUT_DIR, "kindle_master_corrected.png")
    km_corr.save(out_km, "PNG")
    return out_km


def main():
    print("=== Patching Master Covers ===")
    out_std, out_lp = patch_print_master()
    print("  ✓ Created:", out_std)
    print("  ✓ Created:", out_lp)
    out_km = patch_kindle_master()
    print("  ✓ Created:", out_km)


if __name__ == "__main__":
    main()
