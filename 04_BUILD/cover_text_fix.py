#!/usr/bin/env python3
"""
COVER TEXT — surgical correction of the Founder-approved cover art (2026 recovery)
================================================================================
The approved covers carry their text baked into the artwork. After the recovery
several statements on them were no longer true of the book (two facing pages
per game, 'chance and nerve', full-size templates 'at the back', page-level
sources for every rule set) and the front subtitle carries counts that the
verified taxonomy changes. The artwork is kept; only the text is replaced:

  1. the text of each band is removed (OpenCV Telea inpainting over a mask of
     the dark text strokes, dilated a little) — the parchment, frame, compass
     ornaments, olive branch and board are outside every band and untouched;
  2. the corrected text is set in EB Garamond (SIL OFL) in the colours sampled
     from the original text, at the original line pitch, inside the original
     text column.

Inputs are the upscaled masters in 07_ASSETS/processed/cover/x4/ (never
overwritten); outputs go to 07_ASSETS/processed/cover/x4r/. The text itself is
generated from the measured book (cover_copy()), so a count on the cover can
only be the count in the book.

Usage: cover_text_fix.py [--preview DIR]
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
X4 = os.path.join(ROOT, "07_ASSETS", "processed", "cover", "x4")
OUT = os.path.join(ROOT, "07_ASSETS", "processed", "cover", "x4r")
# EB Garamond (SIL OFL 1.1), bundled in the project: 07_ASSETS/fonts, licence in fonts/licenses
GARAMOND = [p for p in (
    os.path.join(ROOT, "07_ASSETS", "fonts", "EBGaramond-Variable.ttf"),
    os.path.expanduser("~/.fonts/valice/EBGaramond-Variable.ttf"),
) if os.path.exists(p)]
GARAMOND_IT = [p for p in (
    os.path.join(ROOT, "07_ASSETS", "fonts", "EBGaramond-Italic-Variable.ttf"),
    os.path.expanduser("~/.fonts/valice/EBGaramond-Italic-Variable.ttf"),
) if os.path.exists(p)]


def font(size, weight=400, italic=False):
    f = ImageFont.truetype((GARAMOND_IT if italic else GARAMOND)[0], size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def text_mask(arr, box, thresh=150, grow=4, diff=16):
    import cv2
    x0, y0, x1, y1 = box
    g = cv2.cvtColor(arr[y0:y1, x0:x1], cv2.COLOR_RGB2GRAY)
    # grey closing = the paper with every stroke thinner than the kernel removed
    bg = cv2.morphologyEx(g, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)))
    m = ((bg.astype(int) - g.astype(int)) > diff).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=grow)
    full = np.zeros(arr.shape[:2], np.uint8)
    full[y0:y1, x0:x1] = m
    return full


def erase(arr, boxes, grain_boxes=None, feather=24):
    """Remove every trace of the text in `boxes`.

    Inpainting at full resolution leaves ghost strokes (it propagates the
    antialiased fringe). Instead the parchment is modelled: the text mask is
    grown generously, the background is filled at 1/8 resolution (where every
    stroke is sub-pixel and fully masked) and scaled back up, and the paper's
    own grain — the high-pass of clean parchment next to the text — is laid
    back over it. Box edges are feathered so no seam shows."""
    import cv2
    out = arr.astype(np.float32).copy()
    mask = np.zeros(arr.shape[:2], np.uint8)
    for b in boxes:
        # only true strokes: the letters are 140+ levels darker than the paper, the paper's own
        # mottling 20-30 — a lower threshold took the mottling too and replaced whole bands
        mask |= text_mask(arr, b, grow=9, diff=40)
    # grain source: clean parchment high-pass
    gsrc = []
    for gb in (grain_boxes or []):
        x0, y0, x1, y1 = gb
        patch = arr[y0:y1, x0:x1].astype(np.float32)
        hp = patch - cv2.GaussianBlur(patch, (0, 0), 6)
        hp = np.clip(hp, -14, 14)          # grain only: no stroke survives the clip
        gsrc.append(hp)
    rng = np.random.default_rng(7)
    for (x0, y0, x1, y1) in boxes:
        reg = arr[y0:y1, x0:x1]
        m = mask[y0:y1, x0:x1]
        small = cv2.resize(reg, None, fx=0.125, fy=0.125, interpolation=cv2.INTER_AREA)
        # a small pixel is masked if ANY of its 8 × 8 source pixels is text
        ms = cv2.resize(cv2.dilate(m, np.ones((8, 8), np.uint8)), (small.shape[1], small.shape[0]),
                        interpolation=cv2.INTER_NEAREST)
        ms = cv2.dilate(ms, np.ones((3, 3), np.uint8), iterations=1)
        fill = cv2.inpaint(small, ms, 3, cv2.INPAINT_TELEA)
        bg = cv2.resize(fill, (reg.shape[1], reg.shape[0]), interpolation=cv2.INTER_CUBIC).astype(np.float32)
        bg = cv2.GaussianBlur(bg, (0, 0), 3)
        if gsrc:
            tile = np.zeros_like(bg)
            h, w = bg.shape[:2]
            B = int(min(64, min(s.shape[0] for s in gsrc), min(s.shape[1] for s in gsrc)))
            for yy in range(0, h, B):
                for xx in range(0, w, B):
                    src = gsrc[rng.integers(len(gsrc))]
                    sh, sw = src.shape[:2]
                    oy = rng.integers(0, sh - B + 1)
                    ox = rng.integers(0, sw - B + 1)
                    ph, pw = min(B, h - yy), min(B, w - xx)
                    tile[yy:yy + ph, xx:xx + pw] = src[oy:oy + ph, ox:ox + pw]
            bg = bg + tile
        # blend: the old strokes and a soft halo round them are replaced in full; the rest of the
        # band keeps its own parchment. (Filling the whole band read as a lighter rectangle with a
        # straight seam, and feathering the band edges left part-strokes there as grey specks.)
        mk = (mask[y0:y1, x0:x1] > 0).astype(np.float32)
        mk = cv2.dilate(mk, np.ones((5, 5), np.uint8), iterations=2)
        fm = np.clip(cv2.GaussianBlur(mk, (0, 0), 4) * 1.6, 0.0, 1.0)
        fm = np.maximum(fm, (mask[y0:y1, x0:x1] > 0).astype(np.float32))
        fm = fm[..., None]
        out[y0:y1, x0:x1] = out[y0:y1, x0:x1] * (1 - fm) + bg * fm
    return np.clip(out, 0, 255).astype(np.uint8), mask


def sample_colour(arr, box):
    import cv2
    x0, y0, x1, y1 = box
    g = cv2.cvtColor(arr[y0:y1, x0:x1], cv2.COLOR_RGB2GRAY)
    sel = g < np.percentile(g, 6)
    px = arr[y0:y1, x0:x1][sel]
    return tuple(int(v) for v in np.median(px, axis=0))


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def set_block(img, x0, x1, y, blocks, pitch, colours, k=1.0, gap_scale=1.0, dry=False):
    """blocks: [(kind, text)] kind in title/head/body/small/gap; returns final y."""
    d = ImageDraw.Draw(img)
    sizes = {"title": (int(pitch * 1.18), 700), "head": (int(pitch * 0.78 * k), 650),
             "body": (int(pitch * 0.70 * k), 420), "small": (int(pitch * 0.58 * k), 420)}
    pitch = int(pitch * k)
    for kind, text in blocks:
        if kind == "gap":
            y += int(pitch * float(text) * gap_scale)
            continue
        size, wt = sizes[kind]
        f = font(size, wt)
        col = colours[kind]
        if kind == "title":
            wdt = d.textlength(text, font=f)
            if not dry:
                d.text(((x0 + x1) / 2 - wdt / 2, y), text, font=f, fill=col)
            y += int(pitch * 1.55)
            continue
        for ln in wrap(d, text, f, x1 - x0):
            if not dry:
                d.text((x0, y), ln, font=f, fill=col)
            y += pitch if kind != "head" else int(pitch * 1.05)
    return y


def back_cover(src, copy, preview=None):
    im = Image.open(src).convert("RGB")
    arr = np.array(im)
    X0, X1 = 225, 2625
    bands = [(X0, 370, X1, 540), (X0, 700, X1, 1065), (X0, 1160, X1, 1645), (X0, 1740, X1, 2130),
             (X0, 2220, X1, 2600), (X0, 2800, X1, 2995), (X0, 3040, 1400, 3200)]
    colours = {"title": sample_colour(arr, (X0, 384, X1, 523)),
               "head": sample_colour(arr, (X0, 1176, X1, 1257)),
               "body": sample_colour(arr, (X0, 1284, X1, 1629)),
               "small": sample_colour(arr, (X0, 2821, X1, 2979))}
    clean, mask = erase(arr, bands, grain_boxes=[(X0, 1060, X1, 1160), (X0, 1640, X1, 1740),
                                                 (X0, 2130, X1, 2220)])
    img = Image.fromarray(clean)
    pitch = 92
    set_block(img, X0 + 10, X1 - 10, 392, [("title", copy["title"])], pitch, colours)
    upper, lower, cur = [], [], None
    cur = upper
    for kind, text in copy["blocks"]:
        if kind == "ornament2":
            cur = lower
            continue
        cur.append((kind, text))
    # fit the upper block between the two ornaments (y 725 … 2590): the
    # largest type that fits, then the spare space shared between the gaps
    top, bottom = 725, 2590
    best = (1.0, 1.0)
    for k in (1.16, 1.12, 1.08, 1.04, 1.0, 0.96, 0.92):
        h = set_block(img, X0 + 10, X1 - 10, top, upper, pitch, colours, k=k, dry=True) - top
        if h <= bottom - top:
            gaps = sum(float(t) for kd, t in upper if kd == "gap")
            spare = (bottom - top) - h
            gs = 1.0 + (spare / (pitch * k * gaps) if gaps else 0)
            best = (k, min(gs, 2.2))
            break
    k, gs = best
    set_block(img, X0 + 10, X1 - 10, top, upper, pitch, colours, k=k, gap_scale=gs)
    set_block(img, X0 + 10, X1 - 10, 2815, lower, pitch, colours, k=1.0)
    return img, mask, colours


FRONT_BANDS = {
    # file: (ONE erase box holding both subtitle lines, clean-parchment grain boxes) in x4
    # pixels, measured on the masters. One box, not one per line: the old ascenders of the
    # second line cross the gap between the lines, and a seam there keeps fragments of them.
    # Each box clears the compass rule above and the map below.
    "GAMES-front-x4.png": ((690, 792, 2320, 1020),
                           [(760, 762, 1350, 790), (1650, 762, 2250, 790), (380, 800, 650, 990),
                            (2350, 800, 2600, 990)]),
    "GAMES-kindle-x4.png": ((1080, 1130, 2910, 1405),
                            [(1000, 1410, 2800, 1450), (2950, 1150, 3300, 1380)]),
}


def line_boxes(arr, box, n=2, lum_max=85):
    """Ink boxes of the n text lines in `box`: only near-black strokes count (the parchment
    and its texture are far lighter), and the lines are split at the widest empty row gaps."""
    x0, y0, x1, y1 = box
    g = arr[y0:y1, x0:x1].astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)
    m = g < lum_max
    rows = np.where(m.sum(axis=1) > 3)[0]
    cuts = sorted(np.argsort(np.diff(rows))[-(n - 1):]) if n > 1 else []
    groups, start = [], 0
    for c in cuts:
        groups.append(rows[start:c + 1])
        start = c + 1
    groups.append(rows[start:])
    out = []
    for gr in groups:
        cols = np.where(m[gr.min():gr.max() + 1].any(axis=0))[0]
        out.append((x0 + int(cols.min()), y0 + int(gr.min()), x0 + int(cols.max()), y0 + int(gr.max())))
    return out


OPTS = {"features": ["onum"]}           # the artwork sets its figures old-style: 63, 4,600, 45


def run_width(d, runs, size):
    return sum(d.textlength(t, font=font(size, 430, it), **OPTS) for t, it in runs)


def front_cover(src, lines):
    """Replace the subtitle lines under the title. `lines` holds one list of runs
    [(text, italic)] per line. The type size is the one at which the new first line has the
    ink width of the old first line (the new lines have exactly as many characters as the
    old); each line is centred on the old one, with its ascenders on the old ascender line."""
    im = Image.open(src).convert("RGB")
    arr = np.array(im)
    box, grain = FRONT_BANDS[os.path.basename(src)]
    olds = line_boxes(arr, box, n=len(lines))
    col = sample_colour(arr, olds[0])
    clean, mask = erase(arr, [box], grain_boxes=grain, feather=10)
    img = Image.fromarray(clean)
    d = ImageDraw.Draw(img)
    ox0, oy0, ox1, oy1 = olds[0]
    lo, hi = 10.0, 400.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if run_width(d, lines[0], int(round(mid))) < (ox1 - ox0):
            lo = mid
        else:
            hi = mid
    size = int(round(lo))
    placed = []
    for (bx0, by0, bx1, by1), runs in zip(olds, lines):
        w = run_width(d, runs, size)
        x = (bx0 + bx1) / 2 - w / 2
        top = min(d.textbbox((0, 0), t, font=font(size, 430, it), **OPTS)[1] for t, it in runs if t.strip())
        y = by0 - top
        for t, it in runs:
            f = font(size, 430, it)
            d.text((x, y), t, font=f, fill=col, **OPTS)
            x += d.textlength(t, font=f, **OPTS)
        placed.append({"oldInk": [bx0, by0, bx1, by1], "newWidth": round(w)})
    return img, {"colour": col, "sizePx": size, "lines": placed}


def subtitle_lines(root, kindle=False):
    m = json.load(open(os.path.join(root, "02_MANUSCRIPT", "frontmatter.json"), encoding="utf-8"))["measured"]
    years = "{:,}".format(m["oldestGameAgeYears"])
    if kindle:
        line1 = [("%d " % m["games"], False), ("games from", True), (" %s years of human play" % years, False)]
    else:
        line1 = [("%d games from %s years of human play" % (m["games"], years), False)]
    line2 = [("Rules, boards and stories from %d cultures" % m["cultures"], False)]
    return [line1, line2]


def cover_copy(root, edition):
    fm = json.load(open(os.path.join(root, "02_MANUSCRIPT", "frontmatter.json"), encoding="utf-8"))
    m = fm["measured"]
    import build_frontmatter as bf
    games, cultures = m["games"], m["cultures"]
    import backmatter_text as bt
    tpl = len({gid for t in bt.TEMPLATES for gid in t.get("games", [])})
    p1 = {"standard": "%d traditional games from %d cultures, from the royal graves of Ur to a South African "
                      "playground — set out so you can play them tonight. Every game opens with its "
                      "board beside its rules, so the book lies open on the table while you play."
                      % (games, cultures),
          "largeprint": "%d traditional games from %d cultures, from the royal graves of Ur to a South African "
                        "playground — set out so you can play them tonight, in clear 16-point type "
                        "with large board diagrams." % (games, cultures)}[edition]
    return {"title": "A reference book you play from.",
            "blocks": [("body", p1), ("gap", "0.55"),
                       ("head", "Sorted by how they work, not by where they are from."),
                       ("body", "Seven families — sowing, hunt and siege, race home, line and territory, "
                                "the war board, chance and scoring, and games without a board. Put that "
                                "way, the mancala pages of Ghana, Sri Lanka and Buganda sit together, and "
                                "you can watch six cultures solve the problem of chess six different ways."),
                       ("gap", "0.55"),
                       ("head", "Honest about what is known."),
                       ("body", "Every rule set names the work it was read from, with the pages or, for a "
                                "modern rulebook, the section. Where a record is incomplete, the entry says so "
                                "and shows what has been reconstructed. A section at the back lists game origin "
                                "stories that are widely repeated and not supported by the record."),
                       ("gap", "0.55"),
                       ("head", "Inside: what to use instead of what — buttons, coins, dried beans, an egg box."),
                       ("body", "Numbered rules, one action to a line, and a worked turn for every game. "
                                "Full-size boards for %s of the games at the back, to photocopy. Almost "
                                "nothing in this book has to be bought." % bf.words_for(tpl)),
                       ("ornament2", ""),
                       # No author line here: the one-liner once printed on this cover is the invented
                       # bio the Founder replaced on 2026-09-02 (project_config.json founder.authorBio$why);
                       # the canonical bio is printed in full on the About the Author page.
                       ("small", "Valice Press")]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preview", default=None)
    a = ap.parse_args()
    sys.path.insert(0, HERE)
    os.makedirs(OUT, exist_ok=True)
    for ed, fn in (("standard", "GAMES-back-std-x4.png"), ("largeprint", "GAMES-back-lp-x4.png")):
        img, mask, cols = back_cover(os.path.join(X4, fn), cover_copy(ROOT, ed))
        img.save(os.path.join(OUT, fn.replace("-x4", "-x4r")))
        if a.preview:
            img.resize((700, 1024)).save(os.path.join(a.preview, "prev-" + fn))
        print("  ✓ %s re-set · colours %s" % (fn, cols))
    for fn, kindle in (("GAMES-front-x4.png", False), ("GAMES-kindle-x4.png", True)):
        img, rep = front_cover(os.path.join(X4, fn), subtitle_lines(ROOT, kindle))
        img.save(os.path.join(OUT, fn.replace("-x4", "-x4r")))
        if a.preview:
            w, h = img.size
            img.resize((700, int(700 * h / w))).save(os.path.join(a.preview, "prev-" + fn))
        print("  ✓ %s subtitle re-set · %s" % (fn, rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
