#!/usr/bin/env python3
"""
DİYAGRAM KAPISI — The Great Book of World Games
================================================================================
`00_CONTEXT/DIAGRAM_LANGUAGE.md` bir sözleşmedir; bu betik onun mekanizmasıdır.

Denetlenen:
  ① Sözlük bütünlüğü — dil dosyası kendi içinde tutarlı mı
  ② Tahta sınıfı ve KOORDİNAT KURALI — her koordinat sınıfına uyuyor mu
  ③ Sınır — koordinat tahtanın İÇİNDE mi
  ④ Glif sözlüğü — kullanılan her glif tanımlı mı
  ⑤ EFSANE — kullanılan gliflerin TAM kümesi mi (eksik yok, FAZLA yok)
  ⑥ YENİDEN KURGULAMA TUTARLILIĞI — diyagram, kaydın beyanını yalanlıyor mu
  ⑦ Panel sayısı
  ⑧ Baskı güvenliği — renk yok, gri yalnızca izinli seviyelerde

⑥ NEDEN EN ÖNEMLİSİ: bir oyun kayıtta `reconstructed` ama diyagramı öyle
demiyorsa, kusursuz çizilmiş bir tahta prozanın dürüstlüğünü SESSİZCE bozar.
Okur diyagrama bakar ve tarihsel kesinlik görür. Bu kapı onu imkânsız kılar.

⑤ NEDEN VAR: kullanılmayan bir sembol efsanede duramaz. Ölü bir kural
sessizce yanlış güven verir (Codex dersi D28) — bir okur efsanede gördüğü
sembolü tahtada arar ve bulamaz.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.facts: dict = {}

    def check(self, cond: bool, label: str) -> bool:
        self.checks += 1
        if cond:
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return bool(cond)

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def brief(items: list, n: int = 5) -> str:
    if not items:
        return ""
    more = "" if len(items) <= n else " … (+%d)" % (len(items) - n)
    return " — %s%s" % (", ".join(str(i) for i in items[:n]), more)


def in_bounds(coord: str, cls: str, size: dict) -> bool:
    """③ Koordinat tahtanın içinde mi.

    Sınır denetimi kalıp denetiminden AYRIDIR: 'z9' kalıba uyar ama dokuz
    sütunlu bir tahtada YOKTUR. Kalıp geçerliliği yer varlığı demek değildir."""
    if cls in ("cell", "point"):
        m = re.match(r"^([a-z])([0-9]+)$", coord)
        if not m:
            return False
        col = ord(m.group(1)) - ord("a") + 1
        row = int(m.group(2))
        return 1 <= col <= size.get("cols", 0) and 1 <= row <= size.get("rows", 0)
    if cls == "pit":
        if re.match(r"^\[[AB]\]$", coord):
            return bool(size.get("stores", True))
        m = re.match(r"^[AB]'?([0-9]+)$", coord)
        return bool(m) and 1 <= int(m.group(1)) <= size.get("pitsPerRow", 0)
    if cls == "track":
        if coord == "out":
            return True
        m = re.match(r"^([0-9]+)[ab]?$", coord)
        return bool(m) and 0 <= int(m.group(1)) <= size.get("stations", 0) + 1
    return True  # bodily: sınır yok, kalıp denetimi yeter


def check_lexicon(lang: dict, rep: Report) -> None:
    print("\n── ① sözlük bütünlüğü ──")
    for key in ("boardClasses", "coordPatterns", "glyphs", "arrows",
                "markers", "panelRules", "print"):
        rep.check(key in lang, "sözlük bloğu var: %s" % key)

    allowed = set(lang["print"]["greyLevelsAllowed"])
    bad = []
    for name, g in lang["glyphs"].items():
        for k in ("fill", "stroke"):
            if g.get(k) not in allowed:
                bad.append("%s.%s=%s" % (name, k, g.get(k)))
    rep.check(not bad,
              "her glif yalnızca izinli gri seviyelerini kullanıyor" + brief(bad))

    rules = {c["coordRule"] for c in lang["boardClasses"].values()}
    missing = sorted(rules - set(lang["coordPatterns"]))
    rep.check(not missing,
              "her tahta sınıfının koordinat kalıbı tanımlı" + brief(missing))

    thin = [n for n, a in lang["arrows"].items()
            if a.get("widthPt", 0) < lang["print"]["minStrokePt"]]
    rep.check(not thin,
              "hiçbir ok en ince çizgi sınırının altında değil (%.2f pt)"
              % lang["print"]["minStrokePt"] + brief(thin))

    rep.check(lang["print"].get("colourForbidden") is True,
              "sözlük rengi yasaklıyor (karar K3)")


def check_rendered_budget(cfg: dict, diagrams: list, root: str,
                          rep: Report) -> None:
    """⑨ 150 MM DİYAGRAM BÜTÇESİ — RENDER EDİLMİŞ ÖLÇÜMDEN (karar K19).

    ⚠ BU KAPI TANIMLAYICIYA BAKMAZ, ÇIKTIYA BAKAR.

    Gerekçe: bir tanımlayıcı "9×9 tahta" der ve bu bir boyut vermez.
    Boyutu adım aralığı, efsane satır sayısı, panel dizilimi ve altyazı
    belirler — yani ancak çizildikten sonra bilinir. "Daha küçük görünüyor"
    bir kanıt değildir ve bu kapı onu kabul etmez.

    Render edilmemiş bir diyagram DENETLENMEMİŞTİR ve denetlenmemiş bir
    diyagram geçemez: aksi hâlde bütçe, çizilmeyen her diyagram için
    sessizce boş koşardı.
    """
    limit = cfg["diagram"]["maxDiagramMmPerGame"]
    print("\n── ⑨ diyagram bütçesi (%d mm · RENDER ÖLÇÜMÜ) ──" % limit)
    path = os.path.join(root, "06_REPORTS", "diagram-render.json")
    if not os.path.exists(path):
        rep.check(not diagrams,
                  "render ölçümü yok — diyagram varsa DENETLENEMEZ "
                  "(önce: 04_BUILD/render_diagrams.py)")
        return
    measured = {d["diagramId"]: d for d in load(path).get("diagrams", [])}

    unrendered = [d["diagramId"] for d in diagrams
                  if d["diagramId"] not in measured]
    rep.check(not unrendered,
              "her diyagram render edilmiş ve ÖLÇÜLMÜŞ" + brief(unrendered))

    # FAZ 5 EKLEMESİ — TERS YÖN: ölçümde olup TANIMI OLMAYAN diyagram.
    #
    # Denetim tek yönlüydü: "her tanımın ölçümü var mı". Tersi sorulmuyordu
    # ve Faz 5'te tam olarak o koptu — K23 iki oyunu kapsamdan çıkardı,
    # tanımları silindi, ama ölçüm dosyası ikisini de SAYMAYA devam etti ve
    # kapı yeşil yandı.
    #
    # Bu bir muhasebe hatası değil bir BÜTÇE hatasıdır: ölçüm dosyası, oyun
    # başına 150 mm toplamının hesaplandığı yerdir. Artık var olmayan bir
    # diyagram o toplama girerse bütçe gerçek kitabı değil eski kitabı
    # denetler.
    # ⚠ AMA YALNIZCA TANIM KÜMESİ TAMSA. `07_ASSETS/diagrams/**` korumalı
    # katmandadır: CI'da yalnızca `pilot` ve `phase3` kayıtları görünür,
    # `phase4_diagrams.json` görünmez. Orada bu denetim, GÖRÜNMEYEN her
    # tanımı "hayalet" sayar ve doğru bir ölçümü kırmızı yakar.
    #
    # Bu, kapının kendisinin de öğrendiği ders: eksik veriyle koşan bir
    # denetim, denetlediğini sanıp başka bir şeyi denetler. Manuscript
    # yereldeyse tam koşar, CI'da açıkça boş koşar (körlüğü selftest
    # kapatır — qa_manuscript ile aynı sözleşme).
    full_view = os.path.exists(os.path.join(root, "02_MANUSCRIPT", "book.json"))
    if full_view:
        ghost = sorted(set(measured) - {d["diagramId"] for d in diagrams})
        rep.check(not ghost,
                  "ölçümde TANIMI OLMAYAN diyagram yok (bayat render raporu)"
                  + brief(ghost))
    else:
        print("  · tanım kümesi kısmi (korumalı katman yok) — bayatlık "
              "denetimi ATLANDI; selftest kapsar")

    ovr = cfg["diagram"].get("diagramBudgetOverrides") or {}

    def _cap(gid: str) -> float:
        o = ovr.get(gid)
        return float(o["maxMm"]) if isinstance(o, dict) and o.get("maxMm") \
            else float(limit)

    over, wide = [], []
    for d in diagrams:
        m = measured.get(d["diagramId"])
        if not m:
            continue
        # Tek diyagram tavanı da K24 istisnasını tanır; yoksa istisna
        # yalnızca TOPLAMDA işler ve tek büyük bir panel yine reddedilirdi.
        if m["heightMm"] > _cap(d["gameId"]):
            over.append("%s → %.1f mm (%+.1f)"
                        % (d["diagramId"], m["heightMm"],
                           m["heightMm"] - _cap(d["gameId"])))
        if m["renderedWidthMm"] > lang_width(cfg, root):
            wide.append("%s → %.1f mm" % (d["diagramId"], m["renderedWidthMm"]))
    rep.check(not over,
              "hiçbir diyagram %d mm bütçesini aşmıyor" % limit + brief(over))
    rep.check(not wide, "hiçbir diyagram genişlik sınırını aşmıyor" + brief(wide))

    # ⚠ BÜTÇE OYUN BAŞINADIR, DİYAGRAM BAŞINA DEĞİL.
    #
    # Faz 4 ölçümü bu kapıda bir KÖRLÜK buldu. Ayarın adı zaten
    # `maxDiagramMmPerGame` ve türetimi de oyun başınadır (çift sayfanın
    # metinden artan 152 mm'si). Kapı ise her diyagramı TEK TEK ölçüyordu.
    # Sonuç: iki diyagramı olan bir madde bütçeyi ikiye katlayabiliyor ve
    # kapı yeşil yanıyordu. Tablut tam olarak bunu yapıyordu — 88,5 + 93,0
    # = 181,5 mm — ve on dokuz maddelik örneklemde çift sayfayı aşan TEK
    # madde oydu. Yani bütçe, tutması gereken şeyi tutmuyordu.
    # ── K24 · TEKİL İSTİSNA ────────────────────────────────────────────
    # Kurucu YALNIZCA cats-cradle için tavanı açtı. Mantık bilerek
    # "istisna listesi" değil "kimlik eşlemesi" biçimindedir:
    #
    #     limit = override.get(gameId, 150)
    #
    # Genel bir "muafiyet bayrağı" (örn. `allowOverBudget: true`) ASLA
    # eklenmedi, çünkü bir bayrak her maddeye yazılabilir; bir kimlik
    # eşlemesi ise her yeni satır için bir KARAR ister.
    overrides = cfg["diagram"].get("diagramBudgetOverrides") or {}

    def limit_for(gid: str) -> tuple:
        ov = overrides.get(gid)
        if isinstance(ov, dict) and ov.get("maxMm"):
            return float(ov["maxMm"]), True
        return float(limit), False

    per_game: dict = {}
    for d in diagrams:
        m = measured.get(d["diagramId"])
        if m:
            per_game.setdefault(d["gameId"], []).append(m["heightMm"])

    over_game, exceptions = [], []
    for g, hs in sorted(per_game.items()):
        cap, is_ex = limit_for(g)
        total = sum(hs)
        if total > cap:
            over_game.append("%s → %.1f mm (%d diyagram, %+.1f · tavan %.0f)"
                             % (g, total, len(hs), total - cap, cap))
        elif is_ex:
            exceptions.append("%s → %.1f mm (%d diyagram · İSTİSNA tavanı "
                              "%.0f · normal tavan %d)"
                              % (g, total, len(hs), cap, limit))
    rep.check(not over_game,
              "hiçbir OYUN kendi diyagram tavanını aşmıyor (normal %d mm)"
              % limit + brief(over_game))
    for line in exceptions:
        print("  · K24 İSTİSNA UYGULANDI: %s" % line)

    # İstisna sözlüğü DARALTILMIŞ kalmalı. Bu denetim istisnanın kendisini
    # değil, istisnanın YAYILMASINI engeller.
    stray = sorted(k for k in overrides
                   if not k.startswith("$") and k != "cats-cradle")
    rep.check(not stray,
              "diyagram bütçesi istisnası YALNIZCA cats-cradle (K24)"
              + brief(stray))
    unused = [k for k in overrides
              if not k.startswith("$") and k not in per_game]
    rep.check(not unused,
              "tanımlı her istisna GERÇEKTEN kullanılıyor (ölü muafiyet yok)"
              + brief(unused))

    if measured:
        hs = [m["heightMm"] for m in measured.values()]
        rep.facts["diagramMm"] = {"min": min(hs), "max": max(hs),
                                  "mean": round(sum(hs) / len(hs), 1),
                                  "limit": limit}
        print("  · ölçülen yükseklik: %.1f – %.1f mm (ortalama %.1f · sınır %d)"
              % (min(hs), max(hs), sum(hs) / len(hs), limit))


def lang_width(cfg: dict, root: str) -> float:
    return load(os.path.join(root, cfg["diagram"]["specData"]))["print"]["maxWidthFullMm"]


def check_diagrams(lang: dict, diagrams: list, games: dict, rep: Report) -> None:
    print("\n── ②–⑧ diyagram tanımlayıcıları (%d) ──" % len(diagrams))
    if not diagrams:
        rep.warn("diyagram tanımlayıcısı yok — kapı boş koşuyor "
                 "(körlüğü selftest kapatır)")
        return

    classes = lang["boardClasses"]
    patterns = lang["coordPatterns"]
    glyphs = set(lang["glyphs"])
    arrows = set(lang["arrows"])
    markers = set(lang["markers"])
    types = set(lang["diagramTypes"])
    grey_ok = set(lang["print"]["greyLevelsAllowed"])

    bad_class, bad_type, bad_coord, out_of_bounds = [], [], [], []
    bad_glyph, legend_missing, legend_extra = [], [], []
    legend_ambiguous: list = []
    recon_mismatch, bad_panels, colour_used, bad_grey = [], [], [], []
    orphan_game = []

    for d in diagrams:
        did = d.get("diagramId", "?")
        cls = d.get("boardClass")
        if cls not in classes:
            bad_class.append("%s → %s" % (did, cls))
            continue
        if d.get("type") not in types:
            bad_type.append("%s → %s" % (did, d.get("type")))

        gid = d.get("gameId")
        if gid not in games:
            orphan_game.append("%s → %s" % (did, gid))

        graph = bool(d.get("nodes"))
        pat = re.compile(patterns["graph"] if graph
                         else patterns[classes[cls]["coordRule"]])
        size = d.get("size", {})
        used: set[str] = set()

        for p in d.get("pieces", []):
            at, gl = p.get("at", ""), p.get("glyph")
            if not pat.match(at):
                bad_coord.append("%s → '%s' (%s kuralı)" % (did, at, cls))
            elif graph:
                # Graph tahtada SINIR, tanımlı düğüm kümesidir. Bir taş
                # tanımsız bir düğümde duramaz — tahtanın dışındadır.
                if at not in d["nodes"]:
                    out_of_bounds.append("%s → '%s' tanımlı düğüm değil" % (did, at))
            elif not in_bounds(at, cls, size):
                out_of_bounds.append("%s → '%s' tahta dışında" % (did, at))
            if gl not in glyphs:
                bad_glyph.append("%s → %s" % (did, gl))
            else:
                used.add(gl)
            # `captured` bir BAYRAKTIR ama okur için bir SEMBOLDÜR: taşın
            # üstüne bir çarpı basar. Kullanılanlar kümesine girmezse efsane
            # onu açıklayamaz (ölü sembol hatası verir) ve × açıklamasız kalır.
            if p.get("captured"):
                used.add("captured")

        for a in d.get("arrows", []):
            if a.get("kind") not in arrows:
                bad_glyph.append("%s → ok:%s" % (did, a.get("kind")))
            else:
                used.add(a["kind"])
            for key in ("from", "to"):
                c = a.get(key, "")
                if c and not pat.match(c):
                    bad_coord.append("%s → ok %s '%s'" % (did, key, c))
                elif c and graph and c not in d["nodes"]:
                    out_of_bounds.append("%s → ok %s '%s' tanımlı düğüm değil"
                                         % (did, key, c))
                elif c and not graph and not in_bounds(c, cls, size):
                    out_of_bounds.append("%s → ok %s '%s' tahta dışında" % (did, key, c))

        for m in d.get("markers", []):
            if m.get("kind") not in markers:
                bad_glyph.append("%s → işaret:%s" % (did, m.get("kind")))
            else:
                used.add(m["kind"])

        # ⑤ EFSANE = kullanılanların TAM kümesi
        legend = {e.get("glyph") for e in d.get("legend", [])}
        for miss in sorted(used - legend):
            legend_missing.append("%s → %s" % (did, miss))
        for extra in sorted(legend - used):
            legend_extra.append("%s → %s (ÖLÜ SEMBOL)" % (did, extra))

        # ── FAZ 5 · EFSANEDE AYIRT EDİLEMEYEN İKİ SEMBOL ─────────────────
        #
        # Faz 4, efsane sembolünün ÇİZİLMESİNİ sağladı (font bağımlılığı
        # gitti) ama ÇİZİMLERİN BİRBİRİNDEN FARKLI olduğunu hiç denetlemedi.
        # Efsane bir glifi yalnızca (dolgu + halka + çarpı) ile çizer; yani
        # `light`, `empty`, `lightAlt`, `seedCount` ve `inHand` efsanede
        # BİREBİR AYNI dairedir. `king` ile `lightSpecial` de öyle.
        #
        # Bu görsel denetimde bulundu: cats-cradle efsanesinde "ipin
        # tutulduğu parmak" ve "ip yolu" satırları aynı boş daireyi
        # taşıyordu ve okur hangisinin hangisi olduğunu ÖĞRENEMİYORDU.
        # Ölçüm sayıları tertemizdi — Faz 4'ün tilki kusurunun aynısı, bir
        # adım öteye taşınmış hâli.
        sig: dict = {}
        for e in d.get("legend", []):
            k = e.get("glyph")
            gl = lang["glyphs"].get(k)
            if not gl:
                continue          # ok/işaret: ayrı çizim yolu
            s = (gl.get("fill"),
                 k in ("king", "lightSpecial", "darkSpecial"),
                 k == "captured")
            if s in sig and sig[s] != k:
                legend_ambiguous.append(
                    "%s → '%s' ile '%s' efsanede AYNI çiziliyor"
                    % (did, sig[s], k))
            sig[s] = k

        # ⑥ Yeniden kurgulama tutarlılığı — iki yönlü
        g = games.get(gid, {})
        is_recon = g.get("playabilityStatus") == "reconstructed"
        claims = bool(d.get("reconstructed"))
        if is_recon and not claims:
            recon_mismatch.append("%s: kayıt 'reconstructed', diyagram DEMİYOR" % did)
        if claims and not is_recon:
            recon_mismatch.append("%s: diyagram 'reconstructed', kayıt DEMİYOR" % did)
        if claims and not (d.get("caption") or "").strip():
            recon_mismatch.append("%s: yeniden kurgulanmış diyagramın altyazısı yok" % did)
        if d.get("adaptedFrom") and not (d.get("caption") or "").strip():
            recon_mismatch.append("%s: uyarlanmış diyagramın altyazısı yok" % did)

        # ⑦ Panel sayısı
        panels = d.get("panels", 1)
        limit = lang["panelRules"]["maxPanels"]
        exact = lang["panelRules"].get("exactPanelsForBoardClass", {})
        key = "%s/%s" % (cls, d.get("frame", ""))
        if key in exact:
            if panels != exact[key]:
                bad_panels.append("%s → %d (tam %d olmalı)" % (did, panels, exact[key]))
        elif panels > limit:
            bad_panels.append("%s → %d (azami %d)" % (did, panels, limit))

        # ⑧ Baskı güvenliği
        if d.get("colour") or d.get("color"):
            colour_used.append(did)
        for lvl in d.get("greyLevels", []):
            if lvl not in grey_ok:
                bad_grey.append("%s → %%%s" % (did, lvl))

    dangling = []
    for d in diagrams:
        if not d.get("nodes"):
            continue
        for a, b in d.get("edges", []):
            for k in (a, b):
                if k not in d["nodes"]:
                    dangling.append("%s → kenar ucu '%s' tanımsız"
                                    % (d.get("diagramId"), k))
    rep.check(not dangling,
              "graph tahtalarda kopuk kenar yok" + brief(dangling))
    rep.check(not bad_class, "her diyagram tanımlı bir tahta sınıfı taşıyor" + brief(bad_class))
    rep.check(not bad_type, "diyagram tipleri geçerli" + brief(bad_type))
    rep.check(not orphan_game, "her diyagram envanterdeki bir oyuna bağlı" + brief(orphan_game))
    rep.check(not bad_coord, "her koordinat sınıfının kuralına uyuyor" + brief(bad_coord))
    rep.check(not out_of_bounds, "her koordinat tahtanın içinde" + brief(out_of_bounds))
    rep.check(not bad_glyph, "kullanılan her glif ve ok sözlükte var" + brief(bad_glyph))
    rep.check(not legend_missing, "efsane kullanılan her sembolü içeriyor" + brief(legend_missing))
    rep.check(not legend_extra, "efsanede ÖLÜ sembol yok" + brief(legend_extra))
    rep.check(not legend_ambiguous,
              "efsanede AYIRT EDİLEMEYEN iki sembol yok" + brief(legend_ambiguous))
    rep.check(not recon_mismatch,
              "diyagram beyanı kaydın beyanıyla tutarlı" + brief(recon_mismatch))
    rep.check(not bad_panels, "panel sayıları kurala uyuyor" + brief(bad_panels))
    rep.check(not colour_used, "hiçbir diyagram renk kullanmıyor" + brief(colour_used))
    rep.check(not bad_grey, "gri yalnızca izinli seviyelerde" + brief(bad_grey))

    rep.facts["diagrams"] = len(diagrams)
    rep.facts["byClass"] = {}
    for d in diagrams:
        c = d.get("boardClass")
        rep.facts["byClass"][c] = rep.facts["byClass"].get(c, 0) + 1
    print("  · sınıf dağılımı: %s" % rep.facts["byClass"])


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  DİYAGRAM DİLİ VE TANIMLAYICI KAPISI")
    print("=" * 74)

    rep = Report(args.verbose)
    try:
        cfg = load(os.path.join(root, "project_config.json"))
        lang = load(os.path.join(root, cfg["diagram"]["specData"]))
        games = {g["gameId"]: g for g in
                 load(os.path.join(root, "01_SOURCE", "game_index.json"))["games"]}
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        print("  ⛔ kaynak dosya okunamadı: %s" % exc)
        return 1

    rep.check(cfg["diagram"].get("frozen") is True,
              "diyagram dili DONDURULMUŞ (kapı: %s)"
              % cfg["diagram"].get("frozenAtPhase"))
    rep.check(os.path.isfile(os.path.join(root, cfg["diagram"]["specDoc"])),
              "insan okunur sözleşme var: %s" % cfg["diagram"]["specDoc"])

    check_lexicon(lang, rep)

    ddir = os.path.join(root, "07_ASSETS", "diagrams")
    diagrams: list = []
    for fn in sorted(os.listdir(ddir)) if os.path.isdir(ddir) else []:
        if not fn.endswith(".json") or fn == "diagram_language.json":
            continue
        try:
            d = load(os.path.join(ddir, fn))
        except json.JSONDecodeError as exc:
            rep.check(False, "diyagram dosyası bozuk: %s — %s" % (fn, exc))
            continue
        diagrams.extend(d.get("diagrams", []) if isinstance(d, dict) else d)

    check_diagrams(lang, diagrams, games, rep)
    check_rendered_budget(cfg, diagrams, root, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · diyagram dili v%s DONDURULMUŞ"
              % (rep.checks, lang.get("version")))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
