# KDP PREVIEWER CHECKLIST
## The Great Book of World Games

> **Generated file** — `04_BUILD/handoff.py`.
>
> The agent cannot run the Amazon KDP Previewer, and nothing in this project
> pretends otherwise. What follows is what the Previewer is likely to say, what
> it cannot be allowed to say, and the pages worth stopping on.

---

## The numbers you will be checking against

| | Paperback | Hardcover |
|---|---|---|
| Final page count | **160** | **160** |
| Trim | 8.5 × 11.0 in | 8.25 × 11.0 in |
| Bleed | none | none |
| Inside margin (gutter) | 0.55 in | 0.675 in |
| Outside margin | 0.5 in | 0.5 in |
| Top / bottom margin | 0.625 / 0.625 in | 0.625 / 0.625 in |
| Spine (from page count) | **0.3603 in** | **0.4600 in** |
| Full cover wrap | 17.6103 × 11.2500 in | 17.2100 × 11.2500 in |
| Fonts | Liberation Serif, embedded and subsetted | same |
| Raster images | none — every diagram is vector | same |

Measured ink margins in the built paperback — the closest any ink comes to the
trim edge, on any of the 160 pages:

- left **0.486 in** · right **0.486 in**
- top **0.361 in** · bottom **0.333 in**

KDP's own minimum without bleed is 0.25 in, so there is real headroom. If the
Previewer reports content outside the printable area, something changed after
this file was generated.

---

## Expected warnings, and which of them are fine

| What you may see | Is it a problem? |
|---|---|
| "Your cover has not been uploaded" | Yes — cover artwork does not exist yet. Expected. |
| Blank pages flagged | No. There are 18 deliberate blanks: a book of two-page spreads needs each game to start on a left-hand page, and part titles open on the right. |
| Low-resolution image warning | Would be a real problem. There are no raster images at all, so it should not appear. |
| Font not embedded | Would be a real problem. All four faces are embedded and subsetted; verified with `pdffonts`. |
| Page size mismatch | Would be a real problem. All 160 pages are exactly 8.5 × 11.0 in. |
| Text too close to the trim | Should not appear — see the measured margins above. |

---

## Pages worth stopping on

1. **The contents (pages 5–6).** Every page reference is generated from the
   built PDF, not from a model. Spot-check three entries against the pages they
   point to; if one is wrong they are all wrong and the build chain broke.
2. **Any game spread — for example pages 16–17.** Confirm the entry begins on
   the **left** page. Every one of the 56 games does; that
   is the whole architecture of the book and the one thing a layout change
   silently breaks.
3. **A spread with two diagrams — for example Alquerque, pages 88–89.** Confirm
   both diagrams sit on the right-hand page with the rules, and neither is
   clipped.
4. **The board templates (from page 140).**
   These are meant to survive a photocopier. Check the line weight is still
   visible at the smallest zoom the Previewer offers.
5. **The three indexes.** Pick a culture, follow it to the page, confirm the
   entry is there and the culture line at the top of the entry matches the
   index heading exactly.
6. **The copyright page.** It should say `PENDING — KDP-PROVIDED ISBN` until an
   ISBN is assigned. If it shows a number you did not enter, stop.

---

## Asset risks

- **No cover, in any format.** Paperback, hardcover and Kindle all need one and
  none exists. This is the single blocking gap.
- **Hardcover geometry is a hypothesis.** The spine above is computed from page
  count and a board allowance; KDP supplies a hardcover template that includes
  hinge and wrap allowances which cannot be derived. Download it and compare
  before generating hardcover artwork.
- **A+ images: 1 missing.**
- **Author biography is empty.** KDP rejected a placeholder biography on a
  sibling title. Write a real one before publishing.

---

## The cover — what to look at

| | paperback | hardcover |
|---|---|---|
| Full wrap | 17.6103 × 11.2500 in | 17.2100 × 11.2500 in |
| Spine | 0.3603 in | 0.4600 in |
| Artwork | 5283 × 3375 px @ 300 ppi | 5163 × 3375 px |
| Type | vector, not rasterised | same |

1. **The spine.** It is 0.360 in — a thin spine, and the title is set at
   8.75 pt to fit the part of the artwork that measured clean.
   In the Previewer, check the spine text is centred between the two folds and
   that no letter touches a fold. This is the single most common cover
   rejection.
2. **The barcode corner.** Lower right of the back panel is deliberately
   empty. Confirm the Previewer's barcode overlay lands on empty artwork and
   covers nothing.
3. **The title block.** Sits in the quietest measured band of the artwork.
   Check nothing in the map runs through a letter at full zoom.
4. **The back copy.** It sits over a feathered wash drawn from the artwork's
   own parchment tone. Check it reads as *paper*, not as a panel. If it looks
   like a box, say so and it will be softened.
5. **Bleed.** The artwork runs into all four bleed edges. Confirm no type is
   within 0.25 in of any trim edge.

---

## A+ content — what to look at

- **5 of 6 modules have artwork.** Module(s) without art:
  **APLUS-05**.
- The header modules keep their **right third clear** — that is where Amazon
  puts your text. Check on **mobile** as well as desktop; the crop differs.
- Module 04 is four separate 220 × 220 squares, split from one composite.
  Check the four read as a set.
- No A+ image contains a single character of text. If you see lettering in
  any of them, stop — it means the wrong file was uploaded.

---

## What you must decide, not check

- whether to publish before any external playtest has been run (zero sessions
  recorded)
- how to answer the AI-generated content declaration
- whether the hardcover ships at all in the first release
