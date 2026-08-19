# FINAL WRITING PHASE CLOSURE

> **The Great Book of World Games** · Faz 5 · Batch 8 · dal: `main`
> Tarih: 19 Ağustos 2026
>
> ```
> TESLİM #1 SONRASI :  48 / 100
> TESLİM #2 SONRASI :  52 / 100
> ```

> ⛔ **FINAL VERIFIED SCOPE = 52 / 100.** Yazım fazı **kapanmadı**;
> kaynağı olan üretim tükendi. Gerekçe § 7'de sayılarla duruyor ve
> § 5'te kurucunun beklediği dokuz oyunun neden dört çıktığı ölçülüyor.

---

## 1 · KURUCUDAN ALINAN DOSYALAR (teslim #2)

| dosya | boyut | GERÇEKTE NE |
|---|---:|---|
| `vdoc.pub_africa-counts-…pdf` | 12 MB | ✅ **Zaslavsky, *Africa Counts*** — GERÇEK, 369 s., ABBYY metin katmanı |
| `Mancala.pdf` | 3.6 MB | ◻ **de Voogt, "Mancala: Games That Count"**, *Expedition* 43/1 — DERGİ YAZISI; ayrıca **görüntü-only** (0 çıkarılabilir karakter) |
| `179359925-omweso-pdf.pdf` | 2.2 MB | ◻ **Wernham**, *International Omweso Society* araştırma özeti — Nsimbi'ye dayanır |

**Russ, *The Complete Mancala Games Book* GELMEDİ.** Önceki teslimdeki
yapay zekâ çıktısı hâlâ dizindedir ve hâlâ kullanılmamaktadır.

---

## 2 · YENİ KAYNAKLAR DOĞRULANDI

### 2.1 Zaslavsky — GERÇEK ve tam

```
Claudia Zaslavsky, Africa Counts: Number and Pattern in African Cultures
369 sayfa · ABBYY FineReader metin katmanı · sayfa denklemi: basılı = pdf − 16
```

PDF künyesi başlığı ve yazarı doğruluyor. Metin katmanı 496 583 karakter.

### 2.2 `Mancala.pdf` bir kural kaynağı DEĞİL

Alex de Voogt'un *Expedition* dergisindeki kültür yazısı: tahta
fotoğrafları, havaalanı anıları, yayılım haritası. **Kural seti yok.**
Ayrıca metin katmanı **yok** — beş sayfa da görüntü. Sayfalar RENDER
edilip gözle okundu ve içerik böyle saptandı.

### 2.3 Wernham özeti — ikinci BAĞIMSIZ kaynak değil

Adlı yazar ve kurumu olan gerçek bir araştırma özeti, kaynakçasında
Nsimbi (1968) var. Ama omweso kuralları için **Zaslavsky ile aynı köke**
(Nsimbi) dayanır, yani `SOURCING_STANDARD § 3` uyarınca bağımsız
sayılmaz. Kural seti için **kullanılmadı**; Zaslavsky sayfa-doğrulanmıştır.

---

## 3 · ⛔ ZASLAVSKY BEKLENEN ALTI OYUNU AÇMADI — ölçüm

Boşluk kaydı Zaslavsky'nin **altı** oyun açacağını söylüyordu. Kitap
geldi ve **kelime sınırıyla** arandı:

| oyun | *Africa Counts* içinde geçiş |
|---|---:|
| `ampe` | **0** |
| `pilolo` | **0** |
| `shisima` | **0** |
| `morabaraba` | **0** |
| `mefuvha` | **0** |
| `ayoayo` (`ayo`) | 7 — ama **kural seti yok** |
| `omweso` | **19 — TAM KURAL SETİ** |

**Bu kitap o beş oyunu içermiyor.** Projenin envanteri onları
*Africa Counts*'a yanlış atfetmiş; büyük olasılıkla Zaslavsky'nin
1998 tarihli *Math Games and Activities from Around the World* adlı
AYRI kitabıyla karışmış.

`ayoayo` da açılmadı: Zaslavsky Yoruba künyesini verir ama kuralı için

> *"The rules are similar to those of the Asante game wari."*

der. Bu bir **çapraz göndermedir**, kural seti değil — ve ondan yazmak
zaten yazılmış `oware`'ın kopyasını üretirdi.

> **Bu bir kurucu hatası değildir.** Kurucu istenen kitabı teslim etti.
> Hatalı olan, kitabın içindekini görmeden yazılmış olan **envanter
> atfıydı** — ve ancak sayfa açılarak görüldü.

---

## 4 · YAZILAN OYUNLAR — bu fazda dört

| oyun | aile | kültür | kaynak |
|---|---|---|---|
| **Omweso** | ekim | Ganda | Zaslavsky ss. 133–136 (Nsimbi 1968 temelli) |
| **Dama** | savaş tahtası | Türk | Bell s. 74 (fig. 60 **gözle** okundu) |
| **Jeu de Dames** | savaş tahtası | Fransız | Bell ss. 74–75 (fig. 61 **gözle** okundu) |
| **Bul** | eve dönüş | Kekchi Maya | Bell ss. 89–90 ('Puluc') |

Üçü **Bell'den** geldi — teslim #1'de adı hiçbir şey söylemeyen
`B-001-002-771.pdf`. Bir kaynak tükenmiş sayılmadan önce **içindekiler
dizini** okunmalıdır: bu fazın en verimli hamlesi Bell'in 43 bölüm
başlığını basılı sayfa numaralarıyla çıkarmak oldu.

### Kurulum ŞEKİLLERİ gözle okundu

`turkish-dama` ve `jeu-de-dames` için kurulum metinde **yoktur**;
Bell onu fig. 60 ve fig. 61'e havale eder. Metin katmanı şekil içeriğini
vermez. **Sayfalar render edildi ve şekiller okundu:**

- fig. 60 → 8×8, her tarafta **ikinci ve üçüncü sıra** dolu, geri sıra **boş** = 16 taş
- fig. 61 → 10×10, her tarafta **dört** dolu sıra = 20 taş

Ezberden yazılmadı; **bakıldı**.

---

## 5 · YAZILMAYAN VE NEDENİ

| oyun | bulunan | neden yazılmadı |
|---|---|---|
| `ayoayo` | Zaslavsky Yoruba künyesi | kural seti yok, **çapraz gönderme** var |
| `ampe` `pilolo` `shisima` `morabaraba` `mefuvha` | — | **kitapta yok** |
| `congklak` `adji-boto` `toguz-kumalak` | — | **Russ gelmedi** |
| `bagh-chal` | Murray'de dört madde | **dördü de Hindistan**, kapsam Nepalli |
| `game-of-the-goose` | Bell'de tam kural | kurallar **1725 İngiliz levhasından**, kapsam İtalyan |
| `konane` | Murray § 4.11.4 | Murray *"none … gives any clear indication of how it is played"* der → **FINAL SOURCE BLOCKED** |
| `alquerque` | Bell s. 48 | Bell: *"These rules … are not sufficient to play a game"* + kendi *Suggested Additional Rules*'u → yazılırsa **reconstructed** olmak zorunda |

---

## 6 · DEĞİŞTİRİLEN OYUN: HİÇBİRİ — ve nedeni ölçüldü

Kurucu § 10 ve § 26 değiştirme yetkisi verdi. Yedek havuz **19 madde**
olarak açıldı ve ölçüldü:

| yedek havuzun gerçek durumu | sayı |
|---|---:|
| Toplam kayıt | 19 |
| **Zaten KAPSAMDA olan** (yani değiştirme değil) | **10** |
| ↳ bunlardan zaten YAZILMIŞ (`achi` · `janggi`) | 2 |
| Gerçekten kapsam DIŞI | **9** |
| ↳ **elimdeki kaynaklarla yazılabilir** | **2** |
| ↳ ↳ bunlardan biri (`puluc`) **`bul` ile AYNI OYUN** | 1 |
| **Kullanılabilir gerçek yedek** | **1** (`cho-han`) |

### İki envanter kusuru bulundu

1. **`puluc` ve `bul` aynı oyundur.** İkisi de Kekchi Maya, ikisi de
   Sapper/Verbeeck hattı; Bell'in *Puluc* bölümü `bul`'un kaynağıdır.
   Biri kapsamda, öteki yedekte duruyor. **İkisini de yazmak yinelenen
   madde üretirdi** — yazılmadı, kayda geçirildi.
2. **Yedek havuzun yarısı zaten kapsamdadır** (`achi` ve `janggi` dahil,
   ki ikisi de basılmıştır). Havuz bir **sigorta** değil, kapsamın
   gölgesidir.

### Karar

**Değiştirme yapılmadı.** Gerekçe aritmetiktir: 48 boş slot vardır ve
yedek havuz **bir** kullanılabilir aday sunmaktadır. Kalan 41 maddenin
engeli bir aday kalitesi sorunu değil, hâlâ bir **arz** sorunudur —
ve § 12 güçlü maddeleri (`oware`, `pallanguzhi`) kolay olanla
değiştirmeyi açıkça yasaklar.

Tek kullanılabilir yedek `cho-han` (Japon, şans) idi. Şans ailesinin
tek boş slotu `mahjong`'undur ve `mahjong` **Bell s. 161'de vardır** —
yani o slot bir kaynak sorunu değil bir **sayfa bütçesi** sorunudur
(projenin kendi kaydı: *"650 kelimeye SIĞMAZ"*). Bir yedeği araya
sokmak, çözülebilir bir maddeyi kapsamdan atmak olurdu.

---

## 7 · NİHAİ KAPSAM

```
FINAL VERIFIED SCOPE = 52 / 100
```

| | |
|---|---:|
| Kapsam hedefi | 100 |
| **Yazılmış** | **52** |
| Kurucu müdahalesi olmadan yazılabilir | 7 |
| Kalan engelli | 41 |
| ↳ `BLOCKED` | 26 |
| ↳ `SOURCE-PENDING` | 13 |
| ↳ `UNRESOLVED` | 2 |
| `UNATTEMPTED` | **0** |

**100 neden bu pasta ulaşılamadı:** 48 slot açıktır; yedek havuz bir
aday verir; kalan 41 maddenin çoğu hâlâ elde olmayan eserlere bağlıdır
(Culin 1895/1907, Russ 2000, Parlett'in TAM metni, Béart 1955,
Townshend 1979, Odeleye 1977 ve bir dizi dergi makalesi). Uydurmadan
kapatılamaz — ve § 31 uydurmayı yasaklar.

---

## 8 · AİLE DAĞILIMI

| aile | yazılan | hedef | açık | tamamlanma |
|---|---:|---:|---:|---|
| The War Board | 13 | 21 | 8 | `███████·····` 62% |
| The Race Home | 11 | 18 | 7 | `███████·····` 61% |
| The Line and the Territory | 8 | 17 | 9 | `█████·······` 47% |
| Games Without a Board | 7 | 16 | 9 | `█████·······` 44% |
| The Hunt and the Siege | 5 | 10 | 5 | `██████······` 50% |
| **The Sowing Games** | **5** | 14 | 9 | `████········` 36% |
| Chance and Nerve | 3 | 4 | 1 | `█████████···` 75% |

**Sapma ve gerekçesi (§ 13):** hiçbir aile hedefi değiştirilmedi. Hiçbir
aile çökmedi. Ekim ailesi hâlâ en zayıf küme ve sebebi tektir: Russ
gelmedi ve Zaslavsky beklenen ekim oyunlarını içermiyordu. Savaş tahtası
baskın **değildir** (13/52 = %25, hedef payı %21).

---

## 9 · KÜLTÜR VE BÖLGE

| | |
|---|---:|
| Yazılan kültür | **36** |
| Kapsam vaadi | 68 |
| Yazılan bölge | **21** |

Bu faz **dört yeni kültür** getirdi: Ganda · Türk · Fransız · Kekchi
Maya. Boardless ailesindeki eski *İngiliz yoğunlaşması* sorunu geri
gelmedi (aile 7 maddede 6 kültür taşıyor).

---

## 10 · SAYFA VE KELİME — GERÇEK DİZGİDEN

| | |
|---|---:|
| **Toplam sayfa (model)** | **254** |
| Yol haritası hedefi | 256 |
| **Sapma** | **−0,8 %** ✅ |
| Ölçülen madde | 52 |
| **Ölçülen kelime** | **37 863** |
| Kelime / oyun | 728 (bant 480–900) |
| Sayfa / oyun | 1,53 |
| Faturalanan sayfa / oyun | 2,04 |
| Çift sayfayı aşan madde | 1/52 (`tablut`) |
| Ciltsiz telif | 8,48 $ |
| Ciltli telif | 11,03 $ |

Model **altı batch'tir** ±%1 içinde. Kanonik ölçüm dosyası
`06_REPORTS/phase2-typeset-measurement.json`'dir; önceki batch'lerde
yalnızca arşiv kopyası yazıldığı için `--check` bir kez bayat kalmıştı
ve bu düzeltildi.

---

## 11 · DİYAGRAM

| | |
|---|---:|
| Render edilen SVG | **49** |
| Diyagramsız madde | **11** (hepsinin sebebi kayıtlı) |
| Diyagram dili | **v1.5 — DEĞİŞMEDİ** |
| 150 mm'yi aşan (K24 dışında) | **0** |

### Görsel denetim bu fazda İKİ kusur daha buldu

Sayısal kapı ikisini de **yeşil** geçirdi:

| kusur | ne olurdu |
|---|---|
| `omweso-capture` — `pit` sınıfının koordinatı (`row-pit`) **yalnızca A ve B sırasını** tanır; dört sıralı tahtanın iki sırası BOŞ çizildi | Dört sıralı bir oyun iki sıralı gibi basılırdı |
| `dama-orthogonal` — `forbidden` oku `move` ile **aynı** çiziliyor | **Yasak** köşegen hamle **yasal** görünürdü |

Birincisinde diyagram **geri çekildi**, ikincisinde **ok çıkarıldı**.
Bu, K32'nin (`track` → yut-nori) üçüncü ve dördüncü örneğidir:
**ölçülen bir diyagram, doğru bir diyagram değildir.**

---

## 12 · KAYNAK DOĞRULAMA

| | |
|---|---:|
| Doğrulama kaydı | **69** |
| `verified` | **50** |
| `pending` | 10 |
| `blocked` | 9 |
| Sayfa veren madde | 41 |
| **Hayalet künye** (sayfa var, doğrulanmış kayıt yok) | **0** ✅ |
| İki BAĞIMSIZ kaydı olan madde | **4** ⚠ |
| **Uydurulmuş sayfa / künye** | **0** ✅ |

Tam denetim: [`FINAL_SOURCE_AUDIT.md`](FINAL_SOURCE_AUDIT.md)

---

## 13 · YENİDEN KURGULAMA

**7 madde** `reconstructed` işaretlidir ve yedisinin de beyanı vardır;
madde ile envanter arasında **0** uyuşmazlık.

Ayrıca `bul` için bir **kısmi kanıt beyanı** eklendi: Bell tek sarı yüz
için puan vermez ve kitabın *"hamle yok"* çözümü prozada **editoryal**
ilan edilir (§ 16).

---

## 14 · OYNANABİLİRLİK

| | |
|---|---:|
| Beş öğe tam | **52 / 52** ✅ |
| Üç soru (berabere · kilit · kural dışı) | **52 / 52** ✅ |
| **DIŞ TEST** | **0 oturum · 0 kayıt** ⛔ |
| `locked` oyun | **0** |

```
PRODUCTION        : AUTHORIZED
FORMAL VALIDATION : PENDING
```

`.gate` = `phase1`, **yükseltilmedi**.

---

## 15 · GIT / CI

| | |
|---|---|
| Dal | `main` · açık PR **yok** |
| CI | ✅ **YEŞİL** |
| Bu fazın commit'i | 3 (batch 8 · batch 8b · kapanış) |

---

## 16 · KALAN RESMÎ DOĞRULAMA GEREKSİNİMLERİ

1. **Dış oynanabilirlik testi — 0 oturum.** `PLAYABILITY_STANDARD § 4`
   testçinin **insan** olmasını şart koşar; ajan bunu yapamaz. Hiçbir
   oyun bu yapılmadan `locked` olamaz.
2. **İkinci bağımsız kaynak — 52 maddenin 48'inde yok.**
3. **48 slot yazılmadı.**

---

## 17 · FAZ 6 HAZIRLIĞI

| hazır | değil |
|---|---|
| 52 madde · beş öğe ve üç soru tam | **48 madde yazılmadı** |
| Sayfa modeli altı batch'tir ±%1 (254) | **Dış test kanıtı (0)** |
| Ekonomi senkron (8,48 $ / 11,03 $) | `locked` oyun (0) |
| Diyagram dili v1.5 · 49 SVG · bütçe içinde | 11 madde diyagramsız |
| Arka madde üretildi · 100 maddelik kaynakça | Ön madde ve giriş denemesi |
| 192 kasıtlı kusur testi · CI yeşil | ~130 görsel |

---

## 18 · DURUM

```
BOOK CONTENT : 52 / 100 · YAZIM SÜRÜYOR
PHASE 6      : BAŞLAMADI
```

**KDP'ye dokunulmadı. Kapak yapılmadı. A+ yapılmadı. Prova sipariş
edilmedi. Yayımlanmadı.**

Bu rapor *"KDP READY"* **demiyor** ve *"BOOK CONTENT COMPLETE"* de
**demiyor**. Ajan kaynağı olan her oyunu yazdı, kaynağı olmayanı
uydurmadı, ve yedek havuzun kapatamayacağı bir açığı kapattı gibi
göstermedi.
