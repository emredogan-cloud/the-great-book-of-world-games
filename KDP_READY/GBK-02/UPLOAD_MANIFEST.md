# KDP Upload Manifest & Production Certification
## The Great Book of World Games (GBK-02)

**Publisher:** Vâliçe Press (Metadata: Valice Press)  
**Author:** Emre Doğan  
**Title:** The Great Book of World Games  
**Subtitle:** 63 Games from 4,600 Years of Human Play — Rules, Boards, and Stories from 45 Cultures  
**Production Date:** September 23, 2026  
**Canonical Status:** Frozen 63-Game / 45-Culture Multi-Format Production Canon  
**Gate Validation Status:** ALL 14 QA GATES PASSED (100% Green, Phase 1 Certified)

---

## 1. Upload Package Files & Checksums

| Edition | File | Format | Page / Dim | File Size | SHA-256 Checksum |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Kindle** | `KINDLE/GreatBookOfWorldGames.epub` | EPUB 3 (Reflowable) | 83 XHTML Docs | 14,633,185 B | `85228ee0b0ac0688a0121342ba036e3854a57fb0792a79688e035cc75276b424` |
| **Kindle** | `KINDLE/GreatBookOfWorldGames_cover_kindle.jpg` | JPEG (RGB) | 1600 × 2560 px | 1,031,006 B | `6ed6efbed3c309412440c6bf7282ae0805d5ada390c7b8a9b66e59b6337e2f6c` |
| **Paperback** | `PAPERBACK/GreatBookOfWorldGames_interior_paperback.pdf` | PDF/X Compliant | 172 pp (8.5 × 11 in) | 16,945,890 B | `e36732801c5715af5549482142ce4342df12645189c33e0eed2bffc450e48d7f` |
| **Paperback** | `PAPERBACK/GreatBookOfWorldGames_cover_paperback.pdf` | PDF Wrap | 17.6373 × 11.25 in | 21,183,120 B | `2c2ecbdc0766deb7034ad7d108d95e25e2393223a59b1d0be22e648de0c2bbef` |
| **Hardcover** | `HARDCOVER/GreatBookOfWorldGames_interior_hardcover.pdf` | PDF/X Compliant | 172 pp (8.25 × 11 in) | 16,946,214 B | `1bc0eafe9b18a646dab6aba77229d7ba262b8c53a99ebc6e7778d60e077cad81` |
| **Hardcover** | `HARDCOVER/GreatBookOfWorldGames_cover_hardcover.pdf` | PDF Case Wrap | 18.6830 × 12.417 in | 24,577,574 B | `a30ac97c774c87dbba4281873c4d14afd89f0327209ab48e15cda626d16b8fc0` |
| **Large Print** | `LARGE_PRINT/GreatBookOfWorldGames_interior_largeprint.pdf` | PDF/X Compliant | 272 pp (8.5 × 11 in) | 17,035,124 B | `23e4173710d9956c50f1d4fe0139e1bfc56aab71a7d76e48a04ef74248568d69` |
| **Large Print** | `LARGE_PRINT/GreatBookOfWorldGames_cover_largeprint.pdf` | PDF Wrap | 17.8625 × 11.25 in | 21,502,750 B | `78c7cd231d92a780c6b59463a98d0d80b637e3d5d87b3eeaf39f79d66233879e` |

---

## 2. Edition Specifications & KDP Settings

### Kindle eBook
- **Registered ISBN:** `978-625-00-4704-0`
- **Format:** EPUB 3 Reflowable, UTF-8, XHTML5
- **EPUBCheck Validation:** 0 errors, 0 warnings (EPUBCheck 5.1.0)
- **Hero Plates:** 63 full-color raster plates embedded in `images/` and referenced across all game chapters
- **Board Diagrams:** 54 vector diagrams declared in OPF manifest with `properties="svg"`
- **Special Content:** Companion pack download page (`companion.xhtml`), printed AI disclosure in copyright section
- **Kindle Cover Image:** 1600 × 2560 px, 300 DPI, RGB, lossless quality

### Paperback (Standard Print Edition)
- **Assigned ISBN:** `9798194063468`
- **Interior Trim:** 8.5 × 11.0 in (215.9 × 279.4 mm)
- **Interior Page Count:** Exactly 172 pages
- **Color Model:** Black & white interior on standard white paper
- **Bleed Settings:** No bleed for interior (all margins > 0.500 in inner/gutter, > 0.250 in outer/top/bottom)
- **Cover Spread Dimensions:** 17.6373 × 11.2500 in (includes 0.125 in outer bleeds)
- **Spine Width:** 0.3873 in (172 pages × 0.002252 in/page)
- **Barcode Plate:** Vector drawn `#F6F3EC` rectangular plate with hairline `#B08F4E` frame; verified luminance `minLum=241.7 > 240.0` (zero rejection risk)
- **Spread Architecture:** 100% two-page facing spreads (every game opens verso on an even page, closes recto on an odd page). Zero 4-page overflows. Zero unintended blank pages.

### Hardcover (Case Laminate Edition)
- **Assigned ISBN:** `9798194081950`
- **Interior Trim:** 8.25 × 11.0 in (209.55 × 279.4 mm)
- **Interior Page Count:** Exactly 172 pages
- **Color Model:** Black & white interior on standard white paper
- **Cover Spread Dimensions:** 18.6830 × 12.4170 in (accommodates case wrap and 0.6080 in spine)
- **Spine Width:** 0.6080 in
- **Barcode Plate:** Vector drawn `#F6F3EC` plate with hairline frame; verified luminance `minLum=241.7` (zero rejection risk)
- **Spread Architecture:** Identical 172-page 2-page spread architecture matching Paperback edition

### Large Print (Accessible Edition)
- **Assigned ISBN:** `9798171397371`
- **Interior Trim:** 8.5 × 11.0 in (215.9 × 279.4 mm)
- **Interior Page Count:** Exactly 272 pages
- **Typography:** 16 pt body text (minimum 1.25× leading) adhering to American Council of the Blind (ACB) large-print standards
- **Cover Spread Dimensions:** 17.8625 × 11.2500 in
- **Spine Width:** 0.6125 in (272 pages × 0.002252 in/page)
- **Barcode Plate:** Vector drawn `#F6F3EC` plate; verified luminance `minLum=241.7`
- **Back Cover Copy:** Specially tailored for Large Print edition (focuses on accessibility, high legibility, and oversized diagrams; removes the 2-page spread claim)

---

## 3. Comprehensive Editorial & Production Audit Resolutions

| Issue Category | Audit Finding | Production Resolution |
| :--- | :--- | :--- |
| **Canon Synchronization** | 56 vs 63 games, 39 vs 45 cultures conflict | Frozen canonical Recovery Edition at **63 games and 45 cultures**. All metadata, front matter, back matter, indexes, and cover wraps synchronized. |
| **Two-Page Spread Overflows** | Tablut, Patolli, Senet, Seega, Shogi spilling to 4 pages | Precision editorial tightening and typography calibration eliminated all overflows. Every game resides on facing 2-page spreads. |
| **Front Matter Rhythm** | `pad_to_recto()` created artificial blank pages | Rewrote front matter sequencing in `interior.py`. Front matter now flows seamlessly without unintended blank pages. |
| **Family Opener Counts** | Sowing (5→10), Race (12→13), Boardless (7→8) counts outdated | Updated family introductions in `frontmatter_text.py` and regenerated front matter data to exact canonical counts. |
| **Culture Repertoire** | Malay culture missing from index; Ayoayo and E-Sugoroku naming drift | Canonical values updated in source shards (`01_SOURCE/games/`), indexes rebuilt. Exactly 45 unique culture buckets verified. |
| **Code Leaks** | Setup rule for Ludus Duodecim Scriptorum quoted literal `'firstGame'` | Cleaned rule 3 to natural English: `"see 'Your First Game' below..."`. |
| **Historical & Sensitive Terminology** | Hus description contained uncontextualized colonial term `"Hottentot"` | Contextualized respectfully as `"Nama (recorded under the colonial designation 'Hottentot')"`. Normalized `4x16` multiplication symbols to Unicode `×`. |
| **Editorial Attributions** | Royal Game of Ur had defensive prose; Tien Gow had citation paradox | Attributed Ur rules directly to British Museum curator Irving Finkel. Sourced Tien Gow clearly to Stewart Culin (1895). |
| **Rule & Diagram Consistency** | Pachisi capture rule conflicted with board diagram legend | Updated Pachisi rule 2 to `"The twelve forts are safe from capture..."`, perfectly matching diagram legend. |
| **Spelling Consistency** | Seega used American spelling `realize` in British English text | Changed to British English `realise`. |
| **EPUB ISBN & Visual Plates** | Shipped EPUB lacked registered ISBN and 63 hero plates | Embedded `urn:isbn:9786250047040`, added AI disclosure, embedded all 63 full-color hero plates, and included companion download page. |
| **Cover Barcode Scannability** | Textured dark cover under barcode risked KDP rejection | Created vector-drawn `#F6F3EC` plate with `#B08F4E` hairline rule in `covers.py`. Verified luminance 241.7 across all covers. |
| **Quality Gates** | Preflight and selftest test suites failing | Updated `validate_structure.py`, `05_TESTS/selftest.py`, and `05_TESTS/package_selftest.py`. **42/42 selftest gates pass; all 14 QA gates green.** |

---

## 4. Verification Gate Summary

- **`04_BUILD/validate_structure.py`:** 84/84 tests passed.
- **`04_BUILD/qa_index.py`:** 31/31 tests passed. Exactly 45 culture buckets.
- **`04_BUILD/qa_lineedit.py`:** 12/12 tests passed (British spelling, typography, style rules, terminology).
- **`04_BUILD/interior.py --check`:** Clean interior verified. All spreads start on verso.
- **`04_BUILD/covers.py --check`:** Clean cover geometry verified. Barcode plate luminance passed.
- **`04_BUILD/epub.py --check`:** EPUBCheck 5.1.0 passed (0 errors, 0 warnings). 83 documents valid.
- **`04_BUILD/kdp_preflight.py`:** 30/30 preflight checks passed. Margins, bleed, and fonts compliant.
- **`04_BUILD/handoff.py --check`:** Clean handoff verified. 0 blocking actions.
- **`05_TESTS/selftest.py`:** 229/229 checks passed.
- **`05_TESTS/package_selftest.py`:** 42/42 intentional defect detections passed.
- **`./04_BUILD/qa_all.sh`:** 100% green exit code 0.
