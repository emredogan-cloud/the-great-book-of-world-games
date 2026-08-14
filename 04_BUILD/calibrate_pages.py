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

    # ⚠ BU LİSTE TAM OLMAK ZORUNDADIR. Ölçülmeyen bir blok, sayfa
    # modelini SESSİZCE küçültür — ve sayfa modeli kitabın ekonomisidir.
    # Faz 3 batch'i üç yeni blok getirdi (stages · legalMoves · firstMove);
    # listeye eklenmeselerdi üç oyun olduğundan kısa ölçülürdü.
    # Faz 4 batch 1 üç blok daha getirdi (placement · figures · scoring) —
    # aynı sebeple aynı anda eklendiler. `qa_manuscript.py --check-blocks`
    # bu listenin manuscript'teki blok kümesini KAPSADIĞINI denetler, yani
    # bir sonraki unutuş sessiz kalmaz.
    for label, key in (("Setup", "setup"), ("Placing", "placement"),
                       ("On your turn", "turnSequence"),
                       ("Capture", "capture"), ("Movement", "movement"),
                       ("Legal moves", "legalMoves"),
                       ("Throw values", "throwValues"), ("Levels", "stages"),
                       ("The figures", "figures"), ("Scoring", "scoring"),
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
                       g.get("setup"), g.get("placement"),
                       g.get("turnSequence"), g.get("capture"),
                       g.get("movement"), g.get("throwValues"),
                       g.get("figures"), g.get("scoring"),
                       g.get("stackingAndSending"), g.get("chain"),
                       g.get("winCondition"), g.get("kingCapture"),
                       g.get("legalMoves"), g.get("stages"),
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


def read_gate_phase(root: str) -> str:
    """Ölçümün fazı `.gate`ten OKUNUR, koda gömülmez (karar K2)."""
    p = os.path.join(root, ".gate")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            return fh.read().strip() or "unknown"
    return "unknown"


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

    # ⚠ BULGU YAZILMAZ, ÖLÇÜMDEN TÜRETİLİR.
    #
    # Faz 2 (3 oyun) "metin sabittir, değişken diyagramdır" dedi ve bu cümle
    # buraya SABİT METİN olarak gömüldü. Faz 3 (11 oyun) metin farkını 0,41'e
    # çıkardı ve cümle zayıfladı; Faz 4 (19 oyun) metin farkını diyagram
    # farkının ÜSTÜNE çıkardı — yani gömülü cümle artık kendi verisini
    # yalanlıyordu ve yine de her koşuda basılıyordu.
    # Gömülü bir sonuç, ölçümü olmayan bir iddiadır. Artık türetiliyor.
    text_spread = (max(r["textPages"] for r in rows)
                   - min(r["textPages"] for r in rows))
    dia_spread = (max(r["diagramPages"] for r in rows)
                  - min(r["diagramPages"] for r in rows))
    if dia_spread > text_spread * 1.25:
        driver, finding = "diagram", (
            "Çift sayfayı aşıran DEĞİŞKEN DİYAGRAM ALANIDIR: diyagram farkı "
            "(%.2f sayfa) metin farkının (%.2f) belirgin biçimde üstünde. "
            "Sayfa bütçesi bir KELİME bütçesi değil, bir DİYAGRAM bütçesidir."
            % (dia_spread, text_spread))
    elif text_spread > dia_spread * 1.25:
        driver, finding = "text", (
            "Çift sayfayı aşıran DEĞİŞKEN METİN UZUNLUĞUDUR: metin farkı "
            "(%.2f sayfa) diyagram farkının (%.2f) üstünde. Faz 2'nin üç "
            "oyunluk örneklemde bulduğu 'metin sabittir' sonucu bu örneklemde "
            "GEÇERSİZDİR." % (text_spread, dia_spread))
    else:
        driver, finding = "both", (
            "Metin farkı (%.2f sayfa) ve diyagram farkı (%.2f) AYNI "
            "büyüklükte. Tek bir sürücü yoktur; sayfa bütçesi ikisini birden "
            "denetlemek zorundadır." % (text_spread, dia_spread))

    print("\n── BULGU: ÇİFT SAYFAYI NE AŞIRIYOR ──")
    print("  · metin  : %.2f sayfa (oyunlar arası fark %.2f)"
          % (avg_text, text_spread))
    print("  · diyagram: %.2f sayfa (oyunlar arası fark %.2f)"
          % (avg_dia, dia_spread))
    print("  → sürücü: %s" % driver.upper())
    print("    %s" % finding)
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
        # ÖLÇÜMÜN FAZI DA ÖLÇÜMDEN GELİR. "phase2" burada sabit yazılıydı ve
        # Faz 3 ile Faz 4 ölçümleri de "Faz 2'de ölçüldü" diye kaydediliyordu.
        #
        # İKİ FAZ AYRI KAYDEDİLİR ve bu ayrım projenin tamamında geçerlidir:
        # `measuredOn` ÜRETİM fazıdır (manuscript kendi fazını taşır),
        # `measuredAtGate` RESMÎ kapı seviyesidir (.gate). İkisi Faz 3'ten
        # beri kasıtlı olarak birbirinden farklıdır (K18 · K21).
        "measuredOn": book.get("phase", "unknown"),
        "measuredAtGate": read_gate_phase(root),
        "sampleSize": n,
        "sampleGames": [r["gameId"] for r in rows],
        "sampleCaveat": (
            "Örneklem %d oyundur. Sınırı bir tercih değil bir KAPI belirler: "
            "bir kural metni yalnızca sayfa seviyesinde doğrulanmış bir "
            "kaynağa dayanabilir, yani ölçülebilen oyun sayısı doğrulanabilen "
            "kaynak sayısıdır. %s" % (
                n,
                "Bu örneklem bir sabiti kanıtlayacak kadar büyük DEĞİLDİR."
                if n < 12 else
                "Bu örneklem bir eğilimi gösterir; taşma oranını belirleyen "
                "aykırı değerler için hâlâ küçüktür.")),
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
        "finding": finding,
        "overflowDriver": driver,
        "textSpreadPages": round(text_spread, 3),
        "diagramSpreadPages": round(dia_spread, 3),
        "projectedBodyPages": body_pages,
        "projectedTotalPages": total_pages,
        "pageTarget": scope["pageTarget"],
        "deviationPct": round(dev, 2),
        "withinTolerance": abs(dev) <= tol,
    }
    out = args.json or os.path.join(root, "06_REPORTS",
                                    "phase2-typeset-measurement.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for path in {out, os.path.join(root, "06_REPORTS", "%s-typeset-measurement.json"
                                   % payload["measuredOn"])}:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    return 0 if ok else 1


def run_check(root: str, args) -> int:
    """--check: ölçüm raporu var ve tutarlı mı.

    Ticari manuscript depoda YOKTUR; CI bu yüzden ölçümü tekrar edemez.
    Denetlenebilen şey, işlenmiş ölçümün kendi içinde tutarlı olmasıdır.

    FAZ 5 EKLEMESİ — BAYAT ÖLÇÜM.
    Manuscript YERELDE varsa, ölçümün hangi maddeleri kapsadığı da
    denetlenir. Faz 5'in kapsam değişikliği iki maddeyi manuscript'ten
    çıkardı; bu kapı hiçbir şey söylemedi ve 22 oyunluk ESKİ ölçümü
    "tutarlı" ilan etti. Sayfa modeli bu kitabın FİYAT modelidir: iki
    madde eksilirken 258 sayfa demeye devam eden bir ölçüm, kapak
    sırtından birim telife kadar her şeyi yanlış hesaplatır.

    CI'da manuscript yoktur ve bölüm eskisi gibi boş koşar."""
    p = os.path.join(root, "06_REPORTS", "phase2-typeset-measurement.json")
    if not os.path.exists(p):
        print("  · dizgi ölçümü henüz yapılmamış — kapı boş koşar")
        return 0
    d = load(p)
    cfg = load(os.path.join(root, "project_config.json"))
    errs = []
    if not d.get("perGame"):
        errs.append("ölçüm boş")

    bp = os.path.join(root, cfg["language"]["commercialManuscriptDir"],
                      "book.json")
    if os.path.exists(bp):
        live = {g["gameId"] for g in load(bp).get("games", [])}
        meas = {r["gameId"] for r in d.get("perGame", [])}
        gone = sorted(meas - live)
        fresh = sorted(live - meas)
        if gone:
            errs.append("ÖLÇÜM BAYAT — manuscript'te OLMAYAN madde ölçülmüş: "
                        "%s (yeniden ölçün)" % ", ".join(gone[:5]))
        if fresh:
            errs.append("ÖLÇÜM BAYAT — manuscript'teki madde ÖLÇÜLMEMİŞ: "
                        "%s (yeniden ölçün)" % ", ".join(fresh[:5]))
    else:
        print("  · manuscript depoda yok — kapsam karşılaştırması atlandı "
              "(CI'da beklenen)")
    if d.get("pageTarget") != cfg["scope"]["pageTarget"]:
        errs.append("ölçüm başka bir sayfa hedefine göre yapılmış")
    for r in d.get("perGame", []):
        if r["measuredPages"] <= 0 or r["words"] <= 0:
            errs.append("geçersiz ölçüm: %s" % r["gameId"])
    if abs(d.get("deviationPct", 0)) > cfg["scope"]["pageTolerancePct"] \
            and d.get("withinTolerance"):
        errs.append("sapma bandı aşıyor ama 'withinTolerance' true")

    # FAZ 5 EKLEMESİ — KALİBRE EDİLMİŞ CONFIG ÖLÇÜMDEN KAYMIŞ MI.
    #
    # Ölçüm raporunu `calibrate_pages.py` yazar; ekonomiyi hesaplayan
    # `page_budget.py` ve `editions.py` ise sayıyı RAPORDAN DEĞİL
    # `project_config.json § production.pageModel.measured` içinden okur.
    # İkisini birbirine bağlayan tek şey, ölçümden sonra config'i
    # güncellemeyi HATIRLAMAKTI.
    #
    # Faz 5'te tam olarak bu koptu: yeni ölçüm 260 sayfa dedi, config 258
    # demeye devam etti ve iki betik eski sayıyla telif hesapladı. Hiçbir
    # kapı itiraz etmedi. Sayfa sayısı kapak sırtını ve birim telifi
    # belirler; sessizce eski kalması, kitabın ekonomisini eski kitaptan
    # hesaplamaktır. (Faz 4'ün "gömülü değer" dersinin ekonomik biçimi.)
    # `p` CANLI ölçümdür; `measured.report` yalnızca arşiv nüshasına bir
    # işarettir. Karşılaştırma canlı ölçümle yapılır.
    meas = (cfg.get("production", {}).get("pageModel", {}).get("measured")
            or {})
    for key in ("projectedTotalPages", "sampleSize", "deviationPct",
                "overflowDriver"):
        if meas and meas.get(key) != d.get(key):
            errs.append(
                "config KAYMIŞ — pageModel.measured.%s = %r ama CANLI ölçüm "
                "%r diyor (ekonomi eski sayıyla hesaplanıyor)"
                % (key, meas.get(key), d.get(key)))
    rp = meas.get("report")
    if rp and not os.path.exists(os.path.join(root, rp)):
        errs.append("config'in işaret ettiği ölçüm raporu yok: %r" % rp)
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
