# -*- coding: utf-8 -*-
"""ÖN MADDE VE AİLE AÇILIŞLARI — Faz 6 teslimatı.

EDITORIAL_ARCHITECTURE § 1 ön maddeyi 14 sayfa, aile açılışlarını 7×2 sayfa
diye modeller. Faz 5 kapanışı ikisini de YAZILMAMIŞ olarak devretti.
"""

INTRO = {
 "id": "introduction",
 "title": "Why We Play",
 "paragraphs": [
  "Go into almost any English cathedral that was once a monastery and look "
  "down at the stone benches in the cloister. Somewhere along them, worn "
  "shallow by centuries of weather and hands, you will find a diagram: three "
  "squares inside one another, joined across the middle of each side. It is "
  "a merels board. Monks cut it into the seat where they were meant to sit "
  "in silence, and then they played on it. At Westminster Abbey the holes of "
  "the smaller game are exceptionally deep, which tells you how much use they "
  "got. In 1699 a church court on the Isle of Man punished two men for making "
  "nine holes with their knives after evening prayers.",

  "That is the first thing worth saying about games: people have always found "
  "the time. The second is stranger. The board those monks cut is the same "
  "board that Zuni players in New Mexico used for awithlaknannai, that Malay "
  "players build their tiger games on, and that grew, somewhere in medieval "
  "Spain, into the game we now call draughts. Nobody planned that. A shape "
  "with twenty-five points and a rule about jumping turns out to be one of "
  "the good ideas, and good ideas travel — or, just as often, get found again "
  "by somebody who never heard of the first person to find them.",

  "This book is arranged around that fact. It is not organised by country. "
  "A book organised by country teaches you geography: here is the India "
  "chapter, here is the Japan chapter, and here, at the back, is a chapter "
  "called Africa doing the work of fifty-four countries at once. Arranged "
  "that way, the most interesting thing about games is invisible. So the "
  "seven parts of this book are seven ideas about how a game can work, and "
  "each part collects the games that share the idea, wherever they are from. "
  "You will meet the sowing games first — a single mechanic that runs from "
  "Ghana to Sri Lanka to the Caribbean — and you will meet them together, "
  "which is the only way to see what they have in common and where they part.",

  "There are fifty-six games here, from thirty-nine cultures, and the oldest "
  "of them is about four thousand six hundred years old. That last number is "
  "not a flourish. It is the Royal Game of Ur, whose boards were buried in "
  "the graves of the city of Ur around 2600 BC and whose rules survive because "
  "a Babylonian scribe wrote them on a tablet almost two and a half thousand "
  "years later. We know how to play it. We do not know how to play a great "
  "many other games, and where that is the case this book says so on the page "
  "rather than filling the gap quietly.",

  "Fifty-six is also not a round number, and that is deliberate. A game got "
  "into this book only if a real source could be opened and a complete set of "
  "rules read out of it: how the board is set up, who moves first, what a "
  "legal move is, how you win, and how the game ends. Where a source turned "
  "out to describe a board without describing the play — which happens more "
  "often than you would think — the game was left out. Seven of the games "
  "here are marked as reconstructed, which means the record is real but "
  "incomplete and the book has closed a gap on the evidence available. Those "
  "seven say so in their own text, in the place where you would need to know.",

  "What you do with the book is play. Every game is a two-page spread so that "
  "the book lies open on the table and nobody has to turn a page in the middle "
  "of a turn. Every game lists what it needs in things you already own: "
  "buttons, coins, dried beans, a sheet of paper, a pencil. Almost none of "
  "them needs anything bought. The board templates at the back are drawn full "
  "size for a photocopier, which is why the book is the shape it is.",

  "One last thing. Play is the oldest evidence we have of people doing "
  "something for no reason but the doing of it. The oldest boards in this book "
  "were made by people whose language we can barely read and whose gods we "
  "know only by their statues, and what those boards tell us is that they sat "
  "down opposite one another and argued about a rule. You are about to do the "
  "same thing. That is the whole of it."
 ]
}

HOWTO = {
 "id": "how-to-use",
 "title": "How to Use This Book",
 "paragraphs": [
  "Every game gets two facing pages and always in the same order, so that "
  "after the second or third game you stop reading the layout and start "
  "reading the game.",
 ],
 "sections": [
  {"heading": "The strip at the top",
   "text": "Players, time, age, materials, difficulty. The age is the age at "
           "which a child can hold the whole game in their head, not the age "
           "at which they can push a piece around; a six-year-old can play "
           "Ashta Kashte properly and will lose Go badly. The time is for one "
           "game between two people who know the rules."},
  {"heading": "Materials and substitution",
   "text": "What the game is traditionally played with, and what you can use "
           "instead. Buttons for pieces, coins for throwing sticks, dried "
           "beans and lentils for two colours of stone, an egg box for a "
           "mancala board. Nothing in this book requires a purchase. Where a "
           "substitution changes the feel of the game, the text says so."},
  {"heading": "The numbered rules",
   "text": "Setup, then how a turn goes, then how pieces move and take, then "
           "how you win and how the game ends. Each numbered line is one "
           "action. They are written flat and dry on purpose: a rule you have "
           "to read twice at the table is a broken rule."},
  {"heading": "Three questions",
   "text": "Every game answers the same three: what happens on a draw, what "
           "happens if nobody can move, and what happens when somebody plays "
           "an illegal move. These are the three arguments that actually "
           "break out, and a book that leaves them to the table has not "
           "finished its job. Where the source does not settle a question, "
           "the book rules on it and says plainly that the ruling is ours."},
  {"heading": "An example turn",
   "text": "One real turn, played out. It is usually the turn that shows the "
           "one rule people get wrong."},
  {"heading": "Variants and your first game",
   "text": "Variants are other recorded forms of the same game, not "
           "inventions. Your first game is a reduced version to start with — "
           "a smaller board, fewer pieces, a shorter goal. It is the "
           "fastest way to teach the game to somebody who has not read the "
           "page, and with children it is usually the right place to begin."},
  {"heading": "Sources",
   "text": "At the foot of the second page, in small type: the work, the "
           "edition, and the pages the rules came from. Where a game is "
           "marked reconstructed, the notice sits in the body of the entry "
           "and not in a footnote, because it changes how you should read "
           "everything above it."},
  {"heading": "At the back",
   "text": "Full-size board templates for the photocopier, a materials guide, "
           "a glossary of the terms this book uses for mechanics, a "
           "bibliography, three indexes — by culture, by number of players, "
           "and by time and age — and one page listing the game origin "
           "stories that are commonly repeated and are not true."}
 ]
}

FAMILIES_MAP = {
 "id": "seven-families",
 "title": "The Seven Families",
 "paragraphs": [
  "Games are sorted here by what they do, not by where they come from. Seven "
  "ideas cover almost everything people have played on a board or a floor. "
  "The boundaries between them are not decorative: each family has a rule for "
  "what belongs in it and a rule for what does not, and a few games sit close "
  "to a border and are placed with an explanation.",
  "The test that matters is mechanical. A sowing game and a race game can "
  "look identical on the table — pieces going round a circuit — but in a race "
  "one piece travels and in sowing a handful is distributed and no piece has "
  "an identity at all. That difference changes every decision a player makes, "
  "so it is the difference the book sorts on."
 ],
 "table": [
  {"n": "I", "name": "The Sowing Games",
   "idea": "A handful of seeds is distributed one to a hollow; where the last "
           "seed lands decides what happens.",
   "test": "The seeds belong to nobody while they are on the board."},
  {"n": "II", "name": "The Hunt and the Siege",
   "idea": "Two unequal sides with two different goals: few and strong against "
           "many and weak.",
   "test": "The two sides are not trying to do the same thing."},
  {"n": "III", "name": "The Race Home",
   "idea": "Pieces travel a fixed track towards a goal, and a lot, throw or "
           "cast decides how far.",
   "test": "One piece moves, and the distance is not chosen."},
  {"n": "IV", "name": "The Line and the Territory",
   "idea": "You win by an arrangement: a line of three, an enclosed area, a "
           "completed connection.",
   "test": "Capture is a consequence of the arrangement, not the aim."},
  {"n": "V", "name": "The War Board",
   "idea": "Two symmetrical sides, the same goal, and capture is a move you "
           "choose to make.",
   "test": "Both players could win the same way."},
  {"n": "VI", "name": "Chance and Nerve",
   "idea": "A cast decides, and there is no track and no developing position.",
   "test": "The decision is whether to risk it, not where to go."},
  {"n": "VII", "name": "Games Without a Board",
   "idea": "Nothing is needed but hands, voices, string, stones, or a mark "
           "scratched on the ground.",
   "test": "There is no board and no casting instrument."}
 ],
 "closing": "One family is much smaller here than the others. Chance and Nerve "
            "has three entries, because a great many games of pure chance are "
            "gambling games and this book rewrites gambling as scoring "
            "wherever it appears — and a gambling game with the betting taken "
            "out is very often no game at all. Where that rewriting has "
            "happened, the entry says so."
}

SOURCES_NOTE = {
 "id": "on-sources",
 "title": "On Sources, and What This Book Does Not Know",
 "paragraphs": [
  "Every game in this book carries a citation, and the citation names the "
  "pages the rules were read from. That sounds like an ordinary thing for a "
  "reference book to do. It is not: a great deal of what is published about "
  "traditional games repeats a rule set that nobody has traced back to "
  "anything, and the repetition is what makes it look reliable.",
  "So the test used here is narrow. A source counts if it was opened, if the "
  "page was read, and if the rules on that page are complete enough to play "
  "from. Where a source turned out to name a game without describing it — "
  "Murray on Tapatan, for instance, who gives a line and a citation and no "
  "rules — the game is not in this book. Where a source gives a board and no "
  "play, the same. That is why the number of games here is fifty-six and not "
  "a hundred: the missing games are missing because the evidence for them "
  "could not be opened, not because they were not interesting.",
  "Seven games are marked reconstructed. It means the record is genuine but "
  "has a hole in it, and the book has filled the hole with the best available "
  "reasoning rather than leaving the game unplayable. The notice appears in "
  "the entry itself and says which part is reconstructed. A book that "
  "reconstructs quietly is not a reference book.",
  "Some of the games here also have a rule that no source supplies at all — "
  "most often the draw. Traditional play does not always define one, because "
  "traditional play has a room full of people who settle it. Where the book "
  "supplies such a rule it says so in the same sentence, so that you can "
  "overrule it. You are allowed to. Every game in here was changing while it "
  "was being recorded, and it will change again on your table.",
  "Finally, one page at the back is given over to origin stories that are "
  "widely repeated and are not supported by anything: that hopscotch was "
  "Roman military drill, that Chinese Checkers is Chinese, that kubb is a "
  "Viking game. They are not there to be clever. They are there because a "
  "reader who has been told one of them, and believed it, deserves to be told "
  "where it came from."
 ]
}

FAMILY_OPENERS = [
 {"family": "sowing", "numeral": "I", "title": "The Sowing Games",
  "standfirst": "A handful of seeds, a ring of hollows, and the whole game "
                "decided by where the last one falls.",
  "paragraphs": [
   "This is the most widely spread single idea in the history of board games. "
   "From the Akan towns of Ghana to the Tamil country, from Buganda to Sri "
   "Lanka to the Philippines and across the Atlantic with the slave trade, "
   "people dig a double row of holes, put counters in them, and play the same "
   "underlying game. The counters are seeds, pebbles, cowries, dried beans, "
   "goat droppings, anything small and identical. That last word matters: the "
   "pieces are identical, and while they sit on the board they belong to "
   "nobody.",
   "That single feature is what makes sowing different from everything else "
   "in this book. In a race game you move your piece. In a war game you move "
   "your piece and take theirs. Here you lift the entire contents of one hole "
   "and drop them one at a time into the holes that follow, and then you look "
   "at where the last one landed, because the last seed decides everything: "
   "whether you capture, whether you go again, whether you have just handed "
   "your opponent a harvest.",
   "Five of the family are printed here. Oware is the Akan game, and it is the "
   "one most people meet first. Bao la Kiswahili from the Swahili coast is the "
   "hardest game in this book by some distance; it is played competitively, "
   "the opening is studied, and it has a rule about a house that keeps its "
   "seeds. Omweso is the royal game of Buganda, played on four rows rather "
   "than two. Olinda Keliya and Pallanguzhi come from Sri Lanka and the Tamil "
   "country, and both use a rule the African games do not: the sowing "
   "continues, lap after lap, until it happens to end in an empty hole.",
   "You do not need a board. An egg box with a bowl at each end is a mancala "
   "board, and so are twelve holes scraped in earth, which is how most of "
   "these games have always been played. If you are teaching a child, teach "
   "Oware and teach it with real beans, because half of what makes the family "
   "work is that counting the seeds out one at a time is a pleasure in itself."
  ]},

 {"family": "hunt-siege", "numeral": "II", "title": "The Hunt and the Siege",
  "standfirst": "Two players, two different jobs. One side is few and strong; "
                "the other is many and weak.",
  "paragraphs": [
   "Nearly every game in this book is symmetrical: both players start with the "
   "same pieces and want the same thing. This family is the exception, and it "
   "is the reason the family exists. Here one player has a tiger, or a fox, or "
   "a king, or two leopards, and the other has a herd — twenty-four men, "
   "seventeen geese, sixteen besiegers. The strong side wins by eating. The "
   "weak side wins by crowding, by walling the strong side in until it cannot "
   "move at all.",
   "The idea turns up everywhere and it does not seem to have travelled from "
   "one place. Tablut was written down in 1732 by a Swedish botanist who went "
   "north into Sápmi looking for plants; Fox and Geese was cut into the "
   "benches of English cloisters; Rimau-rimau is played on cloth in the Malay "
   "peninsula with the lines worked in red; Demala Diviyan Keliya is a Sri "
   "Lankan board of leopards and cattle. What they share is not an ancestor. "
   "It is a situation, and the situation is old enough and common enough that "
   "people keep making a game of it.",
   "Asymmetric games have a particular problem and you should know it before "
   "you sit down: they are usually not balanced. In most of them one side is "
   "easier to play well, and in several the herd wins if it plays a solid "
   "wall and never gets greedy. The traditional answer is the right one. Play "
   "two games and swap sides, and the winner is whoever did better with the "
   "harder job. Several entries in this family say so on the page.",
   "They are also the most legible games in the book for a child. There is a "
   "hunter and there are animals, the goal is obvious from the shape of the "
   "board, and a six-year-old will understand the tiger's problem in one "
   "move. Start with Fox and Geese, and let the child have the geese."
  ]},

 {"family": "race", "numeral": "III", "title": "The Race Home",
  "standfirst": "Cast, count, move. The oldest complete rules we possess "
                "belong to this family.",
  "paragraphs": [
   "The Royal Game of Ur was buried in the graves of a Sumerian city around "
   "2600 BC, and we can play it because a Babylonian astronomer named "
   "Itti-Marduk-balatu wrote the rules on a tablet in 177 BC, two and a half "
   "thousand years after the boards were made. That tablet is why this family "
   "opens the oldest window in the book. Race games are also the family that "
   "changed least: cast something, count the number, move a piece towards "
   "home. A player from Ur would need about a minute to learn Pachisi.",
   "What differs is the casting instrument, and it is worth noticing because "
   "it is the part of these games that dice replaced almost everywhere. Ur "
   "used four-sided pyramids. Senet used flat sticks. Yut Nori uses four split "
   "batons, and a throw of all four flat is worth more than any of the "
   "numbers. Ashta Kashte uses four cowrie shells and counts the mouths that "
   "land upward — and if none of them does, the throw is worth eight, the "
   "biggest number in the game. Zohn Ahl uses marked staves thrown against a "
   "stone. None of these is a die and all of them are.",
   "The other difference is the track. Some are a single line you go up and "
   "come back down, some are a spiral, some are a cross with four arms and a "
   "centre, and some — Pachisi, Patolli — put two or four players on partly "
   "shared roads so that the race becomes a fight. Where a track is shared, "
   "landing on somebody sends them home, and the game stops being a race and "
   "becomes an argument about position.",
   "Twelve games are printed here, which makes this the second largest family "
   "in the book. If you want to see the whole idea at once, play Yut Nori and "
   "then Ur on the same evening. They are four thousand years and five "
   "thousand miles apart and they are recognisably the same game."
  ]},

 {"family": "territory", "numeral": "IV", "title": "The Line and the Territory",
  "standfirst": "You do not win by taking pieces. You win by an arrangement — "
                "three in a row, or a wall around empty ground.",
  "paragraphs": [
   "Put three counters in a line and you have the smallest complete game there "
   "is. Put a hundred and eighty-one stones on a board of three hundred and "
   "sixty-one crossings and you have Go, which is generally reckoned the "
   "deepest. They are in the same family and the family is defined by what "
   "wins: not the destruction of the other side, but a shape.",
   "The small end of it is remarkably crowded. Achi in Ghana, Picaria among "
   "the Tewa, Nerenchi in Sri Lanka, Pong Hau K'i in Canton, Nine Men's "
   "Morris across medieval Europe — all of them are three-in-a-row games and "
   "all of them are different, because the interesting question is never how "
   "to make the line. It is what happens once both players have run out of "
   "pieces to place. Some let you slide to any adjacent point; some let a "
   "player down to three pieces jump anywhere at all; Morris lets a completed "
   "line take an enemy piece off the board and so keeps the game moving.",
   "The large end is Go, and this book prints it on nine lines rather than "
   "nineteen. That is an editorial decision and the entry says so: nineteen "
   "lines cannot be taught in two pages and nine can, and every rule is "
   "identical on both. Nine-line Go is a real game with its own literature, "
   "not a toy version.",
   "Between the two ends sits Dara, a Nigerian game where you may not make a "
   "line during the placing phase at all, and Gomoku, where five in a row wins "
   "and the first player is so strong that the modern rules forbid him three "
   "of his best openings. Both are worth attention for the same reason: they "
   "show a game being repaired by its own players. A rule that forbids the "
   "winning move is a rule somebody added after losing too often."
  ]},

 {"family": "war-board", "numeral": "V", "title": "The War Board",
  "standfirst": "Two equal sides, one goal, and taking a piece is something "
                "you choose to do.",
  "paragraphs": [
   "This is the largest family in the book and the one most readers will "
   "recognise, because chess is in it — not the chess you know, but four of "
   "its ancestors and cousins printed side by side: Chaturanga from India, "
   "Shatranj from the Abbasid caliphate, Xiangqi from China with its river "
   "and its palace, Janggi from Korea, Sittuyin from Burma where you set your "
   "own pieces up however you like, and Shogi from Japan where a captured "
   "piece changes sides and comes back.",
   "Reading them together does something a single chess book cannot. The "
   "pieces are the same pieces — a king, a counsellor, an elephant, a horse, "
   "a chariot, foot soldiers — and every culture that received the game kept "
   "the horse exactly as it was and rebuilt everything else. The horse's move "
   "is the one thing that never changes from India to Japan. Whatever the "
   "original game was, that move was the good part.",
   "The other half of the family is the jumping games, and they descend from "
   "the twenty-five-point board that opens this section: Alquerque, brought "
   "into Spain with the Moors and written down at the court of Alfonso X in "
   "1283. Play it and you are playing the parent of draughts. Then play "
   "Fanorona from Madagascar, where you capture by moving towards a line of "
   "enemies or away from them, and Turkish Dama, where pieces move forward "
   "and sideways and never diagonally at all. The same board, three different "
   "answers to the question of what a capture is.",
   "One warning. Several of these games are long. Shogi and Xiangqi are "
   "hour-long games between people who know them, and neither is a good first "
   "game for a child. Start the family with Alquerque or Hasami Shogi; both "
   "teach the shape of a capturing game in ten minutes."
  ]},

 {"family": "chance", "numeral": "VI", "title": "Chance and Nerve",
  "standfirst": "No track, no position, no plan. The only decision is whether "
                "to take the risk.",
  "paragraphs": [
   "This is the smallest family in the book, and the reason is worth stating "
   "at the front. Games of pure chance are overwhelmingly gambling games, and "
   "the interesting part of a gambling game is usually the stake rather than "
   "the play. Take the money out and a great many of them stop being games at "
   "all. This book rewrites betting as scoring wherever it appears, and where "
   "that rewriting leaves nothing behind, the game is not printed.",
   "Three survive the test. Astragaloi is the knucklebone game of the classical "
   "world, played with the ankle bones of sheep, which fall on four sides of "
   "unequal probability — the Greeks and Romans knew perfectly well which "
   "throws were rare and named the best one after Venus. Set-dilth is a White "
   "Mountain Apache stave game. Tien Gow is a Cantonese domino game with a "
   "ranking of tiles that has to be learned before the game makes sense.",
   "Chance games do something the rest of the book does not, and it is the "
   "reason the family is here rather than cut. They are the only games in "
   "which every player at the table is genuinely equal, whatever their age. A "
   "seven-year-old cannot beat an adult at Xiangqi and can absolutely beat one "
   "at Astragaloi, and knows it. That is not a small thing at a family table, "
   "and it is why these games have outlived so many cleverer ones.",
   "The nerve in the family name is not decoration either. In every one of "
   "these games the real decision is whether to throw again, and the person "
   "who always throws again loses in the long run to the person who knows "
   "when to stop."
  ]},

 {"family": "boardless", "numeral": "VII", "title": "Games Without a Board",
  "standfirst": "Hands, voices, string, stones, and a line scratched on the "
                "ground. Nothing to buy and nothing to lose.",
  "paragraphs": [
   "The games in this part need no equipment at all, or need only what is "
   "already lying about: a length of string, five pebbles, a horse chestnut, a "
   "piece of chalk. They are the games children teach each other, which means "
   "they are the games that have been collected the least carefully and "
   "survive the best. Nobody had to preserve Jan-ken. It preserved itself, in "
   "playgrounds, for centuries.",
   "The family is built on an observation rather than a claim. Cat's Cradle is "
   "played with a loop of string in Japan, in the Arctic, in the Pacific, in "
   "West Africa and across Europe, and the figures are often recognisably the "
   "same. It is tempting to explain that by diffusion. The honest position is "
   "that a loop of string and ten fingers is a small enough system that people "
   "keep arriving at the same figures independently, and where this book "
   "cannot show a route it does not draw one.",
   "Seven games are printed. Jan-ken is the hand game the world plays to "
   "decide who goes first, and it is genuinely Japanese, recorded in that form "
   "in 1895. Gonggi is the Korean five-stones game; Conkers is English and was "
   "collected in the 1890s; Hopscotch is older than any of the stories told "
   "about it and none of those stories is true. Mbube Mbube is Zulu, needs "
   "six to twenty players and a blindfold, and is the only game in this book "
   "that gets louder the better it goes.",
   "These are also the games to reach for when the table is the wrong shape "
   "for a table game — a car, a queue, a waiting room, a beach. Nothing here "
   "has a piece that can be lost, because nothing here has a piece."
  ]}
]
