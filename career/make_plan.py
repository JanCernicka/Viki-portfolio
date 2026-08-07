#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor týždenného plánu.

    python3 career/make_plan.py

Prepíše obe verzie z jedného zdroja:
    career/08-tyzdenny-plan.md    na čítanie a do gitu
    career/08-tyzdenny-plan.html  na odškrtávanie, ukladá sa do prehliadača

HTML si z existujúceho súboru zoberie hlavičku so štýlom (sú v nej vložené
fonty v base64) a skript na konci, prepíše len obsah medzi nimi. Preto sa dá
spúšťať opakovane a fonty sa nemusia nikdy vkladať znova.
"""

import html as htmllib
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(ROOT, "08-tyzdenny-plan.md")
HTML = os.path.join(ROOT, "08-tyzdenny-plan.html")

# ---------------------------------------------------------------------------
# Zdroj obsahu. "w" znamená SHAPELESAI (platená práca), inak hľadanie práce.
# ---------------------------------------------------------------------------

LEDE = ("Osemhodinový pracovný deň, 8:30 až 16:30. Dve dráhy naraz: platená "
        "práca pre SHAPELESAI a hľadanie miesta grafickej dizajnérky. Rytmus "
        "dňa je každý deň rovnaký, menia sa len dva hlboké bloky. "
        "Odškrtávaj priamo tu, ostane to uložené v prehliadači.")

GOALS = [
    ("5", "oslovení, jedno na deň", "h"),
    ("2+", "prihlášky na inzerát", "h"),
    ("5+1", "postov a jeden reel pre SHAPELESAI", "w"),
    ("1", "nová vec do portfólia", "w"),
]

RULES = [
    "Témy nevymýšľaj. Každý deň má pridelený pilier, ty len vyplníš slot.",
    "Texty píš v pondelok všetky naraz. Grafiku rob až v utorok. Nikdy nie oboje v jednom bloku.",
    "Nový layout nekresli. Máš štyri šablóny, meníš v nich text.",
    "Jedno oslovenie denne, medzi 9:00 a 9:15. Na inzerát sa hlás v ten deň, keď ho nájdeš.",
    "Na každú odpoveď reaguj do 24 hodín a vždy poďakuj.",
]

RHYTHM = [
    ("8:30 · 30 min", "Štart", "Pošta, odpovede na to, čo prišlo, kontrola nových inzerátov."),
    ("9:00 · 15 min", "Oslovenie", "Pusti jednu správu z piatkového bloku a zapíš riadok do tabuľky."),
    ("9:15 · 2 h 30", "Hlboký blok 1", "Najťažšia vec dňa. Telefón preč, pošta zavretá."),
    ("11:45 · 45 min", "Obed", "Preč od počítača. Nie je to voliteľné, po ňom ide druhý hlboký blok."),
    ("12:30 · 2 h 15", "Hlboký blok 2", "Druhá veľká vec dňa."),
    ("14:45 · 15 min", "Prestávka", ""),
    ("15:00 · 1 h 15", "Ľahký blok", "Veci, ktoré znesú prerušenie."),
    ("16:15 · 15 min", "Zápis", "Čo je hotové, čo prešlo na zajtra, jeden riadok do tabuľky."),
]

PILLARS = [
    ("Pondelok", "Mýtus a realita",
     "Jedna vec, ktorú si remeselníci myslia, a ako to je v skutočnosti. Formát, ktorý ti už raz fungoval."),
    ("Utorok", "Chyba, ktorá stojí zákazku",
     "Konkrétna chyba pri získavaní zákaziek a čo presne sa ňou stráca."),
    ("Streda", "Ako to funguje",
     "Jeden kúsok mechanizmu: reklama, odpoveď do minúty, stránka, rezervácia, recenzia. Vždy len jeden."),
    ("Štvrtok", "Číslo alebo dôkaz",
     "Výsledok, recenzia, porovnanie pred a po. Bez čísla to nie je dôkaz, je to tvrdenie."),
    ("Piatok", "Za oponou",
     "Ľudia, proces, ako firma pracuje. Toto je jediný pilier, kde sa smie hovoriť o sebe."),
]

COPY_STEPS = [
    ("Háčik", "Jedno tvrdenie alebo otázka, najviac osem slov. Toto je celý prvý obrázok."),
    ("Problém", "Konkrétna situácia z ich sveta. Nie „firmy majú málo zákaziek“, ale čo sa deje v stredu o pol siedmej večer."),
    ("Otočenie", "Čo s tým. Jedna vec, nie zoznam."),
    ("Dôkaz", "Číslo, príklad alebo veta klienta. Ak dôkaz nemáš, priznaj to a použi prirovnanie."),
    ("Výzva", "Jedna a konkrétna. „Napíšte nám“ nie je výzva."),
]

TEMPLATES = [
    ("Karusel", "Obálka plus štyri až šesť strán. Jedna myšlienka na stranu, posledná strana je výzva."),
    ("Statické tvrdenie", "Veľký text na farbe, žiadny obrázok. Najrýchlejší formát, aký máš."),
    ("Číslo alebo recenzia", "Jeden údaj alebo citát klienta, veľa vzduchu okolo."),
    ("Nahľadovka reelu", "Titulok na prvom zábere. Bez nej sa reel neotvorí."),
]

DAYS = [
    ("Pondelok", "Plán a texty", [
        ("9:15 · 2 h 30", "w",
         "Obsahový plán na celý týždeň. Ku každému dňu vyber tému podľa jeho piliera, formát a jednu referenciu.",
         "Toto je blok, v ktorom sa rozhoduje. Keď je hotový, celý zvyšok týždňa už len vykonávaš."),
        ("12:30 · 2 h 15", "w",
         "Napíš texty na všetkých päť príspevkov naraz, podľa vzorca. Nič nekresli, ani nezačínaj Illustrator.",
         "Prepínanie medzi písaním a kreslením je to, čo ti žerie hodiny. Sú to dva rôzne režimy hlavy."),
        ("15:00 · 1 h 15", "h",
         "Prejdi Profesia, LinkedIn Jobs, Grafici.sk a Pretlak. Na čo sedíš, na to sa prihlás ešte dnes.",
         "Dobrý inzerát zmizne za pár dní. Nečakaj na piatok."),
    ]),
    ("Utorok", "Grafika", [
        ("9:15 · 2 h 30", "w",
         "Karusel do šablóny. Text máš hotový z pondelka, meníš len obsah rámčekov.",
         "Ak si musíš vymýšľať layout, znamená to, že šablóna chýba. Dorob ju mimo týždňa, nie teraz."),
        ("12:30 · 2 h 15", "w",
         "Dva statické príspevky a stories na zvyšok týždňa.",
         "Statický príspevok má byť hotový za dvadsať minút. Ak trvá hodinu, prerábaš šablónu."),
        ("15:00 · 1 h 15", "h",
         "LinkedIn: tri komentáre pod príspevky ľudí z brandže. Komentáre, nie lajky.",
         "Lajk nikto nevidí. Komentár ťa dostane pred ich sieť."),
    ]),
    ("Streda", "Video a učenie", [
        ("9:15 · 2 h 30", "w",
         "Reel: scenár podľa textu z pondelka, natočenie, nahratie zvuku.",
         "Reel má najväčší dosah zo všetkého, čo pre nich robíš. Jeden týždenne stačí."),
        ("12:30 · 2 h 15", "w",
         "Strih, titulky, nahľadovka, export a nahratie.",
         "Titulky nie sú voliteľné, väčšina ľudí pozerá bez zvuku."),
        ("15:00 · 1 h 15", "h",
         "Nauč sa jednu vec a zapíš si, čo to bolo. Preflight v Acrobate, CorelDRAW, Figma, After Effects.",
         "Za rok je to päťdesiat vecí. To je rozdiel medzi absolventkou a juniorkou s praxou."),
    ]),
    ("Štvrtok", "Tvoja kariéra", [
        ("9:15 · 2 h 30", "w",
         "Portfólio: dokonči jednu vlastnú vec. Nevyžiadaný návrh, chýbajúci banner, prekreslenie starej práce.",
         "Toto je jediný blok v týždni, ktorý patrí len tebe. Neposúvaj ho, aj keby horelo."),
        ("12:30 · 2 h 15", "h",
         "Prihlášky: sprievodné listy na inzeráty, ktoré si cez týždeň našla. Odsek štyri prepíš pri každom.",
         "Odseky jeden až tri sú rovnaké vždy. Štvrtý je ten, podľa ktorého poznajú, že si inzerát čítala."),
        ("15:00 · 1 h 15", "w",
         "Dokonči rozrobené príspevky a naplánuj ich do nástroja.",
         "Naplánované znamená hotové. Kým visí v priečinku, nie je."),
    ]),
    ("Piatok", "Dokončenie a poriadok", [
        ("9:15 · 2 h 30", "w",
         "Dokonči a naplánuj všetok obsah SHAPELESAI tak, aby cez víkend nebolo čo riešiť.",
         "Piatok poobede je jediný čas, keď vieš urobiť poriadok bez toho, aby ťa niečo tlačilo."),
        ("12:30 · 2 h 15", "h",
         "Blok na budúci týždeň: vyber päť mien, nájdi kontakty, napíš všetkých päť správ a ulož ako koncepty. Potom dohnaj odložené inzeráty.",
         "Predtým to bola nedeľa večer. Presunuté sem, aby si mala voľný víkend. Čas nežerie písanie, ale rozhodovanie, komu napísať."),
        ("15:00 · 1 h 15", "h",
         "Papiere pre úrad práce do jedného priečinka. Potom zápis týždňa do tabuľky: koľko odoslaných, koľko odpovedí, čo ďalej.",
         "Rob to každý piatok. Po troch mesiacoch to spätne nedáš dokopy."),
    ]),
]

SPARE = [
    ("Dopíš texty do zásoby", "Napíš tri príspevky navyše a odlož ich. O mesiac ti to zachráni týždeň, keď ochorieš alebo pôjdeš na pohovor."),
    ("Dorob chýbajúcu šablónu", "Ak si tento týždeň niečo kreslila od nuly, sprav z toho šablónu. Nabudúce to bude na dvadsať minút."),
    ("Nevyžiadaný návrh", "Vyber si firmu, do ktorej sa chceš dostať, a sprav jej jednu vec. Toto je najsilnejší ťah, aký máš."),
    ("Prejdi si vlastné portfólio ako cudzí človek", "Otvor ho na mobile, klikaj a hľadaj, čo je nejasné. Zapíš si to a oprav."),
    ("Nauč sa niečo z remesla", "CorelDRAW základy, Preflight profily, spadávky pri väzbe V1 a V2. Sú to veci, na ktoré sa ťa spýtajú na pohovore."),
    ("Priprav si odpovede na pohovor", "Napíš si, čo povieš na tri otázky: prečo my, čo je vaša najlepšia práca, čo neviete."),
    ("Choď preč od počítača", "Ak si splnila týždenné ciele, máš voľno. Nedopĺňaj hodiny prácou, ktorá nikam nevedie."),
]

REPLIES = [
    ("Odpísal milo", "Poďakuj do 24 hodín a spýtaj sa na jednu konkrétnu vec. Nepýtaj si prácu. Pýtaj si názor na portfólio alebo tip, koho ešte osloviť."),
    ("Dal ti meno", "Napíš tomu človeku do troch dní, kým je odporúčanie čerstvé, a hneď v prvej vete uveď, kto ťa posiela."),
    ("Pozval ťa na hovor", "Choď, aj keď nemajú voľné miesto. Pred hovorom si pozri tri ich posledné práce a priprav si k nim jednu otázku."),
    ("Odmietol", "Poďakuj, jedna veta. Zapíš do tabuľky a o pol roka napíš znova s novou prácou."),
    ("Ticho", "Po siedmich dňoch jeden nudge, tri riadky. Potom už nič a ideš ďalej."),
]

ONEOFFS = [
    ("Postav si päť šablón v Canve alebo Illustratore a pomenuj ich.",
     "Toto je tá jednorazovka, ktorá ti vráti najviac času. Kým ju neurobíš, každý utorok kreslíš od nuly."),
    ("Napíš si zoznam dvadsiatich tém do zásoby, štyri na každý pilier.",
     "Keď máš zásobu, pondelkový plán trvá dvadsať minút namiesto dvoch hodín."),
    ("Priprav si kostru sprievodného listu, kde meníš len štvrtý odsek.", ""),
    ("Založ si priečinok Úrad práce a v pošte štítok na prihlášky.",
     "Doklad musí vzniknúť sám pri prihlasovaní, nie spätne pred návštevou úradu."),
    ("Over si na úrade, akú presnú formu dokladu od teba chcú.", ""),
    ("Prepíš odkaz na portfólio na LinkedIne na viktoriamikuskova.com.",
     "Doména už beží, ale na profile máš starú adresu."),
    ("Vypýtaj si zo SHAPELESAI písomné odporúčanie na LinkedIn.",
     "Odporúčanie od súčasného zamestnávateľa je najsilnejšia vec, akú vie absolvent na profil dať."),
    ("Pridaj na LinkedIn reel a nové práce zo Spolku a NOOK BOOKS.", ""),
    ("Dokresli banner tušom pre Portréty psov, 1600 × 1200 px.", ""),
    ("Napíš trom bývalým učiteľom zo SOŠ polygrafickej.",
     "Ľudia, ktorí ťa poznajú, odpisujú v drvivej väčšine prípadov. Cudzí ľudia zriedka."),
]


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------
def build_md():
    o = ["# Týždenný plán — osem hodín denne", "",
         "Interaktívna verzia s odškrtávaním: `career/08-tyzdenny-plan.html`", "",
         LEDE.replace(" Odškrtávaj priamo tu, ostane to uložené v prehliadači.", ""), "",
         "## Cieľ týždňa", "", "| | |", "|---|---|"]
    o += [f"| {n} | {t} |" for n, t, _ in GOALS]

    o += ["", "## Päť pravidiel", ""]
    o += [f"{i + 1}. {r}" for i, r in enumerate(RULES)]

    o += ["", "## Rytmus dňa", "",
          "Rovnaký každý deň. Menia sa len dva hlboké bloky.", "",
          "| Čas | Blok | |", "|---|---|---|"]
    o += [f"| {t} | **{name}** | {note} |" for t, name, note in RHYTHM]

    o += ["", "## Piliere obsahu", "",
          "Každý deň má pridelenú tému. Nevymýšľaš, čo o čom písať, len vyplníš slot.", "",
          "| Deň | Pilier | Čo to je |", "|---|---|---|"]
    o += [f"| {d} | **{p}** | {w} |" for d, p, w in PILLARS]

    o += ["", "## Vzorec na text", "",
          "Päť riadkov, vždy v tomto poradí. Píšeš ich v pondelok, všetkých päť príspevkov naraz.", ""]
    o += [f"{i + 1}. **{k}** — {v}" for i, (k, v) in enumerate(COPY_STEPS)]

    o += ["", "## Štyri šablóny", "",
          "Toto sú jediné layouty, ktoré počas týždňa používaš. Nový sa nekreslí.", ""]
    o += [f"- **{k}** — {v}" for k, v in TEMPLATES]

    for day, theme, tasks in DAYS:
        o += ["", f"## {day} · {theme}", ""]
        for t, track, what, why in tasks:
            tag = "SHAPELESAI" if track == "w" else "Hľadanie práce"
            o.append(f"- **{t} · {tag}** — {what}")
            if why:
                o.append(f"  > {why}")

    o += ["", "## Sobota a nedeľa · voľno", "",
          "Ak niekto odpísal, odpíš. Inak nič.",
          "Voľný víkend je súčasť plánu, nie odmena za splnený týždeň."]

    o += ["", "## Keď ostane čas", "",
          "Zoznam je zoradený podľa toho, čo ti vráti najviac. Ber odhora.", ""]
    o += [f"- **{k}** — {v}" for k, v in SPARE]

    o += ["", "## Keď niekto odpíše", "",
          "Toto je jediná časť týždňa, ktorá má prednosť pred plánom.", ""]
    o += [f"- **{k}** — {v}" for k, v in REPLIES]

    o += ["", "## Jednorazovky", "",
          "Veci mimo týždenného kolobehu. Urob vždy jednu, keď ti vyjde čas.", ""]
    for what, why in ONEOFFS:
        o.append(f"- [ ] {what}")
        if why:
            o.append(f"  > {why}")

    with open(MD, "w", encoding="utf-8") as f:
        f.write("\n".join(o) + "\n")
    return len(o)


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------
CHECK = ('<span class="box"><svg viewBox="0 0 16 16" aria-hidden="true">'
         '<path d="M2.5 8.5l3.5 3.5 7.5-8" fill="none" stroke="#fff" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg></span>')


def e(s):
    return htmllib.escape(str(s), quote=False)


def task(tid, meta, what, why, track):
    cls = "task w" if track == "w" else "task"
    m = f'<span class="meta">{e(meta)}</span>' if meta else ""
    w = f'<span class="why">{e(why)}</span>' if why else ""
    return (f'      <li><label class="{cls}" for="{tid}"><span class="spine"></span>'
            f'<span class="body">{m}<span class="what">{e(what)}</span>{w}</span>'
            f'<input type="checkbox" id="{tid}">{CHECK}</label></li>')


def build_html():
    with open(HTML, encoding="utf-8") as f:
        old = f.read()
    head = old[:old.index('<div class="wrap">')]
    tail = old[old.rindex("<script>"):]

    o = [head, '<div class="wrap">', "",
         '  <header class="masthead">',
         '    <p class="eyebrow">Týždenný režim</p>',
         "    <h1>Čo robiť tento týždeň</h1>",
         f'    <p class="lede">{e(LEDE)}</p>',
         '    <div class="tracks">',
         '      <span class="track"><span class="dash h"></span> Hľadanie práce</span>',
         '      <span class="track"><span class="dash w"></span> SHAPELESAI</span>',
         "    </div>", "  </header>", "",
         '  <section class="goals" aria-label="Cieľ týždňa">']
    o += [f'    <div class="goal {c}"><b>{e(n)}</b><span>{e(t)}</span></div>'
          for n, t, c in GOALS]
    o += ["  </section>", "",
          '  <section class="rules">',
          "    <h2>Päť pravidiel, ktoré držia celý týždeň</h2>", "    <ol>"]
    o += [f"      <li>{e(r)}</li>" for r in RULES]
    o += ["    </ol>", "  </section>", ""]

    # rytmus dňa
    o += ['  <section class="day">',
          '    <div class="day-head"><h2>Rytmus dňa</h2>'
          '<span class="sum">rovnaký každý deň</span></div>',
          '    <ul class="tasks">']
    for i, (t, name, note) in enumerate(RHYTHM):
        o.append(task(f"r{i}", t, name, note, "h" if i in (0, 1) else "n"))
    o += ["    </ul>", "  </section>", ""]

    # piliere
    o += ['  <section class="day">',
          '    <div class="day-head"><h2>Piliere obsahu</h2>'
          '<span class="sum">nevymýšľaj témy</span></div>',
          '    <ul class="tasks">']
    for i, (d, p, w) in enumerate(PILLARS):
        o.append(task(f"p{i}", d, p, w, "w"))
    o += ["    </ul>", "  </section>", ""]

    # vzorec a šablóny
    o += ['  <section class="day">',
          '    <div class="day-head"><h2>Vzorec na text</h2>'
          '<span class="sum">päť riadkov</span></div>',
          '    <ul class="tasks">']
    for i, (k, v) in enumerate(COPY_STEPS):
        o.append(task(f"c{i}", f"{i + 1}", k, v, "w"))
    o += ["    </ul>", "  </section>", "",
          '  <section class="day">',
          '    <div class="day-head"><h2>Štyri šablóny</h2>'
          '<span class="sum">nový layout nekresli</span></div>',
          '    <ul class="tasks">']
    for i, (k, v) in enumerate(TEMPLATES):
        o.append(task(f"s{i}", "", k, v, "w"))
    o += ["    </ul>", "  </section>", ""]

    # dni
    for di, (day, theme, tasks) in enumerate(DAYS):
        o += ['  <section class="day">',
              f'    <div class="day-head"><h2>{e(day)}</h2>'
              f'<span class="sum">{e(theme)}</span></div>',
              '    <ul class="tasks">']
        for ti, (t, track, what, why) in enumerate(tasks):
            o.append(task(f"d{di}t{ti}", t, what, why, track))
        o += ["    </ul>", "  </section>", ""]

    o += ['  <section class="day">',
          '    <div class="day-head"><h2>Sobota a nedeľa</h2>'
          '<span class="sum">voľno</span></div>',
          '    <ul class="tasks">',
          task("we0", "podľa potreby", "Ak niekto odpísal, odpíš. Inak nič.",
               "Voľný víkend je súčasť plánu, nie odmena za splnený týždeň.", "h"),
          "    </ul>", "  </section>", ""]

    o += ['  <section class="day">',
          '    <div class="day-head"><h2>Keď ostane čas</h2>'
          '<span class="sum">ber odhora</span></div>',
          '    <ul class="tasks">']
    for i, (k, v) in enumerate(SPARE):
        o.append(task(f"x{i}", "", k, v, "w" if i < 3 else "h"))
    o += ["    </ul>", "  </section>", ""]

    o += ['  <section class="day">',
          '    <div class="day-head"><h2>Keď niekto odpíše</h2>'
          '<span class="sum">má prednosť pred plánom</span></div>',
          '    <ul class="tasks">']
    for i, (k, v) in enumerate(REPLIES):
        o.append(task(f"a{i}", k, v, "", "h"))
    o += ["    </ul>", "  </section>", ""]

    o += ['  <section class="day">',
          '    <div class="day-head"><h2>Jednorazovky</h2>'
          '<span class="sum">mimo týždňa</span></div>',
          '    <ul class="tasks">']
    for i, (what, why) in enumerate(ONEOFFS):
        o.append(task(f"o{i}", "", what, why, "h"))
    o += ["    </ul>", "  </section>", "",
          '  <div class="foot">',
          "    <p>Odškrtnuté položky sa ukladajú v tomto prehliadači.</p>",
          '    <button class="reset" type="button" id="reset">Vynulovať týždeň</button>',
          "  </div>", "", "</div>", "", tail]

    with open(HTML, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    return len("\n".join(o))


if __name__ == "__main__":
    n = build_md()
    k = build_html()
    print(f"  08-tyzdenny-plan.md — {n} riadkov")
    print(f"  08-tyzdenny-plan.html — {round(k / 1024)} kB")
