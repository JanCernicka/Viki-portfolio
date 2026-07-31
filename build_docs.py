#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor tlačených a posielateľných dokumentov.

    python3 build_docs.py

Vytvorí:
    portfolio-dokument.html posielateľné portfólio (jedno, všetky disciplíny)
    hlavickovy-papier.html  hlavičkový papier na sprievodné listy
    promo.html              záložky do knihy — promo kus, 4 na A4
    podpis.html             e-mailový podpis + návod na vloženie
    dokumenty.html          stránka na stiahnutie: životopis a portfólio
    assets/dokumenty/qr-web.png

Potom sa z nich urobia PDF-ká:
    node make_pdf.js
"""

import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Jedno miesto, kde je adresa webu. Keď sa viktoriamikuskova.com prepne na
# nové portfólio, prepíš SITE_URL, spusti build_docs.py a node make_pdf.js —
# adresa sa zmení v CV, na hlavičkovom papieri, v podpise aj na záložkách.
# ---------------------------------------------------------------------------
SITE_URL = "viktoria-mikuskova.pages.dev"
SITE_HREF = "https://" + SITE_URL

NAME = "Viktória Mikušková"
# Na úradný list a do podpisu patrí titul; na obálku portfólia a na záložku nie.
NAME_FORMAL = "Mgr. Viktória Mikušková"
ROLE = "Grafická dizajnérka a ilustrátorka"
# Na záložku sa dlhý titulok nezmestí — 45 mm šírky neuživí dva riadky verzálok.
ROLE_SHORT = "Grafická dizajnérka"
PHONE = "0917 749 871"
PHONE_TEL = "0917749871"
EMAIL = "viki.mikuskova@gmail.com"
CITY = "Bratislava"
INSTAGRAM = "https://www.instagram.com/vikca.design"
LINKEDIN = ("https://www.linkedin.com/in/vikt%C3%B3ria-miku%C5%A1kov%C3%A1-245b77324")

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
    imgs = [i for i in (p.get("images") or []) if i.get("src")]

    if cover:
        visual = f'<img class="pf-img" src="{esc(cover)}" alt="">'
    elif imgs:
        visual = f'<img class="pf-img" src="{esc(imgs[0]["src"])}" alt="">'
    else:
        visual = ('<div class="pf-empty"><span>obrázok projektu</span>'
                  '<span class="pf-empty-note">doplniť pred odoslaním</span></div>')

    # Ďalšie zábery na tej istej strane — max tri, aby strana ostala čistá.
    strip = ""
    extra = imgs[1:4] if cover else imgs[1:4]
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
  <section class="page pf-project" style="--ratio:{ratio}">
    <div class="pf-visual">{visual}{strip}</div>
    <div class="pf-text">
      <h2>{esc(p.get("title"))}</h2>
      <p class="pf-meta">{meta_line}</p>
      <p class="pf-body">{esc(body)}</p>
      {facts_html}
    </div>
    <div class="pf-num">{n} / {total}</div>
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

    html = doc_head(f'Portfólio — {v["title"]} — {NAME}', "dokumenty.css") + f'''
  <section class="page pf-cover">
    <img class="pf-cover-logo" src="assets/images/logo.png" alt="">
    <div class="pf-cover-mid">
      <h1>{esc(NAME)}</h1>
      <p class="pf-cover-role">{esc(COVER_ROLE)}</p>
    </div>
    <div class="pf-cover-foot">
      <span>Výber z prác</span>
      <span>{esc(SITE_URL)}</span>
    </div>
  </section>
{pages}{tail}
  <section class="page pf-end">
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
    <img class="pf-end-qr" src="assets/dokumenty/qr-web.png" alt="QR kód na portfólio">
  </section>
</body>
</html>
'''
    with open(os.path.join(ROOT, v["file"]), "w", encoding="utf-8") as f:
        f.write(html)

    n_pages = 1 + total + (1 if tail else 0) + 1
    print(f'  {v["file"]} — {n_pages} strán, {total} projektov naplno, '
          f'{len(other)} v prehľade, {skipped} vynechaných (bez obrázka)')
    return skipped


# ===========================================================================
# Hlavičkový papier
# ===========================================================================
def build_letterhead():
    html = doc_head("Hlavičkový papier — " + NAME, "dokumenty.css") + f'''
  <section class="page lh">
    <header class="lh-head">
      <div>
        <p class="lh-name">{esc(NAME_FORMAL)}</p>
        <p class="lh-role">{esc(ROLE)}</p>
      </div>
      <img class="lh-logo" src="assets/images/logo.png" alt="">
    </header>

    <div class="lh-body" contenteditable="true">
      <p class="lh-place">V Bratislave, 1. januára 2026</p>

      <p class="lh-to">
        Vydavateľstvo ABC<br>
        Meno Priezvisko<br>
        Ulica 1, 000 00 Mesto
      </p>

      <p class="lh-subject">Vec: Žiadosť o miesto grafického dizajnéra</p>

      <p>Dobrý deň, pani/pán …,</p>

      <p>
        [Sem napíš list. Túto stranu môžeš prepísať priamo v prehliadači —
        text je editovateľný. Keď je hotový, dај Ctrl+P → Uložiť ako PDF.]
      </p>

      <p class="lh-sign">S pozdravom<br><span>{esc(NAME_FORMAL)}</span></p>
    </div>

    <footer class="lh-foot">
      <span>{esc(PHONE)}</span>
      <span>{esc(EMAIL)}</span>
      <span>{esc(SITE_URL)}</span>
      <span>{esc(CITY)}</span>
    </footer>
  </section>
</body>
</html>
'''
    html = html.replace("dај", "daj")  # poistka proti preklepu v cyrilike
    with open(os.path.join(ROOT, "hlavickovy-papier.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("  hlavickovy-papier.html")


# ===========================================================================
# Promo kus — záložka do knihy
# ===========================================================================
def bookmark_front():
    return f'''
      <div class="bm bm-front">
        <img class="bm-art" src="assets/images/hero-illustration.jpg" alt="">
        <div class="bm-front-text">
          <p class="bm-name">{esc(NAME)}</p>
          <p class="bm-role">{esc(ROLE_SHORT)}</p>
        </div>
        <p class="bm-focus">knižný dizajn<br>ilustrácia<br>vizuálna identita</p>
      </div>'''


def bookmark_back():
    return f'''
      <div class="bm bm-back">
        <img class="bm-logo" src="assets/images/logo.png" alt="">
        <p class="bm-quote">Typografia má text niesť, nie ho prekrývať.</p>
        <img class="bm-qr" src="assets/dokumenty/qr-web.png" alt="">
        <ul class="bm-contact">
          <li>{esc(SITE_URL)}</li>
          <li>{esc(EMAIL)}</li>
          <li>{esc(PHONE)}</li>
        </ul>
      </div>'''


def build_promo():
    fronts = "".join(bookmark_front() for _ in range(4))
    # Pri obojstrannej tlači sa list preklopí — zadné strany idú zrkadlovo.
    backs = "".join(bookmark_back() for _ in range(4))
    html = doc_head("Záložky — promo kus", "dokumenty.css") + f'''
  <section class="page promo">
    <div class="bm-row">{fronts}</div>
    <p class="promo-note">Predná strana &nbsp;·&nbsp; 4 × 45 × 180 mm &nbsp;·&nbsp;
       tlač obojstranne, dlhá hrana, 300 g matná</p>
  </section>

  <section class="page promo">
    <div class="bm-row">{backs}</div>
    <p class="promo-note">Zadná strana</p>
  </section>
</body>
</html>
'''
    with open(os.path.join(ROOT, "promo.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("  promo.html — 4 záložky, 2 strany A4")


# ===========================================================================
# E-mailový podpis
# ===========================================================================
def signature_markup():
    """Podpis pre e-mail. Tabuľka a inline štýly — inak sa v Outlooku rozsype."""
    return f'''<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;">
<tr>
<td style="border-left:3px solid #C6673D;padding:2px 0 2px 12px;">
<div style="font-size:15px;font-weight:bold;color:#011126;line-height:1.3;">{NAME_FORMAL}</div>
<div style="font-size:12px;color:#C6673D;letter-spacing:.06em;padding-top:2px;">{ROLE.upper()}</div>
<div style="font-size:11px;color:#676340;padding-top:1px;">knižný dizajn &middot; sadzba &middot; vizuálna identita</div>
<div style="font-size:12px;color:#333333;padding-top:8px;line-height:1.6;">
<a href="tel:{PHONE_TEL}" style="color:#333333;text-decoration:none;">{PHONE}</a> &nbsp;|&nbsp;
<a href="mailto:{EMAIL}" style="color:#333333;text-decoration:none;">{EMAIL}</a><br>
<a href="{SITE_HREF}" style="color:#C6673D;text-decoration:none;font-weight:bold;">{SITE_URL}</a> &nbsp;|&nbsp;
<a href="{INSTAGRAM}" style="color:#333333;text-decoration:none;">Instagram</a> &nbsp;|&nbsp;
<a href="{LINKEDIN}" style="color:#333333;text-decoration:none;">LinkedIn</a>
</div>
</td>
</tr>
</table>'''


def build_signature():
    sig = signature_markup()
    code = esc(sig)
    html = doc_head("E-mailový podpis — " + NAME, "dokumenty.css") + f'''
  <div class="tool">
    <h1>E-mailový podpis</h1>
    <p class="tool-lead">
      Podpis je tabuľka s inline štýlmi — takto vydrží aj v Outlooku, kde sa
      bežné CSS zahodí. Neobsahuje obrázok, lebo obrázky v podpise sa v mnohých
      e-mailových klientoch blokujú a namiesto loga by prišiel prázdny štvorec.
    </p>

    <h2>1. Ako vyzerá</h2>
    <div class="sig-preview">
{sig}
    </div>

    <h2>2. Vložiť do Gmailu</h2>
    <ol class="tool-steps">
      <li>Klikni na tlačidlo <strong>Skopírovať podpis</strong> nižšie.</li>
      <li>Gmail → ozubené koliesko → <em>Zobraziť všetky nastavenia</em>.</li>
      <li>Dole v záložke <em>Všeobecné</em> nájdi <em>Podpis</em> → <em>Vytvoriť nový</em>.</li>
      <li>Do poľa daj <kbd>Ctrl</kbd> + <kbd>V</kbd>. Formátovanie sa prenesie.</li>
      <li>Nastav ho pre <em>Nová správa</em> aj <em>Odpoveď/preposlanie</em>.</li>
      <li>Úplne dole <em>Uložiť zmeny</em>.</li>
    </ol>

    <p><button class="tool-btn" id="copySig" type="button">Skopírovať podpis</button>
       <span class="tool-ok" id="copyOk" hidden>skopírované</span></p>

    <h2>3. Vložiť do Outlooku</h2>
    <ol class="tool-steps">
      <li>Skopíruj podpis rovnako ako vyššie.</li>
      <li>Outlook → <em>Súbor</em> → <em>Možnosti</em> → <em>Pošta</em> → <em>Podpisy</em>.</li>
      <li><em>Nový</em>, pomenuj ho, vlož a ulož.</li>
    </ol>

    <h2>4. Zdrojový kód</h2>
    <p class="tool-lead">Ak by ho niekto potreboval vložiť ručne:</p>
    <pre class="tool-code" id="sigCode">{code}</pre>
  </div>

<script>
document.getElementById('copySig').addEventListener('click', async function () {{
  var el = document.querySelector('.sig-preview');
  var ok = document.getElementById('copyOk');
  try {{
    var html = el.innerHTML;
    await navigator.clipboard.write([new ClipboardItem({{
      'text/html': new Blob([html], {{type: 'text/html'}}),
      'text/plain': new Blob([el.innerText], {{type: 'text/plain'}})
    }})]);
  }} catch (e) {{
    // Staršie prehliadače: označíme podpis, nech ho stačí skopírovať klávesnicou.
    var r = document.createRange();
    r.selectNodeContents(el);
    var s = window.getSelection();
    s.removeAllRanges();
    s.addRange(r);
    document.execCommand('copy');
  }}
  ok.hidden = false;
  setTimeout(function () {{ ok.hidden = true; }}, 2500);
}});
</script>
</body>
</html>
'''
    with open(os.path.join(ROOT, "podpis.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("  podpis.html")


# ===========================================================================
# Rozcestník
# ===========================================================================
# ===========================================================================
# Životopis — cv.html je písaný ručne, ale adresa webu v ňom musí sedieť
# s ostatnými dokumentmi. Preto ju sem doťahujeme z SITE_URL.
# ===========================================================================
KNOWN_URLS = ("viktoria-mikuskova.pages.dev", "viktoriamikuskova.com",
              "xmikuskova.myportfolio.com")


def sync_cv_url():
    path = os.path.join(ROOT, "cv.html")
    if not os.path.exists(path):
        print("  ! cv.html neexistuje — adresa nesynchronizovaná")
        return
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
    print(f"  cv.html — adresa webu: {SITE_URL} ({changed} zmien)")


def build_hub(missing):
    """Stránka na stiahnutie. Sem chodí človek, ktorý si prezrel prácu a chce
    si ju odniesť — teda dva súbory a nič iné. Hlavičkový papier, záložky
    a e-mailový podpis sa naďalej generujú, len sa už neponúkajú tu; sú to jej
    pracovné nástroje, nie niečo, čo si sťahuje personalista."""
    # Upozornenie na chýbajúce obrázky patrí do terminálu, nie na stránku,
    # ktorú vidí personalista.
    if missing:
        print(f"  ! {missing} projektov nemá obrázok, do PDF sa nedostali")

    v = VARIANTS["portfolio"]
    html = doc_head("Dokumenty na stiahnutie — " + NAME, "dokumenty.css",
                    noindex=False) + f'''
  <div class="tool">
    <h1>Dokumenty na stiahnutie</h1>
    <p class="tool-lead">
      Ak Vás moje portfólio zaujalo, viete si ho tu stiahnuť.
    </p>

    <ul class="hub">
      <li>
        <h2><a href="assets/cv/Viktoria-Mikuskova-CV.pdf" download>Životopis na stiahnutie</a></h2>
        <p>Jedna strana A4.
           <a href="cv.html">Pozrieť v prehliadači</a></p>
      </li>
      <li>
        <h2><a href="assets/dokumenty/{v["pdf"]}" download>Portfólio na stiahnutie</a></h2>
        <p>Výber prác naprieč vizuálnou identitou, obalmi, ilustráciou, knižným
           dizajnom, tlačovinami aj sociálnymi sieťami.
           <a href="{v["file"]}">Pozrieť v prehliadači</a></p>
      </li>
    </ul>
  </div>
</body>
</html>
'''
    with open(os.path.join(ROOT, "dokumenty.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("  dokumenty.html")


def main():
    projects = load_projects()
    print(f"Dokumenty ({len(projects)} projektov, web: {SITE_URL})")
    build_qr()
    sync_cv_url()
    missing = max(build_portfolio_pdf(projects, k) for k in VARIANTS)
    build_letterhead()
    build_promo()
    build_signature()
    build_hub(missing)
    print("Hotovo. PDF-ká: node make_pdf.js")


if __name__ == "__main__":
    main()
