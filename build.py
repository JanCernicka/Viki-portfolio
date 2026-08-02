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

# Kategórie sú disciplíny, nie dve vetvy. Agentúra hľadá "branding" alebo
# "packaging", nie "ďalšiu tvorbu"; knižný dizajn ostáva ako jedna z nich,
# aby ho vydavateľstvo našlo bez toho, aby rámcoval celé portfólio.
CATEGORIES = {
    "vizualna-identita": {
        "title": "Vizuálna identita",
        "short": "Vizuálna identita",
        "icon": "icon-branding.png",
        "lead": "Logotypy, značky a ich aplikácie, od vizitky po vývesku prevádzky.",
        "hero": "assets/projects/nook-books/01-identita.jpg",
    },
    "obaly": {
        "title": "Obaly a packaging",
        "short": "Obaly",
        "icon": "icon-tlaciviny.png",
        "lead": "Obalový dizajn od ilustrácie cez sadzbu až po prípravu do tlače.",
        "hero": "assets/projects/macarons/03-obal-vrch.jpg",
    },
    "ilustracia": {
        "title": "Ilustrácia",
        "short": "Ilustrácia",
        "icon": "icon-ilustracie.png",
        "lead": "Kresba postáv, digitálna maľba a ilustrácia k textu.",
        "hero": "assets/projects/charaktery/01-charaktery.jpg",
    },
    "knizny-dizajn": {
        "title": "Knižný dizajn",
        "short": "Knižný dizajn",
        "icon": "icon-tlaciviny.png",
        "lead": "Obálky, sadzba a typografia. Zameranie, v ktorom mám polygrafické vzdelanie.",
        "hero": "assets/projects/alica/04-fantasy.jpg",
    },
    "tlacoviny": {
        "title": "Tlačoviny a orientačné systémy",
        "short": "Tlačoviny",
        "icon": "icon-uiux.png",
        "lead": "Plagáty, letáky, mapy a veľkoformátová tlač.",
        "hero": "assets/projects/mapa-skoly/01-ekonomia.jpg",
    },
    "socialne-siete": {
        "title": "Sociálne siete",
        "short": "Sociálne siete",
        "icon": "icon-marketing.png",
        "lead": "Vizuály, obsah a produktová fotografia pre značky.",
        "hero": "assets/projects/spolok-farmacie/04-socialne-siete.jpg",
    },
}


def in_category(p, key):
    """Projekt patrí do kategórie priamo alebo cez pole cross."""
    return p.get("category") == key or key in (p.get("cross") or [])


def of_category(projects, key):
    return sorted([p for p in projects if in_category(p, key)],
                  key=lambda p: p.get("order") or 999)


STATUS = {
    "skolsky":    ("Školský projekt", "st-school"),
    "komercny":   ("Komerčná práca", "st-commercial"),
    "publikovany": ("Publikované", "st-published"),
    "realizovany": ("Realizované", "st-published"),
    "sutaz":      ("2. miesto v súťaži", "st-award"),
    "koncept":    ("Koncepčný projekt", "st-concept"),
}

ASPECT = {"portrait": "is-portrait", "landscape": "is-landscape", "square": "is-square"}

CARET = ('<svg viewBox="0 0 448 512" width="12" height="12" aria-hidden="true"><path fill="currentColor" '
         'd="M201.4 374.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 '
         '306.7 86.6 169.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg>')


def esc(s):
    if s is None:
        return ""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


# Adresa webu naživo. Open Graph vyžaduje absolútne adresy — relatívna cesta
# k obrázku sa v náhľade nezobrazí a LinkedIn odkaz bez náhľadu odmietne.
SITE_URL = "https://viktoria-mikuskova.pages.dev"


def head(title, description, depth=0, path=""):
    up = "../" * depth
    url = SITE_URL + ("/" + path if path else "/")
    return f'''<!DOCTYPE html>
<html lang="sk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(url)}">

<!-- náhľadová karta pre LinkedIn, Facebook, WhatsApp a spol. -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:locale" content="sk_SK">
<meta property="og:url" content="{esc(url)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{SITE_URL}/assets/images/share-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Viktória Mikušková, grafická dizajnérka a ilustrátorka">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{SITE_URL}/assets/images/share-card.jpg">

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

    # V menu je len disciplína, ktorá má aspoň jeden projekt. Nová sa objaví
    # sama, len čo k nej priradíš prácu.
    projects = projects or []
    # Prvá položka je rozcestník so všetkými sekciami. Kto nevie, čo hľadá,
    # nemusí sa rozhodovať už v menu.
    all_act = ' class="active"' if active == "portfolio" else ""
    items = f'          <a href="{up}portfolio.html"{all_act}>Všetky sekcie</a>\n'
    for key, cat in CATEGORIES.items():
        if not of_category(projects, key):
            continue
        act = ' class="active"' if key == active else ""
        items += f'          <a href="{up}{key}.html"{act}>{cat["short"]}</a>\n'

    portfolio_active = active in CATEGORIES or active == "portfolio"
    dropdown = f'''<div class="nav-dropdown">
        <a href="{up}portfolio.html" class="has-caret{' active' if portfolio_active else ''}">PORTFÓLIO
          {CARET}
        </a>
        <div class="dropdown-menu">
{items}        </div>
      </div>'''

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
      {dropdown}
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


def hero_row(p, depth=1):
    """Všetky zábery projektu vedľa seba hore.

    Pri projektoch s dvoma alebo troma obrázkami nemá zmysel schovávať
    zvyšok pod text: človek ich chce vidieť naraz a hneď rozkliknúť.
    """
    up = "../" * depth
    shots = []
    if p.get("cover"):
        shots.append({"src": p["cover"], "caption": p.get("hero_caption"),
                      "orientation": p.get("orientation")})
    shots += [i for i in (p.get("images") or []) if i.get("src")]
    if not shots:
        return None

    portrait_n = sum(1 for s in shots
                     if (s.get("orientation") or p.get("orientation")) == "portrait")
    frame = "frame-portrait" if portrait_n * 2 >= len(shots) else "frame-landscape"
    cells = ""
    for s in shots:
        alt = esc(s.get("caption") or p["title"])
        cells += (f'<figure class="g-item"><a class="g-frame zoom" href="{up}{esc(s["src"])}" '
                  f'data-cap="{alt}"><img src="{up}{esc(s["src"])}" alt="{alt}"></a>'
                  + (f'<figcaption>{esc(s["caption"])}</figcaption>' if s.get("caption") else "")
                  + "</figure>")
    return (f'<p class="g-hint">Kliknutím sa obrázok zväčší.</p>'
            f'<div class="g-grid is-{min(len(shots), 3)} {frame}">{cells}</div>')


def hero_visual(p, depth=1):
    """Úvodný vizuál projektu.

    Nie je to orezaná dlaždica ako v mriežke, ale celý obrázok s obmedzenou
    výškou. Banner cez celú obrazovku odsúval text pod okraj okna a zároveň
    odrezával okraje mockupov.
    """
    if p.get("hero_layout") == "row":
        row = hero_row(p, depth)
        if row:
            return row
    up = "../" * depth
    src = p.get("cover")
    if not src:
        cls = ASPECT.get(p.get("orientation") or "portrait", "is-portrait")
        return (f'<div class="p-thumb {cls} is-empty" role="img" aria-label="Obrázok pripravujem">'
                f'<span>pripravujem</span></div>')
    cap = esc(p.get("hero_caption") or p.get("subtitle") or p["title"])
    img = (f'<a class="cs-hero-img zoom" href="{up}{esc(src)}" data-cap="{cap}">'
           f'<img src="{up}{esc(src)}" alt="{esc(p["title"])}"></a>')

    # Príspevok a reel vedľa seba: obe médiá majú rovnakú výšku, takže sa dá
    # porovnať statický formát s videom bez toho, aby jedno prebilo druhé.
    if (p.get("video") or {}).get("beside_cover"):
        hero_cap = (f'<figcaption>{esc(p["hero_caption"])}</figcaption>'
                    if p.get("hero_caption") else "")
        return f'''<div class="cs-duo">
        <figure class="d-item">{img}{hero_cap}</figure>
        {video_figure(p, depth)}
      </div>'''
    return img


def video_figure(p, depth=1):
    """Prehrávač prehliadača, nič sa nenačítava vopred.

    Bez JavaScriptu ostane vnútri odkaz na súbor, takže sa video dá aspoň
    stiahnuť.
    """
    v = p.get("video")
    if not v or not v.get("src"):
        return ""
    up = "../" * depth
    poster = f' poster="{up}{esc(v["poster"])}"' if v.get("poster") else ""
    cap = f'<figcaption>{esc(v["caption"])}</figcaption>' if v.get("caption") else ""
    return f'''<figure class="v-item">
          <video class="v-player" controls preload="none" playsinline{poster}>
            <source src="{up}{esc(v["src"])}" type="video/mp4">
            <a href="{up}{esc(v["src"])}">Stiahnuť video</a>
          </video>
          {cap}
        </figure>'''


def video_block(p, depth=1):
    """Video samostatne, keď nestojí vedľa úvodného obrázka."""
    fig = video_figure(p, depth)
    if not fig or p.get("video", {}).get("beside_cover"):
        return ""
    return f'''
  <section class="cs-video">
    <div class="container">
      {fig}
    </div>
  </section>
'''


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
    # Domovská ukazuje najlepšiu prácu naprieč disciplínami, nie taxonómiu.
    # Personalista z agentúry chce vidieť práce, nie štruktúru menu.
    featured = sorted([p for p in projects if p.get("featured")],
                      key=lambda p: p.get("order") or 999)[:6]
    cards = "".join(card(p) for p in featured)

    disciplines = ""
    for key, cat in CATEGORIES.items():
        if not of_category(projects, key):
            continue
        disciplines += f'''      <li class="service">
        <a href="{key}.html">
          <img class="service-icon" src="assets/images/{cat["icon"]}" alt="">
          <span class="service-text">
            <span class="service-title">{esc(cat["short"]).upper()}</span>
            <span class="service-sub">{esc(cat["lead"])}</span>
          </span>
        </a>
      </li>
'''

    html = head(f"{SITE_NAME} - {TAGLINE}",
                "Mgr. Viktória Mikušková, grafická dizajnérka a ilustrátorka z Bratislavy. "
                "Vizuálna identita, obaly, ilustrácia, knižný dizajn a tlačoviny.")
    html += header("domov", projects=projects)
    html += '''
<!-- ================= HERO ================= -->
<section class="hero">
  <div class="hero-copy">
    <h1 class="hero-title">
      <span class="hl1">Dizajn, ktorý</span>
      <span class="hl2">rozpráva váš <em>príbeh</em></span>
    </h1>
    <p class="hero-sub">Grafická dizajnérka a ilustrátorka. Vizuálna identita, obaly, ilustrácia a tlačoviny. Za tým všetkým polygrafická priemyslovka, takže viem, čo sa s návrhom stane v tlačiarni.</p>
  </div>

  <picture class="hero-pic">
    <source media="(max-width: 860px)" srcset="assets/images/hero-illustration.jpg">
    <img class="hero-img" src="assets/images/hero.jpg" alt="Ilustrácia — Viktória kreslí na grafickom tablete pri stole s knihami a rastlinami">
  </picture>

  <a class="hero-btn" href="portfolio.html">POZRIEŤ PORTFÓLIO</a>
</section>

<!-- ================= VYBRANÉ PROJEKTY ================= -->
<section class="projects" id="portfolio">
  <div class="container">
    <div class="section-head">
      <h2 class="projects-title">VYBRANÉ PROJEKTY</h2>
    </div>

    <div class="p-grid p-grid-featured">
'''
    html += cards
    html += '''    </div>
  </div>
</section>

<!-- ================= DISCIPLÍNY ================= -->
<section class="services projects-alt" id="sluzby">
  <div class="container">
    <div class="section-head">
      <h2 class="projects-title">ČOMU SA VENUJEM</h2>
    </div>
    <ul class="services-row services-grid">
'''
    html += disciplines
    html += '''    </ul>
  </div>
</section>
'''
    html += about_html
    html += footer()
    return html


# --------------------------------------------------------- portfolio rozcestník
def build_portfolio(projects):
    """Rozcestník: každá sekcia ako obrázok, ktorý na ňu vedie.

    Tlačidlo v úvodnom banneri viedlo priamo na vizuálnu identitu, takže
    zvyšok práce ostal skrytý v menu. Tu vidno naraz všetko, čo robím.
    """
    tiles = ""
    for key, cat in CATEGORIES.items():
        mine = of_category(projects, key)
        if not mine:
            continue
        n = len(mine)
        pocet = "projekt" if n == 1 else "projekty" if n < 5 else "projektov"
        hero = cat.get("hero")
        if hero:
            visual = f'<img src="{esc(hero)}" alt="{esc(cat["title"])}" loading="lazy">'
        else:
            visual = '<span class="sec-empty">pripravujem</span>'
        tiles += f'''      <a class="sec-card" href="{key}.html">
        <span class="sec-pic">{visual}</span>
        <span class="sec-body">
          <span class="sec-count">{n} {pocet}</span>
          <span class="sec-title">{esc(cat["title"])}</span>
          <span class="sec-lead">{esc(cat["lead"])}</span>
          <span class="sec-link">Pozrieť sekciu →</span>
        </span>
      </a>
'''

    html = head(f"Portfólio - {SITE_NAME}",
                "Portfólio Viktórie Mikuškovej podľa sekcií: vizuálna identita, obaly, "
                "ilustrácia, knižný dizajn, tlačoviny a sociálne siete.",
                path="portfolio.html")
    html += header("portfolio", projects=projects)
    html += '''
<main>
  <section class="cat-hero">
    <div class="container">
      <p class="breadcrumb">
        <a href="index.html">Domov</a><span class="sep">/</span><span class="current">Portfólio</span>
      </p>
      <div class="cat-hero-inner">
        <div>
          <p class="cat-eyebrow">PORTFÓLIO</p>
          <h1 class="cat-title">Kreatívna cesta</h1>
          <p class="cat-desc">Objavte moje projekty podľa jednotlivých sekcií.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="sections">
    <div class="container">
      <div class="sec-grid">
'''
    html += tiles
    html += '''      </div>
    </div>
  </section>

  <section class="cat-cta">
    <div class="container">
      <div class="cat-cta-inner">
        <div>
          <h2>Chcete portfólio v PDF?</h2>
          <p>Výber prác na jednom mieste, spolu so životopisom.</p>
        </div>
        <a class="cta-btn" href="dokumenty.html">Stiahnuť portfólio</a>
      </div>
    </div>
  </section>
</main>
'''
    html += footer()
    return html


# ------------------------------------------------------- stránka na stiahnutie
# Súbory drží build_docs.py, tu je len stránka. Keď sa v build_docs.py zmení
# názov PDF portfólia, treba ho prepísať aj tu.
DOWNLOADS = [
    {
        "title": "Životopis na stiahnutie",
        "lead": "Jedna strana A4.",
        "pdf": "assets/cv/Viktoria-Mikuskova-CV.pdf",
        "view": "cv.html",
    },
    {
        "title": "Portfólio na stiahnutie",
        "lead": ("Výber prác naprieč vizuálnou identitou, obalmi, ilustráciou, "
                 "knižným dizajnom, tlačovinami aj sociálnymi sieťami."),
        "pdf": "assets/dokumenty/Viktoria-Mikuskova-portfolio.pdf",
        "view": "portfolio-dokument.html",
    },
]


def build_dokumenty(projects):
    cards = ""
    for d in DOWNLOADS:
        cards += f'''        <article class="dl-card">
          <h2>{esc(d["title"])}</h2>
          <p>{esc(d["lead"])}</p>
          <p class="dl-actions">
            <a class="dl-btn" href="{d["pdf"]}" download>Stiahnuť PDF</a>
            <a class="dl-view" href="{d["view"]}">Pozrieť v prehliadači</a>
          </p>
        </article>
'''

    html = head(f"Dokumenty na stiahnutie - {SITE_NAME}",
                "Životopis a portfólio Viktórie Mikuškovej na stiahnutie v PDF.",
                path="dokumenty.html")
    html += header("dokumenty", projects=projects)
    html += '''
<main>
  <section class="cat-hero">
    <div class="container">
      <p class="breadcrumb">
        <a href="index.html">Domov</a><span class="sep">/</span><span class="current">Dokumenty</span>
      </p>
      <div class="cat-hero-inner">
        <div>
          <p class="cat-eyebrow">NA STIAHNUTIE</p>
          <h1 class="cat-title">Dokumenty na stiahnutie</h1>
          <p class="cat-desc">Ak Vás moje portfólio zaujalo, viete si ho tu stiahnuť.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="downloads">
    <div class="container">
      <div class="dl-grid">
'''
    html += cards
    html += '''      </div>
    </div>
  </section>

  <section class="cat-cta">
    <div class="container">
      <div class="cat-cta-inner">
        <div>
          <h2>Máte otázku?</h2>
          <p>Napíšte mi, čo potrebujete. Rada pošlem aj rozpracované veci.</p>
        </div>
        <a class="cta-btn" href="index.html#kontakt">Napíšte mi</a>
      </div>
    </div>
  </section>
</main>
'''
    html += footer()
    return html


# ------------------------------------------------------------ category page
def build_category(key, projects):
    cat = CATEGORIES[key]
    mine = of_category(projects, key)
    n = len(mine)
    pocet = "projekt" if n == 1 else "projekty" if n < 5 else "projektov"

    html = head(f"{cat['title']} - {SITE_NAME}", f"{cat['title']}. {cat['lead']}",
                path=f"{key}.html")
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
        <span class="cat-count">{n} {pocet}</span>
      </div>
    </div>
  </section>

  <section class="cat-projects">
    <div class="container">
      <div class="p-grid">
'''
    html += "".join(card(p) for p in mine)
    html += '''      </div>
    </div>
  </section>

  <section class="cat-cta">
    <div class="container">
      <div class="cat-cta-inner">
        <div>
          <h2>Zaujali vás moje práce?</h2>
          <p>Ozvite sa mi. Rada si vypočujem, čo potrebujete.</p>
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

    desc = p.get("subtitle") or f"{p['title']}, {cat['title']}"
    html = head(f"{p['title']} - {SITE_NAME}", desc, depth=1,
                path=f"projekt/{p['slug']}.html")
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
      {hero_visual(p)}
    </div>
  </section>
{video_block(p)}
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

    # Pri rade hore sú obrázky už použité, pod textom by sa zopakovali.
    imgs = [] if p.get("hero_layout") == "row" else (p.get("images") or [])
    if imgs:
        # Pri jednom alebo dvoch obrázkoch by mriežka roztiahla dlaždicu cez
        # celú šírku. Počet stĺpcov preto obmedzujeme podľa počtu obrázkov.
        grid_cls = "g-grid" + (f" is-{len(imgs)}" if len(imgs) <= 2 else "")
        # Rám je pre všetky obrázky projektu rovnaký, inak sa popisky rozídu
        # do rôznych výšok. Jeho pomer sa riadi prevahou v projekte, aby
        # obrázky na výšku nesedeli ako známka uprostred širokého rámu.
        portrait_n = sum(1 for im in imgs
                         if (im.get("orientation") or p.get("orientation")) == "portrait")
        grid_cls += " frame-portrait" if portrait_n * 2 >= len(imgs) else " frame-landscape"
        # Pri väčšom počte záberov nižší rad, aby sa ich vošlo viac vedľa seba
        # a galéria nebola stĺpec obrovských obrázkov.
        if len(imgs) >= 6:
            grid_cls += " is-many"
        html += f'''
  <section class="cs-gallery">
    <div class="container">
      <p class="g-hint">Kliknutím sa obrázok zväčší.</p>
      <div class="{grid_cls}">
'''
        for im in imgs:
            if im.get("src"):
                alt = esc(im.get("caption") or p["title"])
                inner = f'<img src="../{esc(im["src"])}" alt="{alt}" loading="lazy">'
                # Obrázky sa nesmú orezávať, ale musia mať rovnakú veľkosť,
                # inak sa popisky rozídu do rôznych výšok. Preto jednotný rám
                # a obrázok v ňom celý, nie orezaný na výplň.
                body = (f'<a class="g-frame zoom" href="../{esc(im["src"])}" '
                        f'data-cap="{alt}">{inner}</a>')
            else:
                body = ('<div class="g-frame is-empty" role="img" aria-label="Obrázok pripravujem">'
                        '<span>pripravujem</span></div>')
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

    open(os.path.join(ROOT, "portfolio.html"), "w", encoding="utf-8").write(build_portfolio(projects))
    print("portfolio.html")

    open(os.path.join(ROOT, "dokumenty.html"), "w", encoding="utf-8").write(build_dokumenty(projects))
    print("dokumenty.html")

    for key in CATEGORIES:
        open(os.path.join(ROOT, f"{key}.html"), "w", encoding="utf-8").write(build_category(key, projects))
        print(f"{key}.html")

    for p in projects:
        open(os.path.join(PROJ_DIR, f"{p['slug']}.html"), "w", encoding="utf-8").write(build_project(p, projects))
        print(f"projekt/{p['slug']}.html")

    # staré kategórie sa nahrádzajú novou štruktúrou
    for old in ("branding", "ilustracie", "uiux", "tlaciviny", "marketing",
                "dalsia-tvorba"):
        f = os.path.join(ROOT, f"{old}.html")
        if os.path.exists(f):
            os.remove(f)
            print(f"odstránené: {old}.html")

    # stránky projektov, ktoré už v dátach nie sú (premenované slugy)
    live = {p["slug"] + ".html" for p in projects}
    for f in sorted(os.listdir(PROJ_DIR)):
        if f.endswith(".html") and f not in live:
            os.remove(os.path.join(PROJ_DIR, f))
            print(f"odstránené: projekt/{f}")

    n_img = sum(1 for p in projects if p.get("cover")) + sum(
        1 for p in projects for i in (p.get("images") or []) if i.get("src"))
    print(f"\nhotovo — {len(projects)} projektov, {n_img} obrázkov doplnených")


if __name__ == "__main__":
    main()
