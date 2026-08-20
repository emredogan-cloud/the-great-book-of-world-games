# -*- coding: utf-8 -*-
"""FAZ 6 KAPAK VE A+ İSTEMLERİ — metin katmanı.

⚠ SAYI YOK. Bütün ölçüler `build_prompt_library.py` tarafından ÖLÇÜLEN
kapak geometrisinden basılır. Bir isteme elle yazılmış piksel değeri,
sırt değiştiği anda yalancı olur.
"""

NO_TEXT_BLOCK = [
    "NO TEXT of any kind, in any language or script.",
    "NO TITLE. NO SUBTITLE. NO AUTHOR NAME. NO PUBLISHER NAME.",
    "NO ISBN. NO BARCODE. NO PRICE. NO LOGO. NO EMBLEM. NO WATERMARK.",
    "NO TYPOGRAPHY, NO LETTERING, NO CALLIGRAPHY, NO SIGNAGE.",
    "NO invented, decorative or 'alien' writing systems.",
    "NO numerals, NO dates, NO captions, NO labels, NO legends.",
    "NO signature and NO artist mark anywhere in the frame.",
    "If any glyph-like mark appears, it is a defect: the artwork is rejected "
    "and regenerated. All lettering is applied afterwards, as vector type, "
    "by the production pipeline.",
]

AVOID_BLOCK = [
    "Avoid a generic 'tribal collage' — no undifferentiated mass of motifs "
    "standing in for whole continents.",
    "Avoid generic fantasy: no dragons, no wizards, no glowing runes, no "
    "magic particles.",
    "Avoid random cultural mash-ups: objects from different traditions must "
    "not be fused into one invented artefact.",
    "Avoid sacred, funerary or restricted objects, and anything that reads as "
    "a ritual item rather than a game.",
    "Avoid stereotypical exoticism: no 'mysterious East', no colonial "
    "curiosity-cabinet framing, no people posed as specimens.",
    "Avoid video-game styling: no HUD, no neon, no chrome, no lens flare, no "
    "3D render sheen.",
    "Avoid children's cartoon clichés: no rounded mascot shapes, no primary "
    "colour blocking, no googly-eyed pieces.",
    "Avoid photorealistic human faces. Hands are permitted; faces are not.",
]

COVER_01 = {
    "id": "COVER-01",
    "title": "COVER OPTION 01 — THE WORLD GAME TABLE",
    "slug": "cover-option-01-world-game-table",
    "concept": (
        "A single continuous overhead still life: one large table, seen from "
        "directly above, on which the game boards and pieces of many "
        "traditions have been laid out and arranged by a careful hand. It "
        "should read as a museum study table photographed for a catalogue, "
        "not as a shop window. The objects are real, worn, and specific."),
    "direction": [
        "Viewpoint: directly overhead, flat-lay, very slight perspective at "
        "the far edge so the table reads as a physical object.",
        "Surface: a dark, aged wooden table top, close-grained, matte, with "
        "the faint marks of long use. It should feel like furniture, not "
        "like a backdrop.",
        "Objects, arranged in loose groups with real space between them: a "
        "carved two-row mancala board with rounded hollows and small seeds "
        "spilling from one of them; a folded dark cloth with a lined grid "
        "worked into it in red thread, with small pebble pieces on the "
        "intersections; a heavy square wooden board of nested squares with "
        "turned wooden men; four flat split reeds and a handful of cowrie "
        "shells; a set of astragali (sheep ankle bones), yellowed with age; "
        "a rolled reed mat with a cross-shaped track marked on it and small "
        "beehive-shaped pieces; a stack of thin bone or ivory dominoes; a "
        "loop of string lying slack.",
        "The objects must be recognisably different in material and "
        "craftsmanship — carved wood, fired clay, woven cloth, cut stone, "
        "bone, seed, shell. Material variety is the argument the image is "
        "making.",
        "Light: a single soft directional light from the upper left, as in a "
        "museum photographic studio. Long, soft shadows that model the "
        "carving. No specular highlights, no rim lighting.",
        "Palette: restrained and warm — aged wood browns, bone white, "
        "unbleached linen, deep indigo cloth, oxidised brass, one accent of "
        "worked red thread. Ink-and-earth, not saturated.",
        "Finish: fine editorial illustration with a printmaker's discipline — "
        "clean edges, controlled texture, a faint plate-like grain over the "
        "whole image. It should survive being printed at 300 dpi in a POD "
        "process on uncoated stock.",
    ],
    "composition": [
        "THIS IS ONE CONTINUOUS ARTWORK ACROSS THE WHOLE WRAP. It is not "
        "three panels. The table runs unbroken from the far left edge to the "
        "far right edge; the spine crosses it like a fold in the cloth, and "
        "nothing is composed to line up with the fold.",
        "The RIGHT THIRD of the image (the front cover) carries the strongest "
        "single object group and the darkest, calmest area of table in its "
        "upper half. That upper half must be almost empty — a broad expanse "
        "of dark wood — because the title is set there afterwards.",
        "The LOWER RIGHT area, across roughly the bottom sixth, is also kept "
        "quiet: the author name is set there.",
        "The CENTRE STRIP, where the spine falls, must be low-contrast and "
        "carry no important object. Anything crossing it will be split in "
        "half by the fold and part of it will be lost into the hinge.",
        "The LEFT THIRD (the back cover) is the quietest region of all. Its "
        "middle band must be broad, dark and near-empty so that a paragraph "
        "of body text can be set directly on it with no panel behind it. Keep "
        "the lower right corner of that third completely clear of objects: "
        "Amazon prints the barcode there.",
        "Read the image at thumbnail size before accepting it. At 120 pixels "
        "wide the front third must still read as 'a table of old games'. If "
        "it becomes a brown smear, the object group is too fine and must be "
        "made larger and fewer.",
    ],
}

COVER_02 = {
    "id": "COVER-02",
    "title": "COVER OPTION 02 — THE BOARD THAT IS A MAP",
    "slug": "cover-option-02-board-that-is-a-map",
    "concept": (
        "A stylised world map drawn in the language of game boards. The "
        "continents are not painted; they are constructed out of the lines, "
        "points, hollows and tracks that games are played on, so that the "
        "whole world reads as one enormous board. Where a region has a game, "
        "the board geometry of that game is what the land is made of."),
    "direction": [
        "Base: an equal-area world map, land only, in a single deep ink tone "
        "on a warm pale ground. No oceans drawn as water — the sea is simply "
        "the empty paper.",
        "Construction: each landmass is built from board geometry rather than "
        "coastline fill. A ruled lattice of points and connecting lines "
        "across one region; a double row of round hollows following the "
        "shape of another; nested concentric squares with joined mid-sides "
        "over another; a cross-shaped track; a long single-file track of "
        "small marks; a dense fine grid of intersections. The geometry must "
        "be drawn accurately — real lattices, evenly spaced, not scribbled "
        "texture.",
        "Connection: fine ruled lines run between regions where a game "
        "travelled, like the rhumb lines of a portolan chart. They are thin, "
        "sparse and purposeful — six or eight of them, not a web.",
        "Scattered along and beside the lines, drawn at a larger scale than "
        "the map and casting a soft shadow onto it, a small number of real "
        "physical pieces: three or four seeds, two turned wooden men, a "
        "cowrie shell, a split reed, one flat stone. They sit ON the map, "
        "as if a game were being played across the world.",
        "Visual language: archival and restrained — the discipline of an "
        "engraved plate in a nineteenth-century atlas. Fine line, controlled "
        "hatching, a faint impression of the plate edge and paper tooth.",
        "Palette: two inks and the paper. A deep blue-black for the "
        "linework, one warm oxide red used sparingly for the travel lines "
        "and one or two pieces, and the unbleached paper for everything "
        "else.",
        "No modern cartographic furniture: no graticule labels, no scale bar, "
        "no compass rose with letters, no country borders, no place names, "
        "no legend box.",
    ],
    "composition": [
        "ONE CONTINUOUS ARTWORK ACROSS THE WHOLE WRAP. The map runs "
        "unbroken across back, spine and front. The spine is a fold across "
        "the ocean, not a border.",
        "Position the map so that the front cover (the right third) is "
        "dominated by one clear, legible landmass built of a strong, "
        "large-scale lattice — something that reads instantly at thumbnail "
        "size — with open sea above it.",
        "The upper half of the front third must be open sea: empty paper. "
        "The title is set there.",
        "The bottom sixth of the front third: also open sea. The author name "
        "is set there.",
        "Keep the spine strip empty of land and of travel lines.",
        "The back cover third should be mostly open sea with one region at "
        "its top edge, leaving a broad clear field in the middle for a "
        "paragraph of body text set directly on the paper tone. The lower "
        "right corner of that third stays completely empty for the barcode.",
        "Test at thumbnail: at 120 pixels wide it must read as 'a map made "
        "of game boards'. If the lattices dissolve into grey, make fewer "
        "regions and draw them at a coarser scale.",
    ],
}

APLUS_MODULES = [
    {"id": "APLUS-01", "n": "01", "name": "HERO / WORLD OF GAMES",
     "slug": "aplus-01-hero-world-of-games",
     "module": "Standard Image Header with Text",
     "w": 970, "h": 600,
     "purpose": "The first thing a shopper sees under the buy box. It has one "
                "job: say 'this is a serious, beautiful, usable reference "
                "book about the games of the world' before a single word is "
                "read.",
     "prompt": [
         "A wide overhead band of a dark wooden table with three game boards "
         "laid across it, spaced apart, lit softly from the upper left: a "
         "carved two-row mancala board with seeds, a nested-squares board "
         "with turned wooden men, and a lined cloth board with pebble pieces "
         "on its intersections.",
         "The objects sit in the LEFT HALF and the CENTRE of the frame. The "
         "RIGHT THIRD is an unbroken expanse of dark table with nothing on "
         "it.",
         "Warm restrained palette: aged wood, bone, unbleached linen, one "
         "thread of oxide red. Museum-catalogue lighting; soft modelling "
         "shadows; no glare.",
     ],
     "safe": "Right third (approximately the rightmost 320 px) must be quiet, "
             "even and low-contrast. Amazon overlays the module heading and "
             "body text there.",
     },
    {"id": "APLUS-02", "n": "02", "name": "CULTURAL DIVERSITY",
     "slug": "aplus-02-cultural-diversity",
     "module": "Standard Image & Text Overlay",
     "w": 970, "h": 600,
     "purpose": "Show that the book's reach is real and specific, not a "
                "marketing claim. Different materials, different hands, "
                "different craft traditions — one frame.",
     "prompt": [
         "Six game objects from clearly different traditions, arranged in two "
         "rows of three on a pale unbleached linen ground, each isolated with "
         "generous space around it, photographed from directly above like a "
         "museum accession plate.",
         "The six: a carved wooden mancala board with rounded hollows; a dark "
         "cloth with a red-worked lattice and small stone pieces; a set of "
         "four split reed casting sticks beside three cowrie shells; a "
         "shallow clay board with a cross-shaped track; a group of yellowed "
         "sheep ankle bones; a slack loop of cord lying in a simple figure.",
         "The point of the image is MATERIAL DIFFERENCE: wood, cloth, reed, "
         "clay, bone, fibre must each be unmistakably itself.",
         "Even, shadowless documentary light. No props, no hands, no "
         "background scenery.",
     ],
     "safe": "Keep the top band (approximately the top 120 px) and the bottom "
             "band (approximately the bottom 120 px) free of objects: the "
             "overlay text sits there.",
     },
    {"id": "APLUS-03", "n": "03", "name": "HOW THE BOOK WORKS",
     "slug": "aplus-03-how-the-book-works",
     "module": "Standard Single Image & Sidebar",
     "w": 300, "h": 400,
     "purpose": "Answer the one question that decides the purchase: can I "
                "actually play from this? Show the book open, flat, in use.",
     "prompt": [
         "A tall portrait view, from slightly above and to one side, of a "
         "large-format hardback lying OPEN AND FLAT on a plain table, so that "
         "both facing pages are visible as one working surface.",
         "The pages are rendered as pale abstracted print texture only — grey "
         "tone blocks standing in for paragraphs and a clean geometric board "
         "diagram on the right-hand page. NO READABLE TEXT, no words, no "
         "letterforms, not even suggested ones.",
         "Beside the book, on the table, a small handful of loose playing "
         "pieces and two buttons, as if a game were about to start.",
         "Plain background, soft daylight from the left, gentle shadow under "
         "the book. Warm neutral palette.",
     ],
     "safe": "The sidebar text is a separate Amazon field and does not sit on "
             "the image. Keep a small quiet border on all four sides so the "
             "image crops cleanly.",
     },
    {"id": "APLUS-04", "n": "04", "name": "TYPES OF GAMES",
     "slug": "aplus-04-types-of-games",
     "module": "Standard Four Image & Text",
     "w": 220, "h": 220,
     "purpose": "Make the book's organising idea visible in four squares: the "
                "book sorts games by how they work, not by where they are "
                "from. FOUR SEPARATE IMAGES ARE NEEDED, one per square.",
     "prompt": [
         "FOUR separate square images, identical in treatment so that they "
         "read as a set: same pale ground, same overhead viewpoint, same soft "
         "even light, same scale of object, same warm restrained palette.",
         "Square A — SOWING: a short section of a carved two-row board, three "
         "hollows visible, seeds distributed unevenly between them and one "
         "seed caught mid-drop above a hollow.",
         "Square B — THE HUNT: a lined lattice board with one large dark "
         "piece surrounded at a distance by several small pale pieces closing "
         "in on it.",
         "Square C — THE RACE: a curved section of a marked track with two "
         "pieces on it, one clearly ahead of the other, and four split reed "
         "casting sticks lying beside the track.",
         "Square D — THE LINE: a fine grid of intersections with pale and "
         "dark stones placed on them, three of one colour forming an obvious "
         "straight line.",
         "Each square must be legible at 220 pixels: one idea, large, "
         "centred, with clear space around it.",
     ],
     "safe": "Keep an even margin of at least 20 px inside each square; "
             "Amazon crops these to a rounded frame in some layouts.",
     },
    {"id": "APLUS-05", "n": "05", "name": "PLAY / FAMILY / DISCOVERY",
     "slug": "aplus-05-play-family-discovery",
     "module": "Standard Image & Light Text Overlay",
     "w": 970, "h": 300,
     "purpose": "The emotional module. This is a book that ends with people "
                "sitting down together, and this is the only image that says "
                "so.",
     "prompt": [
         "A wide, low, letterbox view across a wooden table at close range, "
         "shot from table height so the board is at eye level.",
         "In the centre, a simple lined board part-way through a game, pieces "
         "unevenly placed. At the left and right edges of the frame, only "
         "HANDS: an adult hand resting beside the board, a child's hand "
         "reaching in to move a piece. NO FACES, no bodies, no clothing "
         "detail beyond a cuff.",
         "Warm late-afternoon light raking across the table from the right, "
         "long soft shadows, a faint bloom of dust in the air.",
         "Shallow depth of field: the board and the two hands are sharp; the "
         "room behind dissolves into warm neutral tone with no recognisable "
         "objects.",
     ],
     "safe": "The centre band (approximately the middle 400 px horizontally) "
             "must stay simple and even in tone: the overlay text is set "
             "across it.",
     },
    {"id": "APLUS-06", "n": "06", "name": "THE COMPLETE COLLECTION",
     "slug": "aplus-06-complete-collection",
     "module": "Standard Image Header with Text",
     "w": 970, "h": 600,
     "purpose": "The closing module. It should feel like a survey — the whole "
                "range of the book in one frame — and it should make the "
                "scale feel earned rather than claimed.",
     "prompt": [
         "A wide overhead grid of many small game objects laid out in "
         "regular rows on a pale unbleached ground, like a museum drawer of "
         "accessioned pieces: turned wooden men, seeds, cowrie shells, flat "
         "stones, split reeds, bone dice, small clay counters, a coiled cord.",
         "Regular spacing, straight rows, every object isolated with air "
         "around it. Variation lives in the objects, not in the layout.",
         "The RIGHT THIRD is left as empty ground, with no objects at all.",
         "Even documentary light, soft contact shadows, warm restrained "
         "palette. Nothing dramatic; the impression should be of an ordered "
         "and complete collection.",
     ],
     "safe": "Right third (approximately the rightmost 320 px) reserved for "
             "the module heading and body text.",
     },
]
