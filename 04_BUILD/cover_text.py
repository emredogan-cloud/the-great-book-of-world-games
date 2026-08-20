# -*- coding: utf-8 -*-
"""
KAPAK METNİ — The Great Book of World Games
================================================================================
Kapakta basılan HER kelime burada durur ve **iddia taramasından geçer**
(`covers.py --check`).

⚠ SAYI YOK. Oyun ve kültür sayıları `frontmatter.json § measured` içinden
BASILIR. Kapakta elle yazılmış bir sayı, kitabın en görünür yerinde bayat
bir iddiadır.

⚠ ARKA KAPAK METNİ UYDURULMADI. Onaylı KDP açıklamasından (metadata.json
§ description) **damıtıldı**: her cümlesinin karşılığı orada vardır.
Yeni bir vaat, yeni bir sıfat, yeni bir iddia eklenmedi.
"""

# Ön kapak — alt başlık ölçümden BİÇİMLENİR
FRONT_TITLE_TOP = "THE GREAT BOOK OF"
FRONT_TITLE_MAIN = "WORLD GAMES"


def front_subtitle(m):
    return ("%d games from %s years of human play" %
            (m["games"], "{:,}".format(m["oldestGameAgeYears"])))


def front_subtitle2(m):
    return ("Rules, boards and stories from %d cultures" % m["cultures"])


AUTHOR = "EMRE DOĞAN"

SPINE_TITLE = "THE GREAT BOOK OF WORLD GAMES"
SPINE_AUTHOR = "EMRE DOĞAN"


def back_copy(m):
    """Arka kapak metni — onaylı açıklamadan damıtıldı."""
    return [
        ("head", "A reference book you play from."),
        ("body",
         "%d traditional games from %d cultures, from the royal graves of Ur "
         "to a Zulu playground — set out so you can play them tonight. Each "
         "game gets two facing pages, so the book lies open on the table and "
         "nobody turns a page in the middle of a turn."
         % (m["games"], m["cultures"])),
        ("head", "Sorted by how they work, not by where they are from."),
        ("body",
         "Seven families — sowing, hunt and siege, race home, line and "
         "territory, the war board, chance and nerve, and games without a "
         "board. Put that way, the mancala games of Ghana, Sri Lanka and "
         "Buganda sit together, and you can watch six cultures solve the "
         "problem of chess six different ways."),
        ("head", "Honest about what is known."),
        ("body",
         "Every rule set names the work and the pages it was read from. Where "
         "a record is incomplete, the entry says so and shows what has been "
         "reconstructed. One page at the back lists the game origin stories "
         "that are widely repeated and are not true."),
        ("body",
         "Inside: what to use instead of what — buttons, coins, dried beans, "
         "an egg box. Numbered rules, one action to a line. Board diagrams "
         "drawn to scale, and full-size templates at the back you can "
         "photocopy. Almost nothing in this book has to be bought."),
    ]


# Yasak iddia kalıpları — `aplus.py` ile AYNI liste, kapak için de koşar.
FORBIDDEN = [
    (r"\bbest[- ]?sell(er|ing)\b", "bestseller iddiası"),
    (r"\baward[- ]winning\b|\bprize[- ]winning\b|\bwinner of\b", "ödül iddiası"),
    (r"\bchild[- ]tested\b|\bkid[- ]tested\b|\bplaytested\b", "test iddiası"),
    (r"\bguarantee\w*\b|\bproven to\b|\bwill improve\b|\bboosts?\b",
     "garanti edilmiş sonuç iddiası"),
    (r"\b#\s?1\b|\bnumber one\b|\bworld'?s (best|leading)\b", "sıralama iddiası"),
    (r"\bcomplete (guide|collection) to (all|every)\b", "bütünlük iddiası"),
]
