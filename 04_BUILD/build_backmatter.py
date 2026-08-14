#!/usr/bin/env python3
"""
ARKA MADDE ÜRETECİ — The Great Book of World Games
================================================================================
Yol haritası Faz 4 § 3 ve `EDITORIAL_ARCHITECTURE.md § 5` altı bölüm ister:

  ① Tahta şablonları        8 s.   fotokopiye uygun, tam ölçekli
  ② Malzeme rehberi         2 s.   `substitutionHint` alanlarından
  ③ Sözlük                  3 s.   60 terim — mekanik tasnifin dili
  ④ Kaynakça                4 s.   oyun başına künye
  ⑤ ÜÇ İNDEKS               3 s.   kültür · oyuncu sayısı · süre-yaş
  ⑥ Uydurulmuş gelenekler   1 s.   kaynaksız yaygın iddiaların düzeltmesi
                          ─────
                           21 s.

  ⚠ ARKA MADDE ELLE YAZILMAZ (kurucu § 27).

Üç indeks, malzeme rehberi ve kaynakça **envanterden ÜRETİLİR**. Gerekçe
mimari belgede yazılıdır: arka madde kitabın **en çok kullanılacak** kısmıdır
ve elle tutulan bir liste, envanter değiştiğinde sessizce yalancı olur.
Ebeveyn rafta "20 dakikalık, 2 kişilik, 8 yaş" diye arar; o aramaya yanlış
cevap veren bir indeks, kitabın en çok okunan sayfasını bozar.

Zincir (kurucu § 27):  KAYNAK → ÜRETEÇ → ÇIKTI → DOĞRULAMA

  KAYNAK    01_SOURCE/scope_lock.json · game_index.json ·
            source_verification.json · 07_ASSETS/diagrams/*.json
            02_MANUSCRIPT/book.json (varsa) · dizgi ölçümü (varsa)
  ÜRETEÇ    bu betik
  ÇIKTI     02_MANUSCRIPT/backmatter.json   (korumalı · tam metin)
            06_REPORTS/backmatter.json      (public · yapısal özet)
  DOĞRULAMA 04_BUILD/qa_index.py

⚠ SAYFA NUMARASI UYDURULMAZ. Bir oyunun sayfa göndermesi ancak o oyun
GERÇEKTEN dizilip ölçüldüyse yazılır. Yazılmamış bir oyunun sayfası
`null`dır ve indeks onu "sayfa bekliyor" olarak taşır. Kurucunun § 27
şartı — *"page references must be tested against actual rendered output"* —
yalnızca böyle karşılanabilir: ölçülmemiş bir sayfa numarası, test
edilemeyen bir iddiadır.

Çıkış kodları:  0 = üretildi   1 = üretilemedi   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

# ── ③ SÖZLÜK ────────────────────────────────────────────────────────────
# Mekanik tasnifin dili. Her terim bir AİLEYE ya da kitabın geneline
# bağlıdır; `qa_index.py` bir terimin manuscript'te GERÇEKTEN geçtiğini
# iddia ediyorsa bunu denetler. Bir sözlük, kitabın kullanmadığı kelimeleri
# tanımlıyorsa okurun işine yaramaz.
GLOSSARY: list[tuple[str, str, str]] = [
    # ── ekim (sowing) ────────────────────────────────────────────────
    ("sowing", "sowing",
     "Dropping seeds one by one into consecutive pits, anticlockwise unless "
     "the game says otherwise. The defining action of the mancala family."),
    ("lap", "sowing",
     "A continued sowing: the last seed falls into an occupied pit, the "
     "player lifts that pit's whole contents and sows again in the same turn."),
    ("store", "sowing",
     "The large end pit that holds a player's captured seeds. Not every "
     "sowing game has one."),
    ("pit", "sowing",
     "A hollow holding seeds. Called a hole, cup or house in other accounts; "
     "this book uses pit throughout."),
    ("seed", "sowing",
     "The counter sown in a mancala game. Seeds are not owned by a player; "
     "they belong to the pit they sit in."),
    ("capture on four", "sowing",
     "A rule found across West Africa: a pit that reaches exactly four seeds "
     "is taken, sometimes by its owner rather than the sower."),
    ("starved", "sowing",
     "A player with no seeds to sow. Most sowing games require the opponent "
     "to feed a starved side if a legal feeding move exists."),
    # ── av-kuşatma (hunt-siege) ──────────────────────────────────────
    ("asymmetric", "hunt-siege",
     "A game whose two sides have different powers and different winning "
     "conditions. One hunts, the other surrounds."),
    ("hunt game", "hunt-siege",
     "A board game with one or a few strong pieces against many weak ones, "
     "the strong side capturing by leaping and the weak side by blocking."),
    ("blockade", "hunt-siege",
     "Winning by leaving the opponent no legal move rather than by taking "
     "pieces. The usual victory condition for the weak side of a hunt game."),
    ("leap capture", "hunt-siege",
     "Taking an adjacent piece by jumping over it into the empty point "
     "directly beyond."),
    ("tafl", "hunt-siege",
     "The Norse family of siege games in which a king starts at the centre "
     "and tries to reach the edge while attackers surround him."),
    # ── eve dönüş (race) ─────────────────────────────────────────────
    ("race game", "race",
     "A game whose pieces travel a fixed track and whose object is to finish "
     "the circuit first. Movement is set by a chance device."),
    ("stave dice", "race",
     "Flat sticks thrown as dice, scoring by how many land flat side up. "
     "The commonest randomiser outside the cubic-die world."),
    ("throw value", "race",
     "The distance a throw is worth. In stave games this is rarely the count "
     "of flat faces; the mapping is part of the rules."),
    ("track", "race",
     "The path pieces follow. It may be a circuit, a spiral or a there-and-"
     "back line."),
    ("safe point", "race",
     "A marked point on the track where a piece cannot be sent home."),
    ("sent home", "race",
     "Returned to the start after being landed on by an enemy piece."),
    ("bearing off", "race",
     "Removing a piece from the board after it has completed the track."),
    ("grace throw", "race",
     "A throw that both moves a piece and earns another turn."),
    # ── çizgi-toprak (territory) ─────────────────────────────────────
    ("mill", "territory",
     "Three of your pieces in a row along a marked line, which entitles you "
     "to remove one enemy piece."),
    ("point", "territory",
     "An intersection or marked spot where a piece stands. In this book "
     "pieces sit on points, not inside squares, unless the board is a grid."),
    ("placement phase", "territory",
     "The opening stage in which players put pieces on an empty board before "
     "any movement is allowed."),
    ("liberty", "territory",
     "An empty point directly adjacent to a stone or group. A group with no "
     "liberties is captured."),
    ("group", "territory",
     "Stones of one colour connected along the lines of the board, which "
     "live or die together."),
    ("eye", "territory",
     "An enclosed empty point inside a group. Two separate eyes make a group "
     "permanently safe."),
    ("alignment", "territory",
     "Any completed line of pieces that a game rewards — the general form of "
     "which the mill is the best known case."),
    # ── savaş tahtası (war-board) ────────────────────────────────────
    ("custodian capture", "war-board",
     "Taking an enemy piece by occupying the two points on opposite sides of "
     "it. The piece is not jumped; it is pinned between two of yours."),
    ("approach capture", "war-board",
     "Taking a line of enemy pieces by moving deliberately towards them."),
    ("withdrawal capture", "war-board",
     "Taking a line of enemy pieces by moving deliberately away from them. "
     "The mirror of approach capture, and rare outside Madagascar."),
    ("intersection board", "war-board",
     "A board of lines whose crossing points, not whose spaces, carry the "
     "pieces."),
    ("promotion", "war-board",
     "A piece gaining new powers on reaching a particular rank or point."),
    ("chain capture", "war-board",
     "Continuing to take in one turn for as long as further captures are "
     "available to the same piece."),
    # ── şans (chance) ────────────────────────────────────────────────
    ("randomiser", "chance",
     "Any device that produces the unknown: dice, staves, shells, "
     "knucklebones, a spun top or a drawn lot."),
    ("knucklebone", "chance",
     "The ankle bone of a sheep or goat, thrown as a four-sided die. Its "
     "faces are unequal, so its values are unequal."),
    ("cowrie", "chance",
     "A shell thrown as a two-sided die, scoring by whether the opening "
     "lands up or down."),
    ("bank", "chance",
     "The player against whom the others play in turn. This book scores "
     "banks; it does not stake them."),
    ("stake", "chance",
     "What is risked on an outcome. Where a source records a wager, this "
     "book converts it to points and says so in the entry."),
    ("counting out", "chance",
     "Choosing who starts by a rhyme or a hidden-hand throw rather than by "
     "a die."),
    # ── tahtasız (boardless) ─────────────────────────────────────────
    ("bed", "boardless",
     "A figure drawn on the ground and played inside, as in hopscotch. It "
     "is not a board: its compartments are the ground itself."),
    ("taw line", "boardless",
     "The line a player shoots or throws from."),
    ("chaser", "boardless",
     "The player who pursues in a tag game, usually under a restriction the "
     "others do not carry."),
    ("figure", "boardless",
     "One named stage of a skill game — a string shape, a throwing pattern, "
     "or a hopping sequence — which must be completed before the next."),
    ("dead", "boardless",
     "Out of play for the rest of the round, but not out of the game."),
    # ── genel · kitabın kendi dili ───────────────────────────────────
    ("family", None,
     "One of the seven mechanical groups this book sorts games into. A game "
     "belongs to exactly one."),
    ("first move", None,
     "The opening action of the first player, given explicitly for every "
     "game because a rule text that omits it cannot be played."),
    ("end condition", None,
     "The statement of when play stops. Distinct from the win condition: a "
     "game can end without anyone winning."),
    ("win condition", None,
     "The statement of who has won when play stops."),
    ("stalemate", None,
     "A position in which the player to move has no legal move. Every entry "
     "in this book says what happens then."),
    ("draw", None,
     "A finished game with no winner. Every entry says whether one is "
     "possible and how it is settled."),
    ("reconstruction", None,
     "A rule this book supplies because the source does not give it. Every "
     "reconstruction is declared in the entry that uses it."),
    ("documented rule", None,
     "A rule that can be traced to a page in a named source. The opposite "
     "of a reconstruction, and the default in this book."),
    ("first-hand source", None,
     "A record made by someone who watched the game played or catalogued "
     "the objects used. Preferred over later compilations."),
    ("page-verified", None,
     "A citation whose page has been opened and read, with the supporting "
     "passage recorded. This book distinguishes it from a citation merely "
     "copied from another book."),
    ("substitution", None,
     "A household object standing in for traditional material: an egg box "
     "for a sowing board, buttons for stones, lolly sticks for staves."),
    ("variant", None,
     "A recorded alternative form of the same game, given after the main "
     "rules and attributed where the source names a place."),
    ("player count", None,
     "The number of players a game takes. Where a source gives only one "
     "number, this book does not invent others."),
    ("turn", None,
     "One player's complete action before play passes on."),
    ("piece", None,
     "Any object moved or placed by a player. Called a man, stone, seed or "
     "counter depending on the game."),
    ("board", None,
     "The marked surface a game is played on. A figure scratched in the dirt "
     "is as much a board as an inlaid one."),
    ("setup", None,
     "The starting arrangement, given for every game as a performable list "
     "of steps."),
]

# ── ⑥ UYDURULMUŞ GELENEKLER ─────────────────────────────────────────────
# Yalnızca envanterde işaretlenmiş ve GEREKÇESİ olan iddialar girer.
INVENTED_TRADITIONS = [
    {
        "claim": "Hopscotch was invented by Roman soldiers as drill practice.",
        "verdict": "No source supports it.",
        "detail": "The claim appears in modern popular writing and in no "
                  "early collection. Gomme, who gathered the English forms "
                  "from correspondents across the country, records neither "
                  "the story nor a Roman origin. The game is first described "
                  "in English sources long after Rome.",
        "gameId": "hopscotch",
    },
    {
        "claim": "The Temple of Kurna carries a morris board cut in 1400 BC.",
        "verdict": "The board exists; the date does not.",
        "detail": "Diagrams cut into temple paving cannot be dated by the "
                  "date of the paving. The cutting may be any age up to the "
                  "present. This book prints the board and not the date.",
        "gameId": "nine-mens-morris",
    },
    {
        "claim": "Kalah is an ancient African game.",
        "verdict": "It is an American commercial game of the 1940s.",
        "detail": "Kalah was designed and marketed in the United States. It "
                  "borrows the sowing mechanism of much older African games "
                  "but is not one of them, and this book files it as what it "
                  "is.",
        "gameId": None,
    },
    {
        "claim": "Chinese Checkers is Chinese.",
        "verdict": "It is German, and from 1892.",
        "detail": "The game was published in Germany as Stern-Halma, a star-"
                  "shaped variant of Halma. The Chinese name was applied "
                  "later as a selling point in the United States.",
        "gameId": None,
    },
    {
        "claim": "Every board scratched on a stone is a game board.",
        "verdict": "Some are; most cannot be shown to be.",
        "detail": "Scratched grids appear on temple floors, roof slabs and "
                  "quarry blocks across the ancient world. Without pieces, a "
                  "text or a burial context, a grid is a grid. This book says "
                  "so rather than filling the gap with a story.",
        "gameId": None,
    },
]

# ── ② MALZEME REHBERİ · ARAŞTIRMA NOTU → TİCARİ İNGİLİZCE ──────────────
#
# ⚠ BU EŞLEME BİR KOLAYLIK DEĞİL, BİR KAPIDIR.
#
# Envanterin `substitutionHint` alanları ARAŞTIRMA NOTUDUR ve Türkçedir —
# orada Türkçe olmaları doğrudur (veri katmanı). Malzeme rehberi ise
# TİCARİ İÇERİKTİR ve § 29 uyarınca %100 İngilizce olmak zorundadır.
#
# Faz 5'te bu tam olarak koptu: rehberin ilk sürümü envanterdeki Türkçe
# dizeleri doğrudan ticari katmana taşıdı ve `qa_language_split.py` onu
# yakaladı. Kapı zayıflatılmadı; ÜRETEÇ düzeltildi.
#
# Eşlenmemiş bir ipucu görüldüğünde üreteç ÇÖKER. Sessizce Türkçe basmak
# ya da ipucunu atlamak yerine durur: birincisi dil ayrımını, ikincisi
# rehberin bütünlüğünü sessizce bozardı.
MATERIAL_TERMS: dict[str, str] = {
    "düğme": "buttons",
    "iki renk düğme": "buttons in two colours",
    "yumurta kolisi": "an egg box",
    "iki yumurta kolisi": "two egg boxes",
    "iki yumurta kolisi yan yana": "two egg boxes side by side",
    "yumurta kolisi ve iki kâse": "an egg box and two bowls",
    "kâğıda çizilmiş ızgara": "a grid drawn on paper",
    "kâğıt ızgara": "a paper grid",
    "kâğıda çizilmiş tahta": "the board drawn on paper",
    "kâğıda çizilmiş haç": "a cross drawn on paper",
    "kâğıda çizilmiş iz": "the track drawn on paper",
    "kâğıda çizilmiş spiral": "a spiral drawn on paper",
    "kâğıda çizilmiş üçgen": "a triangle drawn on paper",
    "kâğıda çizilmiş yıldız": "a star drawn on paper",
    "kâğıda çizilmiş sekizgen": "an octagon drawn on paper",
    "kâğıda çizilmiş çizgi": "a line drawn on paper",
    "kâğıda çizilmiş 9×9 ızgara": "a nine by nine grid drawn on paper",
    "kâğıda çizilmiş 3×10 ızgara": "a three by ten grid drawn on paper",
    "kâğıt": "paper",
    "kâğıt ve düğme": "paper and buttons",
    "kuru fasulye": "dried beans",
    "kuru fasulye veya düğme": "dried beans or buttons",
    "kuru nohut": "dried chickpeas",
    "nohut": "chickpeas",
    "çakıl": "pebbles",
    "yere dizilmiş çakıllar": "pebbles laid out on the ground",
    "çakıl ve mısır tanesi": "pebbles and grains of corn",
    "çakıl ve deve dikeni": "pebbles and thorns",
    "boncuk": "beads",
    "kırmızı-siyah boncuk": "red and black beads",
    "dama tahtası": "a draughts board",
    "dama tahtası köşeleri kapatılarak": "a draughts board with the corners blocked off",
    "dama takımı": "a draughts set",
    "dama takımı (8×8 biçimi için)": "a draughts set, for the eight by eight form",
    "tavla tahtası": "a backgammon board",
    "satranç takımı": "a chess set",
    "satranç takımı; piyonlar üçüncü sıraya dizilir":
        "a chess set with the pawns set out on the third rank",
    "satranç takımı; vezir ve fil hareketleri değiştirilir":
        "a chess set with the queen's and bishop's moves altered",
    "üç yassı çubuk": "three flat sticks",
    "üç yassı çubuk; bir yüzü boyalı":
        "three flat sticks, painted on one side",
    "dört yassı çubuk": "four flat sticks",
    "dört yassı çubuk veya bozuk para": "four flat sticks or coins",
    "dört yassı çöp veya bozuk para": "four flat sticks or coins",
    "yarım kesilmiş dört çubuk veya dört bozuk para":
        "four sticks split lengthways, or four coins",
    "masaya dizilmiş çubuklar": "sticks laid out on the table",
    "bozuk para ve düğme": "coins and buttons",
    "düğme veya bozuk para": "buttons or coins",
    "düğme ve bir madeni para": "buttons and one coin",
    "dört bozuk para": "four coins",
    "dört bozuk para (tura = 1)": "four coins, heads counting one",
    "altı bozuk para (tura sayılır)": "six coins, heads counting",
    "iki bozuk para ve iki düğme": "two coins and two buttons",
    "üç bozuk para ve üç düğme": "three coins and three buttons",
    "kürdan veya bozuk para": "cocktail sticks or coins",
    "bir yüzü boyalı dört fasulye": "four beans painted on one side",
    "bir yüzü boyalı beş fasulye": "five beans painted on one side",
    "iki renk düğme ve bir işaretli taş":
        "buttons in two colours and one marked piece",
    "iki renk düğme veya siyah-beyaz çakıl":
        "buttons in two colours, or black and white pebbles",
    "üzerine yazı yazılmış düğmeler": "buttons written on",
    "yassı bir düğme": "one flat button",
    "beş çakıl veya beş küçük düğme": "five pebbles or five small buttons",
    "dört köşeli düğme veya dört yassı taş; her yüz farklı işaretlenir":
        "four square buttons or four flat stones, each face marked differently",
    "dört yüzü işaretli dört yassı nesne":
        "four flat objects with marked faces",
    "dört yüzü at/deve/koyun/keçi diye işaretlenmiş dört yassı nesne":
        "four flat objects marked horse, camel, sheep and goat",
    "üçüncü zar eklenir": "add a third die",
    "üç zar ve kuru fasulye": "three dice and dried beans",
    "kuma açılmış çukurlar": "pits scooped in sand",
    "kuma çizilmiş ızgara": "a grid drawn in sand",
    "kareli defter kâğıdı ve iki kalem": "squared paper and two pencils",
    "kare kâğıt ve kürdanla yapılmış topaç":
        "a square of paper and a cocktail stick made into a spinning top",
    "şişe kapağı": "bottle caps",
    "standart desteden 8, 9 ve 10'lar çıkarılır":
        "a standard pack with the eights, nines and tens taken out",
    "standart desteden 2–5 arası çıkarılır":
        "a standard pack with the twos to fives taken out",
    "standart desteden 2–6 arası çıkarılır":
        "a standard pack with the twos to sixes taken out",
    "48 kartlık standart destenin bir bölümü":
        "forty-eight cards from a standard pack",
    "standart deste ile eşleştirme biçimi; kitap bir dönüşüm tablosu verir":
        "a standard pack matched to the traditional one; the book gives a "
        "conversion table",
    "standart domino takımından 32 taş seçilir; kitap bir eşleştirme tablosu verir":
        "thirty-two tiles from a standard domino set; the book gives a "
        "matching table",
    "ayakkabı bağı düğümlenerek halka yapılır":
        "a shoelace knotted into a loop",
    "delinmiş ceviz veya sert plastik top":
        "a drilled walnut or a hard plastic ball",
    "yumuşak top ve tahta kaşık (güvenli uyarlama)":
        "a soft ball and a wooden spoon, as a safe substitute",
    "madeni paranın etrafına bağlanmış plastik poşet şeritleri":
        "strips of plastic bag tied round a coin",
    "yedi kitap kapağı büyüklüğünde karton":
        "seven pieces of card the size of a book cover",
    "çorap topu": "a ball of rolled socks",
    "atkı veya bandana": "a scarf or bandana",
    "maskeleme bandı (iç mekân)": "masking tape, indoors",
    "eşit büyüklükte taşlar veya tenis topları (iç mekân uyarlaması)":
        "stones of equal size, or tennis balls indoors",
}


PLAYER_BUCKETS = (("2", "Two players"),
                  ("3-4", "Three or four players"),
                  ("5+", "Five players or more"))
DURATION_BUCKETS = (("<=15", "Fifteen minutes or less"),
                    ("<=30", "Up to half an hour"),
                    ("30+", "More than half an hour"))


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dump(path: str, payload) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


# ---------------------------------------------------------------------------
# KOVA ATAMASI — tek tanım. `qa_index.py` bunu İÇE AKTARIR ve kendi
# kopyasını yazmaz: iki kova tanımı ayrışırsa denetim, denetlediğini
# sanıp başka bir şeyi denetler (Faz 4'ün `measured_block_keys` dersi).
# ---------------------------------------------------------------------------
def player_bucket(inv: dict) -> str:
    p = inv.get("players") or {}
    lo, hi = p.get("min") or 0, p.get("max") or 0
    if hi >= 5:
        return "5+"
    if hi >= 3 or lo >= 3:
        return "3-4"
    return "2"


def duration_bucket(inv: dict) -> str:
    d = inv.get("durationMinutes") or {}
    hi = d.get("max") or d.get("min") or 0
    if hi <= 15:
        return "<=15"
    if hi <= 30:
        return "<=30"
    return "30+"


def page_map(root: str) -> dict:
    """Oyun → başlangıç sayfası. YALNIZCA gerçekten ölçülmüş oyunlar.

    Sayfa göndermesi, dizgi ölçümünün `billedPages` değerinden birikimli
    olarak türetilir; ölçülmemiş bir oyun haritada YOKTUR ve indekste
    `null` görünür. Uydurulmuş bir sayfa numarası, test edilemeyen bir
    iddiadır (kurucu § 27)."""
    p = os.path.join(root, "06_REPORTS", "phase2-typeset-measurement.json")
    if not os.path.exists(p):
        return {}
    d = load(p)
    cfg = load(os.path.join(root, "project_config.json"))
    pm = cfg["production"]["pageModel"]
    cursor = pm["frontMatterPages"] + 1
    out = {}
    for r in d.get("perGame", []):
        billed = int(r.get("billedPages") or 2)
        out[r["gameId"]] = cursor
        cursor += billed
    return out


def build(root: str, args) -> int:
    scope = load(os.path.join(root, "01_SOURCE", "scope_lock.json"))
    index = load(os.path.join(root, "01_SOURCE", "game_index.json"))
    inv = {g["gameId"]: g for g in index["games"]}
    entries = scope["entries"]

    verified: dict = {}
    vp = os.path.join(root, "01_SOURCE", "source_verification.json")
    if os.path.exists(vp):
        for r in load(vp)["records"]:
            if r.get("status") == "verified":
                verified.setdefault(r["gameId"], []).append(r)

    written: dict = {}
    bp = os.path.join(root, "02_MANUSCRIPT", "book.json")
    if os.path.exists(bp):
        written = {g["gameId"]: g for g in load(bp)["games"]}

    pages = page_map(root)

    # ── ① TAHTA ŞABLONLARI ───────────────────────────────────────────
    # Şablon, okurun FOTOKOPİYLE alacağı tahtadır: yalnızca kurulum ya da
    # tahta gösteren diyagramlar aday olur; bir hamle ayrıntısı şablon
    # olamaz çünkü üstünde oynanamaz.
    ddir = os.path.join(root, "07_ASSETS", "diagrams")
    templates = []
    seen_game = set()
    for fn in sorted(os.listdir(ddir)) if os.path.isdir(ddir) else []:
        if not fn.endswith("_diagrams.json"):
            continue
        for d in load(os.path.join(ddir, fn)).get("diagrams", []):
            gid = d.get("gameId")
            if gid not in {e["gameId"] for e in entries}:
                continue
            if d.get("type") not in ("setup-illustration", "board-diagram"):
                continue
            if gid in seen_game:
                continue
            seen_game.add(gid)
            templates.append({
                "gameId": gid,
                "title": inv.get(gid, {}).get("name", gid),
                "diagramId": d["diagramId"],
                "boardClass": d.get("boardClass"),
                "size": d.get("size"),
                "reconstructed": bool(d.get("reconstructed")),
                "photocopyNote": "Full scale on 8.5 × 11 with margins.",
            })

    # ── ② MALZEME REHBERİ ────────────────────────────────────────────
    # Araştırma notu Türkçedir; rehber TİCARİ İngilizcedir. Eşlenmemiş bir
    # ipucu sessizce geçirilmez — üreteç DURUR.
    subs: dict = {}
    unmapped: set = set()
    for e in entries:
        g = inv.get(e["gameId"], {})
        for hint in (g.get("substitutionHint") or []):
            term = MATERIAL_TERMS.get(hint)
            if term is None:
                unmapped.add(hint)
                continue
            subs.setdefault(term, []).append(e["gameId"])
    if unmapped:
        print("  ⛔ TİCARİ KARŞILIĞI OLMAYAN malzeme ipucu (%d):"
              % len(unmapped))
        for h in sorted(unmapped):
            print("       · %s" % h)
        print("     MATERIAL_TERMS içine İngilizce karşılığını ekleyin.")
        print("     Türkçe bir araştırma notu ticari arka maddeye giremez "
              "(§29).")
        return 1

    # "Neyin yerine ne konur": ikinci sütun, oyunun YAZILMIŞ maddesinden
    # okunur (orası zaten İngilizcedir). Yazılmamış oyun için boştur ve
    # uydurulmaz.
    materials = []
    for term, gids in sorted(subs.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        replaces = sorted({(written[g].get("spec") or {}).get("materials")
                           for g in gids if g in written
                           and (written[g].get("spec") or {}).get("materials")})
        materials.append({
            "substitute": term,
            "usedBy": sorted(gids),
            "count": len(gids),
            "replaces": replaces,
            "replacesStatus": ("documented" if replaces
                               else "awaiting-entry"),
        })

    # ── ③ SÖZLÜK ─────────────────────────────────────────────────────
    # `attestedIn` ÖLÇÜLÜR, iddia edilmez: terim yazılmış prozada geçiyor mu.
    glossary = []
    for term, family, definition in GLOSSARY:
        attested = []
        pat = re.compile(r"\b%s\b" % re.escape(term), re.I)
        for gid, g in written.items():
            blob = json.dumps(g, ensure_ascii=False)
            if pat.search(blob):
                attested.append(gid)
        glossary.append({
            "term": term,
            "family": family,
            "definition": definition,
            "attestedIn": sorted(attested),
            "attestedCount": len(attested),
        })

    # ── ④ KAYNAKÇA ───────────────────────────────────────────────────
    #
    # ⚠ DOĞRULAMA KAYDININ `locator` ALANI TİCARİ METİN DEĞİLDİR.
    # O alan Türkçe bir araştırma notudur ("'Ring-taw', cilt II, ss. 113–114")
    # ve ticari kaynakçaya basılamaz (§29). Yazılmış bir maddenin kendi
    # `sources` dizisi ZATEN ticari İngilizcedir ve sayfa numarasını da
    # taşır — kaynakçanın doğru kaynağı odur.
    #
    # Doğrulama kaydından yalnızca SAYI alınır: kaç künye sayfa seviyesinde
    # açılıp okundu. Sayı bir iddiadır ve `qa_index.py ⑤` onu kayıtla
    # karşılaştırır; metin ise ticari katmandan gelir.
    bibliography = []
    for e in sorted(entries, key=lambda x: x["name"]):
        gid = e["gameId"]
        recs = verified.get(gid, [])
        entry_sources = None
        if gid in written and written[gid].get("sources"):
            entry_sources = list(written[gid]["sources"])
        bibliography.append({
            "gameId": gid,
            "title": e["name"],
            "culture": e["culture"],
            "sources": entry_sources or e.get("sourceRefs", []),
            "citationSource": ("entry" if entry_sources else "inventory"),
            "pageVerifiedCount": len(recs),
            "verificationLevel": e.get("sourceVerification"),
            "status": ("page-verified" if recs else
                       "cited, page not yet opened"),
        })

    # ── ⑤ ÜÇ İNDEKS ──────────────────────────────────────────────────
    by_culture: dict = {}
    by_players: dict = {k: [] for k, _ in PLAYER_BUCKETS}
    by_duration: dict = {k: [] for k, _ in DURATION_BUCKETS}
    for e in entries:
        gid = e["gameId"]
        g = inv.get(gid, {})
        row = {
            "gameId": gid,
            "title": e["name"],
            "family": e["family"],
            "page": pages.get(gid),
            "pageStatus": "measured" if gid in pages else "awaiting-typesetting",
        }
        by_culture.setdefault(e["culture"], []).append(row)
        by_players[player_bucket(g)].append(
            dict(row, players="%s–%s" % ((g.get("players") or {}).get("min"),
                                         (g.get("players") or {}).get("max"))))
        by_duration[duration_bucket(g)].append(
            dict(row, minutes="%s–%s" % (
                (g.get("durationMinutes") or {}).get("min"),
                (g.get("durationMinutes") or {}).get("max")),
                ageMin=g.get("ageMinEstimate")))

    for v in by_culture.values():
        v.sort(key=lambda r: r["title"])
    for d in (by_players, by_duration):
        for v in d.values():
            v.sort(key=lambda r: r["title"])

    indexes = {
        "byCulture": {
            "key": "culture",
            "sourceField": "culture",
            "buckets": dict(sorted(by_culture.items())),
        },
        "byPlayerCount": {
            "key": "players",
            "sourceField": "players",
            "bucketLabels": dict(PLAYER_BUCKETS),
            "buckets": by_players,
        },
        "byDurationAndAge": {
            "key": "duration",
            "sourceField": "durationMinutes + ageMinEstimate",
            "bucketLabels": dict(DURATION_BUCKETS),
            "buckets": by_duration,
        },
    }

    measured = sum(1 for e in entries if e["gameId"] in pages)
    payload = {
        "$comment": [
            "ARKA MADDE — ÜRETİLMİŞ DOSYA (04_BUILD/build_backmatter.py).",
            "ELLE DÜZENLENMEZ. Envanter değişince yeniden üretilir.",
            "",
            "Sayfa göndermeleri YALNIZCA gerçekten dizilip ölçülmüş oyunlar",
            "için doludur. Ölçülmemiş oyun `page: null` taşır ve indekste",
            "'awaiting-typesetting' görünür. Uydurulmuş bir sayfa numarası,",
            "test edilemeyen bir iddiadır (kurucu § 27).",
            "",
            "Denetleyen: 04_BUILD/qa_index.py",
        ],
        "version": "1.0",
        "generatedAtPhase": "phase5",
        "sections": ["boardTemplates", "materialsGuide", "glossary",
                     "bibliography", "indexes", "inventedTraditions"],
        "scopeGames": len(entries),
        "measuredGames": measured,
        "boardTemplates": templates,
        "materialsGuide": materials,
        "glossary": glossary,
        "bibliography": bibliography,
        "indexes": indexes,
        "inventedTraditions": INVENTED_TRADITIONS,
    }
    dump(os.path.join(root, "02_MANUSCRIPT", "backmatter.json"), payload)

    # ── PUBLIC ÖZET — proza taşımaz, yalnızca YAPI ────────────────────
    public = {
        "$comment": [
            "ARKA MADDE YAPISAL ÖZETİ — public katman.",
            "Tanım metni, künye pasajı ve şablon çizimi BURADA DURMAZ;",
            "yalnızca sayılar ve kimlikler durur (A1 · manuscript koruması).",
        ],
        "generatedAtPhase": "phase5",
        "scopeGames": len(entries),
        "measuredGames": measured,
        "boardTemplates": len(templates),
        "materialsGuideRows": len(materials),
        "glossaryTerms": len(glossary),
        "glossaryAttested": sum(1 for t in glossary if t["attestedCount"]),
        "bibliographyEntries": len(bibliography),
        "bibliographyPageVerified": sum(1 for b in bibliography
                                        if b["pageVerifiedCount"]),
        "inventedTraditions": len(INVENTED_TRADITIONS),
        "indexes": {
            "byCulture": {k: len(v) for k, v in
                          sorted(indexes["byCulture"]["buckets"].items())},
            "byPlayerCount": {k: len(v) for k, v in by_players.items()},
            "byDurationAndAge": {k: len(v) for k, v in by_duration.items()},
        },
    }
    dump(os.path.join(root, "06_REPORTS", "backmatter.json"), public)

    print("  ✓ arka madde üretildi · %d oyun" % len(entries))
    print("      ① tahta şablonu      %3d" % len(templates))
    print("      ② malzeme satırı     %3d" % len(materials))
    print("      ③ sözlük terimi      %3d  (%d tanesi prozada geçiyor)"
          % (len(glossary), public["glossaryAttested"]))
    print("      ④ kaynakça maddesi   %3d  (%d tanesi sayfa-doğrulanmış)"
          % (len(bibliography), public["bibliographyPageVerified"]))
    print("      ⑤ üç indeks          %3d kültür · %s · %s"
          % (len(by_culture),
             "/".join("%s:%d" % (k, len(v)) for k, v in by_players.items()),
             "/".join("%s:%d" % (k, len(v)) for k, v in by_duration.items())))
    print("      ⑥ uydurulmuş gelenek %3d" % len(INVENTED_TRADITIONS))
    print("  · sayfa göndermesi olan oyun: %d/%d (gerisi dizgi bekliyor)"
          % (measured, len(entries)))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    print("=" * 74)
    print("  ARKA MADDE ÜRETECİ")
    print("=" * 74)
    rc = build(root, args)
    print("=" * 74)
    return rc


if __name__ == "__main__":
    sys.exit(main())
