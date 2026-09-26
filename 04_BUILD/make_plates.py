#!/usr/bin/env python3
"""
PLATES — derive the print and Kindle files of every game's illustration
================================================================================
Reads 01_SOURCE/plates.json (one explicit record per game) and writes

  07_ASSETS/plates_print/<gameId>.jpg   greyscale, 1200 px wide, 3:2 — the
                                        print interiors are black ink only
  07_ASSETS/plates_kindle/<gameId>.jpg  colour (if the source is colour),
                                        1000 px wide, quality 80 — small,
                                        because KDP charges delivery per MB

A record may carry "crop": [x0, y0, x1, y1] (source pixels) to cut the image
to 3:2; a public-domain page scan is always cropped to its figure. Kinds:
ai-generated · public-domain · cc0 · drawn (a board rendered by boards.py from the
entry's own diagram data) — see 07_ASSETS/plates/pd/README.md and drawn/README.md.

The build REFUSES: a pending-replacement record, a missing source, and two
records whose source images are identical (the 2026 Jan-ken defect: a plate
that was a byte-for-byte copy of another game's).

Exit codes: 0 built · 1 refused
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def fit_3x2(im, crop=None):
    if crop:
        im = im.crop(tuple(crop))
    w, h = im.size
    target = 1.5
    if abs(w / h - target) > 0.01:
        if w / h > target:            # too wide: trim the sides
            nw = int(round(h * target))
            x0 = (w - nw) // 2
            im = im.crop((x0, 0, x0 + nw, h))
        else:                          # too tall: trim top and bottom evenly
            nh = int(round(w / target))
            y0 = (h - nh) // 2
            im = im.crop((0, y0, w, y0 + nh))
    return im


def main():
    from PIL import Image, ImageOps
    reg = json.load(open(os.path.join(ROOT, "01_SOURCE", "plates.json"), encoding="utf-8"))["plates"]
    errs, seen = [], {}
    for gid, rec in reg.items():
        if rec.get("kind") == "pending-replacement":
            errs.append("%s: plate still pending replacement — %s" % (gid, rec.get("why", "")))
            continue
        src = os.path.join(ROOT, rec["source"])
        if not os.path.exists(src):
            errs.append("%s: source missing: %s" % (gid, rec["source"]))
            continue
        h = sha256(src)
        if h in seen:
            errs.append("DUPLICATE PLATE: %s and %s use the same source image" % (seen[h], gid))
            continue
        seen[h] = gid
    if errs:
        for e in errs:
            print("  ✗ %s" % e)
        return 1
    os.makedirs(os.path.join(ROOT, "07_ASSETS", "plates_print"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "07_ASSETS", "plates_kindle"), exist_ok=True)
    for gid, rec in reg.items():
        im = Image.open(os.path.join(ROOT, rec["source"]))
        im = ImageOps.exif_transpose(im).convert("RGB")
        im = fit_3x2(im, rec.get("crop"))
        pr = im.convert("L")
        if rec.get("kind") != "ai-generated":
            pr = ImageOps.autocontrast(pr, cutoff=0.5)
        pr = pr.resize((1200, 800), Image.LANCZOS)
        pr.save(os.path.join(ROOT, rec["print"]), "JPEG", quality=88, optimize=True, dpi=(300, 300))
        kd = im.resize((1000, 667), Image.LANCZOS)
        kd.save(os.path.join(ROOT, rec["kindle"]), "JPEG", quality=80, optimize=True, progressive=True)
    tot = sum(os.path.getsize(os.path.join(ROOT, r["kindle"])) for r in reg.values())
    print("  ✓ %d plates · Kindle set %.1f MB" % (len(reg), tot / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
