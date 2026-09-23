#!/usr/bin/env python3
"""
İÇ BLOK ÜRETECİ — The Great Book of World Games
================================================================================
Kitabın **basılacak iç bloğunu** üretir: ön madde · yedi aile açılışı ·
elli altı oyun · arka madde. Çıktı KDP'ye yüklenecek PDF'tir.

── MİMARİ SÖZLEŞMESİ ────────────────────────────────────────────────────
`EDITORIAL_ARCHITECTURE § 2` tek bir söz verir ve bütün dizgi ona bağlıdır:

    HER OYUN BİR ÇİFT SAYFADIR. Okur kitabı masaya açar ve sayfa
    çevirmeden oynar.

Bu, tipografik bir tercih değil **oynanabilirlik kuralıdır**: turun
ortasında sayfa çeviren okur kuralı kaybeder. Mekanik karşılığı şudur —
her oyun ÇİFT (sol) sayfada başlar. Kitapta sayfa 1 tektir, dolayısıyla
gövdenin her birimi ÇİFT sayıda sayfa tutmak zorundadır; aksi hâlde
sonraki bütün oyunların pariteси kayar ve söz tek seferde bozulur.
`--check` bunu SAYAR.

── FONT ────────────────────────────────────────────────────────────────
⚠ reportlab'ın varsayılan Times-Roman'ı bir **Type-1 taban fontudur ve
PDF'e GÖMÜLMEZ**. KDP gömülmemiş fontu reddeder. Bu yüzden gerçek bir
TTF kaydedilir: **Liberation Serif** (SIL OFL 1.1 — gömülebilir, ticari
kullanıma açık) ve metrikleri Times ile uyumludur, yani Faz 2'den beri
ölçülen sayfa modeli KAYMAZ.

── SIRT İÇİN SAYFA SAYISI ──────────────────────────────────────────────
Sayfa sayısı TAHMİN EDİLMEZ, SAYILIR. `covers.py` sırtı buradan üretilen
`06_REPORTS/interior-<edition>.json` dosyasındaki `pageCount` alanından
hesaplar. Model (254) 100 oyunluk KAPSAMIN izdüşümüdür ve kapak için
KULLANILMAZ.

── İÇ MARJ ─────────────────────────────────────────────────────────────
KDP iç marjı (gutter) sayfa sayısına göre şart koşar. Sayfa sayısı ise
dizgiye bağlıdır. Bu bir döngüdür ve iterasyonla çözülür: diz → say →
marjı yeniden seç → diz. `--check` yakınsamayı doğrular.

Kullanım:
    interior.py --edition paperback
    interior.py --all
    interior.py --check

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re

import typo
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

IN = 72.0                       # 1 inch = 72 pt
MM = 72.0 / 25.4

# KDP iç marj (gutter) tablosu — Amazon.com, büyük trim, siyah-beyaz.
# Sayfa sayısına göre ZORUNLU asgari; kitap bunun üstünü kullanır.
KDP_GUTTER_IN = [(150, 0.375), (300, 0.500), (500, 0.625),
                 (700, 0.750), (828, 0.875)]
KDP_OUTER_MIN_IN = 0.25         # bleed yoksa dış/üst/alt asgari

# ⚠ EMNİYET PAYI — çıplak KDP asgarisinin ÜSTÜNE eklenir, asgariyi
# DEĞİŞTİRMEZ. Gerçek KDP Previewer 160 sayfalık ciltsizde sayfa 159'da
# "Insufficient gutter" dedi. Kaynak taranınca (04_BUILD/kdp_preflight.py
# check_ink(), 300 dpi, sayfa tarafına göre gutter/dış ayrımı yapılarak)
# bu TEK sayfa değildi — ciltsizde 16 sayfa, gutter tam asgaride (emniyet
# payı SIFIR) dizildiği için 0,0033–0,0100 in kısa ölçüldü. Kök neden bir
# aritmetik hatası değil: bazı karakterlerin (ölçülen örnek: sayfa 159'da
# açılış tek tırnağı ') mürekkebi, Liberation Serif'in glif tasarımı
# gereği harfin nominal başlangıç noktasının hafifçe SOLUNA taşıyor — bu
# yazı tiplerinde sık görülen normal bir çizim gerçeğidir, bir dizgi
# hatası değil. Marj tam yasal asgaride durduğu için bu küçük taşma
# yasal sınırı GEÇİYORDU. Ciltli hiç başarısız olmadı çünkü zaten kendi
# +0,125 in cilt payı bu taşmayı TESADÜFEN yutuyordu — yani ciltsiz de
# aynı sınıf korumaya ihtiyaç duyuyor, tesadüfe bırakılamaz.
#
# En kötü ölçülen taşma 0,0100 in'di (iki sayfa, ikisi de tam bu değerde).
# Pay onun BEŞ KATI: 149 sayfalık bir kitapta bile aynı sınıf bir glif
# taşması bir daha yasal sınırı aşamaz.
GUTTER_SAFETY_IN = 0.05
FONT_DIR_CANDIDATES = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/liberation",
]
FONT_FILES = {
    "GBSerif":     "LiberationSerif-Regular.ttf",
    "GBSerif-B":   "LiberationSerif-Bold.ttf",
    "GBSerif-I":   "LiberationSerif-Italic.ttf",
    "GBSerif-BI":  "LiberationSerif-BoldItalic.ttf",
}


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def gutter_in(pages: int) -> float:
    for limit, val in KDP_GUTTER_IN:
        if pages <= limit:
            return val
    return KDP_GUTTER_IN[-1][1]


def esc(s: str) -> str:
    """Paragraph mini-HTML'i için kaçış + tipografik kesme işareti.

    `&` ilk sırada olmak ZORUNDA.

    ⚠ KESME İŞARETİ DİZGİ ANINDA DÖNÜŞTÜRÜLÜR, VERİDE DEĞİL. Manuscript
    düz ASCII kesme işareti taşır ve öyle kalmalıdır: JSON'da arama,
    karşılaştırma ve diff düz karakterle çalışır. Sayfada ise düz kesme
    işareti daktilo işidir — "Nine Men's Morris" ile "Nine Men’s Morris"
    arasındaki fark, kitabın premium görünüp görünmemesidir. Ligatür gibi:
    bir DİZGİ dönüşümü.
    """
    return typo.xml_text(s)


def register_fonts() -> str:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping
    fdir = None
    for d in FONT_DIR_CANDIDATES:
        if os.path.isdir(d) and all(os.path.exists(os.path.join(d, f))
                                    for f in FONT_FILES.values()):
            fdir = d
            break
    if fdir is None:
        raise RuntimeError(
            "Liberation Serif bulunamadı. KDP GÖMÜLMEMİŞ FONT KABUL ETMEZ ve "
            "reportlab'ın Times-Roman'ı gömülmez. Kurulum: "
            "apt-get install fonts-liberation")
    for name, fn in FONT_FILES.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(fdir, fn)))
    # ⚠ reportlab'ın TABAN fontu Helvetica'dır ve hiç kullanılmasa bile
    # sayfa kaynak sözlüğüne GİRER. `pdffonts` onu 'emb: no' gösterir;
    # KDP'nin ön denetimi gömülmemiş bir font adı görürse dosyayı geri
    # çevirir. Taban fontu gömülü olanla DEĞİŞTİRİLİR.
    import reportlab.rl_config as rl_config
    rl_config.canvas_basefontname = "GBSerif"
    addMapping("GBSerif", 0, 0, "GBSerif")
    addMapping("GBSerif", 1, 0, "GBSerif-B")
    addMapping("GBSerif", 0, 1, "GBSerif-I")
    addMapping("GBSerif", 1, 1, "GBSerif-BI")
    return fdir


def styles(body_pt: float, lead_pt: float, scale: float = 1.0,
           min_pt: float = 0.0):
    """Bütün stiller GÖMÜLÜ fonta bağlanır.

    ⚠ `bulletFontName` DAHİL. reportlab'ın ParagraphStyle varsayılanı
    Helvetica'dır ve madde imi hiç kullanılmasa bile font kaynağa
    girebiliyor; `pdffonts` ilk koşuda üç gömülmemiş font gösterdi
    (Helvetica · Times-Roman · ZapfDingbats) ve KDP üçünü de reddederdi.

    BÜYÜK PUNTO (largeprint): `scale` bütün ölçüleri tek çarpanla büyütür
    (punto, satır aralığı, boşluk, girinti) ve hiçbir yazı `min_pt`in
    altına inemez. scale=1.0 ve min_pt=0 iken bu fonksiyon ESKİSİYLE
    birebir aynı stilleri üretir — ciltsiz ve ciltli çıktı değişmez.
    """
    from reportlab.lib.styles import ParagraphStyle

    def S(**kw):
        kw.setdefault("bulletFontName", "GBSerif")
        if scale != 1.0 or min_pt:
            for k in ("fontSize", "leading", "spaceAfter", "spaceBefore",
                      "leftIndent"):
                if k in kw:
                    kw[k] = kw[k] * scale
            if kw.get("fontSize", 0) < min_pt:
                ratio = min_pt / kw["fontSize"]
                kw["fontSize"] = min_pt
                kw["leading"] = kw["leading"] * ratio
        return ParagraphStyle(**kw)

    def fs(base: float) -> str:
        """Paragraph içi <font size=…> için ölçekli punto (dize)."""
        v = base * scale
        if v < min_pt:
            v = min_pt
        return "%g" % round(v, 2)

    return {
        "_fs":    fs,
        "h1":     S(name="h1", fontName="GBSerif-B", fontSize=17, leading=20,
                    spaceAfter=2),
        "kicker": S(name="k", fontName="GBSerif-I", fontSize=9.5, leading=12,
                    spaceAfter=6),
        "spec":   S(name="sp", fontName="GBSerif", fontSize=9, leading=11.5,
                    spaceAfter=7),
        "body":   S(name="b", fontName="GBSerif", fontSize=body_pt,
                    leading=lead_pt, spaceAfter=5),
        "notice": S(name="n", fontName="GBSerif-I", fontSize=9.5, leading=12.5,
                    spaceAfter=6),
        "h2":     S(name="h2", fontName="GBSerif-B", fontSize=11, leading=13,
                    spaceAfter=2, spaceBefore=3),
        "step":   S(name="st", fontName="GBSerif", fontSize=10, leading=12.5,
                    spaceAfter=1.5, leftIndent=10),
        "source": S(name="src", fontName="GBSerif", fontSize=8, leading=10,
                    spaceAfter=4),
        # ön madde ve arka madde
        "title":  S(name="ti", fontName="GBSerif-B", fontSize=30, leading=34,
                    spaceAfter=10, alignment=1),
        "sub":    S(name="su", fontName="GBSerif-I", fontSize=12.5, leading=16,
                    spaceAfter=8, alignment=1),
        "author": S(name="au", fontName="GBSerif", fontSize=15, leading=19,
                    spaceAfter=4, alignment=1),
        "small":  S(name="sm", fontName="GBSerif", fontSize=8.5, leading=11,
                    spaceAfter=5),
        "sect":   S(name="se", fontName="GBSerif-B", fontSize=20, leading=24,
                    spaceAfter=10),
        "stand":  S(name="sf", fontName="GBSerif-I", fontSize=12, leading=15,
                    spaceAfter=10),
        "toc":    S(name="tc", fontName="GBSerif", fontSize=9.5, leading=12.4,
                    spaceAfter=0),
        "tocfam": S(name="tf", fontName="GBSerif-B", fontSize=10.5, leading=15,
                    spaceAfter=1, spaceBefore=7),
        "idx":    S(name="ix", fontName="GBSerif", fontSize=8.5, leading=10.6,
                    spaceAfter=0),
        "idxh":   S(name="ih", fontName="GBSerif-B", fontSize=9.5, leading=13,
                    spaceAfter=1, spaceBefore=5),
    }


# ── SAYFA MOTORU ─────────────────────────────────────────────────────────
class Page:
    """Bir sayfa: akış çerçevesi + üstbilgi/altbilgi bilgisi."""

    __slots__ = ("items", "runHead", "folio", "blank", "kind", "anchor",
                 "opensSection")

    def __init__(self, kind="body"):
        self.items = []     # (flowable, x, y, w, h) — çizim emirleri
        self.runHead = None
        self.folio = True
        self.blank = False
        self.kind = kind
        self.anchor = None  # bu sayfada başlayan madde
        self.opensSection = False


class Layout:
    """Çift sayfa mimarisini SAYAN dizgi motoru.

    Sayfa numarası 1'den başlar ve TEK'tir (sağ sayfa). `is_verso(n)`
    çift sayfaları — yani okurun SOLUNU — verir.
    """

    def __init__(self, geom, sty):
        self.g = geom
        self.s = sty
        self.pages: list[Page] = []

    # -- sayfa yönetimi --------------------------------------------------
    def new_page(self, kind="body") -> Page:
        p = Page(kind)
        self.pages.append(p)
        return p

    @property
    def n(self) -> int:
        return len(self.pages)

    def is_verso(self, page_no: int) -> bool:
        return page_no % 2 == 0

    def pad_to_verso(self, kind="blank"):
        """Sonraki sayfa SOL (çift) olacak şekilde boş sayfa ekler."""
        if (self.n + 1) % 2 != 0:
            p = self.new_page(kind)
            p.blank = True
            p.folio = False

    def pad_to_recto(self, kind="blank"):
        if (self.n + 1) % 2 != 1:
            p = self.new_page(kind)
            p.blank = True
            p.folio = False

    # -- çerçeve ---------------------------------------------------------
    def frame(self, page_no: int):
        """(x, y_top, width, height) — sayfanın metin çerçevesi.

        İç marj CİLDE bakar: tek sayfada solda, çift sayfada sağda."""
        g = self.g
        inner = g["gutterPt"]
        outer = g["outerPt"]
        x = inner if not self.is_verso(page_no) else outer
        w = g["wPt"] - inner - outer
        y_top = g["hPt"] - g["topPt"]
        h = g["hPt"] - g["topPt"] - g["bottomPt"]
        return x, y_top, w, h

    # -- akış ------------------------------------------------------------
    def flow(self, flowables, kind="body", run_head=None, start_page=None,
             reserve_top=0.0, max_pages=None, height_cap=None):
        """Flowable listesini sayfalara döker.

        Döner: (kullanılan sayfa sayısı, SIĞMAYAN artık).
        Artık boş değilse çağıran karar verir — gövdede bu, maddenin dört
        sayfaya çıkması demektir.
        """
        page = start_page or self.new_page(kind)
        if page.runHead is None:
            page.runHead = run_head
        idx = self.pages.index(page) + 1
        x, y_top, w, h = self.frame(idx)
        y = y_top - reserve_top
        bottom = y_top - h
        if height_cap is not None:
            bottom = max(bottom, y - height_cap)
        used = 1
        queue = list(flowables)

        while queue:
            fl = queue.pop(0)
            avail = y - bottom
            fw, fh = fl.wrap(w, max(avail, 1))
            if fh <= avail + 0.01:
                page.items.append((fl, x, y - fh, w))
                y -= fh
                continue
            # sığmadı — bölmeyi dene
            parts = fl.split(w, avail) if avail > 30 else []
            if parts:
                head = parts[0]
                hw, hh = head.wrap(w, avail)
                page.items.append((head, x, y - hh, w))
                y -= hh
                queue = list(parts[1:]) + queue
                continue
            queue.insert(0, fl)
            if max_pages and used >= max_pages:
                return used, queue
            page = self.new_page(kind)
            page.runHead = run_head
            used += 1
            idx = self.pages.index(page) + 1
            x, y_top, w, h = self.frame(idx)
            y = y_top
            bottom = y_top - h      # kapak YALNIZCA ilk sayfaya uygulanır
        return used, []


# ── İÇERİK → FLOWABLE ────────────────────────────────────────────────────
DIAGRAM_PAGE_BUDGET = 0.52   # çift sayfanın SAĞ yaprağında diyagrama ayrılan pay

# ⚠ HERO GÖRSELİ BÜTÇESİ — SOL yaprakta, başlıktan ÖNCE, sayfa yüksekliğinin
# bu kesri kadar yer kaplar (genişlik değil — 3:2 GPT Image çıktısı bu
# yükseklik hedefine göre kendiliğinden ölçeklenir, bkz. ImageFlow).
# run_check() dört sayfalık madde sayısını ALTI ile sınırlar (K-ARCHIVE
# "çift sayfa" sözü). Bu değer o sınırı AŞMAYACAK şekilde --check ile
# ÖLÇÜLEREK seçilmiştir; büyütülecekse yeniden ölçülmeden büyütülmez.
HERO_IMAGE_BUDGET = 0.19


class ImageFlow:
    """Bir kahraman görselini (GPT Image, raster PNG) akışa sokar.

    SVGFlow ile aynı arayüz (wrap/split/drawOn) — dizgi motoru ikisini
    ayırt etmez. Görsel BÖLÜNMEZ ve yükseklik hedefine göre ölçeklenir;
    genişlik hiçbir zaman sütun genişliğini AŞMAZ.
    """

    def __init__(self, path, max_w_pt, max_h_pt, gap_pt=8.0):
        from reportlab.lib.utils import ImageReader
        self.path = path
        self.reader = ImageReader(path)
        iw, ih = self.reader.getSize()
        self.gap = gap_pt
        s = min(max_w_pt / iw, max_h_pt / ih, 1.0)
        self.w = iw * s
        self.h = ih * s

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.h + self.gap

    def split(self, aw, ah):
        return []                      # görsel BÖLÜNMEZ

    def drawOn(self, canv, x, y, _sW=0):
        cx = x + (getattr(self, "aw", self.w) - self.w) / 2.0
        canv.drawImage(self.reader, cx, y + self.gap, self.w, self.h,
                       preserveAspectRatio=True, mask="auto")

# ⚠ SIRA OKUMA SIRASIDIR, ÖLÇÜM SIRASI DEĞİL.
# `calibrate_pages.py` blokları yükseklik toplamak için sıralar ve orada
# sıranın anlamı yoktur. BASILAN sayfada vardır: ilk sürümde 'Winning'
# 'The first move'dan ÖNCE basılıyordu — okur oyunu nasıl kazanacağını
# ilk hamleyi öğrenmeden okuyordu.
RULE_BLOCKS = (("Setup", "setup"), ("Placing", "placement"),
               ("On your turn", "turnSequence"), ("Movement", "movement"),
               ("Capture", "capture"), ("Legal moves", "legalMoves"),
               ("Throw values", "throwValues"), ("Stages", "stages"),
               ("The figures", "figures"), ("Scoring", "scoring"),
               ("Stacking and sending", "stackingAndSending"),
               ("The chain", "chain"))
PROSE_BEFORE = (("The first move", "firstMove"),)
PROSE_BLOCKS = (("Winning", "winCondition"),
                ("Taking the king", "kingCapture"),
                ("How it ends", "endCondition"))
EDGE_LABEL = {"tie": "If it is a draw.", "stalemate": "If nobody can move.",
              "illegalMove": "If somebody plays an illegal move."}


def game_left(g, sty):
    """Sol sayfa: başlık · künye şeridi · kültürel hikâye · malzeme · kurulum."""
    from reportlab.platypus import Paragraph
    P = lambda t, s: Paragraph(t, sty[s])  # noqa: E731
    out = [P("<b>%s</b>" % esc(g["title"]), "h1"),
           P("%s · %s · %s" % (esc(g["culture"]), esc(g["place"]),
                               esc(g["period"])), "kicker"),
           P(" · ".join("<b>%s</b> %s" % (esc(k.capitalize()), esc(v))
                        for k, v in g["spec"].items()), "spec"),
           P(esc(g["culturalStory"]), "body"),
           P("<b>Materials.</b> " + esc(g["materialsAndSubstitution"]), "body")]
    if g.get("reconstructionNotice"):
        out.append(P("<i>%s</i>" % esc(g["reconstructionNotice"]), "notice"))
    if g.get("safetyNote"):
        out.append(P("<b>Safety.</b> " + esc(g["safetyNote"]), "notice"))
    if g.get("gamblingReframed"):
        out.append(P("<i>%s</i>" % esc(g["gamblingReframed"]), "notice"))
    return out


def game_right(g, sty):
    """Sağ sayfa: kurallar · üç soru · örnek tur · varyant · ilk oyun · künye."""
    from reportlab.platypus import Paragraph
    P = lambda t, s: Paragraph(t, sty[s])  # noqa: E731
    out = []
    for label, key in PROSE_BEFORE:
        if g.get(key):
            out.append(P("<b>%s.</b> %s" % (label, esc(g[key])), "body"))
    for label, key in RULE_BLOCKS:
        if not g.get(key):
            continue
        # BAŞLIK TEK BAŞINA SAYFA SONUNDA KALMAZ. Başlık ile İLK adım tek
        # bir akış birimi olarak bağlanır; ikisi birden sığmazsa ikisi de
        # sonraki sayfaya geçer. (Shatranj'da 'Stages' başlığı bir sayfada,
        # birinci maddesi ötekinde basılmıştı.)
        head = P("<b>%s</b>" % label, "h2")
        first = P("1.&nbsp;%s" % esc(g[key][0]), "step")
        out.append(Bound([head, first]))
        for i, s in enumerate(g[key][1:], 2):
            out.append(P("%d.&nbsp;%s" % (i, esc(s)), "step"))
    for label, key in PROSE_BLOCKS:
        if g.get(key):
            out.append(P("<b>%s.</b> %s" % (label, esc(g[key])), "body"))
    out.append(P("<b>Three questions</b>", "h2"))
    for k, v in g["edgeCases"].items():
        out.append(P("<b>%s</b> %s" % (EDGE_LABEL.get(k, esc(k) + "."),
                                       esc(v)), "body"))
    out.append(P("<b>An example turn.</b> " + esc(g["exampleTurn"]), "body"))
    for v in g.get("variants", []):
        out.append(P("<b>%s.</b> %s" % (esc(v["name"]), esc(v["note"])), "body"))
    out.append(P("<b>Your first game.</b> " + esc(g["firstGame"]), "body"))
    if g.get("aMatchIsTwoGames"):
        out.append(P(esc(g["aMatchIsTwoGames"]), "body"))
    out.append(P("<b>Sources.</b> " + "  ".join(esc(s) for s in g["sources"]),
                 "source"))
    return out



class Bound:
    """İki flowable'ı BÖLÜNMEZ tek birim yapar (başlık + ilk adım).

    Dul başlık bir estetik kusur değildir: numaralı bir kural listesinin
    başlığı bir sayfada, birinci maddesi ötekinde durursa okur listenin
    nerede başladığını kaybeder.
    """

    def __init__(self, items):
        self.items = items

    def wrap(self, aw, ah):
        self.aw = aw
        self.h = sum(it.wrap(aw, ah)[1] for it in self.items)
        return aw, self.h

    def split(self, aw, ah):
        return []

    def drawOn(self, canv, x, y, _sW=0):
        yy = y + self.h
        for it in self.items:
            ih = it.wrap(self.aw, self.h)[1]
            yy -= ih
            it.drawOn(canv, x, yy, _sW)


class SVGFlow:
    """Bir diyagramı VEKTÖR olarak akışa sokar. Raster YOKTUR."""

    def __init__(self, doc, max_w_pt, max_h_pt, gap_pt=6.0):
        self.doc = doc
        self.gap = gap_pt
        s = min(max_w_pt / doc["widthPx"], max_h_pt / doc["heightPx"], 1.0)
        self.w = doc["widthPx"] * s
        self.h = doc["heightPx"] * s

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.h + self.gap

    def split(self, aw, ah):
        return []                      # diyagram BÖLÜNMEZ

    def drawOn(self, canv, x, y, _sW=0):
        import svg_vector as sv
        cx = x + (getattr(self, "aw", self.w) - self.w) / 2.0
        sv.draw_reportlab(canv, self.doc, cx, y + self.h + self.gap,
                          self.w, font="GBSerif")


class Rule:
    """İnce yatay çizgi — bölüm ayırıcısı."""

    def __init__(self, pt=0.6, space=6.0):
        self.pt, self.space = pt, space

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.pt + self.space * 2

    def split(self, aw, ah):
        return []

    def drawOn(self, canv, x, y, _sW=0):
        canv.saveState()
        canv.setLineWidth(self.pt)
        canv.setStrokeColorRGB(0, 0, 0)
        canv.line(x, y + self.space, x + self.aw, y + self.space)
        canv.restoreState()


class VSpace:
    def __init__(self, pt):
        self.pt = pt

    def wrap(self, aw, ah):
        return aw, self.pt

    def split(self, aw, ah):
        return []

    def drawOn(self, canv, x, y, _sW=0):
        pass



TOC_BACK = (("Board templates", "boardTemplates"),
            ("Materials and substitutions", "materialsGuide"),
            ("Glossary", "glossary"), ("Sources", "bibliography"),
            ("Index by culture", "idx-culture"),
            ("Index by players", "idx-players"),
            ("Index by time and age", "idx-duration"),
            ("Invented traditions", "inventedTraditions"))


def _toc_flowables(fm, sty, pagemap, back_pages):
    """İçindekiler. `pagemap` None ise YER TUTUCU (000) üretir."""
    from reportlab.platypus import Paragraph
    P = lambda t, s: Paragraph(t, sty[s])  # noqa: E731
    ph = pagemap is None
    out = [P("Contents", "sect")]
    for item in fm["contents"]:
        if item["kind"] == "family-opener":
            out.append(P("<b>%s</b>" % esc(item["title"]), "tocfam"))
        else:
            pg = "000" if ph else (pagemap.get(item["gameId"]) or "—")
            out.append(P("%s <font size=%s>· %s</font> &nbsp;&nbsp;%s"
                         % (esc(item["title"]), sty["_fs"](8),
                            esc(item["culture"]), pg),
                         "toc"))
    out.append(P("<b>At the back</b>", "tocfam"))
    for lbl, key in TOC_BACK:
        pg = "000" if ph else (back_pages or {}).get(key, "—")
        out.append(P("%s &nbsp;&nbsp;%s" % (lbl, pg), "toc"))
    return out


# ── KİTABI KUR ───────────────────────────────────────────────────────────
def build_layout(root, cfg, book, fm, bm, geom, sty, diagram_docs, plate_docs=None):
    plate_docs = plate_docs or {}
    lay = Layout(geom, sty)
    from reportlab.platypus import Paragraph
    P = lambda t, s: Paragraph(t, sty[s])  # noqa: E731
    tp = fm["titlePage"]
    im = fm["imprint"]

    # ① yarım başlık (tek sayfa) ------------------------------------------
    p = lay.new_page("front")
    p.folio = False
    p.items.append((P("<b>%s</b>" % esc(tp["title"]), "title"),
                    *_center(lay, 1, 0.38)))
    # Başlık sayfası TEK sayfadadır (sağ). Yarım başlıktan sonra bir boş
    # yaprak gelir ve bu bir israf değil, kitabın standart açılışıdır.
    lay.pad_to_recto()

    # ② başlık sayfası -----------------------------------------------------
    p = lay.new_page("front")
    p.folio = False
    x, y_top, w, h = lay.frame(lay.n)
    y = y_top - h * 0.22
    ed_label = geom.get("editionLabel")          # "Large Print Edition" vb.
    tp_items = [P("<b>%s</b>" % esc(tp["title"]), "title"),
                P(esc(tp["subtitle"]), "sub")]
    if ed_label:
        tp_items.append(P("<b>%s</b>" % esc(ed_label), "sub"))
    tp_items += [VSpace(36),
                 P(esc(tp["author"]), "author"),
                 VSpace(h * 0.30),
                 P(esc(tp["publisher"]), "sub")]
    for fl in tp_items:
        fw, fh = fl.wrap(w, h)
        p.items.append((fl, x, y - fh, w))
        y -= fh

    # ③ künye sayfası ------------------------------------------------------
    # Akış `lay.flow()` ile döner (§ Layout.flow) — künye metni (haklar +
    # AI beyanı + yazar biyografisi) her sürümde aynı tek sayfaya sığmaz;
    # büyük puntoda taştığı ÖLÇÜLEREK bulundu (s.4 alt marjı 0.0133 in).
    # Elle y -= fh yığmak çerçeve dışına sessizce basardı; flow() sığmayanı
    # bölüp yeni bir künye-devamı sayfasına taşır.
    p = lay.new_page("front")
    p.folio = False
    x, y_top, w, h = lay.frame(lay.n)
    lines = ["<b>%s</b>" % esc(tp["title"]), esc(tp["subtitle"]), "",
             esc(im["copyright"]), esc(im["publisher"]), "",
             "%s · %s" % (esc(tp["series"]), "Volume %s" % tp["volume"]),
             esc(ed_label or im["edition"]), esc(im["printedBy"]), ""]
    if ed_label:
        # Büyük punto kendi (KDP'nin vereceği) ISBN'ini taşır; öteki
        # sürümlerin numaraları bu künyede listelenmez.
        lines.append("ISBN (large print paperback): %s"
                     % esc(im["isbn"].get("largeprint")
                           or im["isbn"]["paperback"]))
    else:
        for ed in ("paperback", "hardcover"):
            lines.append("ISBN (%s): %s" % (ed, esc(im["isbn"][ed])))
    lines += ["", esc(im["rights"])]
    if im.get("aiDisclosure"):
        lines += ["", esc(im["aiDisclosure"])]
    if im.get("authorBio"):
        lines += ["", "<b>About the author.</b> " + esc(im["authorBio"])]
    flowables = [P(ln or "&nbsp;", "small") for ln in lines]
    used, leftover = lay.flow(flowables, kind="front", start_page=p,
                              reserve_top=h * 0.30)
    if leftover:
        raise RuntimeError("künye sayfası taştı ve flow() artık bırakmamalı — "
                           "%d flowable sığmadı" % len(leftover))
    # devam sayfalarının da folio'su kapalı kalsın (künye numaralanmaz)
    for pg in lay.pages[-used:]:
        pg.folio = False

    # ④ içindekiler --------------------------------------------------------
    # İçindekiler ÖNCE yer tutar, SONRA gerçek numaralarla doldurulur.
    # Yer tutucu, gerçek satırların AYNISIDIR — yalnızca sayfa numarası
    # yerine 000 yazar. Böylece ayrılan sayfa sayısı gerçek içindekilerin
    # sayısıdır; ilk sürüm yalnızca başlığı akıtıyordu ve tek sayfa
    # ayırıp 71 satırlık bir listeyi oraya sığdırmaya çalışıyordu.
    lay.pad_to_recto()
    toc_pages_start = lay.n + 1
    lay.flow(_toc_flowables(fm, sty, None, None), "front", run_head="Contents")
    lay.pages[toc_pages_start - 1].opensSection = True
    toc_flow_pages = lay.n - toc_pages_start + 1

    # ⑤ ön madde denemeleri -------------------------------------------------
    first_fm_sec = True
    for sec in fm["sections"]:
        if first_fm_sec:
            lay.pad_to_recto()
            first_fm_sec = False
        fls = [P("<b>%s</b>" % esc(sec["title"]), "sect")]
        for para in sec.get("paragraphs", []):
            fls.append(P(esc(para), "body"))
        for sub in sec.get("sections", []):
            fls.append(P("<b>%s</b>" % esc(sub["heading"]), "h2"))
            fls.append(P(esc(sub["text"]), "body"))
        if sec.get("table"):
            for row in sec["table"]:
                fls.append(P("<b>%s · %s</b>" % (esc(row["n"]),
                                                 esc(row["name"])), "h2"))
                fls.append(P("%s <i>%s</i>" % (esc(row["idea"]),
                                               esc(row["test"])), "body"))
        if sec.get("closing"):
            fls.append(P(esc(sec["closing"]), "body"))
        first_sec = lay.n + 1
        lay.flow(fls, "front", run_head=sec["title"])
        lay.pages[first_sec - 1].opensSection = True

    front_pages = lay.n

    # ⑥ GÖVDE — aile açılışı + oyunlar --------------------------------------
    openers = {o["family"]: o for o in fm["familyOpeners"]}
    games = {g["gameId"]: g for g in book["games"]}
    pagemap, spreads, overflow = {}, [], []
    cur_family = None
    dia_ratio = []     # büyük punto: diyagram genişliği / ciltsizdeki genişlik
    pb_geom = geometry(cfg, "paperback", 160) if geom.get("largePrint") else None

    for item in fm["contents"]:
        if item["kind"] == "family-opener":
            o = openers[item["family"]]
            cur_family = o["title"]
            # ⚠ AÇILIŞ SAĞ SAYFADADIR.
            # İlk sürüm açılışı SOL sayfaya koyup sağına boş bir yaprak
            # bırakıyordu: okur bölüme boş bir sayfayla karşı karşıya
            # açıyordu ve yedi aile yedi boş sayfa harcıyordu. Sağ sayfada
            # açıldığında bir sonraki sayfa zaten SOL olur ve ilk oyun
            # parite kaybetmeden başlar.
            lay.pad_to_recto()
            fls = [P("Part %s" % esc(o["numeral"]), "kicker"),
                   P("<b>%s</b>" % esc(o["title"]), "sect"),
                   P(esc(o["standfirst"]), "stand"), Rule()]
            for para in o["paragraphs"]:
                fls.append(P(esc(para), "body"))
            fls.append(VSpace(10))
            fls.append(P("<b>In this part:</b> %s."
                         % esc(", ".join(g["title"] for g in book["games"]
                                         if g["family"] == item["family"])),
                         "small"))
            first_op = lay.n + 1
            used, rest = lay.flow(fls, "opener", run_head=o["title"],
                                  max_pages=1)
            lay.pages[first_op - 1].opensSection = True
            if rest:
                overflow.append("family-opener:%s" % item["family"])
            continue

        g = games[item["gameId"]]
        if geom.get("largePrint"):
            # ── BÜYÜK PUNTO: MADDE TEK AKIŞTIR, SAYFA SINIRI YOKTUR ──────
            # 16 puntoda bir madde 3–5 sayfa tutar; çift-sayfa sözü bu
            # sürümde VERİLMEZ (büyük punto okuru sayfa çevirmeyi bekler)
            # ve verilmediği için --check de onu bu sürümde SAYMAZ.
            # Diyagramlar hikâye/malzeme bloğundan sonra, kurallardan
            # ÖNCE akışa girer; fiziksel boyutları ciltsizdekinden
            # KÜÇÜLMEZ (oran raporda ölçülür: diagramScaleVsPaperback).
            first = lay.n + 1
            pagemap[g["gameId"]] = first
            x0, yt0, w0, h0 = lay.frame(first)
            docs = [diagram_docs[d] for d in g.get("diagrams", [])
                    if d in diagram_docs]
            budget = h0 * geom["lpDiagramBudget"]
            dia = [SVGFlow(d, w0, budget / max(len(docs), 1)) for d in docs]
            pw = pb_geom["wPt"] - pb_geom["gutterPt"] - pb_geom["outerPt"]
            ph = pb_geom["hPt"] - pb_geom["topPt"] - pb_geom["bottomPt"]
            for d, lp_d in zip(docs, dia):
                pb_d = SVGFlow(d, pw, ph * DIAGRAM_PAGE_BUDGET / max(len(docs), 1))
                dia_ratio.append(round(lp_d.w / pb_d.w, 3))
            hero = []
            plate_path = plate_docs.get(g["gameId"])
            if plate_path:
                hero = [ImageFlow(plate_path, w0, h0 * HERO_IMAGE_BUDGET)]
            stream = hero + game_left(g, sty) + dia + game_right(g, sty)
            used, rest = lay.flow(stream, "game", run_head=g["title"])
            if rest:
                raise RuntimeError("largeprint: %s akışı bitmedi" % g["gameId"])
            spreads.append((g["gameId"], first, lay.n - first + 1))
            continue

        lay.pad_to_verso()
        first = lay.n + 1
        pagemap[g["gameId"]] = first

        # ⚠ MADDE TEK BİR AKIŞTIR, İKİ AYRI SÜTUN DEĞİL.
        # İlk sürüm sol sayfaya yalnızca başlık + hikâye + malzeme koyup
        # kuralların tamamını sağa yığıyordu; sol sayfa yarı boş kalıyor,
        # sağ sayfa taşıyor ve 56 maddenin 39'u dört sayfaya çıkıyordu.
        # Dizgi ölçümü (calibrate_pages.py) maddeyi TEK AKIŞ olarak ölçer
        # ve 1,56 sayfa der; dizginin de öyle akması gerekir.
        # ── ÇİFT SAYFA DENGESİ ─────────────────────────────────────────
        # Sol sayfayı tepeye kadar doldurup kalanı sağa atmak çalışır ama
        # ÇİRKİN ve yanıltıcıdır: Bao'da sol sayfa doluyor, sağ sayfa
        # diyagramın altında %70 boş kalıyordu. Okur boş bir sayfa görür
        # ve maddenin bittiğini sanır.
        #
        # Bu yüzden akış ÖNCE ölçülür, sonra bölünür: sağ sayfanın metin
        # kapasitesi (çerçeve − diyagram) çıkarılır ve sol sayfa GEREKTİĞİ
        # KADAR doldurulur — ne fazlası ne eksiği.
        x0, yt0, w0, h0 = lay.frame(first)
        # HERO GÖRSELİ — maddenin İLK öğesi, başlıktan bile önce: spread'i
        # AÇAR. Kurucu direktifi: "no game section without a dedicated
        # visual… placed BEFORE that game's rules content."
        hero = []
        plate_path = plate_docs.get(g["gameId"])
        if plate_path:
            hero = [ImageFlow(plate_path, w0, h0 * HERO_IMAGE_BUDGET)]
        stream = hero + game_left(g, sty) + game_right(g, sty)
        docs = [diagram_docs[d] for d in g.get("diagrams", [])
                if d in diagram_docs]
        # ⚠ DİYAGRAM BÜTÇESİ SAYFA BAŞINA, DİYAGRAM BAŞINA DEĞİL.
        # İlk sürüm her diyagrama sayfanın %46'sını veriyordu; iki
        # diyagramlı bir madde sağ sayfanın %92'sini kaplıyor ve metin
        # dördüncü sayfaya taşıyordu. On dört madde böyle taştı. Bütçe
        # artık SPREAD başınadır ve diyagramlar ona sığacak şekilde
        # ORANTILI küçülür — K19'un dizgideki karşılığı.
        budget = h0 * DIAGRAM_PAGE_BUDGET
        dia = [SVGFlow(d, w0, budget / max(len(docs), 1)) for d in docs]
        dia_h = sum(d.wrap(w0, h0)[1] for d in dia)
        total_h = sum(fl.wrap(w0, h0)[1] for fl in stream)
        # Akış flowable sınırında kesilir, tam hedefte değil; bu yüzden
        # sağ sayfaya bir pay bırakılır.
        slack = h0 * 0.04
        right_cap = max(h0 - dia_h - slack, 0.0)
        left_target = min(h0, max(total_h - right_cap, total_h * 0.5))

        used, rest = lay.flow(stream, "game", run_head=cur_family,
                              max_pages=1, height_cap=left_target)
        # SAĞ sayfa — diyagramlar ÜSTTE, sonra akışın geri kalanı
        right = lay.new_page("game")
        right.runHead = g["title"]
        used_r, rest_r = lay.flow(dia + list(rest), "game",
                                  run_head=g["title"], start_page=right,
                                  max_pages=1)
        if rest_r:
            # ÇİFT SAYFAYA SIĞMADI → dört sayfa. Mimarî izin verir
            # (EDITORIAL_ARCHITECTURE § 2, azami altı madde).
            overflow.append(g["gameId"])
            lay.flow(rest_r, "game", run_head=g["title"], max_pages=2)
            if (lay.n - first + 1) % 2:
                q = lay.new_page("game")
                q.blank = True
                q.runHead = g["title"]
        spreads.append((g["gameId"], first, lay.n - first + 1))

    body_end = lay.n

    # ⑦ ARKA MADDE ---------------------------------------------------------
    back_start = lay.n + 1
    _back_matter(lay, bm, sty, pagemap,
                 {g["gameId"]: g["title"] for g in book["games"]},
                 cfg=cfg)

    # ⑧ İÇİNDEKİLER'İ GERÇEK SAYFALARLA DOLDUR ------------------------------
    # İçindekiler ÖNCE yer tutar, SONRA gerçek numaralarla doldurulur:
    # sayfa numarası ölçülmeden yazılmaz (kurucu § 27).
    ok = _refill(lay, toc_pages_start, toc_flow_pages,
                 _toc_flowables(fm, sty, pagemap, lay.back_pages), sty)

    # POD ÇİFT SAYFA İSTER. Tek sayılı bir blok basılamaz; matbaa son
    # yaprağı zaten ekler ve eklediği yaprak KİTABIN İÇİNDE görünür.
    if lay.n % 2:
        q = lay.new_page("blank")
        q.blank = True
        q.folio = False

    return lay, {"tocFitted": ok,
                 "pagemap": pagemap, "spreads": spreads,
                 "overflow": overflow, "frontPages": front_pages,
                 "bodyEnd": body_end, "backStart": back_start,
                 "diagramRatios": dia_ratio}


def _center(lay, page_no, frac):
    x, y_top, w, h = lay.frame(page_no)
    return x, y_top - h * frac, w


def _refill(lay, start_page, npages, flowables, sty):
    """İçindekiler sayfalarını YERİNDE yeniden doldurur."""
    pages = lay.pages[start_page - 1:start_page - 1 + npages]
    for p in pages:
        p.items = []
    queue = list(flowables)
    for i, p in enumerate(pages):
        idx = start_page + i
        x, y_top, w, h = lay.frame(idx)
        y, bottom = y_top, y_top - h
        while queue:
            fl = queue[0]
            fw, fh = fl.wrap(w, max(y - bottom, 1))
            if fh > (y - bottom) + 0.01:
                break
            p.items.append((fl, x, y - fh, w))
            y -= fh
            queue.pop(0)
    return len(queue) == 0


def _back_matter(lay, bm, sty, pagemap, titles=None, cfg=None):
    from reportlab.platypus import Paragraph
    P = lambda t, s: Paragraph(t, sty[s])  # noqa: E731
    lay.back_pages = {}
    # ⚠ OKUR `gameId` GÖRMEZ. Malzeme rehberi ve sözlük oyunları iç
    # kimlikleriyle listeliyordu ("li-b-el-merafib", "bao-la-kiswahili");
    # kitapta o adlar hiçbir yerde geçmez ve okur onları arayamaz.
    titles = titles or {}

    def names(ids):
        return ", ".join(titles.get(i, i) for i in ids)

    def section(key, heading, flowables, standfirst=None):
        lay.pad_to_recto()
        lay.back_pages[key] = lay.n + 1
        fls = [P("<b>%s</b>" % esc(heading), "sect")]
        if standfirst:
            fls.append(P(esc(standfirst), "stand"))
        fls += flowables
        first_bk = lay.n + 1
        lay.flow(fls, "back", run_head=heading)
        lay.pages[first_bk - 1].opensSection = True

    # ① tahta şablonları — fotokopiye uygun, TAM ÖLÇEK
    tpl = []
    # Şablonlar SAYFA SIRASINDA. İlk sürümde tanımlayıcı dosyalarının
    # sırasındaydılar, yani okura RASTGELE görünüyorlardı.
    for t in sorted(bm["boardTemplates"],
                    key=lambda x: (pagemap.get(x["gameId"]) or 9999,
                                   x["title"])):
        pg = pagemap.get(t["gameId"])
        tpl.append(P("<b>%s</b> &nbsp; <font size=%s>%s%s</font>"
                     % (esc(t["title"]), sty["_fs"](8),
                        "page %d" % pg if pg else "",
                        " · reconstructed" if t["reconstructed"] else ""),
                     "idx"))
    section("boardTemplates", "Board Templates", tpl,
            "Every board in this book, listed with the page its game is on. "
            "The diagrams beside each game are drawn to scale and photocopy "
            "cleanly at full size; this book was made 8.5 by 11 inches for "
            "exactly that reason.")

    # ② malzeme rehberi
    mat = []
    for m in sorted(bm["materialsGuide"], key=lambda x: -x["count"]):
        mat.append(P("<b>%s</b> <font size=%s>— used by %d game%s</font>"
                     % (esc(m["substitute"]), sty["_fs"](8), m["count"],
                        "" if m["count"] == 1 else "s"), "idxh"))
        mat.append(P(esc(names(m["usedBy"])), "idx"))
    section("materialsGuide", "Materials and Substitutions", mat,
            "What to use instead of what. Nothing in this book needs to be "
            "bought.")

    # ③ sözlük
    gl = []
    for t in sorted(bm["glossary"], key=lambda x: x["term"]):
        att = (" <font size=%s>(%s)</font>"
               % (sty["_fs"](7.5),
                  esc(names(t["attestedIn"][:6])))) if t["attestedIn"] else ""
        gl.append(P("<b>%s</b> &nbsp;%s%s"
                    % (esc(t["term"]), esc(t["definition"]), att), "idx"))
    section("glossary", "Glossary", gl,
            "The words this book uses for mechanics. Where a term is used in "
            "the rules of particular games, those games are named after it.")

    # ④ kaynakça
    bib = []
    for b in sorted(bm["bibliography"], key=lambda x: x["title"]):
        pg = pagemap.get(b["gameId"])
        bib.append(P("<b>%s</b> <font size=%s>· %s%s</font>"
                     % (esc(b["title"]), sty["_fs"](8), esc(b["culture"]),
                        " · page %d" % pg if pg else ""), "idxh"))
        for s in b["sources"]:
            bib.append(P(esc(s), "idx"))
    section("bibliography", "Sources", bib,
            "Every game, with the work the rules were read from. Where a "
            "source was opened at page level the pages are named.")

    # ⑤ ÜÇ İNDEKS
    idx_specs = [("idx-culture", "Index by Culture", "byCulture", None),
                 ("idx-players", "Index by Number of Players", "byPlayerCount",
                  "bucketLabels"),
                 ("idx-duration", "Index by Time and Age", "byDurationAndAge",
                  "bucketLabels")]
    for key, heading, block, lblkey in idx_specs:
        blk = bm["indexes"][block]
        labels = blk.get(lblkey) or {}
        rows = []
        for bucket in sorted(blk["buckets"]):
            rows.append(P("<b>%s</b>" % esc(labels.get(bucket, bucket)), "idxh"))
            for r in sorted(blk["buckets"][bucket], key=lambda x: x["title"]):
                pg = pagemap.get(r["gameId"])
                rows.append(P("%s &nbsp;%s" % (esc(r["title"]),
                                               pg if pg else "—"), "idx"))
        section(key, heading, rows)

    # ⑥ uydurulmuş gelenekler
    inv = []
    for t in bm["inventedTraditions"]:
        inv.append(P("<b>%s</b>" % esc(t["claim"]), "h2"))
        inv.append(P("<i>%s</i> %s" % (esc(t["verdict"]), esc(t["detail"])),
                     "body"))
    section("inventedTraditions", "Invented Traditions", inv,
            "Origin stories that are widely repeated and are not supported by "
            "anything. They are collected here because a reader who has been "
            "told one of them deserves to know where it came from.")

    # ⑦ eşlikçi — KİTABIN SON SÖZÜ, ve okurun bize dönebileceği tek kapı.
    #
    # Amazon okurun adresini vermez ve hiç vermeyecek. Bir Valice okuruna
    # ikinci kez seslenebileceğimiz tek yer, zaten satın aldığı kitabın
    # içidir. Bu sayfa 2026-09-02'de eklendi: kitabın basılı sürümleri
    # eşlikçiden önce dizilmişti, dolayısıyla bugüne kadar hiçbir okur onun
    # var olduğunu öğrenemedi.
    #
    # KDP bağlantı kuralı: bir bağlantının amacı müşteri bilgisi toplamak
    # olamaz. Burada e-posta yok, form yok, kayıt yok — yalnızca ücretsiz
    # ve gerçek bir materyal. Ev kuralı da aynı yönde: önce değer.
    comp = (cfg or {}).get("companion") or {}
    url = comp.get("url")
    if url:
        items = comp.get("items") or []
        c = [P(esc(comp.get("standfirst", "")), "body")] if comp.get("standfirst") else []
        for it in items:
            c.append(P("<b>%s</b> &nbsp; %s" % (esc(it["name"]), esc(it.get("detail", ""))),
                       "body"))
        c.append(P("<b>%s</b>" % esc(url), "h2"))
        c.append(P(esc("Free, and free of conditions: nothing to sign up for, no email "
                       "asked, no account needed. Print what you want and play."), "body"))

        # BİLEREK `section()` DEĞİL. `section()` önce `pad_to_recto()` çağırır
        # ve bu, kitabı 160'tan 162 sayfaya çıkarır — sırt kalınlığı değişir,
        # kapak geçersizleşir, yayımlanmış bir kitap için tek dosyalık bir
        # güncelleme iki dosyalık bir revizyona dönüşür. Kitap zaten boş bir
        # son sayfayla bitiyor; bu bölüm oraya akar ve sayfa sayısı sabit
        # kalır. Sabit kalıp kalmadığını `05_TESTS` değil, üretim çıktısının
        # kendisi söyler: build 160 yazmıyorsa bu değişiklik geri alınmalıdır.
        lay.back_pages["companion"] = lay.n + 1
        heading = comp.get("heading", "The companion")
        lay.flow([P("<b>%s</b>" % esc(heading), "sect")] + c, "back",
                 run_head=heading)


# ── ÇİZİM ────────────────────────────────────────────────────────────────
def render(lay, path, cfg, geom, sty, title, author):
    from reportlab.pdfgen import canvas as rl_canvas
    c = rl_canvas.Canvas(path, pagesize=(geom["wPt"], geom["hPt"]),
                         pageCompression=1)
    c.setTitle(title)
    c.setAuthor(author)
    c.setSubject("Traditional games of the world — rules, boards and sources")
    c.setCreator("04_BUILD/interior.py · The Great Book of World Games")
    for i, p in enumerate(lay.pages, 1):
        c.setFont("GBSerif", 10.5)      # sayfanın varsayılan fontu GÖMÜLÜ
        for fl, x, y, w in p.items:
            fl.wrap(w, geom["hPt"])
            fl.drawOn(c, x, y)
        if not p.blank:
            _furniture(c, lay, i, p, geom, title)
        c.showPage()
    c.save()


def _furniture(c, lay, i, p, geom, title):
    """Üstbilgi ve sayfa numarası. Boş sayfada YOKTUR."""
    verso = lay.is_verso(i)
    x_in, y_top, w, h = lay.frame(i)
    # Büyük puntoda üstbilgi/folyo da büyür (geom → headPt/folioPt);
    # öteki sürümlerde değerler eskisiyle aynıdır.
    scale = geom.get("typeScale", 1.0)
    c.setFont("GBSerif-I", geom.get("headPt", 8.5))
    c.setFillColorRGB(0, 0, 0)
    # Üstbilgi Paragraph'tan değil DOĞRUDAN tuvalden geçer, yani esc()'i
    # görmez. Dizgi tırnağını burada ayrıca uygulamak ZORUNLU: aksi
    # halde gövdede "Nine Men’s Morris", üstbilgide "Nine Men's
    # Morris" basılır — aynı sayfada iki farklı kesme işareti.
    # xml_text() DEĞİL smart(): tuval XML kaçışı beklemez, `&amp;`
    # sayfaya harfi harfine basılırdı.
    head = typo.smart(p.runHead or title)
    # Bölümün AÇILIŞ sayfasında üstbilgi başlığı TEKRARLAR ve bu bir
    # dizgi hatasıdır: "Contents" bir kez üstbilgide, bir kez H1'de
    # basılıyordu. Standart uygulama açılış sayfasında üstbilgiyi
    # bastırmaktır.
    if p.opensSection:
        return
    # ⚠ Üstbilgi/folyo UZAKLIĞI ölçeklenmez: büyük puntoda 13×1,52 pt
    # yukarı çıkan üstbilgi sayfa üstüne 0,22 in yaklaşıyordu ve KDP'nin
    # 0,25 in mürekkep payını 200 sayfada ihlal ediyordu (kdp_preflight
    # ölçtü). Punto büyür, konum sabit kalır.
    if p.kind != "front" or p.runHead:
        hy = geom["hPt"] - geom["topPt"] + 13
        if verso:
            c.drawString(x_in, hy, head)
        else:
            c.drawRightString(x_in + w, hy, head)
    if p.folio:
        c.setFont("GBSerif", geom.get("folioPt", 9.5))
        fy = geom["bottomPt"] - 20
        if verso:
            c.drawString(x_in, fy, str(i))
        else:
            c.drawRightString(x_in + w, fy, str(i))


# ── SÜRÜM ────────────────────────────────────────────────────────────────
def geometry(cfg, edition: str, pages_guess: int) -> dict:
    prod = cfg["production"]
    # largeprint = ciltsiz trim + büyük punto (project_config → production.largePrint)
    trim = prod["trimHardcover" if edition == "hardcover" else "trimPaperback"]
    bare_min = gutter_in(pages_guess)           # KDP'nin ÇIPLAK asgarisi
    g_in = bare_min + GUTTER_SAFETY_IN           # dizginin GERÇEKTEN kullandığı
    # Ciltli ciltte blok dikişe daha yakın oturur: bir kademe fazla iç marj.
    if edition == "hardcover":
        g_in += 0.125
    outer_in = 0.5
    g = {
        "edition": edition,
        "trimWidthIn": trim["w"], "trimHeightIn": trim["h"],
        "wPt": trim["w"] * IN, "hPt": trim["h"] * IN,
        "gutterIn": g_in, "outerIn": outer_in,
        "gutterBareMinIn": bare_min, "gutterSafetyIn": GUTTER_SAFETY_IN,
        "topIn": 0.625, "bottomIn": 0.625,
        "gutterPt": g_in * IN, "outerPt": outer_in * IN,
        "topPt": 0.625 * IN, "bottomPt": 0.625 * IN,
        "bleed": False,
        "colWidthMm": (trim["w"] - g_in - outer_in) * 25.4,
        "bodyPt": 10.5, "leadingPt": 13.5, "typeScale": 1.0,
        "font": "Liberation Serif (SIL OFL 1.1, embedded)",
    }
    if edition == "largeprint":
        lp = prod["largePrint"]
        scale = lp["bodyPt"] / 10.5
        g.update({
            "largePrint": True,
            "bodyPt": lp["bodyPt"],
            "leadingPt": round(13.5 * scale, 2),
            "typeScale": scale,
            "minPt": lp["minimumPt"],
            "headPt": max(8.5 * scale, lp["minimumPt"]),
            "folioPt": max(9.5 * scale, lp["minimumPt"]),
            "editionLabel": lp["editionLabel"],
            "lpDiagramBudget": lp["diagramPageBudget"],
        })
    return g


def build_edition(root, cfg, edition, out_dir, verbose=True):
    fdir = register_fonts()
    mdir = cfg["language"]["commercialManuscriptDir"]
    book = load(os.path.join(root, mdir, "book.json"))
    fm = load(os.path.join(root, mdir, "frontmatter.json"))
    bmp = os.path.join(root, mdir, "backmatter_printed.json")
    bm = load(bmp if os.path.exists(bmp)
              else os.path.join(root, mdir, "backmatter.json"))

    import svg_vector as sv
    ddir = os.path.join(root, "07_ASSETS", "diagrams")
    diagram_docs = {}
    for fn in sorted(os.listdir(ddir)):
        if fn.endswith(".svg"):
            diagram_docs[fn[:-4]] = sv.parse(os.path.join(ddir, fn))

    # HERO GÖRSELLERİ — gameId'ye göre eşlenir (dosya adı GBK02_GAME_NNN_
    # SLUG_HERO.jpg; NNN book.json games[] içindeki 1-tabanlı sıradır).
    # PRINT İÇİN plates_print/ kullanılır: gri tonlama + küçültülmüş JPEG
    # (bkz. 07_ASSETS/plates/ — orijinal renkli PNG kaynak, dijital/EPUB
    # sürümler için saklanır, iç bloğa GİRMEZ). Kitap siyah mürekkep
    # ekonomisiyle fiyatlandırılır (project_config.json → ink: "black");
    # renkli bir görsel iç blokta baskı presine kontrolsüz bırakılmaz,
    # gri dönüşüm burada YAPILIR (07_BUILD/… optimize_plates.py).
    pdir = os.path.join(root, "07_ASSETS", "plates_print")
    if not os.path.isdir(pdir):
        pdir = os.path.join(root, "07_ASSETS", "plates")  # yedek: optimize edilmemiş
    plate_docs = {}
    if os.path.isdir(pdir):
        order = [g["gameId"] for g in book["games"]]
        for fn in sorted(os.listdir(pdir)):
            m = re.match(r"GBK02_GAME_(\d{3})_.*_HERO\.(jpg|png)$", fn)
            if m:
                idx = int(m.group(1)) - 1
                if 0 <= idx < len(order):
                    plate_docs[order[idx]] = os.path.join(pdir, fn)

    # İÇ MARJ DÖNGÜSÜ: marj sayfa sayısına bağlı, sayfa sayısı marja.
    guess, seen = 200, []
    for _ in range(6):
        geom = geometry(cfg, edition, guess)
        if geom.get("largePrint"):
            sty = styles(10.5, 13.5, geom["typeScale"], geom["minPt"])
        else:
            sty = styles(geom["bodyPt"], geom["leadingPt"])
        lay, meta = build_layout(root, cfg, book, fm, bm, geom, sty,
                                 diagram_docs, plate_docs)
        n = lay.n
        seen.append((guess, n))
        if gutter_in(n) == gutter_in(guess):
            break
        guess = n
    else:
        raise RuntimeError("iç marj döngüsü yakınsamadı: %s" % seen)

    os.makedirs(out_dir, exist_ok=True)
    name = "GreatBookOfWorldGames_interior_%s.pdf" % edition
    path = os.path.join(out_dir, name)
    render(lay, path, cfg, geom, sty, fm["titlePage"]["title"],
           fm["titlePage"]["author"])

    kinds = {}
    for p in lay.pages:
        kinds[p.kind] = kinds.get(p.kind, 0) + 1
    blanks = sum(1 for p in lay.pages if p.blank)
    verso_start = sum(1 for gid, first, _ in meta["spreads"] if first % 2 == 0)

    report = {
        "edition": edition,
        "file": os.path.relpath(path, root),
        "pageCount": lay.n,
        "sha256": sha256(path),
        "bytes": os.path.getsize(path),
        "trim": {"widthIn": geom["trimWidthIn"], "heightIn": geom["trimHeightIn"]},
        "margins": {"gutterIn": geom["gutterIn"], "outerIn": geom["outerIn"],
                    "topIn": geom["topIn"], "bottomIn": geom["bottomIn"],
                    "gutterBareMinIn": geom["gutterBareMinIn"],
                    "gutterSafetyIn": geom["gutterSafetyIn"]},
        "kdpGutterRequiredIn": gutter_in(lay.n),
        "bleed": False,
        "font": geom["font"], "fontDir": fdir,
        "games": len(book["games"]),
        "spreadsStartingVerso": verso_start,
        "spreadsTotal": len(meta["spreads"]),
        "fourPageEntries": meta["overflow"],
        "blankPages": blanks,
        "pageKinds": kinds,
        "frontMatterPages": meta["frontPages"],
        "bodyEndPage": meta["bodyEnd"],
        "backMatterStartPage": meta["backStart"],
        "pagemap": meta["pagemap"],
        "gutterIterations": seen,
        "tocFitted": meta.get("tocFitted", True),
    }
    if geom.get("largePrint"):
        from reportlab.lib.styles import ParagraphStyle
        min_font = min(v.fontSize for v in sty.values()
                       if isinstance(v, ParagraphStyle))
        min_font = min(min_font, float(sty["_fs"](7.5)))
        per_game = {gid: n_pages for gid, first, n_pages in meta["spreads"]}
        report.update({
            "largePrint": True,
            "editionLabel": geom["editionLabel"],
            "bodyPt": geom["bodyPt"], "leadingPt": geom["leadingPt"],
            "typeScale": round(geom["typeScale"], 4),
            "minFontPtSet": round(min_font, 2),
            "headPt": round(geom["headPt"], 2), "folioPt": round(geom["folioPt"], 2),
            "pagesPerGame": per_game,
            "pagesPerGameMax": max(per_game.values()) if per_game else 0,
            "pagesPerGameMean": round(sum(per_game.values()) / len(per_game), 2)
            if per_game else 0,
            "diagramScaleVsPaperbackMin": min(meta["diagramRatios"])
            if meta["diagramRatios"] else None,
            "diagramCount": len(meta["diagramRatios"]),
        })
    dump(os.path.join(root, "06_REPORTS", "interior-%s.json" % edition), report)
    if verbose:
        print("  ✓ %-10s %3d sayfa · %5.1f KB · trim %.2f×%.2f in · "
              "iç marj %.3f in (KDP asgari %.3f + %.3f emniyet payı)"
              % (edition, lay.n, os.path.getsize(path) / 1024.0,
                 geom["trimWidthIn"], geom["trimHeightIn"],
                 geom["gutterIn"], gutter_in(lay.n), GUTTER_SAFETY_IN))
        print("     çift sayfa: %d/%d madde SOL sayfada başlıyor · dört "
              "sayfalık madde: %s · boş sayfa: %d"
              % (verso_start, len(meta["spreads"]),
                 ", ".join(meta["overflow"]) or "yok", blanks))
    return report


def run_check(root, cfg) -> int:
    errs = []
    for ed in ("paperback", "hardcover"):
        p = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if not os.path.exists(p):
            errs.append("%s iç bloğu ÜRETİLMEMİŞ" % ed)
            continue
        r = load(p)
        f = os.path.join(root, r["file"])
        if not os.path.exists(f):
            errs.append("%s PDF yok: %s" % (ed, r["file"]))
            continue
        if sha256(f) != r["sha256"]:
            errs.append("%s PDF sağlama toplamı tutmuyor — dosya değişmiş" % ed)
        if r["spreadsStartingVerso"] != r["spreadsTotal"]:
            errs.append("%s: %d madde SOL sayfada BAŞLAMIYOR — çift sayfa "
                        "sözü bozuldu" % (ed, r["spreadsTotal"]
                                          - r["spreadsStartingVerso"]))
        if r["margins"]["gutterIn"] < r["kdpGutterRequiredIn"]:
            errs.append("%s: iç marj %.3f in < KDP asgari %.3f in"
                        % (ed, r["margins"]["gutterIn"],
                           r["kdpGutterRequiredIn"]))
        if r["pageCount"] % 2:
            errs.append("%s: sayfa sayısı TEK (%d) — POD çift ister"
                        % (ed, r["pageCount"]))
        cost = cfg["production"]["kdpPrintCost"][
            "paperbackLargeTrimBW" if ed == "paperback"
            else "hardcoverLargeTrimBW"]
        if not (cost["minPages"] <= r["pageCount"] <= cost["maxPages"]):
            errs.append("%s: sayfa sayısı KDP bandı dışında (%d ∉ [%d, %d])"
                        % (ed, r["pageCount"], cost["minPages"],
                           cost["maxPages"]))
        if not r.get("tocFitted", True):
            errs.append("%s: içindekiler ayrılan sayfalara SIĞMADI — "
                        "gerçek sayfa numaraları kesildi" % ed)
        if len(r["fourPageEntries"]) > 6:
            errs.append("%s: dört sayfalık madde %d > 6 (mimarî tavan)"
                        % (ed, len(r["fourPageEntries"])))
    # ── BÜYÜK PUNTO (varsa) — çift-sayfa sözü YOK, punto tabanı VAR ──────
    lp_path = os.path.join(root, "06_REPORTS", "interior-largeprint.json")
    lp = None
    if os.path.exists(lp_path):
        lp = load(lp_path)
        f = os.path.join(root, lp["file"])
        lpc = cfg["production"].get("largePrint", {})
        if not os.path.exists(f):
            errs.append("largeprint PDF yok: %s" % lp["file"])
        elif sha256(f) != lp["sha256"]:
            errs.append("largeprint PDF sağlama toplamı tutmuyor — dosya değişmiş")
        if lp["margins"]["gutterIn"] < lp["kdpGutterRequiredIn"]:
            errs.append("largeprint: iç marj %.3f in < KDP asgari %.3f in"
                        % (lp["margins"]["gutterIn"], lp["kdpGutterRequiredIn"]))
        if lp["pageCount"] % 2:
            errs.append("largeprint: sayfa sayısı TEK (%d)" % lp["pageCount"])
        cost = cfg["production"]["kdpPrintCost"]["paperbackLargeTrimBW"]
        if not (cost["minPages"] <= lp["pageCount"] <= cost["maxPages"]):
            errs.append("largeprint: sayfa sayısı KDP bandı dışında (%d ∉ [%d, %d])"
                        % (lp["pageCount"], cost["minPages"], cost["maxPages"]))
        if not lp.get("tocFitted", True):
            errs.append("largeprint: içindekiler ayrılan sayfalara SIĞMADI")
        if lp.get("bodyPt", 0) < lpc.get("bodyPt", 16):
            errs.append("largeprint: gövde puntosu %.1f < %.1f"
                        % (lp.get("bodyPt", 0), lpc.get("bodyPt", 16)))
        if lp.get("minFontPtSet", 0) < lpc.get("minimumPt", 12):
            errs.append("largeprint: en küçük punto %.2f < taban %.2f"
                        % (lp.get("minFontPtSet", 0), lpc.get("minimumPt", 12)))
        if (lp.get("diagramScaleVsPaperbackMin") or 1.0) < 0.98:
            errs.append("largeprint: bir diyagram ciltsizdekinden KÜÇÜK (oran %.3f)"
                        % lp["diagramScaleVsPaperbackMin"])
    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        return 1
    for ed in ("paperback", "hardcover"):
        r = load(os.path.join(root, "06_REPORTS", "interior-%s.json" % ed))
        print("  ✓ %-10s %3d sayfa · %d/%d madde SOL sayfada · iç marj "
              "%.3f in ≥ %.3f" % (ed, r["pageCount"],
                                  r["spreadsStartingVerso"], r["spreadsTotal"],
                                  r["margins"]["gutterIn"],
                                  r["kdpGutterRequiredIn"]))
    if lp:
        print("  ✓ %-10s %3d sayfa · gövde %.1f pt · en küçük %.2f pt · "
              "diyagram oranı ≥ %s · iç marj %.3f in ≥ %.3f"
              % ("largeprint", lp["pageCount"], lp["bodyPt"], lp["minFontPtSet"],
                 lp.get("diagramScaleVsPaperbackMin"),
                 lp["margins"]["gutterIn"], lp["kdpGutterRequiredIn"]))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--edition",
                    choices=["paperback", "hardcover", "largeprint"])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    cfg = load(os.path.join(root, "project_config.json"))

    try:
        import reportlab  # noqa: F401
    except ImportError:
        print("  ⊘ reportlab yok — iç blok ATLANDI")
        return 2

    mdir = cfg["language"]["commercialManuscriptDir"]
    if not os.path.exists(os.path.join(root, mdir, "book.json")):
        print("  · ticari manuscript bu depoda yok — iç blok ATLANDI "
              "(CI'da beklenen)")
        return 0

    print("=" * 74)
    print("  İÇ BLOK ÜRETECİ")
    print("=" * 74)
    if args.check:
        rc = run_check(root, cfg)
        print("=" * 74)
        return rc

    editions = (["paperback", "hardcover"] if args.all or not args.edition
                else [args.edition])
    out_dirs = {"paperback": "PAPERBACK", "hardcover": "HARDCOVER",
                "largeprint": "LARGEPRINT"}
    for ed in editions:
        out = os.path.join(root, "08_OUTPUT", out_dirs[ed])
        build_edition(root, cfg, ed, out)
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
