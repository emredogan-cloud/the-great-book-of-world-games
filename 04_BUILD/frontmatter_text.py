# -*- coding: utf-8 -*-
"""FRONT MATTER AND FAMILY OPENERS — 2026 recovery edition.

Hand-written text. Numbers are never typed here: «games», «cultures» and the
rest are MEASURED by build_frontmatter.py from the manuscript and substituted
at build time. {page:key} references are resolved by interior.py from the
page map of the book being printed. A paragraph given as a dict carries one
text per edition ("print" = paperback and hardcover; "largeprint";
"kindle"): a sentence that is true of one edition must not be printed in
another (audit WG-007).

Corrections made in this revision, with the audit reference:
  WG-008  the truncated sentence in On Sources is restored;
  WG-009  the merels board and the alquerque board are no longer conflated;
  WG-010/011  Ur is the oldest game with (reconstructed) rules, not the oldest
          game; the Babylonian writer is a scribe;
  WG-001  the full-size boards now exist, and every sentence about them says
          exactly what is printed and what is online;
  WG-002  the source claim is stated as it now is: page (or, for a modern
          codified ruleset, section) for every game;
  WG-030  family VI is redefined and renamed; Set-dilth moves to the race family;
  WG-031/032/048  the family openers are proofed against their own entries;
  F-E3    the Isle of Man record is dated 1695 and the cloister claims narrowed.
"""

INTRO = {
 "id": "introduction",
 "title": "Why We Play",
 "paragraphs": [
  "Go into one of the English cathedrals that was once a monastery — "
  "Gloucester, say, or Westminster — and look down at the stone benches in the "
  "cloister. Worn shallow by centuries of weather and hands, you may find a "
  "diagram: three squares inside one another, joined across the middle of each "
  "side. It is a merels board, the board of nine men's morris. Monks and the "
  "boys they taught cut boards like it into the seats where they were meant to "
  "sit in silence, and then they played on them. In 1695 the churchwardens of "
  "Lezayre, on the Isle of Man, reported two men to the church court for "
  "“making nine holes with their knives” on a Sunday after evening prayer.",

  "That is the first thing worth saying about games: people have always found "
  "the time. The second is stranger. At Gloucester the same benches carry a "
  "second board, a cross of thirty-three points on which a fox hunts geese. And "
  "a third shape — a square of twenty-five points crossed by its diagonals, the "
  "alquerque of medieval Spain — is the board that Zuni players stretched into "
  "awithlaknannai and Malay players built their tiger game on, and it is "
  "usually thought to be the parent of draughts. Nobody planned any of that. A "
  "shape with a few points and a rule about jumping turns out to be one of the "
  "good ideas, and good ideas travel — or, just as often, get found again by "
  "somebody who never heard of the first person to find them.",

  "This book is arranged around that fact. It is not organised by country. A "
  "book organised by country teaches you geography: here is the India chapter, "
  "here is the Japan chapter, and here, at the back, is a chapter called Africa "
  "doing the work of fifty-four countries at once. Arranged that way, the most "
  "interesting thing about games is invisible. So the seven parts of this book "
  "are seven ideas about how a game can work, and each part collects the games "
  "that share the idea, wherever they are from. You will meet the sowing games "
  "first — a single mechanic that runs from Ghana to Sri Lanka — and you will "
  "meet them together, which is the only way to see what they have in common "
  "and where they part.",

  "There are «games_word» games here, from «cultures_word» cultures. The oldest "
  "is senet, whose boards were being made in Egypt around 3000 BC; its rules are "
  "lost, and the entry says so. The oldest game whose rules have come down to "
  "us in any form is the Royal Game of Ur: its boards were buried in the royal "
  "graves of the city of Ur around 2600 BC, and a Babylonian scribe wrote down "
  "part of its rules on a clay tablet in 177 BC. We can play it today in a "
  "modern reconstruction built on that tablet. We do not know how to play a "
  "great many other games, and where that is the case this book says so on the "
  "page rather than filling the gap quietly.",

  "«games_word_cap» is not a round number, and that is deliberate. A game got "
  "into this book only if a real source could be opened and its rules traced to "
  "a page. Where a source turned out to describe a board without describing the "
  "play — which happens more often than you would think — the game was left "
  "out, unless the gap was small enough to close honestly. «recon_word_cap» of "
  "the games here are marked as reconstructions: the record is genuine but "
  "incomplete, and each of those entries says, in a box beside the rules, what "
  "the sources give and what this book has supplied.",

  {"print": "What you do with the book is play. Every game begins on a left-hand "
            "page, so that its board and its rules lie open together on the table; "
            "the longer games carry on over a second pair of pages. Every game "
            "lists what it needs in things you already own: buttons, coins, dried "
            "beans, a sheet of paper, a pencil. Almost none of them needs anything "
            "bought. At the back are full-size boards for «tpl_games_word» of the "
            "games, drawn at playing size for the photocopier, and the free "
            "companion pack online has printable boards for every game that needs "
            "one.",
   "largeprint": "What you do with the book is play. Every game begins on a new "
                 "page and sets out its rules in the same order every time. Every "
                 "game lists what it needs in things you already own: buttons, "
                 "coins, dried beans, a sheet of paper, a pencil. Almost none of "
                 "them needs anything bought. At the back are full-size boards for "
                 "«tpl_games_word» of the games, drawn at playing size for the "
                 "photocopier, and the free companion pack online has printable "
                 "boards for every game that needs one.",
   "kindle": "What you do with the book is play. Every game is a single chapter "
             "and sets out its rules in the same order every time. Every game "
             "lists what it needs in things you already own: buttons, coins, dried "
             "beans, a sheet of paper, a pencil. Almost none of them needs anything "
             "bought. The free companion pack online has full-size printable boards "
             "for every game that needs one."},

  "One last thing. Play is the oldest evidence we have of people doing "
  "something for no reason but the doing of it. The oldest boards in this book "
  "were made by people whose language we can barely read and whose gods we know "
  "only by their statues, and what those boards tell us is that they sat down "
  "opposite one another and argued about a rule. You are about to do the same "
  "thing. That is the whole of it."
 ]
}

HOWTO = {
 "id": "how-to-use",
 "title": "How to Use This Book",
 "paragraphs": [
  {"print": "Every game is laid out the same way, so that after the second or "
            "third game you stop reading the layout and start reading the game. "
            "It begins on a left-hand page with the board and the rules facing "
            "each other.",
   "largeprint": "Every game is laid out the same way, so that after the second "
                 "or third game you stop reading the layout and start reading the "
                 "game.",
   "kindle": "Every game is laid out the same way, so that after the second or "
             "third game you stop reading the layout and start reading the game."}
 ],
 "sections": [
  {"heading": "Quick play",
   "text": "The box at the top: how many play, how long a game takes, the age "
           "from which a child can hold the whole game in their head, the "
           "difficulty, what you need and what you are trying to do, then the "
           "game in two sentences. The time is for one game between players who "
           "know the rules."},
  {"heading": "Difficulty",
   "text": "A five-point scale of how much there is to learn before your first "
           "game — not how deep the game goes. Go has few rules and scores low; "
           "it will still take a lifetime. 1 of 5, very easy: one or two "
           "rules. 2 of 5, easy: learnt in about five minutes. 3 of 5, "
           "moderate: a full rule set with captures or special squares; play "
           "a practice game. 4 of 5, demanding: many rules that interact; "
           "allow a practice game or two. 5 of 5, expert: stages and "
           "exceptions; expect several practice games."},
  {"heading": "Background",
   "text": "Where the game comes from and how we know about it. It is kept apart "
           "from the rules, so you can skip it at the table and come back to it "
           "afterwards."},
  {"heading": "What you need",
   "text": "What the game is traditionally played with, and what you can use "
           "instead. Where a substitute changes the feel of the game, the entry "
           "says so."},
  {"heading": "Setup and the rules",
   "text": "Setup, then what you do on your turn, then how pieces move, sow, "
           "capture or score. Each numbered line is one action. They are written "
           "flat and dry on purpose: a rule you have to read twice at the table is "
           "a broken rule."},
  {"heading": "Ending and winning, and special situations",
   "text": "When the game ends and who has won, stated so that both players can "
           "check it. Then the arguments that actually break out: what happens on "
           "a draw, what happens when a player cannot move, and what happens when "
           "somebody plays an illegal move. Where the sources do not settle a "
           "point, the book makes a ruling, marks it with a dagger (†) and says "
           "so under Sources — so that you know it is ours and can overrule it."},
  {"heading": "A worked turn",
   "text": "One real turn, played out from a stated position: what is on the "
           "board, the move, and what the board looks like afterwards. Where a "
           "picture helps, it is drawn."},
  {"heading": "Your first game and the variants",
   "text": "Your first game is a smaller or simpler version to start with, and "
           "with children it is usually the right place to begin. Variants are "
           "other recorded forms of the game; anything that is not a recorded "
           "form is labelled a house rule."},
  {"heading": "Reconstruction and sources",
   "text": "Where the record of a game is incomplete, a box beside the rules says "
           "what the sources give and what this book supplies. The Sources list "
           "at the end of each entry names the works the rules were read from and "
           "the pages; for a modern codified ruleset, such as a federation's "
           "rulebook, it names the document and the section."},
  {"heading": "The diagrams",
   "text": "Black pieces are drawn filled and White pieces open; a ring inside a "
           "piece marks a king, a general or a hunter. Arrows show moves, dashed "
           "arrows show a route, and a cross marks a piece captured. Squares and "
           "points on a grid are named by column letter and row number from the "
           "first player's side (a1 is the bottom left corner). On sowing boards "
           "each player counts their own pits from their own left."},
  {"print": {"heading": "At the back",
             "text": "Full-size boards for the photocopier and a list of what to "
                     "gather for a games kit; a glossary of the terms the rules "
                     "use; the sources; an index of every game under every name "
                     "it goes by; indexes by culture, age and difficulty (players "
                     "and playing time are in Tonight's Game at the front); a page "
                     "of origin stories that are widely repeated and are not true; "
                     "a note on the illustrations; and the address of the free "
                     "companion pack."},
   "kindle": {"heading": "At the back",
              "text": "A glossary of the terms the rules use; the sources; an "
                      "index of every game under every name it goes by; indexes "
                      "by culture, age and difficulty; a page of origin stories "
                      "that are widely repeated and are not true; a note on the "
                      "illustrations; and the address of the free companion pack, "
                      "which has full-size printable boards."}}
 ]
}

FAMILIES_MAP = {
 "id": "seven-families",
 "title": "The Seven Families",
 "paragraphs": [
  "Games are sorted here by what they do, not by where they come from. Seven "
  "ideas cover almost everything people have played on a board or a floor. The "
  "boundaries between them are not decorative: each family has a rule for what "
  "belongs in it and a rule for what does not, and a few games sit close to a "
  "border and are placed with an explanation.",
  "The test that matters is mechanical. A sowing game and a race game can look "
  "identical on the table — pieces going round a circuit — but in a race one "
  "piece travels and in sowing a handful is distributed and no piece has an "
  "identity at all. That difference changes every decision a player makes, so "
  "it is the difference the book sorts on."
 ],
 "table": [
  {"n": "I", "name": "The Sowing Games",
   "idea": "A handful of seeds is sown one to a pit; where the last seed lands "
           "decides what happens.",
   "test": "The seeds belong to nobody while they are on the board."},
  {"n": "II", "name": "The Hunt and the Siege",
   "idea": "Two unequal sides with two different goals: few and strong against "
           "many and weak.",
   "test": "The two sides are not trying to do the same thing."},
  {"n": "III", "name": "The Race Home",
   "idea": "Pieces travel a fixed track towards a goal, and a throw decides how "
           "far.",
   "test": "One piece moves, and the distance is not chosen."},
  {"n": "IV", "name": "The Line and the Territory",
   "idea": "You win by an arrangement: a row of three, a wall round empty "
           "ground, or a position that leaves your opponent no move.",
   "test": "The shape on the board is the aim; capture, where there is any, "
           "serves it."},
  {"n": "V", "name": "The War Board",
   "idea": "Two symmetrical sides, the same goal, and the game is won by "
           "capturing or trapping.",
   "test": "Both players could win the same way."},
  {"n": "VI", "name": "Chance and Scoring",
   "idea": "A throw of bones or a hand of tiles decides, and a score is kept.",
   "test": "Nothing travels along a track and there is no board position to "
           "develop."},
  {"n": "VII", "name": "Games Without a Board",
   "idea": "Nothing is needed but hands, voices, string, stones, or a mark "
           "scratched on the ground.",
   "test": "There is no board and no throwing instrument."}
 ],
 "closing":
  "One family is much smaller than the others. Chance and Scoring has «chance_word» "
  "entries, because most games of pure chance are gambling games, and this book "
  "keeps the play and leaves out the stakes — and a gambling game with the "
  "betting taken out is very often no game at all. Where stakes have been "
  "removed, the entry says so."
}

SOURCES_NOTE = {
 "id": "on-sources",
 "title": "On Sources, and What This Book Does Not Know",
 "paragraphs": [
  "Every game in this book names the work its rules were read from, and the "
  "pages. For the «codified_word» games whose rules today are a codified modern "
  "set — international draughts, for instance, or the Japanese rules of shogi — "
  "the citation names the rulebook and the section instead, because that is "
  "where the rule now lives. That sounds like an ordinary thing for a reference "
  "book to do. It is not: a great deal of what is published about traditional "
  "games repeats a rule set that nobody has traced back to anything, and the "
  "repetition is what makes it look reliable.",
  "So the test used here is narrow. A source counts if it was opened, if the "
  "page was read, and if the rules on that page are complete enough to play "
  "from — or, where they are not, if the gap is small enough to close honestly "
  "and the closing is labelled. Where a source turned out to name a game "
  "without describing it — Murray on Tapatan, for instance, who gives a line and "
  "a citation and no rules — the game is not in this book. Where a source gives "
  "a board and no rules for it, the game is not here either. That is why the "
  "number of games here is «games_word» and not a hundred.",
  "«recon_word_cap» games are marked as reconstructions. It means the record is "
  "genuine but has a hole in it, and the book has filled the hole with the best "
  "available reasoning rather than leaving the game unplayable. A box beside the "
  "rules says what the sources give and what the book supplies, and names the "
  "scholar whose reconstruction is followed where there is one. A book that "
  "reconstructs quietly is not a reference book.",
  "Some games here also need a rule that no source supplies at all — most often "
  "the draw, or who moves first. Traditional play does not always define one, "
  "because traditional play has a room full of people who settle it. Where this "
  "book supplies such a rule it marks it with a dagger (†) and explains it "
  "under Sources, so that you can overrule it. You are allowed to. Every game in "
  "here was changing while it was being recorded, and it will change again on "
  "your table.",
  {"print": "Finally, one section at the back ({page:bm:invented}) is given over "
            "to origin stories that are widely repeated and are not supported by "
            "anything: that hopscotch was Roman military drill, that Chinese "
            "checkers is Chinese, that kalah is an ancient African game. They are "
            "not there to be clever. They are there because a reader who has been "
            "told one of them, and believed it, deserves to be told where it came "
            "from.",
   "kindle": "Finally, one section at the back is given over to origin stories "
             "that are widely repeated and are not supported by anything: that "
             "hopscotch was Roman military drill, that Chinese checkers is "
             "Chinese, that kalah is an ancient African game. They are not there "
             "to be clever. They are there because a reader who has been told one "
             "of them, and believed it, deserves to be told where it came from."}
 ]
}

TONIGHT = {
 "id": "tonight",
 "title": "Tonight’s Game",
 "paragraphs": [
  {"print": "Find the row for the time you have and the column for the number of "
            "players. Every game appears in every square its ranges touch, with "
            "the page it starts on. For age and difficulty, see the indexes at the "
            "back ({page:bm:index-culture}).",
   "kindle": "Find the row for the time you have and the column for the number of "
             "players. Every game appears in every square its ranges touch. For "
             "age and difficulty, see the indexes at the back."}
 ]
}

FAMILY_OPENERS = [
 {"family": "sowing", "numeral": "I", "title": "The Sowing Games",
  "standfirst": "A handful of seeds, a ring of pits, and the whole game decided "
                "by where the last one falls.",
  "paragraphs": [
   "This is the most widely spread single idea in the history of board games. "
   "From the Akan towns of Ghana to the Tamil country, from Buganda to Sri Lanka "
   "and the Malay peninsula, and across the Atlantic with the slave trade, people "
   "dig rows of pits, put counters in them, and play variations on one "
   "underlying game. The counters are seeds, pebbles, cowries, dried beans — "
   "anything small and identical. That last word matters: the pieces are "
   "identical, and while they sit on the board they belong to nobody.",
   "That single feature is what makes sowing different from everything else in "
   "this book. In a race game you move your piece. In a war game you move your "
   "piece and take theirs. Here you lift the entire contents of one pit and drop "
   "them one at a time into the pits that follow, and then you look at where the "
   "last one landed, because the last seed decides everything: whether you "
   "capture, whether you sow on, whether you have just handed your opponent a "
   "harvest.",
   "«fam_count_word_cap» of the family are printed here. Oware is the Akan game, "
   "and it is the one most people meet first. Oware and Ayoayo, the two-row games "
   "of West Africa, end a turn where the last seed falls. Elsewhere the sowing "
   "relays: in Gebeta from Ethiopia, Congkak from the Malay world and Olinda "
   "Keliya from Sri Lanka, a last seed in a loaded pit lifts that pit and sows "
   "on, and the Tamil game lifts the pit after the last seed instead, until the "
   "sowing runs into an empty pit. The four-row games of eastern and "
   "southern Africa — Bao la Kiswahili from the Swahili coast, the royal Omweso "
   "of Buganda, Hus and Mefuvha from the south — relay their sowing from pit to "
   "pit and capture from both of the opponent's rows. Bao is the most demanding "
   "game in this book, and the entry says why.",
   "You do not need a board. An egg box with a bowl at each end is a sowing "
   "board, and so is a row of pits scraped in earth, which is how most of these "
   "games have always been played. If you are teaching a child, teach Oware and "
   "teach it with real beans, because half of what makes the family work is that "
   "counting the seeds out one at a time is a pleasure in itself."
  ]},

 {"family": "hunt-siege", "numeral": "II", "title": "The Hunt and the Siege",
  "standfirst": "Two players, two different jobs. One side is few and strong; "
                "the other is many and weak.",
  "paragraphs": [
   "Nearly every game in this book is symmetrical: both players start with the "
   "same pieces and want the same thing. This family is the exception, and it is "
   "the reason the family exists. Here one player has a tiger, or a fox, or a "
   "king, or two leopards, and the other has a herd — twenty-four cattle, "
   "seventeen geese, a ring of besiegers. The strong side wins by eating or by "
   "escaping. The weak side wins by crowding, by walling the strong side in "
   "until it cannot move at all.",
   "The idea turns up everywhere and it does not seem to have travelled from one "
   "place. Tablut was written down in 1732 by a Swedish botanist travelling in "
   "Sápmi; fox-and-geese boards were cut into the cloister benches at Gloucester; "
   "Rimau-rimau was recorded in the Malay peninsula; Diviyan Keliya, the "
   "leopards-and-cattle game, is a Sri Lankan board with a triangle on every "
   "side. What they share is not an ancestor. It is a situation, and the "
   "situation is old enough and common enough that people keep making a game of "
   "it.",
   "Asymmetric games have a particular problem and you should know it before "
   "you sit down: they are usually not balanced. In most of them one side is "
   "easier to play well. The traditional answer is the right one. Play two games "
   "and swap sides, and the winner is whoever did better with the harder job. "
   "Several entries in this family say so on the page.",
   "They are also the most legible games in the book for a child. There is a "
   "hunter and there are animals, the goal is obvious from the shape of the "
   "board, and a six-year-old will understand the fox's problem in one move. "
   "Start with Fox and Geese, and let the child have the geese."
  ]},

 {"family": "race", "numeral": "III", "title": "The Race Home",
  "standfirst": "Throw, count, move. The oldest game in this book belongs to "
                "this family, and so do the oldest written rules.",
  "paragraphs": [
   "Senet boards were being made in Egypt around 3000 BC, and the Royal Game of "
   "Ur was buried in the royal graves of a Sumerian city around 2600 BC. We can "
   "play Ur because a Babylonian scribe, Itti-Marduk-balāṭu, wrote part of its "
   "rules on a tablet in 177 BC, and a modern scholar has pieced a game together "
   "from it; senet's rules are lost, and what you play is a reconstruction. Race "
   "games are also the family that changed least: throw something, count, move "
   "a piece towards home. A player from Ur would need about a minute to learn "
   "pachisi.",
   "What differs is the thing you throw, and it is worth noticing because it is "
   "the part of these games that dice replaced almost everywhere. Ur used "
   "four-sided pyramids. Senet used flat sticks. Yut Nori uses four split "
   "batons, and the best throw is the one in which all four land round side up. "
   "Ashta Kashte uses four cowrie shells and counts the mouths that land upward "
   "— and if none does, the throw is worth eight, the biggest number in the "
   "game. Set-dilth uses three staves thrown on a flat stone at the centre of a "
   "ring. None of these is a die and all of them are.",
   "The other difference is the track. Some are a single line you go up and "
   "come back down, some a spiral, some a ring, some a cross with four arms "
   "and a centre — and some, like Pachisi and Patolli, put two or four players "
   "on partly shared roads so that the race becomes a fight. Where a track is "
   "shared, landing on somebody sends them back, and the game stops being only "
   "a race.",
   "«fam_count_word_cap» games are printed here, which makes this, with the War "
   "Board, one of the two largest families in the book. If you want to see the "
   "whole idea at once, play Yut Nori and then Ur on the same evening. They were "
   "recorded two thousand years and more than four thousand miles apart, and "
   "they are plainly the same kind of game."
  ]},

 {"family": "territory", "numeral": "IV", "title": "The Line and the Territory",
  "standfirst": "You do not win by taking pieces. You win by an arrangement — "
                "three in a row, a wall round empty ground, or an opponent with "
                "nowhere left to go.",
  "paragraphs": [
   "Put three counters in a line and you have the smallest complete game there "
   "is. Put stones on the crossings of a go board and you have a game generally "
   "reckoned among the deepest ever devised. They are in the same family and the "
   "family is defined by what wins: not the destruction of the other side, but "
   "a shape.",
   "The small end of it is remarkably crowded. Achi in Ghana, Picaria in the "
   "Rio Grande pueblos, Nerenchi in Sri Lanka, Nine Men's Morris across medieval "
   "Europe — all of them are three-in-a-row games and all of them are "
   "different, because the interesting question is never how to make the line. "
   "It is what happens once both players have run out of pieces to place. Some "
   "let you slide to any neighbouring point; some let a player down to three "
   "pieces jump anywhere at all; Morris lets a completed line take an enemy "
   "piece off the board and so keeps the game moving. Pong Hau K'i and Mū "
   "Tōrere belong here for a different reason: there is no line to make, and "
   "you win by leaving your opponent with no move.",
   "The large end is Go, and this book prints it on nine lines rather than "
   "nineteen. That is an editorial decision and the entry says so: nine lines "
   "can be taught in two pages and every rule is the same on both. Nine-line go "
   "is a real game with its own literature, not a toy version.",
   "Between the two ends sits Dara, a Nigerian game in which rows made while "
   "the pieces are being placed do not count, and Gomoku, where five in a row "
   "wins and the first player is so strong that the tournament form, renju, "
   "forbids them certain shapes. Both are worth attention for the same reason: "
   "they show a game being repaired by its own players."
  ]},

 {"family": "war-board", "numeral": "V", "title": "The War Board",
  "standfirst": "Two equal sides, one goal, and the game is decided by what "
                "you take or trap.",
  "paragraphs": [
   "This family includes chess — not the chess you know, but six of its "
   "ancestors and cousins printed side by side: Chaturaji, the four-handed dice "
   "game of medieval India; Shatranj, the chess of the Abbasid world; Xiangqi "
   "from China with its river and its palace; Janggi from Korea; Sittuyin from "
   "Burma, where you arrange your own back pieces before play; and Shogi from "
   "Japan, where a captured piece changes sides and comes back.",
   "Reading them together does something a single chess book cannot. The pieces "
   "are recognisably the same pieces — a king, a counsellor, an elephant, a "
   "horse, a chariot, foot soldiers — and every culture that received the game "
   "kept some and rebuilt others. The horse is the one that survives almost "
   "everywhere, though China and Korea let it be blocked and Japan sends it "
   "forward only.",
   "The other half of the family is the capturing games. Alquerque, written "
   "down at the court of Alfonso X of Castile in 1283, is played on the "
   "twenty-five-point board with diagonals, and it is usually taken to be the "
   "parent of draughts. Fanorona from Madagascar stretches that board to "
   "forty-five points and captures by moving towards a line of enemies or away "
   "from it. Turkish Dama moves its pieces forward and sideways on a board of "
   "sixty-four squares and never diagonally at all. Three boards, three "
   "different answers to the question of what a capture is.",
   "One warning. Several of these games are long. Shogi and Xiangqi are "
   "hour-long games between people who know them, and neither is a good first "
   "game for a child. Start the family with Alquerque or Seega; both teach the "
   "shape of a capturing game in ten minutes."
  ]},

 {"family": "chance", "numeral": "VI", "title": "Chance and Scoring",
  "standfirst": "No track and no position to build. A throw or a hand decides, "
                "and the score is kept.",
  "paragraphs": [
   "This is the smallest family in the book, and the reason is worth stating at "
   "the front. Games of pure chance are overwhelmingly gambling games, and the "
   "interesting part of a gambling game is usually the stake rather than the "
   "play. Take the money out and a great many of them stop being games at all. "
   "This book keeps the play and leaves the stakes out wherever it prints such "
   "a game, and where that leaves nothing behind, the game is not printed.",
   "Two survive the test. Astragaloi is the knucklebone game of the classical "
   "world, played with the ankle bones of sheep and goats, which fall on four "
   "sides of very unequal likelihood — the Greeks and Romans knew exactly which "
   "throws were rare and named the best of them after Aphrodite. Tien Gow is a "
   "Chinese domino game of tricks, played with a ranking of tiles that has to "
   "be learned before the game makes sense and repays the learning.",
   "Chance games do something the rest of the book does not, and it is the "
   "reason the family is here rather than cut. At a throw of the bones every "
   "player at the table is genuinely equal, whatever their age. A seven-year-old "
   "cannot beat an adult at Xiangqi and can absolutely beat one at Astragaloi, "
   "and knows it. That is not a small thing at a family table, and it is why "
   "these games have outlived so many cleverer ones."
  ]},

 {"family": "boardless", "numeral": "VII", "title": "Games Without a Board",
  "standfirst": "Hands, voices, string, stones, and a line scratched on the "
                "ground. Nothing to buy and nothing to lose.",
  "paragraphs": [
   "The games in this part need no equipment at all, or only what is already "
   "lying about: a length of string, five pebbles, a horse chestnut, a piece of "
   "chalk, a shuttlecock. They are the games children teach each other, which "
   "means they are the games that have been collected least carefully and "
   "survive best. Jan-ken has been played in Japan since at least the middle of "
   "the nineteenth century, and older hand games of the same kind for a century "
   "before that, without anybody having to preserve it.",
   "String figures are made almost everywhere people have string, from the "
   "Arctic to Australia, but most are made by one player alone. Cat's cradle, in "
   "which two players take the loop off each other's hands, is a narrower thing: "
   "in 1906 it was known from China, Korea and Japan to the Philippines, Borneo "
   "and Europe, and the anthropologist A. C. Haddon thought it had come west from "
   "Asia, like the kite. Nobody has traced the route, and where this book cannot "
   "show a route it does not draw one.",
   "«fam_count_word_cap» games are printed. Jan-ken is the hand game much of "
   "the world now plays to decide who goes first; Morra is its loud Italian "
   "relative with a history back to Rome. Gonggi is the Korean five-stones game; "
   "Conkers is English and was collected in the 1890s; Hopscotch comes with more "
   "origin stories than evidence, and the entry keeps to the evidence. Mbube "
   "Mbube, from South Africa, takes its name from the Zulu word for lion, needs a "
   "ring of players and two blindfolds, and is the only game in this book played "
   "by ear: the ring chants faster as the lion closes in.",
   "These are also the games to reach for when the table is the wrong shape for "
   "a table game — a car, a queue, a waiting room, a beach. Nothing here has a "
   "piece that can be lost, because almost nothing here has a piece."
  ]},
]
