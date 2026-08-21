# KDP GUTTER FORENSIC REPORT
## The Great Book of World Games

> Generated 2026-08-21 · triggered by a **real** Amazon KDP Print Previewer
> rejection, not a local QA finding. This document is the evidence trail:
> what KDP said, what was actually on the page, why, and what changed.
>
> **Real KDP evidence outranks local preflight.** Everything below was
> measured — page renders, pixel bounding boxes, source-level tracing —
> not assumed from a passing local gate.

---

## 1 · The exact KDP error

> *"Insufficient gutter. Books with 160 pages require at least 0.5"
> (12.700mm) for the gutter (inside margin) and at least 0.25" (6.35mm)
> for the outside, top and bottom margins."*
>
> **Flagged page: 159** (paperback interior).

## 2 · Page 159 — what is actually there

Page 159 is the **Invented Traditions** section (back matter, final
section before the closing blank pad). It is a right-hand (recto, odd)
page — the gutter is its **left** edge.

Rendered at 400 dpi and measured with the same method later built into
the fixed validator (`ImageChops.invert().getbbox()`, side-aware):

| | Measured (before fix) |
|---|---:|
| Left (gutter) ink distance | **0.4900 in** |
| Required (160 pages, 151–300 tier) | 0.5000 in |
| Shortfall | **0.0100 in** (≈ 0.25 mm) |

A 0.01 in shortfall is small — and real. It is exactly the class of
defect a coarse check will miss and a real print RIP will not.

### Root-cause trace

```
PAGE 159 → OBJECT → LAYOUT RULE → SOURCE → GENERATOR
```

- **Object.** The single leftmost ink pixel on the whole page sits at
  y ≈ 5.22–5.23 in, a 3-pixel-tall sliver — one glyph, not a paragraph
  block. Zoomed inspection identifies it precisely: the **opening curly
  quotation mark `'`** that begins the line *"'the Elephant moves in all
  directions as far as the driver pleases'"* (a direct quotation inside
  the "Invented Traditions" entry on the elephant's move in early Indian
  chess).
- **Layout rule.** `Layout.frame()` in `04_BUILD/interior.py` places the
  text frame's left edge at exactly `x = gutterPt` for a recto page —
  arithmetically correct, confirmed by comparing against pages 155 and
  157 (the two preceding index pages), which use the **same** 20 pt bold
  section-title style and measure **exactly** 0.5000 in with zero
  shortfall.
- **Source.** Liberation Serif's glyph design for U+2018 (LEFT SINGLE
  QUOTATION MARK) draws ink that extends measurably left of the
  character's nominal advance origin — a normal font-rendering fact, not
  a layout bug. The same effect was independently confirmed on a second,
  unrelated page (§ 3).
- **Generator.** `04_BUILD/interior.py`'s `geometry()` set the gutter to
  **exactly** the bare KDP legal minimum, with **zero rendering
  headroom**. Any glyph whose ink extends even slightly past its nominal
  origin has nothing to absorb it into.

### Second confirmed instance — the pattern generalizes

The document-wide sweep (§ 4) found the *same* magnitude of shortfall on
**page 15** (the Sowing Games family-opener). Its leftmost ink is a
single italic capital **"A"** (the standfirst *"A handful of seeds, a
ring of hollows..."*, style `GBSerif-I`). Italic letterforms carry the
same kind of small negative left-bearing in this font.

**Two different glyph classes (an opening quote mark, an italic capital)
independently produced the same class of failure.** This rules out a
one-glyph, one-page patch as the correct fix — the failure mode is
systemic (zero rendering headroom against a hard legal floor), not a
single typo.

## 3 · Root cause — one sentence

**The interior typesetting placed body content at exactly the bare KDP
gutter minimum, with no safety margin for ordinary font-rendering
overshoot, so any page whose leading glyph happened to have negative
left-side-bearing (quote marks, italics) could measure below the legal
floor even though the *declared* geometry was correct.**

A second, independent bug let this reach print: `04_BUILD/kdp_preflight.py`'s
ink-margin check compared **every** side (inside *and* outside/top/bottom)
against a single flat 0.25 in, and never read the page-count-derived 0.5 in
gutter rule that `interior.py` itself already implemented correctly. It
also rasterized at 72 dpi, where 1 px ≈ 0.0139 in — a 0.01 in shortfall is
*below one pixel* and rounds away entirely. The local gate could not have
caught this defect even in principle.

## 4 · Document-wide audit — every page, both editions

Method: full interior rendered at 300 dpi (`pdftoppm -gray`), every page's
ink bounding box measured, gutter/outer assigned by page parity (odd =
recto = gutter on **left**; even = verso = gutter on **right**), gutter
requirement derived from actual page count via `interior.gutter_in()`.
No page relied on the synthetic template value alone.

### BEFORE the fix

| | Paperback | Hardcover |
|---|---:|---:|
| Pages rendered | 160 | 160 |
| Required gutter (160 pages) | 0.500 in | 0.500 in |
| Nominal gutter in geometry | 0.500 in | 0.625 in |
| Worst measured gutter | **0.4900 in (page 15 & 159)** | 0.6133 in |
| **Failing pages** | **16** | **0** |
| Worst outer / top / bottom | 0.49 / 0.36 / 0.3467 in (all ≥ 0.25 required) | same |

Hardcover never failed — not because it was built more carefully, but
because its independent +0.125 in binding allowance *happened* to absorb
the same glyph overshoot that broke paperback. That is luck, not a
guarantee, and the fix does not rely on it continuing to hold.

**All 16 paperback failures, in full:**

| Page | Side | Measured gutter | Shortfall |
|---:|---|---:|---:|
| 15 | recto | 0.4900 in | 0.0100 in |
| 27 | recto | 0.4967 in | 0.0033 in |
| 29 | recto | 0.4933 in | 0.0067 in |
| 41 | recto | 0.4967 in | 0.0033 in |
| 44 | verso | 0.4967 in | 0.0033 in |
| 57 | recto | 0.4967 in | 0.0033 in |
| 67 | recto | 0.4967 in | 0.0033 in |
| 75 | recto | 0.4967 in | 0.0033 in |
| 87 | recto | 0.4967 in | 0.0033 in |
| 95 | recto | 0.4933 in | 0.0067 in |
| 114 | verso | 0.4967 in | 0.0033 in |
| 117 | recto | 0.4967 in | 0.0033 in |
| 125 | recto | 0.4967 in | 0.0033 in |
| 141 | recto | 0.4967 in | 0.0033 in |
| 147 | recto | 0.4967 in | 0.0033 in |
| **159** | **recto** | **0.4900 in** | **0.0100 in** |

Worst observed shortfall across the whole document: **0.0100 in.**

### AFTER the fix

| | Paperback | Hardcover |
|---|---:|---:|
| Pages rendered | 160 | 160 |
| Nominal gutter (bare min + 0.05 in safety) | 0.550 in | 0.675 in |
| Worst measured gutter | **0.5400 in (page 15)** | 0.6633 in |
| **Failing pages** | **0** | **0** |
| Page 159 specifically | **0.5400 in** ✅ | n/a (never failed) |

Every page, both editions, independently re-rendered and re-measured —
**zero failures.**

## 5 · Front-matter and early-page spot audit (§7 requirement)

Pages 2–21 and 159–160 were explicitly included in the full 160-page
sweep above (§4 covers *every* page, so this range needed no separate
pass). Representative samples were also rendered and visually inspected
by kind: title/imprint page, a two-page game spread (Olinda Keliya,
pp. 18–19 — diagram intact, rule blocks intact, gutter visibly more open
than before), and the back-matter Invented Traditions page (159 itself).
No visual defect, broken diagram, or clipped text was found anywhere in
the sampled pages.

---

## 6 · The source-level fix

`04_BUILD/interior.py`:

```python
GUTTER_SAFETY_IN = 0.05   # 5× the worst measured overshoot (0.01 in)
```

`geometry()` now computes:

```
bare_min = gutter_in(pages)              # KDP's bare legal minimum — unchanged
gutter   = bare_min + GUTTER_SAFETY_IN   # what the typesetter actually uses
```

This is **not** a page-159 patch. It changes the one function
(`geometry()`) that determines gutter width for the *entire* book, for
*both* editions, for *any* future page count. The bare KDP minimum table
(`KDP_GUTTER_IN`, already page-count-derived and already correct) is
untouched and remains the value the validator checks against.

`04_BUILD/kdp_preflight.py`'s `check_ink()` was rewritten to:
- import and use `interior.gutter_in(pages)` instead of a flat constant
  (single source of truth — no duplicated table),
- measure **gutter** and **outer** separately, assigned by actual page
  parity, instead of a blind `min()` across all four sides,
  and
- rasterize at **300 dpi** by default (was 72 dpi) — fine enough to
  resolve a 0.01 in defect at 3 pixels instead of rounding it to zero.

## 7 · Rebuild — page-count-derived gutter tier, tested at every boundary

`04_BUILD/interior.py`'s `gutter_in()` table (unchanged, already correct)
against the founder's exact required boundary list, now covered by an
automated regression (`05_TESTS/selftest.py § ⑬`):

| Pages | Required gutter |
|---:|---:|
| 149 | 0.375 in |
| 150 | 0.375 in |
| **151** | **0.500 in** |
| 160 (this book) | 0.500 in |
| 300 | 0.500 in |
| **301** | **0.625 in** |

## 8 · Both editions rebuilt from source — final page counts

| | Before | After |
|---|---:|---:|
| Paperback pages | 160 | **160** (unchanged) |
| Hardcover pages | 160 | **160** (unchanged) |
| Games (both editions) | 56 | 56 |
| Four-page entries | 0 | 0 |
| Games starting on left (verso) page | 56 / 56 | 56 / 56 |
| Blank architectural pages | 18 | 18 |
| TOC fitted | yes | yes |

The extra 0.05 in of gutter per page was fully absorbed by the existing
slack in the typesetting engine (diagram budget, spread-balancing logic)
without changing the page count in either edition. Per the founder's own
instruction, the page count was **not** forced back to any target — it
was simply measured after the fix, and it happened to still be 160.

## 9 · Content integrity after reflow

Independently re-verified, not assumed:

- **56/56 games present** in both `02_MANUSCRIPT/book.json` and the
  rebuilt page map — set difference in both directions is empty.
- **0 duplicate start-pages** in the page map.
- **6 randomly sampled games** (`polis`, `fox-and-geese`,
  `olinda-keliya`, `set-dilth`, `senet`, `pachisi`) cross-checked: each
  game's title was confirmed present via `pdftotext` on exactly the page
  number the map claims.
- `interior.py --check`: ✅ both editions, 56/56 spreads start on the
  left page, gutter ≥ required for both.

## 10 · Cover rebuild — independently, per edition

Because the page count did not change, spine geometry is **numerically
identical** to before the fix — but both covers were still rebuilt from
source (not assumed unchanged) once the interior checksum changed, since
`covers.py --check` correctly flags a stale cover the moment the interior
it was computed from changes.

| | Paperback | Hardcover |
|---|---:|---:|
| Spine (page-count-derived, independent formula) | 0.3603 in | 0.4600 in |
| Full wrap | 17.6103 × 11.2500 in | 17.2100 × 11.2500 in |
| Artwork embedded resolution | 5283 × 3375 px @ 300 ppi (measured) | 5163 × 3375 px @ 300 ppi (measured) |
| Safe areas / barcode zone / title / author / back copy | unchanged, re-verified via `covers.py --check` | unchanged, re-verified |

Hardcover spine was **not** derived from paperback's — confirmed by
reading the two independent formulas in `covers.py`'s `geometry()`
(`0.002252 in/page` for paperback vs `0.0025 in/page + 0.06 in board
allowance` for hardcover).

## 11 · Kindle

Kindle has no print gutter — the rule was correctly **not** applied to
it. Independently verified after the rebuild:
- Cover: unchanged (1600×2560 px, vector typography intact — derives from
  the paperback wrap art, which is visually identical since geometry
  didn't change the wrap's outer dimensions).
- EPUB: rebuilt, `epub.py --check` passes; reflowable text has no concept
  of a print gutter.
- Metadata/links/rendering: unaffected by an interior-PDF-only change.
- No stale page-count claim: EPUB and Kindle metadata don't print a page
  count (reflowable format), so there was nothing to go stale.

## 12 · A+

Not touched beyond re-confirming synchronization. A+ copy references
game/culture counts (56/39), not page counts, and those did not change.
`aplus.py --check` passes; `03_APLUS/aplus_content.json` is untouched on
disk (no rebuild was necessary, and none was performed, per the founder's
instruction not to alter A+ unnecessarily).

## 13 · Regression tests — added, not assumed sufficient

1. **`05_TESTS/selftest.py § ⑬`** (fast, no rebuild): every boundary in
   the founder's required list (149/150/151/160/300/301) plus the full
   KDP tier table, asserted against `interior.gutter_in()` directly.
   Also asserts the safety buffer is still ≥ the worst measured overshoot,
   and that `kdp_preflight.py` reads the gutter rule from `interior.py`
   rather than a duplicated constant.
2. **`05_TESTS/package_selftest.py`** — two new cases:
   - *Real-book regression*: `GUTTER_SAFETY_IN` set to **-0.01** in a
     temporary copy, paperback interior rebuilt for real, and
     `kdp_preflight.py` run against the actual rendered PDF — **must
     turn red** (glyph overshoot only ever worsens a deficit, so this is
     deterministic, not flaky). This is the literal page-159-class
     failure, reproduced end to end.
   - *Synthetic threshold precision* (§14's exact mandate): a minimal
     PDF with a filled rectangle — not a font glyph, so no rendering
     ambiguity — placed with its left edge at **exactly** 0.49 in and,
     separately, **exactly** 0.50 in, fed directly into `check_ink()`.
     0.49 in → red. 0.50 in → green. Both confirmed.

Both were run and pass; full results in § 15.

⚠ **Why the boundary test uses a synthetic fixture, not the real book at
exactly 0.50 in nominal:** the real book's own content demonstrated
(§ 4, "before") that a nominal 0.50 in margin does **not** reliably
produce ≥0.50 in of actual ink clearance once real glyphs are rendered —
that was the entire bug. Testing "0.50 in nominal passes" against the
real book would be genuinely flaky. The synthetic rectangle isolates and
locks down the validator's *comparison logic* precisely; the real-book
case (previous bullet) separately locks down that an *insufficient*
nominal margin is still reliably caught.

## 14 · Full QA

| Gate | Result |
|---|---|
| `interior.py --check` (both editions) | ✅ |
| `covers.py --check` | ✅ |
| `kdp_preflight.py` (rewritten, 300 dpi, gutter/outer split) | ✅ 20/20, both editions |
| `05_TESTS/selftest.py` | ✅ 229/229 (was 214 — 15 new gutter-tier checks) |
| `05_TESTS/package_selftest.py` | see § 15 |
| `./04_BUILD/qa_all.sh --fix` | ✅ BÜTÜN KAPILAR YEŞİL |

## 15 · Founder next action

The local pipeline — including a rewritten preflight that now enforces
the exact rule that failed in production — is green. **This means "local
preflight passed," not "KDP ready."** Per the founder's own instruction:
this project does not claim KDP-ready status from local tests alone.

**Next action:** re-run the real Amazon KDP Print Previewer against the
rebuilt `08_OUTPUT/PAPERBACK/GreatBookOfWorldGames_cover_paperback.pdf` /
`..._interior_paperback.pdf` (and the hardcover equivalents) and confirm
page 159 — and the whole document — now clears the gutter check for
real. Nothing has been uploaded, submitted, or ordered as a proof by this
correction round.
