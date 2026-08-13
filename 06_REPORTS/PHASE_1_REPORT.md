# FAZ 1 RAPORU — Envanter, tasnif ve oynanabilirlik mimarisi

> **The Great Book of World Games** · Faz 1 · Kapı: `phase1`
> Dal: `faz/1-envanter` · Etiket: `v0.1.0`
>
> Bu faz **tek bir cümle proza yazmadı**. Ürettiği şey kitabın veri
> omurgası, tasnif tezi ve oynanabilirlik mimarisidir.
>
> Ölçülen sayılar `BOOK_STATS.md` ve `06_REPORTS/*.json` içinde durur ve
> **üretilir**; bu rapor onları yorumlar.

---

## 0 · Tek bakışta

| | Ölçülen | Hedef | Durum |
|---|---:|---:|---|
| Envanter kaydı | **160** | — | |
| Aday oyun (`dropped` hariç) | **153** | ≥140 | ✅ |
| Farklı kültür (yayımlanabilir) | **89** | ≥45 | ✅ **%98 fazla** |
| Farklı bölge | **34** | — | |
| Mekanik aile | **7** | 7 | ✅ |
| Aile başına aday tabanı | **20–24** | ≥16 | ✅ 7/7 |
| Kısıt taraması | **160/160** | muafiyetsiz | ✅ |
| Kural bütünlüğü değerlendirmesi | **160/160** | — | ✅ |
| Üretime hazır kural seti | **119** | — | |
| Kaynak künyesi | **300** | ≥1/oyun | ✅ |
| Sayfa modeli | **250** | 256 ± %6 | ✅ **−%2,3** |
| Kapıların kendi testi | **83 denetim** | 0 hata | ✅ |

**Faz 1 PASS.** Yol haritasının dört PASS ölçütünün dördü de karşılandı.
Bir FAIL ölçütü tetiklendi ve bir **kapsam bulgusu** üretti (§ 5).

---

## 1 · Aday envanteri

### 1.1 Aile dağılımı

| Aile | Kayıt | Aday | **Uygun** | Taban | Hedef |
|---|---:|---:|---:|---:|---:|
| I · Ekim oyunları | 21 | 20 | 14 | 16 | 14 |
| II · Av ve kuşatma | 21 | 21 | **10** | 16 | 14 |
| III · Eve dönüş yarışı | 24 | 24 | 19 | 16 | 15 |
| IV · Çizgi ve toprak | 20 | 20 | 18 | 16 | 14 |
| V · Savaş tahtası | 24 | 24 | 20 | 16 | 13 |
| VI · Şans ve cesaret | 22 | 22 | 19 | 16 | 15 |
| VII · Tahtasız oyunlar | 28 | 22 | 19 | 16 | 15 |
| **Toplam** | **160** | **153** | **119** | 112 | 100 |

**"Uygun" ne demek:** kitaba girebilmek için üç şartı birden geçen kayıt —
düşmemiş, kısıt taramasından `open` ya da `attributed` çıkmış, ve kuralları
oynanacak kadar bilinen. Bu sütun, ham aday sayısından çok daha anlamlıdır:
**153 aday vardır ama kitaba aday olan 119'dur.**

### 1.2 Envanterin katmanları

```
160 kayıt
├── 153 aday
│   ├── 119 UYGUN  ← kitabın seçileceği havuz
│   │   ├── 109 rules-complete
│   │   └──  10 reconstructed (beyanlı)
│   ├──  32 unresolved  — temel bir kural bilinmiyor, UYDURULMADI
│   └──   2 restricted  — anlatılır, oynatılmaz
└──   7 dropped — gerekçesi kayıtta
```

### 1.3 Coğrafi ve kültürel yayılım

89 farklı kültür, 34 bölge. Alt başlığın vaat ettiği 45 sayısının **iki
katı**. Bu, kapsamın rahat olduğu anlamına gelir: kitap kültür bulmakta
değil, **seçmekte** zorlanacaktır — ki bu iyi bir sorundur.

Öneri listesi (96 oyun) yalnız başına **71 farklı kültür** taşıyor.

---

## 2 · Taksonomi — yedi aile

Yedi aile `01_SOURCE/family_index.json` içinde tanımlandı. Her aile dört
zorunlu alan taşır: tanım · giriş kuralı · dışlama kuralı · **sınır kuralı**.

### 2.1 Tasnif deterministiktir

Bir oyun aileye **sabit sıralı** yedi soruyla atanır. İlk "evet" aileyi
belirler; sıra değişirse tasnif değişir, bu yüzden sıra kilitlidir.
Yordam `family_index.json § classificationProcedure` içindedir.

### 2.2 En zor sınır ve çözümü

> **"Değirmen oyunları territory mi, war-board mı?"**

Dokuz Taş'ta oyuncu taş alır — bu onu bir savaş tahtası yapar mı?

**Bulunan ölçüt tek yönlüdür ve deterministiktir:**

> Alma bir **HAMLE** mi, yoksa bir **DİZİLİŞİN SONUCU** mu?

Dokuz Taş'ta hiçbir tur "şu taşı al" hamlesi değildir: değirmen kurulur ve
alma ondan **doğar**. Damada alma turun kendisidir. Ölçüt, aynı cümleyle
iki ailenin sınır bölümünde birden yazılıdır ve iki farklı ajanı aynı
sonuca götürür.

İkinci en zor sınır — `chance` ↔ `boardless` — **nesneyle** çözüldü: şans
ailesi bir çekiliş aleti ister (zar, aşık kemiği, çubuk, kart); tahtasız
aile bedeni ya da bulunmuş nesneyi **beceri** için kullanır. Aynı aşık
kemiği, atılıp puan yazılırsa `chance`, havaya atılıp yakalanırsa
`boardless` olur — ve bu ayrım kayıtta gerekçesiyle durur.

### 2.3 İkincil aile

Üç oyun (`nine-mens-morris`, `dara`, `shax`, `morabaraba`) ikincil aile
taşır. İkincil aile **kitapta basılmaz**; yalnızca kararın tartışmalı
olduğunu kayda geçirir. Okur her oyunu tek yerde bulur.

---

## 3 · Araştırma ve kaynak istatistikleri

### 3.1 Künye sayıları

| | |
|---|---:|
| Toplam kaynak künyesi | **300** |
| Oyun başına ortalama | 1,9 |
| ≥2 **bağımsız** kaynağı olan oyun | **122** |
| Tek kaynaklı oyun | 38 |

### 3.2 Kaynak tipleri

| Tip | Sayı |
|---|---:|
| `book` — monografi | 178 |
| `ethnography` — saha derlemesi | 56 |
| `journal` — hakemli makale | 32 |
| `archive` — tarihsel belge / el yazması | 26 |
| `museum` — müze kaydı | 4 |
| `field-record` — doğrudan aktarım | 4 |

Omurga kamusal alan literatürüdür: Murray (1913, 1952), Culin (1895, 1898,
1900, 1907), Bell (1960–69), Parlett (1991, 1999), Gomme (1894–98),
Best (1925), Béart (1955), Zaslavsky (1973), de Voogt (1995, 1997),
Finkel (2007). Birincil kaynaklar arasında Alfonso X'in *Libro de los
juegos*'u (1283), Linnaeus'un 1732 Lapland günlüğü, Agathias'ın Zeno
epigramı, Durán ve Sahagún'un kronikleri, Lane'in 1836 Mısır kaydı yer alır.

### 3.3 Güven seviyeleri

| Seviye | Sayı |
|---|---:|
| `medium` | 60 |
| `high` | 47 |
| `low` | 35 |
| `reconstructed` | 18 |

### 3.4 ⚠ DOĞRULAMA SEVİYESİ — bu raporun en önemli dürüstlük notu

**160 kaydın 160'ı `sourceVerification: bibliographic` taşır.**

Bu şu demektir: eser ve içerdiği oyun künyelendi, ama **sayfa açılıp
doğrulanmadı**. Faz 1 künye seviyesinde çalışır.

Bu bir eksiklik değil, bir **ayrımdır** ve gizlenmek yerine bir alana
bağlanmıştır. `validate_research.py`, bir oyun `locked` olacaksa
`page-verified` şart koşar ve her künyede bir `locator` arar. Yani:

> **Doğrulanmamış bir künyenin doğrulanmış gibi görünmesi mekanik olarak
> imkânsızdır.**

Faz 2'nin ilk işi, pilot oyunların künyelerini sayfa seviyesine çıkarmaktır.

---

## 4 · Oynanabilirlik bulguları — bu fazın asıl işi

Kitabın ölüm biçimi tektir: **oyun çalışmıyor.** Faz 1 bu riski veri
katmanında ölçülebilir kıldı.

### 4.1 Beş öğe kapısı

Her kayıt beş öğe için ayrı ayrı değerlendirildi:
**kurulum → oyun → tur mantığı → hedef → bitiş koşulu.**

| Kural bütünlüğü | Sayı |
|---|---:|
| `complete` — beşi de bilinir | 116 |
| `partial` — biri kısmen bilinir | 35 |
| `incomplete` — biri bilinmiyor | 9 |

`qa_rules.py` şunu mekanik olarak imkânsız kılar: **bir öğe `unknown` iken
verdict `complete` olamaz.** Kurgusal tamamlamanın önündeki tek engel budur
ve bir disiplin cümlesi değil, bir kapıdır.

### 4.2 Netlik testi — taze okur

Beş soru her kayıt için cevaplandı: kurulum yapılabiliyor mu · ilk hamle
atılabiliyor mu · yasal hamle yasadışıdan ayrılabiliyor mu · kazanan
belirlenebiliyor mu · berabere tanımlı mı.

`rules-complete` sayılan **109 oyunun 109'u** beş sorunun beşini de geçiyor.
İstisna yoktur.

### 4.3 Sonsuz oyun sorunu

Döngü riski taşıyan her üretim adayının **bitiş kuralı şimdiden yazılı**.
Masada "e şimdi ne olacak?" sorusunun cevabı Faz 4'te aranmaz. Örnek:
Oware'de bir devir boyunca alma olmazsa oyun biter ve her oyuncu kendi
tarafındakini alır — bu editoryal bir karardır ve prozada söylenecektir.

### 4.4 Yeniden kurgulanan on oyun — ve neden gizlenmiyor

On oyun `reconstructed` taşıyor: `royal-game-of-ur`, `senet`, `hnefatafl`,
`tablut`, `ludus-duodecim-scriptorum`, `ludus-latrunculorum`, `patolli`,
`chaturanga`, `terni-lapilli`, `ephedrismos`.

Faz 1 sırasında **şemada bir boşluk bulundu ve kapatıldı.** İlk hâlinde
"yeniden kurgulandı" tek başına bir etiketti — ve bir etiket, uydurma ile
yeniden kurgulama arasında **mekanik bir fark üretmiyordu.**

Eklenen alan: **`reconstructionPlan`**. Netlik testinden düşen her
`reconstructed` kayıt, şunu yazmak zorundadır:

> **hangi boşluk** · **hangi kaynağa dayanarak** · **hangi editoryal kararla**

`qa_rules.py` bunu şart koşar. Sonuç: yeniden kurgulama **kayıt tutmadan
yapılamaz.** Sekiz kayıt bu planı taşıyor.

### 4.5 Otuz iki `unresolved` oyun — ve neden tamamlanmadı

Otuz iki oyunun temel bir kuralı bilinmiyor. Dokuzunda kural **hiç yoktur**:

| Oyun | Elimizde olan | Olmayan |
|---|---|---|
| Mehen | tahta, taşlar, mezar resimleri | kuralın tamamı |
| Liubo | tahta, mezar sanatı, TLV deseni | kuralın tamamı |
| Alea Evangelii | 12. yy el yazması ve diyagram | hareket ve alma |
| Brandubh | şiirsel kayıt, 7×7 tahtalar | hareket kuralı |
| Tawlbwrdd | 1587 el yazması, dizilim | hareket ve alma |
| Petteia | Platon'un göndermeleri | kural metni |
| Hounds and Jackals | 58 delikli tahtalar | hareketi ne ürettiği |

**Bunlar tamamlanmadı.** Bir aile oyunu kitabı için bu maddeleri "çalışır
hâle getirmek" kolaydı ve yanlış olurdu. Kitap onları *"kuralı kaybolmuş
oyunlar"* bölümünde anlatacak — oyun olarak değil, **boşluk olarak**.

> Mehen bu kitabın dürüstlük sınavıdır: güzel bir tahta, büyüleyici bir
> hikâye — ve oynanamaz. Bunu söylemek, söylememekten daha değerlidir.

---

## 5 · KAPSAM BULGUSU — av ve kuşatma ailesi

Yol haritasının FAIL ölçütlerinden biri tetiklendi.

**Av ve kuşatma ailesi 21 aday taşıyor (taban 16 ✅) ama yalnızca 10'u
uygun.** Hedef 14'tü.

**Sebep veri hatası değil, araştırma gerçeğidir.** Ailenin adayları iki
kümede toplanıyor ve her iki küme de ayrı bir duvara çarpıyor:

| Küme | Örnek | Duvar |
|---|---|---|
| Tafl kümesi | Tawlbwrdd · Brandubh · Alea Evangelii | **kural yok** — kaynaklar tahtayı verir, hareketi vermez |
| Kaplan-keçi kümesi | Huli-gatta · Bagha Guti · Pulijudam · Komikan · Adugo | **tek kaynak** ve berabere tanımsız |

`score_candidates.py` bir yeniden dengeleme **öneriyor** (toplam 100 korunur):

| Aile | Mevcut | Önerilen |
|---|---:|---:|
| Av ve kuşatma | 14 | **10** |
| Savaş tahtası | 13 | **17** |

**Karşı gerekçe de kayda geçer:** av-kuşatma, kitabın en görsel ve en
çocuk-dostu ailesidir; küçültmek onu zayıflatır. Alternatif, hedefi korumak
ve dört kaplan-keçi oyununa ikinci bağımsız kaynak aramaktır (bölgesel
Hint derlemeleri, Mapuche ve Bororo topluluk kaynakları).

**Karar kurucunundur (A2/A3).** Bu rapor iki yolu da yazar, birini seçmez.

> Yol haritası bunu zaten söylemişti: *"Bu FAIL'ler proje ölümü değildir.
> Hepsi hipotez düzeltmesidir ve Faz 1'in varlık sebebi tam olarak budur."*
> Bir sayıyı burada düzeltmek ucuz; Faz 4'te düzeltmek üç aylık iştir.

---

## 6 · Kültürel kısıt taraması — 160/160, muafiyetsiz

| Durum | Sayı | Kitapta |
|---|---:|---|
| `open` | 116 | ✅ serbest |
| `attributed` | 35 | ✅ kültürel atıf **zorunlu** |
| `restricted` | 6 | ⛔ eğlenceye çevrilemez |
| `excluded` | 3 | ⛔ kitaba giremez |

`qa_taxonomy.py` iki şeyi birden şart koşar: `attributed`/`restricted`/
`excluded` her kaydın **gerekçesi** olmalı, ve `restricted`/`excluded` her
kayıt editoryal olarak da **reddedilmiş** olmalı. Tek yerde söylenen bir
eleme, ikinci bir betiğin onu sessizce kitaba almasına izin verirdi.

### 6.1 Altı `restricted` kayıt

| Oyun | Kültür | Neden |
|---|---|---|
| **Dehontsigwa'ehs** | Haudenosaunee | Yaratıcı'nın oyunu; **şifa için** oynanan bir ilaç oyunudur, izinle düzenlenir. Sömürge adı "lacrosse" ne olduğunu gizler. |
| **Toli** | Choctaw | Yaşayan törensel uygulama; anlaşmazlık çözmeyle iç içe |
| **Pitz** | Maya (Klasik) | Kozmolojik anlatı ve kurban bağlamı — **ayrıca kuralları bilinmiyor** |
| **Na'atl'o'** | Navajo (Diné) | İp figürleri **yalnızca kışın**, örümcekler uyurken oynanır; bu estetik bir gelenek değil, bir uygulama kuralıdır |
| **Ayaraaq** | Inuit | Mevsime bağlı; belirli figürler anlatı ve inançla ilişkili |
| **Chunkey** | Mississippian | Yüksek bahisli ve bazı bağlamlarda törensel; ayrıca mızrak atmayı gerektirir |

**Dehontsigwa'ehs bu taramanın en açık örneğidir:** kaynak mükemmel
(Vennum 1994), kurallar tam, oyun harika — ve kitap onu **basmıyor.**
Bir oyun kitabının verebileceği en güçlü kültürel sinyal budur.

### 6.2 Üç `excluded` kayıt — üç ayrı gerekçe

| Oyun | Gerekçe | Tip |
|---|---|---|
| **Kalah** | 20. yy ortası **ticari icat**; "Afrika oyunu" diye basılamaz | özgünlük |
| **Kubb** | "Viking" iddiasının **hiçbir dayanağı yok**; 1990'lar Gotland | uydurulmuş gelenek |
| **Buzkashi** | Oyun nesnesi bir hayvan gövdesi; **güvenli uyarlama oyunu yok eder** | güvenlik + hayvan refahı |

Üçü de kitapta bir madde olarak değil, arka maddedeki *"uydurulmuş
gelenekler"* kutusunda yer alacak. Aynı kutuda "Chinese Checkers"ın 1892
Almanya icadı olduğu ve seksekin "Roma askerleri" hikâyesinin kaynaksız
olduğu da yazacak.

### 6.3 Güvenlik ve uyarlama

İki maddede güvenlik, kural metnini **değiştirdi** ve bu değişiklik kayıtta
gerekçesiyle duruyor:

- **Olinda Keliya** — oyunun adını veren tohum (*Abrus precatorius*)
  zehirlidir. Kitap özgün malzemeyi **anlatır**, oynamak için boncuk şart
  koşar.
- **Gilli-danda** — sivri uçlu kısa çubuk havaya fırlar; göz yaralanması
  riski gerçektir. Kitap özgün oyunun anlatısını ve **ayrı bir güvenli
  uyarlamayı** basar, uyarlamanın özgün oyun **olmadığını** söyler.

Bahis mekaniği taşıyan **17 oyun** `gamblingReframed: true` işaretli
(karar K5): kitap bahsi tarih olarak anlatır, mekaniği puanla yeniden yazar
ve bunu **açıkça söyler**.

---

## 7 · Şema

`01_SOURCE/game.schema.json` Faz 1'de genişletildi. Eklenen bloklar:

| Alan | Ne için |
|---|---|
| `taxonomyRationale` | Tasnif gerekçesi kayıtta durur, kafada değil |
| `ruleCompleteness` | Beş öğe + verdict + **ne bilinmiyor** |
| `clarity` | Taze okur testi · beş soru + döngü riski + bitiş kuralı |
| `playabilityStatus` | Beş durumlu oynanabilirlik kapısı |
| `reconstructionPlan` | **Faz 1'de eklendi** — beyansız kurguyu imkânsız kılar |
| `sourceVerification` | `bibliographic` ↔ `page-verified` ayrımı |
| `sources[].lineage` | Bağımsızlık sayımının girdisi |
| `scores` | Sekiz ölçütlü seçim modeli |
| `visualNeeds` | Görsel sisteminin girdisi |
| `substitutionHint` · `safetyNotes` · `supervision` · `environment` | Güvenli modern malzeme karşılığı |
| `unresolvedQuestions` | Cevabı olmayan sorular **açıkça** durur |

**Şema pilotu.** Altı oyun tam kural bloğuyla yazıldı ve şema sınandı:

| Oyun | Aile | Kültür | Neyi test etti |
|---|---|---|---|
| Oware | ekim | Akan | tahta/nesne oyunu, çoklu alma zinciri |
| Fox and Geese | av-kuşatma | İngiliz | **çocuk-dostu** + asimetrik hedefler |
| Yut Nori | yarış | Kore | **grup oyunu** (2–8 kişi), ekstra atış |
| Nine Men's Morris | çizgi-toprak | Ortaçağ Avrupası | **basit oyun**, üç aşamalı yapı |
| Fanorona | savaş tahtası | Malgaş | **strateji oyunu**, iki yönlü alma, zorunlu alma |
| Tablut | av-kuşatma | Sámi | **yeniden kurgulanmış** kural seti |

**Şema iki kez kırıldı ve iki kez düzeltildi:**

1. `gameId` kalıbı en az üç karakter istiyordu — **"go" iki harftir.**
   Şema doğrulayıcı bunu yakaladı; alt sınır ikiye indirildi.
2. `reconstructed` etiketi tek başına yetersizdi (§ 4.4) → `reconstructionPlan`.

Pilot ayrıca **sekiz aşırı uzun kural adımı** buldu: `qa_rules.py`
STYLE.md'nin 22 kelimelik cümle azamisini kural adımlarına uyguluyor ve
Oware'in 32 kelimelik, Fanorona'nın 26 kelimelik adımlarını reddetti.
Adımlar tek eyleme bölündü. **Pilotun varlık sebebi tam olarak budur.**

---

## 8 · Test altyapısı

### 8.1 Kapılar

| Betik | Ne denetler | Denetim |
|---|---|---:|
| `build_index.py --check` | Üretilen envanter bayat mı | 1 |
| `validate_spec.py` | **JSON Schema uyumu** · kimlik · kapsam · kapı | 26 |
| `validate_structure.py` | Dosya · gömülü değer · sızıntı · sır · bağ | 62 |
| `qa_taxonomy.py` | Aile tanımı · sınır · kısıt taraması · denge | 20 |
| `qa_rules.py` | **Kural bütünlüğü · netlik · durum tutarlılığı** | 20 |
| `validate_research.py` | Künye · yasaklı kaynak · bağımsızlık · yazım kilidi | 7 |
| `score_candidates.py` | Seçim modeli · uygunluk · kültür kapısı | — |
| `page_budget.py` | Sayfa modeli · hedef bandı · KDP sınırları | — |
| `editions.py` | Telif · başabaş ACOS · KU kontrolü | — |
| `update_docs.py --check` | Üretilen belgeler bayat mı | 2 |

**JSON Schema doğrulayıcı elle yazıldı.** Karar K7 üçüncü taraf paket
yasaklar; şemanın kullanılan alt kümesi `validate_spec.py` içinde uygulandı.
Desteklenmeyen bir şema anahtarının **sessizce yok sayılması** riski ayrı
bir denetimle kapatıldı: şema taranır ve bilinmeyen bir anahtar bulunursa
kapı kırmızı yanar.

### 8.2 Kapıların kendi testi — 83 denetim

`05_TESTS/selftest.py` beş bölüm koşar. Beşinci bölüm Faz 1'de eklendi ve
**yeni sekiz kapının her birini kusurlu bir kurguyla sınar.**

Bu kritiktir çünkü Faz 1 verisinde çoğu kapı **boş koşar**: kilitli oyun
yok, oynanabilirlik testi yok, manuscript yok. Gerçek veriyle asla
ısırmayan bir kapının körlüğü yalnızca burada kapanır.

Kanıtlanan ısırıklar arasında:

- **kurgusal tamamlama** — `unknown` öğe + `complete` verdict → yakalanır
- **beyansız yeniden kurgulama** — plan yok → yakalanır
- **yersiz kurgulama planı** — ölü kural → yakalanır
- **aynı yazarın iki eseri** bağımsız sayılmaz → yakalanır
- **türetilmiş kaynak** (`lineage`) bağımsız sayılmaz → yakalanır
- **sayfa doğrulamasız `locked`** → yakalanır
- **kısıtlı oyunun kilitlenmesi** → yakalanır
- **geçersiz oynanabilirlik testi** (`usedOnlyBookText: false`) → yakalanır
- **kitaba sızan `restricted`** (editoryal durum reddetmiyor) → yakalanır
- **bayat üretilen envanter ve belge** → yakalanır

Ayrıca **negatif test**: envanter değiştiğinde üretilen belgenin bayat
sayıldığı ayrıca kanıtlanır — yoksa `--check` hiçbir şeyi korumuyor olurdu.

### 8.3 CI — YEŞİL

`.github/workflows/validate.yml` altı iş koşar: `gate` · `data` ·
`structure` · `gates-selftest` · `text` · `production-model`.
`text` işi bu fazda **boş koşar** (manuscript depoda yok) ve körlüğü
`gates-selftest` kapatır.

**Faz 1'de kapatılan bir CI körlüğü.** Sekiz yeni kapıdan dördü
`qa_all.sh` içinde koşuyordu ama CI'da **koşmuyordu** — yani yerelde
ısıran bir kapı uzaktan sessiz kalıyordu. Bu, Codex dersi D5'in
(*"bir kapının varlığı, koştuğu anlamına gelmez"*) aynısıdır ve
`validate.yml` dört adımla genişletildi: `build_index --check` ·
`qa_taxonomy` · `score_candidates` · `update_docs --check`.

Sonuç: **7/7 iş yeşil.**

---

## 9 · Üretim modeli

### 9.1 Sayfa bütçesi

| | |
|---|---:|
| Gövde (100 × 2) | 200 |
| Aile açılışları (7 × 2) | 14 |
| Ön madde | 14 |
| Arka madde | 21 |
| **Model** | **250** |
| Hedef | 256 ± %6 |
| **Sapma** | **−%2,3** ✅ |

**Çapraz denetim:** 100 oyun × 650 kelime = 65.000 kelime; 320
kelime/sayfa varsayımıyla gövde ≈ 203 sayfa. Model 200 diyor. Fark **%2** —
iki bağımsız tahmin aynı kitabı tarif ediyor.

> ⚠ **MODEL KALİBRE EDİLMEDİ.** 320 kelime/sayfa bir varsayımdır ve
> diyagram alanını hesaba katmaz. Gerçek ölçüm Faz 2'nin işidir.

### 9.2 Telif (250 sayfa modelinde)

| Sürüm | Liste | Baskı | Telif | Başabaş ACOS |
|---|---:|---:|---:|---:|
| Ciltli | 34,99 $ | 9,90 $ | **11,09 $** | %31,7 |
| Ciltsiz | 22,99 $ | 5,25 $ | **8,54 $** | %37,2 |
| Kindle | 11,99 $ | 1,20 $ | **7,19 $** | %60,0 |

250 sayfa modeli, 256 sayfalık hipoteze göre birim telifi ciltlide
**0,10 $ artırıyor**. KU kontrolü (K6) hâlâ geçerli: tam okuma ≈ 1,20 $,
ciltsiz telif 8,54 $ — **7,1 kat** kayıp.

### 9.3 Görsel sistem

Yedi görsel tipi tanımlandı. Yayımlanabilir 151 kaydın **149'u en az bir
görsel istiyor** — tahtasız oyunlar bile hareket diyagramı ya da kültürel
levha istiyor. Üretim hedefi ≈ 130 görsel (Faz 5).

**Faz 1'de tek bir üretim görseli üretilmedi.** `IMAGE_PROMPT_LIBRARY.html`
Faz 5 teslimatıdır; Faz 1 yalnızca *ne gerektiğini* ölçtü.
Diyagram notasyonu Faz 2'de dondurulur.

---

## 10 · Riskler

| Risk | Durum | Azaltma |
|---|---|---|
| 45 kültür bulunamaz | ✅ **kapandı** — 89 bulundu | — |
| Aile sınırları temiz çizilemez | ✅ **kapandı** — deterministik yordam | — |
| Bir aile zayıf çıkar | ⚠ **gerçekleşti** — av-kuşatma | § 5 · kurucu kararı |
| Kural kaynakları çelişiyor | ⚠ 10 oyunda | `reconstructionPlan` + prozada etiket |
| Künyeler sayfa seviyesinde doğrulanmadı | ⚠ **160/160** | `page-verified` Faz 2 `locked` kapısı |
| 38 oyun tek kaynaklı | ⚠ açık | `locked` olamazlar; havuzda 119 uygun aday var |
| Sayfa modeli kalibre değil | ⚠ açık | Faz 2 gerçek dizgi |
| Oyun testçisi bulunamıyor | ⛔ **Faz 2 bloklayıcısı** | A7 · sahte test kaydı üretilmez |
| Kart oyunları malzeme istiyor | ⚠ açık | Ganjifa/Mahjong destesi evde yok; ya uyarlama ya eleme |

---

## 11 · Kurucudan bekleyen kararlar

| # | Soru | Aciliyet | Bu fazın katkısı |
|---|---|---|---|
| **A1** | Manuscript public depoda mı duracak? | **YÜKSEK** | **K9 kararıyla mekanizmaya bağlandı** (§ aşağıda) |
| **A2** | 7 aile taksonomisi onayı | **YÜKSEK** | Taksonomi yazıldı; **yeniden dengeleme önerisi** § 5'te |
| **A3** | 100 oyunun nihai listesi | **YÜKSEK** | 96 oyunluk **öneri** üretildi + 23 yedek |
| A5 | Kalibre edilmiş STYLE onayı | ORTA | Faz 2 |
| A6 | Yazar biyografisi | ORTA | Faz 5 |
| **A7** | **Oyun testçileri kim** | **YÜKSEK** | **Faz 2 sert bloklayıcısı** — ajan test yapamaz |

**A1 · bu fazda alınan işleyiş kararı (K9).** Faz 1, veri ile proza
arasındaki sınırı **mekanik** hâle getirdi:

- **Veri katmanı** (public): alanlara bölünmüş kayıt — `01_SOURCE/`
- **Proza katmanı** (özel): sekiz sabit blokta sürekli metin — `02_MANUSCRIPT/`

Sınırı `validate_structure.py → check_manuscript_leak()` çizer: proza
şablonunun etiketlerini taşıyan takip edilen bir dosya CI'ı kırmızı yakar.
Bu, A1'i **karara değil mekanizmaya** bağlar. Kurucu onayı hâlâ gereklidir.

---

## 12 · Faz 1 Definition of Done

- [x] `game_index.json` ≥140 aday içeriyor ve şemayı geçiyor — **153**
- [x] Her adayın ailesi, kültürü, bölgesi, dönemi, ≥1 kaynağı var
- [x] 7 ailenin tanımı ve **sınır kuralı** yazılı
- [x] Kısıt taraması **160/160** tamamlandı, muafiyetsiz
- [x] `PLAYABILITY_STANDARD.md` yürürlükte ve mekanizmaya bağlı
- [x] Sayfa modeli üretildi → `06_REPORTS/page-budget.json`
- [x] `selftest.py` yeşil — **83 denetim**, her kapı en az bir kusurlu kurguda ısırıyor
- [x] `06_REPORTS/PHASE_1_REPORT.md` yazıldı
- [x] CI **YEŞİL** — 7/7 iş
- [x] `.gate` → `phase1`

### PASS ölçütleri

| Ölçüt | Hedef | Ölçülen | |
|---|---|---|---|
| Aday sayısı | ≥140 | **153** | ✅ |
| Farklı kültür | ≥45 | **89** | ✅ |
| Aile başına aday | ≥16 | **20–24** | ✅ 7/7 |
| Kısıt taraması | tam · gerekçeli | **160/160** | ✅ |
| Sayfa modeli | ±%6 | **−%2,3** | ✅ |
| `selftest.py` | 0 hata | **0** | ✅ |

**Faz 1 PASS.**

---

## 13 · Faz 2 hazırlığı

Faz 2, Faz 1'in kilitlediği envanterden **12 pilot oyun** seçer — her
aileden en az bir tane ve **en zor olanlardan**.

**Faz 1'in Faz 2'ye devrettiği hazır malzeme:**

- 119 uygun aday · 23 yedek
- 6 tam kural bloğu (şema pilotu) — Faz 2 pilotunun çekirdeği olabilir
- 10 `reconstructed` oyun, beyanlı planlarıyla — pilotun "≥2 reconstructed"
  şartını fazlasıyla karşılıyor
- `boardless` ailesinden tahtasız adaylar — "≥1 tahtasız" şartı hazır
- Yut Nori (2–8 kişi) — "≥1 beş oyunculu" şartı hazır
- Fox and Geese, Tablut, Bagh-Chal — "≥1 asimetrik" şartı hazır

**Faz 2'ye girmeden kapanması gerekenler:**

1. **A7 — oyun testçileri.** Bu sert bir bloktur. Ajan oynanabilirlik testi
   yapamaz; testçi insandır ve yalnızca kitaptaki metni okur. Testçi
   bulunamazsa Faz 2 **bloklanır** ve bu kabul edilen bir bloktur:
   **sahte test kaydı üretilmez.**
2. **A2 — aile taksonomisi** ve § 5'teki yeniden dengeleme kararı.
3. **A3 — 100 oyunun listesi.** Öneri hazır; karar kurucunun.

**Faz 2'nin ilk üç işi:**

1. Pilot 12 oyunun künyelerini `page-verified` seviyesine çıkarmak
2. `DIAGRAM_LANGUAGE.md` — notasyonu dondurmak
3. Gerçek dizgiyle sayfa/oyun ölçümü — 250 sayfalık modelin ilk sınavı

---

## 14 · Bu fazın kendi hakkında bilmediği

Dürüstlük gereği:

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| Künyelerin sayfa seviyesinde doğru olup olmadığı | Faz 2 · `page-verified` |
| 650 kelimenin bir oyuna yetip yetmediği | Faz 2 · gerçek yazım |
| Sayfa/oyun oranının 2,0'da kalıp kalmadığı | Faz 2 · gerçek dizgi |
| Kural şablonunun Şogi/Mahjong'da kırılıp kırılmadığı | Faz 2 · pilot en zorları seçer |
| Yeniden kurgulanan oyunların masada çalışıp çalışmadığı | Faz 2 · insan testçi |
| Puanlama modelinin iyi kitap üretip üretmediği | Yayından sonra |

---

**⛔ FAZ 2 BAŞLAMADI. Kurucu onayı bekleniyor.**
