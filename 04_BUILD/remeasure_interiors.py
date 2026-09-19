#!/usr/bin/env python3
"""
remeasure_interiors.py — re-take the interior build record after a post-process.

WHY THIS EXISTS
`interior.py` writes `06_REPORTS/interior-<edition>.json` at the moment it
finishes: page count, byte size, SHA-256. That record is then the input to
`covers.py` (spine arithmetic) and to `handoff.py` (the upload handbook and the
SHA256SUMS the Founder checks against KDP).

But interior.py is NOT the last step. The companion leaf — the page carrying the
QR code that turns an Amazon buyer into a Valice reader — is spliced in
afterwards, by `Valice-Press-Site/scripts/factory/build-companion-pages.mjs`,
which lives in a different repository. It replaces one page and rewrites the
file. The page count is unchanged; the bytes and the hash are not.

So after every splice the book's own record described a file that no longer
existed, and `handoff.py` said so:

    ✗ paperback iç bloğu kayıttaki sağlamayla uyuşmuyor

That message is correct and the gate is right to refuse. The fix is not to
loosen the gate — it is to take the measurement again, from the file that will
actually be uploaded.

WHAT IT CHANGES, AND NOTHING MORE
  sha256, bytes, and pageCount, each read from the PDF on disk.

Everything else in the record — trim, margins, page kinds, the pagemap, the
spread analysis — describes the typesetting, which a one-page splice does not
touch. If the page COUNT has moved, that is not a splice: this refuses and says
so, because a changed page count changes the spine and must go back through
covers.py rather than being quietly absorbed here.

Usage:
    python3 04_BUILD/remeasure_interiors.py [--root DIR] [--check]

Exit codes:  0 = records match the files (or were updated)   1 = refused
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
EDITIONS = ("paperback", "hardcover", "largeprint")


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def page_count(path: str) -> int:
    out = subprocess.run(["pdfinfo", path], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"^Pages:\s+(\d+)", out, re.M).group(1))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true", help="report drift, write nothing")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    rc, changed = 0, 0
    print("=" * 74)
    print("  İÇ BLOK KAYDI — YENİDEN ÖLÇÜM")
    print("=" * 74)
    for ed in EDITIONS:
        rp = os.path.join(root, "06_REPORTS", f"interior-{ed}.json")
        if not os.path.exists(rp):
            print(f"  · {ed:11} kayıt yok — atlandı")
            continue
        with open(rp, encoding="utf-8") as fh:
            rec = json.load(fh)
        fp = os.path.join(root, rec["file"])
        if not os.path.exists(fp):
            print(f"  ⛔ {ed:11} dosya yok: {rec['file']}")
            rc = 1
            continue

        real_sha, real_bytes, real_pages = sha256(fp), os.path.getsize(fp), page_count(fp)
        if real_pages != rec["pageCount"]:
            print(f"  ⛔ {ed:11} SAYFA SAYISI DEĞİŞMİŞ {rec['pageCount']} → {real_pages}.")
            print(f"     Bu bir ekleme/çıkarma, bir yerleştirme değil. Sırt genişliği "
                  f"değişti; covers.py'den geçmeden burada yutulamaz.")
            rc = 1
            continue
        if real_sha == rec["sha256"] and real_bytes == rec["bytes"]:
            print(f"  ✓ {ed:11} kayıt dosyayla aynı ({real_pages} s.)")
            continue
        if args.check:
            print(f"  ✗ {ed:11} kayıt BAYAT — sha {rec['sha256'][:12]} ≠ {real_sha[:12]}")
            rc = 1
            continue
        rec["sha256"], rec["bytes"] = real_sha, real_bytes
        rec.setdefault("$remeasured", []).append({
            "on": "2026-09-19",
            "why": "companion leaf spliced in by Valice-Press-Site/scripts/factory/"
                   "build-companion-pages.mjs after interior.py finished",
            "pageCount": real_pages,
            "sha256": real_sha,
        })
        with open(rp, "w", encoding="utf-8") as fh:
            json.dump(rec, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        changed += 1
        print(f"  ✓ {ed:11} yeniden ölçüldü ({real_pages} s. · {real_bytes/1024:.1f} KB · "
              f"sha {real_sha[:12]}…)")
    print("=" * 74)
    if changed:
        print(f"  {changed} kayıt güncellendi. covers.py ve handoff.py yeniden çalıştırılmalı.")
    print("=" * 74)
    return rc


if __name__ == "__main__":
    sys.exit(main())
