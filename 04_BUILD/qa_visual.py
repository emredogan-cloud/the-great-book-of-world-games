#!/usr/bin/env python3
"""
GÖRSEL KAPI — The Great Book of World Games
================================================================================
`qa_diagram.py` TANIMLAYICIYI denetler: sembol sözlükte mi, efsane tam mı,
bütçe aşıldı mı. Bu kapı **RENDER EDİLMİŞ SVG'nin KENDİSİNİ** denetler:
sayfaya BASILACAK olan şeyi.

Faz 6'nın açtığı kapı ve nedeni:

  ⛔ EFSANE METNİ TÜRKÇEYDİ. Faz 2 ve 3'te yazılan diyagramların efsane
     etiketleri belge diliyle (Türkçe) yazılmıştı ve efsane METNİ SVG'ye
     ÇİZİLİYOR. Yani ticari İngilizce kitabın diyagramlarında *"kale —
     buradaki taş alınamaz"* basılacaktı. `qa_language_split.py` bunu
     görmedi çünkü o kapı JSON ALANLARINA bakar, ÇİZİLMİŞ METNE değil.
     Sayısal kapıların hepsi yeşildi.

  ⛔ EFSANE METNİ TUVALDEN TAŞIYORDU. Bir etiket tuvalden uzunsa SVG onu
     KIRPMAZ, taşırır; PDF'e gömüldüğünde sütun kenarında KESİLİR. İki
     diyagramda bulundu ve ölçüldü (3,1 mm ve 1,4 mm).

Denetimler:
  ① sözlük        — her eleman `svg_vector.KNOWN_TAGS` içinde
  ② dil           — çizilmiş metinde Türkçe/belge dili YOK
  ③ taşma         — metin ve geometri tuvalin içinde
  ④ çakışma       — iki taş aynı merkeze çizilmemiş
  ⑤ baskı eşiği   — çizgi ≥ minStrokePt, glif ≥ minGlyphPt
  ⑥ mürekkep      — yalnız izinli gri seviyeleri (renk YASAK)
  ⑦ yetim dosya   — tanımlayıcısı olmayan SVG yok
  ⑧ glif          — çizilen her karakter baskı fontunda var
  ⑨ metin üstünde — hiçbir metin başka bir metnin üstüne basılmamış

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

# Belge dili işaretleri. Türkçeye ÖZGÜ harfler + ticari metinde yeri olmayan
# yüksek frekanslı Türkçe kelimeler. Tek bir işaret yeter: çizilmiş metin
# ticari çıktıdır ve orada belge dili BULUNAMAZ.
TR_CHARS = set("ışğçöüİŞĞÇÖÜ")
# ⚠ HARFE GÜVENİLMEZ. `qa_lineedit.py` iki etiketi bu kapının GÖREMEDİĞİ
# yerde buldu: "alttaki oyuncunun generali" ve "alttaki oyuncunun eri" —
# ikisinde de Türkçeye özgü TEK BİR HARF yok, hepsi ASCII. Bir dil kapısı
# yalnızca aksana bakıyorsa, aksansız yazılmış bir sızıntıyı geçirir.
# Bu yüzden KÖK listesi de var ve tek isabet yeter.
TR_WORDS = {"ve", "bir", "bu", "için", "ile", "olan", "taş", "oyuncu",
            "yön", "kare", "sayısı", "gidiş", "hamle", "alınan", "üstteki",
            "alttaki", "öteki", "yasak", "kazanır", "zorunlu", "merkez",
            "buradaki", "yalnız", "çember", "kişi", "arasında", "değil"}
TR_STEMS = ("oyuncunun", "oyuncular", "alttaki", "ustteki", "üstteki",
            "tasi", "taşı", "generali", "sayisi", "sayısı", "gidis",
            "hamlesi", "karesi", "cukur", "çukur", "tohum", "kisi",
            "cember", "yalniz", "birinci", "ikinci", "oteki", "ayni")


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


class Report:
    def __init__(self):
        self.fail: list[str] = []
        self.n = 0
        self.facts: dict = {}

    def check(self, cond, label):
        self.n += 1
        if cond:
            return True
        self.fail.append(label)
        print("  ✗ %s" % label)
        return False


def brief(items, k=6):
    items = list(items)
    if not items:
        return ""
    head = ", ".join(str(x) for x in items[:k])
    return " — %s%s" % (head, " …(+%d)" % (len(items) - k) if len(items) > k else "")


def looks_turkish(s: str) -> bool:
    if any(ch in TR_CHARS for ch in s):
        return True
    low = s.lower()
    if any(st in low for st in TR_STEMS):
        return True
    words = re.findall(r"[A-Za-zÀ-ÿ]+", low)
    return sum(1 for w in words if w in TR_WORDS) >= 2


def run(root: str, args) -> int:
    try:
        import svg_vector as sv
        from reportlab.pdfbase.pdfmetrics import stringWidth
    except ImportError:
        print("  ⊘ reportlab yok — görsel kapı ATLANDI")
        return 2

    lang_path = os.path.join(root, "07_ASSETS", "diagrams", "diagram_language.json")
    if not os.path.exists(lang_path):
        print("  · diyagram dili yok — ATLANDI")
        return 0
    lang = load(lang_path)
    pr = lang["print"]
    ddir = os.path.join(root, "07_ASSETS", "diagrams")

    declared = {}
    bp = os.path.join(root, "02_MANUSCRIPT", "book.json")
    specs = []
    if os.path.exists(bp):
        specs = [d for g in load(bp).get("games", []) for d in (g.get("diagramSpecs") or [])]
    if specs:
        # Since the 2026 recovery the printed diagrams are declared in the manuscript itself
        # (diagramSpecs, drawn by boards.py into this folder); the phase*_diagrams.json
        # descriptors describe the retired renderer. Both directions are still enforced below:
        # no SVG without a declaration, no declaration without its SVG.
        for d in specs:
            declared[d["id"]] = d
    else:
        for fn in sorted(os.listdir(ddir)):
            if fn.endswith(".json") and fn != "diagram_language.json":
                for d in load(os.path.join(ddir, fn)).get("diagrams", []):
                    declared[d["diagramId"]] = d

    # Every SVG that prints is checked: the paperback/hardcover diagrams, the large-print
    # diagrams (drawn with 1.5× labels — where a chart once overflowed onto p. 385) and both
    # sets of full-size templates. Keys are "folder/id".
    folders = [("diagrams", set(declared))]
    if specs:
        folders.append(("diagrams_lp", set(declared)))
        bmp = os.path.join(root, "02_MANUSCRIPT", "backmatter_book.json")
        tpl = {t["id"] for t in load(bmp).get("templates", [])} if os.path.exists(bmp) else set()
        folders += [("templates", tpl), ("templates_lp", tpl)]
    svgs = sorted(f for f in os.listdir(ddir) if f.endswith(".svg"))
    if not svgs:
        # Render edilmiş SVG'ler ÜRETİLİR ve depoda durmazlar (.gitignore).
        # Taze bir klonda hiç yoktur; kapı orada BOŞ KOŞAR.
        print("  · render edilmiş SVG yok — görsel kapı ATLANDI "
              "(önce 04_BUILD/render_diagrams.py)")
        return 0
    rep = Report()
    files = []
    for folder, ids in folders:
        fdir = os.path.join(root, "07_ASSETS", folder)
        have = sorted(f for f in os.listdir(fdir) if f.endswith(".svg")) if os.path.isdir(fdir) else []
        files += [(folder, fn) for fn in have]
    print("=" * 74)
    print("  GÖRSEL KAPI · RENDER EDİLMİŞ SVG (%d dosya · %s)"
          % (len(files), " · ".join(f for f, _ in folders)))
    print("=" * 74)

    # ① sözlük
    print("\n── ① sözlük ──")
    unknown = []
    parsed = {}
    for folder, fn in files:
        try:
            parsed["%s/%s" % (folder, fn[:-4])] = sv.parse(os.path.join(root, "07_ASSETS", folder, fn))
        except sv.UnknownElement as e:
            unknown.append(str(e))
    rep.check(not unknown, "her SVG elemanı bilinen sözlükte" + brief(unknown))
    declared = {"%s/%s" % (folder, i) for folder, ids in folders for i in ids}

    # the fonts the diagrams are PRINTED in (svg_vector maps family → the book's fonts)
    try:
        sys.path.insert(0, HERE)
        import interior as _I
        _I.register_fonts()
        font_files = {k: os.path.join(_I.FONT_DIR, v) for k, v in _I.FONT_FILES.items()}

        def print_font(o):
            return sv._font_for(o.get("family"), o.get("weight"), o.get("style"), sv.DEFAULT_FONTS)
    except Exception as exc:  # noqa: BLE001 — no fonts, no honest measurement
        print("  ⚠ baskı fontları yüklenemedi (%s) — ölçüm Times-Roman ile" % exc)
        font_files = {}

        def print_font(o):
            return "Times-Roman"

    # ② dil — ÇİZİLMİŞ metin ticari dilde olmak zorundadır
    print("\n── ② dil: çizilmiş metin ticari dilde (EN) ──")
    tr = []
    for did, d in parsed.items():
        for o in d["ops"]:
            if o["op"] == "text" and looks_turkish(o["text"]):
                tr.append("%s → %s" % (did, o["text"][:44]))
    rep.check(not tr,
              "çizilmiş metinde belge dili yok (%d etiket)" % len(tr) + brief(tr))
    rep.facts["drawnTextLabels"] = sum(
        1 for d in parsed.values() for o in d["ops"] if o["op"] == "text")

    # ③ taşma
    print("\n── ③ taşma: her şey tuvalin içinde ──")
    over_text, over_geom = [], []
    for did, d in parsed.items():
        W, H = d["widthPx"], d["heightPx"]
        for o in d["ops"]:
            if o["op"] == "text":
                wpx = stringWidth(o["text"], print_font(o),
                                  o["size"] * 72.0 / 96.0) * 96.0 / 72.0
                right = {"start": o["x"] + wpx,
                         "middle": o["x"] + wpx / 2.0,
                         "end": o["x"]}[o["anchor"]]
                if right > W + 0.5 or o["y"] > H + 0.5 or o["x"] < -0.5:
                    over_text.append("%s → %.1f mm taşıyor: %s"
                                     % (did, (right - W) / sv.PX_PER_MM,
                                        o["text"][:34]))
            elif o["op"] == "circle":
                if (o["cx"] + o["r"] > W + 0.5 or o["cx"] - o["r"] < -0.5
                        or o["cy"] + o["r"] > H + 0.5 or o["cy"] - o["r"] < -0.5):
                    over_geom.append("%s → taş tuval dışında" % did)
            elif o["op"] == "line":
                for x, y in ((o["x1"], o["y1"]), (o["x2"], o["y2"])):
                    if x < -0.5 or x > W + 0.5 or y < -0.5 or y > H + 0.5:
                        over_geom.append("%s → çizgi tuval dışında" % did)
    rep.check(not over_text, "efsane ve etiketler tuvalin içinde" + brief(over_text))
    rep.check(not over_geom, "geometri tuvalin içinde" + brief(sorted(set(over_geom))))

    # ④ çakışma
    print("\n── ④ çakışma: iki taş aynı merkezde değil ──")
    clash = []
    for did, d in parsed.items():
        seen = {}
        for o in d["ops"]:
            if o["op"] != "circle":
                continue
            k = (round(o["cx"], 1), round(o["cy"], 1))
            if k in seen and abs(seen[k] - o["r"]) < 0.05:
                clash.append("%s → (%.1f, %.1f)" % (did, k[0], k[1]))
            seen[k] = o["r"]
    rep.check(not clash, "aynı merkeze çizilmiş taş yok" + brief(sorted(set(clash))))

    # ⑤ baskı eşiği
    print("\n── ⑤ baskı eşiği (çizgi %.2f pt · glif %.1f pt) ──"
          % (pr["minStrokePt"], pr["minGlyphPt"]))
    thin, tiny = [], []
    for did, d in parsed.items():
        for o in d["ops"]:
            # SVG sayıları İKİ ONDALIĞA yuvarlanır; 7,0 pt'lik bir glif
            # dosyada 9,33 px olarak durur ve geri çevrildiğinde 6,9975 pt
            # çıkar. Tolerans o yuvarlamanın kendisidir, bir gevşetme değil.
            TOL = 0.02
            if o["op"] in ("line", "circle", "rect") and o.get("strokeWidth"):
                pt = o["strokeWidth"] * 72.0 / 96.0
                if pt < pr["minStrokePt"] - TOL and o["op"] != "rect":
                    thin.append("%s → %.2f pt" % (did, pt))
            if o["op"] == "text":
                pt = o["size"] * 72.0 / 96.0
                if pt < pr["minGlyphPt"] - TOL:
                    tiny.append("%s → %.2f pt" % (did, pt))
    rep.check(not thin, "her çizgi baskı eşiğinin üstünde" + brief(sorted(set(thin))))
    rep.check(not tiny, "her glif baskı eşiğinin üstünde" + brief(sorted(set(tiny))))

    # ⑥ mürekkep
    print("\n── ⑥ mürekkep: yalnız izinli gri ──")
    allowed = set()
    for lv in pr["greyLevelsAllowed"]:
        v = int(round(255 * (100 - lv) / 100.0))
        allowed.add((v, v, v))
    allowed.add((255, 255, 255))
    colour = []
    for did, d in parsed.items():
        for o in d["ops"]:
            for key in ("fill", "stroke"):
                c = o.get(key)
                if c and c not in allowed:
                    colour.append("%s → %s %s" % (did, key, c))
    rep.check(not colour, "renk yok · yalnız izinli gri" + brief(sorted(set(colour))))

    # ⑧ BASKI FONTUNDA GLİF VAR MI
    #
    # Bu kapı Faz 6'da açıldı çünkü bir kusur bulundu: efsanedeki `ring`
    # sembolü (⌒ · U+2312) baskı fontunda (Liberation Serif) YOK. SVG'de
    # duruyordu, `qa_diagram` sözlüğü doğru diyordu, ölçü doğruydu — ve
    # basılı sayfada YER BOŞ KALACAKTI. Bir sembolün TANIMLI olması onun
    # BASILABİLİR olduğunu göstermez.
    print("\n── ⑧ baskı fontunda glif ──")
    missing_glyphs = []
    try:
        from PIL import ImageFont
        fonts_open, seen = {}, set()
        for did, d in parsed.items():
            for o in d["ops"]:
                if o["op"] != "text":
                    continue
                name = print_font(o)
                path = font_files.get(name)
                if not path:
                    continue
                if name not in fonts_open:
                    fonts_open[name] = ImageFont.truetype(path, 40)
                for ch in o["text"]:
                    if (name, ch) in seen or ch.isspace():
                        continue
                    seen.add((name, ch))
                    if fonts_open[name].getmask(ch).getbbox() is None:
                        missing_glyphs.append("%s → %r (U+%04X) · %s" % (did, ch, ord(ch), name))
        if not font_files:
            print("  ⚠ baskı fontu bulunamadı — glif denetimi ATLANDI")
    except ImportError:
        print("  ⚠ Pillow yok — glif denetimi ATLANDI")
    rep.check(not missing_glyphs,
              "çizilen her karakter baskı fontunda var"
              + brief(sorted(set(missing_glyphs))))

    # ⑨ METİN METNİN ÜSTÜNE BASILMAMIŞ
    #
    # GBK-02 (2026-09-26): büyük baskı etiketleri iki kat boyutta çizer; sabit yerleşimli
    # çizimlerde kelimeler birbirinin üstüne bindi ('1 Heaven2 Earth…' Tien Gow'da, Conkers'ta)
    # ve Alquerque'de bir 'next' etiketi sütun harfinin üstüne basıldı. ③ yalnızca tuvalin
    # KENARINA bakıyordu; iki metnin çakışmasını hiçbir denetim görmüyordu.
    # Kutu glife duyarlıdır (Source Sans 3 büyük harf yüksekliği 0,66 em): büyük harf, rakam
    # ya da yükselen harf varsa 0,72 em, yoksa x-yüksekliği 0,49 em; alt uzantı yalnız
    # g j p q y ve parantezde 0,23 em. İki kutu HER İKİ yönde 0,15 mm'den fazla kesişirse
    # metin metnin üstündedir — birbirine değen iki etiket bu denetimi geçer.
    print("\n── ⑨ metin metnin üstünde değil ──")
    tall = re.compile(r"[A-Z0-9bdfhklt'\"()/\[\]{}!?&%$#@|’‘“”]")
    desc = re.compile(r"[gjpqy(),;\[\]{}|Q]")

    def tbox(o):
        em = o["size"]
        wpx = stringWidth(o["text"], print_font(o), em * 72.0 / 96.0) * 96.0 / 72.0
        x0 = {"start": o["x"], "middle": o["x"] - wpx / 2.0, "end": o["x"] - wpx}[o["anchor"]]
        top = (0.72 if tall.search(o["text"]) else 0.49) * em
        bot = (0.23 if desc.search(o["text"]) else 0.01) * em
        return x0, o["y"] - top, x0 + wpx, o["y"] + bot

    near = 0.15 * sv.PX_PER_MM
    on_text = []
    for did, d in parsed.items():
        T = [o for o in d["ops"] if o["op"] == "text" and o["text"].strip()]
        B = [tbox(o) for o in T]
        for i in range(len(T)):
            for j in range(i + 1, len(T)):
                a, b = B[i], B[j]
                if (min(a[2], b[2]) - max(a[0], b[0]) > near
                        and min(a[3], b[3]) - max(a[1], b[1]) > near):
                    on_text.append("%s → %r × %r" % (did, T[i]["text"][:20], T[j]["text"][:20]))
    rep.check(not on_text,
              "hiçbir metin başka bir metnin üstüne basılmamış" + brief(on_text))

    # ⑦ yetim dosya
    print("\n── ⑦ yetim dosya ──")
    orphan = sorted(set(parsed) - set(declared))
    rep.check(not orphan,
              "tanımlayıcısı olmayan SVG yok" + brief(orphan))
    missing = sorted(set(declared) - set(parsed))
    rep.check(not missing, "her tanımlayıcı render edilmiş" + brief(missing))

    rep.facts["svgFiles"] = len(files)
    rep.facts["declared"] = len(declared)

    print("\n" + "=" * 74)
    if rep.fail:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.fail), rep.n))
        for f in rep.fail:
            print("     · %s" % f)
    else:
        print("  ✅ %d denetim yeşil · %d SVG basıma hazır" % (rep.n, len(files)))
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"checks": rep.n, "failed": rep.fail,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)
    return 1 if rep.fail else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--json", default=None)
    # CI bu dizindeki HER qa_*.py betiğini TARAYARAK bulur ve hepsini
    # `--verbose --json <yol>` ile çağırır. Bayrağı kullanmasak bile
    # KABUL ETMEK zorundayız: etmeyince kapı kırmızı yanmaz, argparse
    # çıkış 2 verir ve iş "kapı kırmızı" gibi görünür. Sözleşmeyi
    # 05_TESTS/selftest.py § ⑫ denetler.
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    return run(os.path.abspath(args.root), args)


if __name__ == "__main__":
    sys.exit(main())
