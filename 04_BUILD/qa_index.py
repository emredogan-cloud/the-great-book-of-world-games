#!/usr/bin/env python3
"""
ARKA MADDE VE ÜÇ İNDEKS KAPISI — The Great Book of World Games
================================================================================
Yol haritası Faz 4 § 8 bu kapıyı ister: *"üç indeksin bütünlüğü: her oyun üç
indekste de doğru yerde mi."* Faz 4 arka maddeyi yazmadı; Faz 5 yazdı ve
kapıyı da yazdı.

  ⚠ ÜRETİLMİŞ BİR DOSYA, DENETLENMEDİKÇE ELLE YAZILMIŞ BİR DOSYADAN
  DAHA GÜVENLİ DEĞİLDİR.

Bir üreteç yanlış kova hesaplarsa çıktı **tutarlı görünür** — çünkü hem
indeksi hem de özeti aynı yanlış fonksiyon üretmiştir. Bu yüzden bu kapı
kovaları ÜRETEÇTEN İÇE AKTARMAZ; envanterden **yeniden hesaplar** ve
karşılaştırır. Tek istisna kova TANIMIDIR (`player_bucket` ·
`duration_bucket`): onu ikinci kez yazmak, iki tanımın ayrışması riskini
getirirdi ve o risk daha büyüktür (Faz 4 · `measured_block_keys` dersi).

Denetlenen:
  ① KAPSAM        — 100 oyunun her biri ÜÇ indekste de TAM BİR KEZ
  ② KOVA          — her oyunun kovası envanterden yeniden hesaplandı
  ③ SAYFA         — sayfa göndermesi YALNIZCA gerçekten ölçülmüş oyunda
  ④ SÖZLÜK        — 60+ terim; `attestedIn` iddiası prozada DOĞRULANDI
  ⑤ KAYNAKÇA      — `pageVerified` iddiası doğrulama kaydıyla eşleşiyor
  ⑥ ŞABLON        — her şablon gerçek bir diyagrama ve KAPSAMDAKİ bir oyuna
  ⑦ GELENEK KUTUSU— adı geçen her oyun kapsamda
  ⑧ BAYATLIK      — arka madde, envanterin ŞU ANKİ hâlinden üretilmiş mi

⑧ NEDEN VAR: arka madde envanterden üretilir ama dosyada DONAR. Envanter
değişir ve arka madde yeniden üretilmezse, kitabın en çok kullanılan kısmı
sessizce eski kitabı anlatır. Faz 5'in kapsam değişikliği tam olarak böyle
bir olaydır.

Manuscript depoda YOKTUR: tam metin arka madde orada boş koşar ve public
yapısal özet denetlenir. Körlüğü `selftest.py` kapatır.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

MIN_GLOSSARY_TERMS = 60          # EDITORIAL_ARCHITECTURE § 5
REQUIRED_SECTIONS = ("boardTemplates", "materialsGuide", "glossary",
                     "bibliography", "indexes", "inventedTraditions")
THREE_INDEXES = ("byCulture", "byPlayerCount", "byDurationAndAge")


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
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


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def brief(items, n: int = 5) -> str:
    if not items:
        return ""
    more = "" if len(items) <= n else " … (+%d)" % (len(items) - n)
    return " — %s%s" % (", ".join(str(i) for i in items[:n]), more)


def run(root: str, args) -> tuple:
    rep = Report(args.verbose)
    sys.path.insert(0, HERE)
    import build_backmatter as bb  # noqa: E402

    scope = load(os.path.join(root, "01_SOURCE", "scope_lock.json"))
    index = load(os.path.join(root, "01_SOURCE", "game_index.json"))
    inv = {g["gameId"]: g for g in index["games"]}
    scope_ids = [e["gameId"] for e in scope["entries"]]

    bpath = os.path.join(root, "02_MANUSCRIPT", "backmatter.json")
    ppath = os.path.join(root, "06_REPORTS", "backmatter.json")

    if not os.path.exists(bpath):
        if not os.path.exists(ppath):
            print("  · arka madde henüz üretilmemiş — kapı BOŞ KOŞAR "
                  "(önce: 04_BUILD/build_backmatter.py)")
            return 0, rep
        # PUBLIC KATMAN — CI burada koşar.
        pub = load(ppath)
        print("\n── public yapısal özet (manuscript depoda yok) ──")
        rep.check(pub.get("scopeGames") == len(scope_ids),
                  "özet kapsam sayısı kilitle uyuşuyor (%s/%d)"
                  % (pub.get("scopeGames"), len(scope_ids)))
        rep.check(pub.get("glossaryTerms", 0) >= MIN_GLOSSARY_TERMS,
                  "sözlük ≥%d terim (%s)" % (MIN_GLOSSARY_TERMS,
                                             pub.get("glossaryTerms")))
        for name in THREE_INDEXES:
            b = (pub.get("indexes") or {}).get(name) or {}
            rep.check(sum(b.values()) == len(scope_ids),
                      "%s indeksi 100 oyunu taşıyor (%d)"
                      % (name, sum(b.values())))
        rep.facts = {"layer": "public", "scopeGames": pub.get("scopeGames")}
        return (1 if rep.errors else 0), rep

    bm = load(bpath)

    print("\n── ① kapsam: her oyun üç indekste de tam bir kez ──")
    missing_sections = [s for s in REQUIRED_SECTIONS if s not in bm]
    rep.check(not missing_sections,
              "altı bölümün hepsi var" + brief(missing_sections))

    idx = bm.get("indexes") or {}
    for name in THREE_INDEXES:
        buckets = (idx.get(name) or {}).get("buckets") or {}
        seen: dict = {}
        for rows in buckets.values():
            for r in rows:
                seen[r["gameId"]] = seen.get(r["gameId"], 0) + 1
        missing = [g for g in scope_ids if g not in seen]
        dupe = sorted(g for g, n in seen.items() if n > 1)
        alien = sorted(set(seen) - set(scope_ids))
        rep.check(not missing,
                  "%s: kapsamdaki her oyun var (%d)" % (name, len(seen))
                  + brief(missing))
        rep.check(not dupe, "%s: hiçbir oyun iki kovada değil" % name
                  + brief(dupe))
        rep.check(not alien, "%s: KAPSAM DIŞI oyun yok" % name + brief(alien))

    print("\n── ② kova ataması envanterden YENİDEN hesaplandı ──")
    wrong_p, wrong_d, wrong_c = [], [], []
    for bucket, rows in ((idx.get("byPlayerCount") or {}).get("buckets")
                         or {}).items():
        for r in rows:
            want = bb.player_bucket(inv.get(r["gameId"], {}))
            if want != bucket:
                wrong_p.append("%s: %s→%s" % (r["gameId"], bucket, want))
    for bucket, rows in ((idx.get("byDurationAndAge") or {}).get("buckets")
                         or {}).items():
        for r in rows:
            want = bb.duration_bucket(inv.get(r["gameId"], {}))
            if want != bucket:
                wrong_d.append("%s: %s→%s" % (r["gameId"], bucket, want))
    by_id = {e["gameId"]: e for e in scope["entries"]}
    for culture, rows in ((idx.get("byCulture") or {}).get("buckets")
                          or {}).items():
        for r in rows:
            want = by_id[r["gameId"]]["culture"]
            if want != culture:
                wrong_c.append("%s: %s→%s" % (r["gameId"], culture, want))
    rep.check(not wrong_p, "oyuncu sayısı kovaları doğru" + brief(wrong_p))
    rep.check(not wrong_d, "süre kovaları doğru" + brief(wrong_d))
    rep.check(not wrong_c, "kültür kovaları kilitle birebir" + brief(wrong_c))

    print("\n── ③ sayfa göndermeleri ÖLÇÜLMÜŞ çıktıya dayanıyor ──")
    measured = bb.page_map(root)
    ghost_page, lost_page, bad_status = [], [], []
    for name in THREE_INDEXES:
        for rows in ((idx.get(name) or {}).get("buckets") or {}).values():
            for r in rows:
                gid, pg = r["gameId"], r.get("page")
                if pg is not None and gid not in measured:
                    ghost_page.append("%s/%s" % (name, gid))
                if pg is not None and measured.get(gid) != pg:
                    lost_page.append("%s/%s: %s≠%s"
                                     % (name, gid, pg, measured.get(gid)))
                want = "measured" if gid in measured else "awaiting-typesetting"
                if r.get("pageStatus") != want:
                    bad_status.append("%s/%s" % (name, gid))
    rep.check(not ghost_page,
              "ÖLÇÜLMEMİŞ bir oyuna sayfa numarası verilmemiş"
              + brief(ghost_page))
    rep.check(not lost_page,
              "her sayfa numarası dizgi ölçümüyle birebir" + brief(lost_page))
    rep.check(not bad_status,
              "sayfa durumu ölçüm gerçeğiyle uyuşuyor" + brief(bad_status))

    print("\n── ④ sözlük ──")
    gl = bm.get("glossary") or []
    rep.check(len(gl) >= MIN_GLOSSARY_TERMS,
              "sözlük ≥%d terim taşıyor (%d)" % (MIN_GLOSSARY_TERMS, len(gl)))
    nodef = [t["term"] for t in gl if len((t.get("definition") or "").strip()) < 20]
    rep.check(not nodef, "her terimin tanımı var" + brief(nodef))
    dupterm = sorted({t["term"] for t in gl
                      if [x["term"] for x in gl].count(t["term"]) > 1})
    rep.check(not dupterm, "sözlükte yinelenen terim yok" + brief(dupterm))

    # `attestedIn` bir İDDİADIR ve doğrulanır: sözlük, kitabın kullanmadığı
    # bir kelimeyi "kitapta geçiyor" diye gösteremez.
    written = {}
    mp = os.path.join(root, "02_MANUSCRIPT", "book.json")
    if os.path.exists(mp):
        written = {g["gameId"]: json.dumps(g, ensure_ascii=False)
                   for g in load(mp)["games"]}
    false_claim = []
    for t in gl:
        for gid in t.get("attestedIn") or []:
            blob = written.get(gid)
            if blob is None or not re.search(
                    r"\b%s\b" % re.escape(t["term"]), blob, re.I):
                false_claim.append("%s→%s" % (t["term"], gid))
    rep.check(not false_claim,
              "sözlüğün 'prozada geçiyor' iddiaları DOĞRU" + brief(false_claim))

    print("\n── ⑤ kaynakça ──")
    verified: dict = {}
    vp = os.path.join(root, "01_SOURCE", "source_verification.json")
    if os.path.exists(vp):
        for r in load(vp)["records"]:
            if r.get("status") == "verified":
                verified.setdefault(r["gameId"], []).append(r)
    bib = bm.get("bibliography") or []
    rep.check(len({b["gameId"] for b in bib}) == len(scope_ids),
              "kaynakça kapsamdaki 100 oyunu taşıyor (%d)"
              % len({b["gameId"] for b in bib}))
    nosrc = [b["gameId"] for b in bib if not b.get("sources")]
    rep.check(not nosrc, "kaynakçada künyesiz oyun yok" + brief(nosrc))
    overclaim = [b["gameId"] for b in bib
                 if b.get("pageVerifiedCount", 0) > len(verified.get(b["gameId"], []))]
    rep.check(not overclaim,
              "hiçbir madde OLMAYAN bir sayfa doğrulaması iddia etmiyor"
              + brief(overclaim))

    print("\n── ⑥ tahta şablonları ──")
    ddir = os.path.join(root, "07_ASSETS", "diagrams")
    known = set()
    for fn in sorted(os.listdir(ddir)) if os.path.isdir(ddir) else []:
        if fn.endswith("_diagrams.json"):
            for d in load(os.path.join(ddir, fn)).get("diagrams", []):
                known.add(d["diagramId"])
    tpl = bm.get("boardTemplates") or []
    ghost_t = [t["diagramId"] for t in tpl if t["diagramId"] not in known]
    out_t = [t["gameId"] for t in tpl if t["gameId"] not in set(scope_ids)]
    rep.check(not ghost_t, "her şablon GERÇEK bir diyagrama bağlı" + brief(ghost_t))
    rep.check(not out_t, "her şablon KAPSAMDAKİ bir oyuna bağlı" + brief(out_t))

    print("\n── ⑦ uydurulmuş gelenekler kutusu ──")
    inv_tr = bm.get("inventedTraditions") or []
    rep.check(bool(inv_tr), "kutu en az bir düzeltme taşıyor")
    thin = [t.get("claim", "?") for t in inv_tr
            if len((t.get("detail") or "").strip()) < 40
            or not (t.get("verdict") or "").strip()]
    rep.check(not thin, "her düzeltme gerekçeli" + brief(thin))
    out_g = [t["gameId"] for t in inv_tr
             if t.get("gameId") and t["gameId"] not in set(scope_ids)]
    rep.check(not out_g, "adı geçen her oyun kapsamda" + brief(out_g))

    print("\n── ⑧ bayatlık ──")
    rep.check(bm.get("scopeGames") == len(scope_ids),
              "arka madde ŞU ANKİ kapsamdan üretilmiş (%s/%d)"
              % (bm.get("scopeGames"), len(scope_ids)))
    bm_ids = {b["gameId"] for b in bib}
    drift = sorted(set(scope_ids) ^ bm_ids)
    rep.check(not drift,
              "arka maddedeki oyun kümesi kilitle BİREBİR" + brief(drift))
    rep.check(bm.get("measuredGames") == len(measured),
              "ölçülmüş oyun sayısı güncel (%s/%d)"
              % (bm.get("measuredGames"), len(measured)))

    rep.facts = {
        "layer": "manuscript",
        "scopeGames": len(scope_ids),
        "measuredGames": len(measured),
        "boardTemplates": len(tpl),
        "glossaryTerms": len(gl),
        "glossaryAttested": sum(1 for t in gl if t.get("attestedCount")),
        "bibliographyEntries": len(bib),
        "bibliographyPageVerified": sum(1 for b in bib
                                        if b.get("pageVerifiedCount")),
        "cultures": len((idx.get("byCulture") or {}).get("buckets") or {}),
        "inventedTraditions": len(inv_tr),
    }
    return (1 if rep.errors else 0), rep


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    print("=" * 74)
    print("  ARKA MADDE VE ÜÇ İNDEKS KAPISI")
    print("=" * 74)
    rc, rep = run(root, args)
    print()
    if rc:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
    elif rep.checks:
        print("  ✅ %d denetim yeşil · %s katmanı"
              % (rep.checks, rep.facts.get("layer", "?")))
    print("=" * 74)

    if args.json:
        p = os.path.join(root, args.json)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump({"status": "fail" if rc else "pass",
                       "checks": rep.checks, "errors": rep.errors,
                       **rep.facts}, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
