#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor prípravy na pohovor.

    python3 career/make_pohovor.py

Vytvorí career/09-pohovor-high5.html — jednu stránku na čítanie v mobile
pred pohovorom. Vložené fonty si berie z týždenného plánu, aby sa nemuseli
vkladať znova a aby dokumenty vyzerali rovnako.
"""

import html as htmllib
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_FONTS = os.path.join(ROOT, "08-tyzdenny-plan.html")
OUT = os.path.join(ROOT, "09-pohovor-high5.html")


def e(s):
    return htmllib.escape(str(s), quote=False)


def fonts():
    with open(SRC_FONTS, encoding="utf-8") as f:
        return "\n".join(re.findall(r"@font-face\{[^}]*\}", f.read()))


# ---------------------------------------------------------------------------
# Obsah
# ---------------------------------------------------------------------------

FIRMA = [
    ("2016", "Vznikli ako High 5 studio. Prvého interného kolegu a kanceláriu mali až v roku 2018."),
    ("2021", "Zdvojnásobili mesačný rozpočet v Google Ads na 100 000 €."),
    ("2023", "Tím narástol na dvojciferné číslo a presťahovali sa do väčších kancelárií."),
    ("2024", "Zaviedli AI do svojich procesov. Je to posledná vec, ktorou sa na webe chvália."),
    ("Dnes", "Štrnásť ľudí, Trenčianska 53 pri Štrkovci. Fullservis: výkonnostný marketing, branding, sociálne siete, weby a eshopy, video."),
]

KLIENTI = ("Česká mincovňa, Julius Meinl, Land Rover Bratislava, Securitas, "
           "Institut Français, Carnomed, Stella Car, Papa Grill, Green Bike, "
           "Coller Klíma, Bellmedi, Dual BP, ImageWell.")

PORTFOLIO_ICH = [
    ("Energiaweb", "logo a logomanuál"),
    ("Coffee lovers", "etikety na produkty"),
    ("Jaguar", "bannery do Google reklamy"),
]

PRACE = [
    ("Spolok košických študentov farmácie",
     "Redizajn loga a vizuálna identita, 2024. Druhé miesto v súťaži.",
     "Toto je tvoja hlavná zbraň. Je to jediná práca, kde máš celý cyklus: zadanie, "
     "redizajn loga, farebné aj čiernobiele varianty, aplikácie na tlačoviny "
     "a na sociálne siete. A má vonkajšie ocenenie, ktoré si nedala ty sama.",
     "Prečo som logo zjednodušila a čo to spravilo s použiteľnosťou v malých veľkostiach."),
    ("SHAPELESAI",
     "Sociálne siete od konceptu po výstup vrátane copy, od 2025.",
     "Toto je jediná práca, ktorá je najbližšie k tomu, čo budeš robiť u nich. "
     "Karusely, statické príspevky, reely. Jedno reelsko má cez desaťtisíc zhliadnutí.",
     "Ako som z predajného argumentu firmy spravila vzdelávací obsah a prečo formát "
     "mýtus a realita funguje lepšie než priama ponuka."),
    ("NOOK BOOKS",
     "Vizuálna identita a kompletný dizajn manuál, bakalárska práca, 2024.",
     "V inzeráte majú systémové myslenie ako plus. Dizajn manuál je presne to. "
     "Ochranná zóna, sieťová konštrukcia, farebné profily RGB, CMYK aj HEX, "
     "minimálne rozmery, zakázané verzie.",
     "Prečo som robila manuál a nie len logo: aby značka prežila aj vtedy, "
     "keď ju bude používať niekto iný."),
    ("Orientačný systém PEVŠ",
     "Informačný dizajn, 2023 až 2024. Vyrobené a osadené v areáli.",
     "Jediná práca, ktorá fyzicky existuje vo svete. Znamená to, že tvoj návrh "
     "prešiel od nápadu cez schvaľovanie až do výroby, a to je vec, ktorú "
     "väčšina uchádzačov na tvojej úrovni nemá.",
     "Čo som musela zmeniť medzi návrhom a výrobou a prečo."),
    ("Telekom",
     "Grafika notifikácie, koncept, 2024.",
     "Tri varianty jedného zadania: zotierací žreb, ruka s mincou, SIM karta "
     "ako darček. Toto je dôkaz konceptového myslenia, ktoré v inzeráte žiadajú.",
     "Ako som z jedného zadania spravila tri smery a podľa čoho by som vybrala jeden."),
]

OTAZKY = [
    ("Povedzte nám niečo o sebe.",
     "Deväťdesiat sekúnd, nie životopis. Tri vety: odkiaľ prichádzaš, čo robíš teraz, "
     "prečo si tu.",
     "Som grafická dizajnérka s polygrafickým vzdelaním. Začínala som na SOŠ polygrafickej "
     "v odbore grafik digitálnych médií, potom som vyštudovala Dizajn médií a magisterské "
     "štúdium masmediálnej komunikácie na Paneurópskej vysokej škole. Rok som robila grafiku "
     "a produktovú fotografiu pre MOJESIDLO, teraz robím obsah a vizuály pre SHAPELESAI, "
     "kde mám sociálne siete od konceptu po výstup. Hlásim sa k vám, lebo chcem robiť tam, "
     "kde projekt prejde od konceptu cez kampaň až po print, a nie robiť stále jeden výsek."),
    ("Nemáte tri roky v agentúre. Ako to vidíte?",
     "Toto príde a nesmie ťa to prekvapiť. Nepriznávaj sa k nej ako k previneniu "
     "a neospravedlňuj sa. Pomenuj ju rovno a hneď otoč na to, čo máš namiesto rokov.",
     "Nemám. Mám rok a pol praxe a ani jedna z nich nebola agentúra, to je pravda. "
     "Čo mám namiesto toho, je šírka: viem pripraviť podklady do tlače bez chyby, "
     "viem odfotiť produkt, viem zostrihať reel a viem napísať text k príspevku. "
     "V štrnásťčlennom tíme to znamená, že na jednu vec nepotrebujete troch ľudí. "
     "A viem, že tempo v agentúre je iné než to, na čo som zvyknutá, s tým počítam."),
    ("Prečo agentúra a nie interná pozícia?",
     "Chcú vedieť, či rozumieš, do čoho ideš. Agentúra znamená veľa klientov, "
     "krátke termíny a striedanie štýlov.",
     "Lebo sa chcem naučiť pracovať v cudzích značkách, nie len v jednej. "
     "V agentúre za rok prejdem cez viac zadaní než inhouse za tri. "
     "A baví ma, keď musím vojsť do štýlu, ktorý nie je môj."),
    ("Weby a landing pages sú v náplni práce. Robili ste ich?",
     "Neblafuj. Toto je vec, ktorú si nerobila, a keď to zaklameš, vypadne to "
     "pri prvom zadaní.",
     "Ostré weby som zatiaľ nerobila. Pracujem vo Figme a rozumiem tomu, ako sa "
     "návrh odovzdáva vývojárovi. Je to vec, ktorú sa chcem naučiť, a preto ma "
     "táto pozícia zaujíma, lebo máte interne aj druhého dizajnéra a je od koho."),
    ("Ako reagujete, keď klient zamietne návrh?",
     "Testujú, či nie si na svojich návrhoch citlivo naviazaná. V agentúre sa "
     "zamieta stále.",
     "Pýtam sa, čo konkrétne nesedí, lebo „nepáči sa mi to“ sa nedá opraviť. "
     "Keď viem dôvod, viem urobiť druhú verziu. Návrh nie je moje dieťa, "
     "je to riešenie zadania, a keď zadanie nerieši, tak je zlé."),
    ("Ako pracujete, keď máte tri veci naraz a všetky sú súrne?",
     "Chcú počuť systém, nie ochotu.",
     "Spýtam sa, ktorá má reálny termín a ktorá len pocit. Potom si veci zoradím "
     "podľa toho, čo blokuje niekoho iného. Keď viem, že to nestihnem, poviem to dopredu, "
     "nie v deň termínu."),
    ("Ako sa vám pracuje s copywriterom?",
     "Majú to v náplni práce ako samostatný bod, takže na to dajú.",
     "V SHAPELESAI si copy píšem sama, takže viem, ako sa text a vizuál navzájom "
     "ťahajú. Radšej dostanem text skôr než neskôr, lebo dizajn, ktorý sa robí "
     "okolo hotového textu, drží lepšie než text natlačený do hotového rámčeka."),
    ("Ktorá vaša práca je najlepšia a prečo?",
     "Nikdy nehovor „všetky sú dobré“. Vyber jednu a povedz dôvod, ktorý nie je estetický.",
     "Orientačný systém pre Paneurópsku vysokú školu. Nie preto, že by bol "
     "graficky najkrajší, ale preto, že je jediný, ktorý naozaj vyrobili a osadili. "
     "Musela som ho prekresliť podľa toho, čo šlo vyrobiť, a to ma naučilo viac "
     "než päť školských zadaní."),
    ("Aké sú vaše slabé stránky?",
     "Nikdy nehovor prezlečenú prednosť typu „som perfekcionistka“. Povedz "
     "skutočnú vec a k nej to, čo s ňou robíš.",
     "Dlho mi trvá prvý návrh, lebo skúšam priveľa smerov naraz. Pomohlo mi robiť "
     "si šablóny a rozdeliť si text a grafiku do dvoch dní, aby som neprepínala. "
     "Odvtedy je to výrazne rýchlejšie."),
    ("Kde sa vidíte o dva roky?",
     "Nehovor, že chceš mať vlastné štúdio. Sedíš u niekoho, kto ťa má prijať.",
     "Chcem vedieť samostatne odviesť celú kampaň pre klienta, od konceptu po výstupy, "
     "a rozumieť aj tomu, čo sa po nej stane s číslami. Preto ma zaujíma agentúra, "
     "kde je aj výkonnostná časť, nie len grafika."),
]

MOJE_OTAZKY = [
    ("Máte interne dvoch dizajnérov. Ako máte medzi sebou rozdelenú prácu, "
     "podľa klientov alebo podľa typu výstupu?",
     "Je to v ich inzeráte a hneď sa dozvieš, či budeš robiť všetko, alebo len jednu vrstvu."),
    ("Píšete, že ste v roku 2024 zaviedli AI do procesov. Kde konkrétne "
     "ju používate v grafike?",
     "Toto je posledná vec, ktorou sa na webe chvália, takže o nej radi hovoria. "
     "A ukazuje, že si čítala ich stránku, nie len inzerát."),
    ("Ako u vás vyzerá cesta zadania od klienta k hotovému vizuálu? "
     "Kto píše brief a koľko kôl korektúr je bežných?",
     "Odpoveď ti povie, či majú proces, alebo či sa to rieši za pochodu."),
    ("Čo by mal človek na tejto pozícii zvládnuť do troch mesiacov, "
     "aby ste povedali, že to vyšlo?",
     "Najsilnejšia otázka z celého zoznamu. Dostaneš z nej ich skutočné očakávania "
     "a zároveň to znie, že už premýšľaš ako ich človek."),
    ("Print máte v náplni ako príležitostný. Robíte si prípravu do tlače interne, "
     "alebo to dávate tlačiarni?",
     "Toto je otázka, ktorou ukážeš, že máš polygrafiu. A ak to riešia externe, "
     "práve si im ponúkla vec, ktorú nemajú."),
]

CERVENE = [
    ("Nehovor „len“ a „vlastne“.",
     "Podkopávajú všetko, čo je za nimi. „Robila som vlastne len sociálne siete“ "
     "je to isté ako povedať, že to nestojí za reč."),
    ("Neospravedlňuj sa za to, že si čerstvá absolventka.",
     "Vedeli to z tvojho životopisu a pozvali ťa. To rozhodnutie už padlo."),
    ("Nekritizuj nikoho.",
     "Ani predchádzajúceho zamestnávateľa, ani školu, ani prácu, ktorú vidíš na stene. "
     "Kto kritizuje minulého zamestnávateľa, o budúcom bude hovoriť rovnako."),
    ("Nehovor „to by som musela zistiť“ a stop.",
     "Povedz radšej, ako by si to zistila. Rozdiel je medzi bezradnosťou a postupom."),
    ("Nepýtaj sa na plat ako na prvé.",
     "Nechaj to na nich alebo na koniec. Keď sa spýtajú oni, odpovedz."),
]

PLAT = [
    ("Číslo si urči doma, nie tam.",
     "Rozhodni sa dopredu, pod čo nejdeš, a to číslo si zapíš. V miestnosti sa to "
     "nedá rozmýšľať."),
    ("1 800 € na faktúru nie je to isté ako 1 800 € v pracovnom pomere.",
     "Na faktúru si odvody platíš sama. V prvom roku neplatíš sociálne, takže "
     "na účte to vyzerá dobre, ale od druhého roka ti pribudnú a je to citeľné. "
     "Počítaj s tým, keď porovnávaš s ponukou na trvalý pracovný pomer."),
    ("Ak sa spýtajú, čo si predstavuješ, daj rozpätie a odôvodni ho.",
     "„Vzhľadom na to, že je to na faktúru a odvody idú za mnou, predstavujem si "
     "rozpätie od X do Y. Ak by to bolo na trvalý pracovný pomer, viem ísť nižšie.“"),
    ("Spýtaj sa, či je 1 800 € nástupné alebo strop pre túto pozíciu.",
     "Je to legitímna otázka a odpoveď ti povie viac než samotné číslo."),
]

PRAKTICKE = [
    ("Portfólio si vezmi na notebooku aj vytlačené.",
     "PDF máš na viktoriamikuskova.com/dokumenty.html. Vytlač si ho na dvadsaťjeden "
     "strán A4 na šírku. Na stole vedľa seba pôsobí inak než na obrazovke a pri "
     "grafickej pozícii je to samo o sebe ukážka práce."),
    ("Wifi nepredpokladaj.",
     "Maj PDF stiahnuté v notebooku, nie len odkaz na web."),
    ("Príď o desať minút skôr, nie o pol hodiny.",
     "Trenčianska 53, blízko Štrkovca. Prejdi si cestu deň vopred."),
    ("Zápisník a pero na stôl.",
     "Otvorený zápisník hovorí, že očakávaš, že sa dozvieš niečo dôležité. "
     "A budeš si mať kam zapísať mená a to, čo od teba chcú."),
    ("Oblečenie: čisté a jednoduché.",
     "Marketingová agentúra nie je banka. Nechoď v kostýme, ale ani v tepláckej "
     "súprave. Ty si grafička, oblečenie je prvý vizuál, ktorý uvidia."),
    ("Do 24 hodín poďakuj mailom.",
     "Tri vety. Poďakuj, spomeň jednu konkrétnu vec z rozhovoru a priloží odkaz "
     "na portfólio. Väčšina uchádzačov to neurobí."),
]


# ---------------------------------------------------------------------------
# Stránka
# ---------------------------------------------------------------------------
CSS = """
:root{
  --paper:#FBEFE3;
  --card:#FFF8EF;
  --ink:#241B12;
  --muted:#6B5F51;
  --accent:#C6673D;
  --olive:#676340;
  --rule:rgba(120,105,90,.20);
  --rule2:rgba(120,105,90,.36);
  --serif:"Playfair Display",Georgia,serif;
  --sans:"Montserrat","Segoe UI",Helvetica,Arial,sans-serif;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#16120F;
    --card:#1F1913;
    --ink:#F1E7DA;
    --muted:#A2958A;
    --accent:#E48B5C;
    --olive:#AFA97A;
    --rule:rgba(215,196,172,.16);
    --rule2:rgba(215,196,172,.30);
  }
}
:root[data-theme="dark"]{
  --paper:#16120F;
  --card:#1F1913;
  --ink:#F1E7DA;
  --muted:#A2958A;
  --accent:#E48B5C;
  --olive:#AFA97A;
  --rule:rgba(215,196,172,.16);
  --rule2:rgba(215,196,172,.30);
}
*{box-sizing:border-box;}
body{
  margin:0;
  background:var(--paper);
  color:var(--ink);
  font-family:var(--sans);
  font-size:16px;
  line-height:1.62;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:44rem;margin:0 auto;padding:44px 22px 80px;display:flex;flex-direction:column;gap:40px;}

.masthead{display:flex;flex-direction:column;gap:12px;}
.eyebrow{
  margin:0;font-size:11px;font-weight:600;letter-spacing:.20em;
  text-transform:uppercase;color:var(--accent);
}
h1{
  margin:0;font-family:var(--serif);font-weight:500;
  font-size:clamp(30px,7vw,44px);line-height:1.08;text-wrap:balance;
}
.lede{margin:0;color:var(--muted);font-size:15px;}

.sect{display:flex;flex-direction:column;gap:18px;}
.sect > h2{
  margin:0;padding-top:22px;border-top:1px solid var(--rule2);
  font-size:11px;font-weight:600;letter-spacing:.20em;
  text-transform:uppercase;color:var(--muted);
}
.intro{margin:0;color:var(--muted);font-size:14.5px;}

/* fakty o firme */
.facts{display:flex;flex-direction:column;gap:0;margin:0;}
.facts div{
  display:grid;grid-template-columns:5.2rem 1fr;gap:14px;
  padding:11px 0;border-top:1px solid var(--rule);
}
.facts div:first-child{border-top:0;}
.facts dt{
  margin:0;font-size:12px;font-weight:600;letter-spacing:.06em;
  color:var(--accent);font-variant-numeric:tabular-nums;
}
.facts dd{margin:0;font-size:14.5px;}

/* práca alebo otázka */
.item{
  background:var(--card);border:1px solid var(--rule);border-radius:10px;
  padding:20px 20px 22px;display:flex;flex-direction:column;gap:11px;
}
.item h3{
  margin:0;font-family:var(--serif);font-weight:500;
  font-size:20px;line-height:1.24;text-wrap:balance;
}
.tag{
  margin:0;font-size:11.5px;font-weight:600;letter-spacing:.10em;
  text-transform:uppercase;color:var(--olive);
}
.note{margin:0;font-size:14.5px;color:var(--muted);}
/* Čo naozaj povieš, je odlíšené od toho, čo máš len vedieť. */
.say{
  margin:0;padding:13px 0 13px 16px;border-left:3px solid var(--accent);
  font-size:15.5px;line-height:1.7;
}
.say::before{
  content:"Povedz";display:block;margin-bottom:5px;
  font-size:10.5px;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:var(--accent);
}
.ask::before{content:"Spýtaj sa";}
.angle::before{content:"O čom hovor";}

/* jednoduchý zoznam s dôvodom */
.rows{display:flex;flex-direction:column;gap:0;margin:0;padding:0;list-style:none;}
.rows li{padding:14px 0;border-top:1px solid var(--rule);}
.rows li:first-child{border-top:0;}
.rows b{display:block;font-weight:600;font-size:15px;margin-bottom:3px;}
.rows span{font-size:14px;color:var(--muted);}

.pill{
  display:inline-block;padding:3px 10px;border-radius:999px;
  background:var(--accent);color:var(--paper);
  font-size:11px;font-weight:600;letter-spacing:.10em;text-transform:uppercase;
}
.foot{
  padding-top:22px;border-top:1px solid var(--rule2);
  font-size:13px;color:var(--muted);
}
a{color:var(--accent);}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;}
@media (max-width:420px){
  .facts div{grid-template-columns:1fr;gap:2px;}
}
"""


def build():
    def item(title, tag, note, say, say_cls="say"):
        t = f'<p class="tag">{e(tag)}</p>' if tag else ""
        n = f'<p class="note">{e(note)}</p>' if note else ""
        s = f'<p class="{say_cls}">{e(say)}</p>' if say else ""
        return (f'<div class="item"><h3>{e(title)}</h3>{t}{n}{s}</div>')

    o = [f"<title>Pohovor High5 — príprava</title>", "<style>", fonts(), CSS, "</style>",
         '<div class="wrap">',
         '<header class="masthead">',
         '<p class="eyebrow">Príprava na pohovor</p>',
         "<h1>High5, Mid až Senior Graphic Designer</h1>",
         '<p class="lede">Čítaj to ráno pred pohovorom. Odpovede sa neuč naspamäť, '
         'uč sa ich kostru. Naspamäť naučená veta je počuť.</p>',
         "</header>"]

    o += ['<section class="sect"><h2>Čo o nich vieš</h2>',
          '<p class="intro">Toto je tvoja najväčšia výhoda. Väčšina uchádzačov si '
          'prečíta inzerát a nič viac.</p>',
          '<dl class="facts">']
    o += [f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in FIRMA]
    o += ["</dl>",
          f'<p class="note"><b>Klienti, ktorých uvádzajú:</b> {e(KLIENTI)}</p>',
          '<p class="note"><b>Z grafiky ukazujú v portfóliu:</b> '
          + e(", ".join(f"{a} ({b})" for a, b in PORTFOLIO_ICH)) + '.</p>',
          "</section>"]

    o += ['<section class="sect"><h2>Päť prác a čo pri nich povedať</h2>',
          '<p class="intro">Neopisuj, ako to vyzerá. To vidia. Hovor o rozhodnutí, '
          'ktoré si urobila, a prečo. Toto je jediná vec, ktorá odlíši teba od '
          'ďalších desiatich portfólií.</p>']
    o += [item(t, tag, why, say, "say angle") for t, tag, why, say in PRACE]
    o += ["</section>"]

    o += ['<section class="sect"><h2>Otázky, ktoré prídu</h2>']
    o += [item(q, None, why, say) for q, why, say in OTAZKY]
    o += ["</section>"]

    o += ['<section class="sect"><h2>Čo sa spýtaš ty</h2>',
          '<p class="intro">Vyber si tri. Kto sa nespýta nič, vyzerá, že mu na tom '
          'nezáleží.</p>']
    o += [item(q, None, why, q, "say ask") for q, why in MOJE_OTAZKY]
    o += ["</section>"]

    o += ['<section class="sect"><h2>Čo nehovor</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in CERVENE]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Plat</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in PLAT]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Praktické</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in PRAKTICKE]
    o += ["</ul></section>"]

    o += ['<p class="foot">Jedna veta na záver: pozvali ťa, hoci z tvojho životopisu '
          'vedeli, že tri roky v agentúre nemáš. To znamená, že rozhodlo portfólio. '
          'Choď tam ako človek, ktorý má čo ukázať, nie ako niekto, kto prosí.</p>',
          "</div>"]

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    return os.path.getsize(OUT)


if __name__ == "__main__":
    n = build()
    print(f"  09-pohovor-high5.html — {round(n / 1024)} kB")
