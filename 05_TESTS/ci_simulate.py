#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CI'ı YERELDE koştur — komutları TARİF ETMEZ, iş akışından OKUR.

NEDEN VAR: faz 6'da CI iki kez kırıldı ve ikisi de yerelde YEŞİL görünüyordu.
Sebep basitti — elle yazılmış "simülasyon" iş akışının koştuğu komutları
tahmin ediyordu. `qa_all.sh` kapıları bayraksız çağırıyor; CI ise hepsini
`--verbose --json` ile çağırıyor. İki betik `--verbose` kabul etmiyordu:
argparse çıkış 2 verdi, iş kırmızı yandı, kapı hiç koşmadı.

İki kaynak varsa biri bayatlar. Bu betik `.github/workflows/validate.yml`
dosyasındaki `run:` bloklarının KENDİSİNİ çalıştırır.

DEPO GİBİ DAVRANIR: yalnızca `git ls-files` dosyalarını geçici bir ağaca
kopyalar. Ticari manuscript depoda yoktur (.gitignore § ①), yani metin
kapıları CI'da boş koşar — simülasyon da öyle koşmalıdır, yoksa CI'ın
GÖRMEDİĞİ bir şeyi doğrulamış oluruz.

    python3 05_TESTS/ci_simulate.py [--keep]
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WF = os.path.join(ROOT, ".github", "workflows", "validate.yml")


def steps():
    """(iş, adım adı, kabuk gövdesi) — yaml'sız, girintiye dayalı."""
    src = open(WF, encoding="utf-8").read().splitlines()
    out, job, name, body, ind = [], "?", None, None, 0
    for i, ln in enumerate(src):
        m = re.match(r"^  ([a-z0-9_-]+):\s*$", ln)
        if m:
            job = m.group(1)
        m = re.match(r"^(\s*)- name:\s*(.+?)\s*$", ln)
        if m:
            if name and body:
                out.append((job, name, "\n".join(body)))
            name, body, ind = m.group(2), None, len(m.group(1))
            continue
        m = re.match(r"^\s*run:\s*\|?\s*$", ln)
        if m and name and body is None:
            body = []
            continue
        m = re.match(r"^\s*run:\s+(\S.*)$", ln)
        if m and name and body is None:
            body = [m.group(1)]
            continue
        if body is not None:
            if ln.strip() == "":
                body.append("")
            elif len(ln) - len(ln.lstrip()) > ind:
                body.append(ln)
            else:
                out.append((job, name, "\n".join(body)))
                name, body = None, None
    if name and body:
        out.append((job, name, "\n".join(body)))
    return out


def dedent(t):
    ls = [l for l in t.splitlines() if l.strip()]
    if not ls:
        return t
    n = min(len(l) - len(l.lstrip()) for l in ls)
    return "\n".join(l[n:] if len(l) > n else l for l in t.splitlines())


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keep", action="store_true",
                    help="geçici ağacı silme (hata ayıklama)")
    ap.add_argument("--gate", default=None, help="kapı seviyesi (öntanımlı .gate)")
    args = ap.parse_args()

    gate = args.gate
    if gate is None:
        gp = os.path.join(ROOT, ".gate")
        gate = open(gp, encoding="utf-8").read().strip() if os.path.exists(gp) else "phase1"

    files = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                           capture_output=True, text=True).stdout.split("\0")
    files = [f for f in files if f]
    td = tempfile.mkdtemp(prefix="gbwg-ci-")
    work = os.path.join(td, "repo")
    for f in files:
        d = os.path.join(work, os.path.dirname(f))
        os.makedirs(d, exist_ok=True)
        shutil.copy2(os.path.join(ROOT, f), os.path.join(work, f))

    print("=" * 74)
    print("  CI SİMÜLASYONU · komutlar validate.yml'den OKUNDU")
    print("=" * 74)
    print("  izlenen dosya: %d · kapı: %s" % (len(files), gate))
    print("  manuscript ağaçta: %s (CI'da da böyle olmalı)"
          % ("EVET ⚠" if os.path.exists(
              os.path.join(work, "02_MANUSCRIPT", "book.json")) else "hayır"))

    failed, ran = [], 0
    for job, name, body in steps():
        cmd = dedent(body)
        # iş akışı ifadelerini yerel değerle doldur
        cmd = re.sub(r"\$\{\{\s*needs\.gate\.outputs\.level\s*\}\}", gate, cmd)
        if "${{" in cmd:            # doldurulamayan ifade — atla, SESSİZCE değil
            print("  ⊘ %-52s (iş akışı ifadesi çözülemedi)" % name[:52])
            continue
        # RUNNER KURULUMU kapı değildir. `pip install` yerelde PEP 668
        # (externally-managed-environment) yüzünden düşer ama runner'da
        # temiz bir sanal ortama kurar. Bunu kırmızı saymak simülasyonu
        # kullanılamaz yapar; SESSİZCE atlamak ise yalan olur.
        if re.search(r"^\s*(pip3?|python3? -m pip)\s+install", cmd, re.M):
            print("  ⊘ %-52s (runner kurulumu — yerelde atlanır)" % name[:52])
            continue
        ran += 1
        r = subprocess.run(["bash", "-e", "-c", cmd], cwd=work,
                           capture_output=True, text=True)
        if r.returncode == 0:
            print("  ✓ %s" % name)
        else:
            failed.append(name)
            print("  ✗ %s  → EXIT %d" % (name, r.returncode))
            tail = (r.stdout + r.stderr).strip().splitlines()[-8:]
            for l in tail:
                print("        %s" % l[:150])

    if not args.keep:
        shutil.rmtree(td, ignore_errors=True)
    else:
        print("\n  ağaç: %s" % work)

    print("\n" + "=" * 74)
    if failed:
        print("  ⛔ %d/%d ADIM KIRMIZI" % (len(failed), ran))
        for f in failed:
            print("     · %s" % f)
        print("=" * 74)
        return 1
    print("  ✅ %d adımın hepsi yeşil — CI bu commit'te geçmeli" % ran)
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
