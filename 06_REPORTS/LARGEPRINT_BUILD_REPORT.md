# Large Print Edition — build report (2026-09-02, Phase 2 v3 pilot)

## What was built

| File | Measured |
|---|---|
| `08_OUTPUT/LARGEPRINT/GreatBookOfWorldGames_interior_largeprint.pdf` | **232 pages**, 8.5 × 11 in (612 × 792 pt), 577 KB, four Liberation Serif faces embedded (`pdffonts`: emb yes, sub yes, uni yes), no raster images |
| `08_OUTPUT/LARGEPRINT/GreatBookOfWorldGames_cover_largeprint.pdf` | full wrap 17.7725 × 11.25 in, spine 0.5225 in (232 × 0.002252), 20.9 MB (under KDP's 40 MB), same artwork pipeline as the paperback, "LARGE PRINT EDITION" under the subtitle, " · LARGE PRINT" on the spine, one extra head line on the back |
| `06_REPORTS/interior-largeprint.json` | body 16.0 pt / 20.57 pt leading; type scale 1.5238; smallest type set anywhere 12.00 pt; running head 12.95 pt, folio 14.48 pt; 3.18 pages per game (max 4); 50 diagrams, every one at ≥ 1.00 × its paperback size; gutter 0.550 in (KDP minimum 0.500 for 151–300 pp + 0.05 safety); 9 blank pages (part openers on recto); TOC fitted |
| `06_REPORTS/kdp-preflight.json` | 30/30 checks green for paperback, hardcover and largeprint — fonts, page size, ink margins (largeprint worst: gutter 0.5333, outer 0.4867, top 0.3167, bottom 0.3467 in), language, images, page band, even count |
| `06_REPORTS/editions.json` | largeprint enabled at **$31.99** — see economics |

The two live editions were **not rebuilt**; their outputs are unchanged (`interior.py --check`: paperback 160 pp 56/56 verso starts, hardcover 160 pp 56/56; `covers.py --check`: geometry in sync for all three).

## What changed in the code

- `04_BUILD/interior.py`: `geometry()` knows `largeprint` (paperback trim, values from `project_config.json → production.largePrint`); `styles()` takes `scale` and `min_pt` and, at 1.0/0, produces exactly the old styles; inline `<font size=…>` in the contents and back matter go through `sty["_fs"]`; running head/folio sizes come from the geometry (offsets are deliberately *not* scaled — the first build put the head 0.22 in from the trim and the preflight caught it); a large-print branch in `build_layout()` lays each game as one continuous flow (story → diagrams → rules) with no two-page-spread promise and no page cap (the paperback's four-page cap would have dropped text); `run_check()` verifies the large-print report (gutter, even pages, KDP band, TOC, body ≥ 16 pt, minimum ≥ 12 pt, diagram ratio ≥ 0.98); `--edition largeprint`; output dir `LARGEPRINT`.
- `04_BUILD/covers.py`: `largeprint` in the spine, spine-run, back-box and title-position tables (same trim as paperback); label text; `--largeprint-only`; `run()` includes the edition when its interior report exists.
- `04_BUILD/editions.py`: largeprint uses its **own** counted page count.
- `04_BUILD/kdp_preflight.py`: third edition; largeprint on the paperback rate card.
- `project_config.json`: `production.largePrint` block (bodyPt 16, minimumPt 12, editionLabel, diagramPageBudget 0.60, rationale); `editionsHypothesis.largeprint` enabled, list 31.99, priceBasis.
- New: `04_BUILD/companion_pack.py` (free companion PDFs; see the site's `/companion/world-games`).

## Economics (KDP rate card verified 2026-09-01; `scripts/strategy/price-engine.mjs`)

232 pp, large trim, B&W: print cost **$4.94**; KDP minimum list $8.25.

| List | Royalty (60 %) | Break-even ACOS | Max CPC @ 8 % CVR |
|---|---|---|---|
| $27.99 | $11.85 | 42.3 % | $0.95 |
| $29.99 | $13.05 | 43.5 % | $1.04 |
| **$31.99** | **$14.25** | **44.5 %** | **$1.14** |
| $32.99 | $14.85 | 45.0 % | $1.19 |
| $34.99 | $16.05 | 45.9 % | $1.28 |

$31.99 chosen: clears the 35 % target, sits $3 under the $34.99 hardcover, and is the grid point nearest the roadmap's $31.03 large-print figure. The Founder may move it at Gate 8. Demand is not modelled.

## Limitations, honestly

- The two-page-spread promise ("open the book on the table and play without turning a page") does **not** hold in large print; a game runs 3–4 pages. The imprint says "Large Print Edition" and the layout keeps each game's diagrams on its second page, but the back-cover copy still describes the book generally.
- KDP Previewer has not been run (Founder's upload flow only). The local preflight is not a substitute.
- Part openers still pad to a recto, which costs nine blank pages (≈ $0.15 of print cost per copy).
- "Large Print" is a KDP listing attribute, not a file property; the Founder sets it in the edition details.

## KDP upload steps (Founder)

1. Create a **new paperback** under the same title (do not edit the live paperback): title "The Great Book of World Games", add "(Large Print)" as the edition/format descriptor where KDP asks for it, same author, same description with one added sentence ("This large print edition is set in 16-point type."), same categories; tick **Large Print** in the print options.
2. Trim 8.5 × 11 in, black & white interior on white paper, no bleed, matte or glossy as the paperback.
3. Upload `08_OUTPUT/LARGEPRINT/GreatBookOfWorldGames_interior_largeprint.pdf` (232 pp) and `…_cover_largeprint.pdf`.
4. Run the KDP Previewer; if it flags anything, send the message text back — do not approve with warnings.
5. Price $31.99 (Amazon.com), expanded distribution off, KDP-provided ISBN.
6. After it goes live, paste the ASIN into `scripts/catalog/valice-catalog.mjs` (format `large_print`, `kdp: "live"`) and run the catalog loader; nothing on the website links to the edition until then.
