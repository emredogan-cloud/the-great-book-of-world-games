#!/usr/bin/env python3
"""
KAPSAM KİLİDİ KAPISI — The Great Book of World Games
================================================================================
Kurucu A3 ile nihai 100 oyunu ve Faz 2 pilotunun 12 oyununu KİLİTLEDİ.
Bu betik o kilidi korur.

  ⚠ SESSİZ DEĞİŞİM BU KAPININ TEK DÜŞMANIDIR.

Bir kapsam listesi iki biçimde sessizce bozulur ve ikisi de bir insanın
fark etmesine bırakılamaz:

  ① LİSTE değişir      — biri scope_lock.json'a dokunur, kimse görmez
  ② ENVANTER değişir   — liste aynı kalır ama altındaki kayıt kayar:
                          bir oyun `dropped` olur, kısıt taramasından
                          `restricted` çıkar, ailesi değişir. Liste hâlâ
                          o kimliği taşıdığı için hiçbir kapı ısırmaz.

② birincisinden daha tehlikelidir çünkü hiçbir dosyada bir "değişiklik"
görünmez. Bu yüzden kilit yalnızca kimlik değil, kaydın KARAR ANINDAKİ
DEĞERLERİNİ de taşır ve bu kapı ikisini karşılaştırır.

Değişiklik yasak değildir; SESSİZ değişiklik yasaktır. Bir oyun ancak
kayıtlı bir DEĞİŞİKLİK ŞERHİYLE (amendments[]) çıkarılabilir ve şerh
şunları yazmak zorundadır:
    gerekçe · çıkarılan · yerine konan · aile dengesine etkisi ·
    kültür dengesine etkisi · tarih

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
GAME_INDEX = os.path.join(ROOT, "01_SOURCE", "game_index.json")
FAMILY_INDEX = os.path.join(ROOT, "01_SOURCE", "family_index.json")

ELIGIBLE_RESTRICTION = ("open", "attributed")
ELIGIBLE_PLAYABILITY = ("rules-complete", "reconstructed")

# Kilidin her kaydında saklanan ve envanterle KARŞILAŞTIRILAN alanlar.
# Bunlardan biri kayarsa kitap sessizce başka bir kitaba dönüşmüş demektir.
PINNED = ("family", "culture", "region", "playabilityStatus",
          "restrictionStatus", "researchStatus")

# Kilitli her oyunun taşımak ZORUNDA olduğu envanter alanları.
# Gerekçe: üç indeks (kültür · oyuncu sayısı · süre-yaş) BU alanlardan
# üretilir. Alanı boş bir oyun iki indeksten sessizce kaybolur ve kitabın
# en çok kullanılan bölümü eksik basılır. Faz 1'de bu delik vardı.
REQUIRED_INDEX_FIELDS = ("players", "durationMinutes", "ageMinEstimate",
                         "materialsHint")

AMENDMENT_FIELDS = ("date", "reason", "removed", "added",
                    "familyBalanceEffect", "cultureBalanceEffect")


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


def digest(ids: list[str]) -> str:
    """Kimlik listesinin kanonik özeti. Sıra ÖNEMSİZDİR: bir oyunun yerini
    değiştirmek kitabı değiştirmez, listeden çıkarmak değiştirir."""
    return hashlib.sha256("\n".join(sorted(ids)).encode("utf-8")).hexdigest()


def eligible(g: dict) -> tuple[bool, str]:
    if g.get("status") == "dropped":
        return False, "dropped"
    if g.get("restrictionStatus") not in ELIGIBLE_RESTRICTION:
        return False, "kısıt: %s" % g.get("restrictionStatus")
    if g.get("playabilityStatus") not in ELIGIBLE_PLAYABILITY:
        return False, "oynanabilirlik: %s" % g.get("playabilityStatus")
    return True, ""


def pinned_of(g: dict) -> dict:
    return {
        "family": g.get("family"),
        "culture": g.get("culture"),
        "region": g.get("region"),
        "playabilityStatus": g.get("playabilityStatus"),
        "restrictionStatus": g.get("restrictionStatus"),
        "researchStatus": g.get("status"),
    }


# ---------------------------------------------------------------------------
# YAZMA — kilidi üretir. Kurucu kararıdır, CI'da KOŞMAZ.
# ---------------------------------------------------------------------------
def write_locks(cfg: dict, fams: dict, games: list, pilot_ids: list[str],
                amend_reason: str | None) -> int:
    sys.path.insert(0, HERE)
    import score_candidates as sc  # noqa: E402  (aynı dizinde, üçüncü taraf değil)

    chosen, _ = sc.select(games, fams["families"])
    by = {g["gameId"]: g for g in games}
    fam_order = {f["id"]: f.get("order", 99) for f in fams["families"]}
    chosen_ids = {g["gameId"] for g in chosen}
    reserve = sorted(g["gameId"] for g in games
                     if eligible(g)[0] and g["gameId"] not in chosen_ids)

    entries = []
    for g in sorted(chosen, key=lambda x: (fam_order[x["family"]],
                                           -sc.raw_score(x), x["gameId"])):
        e = {"gameId": g["gameId"], "name": g["name"]}
        e.update(pinned_of(g))
        e.update({
            "countryOrArea": g.get("countryOrArea"),
            "period": g.get("period"),
            "sourceCount": len(g.get("sources", [])),
            "sourceRefs": [s["ref"] for s in g.get("sources", [])],
            "sourceConfidence": g.get("sourceConfidence"),
            "sourceVerification": g.get("sourceVerification"),
            "ruleCompleteness": (g.get("ruleCompleteness") or {}).get("verdict"),
            "eligibility": "eligible",
            "selectionScore": sc.raw_score(g),
            "playersMax": (g.get("players") or {}).get("max"),
            "reconstructed": g.get("playabilityStatus") == "reconstructed",
        })
        entries.append(e)

    path = os.path.join(ROOT, cfg["scope"]["scopeLockFile"])
    old_amendments = []
    if os.path.exists(path):
        try:
            old = load(path)
            old_amendments = old.get("amendments", [])
            if digest([e["gameId"] for e in old.get("entries", [])]) != \
                    digest([e["gameId"] for e in entries]) and not amend_reason:
                print("⛔ Kilit ZATEN VAR ve liste değişiyor.")
                print("   Sessiz değişim yasaktır: --amend '<gerekçe>' verin.")
                return 1
        except (OSError, json.JSONDecodeError):
            pass

    payload = {
        "$comment": [
            "NİHAİ 100 OYUN — kurucu kararı A3 · KİLİTLİ.",
            "ÜRETİLMİŞ ama DONDURULMUŞ dosya: score_candidates.py modeli bir",
            "kez koşturuldu, çıktısı burada dondu ve artık her koşuda yeniden",
            "üretilmez. Model bir gün başka bir liste üretirse bu KAPI ISIRIR;",
            "liste sessizce güncellenmez. Değişiklik amendments[] ister.",
            "Denetleyen: 04_BUILD/validate_scope.py",
        ],
        "version": "1.0",
        "lockedOn": cfg["scope"].get("lockedOn"),
        "decision": "A3",
        "familyTargets": {f["id"]: f["targetGames"] for f in fams["families"]},
        "count": len(entries),
        "cultures": len({e["culture"] for e in entries}),
        "integrity": {"sha256": digest([e["gameId"] for e in entries]),
                      "algorithm": "sha256(sorted gameIds joined by \\n)"},
        "amendments": old_amendments + ([{"date": cfg["scope"].get("lockedOn"),
                                          "reason": amend_reason}]
                                        if amend_reason else []),
        "entries": entries,
        "reserve": reserve,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("  ✓ yazıldı: %s (%d oyun · %d kültür · %d yedek)"
          % (cfg["scope"]["scopeLockFile"], len(entries),
             payload["cultures"], len(reserve)))

    ppath = os.path.join(ROOT, cfg["pilot"]["lockFile"])
    pilot_entries = []
    for gid in pilot_ids:
        g = by[gid]
        pilot_entries.append({
            "gameId": gid, "name": g["name"], "family": g["family"],
            "culture": g.get("culture"),
            "reconstructed": g.get("playabilityStatus") == "reconstructed",
            "playersMax": (g.get("players") or {}).get("max"),
            "asymmetric": g["family"] == "hunt-siege",
            "batch": 1 + pilot_ids.index(gid) // 4,
        })
    ppayload = {
        "$comment": [
            "FAZ 2 PİLOTU — 12 oyun. TEK pilot kapsamıdır.",
            "Seçim ölçütü KOLAY değil ZOR oyunlardır: pilot üretim mimarisine",
            "saldırmak için vardır. Her kaydın 'whyHard' alanı, o oyunun HANGİ",
            "mimari varsayımı sınadığını yazar — bir pilot oyunun varlık sebebi",
            "budur ve gerekçesiz seçim yapılamaz.",
        ],
        "version": "1.0",
        "count": len(pilot_entries),
        "integrity": {"sha256": digest(pilot_ids)},
        "entries": pilot_entries,
    }
    if os.path.exists(ppath):
        try:
            old = load(ppath)
            byid = {e["gameId"]: e for e in old.get("entries", [])}
            for e in ppayload["entries"]:
                if e["gameId"] in byid and "whyHard" in byid[e["gameId"]]:
                    e["whyHard"] = byid[e["gameId"]]["whyHard"]
        except (OSError, json.JSONDecodeError):
            pass
    with open(ppath, "w", encoding="utf-8") as fh:
        json.dump(ppayload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("  ✓ yazıldı: %s (%d oyun)" % (cfg["pilot"]["lockFile"],
                                         len(pilot_entries)))
    return 0


# ---------------------------------------------------------------------------
# KAPI
# ---------------------------------------------------------------------------
def check_scope(cfg, fams, games, lock, rep: Report) -> None:
    print("\n── kapsam kilidi ──")
    by = {g["gameId"]: g for g in games}
    entries = lock.get("entries", [])
    ids = [e["gameId"] for e in entries]

    rep.facts["locked_games"] = len(ids)
    rep.check(len(ids) == len(set(ids)), "kilitli kimlikler tekil")
    rep.check(len(ids) == cfg["scope"]["games"],
              "kilitli oyun sayısı kapsamla eşit (%d/%d)"
              % (len(ids), cfg["scope"]["games"]))

    # ① Kilidin kendi bütünlüğü — dosyaya elle dokunulmuş mu
    want = digest(ids)
    have = (lock.get("integrity") or {}).get("sha256")
    if have != want and not lock.get("amendments"):
        rep.check(False,
                  "kilit özeti tutmuyor ve DEĞİŞİKLİK ŞERHİ YOK "
                  "(beklenen %s… · bulunan %s…)" % (want[:12], str(have)[:12]))
    else:
        rep.check(have == want or bool(lock.get("amendments")),
                  "kilit bütünlüğü doğrulandı")

    # ② Envanter kayması — kilit değil, ALTINDAKİ kayıt değişmiş olabilir
    missing = [i for i in ids if i not in by]
    rep.check(not missing,
              "her kilitli oyun envanterde var" +
              ("" if not missing else " — KAYIP: %s" % missing[:5]))

    drifted, ineligible, thin = [], [], []
    for e in entries:
        g = by.get(e["gameId"])
        if g is None:
            continue
        now = pinned_of(g)
        for k in PINNED:
            if e.get(k) != now.get(k):
                drifted.append("%s.%s: '%s' → '%s'"
                               % (e["gameId"], k, e.get(k), now.get(k)))
        ok, why = eligible(g)
        if not ok:
            ineligible.append("%s (%s)" % (e["gameId"], why))
        gaps = [f for f in REQUIRED_INDEX_FIELDS if not g.get(f)]
        if gaps:
            thin.append("%s → %s" % (e["gameId"], ",".join(gaps)))

    rep.check(not drifted,
              "kilitli kayıtlar karar anındaki değerlerini koruyor" +
              ("" if not drifted else " — SESSİZ KAYMA: %s" % drifted[:5]))
    rep.check(not ineligible,
              "kilitli oyunların hepsi hâlâ uygun" +
              ("" if not ineligible else " — UYGUNLUĞUNU KAYBETTİ: %s"
               % ineligible[:5]))
    rep.check(not thin,
              "kilitli her oyun üç indeksi besleyen alanları taşıyor" +
              ("" if not thin else " — EKSİK: %s" % thin[:5]))

    # ③ Aile dengesi — A2 kararı
    targets = {f["id"]: f["targetGames"] for f in fams["families"]}
    counts: dict = {}
    for e in entries:
        counts[e["family"]] = counts.get(e["family"], 0) + 1
    bad = ["%s %d≠%d" % (fid, counts.get(fid, 0), t)
           for fid, t in sorted(targets.items()) if counts.get(fid, 0) != t]
    rep.facts["familyCounts"] = counts
    rep.check(not bad,
              "aile dağılımı A2 hedefleriyle birebir" +
              ("" if not bad else " — SAPMA: %s" % bad))
    rep.check(sum(targets.values()) == cfg["scope"]["games"],
              "aile hedefleri toplamı %d" % cfg["scope"]["games"])

    # ④ Kültürel kısıt — restricted/excluded kitaba GİREMEZ
    forbidden = [g["gameId"] for g in games
                 if g.get("restrictionStatus") in ("restricted", "excluded")]
    leaked = sorted(set(ids) & set(forbidden))
    rep.facts["restrictedTotal"] = len(forbidden)
    rep.check(not leaked,
              "hiçbir restricted/excluded oyun kilitte değil (%d taranan)"
              % len(forbidden) +
              ("" if not leaked else " — SIZAN: %s" % leaked))

    cultures = {e["culture"] for e in entries if e.get("culture")}
    rep.facts["locked_cultures"] = len(cultures)
    rep.check(len(cultures) >= cfg["scope"]["cultures"],
              "kilitli liste kültür vaadini tutuyor (%d ≥ %d)"
              % (len(cultures), cfg["scope"]["cultures"]))

    # ⑤ Değişiklik şerhi — eksiksiz mi
    for i, am in enumerate(lock.get("amendments", [])):
        miss = [f for f in AMENDMENT_FIELDS if not am.get(f)]
        rep.check(not miss,
                  "değişiklik şerhi #%d eksiksiz" % (i + 1) +
                  ("" if not miss else " — EKSİK ALAN: %s" % miss))


def check_pilot(cfg, games, lock, pilot, rep: Report) -> None:
    print("\n── pilot kilidi ──")
    by = {g["gameId"]: g for g in games}
    scope_ids = {e["gameId"] for e in lock.get("entries", [])}
    entries = pilot.get("entries", [])
    ids = [e["gameId"] for e in entries]
    pcfg = cfg["pilot"]

    rep.facts["pilot_games"] = len(ids)
    rep.check(len(ids) == len(set(ids)), "pilot kimlikleri tekil")
    rep.check(len(ids) == pcfg["count"],
              "pilot %d oyun taşıyor (ölçülen %d)" % (pcfg["count"], len(ids)))
    rep.check((pilot.get("integrity") or {}).get("sha256") == digest(ids),
              "pilot kilidi bütünlüğü doğrulandı")

    outside = sorted(set(ids) - scope_ids)
    rep.check(not outside,
              "pilot oyunların hepsi KİLİTLİ 100'ün içinden" +
              ("" if not outside else " — GİZLİ İKİNCİ KAPSAM: %s" % outside))

    fams_present = {by[i]["family"] for i in ids if i in by}
    all_fams = {e["family"] for e in lock.get("entries", [])}
    missing_f = sorted(all_fams - fams_present)
    if pcfg.get("requireEveryFamily"):
        rep.check(not missing_f,
                  "her aile pilotta temsil ediliyor (%d/%d)"
                  % (len(fams_present), len(all_fams)) +
                  ("" if not missing_f else " — TEMSİLSİZ: %s" % missing_f))

    recon = [i for i in ids if i in by
             and by[i].get("playabilityStatus") == "reconstructed"]
    rep.check(len(recon) >= pcfg["minReconstructed"],
              "yeniden kurgulanmış oyun ≥ %d (ölçülen %d: %s)"
              % (pcfg["minReconstructed"], len(recon), ", ".join(recon)))

    boardless = [i for i in ids if i in by and by[i]["family"] == "boardless"]
    rep.check(len(boardless) >= pcfg["minBoardless"],
              "tahtasız oyun ≥ %d (ölçülen %d: %s)"
              % (pcfg["minBoardless"], len(boardless), ", ".join(boardless)))

    five = [i for i in ids if i in by
            and (by[i].get("players") or {}).get("max", 0) >= 5]
    rep.check(len(five) >= pcfg["minFivePlayer"],
              "beş+ oyunculu oyun ≥ %d (ölçülen %d: %s)"
              % (pcfg["minFivePlayer"], len(five), ", ".join(five)))

    # Asimetri TANIMDIR, etiket değil: hunt-siege ailesinin giriş kuralı
    # "tarafların KAZANMA KOŞULLARI farklıdır" der (family_index.json).
    asym = [i for i in ids if i in by and by[i]["family"] == "hunt-siege"]
    rep.check(len(asym) >= pcfg["minAsymmetric"],
              "asimetrik oyun ≥ %d (ölçülen %d: %s)"
              % (pcfg["minAsymmetric"], len(asym), ", ".join(asym)))

    # Pilot ZOR olmak zorundadır. Gerekçesiz seçim yapılamaz.
    nowhy = [e["gameId"] for e in entries if not e.get("whyHard")]
    rep.check(not nowhy,
              "her pilot oyunun 'hangi mimari varsayımı sınıyor' gerekçesi var" +
              ("" if not nowhy else " — GEREKÇESİZ: %s" % nowhy))

    batches: dict = {}
    for e in entries:
        batches.setdefault(e.get("batch"), []).append(e["gameId"])
    rep.check(sorted(len(v) for v in batches.values()) ==
              sorted(pcfg["batches"]),
              "batch dağılımı %s (ölçülen %s)"
              % (pcfg["batches"], sorted(len(v) for v in batches.values())))


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true",
                    help="kilidi ÜRET (kurucu kararı; CI'da koşmaz)")
    ap.add_argument("--amend", default=None, help="--write ile: değişiklik gerekçesi")
    ap.add_argument("--pilot", default=None,
                    help="--write ile: virgülle ayrılmış 12 pilot gameId")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  KAPSAM KİLİDİ (A3) VE PİLOT KİLİDİ")
    print("=" * 74)

    rep = Report(args.verbose)
    try:
        cfg, fams = load(CONFIG), load(FAMILY_INDEX)
        games = load(GAME_INDEX)["games"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        print("  ⛔ kaynak dosya okunamadı: %s" % exc)
        return 1

    if args.write:
        pilot_ids = [s.strip() for s in (args.pilot or "").split(",") if s.strip()]
        if len(pilot_ids) != cfg["pilot"]["count"]:
            print("  ⛔ --pilot tam %d kimlik ister (verilen %d)"
                  % (cfg["pilot"]["count"], len(pilot_ids)))
            return 2
        return write_locks(cfg, fams, games, pilot_ids, args.amend)

    if not cfg["scope"].get("locked"):
        rep.warn("scope.locked = false — kapsam kilidi henüz yürürlükte değil")
        print("\n" + "=" * 74)
        print("  ⊘ kapsam kilitli değil; kapı boş koştu")
        print("=" * 74)
        return 0

    lock_path = os.path.join(ROOT, cfg["scope"]["scopeLockFile"])
    pilot_path = os.path.join(ROOT, cfg["pilot"]["lockFile"])
    for p in (lock_path, pilot_path):
        if not os.path.exists(p):
            rep.check(False, "kilit dosyası yok: %s" % os.path.relpath(p, ROOT))
    if rep.errors:
        print("\n⛔ kilit dosyaları olmadan denetim yapılamaz")
        return 1

    lock, pilot = load(lock_path), load(pilot_path)
    check_scope(cfg, fams, games, lock, rep)
    check_pilot(cfg, games, lock, pilot, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · kapsam ve pilot KİLİTLİ" % rep.checks)
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
