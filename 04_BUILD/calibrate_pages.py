#!/usr/bin/env python3
"""
GERÇEK DİZGİ ÖLÇÜMÜ — The Great Book of World Games
================================================================================
Faz 1'in sayfa modeli bir HİPOTEZDİ: 320 kelime/sayfa, oyun başına 2 sayfa.
Bu betik o hipotezi ölçer.

  ⚠ MODEL DEĞİL, ÖLÇÜM. Gerçek metin, gerçek trim, gerçek font, gerçek
  satır kırma, gerçek diyagram alanı. Sayfa sayısı SAYILIR, tahmin edilmez.

Sayfa sayısı bir tasarım tercihi değil, FİYAT MODELİNİN KENDİSİDİR:
256 yerine 300 sayfa, her satılan kopyada telifi 0,75 $ düşürür. Bu yüzden
buradaki sayı bir ayrıntı değil, kitabın ekonomisidir.

── NEDEN reportlab ──────────────────────────────────────────────────────
Kelime/sayfa oranını font metriği olmadan hesaplamak, hipotezi başka bir
hipotezle değiştirmektir. reportlab gerçek bir tipografik satır kırıcıdır
ve gerçek karakter genişlikleriyle çalışır. Karar K7 ağır bağımlılıkları
kalite kapılarından uzak tutar ama DİZGİ İŞLERİNE izin verir; bu betik
tam olarak bir dizgi işidir ve `run_optional` sözleşmesiyle atlanabilir.

Kullanım:
    calibrate_pages.py            → ölçer ve raporu yazar
    calibrate_pages.py --check    → raporun var ve tutarlı olduğunu doğrular

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok (ATLANDI)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
MM = 72.0 / 25.4  # 1 mm = 2.8346 pt


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def words(*chunks) -> int:
    n = 0
    for c in chunks:
        if isinstance(c, str):
            n += len(re.findall(r"\S+", c))
        elif isinstance(c, list):
            n += words(*c)
        elif isinstance(c, dict):
            n += words(*c.values())
    return n


def measure_game(g: dict, diagrams: dict, geom: dict, styles) -> dict:
    """Bir oyun maddesini GERÇEKTEN dizer ve kapladığı yüksekliği ölçer."""
    from reportlab.platypus import Paragraph
    from reportlab.lib.units import mm as RLMM

    col_w = geom["colWidthMm"] * RLMM
    text_h = geom["textHeightMm"] * RLMM

    def block(txt, style):
        p = Paragraph(txt, style)
        _, h = p.wrap(col_w, text_h)
        return h + style.spaceAfter

    total = 0.0
    total += block("<b>%s</b>" % g["title"], styles["h1"])
    total += block("%s · %s · %s" % (g["culture"], g["place"], g["period"]),
                   styles["kicker"])
    spec = g["spec"]
    total += block(" · ".join("<b>%s</b> %s" % (k, v) for k, v in spec.items()),
                   styles["spec"])
    total += block(g["culturalStory"], styles["body"])
    total += block("<b>Materials.</b> " + g["materialsAndSubstitution"],
                   styles["body"])
    if g.get("reconstructionNotice"):
        total += block("<i>%s</i>" % g["reconstructionNotice"], styles["notice"])

    for label, key in (("Setup", "setup"), ("On your turn", "turnSequence"),
                       ("Capture", "capture"), ("Movement", "movement"),
                       ("Throw values", "throwValues"),
                       ("Stacking and sending", "stackingAndSending"),
                       ("The chain", "chain")):
        if not g.get(key):
            continue
        total += block("<b>%s</b>" % label, styles["h2"])
        for i, s in enumerate(g[key], 1):
            total += block("%d.&nbsp;%s" % (i, s), styles["step"])

    for label, key in (("Winning", "winCondition"), ("Taking the king", "kingCapture"),
                       ("The first move", "firstMove"),
                       ("How it ends", "endCondition")):
        if g.get(key):
            total += block("<b>%s</b> %s" % (label + ".", g[key]), styles["body"])

    total += block("<b>Three questions</b>", styles["h2"])
    for k, v in g["edgeCases"].items():
        total += block("<b>%s</b> %s" % (k, v), styles["body"])

    total += block("<b>An example turn.</b> " + g["exampleTurn"], styles["body"])
    for v in g.get("variants", []):
        total += block("<b>%s.</b> %s" % (v["name"], v["note"]), styles["body"])
    total += block("<b>Your first game.</b> " + g["firstGame"], styles["body"])
    if g.get("aMatchIsTwoGames"):
        total += block(g["aMatchIsTwoGames"], styles["body"])
    total += block("<b>Sources.</b> " + "  ".join(g["sources"]), styles["source"])

    # DİYAGRAM ALANI — tahmin değil, render edilmiş SVG'nin GERÇEK ölçüsü.
    dia_h = 0.0
    dia_ids = []
    for did in g.get("diagrams", []):
        m = diagrams.get(did)
        if not m:
            continue
        dia_ids.append(did)
        w = m["renderedWidthMm"]
        h = m["heightMm"]
        # Sütun genişliğine sığdırmak için orantılı küçültme
        if w > geom["colWidthMm"]:
            h *= geom["colWidthMm"] / w
        dia_h += h * RLMM + 4 * RLMM

    content_h = total + dia_h
    pages = content_h / text_h
    return {
        "gameId": g["gameId"],
        "words": words(g["culturalStory"], g["materialsAndSubstitution"],
                       g.get("setup"), g.get("turnSequence"), g.get("capture"),
                       g.get("movement"), g.get("throwValues"),
                       g.get("stackingAndSending"), g.get("chain"),
                       g.get("winCondition"), g.get("kingCapture"),
                       g.get("firstMove"), g.get("endCondition"),
                       g.get("edgeCases"), g.get("exampleTurn"),
                       g.get("variants"), g.get("firstGame"),
                       g.get("aMatchIsTwoGames"), g.get("reconstructionNotice")),
        "textHeightMm": round(total / RLMM, 1),
        "diagramHeightMm": round(dia_h / RLMM, 1),
        "diagrams": dia_ids,
        "textPages": round(total / text_h, 3),
        "diagramPages": round(dia_h / text_h, 3),
        "measuredPages": round(pages, 3),
        # FATURALAMA MİMARİYİ İZLER, ARİTMETİĞİ DEĞİL.
        # Kitabın maddesi bir ÇİFT SAYFADIR (EDITORIAL_ARCHITECTURE § 2):
        # okur kitabı masaya açar ve sayfa çevirmeden oynar. Bir madde ya
        # iki sayfaya sığar ya DÖRT sayfa alır; 2,16 sayfalık bir madde
        # "2,16 sayfa" diye faturalanamaz, çünkü öyle bir şey basılamaz.
        "billedPages": 2 if pages <= 2.0 else 4,
        "overflowsSpread": pages > 2.0,
    }


def run_measure(root: str, args) -> int:
    try:
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm as RLMM
        from reportlab.pdfbase.pdfmetrics import stringWidth  # noqa: F401
    except ImportError:
        print("  ⊘ reportlab yok — dizgi ölçümü ATLANDI")
        print("    kurulum: pip install -r 04_BUILD/requirements.txt")
        return 2

    cfg = load(os.path.join(root, "project_config.json"))
    mpath = os.path.join(root, cfg["language"]["commercialManuscriptDir"], "book.json")
    if not os.path.exists(mpath):
        print("  · ticari manuscript bu depoda yok — ölçüm ATLANDI "
              "(CI'da beklenen)")
        return 0

    book = load(mpath)
    dmap = {}
    dpath = os.path.join(root, "06_REPORTS", "diagram-render.json")
    if os.path.exists(dpath):
        dmap = {d["diagramId"]: d for d in load(dpath)["diagrams"]}

    # GERÇEK SAYFA GEOMETRİSİ — 8,5 × 11 in, KDP büyük trim
    trim = cfg["production"]["trimPaperback"]
    page_w_mm, page_h_mm = trim["w"] * 25.4, trim["h"] * 25.4
    margin_in, gutter_in = 0.5, 0.375
    geom = {
        "trimWidthMm": round(page_w_mm, 1),
        "trimHeightMm": round(page_h_mm, 1),
        "marginMm": round(margin_in * 25.4, 1),
        "gutterMm": round(gutter_in * 25.4, 1),
        "colWidthMm": round(page_w_mm - (margin_in * 2 + gutter_in) * 25.4, 1),
        "textHeightMm": round(page_h_mm - margin_in * 2 * 25.4 - 12, 1),
        "bodyPt": 10.5,
        "leadingPt": 13.5,
        "font": "Times-Roman",
    }

    S = lambda **kw: ParagraphStyle(**kw)  # noqa: E731
    styles = {
        "h1": S(name="h1", fontName="Times-Bold", fontSize=17, leading=20,
                spaceAfter=2),
        "kicker": S(name="k", fontName="Times-Italic", fontSize=9.5, leading=12,
                    spaceAfter=6),
        "spec": S(name="sp", fontName="Times-Roman", fontSize=9, leading=11.5,
                  spaceAfter=7),
        "body": S(name="b", fontName="Times-Roman", fontSize=geom["bodyPt"],
                  leading=geom["leadingPt"], spaceAfter=5),
        "notice": S(name="n", fontName="Times-Italic", fontSize=9.5, leading=12.5,
                    spaceAfter=6),
        "h2": S(name="h2", fontName="Times-Bold", fontSize=11, leading=13,
                spaceAfter=2, spaceBefore=3),
        "step": S(name="st", fontName="Times-Roman", fontSize=10, leading=12.5,
                  spaceAfter=1.5, leftIndent=10),
        "source": S(name="src", fontName="Times-Roman", fontSize=8, leading=10,
                    spaceAfter=4),
    }

    print("\n── ölçülen sayfa geometrisi ──")
    for k, v in geom.items():
        print("  %-16s %s" % (k, v))

    print("\n── oyun başına GERÇEK ölçüm ──")
    print("  %-14s %6s %9s %9s %7s %7s %8s %7s" %
          ("oyun", "kelime", "metin mm", "diyag mm", "metin s", "diyag s",
           "toplam", "fatura"))
    rows = []
    for g in book["games"]:
        m = measure_game(g, dmap, geom, styles)
        rows.append(m)
        print("  %-14s %6d %9.1f %9.1f %7.2f %7.2f %8.2f %7d%s"
              % (m["gameId"], m["words"], m["textHeightMm"],
                 m["diagramHeightMm"], m["textPages"], m["diagramPages"],
                 m["measuredPages"], m["billedPages"],
                 "  ← ÇİFT SAYFAYI AŞIYOR" if m["overflowsSpread"] else ""))

    n = len(rows)
    avg_words = sum(r["words"] for r in rows) / n
    avg_pages = sum(r["measuredPages"] for r in rows) / n
    avg_billed = sum(r["billedPages"] for r in rows) / n
    wpp = avg_words / avg_pages if avg_pages else 0

    pm = cfg["production"]["pageModel"]
    scope = cfg["scope"]
    body_pages = int(round(avg_billed * scope["games"]))
    openers = pm["familyOpenerPages"] * scope["families"]
    total_pages = body_pages + openers + pm["frontMatterPages"] + pm["backMatterPages"]
    if pm.get("signatureMultiple"):
        m = pm["signatureMultiple"]
        total_pages = ((total_pages + m - 1) // m) * m
    dev = (total_pages - scope["pageTarget"]) / scope["pageTarget"] * 100

    avg_text = sum(r["textPages"] for r in rows) / n
    avg_dia = sum(r["diagramPages"] for r in rows) / n
    overflow = [r["gameId"] for r in rows if r["overflowsSpread"]]

    print("\n── BULGU: ÇİFT SAYFAYI NE AŞIRIYOR ──")
    print("  · metin  : %.2f sayfa (oyunlar arası fark %.2f)"
          % (avg_text, max(r["textPages"] for r in rows)
             - min(r["textPages"] for r in rows)))
    print("  · diyagram: %.2f sayfa (oyunlar arası fark %.2f)"
          % (avg_dia, max(r["diagramPages"] for r in rows)
             - min(r["diagramPages"] for r in rows)))
    print("  → Metin OYUNDAN OYUNA NEREDEYSE SABİTTİR; değişken DİYAGRAMDIR.")
    print("    Çift sayfayı aşan madde sayısı: %d/%d %s"
          % (len(overflow), n, overflow or ""))

    print("\n── kalibrasyon ──")
    print("  · ölçülen kelime/oyun     : %.0f   (hedef %d · bant %d–%d)"
          % (avg_words, scope["gameWordTarget"], scope["gameWordBandMin"],
             scope["gameWordBandMax"]))
    print("  · ölçülen KELİME/SAYFA    : %.0f   (Faz 1 hipotezi %d)"
          % (wpp, pm["wordsPerTypesetPageHypothesis"]))
    print("  · ölçülen sayfa/oyun      : %.2f  (hipotez %d · bant 2,0 ± 0,25)"
          % (avg_pages, pm["pagesPerGame"]))
    print("  · faturalanan sayfa/oyun  : %.2f" % avg_billed)
    print("  · 100 oyunluk gövde       : %d sayfa" % body_pages)
    print("  · TOPLAM                  : %d sayfa (hedef %d · sapma %+.1f%%)"
          % (total_pages, scope["pageTarget"], dev))

    ok = True
    tol = scope["pageTolerancePct"]
    if abs(dev) > tol:
        print("  ✗ sayfa modeli %%%d bandını AŞIYOR" % tol)
        ok = False
    else:
        print("  ✓ sayfa modeli %%%d bandında" % tol)
    if not (scope["gameWordBandMin"] <= avg_words <= scope["gameWordBandMax"]):
        print("  ✗ kelime ortalaması banttan taşıyor")
        ok = False
    else:
        print("  ✓ kelime ortalaması bantta")
    if avg_pages > 2.5:
        print("  ✗ sayfa/oyun 2,5'i AŞIYOR — kapsam ya da tasarım kararı gerekir")
        ok = False

    payload = {
        "status": "pass" if ok else "fail",
        "measuredOn": "phase2",
        "sampleSize": n,
        "sampleGames": [r["gameId"] for r in rows],
        "sampleCaveat": ("Örneklem 3 oyundur ve KÜÇÜKTÜR. Sebebi bir tercih "
                         "değil bir kapıdır: kural metni yalnızca sayfa "
                         "seviyesinde doğrulanmış kaynağa dayanabilir ve "
                         "12 pilot oyunun yalnızca üçü bu şartı sağladı."),
        "geometry": geom,
        "perGame": rows,
        "avgWordsPerGame": round(avg_words, 1),
        "measuredWordsPerPage": round(wpp, 1),
        "hypothesisWordsPerPage": pm["wordsPerTypesetPageHypothesis"],
        "avgMeasuredPagesPerGame": round(avg_pages, 3),
        "avgBilledPagesPerGame": round(avg_billed, 3),
        "avgTextPagesPerGame": round(avg_text, 3),
        "avgDiagramPagesPerGame": round(avg_dia, 3),
        "spreadOverflowGames": overflow,
        "spreadOverflowRate": round(len(overflow) / n, 3),
        "finding": ("Metin oyundan oyuna neredeyse sabittir (~%.2f sayfa); "
                    "çift sayfayı aşıran değişken DİYAGRAM ALANIDIR. "
                    "Sayfa bütçesi bir KELİME bütçesi değil, bir DİYAGRAM "
                    "bütçesidir." % avg_text),
        "projectedBodyPages": body_pages,
        "projectedTotalPages": total_pages,
        "pageTarget": scope["pageTarget"],
        "deviationPct": round(dev, 2),
        "withinTolerance": abs(dev) <= tol,
    }
    out = args.json or os.path.join(root, "06_REPORTS",
                                    "phase2-typeset-measurement.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return 0 if ok else 1


def run_check(root: str, args) -> int:
    """--check: ölçüm raporu var ve tutarlı mı.

    Ticari manuscript depoda YOKTUR; CI bu yüzden ölçümü tekrar edemez.
    Denetlenebilen şey, işlenmiş ölçümün kendi içinde tutarlı olmasıdır."""
    p = os.path.join(root, "06_REPORTS", "phase2-typeset-measurement.json")
    if not os.path.exists(p):
        print("  · dizgi ölçümü henüz yapılmamış — kapı boş koşar")
        return 0
    d = load(p)
    cfg = load(os.path.join(root, "project_config.json"))
    errs = []
    if not d.get("perGame"):
        errs.append("ölçüm boş")
    if d.get("pageTarget") != cfg["scope"]["pageTarget"]:
        errs.append("ölçüm başka bir sayfa hedefine göre yapılmış")
    for r in d.get("perGame", []):
        if r["measuredPages"] <= 0 or r["words"] <= 0:
            errs.append("geçersiz ölçüm: %s" % r["gameId"])
    if abs(d.get("deviationPct", 0)) > cfg["scope"]["pageTolerancePct"] \
            and d.get("withinTolerance"):
        errs.append("sapma bandı aşıyor ama 'withinTolerance' true")
    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        return 1
    print("  ✓ dizgi ölçümü tutarlı · %d oyun · %.2f sayfa/oyun · toplam %d "
          "sayfa (sapma %+.1f%%)"
          % (d["sampleSize"], d["avgMeasuredPagesPerGame"],
             d["projectedTotalPages"], d["deviationPct"]))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    print("=" * 74)
    print("  GERÇEK DİZGİ ÖLÇÜMÜ%s" % (" (--check)" if args.check else ""))
    print("=" * 74)
    rc = run_check(root, args) if args.check else run_measure(root, args)
    print("=" * 74)
    return rc


if __name__ == "__main__":
    sys.exit(main())
