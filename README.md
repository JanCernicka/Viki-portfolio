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
_headers            # Cloudflare Pages long-cache rules for /assets/*
```

## Sections

Header/nav · Hero · Služby (services) · Vybrané projekty · O mne · Kde čarujem · Moja kreatívna cesta · Footer/Kontakt.

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
