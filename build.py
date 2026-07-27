#!/usr/bin/env python3
"""
Generátor portfólia Viktórie Mikuškovej.

Zdroj dát:  content/projects.json
Spustenie:  python3 build.py

Generuje:   index.html, knizny-dizajn.html, dalsia-tvorba.html
            projekt/<slug>.html pre každý projekt

Statické súbory (styles.css, script.js, assets/) sa negenerujú.
"""

import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "content", "projects.json")
PROJ_DIR = os.path.join(ROOT, "projekt")

SITE_NAME = "Viktória Mikušková"
TAGLINE = "Grafická dizajnérka"

CATEGORIES = {
    "knizny-dizajn": {
        "title": "Knižný dizajn",
        "lead": "Obálky, sadzba a propagácia kníh — od žánrovej analýzy po hotovú tlačovú predlohu.",
        "groups": [
            ("obalky", "Obálky kníh", "Obálky"),
            ("sadzba", "Sadzba a dvojstrany", "Sadzba"),
            ("knizna-ilustracia", "Knižná ilustrácia", "Ilustrácia"),
            ("propagacia", "Plagáty a propagácia", "Propagácia"),
        ],
    },
    "dalsia-tvorba": {
        "title": "Ďalšia tvorba",
        "lead": "Branding, ilustrácia, informačný dizajn a marketingové vizuály.",
        "groups": [
            ("branding", "Branding a vizuálna identita", "Branding"),
            ("produktovy-dizajn", "Produktový dizajn a obaly", "Produktový dizajn"),
            ("ilustracia", "Ilustrácia", "Ilustrácie"),
            ("informacny-dizajn", "Informačný dizajn", "Informačný dizajn"),
            ("uiux", "UI/UX dizajn", "UI/UX dizajn"),
            ("marketing", "Sociálne siete a marketing", "Sociálne siete"),
        ],
    },
}

STATUS = {
    "skolsky":    ("Školský projekt", "st-school"),
    "komercny":   ("Komerčná práca", "st-commercial"),
    "publikovany": ("Publikované", "st-published"),
    "koncept":    ("Koncepčný redizajn", "st-concept"),
}

ASPECT = {"portrait": "is-portrait", "landscape": "is-landscape", "square": "is-square"}

CARET = ('<svg viewBox="0 0 448 512" width="12" height="12" aria-hidden="true"><path fill="currentColor" '
         'd="M201.4 374.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 '
         '306.7 86.6 169.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg>')


def esc(s):
    if s is None:
        return ""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def head(title, description, depth=0):
    up = "../" * depth
    return f'''<!DOCTYPE html>
<html lang="sk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="icon" type="image/png" href="{up}assets/images/logo.png">
<link rel="stylesheet" href="{up}assets/fonts/fonts.css">
<link rel="stylesheet" href="{up}styles.css">
</head>
<body>
'''


def header(active, depth=0, projects=None):
    up = "../" * depth
    def cls(name):
        return ' class="active"' if name == active else ""

    # Rozbaľovacie menu pre Ďalšiu tvorbu — len disciplíny, ktoré majú projekt.
    # Nová disciplína sa objaví automaticky, len čo k nej priradíš projekt.
    projects = projects or []
    used = {p.get("subcategory") for p in projects if p.get("category") == "dalsia-tvorba"}
    items = "".join(
        f'          <a href="{up}dalsia-tvorba.html#{slug}">{label}</a>\n'
        for slug, _h, label in CATEGORIES["dalsia-tvorba"]["groups"] if slug in used
    )
    if items:
        dalsia = f'''<div class="nav-dropdown">
        <a href="{up}dalsia-tvorba.html" class="has-caret{' active' if active == 'dalsia-tvorba' else ''}">ĎALŠIA TVORBA
          {CARET}
        </a>
        <div class="dropdown-menu">
{items}        </div>
      </div>'''
    else:
        dalsia = f'<a href="{up}dalsia-tvorba.html"{cls("dalsia-tvorba")}>ĎALŠIA TVORBA</a>'

    return f'''
<header class="site-header" id="domov">
  <div class="container header-inner">
    <a class="logo" href="{up}index.html" aria-label="{SITE_NAME}">
      <img src="{up}assets/images/logo.png" alt="Logo VM">
    </a>
    <button class="nav-toggle" aria-label="Otvoriť menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav class="main-nav">
      <a href="{up}index.html"{cls('domov')}>DOMOV</a>
      <a href="{up}knizny-dizajn.html"{cls('knizny-dizajn')}>KNIŽNÝ DIZAJN</a>
      {dalsia}
      <a href="{up}index.html#o-mne">O MNE</a>
      <a href="{up}index.html#kontakt">KONTAKT</a>
    </nav>
  </div>
</header>
'''


def footer(depth=0):
    up = "../" * depth
    return f'''
<footer class="site-footer" id="kontakt">
  <div class="container">
    <hr class="footer-rule">
    <div class="footer-inner">
      <a class="footer-logo" href="{up}index.html" aria-label="{SITE_NAME}">
        <img src="{up}assets/images/logo.png" alt="Logo VM">
      </a>
      <div class="footer-contact">
        <a href="tel:0917749871">
          <svg class="ci" viewBox="0 0 512 512" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M164.9 24.6c-7.7-18.6-28-28.5-47.4-23.2l-88 24C12.1 30.2 0 46 0 64C0 311.4 200.6 512 448 512c18 0 33.8-12.1 38.6-29.5l24-88c5.3-19.4-4.6-39.7-23.2-47.4l-96-40c-16.3-6.8-35.2-2.1-46.3 11.6L304.7 368C234.3 334.7 177.3 277.7 144 207.3L193.3 167c13.7-11.2 18.4-30 11.6-46.3l-40-96z"/></svg>
          0917749871
        </a>
        <a href="mailto:viki.mikuskova@gmail.com">
          <svg class="ci" viewBox="0 0 512 512" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48L48 64zM0 176L0 384c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64l0-208L294.4 339.2c-22.8 17.1-54 17.1-76.8 0L0 176z"/></svg>
          viki.mikuskova@gmail.com
        </a>
      </div>
      <div class="footer-social">
        <a href="https://www.instagram.com/vikca.design" target="_blank" rel="noopener" aria-label="Instagram" class="soc soc-ig">
          <svg viewBox="0 0 448 512" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z"/></svg>
        </a>
        <a href="https://www.linkedin.com/in/vikt%C3%B3ria-miku%C5%A1kov%C3%A1-245b77324" target="_blank" rel="noopener" aria-label="LinkedIn" class="soc soc-in">
          <svg viewBox="0 0 448 512" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M416 32H31.9C14.3 32 0 46.5 0 64.3v383.4C0 465.5 14.3 480 31.9 480H416c17.6 0 32-14.5 32-32.3V64.3c0-17.8-14.4-32.3-32-32.3zM135.4 416H69V202.2h66.5V416zm-33.2-243c-21.3 0-38.5-17.3-38.5-38.5S80.9 96 102.2 96c21.2 0 38.5 17.3 38.5 38.5 0 21.3-17.2 38.5-38.5 38.5zm282.1 243h-66.4V312c0-24.8-.5-56.7-34.5-56.7-34.6 0-39.9 27-39.9 54.9V416h-66.4V202.2h63.7v29.2h.9c8.9-16.8 30.6-34.5 62.9-34.5 67.2 0 79.7 44.3 79.7 101.9V416z"/></svg>
        </a>
        <a href="https://www.tiktok.com/@vikcadesigns" target="_blank" rel="noopener" aria-label="TikTok" class="soc soc-tt">
          <svg viewBox="0 0 448 512" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M448 209.9a210.06 210.06 0 0 1-122.77-39.25V349.38A162.55 162.55 0 1 1 185 188.31V278.2a74.62 74.62 0 1 0 52.23 71.18V0l88 0a121.18 121.18 0 0 0 1.86 22.17h0A122.18 122.18 0 0 0 381 102.39a121.43 121.43 0 0 0 67 20.14z"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>

<script src="{up}script.js" defer></script>
</body>
</html>
'''


def thumb(p, depth=0):
    """Náhľad projektu — rešpektuje orientáciu, knižné práce sú na výšku."""
    up = "../" * depth
    cls = ASPECT.get(p.get("orientation") or "portrait", "is-portrait")
    if p.get("cover"):
        inner = f'<img src="{up}{esc(p["cover"])}" alt="{esc(p["title"])}" loading="lazy">'
        return f'<div class="p-thumb {cls}">{inner}</div>'
    # zástupná plocha so správnym pomerom strán, kým nepríde obrázok
    return (f'<div class="p-thumb {cls} is-empty" role="img" aria-label="Obrázok pripravujem">'
            f'<span>pripravujem</span></div>')


def status_badge(p):
    s = STATUS.get(p.get("status"))
    if not s:
        return ""
    label, cls = s
    return f'<span class="p-status {cls}">{label}</span>'


def card(p, depth=0):
    up = "../" * depth
    meta = " · ".join([x for x in [p.get("client"), p.get("year")] if x])
    sub = esc(p.get("subtitle") or meta)
    return f'''      <a class="p-card" href="{up}projekt/{p['slug']}.html">
        {thumb(p, depth)}
        <div class="p-body">
          {status_badge(p)}
          <h3>{esc(p['title'])}</h3>
          {f'<p class="p-sub">{sub}</p>' if sub else ''}
          <span class="p-link">Pozrieť projekt →</span>
        </div>
      </a>
'''


# ---------------------------------------------------------------- homepage
def build_index(projects, about_html):
    featured = [p for p in projects if p.get("featured")][:3]
    cards = "".join(card(p) for p in featured)

    html = head(f"{SITE_NAME} — {TAGLINE}",
                "Mgr. Viktória Mikušková — grafická dizajnérka z Bratislavy so zameraním na knižný dizajn: obálky, sadzba a propagácia kníh.")
    html += header("domov", projects=projects)
    html += '''
<!-- ================= HERO ================= -->
<section class="hero">
  <div class="hero-copy">
    <h1 class="hero-title">
      <span class="hl1">Dizajn, ktorý</span>
      <span class="hl2">rozpráva váš <em>príbeh</em></span>
    </h1>
    <p class="hero-sub">Grafická dizajnérka so zameraním na knižný dizajn — obálky, sadzba a propagácia kníh.</p>
  </div>

  <picture class="hero-pic">
    <source media="(max-width: 860px)" srcset="assets/images/hero-illustration.jpg">
    <img class="hero-img" src="assets/images/hero.jpg" alt="Ilustrácia — Viktória kreslí na grafickom tablete pri stole s knihami a rastlinami">
  </picture>

  <a class="hero-btn" href="knizny-dizajn.html">POZRIEŤ PORTFÓLIO</a>
</section>

<!-- ================= VYBRANÉ PROJEKTY ================= -->
<section class="projects" id="portfolio">
  <div class="container">
    <div class="section-head">
      <h2 class="projects-title">VYBRANÉ PROJEKTY</h2>
      <a class="projects-link" href="knizny-dizajn.html">CELÉ PORTFÓLIO&nbsp;→</a>
    </div>

    <div class="p-grid p-grid-featured">
'''
    html += cards
    html += '''    </div>
  </div>
</section>

<!-- ================= OBLASTI ================= -->
<section class="services" id="sluzby">
  <div class="container">
    <p class="eyebrow eyebrow-olive">ČOMU SA VENUJEM</p>
    <ul class="services-row">
      <li class="service">
        <img class="service-icon" src="assets/images/icon-tlaciviny.png" alt="">
        <div class="service-text">
          <span class="service-title">KNIŽNÝ DIZAJN</span>
          <span class="service-sub">obálky, sadzba, propagácia</span>
        </div>
      </li>
      <li class="service">
        <img class="service-icon" src="assets/images/icon-branding.png" alt="">
        <div class="service-text">
          <span class="service-title">BRANDING</span>
          <span class="service-sub">logá, vizuálna identita</span>
        </div>
      </li>
      <li class="service">
        <img class="service-icon" src="assets/images/icon-ilustracie.png" alt="">
        <div class="service-text">
          <span class="service-title">ILUSTRÁCIE</span>
          <span class="service-sub">digitálne ilustrácie</span>
        </div>
      </li>
      <li class="service">
        <img class="service-icon" src="assets/images/icon-marketing.png" alt="">
        <div class="service-text">
          <span class="service-title">MARKETING</span>
          <span class="service-sub">sociálne siete, stratégia</span>
        </div>
      </li>
    </ul>
  </div>
</section>
'''
    html += about_html
    html += footer()
    return html


# ------------------------------------------------------------ category page
def build_category(key, projects):
    cat = CATEGORIES[key]
    mine = sorted([p for p in projects if p.get("category") == key],
                  key=lambda p: p.get("order") or 999)

    html = head(f"{cat['title']} — {SITE_NAME}", f"{cat['title']} — {cat['lead']}")
    html += header(key, projects=projects)
    html += f'''
<main>
  <section class="cat-hero">
    <div class="container">
      <p class="breadcrumb">
        <a href="index.html">Domov</a><span class="sep">/</span><span class="current">{esc(cat['title'])}</span>
      </p>
      <div class="cat-hero-inner">
        <div>
          <p class="cat-eyebrow">PORTFÓLIO</p>
          <h1 class="cat-title">{esc(cat['title'])}</h1>
          <p class="cat-desc">{esc(cat['lead'])}</p>
        </div>
      </div>
    </div>
  </section>
'''
    for slug, label, _short in cat["groups"]:
        group = [p for p in mine if p.get("subcategory") == slug]
        if not group:
            continue
        html += f'''
  <section class="cat-projects" id="{slug}">
    <div class="container">
      <div class="cat-projects-head">
        <p class="eyebrow eyebrow-olive">{esc(label)}</p>
        <span class="cat-count">{len(group)} {"projekt" if len(group)==1 else "projekty" if len(group)<5 else "projektov"}</span>
      </div>
      <div class="p-grid">
'''
        html += "".join(card(p) for p in group)
        html += '''      </div>
    </div>
  </section>
'''
    html += '''
  <section class="cat-cta">
    <div class="container">
      <div class="cat-cta-inner">
        <div>
          <h2>Máte podobný projekt v hlave?</h2>
          <p>Rada si vypočujem váš nápad a posuniem ho vizuálne ďalej.</p>
        </div>
        <a class="cta-btn" href="mailto:viki.mikuskova@gmail.com">Napíšte mi</a>
      </div>
    </div>
  </section>
</main>
'''
    html += footer()
    return html


# ------------------------------------------------------------- project page
def field(label, value):
    if not value:
        return f'<div class="m-item is-todo"><dt>{esc(label)}</dt><dd>doplniť</dd></div>'
    if isinstance(value, list):
        value = ", ".join(value)
    return f'<div class="m-item"><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>'


def prose(label, value):
    if not value:
        return (f'<div class="cs-block is-todo"><h2>{esc(label)}</h2>'
                f'<p class="todo">Popis projektu pripravujem.</p></div>')
    return f'<div class="cs-block"><h2>{esc(label)}</h2><p>{esc(value)}</p></div>'


def build_project(p, projects):
    cat = CATEGORIES[p["category"]]
    ordered = sorted(projects, key=lambda x: x.get("order") or 999)
    idx = [x["slug"] for x in ordered].index(p["slug"])
    prev_p = ordered[idx - 1] if idx > 0 else None
    next_p = ordered[idx + 1] if idx < len(ordered) - 1 else None

    desc = p.get("subtitle") or f"{p['title']} — {cat['title']}"
    html = head(f"{p['title']} — {SITE_NAME}", desc, depth=1)
    html += header(p["category"], depth=1, projects=projects)

    html += f'''
<main class="case-study">
  <section class="cs-top">
    <div class="container">
      <p class="breadcrumb">
        <a href="../index.html">Domov</a><span class="sep">/</span><a href="../{p['category']}.html">{esc(cat['title'])}</a><span class="sep">/</span><span class="current">{esc(p['title'])}</span>
      </p>

      <div class="cs-head">
        {status_badge(p)}
        <h1 class="cs-title">{esc(p['title'])}</h1>
        {f'<p class="cs-sub">{esc(p["subtitle"])}</p>' if p.get("subtitle") else ''}
      </div>
    </div>
  </section>

  <section class="cs-hero">
    <div class="container">
      {thumb(p, depth=1)}
    </div>
  </section>

  <section class="cs-meta">
    <div class="container">
      <dl class="cs-meta-grid">
        {field("Rok", p.get("year"))}
        {field("Zadávateľ", p.get("client"))}
        {field("Moja rola", p.get("role"))}
        {field("Formát", p.get("format"))}
        {field("Softvér", p.get("software"))}
      </dl>
    </div>
  </section>

  <section class="cs-prose">
    <div class="container">
      {prose("Zadanie", p.get("brief"))}
      {prose("Riešenie", p.get("solution"))}
      {prose("Prečo takto", p.get("why"))}
    </div>
  </section>
'''

    imgs = p.get("images") or []
    if imgs:
        html += '''
  <section class="cs-gallery">
    <div class="container">
      <div class="g-grid">
'''
        for im in imgs:
            cls = ASPECT.get(im.get("orientation") or p.get("orientation") or "portrait", "is-portrait")
            if im.get("src"):
                inner = f'<img src="../{esc(im["src"])}" alt="{esc(im.get("caption") or p["title"])}" loading="lazy">'
                body = f'<div class="p-thumb {cls}">{inner}</div>'
            else:
                body = (f'<div class="p-thumb {cls} is-empty" role="img" aria-label="Obrázok pripravujem">'
                        f'<span>pripravujem</span></div>')
            cap = f'<figcaption>{esc(im.get("caption"))}</figcaption>' if im.get("caption") else ""
            html += f'        <figure class="g-item">{body}{cap}</figure>\n'
        html += '''      </div>
    </div>
  </section>
'''

    html += '  <section class="cs-nav"><div class="container"><div class="cs-nav-inner">\n'
    if prev_p:
        html += f'    <a class="cs-prev" href="{prev_p["slug"]}.html"><span>← Predchádzajúci</span><strong>{esc(prev_p["title"])}</strong></a>\n'
    else:
        html += '    <span></span>\n'
    if next_p:
        html += f'    <a class="cs-next" href="{next_p["slug"]}.html"><span>Ďalší →</span><strong>{esc(next_p["title"])}</strong></a>\n'
    else:
        html += '    <span></span>\n'
    html += '''  </div></div></section>

  <section class="cat-cta">
    <div class="container">
      <div class="cat-cta-inner">
        <div>
          <h2>Máte podobný projekt v hlave?</h2>
          <p>Rada si vypočujem váš nápad a posuniem ho vizuálne ďalej.</p>
        </div>
        <a class="cta-btn" href="mailto:viki.mikuskova@gmail.com">Napíšte mi</a>
      </div>
    </div>
  </section>
</main>
'''
    html += footer(depth=1)
    return html


# --------------------------------------------------------------------- main
def extract_about():
    """Sekcia 'O mne' sa preberá z existujúceho index.html, aby sa text nestratil."""
    src = os.path.join(ROOT, "index.html")
    if not os.path.exists(src):
        return ""
    txt = open(src, encoding="utf-8").read()
    m = re.search(r'<!-- ================= O MNE .*?</section>', txt, re.S)
    return "\n" + m.group(0) + "\n" if m else ""


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    projects = data["projects"]
    about = extract_about()

    os.makedirs(PROJ_DIR, exist_ok=True)

    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(build_index(projects, about))
    print("index.html")

    for key in CATEGORIES:
        open(os.path.join(ROOT, f"{key}.html"), "w", encoding="utf-8").write(build_category(key, projects))
        print(f"{key}.html")

    for p in projects:
        open(os.path.join(PROJ_DIR, f"{p['slug']}.html"), "w", encoding="utf-8").write(build_project(p, projects))
        print(f"projekt/{p['slug']}.html")

    # staré kategórie sa nahrádzajú novou štruktúrou
    for old in ("branding", "ilustracie", "uiux", "tlaciviny", "marketing"):
        f = os.path.join(ROOT, f"{old}.html")
        if os.path.exists(f):
            os.remove(f)
            print(f"odstránené: {old}.html")

    n_img = sum(1 for p in projects if p.get("cover")) + sum(
        1 for p in projects for i in (p.get("images") or []) if i.get("src"))
    print(f"\nhotovo — {len(projects)} projektov, {n_img} obrázkov doplnených")


if __name__ == "__main__":
    main()
