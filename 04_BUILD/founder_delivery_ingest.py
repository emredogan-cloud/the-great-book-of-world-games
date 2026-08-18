#!/usr/bin/env python3
"""
KURUCU TESLİM ALIMI — The Great Book of World Games
================================================================================
Kurucu direktifi § 17'nin hattı:

  KURUCU KAYNAĞI → ALIM → HASH → AYRIŞTIR → ÇIKAR → OYUN EŞLE →
  KANIT DENETLE → KAYIT GÜNCELLE → KAYNAK DURUMU İŞARETLE → KUYRUĞA AL →
  YAZ → DİYAGRAM → QA → CI

Bu betik hattın İLK ALTI adımını yapar ve **orada durur**. Yazma, diyagram
ve QA adımları ajanın işidir ve teslim GERÇEKTEN geldiğinde koşarlar
(§ 17: "kurucu malzemeyi teslim edene kadar sonraki aşamaları çalıştırma").

⚠ BU BETİĞİN YAPAMAYACAĞI ŞEY — ve bunu SÖYLEMESİ onun asıl işidir:
   Bir PDF'in içinde kural olup olmadığına makine karar VEREMEZ. Betik
   MEKANİK doğrulama yapar (dosya var mı · hash · künye alanları · kayıt
   eşleşmesi) ve geri kalanı `awaiting-agent-extraction` diye işaretler.
   Bir taramayı görüp "kural tam" demek, sayfayı OKUMADAN künye yazmakla
   aynı hatadır — proje bu hatayı Faz 2'de bir kez ölçtü ve K17'yi doğurdu.

⚠ SAYFA NUMARASI UYDURULMAZ. `bibliography.md` sayfa vermiyorsa kayıt
   `bibliographyStatus: incomplete` taşır ve oyun `locked` OLAMAZ.
   Doğrulayıcıyı yeşile boyamak için künye uydurmak, kitabın tek
   denetlenebilir iddiasını yıkar.

Kullanım:
  ./04_BUILD/founder_delivery_ingest.py              teslimi al ve raporla
  ./04_BUILD/founder_delivery_ingest.py --check      CI kapısı (teslim yoksa BOŞ KOŞAR)
  ./04_BUILD/founder_delivery_ingest.py --scaffold 10  ilk 10 öncelik için klasör aç
  ./04_BUILD/founder_delivery_ingest.py --scaffold-game oware

Çıkış kodları:  0 = alındı / teslim yok   1 = teslim KUSURLU
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

DELIVERY_DIR = "06_FOUNDER_DELIVERY"
REGISTER = os.path.join("01_SOURCE", "founder_research_gap_register.json")
PUBLIC_REPORT = os.path.join("06_REPORTS", "founder-delivery-ingest.json")

# Künye alanları — `bibliography.md` içinde aranır. Türkçe ve İngilizce
# etiketlerin ikisi de kabul edilir: kurucu hangi dilde yazarsa yazsın
# teslim reddedilmez. Reddedilirse kurucu ikinci kez yazmak zorunda kalır
# ve bu, alım hattının kendisini bir engele çevirir.
BIB_FIELDS = {
    "author":  [r"^\s*(?:author|yazar)\s*[:：]", ],
    "title":   [r"^\s*(?:title|başlık|baslik|eser)\s*[:：]", ],
    "edition": [r"^\s*(?:edition|baskı|baski)\s*[:：]", ],
    "year":    [r"^\s*(?:year|publication year|yıl|yil|tarih)\s*[:：]", ],
    "pages":   [r"^\s*(?:pages?|sayfa|ss?\.)\s*[:：]", ],
    "locator": [r"^\s*(?:locator|url|link|adres|erişim|erisim)\s*[:：]", ],
}
SOURCE_EXT = (".pdf", ".txt", ".md", ".png", ".jpg", ".jpeg", ".tif", ".tiff",
              ".webp", ".html", ".epub", ".djvu")


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def parse_bibliography(path):
    """Künye alanlarını AYRIŞTIRIR — uydurmaz, yalnızca bulur."""
    found, missing = {}, []
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return {}, list(BIB_FIELDS)
    for field, pats in BIB_FIELDS.items():
        val = None
        for ln in lines:
            for pat in pats:
                if re.search(pat, ln, flags=re.IGNORECASE):
                    val = ln.split(":", 1)[-1].strip() or None
                    break
            if val:
                break
        if val:
            found[field] = val
        else:
            missing.append(field)
    return found, missing


REQUEST_TEMPLATE = """# TESLİM İSTEĞİ — {title} (`{gid}`)

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/founder_delivery_ingest.py --scaffold -->

| | |
|---|---|
| **oyun** | {title} |
| **kültür** | {culture} · {region} |
| **aile** | {family} |
| **öncelik** | {pri} · bileşik puan {score} |
| **engel** | `{blocker}` — {blocker_name} |
| **durum** | `{status}` |

## NEDEN YAZILAMIYOR

{why}

## ZATEN DENETLENDİ — BUNLARI TEKRAR ARAMAYIN

{checked}

## ARANACAK

{find}

## ASGARİ KABUL EDİLEBİLİR KANIT

```
{evidence}
```

## İDEAL KANIT

{ideal}

## ARAMA KALIPLARI

*Bunlar birer stratejidir; bu adreslerin var olduğu iddia edilmez.*

{patterns}

## BU KLASÖRE NE KOYULUR

```
{gid}/
    source.pdf          tarama · PDF · ekran görüntüsü        (opsiyonel)
    source.md           metin ya da kural özeti               (opsiyonel)
    bibliography.md     ZORUNLU — aşağıdaki şablon            (zorunlu)
    notes.md            ne bulundu · ne bulunamadı            (opsiyonel)
```

`bibliography.md` şablonu — **sayfa yoksa boş bırakın, UYDURMAYIN**:

```
author  :
title   :
edition :
year    :
pages   :
locator :
```
"""


def scaffold(root, rows, only=None, top=0):
    made = []
    sel = [r for r in rows if r["gameId"] == only] if only else rows[:top]
    if only and not sel:
        print("  ✗ kayıtta böyle bir oyun yok: %s" % only)
        return None
    for r in sel:
        d = os.path.join(root, DELIVERY_DIR, r["gameId"])
        os.makedirs(d, exist_ok=True)
        ev = []
        for label, key in (("RULE EVIDENCE", "rule"), ("SOURCE EVIDENCE", "source"),
                           ("CULTURAL EVIDENCE", "cultural"),
                           ("RECONSTRUCTION EVIDENCE", "reconstruction")):
            items = r["minimumEvidence"].get(key) or []
            if items:
                ev.append(label)
                ev.append("  " + "  ".join("[ ] %s" % i for i in items))
        body = REQUEST_TEMPLATE.format(
            gid=r["gameId"], title=r["title"], culture=r["culture"],
            region=r["region"], family=r["family"], pri=r["priorityClass"],
            score=r["compositeScore"], blocker=r["primaryBlocker"],
            blocker_name=r["primaryBlockerName"], status=r["status"],
            why=r["whyAgentCannotWrite"],
            checked="\n".join("- %s" % c for c in r["alreadyChecked"]),
            find="\n".join("%d. %s" % (i, f) for i, f in enumerate(r["founderMustFind"], 1)),
            evidence="\n".join(ev), ideal=r["idealEvidence"],
            patterns="\n".join("- `%s`" % p for p in r["searchPatterns"]) or "—")
        p = os.path.join(d, "REQUEST.md")
        old = None
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                old = fh.read()
        if old != body:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(body)
        made.append(r["gameId"])
    return made


def ingest_game(root, gid, reg_by_id):
    """Tek bir teslim klasörünü ALIR — ve neyi ALAMADIĞINI söyler."""
    d = os.path.join(root, DELIVERY_DIR, gid)
    rec = dict(gameId=gid, files=[], bytes=0, sourceFiles=0,
               bibliography={}, bibliographyMissing=[], errors=[], warnings=[])

    entry = reg_by_id.get(gid)
    if entry is None:
        rec["errors"].append(
            "kayıtta böyle bir oyun YOK — gameId yanlış ya da oyun zaten yazılmış")
        rec["state"] = "error"
        return rec
    rec.update(title=entry["title"], family=entry["family"],
               culture=entry["culture"], primaryBlocker=entry["primaryBlocker"],
               priorityClass=entry["priorityClass"])

    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        if not os.path.isfile(p) or name.startswith("."):
            continue
        size = os.path.getsize(p)
        rec["files"].append(dict(name=name, bytes=size, sha256=sha256(p)))
        rec["bytes"] += size
        if name.lower().endswith(SOURCE_EXT) and name not in ("REQUEST.md", "bibliography.md", "notes.md"):
            rec["sourceFiles"] += 1

    # İSKELE ≠ TESLİM. `--scaffold` bir klasör açar ve içine YALNIZCA
    # REQUEST.md koyar. O klasörü "künyesi eksik teslim" saymak, kurucuya
    # kendi yaratmadığı bir kusur bildirmek olurdu: dosya hiç gelmemiştir.
    payload = [f for f in rec["files"] if f["name"] != "REQUEST.md"]
    if not payload:
        rec["warnings"].append("henüz teslim yok — klasör açık, bekliyor")
        rec["state"] = "awaiting-delivery"
        return rec

    bib = os.path.join(d, "bibliography.md")
    if os.path.exists(bib):
        found, missing = parse_bibliography(bib)
        rec["bibliography"] = found
        rec["bibliographyMissing"] = missing
    else:
        rec["bibliographyMissing"] = list(BIB_FIELDS)
        rec["errors"].append("bibliography.md YOK — künyesiz teslim alınamaz")

    if not rec["sourceFiles"]:
        rec["warnings"].append(
            "kaynak dosyası yok (yalnızca künye/not) — kural metni ajanın "
            "okuyabileceği bir biçimde gelmeli")

    # ⚠ EN ÖNEMLİ DENETİM — künye ile iddia çelişemez.
    has_pages = bool(rec["bibliography"].get("pages"))
    rec["bibliographyStatus"] = "complete" if not rec["bibliographyMissing"] else "incomplete"
    rec["founderSupplied"] = True
    rec["independentVerification"] = False   # kurucu teslimi bağımsız doğrulama DEĞİLDİR
    rec["canBeLocked"] = has_pages and rec["bibliographyStatus"] == "complete"
    if not has_pages:
        rec["warnings"].append(
            "SAYFA YOK → `bibliographyStatus: incomplete` · oyun YAZILABİLİR "
            "ama `locked` OLAMAZ (§ K17). Bu bir kusur değil bir ÖLÇÜMDÜR.")

    rec["requiredEvidence"] = entry["minimumEvidence"]
    rec["state"] = "error" if rec["errors"] else "awaiting-agent-extraction"
    rec["nextAction"] = (
        "ajan kaynağı OKUR → kanıt listesini tek tek işaretler → "
        "source_verification.json kaydı açar → engel çözülür → üretim kuyruğu"
        if rec["state"] == "awaiting-agent-extraction" else "kusuru giderin")
    return rec


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true",
                    help="CI kapısı — teslim yoksa BOŞ KOŞAR ve 0 döner")
    ap.add_argument("--scaffold", type=int, default=0, metavar="N",
                    help="en yüksek öncelikli N oyun için klasör + REQUEST.md aç")
    ap.add_argument("--scaffold-game", default=None, metavar="GAME_ID")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    print("=" * 74)
    print("  KURUCU TESLİM ALIMI%s" % (" (--check)" if args.check else ""))
    print("=" * 74)

    rp = os.path.join(root, REGISTER)
    if not os.path.exists(rp):
        print("  ✗ kayıt yok: %s" % REGISTER)
        print("    önce: ./04_BUILD/build_gap_register.py")
        print("=" * 74)
        return 1
    reg = load(rp)
    rows = reg["games"]
    reg_by_id = {r["gameId"]: r for r in rows}

    if args.scaffold or args.scaffold_game:
        made = scaffold(root, rows, only=args.scaffold_game, top=args.scaffold)
        if made is None:
            print("=" * 74)
            return 1
        print("  ✓ %d teslim klasörü hazır:" % len(made))
        for m in made:
            print("      %s/%s/REQUEST.md" % (DELIVERY_DIR, m))
        print("=" * 74)
        return 0

    ddir = os.path.join(root, DELIVERY_DIR)
    if not os.path.isdir(ddir):
        print("  · teslim dizini yok — kapı BOŞ KOŞAR")
        print("    kurucu teslim yaptığında: %s/<GAME_ID>/" % DELIVERY_DIR)
        print("=" * 74)
        return 0

    gids = sorted(x for x in os.listdir(ddir)
                  if os.path.isdir(os.path.join(ddir, x)) and not x.startswith("."))
    if not gids:
        print("  · teslim dizini boş — kapı BOŞ KOŞAR")
        print("=" * 74)
        return 0

    records = [ingest_game(root, g, reg_by_id) for g in gids]
    delivered = [r for r in records if r.get("state") == "awaiting-agent-extraction"]
    waiting = [r for r in records if r.get("state") == "awaiting-delivery"]
    bad = [r for r in records if r.get("state") == "error"]

    for r in records:
        mark = {"awaiting-agent-extraction": "✓", "awaiting-delivery": "·",
                "error": "✗"}[r["state"]]
        print("  %s %-26s %2d dosya · %7.1f KB · künye: %s"
              % (mark, r["gameId"], len(r["files"]), r["bytes"] / 1024.0,
                 r.get("bibliographyStatus", "—")))
        for e in r["errors"]:
            print("        ✗ %s" % e)
        for w in r["warnings"]:
            print("        ! %s" % w)

    pub = {
        "$comment": [
            "KURUCU TESLİM ALIMI — public yapısal özet.",
            "Kural metni BURADA DURMAZ; yalnızca hash, künye durumu ve bayraklar.",
            "Ham teslim 06_FOUNDER_DELIVERY/ altındadır ve TAKİP EDİLMEZ:",
            "telifli tarama public bir depoya konmaz (K12 ile aynı gerekçe).",
            "",
            "`awaiting-agent-extraction` bir başarısızlık DEĞİLDİR: makine bir",
            "PDF'in içinde kural olup olmadığına karar veremez. Kanıt listesini",
            "ajan SAYFAYI OKUYARAK işaretler — K17'nin kendisi budur.",
        ],
        "deliveryRoot": DELIVERY_DIR + "/",
        "gamesWithFolder": len(records),
        "delivered": len(delivered),
        "awaitingDelivery": len(waiting),
        "errors": len(bad),
        "bibliographyComplete": sum(1 for r in delivered
                                    if r.get("bibliographyStatus") == "complete"),
        "lockable": sum(1 for r in delivered if r.get("canBeLocked")),
        "independentlyVerified": 0,
        "records": [{k: v for k, v in r.items() if k != "requiredEvidence"}
                    for r in records],
    }
    dump(os.path.join(root, PUBLIC_REPORT), pub)
    if args.json:
        dump(os.path.join(root, args.json), {k: v for k, v in pub.items() if k != "records"})

    print()
    print("  klasörü olan oyun     : %d" % len(records))
    print("  TESLİM EDİLMİŞ        : %d" % len(delivered))
    print("  teslim BEKLEYEN       : %d" % len(waiting))
    print("  künyesi TAM           : %d" % pub["bibliographyComplete"])
    print("  `locked` olabilir     : %d" % pub["lockable"])
    print("  BAĞIMSIZ doğrulanmış  : 0  ← kurucu teslimi bağımsız doğrulama DEĞİLDİR")
    print()
    if bad:
        print("  ⛔ %d TESLİM KUSURLU" % len(bad))
        print("=" * 74)
        return 1
    if delivered:
        print("  ▸ SONRAKİ ADIM (ajan): kaynağı OKU → kanıt listesini işaretle →")
        print("    source_verification kaydı aç → engeli çöz → kuyruğa al →")
        print("    YAZ → DİYAGRAM → QA → CI (§ 18 · § 19: yarım bırakma yok)")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
