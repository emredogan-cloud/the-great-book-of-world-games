#!/usr/bin/env python3
"""
KINDLE EPUB ÜRETECİ — The Great Book of World Games
================================================================================
EPUB 3 (yeniden akan / reflowable) üretir.

── NEDEN SABİT DÜZEN (FIXED-LAYOUT) DEĞİL ──────────────────────────────
Bu kitabın basılı mimarisi bir ÇİFT SAYFA sözüdür: okur kitabı masaya açar
ve tur ortasında sayfa çevirmez. Kindle'da bu sözü korumanın tek yolu sabit
düzendir — ve sabit düzen bu kitap için YANLIŞ karardır:

  · Sabit düzen 8,5 × 11 inçlik bir çift sayfayı telefon ekranına sıkıştırır;
    10,5 punto gövde metni okunamaz hâle gelir ve okur yakınlaştırıp
    kaydırmak zorunda kalır. Basılı sözü korumak için ekran deneyimi
    feda edilmiş olur.
  · Sabit düzen yazı tipi boyutunu, temayı ve satır aralığını kilitler;
    Kindle okurunun erişilebilirlik ayarları çalışmaz.
  · Amazon'un kendi yönlendirmesi sabit düzeni resim-metin bağı SIKI olan
    türlere (çocuk kitabı, çizgi roman, yemek kitabı) önerir.

Asıl gerekçe şudur: **çift sayfa sözü bir BASKI kısıtına verilmiş bir
cevaptır.** Kâğıtta bir maddeyi bölen şey yaprağın kendisidir. Kaydırılan
bir ekranda o kısıt YOKTUR — madde tek ve kesintisiz akar, yani söz ihlal
edilmez, KONUSUZ kalır. Bu yüzden Kindle sürümü yeniden akandır ve her oyun
tek bir kesintisiz bölümdür.

Diyagramlar **SVG olarak gömülür**: her ekran yoğunluğunda keskin kalırlar
ve raster bir kopyanın onda biri yer tutarlar.

⚠ KAPAK: Kindle bir kapak görseli ister ve o görsel kurucu sanatından
üretilir. Sanat yokken EPUB kapak SAYFASI olmadan üretilir ve dosya
"KAPAK BEKLİYOR" diye işaretlenir. Sahte bir kapak konmaz.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = bağımlılık yok
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

UUID_NS = "urn:uuid:great-book-of-world-games-"


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def E(s):
    """XHTML kaçışı + tipografik kesme işareti (interior.py ile AYNI kural).

    İki çıktı aynı kitaptır; birinde eğri birinde düz kesme işareti olması
    aynı cümlenin iki farklı biçimde basılması demektir."""
    t = html.escape(str(s), quote=False)
    # AÇILIŞ tırnağı da dönüşür. İlk sürüm yalnızca kapanışı dönüştürdü ve
    # sayfada "'to surround the hare’" çıktı: bir tarafı daktilo, öteki
    # tarafı dizgi. Karışık tırnak, hiç dönüştürmemekten daha kötüdür.
    t = re.sub(r"(?<![A-Za-zÀ-ÿ0-9])'(?=[A-Za-zÀ-ÿ])", "\u2018", t)
    t = re.sub(r"(?<=[A-Za-zÀ-ÿ])'(?=[A-Za-zÀ-ÿ])", "\u2019", t)
    t = re.sub(r"(?<=[A-Za-zÀ-ÿ])'(?=\s|$|[,.;:!?])", "\u2019", t)
    return t


CSS = """@charset "utf-8";
html{font-size:100%}
body{font-family:Georgia,'Liberation Serif',serif;line-height:1.5;
     margin:0 5%;text-align:left;hyphens:auto}
h1{font-size:1.6em;line-height:1.2;margin:1.2em 0 .1em;page-break-before:always}
h2{font-size:1.15em;margin:1.4em 0 .2em}
h3{font-size:1em;margin:1.2em 0 .2em;text-transform:uppercase;
   letter-spacing:.05em}
p{margin:.5em 0;text-indent:0}
.kicker{font-style:italic;font-size:.9em;color:#555;margin:.1em 0 .6em}
.spec{font-size:.88em;border-top:1px solid #999;border-bottom:1px solid #999;
      padding:.4em 0;margin:.6em 0}
.notice{font-style:italic;border-left:3px solid #999;padding-left:.7em;
        margin:.7em 0}
ol{margin:.3em 0 .8em 1.4em;padding:0}
ol li{margin:.2em 0}
.sources{font-size:.8em;color:#444;margin-top:1em;border-top:1px solid #ccc;
         padding-top:.5em}
figure{margin:1em 0;text-align:center;page-break-inside:avoid}
figure svg{max-width:100%;height:auto}
.standfirst{font-style:italic;font-size:1.05em;margin:.3em 0 1em}
nav ol{list-style:none;margin-left:0}
nav ol ol{margin-left:1.2em}
.frontmatter h1{page-break-before:auto}
.q{margin:.4em 0}
.q b{font-style:normal}
"""


def svg_inline(path: str, max_w="26em") -> str:
    """SVG'yi olduğu gibi gömer. Raster YOK."""
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    s = re.sub(r"<\?xml[^>]*\?>\s*", "", s)
    s = s.replace("<svg ", '<svg style="max-width:%s" ' % max_w, 1)
    return s


def xhtml(title, body, cls="") -> str:
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" lang="en" '
            'xml:lang="en">\n<head><title>%s</title>'
            '<meta charset="utf-8"/>'
            '<link rel="stylesheet" type="text/css" href="../style.css"/>'
            '</head>\n<body%s>\n%s\n</body></html>\n'
            % (E(title), ' class="%s"' % cls if cls else "", body))


RULE_BLOCKS = (("Setup", "setup"), ("Placing", "placement"),
               ("On your turn", "turnSequence"), ("Movement", "movement"),
               ("Capture", "capture"), ("Legal moves", "legalMoves"),
               ("Throw values", "throwValues"), ("Stages", "stages"),
               ("The figures", "figures"), ("Scoring", "scoring"),
               ("Stacking and sending", "stackingAndSending"),
               ("The chain", "chain"))
EDGE_LABEL = {"tie": "If it is a draw.", "stalemate": "If nobody can move.",
              "illegalMove": "If somebody plays an illegal move."}


def game_xhtml(g, ddir) -> str:
    o = ['<h1 id="%s">%s</h1>' % (E(g["gameId"]), E(g["title"]))]
    o.append('<p class="kicker">%s · %s · %s</p>'
             % (E(g["culture"]), E(g["place"]), E(g["period"])))
    o.append('<p class="spec">%s</p>' % " · ".join(
        "<b>%s</b> %s" % (E(k.capitalize()), E(v))
        for k, v in g["spec"].items()))
    o.append("<p>%s</p>" % E(g["culturalStory"]))
    o.append("<p><b>Materials.</b> %s</p>" % E(g["materialsAndSubstitution"]))
    if g.get("reconstructionNotice"):
        o.append('<p class="notice">%s</p>' % E(g["reconstructionNotice"]))
    if g.get("safetyNote"):
        o.append('<p class="notice"><b>Safety.</b> %s</p>' % E(g["safetyNote"]))
    for did in g.get("diagrams", []):
        p = os.path.join(ddir, did + ".svg")
        if os.path.exists(p):
            o.append("<figure>%s</figure>" % svg_inline(p))
    if g.get("firstMove"):
        o.append("<p><b>The first move.</b> %s</p>" % E(g["firstMove"]))
    for label, key in RULE_BLOCKS:
        if not g.get(key):
            continue
        o.append("<h3>%s</h3><ol>%s</ol>"
                 % (E(label), "".join("<li>%s</li>" % E(s) for s in g[key])))
    for label, key in (("Winning", "winCondition"),
                       ("Taking the king", "kingCapture"),
                       ("How it ends", "endCondition")):
        if g.get(key):
            o.append("<p><b>%s.</b> %s</p>" % (E(label), E(g[key])))
    o.append("<h3>Three questions</h3>")
    for k, v in g["edgeCases"].items():
        o.append('<p class="q"><b>%s</b> %s</p>'
                 % (E(EDGE_LABEL.get(k, k + ".")), E(v)))
    o.append("<p><b>An example turn.</b> %s</p>" % E(g["exampleTurn"]))
    for v in g.get("variants", []):
        o.append("<p><b>%s.</b> %s</p>" % (E(v["name"]), E(v["note"])))
    o.append("<p><b>Your first game.</b> %s</p>" % E(g["firstGame"]))
    if g.get("aMatchIsTwoGames"):
        o.append("<p>%s</p>" % E(g["aMatchIsTwoGames"]))
    o.append('<p class="sources"><b>Sources.</b> %s</p>'
             % "  ".join(E(s) for s in g["sources"]))
    return "\n".join(o)


def build(root: str) -> int:
    cfg = load(os.path.join(root, "project_config.json"))
    mdir = cfg["language"]["commercialManuscriptDir"]
    for f in ("book.json", "frontmatter.json"):
        if not os.path.exists(os.path.join(root, mdir, f)):
            print("  · %s yok — EPUB ATLANDI (CI'da beklenen)" % f)
            return 0
    book = load(os.path.join(root, mdir, "book.json"))
    fm = load(os.path.join(root, mdir, "frontmatter.json"))
    bmp = os.path.join(root, mdir, "backmatter_printed.json")
    bm = load(bmp) if os.path.exists(bmp) else None
    ddir = os.path.join(root, "07_ASSETS", "diagrams")
    games = {g["gameId"]: g for g in book["games"]}
    tp, im, m = fm["titlePage"], fm["imprint"], fm["measured"]

    files, spine, nav_items = [], [], []

    def add(name, title, body, cls="", in_spine=True, in_nav=None):
        files.append(("OEBPS/text/%s" % name, xhtml(title, body, cls)))
        if in_spine:
            spine.append(name)
        if in_nav:
            nav_items.append((name, in_nav[0], in_nav[1]))

    # ── ön madde ──────────────────────────────────────────────────────
    add("title.xhtml", tp["title"],
        '<h1>%s</h1><p class="standfirst">%s</p><p>%s</p><p>%s</p>'
        % (E(tp["title"]), E(tp["subtitle"]), E(tp["author"]),
           E(tp["publisher"])), "frontmatter", in_nav=("Title page", 0))
    imprint = ["<h1>Copyright</h1>", "<p>%s</p>" % E(im["copyright"]),
               "<p>%s</p>" % E(im["publisher"]),
               "<p>%s · Volume %s</p>" % (E(tp["series"]), E(tp["volume"]))]
    for ed in ("paperback", "hardcover"):
        imprint.append("<p>ISBN (%s print edition): %s</p>"
                       % (ed, E(im["isbn"][ed])))
    imprint.append("<p>%s</p>" % E(im["rights"]))
    if im.get("authorBio"):
        imprint.append("<p><b>About the author.</b> %s</p>"
                       % E(im["authorBio"]))
    add("imprint.xhtml", "Copyright", "\n".join(imprint), "frontmatter",
        in_nav=("Copyright", 0))

    for sec in fm["sections"]:
        b = ['<h1>%s</h1>' % E(sec["title"])]
        for p in sec.get("paragraphs", []):
            b.append("<p>%s</p>" % E(p))
        for sub in sec.get("sections", []):
            b.append("<h2>%s</h2><p>%s</p>" % (E(sub["heading"]),
                                               E(sub["text"])))
        for row in sec.get("table", []):
            b.append("<h2>%s · %s</h2><p>%s <i>%s</i></p>"
                     % (E(row["n"]), E(row["name"]), E(row["idea"]),
                        E(row["test"])))
        if sec.get("closing"):
            b.append("<p>%s</p>" % E(sec["closing"]))
        add("%s.xhtml" % sec["id"], sec["title"], "\n".join(b), "frontmatter",
            in_nav=(sec["title"], 0))

    # ── gövde ─────────────────────────────────────────────────────────
    openers = {o["family"]: o for o in fm["familyOpeners"]}
    for item in fm["contents"]:
        if item["kind"] == "family-opener":
            o = openers[item["family"]]
            b = ['<h1>%s</h1>' % E(o["title"]),
                 '<p class="kicker">Part %s</p>' % E(o["numeral"]),
                 '<p class="standfirst">%s</p>' % E(o["standfirst"])]
            for p in o["paragraphs"]:
                b.append("<p>%s</p>" % E(p))
            add("part-%s.xhtml" % o["family"], o["title"], "\n".join(b),
                in_nav=(o["title"], 0))
        else:
            g = games[item["gameId"]]
            add("game-%s.xhtml" % g["gameId"], g["title"],
                game_xhtml(g, ddir), in_nav=(g["title"], 1))

    # ── arka madde ────────────────────────────────────────────────────
    if bm:
        gl = ["<h1>Glossary</h1>"] + [
            "<p><b>%s</b> %s</p>" % (E(t["term"]), E(t["definition"]))
            for t in sorted(bm["glossary"], key=lambda x: x["term"])]
        add("glossary.xhtml", "Glossary", "\n".join(gl), "frontmatter",
            in_nav=("Glossary", 0))
        bib = ["<h1>Sources</h1>"]
        for b_ in sorted(bm["bibliography"], key=lambda x: x["title"]):
            bib.append("<h2>%s · %s</h2>" % (E(b_["title"]), E(b_["culture"])))
            for s in b_["sources"]:
                bib.append("<p>%s</p>" % E(s))
        add("sources.xhtml", "Sources", "\n".join(bib), "frontmatter",
            in_nav=("Sources", 0))
        inv = ["<h1>Invented Traditions</h1>"]
        for t in bm["inventedTraditions"]:
            inv.append("<h2>%s</h2><p><i>%s</i> %s</p>"
                       % (E(t["claim"]), E(t["verdict"]), E(t["detail"])))
        add("invented.xhtml", "Invented Traditions", "\n".join(inv),
            "frontmatter", in_nav=("Invented Traditions", 0))
        mg = ["<h1>Materials and Substitutions</h1>"]
        for x in sorted(bm["materialsGuide"], key=lambda y: -y["count"]):
            mg.append("<h2>%s</h2><p>%s</p>"
                      % (E(x["substitute"]), E(", ".join(x["usedBy"]))))
        add("materials.xhtml", "Materials and Substitutions", "\n".join(mg),
            "frontmatter", in_nav=("Materials and Substitutions", 0))
        note = ("<h1>Board Templates</h1><p>The print editions of this book "
                "carry full-size board templates for photocopying. In this "
                "digital edition the board for each game is drawn beside its "
                "rules, and scales to any screen; draw the board on paper "
                "from the diagram.</p>")
        add("templates.xhtml", "Board Templates", note, "frontmatter",
            in_nav=("Board Templates", 0))

    # ── nav ───────────────────────────────────────────────────────────
    # İki seviyeli içindekiler. `<ol>` bir `<li>`nin İÇİNDE açılmak
    # zorundadır; ilk sürüm onu kardeş olarak açıyordu ve nav.xhtml
    # bozuk XML çıkıyordu — EPUB okuyucuları bunu reddeder.
    nav = ['<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>']
    i = 0
    while i < len(nav_items):
        name, label, lvl = nav_items[i]
        nav.append('<li><a href="text/%s">%s</a>' % (name, E(label)))
        kids = []
        j = i + 1
        while j < len(nav_items) and nav_items[j][2] > lvl:
            kids.append(nav_items[j])
            j += 1
        if kids:
            nav.append("<ol>")
            for kn, kl, _ in kids:
                nav.append('<li><a href="text/%s">%s</a></li>' % (kn, E(kl)))
            nav.append("</ol>")
        nav.append("</li>")
        i = j
    nav.append("</ol></nav>")
    nav_doc = ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
               '<html xmlns="http://www.w3.org/1999/xhtml" '
               'xmlns:epub="http://www.idpf.org/2007/ops" lang="en" '
               'xml:lang="en"><head><title>Contents</title>'
               '<meta charset="utf-8"/>'
               '<link rel="stylesheet" type="text/css" href="style.css"/>'
               '</head><body>%s</body></html>\n' % "".join(nav))

    # ── OPF ───────────────────────────────────────────────────────────
    uid = UUID_NS + hashlib.sha1(
        (tp["title"] + tp["subtitle"]).encode()).hexdigest()[:12]
    manifest = ['<item id="nav" href="nav.xhtml" '
                'media-type="application/xhtml+xml" properties="nav"/>',
                '<item id="css" href="style.css" media-type="text/css"/>']
    for i, n in enumerate(spine):
        manifest.append('<item id="s%d" href="text/%s" '
                        'media-type="application/xhtml+xml"/>' % (i, n))
    opf = ('<?xml version="1.0" encoding="utf-8"?>\n'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
           'unique-identifier="bookid" xml:lang="en">\n'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
           '<dc:identifier id="bookid">%s</dc:identifier>\n'
           '<dc:title>%s</dc:title>\n'
           '<dc:creator>%s</dc:creator>\n'
           '<dc:publisher>%s</dc:publisher>\n'
           '<dc:language>en</dc:language>\n'
           '<dc:description>%s</dc:description>\n'
           '<meta property="dcterms:modified">2026-08-20T00:00:00Z</meta>\n'
           '<meta property="schema:accessMode">textual</meta>\n'
           '<meta property="schema:accessMode">visual</meta>\n'
           '<meta property="schema:accessibilityFeature">structuralNavigation</meta>\n'
           '</metadata>\n<manifest>\n%s\n</manifest>\n<spine>\n%s\n</spine>\n'
           '</package>\n'
           % (uid, E(tp["title"]), E(tp["author"]), E(tp["publisher"]),
              E(tp["subtitle"]),
              "\n".join(manifest),
              "\n".join('<itemref idref="s%d"/>' % i
                        for i in range(len(spine)))))

    out_dir = os.path.join(root, "08_OUTPUT", "KINDLE")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "GreatBookOfWorldGames.epub")
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0" encoding="utf-8"?>\n'
                   '<container version="1.0" '
                   'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" '
                   'media-type="application/oebps-package+xml"/></rootfiles>'
                   '</container>\n', zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav_doc, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, zipfile.ZIP_DEFLATED)
        for name, data in files:
            z.writestr(name, data, zipfile.ZIP_DEFLATED)

    cover_raw = os.path.join(root, "07_ASSETS", "raw", "cover")
    have_cover = bool(os.path.isdir(cover_raw) and
                      [f for f in os.listdir(cover_raw)
                       if not f.startswith(".")])
    rep = {
        "format": "EPUB 3, reflowable",
        "file": os.path.relpath(path, root),
        "sha256": sha256(path), "bytes": os.path.getsize(path),
        "documents": len(files), "spineItems": len(spine),
        "games": len(book["games"]),
        "diagramsEmbedded": sum(len(g.get("diagrams") or [])
                                for g in book["games"]),
        "diagramFormat": "inline SVG (vector, no raster)",
        "coverImage": None,
        "coverStatus": ("READY" if have_cover
                        else "BLOCKED — kurucu kapak sanatı yok; sahte kapak "
                             "KONMADI"),
        "fixedLayout": False,
        "fixedLayoutRationale":
            "Çift sayfa mimarisi bir BASKI kısıtına verilmiş cevaptır. "
            "Kaydırılan bir ekranda o kısıt yoktur; madde kesintisiz akar. "
            "Sabit düzen ise gövde metnini telefonda okunamaz kılar ve "
            "okurun erişilebilirlik ayarlarını kilitler.",
        "measured": m,
    }
    dump(os.path.join(root, "06_REPORTS", "epub.json"), rep)

    print("  ✓ EPUB 3 (reflowable) · %d belge · %d oyun · %d diyagram (SVG)"
          % (len(files), len(book["games"]), rep["diagramsEmbedded"]))
    print("    %s · %.1f KB" % (rep["file"], rep["bytes"] / 1024.0))
    if not have_cover:
        print("    ⛔ KAPAK YOK — Kindle bir kapak görseli ister. Sahte kapak "
              "konmadı; kurucu sanatı bekleniyor.")
    return 0



def manuscript_absent(root: str) -> bool:
    """Ticari manuscript depoda YOKTUR (karar K12).

    CI taze bir klonda koşar ve orada `02_MANUSCRIPT/book.json` bulunmaz.
    Bu bir kusur DEĞİLDİR ve kapı orada BOŞ KOŞAR. Bir kapının CI'da
    kırmızı yanması, kusuru olduğu için olmalıdır; verinin orada olmaması
    için değil."""
    return not os.path.exists(os.path.join(root, "02_MANUSCRIPT", "book.json"))


def run_check(root: str) -> int:
    p = os.path.join(root, "06_REPORTS", "epub.json")
    if not os.path.exists(p):
        print("  · EPUB üretilmemiş — ATLANDI")
        return 0
    if manuscript_absent(root):
        print("  · ticari manuscript bu depoda yok — EPUB denetimi ATLANDI "
              "(CI'da beklenen)")
        return 0
    r = load(p)
    f = os.path.join(root, r["file"])
    if not os.path.exists(f):
        print("  ✗ EPUB dosyası yok: %s" % r["file"])
        return 1
    if sha256(f) != r["sha256"]:
        print("  ✗ EPUB sağlama toplamı tutmuyor")
        return 1
    with zipfile.ZipFile(f) as z:
        names = z.namelist()
        if names[0] != "mimetype":
            print("  ✗ EPUB: 'mimetype' ilk giriş DEĞİL — okuyucular reddeder")
            return 1
        if z.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
            print("  ✗ EPUB: 'mimetype' SIKIŞTIRILMIŞ — sıkıştırılmamalı")
            return 1
        bad = z.testzip()
        if bad:
            print("  ✗ EPUB bozuk: %s" % bad)
            return 1
        # ⚠ XHTML İYİ BİÇİMLİ OLMAK ZORUNDA. EPUB HTML değil XML'dir;
        # tek bir eşleşmeyen etiket dosyayı okuyucuda açılmaz yapar.
        # nav.xhtml ilk sürümde tam olarak böyle bozuktu.
        import xml.etree.ElementTree as ET
        ill = []
        for n in names:
            if n.endswith((".xhtml", ".opf", ".xml")):
                try:
                    ET.fromstring(z.read(n))
                except ET.ParseError as exc:
                    ill.append("%s: %s" % (n, exc))
        if ill:
            for x in ill[:6]:
                print("  ✗ bozuk XML — %s" % x)
            return 1
    print("  ✓ EPUB geçerli · %d belge · %s"
          % (r["documents"], r["coverStatus"].split("—")[0].strip()))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  KINDLE EPUB")
    print("=" * 74)
    rc = run_check(root) if args.check else build(root)
    print("=" * 74)
    return rc


if __name__ == "__main__":
    sys.exit(main())
