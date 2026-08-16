#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Príprava na pohovor v Slovenskej národnej galérii.

    python3 career/make_pohovor_sng.py

Vytvorí career/10-pohovor-sng.html. Vzhľad aj vložené fonty si berie
z prípravy na High5, aby dokumenty vyzerali rovnako a fonty sa nevkladali
druhýkrát.
"""

import importlib.util
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "10-pohovor-sng.html")

_spec = importlib.util.spec_from_file_location(
    "high5", os.path.join(ROOT, "make_pohovor.py"))
_h5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_h5)
e, fonts, CSS = _h5.e, _h5.fonts, _h5.CSS


# ---------------------------------------------------------------------------
# Obsah
# ---------------------------------------------------------------------------

KEDY = [
    ("Kedy", "Pondelok 17. augusta 2026 o 11:00. Buď tam o 10:50, nie skôr a nie neskôr."),
    ("Kde", "Administratívna budova SNG, Riečna 1, Bratislava."),
    ("S kým", "Alexandra Pilo, HR manažérka. Prvé kolo teda nebude o technike, "
              "ale o tebe, o motivácii a o plate."),
    ("Kontakt", "Marta Kapustová, asistentka, 0914 168 132, marta.kapustova@sng.sk. "
                "Vytoč ju, len ak meškáš alebo blúdiš."),
    ("Plat v inzeráte", "1 400 až 1 600 € v hrubom, podľa zákona o odmeňovaní "
                        "vo verejnom záujme."),
]

GALERIA = [
    ("1948", "Vznikla zákonom Slovenskej národnej rady, z podnetu Laca Novomeského."),
    ("90 000", "Zhruba toľko diel má v zbierkach, od stredoveku po súčasnosť."),
    ("Budovy", "Vodné kasárne z rokov 1759 až 1763, Esterházyho palác a Dedečkovo "
               "premostenie, ktoré je dnes ikonou slovenskej modernej architektúry."),
    ("2022", "Znovuotvorenie po sedemročnej rekonštrukcii."),
    ("Regióny", "Zvolenský zámok, Kaštieľ Strážky, Schaubmarov mlyn v Pezinku "
                "a Galéria Ľudovíta Fullu v Ružomberku."),
    ("Vedenie", "Generálny riaditeľ Mgr. art. Juraj Králik, vo funkcii od apríla 2025. "
                "Umelecký riaditeľ a hlavný kurátor zbierok Martin Dostál."),
]

IDENTITA = (
    "Vizuálnu identitu SNG navrhla Pavlína Morháčová s Branislavom Matisom a v roku "
    "2016 za ňu dostali Národnú cenu za komunikačný dizajn. Podstatné je, ako "
    "vznikala: obaja sú zamestnancami galérie, nie externé štúdio. Sami to opísali "
    "tak, že to nie je jednorazový manuál, ale postupný vývoj, a že rozsah ide "
    "od pozvánok cez evakuačné plány až po kampane a katalógy."
)

IDENTITA_PRECO = (
    "Prečítaj si tú vetu ešte raz. Evakuačné plány a pozvánky v jednom dychu "
    "s kampaňami, to je presne tvoj inzerát. Keď to spomenieš, budeš jediná "
    "uchádzačka, ktorá vie, ako u nich grafika naozaj funguje."
)

VYSTAVY = [
    ("Galanda a galandovci · toto je tvoja voľba",
     "12. decembra 2025 až 6. septembra 2026. Kurátori Martin Dostál a Martin "
     "Vančo. Mikuláš Galanda a Skupina Mikuláša Galandu, ktorá vznikla na prvej "
     "spoločnej výstave v decembri 1957 v Žiline. Krivoš, Barčík, Štubňa, Laluha."),
    ("Jiří Kolář a Ladislav Novák: Pocta muchám pavúkom rybám myšiam a psom",
     "26. marca až 30. augusta 2026. Končí o dva týždne."),
    ("Adam Szentpétery: Network", "29. mája až 25. októbra 2026."),
    ("Bang?! Bang! 2",
     "30. apríla až 15. novembra 2026. Táto sa ako obľúbená nehodí, pozri "
     "poznámku nižšie."),
]

GALANDA = (
    "Mikuláš Galanda, 1895 až 1938, je jeden zo zakladateľov slovenskej výtvarnej "
    "moderny. Pre teba je dôležité niečo iné než maľba: v rokoch 1924 až 1926 bol "
    "prvým grafickým redaktorom avantgardného časopisu DAV, s Ľudovítom Fullom "
    "vydával Súkromné listy Fullu a Galandu, ktorých prvé číslo vyšlo 28. februára "
    "1930, a napísali spolu Manifest slovenskej výtvarnej moderny. Knižnej grafike "
    "a ilustrácii sa venoval celý život a práve za ňu dostal za svojho života "
    "najväčšie uznanie: v roku 1933 krajinskú cenu za knižnú grafiku a na Svetovej "
    "výstave v Paríži v roku 1937 striebornú medailu."
)

GALANDA_POVEDZ = (
    "Galanda bol v podstate grafický dizajnér. Robil grafickú redakciu časopisu, "
    "sám si s Fullom vydával a sádzal manifest a navrhoval obálky a ilustrácie "
    "pre básnikov. A za svojho života ho ocenili práve za knižnú grafiku, nie za "
    "maľbu. Preto ma tá výstava zaujíma z môjho konca, nie len ako diváčku."
)

BANG = (
    "Bang?! Bang! 2 je pokračovanie výstavy, ktorá vyvolala verejný spor. Pri "
    "prvej časti viacerí vystavení umelci žiadali stiahnutie svojich diel a "
    "tvrdili, že ich nikto neoslovil. Kurátormi série sú generálny a umelecký "
    "riaditeľ. Nevyberaj si ju ako obľúbenú a sama tú tému neotváraj. Ak ju "
    "otvoria oni, povedz, že si o tom čítala, ale nemáš dosť informácií, aby si "
    "to hodnotila, a vráť sa k dielam."
)

ZHODY = [
    ("Orientačný systém pre Paneurópsku vysokú školu",
     "Informačný dizajn, 2023 až 2024, realizované",
     "V inzeráte doslova stojí „grafické riešenia pre informačné a navigačné systémy "
     "vo výstavných aj administratívnych priestoroch“. Ty máš navigačný systém, "
     "ktorý je vyrobený a visí v areáli školy. Ani jeden iný uchádzač na juniorskú "
     "pozíciu to mať nebude.",
     "Riešila som to tak, aby šípky fungovali z oboch smerov chodby, lebo človek "
     "prichádza z dvoch strán a mapa musí sedieť obom. To bolo ťažšie než samotná "
     "kresba a naučilo ma to, že navigácia sa nekreslí, ale testuje."),
    ("Stredná odborná škola polygrafická",
     "Grafik digitálnych médií, 2017 až 2021",
     "Požiadavky menujú predtlačovú prípravu, sadzbu, typografiu, CMYK a RGB "
     "a export podkladov pre tlač. To nie je pre teba nová téma, to je tvoja "
     "stredná škola. Toto je dôvod, prečo ťa pozvali.",
     "Spadávky, orezové značky, farebné profily a kontrolu pred odovzdaním "
     "beriem ako samozrejmosť, nie ako vec, ktorú riešim až keď sa niečo vráti "
     "z tlačiarne."),
    ("Alica v krajine zázrakov a NOOK BOOKS",
     "Sadzba, ilustrácia a dizajn manuál",
     "Bulletiny, sprievodcovia a katalógy sú dlhé dokumenty. Päť kompletných "
     "knižných prebalov a dizajn manuál sú dôkaz, že InDesign nie je len "
     "položka v životopise.",
     "Pri piatich prebaloch tej istej knihy v rôznych žánrových rámcoch som sa "
     "naučila držať jeden systém a meniť v ňom len to, čo sa meniť má. To je "
     "presne to, čo potrebuje inštitúcia s jednou identitou a desiatkami výstav."),
]

OTAZKY = [
    ("Povedzte nám niečo o sebe.",
     "Prvá otázka a jediná, ktorú vieš na sto percent dopredu. Maximálne "
     "deväťdesiat sekúnd, tri body: odkiaľ prichádzaš, čo robíš teraz, prečo "
     "ste tu dnes.",
     "Grafike sa venujem od strednej polygrafickej, potom som vyštudovala dizajn "
     "médií a magisterské štúdium masmediálnej a marketingovej komunikácie. "
     "Teraz robím obsah a vizuály pre ShapelesAi, predtým som bola v MOJESIDLO.SK. "
     "Hľadám miesto, kde bude príprava tlačovín a sadzba hlavná náplň, a preto "
     "som tu."),
    ("Prečo galéria a prečo kultúra?",
     "Toto je hlavná otázka celého pohovoru. „Lebo mám rada umenie“ je odpoveď, "
     "ktorú počujú od každého. Odpoveď musí byť o práci, nie o vkuse.",
     "Lákajú ma zadania, ktoré niekto naozaj drží v ruke a chodí okolo nich. "
     "Tlačoviny k výstavám, sprievodcovia, tabule v priestore. Vo firemnej grafike "
     "väčšina vecí skončí na obrazovke, tu má veľká časť výstupov fyzickú podobu "
     "a to je práca, ktorú viem robiť poriadne."),
    ("Prečo sa hlásite na juniorskú pozíciu, keď máte magisterský titul?",
     "Padne to, lebo to vyzerá ako nesúlad. Neospravedlňuj sa a nehovor, "
     "že berieš hocičo.",
     "Titul mám z komunikácie, nie z grafiky, tú mám z priemyslovky a z praxe. "
     "Chcem sa dostať do inštitúcie, kde sa robí veľa tlačovín, a naučiť sa to "
     "tam poriadne. Juniorská pozícia je na to správne miesto."),
    ("Opíšte, ako pripravujete súbor do tlače.",
     "Ak príde technická otázka, príde táto. Odpovedz procesom, nie zoznamom "
     "programov. Toto je tvoja domáca pôda.",
     "Sadzba v InDesigne, spadávky podľa toho, čo chce tlačiareň, obrázky v CMYK "
     "s profilom, ktorý si od nich vypýtam, texty do kriviek alebo vložené fonty, "
     "kontrola preflightom a nakoniec export do PDF/X. Pred odovzdaním si vždy "
     "prejdem náhľad po stranách, lebo tam sa nájde to, čo preflight neukáže."),
    ("Ako pracujete s cudzou vizuálnou identitou, keď máte vlastný názor?",
     "Kľúčová otázka práve tu. SNG má silnú identitu, ktorú robia interne roky. "
     "Hľadajú človeka, ktorý ju bude držať, nie prekresľovať.",
     "Beriem to ako pravidlá hry. Najprv chcem vedieť, prečo je niečo tak, ako "
     "je, lebo v identite, ktorá vzniká roky, býva za každým pravidlom dôvod. "
     "Ak by som mala návrh na zmenu, poviem ho, ale až keď tomu systému rozumiem, "
     "nie na tretí deň."),
    ("Ako zvládate viac zadaní naraz a termíny?",
     "Inzerát to menuje dvakrát. Odpovedz konkrétne, nie „som organizovaná“.",
     "V ShapelesAi robím celý týždenný obsah dopredu, takže mám natrénované "
     "plánovať na týždeň a nie na deň. Pri viacerých zadaniach sa pýtam na "
     "termín tlače, nie na termín odovzdania grafiky. Podľa toho sa dá počítať "
     "spätne a hneď je vidieť, čo je naozaj súrne."),
    ("Čo je vaša slabá stránka?",
     "Nehovor „som perfekcionistka“. Povedz skutočnú vec, ktorá nie je pre "
     "túto prácu smrteľná, a hneď k nej to, čo s ňou robíš.",
     "Motion. Reely strihám bežne, ale animácia nie je to, v čom som najsilnejšia. "
     "Beriem si na to čas mimo práce, lebo viem, že sa to bude čoraz viac pýtať."),
    ("Aké sú vaše platové očakávania?",
     "Nepovedz číslo ako prvá vec. Najprv ukáž, že vieš, ako sa plat "
     "vo verejnej správe tvorí. Tým sa rozhovor posunie na osobné ohodnotenie, "
     "čo je jediná časť, o ktorej sa dá hovoriť.",
     "Viem, že tarifa je daná zákonom podľa platovej triedy a započítanej praxe "
     "a že pohyblivá je časť v osobnom ohodnotení. V inzeráte je rozpätie "
     "1 400 až 1 600 eur a ja by som sa rada bavila o hornej polovici. Mám "
     "magisterský titul, polygrafickú strednú a takmer dva roky praxe, "
     "z toho realizovaný orientačný systém."),
    ("Kedy môžete nastúpiť?",
     "Maj odpoveď pripravenú a konkrétnu. Neurčitosť tu stojí body.",
     "Rada by som to zladila s tým, čo mám rozrobené v ShapelesAi. Reálne to "
     "viem podľa dohody, ideálne do mesiaca."),
    ("Máte na nás nejaké otázky?",
     "Vždy áno. Kto sa nespýta nič, vyzerá, že mu na tom nezáleží. "
     "Vyber si tri z nasledujúcej sekcie.",
     None),
]

MOJE_OTAZKY = [
    ("Čítala som, že vašu vizuálnu identitu robíte interne a že sa vyvíja "
     "postupne, nie ako jednorazový manuál. Ako to vyzerá v praxi, keď príde "
     "nová výstava?",
     "Toto je najsilnejšia otázka, akú tam môžeš položiť. Ukáže, že si si "
     "o nich zistila viac než inzerát, a zároveň sa pýtaš na to, ako sa "
     "u nich naozaj pracuje."),
    ("S kým by som pracovala a kto dnes robí grafiku k výstavám?",
     "Praktické a normálne. Zároveň zistíš, či budeš v tíme alebo sama."),
    ("V akej fáze prípravy výstavy vstupuje do hry grafik?",
     "Rozdiel medzi „dostaneš text a vysádž ho“ a „si pri tom od začiatku“ "
     "je pre teba zásadný a oni to vedia."),
    ("S ktorými tlačiarňami spolupracujete a rieši komunikáciu s nimi grafik?",
     "Otázka, ktorú položí len človek, ktorý už raz podklady odovzdával. "
     "Presne tú stránku seba tam chceš ukázať."),
    ("Čo by ste chceli, aby ten človek zvládol sám do pol roka?",
     "Dozvieš sa, čo od pozície naozaj čakajú, a znie to ako od niekoho, "
     "kto rozmýšľa, či to zvládne, nie či to dostane."),
]

DIZAJN_UVOD = (
    "Na High5 ti dali presne tieto otázky a v galérii prídu tiež. Sú to jediné "
    "otázky na pohovore, kde sa nedá pripraviť odpoveď, dá sa pripraviť len "
    "spôsob, akým budeš rozmýšľať nahlas. Preto tu nie sú vety na naučenie, "
    "ale postup."
)

DIZAJN = [
    ("Komu je tento dizajn určený? Na koho cieli?",
     "Nehádaj podľa vkusu, čítaj signály. Kde to žije, teda plagát v meste, "
     "pozvánka do ruky alebo príspevok na Instagrame. Aké je písmo, či ťažký "
     "grotesk alebo jemná antikva. Koľko je tam textu a aký je formálny. "
     "A čo tam nie je, lebo aj to niečo hovorí.",
     "Povedz, komu to je určené, a hneď dve veci, z ktorých to čítaš. Napríklad "
     "veľké písmo a málo textu znamená, že to má fungovať z diaľky a za pár "
     "sekúnd, teda pre človeka v pohybe. Dlhý text a jemná sadzba znamenajú "
     "niekoho, kto si sadne."),
    ("A komu cieli SNG?",
     "Túto si priprav dopredu, lebo je to ich vlastná otázka na ich vlastnú "
     "prácu. Odpoveď máš priamo v inzeráte, menujú tri publiká: širokú "
     "verejnosť, rodiny s deťmi a školy. K tomu odborné publikum pri katalógoch "
     "a zahraniční návštevníci.",
     "Zaujímavé na tom je, že galéria hovorí k trom rôznym publikám jednou "
     "identitou. Plagát pre dospelého návštevníka, sprievodca pre školu a leták "
     "pre rodinu s deťmi musia vyzerať ako jedna inštitúcia, ale nesmú hovoriť "
     "rovnako. To je pre grafika ťažšie než urobiť tri rôzne vizuály."),
    ("Páči sa vám náš dizajn? Prečo?",
     "Pasca na oboch koncoch. Nadšenie bez obsahu znie prázdno a kritika na "
     "pohovore znie ako drzosť, hlavne keď autori identity sedia v tej istej "
     "budove. Odpovedz ako grafička, nie ako divák.",
     "Pomenuj jednu konkrétnu vec, ktorá funguje, a povedz prečo funguje. Nie "
     "„je to pekné a čisté“, ale napríklad ako je použitý priestor okolo názvu "
     "výstavy alebo ako sa to isté písmo správa na plagáte a v bulletine. "
     "Potom pridaj jednu otázku, nie výhradu."),
    ("Čo by ste na tom zmenili?",
     "Ak sa spýtajú priamo, kritika je povolená, ale iba vo forme otázky na "
     "obmedzenia. Nikdy nie ako rozsudok. Ty nevieš, čo im diktoval rozpočet, "
     "termín alebo pamiatkari.",
     "Skôr než by som niečo menila, chcela by som vedieť, čo to obmedzovalo. "
     "Pri tabuliach v priestore býva rozhodujúce, z akej vzdialenosti sa to "
     "číta a čo dovolí budova. Bez toho by som hodnotila len vzhľad."),
    ("Aký je váš štýl?",
     "Klasická otázka na juniora a klasická pasca. Vymyslené manifesto je "
     "počuť. Úprimná odpoveď, ktorá pomenuje, čo ťa naozaj baví, znie lepšie "
     "než vzletné slová.",
     "Mám najbližšie k typografii a k veciam, ktoré idú do tlače. Baví ma, keď "
     "vznikne systém, v ktorom sa dá pracovať ďalej, a nie jeden pekný obrázok. "
     "K tomu ilustrácia, tú robím rada, ale ako doplnok, nie ako hlavnú vec."),
]

VKUS_UVOD = (
    "Toto je pri galérii najpravdepodobnejšia skupina otázok a zároveň jediná, "
    "kde ti nemôžem napísať odpoveď. Musí byť tvoja, inak je počuť, že je "
    "naučená. Čo sa dá pripraviť, je tvar odpovede a menu mien, z ktorého si "
    "vyberieš len to, čo je pravda. Netestujú vedomosti. Testujú, či vieš "
    "pomenovať, prečo sa ti niečo páči. Konkrétna odpoveď o menej známom mene "
    "je vždy lepšia než vzletná odpoveď o Picassovi."
)

VKUS_FORMULA = (
    "Meno, potom jedna konkrétna práca, potom jedno rozhodnutie, ktoré v nej "
    "vidíš, a na koniec veta, čo si z toho berieš do vlastnej práce. Štyri kroky, "
    "tridsať sekúnd. Kto povie len meno, pôsobí, že ho počul, nie videl."
)

VKUS = [
    ("Kto je váš obľúbený dizajnér?",
     "Vyber si niekoho, koho prácu vieš naozaj otvoriť a opísať. Ak povieš "
     "meno, ktoré len znie dobre, druhá otázka ťa položí. Pri slovenskej "
     "inštitúcii sa slovenské meno cení viac než zahraničná hviezda, lebo "
     "ukazuje, že poznáš prostredie, do ktorého ideš.",
     "Mená, ktoré sedia k tomu, čo robíš ty: Vladislav Rostoka, plagáty "
     "a typografia, a je práve teraz v ich Bang?! Bang! 2. Albín Brunovský "
     "a Dušan Kállay, ak ťa ťahá knižná ilustrácia. Miroslav Cipár, ak ťa baví "
     "spojenie ilustrácie a logotypu. Ľudovít Fulla, ak chceš ostať pri téme "
     "výstavy. Otvor si dnes jedno z tých mien a vyber si podľa toho, čo ti "
     "naozaj sadne."),
    ("Kto je váš obľúbený umelec?",
     "Túto máš vďaka dnešku vybavenú. Ak si na výstave, odpoveď je Galanda "
     "a máš k nemu dôvod, ktorý nepovie nikto iný.",
     "Mikuláš Galanda. Bol v podstate grafický dizajnér, robil grafickú "
     "redakciu časopisu DAV, s Fullom si sám vydával manifest a navrhoval "
     "obálky pre básnikov. A za svojho života ho ocenili práve za knižnú "
     "grafiku, nie za maľbu."),
    ("Aký štýl umenia máte rada?",
     "Nepovedz minimalizmus. To hovorí každý a nič to nehovorí. Neodpovedaj "
     "názvom smeru, odpovedz tým, čo ťa na veciach zaujíma, a jedným príkladom.",
     "Skôr než smer ma zaujíma, keď je za vecou systém. Baví ma, keď vidno "
     "pravidlo, podľa ktorého to vzniklo, a keď sa to pravidlo dá použiť ďalej. "
     "Preto mi sedia geometrické a konceptuálne veci a preto ma bavila práca "
     "na dizajn manuáli aj na orientačnom systéme."),
    ("Akým štýlom tvoríte vy?",
     "Neodpovedaj prídavnými menami. Odpovedz tým, čo je v tvojom portfóliu, "
     "lebo to si vedia otvoriť a overiť.",
     "Mám dve polohy a viem, ktorá je ktorá. Prvá je typografia a sadzba, tam "
     "pracujem v systémoch, mriežkach a pravidlách. Druhá je ilustrácia, kresba "
     "postáv a digitálna maľba, tam je to voľnejšie. Najradšej mám zadania, kde "
     "sa obe stretnú, napríklad knižná obálka alebo obal."),
    ("Sledujete niečo zo súčasnej scény?",
     "Ak nesleduješ systematicky, nepredstieraj to. Priznaná medzera "
     "s konkrétnym plánom znie lepšie než vymyslený zoznam mien.",
     "Systematicky nie, sledujem skôr jednotlivé veci než celé scény. Čo si "
     "otváram pravidelne, sú súťaže knižného dizajnu a Národná cena za dizajn, "
     "lebo tam je vidieť, čo sa v odbore hýbe."),
    ("Máte obľúbenú knihu alebo obálku?",
     "Táto padne pri galérii ľahko a je to darček. Maj pripravený jeden titul, "
     "ktorý si naozaj držala v ruke.",
     "Odpovedz konkrétnym titulom a jednou vecou na ňom, napríklad ako je "
     "riešený chrbát alebo ako sa správa názov na obálke a na titulnej strane. "
     "Toto je presne ten typ detailu, ktorý od grafika chcú počuť."),
]

CERVENE = [
    ("Politika okolo vedenia galérie",
     "Okolo súčasného generálneho riaditeľa boli v médiách spory. Nespomínaj "
     "to ani slovom, ani ako otázku. Nie je to tvoja téma a nemáš z toho "
     "ako vyjsť dobre."),
    ("Kritika ich vizuálu alebo výstav",
     "Identitu robia ľudia, ktorí možno sedia v tej istej budove. Aj dobre "
     "mienená pripomienka na pohovore znie ako drzosť."),
    ("„Beriem to zatiaľ, kým nenájdem niečo lepšie“",
     "Ani v náznaku. Do štátnej inštitúcie sa nehľadá človek na pol roka."),
    ("„Vizitky a štítky ma nebavia“",
     "Sú priamo v náplni práce. Vieš to a hlásiš sa aj tak, tak to neznižuj."),
    ("Benefity ako prvá otázka",
     "Multisport ani zľava v kaviarni nesmú byť prvá vec, na ktorú sa spýtaš."),
    ("Sťažovanie na predchádzajúcu prácu",
     "Aj keby si mala dôvod. Hovor o tom, kam ideš, nie o tom, odkiaľ utekáš."),
]

PLAT = [
    ("Ako sa ten plat počíta",
     "Zákon 553/2003 o odmeňovaní vo verejnom záujme. Tarifa vychádza "
     "z platovej triedy a zo započítanej praxe, takže sa o nej nedá vyjednávať. "
     "Vyjednáva sa o osobnom ohodnotení, ktoré tvorí ten zvyšok do 1 600 eur."),
    ("Čo povedať",
     "Že vieš, ako je to postavené, a že ťa zaujíma horná polovica rozpätia. "
     "Odôvodni to titulom, polygrafickou a realizovaným orientačným systémom."),
    ("Čo nepovedať",
     "Konkrétne číslo ako prvú vec a bez odôvodnenia. A nikdy nie sumu "
     "nad rozpätím v inzeráte, tú tam podľa zákona ani nemôžu dať."),
    ("Ak zatlačia na jedno číslo",
     "Povedz 1 550 a hneď dôvod. Číslo, ktoré nie je okrúhle, znie ako "
     "spočítané, nie ako vystrelené."),
    ("Čo do platu nerátaj",
     "Päť dní dovolenky navyše, pružný čas 37,5 hodiny týždenne, ICOM karta "
     "a Multisport sú príjemné, ale nie sú plat. Neplať nimi rozdiel."),
]

DNES_VECER = [
    ("Dvadsať minút na sng.sk",
     "Pozri si štyri výstavy, ktoré práve bežia, a k jednej si otvor plagát "
     "a pozvánku. Stačí, aby si vedela povedať, ktorá ťa zaujala a prečo."),
    ("Desať minút na ich Instagrame a Facebooku",
     "Uvidíš, ako vyzerá ich bežný obsah a v akom tóne hovoria. To je vec, "
     "ktorú budeš robiť aj ty."),
    ("Vytlač a vyplň dotazník",
     "Prišiel v prílohe pozvánky. Nevypĺňaj ho v čakárni, to je zbytočný stres."),
    ("Priprav portfólio dvakrát",
     "V notebooku aj vytlačené. Ak sa im nechce pozerať do obrazovky, "
     "papier ťa zachráni."),
    ("Prejdi si prvú odpoveď nahlas",
     "Len tú jednu, o sebe. Zvyšok sa neuč naspamäť, naučená veta je počuť."),
    ("Choď tam dnes, kým je otvorené",
     "Nedeľa 10:00 až 18:00, v pondelok majú zatvorené, takže dnes je posledná "
     "možnosť. Pozri si Galandu a k tomu si všímaj tlačoviny: texty na stenách, "
     "popisky pri dielach, sprievodcu, navigáciu v budove. Odfoť si to. "
     "Veta „bola som tam včera a všimla som si“ je na pohovore neprebitná."),
    ("Otvor si dva ich plagáty a napíš si o nich tri vety",
     "Konkrétne veci: aké písmo, koľko priestoru okolo názvu, ako je použité "
     "logo. Toto je jediná príprava na otázku, či sa ti páči ich dizajn. "
     "Bez nej z toho vyjde iba „je to pekné“."),
]

PRAKTICKE = [
    ("Kedy vyraziť",
     "Buď pred budovou o 10:50. Nie o 10:30, čakanie ťa rozhodí, a nie o 11:00."),
    ("Čo si vezmi",
     "Vyplnený dotazník, dve vytlačené kópie životopisu, portfólio v notebooku "
     "aj na papieri, občiansky preukaz a nabíjačku."),
    ("Ako sa obleč",
     "Čisto a jednoducho. Galéria nie je banka ani agentúra, prehnaná "
     "formálnosť tam pôsobí rovnako cudzo ako tepláky."),
    ("Ak dostaneš praktické zadanie",
     "Spýtaj sa najprv na formát, rozmer, či to ide do tlače a dokedy to chcú. "
     "Kto sa pýta skôr než začne, vyzerá skúsenejšie než ten, kto hneď kreslí."),
    ("Do 24 hodín po pohovore",
     "Pošli krátky ďakovný mail Alexandre Pilo a pridaj jednu vetu k niečomu, "
     "čo na pohovore odznelo. Vtedy je na mieste aj veta o budúcej spolupráci."),
    ("Spojenie na LinkedIne",
     "Až po pohovore, nie pred ním. Ideálne v ten istý deň, spolu s poďakovaním."),
]


# ---------------------------------------------------------------------------
def build():
    def item(title, tag, note, say, say_cls="say"):
        t = f'<p class="tag">{e(tag)}</p>' if tag else ""
        n = f'<p class="note">{e(note)}</p>' if note else ""
        s = f'<p class="{say_cls}">{e(say)}</p>' if say else ""
        return f'<div class="item"><h3>{e(title)}</h3>{t}{n}{s}</div>'

    o = ["<title>Pohovor SNG — príprava</title>", "<style>", fonts(), CSS, "</style>",
         '<div class="wrap">',
         '<header class="masthead">',
         '<p class="eyebrow">Príprava na pohovor</p>',
         "<h1>Slovenská národná galéria, junior grafik a DTP operátor</h1>",
         '<p class="lede">Prečítaj si to dnes večer a ráno ešte raz tie tri '
         'sekcie, ktoré si označíš. Odpovede sa neuč naspamäť, uč sa ich kostru.</p>',
         "</header>"]

    o += ['<section class="sect"><h2>Kde a s kým</h2>', '<dl class="facts">']
    o += [f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in KEDY]
    o += ["</dl>",
          '<p class="note">Pohovor vedie HR manažérka, nie grafik. Prvé kolo teda '
          'nebude o krivkách a profiloch, ale o tom, kto si, prečo galéria a za '
          'koľko. Odborné otázky môžu prísť až v druhom kole.</p>',
          "</section>"]

    o += ['<section class="sect"><h2>Čo o galérii vieš</h2>',
          '<p class="intro">Toto je tvoja najlacnejšia výhoda. Väčšina uchádzačov '
          'si prečíta inzerát a nič viac.</p>',
          '<dl class="facts">']
    o += [f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in GALERIA]
    o += ["</dl>", "</section>"]

    o += ['<section class="sect"><h2>Ich vizuálna identita, toto si zapamätaj</h2>',
          f'<p class="intro">{e(IDENTITA)}</p>',
          f'<p class="say angle">{e(IDENTITA_PRECO)}</p>',
          '<h2 style="margin-top:8px">Čo práve teraz visí</h2>',
          '<p class="intro">Vyber si jednu a vedz, prečo práve tú.</p>',
          '<ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in VYSTAVY]
    o += ["</ul>",
          '<h2 style="margin-top:8px">Galanda, a prečo práve on</h2>',
          f'<p class="intro">{e(GALANDA)}</p>',
          f'<p class="say">{e(GALANDA_POVEDZ)}</p>',
          f'<p class="note"><b>Pozor na Bang?! Bang! 2.</b> {e(BANG)}</p>',
          "</section>"]

    o += ['<section class="sect"><h2>Tri veci, ktorými vyhráš</h2>',
          '<p class="intro">Toto nie je zoznam prác. Sú to tri miesta, kde tvoj '
          'životopis a ich inzerát sedia na seba. Ku každej si pripravená veta, '
          'ktorá hovorí o rozhodnutí, nie o tom, ako to vyzerá.</p>']
    o += [item(t, tag, why, say, "say angle") for t, tag, why, say in ZHODY]
    o += ["</section>"]

    o += ['<section class="sect"><h2>Otázky, ktoré prídu</h2>']
    o += [item(q, None, why, say) for q, why, say in OTAZKY]
    o += ["</section>"]

    o += ['<section class="sect"><h2>Otázky na vkus a na umenie</h2>',
          f'<p class="intro">{e(VKUS_UVOD)}</p>',
          f'<p class="say angle">{e(VKUS_FORMULA)}</p>']
    o += [item(q, None, why, say) for q, why, say in VKUS]
    o += ["</section>"]

    o += ['<section class="sect"><h2>Otázky na dizajn</h2>',
          f'<p class="intro">{e(DIZAJN_UVOD)}</p>']
    o += [item(q, None, why, say, "say angle") for q, why, say in DIZAJN]
    o += ["</section>"]

    o += ['<section class="sect"><h2>Čo sa spýtaš ty</h2>',
          '<p class="intro">Vyber si tri a jednu z nich nech je tá prvá.</p>']
    o += [item(q, None, why, q, "say ask") for q, why in MOJE_OTAZKY]
    o += ["</section>"]

    o += ['<section class="sect"><h2>Plat</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in PLAT]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Čo nehovor</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in CERVENE]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Dnes večer, hodina práce</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in DNES_VECER]
    o += ["</ul></section>"]

    o += ['<section class="sect"><h2>Zajtra</h2><ul class="rows">']
    o += [f"<li><b>{e(k)}</b><span>{e(v)}</span></li>" for k, v in PRAKTICKE]
    o += ["</ul></section>"]

    o += ['<p class="foot">Jedna veta na záver. V inzeráte žiadajú navigačné systémy '
          'v priestore a predtlačovú prípravu. Ty máš navigačný systém, ktorý je '
          'vyrobený a visí v areáli školy, a predtlačovú prípravu máš zo strednej. '
          'Na juniorskú pozíciu to nebude mať skoro nikto. Choď tam ako človek, '
          'ktorý to vie, nie ako niekto, kto prosí.</p>',
          "</div>"]

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    return os.path.getsize(OUT)


if __name__ == "__main__":
    n = build()
    print(f"  10-pohovor-sng.html — {round(n / 1024)} kB")
