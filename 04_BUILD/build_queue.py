#!/usr/bin/env python3
"""
ÜRETİM KUYRUĞU — The Great Book of World Games
================================================================================
Faz 4 kuyruğunu ÜRETİR ve ERİŞİLEBİLİR-ÖNCE sırasını DENETLER.

  Kurucu talimatı § 4:  ERİŞİLEBİLİR OYUNLAR ÖNCE · ENGELLİ OYUNLAR EN SONA.

Beş öncelik seviyesi vardır ve bunlar bir tercih değil bir TÜRETMEDİR:

  P1  erişilebilir + yeterince doğrulanmış + kuralı tam
  P2  erişilebilir + Faz 4 içinde gerçekçi olarak tamamlanabilir doğrulama
  P3  yeniden kurgulanmış ama YETERİNCE BELGELİ (reconstructionPlan var)
  P4  kaynak erişimi bekliyor / telif engelli   ← DENENDİ ve ERİŞİLEMEDİ
  P5  çözülmemiş kural kimliği / kaynak uyuşmazlığı
  P6  kaynak ARANDI ve KAYIT BULUNAMADI          ← FAZ 5'te eklendi

⚠ EN ÖNEMLİ AYRIM (§ 5):  "denenmedi" ≠ "engellendi".

⚠ FAZ 5'İN EKLEDİĞİ İKİNCİ AYRIM:  "engellendi" ≠ "kaydı yok".

P4 bir ERİŞİM engelidir: kayıt VARDIR, nüshası kapalıdır ve kurucunun bir
kütüphane kartı onu açar. P6 bir VARLIK sorunudur: denetlenebilir bir kayıt
henüz bulunamamıştır ve hiçbir erişim izni onu var etmez.

İkisini aynı kovaya atmak, Faz 3'ün "denenmedi = engelli" hatasının aynısı
olurdu — yalnızca bir seviye daha derinde. K23 kapsam değişikliğiyle gelen
iki oyun (lagori · kho-kho) tam olarak buradadır: kaynakları ARANDI,
bulunamadı, ve ikisi de zayıf kanıtla YAZILAMAZ (§13).

Bir oyun P4'e YALNIZCA `source_access_pending.json` içinde, yani gerçekten
denenip erişilememişse girer. Henüz sıraya gelmemiş bir oyun bir ENGEL değil
bir SIRA meselesidir ve P2/P3'te durur. Bu ayrım Faz 3'te bir düzeltmeydi:
kuyruğun ilk sürümü 80 oyunu "kaynak bekliyor" gösteriyordu, gerçek sayı
dörttü. Bir engeli abartmak onu küçümsemek kadar yanlıştır.

--check ne yapar: kuyruğun SIRASI erişilebilir-önce mi. Engelli bir oyun
erişilebilir bir oyunun ÖNÜNE geçmişse kapı ısırır. Manuscript depoda
olmadığı için üretim yerelde, denetim CI'da koşar.

Çıkış kodları:  0 = temiz   1 = kusur   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

# Öncelik seviyeleri — açıklamaları kuyruğa da yazılır, kod okuyan tek yer
# burası olmasın diye.
PRIORITY_MEANING = {
    1: "erişilebilir · yeterince doğrulanmış · kuralı tam",
    2: "erişilebilir · doğrulama Faz 4 içinde tamamlanabilir",
    3: "yeniden kurgulanmış · reconstructionPlan belgeli",
    4: "kaynak DENENDİ ve erişilemedi — telif / ödünç kısıtı",
    5: "çözülmemiş kural kimliği ya da kaynak uyuşmazlığı",
    6: "kaynak ARANDI · denetlenebilir KAYIT BULUNAMADI",
}
ACCESSIBLE = (1, 2, 3)
# P6 en sondadır ve bu bir sıralama tercihi değil bir türetmedir: P4'ün
# kaydı vardır ve bir kütüphane kartı onu açar; P6'nın kaydı henüz yoktur.
DEFERRED = (4, 5, 6)


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dump(path: str, payload) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")



def librarian_ids(root: str) -> set:
    """Kütüphaneci teslimindeki oyun kimlikleri.

    ⚠ İKİ KATMAN. Tam kayıt (`01_SOURCE/rules/librarian_delivery.json`)
    KORUMALIDIR ve CI'da YOKTUR — kural metni taşır. Public özet
    (`06_REPORTS/librarian-ingest.json`) yalnızca SAYI ve KİMLİK taşır ve
    takip edilir. Kapı önce korumalı kaydı dener, yoksa public özete düşer.

    Bu ayrım olmadan kapı CI'da beş oyunu "dayanaksız" sayıyordu: dosya
    orada yoktu, yani kanıt yok sanıldı. Kimlik listesi güvenli
    metadatadır; kural metni değildir.
    """
    p = os.path.join(root, "01_SOURCE", "rules", "librarian_delivery.json")
    if os.path.exists(p):
        return {r["gameId"] for r in load(p).get("records", [])}
    p = os.path.join(root, "06_REPORTS", "librarian-ingest.json")
    if os.path.exists(p):
        return set(load(p).get("games", []))
    return set()

def diagram_complexity(entry: dict, inv: dict) -> str:
    """Diyagram yükü — 150 mm bütçesini kimin zorlayacağının ön kestirimi.

    Bu bir TAHMİNDİR ve bütçe denetimi DEĞİLDİR: bütçe yalnızca render
    edilmiş çıktıdan ölçülür (K19). Burada yalnızca kuyruk sıralamasına
    yardım eder."""
    needs = set(inv.get("visualNeeds") or [])
    n = len(needs)
    if "move-diagram" in needs and "setup-illustration" in needs and n >= 4:
        return "high"
    if n >= 3:
        return "medium"
    return "low"


def page_weight(entry: dict, inv: dict) -> float:
    """Beklenen sayfa ağırlığı — ölçülen modelden türetilir, uydurulmaz.

    Faz 3 ölçümü: metin oyun başına ~1,18 sayfa ve oyunlar arası farkı
    küçük; değişken olan diyagramdır (0,17 – 0,78). Kestirim bu iki
    bileşenin toplamıdır."""
    base = 1.18
    return round(base + {"high": 0.62, "medium": 0.34, "low": 0.22}[
        diagram_complexity(entry, inv)], 2)


def classify(entry: dict, inv: dict, verified: int, blocked_ids: set,
             unresolved: dict, gap_ids: set) -> tuple:
    """(priority, reason, blocker) — sıralamanın TEK karar noktası."""
    gid = entry["gameId"]

    if gid in unresolved:
        return 5, unresolved[gid], "kural kimliği çözülmedi"
    if gid in blocked_ids:
        return 4, "kaynak DENENDİ ve erişilemedi", "kaynak erişimi"
    # P6, doğrulanmış künyesi olmadığı SÜRECE geçerlidir: kayıt bulunursa
    # oyun kendiliğinden normal hatta döner ve bu satır susar.
    if gid in gap_ids and verified == 0:
        return 6, "kaynak ARANDI · denetlenebilir kayıt bulunamadı", \
            "kaynak kaydı yok"

    reconstructed = bool(entry.get("reconstructed")) or \
        inv.get("sourceConfidence") == "reconstructed"
    rules_complete = entry.get("ruleCompleteness") == "complete"

    if verified >= 1 and rules_complete and not reconstructed:
        return 1, "≥1 sayfa-doğrulanmış künye · kural tam", None
    if reconstructed:
        if inv.get("reconstructionPlan"):
            return 3, "yeniden kurgulanmış · plan belgeli", None
        return 5, "yeniden kurgulanmış · reconstructionPlan YOK", \
            "beyansız yeniden kurgulama"
    if rules_complete:
        return 2, "erişilebilir · sayfa doğrulaması henüz yapılmadı", None
    return 5, "kural bütünlüğü tam değil", "eksik kural"


def build(root: str, args) -> int:
    scope = load(os.path.join(root, "01_SOURCE", "scope_lock.json"))
    index = load(os.path.join(root, "01_SOURCE", "game_index.json"))
    sv = load(os.path.join(root, "01_SOURCE", "source_verification.json"))
    pending_path = os.path.join(root, "01_SOURCE", "source_access_pending.json")
    pending = load(pending_path)

    inv = {g["gameId"]: g for g in index["games"]}
    blocked_ids = {g["gameId"] for g in pending["games"]}
    unresolved = {u["gameId"]: u.get("reason", "kural kimliği çözülmedi")
                  for u in pending.get("unresolvedIdentity", [])}
    # P6 artık yalnızca K23 terfilerine özgü değildir: kaynağı ARANIP
    # bulunamayan HER oyun buraya girer (kurucu · batch 4 direktifi).
    gap_ids = {g["gameId"] for g in pending.get("amendmentSourceGaps", [])} | \
        {g["gameId"] for g in pending.get("sourceRecordGaps", [])}
    holds = {h["gameId"]: h["conflict"]
             for h in pending.get("editorialHolds", [])
             if h.get("status") == "open"}

    ver, blk = {}, {}
    for r in sv["records"]:
        (ver if r["status"] == "verified" else blk)[r["gameId"]] = \
            (ver if r["status"] == "verified" else blk).get(r["gameId"], 0) + 1

    # Manuscript depoda YOKTUR. Varsa okunur, yoksa mevcut kuyruğun
    # durumu korunur — bir sayı uydurmaktansa öncekini taşımak dürüsttür.
    written = {}
    bp = os.path.join(root, "02_MANUSCRIPT", "book.json")
    if os.path.exists(bp):
        for g in load(bp)["games"]:
            written[g["gameId"]] = "draft"
    else:
        old = os.path.join(root, "01_SOURCE", "production_queue.json")
        if os.path.exists(old):
            for g in load(old)["games"]:
                if g["manuscriptStatus"] != "not-started":
                    written[g["gameId"]] = g["manuscriptStatus"]

    rows = []
    for e in scope["entries"]:
        gid = e["gameId"]
        iv = inv.get(gid, {})
        v, b = ver.get(gid, 0), blk.get(gid, 0)
        pr, reason, blocker = classify(e, iv, v, blocked_ids, unresolved,
                                       gap_ids)
        status = ("verified" if v >= 2 else
                  "partially-verified" if v == 1 else
                  "access-blocked" if gid in blocked_ids else
                  "record-not-found" if gid in gap_ids else "not-attempted")
        rows.append({
            "gameId": gid,
            "title": e.get("name", gid),
            "family": e["family"],
            "culture": e["culture"],
            "priority": pr,
            "reason": reason,
            "accessibility": "accessible" if pr in ACCESSIBLE else "deferred",
            "sourceStatus": status,
            "verifiedSources": v,
            "blockedSources": b,
            "ruleStatus": e.get("ruleCompleteness", "unknown"),
            "playabilityStatus": e.get("playabilityStatus",
                                       iv.get("playabilityStatus", "unknown")),
            "reconstructionStatus": (
                "documented" if iv.get("reconstructionPlan") else
                "reconstructed-undocumented" if e.get("reconstructed") else
                "not-reconstructed"),
            "diagramComplexity": diagram_complexity(e, iv),
            "expectedPageWeight": page_weight(e, iv),
            "manuscriptStatus": written.get(gid, "not-started"),
            "blocker": blocker,
            "deferralReason": reason if pr in DEFERRED else None,
            # EDİTORYAL ASKI önceliği DEĞİŞTİRMEZ ve `blocker` DEĞİLDİR:
            # kaynak tamdır, oyun erişilebilirdir. Engel kitabın kendi
            # üretim kuralındadır. Kuyruğu bozmadan GÖRÜNÜR kalmalı, yoksa
            # bir sonraki üretici onu P1'de görüp duvara çarpar.
            "editorialHold": holds.get(gid),
        })

    rows.sort(key=lambda r: (r["priority"], -r["verifiedSources"],
                             r["family"], r["gameId"]))

    by_pri, by_status, by_family = {}, {}, {}
    for r in rows:
        by_pri[str(r["priority"])] = by_pri.get(str(r["priority"]), 0) + 1
        by_status[r["sourceStatus"]] = by_status.get(r["sourceStatus"], 0) + 1
        if r["accessibility"] == "accessible" and \
                r["manuscriptStatus"] == "not-started":
            by_family[r["family"]] = by_family.get(r["family"], 0) + 1

    payload = {
        "$comment": [
            "FAZ 4 ÜRETİM KUYRUĞU — ÜRETİLMİŞ DOSYA (04_BUILD/build_queue.py).",
            "",
            "Sıra kuralı (kurucu § 4): ERİŞİLEBİLİR ÖNCE, ENGELLİ EN SONA.",
            "Engelli bir oyun erişilebilir bir oyunun önüne geçemez ve bunu",
            "denetleyen `--check` kapısı CI'da koşar.",
            "",
            "P4 = DENENDİ ve ERİŞİLEMEDİ. Henüz denenmemiş bir oyun P4'e",
            "GİRMEZ; o bir engel değil bir sıra meselesidir ve P2/P3'te durur.",
            "Bu ayrım Faz 3'ün düzeltmesidir ve korunur.",
            "",
            "`expectedPageWeight` bir KESTİRİMDİR, bir bütçe denetimi değil.",
            "150 mm bütçesi yalnızca RENDER edilmiş çıktıdan ölçülür (K19).",
            "",
            "FAZ 5: P6 eklendi — 'kaynak ARANDI, KAYIT BULUNAMADI'. P4'ten",
            "ayrıdır: P4'ün kaydı vardır ve erişim izni onu açar; P6'nın",
            "kaydı henüz yoktur ve hiçbir izin onu var etmez. K23 kapsam",
            "değişikliğiyle gelen iki oyun buradadır.",
        ],
        "generatedAtPhase": "phase5",
        "priorityMeaning": {str(k): v for k, v in PRIORITY_MEANING.items()},
        "orderingRule": "priority ASC → verifiedSources DESC → family → gameId",
        "total": len(rows),
        "byPriority": by_pri,
        "bySourceStatus": by_status,
        "accessibleNotYetWrittenByFamily": by_family,
        "games": rows,
    }
    out = os.path.join(root, "01_SOURCE", "production_queue.json")
    dump(out, payload)
    print("  ✓ kuyruk üretildi · %d oyun" % len(rows))
    for k in sorted(by_pri):
        print("      P%s  %3d   %s" % (k, by_pri[k], PRIORITY_MEANING[int(k)]))
    print("  · erişilebilir ve HENÜZ YAZILMAMIŞ: %d"
          % sum(by_family.values()))
    return 0


def check(root: str, args) -> int:
    """Sıra denetimi — engelli oyun erişilebilirin önüne geçmiş mi."""
    p = os.path.join(root, "01_SOURCE", "production_queue.json")
    q = load(p)
    errs = []
    rows = q["games"]

    if len(rows) != 100:
        errs.append("kuyruk 100 oyun taşımıyor (%d)" % len(rows))
    if len({r["gameId"] for r in rows}) != len(rows):
        errs.append("kuyrukta yinelenen oyun var")

    # ① ERİŞİLEBİLİR-ÖNCE: ertelenmiş bir oyundan SONRA erişilebilir bir
    #    oyun gelemez.
    first_deferred = next((i for i, r in enumerate(rows)
                           if r["priority"] in DEFERRED), None)
    if first_deferred is not None:
        late = [r["gameId"] for r in rows[first_deferred:]
                if r["priority"] in ACCESSIBLE]
        if late:
            errs.append("ENGELLİ oyun erişilebilirin ÖNÜNE geçmiş: %s"
                        % ", ".join(late[:5]))

    # ② öncelik monotonluğu
    for a, b in zip(rows, rows[1:]):
        if b["priority"] < a["priority"]:
            errs.append("öncelik sırası bozuk: %s(P%d) → %s(P%d)"
                        % (a["gameId"], a["priority"],
                           b["gameId"], b["priority"]))
            break

    # ③ P4 YALNIZCA gerçekten denenip erişilemeyenlerdir
    pending = load(os.path.join(root, "01_SOURCE",
                                "source_access_pending.json"))
    blocked_ids = {g["gameId"] for g in pending["games"]}
    wrong = [r["gameId"] for r in rows
             if r["priority"] == 4 and r["gameId"] not in blocked_ids]
    if wrong:
        errs.append("P4'te DENENMEMİŞ oyun var (engel abartılmış): %s"
                    % ", ".join(wrong[:5]))
    missing = [g for g in blocked_ids
               if not any(r["gameId"] == g and r["priority"] == 4
                          for r in rows)]
    if missing:
        errs.append("engelli oyun P4'te değil: %s" % ", ".join(missing[:5]))

    # ④ erişilebilir sayılan bir oyun blocker taşıyamaz
    contradiction = [r["gameId"] for r in rows
                     if r["accessibility"] == "accessible" and r["blocker"]]
    if contradiction:
        errs.append("erişilebilir ama blocker taşıyor: %s"
                    % ", ".join(contradiction[:5]))

    # ⑤ yazılmış bir oyun DAYANAKSIZ olamaz.
    #
    # FAZ 5 · K28 GENİŞLETMESİ. Kapı eskiden tek bir dayanak tanıyordu:
    # `source_verification.json` içinde `verified` bir kayıt. Kurucunun
    # kütüphaneci teslimi ÜÇÜNCÜ bir dayanak getirdi ve o kayıtlar bilerek
    # `verified` DEĞİLDİR — künyeleri eksiktir ve öyle olduklarını
    # söylerler. Onları `verified` saymak, kurucunun § 24 talimatının tam
    # tersi olurdu: "kurucu özetini bağımsız doğrulanmış kaynağa
    # YÜKSELTME".
    #
    # Bu yüzden kapı ikisini AYRI AYRI tanır ve ikisini de kabul eder;
    # ama dayanağı OLMAYAN bir yazılmış oyunu hâlâ reddeder.
    lib = librarian_ids(root)
    ghost = [r["gameId"] for r in rows
             if r["manuscriptStatus"] != "not-started"
             and r["verifiedSources"] == 0
             and r["gameId"] not in lib]
    if ghost:
        errs.append("DAYANAKSIZ yazılmış oyun (ne doğrulanmış künye ne "
                    "kütüphaneci kaydı): %s" % ", ".join(ghost[:5]))

    # ⑥ P6 — FAZ 5. Üç yönlü denetim, çünkü bu seviye üç farklı yalanı
    #    mümkün kılar: kaydı olmayan bir oyunu ERİŞİLEBİLİR göstermek,
    #    kaydı olan bir oyunu P6'ya sürgün etmek, ve P6'daki bir oyunu
    #    yine de YAZMAK.
    gaps = {g["gameId"] for g in pending.get("amendmentSourceGaps", [])} | \
        {g["gameId"] for g in pending.get("sourceRecordGaps", [])}
    p6 = {r["gameId"] for r in rows if r["priority"] == 6}
    stray = sorted(p6 - gaps)
    if stray:
        errs.append("P6'da KAYIT BOŞLUĞU BELGELENMEMİŞ oyun var: %s"
                    % ", ".join(stray[:5]))
    hidden = sorted(g for g in gaps
                    if not any(r["gameId"] == g and
                               (r["priority"] == 6 or r["verifiedSources"] > 0)
                               for r in rows))
    if hidden:
        errs.append("kaynak kaydı bulunamayan oyun P6'da DEĞİL "
                    "(boşluk gizlenmiş): %s" % ", ".join(hidden[:5]))
    written_gap = [r["gameId"] for r in rows
                   if r["priority"] == 6
                   and r["manuscriptStatus"] != "not-started"
                   and r["gameId"] not in lib]
    if written_gap:
        errs.append("KAYNAKSIZ oyun YAZILMIŞ (§13 ihlali): %s"
                    % ", ".join(written_gap[:5]))

    # ⑦ EDİTORYAL ASKI — FAZ 5. Askı bir gerekçedir, bir etiket değil.
    documented = {h["gameId"] for h in pending.get("editorialHolds", [])}
    undoc = [r["gameId"] for r in rows
             if r.get("editorialHold") and r["gameId"] not in documented]
    if undoc:
        errs.append("BELGELENMEMİŞ editoryal askı: %s" % ", ".join(undoc[:5]))
    held_written = [r["gameId"] for r in rows
                    if r.get("editorialHold")
                    and r["manuscriptStatus"] != "not-started"]
    if held_written:
        errs.append("EDİTORYAL ASKIDAKİ oyun yazılmış: %s"
                    % ", ".join(held_written[:5]))

    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        return 1
    acc = sum(1 for r in rows if r["priority"] in ACCESSIBLE)
    print("  ✓ kuyruk erişilebilir-önce sıralı · %d erişilebilir · %d ertelenmiş"
          % (acc, len(rows) - acc))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    print("=" * 74)
    print("  ÜRETİM KUYRUĞU%s" % (" (--check)" if args.check else ""))
    print("=" * 74)
    rc = check(root, args) if args.check else build(root, args)
    print("=" * 74)
    return rc


if __name__ == "__main__":
    sys.exit(main())
