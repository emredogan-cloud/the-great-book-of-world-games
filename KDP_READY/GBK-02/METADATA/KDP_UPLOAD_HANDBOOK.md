# KDP UPLOAD HANDBOOK
## The Great Book of World Games

> **Generated file** — `04_BUILD/handoff.py`. Every number below is measured
> from the built artefacts. If you rebuild anything, rebuild this file.
>
> Generated at phase **6** · interior **258 pages** ·
> **63 games** · **42 cultures**

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
| Paperback | ✅ 258 pp | ✅ wrap PDF | **yes** |
| Hardcover | ✅ 258 pp | ✅ wrap PDF | **yes** |
| Kindle | ✅ EPUB 3 | ✅ 1600 × 2560 JPG | **yes** |
| A+ Content | copy ✅ 6 modules | ✅ 5 of 6 modules have art | **yes, 5 modules** |

---

## Blocking founder actions

- ⛔ **SUBTITLE-NEW-EDITION** — `metadata.subtitleRegisteredOnKdp`
  The verified subtitle (63 Games from 5,000 Years of Human Play — Rules, Boards and Stories from 42 Cultures, Ready to Play Tonight) differs from the one registered on the live KDP print records (63 Games from 4,600 Years of Human Play — Rules, Boards and Stories from 45 Cultures, Ready to Play Tonight). KDP locks a paperback/hardcover title and subtitle 72 hours after publication; the corrected files need a NEW EDITION with a new ISBN (or KDP support). Decide before uploading the print files.
- ⛔ **AI-QUESTIONNAIRE** — `founder.aiDisclosure`
  Under KDP's definitions the text of this book is AI-GENERATED (created by AI tools, then edited), not AI-assisted; most plates and the cover are AI-generated images. Re-answer the KDP AI content questions for every edition when uploading.
- ⛔ **AI-DECL** — `founder.aiDisclosure.founderConfirmed`
  The AI-generated content declaration is a legal statement and the choice is yours alone. The agent cannot make it. The facts you need are in `aiProductionFacts`.
- · **APLUS-ART** — 1 of 6 A+ module(s) missing artwork: APLUS-05. Copy is written and waiting; the project is uploadable today with the other 5 module(s). Prompts are in `07_ASSETS/IMAGE_PROMPT_LIBRARY.html`.

- · **PLAYTEST** — the release standard for this book is: *Pre-publication simulation and rule verification completed.* (Founder decision PLAYTEST-STANDARD-2026-09-19, 2026-09-19).
  It replaced: *At least one external human playtest per game, 100 games.* — of which **0** session(s) were ever recorded.
  No session may be recorded that did not happen. `fabricationIsProjectEndingOffence` stays true, `evidenceTypes` stays split, and if external human playtesting is ever run its records go in 01_SOURCE/playtests/ under the same rules as before. This decision lowers the RELEASE bar; it does not lower the EVIDENCE bar.

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
63 Games from 5,000 Years of Human Play — Rules, Boards and Stories from 42 Cultures, Ready to Play Tonight
```
(107 of 200 characters.)

⚠ The two numbers in this subtitle are measured, not chosen. The book
contains **63 games** from **42
cultures**. If you edit the subtitle, do not round them up.

### 5 · Author
*agent prepared* Primary author: **Emre Doğan**.

### 6 · Contributors
*agent prepared* None. Leave the contributor list empty — an empty contributor row will
block the form.

### 7 · Description
*agent prepared* Paste the description from
`06_REPORTS/tracked/metadata.json` → `description.text`
(2121 of 4000 characters).
It is written to read correctly as plain text; KDP's limited HTML is not
required.

### 8 · Publishing rights
**FOUNDER ACTION** Select: *I own the copyright and I hold the necessary publishing rights.*
*agent prepared* Basis: Kitabın metni bu proje için yazılmıştır. Kural kaynakları KAMUSAL ALAN eserlerdir ve alıntı değil KÜNYE olarak kullanılır; hiçbir kaynaktan blok metin aktarılmamıştır.

### 9 · Keywords
*agent prepared* Seven slots, one phrase each:

1. `traditional board games rules book`
2. `games from around the world`
3. `mancala oware rules`
4. `royal game of ur senet rules`
5. `go xiangqi shogi rules`
6. `family board games history`
7. `classroom games activity book`

### 10 · Categories
**FOUNDER ACTION** KDP now picks categories from its own tree. Choose three that match:
- GAMES & ACTIVITIES / Board — `GAM002000`
- REFERENCE / General — `REF000000`
- HISTORY / General — `HIS000000`

### 11 · Age and grade range
**FOUNDER ACTION** **Leave empty.** KDP yaş aralığı YALNIZCA çocuk kitabı olarak işaretlenen başlıklarda sorulur. Bu kitap bir aile başvuru cildidir ve çocuk kitabı olarak işaretlenMEZ — işaretlenirse yetişkin alıcı aramalarından düşer.

### 12 · ISBN
**FOUNDER ACTION** Select **Get a free KDP ISBN**. Current recorded value: `9798194063468`.
*agent prepared* No ISBN has been invented anywhere in this package. Once KDP assigns one,
write it into `project_config.json → founder.isbn.paperback` and rebuild: the
copyright page will then print the real number instead of `PENDING`.

### 13 · AI-generated content declaration
**FOUNDER ACTION** **This choice is yours and only yours.** The agent cannot make a legal
declaration on your behalf. The facts you need in order to answer:

- Text — The rules, the notes on each game and the front matter were researched and written with AI tools working from the printed sources named in each entry, under the author's direction. Each rule is cited to the page (or, for a modern codified ruleset, the section) it was read from; rulings the sources do not give are marked in the book as the book's own.
- Images — Most game plates and the cover art were generated with an image model and chosen one at a time; each AI plate is labelled 'AI-generated illustration' on its page. Plates that an invented image would misrepresent — the equipment of a game, or members of a living people — are public-domain or CC0 images, credited on the page and at the back. Two plates (Achi, Mū Tōrere) are board drawings made by 04_BUILD/boards.py. Board diagrams and full-size boards are NOT AI images: they are vector drawings made by 04_BUILD/boards.py from the positions written into each game's rules and checked by count.
- Translation — None. The text is written in English.

### 14 · Manuscript upload
*agent prepared* Upload:

```
08_OUTPUT/PAPERBACK/GreatBookOfWorldGames_interior_paperback.pdf
```
- 258 pages · trim 8.5 × 11 in
- no bleed · inside margin 0.7 in · outside 0.825 in
- all fonts embedded and subsetted (Source Serif 4 / Source Sans 3 / Cinzel (SIL OFL 1.1, embedded))
- SHA-256 `9f0aa934021de6a4ab75cf5e3b4a58f8486bc9d9b02e83d5224730034125375f`

**FOUNDER ACTION** Trim size in the KDP form: **8.5 x 11 in**.
Bleed: **No bleed**. Paper: **White**. Ink: **Black & white**.

### 15 · Cover upload
*agent prepared* Upload:

```
08_OUTPUT/PAPERBACK/GreatBookOfWorldGames_cover_paperback.pdf
```
- full wrap **17.8310 × 11.2500 in**, including
  0.125 in bleed on all four sides
- spine **0.5810 in**, computed from this exact page count
  (258 pages × 0.002252 in/page)
- artwork embedded at **5349 × 3375 px**
  (300 ppi); the cover is one raster image, its type included
- SHA-256 `f5f1a1fd61cccc9917ae280ad5db93d3a2137f84ff3b7d3551d5b6eb055c2815`

The cover is the Founder-approved final artwork. Its subtitle counts and its back
copy were re-set from the measured manuscript by `04_BUILD/cover_text_fix.py`
(EB Garamond, SIL OFL 1.1) — the only change made to the artwork; nothing was
redrawn or generated. Geometry: KDP paperback formula (pages × 0.002252 in; bleed + back + spine + front + bleed)

⚠ The barcode area (lower right of the back panel) carries a plain light plate.
**Do not place anything there** — Amazon prints the barcode itself.

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
63 Games from 5,000 Years of Human Play — Rules, Boards and Stories from 42 Cultures, Ready to Play Tonight
```
(107 of 200 characters.)

⚠ The two numbers in this subtitle are measured, not chosen. The book
contains **63 games** from **42
cultures**. If you edit the subtitle, do not round them up.

### 5 · Author
*agent prepared* Primary author: **Emre Doğan**.

### 6 · Contributors
*agent prepared* None. Leave the contributor list empty — an empty contributor row will
block the form.

### 7 · Description
*agent prepared* Paste the description from
`06_REPORTS/tracked/metadata.json` → `description.text`
(2121 of 4000 characters).
It is written to read correctly as plain text; KDP's limited HTML is not
required.

### 8 · Publishing rights
**FOUNDER ACTION** Select: *I own the copyright and I hold the necessary publishing rights.*
*agent prepared* Basis: Kitabın metni bu proje için yazılmıştır. Kural kaynakları KAMUSAL ALAN eserlerdir ve alıntı değil KÜNYE olarak kullanılır; hiçbir kaynaktan blok metin aktarılmamıştır.

### 9 · Keywords
*agent prepared* Seven slots, one phrase each:

1. `traditional board games rules book`
2. `games from around the world`
3. `mancala oware rules`
4. `royal game of ur senet rules`
5. `go xiangqi shogi rules`
6. `family board games history`
7. `classroom games activity book`

### 10 · Categories
**FOUNDER ACTION** KDP now picks categories from its own tree. Choose three that match:
- GAMES & ACTIVITIES / Board — `GAM002000`
- REFERENCE / General — `REF000000`
- HISTORY / General — `HIS000000`

### 11 · Age and grade range
**FOUNDER ACTION** **Leave empty.** KDP yaş aralığı YALNIZCA çocuk kitabı olarak işaretlenen başlıklarda sorulur. Bu kitap bir aile başvuru cildidir ve çocuk kitabı olarak işaretlenMEZ — işaretlenirse yetişkin alıcı aramalarından düşer.

### 12 · ISBN
**FOUNDER ACTION** Select **Get a free KDP ISBN**. Current recorded value: `9798194081950`.
*agent prepared* No ISBN has been invented anywhere in this package. Once KDP assigns one,
write it into `project_config.json → founder.isbn.hardcover` and rebuild: the
copyright page will then print the real number instead of `PENDING`.

### 13 · AI-generated content declaration
**FOUNDER ACTION** **This choice is yours and only yours.** The agent cannot make a legal
declaration on your behalf. The facts you need in order to answer:

- Text — The rules, the notes on each game and the front matter were researched and written with AI tools working from the printed sources named in each entry, under the author's direction. Each rule is cited to the page (or, for a modern codified ruleset, the section) it was read from; rulings the sources do not give are marked in the book as the book's own.
- Images — Most game plates and the cover art were generated with an image model and chosen one at a time; each AI plate is labelled 'AI-generated illustration' on its page. Plates that an invented image would misrepresent — the equipment of a game, or members of a living people — are public-domain or CC0 images, credited on the page and at the back. Two plates (Achi, Mū Tōrere) are board drawings made by 04_BUILD/boards.py. Board diagrams and full-size boards are NOT AI images: they are vector drawings made by 04_BUILD/boards.py from the positions written into each game's rules and checked by count.
- Translation — None. The text is written in English.

### 14 · Manuscript upload
*agent prepared* Upload:

```
08_OUTPUT/HARDCOVER/GreatBookOfWorldGames_interior_hardcover.pdf
```
- 258 pages · trim 8.25 × 11 in
- no bleed · inside margin 0.675 in · outside 0.6 in
- all fonts embedded and subsetted (Source Serif 4 / Source Sans 3 / Cinzel (SIL OFL 1.1, embedded))
- SHA-256 `54bc5448aa2ccb87aab1563ac8bc22ce1f08f77cff4d332f305084efd494041d`

**FOUNDER ACTION** Trim size in the KDP form: **8.25 x 11 in**.
Bleed: **No bleed**. Paper: **White**. Ink: **Black & white**.

### 15 · Cover upload
*agent prepared* Upload:

```
08_OUTPUT/HARDCOVER/GreatBookOfWorldGames_cover_hardcover.pdf
```
- full wrap **18.8450 × 12.4170 in**, including
  0.591 in wrap allowance on all four sides
- spine **0.7700 in**, **confirmed directly from KDP** — not computed from a formula (KDP Print Cover Calculator reading for 258 pages)
- artwork embedded at **5654 × 3725 px**
  (300 ppi); the cover is one raster image, its type included
- SHA-256 `a4ede697b14a6b18c5e37393eeb443966c3f168cad1fb647c346e80dc04a693a`

The cover is the Founder-approved final artwork. Its subtitle counts and its back
copy were re-set from the measured manuscript by `04_BUILD/cover_text_fix.py`
(EB Garamond, SIL OFL 1.1) — the only change made to the artwork; nothing was
redrawn or generated. Geometry: KDP Print Cover Calculator reading for 258 pages

⚠ The barcode area (lower right of the back panel) carries a plain light plate.
**Do not place anything there** — Amazon prints the barcode itself.

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
- 8843 KB · SHA-256 `a560f65f1c8851d73ad4c87f960fe1b98a140cb4f312adb1b72a950cde97a9ea`
- diagrams are embedded as **inline SVG**, so they stay sharp at any screen
  size and add almost nothing to the file size

**Why reflowable and not fixed-layout.** The print book's two-page spread is
an answer to a constraint that a scrolling screen does not have. Fixed layout
would squeeze an 8.5 × 11 spread onto a phone, lock the reader's font size and
break their accessibility settings, to preserve a promise that reflowing keeps
anyway: each game is one uninterrupted entry.

### 15 · Cover upload
*agent prepared* Upload:

```
08_OUTPUT/KINDLE/GreatBookOfWorldGames_cover_kindle.jpg
```
- **1600 × 2560 px** (Amazon's recommended 1:1.6), JPEG
- SHA-256 `b4d6ceb0f2236cb107f9eb6dd19b4735ecea9d4c1cb9ef15a079aeae98ea9594`
- the Founder-approved Kindle master (the front-cover artwork composed at 1:1.6),
  not the wrap — an ebook cover must not show a spine or a back panel
- title and author are part of the Founder's artwork; the subtitle counts were
  re-set from the measured manuscript by `04_BUILD/cover_text_fix.py`

⚠ Amazon evaluates Kindle covers by **pixel dimensions**, not DPI — there is
no physical print size for an eBook. The file's 300×300 dpi tag is a
compatibility label only. 1600 × 2560 comfortably clears Amazon's stated
minimum (1000 × 625) and matches its recommended 1.6:1 ratio.

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
*agent prepared* Processed and sized in `07_ASSETS/web/aplus/`. Ready modules:
**APLUS-01, APLUS-02, APLUS-03, APLUS-04, APLUS-06**.

⚠ **One module has no artwork: APLUS-05.** The
file delivered as `aplus-05-play-family-discovery.png` is, on inspection, the
**module 06** brief — rows of game objects on a pale ground with the right
third left clear. It was mapped to module 06 by content rather than by
filename. Module 05 (hands over a board, no faces) was not delivered, so the
uploadable A+ project is **5 modules**, not six. Its copy is written and
waiting if you generate the art later.

⚠ Module 04 was delivered as a single 2 × 2 composite. It was **split** into
four 220 × 220 squares by measuring the gutters — no pixels were invented.

⚠ The generated images contain **no text**. All wording goes in Amazon's own
fields, where it stays searchable and correctable.

### 6 · Title and body text
*agent prepared* Ready, and every number in them is measured against the book:

**APLUS-01 — HERO / WORLD OF GAMES**

- Title (33 chars): 63 games. 42 cultures. One table.
- Body (364 chars): This is a reference book you play from, not one you only read. Every game opens with its board beside its rules, so the book lies open on the table while you play. Every rule set names the work it was read from, with the pages or, for a modern rulebook, the section, and where a record is incomplete the book says so on the page instead of filling the gap quietly.

**APLUS-02 — CULTURAL DIVERSITY**

- Title (51 chars): Sorted by how they work, not by where they are from
- Body (382 chars): Most collections file games by country, which teaches geography and hides the interesting part. This one files them by mechanism, so the sowing games of Ghana, Sri Lanka and Buganda sit together and you can see what they share and where they part. 42 cultures are represented, from ancient Mesopotamia to the Sámi, and each entry names the culture precisely rather than a continent.

**APLUS-03 — HOW THE BOOK WORKS**

- Title (46 chars): Everything you need for one game, in one place
- Body (412 chars): Players, time, age, materials and difficulty at the top. What to use instead of what — buttons, coins, dried beans, an egg box. Numbered rules, one action to a line. A worked turn drawn on the board. Then three questions every table actually argues about: what happens on a draw, what happens if nobody can move, and what happens when somebody plays an illegal move. Almost nothing in this book has to be bought.

**APLUS-04 — TYPES OF GAMES**

- Title (18 chars): 7 families of play
- Body (281 chars): Sowing · Hunt and siege · Race home · Line and territory · War board · Chance and scoring · Games without a board. Each family opens with a portrait of the idea behind it, and each has a written rule for what belongs in it and what does not. The boundaries are argued, not assumed.

**APLUS-05 — PLAY / FAMILY / DISCOVERY**

- Title (43 chars): For a table with an adult and a child at it
- Body (278 chars): Ages are given per game and they mean something: the age at which a player can hold the whole game in their head. Every entry has a first game to start with — often a smaller board or fewer pieces — which is the fastest way to teach a game to somebody who has not read the page.

**APLUS-06 — THE COMPLETE COLLECTION**

- Title (44 chars): Full-size boards, a glossary and the indexes
- Body (395 chars): The back of the book is the part that gets used. Full-size boards to photocopy, in the print editions. A list of what to gather for a games kit. A glossary of the terms the rules use. Sources for every game. An index of every game under every name it goes by, and indexes by culture, age and difficulty. And a page of game origin stories that are widely repeated and not supported by the record.


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
