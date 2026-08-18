# FOUNDER RESEARCH GAP REGISTER

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/build_gap_register.py · ELLE DÜZENLEMEYİN -->

> **The Great Book of World Games** · kurucu araştırma teslim kaydı
> 
> Bu dosya İNGİLİZCE alan adlarıyla yazılmıştır çünkü kurucu direktifi
> (§ 6 · § 13) alan listesini İngilizce verir ve paket bir kütüphaneciye
> ya da araştırmacıya doğrudan uzatılabilir olmalıdır. Gerekçe metinleri
> deponun dili olan Türkçedir.

> ⛔ **Bu bir 'kalan oyunlar' listesi DEĞİLDİR.** Yalnızca kurucunun
> müdahalesi olmadan yazılamayacak maddeleri taşır. Kaynağı elde olan
> ve yalnızca sıra bekleyen oyunlar § 2'de AYRI durur.

---

## 1 · TEK BAKIŞTA

| | ölçülen |
|---|---:|
| Nihai kapsam | **100** |
| Yazılmış | **47** |
| Kurucu MÜDAHALESİ OLMADAN yazılabilir | **7** |
| **KURUCU ARAŞTIRMASI GEREKEN** | **46** |
| ↳ `BLOCKED` — kaynak denendi, açılamadı | **28** |
| ↳ `SOURCE-PENDING` — künye var, HENÜZ denenmedi | **16** |
| ↳ `UNRESOLVED` — kaynak açık, kimlik/kültür uyuşmuyor | **2** |
| `UNATTEMPTED` — hiç denenmemiş ve engelsiz | **0** |

> `UNATTEMPTED` **sıfırdır** ve bu kasıtlıdır: Batch 6'da kalan 59 oyunun
> **tamamı** elde bulunan kamusal alan derlemelerine karşı tek tek tarandı.
> Artık 'henüz bakılmadı' diyebileceğimiz bir oyun yok. Bu, Faz 3'ün
> 'denenmedi = engelli' hatasının TERSİ yönde kapatılmasıdır.

### Engel sınıflarının dağılımı

| sınıf | ad | sayı |
|---|---|---:|
| `P1` | SOURCE ACCESS BLOCKED | 20 |
| `P2` | SOURCE TEXT UNAVAILABLE | 18 |
| `P3` | RULES INCOMPLETE | 2 |
| `P5` | CULTURAL IDENTITY / ATTRIBUTION UNRESOLVED | 2 |
| `P6` | RECONSTRUCTION TOO UNCERTAIN | 3 |
| `P8` | SOURCE LOCATOR MISSING | 1 |

---

## 2 · KURUCU MÜDAHALESİ GEREKTİRMEYEN 7 OYUN

Bunlar **engelli değildir** — sıra beklerler. Kaynakları elde bulunan
kamusal alan derlemelerindedir ve ajan bunları kurucu beklemeden yazar.

| oyun | aile | isabet |
|---|---|---|
| `alquerque` | The War Board | Fiske 1905 |
| `chaupar` | The Race Home | Culin 1895 · 'Chausar' — ⚠ kültür tuzağı riski: isabet Culin'in KORE cildindedir, sayfa açılmadan yazılamaz |
| `gilli-danda` | Games Without a Board | Culin 1907 · 'Tipcat' — ⚠ kültür tuzağı riski: isabet İNGİLİZ/Kuzey Amerika kaydıdır, sayfa açılmadan yazılamaz |
| `ludus-latrunculorum` | The War Board | Falkener 1892 — ⚠ yeniden kurgulama beyanı zorunlu |
| `nine-holes` | The Line and the Territory | Gomme 1894 |
| `tabula` | The Race Home | Fiske 1905 |
| `tuknanavuhpi` | The War Board | Culin 1907 |

> ⚠ İlk ikisi **kültür tuzağı riski** taşır ve sayfa açılmadan yazılamaz.
> Totolospi, sugoroku, tien-gow, jianzi ve xiangqi'de aynı tuzak beş kez
> ölçüldü: bir derlemenin başka bir kültüre ait bölümünden yazmak,
> kitabın kültür künyesini yalanlar.

---

## 3 · AİLE AÇIĞI

| aile | hedef | yazılan | yazılabilir | **engelli** | açık | tamamlanma |
|---|---:|---:|---:|---:|---:|---|
| The Sowing Games | 14 | 4 | 0 | **10** | 10 | `███·········` 29% |
| The Line and the Territory | 17 | 8 | 1 | **8** | 9 | `█████·······` 47% |
| Games Without a Board | 16 | 7 | 1 | **8** | 9 | `█████·······` 44% |
| The Race Home | 18 | 9 | 2 | **7** | 9 | `██████······` 50% |
| The War Board | 21 | 11 | 3 | **7** | 10 | `██████······` 52% |
| The Hunt and the Siege | 10 | 5 | 0 | **5** | 5 | `██████······` 50% |
| Chance and Nerve | 4 | 3 | 0 | **1** | 1 | `█████████···` 75% |

> **Ekim ailesi kitabın en büyük açığıdır ve tek bir sebebi vardır:**
> on iki maddenin on ikisi de Murray · Bell · Zaslavsky · Russ ·
> de Voogt · Townshend hattına bağlıdır ve o hattın beşi engellidir.
> Aile 14 hedefinde **2** yazılmıştır — kitabın kendi adını taşıyan
> ailelerinden biri, açık ara en zayıfıdır.

---

## 4 · KÜLTÜR VE BÖLGE AÇIĞI

Kapsam **68 kültür** vaat ediyor; yazılan **27**. Kalan **34 kültürün**
tamamı bu kayıttaki maddelerdedir — yani bu kayıt çözülmezse kitap
kültür vaadini **68'de değil 27'de** kapatır.

Bölge olarak **dokuz bölge** YALNIZCA engelli kümede yaşıyor ve
çözülmezse kitaptan tamamen düşer:

- **Anatolia · Eastern Mediterranean** — `turkish-dama`
- **Central Asia** — `toguz-kumalak`
- **Central Europe** — `bohnenspiel`
- **Horn of Africa** — `gebeta` · `shax`
- **North-East Africa** — `li-b-el-merafib`
- **South America** — `adji-boto`
- **Southern Europe** — `game-of-the-goose`

---

## 5 · MEKANİK AÇIK

Engelli küme yalnızca kültür değil **mekanik** de taşıyor. Aşağıdaki
yapılar kitapta **hiç yoktur** ve yalnızca bu kayıttaki maddelerdedir:

| mekanik | taşıyan madde | not |
|---|---|---|
| dört sıralı ekim (four-row mancala) | `omweso` · `hus` · `mefuvha` | yazılan iki ekim oyununun ikisi de iki sıralıdır |
| ekimde tur sonu yeniden dizme | `pallanguzhi` · `congklak` | yok |
| kutsal çukur / tuzdyk | `toguz-kumalak` | yok |
| alırken ikinci taşı da kaldırma | `yote` | kitapta eşi yok |
| dikey-yatay (köşegensiz) dama | `turkish-dama` | yazılan damaların hepsi köşegendir |
| halkadan geçerek uzaktan alma | `surakarta` | kitapta eşi yok |
| kıstırarak alma (custodial capture) | `hasami-shogi` | seega yazıldı ama tahta oyunu olarak tek örnektir |
| kilitlenme galibiyeti (hamlesiz kalan kaybeder) | `mu-torere` · `konane` | yok |
| sarmal iz + serbest bırakma koşulu | `li-b-el-merafib` | yok |
| saf şans yarışı (karar yok) | `game-of-the-goose` | tarihsel önem gerekçesi prozada yazılmalı |
| taş dizme + set toplama (yığın devirme) | `lagori` | yok |
| yön kısıtlı kovalamaca + devir | `kho-kho` | yok |

---

## 6 · KALDIRAÇ — HANGİ TEK KAYNAK KAÇ OYUN AÇAR

> **Bu tablonun ilk satırı bu belgenin en önemli cümlesidir.**

| eser | açtığı madde | durum |
|---|---:|---|
| Murray, H. J. R., A History of Board-Games Other Than Chess | **20** | ⛔ denendi · açılamadı |
| Bell, R. C., Board and Table Games from Many Civilizations | **10** | ⛔ denendi · açılamadı |
| Parlett, David, The Oxford History of Board Games | **10** | ⛔ denendi · açılamadı |
| Uzmanlık makaleleri — tek oyunu açan dar künyeler | **10** | ◻ HİÇ denenmedi |
| Zaslavsky, Claudia, Africa Counts: Number and Pattern in African Culture | **8** | ⛔ denendi · açılamadı |
| Russ, Laurence, The Complete Mancala Games Book | **4** | ⛔ denendi · açılamadı |
| Townshend, Philip, 'Mankala in Eastern and Southern Africa: A Distributional Analysis', Azania: Journal of the British Institute in Eastern Africa 14 | **4** | ◻ HİÇ denenmedi |
| Béart, Charles, Jeux et jouets de l'Ouest africain, Mémoires de l'IFAN 42 | **2** | ◻ HİÇ denenmedi |
| Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 | **2** | ◻ HİÇ denenmedi |
| Pollux, Julius, Onomasticon, Book IX — denetlenebilir modern edisyon: E. Bethe | **2** | ⛔ denendi · açılamadı |
| Kaydın KENDİSİ bulunamayan oyunlar — arama görevi kurucuya aittir | **2** | ⛔ denendi · açılamadı |
| Culin, Stewart, 'Hawaiian Games', American Anthropologist 1:2 | **1** | ⛔ denendi · açılamadı |
| de Voogt, Alex, Mancala Board Games | **1** | ⛔ denendi · açılamadı |
| Yaşayan federasyon/kodifikasyon kuralları | **1** | ◻ HİÇ denenmedi |
| Murray, H. J. R., A History of Chess | **1** | ⛔ denendi · açılamadı |
| Volpicelli, Z., 'Wei-ch'i', Journal of the China Branch of the Royal Asiatic Society, N.S. XXVI | **1** | ◻ HİÇ denenmedi |

**Kümülatif:** Murray 1952 tek başına **24** madde açar. Ona Parlett,
Zaslavsky, Bell ve Russ eklenirse **52 maddenin 46'sı** açılır. Geri
kalan altısı ayrı ayrı avlanmak zorundadır.

---

## 7 · ÖNCELİK SIRALAMASI

Bileşik puan **beş bileşenden** oluşur ve dördü projenin KENDİ
verisinden okunur — yalnızca `unlockEase` bu kayıtta verilir:

```
compositeScore = unlockEase        (0–5 · açık cetvel, aşağıda)
               + familyDeficit     (0–5 · aile açığı ÷ hedef, ölçülen)
               + culturalValue     (0–5 · game_index scores.cultural)
               + mechanicalUnique  (0–5 · game_index scores.distinct)
               + pageEconomy       (0–5 · game_index scores.explain)
```

| sınıf | anlamı | sayı |
|---|---|---:|
| **A** | YÜKSEK GETİRİ — tek iyi kaynak maddeyi hemen açar | 18 |
| **B** | AİLE DENGESİ — ciddi eksik bir aileyi doldurur | 0 |
| **C** | KÜLTÜREL ÇEŞİTLİLİK — kaybedilen bir kültürü geri getirir | 15 |
| **D** | MEKANİK ÇEŞİTLİLİK — eşi olmayan bir mekanik taşır | 2 |
| **E** | DÜŞÜK ETKİ — yararlı ama kritik değil | 11 |

| # | oyun | aile | kültür | sınıf | puan | durum | engel |
|---:|---|---|---|:---:|---:|---|---|
| 1 | **Morra** `morra` | Games Without a Board | Italian | A | **21.8** | `BLOCKED` | `P3` |
| 2 | **Bohnenspiel** `bohnenspiel` | The Sowing Games | German | A | **21.6** | `BLOCKED` | `P1` |
| 3 | **Bagh-Chal** `bagh-chal` | The Hunt and the Siege | Nepali | A | **20.5** | `BLOCKED` | `P1` |
| 4 | **Kōnane** `konane` | The War Board | Hawaiian | C | **20.4** | `BLOCKED` | `P2` |
| 5 | **Yoté** `yote` | The War Board | Wolof | C | **20.4** | `SOURCE-PENDING` | `P2` |
| 6 | **Ampe** `ampe` | Games Without a Board | Akan | A | **19.8** | `BLOCKED` | `P1` |
| 7 | **Pilolo** `pilolo` | Games Without a Board | Ga | A | **19.8** | `BLOCKED` | `P1` |
| 8 | **Adji-boto** `adji-boto` | The Sowing Games | Ndyuka Maroon | C | **19.6** | `SOURCE-PENDING` | `P2` |
| 9 | **Congklak** `congklak` | The Sowing Games | Javanese | A | **19.6** | `BLOCKED` | `P1` |
| 10 | **Shisima** `shisima` | The Line and the Territory | Luhya | A | **19.6** | `BLOCKED` | `P1` |
| 11 | **Sungka** `sungka` | The Sowing Games | Visayan | A | **19.6** | `SOURCE-PENDING` | `P2` |
| 12 | **Aadu Puli Attam** `aadu-puli-attam` | The Hunt and the Siege | Tamil | A | **19.5** | `BLOCKED` | `P1` |
| 13 | **Bul** `bul` | The Race Home | Kekchi Maya | C | **19.5** | `SOURCE-PENDING` | `P2` |
| 14 | **Li'b el-Merafib** `li-b-el-merafib` | The Race Home | Sudanese Arab | C | **19.5** | `SOURCE-PENDING` | `P2` |
| 15 | **Dama** `turkish-dama` | The War Board | Turkish | A | **19.4** | `BLOCKED` | `P1` |
| 16 | **Pétanque** `petanque` | Games Without a Board | Provençal | A | **18.8** | `SOURCE-PENDING` | `P8` |
| 17 | **Gebeta** `gebeta` | The Sowing Games | Amhara | C | **18.6** | `SOURCE-PENDING` | `P2` |
| 18 | **Go** `go` | The Line and the Territory | Han Chinese | C | **18.6** | `UNRESOLVED` | `P5` |
| 19 | **Hus** `hus` | The Sowing Games | Nama | C | **18.6** | `SOURCE-PENDING` | `P2` |
| 20 | **Morabaraba** `morabaraba` | The Line and the Territory | Sotho | A | **18.6** | `BLOCKED` | `P1` |
| 21 | **Omweso** `omweso` | The Sowing Games | Ganda | C | **18.6** | `SOURCE-PENDING` | `P2` |
| 22 | **Shax** `shax` | The Line and the Territory | Somali | A | **18.6** | `BLOCKED` | `P1` |
| 23 | **Tapatan** `tapatan` | The Line and the Territory | Tagalog | A | **18.6** | `BLOCKED` | `P2` |
| 24 | **Toguz Kumalak** `toguz-kumalak` | The Sowing Games | Kazakh | D | **18.6** | `BLOCKED` | `P1` |
| 25 | **Ashta Kashte** `ashta-kashte` | The Race Home | Bengali | A | **18.5** | `BLOCKED` | `P1` |
| 26 | **Daldøs** `daldos` | The Race Home | Danish | C | **18.5** | `SOURCE-PENDING` | `P2` |
| 27 | **The Game of the Goose** `game-of-the-goose` | The Race Home | Italian | E | **17.5** | `SOURCE-PENDING` | `P1` |
| 28 | **Len Choa** `len-choa` | The Hunt and the Siege | Thai | A | **17.5** | `BLOCKED` | `P1` |
| 29 | **Nard** `nard` | The Race Home | Persian | C | **17.5** | `SOURCE-PENDING` | `P2` |
| 30 | **Rimau-rimau** `rimau-rimau` | The Hunt and the Siege | Malay | A | **17.5** | `BLOCKED` | `P1` |
| 31 | **Zamma** `zamma` | The War Board | Amazigh | C | **17.4** | `SOURCE-PENDING` | `P2` |
| 32 | **Ayòayò** `ayoayo` | The Sowing Games | Yoruba | E | **16.6** | `SOURCE-PENDING` | `P2` |
| 33 | **Mefuvha** `mefuvha` | The Sowing Games | Venda | E | **16.6** | `SOURCE-PENDING` | `P2` |
| 34 | **Halatafl** `halatafl` | The Hunt and the Siege | Icelandic | E | **16.5** | `BLOCKED` | `P3` |
| 35 | **Jeu de Dames** `jeu-de-dames` | The War Board | French | A | **16.4** | `BLOCKED` | `P1` |
| 36 | **Makruk** `makruk` | The War Board | Thai | E | **16.4** | `BLOCKED` | `P1` |
| 37 | **Surakarta** `surakarta` | The War Board | Javanese | D | **16.4** | `UNRESOLVED` | `P5` |
| 38 | **Ephedrismos** `ephedrismos` | Games Without a Board | Ancient Greek | C | **15.8** | `BLOCKED` | `P6` |
| 39 | **Lagori** `lagori` | Games Without a Board | Kannada | E | **15.8** | `BLOCKED` | `P2` |
| 40 | **Myinda** `myinda` | Games Without a Board | Ancient Greek | E | **15.8** | `BLOCKED` | `P1` |
| 41 | **Twelve Men's Morris** `twelve-mens-morris` | The Line and the Territory | Medieval European | E | **15.6** | `BLOCKED` | `P1` |
| 42 | **Ludus Duodecim Scriptorum** `ludus-duodecim-scriptorum` | The Race Home | Roman | C | **15.5** | `SOURCE-PENDING` | `P6` |
| 43 | **Kho Kho** `kho-kho` | Games Without a Board | Marathi | E | **14.8** | `BLOCKED` | `P2` |
| 44 | **Luk Tsut K'i** `luk-tsut-kei` | The Line and the Territory | Cantonese | E | **14.6** | `BLOCKED` | `P2` |
| 45 | **Terni Lapilli** `terni-lapilli` | The Line and the Territory | Roman | E | **14.6** | `BLOCKED` | `P6` |
| 46 | **Mahjong** `mahjong` | Chance and Nerve | Han Chinese | C | **14.2** | `BLOCKED` | `P1` |

---

## 8 · KAYIT — OYUN OYUN

Her madde kurucu direktifi § 6'nın istediği on beş alanı taşır.

---

### 1 · Morra

| | |
|---|---|
| **GAME ID** | `morra` |
| **TITLE** | Morra |
| **ALTERNATE NAME(S)** | Micatio, Mora |
| **CULTURE** | Italian |
| **REGION** | Mediterranean · Italy (Roman antecedent) |
| **FAMILY** | Games Without a Board |
| **PRIMARY BLOCKER** | `P3` — RULES INCOMPLETE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 21.8 |

**WHY THE AGENT CANNOT WRITE IT**

Erişilebilir kaynak AÇILDI ve mekaniği verdi ama PUANLAMA ve KAZANMA KOŞULU yoktur. Bir oyun bitişi olmadan basılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Falkener 1892 § Atep/Mora, ss. 103–105 AÇILDI: iki biçim kayıtlı (ikisi birden parmak atar ve ikisi de tahmin eder; ya da biri atar öteki tahmin eder) ve İTALYAN oyunu adlandırılıyor
- Cicero De Officiis III.77 — bir ATASÖZÜDÜR, kural değil
- Parlett 1999 telif altında

**WHAT SOURCE WAS ATTEMPTED**

- Parlett, David, The Oxford History of Board Games (Oxford: Oxford University Press, 1999)

**WHAT WAS MISSING**

Puanlama, kazanma koşulu, tur yapısı ve berabere kuralı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Morra'nın PUANLAMASINI ve KAZANMA koşulunu veren herhangi bir künye
2. Tur yapısı: kaç el oynanır, puan nasıl birikir
3. Berabere durumunda ne olduğu

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] turn order  [ ] scoring  [ ] end condition  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Bir İtalyan halk oyunları derlemesi ya da Parlett'in morra bölümü.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/morra/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"morra" Italian finger game rules scoring`
- `"micatio" mora game history rules`
- `morra gioco regole punteggio storico`

---

### 2 · Bohnenspiel

| | |
|---|---|
| **GAME ID** | `bohnenspiel` |
| **TITLE** | Bohnenspiel |
| **ALTERNATE NAME(S)** | Das Bohnenspiel |
| **CULTURE** | German |
| **REGION** | Central Europe · Germany |
| **FAMILY** | The Sowing Games |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 21.6 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 ve Bell proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)
- Bell, R. C., Board and Table Games from Many Civilizations (Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)

**WHAT WAS MISSING**

İki künyenin ikisi de engelli.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray 1952 ya da Bell'de Bohnenspiel maddesi — 2×6 çukur, 6'şar tohum, ekim yönü, 2/4/6 alma kuralı, zincirli alma
2. Oyunun Avrupa'ya nasıl ulaştığına dair BİR İDDİA DEĞİL, bir kayıt (kayıt köken iddiasını açıkça yasaklıyor)

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Alman kaynaklı bir dönem kaydı köken sorununu da hafifletir.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/bohnenspiel/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"Bohnenspiel" German mancala rules Murray`
- `das Bohnenspiel Regeln historisch Saatspiel`

---

### 3 · Bagh-Chal

| | |
|---|---|
| **GAME ID** | `bagh-chal` |
| **TITLE** | Bagh-Chal |
| **ALTERNATE NAME(S)** | Baghchal, Tigers and Goats |
| **CULTURE** | Nepali |
| **REGION** | South Asia · Nepal |
| **FAMILY** | The Hunt and the Siege |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 20.5 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Bell ve Parlett proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Bell, R. C., Board and Table Games from Many Civilizations (Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)
- Parlett, David, The Oxford History of Board Games (Oxford: Oxford University Press, 1999)

**WHAT WAS MISSING**

İki künyenin ikisi de engelli.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Bell ya da Parlett'te bagh-chal maddesi
2. 5×5 köşegenli tahta, 4 kaplan / 20 keçi, yerleştirme aşaması, atlama-alma, kaplanların kilitlenmesi, kaç keçi kaybı kaplan galibiyeti

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Nepal kaynaklı çağdaş bir künye ile birlikte olursa kültür atfı da güçlenir.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/bagh-chal/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"bagh chal" rules tigers goats Nepal board game`
- `bagh-chal Nepali traditional game rules ethnography`

---

### 4 · Kōnane

| | |
|---|---|
| **GAME ID** | `konane` |
| **TITLE** | Kōnane |
| **ALTERNATE NAME(S)** | Hawaiian checkers |
| **CULTURE** | Hawaiian |
| **REGION** | Oceania · Hawai'i |
| **FAMILY** | The War Board |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED · `P5` CULTURAL IDENTITY / ATTRIBUTION UNRESOLVED |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `attributed` · öncelik C · puan 20.4 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye KAMUSAL ALANDADIR ama yalnızca JSTOR nüshası bulundu ve tam metin indirilemedi; ikinci künye (Bell) engelli. Oyun `attributed` taranmıştır: Hawaii atfı ZORUNLUDUR ve kayıt ÇAĞDAŞ Kānaka Maoli kaynaklı bir künye istiyor.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Culin 1899 · 'Hawaiian Games', American Anthropologist 1:2 — yalnızca JSTOR nüshası, tam metin indirilemedi (Batch 4 avı)
- Culin 1898 · Chess and Playing-Cards AÇILDI (pachisi ve patolli buradan doğrulandı) — kōnane maddesi taranmadı
- Bell proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Culin, Stewart, 'Hawaiian Games', American Anthropologist 1:2 (1899)
- Bell, R. C., Board and Table Games from Many Civilizations (Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)

**WHAT WAS MISSING**

Culin'in kōnane bölümü ve çağdaş Hawaii atfı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Culin, Stewart, 'Hawaiian Games', American Anthropologist 1:2 (1899) — kōnane bölümü, SAYFA NUMARASIYLA (KAMUSAL ALAN; ciltli dergi taraması aranmalı — proje bu makalenin sayfa aralığını henüz görmedi)
2. Tahta ölçüsü, ilk iki taşın kaldırılması, YALNIZCA atlayarak alma, çoklu atlama kuralı ve hamlesiz kalanın kaybetmesi
3. ÇAĞDAŞ Kānaka Maoli kaynaklı bir künye — atıf zorunluluğu için (Bishop Museum · Hawaiian kültür kurumları)

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — American Anthropologist cilt 1 (1899) taraması + Bishop Museum kaydı.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/konane/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Culin "Hawaiian Games" American Anthropologist 1899 archive.org`
- `American Anthropologist volume 1 1899 full text HathiTrust`
- `konane Hawaiian checkers rules Bishop Museum`

---

### 5 · Yoté

| | |
|---|---|
| **GAME ID** | `yote` |
| **TITLE** | Yoté |
| **ALTERNATE NAME(S)** | Yote, Choko (related) |
| **CULTURE** | Wolof |
| **REGION** | West Africa · Senegal · Gambia · Mali |
| **FAMILY** | The War Board |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `open` · öncelik C · puan 20.4 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye Dakar basımı dar dağıtımlı bir eserdir ve HİÇ DENENMEDİ; ikinci künye (Zaslavsky) engelli.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Béart 1955 · Mémoires de l'IFAN 42 — HİÇ denenmedi
- Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Béart, Charles, Jeux et jouets de l'Ouest africain, Mémoires de l'IFAN 42 (Dakar: IFAN, 1955), 2 cilt
- Zaslavsky, Claudia, Africa Counts: Number and Pattern in African Culture (Boston: Prindle, Weber & Schmidt, 1973)

**WHAT WAS MISSING**

Béart'ın yoté kaydı — özellikle ÇİFT ALMA kuralı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Béart, Charles, Jeux et jouets de l'Ouest africain (Dakar: IFAN, 1955) — yoté bölümü (Fransızca)
2. 5×6 ızgara, elde tutulan taşların sırayla girmesi, atlayarak alma ve ALINAN HER TAŞLA BİRLİKTE İKİNCİ BİR TAŞIN DA KALDIRILMASI kuralı — oyunun ayırt edici mekaniği budur (distinct=5)
3. Wolof atfını veren bir kaynak

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Béart 1955 — Batı Afrika oyunlarının en iyi saha kaydı; zamma ile AYNI kaynak, tek teslim iki oyun açar.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/yote/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Béart "Jeux et jouets de l'Ouest africain" IFAN 1955 PDF`
- `"yoté" OR "yote" Wolof Senegal game rules double capture`
- `jeux ouest africain yoté règles IFAN Dakar`

---

### 6 · Ampe

| | |
|---|---|
| **GAME ID** | `ampe` |
| **TITLE** | Ampe |
| **ALTERNATE NAME(S)** | Ampe (Ghana) |
| **CULTURE** | Akan |
| **REGION** | West Africa · Ghana |
| **FAMILY** | Games Without a Board |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | `P2` SOURCE TEXT UNAVAILABLE |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 19.8 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Zaslavsky, Claudia, Africa Counts: Number and Pattern in African Culture (Boston: Prindle, Weber & Schmidt, 1973)

**WHAT WAS MISSING**

Zaslavsky bu oyunun TEK künyesidir; açılamadığı için ne kural ne de ikinci bağımsız kaynak vardır.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Zaslavsky 1973'te ampe maddesi — sıçrama/ayak biçimi, puanlama, tur, bitiş
2. GANA KAYNAKLI ikinci bağımsız künye (Akan çocuk oyunları derlemesi)

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/ampe/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"ampe" Ghana game rules`
- `"ampe" Akan children's game ethnography`

---

### 7 · Pilolo

| | |
|---|---|
| **GAME ID** | `pilolo` |
| **TITLE** | Pilolo |
| **ALTERNATE NAME(S)** | Time to search for |
| **CULTURE** | Ga |
| **REGION** | West Africa · Ghana |
| **FAMILY** | Games Without a Board |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | `P2` SOURCE TEXT UNAVAILABLE |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 19.8 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Zaslavsky, Claudia, Africa Counts: Number and Pattern in African Culture (Boston: Prindle, Weber & Schmidt, 1973)

**WHAT WAS MISSING**

Zaslavsky bu oyunun TEK künyesidir; ne kural ne ikinci bağımsız kaynak var.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Zaslavsky 1973'te pilolo maddesi — saklama/arama sırası, puanlama, bitiş
2. GANA KAYNAKLI ikinci bağımsız künye (Ga çocuk oyunları)

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/pilolo/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"pilolo" Ghana Ga children's game rules`
- `Ga people traditional children games Ghana ethnography`

---

### 8 · Adji-boto

| | |
|---|---|
| **GAME ID** | `adji-boto` |
| **TITLE** | Adji-boto |
| **ALTERNATE NAME(S)** | Adji |
| **CULTURE** | Ndyuka Maroon |
| **REGION** | South America · Suriname |
| **FAMILY** | The Sowing Games |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `attributed` · öncelik C · puan 19.6 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye 1932 tarihli bir antropoloji dergisidir ve HİÇ DENENMEDİ; ikinci künye (Russ 2000) engelli. Oyun `attributed` taranmıştır: Ndyuka Maroon atfı ZORUNLUDUR.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Herskovits 1932 · JRAI 62 — HİÇ denenmedi
- Russ 2000 proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Uzmanlık makaleleri — tek oyunu açan dar künyeler
- Russ, Laurence, The Complete Mancala Games Book (New York: Marlowe & Company, 2000)

**WHAT WAS MISSING**

Çukur dizilimi, ekim yönü, alma kuralı ve Ndyuka bağlamı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Herskovits, Melville J., 'Wari in the New World', Journal of the Royal Anthropological Institute 62 (1932) — makalenin tamamı
2. Ndyuka Maroon topluluğunun oyunla ilişkisini veren çağdaş bir kaynak (atıf zorunluluğu için)

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — 1932 makalesi kamusal alanda olabilir; JRAI ciltli sayısı ideal.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/adji-boto/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Herskovits "Wari in the New World" JRAI 1932 PDF`
- `"adji boto" Ndyuka Maroon Suriname game rules`

---

### 9 · Congklak

| | |
|---|---|
| **GAME ID** | `congklak` |
| **TITLE** | Congklak |
| **ALTERNATE NAME(S)** | Congkak, Dakon |
| **CULTURE** | Javanese |
| **REGION** | Southeast Asia · Indonesia · Malaysia |
| **FAMILY** | The Sowing Games |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 19.6 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 ve Russ 2000 proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)
- Russ, Laurence, The Complete Mancala Games Book (New York: Marlowe & Company, 2000)

**WHAT WAS MISSING**

İki künyenin ikisi de engelli.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray 1952 ya da Russ 2000'de congklak/congkak/dakon maddesi
2. Çukur sayısı, depo (rumah) kuralı, eş zamanlı başlangıç olup olmadığı, ekim yönü, alma, tur sonu ve yeniden dizme kuralı
3. KARAR MALZEMESİ: sungka ile mekanik farkı — kitap ikisini ayrı madde yapacaksa farkı yazmalı

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/congklak/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"congklak" OR "congkak" OR "dakon" Javanese mancala rules`
- `congkak Malay Indonesian sowing game rules ethnography`

---

### 10 · Shisima

| | |
|---|---|
| **GAME ID** | `shisima` |
| **TITLE** | Shisima |
| **ALTERNATE NAME(S)** | Esisima |
| **CULTURE** | Luhya |
| **REGION** | East Africa · western Kenya |
| **FAMILY** | The Line and the Territory |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | `P2` SOURCE TEXT UNAVAILABLE |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 19.6 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Zaslavsky, Claudia, Africa Counts: Number and Pattern in African Culture (Boston: Prindle, Weber & Schmidt, 1973)

**WHAT WAS MISSING**

Zaslavsky bu oyunun TEK künyesidir; ne kural ne ikinci bağımsız kaynak var.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Zaslavsky 1973'te shisima maddesi — sekizgen tahta, 3'er taş, hareket kısıtı, üçlü sıra, bitiş
2. KENYA KAYNAKLI ikinci bağımsız künye (Luhya)

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/shisima/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"shisima" Luhya Kenya game rules octagon`
- `shisima Kenyan traditional game three in a row`

---

### 11 · Sungka

| | |
|---|---|
| **GAME ID** | `sungka` |
| **TITLE** | Sungka |
| **ALTERNATE NAME(S)** | Sungkaan |
| **CULTURE** | Visayan |
| **REGION** | Southeast Asia · Philippines |
| **FAMILY** | The Sowing Games |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `open` · öncelik A · puan 19.6 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye 1900 tarihli bir dergi makalesidir — KAMUSAL ALANDADIR — ama proje onu HİÇ DENEMEDİ; ikinci künye (Murray 1952) engelli.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Culin 1900 · 'Philippine Games', American Anthropologist 2:4 — HİÇ denenmedi (AYNI derginin 1899 Hawaiian sayısı denendi ve yalnızca JSTOR nüshası bulundu)
- Murray 1952 DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900)
- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)

**WHAT WAS MISSING**

Culin'in sungka bölümü — çukur sayısı, depo kuralı, ekim yönü, alma.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900) — sungka bölümü, SAYFA NUMARASIYLA (proje bu makalenin sayfa aralığını henüz görmedi ve tahmin etmiyor)
2. KARAR MALZEMESİ: congklak ile mekanik farkı — varyant kutusuna mı sığar, ayrı madde mi olmalı?

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — American Anthropologist cilt 2 (1900) ciltli sayısının taraması — kamusal alandadır ve archive.org/HathiTrust'ta olması beklenir.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/sungka/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Culin "Philippine Games" American Anthropologist 1900 archive.org`
- `American Anthropologist volume 2 1900 full text archive`
- `"sungka" Visayan Philippine mancala rules Culin`

---

### 12 · Aadu Puli Attam

| | |
|---|---|
| **GAME ID** | `aadu-puli-attam` |
| **TITLE** | Aadu Puli Attam |
| **ALTERNATE NAME(S)** | Puli Meka, Goats and Tigers |
| **CULTURE** | Tamil |
| **REGION** | South Asia · Tamil Nadu, India |
| **FAMILY** | The Hunt and the Siege |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | `P4` GAME IDENTITY UNRESOLVED |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 19.5 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Bell ve Murray 1952 proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Bell, R. C., Board and Table Games from Many Civilizations (Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)
- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)

**WHAT WAS MISSING**

İki künyenin ikisi de engelli; kural metni elde yok.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Bell ya da Murray 1952'de aadu puli attam / puli meka maddesi
2. Tahta çizimi (üçgen ızgara), keçi ve kaplan sayıları, yerleştirme aşaması, atlama-alma kuralı, kaplanın kilitlenme koşulu

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Bir madde ki hem tahtayı hem de KAPLAN KİLİTLENMESİ koşulunu versin — Bagh-Chal ile farkı buradadır ve kitap iki maddeyi ayırmak için bu farkı yazmak zorundadır.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/aadu-puli-attam/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"aadu puli attam" rules board tigers goats Tamil`
- `"puli meka" game rules South India`

---

### 13 · Bul

| | |
|---|---|
| **GAME ID** | `bul` |
| **TITLE** | Bul |
| **ALTERNATE NAME(S)** | Buul, Boolik |
| **CULTURE** | Kekchi Maya |
| **REGION** | Mesoamerica · Guatemala · Belize |
| **FAMILY** | The Race Home |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `attributed` · öncelik C · puan 19.5 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye bir hakemli dergi makalesidir ve HİÇ DENENMEDİ; ikinci künye (Bell) engelli. Oyun `attributed` taranmıştır: Kekchi Maya atfı ZORUNLUDUR.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Verbeeck 1998 · Board Game Studies 1 — HİÇ denenmedi
- Bell proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Uzmanlık makaleleri — tek oyunu açan dar künyeler
- Bell, R. C., Board and Table Games from Many Civilizations (Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)

**WHAT WAS MISSING**

Makale metni: iz uzunluğu, mısır tanesi atışı, çarpışma/öldürme kuralı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Verbeeck, Lieve, 'Bul: A Patolli Game in Maya Lowland', Board Game Studies 1 (1998) — makalenin tamamı
2. Kekchi Maya atfını ve çağdaş bağlamı veren bir kaynak

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Board Game Studies cilt 1 PDF'i — dergi eski sayılarını açık arşivde tutuyor olabilir.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/bul/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Verbeeck "Bul" Patolli Maya Board Game Studies 1998 PDF`
- `"bul" OR "boolik" Kekchi Maya game rules`

---

### 14 · Li'b el-Merafib

| | |
|---|---|
| **GAME ID** | `li-b-el-merafib` |
| **TITLE** | Li'b el-Merafib |
| **ALTERNATE NAME(S)** | The Hyena Game, Li'b el-Akil |
| **CULTURE** | Sudanese Arab |
| **REGION** | North-East Africa · Sudan |
| **FAMILY** | The Race Home |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `open` · öncelik C · puan 19.5 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye 1925 tarihli bir bölgesel dergidir ve HİÇ DENENMEDİ; ikinci künye (Bell) engelli.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Davies 1925 · Sudan Notes and Records 8 — HİÇ denenmedi
- Bell proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Uzmanlık makaleleri — tek oyunu açan dar künyeler
- Bell, R. C., Board and Table Games from Many Civilizations (Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)

**WHAT WAS MISSING**

Sarmal izin uzunluğu, sırtlan ve anne taşlarının kuralı, kuyu kuralı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Davies, R., 'Some Arab Games and Puzzles', Sudan Notes and Records 8 (1925) — makalenin tamamı
2. Sarmal iz, 'anne' taşı, sırtlanın serbest kalma koşulu ve kuyuya varma kuralı

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — 1925 tarihli makale kamusal alanda olabilir; ciltli dergi taraması ideal.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/li-b-el-merafib/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Davies "Some Arab Games and Puzzles" Sudan Notes Records 1925`
- `"hyena game" Sudan spiral race game rules`
- `"li'b el merafib" rules`

---

### 15 · Dama

| | |
|---|---|
| **GAME ID** | `turkish-dama` |
| **TITLE** | Dama |
| **ALTERNATE NAME(S)** | Turkish draughts |
| **CULTURE** | Turkish |
| **REGION** | Anatolia · Eastern Mediterranean · Türkiye |
| **FAMILY** | The War Board |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 19.4 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 ve Parlett proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)
- Parlett, David, The Oxford History of Board Games (Oxford: Oxford University Press, 1999)

**WHAT WAS MISSING**

İki künyenin ikisi de engelli.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray 1952 ya da Parlett'te Turkish draughts maddesi — 8×8 tahta, 16'şar taş İKİNCİ ve ÜÇÜNCÜ sırada, taşların İLERİ VE YANA gitmesi (köşegen DEĞİL), dama taşının uzun menzili, alma zorunluluğu
2. Anadolu kaynaklı bir dönem kaydı

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Osmanlı/Türk kaynaklı bir dönem kaydı kültür künyesini güçlendirir.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/turkish-dama/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Turkish draughts dama rules orthogonal capture`
- `Türk daması kuralları tarihi kaynak`
- `Murray Turkish draughts rules 1952`

---

### 16 · Pétanque

| | |
|---|---|
| **GAME ID** | `petanque` |
| **TITLE** | Pétanque |
| **ALTERNATE NAME(S)** | Boules, Jeu provençal (related) |
| **CULTURE** | Provençal |
| **REGION** | Western Europe · Provence, France |
| **FAMILY** | Games Without a Board |
| **PRIMARY BLOCKER** | `P8` — SOURCE LOCATOR MISSING |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `open` · öncelik A · puan 18.8 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni yayımlanmıştır ve erişilebilir; eksik olan PROJE STANDARDIDIR: künye (baskı · yıl · madde numarası) ve bağımsız ikinci kaynak. 'Geleneksel' etiketi 1907 kodifikasyonu yüzünden gerekçe ister.

**WHAT HAS ALREADY BEEN CHECKED**

- Parlett 1999 telif altında
- FIPJP kural kitabı HİÇ DENENMEDİ

**WHAT SOURCE WAS ATTEMPTED**

- Yaşayan federasyon/kodifikasyon kuralları
- Parlett, David, The Oxford History of Board Games (Oxford: Oxford University Press, 1999)

**WHAT WAS MISSING**

FIPJP kural kitabının sürüm künyesi ve oyunun tarihsel çerçevesini veren bağımsız bir kaynak.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. FIPJP resmî kural kitabı — SÜRÜM, yürürlük tarihi ve madde numaraları
2. Pétanque'ın 1907 La Ciotat kökenini veren bağımsız tarihsel künye
3. Jeu provençal ile pétanque arasındaki farkı söyleyen bir kaynak

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] scoring  [ ] end condition  [ ] variants
SOURCE EVIDENCE
  [ ] title  [ ] edition  [ ] publication year  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] historical context
```

**IDEAL EVIDENCE** — FIPJP kural kitabının PDF'i (sürüm ve tarih görünür) + bir spor tarihi çalışmasının pétanque bölümü.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/petanque/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `FIPJP official rules of petanque PDF version`
- `petanque 1907 La Ciotat origin history jeu provençal`

---

### 17 · Gebeta

| | |
|---|---|
| **GAME ID** | `gebeta` |
| **TITLE** | Gebeta |
| **ALTERNATE NAME(S)** | Gabata, Gebet'a |
| **CULTURE** | Amhara |
| **REGION** | Horn of Africa · Ethiopia |
| **FAMILY** | The Sowing Games |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `open` · öncelik C · puan 18.6 |

**WHY THE AGENT CANNOT WRITE IT**

İki künyenin ikisi de hakemli dergi makalesidir ve İKİSİ DE HİÇ DENENMEDİ. Bu oyun kayıtta engelli KANITI olmayan az sayıdaki maddeden biridir.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Pankhurst 1971 · Ethiopia Observer 14 — HİÇ denenmedi
- Townshend 1979 · Azania 14 — HİÇ denenmedi

**WHAT SOURCE WAS ATTEMPTED**

- Uzmanlık makaleleri — tek oyunu açan dar künyeler
- Townshend, Philip, 'Mankala in Eastern and Southern Africa: A Distributional Analysis', Azania: Journal of the British Institute in Eastern Africa 14 (1979)

**WHAT WAS MISSING**

Gabata biçimlerinin hangisinin basılacağı ve o biçimin kural metni.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Pankhurst, Richard, 'Gabata and Related Board Games of Ethiopia and the Horn of Africa', Ethiopia Observer 14 (1971) — makalenin tamamı
2. Townshend 1979 · Azania 14 — ikinci bağımsız kaynak olarak
3. ⚠ Kayıt uyarıyor: kaya oyulmuş tahtaların TARİHLENDİRMESİ tartışmalıdır; kitap kesin tarih VERMEYECEK — kaynak bunu desteklemeli

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Pankhurst makalesi + Amhara atfını veren çağdaş bir kaynak.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/gebeta/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Pankhurst "Gabata" Ethiopia Observer 1971 board games`
- `"gebeta" OR "gabata" Ethiopian mancala rules Amhara`
- `Townshend Mankala Eastern Southern Africa Azania 1979`

---

### 18 · Go

| | |
|---|---|
| **GAME ID** | `go` |
| **TITLE** | Go |
| **ALTERNATE NAME(S)** | Weiqi, Baduk, Igo |
| **CULTURE** | Han Chinese |
| **REGION** | East Asia · China · Korea · Japan |
| **FAMILY** | The Line and the Territory |
| **PRIMARY BLOCKER** | `P5` — CULTURAL IDENTITY / ATTRIBUTION UNRESOLVED |
| **SECONDARY BLOCKERS** | `P7` VARIANT CONFLICT |
| **CURRENT STATUS** | `UNRESOLVED` · kısıt taraması: `open` · öncelik C · puan 18.6 |

**WHY THE AGENT CANNOT WRITE IT**

KAYNAK TAM AMA KÜLTÜR UYUŞMUYOR. Smith 1908 (ss. 24–26) EKSİKSİZ bir kural kitabıdır — sıra, yerleştirme, ko, taşların bir daha oynanmaması, toprak amacı — ama JAPON kodifikasyonunu ve JAPON SAYIMINI (alınan taşlarla toprağı doldurma) verir, Çin ALAN sayımını değil. Kapsam kaydı HAN ÇİNLİSİ der. § 9'un 'kaynak iddia edilen kültürü desteklemeli' şartı KARŞILANMIYOR.

**WHAT HAS ALREADY BEEN CHECKED**

- Smith 1908 'Rules of Play' ss. 24–26 AÇILDI ve TAM kural seti doğrulandı
- Falkener 1892 Bölüm XXIII ss. 239–240 AÇILDI: 19×19, taşlar konduktan sonra hareket etmez, bağlantı yalnızca çizgi boyunca
- Murray 1952 · Parlett 1999 · Shotwell 2003 — üçü de erişilemedi
- Culin 1895 tarandı — Çin biçimi için kural seti yok

**WHAT SOURCE WAS ATTEMPTED**

- Volpicelli, Z., 'Wei-ch'i', Journal of the China Branch of the Royal Asiatic Society, N.S. XXVI (1894)
- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)

**WHAT WAS MISSING**

ÇİN biçimini ve ÇİN ALAN SAYIMINI veren bir kaynak.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Volpicelli, Z., 'Wei-ch'i', Journal of the China Branch of the Royal Asiatic Society N.S. XXVI (1894) — Smith'in KENDİ künyesinde geçiyor
2. Ya da: Çin alan sayımını (taş + çevrelenen boş kesişim) veren başka herhangi bir denetlenebilir kaynak
3. ⚠ ALTERNATİF ÇÖZÜM — KURUCU KARARI: maddenin kültür künyesi JAPON olarak değiştirilirse Smith 1908 ZATEN YETERLİDİR ve oyun BUGÜN yazılır. Bu bir araştırma değil bir karardır.
4. KARAR MALZEMESİ: kitap 9×9 mı 19×19 mu basacak? 650 kelimede 19×19 öğretilemez; 9×9 seçimi EDİTORYALDİR ve gerekçesi yazılmalıdır

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] scoring
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Volpicelli makalesi — hem Çin biçimini hem Çin sayımını verir ve kültür uyuşmazlığını tek hamlede kapatır.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/go/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Volpicelli "Wei-chi" Journal China Branch Royal Asiatic Society 1894`
- `weiqi Chinese area scoring rules 19th century source`
- `wei-ch'i Chinese go rules historical article archive.org`

---

### 19 · Hus

| | |
|---|---|
| **GAME ID** | `hus` |
| **TITLE** | Hus |
| **ALTERNATE NAME(S)** | ǁHus, Ohus |
| **CULTURE** | Nama |
| **REGION** | Southern Africa · Namibia |
| **FAMILY** | The Sowing Games |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `attributed` · öncelik C · puan 18.6 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye (Murray 1952) engelli; ikincisi (Townshend 1979) HİÇ DENENMEDİ. Oyun `attributed` taranmıştır: Nama atfı ZORUNLUDUR.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 DENENDİ ve açılamadı
- Townshend 1979 — HİÇ denenmedi

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)
- Townshend, Philip, 'Mankala in Eastern and Southern Africa: A Distributional Analysis', Azania: Journal of the British Institute in Eastern Africa 14 (1979)

**WHAT WAS MISSING**

Dört sıralı tahtanın kural metni ve Nama bağlamı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray 1952 ya da Townshend 1979'da hus/ǁhus maddesi — dört sıra, ekim yönü, alma koşulu, bitiş
2. Nama topluluğu atfını veren bir kaynak (atıf zorunluluğu için)

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/hus/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"hus" Nama mancala four row rules Namibia`
- `Townshend Mankala Azania 1979 hus ohus`

---

### 20 · Morabaraba

| | |
|---|---|
| **GAME ID** | `morabaraba` |
| **TITLE** | Morabaraba |
| **ALTERNATE NAME(S)** | Umlabalaba, Mmela |
| **CULTURE** | Sotho |
| **REGION** | Southern Africa · Lesotho · South Africa |
| **FAMILY** | The Line and the Territory |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `attributed` · öncelik A · puan 18.6 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz. Oyun `attributed` taranmıştır: Sotho atfı ZORUNLUDUR.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Zaslavsky 1973 ve Murray 1952 proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Zaslavsky, Claudia, Africa Counts: Number and Pattern in African Culture (Boston: Prindle, Weber & Schmidt, 1973)
- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)

**WHAT WAS MISSING**

Kural metni ve Sotho atfı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Zaslavsky 1973 ya da Murray 1952'de morabaraba/umlabalaba maddesi
2. 12'şer taş, köşegenli morris tahtası, değirmen kuralı, 'uçma' kuralı (üç taşa düşünce serbest hamle) ve bitiş
3. Sotho topluluğu atfını veren bir kaynak
4. KARAR MALZEMESİ: twelve-mens-morris ile AYNI tahta — kitap ikisini birden basarsa tekrar riski ciddidir

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/morabaraba/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"morabaraba" Sotho rules twelve pieces mill game`
- `"umlabalaba" OR "mmela" Southern Africa morris rules`

---

### 21 · Omweso

| | |
|---|---|
| **GAME ID** | `omweso` |
| **TITLE** | Omweso |
| **ALTERNATE NAME(S)** | Mweso |
| **CULTURE** | Ganda |
| **REGION** | East Africa · Uganda |
| **FAMILY** | The Sowing Games |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `attributed` · öncelik C · puan 18.6 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye 1968 tarihli dar dağıtımlı bir monografidir ve HİÇ DENENMEDİ; üçüncü künye (Russ 2000) engelli. Oyun `attributed` taranmıştır: Ganda atfı ZORUNLUDUR.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Nsimbi 1968 — HİÇ denenmedi
- Townshend 1979 — HİÇ denenmedi
- Russ 2000 DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Uzmanlık makaleleri — tek oyunu açan dar künyeler
- Townshend, Philip, 'Mankala in Eastern and Southern Africa: A Distributional Analysis', Azania: Journal of the British Institute in Eastern Africa 14 (1979)
- Russ, Laurence, The Complete Mancala Games Book (New York: Marlowe & Company, 2000)

**WHAT WAS MISSING**

Dört sıralı tahtanın tam kural metni — omweso alma kuralları karmaşıktır.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Nsimbi, M. B., Omweso: A Game People Play in Uganda (Los Angeles: UCLA African Studies Center, 1968) — kural bölümü
2. Başlangıç dizilimi, ekim yönü, alma koşulu, emitwe (özel hamle) kuralı, bitiş
3. Ganda atfını veren çağdaş bir kaynak

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Nsimbi 1968 — oyunun en yetkili tek kaynağıdır ve UCLA yayınıdır.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/omweso/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Nsimbi "Omweso: A Game People Play in Uganda" 1968 PDF`
- `"omweso" OR "mweso" Ganda Uganda mancala rules four row`

---

### 22 · Shax

| | |
|---|---|
| **GAME ID** | `shax` |
| **TITLE** | Shax |
| **ALTERNATE NAME(S)** | Jare, Shantarad |
| **CULTURE** | Somali |
| **REGION** | Horn of Africa · Somalia · Somaliland · Djibouti |
| **FAMILY** | The Line and the Territory |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 18.6 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz. Kayıt ayrıca SOMALİ KAYNAKLI çağdaş bir künye istiyor.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 ve Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)
- Zaslavsky, Claudia, Africa Counts: Number and Pattern in African Culture (Boston: Prindle, Weber & Schmidt, 1973)

**WHAT WAS MISSING**

Kural metni ve Somali kaynaklı künye.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray 1952 ya da Zaslavsky 1973'te shax/jare maddesi
2. 12'şer taş, yerleştirme aşaması, ilk değirmenin ÖZEL kuralı, kaydırma aşaması, bitiş
3. Somali kaynaklı çağdaş bir künye

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/shax/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"shax" Somali game rules twelve pieces`
- `"jare" OR "shantarad" Somali board game rules`

---

### 23 · Tapatan

| | |
|---|---|
| **GAME ID** | `tapatan` |
| **TITLE** | Tapatan |
| **ALTERNATE NAME(S)** | Three Men's Morris (Philippines) |
| **CULTURE** | Tagalog |
| **REGION** | Southeast Asia · Philippines |
| **FAMILY** | The Line and the Territory |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 18.6 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye 1900 tarihli bir dergi makalesidir — KAMUSAL ALANDADIR — ama açık nüshası bulunmadı; ikinci künye (Murray 1952) engelli.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Culin 1900 · 'Philippine Games' — açık nüsha bulunamadı; AYNI derginin 1899 sayısı denendi ve yalnızca JSTOR nüshası çıktı
- Murray 1952 DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900)
- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)

**WHAT WAS MISSING**

Culin'in tapatan bölümü.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900) — tapatan bölümü, sayfa numarasıyla
2. KARAR MALZEMESİ: kitapta ZATEN achi ve picaria var ve nine-holes yazılabilir durumda. Kayıt uyarıyor: 'kitapta en fazla üç üç-taş oyunu olmalı'. Bu maddenin yerine bir yedek düşünülebilir

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — American Anthropologist cilt 2 (1900) taraması — sungka ile AYNI kaynak, tek teslim iki oyun açar.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/tapatan/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Culin "Philippine Games" American Anthropologist 1900 tapatan`
- `American Anthropologist volume 2 1900 archive.org full text`

---

### 24 · Toguz Kumalak

| | |
|---|---|
| **GAME ID** | `toguz-kumalak` |
| **TITLE** | Toguz Kumalak |
| **ALTERNATE NAME(S)** | Toguz Korgool, Togyz Kumalak |
| **CULTURE** | Kazakh |
| **REGION** | Central Asia · Kazakhstan · Kyrgyzstan |
| **FAMILY** | The Sowing Games |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | `P7` VARIANT CONFLICT |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik D · puan 18.6 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz. Ayrıca MODERN SPOR KURALLARI ile 19. yüzyıl derlemeleri arasındaki fark ÖLÇÜLMEMİŞTİR ve kitabın hangisini basacağı belirsizdir.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Russ 2000 ve de Voogt 1997 proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Russ, Laurence, The Complete Mancala Games Book (New York: Marlowe & Company, 2000)
- de Voogt, Alex, Mancala Board Games (London: British Museum Press, 1997)

**WHAT WAS MISSING**

Kural metni ve hangi kural katmanının (dönem mi, modern spor mu) basılacağı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Russ 2000 ya da de Voogt 1997'de toguz kumalak maddesi — 2×9 çukur, 9'ar tohum, tuzdyk (kutsal çukur) kuralı, kazan, alma koşulu, bitiş
2. 19. yüzyıl bir Orta Asya kaydı — modern spor kodifikasyonuyla FARKI ölçmek için
3. Kazak atfını veren bir kaynak

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Hem dönem kaydını hem modern kodifikasyonu tartışan bir çalışma.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/toguz-kumalak/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"toguz kumalak" OR "togyz kumalak" rules tuzdyk Kazakh`
- `toguz korgool Kyrgyz Kazakh mancala historical rules`

---

### 25 · Ashta Kashte

| | |
|---|---|
| **GAME ID** | `ashta-kashte` |
| **TITLE** | Ashta Kashte |
| **ALTERNATE NAME(S)** | Ashta-kashte |
| **CULTURE** | Bengali |
| **REGION** | South Asia · Bengal |
| **FAMILY** | The Race Home |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 18.5 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 ve Bell proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)
- Bell, R. C., Board and Table Games from Many Civilizations (Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)

**WHAT WAS MISSING**

İki künyenin ikisi de engelli.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray 1952 ya da Bell'de ashta-kashte maddesi
2. 7×7 tahta, işaretli güvenli kareler, dört kavrukemik/deniz kabuğu atışı, iz yönü, alma, eve giriş koşulu

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/ashta-kashte/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"ashta kashte" Bengali race game rules board`
- `ashtapada cowrie race game Bengal rules`

---

### 26 · Daldøs

| | |
|---|---|
| **GAME ID** | `daldos` |
| **TITLE** | Daldøs |
| **ALTERNATE NAME(S)** | Daldøsa, Sáhkku (related) |
| **CULTURE** | Danish |
| **REGION** | Northern Europe · Jutland, Denmark · south-west Norway |
| **FAMILY** | The Race Home |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `open` · öncelik C · puan 18.5 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye bir dergi çalışmasıdır ve HİÇ DENENMEDİ; ikinci künye (Parlett) engelli.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Michaelsen · Board Game Studies — HİÇ denenmedi
- Parlett proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Uzmanlık makaleleri — tek oyunu açan dar künyeler
- Parlett, David, The Oxford History of Board Games (Oxford: Oxford University Press, 1999)

**WHAT WAS MISSING**

Kural metni: tahta biçimi, dört yüzlü çubuk zar, taş hareketi, alma.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Michaelsen, Peter — daldøs ve ilgili kuzey yarış oyunları üzerine Board Game Studies makalesi
2. Daldøs ile Sámi sáhkku arasındaki ilişkiyi TARTIŞAN ama KÖKEN İDDİASI YAPMAYAN bir kaynak (kayıt bu iddiayı açıkça yasaklıyor)

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Board Game Studies makalesi PDF'i + Danimarka müze nesne kaydı.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/daldos/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Michaelsen daldøs Board Game Studies PDF`
- `"daldøs" OR "daldosa" game rules Denmark`
- `sáhkku daldøs Nordic race game scholarship`

---

### 27 · The Game of the Goose

| | |
|---|---|
| **GAME ID** | `game-of-the-goose` |
| **TITLE** | The Game of the Goose |
| **ALTERNATE NAME(S)** | Giuoco dell'Oca, Jeu de l'oie |
| **CULTURE** | Italian |
| **REGION** | Southern Europe · Italy |
| **FAMILY** | The Race Home |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `open` · öncelik E · puan 17.5 |

**WHY THE AGENT CANNOT WRITE IT**

Her iki künye de telif altındadır; biri (Parlett) DENENDİ ve açılamadı, öteki (Seville 2019) hiç denenmedi.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Parlett DENENDİ ve açılamadı
- Seville 2019 — HİÇ denenmedi

**WHAT SOURCE WAS ATTEMPTED**

- Parlett, David, The Oxford History of Board Games (Oxford: Oxford University Press, 1999)
- Uzmanlık makaleleri — tek oyunu açan dar künyeler

**WHAT WAS MISSING**

Kanonik 63 haneli izin hane hane anlamı ve ceza kuralları.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Seville, Adrian, The Cultural Legacy of the Royal Game of the Goose (Amsterdam University Press, 2019) — AUP başlıklarının bir bölümü AÇIK ERİŞİMLİDİR
2. 63 hanenin kanonik listesi: kaz haneleri, köprü, han, kuyu, labirent, hapishane, ölüm ve her birinin cezası
3. Fazla atışın geri sayılması kuralı

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — AUP açık erişim PDF'i ya da bir dönem oyun tahtasının müze künyesi + basılı kural metni.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/game-of-the-goose/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Seville "Cultural Legacy of the Royal Game of the Goose" open access PDF`
- `"game of the goose" 63 spaces rules historical`
- `giuoco dell'oca regole storiche 63`

---

### 28 · Len Choa

| | |
|---|---|
| **GAME ID** | `len-choa` |
| **TITLE** | Len Choa |
| **ALTERNATE NAME(S)** | Leopard game (Thai) |
| **CULTURE** | Thai |
| **REGION** | Southeast Asia · Thailand |
| **FAMILY** | The Hunt and the Siege |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | `P2` SOURCE TEXT UNAVAILABLE |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 17.5 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Bell proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Bell, R. C., Board and Table Games from Many Civilizations (Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)

**WHAT WAS MISSING**

Bell bu oyunun TEK künyesidir; ne kural ne ikinci bağımsız kaynak var.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Bell'de len choa maddesi — tahta, leopar/hayvan sayıları, hareket, alma, bitiş
2. TAYLAND KAYNAKLI ikinci bağımsız künye

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/len-choa/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"len choa" Thai leopard game rules`
- `Thai traditional board games leopard tiger rules`

---

### 29 · Nard

| | |
|---|---|
| **GAME ID** | `nard` |
| **TITLE** | Nard |
| **ALTERNATE NAME(S)** | Nardshir, Takhteh nard |
| **CULTURE** | Persian |
| **REGION** | West Asia · Iran |
| **FAMILY** | The Race Home |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `open` · öncelik C · puan 17.5 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye engelli (Murray 1952); ikinci künye bir Orta Farsça ANLATIDIR (Wizārišn ī Chatrang), kural metni değil, ve hiç denenmedi.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 DENENDİ ve açılamadı
- Wizārišn ī Chatrang ud Nihišn ī Nēw-Ardaxšīr — HİÇ denenmedi

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)

**WHAT WAS MISSING**

Nard'ın DÖNEM kural metni: tahta, taş sayısı, zar, iz yönü, alma, bitiş.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Nard'ın ORTAÇAĞ kural metni — Arapça/Farsça bir dönem kaydı ya da onu aktaran akademik bir çalışma
2. Wizārišn ī Chatrang'ın çevirisi — oyunun kozmolojik çerçevesi için (kültürel hikâye bölümüne girer)
3. KARAR MALZEMESİ: nard, tabula ve tavla kitapta ÜÇ ayrı madde mi olmalı? Kayıt tekrar riskini işaretliyor

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Bir Fars/Arap oyun tarihi çalışması ki hem kuralı hem kozmolojik çerçeveyi versin.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/nard/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"nard" Persian backgammon medieval rules text`
- `Wizarisn i Chatrang translation nard chess Middle Persian`
- `nardshir medieval Arabic backgammon rules scholarship`

---

### 30 · Rimau-rimau

| | |
|---|---|
| **GAME ID** | `rimau-rimau` |
| **TITLE** | Rimau-rimau |
| **ALTERNATE NAME(S)** | Main Rimau |
| **CULTURE** | Malay |
| **REGION** | Southeast Asia · Malaysia |
| **FAMILY** | The Hunt and the Siege |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 17.5 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 ve Bell proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)
- Bell, R. C., Board and Table Games from Many Civilizations (Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)

**WHAT WAS MISSING**

İki künyenin ikisi de engelli.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray 1952 ya da Bell'de rimau-rimau / main rimau maddesi
2. Tahta (alquerque temelli), kaplan sayısı, av taşı sayısı, çoklu alma kuralı

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Malezya kaynaklı çağdaş bir künye kültür atfını güçlendirir.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/rimau-rimau/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"rimau rimau" Malay tiger game rules`
- `"main rimau" Malaysia traditional board game`

---

### 31 · Zamma

| | |
|---|---|
| **GAME ID** | `zamma` |
| **TITLE** | Zamma |
| **ALTERNATE NAME(S)** | Sig, Kharbga (related) |
| **CULTURE** | Amazigh |
| **REGION** | North Africa · Algeria · Morocco · Sahara |
| **FAMILY** | The War Board |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED · `P7` VARIANT CONFLICT |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `attributed` · öncelik C · puan 17.4 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye (Murray 1952) engelli; ikincisi (Béart 1955) HİÇ DENENMEDİ. Ayrıca TAŞ SAYISI kaynaklara göre DEĞİŞİYOR ve kitap bir sayı seçip gerekçesini yazmak zorundadır. Oyun `attributed` taranmıştır: Amazigh atfı ZORUNLUDUR.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 DENENDİ ve açılamadı
- Béart 1955 — HİÇ denenmedi

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)
- Béart, Charles, Jeux et jouets de l'Ouest africain, Mémoires de l'IFAN 42 (Dakar: IFAN, 1955), 2 cilt

**WHAT WAS MISSING**

Kural metni ve taş sayısı çelişkisini çözecek bir künye.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray 1952 ya da Béart 1955'te zamma/sig maddesi
2. Tahta (9×9 köşegenli ızgara), taş sayısı, hareket, atlayarak alma, 'mollah' (dama) taşının menzili
3. TAŞ SAYISI için bir karar dayanağı: kaynaklar farklı sayı veriyor ve kitap birini seçip gerekçesini yazacak
4. Amazigh atfını veren bir kaynak

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/zamma/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"zamma" Berber Amazigh draughts rules North Africa`
- `"sig" OR "kharbga" North African board game rules`
- `Béart jeux ouest africain zamma sig règles`

---

### 32 · Ayòayò

| | |
|---|---|
| **GAME ID** | `ayoayo` |
| **TITLE** | Ayòayò |
| **ALTERNATE NAME(S)** | Ayo |
| **CULTURE** | Yoruba |
| **REGION** | West Africa · Nigeria |
| **FAMILY** | The Sowing Games |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `open` · öncelik E · puan 16.6 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye Nijerya basımı dar dağıtımlı bir monografidir ve HİÇ DENENMEDİ; ikinci künye (Zaslavsky) engelli.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Odeleye 1977 — HİÇ denenmedi
- Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Uzmanlık makaleleri — tek oyunu açan dar künyeler
- Zaslavsky, Claudia, Africa Counts: Number and Pattern in African Culture (Boston: Prindle, Weber & Schmidt, 1973)

**WHAT WAS MISSING**

Ayò'nun ekim ve alma kuralı ve Oware'den FARKI.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Odeleye, A. O., Ayo: A Popular Yoruba Game (Ibadan: Oxford University Press Nigeria, 1977) — kural bölümü
2. KARAR MALZEMESİ: Ayòayò ile Oware kitapta AYRI maddeler mi? Kayıt mekanik yakınlığı ve tekrar riskini işaretliyor — farkı yazan bir kaynak gerekir

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/ayoayo/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Odeleye "Ayo: A Popular Yoruba Game" 1977`
- `"ayoayo" OR "ayò" Yoruba mancala rules`

---

### 33 · Mefuvha

| | |
|---|---|
| **GAME ID** | `mefuvha` |
| **TITLE** | Mefuvha |
| **ALTERNATE NAME(S)** | Muravharavha |
| **CULTURE** | Venda |
| **REGION** | Southern Africa · Limpopo, South Africa |
| **FAMILY** | The Sowing Games |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `attributed` · öncelik E · puan 16.6 |

**WHY THE AGENT CANNOT WRITE IT**

Birincil künye (Zaslavsky) engelli; ikincisi (Townshend 1979) HİÇ DENENMEDİ. Oyun `attributed` taranmıştır: Venda atfı ZORUNLUDUR.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Zaslavsky 1973 DENENDİ ve açılamadı
- Townshend 1979 — HİÇ denenmedi

**WHAT SOURCE WAS ATTEMPTED**

- Zaslavsky, Claudia, Africa Counts: Number and Pattern in African Culture (Boston: Prindle, Weber & Schmidt, 1973)
- Townshend, Philip, 'Mankala in Eastern and Southern Africa: A Distributional Analysis', Azania: Journal of the British Institute in Eastern Africa 14 (1979)

**WHAT WAS MISSING**

Dört sıralı tahtanın kural metni ve Venda bağlamı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Zaslavsky 1973 ya da Townshend 1979'da mefuvha/muravharavha maddesi
2. Venda topluluğu atfını veren bir kaynak

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/mefuvha/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"mefuvha" OR "muravharavha" Venda game rules South Africa`
- `Venda traditional board game four row mancala`

---

### 34 · Halatafl

| | |
|---|---|
| **GAME ID** | `halatafl` |
| **TITLE** | Halatafl |
| **ALTERNATE NAME(S)** | Fox game (Icelandic) |
| **CULTURE** | Icelandic |
| **REGION** | Northern Europe · Iceland |
| **FAMILY** | The Hunt and the Siege |
| **PRIMARY BLOCKER** | `P3` — RULES INCOMPLETE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED · `P4` GAME IDENTITY UNRESOLVED |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik E · puan 16.5 |

**WHY THE AGENT CANNOT WRITE IT**

Erişilebilir kaynak AÇILDI ve oyunun yalnızca ADINI verdi: Fiske 1905'te halatafl bir SÖZLÜK GÖNDERMESİDİR, kural değil. Ayrıca oyunun fox-and-geese'ten AYRI bir madde olup olmadığı çözülmemiştir — fox-and-geese ZATEN YAZILDI ve tekrar riski gerçektir.

**WHAT HAS ALREADY BEEN CHECKED**

- Fiske 1905 'Stray Notes', s. 59 AÇILDI: terimin VARLIĞI doğrulandı, kural yok (source_verification.json, 2026-08-14)
- Fiske'in kitabındaki TEK belgelenmiş tafl oyunu tablut'tur ve o yazıldı
- Murray 1952 DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)

**WHAT WAS MISSING**

Kural metninin tamamı ve halatafl'ın fox-and-geese'ten farkı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Halatafl'ın KURALINI veren bir kaynak — tahta, taş sayıları, hareket, alma
2. İzlanda saga/sözlük geleneğinde halatafl'ın ne olduğunu söyleyen bir çalışma
3. KARAR MALZEMESİ: halatafl fox-and-geese'ten AYRI bir oyun mu? Ayrı değilse kapsam kaydı bir yedekle değiştirilmelidir

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Bir İskandinav oyun tarihi çalışması ki halatafl ile fox-and-geese ilişkisini AÇIKÇA tartışsın.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/halatafl/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"halatafl" Icelandic fox game rules`
- `halatafl saga reference fox and geese Iceland`
- `Icelandic board games hnefatafl halatafl scholarship`

---

### 35 · Jeu de Dames

| | |
|---|---|
| **GAME ID** | `jeu-de-dames` |
| **TITLE** | Jeu de Dames |
| **ALTERNATE NAME(S)** | International draughts, Polish draughts |
| **CULTURE** | French |
| **REGION** | Western Europe · France · Netherlands |
| **FAMILY** | The War Board |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik A · puan 16.4 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 ve Parlett proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)
- Parlett, David, The Oxford History of Board Games (Oxford: Oxford University Press, 1999)

**WHAT WAS MISSING**

İki künyenin ikisi de engelli.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray 1952 ya da Parlett'te international/Polish draughts maddesi — 10×10 tahta, 20'şer taş, geriye alma, dama taşının uzun menzili, AZAMİ ALMA ZORUNLULUĞU
2. Oyunun 1723 Paris kökeni ve 'Polonya daması' adının hikâyesi
3. KARAR MALZEMESİ: kayıt uyarıyor — 'okur damayı zaten biliyor; kitaba girmesi ancak Alquerque–Dama–Türk Daması hattını göstermek içinse anlamlıdır'. alquerque YAZILABİLİR durumda; hat bu maddeyle tamamlanır

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/jeu-de-dames/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `international draughts rules 10x10 majority capture history`
- `jeu de dames polonaises 1723 histoire règles`

---

### 36 · Makruk

| | |
|---|---|
| **GAME ID** | `makruk` |
| **TITLE** | Makruk |
| **ALTERNATE NAME(S)** | Thai chess |
| **CULTURE** | Thai |
| **REGION** | Southeast Asia · Thailand |
| **FAMILY** | The War Board |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | `P3` RULES INCOMPLETE |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik E · puan 16.4 |

**WHY THE AGENT CANNOT WRITE IT**

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz. Ayrıca SAYMA (nap) kuralları karmaşıktır ve tam basılırsa sayfa bütçesini zorlar (§ K19).

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1913 DENENDİ — archive.org HTTP 401 (ödünç kısıtı). Eser KAMUSAL ALANDADIR; engel telif değil DAĞITIMDIR
- Parlett proje genelinde DENENDİ ve açılamadı
- Falkener 1892 Burma satrancı bölümü AÇILDI (sittuyin yazıldı) — Siyam biçimi için ayrı kural seti vermiyor

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Chess (Oxford: Clarendon Press, 1913)
- Parlett, David, The Oxford History of Board Games (Oxford: Oxford University Press, 1999)

**WHAT WAS MISSING**

Murray 1913'ün Siyam satrancı bölümü ve sayma kurallarının basılabilir biçimi.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray, A History of Chess (1913) — Siyam satrancı bölümü (HathiTrust ya da Google Books TAM GÖRÜNÜM; eser kamusal alandadır)
2. Taşların adı ve hareketi, ERLERİN ÜÇÜNCÜ SIRADAN başlaması, erin terfi karesi, med (vezir) hareketi
3. Sayma (nap) kurallarının SADELEŞTİRİLEBİLİR bir özeti — kitap iki sayfaya sığmalı

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Murray 1913 kamusal alan tam görünümü — HathiTrust bu sınıf eserde en yüksek başarı şansını veriyor.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/makruk/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Murray "A History of Chess" 1913 HathiTrust full view Siamese`
- `makruk Thai chess rules counting nap`
- `makruk rules promotion third rank`

---

### 37 · Surakarta

| | |
|---|---|
| **GAME ID** | `surakarta` |
| **TITLE** | Surakarta |
| **ALTERNATE NAME(S)** | Permainan |
| **CULTURE** | Javanese |
| **REGION** | Southeast Asia · Indonesia |
| **FAMILY** | The War Board |
| **PRIMARY BLOCKER** | `P5` — CULTURAL IDENTITY / ATTRIBUTION UNRESOLVED |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED · `P4` GAME IDENTITY UNRESOLVED |
| **CURRENT STATUS** | `UNRESOLVED` · kısıt taraması: `open` · öncelik D · puan 16.4 |

**WHY THE AGENT CANNOT WRITE IT**

OYUNUN GELENEKSEL Mİ YOKSA 20. YÜZYIL İCADI MI OLDUĞU KESİN DEĞİLDİR. Kayıt bunu açıkça yazıyor: bu netleşmeden madde kitaba 'geleneksel' diye GİREMEZ. Ayrıca tek künyesi (Parlett) engellidir ve ikinci bağımsız kaynağı yoktur — yani hem kimlik hem kaynak açıktır.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Parlett proje genelinde DENENDİ ve açılamadı
- İkinci bağımsız kaynak Faz 1'den beri aranıyor ve bulunamadı

**WHAT SOURCE WAS ATTEMPTED**

- Parlett, David, The Oxford History of Board Games (Oxford: Oxford University Press, 1999)

**WHAT WAS MISSING**

Oyunun Java'daki geleneksel varlığına dair BİR KANIT — ya da tersi.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Surakarta'nın Java'daki geleneksel varlığını gösteren bir DÖNEM kaydı (20. yy öncesi ya da erken 20. yy saha kaydı)
2. Ya da tersi: oyunun modern bir icat/ticari yayın olduğunu gösteren bir kayıt
3. Kural metni: 8×8 ızgara, köşe halkaları, HALKADAN GEÇEREK ALMA kuralı
4. ⚠ ALTERNATİF ÇÖZÜM — KURUCU KARARI: kimlik netleşmezse madde kapsamdan çıkarılıp yedekle değiştirilebilir. Kayıt source=2 veriyor: bu kapsamın EN ZAYIF kaynak puanlarından biridir

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Java kaynaklı bir dönem saha kaydı — oyunun geleneksel olduğunu ya da OLMADIĞINI kesin söyleyen herhangi bir kanıt.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/surakarta/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `surakarta game origin traditional Javanese evidence`
- `permainan surakarta Jawa asal usul permainan tradisional`
- `surakarta board game history invented 20th century`

---

### 38 · Ephedrismos

| | |
|---|---|
| **GAME ID** | `ephedrismos` |
| **TITLE** | Ephedrismos |
| **ALTERNATE NAME(S)** | Piggyback game |
| **CULTURE** | Ancient Greek |
| **REGION** | Mediterranean · Greece |
| **FAMILY** | Games Without a Board |
| **PRIMARY BLOCKER** | `P6` — RECONSTRUCTION TOO UNCERTAIN |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik C · puan 15.8 |

**WHY THE AGENT CANNOT WRITE IT**

Yeniden kurgulama BELİRSİZDİR: kaç atış yapıldığı ve taşıma mesafesi bilinmiyor; bilinenler heykel ve vazolardan çıkarılmıştır. § 13 zayıf kanıtla yazmayı yasaklar.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Pollux Onomasticon IX — denetlenebilir açık edisyon bulunamadı
- Müze terracotta kayıtları oyunun VARLIĞINI verir, kuralını değil

**WHAT SOURCE WAS ATTEMPTED**

- Pollux, Julius, Onomasticon, Book IX — denetlenebilir modern edisyon: E. Bethe (ed.), Pollucis Onomasticon (Leipzig: Teubner, 1900–1937)

**WHAT WAS MISSING**

Atış sayısı, taşıma mesafesi ve bitiş koşulu hiçbir kaynakta yok.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Pollux IX'da ephedrismos pasajı — Yunanca metin + satır numarası
2. Oyunu bir KURAL olarak tarif eden herhangi bir antik pasaj
3. Modern bir akademik yeniden kurgulama — belirsizlik beyanıyla birlikte

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] first move  [ ] turn order  [ ] scoring  [ ] end condition
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
RECONSTRUCTION EVIDENCE
  [ ] reconstruction source  [ ] uncertainty statement  [ ] competing interpretation
```

**IDEAL EVIDENCE** — Bir klasik filoloji çalışması ya da müze sergi künyesi ki hem pasajı hem ikonografiyi tartışsın ve NE BİLİNMEDİĞİNİ söylesin.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/ephedrismos/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"ephedrismos" Greek game reconstruction`
- `Pollux Onomasticon IX games Bethe edition`

---

### 39 · Lagori

| | |
|---|---|
| **GAME ID** | `lagori` |
| **TITLE** | Lagori |
| **ALTERNATE NAME(S)** | Pittu, Seven Stones, Lingocha |
| **CULTURE** | Kannada |
| **REGION** | South Asia · India (widespread) |
| **FAMILY** | Games Without a Board |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik E · puan 15.8 |

**WHY THE AGENT CANNOT WRITE IT**

Dönem birinci-el kaydı ARANDI ve BULUNAMADI. Hiçbir kural iddiası doğrulanmamıştır.

**WHAT HAS ALREADY BEEN CHECKED**

- archive.org tam metin + katalog taraması (2026-08-14)
- Thurston 1906 · Ethnographic Notes in Southern India tarandı — oyun bölümü yok
- archive.org 1850–1930 başlık taraması sonuç vermedi

**WHAT SOURCE WAS ATTEMPTED**

- Kaydın KENDİSİ bulunamayan oyunlar — arama görevi kurucuya aittir

**WHAT WAS MISSING**

Kannada/Karnataka bağlamında oyunu KURAL seviyesinde veren dönem kaydı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. 20. yy başı bir Güney Hindistan saha kaydı ya da folklor derlemesi
2. Kannada dilinde bir çocuk oyunları derlemesi
3. İkinci bağımsız künye

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Dönem etnografyası, sayfa-doğrulanmış, Kannada/Karnataka atfıyla.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/lagori/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"lagori" OR "pittu" OR "lingocha" Karnataka game ethnography`
- `seven stones game South India folklore 1900s archive`

---

### 40 · Myinda

| | |
|---|---|
| **GAME ID** | `myinda` |
| **TITLE** | Myinda |
| **ALTERNATE NAME(S)** | Blind man's buff (Greek), Muinda |
| **CULTURE** | Ancient Greek |
| **REGION** | Mediterranean · Greece |
| **FAMILY** | Games Without a Board |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | `P5` CULTURAL IDENTITY / ATTRIBUTION UNRESOLVED |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik E · puan 15.8 |

**WHY THE AGENT CANNOT WRITE IT**

Elde açılabilir tek kayıt Gomme'un İNGİLİZ 'Blind Man's Buff' maddesidir ve bu bir KÜLTÜR TUZAĞIDIR: Antik Yunan maddesini İngiliz kaydından yazmak kitabın kültür künyesini yalanlar.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Gomme 1894 cilt I AÇILDI: 'Blind Man's Buff' İNGİLİZ oyunudur — kullanılmadı (Batch 4 kaynak avı bunu açıkça kaydetti)
- Pollux Onomasticon IX — denetlenebilir açık edisyon bulunamadı

**WHAT SOURCE WAS ATTEMPTED**

- Pollux, Julius, Onomasticon, Book IX — denetlenebilir modern edisyon: E. Bethe (ed.), Pollucis Onomasticon (Leipzig: Teubner, 1900–1937)

**WHAT WAS MISSING**

Antik Yunan biçimini KURAL seviyesinde veren bir kaynak.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Pollux IX'da myinda/muinda pasajı — Yunanca metin + satır numarası + çeviri
2. Oyunun Yunan biçimini tarif eden başka bir antik pasaj ya da akademik çalışma
3. Yunan biçimi ile İngiliz biçimi arasındaki farkı söyleyen bir kaynak

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/myinda/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"myinda" OR "muinda" Greek game Pollux`
- `ancient Greek blind man's buff game evidence`

---

### 41 · Twelve Men's Morris

| | |
|---|---|
| **GAME ID** | `twelve-mens-morris` |
| **TITLE** | Twelve Men's Morris |
| **ALTERNATE NAME(S)** | Morabaraba-type morris, Larger merels |
| **CULTURE** | Medieval European |
| **REGION** | Europe · Europe (widespread) |
| **FAMILY** | The Line and the Territory |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | `P3` RULES INCOMPLETE · `P7` VARIANT CONFLICT |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik E · puan 15.6 |

**WHY THE AGENT CANNOT WRITE IT**

Erişilebilir kaynak AÇILDI ve YALNIZCA dokuz taşlı biçimi verdi — o biçim zaten YAZILDI. ON İKİ taşlı biçim için ayrı bir kayıt bulunamadı.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Gomme 1894 cilt I § Nine Men's Morris AÇILDI: dokuz taşlı biçim var (yazıldı), ON İKİ taşlı biçim için ayrı kayıt YOK (Batch 4 kaynak avı)
- Murray 1952 ve Bell proje genelinde DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)
- Bell, R. C., Board and Table Games from Many Civilizations (Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)

**WHAT WAS MISSING**

On iki taşlı biçimin tahtası (köşegenli) ve o biçime özgü kurallar.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray 1952 ya da Bell'de twelve men's morris maddesi — KÖŞEGENLİ tahta ve 12'şer taş
2. Dokuz taşlı biçimden FARKI: köşegenler, berabere sıklığı, 'uçma' kuralı
3. KARAR MALZEMESİ: bu madde nine-mens-morris içinde bir VARYANT KUTUSU mu olmalı? Kayıt tekrar riskini işaretliyor (distinct=2) ve morabaraba ile AYNI tahtayı paylaşıyor

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/twelve-mens-morris/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"twelve men's morris" rules diagonal board history`
- `twelve mens morris larger merels rules Murray`

---

### 42 · Ludus Duodecim Scriptorum

| | |
|---|---|
| **GAME ID** | `ludus-duodecim-scriptorum` |
| **TITLE** | Ludus Duodecim Scriptorum |
| **ALTERNATE NAME(S)** | XII scripta, Twelve-line game |
| **CULTURE** | Roman |
| **REGION** | Mediterranean · Roman Empire |
| **FAMILY** | The Race Home |
| **PRIMARY BLOCKER** | `P6` — RECONSTRUCTION TOO UNCERTAIN |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `SOURCE-PENDING` · kısıt taraması: `open` · öncelik C · puan 15.5 |

**WHY THE AGENT CANNOT WRITE IT**

Yeniden kurgulama BELİRSİZDİR: taşların iz üzerindeki YÖNÜ ve başlangıç yerleşimi kesin bilinmiyor. Tahta yazıtları kural değil, SÖZ OYUNUDUR — yani en çok bulunan kanıt en az kural taşıyan kanıttır.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 DENENDİ ve açılamadı
- Schädler · Board Game Studies — HİÇ denenmedi

**WHAT SOURCE WAS ATTEMPTED**

- Uzmanlık makaleleri — tek oyunu açan dar künyeler
- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)

**WHAT WAS MISSING**

İz yönü, başlangıç yerleşimi ve alma kuralı — hiçbiri kesin değil.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Schädler, Ulrich — Roma tahta oyunları üzerine Board Game Studies çalışması
2. XII scripta için önerilmiş yeniden kurgulamalar ve ARALARINDAKİ FARK
3. Tabula ile XII scripta arasındaki tarihsel geçişi veren bir kaynak

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
RECONSTRUCTION EVIDENCE
  [ ] reconstruction source  [ ] uncertainty statement  [ ] competing interpretation
```

**IDEAL EVIDENCE** — Rakip yeniden kurgulamaları KARŞILAŞTIRAN bir çalışma — kitap tek yorum seçecek ve seçtiğini beyan edecek.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/ludus-duodecim-scriptorum/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `Schädler ludus duodecim scriptorum reconstruction Board Game Studies`
- `XII scripta Roman game reconstruction rules scholarship`

---

### 43 · Kho Kho

| | |
|---|---|
| **GAME ID** | `kho-kho` |
| **TITLE** | Kho Kho |
| **ALTERNATE NAME(S)** | Kho-Kho |
| **CULTURE** | Marathi |
| **REGION** | South Asia · Maharashtra, India |
| **FAMILY** | Games Without a Board |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | — |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik E · puan 14.8 |

**WHY THE AGENT CANNOT WRITE IT**

Oyunun oynanabilir biçimi 20. yüzyıl KODİFİKASYONUDUR ve o kodifikasyonun denetlenebilir bir nüshası bulunamadı. Kayıt VARDIR (1914 komite · 1935 kural kitabı) ama nüshası yok.

**WHAT HAS ALREADY BEEN CHECKED**

- archive.org katalog + web taraması (2026-08-14) — denetlenebilir edisyon yok
- Kayıt kapsama K23 kapsam değişikliğiyle girdi

**WHAT SOURCE WAS ATTEMPTED**

- Kaydın KENDİSİ bulunamayan oyunlar — arama görevi kurucuya aittir

**WHAT WAS MISSING**

1935 Akhil Maharashtra Shareerik Shikshan Mandal kural kitabının nüshası.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. 1935 Akhil Maharashtra kural kitabı — tarama ya da kütüphane künyesi
2. 1914 Deccan Gymkhana (Pune) kural komitesinin kaydı
3. Sekiz kişiden az oyuncuyla oynanan bir UYARLAMA gerekiyorsa, uyarlamanın MODERN olduğunu söyleyen bir kaynak

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — 1935 kural kitabının taranmış nüshası, künyesi tam.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/kho-kho/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"kho kho" 1935 rulebook Akhil Maharashtra`
- `"kho-kho" Deccan Gymkhana 1914 rules`
- `kho kho indigenous games India codification archive`

---

### 44 · Luk Tsut K'i

| | |
|---|---|
| **GAME ID** | `luk-tsut-kei` |
| **TITLE** | Luk Tsut K'i |
| **ALTERNATE NAME(S)** | Six Men's Game |
| **CULTURE** | Cantonese |
| **REGION** | East Asia · southern China |
| **FAMILY** | The Line and the Territory |
| **PRIMARY BLOCKER** | `P2` — SOURCE TEXT UNAVAILABLE |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik E · puan 14.6 |

**WHY THE AGENT CANNOT WRITE IT**

Elde bulunan derlemelerde KULLANILABİLİR isabet yok. Culin 1895 Kore cildidir ve Çin maddeleri yalnızca KARŞILAŞTIRMA notudur — aynı sınıf tuzak xiangqi, tien-gow ve jianzi'de üç kez ölçüldü.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Culin 1895 · Korean Games tarandı — Kanton biçimi için kullanılabilir kural seti bulunamadı
- Murray 1952 DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)

**WHAT WAS MISSING**

Kanton kaynaklı ya da Çin biçimini açıkça veren bir kural kaydı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Murray 1952'de luk tsut k'i maddesi
2. Ya da: Çin/Kanton kaynaklı bir üç-taş oyunu kaydı
3. KARAR MALZEMESİ: Morris ailesiyle TEKRAR RİSKİ yüksek (kayıt distinct=2 veriyor, kayıttaki en düşük ayırt edicilik puanlarından biri). Kitapta zaten nine-mens-morris, achi ve picaria var. Bu madde bir yedekle değiştirilmeye EN UYGUN adaydır

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**IDEAL EVIDENCE** — Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/luk-tsut-kei/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `"luk tsut kei" Chinese six men's game rules`
- `Cantonese six men morris game rules Culin`

---

### 45 · Terni Lapilli

| | |
|---|---|
| **GAME ID** | `terni-lapilli` |
| **TITLE** | Terni Lapilli |
| **ALTERNATE NAME(S)** | Three-stone game (Roman) |
| **CULTURE** | Roman |
| **REGION** | Mediterranean · Roman Empire |
| **FAMILY** | The Line and the Territory |
| **PRIMARY BLOCKER** | `P6` — RECONSTRUCTION TOO UNCERTAIN |
| **SECONDARY BLOCKERS** | `P1` SOURCE ACCESS BLOCKED · `P4` GAME IDENTITY UNRESOLVED |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik E · puan 14.6 |

**WHY THE AGENT CANNOT WRITE IT**

Yeniden kurgulama BELİRSİZDİR: taşların yerleştirmeden sonra KAYDIRILIP kaydırılmadığı kaynaklardan kesin çıkmaz — yani oyunun temel mekaniği bilinmiyor. Ovid bir GÖNDERMEDİR, kural değil.

**WHAT HAS ALREADY BEEN CHECKED**

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Ovid, Ars Amatoria III — üç taşlı bir oyuna GÖNDERME, kural yok
- Murray 1952 DENENDİ ve açılamadı

**WHAT SOURCE WAS ATTEMPTED**

- Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)

**WHAT WAS MISSING**

Taşların yerleştirmeden sonra kaydırılıp kaydırılmadığı.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. Roma üç-taş oyununun MEKANİĞİNİ tartışan bir arkeoloji/klasik filoloji çalışması
2. Roma kazı buluntularındaki oyun ızgaralarını yorumlayan bir kaynak
3. ⚠ Kayıt uyarıyor: modern 'XOX' ile ilişkisi KESİN DEĞİLDİR ve kitap köken iddiası YAPMAYACAK
4. KARAR MALZEMESİ: üç-taş kümesi kitapta zaten kalabalık (achi · picaria · nine-holes · tapatan). Kaynak gelmezse bu madde yedekle değiştirilmeye uygundur

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
RECONSTRUCTION EVIDENCE
  [ ] reconstruction source  [ ] uncertainty statement  [ ] competing interpretation
```

**IDEAL EVIDENCE** — Rakip yorumları KARŞILAŞTIRAN bir çalışma; kitap tek yorum seçip beyan edecek.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/terni-lapilli/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `terni lapilli Roman three stone game archaeology reconstruction`
- `Roman game boards graffiti three in a row scholarship`

---

### 46 · Mahjong

| | |
|---|---|
| **GAME ID** | `mahjong` |
| **TITLE** | Mahjong |
| **ALTERNATE NAME(S)** | Majiang |
| **CULTURE** | Han Chinese |
| **REGION** | East Asia · China |
| **FAMILY** | Chance and Nerve |
| **PRIMARY BLOCKER** | `P1` — SOURCE ACCESS BLOCKED |
| **SECONDARY BLOCKERS** | `P7` VARIANT CONFLICT |
| **CURRENT STATUS** | `BLOCKED` · kısıt taraması: `open` · öncelik C · puan 14.2 |

**WHY THE AGENT CANNOT WRITE IT**

Kaynak DENENDİ ve erişilemedi. Ayrıca puanlama sistemleri bölgeye göre TAMAMEN farklıdır: doğrulanmamış bir kaynaktan tek sistem seçmek, seçimin GEREKÇESİNİ de doğrulanamaz kılar.

**WHAT HAS ALREADY BEEN CHECKED**

- Parlett 1999 DENENDİ — telif altında, açık tam metin yok (2026-08-13)
- Foster's Complete Hoyle 1897 tarandı — mahjong yok (Batch 4 avı)

**WHAT SOURCE WAS ATTEMPTED**

- Parlett, David, The Oxford History of Board Games (Oxford: Oxford University Press, 1999)
- Uzmanlık makaleleri — tek oyunu açan dar künyeler

**WHAT WAS MISSING**

Tek bir DETERMİNİSTİK ruleset ve onun künyesi.

**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**

1. 1920'lerin BİRİNCİ ELDEN bir kural kitabı (Babcock 1920 ve çağdaşları — ABD'de kamusal alanda olabilir)
2. Ya da: kitabın basacağı ruleset için kurucu KARARI + o rulesetin künyesi
3. Puanlamanın sadeleştirilebileceği bir temel biçim (§ K19 sayfa bütçesi: madde 650 kelimeye SIĞMIYOR ve dört sayfa isteyebilir)

**MINIMUM ACCEPTABLE EVIDENCE**

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**IDEAL EVIDENCE** — 1920'lerin kamusal alandaki bir kural kitabı + hangi bölgesel sistemin basılacağına dair açık bir gerekçe.

**EXPECTED FILE FORMAT** — PDF · tarama · kararlı URL · künye notu (.md ya da .txt) — JSON'a çevirmek GEREKMEZ

**EXPECTED SOURCE LOCATION** — `06_FOUNDER_DELIVERY/mahjong/`

**HOW THE AGENT WILL USE THE DELIVERY** — 04_BUILD/founder_delivery_ingest.py alır → hash'ler → kanıt listesini denetler → source_verification kaydı açar → engeli çözer → üretim kuyruğuna alır → yazar → diyagram → QA → CI

**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —
bu adreslerin var olduğu İDDİA EDİLMEZ)

- `mahjong 1920 rulebook Babcock public domain archive`
- `"rules for mah-jongg" 1923 archive.org`
- `Stanwick mahjong origins Playing-Card`

---

## 9 · TESLİM VE ALIM

Teslim yapısı ve alım hattı için:
[`FOUNDER_RESEARCH_PACK.md`](FOUNDER_RESEARCH_PACK.md) § 1 ve § 4.

Alım aracı: `04_BUILD/founder_delivery_ingest.py`

