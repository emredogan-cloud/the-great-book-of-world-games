# FOUNDER RESEARCH PACK

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/build_gap_register.py · ELLE DÜZENLEMEYİN -->

> **The Great Book of World Games** · insan araştırmacı için çalışma paketi
> 
> Tam kayıt: [`FOUNDER_RESEARCH_GAP_REGISTER.md`](FOUNDER_RESEARCH_GAP_REGISTER.md)

Bu paket **kaynağa göre** düzenlenmiştir, oyuna göre değil. Sebebi
pratiktir: kütüphaneye bir oyun için değil bir **kitap** için gidilir,
ve o kitap masaya oturduğunda içinden birden çok madde çıkar.

---

## 0 · ÖNCE BUNU OKUYUN — ÜÇ SATIRLIK ÖZET

1. **Murray 1952'yi bulun.** Tek başına 46 maddenin **24'ünü** açar.
2. Sonra **Parlett 1999 · Zaslavsky 1973 · Bell 1960–69 · Russ 2000**.
   Beşi birlikte **46 madde** açar.
3. Geri kalan altı madde tek tek avlanır ve § 3'te ayrı listelenmiştir.

**Bell 1960–69 en ucuz başlangıçtır**: Dover tıpkıbasımı hâlâ basılıyor
ve ikinci el piyasada bol. **Murray 1952 en yüksek getirilidir** ama
kütüphane gerektirir.

---

## 1 · TESLİM BİÇİMİ — HER ŞEY İÇİN AYNI

```
06_FOUNDER_DELIVERY/
    <GAME_ID>/                  ← kayıttaki gameId, birebir
        source.pdf              ← tarama · PDF · ekran görüntüsü (opsiyonel)
        source.md               ← metin ya da kural özeti (opsiyonel)
        bibliography.md         ← ZORUNLU · yazar · başlık · baskı · yıl · sayfa
        notes.md                ← ne bulundu · ne bulunamadı (opsiyonel)
```

Birden çok oyunu açan bir kitap teslim ediliyorsa **her oyun için ayrı
klasör** açın ve ilgili sayfaları o klasöre koyun. Aynı taramayı iki
klasöre kopyalamak sorun değildir — alım betiği hash'e bakar ve
yinelenen dosyayı tanır.

### Ne göndermeniz GEREKMİYOR

- JSON'a çevirmek **gerekmez**. Alım betiği bunu yapar.
- Kuralı yeniden yazmak **gerekmez**. Ham metin/tarama yeterlidir.
- Zaten elimizde olan bir şeyi tekrar bulmak **gerekmez** — her maddede
  `WHAT HAS ALREADY BEEN CHECKED` alanı neyin elde olduğunu söyler.

### ⚠ İki dürüstlük kuralı

1. **Sayfa numarası olmayan bir teslim de kabul edilir** — ama kayıt
   `bibliographyStatus: incomplete` taşır ve o oyun `locked` olamaz.
   Uydurulmuş bir sayfa numarası kitabın tek denetlenebilir iddiasını
   yıkar; **eksik künye bunu yıkmaz**.
2. **Kurucu teslimi bağımsız doğrulama DEĞİLDİR.** Kayıt bunu
   `founderSupplied: true · independentVerification: false` olarak
   taşır ve prozada gizlenmez.

---

## 2 · KAYNAK KAYNAK ÇALIŞMA LİSTESİ

---

### ▸ Murray, H. J. R., A History of Board-Games Other Than Chess (Oxford: Clarendon Press, 1952)

| | |
|---|---|
| **AÇTIĞI MADDE** | **20** |
| **DURUM** | ⛔ **DENENDİ ve açılamadı** |
| **KANIT** | archive.org nüshası yalnızca ÖDÜNÇ erişimine açık — HTTP 401 (source_verification.json · tablut kaydı, 2026-08-13) |
| **NEDEN** | 1952 tarihli ve telif altındadır; tam metin indirilemez. |

**NEREDE ARANIR**

- Üniversite kütüphanesi — kapalı raf ya da ödünç
- archive.org ödünç hesabı (1 saatlik ödünç, sayfa görüntüsü)
- İkinci el nüsha — Oxford/Clarendon 1952 ya da Hacker 1978 tıpkıbasımı

**NE İSTİYORUZ**

Aşağıdaki oyunların GEÇTİĞİ sayfaların taraması ya da fotoğrafı. Murray oyunları bölüm bölüm ve numaralı alt başlıklarla verir; her oyun için ilgili alt başlığın TAMAMI gerekir.

> KİTABIN EN YÜKSEK GETİRİLİ TEK KAYNAĞIDIR. Tek başına kayıttaki 52 oyunun 24'ünü açar — geri kalan bütün eserlerin toplamından fazla.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `bohnenspiel` | The Sowing Games | German | A | 21.6 | Murray 1952 ya da Bell'de Bohnenspiel maddesi — 2×6 çukur, 6'şar tohum, ekim yönü, 2/4/6 alma kuralı, zincirli alma |
| `congklak` | The Sowing Games | Javanese | A | 19.6 | Murray 1952 ya da Russ 2000'de congklak/congkak/dakon maddesi |
| `sungka` | The Sowing Games | Visayan | A | 19.6 | Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900) — sungka bölümü, SAYFA NUMARASIYLA (proje bu makalenin sayfa aralığını henüz… |
| `aadu-puli-attam` | The Hunt and the Siege | Tamil | A | 19.5 | Bell ya da Murray 1952'de aadu puli attam / puli meka maddesi |
| `turkish-dama` | The War Board | Turkish | A | 19.4 | Murray 1952 ya da Parlett'te Turkish draughts maddesi — 8×8 tahta, 16'şar taş İKİNCİ ve ÜÇÜNCÜ sırada, taşların İLERİ VE YANA gitmesi (köşegen DEĞİ… |
| `go` | The Line and the Territory | Han Chinese | C | 18.6 | Volpicelli, Z., 'Wei-ch'i', Journal of the China Branch of the Royal Asiatic Society N.S. XXVI (1894) — Smith'in KENDİ künyesinde geçiyor |
| `hus` | The Sowing Games | Nama | C | 18.6 | Murray 1952 ya da Townshend 1979'da hus/ǁhus maddesi — dört sıra, ekim yönü, alma koşulu, bitiş |
| `morabaraba` | The Line and the Territory | Sotho | A | 18.6 | Zaslavsky 1973 ya da Murray 1952'de morabaraba/umlabalaba maddesi |
| `shax` | The Line and the Territory | Somali | A | 18.6 | Murray 1952 ya da Zaslavsky 1973'te shax/jare maddesi |
| `tapatan` | The Line and the Territory | Tagalog | A | 18.6 | Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900) — tapatan bölümü, sayfa numarasıyla |
| `ashta-kashte` | The Race Home | Bengali | A | 18.5 | Murray 1952 ya da Bell'de ashta-kashte maddesi |
| `nard` | The Race Home | Persian | C | 17.5 | Nard'ın ORTAÇAĞ kural metni — Arapça/Farsça bir dönem kaydı ya da onu aktaran akademik bir çalışma |
| `rimau-rimau` | The Hunt and the Siege | Malay | A | 17.5 | Murray 1952 ya da Bell'de rimau-rimau / main rimau maddesi |
| `zamma` | The War Board | Amazigh | C | 17.4 | Murray 1952 ya da Béart 1955'te zamma/sig maddesi |
| `halatafl` | The Hunt and the Siege | Icelandic | E | 16.5 | Halatafl'ın KURALINI veren bir kaynak — tahta, taş sayıları, hareket, alma |
| `jeu-de-dames` | The War Board | French | A | 16.4 | Murray 1952 ya da Parlett'te international/Polish draughts maddesi — 10×10 tahta, 20'şer taş, geriye alma, dama taşının uzun menzili, AZAMİ ALMA ZO… |
| `twelve-mens-morris` | The Line and the Territory | Medieval European | E | 15.6 | Murray 1952 ya da Bell'de twelve men's morris maddesi — KÖŞEGENLİ tahta ve 12'şer taş |
| `ludus-duodecim-scriptorum` | The Race Home | Roman | C | 15.5 | Schädler, Ulrich — Roma tahta oyunları üzerine Board Game Studies çalışması |
| `luk-tsut-kei` | The Line and the Territory | Cantonese | E | 14.6 | Murray 1952'de luk tsut k'i maddesi |
| `terni-lapilli` | The Line and the Territory | Roman | E | 14.6 | Roma üç-taş oyununun MEKANİĞİNİ tartışan bir arkeoloji/klasik filoloji çalışması |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `"Bohnenspiel" German mancala rules Murray`
- `das Bohnenspiel Regeln historisch Saatspiel`
- `"congklak" OR "congkak" OR "dakon" Javanese mancala rules`
- `congkak Malay Indonesian sowing game rules ethnography`
- `Culin "Philippine Games" American Anthropologist 1900 archive.org`
- `American Anthropologist volume 2 1900 full text archive`
- `"sungka" Visayan Philippine mancala rules Culin`
- `"aadu puli attam" rules board tigers goats Tamil`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/bohnenspiel/
06_FOUNDER_DELIVERY/congklak/
06_FOUNDER_DELIVERY/sungka/
06_FOUNDER_DELIVERY/aadu-puli-attam/
06_FOUNDER_DELIVERY/turkish-dama/
06_FOUNDER_DELIVERY/go/
06_FOUNDER_DELIVERY/hus/
06_FOUNDER_DELIVERY/morabaraba/
06_FOUNDER_DELIVERY/shax/
06_FOUNDER_DELIVERY/tapatan/
06_FOUNDER_DELIVERY/ashta-kashte/
06_FOUNDER_DELIVERY/nard/
06_FOUNDER_DELIVERY/rimau-rimau/
06_FOUNDER_DELIVERY/zamma/
06_FOUNDER_DELIVERY/halatafl/
06_FOUNDER_DELIVERY/jeu-de-dames/
06_FOUNDER_DELIVERY/twelve-mens-morris/
06_FOUNDER_DELIVERY/ludus-duodecim-scriptorum/
06_FOUNDER_DELIVERY/luk-tsut-kei/
06_FOUNDER_DELIVERY/terni-lapilli/
```

---

### ▸ Bell, R. C., Board and Table Games from Many Civilizations (Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)

| | |
|---|---|
| **AÇTIĞI MADDE** | **10** |
| **DURUM** | ⛔ **DENENDİ ve açılamadı** |
| **KANIT** | telif altında — açık tam metin yok (blockedSources kaydı) |
| **NEDEN** | Telif altındadır. Dover tıpkıbasımı yaygın ve ucuzdur. |

**NEREDE ARANIR**

- Dover 1979 tıpkıbasımı — ikinci el piyasada bol ve ucuz
- Üniversite kütüphanesi
- archive.org ödünç hesabı

**NE İSTİYORUZ**

İlgili oyunların maddeleri. Bell her oyunu tahta diyagramıyla ve kısa kural metniyle verir; madde + diyagram birlikte gerekir.

> EN UCUZ ÇÖZÜM. Dover tıpkıbasımı hâlâ basılıyor.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `bohnenspiel` | The Sowing Games | German | A | 21.6 | Murray 1952 ya da Bell'de Bohnenspiel maddesi — 2×6 çukur, 6'şar tohum, ekim yönü, 2/4/6 alma kuralı, zincirli alma |
| `bagh-chal` | The Hunt and the Siege | Nepali | A | 20.5 | Bell ya da Parlett'te bagh-chal maddesi |
| `konane` | The War Board | Hawaiian | C | 20.4 | Culin, Stewart, 'Hawaiian Games', American Anthropologist 1:2 (1899) — kōnane bölümü, SAYFA NUMARASIYLA (KAMUSAL ALAN; ciltli dergi taraması aranma… |
| `aadu-puli-attam` | The Hunt and the Siege | Tamil | A | 19.5 | Bell ya da Murray 1952'de aadu puli attam / puli meka maddesi |
| `bul` | The Race Home | Kekchi Maya | C | 19.5 | Verbeeck, Lieve, 'Bul: A Patolli Game in Maya Lowland', Board Game Studies 1 (1998) — makalenin tamamı |
| `li-b-el-merafib` | The Race Home | Sudanese Arab | C | 19.5 | Davies, R., 'Some Arab Games and Puzzles', Sudan Notes and Records 8 (1925) — makalenin tamamı |
| `ashta-kashte` | The Race Home | Bengali | A | 18.5 | Murray 1952 ya da Bell'de ashta-kashte maddesi |
| `len-choa` | The Hunt and the Siege | Thai | A | 17.5 | Bell'de len choa maddesi — tahta, leopar/hayvan sayıları, hareket, alma, bitiş |
| `rimau-rimau` | The Hunt and the Siege | Malay | A | 17.5 | Murray 1952 ya da Bell'de rimau-rimau / main rimau maddesi |
| `twelve-mens-morris` | The Line and the Territory | Medieval European | E | 15.6 | Murray 1952 ya da Bell'de twelve men's morris maddesi — KÖŞEGENLİ tahta ve 12'şer taş |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `"Bohnenspiel" German mancala rules Murray`
- `das Bohnenspiel Regeln historisch Saatspiel`
- `"bagh chal" rules tigers goats Nepal board game`
- `bagh-chal Nepali traditional game rules ethnography`
- `Culin "Hawaiian Games" American Anthropologist 1899 archive.org`
- `American Anthropologist volume 1 1899 full text HathiTrust`
- `konane Hawaiian checkers rules Bishop Museum`
- `"aadu puli attam" rules board tigers goats Tamil`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/bohnenspiel/
06_FOUNDER_DELIVERY/bagh-chal/
06_FOUNDER_DELIVERY/konane/
06_FOUNDER_DELIVERY/aadu-puli-attam/
06_FOUNDER_DELIVERY/bul/
06_FOUNDER_DELIVERY/li-b-el-merafib/
06_FOUNDER_DELIVERY/ashta-kashte/
06_FOUNDER_DELIVERY/len-choa/
06_FOUNDER_DELIVERY/rimau-rimau/
06_FOUNDER_DELIVERY/twelve-mens-morris/
```

---

### ▸ Parlett, David, The Oxford History of Board Games (Oxford: Oxford University Press, 1999)

| | |
|---|---|
| **AÇTIĞI MADDE** | **10** |
| **DURUM** | ⛔ **DENENDİ ve açılamadı** |
| **KANIT** | telif altında — açık tam metin yok (source_verification.json · mahjong kaydı, 2026-08-13) |
| **NEDEN** | Telif altındadır; açık erişimli tam metni yoktur. |

**NEREDE ARANIR**

- Üniversite kütüphanesi
- archive.org ödünç hesabı
- İkinci el nüsha (OUP 1999 ya da Echo Point 2018 tıpkıbasımı)

**NE İSTİYORUZ**

İlgili oyunların bölümleri. Parlett oyunları AİLE başlıkları altında toplar; oyun adının geçtiği bölümün tamamı gerekir.

> Şans ailesi tek başına buna bağlıdır ve aile 4/4 hedefinde 3 yazılmıştır.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `morra` | Games Without a Board | Italian | A | 21.8 | Morra'nın PUANLAMASINI ve KAZANMA koşulunu veren herhangi bir künye |
| `bagh-chal` | The Hunt and the Siege | Nepali | A | 20.5 | Bell ya da Parlett'te bagh-chal maddesi |
| `turkish-dama` | The War Board | Turkish | A | 19.4 | Murray 1952 ya da Parlett'te Turkish draughts maddesi — 8×8 tahta, 16'şar taş İKİNCİ ve ÜÇÜNCÜ sırada, taşların İLERİ VE YANA gitmesi (köşegen DEĞİ… |
| `petanque` | Games Without a Board | Provençal | A | 18.8 | FIPJP resmî kural kitabı — SÜRÜM, yürürlük tarihi ve madde numaraları |
| `daldos` | The Race Home | Danish | C | 18.5 | Michaelsen, Peter — daldøs ve ilgili kuzey yarış oyunları üzerine Board Game Studies makalesi |
| `game-of-the-goose` | The Race Home | Italian | E | 17.5 | Seville, Adrian, The Cultural Legacy of the Royal Game of the Goose (Amsterdam University Press, 2019) — AUP başlıklarının bir bölümü AÇIK ERİŞİMLİDİR |
| `jeu-de-dames` | The War Board | French | A | 16.4 | Murray 1952 ya da Parlett'te international/Polish draughts maddesi — 10×10 tahta, 20'şer taş, geriye alma, dama taşının uzun menzili, AZAMİ ALMA ZO… |
| `makruk` | The War Board | Thai | E | 16.4 | Murray, A History of Chess (1913) — Siyam satrancı bölümü (HathiTrust ya da Google Books TAM GÖRÜNÜM; eser kamusal alandadır) |
| `surakarta` | The War Board | Javanese | D | 16.4 | Surakarta'nın Java'daki geleneksel varlığını gösteren bir DÖNEM kaydı (20. yy öncesi ya da erken 20. yy saha kaydı) |
| `mahjong` | Chance and Nerve | Han Chinese | C | 14.2 | 1920'lerin BİRİNCİ ELDEN bir kural kitabı (Babcock 1920 ve çağdaşları — ABD'de kamusal alanda olabilir) |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `"morra" Italian finger game rules scoring`
- `"micatio" mora game history rules`
- `morra gioco regole punteggio storico`
- `"bagh chal" rules tigers goats Nepal board game`
- `bagh-chal Nepali traditional game rules ethnography`
- `Turkish draughts dama rules orthogonal capture`
- `Türk daması kuralları tarihi kaynak`
- `Murray Turkish draughts rules 1952`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/morra/
06_FOUNDER_DELIVERY/bagh-chal/
06_FOUNDER_DELIVERY/turkish-dama/
06_FOUNDER_DELIVERY/petanque/
06_FOUNDER_DELIVERY/daldos/
06_FOUNDER_DELIVERY/game-of-the-goose/
06_FOUNDER_DELIVERY/jeu-de-dames/
06_FOUNDER_DELIVERY/makruk/
06_FOUNDER_DELIVERY/surakarta/
06_FOUNDER_DELIVERY/mahjong/
```

---

### ▸ Uzmanlık makaleleri — tek oyunu açan dar künyeler

| | |
|---|---|
| **AÇTIĞI MADDE** | **10** |
| **DURUM** | ◻ **HİÇ DENENMEDİ** — engelli değil, sırası gelmedi |
| **KANIT** | proje bunların hiçbirini denemedi |
| **NEDEN** | Hakemli dergi ya da dar dağıtımlı monografi. |

**NEREDE ARANIR**

- Board Game Studies Journal — eski sayıları açık arşivde olabilir
- JSTOR / Taylor & Francis (kurumsal erişim)
- Yazar kopyası / akademik ağ
- Üniversite kütüphanesi

**NE İSTİYORUZ**

Aşağıdaki her künye TEK bir oyunu açar:
  · Verbeeck, Lieve, 'Bul: A Patolli Game in Maya Lowland', Board Game Studies 1 (1998) → bul
  · Michaelsen, Peter, daldøs ve kuzey yarış oyunları üzerine çalışmalar, Board Game Studies → daldos
  · Schädler, Ulrich, Roma tahta oyunları üzerine çalışmalar, Board Game Studies → ludus-duodecim-scriptorum
  · Davies, R., 'Some Arab Games and Puzzles', Sudan Notes and Records 8 (1925) → li-b-el-merafib
  · Herskovits, Melville J., 'Wari in the New World', Journal of the Royal Anthropological Institute 62 (1932) → adji-boto
  · Pankhurst, Richard, 'Gabata and Related Board Games of Ethiopia and the Horn of Africa', Ethiopia Observer 14 (1971) → gebeta
  · Odeleye, A. O., Ayo: A Popular Yoruba Game (Ibadan: OUP Nigeria, 1977) → ayoayo
  · Nsimbi, M. B., Omweso: A Game People Play in Uganda (Los Angeles: UCLA African Studies Center, 1968) → omweso
  · Ascher, Marcia, 'Mu Torere: An Analysis of a Maori Game', Mathematics Magazine 60:2 (1987) → mu-torere
  · Seville, Adrian, The Cultural Legacy of the Royal Game of the Goose (Amsterdam University Press, 2019) → game-of-the-goose
  · Austin, R. G., "Zeno's Game of τάβλη", Journal of Hellenic Studies 54 (1934) → tabula (destek)
  · Stanwick, Michael, mahjong kökeni üzerine çalışmalar, The Playing-Card (IPCS) → mahjong (destek)

> Board Game Studies eski sayıları ve Amsterdam University Press başlıklarının bir bölümü AÇIK ERİŞİMLİDİR. Denenmeden engelli sayılmazlar — bu yüzden hepsi SOURCE-PENDING'dir, BLOCKED değil.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `adji-boto` | The Sowing Games | Ndyuka Maroon | C | 19.6 | Herskovits, Melville J., 'Wari in the New World', Journal of the Royal Anthropological Institute 62 (1932) — makalenin tamamı |
| `bul` | The Race Home | Kekchi Maya | C | 19.5 | Verbeeck, Lieve, 'Bul: A Patolli Game in Maya Lowland', Board Game Studies 1 (1998) — makalenin tamamı |
| `li-b-el-merafib` | The Race Home | Sudanese Arab | C | 19.5 | Davies, R., 'Some Arab Games and Puzzles', Sudan Notes and Records 8 (1925) — makalenin tamamı |
| `gebeta` | The Sowing Games | Amhara | C | 18.6 | Pankhurst, Richard, 'Gabata and Related Board Games of Ethiopia and the Horn of Africa', Ethiopia Observer 14 (1971) — makalenin tamamı |
| `omweso` | The Sowing Games | Ganda | C | 18.6 | Nsimbi, M. B., Omweso: A Game People Play in Uganda (Los Angeles: UCLA African Studies Center, 1968) — kural bölümü |
| `daldos` | The Race Home | Danish | C | 18.5 | Michaelsen, Peter — daldøs ve ilgili kuzey yarış oyunları üzerine Board Game Studies makalesi |
| `game-of-the-goose` | The Race Home | Italian | E | 17.5 | Seville, Adrian, The Cultural Legacy of the Royal Game of the Goose (Amsterdam University Press, 2019) — AUP başlıklarının bir bölümü AÇIK ERİŞİMLİDİR |
| `ayoayo` | The Sowing Games | Yoruba | E | 16.6 | Odeleye, A. O., Ayo: A Popular Yoruba Game (Ibadan: Oxford University Press Nigeria, 1977) — kural bölümü |
| `ludus-duodecim-scriptorum` | The Race Home | Roman | C | 15.5 | Schädler, Ulrich — Roma tahta oyunları üzerine Board Game Studies çalışması |
| `mahjong` | Chance and Nerve | Han Chinese | C | 14.2 | 1920'lerin BİRİNCİ ELDEN bir kural kitabı (Babcock 1920 ve çağdaşları — ABD'de kamusal alanda olabilir) |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `Herskovits "Wari in the New World" JRAI 1932 PDF`
- `"adji boto" Ndyuka Maroon Suriname game rules`
- `Verbeeck "Bul" Patolli Maya Board Game Studies 1998 PDF`
- `"bul" OR "boolik" Kekchi Maya game rules`
- `Davies "Some Arab Games and Puzzles" Sudan Notes Records 1925`
- `"hyena game" Sudan spiral race game rules`
- `"li'b el merafib" rules`
- `Pankhurst "Gabata" Ethiopia Observer 1971 board games`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/adji-boto/
06_FOUNDER_DELIVERY/bul/
06_FOUNDER_DELIVERY/li-b-el-merafib/
06_FOUNDER_DELIVERY/gebeta/
06_FOUNDER_DELIVERY/omweso/
06_FOUNDER_DELIVERY/daldos/
06_FOUNDER_DELIVERY/game-of-the-goose/
06_FOUNDER_DELIVERY/ayoayo/
06_FOUNDER_DELIVERY/ludus-duodecim-scriptorum/
06_FOUNDER_DELIVERY/mahjong/
```

---

### ▸ Zaslavsky, Claudia, Africa Counts: Number and Pattern in African Culture (Boston: Prindle, Weber & Schmidt, 1973)

| | |
|---|---|
| **AÇTIĞI MADDE** | **8** |
| **DURUM** | ⛔ **DENENDİ ve açılamadı** |
| **KANIT** | telif altında — açık tam metin yok (source_verification.json · mbube-mbube kaydı, 2026-08-13) |
| **NEDEN** | Telif altındadır. |

**NEREDE ARANIR**

- Lawrence Hill Books 1999 üçüncü baskısı — hâlâ basılıyor
- Üniversite kütüphanesi
- archive.org ödünç hesabı

**NE İSTİYORUZ**

Oyun bölümleri (kitabın oyunlara ayrılmış kısmı). Ampe, pilolo ve shisima için bu eser oyunların TEK künyesidir.

> Afrika kültürlerinin çoğu buna bağlıdır ve altı oyun için TEK kaynaktır — yani ikinci bağımsız kaynak ayrıca gerekir.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `yote` | The War Board | Wolof | C | 20.4 | Béart, Charles, Jeux et jouets de l'Ouest africain (Dakar: IFAN, 1955) — yoté bölümü (Fransızca) |
| `ampe` | Games Without a Board | Akan | A | 19.8 | Zaslavsky 1973'te ampe maddesi — sıçrama/ayak biçimi, puanlama, tur, bitiş |
| `pilolo` | Games Without a Board | Ga | A | 19.8 | Zaslavsky 1973'te pilolo maddesi — saklama/arama sırası, puanlama, bitiş |
| `shisima` | The Line and the Territory | Luhya | A | 19.6 | Zaslavsky 1973'te shisima maddesi — sekizgen tahta, 3'er taş, hareket kısıtı, üçlü sıra, bitiş |
| `morabaraba` | The Line and the Territory | Sotho | A | 18.6 | Zaslavsky 1973 ya da Murray 1952'de morabaraba/umlabalaba maddesi |
| `shax` | The Line and the Territory | Somali | A | 18.6 | Murray 1952 ya da Zaslavsky 1973'te shax/jare maddesi |
| `ayoayo` | The Sowing Games | Yoruba | E | 16.6 | Odeleye, A. O., Ayo: A Popular Yoruba Game (Ibadan: Oxford University Press Nigeria, 1977) — kural bölümü |
| `mefuvha` | The Sowing Games | Venda | E | 16.6 | Zaslavsky 1973 ya da Townshend 1979'da mefuvha/muravharavha maddesi |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `Béart "Jeux et jouets de l'Ouest africain" IFAN 1955 PDF`
- `"yoté" OR "yote" Wolof Senegal game rules double capture`
- `jeux ouest africain yoté règles IFAN Dakar`
- `"ampe" Ghana game rules`
- `"ampe" Akan children's game ethnography`
- `"pilolo" Ghana Ga children's game rules`
- `Ga people traditional children games Ghana ethnography`
- `"shisima" Luhya Kenya game rules octagon`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/yote/
06_FOUNDER_DELIVERY/ampe/
06_FOUNDER_DELIVERY/pilolo/
06_FOUNDER_DELIVERY/shisima/
06_FOUNDER_DELIVERY/morabaraba/
06_FOUNDER_DELIVERY/shax/
06_FOUNDER_DELIVERY/ayoayo/
06_FOUNDER_DELIVERY/mefuvha/
```

---

### ▸ Russ, Laurence, The Complete Mancala Games Book (New York: Marlowe & Company, 2000)

| | |
|---|---|
| **AÇTIĞI MADDE** | **4** |
| **DURUM** | ⛔ **DENENDİ ve açılamadı** |
| **KANIT** | telif altında — açık tam metin yok (source_verification.json · olinda-keliya kaydı, 2026-08-13) |
| **NEDEN** | Telif altındadır. |

**NEREDE ARANIR**

- İkinci el nüsha
- Üniversite kütüphanesi

**NE İSTİYORUZ**

İlgili ekim oyunlarının maddeleri.

> Ekim ailesinin ikinci en yüksek getirili eseri.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `adji-boto` | The Sowing Games | Ndyuka Maroon | C | 19.6 | Herskovits, Melville J., 'Wari in the New World', Journal of the Royal Anthropological Institute 62 (1932) — makalenin tamamı |
| `congklak` | The Sowing Games | Javanese | A | 19.6 | Murray 1952 ya da Russ 2000'de congklak/congkak/dakon maddesi |
| `omweso` | The Sowing Games | Ganda | C | 18.6 | Nsimbi, M. B., Omweso: A Game People Play in Uganda (Los Angeles: UCLA African Studies Center, 1968) — kural bölümü |
| `toguz-kumalak` | The Sowing Games | Kazakh | D | 18.6 | Russ 2000 ya da de Voogt 1997'de toguz kumalak maddesi — 2×9 çukur, 9'ar tohum, tuzdyk (kutsal çukur) kuralı, kazan, alma koşulu, bitiş |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `Herskovits "Wari in the New World" JRAI 1932 PDF`
- `"adji boto" Ndyuka Maroon Suriname game rules`
- `"congklak" OR "congkak" OR "dakon" Javanese mancala rules`
- `congkak Malay Indonesian sowing game rules ethnography`
- `Nsimbi "Omweso: A Game People Play in Uganda" 1968 PDF`
- `"omweso" OR "mweso" Ganda Uganda mancala rules four row`
- `"toguz kumalak" OR "togyz kumalak" rules tuzdyk Kazakh`
- `toguz korgool Kyrgyz Kazakh mancala historical rules`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/adji-boto/
06_FOUNDER_DELIVERY/congklak/
06_FOUNDER_DELIVERY/omweso/
06_FOUNDER_DELIVERY/toguz-kumalak/
```

---

### ▸ Townshend, Philip, 'Mankala in Eastern and Southern Africa: A Distributional Analysis', Azania: Journal of the British Institute in Eastern Africa 14 (1979)

| | |
|---|---|
| **AÇTIĞI MADDE** | **4** |
| **DURUM** | ◻ **HİÇ DENENMEDİ** — engelli değil, sırası gelmedi |
| **KANIT** | proje bu makaleyi HİÇ denemedi |
| **NEDEN** | Hakemli dergi makalesi; erişimi kurumsal abonelik gerektirebilir. |

**NEREDE ARANIR**

- Taylor & Francis / Azania dergi arşivi (kurumsal erişim)
- British Institute in Eastern Africa
- Yazar kopyası / akademik ağ

**NE İSTİYORUZ**

Makalenin tamamı. Dört ekim oyunu (gebeta, hus, mefuvha, omweso) için ikinci bağımsız kaynaktır.

> DENENMEDİ — engelli DEĞİL. Kurucu denemeden önce ajan da deneyebilir.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `gebeta` | The Sowing Games | Amhara | C | 18.6 | Pankhurst, Richard, 'Gabata and Related Board Games of Ethiopia and the Horn of Africa', Ethiopia Observer 14 (1971) — makalenin tamamı |
| `hus` | The Sowing Games | Nama | C | 18.6 | Murray 1952 ya da Townshend 1979'da hus/ǁhus maddesi — dört sıra, ekim yönü, alma koşulu, bitiş |
| `omweso` | The Sowing Games | Ganda | C | 18.6 | Nsimbi, M. B., Omweso: A Game People Play in Uganda (Los Angeles: UCLA African Studies Center, 1968) — kural bölümü |
| `mefuvha` | The Sowing Games | Venda | E | 16.6 | Zaslavsky 1973 ya da Townshend 1979'da mefuvha/muravharavha maddesi |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `Pankhurst "Gabata" Ethiopia Observer 1971 board games`
- `"gebeta" OR "gabata" Ethiopian mancala rules Amhara`
- `Townshend Mankala Eastern Southern Africa Azania 1979`
- `"hus" Nama mancala four row rules Namibia`
- `Townshend Mankala Azania 1979 hus ohus`
- `Nsimbi "Omweso: A Game People Play in Uganda" 1968 PDF`
- `"omweso" OR "mweso" Ganda Uganda mancala rules four row`
- `"mefuvha" OR "muravharavha" Venda game rules South Africa`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/gebeta/
06_FOUNDER_DELIVERY/hus/
06_FOUNDER_DELIVERY/omweso/
06_FOUNDER_DELIVERY/mefuvha/
```

---

### ▸ Béart, Charles, Jeux et jouets de l'Ouest africain, Mémoires de l'IFAN 42 (Dakar: IFAN, 1955), 2 cilt

| | |
|---|---|
| **AÇTIĞI MADDE** | **2** |
| **DURUM** | ◻ **HİÇ DENENMEDİ** — engelli değil, sırası gelmedi |
| **KANIT** | proje bu eseri HİÇ denemedi |
| **NEDEN** | Dakar basımı, dar dağıtımlı, muhtemelen yalnızca basılı. |

**NEREDE ARANIR**

- IFAN (Institut Fondamental d'Afrique Noire) — Dakar
- Fransız üniversite kütüphaneleri · BnF
- Gallica dijital arşivi

**NE İSTİYORUZ**

yoté ve zamma/sig maddeleri. Béart oyunları saha kaydı olarak verir.

> Fransızca. Batı Afrika savaş tahtası oyunlarının en iyi birinci el kaydı.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `yote` | The War Board | Wolof | C | 20.4 | Béart, Charles, Jeux et jouets de l'Ouest africain (Dakar: IFAN, 1955) — yoté bölümü (Fransızca) |
| `zamma` | The War Board | Amazigh | C | 17.4 | Murray 1952 ya da Béart 1955'te zamma/sig maddesi |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `Béart "Jeux et jouets de l'Ouest africain" IFAN 1955 PDF`
- `"yoté" OR "yote" Wolof Senegal game rules double capture`
- `jeux ouest africain yoté règles IFAN Dakar`
- `"zamma" Berber Amazigh draughts rules North Africa`
- `"sig" OR "kharbga" North African board game rules`
- `Béart jeux ouest africain zamma sig règles`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/yote/
06_FOUNDER_DELIVERY/zamma/
```

---

### ▸ Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900)

| | |
|---|---|
| **AÇTIĞI MADDE** | **2** |
| **DURUM** | ◻ **HİÇ DENENMEDİ** — engelli değil, sırası gelmedi |
| **KANIT** | proje bu makaleyi denemedi; AYNI DERGİNİN 1899 sayısı (Hawaiian Games) denendi ve yalnızca JSTOR nüshası bulundu |
| **NEDEN** | Dergi makalesi. 1900 tarihlidir ve ABD'de KAMUSAL ALANDADIR — yani bu bir telif engeli değil, bir dağıtım meselesidir. |

**NEREDE ARANIR**

- archive.org — American Anthropologist cilt 2 (1900) ciltli sayısı
- Wiley Online Library (eski seri, açık olabilir)
- HathiTrust — kamusal alan cildi tam görünür olmalı

**NE İSTİYORUZ**

sungka ve tapatan bölümleri, sayfa numaralarıyla.

> YÜKSEK GETİRİ · DÜŞÜK MALİYET. Kamusal alandadır ve iki oyun açar.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `sungka` | The Sowing Games | Visayan | A | 19.6 | Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900) — sungka bölümü, SAYFA NUMARASIYLA (proje bu makalenin sayfa aralığını henüz… |
| `tapatan` | The Line and the Territory | Tagalog | A | 18.6 | Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900) — tapatan bölümü, sayfa numarasıyla |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `Culin "Philippine Games" American Anthropologist 1900 archive.org`
- `American Anthropologist volume 2 1900 full text archive`
- `"sungka" Visayan Philippine mancala rules Culin`
- `Culin "Philippine Games" American Anthropologist 1900 tapatan`
- `American Anthropologist volume 2 1900 archive.org full text`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/sungka/
06_FOUNDER_DELIVERY/tapatan/
```

---

### ▸ Pollux, Julius, Onomasticon, Book IX — denetlenebilir modern edisyon: E. Bethe (ed.), Pollucis Onomasticon (Leipzig: Teubner, 1900–1937)

| | |
|---|---|
| **AÇTIĞI MADDE** | **2** |
| **DURUM** | ⛔ **DENENDİ ve açılamadı** |
| **KANIT** | açık erişimli denetlenebilir edisyon bulunamadı; Yunanca metin ve satır numarası olmadan locator verilemez (source_verification.json · astragaloi kaydı) |
| **NEDEN** | Teubner edisyonunun açık tam metni bulunamadı. |

**NEREDE ARANIR**

- archive.org — Bethe Teubner cildi (kamusal alan, 1900–1937)
- Perseus Digital Library
- TLG (kurumsal erişim)
- Üniversite klasik filoloji kütüphanesi

**NE İSTİYORUZ**

myinda ve ephedrismos'un geçtiği pasajlar — Yunanca metin + kitap/bölüm/satır numarası + bir modern çeviri.

> Pollux bir OYUN LİSTESİ verir, bir kural kitabı değildir; kural boşluğu muhtemelen kaynakla KAPANMAYACAKTIR ve bu ayrıca kaydedilmiştir.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `ephedrismos` | Games Without a Board | Ancient Greek | C | 15.8 | Pollux IX'da ephedrismos pasajı — Yunanca metin + satır numarası |
| `myinda` | Games Without a Board | Ancient Greek | E | 15.8 | Pollux IX'da myinda/muinda pasajı — Yunanca metin + satır numarası + çeviri |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `"ephedrismos" Greek game reconstruction`
- `Pollux Onomasticon IX games Bethe edition`
- `"myinda" OR "muinda" Greek game Pollux`
- `ancient Greek blind man's buff game evidence`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/ephedrismos/
06_FOUNDER_DELIVERY/myinda/
```

---

### ▸ Kaydın KENDİSİ bulunamayan oyunlar — arama görevi kurucuya aittir

| | |
|---|---|
| **AÇTIĞI MADDE** | **2** |
| **DURUM** | ⛔ **DENENDİ ve açılamadı** |
| **KANIT** | archive.org tam metin + katalog taraması; Thurston 1906 tarandı, oyun bölümü yok (source_verification.json, 2026-08-14) |
| **NEDEN** | Bir erişim engeli DEĞİLDİR: erişilemeyen bir kayıt yok, HENÜZ UYGUN BİR KAYIT BULUNAMADI. Hiçbir kütüphane izni bunu var edemez. |

**NEREDE ARANIR**

- Kannada/Marathi dilinde dönem folklor derlemeleri
- Hindistan bölgesel devlet arşivleri · Karnataka & Maharashtra
- Deccan Gymkhana (Pune) arşivi — 1914 kural komitesi
- Akhil Maharashtra Shareerik Shikshan Mandal — 1935 kural kitabı
- Üniversite Güney Asya koleksiyonları (SOAS · Chicago · Penn)

**NE İSTİYORUZ**

lagori → 20. yy başı bir saha kaydı ya da dönem folklor derlemesi.
kho-kho → 1935 Akhil Maharashtra kural kitabının denetlenebilir nüshası (ya da 1914 Deccan Gymkhana komite kaydı).

> ⚠ Bu iki oyun kapsama K23 kapsam değişikliğiyle GİRDİ ve kaynağı bulunamadı. Kaynak gelmezse çözüm bir kapsam değişikliğidir, bir araştırma değil.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `lagori` | Games Without a Board | Kannada | E | 15.8 | 20. yy başı bir Güney Hindistan saha kaydı ya da folklor derlemesi |
| `kho-kho` | Games Without a Board | Marathi | E | 14.8 | 1935 Akhil Maharashtra kural kitabı — tarama ya da kütüphane künyesi |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `"lagori" OR "pittu" OR "lingocha" Karnataka game ethnography`
- `seven stones game South India folklore 1900s archive`
- `"kho kho" 1935 rulebook Akhil Maharashtra`
- `"kho-kho" Deccan Gymkhana 1914 rules`
- `kho kho indigenous games India codification archive`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/lagori/
06_FOUNDER_DELIVERY/kho-kho/
```

---

### ▸ Culin, Stewart, 'Hawaiian Games', American Anthropologist 1:2 (1899)

| | |
|---|---|
| **AÇTIĞI MADDE** | **1** |
| **DURUM** | ⛔ **DENENDİ ve açılamadı** |
| **KANIT** | yalnızca JSTOR nüshası bulundu; tam metin indirilemedi (sourceHunts · phase5-batch4, 2026-08-16) |
| **NEDEN** | 1899 tarihlidir ve KAMUSAL ALANDADIR; engel telif değil DAĞITIMDIR. |

**NEREDE ARANIR**

- archive.org — American Anthropologist cilt 1 (1899) ciltli sayısı
- HathiTrust tam görünüm
- JSTOR (kurumsal erişim)

**NE İSTİYORUZ**

kōnane bölümü, sayfa numarasıyla.

> Kamusal alan bir metnin JSTOR arkasında durması bir erişim sorunudur, bir telif sorunu değil — ve kütüphane erişimiyle çözülür.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `konane` | The War Board | Hawaiian | C | 20.4 | Culin, Stewart, 'Hawaiian Games', American Anthropologist 1:2 (1899) — kōnane bölümü, SAYFA NUMARASIYLA (KAMUSAL ALAN; ciltli dergi taraması aranma… |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `Culin "Hawaiian Games" American Anthropologist 1899 archive.org`
- `American Anthropologist volume 1 1899 full text HathiTrust`
- `konane Hawaiian checkers rules Bishop Museum`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/konane/
```

---

### ▸ de Voogt, Alex, Mancala Board Games (London: British Museum Press, 1997)

| | |
|---|---|
| **AÇTIĞI MADDE** | **1** |
| **DURUM** | ⛔ **DENENDİ ve açılamadı** |
| **KANIT** | telif altında; kamusal alan alternatifi tarandı ve uygun bulunmadı (source_verification.json · bao-la-kiswahili kaydı) |
| **NEDEN** | Telif altındadır. |

**NEREDE ARANIR**

- British Museum Press nüshası
- Üniversite kütüphanesi

**NE İSTİYORUZ**

oware ve toguz-kumalak maddeleri.

> bao-la-kiswahili İÇİN ARTIK GEREKMİYOR — o oyun kurucu teslimiyle yazıldı.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `toguz-kumalak` | The Sowing Games | Kazakh | D | 18.6 | Russ 2000 ya da de Voogt 1997'de toguz kumalak maddesi — 2×9 çukur, 9'ar tohum, tuzdyk (kutsal çukur) kuralı, kazan, alma koşulu, bitiş |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `"toguz kumalak" OR "togyz kumalak" rules tuzdyk Kazakh`
- `toguz korgool Kyrgyz Kazakh mancala historical rules`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/toguz-kumalak/
```

---

### ▸ Yaşayan federasyon/kodifikasyon kuralları

| | |
|---|---|
| **AÇTIĞI MADDE** | **1** |
| **DURUM** | ◻ **HİÇ DENENMEDİ** — engelli değil, sırası gelmedi |
| **KANIT** | proje FIPJP kural kitabını denemedi |
| **NEDEN** | Yayımlanmış ve erişilebilir; eksik olan KÜNYE (baskı · yıl · madde no) ve tarihsel çerçevedir. |

**NEREDE ARANIR**

- FIPJP resmî kural kitabı (fipjp.org) — sürüm ve yürürlük tarihi ile
- Pétanque'ın 1907 La Ciotat kökeni için dönem kaydı ya da akademik bir spor tarihi çalışması

**NE İSTİYORUZ**

petanque → (a) FIPJP kural kitabının SÜRÜMÜ ve madde numaraları, (b) jeu provençal / pétanque ayrımını ve 1907 kodifikasyonunu veren bağımsız bir tarihsel künye.

> Kayıt zaten uyarıyor: 'modern kodifikasyon 1907'dir; geleneksel etiketi dikkatle kullanılmalıdır.'

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `petanque` | Games Without a Board | Provençal | A | 18.8 | FIPJP resmî kural kitabı — SÜRÜM, yürürlük tarihi ve madde numaraları |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `FIPJP official rules of petanque PDF version`
- `petanque 1907 La Ciotat origin history jeu provençal`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/petanque/
```

---

### ▸ Murray, H. J. R., A History of Chess (Oxford: Clarendon Press, 1913)

| | |
|---|---|
| **AÇTIĞI MADDE** | **1** |
| **DURUM** | ⛔ **DENENDİ ve açılamadı** |
| **KANIT** | archive.org — HTTP 401 (ödünç kısıtı) (source_verification.json · shogi kaydı) |
| **NEDEN** | 1913 tarihlidir ve ABD'de KAMUSAL ALANDADIR; engel TELİF değil DAĞITIMDIR — nüsha ödünç kısıtı altındadır. |

**NEREDE ARANIR**

- HathiTrust tam görünüm (kamusal alan cildi)
- Google Books tam görünüm
- Üniversite kütüphanesi
- Oxford 1913 / Benjamin Press 1985 tıpkıbasımı

**NE İSTİYORUZ**

makruk (Siyam satrancı) bölümü — taşlar, kurulum, sayma (nap) kuralları.

> Kamusal alan olduğu hâlde açılamayan tek eser bu değildir; bu sınıf kütüphane erişimiyle en kolay çözülen sınıftır.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `makruk` | The War Board | Thai | E | 16.4 | Murray, A History of Chess (1913) — Siyam satrancı bölümü (HathiTrust ya da Google Books TAM GÖRÜNÜM; eser kamusal alandadır) |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `Murray "A History of Chess" 1913 HathiTrust full view Siamese`
- `makruk Thai chess rules counting nap`
- `makruk rules promotion third rank`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/makruk/
```

---

### ▸ Volpicelli, Z., 'Wei-ch'i', Journal of the China Branch of the Royal Asiatic Society, N.S. XXVI (1894)

| | |
|---|---|
| **AÇTIĞI MADDE** | **1** |
| **DURUM** | ◻ **HİÇ DENENMEDİ** — engelli değil, sırası gelmedi |
| **KANIT** | Smith 1908'in KENDİ künyesinde geçiyor; proje henüz aramadı |
| **NEDEN** | Eski dergi cildi; dijital nüshası aranmadı. |

**NEREDE ARANIR**

- archive.org — JCBRAS cilt XXVI
- HathiTrust
- Royal Asiatic Society China arşivi

**NE İSTİYORUZ**

Makalenin tamamı — ÇİN biçimini ve ÇİN alan sayımını veren bölüm.

> go'nun kültür uyuşmazlığını çözecek TEK adaydır: Smith 1908 tam bir kural kitabıdır ama JAPON kodifikasyonunu ve JAPON sayımını verir.

**AÇTIĞI MADDELER**

| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |
|---|---|---|:---:|---:|---|
| `go` | The Line and the Territory | Han Chinese | C | 18.6 | Volpicelli, Z., 'Wei-ch'i', Journal of the China Branch of the Royal Asiatic Society N.S. XXVI (1894) — Smith'in KENDİ künyesinde geçiyor |

**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin
var olduğu iddia edilmez*

- `Volpicelli "Wei-chi" Journal China Branch Royal Asiatic Society 1894`
- `weiqi Chinese area scoring rules 19th century source`
- `wei-ch'i Chinese go rules historical article archive.org`

**BUNLARI ŞURAYA BIRAKIN**

```
06_FOUNDER_DELIVERY/go/
```

---

## 3 · EN YÜKSEK ÖNCELİKLİ ON MADDE — TEK TEK

Kaynak kaynak liste verimlidir; bu bölüm ise **tek bir maddeyi**
bitirmek isteyen bir araştırmacı içindir.

---

```
GAME     : Morra (morra)
CULTURE  : Italian · Mediterranean
FAMILY   : Games Without a Board
PRIORITY : A · composite 21.8
BLOCKER  : P3 — RULES INCOMPLETE
```

**SEARCH FOR:**

1. Morra'nın PUANLAMASINI ve KAZANMA koşulunu veren herhangi bir künye
2. Tur yapısı: kaç el oynanır, puan nasıl birikir
3. Berabere durumunda ne olduğu

**MINIMUM ACCEPTABLE SOURCE:**

Kanıt listesi aşağıdadır; hepsi tek bir kaynaktan gelmek zorunda
değildir. `bibliography.md` hangi kanıtın hangi kaynaktan geldiğini
söylediği sürece iki ayrı kaynak birleştirilebilir.

```
RULE EVIDENCE
  [ ] turn order  [ ] scoring  [ ] end condition  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**PREFERRED SOURCE:** Bir İtalyan halk oyunları derlemesi ya da Parlett'in morra bölümü.

**WHAT TO RETURN:** PDF · tarama · kararlı URL · künye (yazar ·
başlık · baskı · yıl · **sayfa**) · ilgili sayfa aralığı · gerekirse
kısa bir kural özeti

**SAVE AS / DROP INTO:**

```
06_FOUNDER_DELIVERY/morra/source.pdf
06_FOUNDER_DELIVERY/morra/bibliography.md
```

---

```
GAME     : Bohnenspiel (bohnenspiel)
CULTURE  : German · Central Europe
FAMILY   : The Sowing Games
PRIORITY : A · composite 21.6
BLOCKER  : P1 — SOURCE ACCESS BLOCKED
```

**SEARCH FOR:**

1. Murray 1952 ya da Bell'de Bohnenspiel maddesi — 2×6 çukur, 6'şar tohum, ekim yönü, 2/4/6 alma kuralı, zincirli alma
2. Oyunun Avrupa'ya nasıl ulaştığına dair BİR İDDİA DEĞİL, bir kayıt (kayıt köken iddiasını açıkça yasaklıyor)

**MINIMUM ACCEPTABLE SOURCE:**

Kanıt listesi aşağıdadır; hepsi tek bir kaynaktan gelmek zorunda
değildir. `bibliography.md` hangi kanıtın hangi kaynaktan geldiğini
söylediği sürece iki ayrı kaynak birleştirilebilir.

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**PREFERRED SOURCE:** Alman kaynaklı bir dönem kaydı köken sorununu da hafifletir.

**WHAT TO RETURN:** PDF · tarama · kararlı URL · künye (yazar ·
başlık · baskı · yıl · **sayfa**) · ilgili sayfa aralığı · gerekirse
kısa bir kural özeti

**SAVE AS / DROP INTO:**

```
06_FOUNDER_DELIVERY/bohnenspiel/source.pdf
06_FOUNDER_DELIVERY/bohnenspiel/bibliography.md
```

---

```
GAME     : Bagh-Chal (bagh-chal)
CULTURE  : Nepali · South Asia
FAMILY   : The Hunt and the Siege
PRIORITY : A · composite 20.5
BLOCKER  : P1 — SOURCE ACCESS BLOCKED
```

**SEARCH FOR:**

1. Bell ya da Parlett'te bagh-chal maddesi
2. 5×5 köşegenli tahta, 4 kaplan / 20 keçi, yerleştirme aşaması, atlama-alma, kaplanların kilitlenmesi, kaç keçi kaybı kaplan galibiyeti

**MINIMUM ACCEPTABLE SOURCE:**

Kanıt listesi aşağıdadır; hepsi tek bir kaynaktan gelmek zorunda
değildir. `bibliography.md` hangi kanıtın hangi kaynaktan geldiğini
söylediği sürece iki ayrı kaynak birleştirilebilir.

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**PREFERRED SOURCE:** Nepal kaynaklı çağdaş bir künye ile birlikte olursa kültür atfı da güçlenir.

**WHAT TO RETURN:** PDF · tarama · kararlı URL · künye (yazar ·
başlık · baskı · yıl · **sayfa**) · ilgili sayfa aralığı · gerekirse
kısa bir kural özeti

**SAVE AS / DROP INTO:**

```
06_FOUNDER_DELIVERY/bagh-chal/source.pdf
06_FOUNDER_DELIVERY/bagh-chal/bibliography.md
```

---

```
GAME     : Kōnane (konane)
CULTURE  : Hawaiian · Oceania
FAMILY   : The War Board
PRIORITY : C · composite 20.4
BLOCKER  : P2 — SOURCE TEXT UNAVAILABLE
```

**SEARCH FOR:**

1. Culin, Stewart, 'Hawaiian Games', American Anthropologist 1:2 (1899) — kōnane bölümü, SAYFA NUMARASIYLA (KAMUSAL ALAN; ciltli dergi taraması aranmalı — proje bu makalenin sayfa aralığını henüz görmedi)
2. Tahta ölçüsü, ilk iki taşın kaldırılması, YALNIZCA atlayarak alma, çoklu atlama kuralı ve hamlesiz kalanın kaybetmesi
3. ÇAĞDAŞ Kānaka Maoli kaynaklı bir künye — atıf zorunluluğu için (Bishop Museum · Hawaiian kültür kurumları)

**MINIMUM ACCEPTABLE SOURCE:**

Kanıt listesi aşağıdadır; hepsi tek bir kaynaktan gelmek zorunda
değildir. `bibliography.md` hangi kanıtın hangi kaynaktan geldiğini
söylediği sürece iki ayrı kaynak birleştirilebilir.

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**PREFERRED SOURCE:** American Anthropologist cilt 1 (1899) taraması + Bishop Museum kaydı.

**WHAT TO RETURN:** PDF · tarama · kararlı URL · künye (yazar ·
başlık · baskı · yıl · **sayfa**) · ilgili sayfa aralığı · gerekirse
kısa bir kural özeti

**SAVE AS / DROP INTO:**

```
06_FOUNDER_DELIVERY/konane/source.pdf
06_FOUNDER_DELIVERY/konane/bibliography.md
```

---

```
GAME     : Yoté (yote)
CULTURE  : Wolof · West Africa
FAMILY   : The War Board
PRIORITY : C · composite 20.4
BLOCKER  : P2 — SOURCE TEXT UNAVAILABLE
```

**SEARCH FOR:**

1. Béart, Charles, Jeux et jouets de l'Ouest africain (Dakar: IFAN, 1955) — yoté bölümü (Fransızca)
2. 5×6 ızgara, elde tutulan taşların sırayla girmesi, atlayarak alma ve ALINAN HER TAŞLA BİRLİKTE İKİNCİ BİR TAŞIN DA KALDIRILMASI kuralı — oyunun ayırt edici mekaniği budur (distinct=5)
3. Wolof atfını veren bir kaynak

**MINIMUM ACCEPTABLE SOURCE:**

Kanıt listesi aşağıdadır; hepsi tek bir kaynaktan gelmek zorunda
değildir. `bibliography.md` hangi kanıtın hangi kaynaktan geldiğini
söylediği sürece iki ayrı kaynak birleştirilebilir.

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**PREFERRED SOURCE:** Béart 1955 — Batı Afrika oyunlarının en iyi saha kaydı; zamma ile AYNI kaynak, tek teslim iki oyun açar.

**WHAT TO RETURN:** PDF · tarama · kararlı URL · künye (yazar ·
başlık · baskı · yıl · **sayfa**) · ilgili sayfa aralığı · gerekirse
kısa bir kural özeti

**SAVE AS / DROP INTO:**

```
06_FOUNDER_DELIVERY/yote/source.pdf
06_FOUNDER_DELIVERY/yote/bibliography.md
```

---

```
GAME     : Ampe (ampe)
CULTURE  : Akan · West Africa
FAMILY   : Games Without a Board
PRIORITY : A · composite 19.8
BLOCKER  : P1 — SOURCE ACCESS BLOCKED
```

**SEARCH FOR:**

1. Zaslavsky 1973'te ampe maddesi — sıçrama/ayak biçimi, puanlama, tur, bitiş
2. GANA KAYNAKLI ikinci bağımsız künye (Akan çocuk oyunları derlemesi)

**MINIMUM ACCEPTABLE SOURCE:**

Kanıt listesi aşağıdadır; hepsi tek bir kaynaktan gelmek zorunda
değildir. `bibliography.md` hangi kanıtın hangi kaynaktan geldiğini
söylediği sürece iki ayrı kaynak birleştirilebilir.

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**PREFERRED SOURCE:** Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**WHAT TO RETURN:** PDF · tarama · kararlı URL · künye (yazar ·
başlık · baskı · yıl · **sayfa**) · ilgili sayfa aralığı · gerekirse
kısa bir kural özeti

**SAVE AS / DROP INTO:**

```
06_FOUNDER_DELIVERY/ampe/source.pdf
06_FOUNDER_DELIVERY/ampe/bibliography.md
```

---

```
GAME     : Pilolo (pilolo)
CULTURE  : Ga · West Africa
FAMILY   : Games Without a Board
PRIORITY : A · composite 19.8
BLOCKER  : P1 — SOURCE ACCESS BLOCKED
```

**SEARCH FOR:**

1. Zaslavsky 1973'te pilolo maddesi — saklama/arama sırası, puanlama, bitiş
2. GANA KAYNAKLI ikinci bağımsız künye (Ga çocuk oyunları)

**MINIMUM ACCEPTABLE SOURCE:**

Kanıt listesi aşağıdadır; hepsi tek bir kaynaktan gelmek zorunda
değildir. `bibliography.md` hangi kanıtın hangi kaynaktan geldiğini
söylediği sürece iki ayrı kaynak birleştirilebilir.

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**PREFERRED SOURCE:** Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**WHAT TO RETURN:** PDF · tarama · kararlı URL · künye (yazar ·
başlık · baskı · yıl · **sayfa**) · ilgili sayfa aralığı · gerekirse
kısa bir kural özeti

**SAVE AS / DROP INTO:**

```
06_FOUNDER_DELIVERY/pilolo/source.pdf
06_FOUNDER_DELIVERY/pilolo/bibliography.md
```

---

```
GAME     : Adji-boto (adji-boto)
CULTURE  : Ndyuka Maroon · South America
FAMILY   : The Sowing Games
PRIORITY : C · composite 19.6
BLOCKER  : P2 — SOURCE TEXT UNAVAILABLE
```

**SEARCH FOR:**

1. Herskovits, Melville J., 'Wari in the New World', Journal of the Royal Anthropological Institute 62 (1932) — makalenin tamamı
2. Ndyuka Maroon topluluğunun oyunla ilişkisini veren çağdaş bir kaynak (atıf zorunluluğu için)

**MINIMUM ACCEPTABLE SOURCE:**

Kanıt listesi aşağıdadır; hepsi tek bir kaynaktan gelmek zorunda
değildir. `bibliography.md` hangi kanıtın hangi kaynaktan geldiğini
söylediği sürece iki ayrı kaynak birleştirilebilir.

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**PREFERRED SOURCE:** 1932 makalesi kamusal alanda olabilir; JRAI ciltli sayısı ideal.

**WHAT TO RETURN:** PDF · tarama · kararlı URL · künye (yazar ·
başlık · baskı · yıl · **sayfa**) · ilgili sayfa aralığı · gerekirse
kısa bir kural özeti

**SAVE AS / DROP INTO:**

```
06_FOUNDER_DELIVERY/adji-boto/source.pdf
06_FOUNDER_DELIVERY/adji-boto/bibliography.md
```

---

```
GAME     : Congklak (congklak)
CULTURE  : Javanese · Southeast Asia
FAMILY   : The Sowing Games
PRIORITY : A · composite 19.6
BLOCKER  : P1 — SOURCE ACCESS BLOCKED
```

**SEARCH FOR:**

1. Murray 1952 ya da Russ 2000'de congklak/congkak/dakon maddesi
2. Çukur sayısı, depo (rumah) kuralı, eş zamanlı başlangıç olup olmadığı, ekim yönü, alma, tur sonu ve yeniden dizme kuralı
3. KARAR MALZEMESİ: sungka ile mekanik farkı — kitap ikisini ayrı madde yapacaksa farkı yazmalı

**MINIMUM ACCEPTABLE SOURCE:**

Kanıt listesi aşağıdadır; hepsi tek bir kaynaktan gelmek zorunda
değildir. `bibliography.md` hangi kanıtın hangi kaynaktan geldiğini
söylediği sürece iki ayrı kaynak birleştirilebilir.

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

**PREFERRED SOURCE:** Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**WHAT TO RETURN:** PDF · tarama · kararlı URL · künye (yazar ·
başlık · baskı · yıl · **sayfa**) · ilgili sayfa aralığı · gerekirse
kısa bir kural özeti

**SAVE AS / DROP INTO:**

```
06_FOUNDER_DELIVERY/congklak/source.pdf
06_FOUNDER_DELIVERY/congklak/bibliography.md
```

---

```
GAME     : Shisima (shisima)
CULTURE  : Luhya · East Africa
FAMILY   : The Line and the Territory
PRIORITY : A · composite 19.6
BLOCKER  : P1 — SOURCE ACCESS BLOCKED
```

**SEARCH FOR:**

1. Zaslavsky 1973'te shisima maddesi — sekizgen tahta, 3'er taş, hareket kısıtı, üçlü sıra, bitiş
2. KENYA KAYNAKLI ikinci bağımsız künye (Luhya)

**MINIMUM ACCEPTABLE SOURCE:**

Kanıt listesi aşağıdadır; hepsi tek bir kaynaktan gelmek zorunda
değildir. `bibliography.md` hangi kanıtın hangi kaynaktan geldiğini
söylediği sürece iki ayrı kaynak birleştirilebilir.

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

**PREFERRED SOURCE:** Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

**WHAT TO RETURN:** PDF · tarama · kararlı URL · künye (yazar ·
başlık · baskı · yıl · **sayfa**) · ilgili sayfa aralığı · gerekirse
kısa bir kural özeti

**SAVE AS / DROP INTO:**

```
06_FOUNDER_DELIVERY/shisima/source.pdf
06_FOUNDER_DELIVERY/shisima/bibliography.md
```

---

## 4 · TESLİMDEN SONRA NE OLUR

Kurucu direktifi § 18 bunu bağlayıcı kılar. Teslim geldiğinde ajan
**durmaz ve onay beklemez**:

```
  ./04_BUILD/founder_delivery_ingest.py        ← alır · hash'ler · denetler
        ↓
  kanıt listesi karşılandı mı?  ── hayır ──▶  eksik kanıt raporu · beklemede
        ↓ evet
  source_verification kaydı açılır (founderSupplied bayrağıyla)
        ↓
  engel çözülür · üretim kuyruğuna alınır
        ↓
  YAZ → DİYAGRAM → kaynak QA → oynanabilirlik QA → kültürel QA
        ↓
  dizgi · ölçüm · sayfa modeli · indeksler · arka madde
        ↓
  commit · push · CI YEŞİL → SONRAKİ OYUN
```

> Bir oyunun engeli çözüldüğünde **yarım bırakılmaz** (§ 19).
> Hedef `KAYNAK → TAM OYUN → QA → CI`'dır, `KAYNAK → TASLAK` değil.

