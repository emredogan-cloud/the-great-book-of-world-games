# KDP UPLOAD HANDBOOK
## The Great Book of World Games

> **Generated file** — `04_BUILD/handoff.py`. Every number below is measured
> from the built artefacts. If you rebuild anything, rebuild this file.
>
> Generated at phase **6** · interior **160 pages** ·
> **56 games** · **39 cultures**

---

## How to read this document

Every step is marked. **FOUNDER ACTION** means you must do it in the Amazon KDP panel;
the agent has no access to your account and has not touched it. *agent prepared* means the
value or file is already prepared and only needs pasting or uploading.

**Nothing in this package has been uploaded, submitted, previewed, priced or
published.** No proof copy has been ordered.

---

## Status at a glance

| Format | Interior | Cover | Ready to upload |
|---|---|---|---|
| Paperback | ✅ 160 pp | ⛔ artwork missing | interior yes, cover no |
| Hardcover | ✅ 160 pp | ⛔ artwork missing | interior yes, cover no |
| Kindle | ✅ EPUB 3 | ⛔ artwork missing | manuscript yes, cover no |
| A+ Content | copy ✅ 6 modules | ⛔ 9 images missing | no |

---

## Blocking founder actions

- ⛔ **A6** — `founder.authorBio`
  `founder.authorBio` is empty. KDP asks for an author biography, and on a sibling title KDP rejected a placeholder biography as template text (12 August 2026). Write a real one before publishing.
- ⛔ **AI-DECL** — `founder.aiDisclosure.founderConfirmed`
  The AI-generated content declaration is a legal statement and the choice is yours alone. The agent cannot make it. The facts you need are in `aiProductionFacts`.
- · **ISBN-paperback** — `founder.isbn.paperback`
  KDP assigns a free ISBN. Once it does, write it here and rebuild: the copyright page will print the real number instead of PENDING. No ISBN has been invented anywhere in this package.
- · **ISBN-hardcover** — `founder.isbn.hardcover`
  KDP assigns a free ISBN. Once it does, write it here and rebuild: the copyright page will print the real number instead of PENDING. No ISBN has been invented anywhere in this package.

- ⛔ **COVER-ART** — no cover artwork exists. Prompts are ready in
  `07_ASSETS/IMAGE_PROMPT_LIBRARY.html`.
- ⛔ **APLUS-ART** — no A+ artwork exists. Prompts are in the same file.
- ⛔ **PLAYTEST** — the project's own playability standard requires at least
  one external human playtest per game before a game may be called locked.
  Zero sessions have been recorded. The book does not claim to have been
  playtested, and the subtitle's promise rests on rule completeness rather
  than on tested play. Publishing before playtesting is your decision to
  make, and it should be a decision rather than an oversight.

---

# PAPERBACK

### 1 · KDP Bookshelf
**FOUNDER ACTION** Sign in at kdp.amazon.com → **Bookshelf** → **+ Create** →
**Create Paperback**.
Do not start a new title if you have already created one for the other print
format — use **+ Create Hardcover**
underneath the existing title so the two editions stay linked on one detail
page.

### 2 · Book Details — language
*agent prepared* Language: **en**.

### 3 · Title
*agent prepared* Paste exactly, with no trailing space:

```
The Great Book of World Games
```
(29 characters of the 200 allowed.)

### 4 · Subtitle
*agent prepared* Paste exactly:

```
56 Games from 4,600 Years of Human Play — Rules, Boards and Stories from 39 Cultures, Ready to Play Tonight
```
(107 of 200 characters.)

⚠ The two numbers in this subtitle are measured, not chosen. The book
contains **56 games** from **39
cultures**. If you edit the subtitle, do not round them up.

### 5 · Author
*agent prepared* Primary author: **Emre Doğan**.

### 6 · Contributors
*agent prepared* None. Leave the contributor list empty — an empty contributor row will
block the form.

### 7 · Description
*agent prepared* Paste the description from
`06_REPORTS/tracked/metadata.json` → `description.text`
(1981 of 4000 characters).
It is written to read correctly as plain text; KDP's limited HTML is not
required.

### 8 · Publishing rights
**FOUNDER ACTION** Select: *I own the copyright and I hold the necessary publishing rights.*
*agent prepared* Basis: Kitabın metni bu proje için yazılmıştır. Kural kaynakları KAMUSAL ALAN eserlerdir ve alıntı değil KÜNYE olarak kullanılır; hiçbir kaynaktan blok metin aktarılmamıştır.

### 9 · Keywords
*agent prepared* Seven slots, one phrase each:

1. `traditional board games book`
2. `world games rules and history`
3. `family games for adults and kids`
4. `mancala backgammon go rules`
5. `history of board games reference`
6. `games from around the world`
7. `classroom games activity book`

### 10 · Categories
**FOUNDER ACTION** KDP now picks categories from its own tree. Choose three that match:
- GAMES & ACTIVITIES / Board — `GAM002000`
- REFERENCE / General — `REF000000`
- HISTORY / General — `HIS000000`

### 11 · Age and grade range
**FOUNDER ACTION** **Leave empty.** KDP yaş aralığı YALNIZCA çocuk kitabı olarak işaretlenen başlıklarda sorulur. Bu kitap bir aile başvuru cildidir ve çocuk kitabı olarak işaretlenMEZ — işaretlenirse yetişkin alıcı aramalarından düşer.

### 12 · ISBN
**FOUNDER ACTION** Select **Get a free KDP ISBN**. Current recorded value: `PENDING — KDP-PROVIDED ISBN`.
*agent prepared* No ISBN has been invented anywhere in this package. Once KDP assigns one,
write it into `project_config.json → founder.isbn.paperback` and rebuild: the
copyright page will then print the real number instead of `PENDING`.

### 13 · AI-generated content declaration
**FOUNDER ACTION** **This choice is yours and only yours.** The agent cannot make a legal
declaration on your behalf. The facts you need in order to answer:

- Text — Text was drafted with AI assistance and edited by the author; every rule set is traced to a named printed source at page level.
- Images — Cover and A+ artwork are generated externally by the author; interior diagrams are drawn deterministically by the project's own code from data, not generated.
- Translation — None. The commercial text is written directly in English.

### 14 · Manuscript upload
*agent prepared* Upload:

```
08_OUTPUT/PAPERBACK/GreatBookOfWorldGames_interior_paperback.pdf
```
- 160 pages · trim 8.5 × 11.0 in
- no bleed · inside margin 0.5 in · outside 0.5 in
- all fonts embedded and subsetted (Liberation Serif, SIL OFL 1.1)
- SHA-256 `f834a260a24d5ec4441774b8a05a97826b457f979e48d4ceaaedc716b5208672`

**FOUNDER ACTION** Trim size in the KDP form: **8.5 x 11.0 in**.
Bleed: **No bleed**. Paper: **White**. Ink: **Black & white**.

### 15 · Cover upload
**FOUNDER ACTION** ⛔ **NOT READY.** No cover artwork exists yet. Generate it from
`07_ASSETS/IMAGE_PROMPT_LIBRARY.html`, drop the raw files into
`07_ASSETS/raw/cover/`, then run `04_BUILD/cover_artwork.py --upscale`
and `04_BUILD/covers.py`.

*agent prepared* The geometry is already computed from this exact page count:
- spine **0.3603 in** (160 pages ×
  0.002252 in/page)
- full wrap **17.6103 × 11.2500 in**
- at 300 ppi that is **5283 × 3375 px**
- spine text is allowed
  (KDP threshold 79 pages)

⚠ If you rebuild the interior and the page count changes, this spine is wrong
and the cover will not fit. Rebuild the cover after the interior, never before.

### 16 · Previewer
**FOUNDER ACTION** Open the KDP Previewer and work through
`08_OUTPUT/KDP_PREVIEWER_CHECKLIST.md`. The agent cannot run the Previewer
and does not claim to have done so.

### 17 · Pricing
*agent prepared* Modelled list price: **$22.99**.
**FOUNDER ACTION** Enter it and check the royalty KDP shows you against
`06_REPORTS/editions.json`. If they differ, KDP's printing cost has changed
and the model needs re-running, not overriding.

### 18 · Territories
**FOUNDER ACTION** All territories (worldwide rights).

### 19 · Royalty
**FOUNDER ACTION** Select the **60%** royalty plan (list price is above $9.99).
*agent prepared* KDP Select / Kindle Unlimited: **do NOT enrol**.
KU'ya GİRİLMEZ: 256 sayfalık tam okuma ≈ 1,23 $, ciltsiz telif 8,44 $. 6,9 kat kayıp.

### 20 · Final review
**FOUNDER ACTION** Read the whole preview once more. Confirm the copyright page shows the
real ISBN if one has been assigned, and that the author biography is present
if you have entered one.

### 21 · Publish
**FOUNDER ACTION** Press Publish. **The agent has not done this and cannot do it.**

# HARDCOVER

### 1 · KDP Bookshelf
**FOUNDER ACTION** Sign in at kdp.amazon.com → **Bookshelf** → **+ Create** →
**Create Hardcover**.
Do not start a new title if you have already created one for the other print
format — use **+ Create Paperback**
underneath the existing title so the two editions stay linked on one detail
page.

### 2 · Book Details — language
*agent prepared* Language: **en**.

### 3 · Title
*agent prepared* Paste exactly, with no trailing space:

```
The Great Book of World Games
```
(29 characters of the 200 allowed.)

### 4 · Subtitle
*agent prepared* Paste exactly:

```
56 Games from 4,600 Years of Human Play — Rules, Boards and Stories from 39 Cultures, Ready to Play Tonight
```
(107 of 200 characters.)

⚠ The two numbers in this subtitle are measured, not chosen. The book
contains **56 games** from **39
cultures**. If you edit the subtitle, do not round them up.

### 5 · Author
*agent prepared* Primary author: **Emre Doğan**.

### 6 · Contributors
*agent prepared* None. Leave the contributor list empty — an empty contributor row will
block the form.

### 7 · Description
*agent prepared* Paste the description from
`06_REPORTS/tracked/metadata.json` → `description.text`
(1981 of 4000 characters).
It is written to read correctly as plain text; KDP's limited HTML is not
required.

### 8 · Publishing rights
**FOUNDER ACTION** Select: *I own the copyright and I hold the necessary publishing rights.*
*agent prepared* Basis: Kitabın metni bu proje için yazılmıştır. Kural kaynakları KAMUSAL ALAN eserlerdir ve alıntı değil KÜNYE olarak kullanılır; hiçbir kaynaktan blok metin aktarılmamıştır.

### 9 · Keywords
*agent prepared* Seven slots, one phrase each:

1. `traditional board games book`
2. `world games rules and history`
3. `family games for adults and kids`
4. `mancala backgammon go rules`
5. `history of board games reference`
6. `games from around the world`
7. `classroom games activity book`

### 10 · Categories
**FOUNDER ACTION** KDP now picks categories from its own tree. Choose three that match:
- GAMES & ACTIVITIES / Board — `GAM002000`
- REFERENCE / General — `REF000000`
- HISTORY / General — `HIS000000`

### 11 · Age and grade range
**FOUNDER ACTION** **Leave empty.** KDP yaş aralığı YALNIZCA çocuk kitabı olarak işaretlenen başlıklarda sorulur. Bu kitap bir aile başvuru cildidir ve çocuk kitabı olarak işaretlenMEZ — işaretlenirse yetişkin alıcı aramalarından düşer.

### 12 · ISBN
**FOUNDER ACTION** Select **Get a free KDP ISBN**. Current recorded value: `PENDING — KDP-PROVIDED ISBN`.
*agent prepared* No ISBN has been invented anywhere in this package. Once KDP assigns one,
write it into `project_config.json → founder.isbn.hardcover` and rebuild: the
copyright page will then print the real number instead of `PENDING`.

### 13 · AI-generated content declaration
**FOUNDER ACTION** **This choice is yours and only yours.** The agent cannot make a legal
declaration on your behalf. The facts you need in order to answer:

- Text — Text was drafted with AI assistance and edited by the author; every rule set is traced to a named printed source at page level.
- Images — Cover and A+ artwork are generated externally by the author; interior diagrams are drawn deterministically by the project's own code from data, not generated.
- Translation — None. The commercial text is written directly in English.

### 14 · Manuscript upload
*agent prepared* Upload:

```
08_OUTPUT/HARDCOVER/GreatBookOfWorldGames_interior_hardcover.pdf
```
- 160 pages · trim 8.25 × 11.0 in
- no bleed · inside margin 0.625 in · outside 0.5 in
- all fonts embedded and subsetted (Liberation Serif, SIL OFL 1.1)
- SHA-256 `c615a6fb8c651d76a2af11f36552dfe5dd6998afd40cc8ebd0256e002f93e5ff`

**FOUNDER ACTION** Trim size in the KDP form: **8.25 x 11.0 in**.
Bleed: **No bleed**. Paper: **White**. Ink: **Black & white**.

### 15 · Cover upload
**FOUNDER ACTION** ⛔ **NOT READY.** No cover artwork exists yet. Generate it from
`07_ASSETS/IMAGE_PROMPT_LIBRARY.html`, drop the raw files into
`07_ASSETS/raw/cover/`, then run `04_BUILD/cover_artwork.py --upscale`
and `04_BUILD/covers.py`.

*agent prepared* The geometry is already computed from this exact page count:
- spine **0.4600 in** (160 pages ×
  0.0025 in/page + board allowance)
- full wrap **17.2100 × 11.2500 in**
- at 300 ppi that is **5163 × 3375 px**
- spine text is allowed
  (KDP threshold 79 pages)

⚠ If you rebuild the interior and the page count changes, this spine is wrong
and the cover will not fit. Rebuild the cover after the interior, never before.

### 16 · Previewer
**FOUNDER ACTION** Open the KDP Previewer and work through
`08_OUTPUT/KDP_PREVIEWER_CHECKLIST.md`. The agent cannot run the Previewer
and does not claim to have done so.

### 17 · Pricing
*agent prepared* Modelled list price: **$34.99**.
**FOUNDER ACTION** Enter it and check the royalty KDP shows you against
`06_REPORTS/editions.json`. If they differ, KDP's printing cost has changed
and the model needs re-running, not overriding.

### 18 · Territories
**FOUNDER ACTION** All territories (worldwide rights).

### 19 · Royalty
**FOUNDER ACTION** Select the **60%** royalty plan (list price is above $9.99).
*agent prepared* KDP Select / Kindle Unlimited: **do NOT enrol**.
KU'ya GİRİLMEZ: 256 sayfalık tam okuma ≈ 1,23 $, ciltsiz telif 8,44 $. 6,9 kat kayıp.

### 20 · Final review
**FOUNDER ACTION** Read the whole preview once more. Confirm the copyright page shows the
real ISBN if one has been assigned, and that the author biography is present
if you have entered one.

### 21 · Publish
**FOUNDER ACTION** Press Publish. **The agent has not done this and cannot do it.**

# KINDLE / EBOOK

### 1 · KDP Bookshelf
**FOUNDER ACTION** **+ Create** → **Create eBook**, or **+ Create Kindle eBook** beneath the
existing print title so the editions stay linked.

### 2–13 · Book details
*agent prepared* Identical to the paperback: same title, subtitle, author, description,
keywords and categories. **FOUNDER ACTION** The AI declaration is asked again and is again
yours to answer.

**FOUNDER ACTION** ISBN: an eBook does **not** need one. Leave it blank.

### 14 · Manuscript upload
*agent prepared* Upload:

```
08_OUTPUT/KINDLE/GreatBookOfWorldGames.epub
```
- EPUB 3, **reflowable**
- 215 KB · SHA-256 `ddfcad43ba5cba101f8ac2b23914c032c0d5d0e4616c1137895fcfe61040ecf8`
- diagrams are embedded as **inline SVG**, so they stay sharp at any screen
  size and add almost nothing to the file size

**Why reflowable and not fixed-layout.** The print book's two-page spread is
an answer to a constraint that a scrolling screen does not have. Fixed layout
would squeeze an 8.5 × 11 spread onto a phone, lock the reader's font size and
break their accessibility settings, to preserve a promise that reflowing keeps
anyway: each game is one uninterrupted entry.

### 15 · Cover upload
**FOUNDER ACTION** ⛔ **NOT READY.** Kindle requires a cover image (1.6:1 ratio, at least
1000 px on the shorter side; 2560 × 1600 px is the recommended size). It will
be produced from the same artwork as the print cover. No placeholder cover has
been inserted.

### 16 · Previewer
**FOUNDER ACTION** Use the Kindle Previewer. Check in particular: the diagrams at the
smallest font size, the numbered rule lists, and the three-question blocks.

### 17 · Pricing
*agent prepared* Modelled list price **$11.99**.
**FOUNDER ACTION** Select the **70%** royalty option — the price sits inside the
$2.99–$9.99… band check KDP shows you, and if it does not, take the 35% plan
rather than dropping the price to fit.

### 18–21 · Territories, royalty, review, publish
**FOUNDER ACTION** As for print. KDP Select enrolment: **do not enrol** — see the note above.

# A+ CONTENT

### 1 · Marketing
**FOUNDER ACTION** Bookshelf → the title's **…** menu → **Marketing** (or Author Central →
A+ Content, depending on the account).

### 2 · A+ Content
**FOUNDER ACTION** **Create A+ Content** → give the project an internal name, e.g.
`GBWG-EN-v1`. This name is not shown to shoppers.

### 3 · Module creation
*agent prepared* Six modules are specified, in this order:

| # | Module type | Image | Size |
|---|---|---|---|
| 01 | Standard Image Header with Text | `aplus-01-hero-world-of-games.png` | 970 × 600 px |
| 02 | Standard Image & Text Overlay | `aplus-02-cultural-diversity.png` | 970 × 600 px |
| 03 | Standard Single Image & Sidebar | `aplus-03-how-the-book-works.png` | 300 × 400 px |
| 04 | Standard Four Image & Text | `aplus-04-types-of-games-a.png`, `aplus-04-types-of-games-b.png`, `aplus-04-types-of-games-c.png`, `aplus-04-types-of-games-d.png` | 220 × 220 px |
| 05 | Standard Image & Light Text Overlay | `aplus-05-play-family-discovery.png` | 970 × 300 px |
| 06 | Standard Image Header with Text | `aplus-06-complete-collection.png` | 970 × 600 px |

### 4 · Module type
**FOUNDER ACTION** Pick each module type exactly as listed above. If Amazon has renamed or
retired one, choose the closest and note the change — do not force an image
into a module with a different aspect ratio.

### 5 · Image upload
**FOUNDER ACTION** ⛔ **NOT READY.** 9 images are missing. Generate them
from `07_ASSETS/IMAGE_PROMPT_LIBRARY.html`, put them in
`07_ASSETS/raw/aplus/`, then run `04_BUILD/aplus.py`.

⚠ The generated images contain **no text**. All wording goes in Amazon's own
fields, where it stays searchable and correctable.

### 6 · Title and body text
*agent prepared* Ready, and every number in them is measured against the book:

**APLUS-01 — HERO / WORLD OF GAMES**

- Title (33 chars): 56 games. 39 cultures. One table.
- Body (337 chars): This is a reference book you play from, not one you only read. Every game is set out across two facing pages so the book lies open on the table and nobody turns a page mid-turn. Every rule set names the work and the pages it was read from, and where a record is incomplete the book says so on the page instead of filling the gap quietly.

**APLUS-02 — CULTURAL DIVERSITY**

- Title (51 chars): Sorted by how they work, not by where they are from
- Body (368 chars): Most collections file games by country, which teaches geography and hides the interesting part. This one files them by mechanism, so the sowing games of Ghana, Sri Lanka and Buganda sit together and you can see what they share and where they part. 39 cultures are represented, from Sumer to the Sámi, and each entry names the culture precisely rather than a continent.

**APLUS-03 — HOW THE BOOK WORKS**

- Title (48 chars): Everything you need for one game, on one opening
- Body (410 chars): Players, time, age, materials and difficulty at the top. What to use instead of what — buttons, coins, dried beans, an egg box. Numbered rules, one action to a line. A board diagram drawn to scale. Then three questions every table actually argues about: what happens on a draw, what happens if nobody can move, and what happens when somebody plays an illegal move. Almost nothing in this book has to be bought.

**APLUS-04 — TYPES OF GAMES**

- Title (18 chars): 7 families of play
- Body (279 chars): Sowing · Hunt and siege · Race home · Line and territory · War board · Chance and nerve · Games without a board. Each family opens with a portrait of the idea behind it, and each has a written rule for what belongs in it and what does not. The boundaries are argued, not assumed.

**APLUS-05 — PLAY / FAMILY / DISCOVERY**

- Title (43 chars): For a table with an adult and a child at it
- Body (281 chars): Ages are given per game and they mean something: the age at which a player can hold the whole game in their head. Every entry ends with a shorter version to start with — a smaller board, fewer pieces — which is the fastest way to teach a game to somebody who has not read the page.

**APLUS-06 — THE COMPLETE COLLECTION**

- Title (45 chars): Board templates, a glossary and three indexes
- Body (391 chars): The back of the book is the part that gets used. Full-size board templates you can photocopy — the page size was chosen for exactly that. A materials guide. A glossary of the terms the book uses for mechanics. Sources for every game. Three indexes, by culture, by number of players, and by time and age. And one page listing the game origin stories that are widely repeated and are not true.


### 7 · Preview
**FOUNDER ACTION** Use A+ preview on both desktop and mobile. The right-hand third of the
header modules is where Amazon puts the text — check nothing important in the
artwork is hidden behind it.

### 8 · Submit
**FOUNDER ACTION** Submit for review. A+ content is moderated by Amazon.

### 9 · Moderation
**FOUNDER ACTION** Moderation usually takes up to seven days. The most common rejections are
claims that cannot be substantiated, contact details, and pricing or shipping
language. This copy has been scanned against
7 forbidden claim patterns and carries no
bestseller, award, testing or guaranteed-outcome claim. Every number in the
copy is checked against the book's measured values.

### 10 · Live verification
**FOUNDER ACTION** Once it is live, open the detail page as a shopper and confirm all six
modules render, in order, on desktop and on mobile.

---

## What the agent did not do

- did not sign in to Amazon
- did not upload any file
- did not run the KDP Previewer or the Kindle Previewer
- did not set a price, a territory or a royalty plan
- did not answer the AI-generated content declaration
- did not submit A+ content for moderation
- did not order a proof copy
- did not publish

Each of those is yours, and none of them is claimed as done anywhere in this
package.
