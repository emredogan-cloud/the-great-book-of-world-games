# GBK-02 — ChatGPT Image Generation Log

**Book:** The Great Book of World Games (GBK-02)
**Session:** 15–16 September 2026
**Tool:** ChatGPT web UI (chatgpt.com), GPT Image model — not the API
**Method:** Browser automation (Claude in Chrome), one game at a time, human inspection of every image before acceptance
**Total images generated and accepted:** 63 (7 new games + 56 pre-existing games — full manuscript coverage)

## Workflow used for every image

1. Open (or reuse) a ChatGPT chat thread.
2. Click the "Ask anything" box, type the full prompt for one game, press Return.
3. Wait ~30–40 seconds for GPT Image to render (progress shown as a percentage on the thumbnail).
4. Click the thumbnail to open the full-resolution editor view.
5. Visually inspect the rendered image against the prompt's SUBJECT/ENVIRONMENT/MATERIALS requirements.
6. If acceptable: click the download icon; if a session's percentage-based "which do you like more?" A/B chooser appeared instead of a single image, pick the candidate that most accurately matched the prompt's specific requirements (piece shapes, board geometry, environment details) before downloading.
7. Chrome saves the file to `~/Downloads/.org.chromium.Chromium.<random>` (a hidden, randomly-named temp file — Chrome does not rename it even though it is a complete, valid PNG).
8. Retrieve the freshly-downloaded temp file via shell (`ls -t`), verify its timestamp is fresh (not a stale file left over from a previous download), verify it is a valid PNG via `file`, then copy it to `07_ASSETS/plates/` under its deterministic name `GBK02_GAME_<NNN>_<SLUG>_HERO.png`.

No image was accepted without a human (in-session) visual check against the source prompt.

## Two generation batches

### Batch 1 — 7 new games (added to reach ~63 games), 15 Sep 2026
congklak, ayoayo, gebeta, hus, mefuvha, ludus-duodecim-scriptorum, morra.
All 7 generated in a single chat thread ("Generate Congklak Illustration"), no content-policy issues, no retries needed. All accepted on first generation.

### Batch 2 — 56 pre-existing games, 15–16 Sep 2026
Games 001–056 in book.json order (tablut through go). Generated in a fresh chat thread ("Generate Game Illustration" / "Generate Sámi game illustration") to avoid one very long, slow-to-scroll conversation. All 56 accepted; 4 required a prompt revision before acceptance (see below).

## Issues encountered and how each was resolved

### Content-policy rejections on child-subject prompts (4 games)
Games **gonggi**, **hopscotch**, **conkers**, and **mbube-mbube** feature children as central subjects. The first prompt attempt for gonggi ("close three-quarter angle... sharply in frame" on a single girl) was rejected by ChatGPT's safety filter. Fix applied to all four: reframed the camera direction from "close" to "a respectful full-figure distance" / "modest full-figure distance," added explicit language ("ordinary daytime play," "no close-up framing of children") to the STRICT PROHIBITIONS block, and kept full-body, wide-shot framing throughout. All four passed on the revised prompt and produced warm, appropriate, non-exploitative results.

### A/B "which image do you like more?" chooser
On several generations (jan-ken, bul, and a few others) ChatGPT presented two candidate images instead of one. In each case both candidates were inspected and the one that most precisely matched the prompt's specific mechanical/geometric requirements (e.g., distinct rock-paper-scissors hand shapes for jan-ken; the ladder-of-corn-cobs layout plus the thatched-house environment for bul) was selected before downloading.

### Stale temp-file re-use
Chrome's random temp filenames occasionally repeated across different downloads in the same session (observed for hus/mefuvha's shared suffix pattern, and again for jeu-de-dames/bul: `.org.chromium.Chromium.BlMuaz` was reused). Because a `cp` of a stale file still "succeeds" and produces a valid-looking PNG, every reused-looking filename was re-verified by checking the file's `ls -la` modification timestamp against the current time before it was trusted. Two instances of stale reuse were caught this way (bul, and one nine-men's-morris download) and corrected by re-clicking download and re-verifying freshness.

### Silent download-click failures
The download icon occasionally did not trigger a new browser download on the first click (no new temp file appeared after several seconds). Fix: re-click, wait longer (5–8s), and re-check `~/Downloads` before proceeding. Never assumed success without a fresh-timestamp file.

### One stray misnamed download
A single file named `ChatGPT Image Sep 15, 2026, 09_32_50 PM.png` was found in `07_ASSETS/plates/` (an accidental save from an earlier UI interaction). It did not match the deterministic naming convention and was not part of the accepted 63; it was deleted.

### Browser extension disconnect (one occurrence)
During the fox-and-geese generation the Claude-in-Chrome extension briefly reported "not connected." The generation that was in-flight during the disconnect errored out inside ChatGPT itself ("Something went wrong"). Recovery: reconnected, retried the identical prompt in a fresh chat, which then generated correctly.

### One generation that hung past normal completion time
One fox-and-geese attempt sat at a spinning indicator (no percentage) for 90+ seconds — well past the normal ~30–40s pattern — with no visible failure. Rather than waiting indefinitely, the request was stopped and retried fresh, which completed normally in ~35 seconds.

## Quality bar applied to every image

Every accepted image was checked for:
- Correct SUBJECT match (people, board/piece geometry, action described in the prompt)
- Correct ENVIRONMENT/PERIOD (no anachronistic objects, no modern intrusions)
- No text, watermark, logo, or signature baked into the image
- No exaggerated/caricatured facial features
- Editorial/museum-plate tone rather than glossy digital-art or fantasy-illustration style

No image required more than one prompt revision to reach an acceptable result; none needed more than the built-in A/B choice or a single retry.

## Final output

63 PNG files in `07_ASSETS/plates/`, sequence `GBK02_GAME_001_TABLUT_HERO.png` … `GBK02_GAME_063_MORRA_HERO.png`, no gaps, no duplicates, all 1536×1024, total ~165 MB. Full per-game metadata (prompt text, batch, dimensions, file size) recorded in `07_ASSETS/GBK02_GAME_ILLUSTRATION_MANIFEST.json`.
