# Core na večerný zábavný kvíz — Reštaurácia Zuzana

Cieľová dĺžka **35 s** (rozsah 30–40). Podľa štruktúry z `kampan/skript.md` v repe DKP:
osem pomenovaných blokov, tempo 145 slov na 60 s, rezy každé 2,5–5 s.
Na 35 s to je **zhruba 85 slov a 10 rezov**.

Core sa nahráva **raz**. Hooky a subhooky sú samostatné klipy, ktoré sa naň lepia
spredu — core nesmie prezradiť to, čo hovorí hook.

## Zadanie

| Parameter | Hodnota |
|---|---|
| Orientácia | 9:16 na výšku, 1080 × 1920 |
| Snímkovanie | 30 fps |
| Dĺžka | 30–40 s, cieľ 35 |
| Tempo reči | 145 slov na 60 s |
| Titulky | napevno, spodná tretina |
| Strih | rez každé 2,5–5 s |
| Komentár | mimo obraz, nie hovoriaca tvár |
| CTA tlačidlo | Zistiť viac |

## Časová os

| Blok | Čas | Sekúnd | Čo tam je |
|---|---|---|---|
| OFFER | 0,0–8,0 | 8,0 | Čo to je, kedy to je |
| ELIMINATION | 8,0–13,0 | 5,0 | Zhodenie námietky „na to nemám" |
| GUARANTEE | 13,0–17,0 | 4,0 | Čo má hosť isté aj tak |
| BONUS | 17,0–21,0 | 4,0 | Výhry a čo je navyše |
| CTA | 21,0–25,0 | 4,0 | Prvá výzva |
| TIME LIMIT | 25,0–28,5 | 3,5 | Dátum |
| SCARCITY | 28,5–32,0 | 3,5 | Obmedzený počet stolov |
| CTA | 32,0–35,0 | 3,0 | Druhá výzva |

## Komentár na nahovorenie

Hranaté zátvorky treba nahradiť skutočnými údajmi. **Nevymýšľaj ich.**

```
[OFFER]
Každý [DEŇ] večer o [ČAS] je u nás v Zuzane kvízový večer. Šesť kôl,
otázky na všetko od filmov po Liptov, a stôl plný jedla popri tom.

[ELIMINATION]
Nemusíte byť vševed ani chodiť s partiou. Tímy staviame na mieste,
prídete aj sami a hrať budete s niekým.

[GUARANTEE]
Moderátora, bodovanie aj ceny riešime my. Vy si len sadnete
a objednáte.

[BONUS]
Víťazný tím berie [VÝHRA]. A druhý aj tretí odchádzajú tiež s niečím.

[CTA]
Kliknite na tlačidlo pod videom a rezervujte si stôl.

[TIME LIMIT]
Najbližší kvíz je [DÁTUM].

[SCARCITY]
Stolov máme [POČET], viac sa ich do sály nezmestí.

[CTA]
Tak neváhajte, kliknite a ozveme sa vám s potvrdením.
```

Spolu 86 slov, čo pri 145 slovách na minútu vychádza na 35,6 s. Sedí.

## Prompt do CapCutu

```
Zostrihaj 35-sekundový vertikálny reel 9:16, 1080x1920, 30 fps, pre Reštauráciu
Zuzana v Liptovskej Teplej. Je to reklama na večerný zábavný kvíz.

Tón: veselý, spoločenský, večerný. Nie luxusný, ale plný ľudí a smiechu.
Rez každé 2,5 az 5 sekúnd, nikdy nie dlhšie. Žiadne prechody, len tvrdé strihy.
Teplé farby, večerné svetlo nechaj teplé, nevyvažuj ho do bielej.

Komentár je nahovorený mimo obraz, hovoriaca tvár sa v zábere neobjaví.
Titulky napevno v spodnej tretine, Montserrat Bold, biele s tenkým čiernym
obrysom, vždy len jedna veta na obrazovke, synchrónne s hlasom.

Časová os a čo v ktorom úseku ukázať:
0,0-8,0   plná sála, ľudia pri dlhých stoloch, moderátor s mikrofónom,
          odpoveďové hárky na stole
8,0-13,0  detail dvoch az troch ľudí, ktorí sa radia nad hárkom a smejú sa
13,0-17,0 moderátor vyhlasuje, ruka zapisuje body na tabuľu
17,0-21,0 ceny na stole, víťazný tím dvíha ruky
21,0-25,0 celkový záber sály, zvonku vidno rozsvietenú prevádzku
25,0-28,5 detail prestretého stola s jedlom a nápojmi
28,5-32,0 pomalý prejazd pozdĺž obsadených stolov
32,0-35,0 exteriér s nápisom Reštaurácia Zuzana

Hudba: veselý podklad bez spevu, aby komentár ostal zrozumiteľný. Pod hlasom
stiahni hlasitosť. Na sekunde 21,0 a 32,0 daj hudbe krátky dôraz, tam padajú
obe výzvy.

Na konci nedávaj žiadny statický koncový panel dlhší než sekundu. Posledný
záber musí byť živý obraz, nie logo na plnú obrazovku.
```

## Čo treba natočiť

Ak sa kvíz ešte nekonal, toto sú zábery, bez ktorých sa core nezostrihá.
Stačí mobil, ale **klopový mikrofón na komentár je nutný.**

| Záber | Kam patrí |
|---|---|
| Plná sála pri dlhých stoloch, večerné svetlo | OFFER, CTA |
| Moderátor s mikrofónom, zozadu alebo z boku | OFFER, GUARANTEE |
| Odpoveďové hárky a perá na stole, detail | OFFER |
| Dvaja až traja ľudia sa radia nad hárkom a smejú | ELIMINATION |
| Ruka zapisuje body na tabuľu alebo do hárku | GUARANTEE |
| Ceny položené na stole | BONUS |
| Víťazný tím, dvihnuté ruky alebo potlesk | BONUS |
| Prestretý stôl s jedlom a nápojmi | TIME LIMIT |
| Pomalý prejazd pozdĺž obsadených stolov | SCARCITY |
| Exteriér s nápisom Reštaurácia Zuzana, večer | posledný záber |

🔴 **Súhlas hostí.** Ak sú v zábere rozpoznateľné tváre hostí, treba ich súhlas.
Najbezpečnejšie je točiť ruky, stoly, hárky a chrbty, tvár moderátora s jeho
súhlasom a celkové zábery zozadu.

## Čo sa nesmie povedať, kým to klient nepotvrdí

- Žiadna výhra ani suma, ktorú klient nepotvrdil.
- Žiadny konkrétny dátum, ktorý klient negarantuje.
- Žiadne „vstup zdarma", ak sa platí štartovné.
- Žiadny počet stolov, ktorý nezodpovedá kapacite sály.
