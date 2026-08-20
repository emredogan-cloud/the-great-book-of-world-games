#!/usr/bin/env python3
"""
SATIR EDİTÖRÜ KAPISI — The Great Book of World Games
================================================================================
Kurucu § 22–23'ün mekanikleştirilebilir yarısı. **İnsan okumasının yerine
geçmez**; okumanın bulamayacağı şeyi bulur: 56 madde boyunca TUTARSIZLIK.

Bir satır editörü tek bir sayfayı iyi okur. Elli altı maddede "anticlockwise"
ile "counterclockwise"ın karıştığını, bir maddede eğri bir maddede düz
kesme işareti kullanıldığını ya da aynı cümle açılışının yirmi kez
tekrarlandığını göremez. Bu kapı tam olarak onu ölçer.

Denetimler:
  ① yazım kayması   — tek bir imla ailesi (İngiliz) her yerde mi
  ② noktalama       — çift boşluk, noktalama önü boşluk, tekrarlı kelime
  ③ tipografi       — kesme/tırnak işareti tutarlı mı, tire aileleri doğru mu
  ④ terminoloji     — aynı mekanik her yerde AYNI kelimeyle mi anılıyor
  ⑤ yasak kalıp     — STYLE.md § 4 (AI metninin tanınır kalıpları)
  ⑥ tekrar          — aynı cümle açılışı / aynı ifade kaç maddede
  ⑦ cümle uzunluğu  — anlatı ortalaması STYLE bandında mı
  ⑧ kural bütünlüğü — beş öğe + üç soru + kaynak, her maddede
  ⑨ diyagram uyumu  — efsanedeki terim maddenin metninde geçiyor mu
  ⑩ diakritik       — kültür ve başlık adları her geçtiği yerde AYNI mı

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

# ① Tek imla ailesi: İNGİLİZ. Gerekçe editoryaldir — kaynakların büyük
# çoğunluğu (Murray, Bell, Gomme, Parker, Culin'in İngiliz baskıları)
# İngiliz imlasıyla basılmıştır ve künye ile gövde arasında imla değişmesi
# okuru kaynağın alıntı olup olmadığı konusunda tereddüde düşürür.
SPELLING = [
    (r"\bcolor(s|ed|ing|ful)?\b", "colour…", "US"),
    (r"\bcenter(s|ed|ing)?\b", "centre…", "US"),
    (r"\bmeter(s)?\b", "metre(s)", "US"),
    (r"\bgray\b", "grey", "US"),
    (r"\bcounterclockwise\b", "anticlockwise", "US"),
    (r"\bpractice(s|d|ing)\b(?= )", "practise (verb)", "US-verb"),
    (r"\b(\w+)ize(s|d|r)?\b", "-ise", "US-suffix"),
    (r"\b(\w+)ization\b", "-isation", "US-suffix"),
    (r"\btowards?\b", None, "OK"),
]
SPELLING_ALLOW = {"size", "sizes", "sized", "prize", "prizes", "seize",
                  "seizes", "capsize", "maize", "bronze", "dozen"}

FORBIDDEN_PATTERNS = [
    (r"not only\b.{0,60}\bbut also\b", "STYLE § 4 — 'not only … but also'"),
    (r"\bin today'?s world\b", "STYLE § 4"),
    (r"\bdive into\b", "STYLE § 4"),
    (r"\bunlock the secrets?\b", "STYLE § 4"),
    (r"\bembark on a journey\b", "STYLE § 4"),
    (r"\bdelve into\b", "STYLE § 4 (aynı aile)"),
    (r"\bit'?s worth noting that\b", "STYLE § 4 (aynı aile)"),
    (r"\bin the realm of\b", "STYLE § 4 (aynı aile)"),
    (r"\brich tapestry\b", "STYLE § 4 (aynı aile)"),
    (r"\btestament to\b", "STYLE § 4 (aynı aile)"),
]

# ④ Aynı mekanik, aynı kelime. Sol taraf KANONİK; sağ taraf kanonikle
# çakışan eş anlamlılardır. Bir oyun kendi kültürünün kelimesini
# kullanıyorsa (nyumba, kichwa, farzin) o AYRI bir şeydir ve buraya girmez.
TERMS = [
    ("anticlockwise", ["counter-clockwise", "counterclockwise",
                       "anti-clockwise"]),
    ("clockwise", ["clock-wise"]),
    ("board", ["gameboard", "game-board"]),
    ("piece", ["playing piece", "game piece"]),
    ("row", ["line of three"]),
]

TEXT_FIELDS = ["culturalStory", "materialsAndSubstitution", "setup",
               "placement", "turnSequence", "capture", "movement",
               "legalMoves", "throwValues", "stages", "figures", "scoring",
               "stackingAndSending", "chain", "firstMove", "winCondition",
               "kingCapture", "endCondition", "exampleTurn", "firstGame",
               "aMatchIsTwoGames", "reconstructionNotice", "safetyNote",
               "gamblingReframed", "sources"]
FIVE_ELEMENTS = {
    "setup": ["setup"],
    # 'İlk hamle / tur' bir ALAN ADI değil bir BİLGİDİR: bazı oyunlarda
    # yerleştirme evresi (placement), bazılarında turun aşamaları (stages),
    # bazılarında da kurulumun son satırı ("The fox moves first.") taşır.
    # Kapı alanı değil BİLGİYİ arar.
    "first move / turn": ["firstMove", "turnSequence", "throwValues",
                          "placement", "stages"],
    "legal moves": ["movement", "capture", "legalMoves", "turnSequence",
                    "stages", "scoring", "figures", "stackingAndSending",
                    "chain", "placement"],
    "objective": ["winCondition"],
    "ending": ["endCondition"],
}


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def texts(g) -> list:
    out = []
    for k in TEXT_FIELDS:
        v = g.get(k)
        if isinstance(v, str):
            out.append((k, v))
        elif isinstance(v, list):
            for i, s in enumerate(v):
                if isinstance(s, str):
                    out.append(("%s[%d]" % (k, i + 1), s))
    for i, v in enumerate(g.get("variants") or []):
        out.append(("variants[%d].name" % (i + 1), v.get("name", "")))
        out.append(("variants[%d].note" % (i + 1), v.get("note", "")))
    for k, v in (g.get("edgeCases") or {}).items():
        out.append(("edgeCases.%s" % k, v))
    return out


def sentences(s: str) -> list:
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", s) if x.strip()]


class Rep:
    def __init__(self):
        self.n = 0
        self.fail = []
        self.notes = []

    def check(self, cond, label, detail=None):
        self.n += 1
        if cond:
            return True
        self.fail.append(label)
        print("  ✗ %s" % label)
        for d in (detail or [])[:12]:
            print("      · %s" % d)
        if detail and len(detail) > 12:
            print("      … ve %d tane daha" % (len(detail) - 12))
        return False


def run(root: str, args) -> int:
    mdir = "02_MANUSCRIPT"
    bp = os.path.join(root, mdir, "book.json")
    if not os.path.exists(bp):
        print("  · ticari manuscript bu depoda yok — satır editörü ATLANDI")
        return 0
    book = load(bp)
    games = book["games"]
    fmp = os.path.join(root, mdir, "frontmatter.json")
    fm = load(fmp) if os.path.exists(fmp) else None

    # ön madde ve aile açılışları da DENETLENİR: kitabın en çok okunan
    # sayfaları oralardır ve ilk sürümde hiç denetlenmemişlerdi.
    corpus = []
    for g in games:
        for k, v in texts(g):
            corpus.append((g["gameId"], k, v))
    if fm:
        for sec in fm["sections"]:
            for i, p in enumerate(sec.get("paragraphs", [])):
                corpus.append(("front:" + sec["id"], "p%d" % (i + 1), p))
            for i, sub in enumerate(sec.get("sections", [])):
                corpus.append(("front:" + sec["id"], "h%d" % (i + 1),
                               sub["heading"]))
                corpus.append(("front:" + sec["id"], "t%d" % (i + 1),
                               sub["text"]))
            for i, row in enumerate(sec.get("table", [])):
                corpus.append(("front:" + sec["id"], "row%d" % (i + 1),
                               row["idea"] + " " + row["test"]))
            if sec.get("closing"):
                corpus.append(("front:" + sec["id"], "closing", sec["closing"]))
        for o in fm["familyOpeners"]:
            corpus.append(("part:" + o["family"], "standfirst",
                           o["standfirst"]))
            for i, p in enumerate(o["paragraphs"]):
                corpus.append(("part:" + o["family"], "p%d" % (i + 1), p))

    rep = Rep()
    print("=" * 74)
    print("  SATIR EDİTÖRÜ KAPISI · %d madde · %d metin bloğu"
          % (len(games), len(corpus)))
    print("=" * 74)

    # ① imla
    print("\n── ① imla ailesi (İngiliz) ──")
    hits = []
    for gid, f, t in corpus:
        for pat, want, kind in SPELLING:
            if want is None:
                continue
            for m in re.finditer(pat, t):
                w = m.group(0).lower()
                if w in SPELLING_ALLOW:
                    continue
                hits.append("%s.%s → %r (İngilizcesi: %s)" % (gid, f,
                                                              m.group(0), want))
    rep.check(not hits, "tek imla ailesi (%d kayma)" % len(hits), hits)

    # ② noktalama
    print("\n── ② noktalama ──")
    punct = []
    for gid, f, t in corpus:
        if "  " in t:
            punct.append("%s.%s → çift boşluk" % (gid, f))
        if re.search(r"\s+[,.;:!?]", t):
            punct.append("%s.%s → noktalama önü boşluk" % (gid, f))
        for m in re.finditer(r"\b(\w+)\s+\1\b", t, re.I):
            # Oyun adları GERÇEKTEN tekrarlı olabilir: Mbube Mbube,
            # Rimau-rimau, Aadu Puli. Bir kapı meşru bir adı kusur sayarsa,
            # gerçek bir kusur bulduğunda da güvenilmez olur.
            if m.group(1).lower() not in ("that", "had", "sing") \
               and not m.group(0)[0].isupper():
                punct.append("%s.%s → tekrarlı kelime %r" % (gid, f,
                                                             m.group(0)))
        if re.search(r"[a-z],[A-Za-z]", t):
            punct.append("%s.%s → virgülden sonra boşluk yok" % (gid, f))
    rep.check(not punct, "noktalama temiz (%d kusur)" % len(punct), punct)

    # ③ tipografi
    print("\n── ③ tipografi ──")
    typo = []
    curly = sum(t.count("’") for _, _, t in corpus)
    straight = sum(len(re.findall(r"(?<=\w)'(?=\w)", t)) for _, _, t in corpus)
    for gid, f, t in corpus:
        if '"' in t:
            typo.append("%s.%s → düz çift tırnak" % (gid, f))
        if "--" in t:
            typo.append("%s.%s → çift tire (— olmalı)" % (gid, f))
        if re.search(r"\w\s-\s\w", t):
            typo.append("%s.%s → boşluklu kısa tire (— olmalı)" % (gid, f))
    if curly and straight:
        typo.append("kesme işareti KARIŞIK: %d eğri (’), %d düz (') — "
                    "biri seçilmeli" % (curly, straight))
    rep.check(not typo, "tipografi tutarlı (%d kusur)" % len(typo), typo)

    # ④ terminoloji
    print("\n── ④ terminoloji ──")
    term = []
    for canon, variants in TERMS:
        for v in variants:
            for gid, f, t in corpus:
                if re.search(r"\b%s\b" % re.escape(v), t, re.I):
                    term.append("%s.%s → %r (kanonik: %r)" % (gid, f, v, canon))
    rep.check(not term, "aynı mekanik aynı kelimeyle (%d kayma)" % len(term),
              term)

    # ⑤ yasak kalıp
    print("\n── ⑤ yasak kalıp (STYLE § 4) ──")
    forb = []
    for gid, f, t in corpus:
        for pat, why in FORBIDDEN_PATTERNS:
            for m in re.finditer(pat, t, re.I):
                forb.append("%s.%s → %r · %s" % (gid, f, m.group(0), why))
    rep.check(not forb, "yasak kalıp yok (%d)" % len(forb), forb)

    # ⑥ tekrar
    print("\n── ⑥ tekrar ──")
    # ⚠ KURAL METNİNDE TEKRAR BİR KUSUR DEĞİL, BİR ÖZELLİKTİR.
    # "Play ends when…" ya da "A player with no legal move…" elli altı
    # maddede aynı biçimde durmalıdır: okur kalıbı öğrenir ve maddeyi
    # taramayı bırakıp OYNAMAYA başlar. STYLE § 4'ün yasakladığı şey
    # ANLATI kaydındaki kalıptır — AI metninin tanınır işareti orada
    # ortaya çıkar. Bu yüzden tekrar taraması yalnızca anlatıyı ölçer.
    # `firstGame` bir RUBRİK alanıdır ("Play the first game with…") ve
    # kalıbı KASITLIDIR: okur onu her maddede aynı yerde arar.
    NARRATIVE = ("culturalStory", "exampleTurn", "variants",
                 "aMatchIsTwoGames")
    openers = collections.Counter()
    phrases = collections.Counter()
    where = collections.defaultdict(set)
    for gid, f, t in corpus:
        base = re.sub(r"[\[\.].*$", "", f)
        if not (base in NARRATIVE or gid.startswith(("front:", "part:"))):
            continue
        for s in sentences(t):
            w = re.findall(r"[A-Za-z']+", s)
            if len(w) >= 4:
                key = " ".join(w[:3]).lower()
                openers[key] += 1
                where["O" + key].add(gid)
            for i in range(len(w) - 4):
                key = " ".join(w[i:i + 5]).lower()
                phrases[key] += 1
                where["P" + key].add(gid)
    rep_open = sorted([(k, v, len(where["O" + k])) for k, v in openers.items()
                       if v >= 6 and len(where["O" + k]) >= 5],
                      key=lambda x: -x[1])
    rep_ph = sorted([(k, v, len(where["P" + k])) for k, v in phrases.items()
                     if v >= 4 and len(where["P" + k]) >= 4],
                    key=lambda x: -x[1])
    if rep_open:
        print("  · en sık anlatı açılışları (BİLGİ — kapı değil):")
        for k, v, g in rep_open[:6]:
            print("      %r — %d kez, %d maddede" % (k, v, g))
    detail = ["birebir ifade %r — %d kez, %d maddede" % (k, v, g)
              for k, v, g in rep_ph]
    rep.check(not detail,
              "anlatıda birebir tekrarlanan ifade yok (%d)" % len(detail),
              detail)

    # ⑦ cümle uzunluğu
    print("\n── ⑦ anlatı cümle ortalaması ──")
    cfg = load(os.path.join(root, "project_config.json"))
    lo = cfg["style"]["narrativeSentenceAvgMin"]
    hi = cfg["style"]["narrativeSentenceAvgMax"]
    # ⚠ ÖLÇÜM BANDI DEĞİŞTİRMEZ, BANDA RAPOR EDER.
    # Ölçülen ortanca 22,4; config bandı 12–19. Bant Faz 2'de bir HİPOTEZ
    # olarak yazıldı, onu denetleyecek kapı (qa_drift.py) hiç yazılmadı ve
    # elli altı madde beş fazda o bandın dışında yazıldı.
    #
    # Burada iki yanlış yol var ve ikisi de reddedildi:
    #   (a) 48 kültürel hikâyeyi bandı tutturmak için yeniden yazmak —
    #       yol haritası § 3 'Sürüklenme disiplini' bunu açıkça yasaklar:
    #       "Metriği tatmin etmek için proza yeniden yazılmaz."
    #   (b) config'teki bandı sessizce ölçüme çekmek — bu, kapıyı kapıya
    #       uydurmaktır ve `style` bloğu KURUCU onayına bağlıdır (A5).
    #
    # Üçüncü yol: ÖLÇ, RAPOR ET, aykırı değeri DÜZELT. Kapı yalnızca
    # gerçek aykırı değerde ısırır (bandın iki katı); gerisi kurucu
    # kararına (A5) bir ÖLÇÜMLE gider.
    vals = []
    for g in games:
        s = sentences(g["culturalStory"])
        if s:
            vals.append((sum(len(re.findall(r"\S+", x)) for x in s) / len(s),
                         g["gameId"]))
    vals.sort()
    med = vals[len(vals) // 2][0] if vals else 0
    outside = [v for v in vals if not (lo <= v[0] <= hi)]
    extreme = ["%s → %.1f kelime/cümle (aykırı: bandın iki katı üstü)"
               % (g, v) for v, g in vals if v > hi * 2]
    print("  · ölçülen: ortanca %.1f · en düşük %.1f (%s) · en yüksek %.1f (%s)"
          % (med, vals[0][0], vals[0][1], vals[-1][0], vals[-1][1]))
    print("  · config bandı %.1f–%.1f · dışında kalan %d/%d madde"
          % (lo, hi, len(outside), len(vals)))
    print("  ⚠ AÇIK KARAR A5: bant Faz 2 hipotezidir ve hiç denetlenmedi.")
    print("    Kurucu ya bandı ölçüme çeker ya da yeniden yazım ister;")
    print("    ajan ikisini de KENDİ BAŞINA yapmaz.")
    rep.check(not extreme, "aykırı uzunlukta kültürel hikâye yok (%d)"
              % len(extreme), extreme)

    # ⑧ kural bütünlüğü
    print("\n── ⑧ beş öğe · üç soru · kaynak ──")
    miss = []
    for g in games:
        for el, keys in FIVE_ELEMENTS.items():
            if any(g.get(k) for k in keys):
                continue
            if el == "first move / turn" and re.search(
                    r"\b(moves? first|goes first|begins|opens)\b",
                    " ".join(g.get("setup") or []) + " "
                    + (g.get("winCondition") or ""), re.I):
                continue
            miss.append("%s → '%s' öğesi YOK" % (g["gameId"], el))
        for q in ("tie", "stalemate", "illegalMove"):
            if not (g.get("edgeCases") or {}).get(q):
                miss.append("%s → üç sorudan %r cevapsız" % (g["gameId"], q))
        if not g.get("sources"):
            miss.append("%s → kaynak künyesi YOK" % g["gameId"])
        if g.get("reconstructed") and not g.get("reconstructionNotice"):
            miss.append("%s → reconstructed ama BEYAN YOK" % g["gameId"])
    rep.check(not miss, "her maddede beş öğe, üç soru ve künye (%d eksik)"
              % len(miss), miss)

    # ⑨ diyagram uyumu
    print("\n── ⑨ diyagram ↔ metin ──")
    ddir = os.path.join(root, "07_ASSETS", "diagrams")
    declared = {}
    if os.path.isdir(ddir):
        for fn in sorted(os.listdir(ddir)):
            if fn.endswith(".json") and fn != "diagram_language.json":
                for d in load(os.path.join(ddir, fn))["diagrams"]:
                    declared[d["diagramId"]] = d
    dia = []
    for g in games:
        blob = " ".join(v for _, v in texts(g)).lower()
        for did in g.get("diagrams", []):
            d = declared.get(did)
            if not d:
                dia.append("%s → %r tanımlayıcısı YOK" % (g["gameId"], did))
                continue
            if d.get("gameId") != g["gameId"]:
                dia.append("%s → %r BAŞKA oyuna ait (%s)"
                           % (g["gameId"], did, d.get("gameId")))
            for e in d.get("legend", []):
                STOP = {"player", "players", "piece", "pieces", "other",
                        "second", "shown", "taken", "board", "first",
                        "their", "there", "which", "these", "those",
                        "moves", "moved", "playing", "shows", "start",
                        "starts", "began", "close", "closes", "closing",
                        "front", "along", "round", "where", "while",
                        "near", "far", "the", "and", "its",
                        # yön kelimeleri DİYAGRAMA aittir: bir diyagramın
                        # sağı vardır, prozanın yoktur (okurlar masanın
                        # karşılıklı yanlarında oturur).
                        "left", "right", "upper", "lower", "this", "that",
                        "above", "below", "side", "sides", "end", "ends"}
                words = [w for w in re.findall(r"[a-z]{4,}",
                                               (e.get("label") or "").lower())
                         if w not in STOP]
                # tekil/çoğul katlanır: 'stones' metinde 'stone' olabilir
                def seen(w):
                    return (w in blob or w.rstrip("s") in blob
                            or (len(w) >= 5 and w[:5] in blob)
                            or (len(w) >= 4 and w[:4] in blob))
                if words and not any(seen(w) for w in words):
                    dia.append("%s → efsane %r maddenin metninde GEÇMİYOR"
                               % (g["gameId"], e.get("label")))
    rep.check(not dia, "efsane terimi metinle örtüşüyor (%d kopukluk)"
              % len(dia), dia)

    # ⑩ diakritik
    print("\n── ⑩ ad tutarlılığı ──")
    names = {}
    for g in games:
        names[g["title"]] = g["gameId"]
    diac = []
    # Katlama unicodedata ile TÜRETİLİR. Elle yazılmış bir çeviri tablosu
    # iki kez uzunluk hatası verdi; bir tabloyu elle saymak, sayılabilecek
    # bir şeyi tahmin etmektir.
    import unicodedata

    def fold(t):
        return "".join(c for c in unicodedata.normalize("NFD", t.lower())
                       if unicodedata.category(c) != "Mn")
    folded = collections.defaultdict(set)
    for t in names:
        folded[fold(t)].add(t)
    for k, v in folded.items():
        if len(v) > 1:
            diac.append("aynı ad farklı yazılmış: %s" % " / ".join(sorted(v)))
    rep.check(not diac, "başlık diakritikleri tutarlı (%d)" % len(diac), diac)


    # ⑪ BİÇİMLENDİRME VE İÇ SÖZLÜK SIZINTISI
    #
    # İkisi de basılı sayfada bulundu, hiçbir sayısal kapı görmedi:
    #   · `**Do not use the seeds…**` — markdown yıldızları OLDUĞU GİBİ
    #     basılıyordu, üstelik bir GÜVENLİK uyarısının içinde.
    #   · "ACCESS-BLOCKED", "librarian delivery", "FOUNDER-SUPPLIED" —
    #     projenin İÇ SÖZLÜĞÜ on iki maddenin künyesinde basılıyordu.
    #     Beyanın kendisi doğruydu ve KALDI; okurun anlamadığı kelimelerle
    #     yazılmış olması kusurdu.
    print("\n── ⑪ biçimlendirme ve iç sözlük ──")
    md, jar = [], []
    JARGON = (r"\b(ACCESS[- ]BLOCKED|SOURCE[- ]PENDING|page-verified|"
              r"bibliographyStatus|sourceStatus|librarian delivery|"
              r"FOUNDER-SUPPLIED|NOT INDEPENDENTLY VERIFIED|locked scope|"
              r"reserve pool|amendment K\d+|founder-supplied|the project'?s "
              r"own record)\b")
    for gid, f, t in corpus:
        for m in re.finditer(r"\*\*|__|\[[^\]]+\]\(|`", t):
            md.append("%s.%s → %r" % (gid, f, m.group(0)))
        for m in re.finditer(JARGON, t, re.I):
            jar.append("%s.%s → %r" % (gid, f, m.group(0)))
    rep.check(not md, "basılan metinde markdown işareti yok (%d)" % len(md), md)
    rep.check(not jar, "basılan metinde projenin iç sözlüğü yok (%d)"
              % len(jar), jar)

    facts = {"games": len(games), "textBlocks": len(corpus),
             "checks": rep.n, "failed": rep.fail}
    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(facts, fh, ensure_ascii=False, indent=1)

    print("\n" + "=" * 74)
    if rep.fail:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.fail), rep.n))
    else:
        print("  ✅ %d denetim yeşil · %d madde · %d metin bloğu"
              % (rep.n, len(games), len(corpus)))
        print("     ⚠ Bu kapı İNSAN OKUMASININ yerine geçmez; okumanın")
        print("       göremeyeceği TUTARSIZLIĞI ölçer.")
    print("=" * 74)
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
