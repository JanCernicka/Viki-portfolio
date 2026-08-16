#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ťahák na otázky o umení a dizajne.

    python3 career/make_tahak.py

Vytvorí career/11-tahak-mena.html. Krátke, na prečítanie v aute pred
pohovorom. Vzhľad si berie z prípravy na High5.
"""

import importlib.util
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "11-tahak-mena.html")

_spec = importlib.util.spec_from_file_location(
    "high5", os.path.join(ROOT, "make_pohovor.py"))
_h5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_h5)
e, fonts, CSS = _h5.e, _h5.fonts, _h5.CSS


PRAVIDLO = (
    "Menuj len toho, koho vieš opísať. Zoznam nižšie je na to, aby ti "
    "nevypadla hlava, nie na vymenúvanie. Jedno meno a jedna konkrétna vec "
    "o ňom sú lepšie než päť mien bez obsahu."
)

MUCHA = [
    ("Kto", "Alfons Mucha, 1860 až 1939, Moravan, ktorý sa preslávil v Paríži."),
    ("Zlom", "Plagát Gismonda pre Sarah Bernhardt z roku 1894. Urobil ho cez "
             "Vianoce, keď nikto iný nebol v tlačiarni, a cez noc sa stal známym."),
    ("Štýl", "Vysoký úzky formát, žena s vlnitými vlasmi, oblúk alebo svätožiara "
             "za hlavou, tlmená pastelová farebnosť, ornamentálny rám a písmo, "
             "ktoré je súčasťou obrazu, nie prilepené navrch."),
    ("Prečo je tvoj", "Bol to reklamný grafik. Robil plagáty, obaly na cigaretové "
                      "papieriky JOB, etikety pre Moët & Chandon, šperky aj "
                      "vzorkovníky. Presne tá kombinácia ilustrácie a typografie, "
                      "ktorú robíš ty."),
    ("Keby sa pýtali ďalej", "Slovanská epopej, dvadsať monumentálnych plátien, "
                             "na ktorých robil osemnásť rokov a považoval ich za "
                             "svoje životné dielo."),
]

MUCHA_POVEDZ = (
    "Mucha, kvôli plagátom. Páči sa mi, že u neho písmo nie je nalepené na "
    "obrázok, ale je súčasťou kompozície, aj ten oblúk za hlavou, ktorý drží "
    "celý plagát pokope. A bol to v podstate reklamný grafik, robil obaly aj "
    "etikety, takže je mi blízky aj tým, čo robil, nielen ako to vyzerá."
)

STARCK = [
    ("Kto", "Philippe Starck, francúzsky dizajnér, jedno z najznámejších mien "
            "priemyselného dizajnu."),
    ("Ten pavúk", "Volá sa Juicy Salif, odšťavovač na citrusy pre taliansku "
                  "Alessi, 1988."),
    ("Historka", "Nakreslil ho na obrúsok v pizzerii pri mori. Priniesli mu "
                 "kalamáre s citrónom a z tvaru chápadiel vznikli tie tri nohy."),
    ("Prečo je slávny", "Je v stálych zbierkach MoMA aj Metropolitného múzea "
                        "v New Yorku a vo Victoria and Albert v Londýne. "
                        "Zároveň je to najznámejší spor o to, či musí dizajn "
                        "dobre fungovať, alebo stačí, keď o ňom ľudia hovoria."),
    ("Pozor na jednu vec", "Nie je nerezový, je z lešteného hliníka. Ak povieš "
                           "nerez, opravia ťa."),
]

KANVICA = [
    ("Richard Sapper, kávovar 9090, Alessi, 1979",
     "Nerezový espresovar s bruchatým spodkom. Prvý predmet Alessi, ktorý sa "
     "dostal do stálej zbierky MoMA. Ak to bol kávovar na sporák, je to "
     "najpravdepodobnejšie tento."),
    ("Aldo Rossi, La Conica, Alessi, 1984",
     "Nerezový kávovar s kužeľovou strieškou navrchu, vyzerá ako malá "
     "architektúra."),
    ("Michael Graves, kanvica 9093, Alessi, 1985",
     "Nerezová kanvica s červeným vtáčikom na hubici, ktorý píska. Toto je "
     "kanvica na vodu, nie na kávu, ale je najznámejšia zo všetkých."),
]

GRAFICI = [
    ("Plagát a secesia",
     "Alfons Mucha · Henri de Toulouse-Lautrec · Jules Chéret · "
     "A. M. Cassandre"),
    ("Klasici modernej grafiky",
     "Paul Rand, logá IBM a UPS · Saul Bass, filmové titulky a logá · "
     "Milton Glaser, I love NY · Massimo Vignelli, newyorské metro"),
    ("Typografia a švajčiarska škola",
     "Jan Tschichold · Josef Müller-Brockmann · Herb Lubalin · "
     "Adrian Frutiger, písmo Univers"),
    ("Novšia vlna",
     "Neville Brody, časopis The Face · David Carson, Ray Gun · "
     "Stefan Sagmeister · Paula Scher"),
    ("Slovenskí a českí",
     "Mikuláš Galanda a Ľudovít Fulla · Vladislav Rostoka · Miroslav Cipár · "
     "Albín Brunovský · Dušan Kállay · Ladislav Sutnar · Karel Teige"),
]

PRODUKT = [
    ("Ikony", "Philippe Starck · Dieter Rams, Braun a jeho desať princípov · "
              "Charles a Ray Eames, stoličky · Achille Castiglioni, lampa Arco"),
    ("Bauhaus a nábytok", "Marcel Breuer · Mies van der Rohe · Le Corbusier"),
    ("Alessi", "Richard Sapper · Aldo Rossi · Michael Graves · Alessandro Mendini"),
    ("Súčasní", "Jonathan Ive, Apple · Naoto Fukasawa · bratia Bouroullecovci"),
]

UMELCI = [
    ("Starší majstri",
     "Leonardo da Vinci · Rembrandt · Vermeer · Caravaggio · Bruegel"),
    ("Prelom storočí",
     "Vincent van Gogh · Claude Monet · Gustav Klimt · Egon Schiele · "
     "Edvard Munch · Toulouse-Lautrec"),
    ("Moderna",
     "Pablo Picasso · Henri Matisse · Wassily Kandinsky · Piet Mondrian · "
     "Paul Klee · Joan Miró · Salvador Dalí · René Magritte · Frida Kahlo"),
    ("Povojnoví a súčasní",
     "Andy Warhol · Roy Lichtenstein · Mark Rothko · Jean-Michel Basquiat · "
     "David Hockney · Yayoi Kusama · Banksy"),
    ("Slovenskí",
     "Mikuláš Galanda · Ľudovít Fulla · Martin Benka · Miloš Alexander "
     "Bazovský · Stano Filko · Juraj Bartusz · Rudolf Krivoš · Milan Laluha · "
     "Vladimír Kompánek · Erik Šille"),
]

ZALOZKA = [
    ("Ak ti vypadne meno",
     "Nepanikár a nehádaj. Povedz, čo si pamätáš: „Neviem si spomenúť na meno, "
     "ale bol to ten odšťavovač pre Alessi, čo vyzerá ako pavúk.“ Opísaná vec "
     "je lepšia než zlé meno a pôsobí to normálne, nie hlúpo."),
    ("Ak sa spýtajú na niekoho, koho nepoznáš",
     "Priznaj to jednou vetou a spýtaj sa. „To meno nepoznám, čo od neho mám "
     "pozrieť?“ Zvedavosť je pri juniorovi plus, predstieranie je mínus."),
    ("Neprepíname sa do prednášky",
     "Tridsať sekúnd na odpoveď. Ak ich to zaujme, spýtajú sa ďalej."),
]


def build():
    o = ["<title>Ťahák — umenie a dizajn</title>", "<style>", fonts(), CSS, "</style>",
         '<div class="wrap">',
         '<header class="masthead">',
         '<p class="eyebrow">Ťahák pred pohovorom</p>',
         "<h1>Obľúbený umelec, obľúbený dizajnér</h1>",
         f'<p class="lede">{e(PRAVIDLO)}</p>',
         "</header>"]

    o += ['<section class="sect"><h2>Tvoja odpoveď číslo jeden: Mucha</h2>',
          '<dl class="facts">']
    o += [f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in MUCHA]
    o += ["</dl>", f'<p class="say">{e(MUCHA_POVEDZ)}</p>', "</section>"]

    o += ['<section class="sect"><h2>Tvoja odpoveď číslo dva: Starck</h2>',
          '<dl class="facts">']
    o += [f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in STARCK]
    o += ["</dl>",
          '<p class="say">Z produktového dizajnu mám najradšej Juicy Salif od '
          'Philippa Starcka. Je to odšťavovač, ktorý vyzerá ako pavúk, a je '
          'zaujímavý tým, že sa doteraz vedú spory, či dobre funguje. Mne sa '
          'páči, že vec z kuchyne dokáže byť téma na rozhovor.</p>',
          '<h2 style="margin-top:8px">Tá nerezová kanvica na kávu</h2>',
          '<p class="intro">Podľa opisu to nevieš určiť naisto, tak si pozri '
          'tieto tri a spoznáš ju. Všetky sú od Alessi.</p>',
          '<ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in KANVICA]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Grafici a plagátisti</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in GRAFICI]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Produktový a priemyselný dizajn</h2>'
          '<ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in PRODUKT]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Výtvarní umelci</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in UMELCI]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Keď to zaškrípe</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in ZALOZKA]
    o += ["</ul></section>"]

    o += ['<p class="foot">Zapamätaj si dve mená a pri každom jednu vec: '
          'Mucha a to, že písmo je uňho súčasťou kompozície. Starck a ten '
          'obrúsok v pizzerii. To bohato stačí a je to pravda.</p>',
          "</div>"]

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    return os.path.getsize(OUT)


if __name__ == "__main__":
    n = build()
    print(f"  11-tahak-mena.html — {round(n / 1024)} kB")
