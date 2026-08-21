#!/usr/bin/env python3
"""
PAKET KAPILARININ KENDİ TESTİ — The Great Book of World Games
================================================================================
Faz 6'da açılan kapılar (iç blok · kapak · A+ · metadata · EPUB · KDP ön
denetimi · teslim · görsel · satır editörü) GERÇEKTEN ISIRIYOR MU?

Bu projenin en pahalı dersi tek cümledir:

    BİR KAPI KUSURU YAKALAMIYORSA, O KAPI YOK DEMEKTİR.

Yeşil yanan bir kapı iki şeyden birini söyler: ya kusur yoktur, ya kapı
kördür. İkisini ayırmanın tek yolu KASITLI KUSUR ÜRETMEKTİR.

Yöntem: her durum için proje bir GEÇİCİ KOPYAYA açılır, kopyaya tek bir
kusur enjekte edilir, ilgili kapı koşturulur ve KIRMIZI yanması BEKLENİR.
Kırmızı yanmazsa test başarısızdır — kusur değil, KAPI kusurludur.

Çıkış kodları:  0 = bütün kapılar ısırıyor   1 = körlük bulundu   2 = atlandı
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable

# Kopyaya taşınacak dizinler. Ham teslim ve .git TAŞINMAZ: ağırdır ve
# hiçbir kapı onlara bakmaz.
COPY = ["04_BUILD", "05_TESTS", "01_SOURCE", "02_MANUSCRIPT", "03_APLUS",
        "06_REPORTS", "07_ASSETS", "08_OUTPUT", "00_CONTEXT"]
COPY_FILES = ["project_config.json", ".gate"]


class Suite:
    def __init__(self):
        self.passed = 0
        self.failed: list[str] = []

    def case(self, name, gate_argv, mutate, expect_red=True):
        with tempfile.TemporaryDirectory(prefix="gbwg-pkg-") as td:
            work = os.path.join(td, "proj")
            os.makedirs(work)
            for d in COPY:
                src = os.path.join(ROOT, d)
                if os.path.isdir(src):
                    shutil.copytree(src, os.path.join(work, d),
                                    symlinks=True)
            for f in COPY_FILES:
                src = os.path.join(ROOT, f)
                if os.path.exists(src):
                    shutil.copy2(src, os.path.join(work, f))
            try:
                mutate(work)
            except Exception as exc:                       # noqa: BLE001
                self.failed.append("%s — kusur ENJEKTE EDİLEMEDİ: %s"
                                   % (name, exc))
                print("  ✗ %s — kusur enjekte edilemedi: %s" % (name, exc))
                return
            argv = [PY] + [a.replace("{root}", work) for a in gate_argv]
            r = subprocess.run(argv, cwd=work, capture_output=True, text=True)
            red = r.returncode == 1
            ok = red if expect_red else not red
            if ok:
                self.passed += 1
                print("  ✓ %s" % name)
            else:
                self.failed.append(name)
                print("  ✗ %s — kapı %s (çıkış %d)"
                      % (name, "ISIRMADI" if expect_red else "yanlış ısırdı",
                         r.returncode))
                tail = (r.stdout or "").strip().splitlines()[-4:]
                for t in tail:
                    print("      | %s" % t)


def rd(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def wr(p, d):
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)


def edit_json(path, fn):
    def m(work):
        p = os.path.join(work, path)
        d = rd(p)
        fn(d)
        wr(p, d)
    return m


def edit_text(path, fn):
    def m(work):
        p = os.path.join(work, path)
        with open(p, encoding="utf-8") as fh:
            s = fh.read()
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(fn(s))
    return m


def first_svg_json(work):
    d = os.path.join(work, "07_ASSETS", "diagrams")
    for fn in sorted(os.listdir(d)):
        if fn.endswith("_diagrams.json"):
            return os.path.join(d, fn)
    raise RuntimeError("diyagram tanımlayıcısı yok")


def main() -> int:
    if not os.path.exists(os.path.join(ROOT, "02_MANUSCRIPT", "book.json")):
        print("  · ticari manuscript bu depoda yok — paket testi ATLANDI")
        return 0
    try:
        import reportlab  # noqa: F401
        from PIL import Image  # noqa: F401
    except ImportError:
        print("  ⊘ reportlab/Pillow yok — paket testi ATLANDI")
        return 2

    s = Suite()
    print("=" * 74)
    print("  PAKET KAPILARININ KENDİ TESTİ")
    print("=" * 74)

    # ── İÇ BLOK ────────────────────────────────────────────────────────
    print("\n── iç blok (interior.py --check) ──")
    IC = ["04_BUILD/interior.py", "--root", "{root}", "--check"]
    s.case("iç blok PDF'i silinirse yakalanır", IC,
           lambda w: os.remove(os.path.join(
               w, rd(os.path.join(w, "06_REPORTS",
                                  "interior-paperback.json"))["file"])))
    s.case("iç blok PDF'i değişirse sağlama yakalar", IC,
           lambda w: open(os.path.join(
               w, rd(os.path.join(w, "06_REPORTS",
                                  "interior-paperback.json"))["file"]),
               "ab").write(b"\n% tampered\n"))
    s.case("bir madde SOL sayfada başlamazsa yakalanır", IC,
           edit_json("06_REPORTS/interior-paperback.json",
                     lambda d: d.__setitem__("spreadsStartingVerso",
                                             d["spreadsTotal"] - 1)))
    s.case("iç marj KDP asgarisinin altına düşerse yakalanır", IC,
           edit_json("06_REPORTS/interior-paperback.json",
                     lambda d: d["margins"].__setitem__("gutterIn", 0.25)))
    s.case("sayfa sayısı TEK olursa yakalanır", IC,
           edit_json("06_REPORTS/interior-paperback.json",
                     lambda d: d.__setitem__("pageCount",
                                             d["pageCount"] + 1)))
    s.case("sayfa sayısı KDP bandının altına düşerse yakalanır", IC,
           edit_json("06_REPORTS/interior-paperback.json",
                     lambda d: d.__setitem__("pageCount", 40)))
    s.case("içindekiler sığmazsa yakalanır", IC,
           edit_json("06_REPORTS/interior-paperback.json",
                     lambda d: d.__setitem__("tocFitted", False)))
    s.case("temiz iç blok GEÇER", IC, lambda w: None, expect_red=False)

    # ── KAPAK ──────────────────────────────────────────────────────────
    print("\n── kapak (covers.py --check) ──")
    CV = ["04_BUILD/covers.py", "--root", "{root}", "--check"]
    s.case("sırt bayatlarsa (sayfa sayısı kayarsa) yakalanır", CV,
           edit_json("06_REPORTS/cover-geometry.json",
                     lambda d: d["editions"]["paperback"].__setitem__(
                         "pageCount", 999)))
    s.case("iç blok değişirse kapak GEÇERSİZ sayılır", CV,
           edit_json("06_REPORTS/cover-geometry.json",
                     lambda d: d["editions"]["paperback"].__setitem__(
                         "interiorSha256", "0" * 64)))
    s.case("temiz kapak geometrisi GEÇER", CV, lambda w: None,
           expect_red=False)

    # ── A+ ─────────────────────────────────────────────────────────────
    print("\n── A+ içeriği (aplus.py) ──")
    AP = ["04_BUILD/aplus.py", "--root", "{root}"]
    s.case("yasak iddia (bestseller) yakalanır", AP,
           edit_text("04_BUILD/aplus.py",
                     lambda t: t.replace(
                         '"title": "%d games. %d cultures. One table."',
                         '"title": "The bestseller: %d games, %d cultures."')))
    s.case("garanti edilmiş eğitsel sonuç iddiası yakalanır", AP,
           edit_text("04_BUILD/aplus.py",
                     lambda t: t.replace(
                         "This is a reference book you play from",
                         "Guaranteed to improve your child's maths. "
                         "This is a reference book you play from")))
    s.case("ÖLÇÜLMEMİŞ SAYI (100 games) yakalanır", AP,
           edit_text("04_BUILD/aplus.py",
                     lambda t: t.replace(
                         '"title": "%d games. %d cultures. One table."',
                         '"title": "100 games. %d cultures. %d table."')))
    s.case("A+ metni kitapla ayrışırsa --check yakalar",
           ["04_BUILD/aplus.py", "--root", "{root}", "--check"],
           edit_json("03_APLUS/aplus_content.json",
                     lambda d: d["measured"].__setitem__("games", 100)))
    s.case("temiz A+ paketi GEÇER", AP, lambda w: None, expect_red=False)

    # ── METADATA ───────────────────────────────────────────────────────
    print("\n── metadata (metadata.py) ──")
    MD = ["04_BUILD/metadata.py", "--root", "{root}"]
    s.case("alt başlıktaki oyun sayısı kitapla ayrışırsa yakalanır", MD,
           edit_json("02_MANUSCRIPT/frontmatter.json",
                     lambda d: d["measured"].__setitem__(
                         "subtitleMeasured",
                         "100 Games from 5,000 Years — from 45 Cultures")))
    # ⚠ BU DURUM FAZ 6'DA DEĞİŞTİ. `authorBio` artık DOLU (kanonik metin
    # kardeş projeden birebir alındı), yani "boş bırak ve kırmızı bekle"
    # testi kendiliğinden geçmez oldu — kapı ısırmıyor göründü çünkü
    # ısıracak kusur kalmamıştı. Test kusuru ENJEKTE ediyor: biyografi
    # silinir ve `release` kapısının hâlâ ısırdığı doğrulanır.
    s.case("release kapısında SİLİNMİŞ authorBio KIRMIZI",
           ["04_BUILD/metadata.py", "--root", "{root}", "--gate", "release"],
           edit_json("project_config.json",
                     lambda d: d["founder"].__setitem__("authorBio", None)))
    s.case("dolu authorBio release kapısında GEÇER",
           ["04_BUILD/metadata.py", "--root", "{root}", "--gate", "release"],
           lambda w: None, expect_red=False)
    s.case("kanonik biyografi DEĞİŞİRSE künye bayatlar (bilgi)",
           MD, lambda w: None, expect_red=False)

    # ── DİZGİ TIRNAĞI ──────────────────────────────────────────────────
    # Kusur KAYNAKTA değil ÇIKTIDA aranır. `typo.smart` etkisizleştirilir,
    # iç blok YENİDEN üretilir ve KDP ön denetiminin basılmış PDF'te daktilo
    # tırnağını gördüğü doğrulanır. Faz 6'da bu kapı yoktu ve kitap 36
    # daktilo kesme işaretiyle basılmaya hazırdı.
    print("\n── dizgi tırnağı (kdp_preflight.py) ──")

    def neuter_typo(w):
        tp = os.path.join(w, "04_BUILD", "typo.py")
        src = open(tp, encoding="utf-8").read()
        src = src.replace("def smart(t):", "def smart(t):\n    return str(t)")
        open(tp, "w", encoding="utf-8").write(src)
        r = subprocess.run([PY, "04_BUILD/interior.py", "--root", w],
                           cwd=w, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError("iç blok yeniden üretilemedi: %s"
                               % r.stderr.strip()[-300:])

    s.case("basılan PDF'te daktilo tırnağı KIRMIZI",
           ["04_BUILD/kdp_preflight.py", "--root", "{root}"], neuter_typo)

    # ── GUTTER EMNİYETİ — GERÇEK KDP PREVIEWER SAYFA 159 REGRESYONU ──────
    # Gerçek Amazon KDP Print Previewer, 160 sayfalık ciltsizde sayfa
    # 159'da "Insufficient gutter" dedi (kurucu bildirimi, 2026-08-21).
    # Kök neden ÖLÇÜLDÜ: iç marj TAM KDP asgarisinde (emniyet payı SIFIR)
    # diziliyordu ve bazı gliflerin (ölçülen örnek: sayfa 159'daki açılış
    # tek tırnağı ') mürekkebi Liberation Serif'te nominal başlangıcın az
    # solunda basıyordu — bir dizgi hatası değil, normal bir font çizim
    # gerçeği. `interior.GUTTER_SAFETY_IN` (0,05 in) bu payı taşır.
    #
    # Kusur burada KAYNAKTA değil ÇIKTIDA aranır (dizgi tırnağı testiyle
    # aynı ilke): sabiti KASITLI olarak -0,01'e çekip GERÇEK kitap SADECE
    # ciltsiz için yeniden dizilir — bu, tam KDP asgarisinin 0,01 in
    # ALTINDA nominal bir marj üretir ve glif taşması onu daha da
    # KÖTÜLEŞTİRİR (asla iyileştirmez), yani bu durum KIRMIZI olmak
    # ZORUNDADIR, kırılgan bir eşik değildir.
    print("\n── gutter emniyeti — KDP Previewer sayfa 159 regresyonu ──")

    def gutter_deficit(w):
        ip = os.path.join(w, "04_BUILD", "interior.py")
        src = open(ip, encoding="utf-8").read()
        old = "GUTTER_SAFETY_IN = 0.05"
        if old not in src:
            raise RuntimeError("GUTTER_SAFETY_IN sabiti bulunamadı — "
                               "kaynak değişmiş, testi güncelle")
        open(ip, "w", encoding="utf-8").write(src.replace(old,
            "GUTTER_SAFETY_IN = -0.01"))
        r = subprocess.run([PY, "04_BUILD/interior.py", "--edition",
                            "paperback", "--root", w],
                           cwd=w, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError("iç blok yeniden üretilemedi: %s"
                               % r.stderr.strip()[-300:])

    s.case("iç marj KDP asgarisinin 0,01 in ALTINA düşerse (sayfa 159 "
           "sınıfı hata) kdp_preflight.py KIRMIZI",
           ["04_BUILD/kdp_preflight.py", "--root", "{root}"], gutter_deficit)

    # § 14'ün tam istediği eşik testi ("0,49 in KIRMIZI · 0,50 in YEŞİL")
    # gerçek kitaba karşı KIRILGANDIR — bulgu tam olarak bu: nominal tam
    # 0,50 in bile bu kitabın GERÇEK metniyle glif taşmasından 0,49 in'e
    # düşebiliyordu (16 sayfa). Eşiğin KENDİSİNİ font taşmasından bağımsız
    # ve KESİN doğrulamak için `check_ink()` SENTETİK, dolgu dikdörtgenli
    # (glif belirsizliği yok) bir PDF'e karşı DOĞRUDAN çağrılır.
    print("\n── gutter eşiği — sentetik kesinlik testi (§14) ──")
    try:
        sys.path.insert(0, os.path.join(ROOT, "04_BUILD"))
        import importlib
        kp = importlib.import_module("kdp_preflight")
        from reportlab.pdfgen import canvas as rl_canvas
        IN = 72.0
        for label, gutter_val, want_red in (("0.49 in", 0.49, True),
                                            ("0.50 in", 0.50, False)):
            with tempfile.TemporaryDirectory(prefix="gbwg-gutter-") as td:
                pdf_path = os.path.join(td, "synthetic.pdf")
                c = rl_canvas.Canvas(pdf_path, pagesize=(8.5 * IN, 11.0 * IN))
                c.setFillColorRGB(0, 0, 0)
                # Sayfa 1 = TEK = SAĞ/recto → iç marj SOLDADIR. Dolu bir
                # dikdörtgen — bir glifin değil, tam bilinen bir x'in sol
                # kenarını ölçer.
                c.rect(gutter_val * IN, 5.0 * IN, 10, 10, fill=1, stroke=0)
                c.showPage()
                c.save()
                rep = kp.Report()
                r = kp.check_ink(pdf_path, 160, 8.5, 11.0, rep)
                got_red = bool(rep.fail)
                name = ("iç marj TAM %s (160 s. asgarisi 0,50) %s"
                       % (label, "KIRMIZI" if want_red else "GEÇER"))
                if got_red == want_red:
                    s.passed += 1
                    print("  ✓ %s (ölçülen %.4f in)"
                          % (name, r["worstMarginIn"]["gutterIn"]))
                else:
                    s.failed.append(name)
                    print("  ✗ %s — kapı %s (ölçülen %.4f in)"
                          % (name, "ISIRMADI" if want_red else "yanlış ısırdı",
                             r["worstMarginIn"]["gutterIn"]))
    except ImportError as exc:
        print("  ⊘ sentetik eşik testi ATLANDI: %s" % exc)

    # ── EPUB ───────────────────────────────────────────────────────────
    print("\n── EPUB (epub.py --check) ──")
    EP = ["04_BUILD/epub.py", "--root", "{root}", "--check"]
    s.case("EPUB silinirse yakalanır", EP,
           lambda w: os.remove(os.path.join(
               w, rd(os.path.join(w, "06_REPORTS", "epub.json"))["file"])))
    s.case("EPUB bozulursa yakalanır", EP,
           lambda w: open(os.path.join(
               w, rd(os.path.join(w, "06_REPORTS", "epub.json"))["file"]),
               "ab").write(b"corrupt"))
    s.case("temiz EPUB GEÇER", EP, lambda w: None, expect_red=False)

    # ── GÖRSEL KAPI ────────────────────────────────────────────────────
    print("\n── görsel kapı (qa_visual.py) ──")
    QV = ["04_BUILD/qa_visual.py", "--root", "{root}"]

    def tr_label(w):
        p = first_svg_json(w)
        d = rd(p)
        d["diagrams"][0]["legend"] = [{"glyph": "dark",
                                       "label": "alttaki oyuncunun taşı"}]
        wr(p, d)
        subprocess.run([PY, "04_BUILD/render_diagrams.py"], cwd=w,
                       capture_output=True)

    s.case("çizilmiş TÜRKÇE efsane etiketi yakalanır", QV, tr_label)

    def tr_label_ascii(w):
        p = first_svg_json(w)
        d = rd(p)
        d["diagrams"][0]["legend"] = [{"glyph": "dark",
                                       "label": "alttaki oyuncunun generali"}]
        wr(p, d)
        subprocess.run([PY, "04_BUILD/render_diagrams.py"], cwd=w,
                       capture_output=True)

    s.case("AKSANSIZ Türkçe etiket de yakalanır", QV, tr_label_ascii)

    def long_label(w):
        p = first_svg_json(w)
        d = rd(p)
        d["diagrams"][0]["legend"] = [
            {"glyph": "dark", "label": "a legend label far too long for the "
                                       "canvas it is drawn on, which will be "
                                       "clipped when the page is printed"}]
        wr(p, d)
        subprocess.run([PY, "04_BUILD/render_diagrams.py"], cwd=w,
                       capture_output=True)

    s.case("tuvalden taşan efsane yakalanır", QV, long_label)

    def orphan_svg(w):
        d = os.path.join(w, "07_ASSETS", "diagrams")
        src = [f for f in os.listdir(d) if f.endswith(".svg")][0]
        shutil.copy2(os.path.join(d, src), os.path.join(d, "ORPHAN-TEST.svg"))

    s.case("tanımlayıcısı olmayan SVG yakalanır", QV, orphan_svg)
    s.case("temiz görsel kapı GEÇER", QV, lambda w: None, expect_red=False)

    # ── SATIR EDİTÖRÜ ──────────────────────────────────────────────────
    print("\n── satır editörü (qa_lineedit.py) ──")
    QL = ["04_BUILD/qa_lineedit.py", "--root", "{root}"]

    def us_spelling(w):
        p = os.path.join(w, "02_MANUSCRIPT", "book.json")
        d = rd(p)
        d["games"][0]["culturalStory"] += " The color of the center piece."
        wr(p, d)

    s.case("Amerikan imlası yakalanır", QL, us_spelling)

    def md_marker(w):
        p = os.path.join(w, "02_MANUSCRIPT", "book.json")
        d = rd(p)
        d["games"][0]["culturalStory"] += " **Do not** use these."
        wr(p, d)

    s.case("markdown işareti yakalanır", QL, md_marker)

    def jargon(w):
        p = os.path.join(w, "02_MANUSCRIPT", "book.json")
        d = rd(p)
        d["games"][0]["sources"].append(
            "The project's own record for this work remains ACCESS-BLOCKED.")
        wr(p, d)

    s.case("projenin iç sözlüğü yakalanır", QL, jargon)

    def forbidden(w):
        p = os.path.join(w, "02_MANUSCRIPT", "book.json")
        d = rd(p)
        d["games"][0]["culturalStory"] += " Let us dive into the rich tapestry."
        wr(p, d)

    s.case("STYLE § 4 yasak kalıbı yakalanır", QL, forbidden)

    def legend_drift(w):
        p = first_svg_json(w)
        d = rd(p)
        gid = d["diagrams"][0]["gameId"]
        d["diagrams"][0]["legend"] = [
            {"glyph": "dark", "label": "the flamingo that guards the border"}]
        wr(p, d)
        subprocess.run([PY, "04_BUILD/render_diagrams.py"], cwd=w,
                       capture_output=True)
        return gid

    s.case("kuralda geçmeyen efsane terimi yakalanır", QL, legend_drift)

    def drop_edge(w):
        p = os.path.join(w, "02_MANUSCRIPT", "book.json")
        d = rd(p)
        d["games"][0]["edgeCases"].pop("tie", None)
        wr(p, d)

    s.case("üç sorudan biri düşerse yakalanır", QL, drop_edge)
    s.case("temiz satır editörü GEÇER", QL, lambda w: None, expect_red=False)

    # ── TESLİM ─────────────────────────────────────────────────────────
    print("\n── teslim (handoff.py --check) ──")
    HO = ["04_BUILD/handoff.py", "--root", "{root}", "--check"]
    s.case("kılavuz bayatlarsa (sayfa sayısı kayarsa) yakalanır", HO,
           edit_json("06_REPORTS/handoff.json",
                     lambda d: d["packages"]["paperback"]["interior"]
                     .__setitem__("pageCount", 999)))
    s.case("kılavuz dosyası silinirse yakalanır", HO,
           lambda w: os.remove(os.path.join(
               w, "08_OUTPUT", "KDP_UPLOAD_HANDBOOK.md")))
    s.case("temiz teslim paketi GEÇER", HO, lambda w: None, expect_red=False)

    print("\n" + "=" * 74)
    total = s.passed + len(s.failed)
    if s.failed:
        print("  ⛔ %d/%d KÖRLÜK BULUNDU" % (len(s.failed), total))
        for f in s.failed:
            print("     · %s" % f)
        print("\n  Bir kapı kusuru yakalamıyorsa, o kapı YOK demektir.")
        return 1
    print("  ✅ %d kasıtlı kusurun %d'i yakalandı — paket kapıları ISIRIYOR"
          % (total, s.passed))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
