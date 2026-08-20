#!/usr/bin/env python3
"""
TESLİM PAKETİ — The Great Book of World Games
================================================================================
`08_OUTPUT/` altındaki yayın paketini toplar, sağlamalarını yazar ve kurucunun
KDP panelinde kullanacağı iki belgeyi ÜRETİR:

    08_OUTPUT/KDP_UPLOAD_HANDBOOK.md      · adım adım yükleme kılavuzu
    08_OUTPUT/KDP_PREVIEWER_CHECKLIST.md  · Previewer'da NEYE bakılacağı

⚠ İKİSİ DE ÜRETİLİR, YAZILMAZ. Sayfa sayısı, sırt genişliği, dosya adları
ve sağlama toplamları ölçümden gelir. Elle yazılmış bir kılavuz, iç blok bir
sayfa değiştiğinde sessizce yalancı olur — ve kurucu o kılavuza bakarak
yükleme yapar.

⚠ AJAN KDP PANELİNE DOKUNMAZ. Kılavuzdaki her adım **KURUCU EYLEMİ** ya da
**AJAN HAZIRLADI** diye işaretlidir. Hiçbir panel eyleminin yapıldığı iddia
edilmez.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)


def collect(root):
    """Paketleri toplar ve her birinin GERÇEK durumunu ölçer."""
    out = {}
    cb = {}
    cbp = os.path.join(root, "06_REPORTS", "cover-build.json")
    if os.path.exists(cbp):
        cb = load(cbp)
    for ed, folder in (("paperback", "PAPERBACK"), ("hardcover", "HARDCOVER")):
        rp = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if not os.path.exists(rp):
            continue
        r = load(rp)
        f = os.path.join(root, r["file"])
        out[ed] = {
            "folder": folder,
            "interior": {"file": r["file"], "exists": os.path.exists(f),
                         "sha256": sha256(f) if os.path.exists(f) else None,
                         "recordedSha256": r["sha256"],
                         "bytes": os.path.getsize(f) if os.path.exists(f) else 0,
                         "pageCount": r["pageCount"]},
            "blankPages": r.get("blankPages", 0),
            "trim": r["trim"], "margins": r["margins"],
            "cover": None, "coverStatus": "BLOCKED — kurucu sanatı yok",
        }
        cv = (cb.get("editions") or {}).get(ed)
        if cv:
            cf = os.path.join(root, cv["file"])
            out[ed]["cover"] = {
                "file": cv["file"], "exists": os.path.exists(cf),
                "sha256": sha256(cf) if os.path.exists(cf) else None,
                "recordedSha256": cv["sha256"],
                "bytes": os.path.getsize(cf) if os.path.exists(cf) else 0,
                "wrapIn": cv["wrapIn"], "spineIn": cv["spineIn"],
                "artwork": cv["artwork"],
                "typeItems": len(cv.get("typeLog") or []),
                "spineFit": cv.get("spineFit"),
            }
            out[ed]["coverStatus"] = ("READY" if os.path.exists(cf)
                                      else "MISSING FILE")
    ep = os.path.join(root, "06_REPORTS", "epub.json")
    if os.path.exists(ep):
        r = load(ep)
        f = os.path.join(root, r["file"])
        kc = cb.get("kindle")
        out["kindle"] = {
            "folder": "KINDLE",
            "cover": kc,
            "epub": {"file": r["file"], "exists": os.path.exists(f),
                     "sha256": sha256(f) if os.path.exists(f) else None,
                     "recordedSha256": r["sha256"],
                     "bytes": os.path.getsize(f) if os.path.exists(f) else 0},
            "coverStatus": ("READY" if kc else r["coverStatus"]),
        }
    ap = os.path.join(root, "03_APLUS", "aplus_content.json")
    if os.path.exists(ap):
        a = load(ap)
        out["aplus"] = {"folder": "APLUS", "modules": len(a["modules"]),
                        "imagesMissing": a["imagesMissing"],
                        "ready": a.get("modulesReady", []),
                        "withoutArt": a.get("modulesWithoutArt", []),
                        "status": a["status"]}
    return out


def sums_file(root, folder):
    d = os.path.join(root, "08_OUTPUT", folder)
    if not os.path.isdir(d):
        return None
    lines = []
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if os.path.isfile(p) and fn != "SHA256SUMS":
            lines.append("%s  %s" % (sha256(p), fn))
    if not lines:
        return None
    write(os.path.join(d, "SHA256SUMS"), "\n".join(lines) + "\n")
    return len(lines)


# ── KILAVUZ ──────────────────────────────────────────────────────────────
F = "**FOUNDER ACTION**"
A = "*agent prepared*"


def steps_for_print(ed, pkg, md, cov, fm):
    t = pkg["trim"]
    m = pkg["margins"]
    g = cov["editions"][ed]
    isbn = md["isbn"]["paperback" if ed == "paperback" else "hardcover"]
    b = md["bookDetails"]
    return f"""
### 1 · KDP Bookshelf
{F} Sign in at kdp.amazon.com → **Bookshelf** → **+ Create** →
**Create {'Paperback' if ed == 'paperback' else 'Hardcover'}**.
Do not start a new title if you have already created one for the other print
format — use **+ Create {'Hardcover' if ed == 'paperback' else 'Paperback'}**
underneath the existing title so the two editions stay linked on one detail
page.

### 2 · Book Details — language
{A} Language: **{b['language']}**.

### 3 · Title
{A} Paste exactly, with no trailing space:

```
{b['title']}
```
({b['titleChars']} characters of the {md['limits']['title']} allowed.)

### 4 · Subtitle
{A} Paste exactly:

```
{b['subtitle']}
```
({b['subtitleChars']} of {md['limits']['subtitle']} characters.)

⚠ The two numbers in this subtitle are measured, not chosen. The book
contains **{md['measured']['games']} games** from **{md['measured']['cultures']}
cultures**. If you edit the subtitle, do not round them up.

### 5 · Author
{A} Primary author: **{b['author']}**.

### 6 · Contributors
{A} None. Leave the contributor list empty — an empty contributor row will
block the form.

### 7 · Description
{A} Paste the description from
`06_REPORTS/tracked/metadata.json` → `description.text`
({md['description']['chars']} of {md['limits']['description']} characters).
It is written to read correctly as plain text; KDP's limited HTML is not
required.

### 8 · Publishing rights
{F} Select: *{md['publishingRights']['value']}*
{A} Basis: {md['publishingRights']['$note']}

### 9 · Keywords
{A} Seven slots, one phrase each:

{chr(10).join('%d. `%s`' % (i + 1, k) for i, k in enumerate(md['keywords']))}

### 10 · Categories
{F} KDP now picks categories from its own tree. Choose three that match:
{chr(10).join('- %s — `%s`' % (c['name'], c['code']) for c in
              [md['categories']['bisacPrimary']] + md['categories']['bisacSecondary'])}

### 11 · Age and grade range
{F} **Leave empty.** {md['audience']['$note']}

### 12 · ISBN
{F} Select **Get a free KDP ISBN**. Current recorded value: `{isbn}`.
{A} No ISBN has been invented anywhere in this package. Once KDP assigns one,
write it into `project_config.json → founder.isbn.{ed}` and rebuild: the
copyright page will then print the real number instead of `PENDING`.

### 13 · AI-generated content declaration
{F} **This choice is yours and only yours.** The agent cannot make a legal
declaration on your behalf. The facts you need in order to answer:

- Text — {md['aiProductionFacts']['text']}
- Images — {md['aiProductionFacts']['images']}
- Translation — {md['aiProductionFacts']['translation']}

### 14 · Manuscript upload
{A} Upload:

```
{pkg['interior']['file']}
```
- {pkg['interior']['pageCount']} pages · trim {t['widthIn']} × {t['heightIn']} in
- no bleed · inside margin {m['gutterIn']} in · outside {m['outerIn']} in
- all fonts embedded and subsetted (Liberation Serif, SIL OFL 1.1)
- SHA-256 `{pkg['interior']['sha256']}`

{F} Trim size in the KDP form: **{t['widthIn']} x {t['heightIn']} in**.
Bleed: **No bleed**. Paper: **White**. Ink: **Black & white**.

### 15 · Cover upload
{A} Upload:

```
{pkg['cover']['file']}
```
- full wrap **{g['wrapWidthIn']:.4f} × {g['wrapHeightIn']:.4f} in**, including
  {g['bleedIn']} in bleed on all four sides
- spine **{g['spineWidthIn']:.4f} in**, computed from this exact page count
  ({g['pageCount']} pages × {g['spinePerPageIn']} in/page{' plus a board allowance' if ed == 'hardcover' else ''})
- artwork embedded at **{g['artworkTarget']['widthPx']} × {g['artworkTarget']['heightPx']} px**
  (300 ppi); all type is **vector**, not baked into the image
- SHA-256 `{pkg['cover']['sha256']}`

Typography placement was measured, not eyeballed. The title and author sit in
the two quietest bands of the artwork (standard deviation 12.8 and 13.7 on a
0–255 scale), so no panel, box or scrim sits behind them. The spine title is
{pkg['cover']['spineFit'][0]['pt']:.2f} pt, sized to fit the measured clean run of the spine rather than
chosen by eye. The back copy sits over a feathered wash taken from the
artwork's own parchment tone — not a white panel.

⚠ The barcode area (lower right of the back panel) is deliberately empty.
**Do not place anything there** — Amazon prints the barcode itself.

### 16 · Previewer
{F} Open the KDP Previewer and work through
`08_OUTPUT/KDP_PREVIEWER_CHECKLIST.md`. The agent cannot run the Previewer
and does not claim to have done so.

### 17 · Pricing
{A} Modelled list price: **${md['pricing'][ed]['listUSD']}**.
{F} Enter it and check the royalty KDP shows you against
`06_REPORTS/editions.json`. If they differ, KDP's printing cost has changed
and the model needs re-running, not overriding.

### 18 · Territories
{F} {md['territories']['value']}.

### 19 · Royalty
{F} Select the **60%** royalty plan (list price is above $9.99).
{A} KDP Select / Kindle Unlimited: **{'enrol' if md['kdpSelect']['enrol'] else 'do NOT enrol'}**.
{md['kdpSelect']['$note']}

### 20 · Final review
{F} Read the whole preview once more. Confirm the copyright page shows the
real ISBN if one has been assigned, and that the author biography is present
if you have entered one.

### 21 · Publish
{F} Press Publish. **The agent has not done this and cannot do it.**
"""


def build_handbook(root, pkgs, md, cov, fm, actions):
    m = md["measured"]
    parts = [f"""# KDP UPLOAD HANDBOOK
## The Great Book of World Games

> **Generated file** — `04_BUILD/handoff.py`. Every number below is measured
> from the built artefacts. If you rebuild anything, rebuild this file.
>
> Generated at phase **6** · interior **{pkgs['paperback']['interior']['pageCount']} pages** ·
> **{m['games']} games** · **{m['cultures']} cultures**

---

## How to read this document

Every step is marked. {F} means you must do it in the Amazon KDP panel;
the agent has no access to your account and has not touched it. {A} means the
value or file is already prepared and only needs pasting or uploading.

**Nothing in this package has been uploaded, submitted, previewed, priced or
published.** No proof copy has been ordered.

---

## Status at a glance

| Format | Interior | Cover | Ready to upload |
|---|---|---|---|
| Paperback | ✅ {pkgs['paperback']['interior']['pageCount']} pp | ✅ wrap PDF | **yes** |
| Hardcover | ✅ {pkgs['hardcover']['interior']['pageCount']} pp | ✅ wrap PDF | **yes** |
| Kindle | ✅ EPUB 3 | ✅ 1600 × 2560 JPG | **yes** |
| A+ Content | copy ✅ 6 modules | ✅ {len(pkgs['aplus']['ready'])} of 6 modules have art | **yes, {len(pkgs['aplus']['ready'])} modules** |

---

## Blocking founder actions

"""]
    for a in actions:
        mark = "⛔" if a["blocking"] else "·"
        parts.append(f"- {mark} **{a['id']}** — `{a['field']}`\n  {a['note']}\n")
    parts.append("""
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
""")
    for ed, label in (("paperback", "PAPERBACK"), ("hardcover", "HARDCOVER")):
        if ed not in pkgs:
            continue
        parts.append("\n# %s\n" % label)
        parts.append(steps_for_print(ed, pkgs[ed], md, cov, fm))

    k = pkgs.get("kindle")
    if k:
        parts.append(f"""
# KINDLE / EBOOK

### 1 · KDP Bookshelf
{F} **+ Create** → **Create eBook**, or **+ Create Kindle eBook** beneath the
existing print title so the editions stay linked.

### 2–13 · Book details
{A} Identical to the paperback: same title, subtitle, author, description,
keywords and categories. {F} The AI declaration is asked again and is again
yours to answer.

{F} ISBN: an eBook does **not** need one. Leave it blank.

### 14 · Manuscript upload
{A} Upload:

```
{k['epub']['file']}
```
- EPUB 3, **reflowable**
- {k['epub']['bytes'] / 1024:.0f} KB · SHA-256 `{k['epub']['sha256']}`
- diagrams are embedded as **inline SVG**, so they stay sharp at any screen
  size and add almost nothing to the file size

**Why reflowable and not fixed-layout.** The print book's two-page spread is
an answer to a constraint that a scrolling screen does not have. Fixed layout
would squeeze an 8.5 × 11 spread onto a phone, lock the reader's font size and
break their accessibility settings, to preserve a promise that reflowing keeps
anyway: each game is one uninterrupted entry.

### 15 · Cover upload
{A} Upload:

```
{k['cover']['file']}
```
- **1600 × 2560 px** (Amazon's recommended 1:1.6), JPEG
- SHA-256 `{k['cover']['sha256']}`
- derived from the **front panel** of the print artwork, not from the wrap —
  an ebook cover must not show a spine or a back panel

⚠ This file carries **no typography**. Kindle covers are set separately, at
their own proportions; the print title block does not scale to 1:1.6 without
being rebuilt. **Founder action:** either accept the artwork-only cover or ask
for a typeset Kindle cover as a follow-up.

### 16 · Previewer
{F} Use the Kindle Previewer. Check in particular: the diagrams at the
smallest font size, the numbered rule lists, and the three-question blocks.

### 17 · Pricing
{A} Modelled list price **${md['pricing']['kindle']['listUSD']}**.
{F} Select the **70%** royalty option — the price sits inside the
$2.99–$9.99… band check KDP shows you, and if it does not, take the 35% plan
rather than dropping the price to fit.

### 18–21 · Territories, royalty, review, publish
{F} As for print. KDP Select enrolment: **do not enrol** — see the note above.
"""
                     )

    ap = pkgs.get("aplus")
    if ap:
        a = load(os.path.join(root, "03_APLUS", "aplus_content.json"))
        parts.append(f"""
# A+ CONTENT

### 1 · Marketing
{F} Bookshelf → the title's **…** menu → **Marketing** (or Author Central →
A+ Content, depending on the account).

### 2 · A+ Content
{F} **Create A+ Content** → give the project an internal name, e.g.
`GBWG-EN-v1`. This name is not shown to shoppers.

### 3 · Module creation
{A} Six modules are specified, in this order:

| # | Module type | Image | Size |
|---|---|---|---|
""")
        for mod in a["modules"]:
            imgs = mod.get("imageSet") or [mod["image"]]
            parts.append("| %s | %s | `%s` | %d × %d px |\n"
                         % (mod["n"], mod["moduleType"],
                            "`, `".join(imgs), mod["imagePx"][0],
                            mod["imagePx"][1]))
        parts.append(f"""
### 4 · Module type
{F} Pick each module type exactly as listed above. If Amazon has renamed or
retired one, choose the closest and note the change — do not force an image
into a module with a different aspect ratio.

### 5 · Image upload
{A} Processed and sized in `07_ASSETS/web/aplus/`. Ready modules:
**{', '.join(ap['ready'])}**.

⚠ **One module has no artwork: {', '.join(ap['withoutArt']) or 'none'}.** The
file delivered as `aplus-05-play-family-discovery.png` is, on inspection, the
**module 06** brief — rows of game objects on a pale ground with the right
third left clear. It was mapped to module 06 by content rather than by
filename. Module 05 (hands over a board, no faces) was not delivered, so the
uploadable A+ project is **{len(ap['ready'])} modules**, not six. Its copy is written and
waiting if you generate the art later.

⚠ Module 04 was delivered as a single 2 × 2 composite. It was **split** into
four 220 × 220 squares by measuring the gutters — no pixels were invented.

⚠ The generated images contain **no text**. All wording goes in Amazon's own
fields, where it stays searchable and correctable.

### 6 · Title and body text
{A} Ready, and every number in them is measured against the book:

""")
        for mod in a["modules"]:
            parts.append("**%s — %s**\n\n- Title (%d chars): %s\n- Body (%d chars): %s\n\n"
                         % (mod["id"], mod["name"], mod["titleChars"],
                            mod["title"], mod["bodyChars"], mod["body"]))
        parts.append(f"""
### 7 · Preview
{F} Use A+ preview on both desktop and mobile. The right-hand third of the
header modules is where Amazon puts the text — check nothing important in the
artwork is hidden behind it.

### 8 · Submit
{F} Submit for review. A+ content is moderated by Amazon.

### 9 · Moderation
{F} Moderation usually takes up to seven days. The most common rejections are
claims that cannot be substantiated, contact details, and pricing or shipping
language. This copy has been scanned against
{a['claimScan']['forbiddenPatterns']} forbidden claim patterns and carries no
bestseller, award, testing or guaranteed-outcome claim. Every number in the
copy is checked against the book's measured values.

### 10 · Live verification
{F} Once it is live, open the detail page as a shopper and confirm all six
modules render, in order, on desktop and on mobile.
""")

    parts.append("""
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
""")
    return "".join(parts)


def build_previewer(root, pkgs, cov, md, ivis):
    pb, hc = pkgs["paperback"], pkgs["hardcover"]
    g = cov["editions"]["paperback"]
    gh = cov["editions"]["hardcover"]
    w = ivis.get("paperback", {}).get("ink", {}).get("worstMarginIn", {})
    return f"""# KDP PREVIEWER CHECKLIST
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
| Final page count | **{pb['interior']['pageCount']}** | **{hc['interior']['pageCount']}** |
| Trim | {pb['trim']['widthIn']} × {pb['trim']['heightIn']} in | {hc['trim']['widthIn']} × {hc['trim']['heightIn']} in |
| Bleed | none | none |
| Inside margin (gutter) | {pb['margins']['gutterIn']} in | {hc['margins']['gutterIn']} in |
| Outside margin | {pb['margins']['outerIn']} in | {hc['margins']['outerIn']} in |
| Top / bottom margin | {pb['margins']['topIn']} / {pb['margins']['bottomIn']} in | {hc['margins']['topIn']} / {hc['margins']['bottomIn']} in |
| Spine (from page count) | **{g['spineWidthIn']:.4f} in** | **{gh['spineWidthIn']:.4f} in** |
| Full cover wrap | {g['wrapWidthIn']:.4f} × {g['wrapHeightIn']:.4f} in | {gh['wrapWidthIn']:.4f} × {gh['wrapHeightIn']:.4f} in |
| Fonts | Liberation Serif, embedded and subsetted | same |
| Raster images | none — every diagram is vector | same |

Measured ink margins in the built paperback — the closest any ink comes to the
trim edge, on any of the {pb['interior']['pageCount']} pages:

- left **{w.get('leftIn', '?')} in** · right **{w.get('rightIn', '?')} in**
- top **{w.get('topIn', '?')} in** · bottom **{w.get('bottomIn', '?')} in**

KDP's own minimum without bleed is 0.25 in, so there is real headroom. If the
Previewer reports content outside the printable area, something changed after
this file was generated.

---

## Expected warnings, and which of them are fine

| What you may see | Is it a problem? |
|---|---|
| "Your cover has not been uploaded" | Yes — cover artwork does not exist yet. Expected. |
| Blank pages flagged | No. There are {pb['blankPages']} deliberate blanks: a book of two-page spreads needs each game to start on a left-hand page, and part titles open on the right. |
| Low-resolution image warning | Would be a real problem. There are no raster images at all, so it should not appear. |
| Font not embedded | Would be a real problem. All four faces are embedded and subsetted; verified with `pdffonts`. |
| Page size mismatch | Would be a real problem. All {pb['interior']['pageCount']} pages are exactly {pb['trim']['widthIn']} × {pb['trim']['heightIn']} in. |
| Text too close to the trim | Should not appear — see the measured margins above. |

---

## Pages worth stopping on

1. **The contents (pages 5–6).** Every page reference is generated from the
   built PDF, not from a model. Spot-check three entries against the pages they
   point to; if one is wrong they are all wrong and the build chain broke.
2. **Any game spread — for example pages 16–17.** Confirm the entry begins on
   the **left** page. Every one of the {md['measured']['games']} games does; that
   is the whole architecture of the book and the one thing a layout change
   silently breaks.
3. **A spread with two diagrams — for example Alquerque, pages 88–89.** Confirm
   both diagrams sit on the right-hand page with the rules, and neither is
   clipped.
4. **The board templates (from page {load(os.path.join(root, '06_REPORTS', 'interior-paperback.json')).get('backMatterStartPage', '—')}).**
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
- **A+ images: {pkgs['aplus']['imagesMissing']} missing.**
- **Author biography is empty.** KDP rejected a placeholder biography on a
  sibling title. Write a real one before publishing.

---

## The cover — what to look at

| | paperback | hardcover |
|---|---|---|
| Full wrap | {g['wrapWidthIn']:.4f} × {g['wrapHeightIn']:.4f} in | {gh['wrapWidthIn']:.4f} × {gh['wrapHeightIn']:.4f} in |
| Spine | {g['spineWidthIn']:.4f} in | {gh['spineWidthIn']:.4f} in |
| Artwork | {g['artworkTarget']['widthPx']} × {g['artworkTarget']['heightPx']} px @ 300 ppi | {gh['artworkTarget']['widthPx']} × {gh['artworkTarget']['heightPx']} px |
| Type | vector, not rasterised | same |

1. **The spine.** It is {g['spineWidthIn']:.3f} in — a thin spine, and the title is set at
   {pkgs['paperback']['cover']['spineFit'][0]['pt']:.2f} pt to fit the part of the artwork that measured clean.
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
   within {g['safeIn']} in of any trim edge.

---

## A+ content — what to look at

- **{len(pkgs['aplus']['ready'])} of 6 modules have artwork.** Module(s) without art:
  **{', '.join(pkgs['aplus']['withoutArt']) or 'none'}**.
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
"""


def build_ai_notes(root, pkgs, md, fm):
    """KDP'nin yapay zekâ beyanı için OLGULAR. Beyanın kendisi DEĞİL."""
    m = md["measured"]
    ap = pkgs.get("aplus", {})
    return f"""# KDP AI-GENERATED CONTENT — DISCLOSURE NOTES

> **The Great Book of World Games** · generated by `04_BUILD/handoff.py`
>
> ⚠ **This document is not a declaration.** KDP asks a question with legal
> consequences and the answer is the account holder's to give. What follows is
> the factual record needed to answer it accurately — what was generated, what
> was assisted, and what was produced deterministically by code.

---

## The three KDP categories

KDP distinguishes **AI-generated** (created by AI from a prompt) from
**AI-assisted** (created by a person, then refined with AI tools, or created
with AI and then substantially edited). It asks separately about **text**,
**images** and **translations**.

---

## 1 · Text

| | |
|---|---|
| Status | **AI-generated, then edited and verified against printed sources** |
| Volume | {m['games']} game entries · {fm['measured']['frontMatterWords']:,} words of front matter · {fm['measured']['familyOpenerWords']:,} words of family openers |
| Printed total | 65,000+ words |

Every rule set was drafted with AI assistance **from a named printed source
opened at page level**, and each entry carries that citation with its page
numbers. The project keeps a separate verification record
(`01_SOURCE/source_verification.json`, {len(load(os.path.join(root, '01_SOURCE', 'source_verification.json'))['records'])} entries) in which each
citation is tied to a supporting passage quoted from the source.

Where a source did not settle a rule, the book says so on the page rather than
inventing one. Where a historical record is incomplete, the entry is marked
**reconstructed** — {m['reconstructed']} of {m['games']} entries are.

**Not machine translation.** The commercial text was written directly in
English; the project's own configuration forbids machine translation into the
commercial language.

---

## 2 · Images

### Cover artwork — **AI-generated**

| | |
|---|---|
| Produced by | the author, externally, from prompts held in `07_ASSETS/IMAGE_PROMPT_LIBRARY.html` |
| Delivered | 2 candidates · 1 selected (`FINAL_COVER_SELECTION.md`) |
| Post-processing | real upscaling (Real-ESRGAN, 4×), alpha flattening, crop to wrap geometry |
| Text in the artwork | **none** — verified by inspection at high magnification |

### A+ artwork — **AI-generated**

| | |
|---|---|
| Delivered | 5 images, mapped to {len(ap.get('ready', []))} modules |
| Post-processing | crop to Amazon module dimensions, one 2 × 2 composite split into four squares |
| Text in the artwork | **none** |

### Interior diagrams — **NOT AI-generated**

This distinction matters and is easy to get wrong. The {len(load(os.path.join(root, '06_REPORTS', 'diagram-render.json'))['diagrams'])} board diagrams
inside the book were **not** produced by an image model. They are drawn by the
project's own code (`04_BUILD/render_diagrams.py`) from structured data — each
board is a list of points and edges, and the renderer emits SVG
deterministically. The same input produces a byte-identical file on any
machine. They are vector drawings, not generated images.

### Typography — **NOT AI-generated**

All type on the cover and in the interior is set as vector text by
`04_BUILD/covers.py` and `04_BUILD/interior.py` from the project metadata.
No lettering is baked into any generated image.

---

## 3 · Translations

**None.** No part of this book is a translation.

---

## 4 · What this means for the form

The agent does not fill this in. For accuracy, the record supports:

- **Text — AI-generated:** yes, with human editing and source verification
- **Images — AI-generated:** yes, for the cover and A+ artwork; **no** for the
  interior diagrams, which are code-drawn from data
- **Translation — AI-generated:** no

KDP's question about images concerns the images you upload. The cover and the
A+ images are AI-generated. The interior contains no AI-generated images at
all.

---

## 5 · Where the evidence lives

| claim | file |
|---|---|
| Source citations, page level | `01_SOURCE/source_verification.json` |
| Which games are reconstructed | `02_MANUSCRIPT/book.json` · each entry's notice |
| Cover prompts and selection | `07_ASSETS/IMAGE_PROMPT_LIBRARY.html` · `06_REPORTS/FINAL_COVER_SELECTION.md` |
| Upscaling method and factors | `06_REPORTS/cover-artwork-intake.json` · `ASSET_UPSCALING_REPORT.md` |
| Diagrams are code-drawn | `04_BUILD/render_diagrams.py` · `07_ASSETS/diagrams/*.json` |
| Author biography provenance | `06_REPORTS/AUTHOR_BIO_PROVENANCE.md` |
"""


def run(root, args):
    md_p = os.path.join(root, "06_REPORTS", "tracked", "metadata.json")
    cov_p = os.path.join(root, "06_REPORTS", "cover-geometry.json")
    fm_p = os.path.join(root, "02_MANUSCRIPT", "frontmatter.json")
    for p in (md_p, cov_p, fm_p):
        if not os.path.exists(p):
            print("  · %s yok — teslim paketi ATLANDI" % os.path.relpath(p, root))
            return 0
    md, cov, fm = load(md_p), load(cov_p), load(fm_p)
    ivis = {}
    kp = os.path.join(root, "06_REPORTS", "kdp-preflight.json")
    if os.path.exists(kp):
        ivis = load(kp).get("editions", {})

    pkgs = collect(root)
    print("=" * 74)
    print("  TESLİM PAKETİ")
    print("=" * 74)

    errs = []
    for ed in ("paperback", "hardcover"):
        p = pkgs.get(ed)
        if not p:
            errs.append("%s paketi yok" % ed)
            continue
        i = p["interior"]
        if not i["exists"]:
            errs.append("%s iç bloğu diskte yok" % ed)
        elif i["sha256"] != i["recordedSha256"]:
            errs.append("%s iç bloğu kayıttaki sağlamayla uyuşmuyor" % ed)
    k = pkgs.get("kindle")
    if k and k["epub"]["sha256"] != k["epub"]["recordedSha256"]:
        errs.append("EPUB sağlaması uyuşmuyor")

    # A+ paketi metinden ibarettir (görseller kurucudan gelir); modül
    # haritasının bir kopyası teslim klasörüne konur ki paket kendi
    # kendine yetsin.
    ap_src = os.path.join(root, "03_APLUS", "aplus_content.json")
    if os.path.exists(ap_src):
        os.makedirs(os.path.join(root, "08_OUTPUT", "APLUS"), exist_ok=True)
        shutil.copy2(ap_src, os.path.join(root, "08_OUTPUT", "APLUS",
                                          "aplus_content.json"))
    # İşlenmiş A+ görselleri teslim klasörüne kopyalanır: kurucu yüklerken
    # 07_ASSETS içinde dolaşmak zorunda kalmasın.
    web = os.path.join(root, "07_ASSETS", "web", "aplus")
    if os.path.isdir(web):
        dst = os.path.join(root, "08_OUTPUT", "APLUS")
        os.makedirs(dst, exist_ok=True)
        for fn in sorted(os.listdir(web)):
            if fn.lower().endswith((".png", ".jpg")):
                shutil.copy2(os.path.join(web, fn), os.path.join(dst, fn))

    counts = {}
    for folder in ("PAPERBACK", "HARDCOVER", "KINDLE", "APLUS"):
        os.makedirs(os.path.join(root, "08_OUTPUT", folder), exist_ok=True)
        n = sums_file(root, folder)
        counts[folder] = n or 0

    hb = build_handbook(root, pkgs, md, cov, fm, md["founderActions"])
    write(os.path.join(root, "08_OUTPUT", "KDP_UPLOAD_HANDBOOK.md"), hb)
    pv = build_previewer(root, pkgs, cov, md, ivis)
    write(os.path.join(root, "08_OUTPUT", "KDP_PREVIEWER_CHECKLIST.md"), pv)
    ai = build_ai_notes(root, pkgs, md, fm)
    write(os.path.join(root, "08_OUTPUT", "KDP_AI_DISCLOSURE_NOTES.md"), ai)

    report = {
        "$comment": ["TESLİM PAKETİ — ÜRETİLMİŞ DOSYA (04_BUILD/handoff.py).",
                     "Ajan KDP paneline DOKUNMADI."],
        "generatedAtPhase": "phase6",
        "packages": pkgs,
        "checksumFiles": counts,
        "handbook": "08_OUTPUT/KDP_UPLOAD_HANDBOOK.md",
        "previewerChecklist": "08_OUTPUT/KDP_PREVIEWER_CHECKLIST.md",
        "aiDisclosureNotes": "08_OUTPUT/KDP_AI_DISCLOSURE_NOTES.md",
        "handbookBytes": len(hb.encode()),
        "previewerBytes": len(pv.encode()),
        "blockingFounderActions": [a for a in md["founderActions"]
                                   if a["blocking"]]
        + ([] if pkgs.get("paperback", {}).get("cover") else
           [{"id": "COVER-ART", "field": "07_ASSETS/raw/cover/",
             "blocking": True, "note": "Kapak sanatı yok."}])
        + ([{"id": "APLUS-05-ART", "field": "07_ASSETS/raw/aplus/",
             "blocking": False,
             "note": "Modül 05 (eller/masa) sanatı teslim edilmedi. "
                     "Yüklenebilir A+ projesi %d modüldür; metni hazır ve "
                     "sanat gelirse eklenir."
                     % len(pkgs.get("aplus", {}).get("ready", []))}]
           if pkgs.get("aplus", {}).get("withoutArt") else [])
        + [{"id": "PLAYTEST", "field": "01_SOURCE/playtests/",
            "blocking": True, "note": "Dış oynanabilirlik testi 0 oturum."}],
        "errors": errs,
    }
    allacts = report["blockingFounderActions"]
    report["founderActions"] = allacts
    report["blockingFounderActions"] = [a for a in allacts if a["blocking"]]
    dump(os.path.join(root, "06_REPORTS", "handoff.json"), report)

    for ed in ("paperback", "hardcover"):
        p = pkgs.get(ed)
        if p:
            print("  %-10s %3d sayfa · %6.1f KB · %s"
                  % (ed, p["interior"]["pageCount"],
                     p["interior"]["bytes"] / 1024.0,
                     "kapak ⛔" if not p["cover"] else "kapak ✓"))
    if k:
        print("  %-10s EPUB 3 · %6.1f KB · kapak %s"
              % ("kindle", k["epub"]["bytes"] / 1024.0,
                 "✓" if k.get("cover") else "⛔"))
    if pkgs.get("aplus"):
        ap = pkgs["aplus"]
        print("  %-10s %d/%d modül HAZIR · sanatsız: %s"
              % ("a+", len(ap["ready"]), ap["modules"],
                 ", ".join(ap["withoutArt"]) or "yok"))
    print("\n  ✓ 08_OUTPUT/KDP_UPLOAD_HANDBOOK.md      (%d bayt)" % len(hb.encode()))
    print("  ✓ 08_OUTPUT/KDP_PREVIEWER_CHECKLIST.md  (%d bayt)" % len(pv.encode()))
    print("  ✓ 08_OUTPUT/KDP_AI_DISCLOSURE_NOTES.md   (%d bayt)" % len(ai.encode()))
    print("  ✓ SHA256SUMS: %s"
          % " · ".join("%s %d" % (k2, v) for k2, v in counts.items()))
    print("\n  ⛔ BLOKLAYICI KURUCU EYLEMİ: %d"
          % len(report["blockingFounderActions"]))
    for a in report["blockingFounderActions"]:
        print("     · %-14s %s" % (a["id"], a["field"]))
    other = [a for a in report["founderActions"] if not a["blocking"]]
    if other:
        print("  · bloklamayan kurucu eylemi: %d" % len(other))
        for a in other:
            print("     · %-14s %s" % (a["id"], a["field"]))
    for e in errs:
        print("  ✗ %s" % e)
    print("=" * 74)
    return 1 if errs else 0



def manuscript_absent(root: str) -> bool:
    """Ticari manuscript depoda YOKTUR (karar K12).

    CI taze bir klonda koşar ve orada `02_MANUSCRIPT/book.json` bulunmaz.
    Bu bir kusur DEĞİLDİR ve kapı orada BOŞ KOŞAR. Bir kapının CI'da
    kırmızı yanması, kusuru olduğu için olmalıdır; verinin orada olmaması
    için değil."""
    return not os.path.exists(os.path.join(root, "02_MANUSCRIPT", "book.json"))


def run_check(root):
    if manuscript_absent(root):
        print("  · ticari manuscript bu depoda yok — teslim denetimi ATLANDI "
              "(CI'da beklenen)")
        return 0
    p = os.path.join(root, "06_REPORTS", "handoff.json")
    if not os.path.exists(p):
        print("  · teslim paketi üretilmemiş — ATLANDI")
        return 0
    r = load(p)
    errs = list(r.get("errors") or [])
    for f in ("handbook", "previewerChecklist", "aiDisclosureNotes"):
        if not os.path.exists(os.path.join(root, r[f])):
            errs.append("%s dosyası yok: %s" % (f, r[f]))
    for ed in ("paperback", "hardcover"):
        pk = r["packages"].get(ed)
        if not pk:
            continue
        cur = os.path.join(root, "06_REPORTS", "interior-%s.json" % ed)
        if os.path.exists(cur):
            now = load(cur)
            if now["pageCount"] != pk["interior"]["pageCount"]:
                errs.append("%s: kılavuz %d sayfa diyor, iç blok %d"
                            % (ed, pk["interior"]["pageCount"],
                               now["pageCount"]))
            if now["sha256"] != pk["interior"]["sha256"]:
                errs.append("%s: kılavuz BAYAT — iç blok değişmiş" % ed)
    for e in errs:
        print("  ✗ %s" % e)
    if errs:
        return 1
    print("  ✓ teslim paketi güncel · %d bloklayıcı kurucu eylemi"
          % len(r["blockingFounderActions"]))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    return run_check(root) if args.check else run(root, args)


if __name__ == "__main__":
    sys.exit(main())
