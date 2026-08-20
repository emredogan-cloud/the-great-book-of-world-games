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
    for fn in sorted(os.listdir(ddir)):
        if fn.endswith(".json") and fn != "diagram_language.json":
            for d in load(os.path.join(ddir, fn)).get("diagrams", []):
                declared[d["diagramId"]] = d

    svgs = sorted(f for f in os.listdir(ddir) if f.endswith(".svg"))
    if not svgs:
        # Render edilmiş SVG'ler ÜRETİLİR ve depoda durmazlar (.gitignore).
        # Taze bir klonda hiç yoktur; kapı orada BOŞ KOŞAR.
        print("  · render edilmiş SVG yok — görsel kapı ATLANDI "
              "(önce 04_BUILD/render_diagrams.py)")
        return 0
    rep = Report()
    print("=" * 74)
    print("  GÖRSEL KAPI · RENDER EDİLMİŞ SVG (%d dosya)" % len(svgs))
    print("=" * 74)

    # ① sözlük
    print("\n── ① sözlük ──")
    unknown = []
    parsed = {}
    for fn in svgs:
        try:
            parsed[fn[:-4]] = sv.parse(os.path.join(ddir, fn))
        except sv.UnknownElement as e:
            unknown.append(str(e))
    rep.check(not unknown, "her SVG elemanı bilinen sözlükte" + brief(unknown))

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
                wpx = stringWidth(o["text"], "Times-Roman",
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
    fdir = "/usr/share/fonts/truetype/liberation"
    fpath = os.path.join(fdir, "LiberationSerif-Regular.ttf")
    if os.path.exists(fpath):
        try:
            from PIL import ImageFont
            fnt = ImageFont.truetype(fpath, 40)
            seen = set()
            for did, d in parsed.items():
                for o in d["ops"]:
                    if o["op"] != "text":
                        continue
                    for ch in o["text"]:
                        if ch in seen or ch.isspace():
                            continue
                        seen.add(ch)
                        if fnt.getmask(ch).getbbox() is None:
                            missing_glyphs.append("%s → %r (U+%04X)"
                                                  % (did, ch, ord(ch)))
        except ImportError:
            print("  ⚠ Pillow yok — glif denetimi ATLANDI")
    else:
        print("  ⚠ baskı fontu bulunamadı — glif denetimi ATLANDI")
    rep.check(not missing_glyphs,
              "çizilen her karakter baskı fontunda var"
              + brief(sorted(set(missing_glyphs))))

    # ⑦ yetim dosya
    print("\n── ⑦ yetim dosya ──")
    orphan = sorted(set(parsed) - set(declared))
    rep.check(not orphan,
              "tanımlayıcısı olmayan SVG yok" + brief(orphan))
    missing = sorted(set(declared) - set(parsed))
    rep.check(not missing, "her tanımlayıcı render edilmiş" + brief(missing))

    rep.facts["svgFiles"] = len(svgs)
    rep.facts["declared"] = len(declared)

    print("\n" + "=" * 74)
    if rep.fail:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.fail), rep.n))
        for f in rep.fail:
            print("     · %s" % f)
    else:
        print("  ✅ %d denetim yeşil · %d SVG basıma hazır" % (rep.n, len(svgs)))
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
    args = ap.parse_args()
    return run(os.path.abspath(args.root), args)


if __name__ == "__main__":
    sys.exit(main())
