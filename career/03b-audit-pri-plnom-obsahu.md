# Krok 3b — Audit za predpokladu, že portfólio je plné

**Premisa:** predstavme si, že všetkých 30 slotov je naplnených skutočnými prácami — 5 obálok z diplomovky (Alica v krajine zázrakov), školské projekty (mapa školy, filmové plagáty), práce z MOJESIDLO a SHAPELESAI, sociálne siete. Žiadne placeholdery.

**Otázka:** čo by na portfóliu nefungovalo **aj tak**?

---

## 0. Hlavné zistenie

Toto je najužitočnejší výsledok celej analýzy, a je nepríjemný:

> **Prázdnota nebola hlavný problém. Iba ho zakrývala.**

Aj s kompletným obsahom by portfólio prepadlo vo väčšine bodov rubriky — pretože **súčasný web nie je postavený ako portfólio. Je postavený ako brožúra služieb.**

Pozri sa na jeho stavbu: päť služieb s ikonkami → dlaždice kategórií → „O mne" → výzva na kontakt. To je štruktúra, ktorej úlohou je **opísať, čo ponúkaš**. Portfólio má inú úlohu — **ukázať, čo si spravila**, a nechať prácu hovoriť za teba.

Rozdiel nie je kozmetický. Prejavuje sa v deviatich konkrétnych miestach nižšie a týka sa vecí, ktoré sa nedajú vyriešiť nahratím obrázkov.

**Dobrá správa:** takmer všetko z toho viem opraviť **teraz, bez tvojich súborov**. Takže čakanie na ten počítač nás nezdržiava — práve naopak, mám čo robiť.

---

## 1. Revidované skóre (pri plnom obsahu)

| # | Kritérium | Prázdne | **Plné** | Prečo |
|---|---|---|---|---|
| 1 | Jeden sektor viditeľný do pár sekúnd | ❌ | ❌ | Architektúra: 5 rovnocenných kategórií, knižný dizajn medzi nimi nie je |
| 2 | Práce zodpovedajú sektoru | ❌ | ⚠️ | Existujú, ale zahrabané v „Tlačoviny" |
| 3 | Nerelevantné odstránené | ❌ | ❌ | Web nemá mechanizmus ukázať výber |
| 4 | Dosť prác v cieľovej oblasti | ❌ | ⚠️ | 5 z 30 = 17 % portfólia |
| 5 | Všestrannosť vnútri sektora | ❌ | ⚠️ | Nedá sa ukázať — delí sa podľa disciplíny, nie sektora |
| 6 | Každý kus na ~87 % | — | ❌ | **30 slotov si vynucuje vatu** |
| 7 | Žiadna kolísavá kvalita | — | ❌ | Pri 30 kusoch zaručene nastane |
| 8–10 | Zavádzajúce / sebestredné / skice | — | ? | Závisí od obsahu |
| 11 | Otvára najsilnejšou prácou | ❌ | ❌ | **Homepage neukazuje ani jeden projekt** |
| 12 | Reálna/publikovaná práca vpredu | ❌ | ❌ | Nedá sa odlíšiť od školskej |
| 13 | Kurátorované podľa sily | — | ❌ | Žiadna logika poradia |
| 14 | Drop-off test (15 s bez teba) | ❌ | ❌ | **Neexistuje stránka projektu** |
| 15 | Súdržný celok | ⚠️ | ⚠️ | Roztrieštené na 5 disciplín |
| 16 | Práca v kontexte (mock-up, in situ) | ❌ | ❌ | Šablóna to neumožňuje |
| 17 | Popisky | ❌ | ❌ | Karta má jeden riadok |
| 18 | Problém → riešenie → prečo | ❌ | ❌ | Nie je kam to napísať |
| 19 | Čestne uvedená rola | — | ❌ | Nie je na to pole |
| 20 | Pozadia podporujú prácu | ✅ | ⚠️ | Placeholderové gradienty treba nahradiť |
| 21 | Vysoké rozlíšenie | — | ? | Závisí od tvojich súborov |
| 22 | Konzistentná orientácia | ✅ | ❌ | **Náhľad je 4:3 na šírku, obálky sú na výšku** |
| 23 | Žiadna nedbalosť | ⚠️ | ⚠️ | „CELÉ PORTFÓLIO" stále vedie na branding.html |
| 24 | Navigácia, rýchlosť, bez preklepov | ✅ | ✅ | V poriadku |
| 25 | CV ako typografický kus | ❌ | ❌ | Nezávisí od obsahu — stále chýba |
| 26 | Hlavičkový papier, podpis | ⚠️ | ⚠️ | Stále chýba |
| 27 | Kontakt na artefaktoch | ✅ | ✅ | Na webe áno |
| 28 | PDF na posielanie | ❌ | ❌ | Stále chýba |
| 29 | Krátky promo kus | ❌ | ❌ | Stále chýba |

**Splnené: 3 z 29** (oproti 4 pri prázdnom — bod 22 sa naplnením obsahu dokonca *zhorší*).

---

## 2. Deväť zistení, ktoré vidno až pri plnom portfóliu

### 2.1 Homepage neukazuje ani jeden projekt — ani keď ich máš 30 ⚠️ *najzávažnejšie*

**Overené v kóde:** `index.html` obsahuje **0 kariet projektov** a **5 dlaždíc kategórií**.

Nadpis „VYBRANÉ PROJEKTY" teda nesľubuje dvakrát — nesľubuje vôbec. Aj s plným portfóliom návštevník na úvodnej stránke neuvidí ani jednu tvoju prácu, iba päť ikoniek s odkazmi „Zobraziť →".

Kniha pritom žiada pravý opak:

> „it's generally agreed you should **start with your strongest piece** and end on a similarly high note."

A pripomeňme, čím dnes homepage otvára: **ilustráciou dievčaťa pri stole, ktorá nie je tvoja práca.** Prvý vizuálny dojem z portfólia grafickej dizajnérky je cudzí obrázok.

Art director má na teba podľa knihy pätnásť minút — a často len drop-off bez teba. Ak musí urobiť dve kliknutia, než uvidí prvú prácu, veľká časť tej pozornosti je preč.

### 2.2 Neexistuje stránka projektu — „Zobraziť projekt →" je mŕtvy text ⚠️

**Overené v kóde:** `<span class="project-link">Zobraziť projekt →</span>` — **0 odkazov `<a>`, 6 elementov `<span>`** na každej podstránke. Vyzerá to ako odkaz, ale nikam nevedie. A žiadna detailná stránka projektu v repozitári neexistuje.

To znamená, že najhlbšie, kam sa návštevník dostane, je **náhľad + jeden riadok textu**. Tým padajú naraz štyri body rubriky (14, 16, 17, 18) a nedá sa splniť ani bod 19 (čestné uvedenie roly).

Konkrétne: o diplomovke by sa art director dozvedel „Obálka knihy — dizajn — Alica v krajine zázrakov". Nič o tom, že ide o päť žánrových spracovaní jedného titulu, ktoré je celým jej zmyslom.

**Toto je najväčšia štrukturálna diera celého webu.**

### 2.3 Náhľady sú na šírku, knižné obálky sú na výšku

**Overené v kóde:** `.project-thumb { aspect-ratio: 4/3; }` — teda formát na šírku.

Knižná obálka má pomer zhruba **2:3 na výšku**. Vložená do 4:3 rámu na šírku sa buď **oreže** (príde o hornú a dolnú časť — teda spravidla o názov alebo meno autora), alebo **pláva v prázdnom priestore** s pruhmi po stranách.

Päť obálok z diplomovky by teda bolo prezentovaných v presne najhoršom možnom formáte. Kniha má na orientáciu explicitné pravidlo:

> „try to minimize the amount of folder-twirling your interviewer will have to do by **deciding in which direction both formats will face, and abiding by that decision** throughout your portfolio."

Pri portfóliu zameranom na knihy má byť **základný formát na výšku**, nie na šírku.

### 2.4 Architektúra si vynucuje 30 projektov — a tým vatu

**Overené:** 6 kariet × 5 podstránok = **30 slotov**. Mriežka je vizuálne navrhnutá tak, aby bola plná — tri stĺpce, dva riadky. Prázdne miesto v nej vyzerá ako chyba.

To vytvára tlak doplniť 30 prác. Lenže kniha hovorí, že niektorí art directori chcú vidieť **3 až 6 projektov celkovo**, a formuluje to nekompromisne:

> „I would rather see a book with **only a few really good pieces**, than one with a lot of inconsistent pieces." — Steve Scott, Scholastic

> „Seeing work of varying standards in the same portfolio would **put me off commissioning someone**." — Anamaria Stanley

Absolventka, ktorá napĺňa 30 slotov, tam nutne dá aj slabšie veci. A slabší kus podľa knihy neuberie priemeru — **zničí dôveru**, lebo naznačuje, že nevieš rozoznať svoju dobrú prácu od nie takej dobrej.

**Mriežka teda aktívne pracuje proti tebe.**

### 2.5 Knižný dizajn nemá na webe kde byť

V navigácii je päť kategórií: Branding · Ilustrácie · UI/UX dizajn · Tlačoviny · Marketing. **Knižný dizajn medzi nimi nie je.**

Päť obálok z diplomovky by teda skončilo v „Tlačoviny", ktorej podtitul znie *„plagáty, brožúry, knihy"* — knihy až na treťom mieste. Tvoja najsilnejšia a pre cieľ najrelevantnejšia práca by bola zaradená ako tretia položka pod generickým nadpisom.

To nie je nedostatok obsahu. To je **chyba informačnej architektúry** — a preto body 1 až 5 rubriky padajú aj pri plnom portfóliu.

### 2.6 Séria sa nedá ukázať ako séria

Toto je jemné, ale dôležité. Diplomovka je **jeden projekt s piatimi výstupmi** — päť žánrových spracovaní toho istého titulu. Sila je práve v porovnaní.

V súčasnej mriežke by z toho bolo **päť samostatných kariet vedľa seba**, každá s vlastným názvom a popiskom. Tým sa myšlienka rozpadne: návštevník uvidí päť obálok, nie jednu tézu.

Šablóna nepozná pojem „projekt obsahuje viac obrázkov". A práve to je formát, ktorý tvoja najlepšia práca potrebuje.

### 2.7 Nedá sa odlíšiť reálna práca od školskej

Karta má polia: štítok · názov · typ · popis. Nemá pole pre **klienta, rok, ani status** (školské / komerčné / publikované / koncepčný redizajn).

Kniha pritom kladie na publikovanú prácu veľký dôraz:

> „Most creative employers will be delighted and reassured to see published work in your portfolio, so **give it pride of place** — as near to the front of your portfolio as possible... it marks you out as a professional from the start."

Práce pre MOJESIDLO a SHAPELESAI **sú** komerčné práce pre reálnych klientov. Dnes by na webe vyzerali presne rovnako ako školské cvičenie. To je premrhaná výhoda.

Zároveň bez poľa pre rolu sa nedá splniť požiadavka na čestnosť: *„just be honest about your role."*

### 2.8 Poradie prác je náhodné

Neexistuje mechanizmus kurátorstva — ani „vybrané", ani preradenie, ani odlíšenie hlavného projektu. Kniha pritom výslovne varuje pred chronologickým a náhodným radením a žiada otvárať najsilnejším kusom.

### 2.9 Aparát okolo portfólia chýba nezávisle od obsahu

CV, posielateľné PDF, krátky promo kus, hlavičkový papier a e-mailový podpis. Ani jedna z týchto vecí nezávisí od tvojich súborov — **všetky sa dajú spraviť hneď**, a všetky sú v knihe uvedené ako povinná výbava.

---

## 3. Čo z toho vyplýva

Prvý audit vyzeral takto: *„chýba obsah, doplň obsah."*
Druhý audit hovorí niečo iné: **„web treba prestavať a obsah doňho vložiť."**

To je v skutočnosti lepšia správa, než sa zdá — pretože **prestavba nezávisí od toho, kedy sa dostaneš k tomu počítaču.** Môžem s ňou začať okamžite a mať pripravený rám, do ktorého sa práce už len vložia.

### Priorita opráv (všetko bez tvojich súborov)

| # | Oprava | Rieši body |
|---|---|---|
| **1** | **Stránka projektu (case study)** — hlavný vizuál, galéria viacerých obrázkov, zadanie / riešenie / prečo, fakty (rok, klient, rola, formát, softvér), práca v kontexte | 14, 16, 17, 18, 19, 2.2, 2.6 |
| **2** | **Nová kategória „Knižný dizajn"** ako prvá v navigácii, ostatné disciplíny nižšie ako „Ďalšia tvorba" | 1, 2, 3, 5, 2.5 |
| **3** | **Homepage ukazuje 3–4 skutočné projekty**, začínajúc diplomovkou; dlaždice kategórií až pod nimi | 11, 12, 2.1 |
| **4** | **Formát náhľadu na výšku (2:3)** pre knižné práce, s možnosťou na šírku pre ostatné | 22, 2.3 |
| **5** | **Zmenšiť mriežku** — z 30 slotov na 8–12 kurátorovaných miest; prázdne miesto nesmie pôsobiť ako chyba | 6, 7, 2.4 |
| **6** | **Polia pre klienta, rok, rolu a status** + vizuálne odlíšenie komerčnej a publikovanej práce | 12, 19, 2.7 |
| **7** | **Poradie podľa sily**, nie podľa kategórie | 13, 2.8 |
| **8** | **CV** (stránka + PDF), **posielateľné PDF portfólio**, **promo kus**, **hlavičkový papier a e-mailový podpis** | 25, 26, 28, 29 |
| **9** | Oprava odkazu „CELÉ PORTFÓLIO" | 23 |

### Čo aj tak zostane na tebe

Iba tri veci — a ani jedna nevyžaduje, aby som čakal:

- **Texty k projektom** (zadanie, riešenie, prečo). Fakty musia byť tvoje; formuláciu doladím.
- **Kvalita a rozlíšenie súborov** — min. 2000 px na dlhšej strane, plus tlačové PDF.
- **Rozhodnutie, ktoré práce sa do kurátorovaného výberu vôbec dostanú.** To je podľa knihy najdôležitejšia dizajnérska schopnosť v celom procese: *„If you don't believe in it, bin it."*

---

*Audit vychádza z rovnakej rubriky ako `03-analyza-portfolia.md`, aplikovanej za predpokladu plného obsahu. Technické tvrdenia (počet kariet, pomer strán, mŕtve odkazy, kapacita mriežky) sú overené priamo v kóde repozitára, nie odhadnuté.*
