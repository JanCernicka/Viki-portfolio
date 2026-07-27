# Viktória Mikušková — Portfolio

A faithful static recreation of the [viktoriamikuskova.com](https://viktoriamikuskova.com) portfolio landing page for **Mgr. Viktória Mikušková**, a graphic designer & marketer from Bratislava.

## Stack

- Plain, dependency-free **HTML + CSS** (single page)
- Self-hosted fonts: **Playfair Display** (headings) and **Montserrat** (UI/body) — `assets/fonts/`
- All illustrations, the portrait, logo, service icons and the software row are the original images, extracted from the source and stored in `assets/images/`
- Brand / contact icons are inline SVG

## Structure

```
index.html          # markup for all sections
styles.css          # design system: palette, type, layout, responsive rules
assets/
  images/           # hero, portrait, logo, service icons, software row
  fonts/            # woff2 (latin + latin-ext) + fonts.css
_headers            # Cloudflare Pages cache rules for /assets/*
```

## Sections

Header/nav · Hero · Knižný dizajn · Ďalšia tvorba · Čomu sa venujem · O mne ·
Kde čarujem · Moja kreatívna cesta · Footer/Kontakt.

The homepage leads with book design and puts the other disciplines directly
below it, so the same site serves a publisher and a studio without either
having to hunt through the menu.

## Palette

| Token | Hex | Use |
|-------|-----|-----|
| Cream | `#FBEFE3` | page background |
| Terracotta | `#C6673D` | accents, links, italics |
| Olive | `#676340` | section labels |
| Button olive | `#666240` | CTA button |
| Sage | `#ACB783` | icon circles |
| Peach | `#F1CBAC` | icon circles |
| Dark | `#011126` | headings |


## Adding projects

Project content lives in one place: **`content/projects.json`**. The HTML is
generated from it.

```bash
python3 build.py
```

This regenerates `index.html`, the two category pages and one page per project
under `projekt/`. Nothing else is touched.

To add or finish a project, edit its entry in `content/projects.json`:

| Field | Notes |
|---|---|
| `cover`, `images[].src` | Paths under `assets/projects/…`. `null` renders a placeholder block at the right aspect ratio. |
| `orientation` | `portrait` for book covers, `landscape`, or `square`. Drives the thumbnail ratio. |
| `status` | `skolsky` · `komercny` · `publikovany` · `koncept` — renders a badge. |
| `brief`, `solution`, `why` | The case-study text. `null` renders a visible "doplniť" marker. |
| `featured` | Shows the project on the homepage. |
| `order` | Controls sequence — lowest first. Put the strongest work first. |

Images should be at least 2000 px on the long edge.

## Documents (CV, sendable portfolio, letterhead, promo, signature)

Everything that gets emailed or printed is generated from the same data and the
same brand tokens as the site.

The sendable portfolio comes in two variants, defined by `VARIANTS` in
`build_docs.py`. They are not two portfolios — they are one body of work entered
from two doors. Each leads with the discipline its reader asked about, in full
pages, and closes with the other as a one-page contact sheet.

```bash
python3 build_docs.py   # regenerates the HTML pages
node make_pdf.js        # renders them to PDF
```

| Page | PDF | What it's for |
|---|---|---|
| `cv.html` | `assets/cv/Viktoria-Mikuskova-CV.pdf` | One-page A4 CV |
| `portfolio-knihy.html` | `assets/dokumenty/…-portfolio-knizny-dizajn.pdf` | Portfolio for publishers: book work in full, everything else as a closing contact sheet |
| `portfolio-grafika.html` | `assets/dokumenty/…-portfolio-grafika.pdf` | Same work for studios and agencies, the other way round |
| `hlavickovy-papier.html` | `assets/dokumenty/…-hlavickovy-papier.pdf` | Letterhead; the body is `contenteditable`, so the letter can be typed in the browser and printed to PDF |
| `promo.html` | `assets/dokumenty/…-zalozky.pdf` | Promo piece — 4 bookmarks (45 × 180 mm) per A4, front and back |
| `podpis.html` | — | Email signature plus paste instructions for Gmail and Outlook |
| `dokumenty.html` | — | Index of all of the above. Not in the nav, `noindex`. |

The site address is defined **once**, as `SITE_URL` in `build_docs.py`. Change it
there and rerun both commands and it updates in the CV, the letterhead, the
bookmarks, the QR code and the email signature.

`/assets/cv/*` and `/assets/dokumenty/*` are served with a 5-minute cache and
the rest of `/assets/*` with a day, both revalidating (`_headers`). Nothing is
`immutable`: images get replaced while the portfolio is being built, and a
year-long cache strands anyone who already loaded the page. Cloudflare Pages
concatenates every matching rule into one header instead of letting the
narrowest win, so the specific rules are listed **first**.

## Local preview

```bash
python3 -m http.server 8099
# open http://localhost:8099
```

## Deploy (Cloudflare Pages)

Static site — no build step.

- **Build command:** *(none)*
- **Build output directory:** `/` (repository root)

Connect this repository in the Cloudflare Pages dashboard, or deploy with Wrangler:

```bash
npx wrangler pages deploy . --project-name <your-project>
```
