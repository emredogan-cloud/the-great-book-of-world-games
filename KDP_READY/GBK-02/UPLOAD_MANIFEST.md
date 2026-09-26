# GBK-02 · The Great Book of World Games — KDP upload package

**Status: NOT READY — BLOCKED BY SPECIFIC RELEASE GATES.** Do not upload until the gates in the final report (`06_REPORTS/editorial/GBK-02_FINAL_RECOVERY_AND_KDP_READINESS_REPORT.md`, §24) are cleared: external playtesting, the subtitle/new-edition decision, the AI-content declaration, the companion deployment, the K19 diagram-budget decision, and a physical proof.

Packaged 2026-09-26 12:08 UTC from the recovery build. Every file here is **FINAL**; nothing old or superseded is in this folder. The previous package is archived at `09_ARCHIVE/kdp-ready-superseded-20260926-150827/`, and stale builds from `08_OUTPUT/` at `09_ARCHIVE/output-superseded-20260926-150827/`.

## Book

- Title: The Great Book of World Games
- Subtitle (printed in this build): 63 Games from 5,000 Years of Human Play — Rules, Boards and Stories from 42 Cultures, Ready to Play Tonight
- Subtitle on the live KDP print records: 63 Games from 4,600 Years of Human Play — Rules, Boards and Stories from 45 Cultures, Ready to Play Tonight — **differs** (new edition decision)
- Author: Emre Doğan · Publisher: Valice Press
- 63 games · 42 cultures · 7 families · 12 reconstructed

## Upload map

| Edition | Interior / book file | Cover | Notes |
|---|---|---|---|
| Paperback | `PAPERBACK/GreatBookOfWorldGames_interior_paperback.pdf` (258 pp · 8.5 × 11 in) | `PAPERBACK/GreatBookOfWorldGames_cover_paperback.pdf` (258 pp · spine 0.581 in · 17.831 × 11.25 in) | B&W, white paper, no bleed |
| Hardcover | `HARDCOVER/GreatBookOfWorldGames_interior_hardcover.pdf` (258 pp · 8.25 × 11 in) | `HARDCOVER/GreatBookOfWorldGames_cover_hardcover.pdf` (258 pp · spine 0.770 in · 18.845 × 12.417 in) | B&W, white paper, no bleed |
| Large print | `LARGE_PRINT/GreatBookOfWorldGames_interior_largeprint.pdf` (498 pp · 8.5 × 11 in) | `LARGE_PRINT/GreatBookOfWorldGames_cover_largeprint.pdf` (498 pp · spine 1.121 in · 18.371 × 11.25 in) | B&W, white paper, no bleed |
| Kindle | `KINDLE/GreatBookOfWorldGames.epub` | `KINDLE/GreatBookOfWorldGames_cover_kindle.jpg` (1600 × 2560) | reflowable EPUB 3 |

Book details to paste: `METADATA/kdp_metadata.json`, step by step in `METADATA/KDP_UPLOAD_HANDBOOK.md`. A+ content: `APLUS/`.

## Provenance

| File | Source | Built by | Built (UTC) | Pages / size | Validation |
|---|---|---|---|---|---|
| `PAPERBACK/GreatBookOfWorldGames_interior_paperback.pdf` | `08_OUTPUT/PAPERBACK/GreatBookOfWorldGames_interior_paperback.pdf` | `04_BUILD/interior.py` | 2026-09-26 11:20 | 258 pp · 8.5 × 11 in | KDP pre-flight 30 checks, 0 failed; qa_output green; manuscript a639870c1e27 |
| `PAPERBACK/GreatBookOfWorldGames_cover_paperback.pdf` | `08_OUTPUT/PAPERBACK/GreatBookOfWorldGames_cover_paperback.pdf` | `04_BUILD/build_gbk02_covers.py` | 2026-09-26 11:21 | 258 pp · spine 0.581 in · 17.831 × 11.25 in | covers.py --check green; geometry: KDP paperback formula (pages × 0.002252 in; bleed + back + spine + front + bleed) |
| `HARDCOVER/GreatBookOfWorldGames_interior_hardcover.pdf` | `08_OUTPUT/HARDCOVER/GreatBookOfWorldGames_interior_hardcover.pdf` | `04_BUILD/interior.py` | 2026-09-26 11:20 | 258 pp · 8.25 × 11 in | KDP pre-flight 30 checks, 0 failed; qa_output green; manuscript a639870c1e27 |
| `HARDCOVER/GreatBookOfWorldGames_cover_hardcover.pdf` | `08_OUTPUT/HARDCOVER/GreatBookOfWorldGames_cover_hardcover.pdf` | `04_BUILD/build_gbk02_covers.py` | 2026-09-26 11:21 | 258 pp · spine 0.770 in · 18.845 × 12.417 in | covers.py --check green; geometry: KDP Print Cover Calculator reading for 258 pages |
| `LARGE_PRINT/GreatBookOfWorldGames_interior_largeprint.pdf` | `08_OUTPUT/LARGEPRINT/GreatBookOfWorldGames_interior_largeprint.pdf` | `04_BUILD/interior.py` | 2026-09-26 11:20 | 498 pp · 8.5 × 11 in | KDP pre-flight 30 checks, 0 failed; qa_output green; manuscript a639870c1e27 |
| `LARGE_PRINT/GreatBookOfWorldGames_cover_largeprint.pdf` | `08_OUTPUT/LARGEPRINT/GreatBookOfWorldGames_cover_largeprint.pdf` | `04_BUILD/build_gbk02_covers.py` | 2026-09-26 11:21 | 498 pp · spine 1.121 in · 18.371 × 11.25 in | covers.py --check green; geometry: KDP paperback formula (pages × 0.002252 in; bleed + back + spine + front + bleed) |
| `KINDLE/GreatBookOfWorldGames.epub` | `08_OUTPUT/KINDLE/GreatBookOfWorldGames.epub` | `04_BUILD/epub.py` | 2026-09-26 11:21 | EPUB 3 · 86 documents | EPUBCheck 0 fatals / 0 errors / 0 warnings |
| `KINDLE/GreatBookOfWorldGames_cover_kindle.jpg` | `08_OUTPUT/KINDLE/GreatBookOfWorldGames_cover_kindle.jpg` | `04_BUILD/build_gbk02_covers.py` | 2026-09-26 11:21 | 1600 × 2560 px | 1600 × 2560 px, 1:1.6 |
| `METADATA/kdp_metadata.json` | `06_REPORTS/tracked/metadata.json` | `04_BUILD/metadata.py` | 2026-09-26 11:21 | 9329 bytes | metadata.py: consistent; 3 Founder actions |
| `METADATA/KDP_UPLOAD_HANDBOOK.md` | `08_OUTPUT/KDP_UPLOAD_HANDBOOK.md` | `04_BUILD/handoff.py` | 2026-09-26 12:08 | 25620 bytes | handoff.py --check green |
| `METADATA/KDP_PREVIEWER_CHECKLIST.md` | `08_OUTPUT/KDP_PREVIEWER_CHECKLIST.md` | `04_BUILD/handoff.py` | 2026-09-26 12:08 | 5867 bytes | handoff.py --check green |
| `METADATA/KDP_AI_DISCLOSURE_NOTES.md` | `08_OUTPUT/KDP_AI_DISCLOSURE_NOTES.md` | `04_BUILD/handoff.py` | 2026-09-26 12:08 | 5489 bytes | handoff.py --check green |
| `APLUS/aplus-01-hero-world-of-games.png` | `08_OUTPUT/APLUS/aplus-01-hero-world-of-games.png` | `04_BUILD/aplus.py` | 2026-09-26 11:21 | 964255 bytes | aplus.py --check READY (module 05 without art) |
| `APLUS/aplus-02-cultural-diversity.png` | `08_OUTPUT/APLUS/aplus-02-cultural-diversity.png` | `04_BUILD/aplus.py` | 2026-09-26 11:21 | 1015028 bytes | aplus.py --check READY (module 05 without art) |
| `APLUS/aplus-03-how-the-book-works.png` | `08_OUTPUT/APLUS/aplus-03-how-the-book-works.png` | `04_BUILD/aplus.py` | 2026-09-26 11:21 | 173536 bytes | aplus.py --check READY (module 05 without art) |
| `APLUS/aplus-04-types-of-games-a.png` | `08_OUTPUT/APLUS/aplus-04-types-of-games-a.png` | `04_BUILD/aplus.py` | 2026-09-26 11:21 | 78282 bytes | aplus.py --check READY (module 05 without art) |
| `APLUS/aplus-04-types-of-games-b.png` | `08_OUTPUT/APLUS/aplus-04-types-of-games-b.png` | `04_BUILD/aplus.py` | 2026-09-26 11:21 | 76887 bytes | aplus.py --check READY (module 05 without art) |
| `APLUS/aplus-04-types-of-games-c.png` | `08_OUTPUT/APLUS/aplus-04-types-of-games-c.png` | `04_BUILD/aplus.py` | 2026-09-26 11:21 | 88823 bytes | aplus.py --check READY (module 05 without art) |
| `APLUS/aplus-04-types-of-games-d.png` | `08_OUTPUT/APLUS/aplus-04-types-of-games-d.png` | `04_BUILD/aplus.py` | 2026-09-26 11:21 | 70591 bytes | aplus.py --check READY (module 05 without art) |
| `APLUS/aplus-06-complete-collection.png` | `08_OUTPUT/APLUS/aplus-06-complete-collection.png` | `04_BUILD/aplus.py` | 2026-09-26 11:21 | 842573 bytes | aplus.py --check READY (module 05 without art) |
| `APLUS/aplus_content.json` | `08_OUTPUT/APLUS/aplus_content.json` | `04_BUILD/aplus.py` | 2026-09-26 11:21 | 11188 bytes | aplus.py --check READY (module 05 without art) |

## SHA-256 checksums

The same list is in `SHA256SUMS` (verify with `sha256sum -c SHA256SUMS` in this folder). It is repeated here because the repository tracks this manifest but not the binary files or `SHA256SUMS`.

```
9f0aa934021de6a4ab75cf5e3b4a58f8486bc9d9b02e83d5224730034125375f  PAPERBACK/GreatBookOfWorldGames_interior_paperback.pdf
f5f1a1fd61cccc9917ae280ad5db93d3a2137f84ff3b7d3551d5b6eb055c2815  PAPERBACK/GreatBookOfWorldGames_cover_paperback.pdf
54bc5448aa2ccb87aab1563ac8bc22ce1f08f77cff4d332f305084efd494041d  HARDCOVER/GreatBookOfWorldGames_interior_hardcover.pdf
a4ede697b14a6b18c5e37393eeb443966c3f168cad1fb647c346e80dc04a693a  HARDCOVER/GreatBookOfWorldGames_cover_hardcover.pdf
1ba05c6653e7c2597ba2ffb9250812dd73a83a066aafd24d25308a2cb4aef415  LARGE_PRINT/GreatBookOfWorldGames_interior_largeprint.pdf
dd14b1645a094a1af870d6cef72a277aeeb5720681e5f2c68f3d8a523647a24d  LARGE_PRINT/GreatBookOfWorldGames_cover_largeprint.pdf
a560f65f1c8851d73ad4c87f960fe1b98a140cb4f312adb1b72a950cde97a9ea  KINDLE/GreatBookOfWorldGames.epub
b4d6ceb0f2236cb107f9eb6dd19b4735ecea9d4c1cb9ef15a079aeae98ea9594  KINDLE/GreatBookOfWorldGames_cover_kindle.jpg
22c9306882bb3650e42e45417023f217c528aeed38457ba40acdc388ddafa023  METADATA/kdp_metadata.json
f6dd53db58887c7610965d10552c66a2dc2bf3187896769fb6b3ee79ecd80945  METADATA/KDP_UPLOAD_HANDBOOK.md
ed677c1d44c58ac7e2ff587ad731f310d2fc8dc66a060814a9c7f67d2db06ad4  METADATA/KDP_PREVIEWER_CHECKLIST.md
c7e1f3c26fe7390f04e5b729214e6efa61ec8cc94644be6c89032972c8a45a2b  METADATA/KDP_AI_DISCLOSURE_NOTES.md
3d2758389d5ac20b61175728fd364f34c27b1b652867cd8a8c8c3ca75ca8a48d  APLUS/aplus-01-hero-world-of-games.png
0bb445e8fae2d1ea3c824006ee235faa2784818990a72a6c3fedb9848d0dc1cc  APLUS/aplus-02-cultural-diversity.png
2dfae992a8671cf3a1bf54e1d86f3edafd86db1a361cb7121b9b563f989235eb  APLUS/aplus-03-how-the-book-works.png
f0ec090b6d600abe260362ad110089eda41b45a61ba68a28e37ddf09cb0be36a  APLUS/aplus-04-types-of-games-a.png
a4f746ffb3bfd89c8ef795352731e6777569b5db715db12e91a92cdb47e40f7b  APLUS/aplus-04-types-of-games-b.png
8cac2c487e3920a00a14e7889b257d4273bd1c9f5c0a367638cabbec838f8a0d  APLUS/aplus-04-types-of-games-c.png
01f4b97e6ef2418fcd8d6433d0eb9a2805f10548fd0830ab98b04870f9673b08  APLUS/aplus-04-types-of-games-d.png
c89a0373e94fe9f8bce255f3bee5ced51f24b99590922b5fc8cd1313e61c9ed4  APLUS/aplus-06-complete-collection.png
d5152e0e03442a12346390a6c00f280eee9be32397171eb683f9ae50acb75094  APLUS/aplus_content.json
```

## Release notes — recovery edition (2026-09-26) against the edition on sale

- All 63 entries rewritten from page-verified sources: numbered rules, draw / blocked / illegal-move answers, a worked turn for every game, editorial rulings marked †, reconstructions boxed.
- The 21 games the 2026-09-25 audit found unplayable as printed now carry the missing rules (Bao, Hus, Diviyan Keliya, Ludus Duodecim Scriptorum, Pachisi, Patolli, Awithlaknannai, Cat's Cradle and others).
- Culture labels by one rule: 42 cultures (was printed as 45). Oldest game senet, c. 3100 BC (was 4,600 years).
- 121 diagrams and 14 full-size boards redrawn from the rules and checked by count; large-print versions.
- New two-column typography; A–Z index of games and other names; index by culture, age and difficulty; hand-written glossary; bibliography by work; games-kit table; invented-traditions page.
- Plates: the duplicate Jan-ken plate replaced; object-focused images for the named Indigenous cultures; the AI disclosure printed and counted (52 of 63 plates).
- Companion pack rebuilt (52 boards, 63 cards); the printed companion page quotes its real counts.
- Covers: the Founder's artwork with corrected counts; the invented author line removed from the back cover.
- Page counts: paperback and hardcover 258, large print 498.

