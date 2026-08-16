#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Krátky ťahák na celý pohovor.

    python3 career/make_tahak_pohovor.py

Vytvorí career/12-tahak-pohovor.html. Toto je verzia na prečítanie tesne
pred pohovorom. Dlhá príprava 10-pohovor-sng.html ostáva ako záloha.
"""

import importlib.util
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "12-tahak-pohovor.html")

_spec = importlib.util.spec_from_file_location(
    "high5", os.path.join(ROOT, "make_pohovor.py"))
_h5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_h5)
e, fonts, CSS = _h5.e, _h5.fonts, _h5.CSS


UPOKOJENIE = (
    "Skôr než začneš čítať čokoľvek iné. Z ľudí, ktorí poslali životopis, "
    "pozvali teba. Rozhodnutie o tom, či si dosť dobrá na to, aby s tebou "
    "strácali hodinu, už padlo a dopadlo pre teba. Zajtra sa nerozhoduje, "
    "či vieš robiť grafiku. Zajtra sa zisťuje, či si sadnete."
)

PRIEBEH = [
    ("10:50", "Buď pred budovou. Na recepcii povedz: mám dohodnutý pohovor "
              "s pani Pilo o jedenástej."),
    ("0 až 3 min", "Privítanie, kam si odložiť veci, ponúknu ti vodu. "
                   "Vezmi si ju. Dúšok je jediná legálna pauza, ktorú počas "
                   "rozhovoru máš."),
    ("3 až 5 min", "Odovzdáš vyplnený dotazník. Tým sa začne rozhovor sám, "
                   "nemusíš nič vymýšľať."),
    ("5 až 10 min", "Povedzte nám niečo o sebe. Deväťdesiat sekúnd, tri body. "
                    "Toto je jediná otázka, ktorú vieš na sto percent dopredu."),
    ("10 až 25 min", "Otázky o praxi, o programoch, o tom, ako pracuješ. "
                     "Sem patrí aj portfólio, ak si ho vypýtajú."),
    ("25 až 35 min", "Predstavia pozíciu, tím a to, ako to u nich chodí. "
                     "Tu si píš. Písanie ťa zároveň upokojí."),
    ("35 až 40 min", "Tvoje otázky, plat a termín nástupu."),
    ("Na konci", "Povedia, dokedy sa ozvú. Ak to nepovedia, spýtaj sa. "
                 "Je to normálna otázka a ušetrí ti týždeň čakania."),
]

VETY = [
    ("O sebe",
     "Grafike sa venujem od strednej polygrafickej, potom som vyštudovala "
     "dizajn médií a magisterské štúdium masmediálnej a marketingovej "
     "komunikácie. Teraz robím obsah a vizuály pre ShapelesAi, predtým som "
     "bola v MOJESIDLO.SK. Hľadám miesto, kde bude príprava tlačovín a sadzba "
     "hlavná náplň, a preto som tu."),
    ("Prečo galéria",
     "Lákajú ma zadania, ktoré niekto naozaj drží v ruke a chodí okolo nich. "
     "Vo firemnej grafike väčšina vecí skončí na obrazovke, tu má veľká časť "
     "výstupov fyzickú podobu."),
    ("Prečo junior, keď máš titul",
     "Titul mám z komunikácie, grafiku mám z priemyslovky a z praxe. Chcem sa "
     "dostať tam, kde sa robí veľa tlačovín, a naučiť sa to poriadne."),
    ("Ako pripravuješ do tlače",
     "Sadzba v InDesigne, spadávky podľa tlačiarne, obrázky v CMYK s ich "
     "profilom, kontrola preflightom a export do PDF/X. Pred odovzdaním "
     "si vždy prejdem náhľad po stranách."),
    ("Cudzia identita a vlastný názor",
     "Beriem to ako pravidlá hry. Najprv chcem vedieť, prečo je niečo tak, "
     "ako je. Návrh na zmenu poviem, ale až keď tomu systému rozumiem, "
     "nie na tretí deň."),
    ("Plat",
     "Viem, že tarifa je daná zákonom a pohyblivé je osobné ohodnotenie. "
     "V inzeráte je 1 400 až 1 600 a rada by som sa bavila o hornej polovici. "
     "Mám magisterský titul, polygrafickú strednú a takmer dva roky praxe."),
]

TROJKA = [
    ("Orientačný systém pre PEVŠ",
     "Vyrobený a visí v areáli školy. V inzeráte pýtajú navigačné systémy "
     "v priestore. Toto nebude mať nikto iný."),
    ("Polygrafická priemyslovka",
     "Spadávky, orezové značky, CMYK, export do tlače. Ich požiadavky sú "
     "tvoja stredná škola."),
    ("Alica a NOOK BOOKS",
     "Päť knižných prebalov a dizajn manuál. Dôkaz, že InDesign nie je "
     "len položka v životopise."),
]

MOJE_OTAZKY = [
    "Čítala som, že vašu identitu robíte interne a vyvíja sa postupne. "
    "Ako to vyzerá, keď príde nová výstava?",
    "S kým by som pracovala a kto dnes robí grafiku k výstavám?",
    "V akej fáze prípravy výstavy vstupuje do hry grafik?",
    "Čo by ste chceli, aby ten človek zvládol sám do pol roka?",
]

ZASEKNUTIE = [
    ("Keď ti vypadne slovo",
     "Povedz nahlas: dám si sekundu, nech to poviem poriadne. Dve sekundy "
     "ticha znejú premyslene. Vypĺňanie ticha zvukmi nie."),
    ("Keď niečo nevieš",
     "Priznaj to jednou vetou a spýtaj sa. To som zatiaľ nerobila, ako to "
     "u vás chodí? Pri juniorovi je zvedavosť plus, predstieranie mínus."),
    ("Keď ti vypadne meno",
     "Opíš vec. Neviem si spomenúť na meno, ale bol to ten odšťavovač pre "
     "Alessi, čo vyzerá ako pavúk. Opísaná vec je lepšia než zlé meno."),
    ("Keď je ticho",
     "Ticho po tvojej odpovedi je ich problém, nie tvoj. Nedopĺňaj ho "
     "ďalšími vetami. Väčšina ľudí sa zhorší práve tým, že hovorí ďalej."),
    ("Keď sa spýtajú na niečo nepríjemné",
     "Odpovedz krátko, bez ospravedlňovania, a vráť sa k tomu, čo vieš. "
     "Zdržiavanie sa pri slabine je horšie než tá slabina."),
]

VEZMI = [
    ("Vyplnený dotazník", "Vytlačený a vyplnený doma, nie v čakárni."),
    ("Dve kópie životopisu", "Vytlačené. Môžu tam byť dvaja ľudia."),
    ("Portfólio dvakrát", "V notebooku aj vytlačené. Nabitý notebook."),
    ("Papier a pero", "Aby si si mohla písať. Zamestná ti to ruky."),
    ("Občiansky preukaz", "Do administratívnej budovy môžu chcieť zápis."),
    ("Vodu", "Vlastnú, keby neponúkli."),
]

NERVOZITA = [
    ("Vedie to HR, nie grafik",
     "Alexandra Pilo je HR manažérka. Nebude ťa skúšať z kriviek ani "
     "z profilov. Prvé kolo je o tom, kto si a či to má hlavu a pätu."),
    ("Nie je to skúška, je to rozhovor",
     "Aj ty si vyberáš. Preto tam máš svoje otázky. Keď si ich položíš, "
     "sama sa v tom cítiš inak."),
    ("Ruky",
     "Pohár vody, papier, pero. Nervozita sa najviac vidí na rukách, "
     "tak im daj čo robiť."),
    ("Prvé tri minúty",
     "Sú najhoršie a potom to prejde. Vydrž ich a zvyšok už ide sám."),
    ("Nechoď priskoro",
     "Dvadsať minút v čakárni ťa rozhodí viac než čokoľvek iné. Desať minút "
     "je akurát."),
    ("Ak sa pomýliš",
     "Nikto si to nezapíše. Ľudia si z pohovoru pamätajú dojem, nie vety."),
]


def build():
    o = ["<title>Ťahák na pohovor SNG</title>", "<style>", fonts(), CSS, "</style>",
         '<div class="wrap">',
         '<header class="masthead">',
         '<p class="eyebrow">Pondelok 17. augusta, 11:00, Riečna 1</p>',
         "<h1>Ťahák na pohovor</h1>",
         f'<p class="lede">{e(UPOKOJENIE)}</p>',
         "</header>"]

    o += ['<section class="sect"><h2>Čo sa bude diať</h2>',
          '<p class="intro">Bežný prvý pohovor trvá tridsať až štyridsaťpäť '
          'minút a má takmer vždy toto poradie. Keď vieš, čo príde, prestane '
          'to byť neznáme.</p>',
          '<dl class="facts">']
    o += [f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in PRIEBEH]
    o += ["</dl></section>"]

    o += ['<section class="sect"><h2>Šesť viet, ktoré stačia</h2>',
          '<p class="intro">Neuč sa ich naspamäť, prečítaj si ich dvakrát. '
          'Stačí, keď si zapamätáš kostru, slová si nájdeš sama.</p>',
          '<ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in VETY]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Tri veci, ktoré musia zaznieť</h2>',
          '<p class="intro">Ak z celého pohovoru povieš len tieto tri, '
          'urobila si maximum.</p>',
          '<ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in TROJKA]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Čo sa spýtaš ty</h2>',
          '<p class="intro">Vyber si dve. Prvá je najsilnejšia.</p>',
          '<ul class="rows">']
    o += [f"<li><b>{e(q)}</b></li>" for q in MOJE_OTAZKY]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Keď to zaškrípe</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in ZASEKNUTIE]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Čo si vezmi</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in VEZMI]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Na tú nervozitu</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in NERVOZITA]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Čo nehovor</h2><ul class="rows">',
          '<li><b>Politiku okolo vedenia galérie</b><span>Ani slovom, ani ako '
          'otázku.</span></li>',
          '<li><b>Kritiku ich vizuálu alebo výstav</b><span>Autori identity '
          'sedia v tej istej budove.</span></li>',
          '<li><b>Beriem to zatiaľ</b><span>Ani v náznaku.</span></li>',
          '<li><b>Vizitky ma nebavia</b><span>Sú priamo v náplni '
          'práce.</span></li>',
          '<li><b>Benefity ako prvú otázku</b><span>Multisport nie je '
          'to, čo ťa tam ťahá.</span></li>',
          '<li><b>Sťažnosti na predchádzajúcu prácu</b><span>Hovor o tom, kam '
          'ideš, nie odkiaľ utekáš.</span></li>',
          "</ul></section>"]

    o += ['<p class="foot">Po pohovore, do 24 hodín: krátky ďakovný mail '
          'Alexandre Pilo s jednou vetou k niečomu, čo odznelo, a žiadosť '
          'o spojenie na LinkedIne. Vtedy je na mieste aj veta o budúcej '
          'spolupráci. A ešte raz to hlavné: oni si ťa vybrali. Choď tam ako '
          'človek, ktorý má čo ukázať.</p>',
          "</div>"]

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    return os.path.getsize(OUT)


if __name__ == "__main__":
    n = build()
    print(f"  12-tahak-pohovor.html — {round(n / 1024)} kB")
