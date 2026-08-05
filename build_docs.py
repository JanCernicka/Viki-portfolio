#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor tlačených a posielateľných dokumentov.

    python3 build_docs.py

Vytvorí:
    portfolio-dokument.html posielateľné portfólio (jedno, všetky disciplíny)
    assets/dokumenty/qr-web.png

Stránku na stiahnutie (dokumenty.html) generuje build.py — je to bežná
stránka webu s menu a pätičkou, nie dokument.

Potom sa z nich urobia PDF-ká:
    node make_pdf.js
"""

import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Jedno miesto, kde je adresa webu. Prepíš SITE_URL, spusti build_docs.py
# a node make_pdf.js a adresa sa zmení v oboch životopisoch, v portfóliu
# aj v QR kóde.
# ---------------------------------------------------------------------------
SITE_URL = "viktoriamikuskova.com"
SITE_HREF = "https://" + SITE_URL

NAME = "Viktória Mikušková"
PHONE = "0917 749 871"
EMAIL = "viki.mikuskova@gmail.com"
CITY = "Bratislava"

STATUS = {
    "skolsky": "Školský projekt",
    "komercny": "Komerčná práca",
    "publikovany": "Publikované",
    "realizovany": "Realizované",
    "sutaz": "2. miesto v súťaži",
    "koncept": "Koncepčný projekt",
}

ASPECT = {"portrait": "2 / 3", "landscape": "4 / 3", "square": "1 / 1"}


def esc(s):
    if s is None:
        return ""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def load_projects():
    with open(os.path.join(ROOT, "content", "projects.json"), encoding="utf-8") as f:
        data = json.load(f)
    return sorted(data["projects"], key=lambda p: p.get("order", 999))


def doc_head(title, css, noindex=True):
    robots = '\n<meta name="robots" content="noindex">' if noindex else ""
    return f'''<!DOCTYPE html>
<html lang="sk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>{robots}
<link rel="icon" type="image/png" href="assets/images/logo.png">
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="{css}">
</head>
<body>
'''


# ===========================================================================
# QR kód na web
# ===========================================================================
def build_qr():
    try:
        import segno
    except ImportError:
        print("  ! segno nie je nainštalované — QR preskočený (pip install segno)")
        return False
    out = os.path.join(ROOT, "assets", "dokumenty", "qr-web.png")
    segno.make(SITE_HREF, error="m").save(
        out, scale=14, border=2, dark="#011126", light="#FBEFE3")
    print(f"  qr-web.png ({os.path.getsize(out)} B) -> {SITE_HREF}")
    return True


# ===========================================================================
# Posielateľné portfólio (PDF)
# ===========================================================================
def portfolio_page(p, n, total):
    orient = p.get("orientation") or "landscape"
    ratio = ASPECT.get(orient, "4 / 3")
    cover = p.get("cover")
    # Panel s textom strieda ľavú a pravú stranu a k tomu strieda odtieň.
    # Sedemnásť strán s rovnakým rozložením sa číta ako katalóg.
    side, tint = ("is-left", "tint-peach") if n % 2 else ("is-right", "tint-sage")
    imgs = [i for i in (p.get("images") or []) if i.get("src")]

    # Projekty, ktoré majú na webe zábery vedľa seba, ich majú vedľa seba aj tu.
    # Dvojica portrétov alebo dvojica plagátov je pointa práce; jeden veľký
    # a jeden ako známka pod ním to rozbíja. Zábery na šírku sa takto ale
    # zmestia do tretiny strany a zdrobnejú, tie ostávajú pri jednom hlavnom.
    row = p.get("hero_layout") == "row" and orient != "landscape"
    shots = ([{"src": cover}] if cover else []) + imgs
    if row and len(shots) > 1:
        cells = "".join(f'<img src="{esc(i["src"])}" alt="">' for i in shots[:3])
        visual = f'<div class="pf-row">{cells}</div>'
        imgs = []
    elif cover:
        visual = f'<img class="pf-img" src="{esc(cover)}" alt="">'
    elif imgs:
        visual = f'<img class="pf-img" src="{esc(imgs[0]["src"])}" alt="">'
    else:
        visual = ('<div class="pf-empty"><span>obrázok projektu</span>'
                  '<span class="pf-empty-note">doplniť pred odoslaním</span></div>')

    # Do PDF sa video nedostane, ale jeho úvodná snímka áno — inak by
    # najúspešnejšia práca v portfóliu chýbala.
    v = p.get("video") or {}
    if v.get("poster"):
        imgs = imgs + [{"src": v["poster"]}]

    # Ďalšie zábery na tej istej strane — max tri, aby strana ostala čistá.
    # Keď je hlavný obrázok cover, pás začína prvým obrázkom z galérie; bez
    # coveru ho zabral prvý obrázok, takže pás začína až druhým. Predtým sa
    # v oboch prípadoch preskakoval prvý, čiže pri projekte s coverom a jedným
    # obrázkom (Portréty psov) nezostalo do pásu nič.
    strip = ""
    extra = imgs[0:3] if cover else imgs[1:4]
    if extra:
        cells = "".join(f'<img src="{esc(i["src"])}" alt="">' for i in extra)
        strip = f'<div class="pf-strip">{cells}</div>'

    meta = []
    if p.get("client"):
        meta.append(esc(p["client"]))
    if p.get("year"):
        meta.append(esc(p["year"]))
    if p.get("status") in STATUS:
        meta.append(STATUS[p["status"]])
    # Pri školských prácach je zadávateľ aj štítok "Školský projekt", takže by
    # sa v riadku zopakoval dvakrát. Na webe sú od seba, tu vedľa seba.
    seen, uniq = set(), []
    for m in meta:
        if m.casefold() not in seen:
            seen.add(m.casefold())
            uniq.append(m)
    meta_line = " &nbsp;·&nbsp; ".join(uniq)

    body = p.get("solution") or p.get("brief") or p.get("subtitle") or ""
    # Najdlhší popis má vyše deväťsto znakov a v bočnom stĺpci by pretiekol
    # cez spodok strany. Namiesto skracovania jej textu sa zmenší písmo.
    long_cls = " is-long" if len(body) > 620 else ""

    facts = []
    if p.get("role"):
        facts.append(("Rola", p["role"]))
    if p.get("format"):
        facts.append(("Formát", p["format"]))
    if p.get("software"):
        facts.append(("Softvér", ", ".join(p["software"])))
    facts_html = ""
    if facts:
        facts_html = '<dl class="pf-facts">' + "".join(
            f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in facts) + "</dl>"

    return f'''
  <section class="page pf-project {side} {tint}{long_cls}" style="--ratio:{ratio}">
    <div class="pf-visual">{visual}{strip}</div>
    <div class="pf-panel">
      <div class="pf-panel-head">
        <span class="pf-num">{n:02d}</span>
        <h2>{esc(p.get("title"))}</h2>
        <p class="pf-meta">{meta_line}</p>
      </div>
      <div class="pf-panel-body">
        <p class="pf-body">{esc(body)}</p>
        {facts_html}
      </div>
    </div>
  </section>
'''


# ---------------------------------------------------------------------------
# Obsah a strana o mne. Devätnásťstranový dokument bez obsahu sa listuje
# naslepo a personalista sa k práci, ktorá ho zaujíma, nedostane.
# ---------------------------------------------------------------------------
CAT_LABEL = {
    "vizualna-identita": "Vizuálna identita",
    "obaly": "Obaly a packaging",
    "ilustracia": "Ilustrácia",
    "knizny-dizajn": "Knižný dizajn",
    "tlacoviny": "Tlačoviny a orientačné systémy",
    "socialne-siete": "Sociálne siete",
}


def contents_page(items):
    rows = "".join(
        f'<li><span class="pf-toc-n">{i + 1:02d}</span>'
        f'<span class="pf-toc-t">{esc(p.get("title"))}</span>'
        f'<span class="pf-toc-c">{esc(CAT_LABEL.get(p.get("category"), ""))}</span></li>'
        for i, p in enumerate(items))
    return f'''
  <section class="page pf-toc">
    <div class="pf-toc-list"><ol>{rows}</ol></div>
    <h2 class="pf-toc-title">Obsah</h2>
    <span class="pf-shape pf-shape-c"></span>
    <span class="pf-shape pf-shape-d"></span>
  </section>
'''


ABOUT_TEXT = (
    "Vyštudovala som SOŠ polygrafickú, odbor grafik digitálnych médií, potom Dizajn médií "
    "a magisterské štúdium masmediálnej komunikácie na Paneurópskej vysokej škole. "
    "Remeslo z polygrafie a z prípravy podkladov do tlače spájam s marketingovým myslením "
    "zo štúdia mediálnej komunikácie.")
ABOUT_QUOTE = "Typografia, ktorá text nesie a neprekrýva."

ABOUT_FACTS = [
    ("Robím", "Vizuálnu identitu, obaly, tlačoviny, ilustráciu a obsah pre značky"),
    ("Softvér", "InDesign, Illustrator, Photoshop, Acrobat, Figma, Procreate"),
    ("Prax", "SHAPELESAI, MOJESIDLO.SK, PwC Slovensko"),
]


def about_page():
    facts = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in ABOUT_FACTS)
    return f'''
  <section class="page pf-about">
    <div class="pf-about-top">
      <div class="pf-about-text">
        <h2>O mne</h2>
        <p class="pf-about-lead">{esc(ABOUT_TEXT)}</p>
        <p class="pf-about-quote">{esc(ABOUT_QUOTE)}</p>
      </div>
    </div>
    <div class="pf-about-bottom">
      <div class="pf-about-photo">
        <span class="pf-photo-disc"></span>
        <img src="assets/cv/portrait.jpg" alt="{esc(NAME)}">
      </div>
      <dl class="pf-about-facts">{facts}</dl>
      <div class="pf-about-foot">
        <span>{esc(PHONE)}</span><span>{esc(EMAIL)}</span><span>{esc(SITE_URL)}</span>
      </div>
    </div>
  </section>
'''


# Jedno posielateľné portfólio zo všetkých disciplín. Predtým boli dve verzie,
# jedna pre vydavateľstvá a jedna pre agentúry, a pred každým odoslaním sa
# muselo rozhodovať, ktorá pôjde von. Teraz je jeden odkaz, ktorý sa dá poslať
# komukoľvek, a poradie strán robí to, čo predtým robil výber verzie: najprv
# najsilnejšie práce, potom zvyšok.
COVER_ROLE = "Grafická dizajnérka a ilustrátorka"
CV_PROFILE = (
    "Grafická dizajnérka s polygrafickým vzdelaním a praxou v tvorbe vizuálnych identít, obalov, tlačovín a obsahu pre značky. "
    "Remeselný základ z polygrafie a z prípravy podkladov do tlače spájam s marketingovým myslením zo štúdia mediálnej komunikácie a s typografiou, ktorá text nesie a neprekrýva.")

VARIANTS = {
    "portfolio": {
        "file": "portfolio-dokument.html",
        "pdf": "Viktoria-Mikuskova-portfolio.pdf",
        # Všetky disciplíny naplno. Dve verzie znamenali, že sa pred každým
        # odoslaním muselo rozhodovať, ktorú poslať; jedna to rozhodovanie ruší.
        "lead": ["vizualna-identita", "obaly", "ilustracia", "knizny-dizajn",
                 "tlacoviny", "socialne-siete"],
        "title": "Portfólio",
        "closing": CV_PROFILE,
        "more_title": None,
        "more_lead": None,
    },
}


def in_lead(p, keys):
    """Projekt patrí do vedúcej časti priamo alebo cez pole cross."""
    cats = {p.get("category")} | set(p.get("cross") or [])
    return bool(cats & set(keys))


def more_page(items, title, lead):
    """Záverečný prehľad druhej disciplíny — kontaktný hárok, nie plné strany."""
    cells = ""
    for p in items:
        img = p.get("cover") or next(
            (i["src"] for i in (p.get("images") or []) if i.get("src")), None)
        vis = (f'<img src="{esc(img)}" alt="">' if img
               else '<div class="pf-mini-empty"><span>obrázok</span></div>')
        cells += (f'<figure class="pf-mini">{vis}'
                  f'<figcaption>{esc(p.get("title"))}</figcaption></figure>')
    return f'''
  <section class="page pf-more">
    <div class="pf-more-head">
      <h2>{esc(title)}</h2>
      <p>{esc(lead)}</p>
    </div>
    <div class="pf-mini-grid">{cells}</div>
  </section>
'''


def has_image(p):
    return bool(p.get("cover") or [i for i in (p.get("images") or []) if i.get("src")])


def build_portfolio_pdf(projects, key):
    v = VARIANTS[key]
    # Do posielaného PDF ide len hotová práca. Projekt bez obrázka by bol
    # prázdna strana, a tá ubližuje viac, než keby tam nebola vôbec — na webe
    # ostáva s poznámkou, že sa pripravuje.
    ready = [p for p in projects if has_image(p)]
    lead = [p for p in ready if in_lead(p, v["lead"])]
    other = [p for p in ready if not in_lead(p, v["lead"])]
    skipped = len(projects) - len(ready)

    total = len(lead)
    pages = "".join(portfolio_page(p, i + 1, total) for i, p in enumerate(lead))
    tail = (more_page(other, v["more_title"], v["more_lead"])
            if other and v.get("more_title") else "")

    html = doc_head(f'Portfólio - {NAME}', "dokumenty.css") + f'''
  <section class="page pf-cover">
    <header class="pf-cover-top">
      <div class="pf-cover-id">
        <img class="pf-cover-logo" src="assets/images/logo.png" alt="">
        <p class="pf-cover-name">{esc(NAME)}</p>
      </div>
      <div class="pf-cover-cols">
        <div><h3>Kontakt</h3><p>{esc(EMAIL)}<br>{esc(PHONE)}</p></div>
        <div><h3>Miesto</h3><p>{esc(CITY)}<br>Slovensko</p></div>
        <div><h3>Web</h3><p>{esc(SITE_URL)}</p></div>
      </div>
    </header>
    <div class="pf-cover-mid">
      <p class="pf-cover-kicker">Výber z prác</p>
      <h1><span class="pf-outline">Grafické</span><span class="pf-solid">Portfólio</span></h1>
      <p class="pf-cover-role">{esc(COVER_ROLE)}</p>
    </div>
    <span class="pf-shape pf-shape-a"></span>
    <span class="pf-shape pf-shape-b"></span>
  </section>
{contents_page(lead)}{about_page()}
{pages}{tail}
  <section class="page pf-end">
    <div class="pf-cover-id pf-end-id">
      <img class="pf-cover-logo" src="assets/images/logo.png" alt="">
      <p class="pf-cover-name">{esc(NAME)}</p>
    </div>
    <div class="pf-end-mid">
      <h2>Ďakujem za pozornosť</h2>
      <p class="pf-end-text">{esc(v["closing"])}</p>
      <ul class="pf-end-contact">
        <li>{esc(PHONE)}</li>
        <li>{esc(EMAIL)}</li>
        <li>{esc(SITE_URL)}</li>
        <li>{esc(CITY)}</li>
      </ul>
    </div>
    <figure class="pf-end-qr">
      <img src="assets/dokumenty/qr-web.png" alt="QR kód na portfólio">
      <figcaption>{esc(SITE_URL)}</figcaption>
    </figure>
    <span class="pf-shape pf-shape-e"></span>
  </section>
</body>
</html>
'''
    with open(os.path.join(ROOT, v["file"]), "w", encoding="utf-8") as f:
        f.write(html)

    n_pages = 3 + total + (1 if tail else 0) + 1
    print(f'  {v["file"]} — {n_pages} strán, {total} projektov naplno, '
          f'{len(other)} v prehľade, {skipped} vynechaných (bez obrázka)')
    return skipped


# ===========================================================================
# Životopis — cv.html je písaný ručne, ale adresa webu v ňom musí sedieť
# s ostatnými dokumentmi. Preto ju sem doťahujeme z SITE_URL.
# ===========================================================================
KNOWN_URLS = ("viktoria-mikuskova.pages.dev", "viktoriamikuskova.com",
              "xmikuskova.myportfolio.com")


def sync_cv_url():
    for name in ("cv.html", "cv-en.html"):
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            print(f"  ! {name} neexistuje — adresa nesynchronizovaná")
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()

        changed = 0
        for old in KNOWN_URLS:
            if old == SITE_URL:
                continue
            changed += html.count(old)
            html = html.replace(old, SITE_URL)

        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
        print(f"  {name} — adresa webu: {SITE_URL} ({changed} zmien)")


def main():
    projects = load_projects()
    print(f"Dokumenty ({len(projects)} projektov, web: {SITE_URL})")
    build_qr()
    sync_cv_url()
    missing = max(build_portfolio_pdf(projects, k) for k in VARIANTS)
    if missing:
        print(f"  ! {missing} projektov nemá obrázok, do PDF sa nedostali")
    print("Hotovo. PDF-ká: node make_pdf.js")


if __name__ == "__main__":
    main()
