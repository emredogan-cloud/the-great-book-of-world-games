#!/usr/bin/env python3
"""
KAPAK ÜRETECİ — The Great Book of World Games
================================================================================
Sırt genişliğini, tam sarım geometrisini ve güvenli alanları **ölçülen sayfa
sayısından** hesaplar; kurucu sanatı geldiğinde tam sarım kapağı basar.

── SIRT SAYFA SAYISINDAN GELİR ─────────────────────────────────────────
Yol haritası Faz 6 § 8 bunu bir SIRA kuralı yapar:

    Kapak kapısı iç blok kapısından SONRA koşar: sayfa sayısı değişirse
    sırt kayar ve eski kapak GEÇERSİZ olur.

Bu yüzden burada hiçbir sayfa sayısı gömülü DEĞİLDİR. Kaynak tek:
`06_REPORTS/interior-<edition>.json § pageCount` — ki o da `interior.py`ın
SAYDIĞI değerdir, modelin tahmin ettiği değil.

── VARLIK KAPISI ───────────────────────────────────────────────────────
Kapak SANATI kurucu tarafından üretilir (§ 11). Bu betik sanat yokken de
koşar ve GEOMETRİYİ üretir; kompozisyonu YAPMAZ ve yaptığını iddia etmez.
Sanat `07_ASSETS/raw/cover/` altına düştüğünde `--build` devreye girer.

── TİPOGRAFİ ───────────────────────────────────────────────────────────
Kapak yazısı DETERMİNİSTİK ve VEKTÖRDÜR (§ 14): sanatın üstüne beyaz kutu
konmaz, yazı rasterlenmez. Aynı girdi her koşuda byte-byte aynı PDF verir.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
IN = 72.0

# ── KDP GEOMETRİ SABİTLERİ ───────────────────────────────────────────────
# Amazon.com · KDP yardım sayfalarının yayımladığı değerler.
#
# ⚠ CİLTSİZ değerleri KDP'nin kendi formülüdür ve yıllardır sabittir.
# ⚠ CİLTLİ değerleri HİPOTEZDİR ve KURUCU DOĞRULAMASI BEKLER: KDP ciltli
#   kapak şablonunu bir üreteçle verir (kalıp payı, menteşe ve tahta
#   kalınlığı dahil) ve o şablon indirilmeden ciltli kapak BASILMAZ.
#   Bu betik ciltli geometriyi HESAPLAR ama `founderConfirmedTemplate`
#   false olduğu sürece çıktıyı "TEMPLATE PENDING" diye işaretler.
SPINE_PER_PAGE_IN = {
    "paperback": 0.002252,      # beyaz kâğıt · siyah-beyaz mürekkep
    "hardcover": 0.0025,        # HİPOTEZ — şablonla doğrulanacak
}
HARDCOVER_BOARD_IN = 0.06       # HİPOTEZ — tahta payı
BLEED_IN = 0.125
COVER_SAFE_IN = 0.25            # trim kenarından metin/logo uzaklığı
SPINE_TEXT_MIN_PAGES = 79       # KDP: sırta yazı ancak bu sayfadan sonra
BARCODE_W_IN, BARCODE_H_IN = 2.0, 1.2
BARCODE_CLEAR_IN = 0.25


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def geometry(cfg, edition: str, pages: int) -> dict:
    trim = cfg["production"]["trimPaperback" if edition == "paperback"
                             else "trimHardcover"]
    tw, th = trim["w"], trim["h"]
    spine = pages * SPINE_PER_PAGE_IN[edition]
    if edition == "hardcover":
        spine += HARDCOVER_BOARD_IN
    wrap_w = tw * 2 + spine + BLEED_IN * 2
    wrap_h = th + BLEED_IN * 2

    # Sarımın sol kenarından ölçülen bölge sınırları
    back_x0 = BLEED_IN
    spine_x0 = back_x0 + tw
    front_x0 = spine_x0 + spine
    front_x1 = front_x0 + tw

    g = {
        "edition": edition,
        "pageCount": pages,
        "trimWidthIn": tw, "trimHeightIn": th,
        "bleedIn": BLEED_IN, "safeIn": COVER_SAFE_IN,
        "spineWidthIn": round(spine, 4),
        "spinePerPageIn": SPINE_PER_PAGE_IN[edition],
        "spineTextAllowed": pages >= SPINE_TEXT_MIN_PAGES,
        "spineTextMinPages": SPINE_TEXT_MIN_PAGES,
        "wrapWidthIn": round(wrap_w, 4), "wrapHeightIn": round(wrap_h, 4),
        "wrapWidthPt": round(wrap_w * IN, 2),
        "wrapHeightPt": round(wrap_h * IN, 2),
        "zones": {
            "backCover": {"x0": round(back_x0, 4), "x1": round(spine_x0, 4)},
            "spine":     {"x0": round(spine_x0, 4), "x1": round(front_x0, 4)},
            "frontCover": {"x0": round(front_x0, 4), "x1": round(front_x1, 4)},
        },
        "safeZones": {
            "backCopy": {
                "x0": round(back_x0 + COVER_SAFE_IN, 4),
                "x1": round(spine_x0 - COVER_SAFE_IN, 4),
                "y0": round(BLEED_IN + COVER_SAFE_IN, 4),
                "y1": round(BLEED_IN + th - COVER_SAFE_IN, 4)},
            "spineText": {
                "x0": round(spine_x0 + 0.0625, 4),
                "x1": round(front_x0 - 0.0625, 4),
                "y0": round(BLEED_IN + 0.5, 4),
                "y1": round(BLEED_IN + th - 0.5, 4)},
            "frontTitle": {
                "x0": round(front_x0 + COVER_SAFE_IN, 4),
                "x1": round(front_x1 - COVER_SAFE_IN, 4),
                "y0": round(BLEED_IN + th * 0.60, 4),
                "y1": round(BLEED_IN + th - COVER_SAFE_IN, 4)},
            "frontAuthor": {
                "x0": round(front_x0 + COVER_SAFE_IN, 4),
                "x1": round(front_x1 - COVER_SAFE_IN, 4),
                "y0": round(BLEED_IN + COVER_SAFE_IN, 4),
                "y1": round(BLEED_IN + th * 0.18, 4)},
            "barcode": {
                "x0": round(spine_x0 - BARCODE_CLEAR_IN - BARCODE_W_IN, 4),
                "x1": round(spine_x0 - BARCODE_CLEAR_IN, 4),
                "y0": round(BLEED_IN + BARCODE_CLEAR_IN, 4),
                "y1": round(BLEED_IN + BARCODE_CLEAR_IN + BARCODE_H_IN, 4),
                "$note": "KDP barkodu KENDİSİ basar. Bu alan BOŞ ve sade "
                         "bırakılır; sahte barkod çizilmez."},
        },
        "artworkTarget": {
            "$note": "Kurucu sanatının HAM hedefi. 300 ppi baskı standardıdır; "
                     "daha yüksek çözünürlük zarar vermez, düşüğü POD'da "
                     "görünür.",
            "ppi": 300,
            "widthPx": int(round(wrap_w * 300)),
            "heightPx": int(round(wrap_h * 300)),
            "frontOnlyWidthPx": int(round((tw + BLEED_IN) * 300)),
            "frontOnlyHeightPx": int(round(wrap_h * 300)),
        },
    }
    if edition == "hardcover":
        g["$hardcoverWarning"] = (
            "CİLTLİ GEOMETRİ HİPOTEZDİR. KDP ciltli kapak şablonunu bir "
            "üreteçle verir; kalıp payı, menteşe ve tahta kalınlığı oradan "
            "okunur. KURUCU EYLEMİ: şablonu indir, buradaki sırt ve sarım "
            "ölçüleriyle KARŞILAŞTIR, farklıysa project_config.json içine "
            "gerçek değerleri yaz.")
        g["founderConfirmedTemplate"] = bool(
            cfg.get("production", {}).get("hardcoverTemplateConfirmed"))
    return g



def feathered_scrim(im, box_in, wrap_w_in, wrap_h_in, strength=0.62,
                    feather_in=0.55):
    """Metnin arkasına TÜYLENMİŞ bir parşömen yıkaması uygular.

    ⚠ BU BİR BEYAZ PANEL DEĞİLDİR ve öyle görünmez. § 7 beyaz kutuyu,
    beyaz başlık kartını ve beyaz sırt şeridini YASAKLAR; aynı madde
    *"measured contrast support only where needed"* der. Buradaki destek
    ÖLÇÜMLE gerekçelidir: arka kapak metin bloğunun sd değeri 27,7'dir ve
    kırmızı seyahat çizgileri metnin içinden geçer.

    Yıkama, sanatın KENDİ açık parşömen tonundan alınır (ortalama üst
    yüzdelik), kenarları yarım inçten uzun bir Gauss ile tüylendirilir ve
    hiçbir yerde tam opak olmaz. Sonuç bir kutu değil, kâğıdın o bölgede
    biraz daha açık olmasıdır.
    """
    from PIL import Image, ImageFilter, ImageStat
    W, H = im.size
    x0 = int(box_in[0] / wrap_w_in * W); x1 = int(box_in[2] / wrap_w_in * W)
    y0 = int((wrap_h_in - box_in[3]) / wrap_h_in * H)
    y1 = int((wrap_h_in - box_in[1]) / wrap_h_in * H)
    # yıkama rengi: bölgenin KENDİ açık tonu (sanattan alınır, uydurulmaz)
    reg = im.crop((x0, y0, x1, y1))
    px = sorted(reg.convert("L").getdata())
    light = px[int(len(px) * 0.92)]
    st = ImageStat.Stat(reg)
    r, g, b = [min(255, int(c * (light / max(1.0, st.mean[0])))) for c in st.mean[:3]]
    pad = int(feather_in / wrap_w_in * W)
    mask = Image.new("L", (W, H), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).rectangle([x0 + pad // 2, y0 + pad // 2,
                                    x1 - pad // 2, y1 - pad // 2],
                                   fill=int(255 * strength))
    mask = mask.filter(ImageFilter.GaussianBlur(pad * 0.75))
    wash = Image.new("RGB", (W, H), (r, g, b))
    return Image.composite(wash, im, mask), {
        "boxIn": list(box_in), "washRGB": [r, g, b],
        "strength": strength, "featherIn": feather_in,
        "$note": "tüylenmiş yıkama · beyaz panel DEĞİL · § 7 ölçülen destek"}


# ── SANAT HAZIRLIĞI ──────────────────────────────────────────────────────
def prepare_artwork(root, geo_ed, src_rel, out_rel, verbose=True,
                    scrim_boxes=None):
    """İşlenmiş sanatı sürümün TAM sarım pikseline getirir.

    ⚠ ALFA DÜZLEŞTİRİLİR. Kurucu dosyaları RGBA geldi; baskıda alfa
    kanalının anlamı yoktur ve KDP'nin dönüştürücüsü onu siyaha da
    çevirebilir. Beyaz üstüne düzleştirilir.

    ⚠ KIRPMA ORANTIYI KORUR. Ciltli sarım ciltsizden DAR ve aynı
    yüksekliktedir; sanat gerilmez, ORTADAN kırpılır.
    """
    from PIL import Image
    src = os.path.join(root, src_rel)
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(bg, im)
    im = im.convert("RGB")

    tw = geo_ed["artworkTarget"]["widthPx"]
    th = geo_ed["artworkTarget"]["heightPx"]
    want = tw / float(th)
    have = im.width / float(im.height)
    if abs(have - want) > 1e-4:
        if have > want:                     # çok geniş → yanlardan kırp
            nw = int(round(im.height * want))
            x = (im.width - nw) // 2
            im = im.crop((x, 0, x + nw, im.height))
        else:                               # çok yüksek → üst/alttan kırp
            nh = int(round(im.width / want))
            y = (im.height - nh) // 2
            im = im.crop((0, y, im.width, y + nh))
    scale = tw / float(im.width)
    im = im.resize((tw, th), Image.LANCZOS)
    scrims = []
    for box in (scrim_boxes or []):
        im, meta = feathered_scrim(im, box, geo_ed["wrapWidthIn"],
                                   geo_ed["wrapHeightIn"])
        scrims.append(meta)
    out = os.path.join(root, out_rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, dpi=(300, 300))
    if verbose:
        print("     sanat → %d × %d px (×%.3f) · %s"
              % (tw, th, scale, os.path.basename(out)))
    return {"file": out_rel, "widthPx": tw, "heightPx": th,
            "scrims": scrims,
            "scaleFromProcessed": round(scale, 4),
            "effectiveDpi": round(tw / geo_ed["wrapWidthIn"], 1),
            "sha256": sha256(out), "bytes": os.path.getsize(out)}


# Sırtın ölçülen koşuları (FINAL_COVER_SELECTION § 6).
#
# ⚠ 'sd' YANLIŞ SORUYU SORUYORDU. Sırt şeridinin standart sapması orta
# bölgede 32–47'dir ve ilk yerleşim bunu "yazı geçirilemez" diye okudu;
# başlığı 1,96 inçlik bir koşuya sıkıştırıp 6,5 punto'ya düşürdü — ince
# bir sırt için bile fazla ürkek.
#
# Doğru soru KOYU PİKSEL ORANIDIR. Ölçüldü: sırtın en kalabalık yarım inçi
# bile yalnızca %25 koyudur, ortalama parlaklık 157–205 arasında kalır.
# Yani zemin AÇIK parşömendir ve üstündeki koyu şeyler İNCE ÇİZGİLERDİR;
# koyu bir harf onların üstünde okunur. Yüksek sd, kütle değil KENARDAN
# gelir.
#
# Başlık koşusu bu ölçümle seçildi: y 7,55–10,30 aralığında koyu piksel
# oranı %8,2'yi hiç geçmiyor.
SPINE_RUNS = {"title": (7.55, 10.30), "author": (0.62, 1.58)}


def fit_tracked(text, font, max_in, start_pt=11.0, track_ratio=0.12,
                min_pt=8.0):
    """Metni verilen inç uzunluğuna SIĞDIRAN punto ve harf aralığını bulur.

    Sırt 0,3603 inçtir — ince bir sırttır ve üstündeki yazı da incedir.
    Punto tahmin edilmez: ölçülen temiz koşunun uzunluğundan TÜRETİLİR.
    """
    from reportlab.pdfbase.pdfmetrics import stringWidth
    pt = start_pt
    while pt >= min_pt:
        track = pt * track_ratio
        w = sum(stringWidth(ch, font, pt) for ch in text) + track * (len(text) - 1)
        if w <= max_in * IN:
            return pt, track, w
        pt -= 0.25
    track = min_pt * track_ratio
    w = sum(stringWidth(ch, font, min_pt) for ch in text) + track * (len(text) - 1)
    return min_pt, track, w


class TypeLog:
    """Basılan her metin parçasının GERÇEK kutusunu inç olarak kaydeder.

    Kapağı gözle denetlemek gerekir ama YETMEZ: bir harfin güvenli alanı
    yarım milim aşması gözle görülmez, kesimde görülür. Bu kayıt,
    `covers.py --check`'in denetleyebileceği bir olgu üretir.
    """

    def __init__(self):
        self.items = []

    def add(self, kind, x0, y0, x1, y1, text=""):
        self.items.append({"kind": kind, "text": text[:60],
                           "x0": round(x0 / IN, 4), "y0": round(y0 / IN, 4),
                           "x1": round(x1 / IN, 4), "y1": round(y1 / IN, 4)})


# ── TİPOGRAFİ ────────────────────────────────────────────────────────────
# Ölçülen en sakin arka kapak bloğu (sd 27,7) — FINAL_COVER_SELECTION § 6
BACK_BOX = (0.70, 0.60, 5.90, 7.60)
INK = (0.106, 0.094, 0.078)          # koyu kahve-siyah: parşömende mürekkep
FONT_DIR = "/usr/share/fonts/truetype/liberation"
FONTS = {"CoverSerif": "LiberationSerif-Regular.ttf",
         "CoverSerif-B": "LiberationSerif-Bold.ttf",
         "CoverSerif-I": "LiberationSerif-Italic.ttf"}


def _register(pdfmetrics, TTFont):
    for n, f in FONTS.items():
        p = os.path.join(FONT_DIR, f)
        if not os.path.exists(p):
            raise RuntimeError("kapak fontu yok: %s" % p)
        pdfmetrics.registerFont(TTFont(n, p))


def _tracked(c, text, x, y, font, size, track, anchor="center", log=None,
             kind="text", tf=None):
    """Harf aralıklı (letterspaced) tek satır. Genişliği döner."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    w = sum(stringWidth(ch, font, size) for ch in text) + track * (len(text) - 1)
    if anchor == "center":
        cur = x - w / 2.0
    elif anchor == "right":
        cur = x - w
    else:
        cur = x
    start = cur
    c.setFont(font, size)
    for ch in text:
        c.drawString(cur, y, ch)
        cur += stringWidth(ch, font, size) + track
    if log is not None:
        if tf is None:
            log.add(kind, start, y - size * 0.24, start + w, y + size * 0.75,
                    text)
        else:
            # sırt: döndürülmüş koordinat → sarım koordinatına çevrilir
            sx, y0, y1 = tf
            log.add(kind, sx - size * 0.75, -(start + w), sx + size * 0.24,
                    -start, text)
    return w


def _wrap(text, font, size, maxw):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def compose(root, cfg, ed, geo_ed, art_rel, measured, out_dir, verbose=True):
    """Tam sarım kapağı VEKTÖR tipografiyle basar."""
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import reportlab.rl_config as rl_config
    sys.path.insert(0, HERE)
    import cover_text as CT

    _register(pdfmetrics, TTFont)
    rl_config.canvas_basefontname = "CoverSerif"

    W = geo_ed["wrapWidthIn"] * IN
    H = geo_ed["wrapHeightIn"] * IN
    Z, ZN = geo_ed["safeZones"], geo_ed["zones"]
    os.makedirs(out_dir, exist_ok=True)
    name = "GreatBookOfWorldGames_cover_%s.pdf" % ed
    path = os.path.join(out_dir, name)

    c = rl_canvas.Canvas(path, pagesize=(W, H), pageCompression=1)
    c.setTitle("%s — cover (%s)" % (cfg["project"]["title"], ed))
    c.setAuthor(cfg["founder"]["author"])
    c.setCreator("04_BUILD/covers.py")
    c.drawImage(os.path.join(root, art_rel), 0, 0, width=W, height=H,
                preserveAspectRatio=False, anchor="c")
    c.setFillColorRGB(*INK)
    c.setStrokeColorRGB(*INK)
    log = TypeLog()
    spine_fit = []

    fx0, fx1 = ZN["frontCover"]["x0"] * IN, ZN["frontCover"]["x1"] * IN
    fcx = (fx0 + fx1) / 2.0
    colw = (Z["frontTitle"]["x1"] - Z["frontTitle"]["x0"]) * IN

    # ── ÖN KAPAK · başlık bloğu (ölçülen sakin bant: y 9,35–10,85 in) ──
    # Alt başlık ilk sürümde AÇIK RENKLİ TAHTA PİYONUN üstüne düşüyordu
    # (piyon x 11,0–11,6 in · y 9,4–10,2 in). Blok yukarı alındı ve alt
    # başlık daraltıldı; artık piyonun üstünde kalıyor.
    y = 10.60 * IN
    _tracked(c, CT.FRONT_TITLE_TOP, fcx, y, "CoverSerif", 19.5, 5.4,
             log=log, kind="frontTitle")
    y -= 0.60 * IN
    _tracked(c, CT.FRONT_TITLE_MAIN, fcx, y, "CoverSerif-B", 60, 2.0,
             log=log, kind="frontTitle")
    y -= 0.24 * IN
    c.setLineWidth(1.0)
    c.line(fcx - 1.85 * IN, y, fcx + 1.85 * IN, y)
    y -= 0.215 * IN
    from reportlab.pdfbase.pdfmetrics import stringWidth as _sw
    c.setFont("CoverSerif-I", 12.0)
    for txt in (CT.front_subtitle(measured), CT.front_subtitle2(measured)):
        c.drawCentredString(fcx, y, txt)
        hw = _sw(txt, "CoverSerif-I", 12.0) / 2.0
        log.add("frontTitle", fcx - hw, y - 3.0, fcx + hw, y + 9.0, txt)
        y -= 0.185 * IN

    # ── ÖN KAPAK · yazar (ölçülen sakin bant: y 0,45–1,55 in) ──
    _tracked(c, CT.AUTHOR, fcx, 0.86 * IN, "CoverSerif-B", 23, 4.4,
             log=log, kind="frontAuthor")

    # ── SIRT — ORTASI KALABALIK, İKİ UCU TEMİZ (ölçüldü) ──
    # Yazı ortadan geçirilmez: başlık üstteki temiz koşuya, yazar alttaki
    # temiz koşuya. Kalabalık orta bölge BOŞ bırakılır.
    sx = (ZN["spine"]["x0"] + ZN["spine"]["x1"]) / 2.0 * IN
    c.saveState()
    c.translate(sx, 0)
    c.rotate(-90)                      # yukarıdan aşağı okunur (KDP normu)
    for key, txt, font in (("title", CT.SPINE_TITLE, "CoverSerif-B"),
                           ("author", CT.SPINE_AUTHOR, "CoverSerif")):
        lo, hi = SPINE_RUNS[key]
        pt, track, w = fit_tracked(txt, font, hi - lo)
        mid = (lo + hi) / 2.0
        _tracked(c, txt, -(mid * IN), -pt * 0.34, font, pt, track,
                 log=log, kind="spineText", tf=(sx, 0, 0))
        spine_fit.append({"part": key, "text": txt, "pt": pt,
                          "trackPt": round(track, 2),
                          "widthIn": round(w / IN, 3),
                          "runIn": [lo, hi]})
    c.restoreState()

    # ── ARKA KAPAK (ölçülen sakin blok: x 0,70–5,90 · y 0,60–4,60 in) ──
    bx = BACK_BOX[0] * IN + 0.10 * IN
    bw = (BACK_BOX[2] - BACK_BOX[0]) * IN - 0.20 * IN
    by = BACK_BOX[3] * IN - 0.30 * IN
    for kind, text in CT.back_copy(measured):
        if kind == "head":
            c.setFont("CoverSerif-B", 12.2)
            for ln in _wrap(text, "CoverSerif-B", 12.2, bw):
                c.drawString(bx, by, ln)
                log.add("backCopy", bx, by - 3, bx + bw, by + 9, ln)
                by -= 15.0
            by -= 2.0
        else:
            c.setFont("CoverSerif", 10.6)
            for ln in _wrap(text, "CoverSerif", 10.6, bw):
                c.drawString(bx, by, ln)
                log.add("backCopy", bx, by - 3, bx + bw, by + 8, ln)
                by -= 13.4
            by -= 7.0

    # yazar biyografisi — kanonik metin, arka kapağın altında
    bio = cfg["founder"].get("authorBio")
    if bio:
        by -= 4.0
        c.setLineWidth(0.7)
        c.line(bx, by + 8, bx + 2.0 * IN, by + 8)
        by -= 6.0
        c.setFont("CoverSerif-I", 10.2)
        for ln in _wrap(bio, "CoverSerif-I", 10.2, bw):
            c.drawString(bx, by, ln)
            log.add("backCopy", bx, by - 3, bx + bw, by + 8, ln)
            by -= 13.0

    # yayıncı künyesi — barkod alanının ÜSTÜNDE, içinde değil
    # Yayıncı künyesi ilk sürümde SIRTIN DİBİNE düşmüştü. Yeri, metin
    # bloğunun altı — barkod alanına girmez.
    c.setFont("CoverSerif", 9.8)
    c.drawString(bx, max(by - 6.0, (Z["barcode"]["y1"] + 0.30) * IN),
                 cfg["founder"]["publisher"])
    c.showPage()
    c.save()

    rep = {"edition": ed, "typeLog": log.items, "spineFit": spine_fit,
           "file": os.path.relpath(path, root),
           "sha256": sha256(path), "bytes": os.path.getsize(path),
           "wrapIn": [geo_ed["wrapWidthIn"], geo_ed["wrapHeightIn"]],
           "spineIn": geo_ed["spineWidthIn"], "artwork": art_rel}
    if verbose:
        print("     kapak → %s (%.1f KB)" % (name, os.path.getsize(path) / 1024.0))
    return rep


def raw_assets(root: str) -> dict:
    d = os.path.join(root, "07_ASSETS", "raw", "cover")
    if not os.path.isdir(d):
        return {"dir": os.path.relpath(d, root), "files": []}
    files = []
    for fn in sorted(os.listdir(d)):
        if fn.startswith("."):
            continue
        p = os.path.join(d, fn)
        if not os.path.isfile(p):
            continue
        rec = {"file": fn, "bytes": os.path.getsize(p), "sha256": sha256(p)}
        try:
            from PIL import Image
            with Image.open(p) as im:
                rec["widthPx"], rec["heightPx"] = im.size
                rec["mode"] = im.mode
                rec["format"] = im.format
        except Exception as exc:
            rec["imageError"] = str(exc)
        files.append(rec)
    return {"dir": os.path.relpath(d, root), "files": files}


def _pil_tracked(draw, text, cx, y, font, track_px, fill):
    """Harf aralıklı, ORTALANMIŞ tek satır — `_tracked()`'ın PIL/rasterlenmiş
    karşılığı. Her karakter kendi ilerleme genişliğince ilerler, aralarına
    track_px eklenir. Anchor 'ls' → (x, y) sol-taban (baseline)."""
    widths = [font.getlength(ch) for ch in text]
    total = sum(widths) + track_px * (len(text) - 1)
    x = cx - total / 2.0
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += w + track_px
    return total


def _pil_fit_tracked(text, font_path, start_px, max_w_px, track_ratio,
                     min_px=None):
    """Metni verilen piksel genişliğine SIĞDIRAN punto/harf aralığını
    bulur — `fit_tracked()`'ın (§ sırt) PIL karşılığı. Punto TAHMİN
    edilmez, ölçülen genişlikten TÜRETİLİR."""
    from PIL import ImageFont
    min_px = min_px if min_px is not None else max(8.0, start_px * 0.55)
    size = start_px
    while size >= min_px:
        font = ImageFont.truetype(font_path, max(1, round(size)))
        track = size * track_ratio
        w = sum(font.getlength(ch) for ch in text) + track * (len(text) - 1)
        if w <= max_w_px:
            return font, track, w
        size -= 1.0
    font = ImageFont.truetype(font_path, max(1, round(min_px)))
    track = min_px * track_ratio
    w = sum(font.getlength(ch) for ch in text) + track * (len(text) - 1)
    return font, track, w


def kindle_typography(front, geo_ed, measured):
    """Kindle ön kapağına VEKTÖR ANAHATTAN (TrueType) tipografi basar.

    Beyaz kutu YOK, AI-üretilmiş metin YOK. Yerleşim İCAT EDİLMEDİ: sarımın
    ölçülen sakin bantlarıyla AYNI dikey konumlar kullanılır
    (FINAL_COVER_SELECTION.md § 6 — ön başlık y 9,35–10,85 in · ön yazar
    y 0,45–1,55 in, ikisi de sd < 14 yani "gerek yok" düzeyinde sakin);
    yalnızca bu görselin KENDİ px/in oranına ÖLÇEKLENİR. Kindle kırpması
    (`kindle_cover`) sarımın ön panel sütununun ORTALANMIŞ bir alt kümesi
    olduğundan, yatayda görsel merkezine ortalamak aynı sakin bandı korur.
    """
    from PIL import ImageDraw
    sys.path.insert(0, HERE)
    import cover_text as CT

    draw = ImageDraw.Draw(front)
    W, H = front.size
    scale = H / geo_ed["wrapHeightIn"]           # px / gerçek inç (bu görsel)
    cx = W / 2.0
    fill = tuple(min(255, round(c * 255)) for c in INK)
    margin_px = COVER_SAFE_IN * scale
    max_w = W - 2 * margin_px
    reg = os.path.join(FONT_DIR, FONTS["CoverSerif"])
    bold = os.path.join(FONT_DIR, FONTS["CoverSerif-B"])
    ital = os.path.join(FONT_DIR, FONTS["CoverSerif-I"])
    if not (os.path.exists(reg) and os.path.exists(bold) and os.path.exists(ital)):
        raise RuntimeError("kapak fontu yok: %s" % FONT_DIR)
    log = []

    def y_of(y_in_from_bottom):
        return H - y_in_from_bottom * scale      # PDF y (alttan) → PIL y (üstten)

    # ── üst satır — "THE GREAT BOOK OF" (wrap: y 10.60 in) ──
    y = y_of(10.60)
    f, tr, w = _pil_fit_tracked(CT.FRONT_TITLE_TOP, reg, 19.5 * scale / IN,
                                max_w, 5.4 / 19.5)
    _pil_tracked(draw, CT.FRONT_TITLE_TOP, cx, y, f, tr, fill)
    log.append({"kind": "frontTitle", "text": CT.FRONT_TITLE_TOP,
               "px": round(f.size, 1)})

    # ── ana başlık — "WORLD GAMES" (wrap: 0.60 in aşağı) ──
    y = y_of(10.60 - 0.60)
    f, tr, w = _pil_fit_tracked(CT.FRONT_TITLE_MAIN, bold, 60 * scale / IN,
                                max_w, 2.0 / 60)
    _pil_tracked(draw, CT.FRONT_TITLE_MAIN, cx, y, f, tr, fill)
    log.append({"kind": "frontTitle", "text": CT.FRONT_TITLE_MAIN,
               "px": round(f.size, 1)})

    # ── ayırıcı çizgi ──
    y = y_of(10.60 - 0.60 - 0.24)
    half = 1.85 * scale
    draw.line([(cx - half, y), (cx + half, y)], fill=fill,
             width=max(1, round(1.0 * scale / IN)))

    # ── alt başlıklar — measured'dan basılır, SAYI elle yazılmaz ──
    y = y_of(10.60 - 0.60 - 0.24 - 0.215)
    for i, txt in enumerate((CT.front_subtitle(measured),
                             CT.front_subtitle2(measured))):
        f, tr, w = _pil_fit_tracked(txt, ital, 12 * scale / IN, max_w, 0.0)
        draw.text((cx, y), txt, font=f, fill=fill, anchor="ms")
        log.append({"kind": "frontTitle", "text": txt, "px": round(f.size, 1)})
        y = y_of(10.60 - 0.60 - 0.24 - 0.215 - 0.185 * (i + 1))

    # ── yazar (wrap: y 0.86 in) ──
    y = y_of(0.86)
    f, tr, w = _pil_fit_tracked(CT.AUTHOR, bold, 23 * scale / IN, max_w,
                                4.4 / 23)
    _pil_tracked(draw, CT.AUTHOR, cx, y, f, tr, fill)
    log.append({"kind": "frontAuthor", "text": CT.AUTHOR,
               "px": round(f.size, 1)})

    return front, log


def kindle_cover(root, geo_ed, art_rel, out_dir, measured, verbose=True):
    """Kindle kapağı — ÖN paneldan türetilir, sarımdan DEĞİL.

    Amazon 1:1,6 en-boy ister ve 2560 × 1600 px önerir. Ön panel 1:1,304'tür,
    yani yükseklik yetmez: sarımın ön panelinden 1:1,6 oranında bir dikey
    dilim ORTADAN kırpılır. Tam sarımı ebook kapağı diye yüklemek, okura
    sırtı ve arka kapağı göstermek demektir.

    Tipografi bu kırpmanın ÜZERİNE, sarımla AYNI vektör-anahat yerleşimiyle
    basılır — bkz. `kindle_typography()`. DPI etiketi basılmaz iddiası
    taşımaz: bu bir EKRAN varlığıdır, KDP Kindle kapaklarını piksel
    boyutuyla değerlendirir (bkz. 300×300 dpi etiketi yalnızca uyumluluk
    içindir, gerçek px/in ~227,6 — ekranda anlamsızdır ve final raporda
    açıkça yazılır).
    """
    from PIL import Image
    im = Image.open(os.path.join(root, art_rel)).convert("RGB")
    W, H = im.size
    Z = geo_ed["zones"]["frontCover"]
    wi = geo_ed["wrapWidthIn"]
    x0 = int(Z["x0"] / wi * W)
    x1 = int(Z["x1"] / wi * W)
    front = im.crop((x0, 0, x1, H))
    want = 1600.0 / 2560.0                      # genişlik / yükseklik
    have = front.width / float(front.height)
    if have > want:
        nw = int(round(front.height * want))
        x = (front.width - nw) // 2
        front = front.crop((x, 0, x + nw, front.height))
    else:
        nh = int(round(front.width / want))
        y = (front.height - nh) // 2
        front = front.crop((0, y, front.width, y + nh))
    front = front.resize((1600, 2560), Image.LANCZOS)
    front, typo_log = kindle_typography(front, geo_ed, measured)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "GreatBookOfWorldGames_cover_kindle.jpg")
    front.save(path, "JPEG", quality=95, dpi=(300, 300), optimize=True)
    if verbose:
        print("     kindle kapağı → 1600 × 2560 px · vektör tipografi (%d öge) · %.1f KB"
              % (len(typo_log), os.path.getsize(path) / 1024.0))
    return {"file": os.path.relpath(path, root), "widthPx": 1600,
            "heightPx": 2560, "aspect": round(1600 / 2560.0, 4),
            "sha256": sha256(path), "bytes": os.path.getsize(path),
            "typography": typo_log,
            "note": "ÖN panelden türetildi; tam sarım DEĞİL. Tipografi "
                    "VEKTÖR ANAHATTAN (LiberationSerif TTF, AI-üretilmiş "
                    "METİN DEĞİL) basıldı; konum sarımın ölçülen sakin "
                    "bantlarıyla AYNI, yalnızca bu görselin px/in oranına "
                    "ölçeklendi."}


def build_covers(root, cfg, args) -> int:
    """Seçilen sanattan bütün kapakları üretir."""
    gp = os.path.join(root, "06_REPORTS", "cover-geometry.json")
    geo = load(gp)
    sel = args.artwork or os.path.join("07_ASSETS", "processed", "cover",
                                       "cover-02-4x-300dpi.png")
    if not os.path.exists(os.path.join(root, sel)):
        print("  ⛔ işlenmiş sanat yok: %s" % sel)
        print("     önce: 04_BUILD/cover_artwork.py --upscale")
        return 1
    fm = load(os.path.join(root, "02_MANUSCRIPT", "frontmatter.json"))
    measured = fm["measured"]

    print("=" * 74)
    print("  KAPAK ÜRETİMİ")
    print("=" * 74)
    print("  seçilen sanat: %s" % sel)
    print("  künye        : 06_REPORTS/FINAL_COVER_SELECTION.md")

    out = {"$comment": ["KAPAK ÜRETİMİ — ÜRETİLMİŞ DOSYA (04_BUILD/covers.py).",
                        "Tipografi VEKTÖRDÜR; sanatın üstüne beyaz kutu",
                        "konmadı. Yerleşim ölçülen sakin bantlardadır."],
           "generatedAtPhase": "phase6",
           "selectedArtwork": sel, "editions": {}}

    kindle_only = getattr(args, "kindle_only", False)
    if kindle_only:
        # Yalnızca Kindle yeniden dizilecekse ciltsiz/ciltli PDF'lere
        # DOKUNULMAZ — SHA-256'ları KDP_UPLOAD_HANDBOOK.md içinde basılı ve
        # gereksiz yeniden üretim yalnızca zaman damgasını değiştirip o
        # kılavuzu bayatlatır. Önceki kaydı taşı.
        prev_path = os.path.join(root, "06_REPORTS", "cover-build.json")
        if not os.path.exists(prev_path):
            print("  ⛔ --kindle-only önce en az bir tam --build ister "
                  "(ciltsiz/ciltli kaydı yok)")
            return 1
        out["editions"] = load(prev_path).get("editions", {})
        print("\n  · --kindle-only: ciltsiz/ciltli PDF'lere DOKUNULMADI, "
              "önceki kayıt korundu")
    else:
        for ed in ("paperback", "hardcover"):
            if ed not in geo["editions"]:
                continue
            g = geo["editions"][ed]
            print("\n── %s ── sarım %.4f × %.4f in · sırt %.4f in"
                  % (ed.upper(), g["wrapWidthIn"], g["wrapHeightIn"],
                     g["spineWidthIn"]))
            art_rel = os.path.join("07_ASSETS", "print",
                                   "cover-wrap-%s.png" % ed)
            art = prepare_artwork(root, g, sel, art_rel,
                                  scrim_boxes=[BACK_BOX])
            odir = os.path.join(root, "08_OUTPUT",
                                "PAPERBACK" if ed == "paperback" else "HARDCOVER")
            rep = compose(root, cfg, ed, g, art_rel, measured, odir)
            rep["artworkPrep"] = art
            out["editions"][ed] = rep

    kdir = os.path.join(root, "08_OUTPUT", "KINDLE")
    print("\n── KINDLE ──")
    out["kindle"] = kindle_cover(
        root, geo["editions"]["paperback"],
        os.path.join("07_ASSETS", "print", "cover-wrap-paperback.png"), kdir,
        measured)

    dump(os.path.join(root, "06_REPORTS", "cover-build.json"), out)
    print("\n" + "=" * 74)
    print("  ✅ kapaklar üretildi · ciltsiz · ciltli · kindle")
    print("=" * 74)
    return 0


def run(root: str, args) -> int:
    cfg = load(os.path.join(root, "project_config.json"))
    out, errs = {}, []
    for ed in ("paperback", "hardcover"):
        p = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if not os.path.exists(p):
            errs.append("%s iç bloğu YOK — sırt hesaplanamaz" % ed)
            continue
        r = load(p)
        g = geometry(cfg, ed, r["pageCount"])
        g["interiorSha256"] = r["sha256"]
        g["interiorFile"] = r["file"]
        out[ed] = g

    assets = raw_assets(root)
    payload = {
        "$comment": [
            "KAPAK GEOMETRİSİ — ÜRETİLMİŞ DOSYA (04_BUILD/covers.py).",
            "Sırt genişliği ÖLÇÜLEN sayfa sayısından gelir; hiçbir sayfa",
            "sayısı gömülü değildir. İç blok değişirse bu dosya BAYATLAR",
            "ve --check kırmızı yanar.",
        ],
        "generatedAtPhase": "phase6",
        "editions": out,
        "rawArtwork": assets,
        "artworkPresent": bool(assets["files"]),
        "compositionStatus": ("BLOCKED — kurucu sanatı yok"
                              if not assets["files"] else "READY"),
    }
    dump(os.path.join(root, "06_REPORTS", "cover-geometry.json"), payload)

    print("=" * 74)
    print("  KAPAK GEOMETRİSİ")
    print("=" * 74)
    for ed, g in out.items():
        print("\n── %s ──" % ed.upper())
        print("  sayfa sayısı        %d  (ÖLÇÜLDÜ, tahmin değil)"
              % g["pageCount"])
        print("  sırt                %.4f in  (%.4f in/sayfa%s)"
              % (g["spineWidthIn"], g["spinePerPageIn"],
                 " + %.2f in tahta" % HARDCOVER_BOARD_IN
                 if ed == "hardcover" else ""))
        print("  tam sarım           %.4f × %.4f in  (%.0f × %.0f px @300 ppi)"
              % (g["wrapWidthIn"], g["wrapHeightIn"],
                 g["artworkTarget"]["widthPx"], g["artworkTarget"]["heightPx"]))
        print("  sırta yazı          %s (KDP eşiği %d sayfa)"
              % ("EVET" if g["spineTextAllowed"] else "HAYIR",
                 g["spineTextMinPages"]))
        z = g["zones"]
        print("  bölgeler (in)       arka %.3f–%.3f · sırt %.3f–%.3f · "
              "ön %.3f–%.3f"
              % (z["backCover"]["x0"], z["backCover"]["x1"],
                 z["spine"]["x0"], z["spine"]["x1"],
                 z["frontCover"]["x0"], z["frontCover"]["x1"]))
        if ed == "hardcover" and not g.get("founderConfirmedTemplate"):
            print("  ⚠ CİLTLİ ŞABLON DOĞRULANMADI — KURUCU EYLEMİ")

    print("\n── HAM KAPAK SANATI ──")
    print("  dizin: %s" % assets["dir"])
    if not assets["files"]:
        print("  ⛔ VARLIK KAPISI: kurucu sanatı YOK.")
        print("     Kapak KOMPOZİSYONU yapılmadı ve yapıldığı İDDİA EDİLMİYOR.")
        print("     İstemler: 07_ASSETS/IMAGE_PROMPT_LIBRARY.html")
    else:
        for f in assets["files"]:
            px = ("%d × %d px" % (f.get("widthPx", 0), f.get("heightPx", 0))
                  if "widthPx" in f else "OKUNAMADI")
            print("  · %-40s %10s  %s" % (f["file"], px, f["sha256"][:12]))

    for e in errs:
        print("  ✗ %s" % e)
    print("=" * 74)
    return 1 if errs else 0


def run_check(root: str) -> int:
    p = os.path.join(root, "06_REPORTS", "cover-geometry.json")
    if not os.path.exists(p):
        print("  · kapak geometrisi üretilmemiş — ATLANDI")
        return 0
    g = load(p)
    errs = []
    for ed, blk in g["editions"].items():
        ip = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if not os.path.exists(ip):
            errs.append("%s iç bloğu kayboldu" % ed)
            continue
        r = load(ip)
        if r["pageCount"] != blk["pageCount"]:
            errs.append("%s: SIRT BAYAT — kapak %d sayfaya göre, iç blok %d "
                        "sayfa (sırt kaydı, kapak GEÇERSİZ)"
                        % (ed, blk["pageCount"], r["pageCount"]))
        if r["sha256"] != blk.get("interiorSha256"):
            errs.append("%s: iç blok DEĞİŞMİŞ — kapak yeniden hesaplanmalı"
                        % ed)
    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        return 1
    print("  ✓ kapak geometrisi iç blokla senkron (%s)"
          % " · ".join("%s %d s. → sırt %.4f in"
                       % (e, b["pageCount"], b["spineWidthIn"])
                       for e, b in g["editions"].items()))
    if not g["artworkPresent"]:
        print("  · VARLIK KAPISI AÇIK: kurucu kapak sanatı bekleniyor "
              "(kompozisyon YAPILMADI)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--kindle-only", action="store_true",
                    help="yalnızca Kindle kapağını yeniden üret; "
                         "ciltsiz/ciltli PDF'lere DOKUNMAZ")
    ap.add_argument("--artwork", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    if args.check:
        return run_check(root)
    if args.build:
        cfg = load(os.path.join(root, "project_config.json"))
        # ÖNCE geometri, SONRA kompozisyon. İkisi ayrı dosyalara yazar
        # (cover-geometry.json ve cover-build.json) ve --check GEOMETRİYİ
        # okur. Yalnızca --build çalıştırıldığında geometri dosyası eski
        # iç bloğun sağlamasını taşımaya devam ediyordu: kapak TAZE, kayıt
        # BAYAT, kapı haklı olarak kırmızı. Tek komut ikisini birden tazeler.
        rc = run(root, args)
        if rc:
            return rc
        return build_covers(root, cfg, args)
    return run(root, args)


if __name__ == "__main__":
    sys.exit(main())
