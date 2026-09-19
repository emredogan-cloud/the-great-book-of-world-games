# THE GREAT BOOK OF WORLD GAMES — Visual Integration Handoff for Agent A

Planning only. No image generated, no PDF/EPUB touched, no manuscript text changed, and —
most importantly for this book — **no existing rule diagram touched, referenced for
replacement, or placed on the same page as a new plate.**

Master data: `data/WORLDGAMES.json`. Page audit: `audits/WORLDGAMES-PAGE-AUDIT.md`.

## 0 — Two things to flag before starting

**(a) No AI-disclosure statement found**, same open question as Epictetus in this
session's batch — confirm with the Founder whether this book's cover/apparatus needs one
before any new visual (real or otherwise) ships.

**(b) `07_ASSETS/IMAGE_PROMPT_LIBRARY.html` in this book is NOT this mission's deliverable
and must not be confused with it or overwritten.** It is a Phase 6 cover/A+ marketing
prompt file, unrelated to interior visuals. This mission's interior-visual data lives
entirely in `data/WORLDGAMES.json` (staging) and will populate a new `07_ASSETS/plates/`
directory once Agent A sources images — a sibling to, never a replacement for,
`07_ASSETS/diagrams/`.

## 1 — Numbers

*(Corrected by the orchestrator against the final `data/WORLDGAMES.json` — an earlier
draft of this section undercounted at 23 total/22 new; the book's own generator script,
re-run and re-validated, confirms the figures below.)*

- 90 total records: 51 individual KEEP entries for the existing rule diagrams/family
  furniture, 39 newly planned (7 family openers, 30 of the 56 games, 2 front/back-matter
  locations).
- 160 pages, 56 games. Target ≈ 53 at 1-per-3. 39 new plates ≈ 1 per 4 pages — still
  deliberately short of the raw target: this book's rule diagrams already carry the
  primary explanatory load on every page, so new visuals are a supplementary
  craftsmanship/context layer rather than a comprehension necessity, and mission §11
  explicitly warns against padding this specific book with decorative filler.
- New-record priority: P0=12, P1=21, P2=6 (P0s include Royal Game of Ur, Senet, Nine
  Men's Morris, Pachisi and other games whose history note points at a specific,
  real, named object or place).
- New-record image class: REAL_SOURCE_CANDIDATE=19, GENERATIVE_IMAGE=19,
  PROGRAMMATIC_GRAPHIC=1.
- 9 records carry explicit cultural cautions (the five living-Indigenous-nation games
  named in the audit, plus Mbube Mbube/Zulu, Fanorona's royal figure, Seega's
  unverifiable current site, and Jan-ken's generic-faces note) and a Founder-review
  flag — see the audit's closing section.

## 2 — The one rule that governs every placement decision

**Never place a new plate on the same page or spread as that game's rule diagram.** Every
`placement.detail` in `data/WORLDGAMES.json` says this explicitly. The rule diagrams are
black-and-white, four-greyscale-level, self-contained, and designed to be read at the
table while playing (per `00_CONTEXT/DIAGRAM_LANGUAGE.md`); a photographic plate sharing
that spread would visually compete with the one thing on the page that must stay legible
at a glance. Place new plates on the chapter-opener page, in a margin on an adjacent page,
or on the reverse of the rule spread.

## 3 — Placement, format impact, mandatory/optional

`anchorText` for most records references the game's `culturalStory` field in
`02_MANUSCRIPT/book.json` — a stable, already-written prose passage — rather than a page
number, since this book's own page model is still subject to recalibration
(`00_CONTEXT/EDITORIAL_ARCHITECTURE.md` flags the page model as not yet fully calibrated
even at Phase 1). Full-page entries (Royal Game of Ur, Senet, Nine Men's Morris, Pachisi)
are `FIXED` to their chapter openers and will add roughly +1 page each; every other record
is `FLEXIBLE_ANCHOR` and `NO_MAJOR_CHANGE`. P0/P1 records should be sourced first; the five
living-nation landscape plates and the P2 "safe texture" items (Yut Nori sticks, Cat's
Cradle hands, Sittuyin pieces) can be deferred without weakening the book.

## 4 — Existing diagrams

**KEEP, unconditionally, all 58.** Nothing REPLACE, SUPPLEMENT, or REMOVE among them. The
one new addition that touches the same conceptual territory — a representative real
mancala board opening the sowing-games family — is a genuinely new, separate visual
register (photographic, not schematic) and does not duplicate anything the diagrams show.

## 5 — PDF/EPUB and QA

This book's build pipeline (`04_BUILD/interior.py`, `epub.py`, `qa_diagram.py`,
`qa_visual.py`) already has a diagram-specific QA gate — extend it, after insertion, to
also confirm no new plate was placed on a rule-diagram page/spread (per §2), and re-run
`04_BUILD/qa_visual.py` and `page_budget.py` to re-measure the real page-count impact of
the four full-page additions. For the five living-nation games, do not proceed to sourcing
without an explicit Founder decision, recorded the same way UES-01's cultural-gate
decisions are recorded, given this book currently has no equivalent formal gate document.
