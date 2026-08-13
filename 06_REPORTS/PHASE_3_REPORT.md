# FAZ 3 RAPORU — Üretim, erişilebilir kaynakla ölçek ve sayfa modelinin düzeltilmesi

> **The Great Book of World Games** · Faz 3 · Dal: `faz/3-blok-1`
>
> Bu faz iki şey yaptı: **sekiz oyun yazdı** ve **Faz 2'nin en önemli
> sayısının yanlış olduğunu kanıtladı.**
>
> İkincisi birincisinden daha değerlidir.

---

## 0 · Tek bakışta

| | Faz 2 | **Faz 3** | |
|---|---:|---:|---|
| Yazılmış oyun | 3 | **11** | +8 |
| Doğrulanmış künye | 9 | **17** | +8 |
| Dizgi örneklemi | 3 oyun | **11 oyun** | |
| Ölçülen kelime/sayfa | 389 | **405** | |
| Ölçülen sayfa/oyun | 1,82 | **1,52** | |
| Çift sayfa taşma oranı | %33 | **%9** | |
| **Kitap sayfa modeli** | **316** | **268** | **−48** |
| **Hedeften sapma** | +%23,4 ⛔ | **+%4,7 ✅** | **BANDA GİRDİ** |
| Ciltsiz birim telif | 7,42 $ | **8,24 $** | +0,82 $ |
| Diyagram (render) | 8 | **16** | hepsi ≤150 mm |
| Selftest denetimi | 117 | **126** | |
| CI | yeşil | **yeşil** | |
| **Dış insan testi** | **0** | **0** | ⛔ değişmedi |
| **`.gate`** | `phase1` | **`phase1`** | yükseltilmedi |

---

## 1 · Faz 3 kapsamı

Faz 3, yol haritasının ilk büyük **üretim** fazıdır. Amacı ham oyun sayısı
değil, tek bir sorunun cevabıdır:

> **Üretim sistemi, Faz 2'de bulunan kusurları çoğaltmadan çok sayıda
> yüksek kaliteli madde yazabiliyor mu?**

Cevap: **evet, ama üretim hızını kaynak erişimi belirliyor.**

---

## 2 · Kurucu istisnası — koşullu üretim şeridi (K18)

Faz 2'nin resmî kapısı kapanmadı ve **kapanmamış olarak kaldı**. Kurucu
buna rağmen üretim işini yetkilendirdi. İki durum bilerek ayrı tutulur:

| | Durum |
|---|---|
| **Faz 3 üretim işi** | ✅ **YETKİLİ ve YAPILDI** |
| **Resmî faz kapısı** | ⛔ **AÇILMADI — `.gate` = `phase1`** |
| **`locked` oyun** | **0** — uydurulmadı |

`.gate` yükseltilmedi çünkü `phase2` kapısı 12 `locked` oyun ister ve
**sıfır oyun kilitlenebildi**. Kapı seviyesi, kitabın ne kadar hazır
olduğunu söyleyen tek makine okunur sayıdır; onu ilerlemiş göstermek bu
projede yapılabilecek en pahalı yalandır.

Bu koşul `PROJECT_CONTEXT.md`, `ROADMAP_PROGRESS.md` ve bu raporda
**açıkça** yazılıdır ve gizlenmemiştir.

---

## 3 · Yazılan sekiz oyun

Hepsi **doğrudan İngilizce** yazıldı ve hepsi **birinci elden** kaynağa
dayanıyor.

| Oyun | Aile | Kültür | Kaynak | Çeşitlilik rolü |
|---|---|---|---|---|
| **Pong Hau K'i** | çizgi-toprak | Kantonlu | Culin 1895, ss. 100–101 | kitabın **en basit** oyunu |
| **Gonggi** | tahtasız | Kore | Culin 1895, ss. 58–59 | **tahtasız**, beceri, 1–6 kişi |
| **Olinda Keliya** | ekim | Sinhala | Parker 1909, ss. 588–595 | ekim + **güvenlik ikamesi** |
| **Nerenchi** | çizgi-toprak | Sinhala | Parker 1909, ss. 577–580 | iki aşamalı değirmen |
| **Demala Diviyan Keliya** | av-kuşatma | Sinhala | Parker 1909, ss. 581–582 | **ASİMETRİK** — 2'ye 24 |
| **Awithlaknannai** | savaş tahtası | Zuni | Culin 1907, s. 801 | **diyagram-ağır**, 19 nokta |
| **Picaria** | çizgi-toprak | Tewa Pueblo | Culin 1907, s. 797 | basit, 9 nokta |
| **Zohn Ahl** | eve dönüş | Kiowa | Culin 1907, ss. 124–125 | **çok oyunculu**, K5 puanlama |

Altı aile temsil edildi. Manuscript **3 → 11 oyuna** çıktı.

### 3.1 Neden on değil sekiz

Yol haritası ilk on oyunu zorunlu kalibrasyon örneklemi sayıyor. Sekiz
yazıldı; **ikisi gerekçesiyle ertelendi** (§ 4). Sebep bir üretim
yavaşlığı değil bir **kaynak dürüstlüğü** kararıdır: bir oyunu yazmak
için elimde onun kuralını veren açık bir kaynak olması gerekiyordu ve
iki oyunda yoktu.

Örneklem yine de Faz 2'nin üç oyununun **neredeyse dört katıdır** ve
kalibrasyonu belirleyici biçimde değiştirdi (§ 7).

---

## 4 · Ertelenen oyunlar

| Oyun | Neden ertelendi |
|---|---|
| **Totolospi** | Erişilebilir kaynak (Culin 1907, s. 795) oyunu bir **atlamalı dama** olarak anlatıyor; envanter kaydı ise `race` ailesinde. Faz 1 zaten *"aynı ad hem yarış hem alquerque tipi bir oyun için kullanılır"* uyarısını koymuştu ve sayfa doğrulaması bunu **doğruladı**. Kaydın ailesiyle kaynağın anlattığı oyun aynı değil; ikisi çözülmeden yazılamaz. |
| **Oware** | Culin'in *Mancala* (1896) monografisi oyunu yalnızca **bir cümlede** anıyor ve kural vermiyor. Faz 1 kural bloğu var ama kaynağı sayfa seviyesinde açılmadı. |

**İkisi de silinmedi.** Kapsam 100'de duruyor; ikisi de üretim kuyruğunda
kendi öncelik seviyesinde bekliyor.

---

## 5 · Kaynak durumu

| Durum | Oyun |
|---|---:|
| `verified` — ≥2 doğrulanmış künye | **3** |
| `partially-verified` — 1 doğrulanmış künye | **11** |
| `access-blocked` — denendi, erişilemedi | **4** |
| `not-attempted` — henüz sıraya gelmedi | **82** |

### 5.1 "Erişilemedi" ile "denenmedi" ayrı sayılır

Bu ayrım Faz 3'te **bilerek** yapıldı ve bir düzeltmedir. Kuyruğun ilk
sürümü ikisini birleştiriyor ve **80 oyunu "kaynak erişimi bekliyor"**
gösteriyordu. Bu sayı bir engeli olduğundan büyük gösterir.

Gerçek rakam: **denenip erişilemeyen oyun sayısı dörttür.** Geri kalan
82 oyun engelli değil, **henüz sıraya gelmemiştir**.

> Bir engeli abartmak, onu küçümsemek kadar yanlıştır. İkisi de aynı
> şeyi yapar: kararı yanlış veriye dayandırır.

### 5.2 Faz 3'ün kaynak bulgusu — erişilebilir ≠ güvenilir (K20)

Faz 2'nin bulgusu şuydu: *iyi kaynaklar teliflidir.* Faz 3 bunun
devamını buldu:

> **Kamusal alandaki kaynak eski demektir; eski, yeniden kurgulamalarda
> geçersiz demektir.**

Falkener'ın *Games Ancient and Oriental*'ı (1892) Murray'den öncedir ve
bir **derlemedir**, bir saha kaydı değil. Sayfa doğrulaması bunu iki
yerde somut gösterdi:

- **Pachisi** bölümü (s. 258) Akbar'ın "canlı taşlarla oynanan dev tahta"
  anlatısını ikincil bir dergiden aktarır ve Falkener'ın kendisi
  *"I applied at the India Office, but could get no information"* yazar.
  Faz 1 kaydı bu anlatı için tam da bu uyarıyı koymuştu — **doğrulandı**.
- **Chinese Chess** bölümü kural açıklaması değil **oyun kayıtlarıdır**
  (hamle notasyonu), ve OCR'da okunamaz durumdadır.

**Sonuç:** Faz 3 kaynakları türüne göre sıraladı ve **yalnızca birinci
elden** kayıtlardan yazdı — Culin'in müze envanterli Kore saha çalışması,
Culin'in BAE saha çalışması, Parker'ın Seylan saha çalışması. Falkener
hiçbir maddenin **tek** dayanağı olmadı.

Bu, `chaturanga` ve `senet` gibi yeniden kurgulanmış oyunların neden bu
batch'te yazılmadığını da açıklar: onların erişilebilir tek kaynağı bir
Viktorya yeniden kurgulamasıdır ve **eski bir kurgu, yeni bir kurgu kadar
kesin görünür**. Okur ikisini ayırt edemez.

---

## 6 · İç simülasyon ve dış insan kanıtı

Kurucu, gereksiz iç simülasyonun atlanmasını yetkilendirdi (Karar B).
Bu batch'te **iç simülasyon kullanılmadı**: sekiz oyunun sekizi de
kaynağın kendi kural metninden doğrudan izlenebiliyordu ve simülasyon
yeni bilgi üretmeyecekti.

| Kanıt türü | Sayı |
|---|---:|
| `internal` — ajan / doğrulayıcı | 0 |
| **`external` — gerçek insan** | **0** |

`01_SOURCE/playtests/` **hâlâ boştur.**

> **Sahte kayıt üretilmedi ve iç doğrulama dış kanıt diye sunulmadı.**

Her oyun `EXTERNAL PLAYTEST PENDING` durumundadır. Bu, sekiz maddenin
`draft` seviyesinde kalmasının ve hiçbirinin `locked` olamamasının
sebebidir.

---

## 7 · SAYFA MODELİ — Faz 2'nin sayısı yanlıştı

Bu, Faz 3'ün en önemli çıktısıdır.

| | Faz 2 (3 oyun) | **Faz 3 (11 oyun)** |
|---|---:|---:|
| Kelime / sayfa | 389 | **405** |
| Kelime / oyun | 708 | **616** |
| Metin sayfa/oyun | 1,37 | **1,18** |
| Diyagram sayfa/oyun | 0,45 | **0,34** |
| Ölçülen sayfa/oyun | 1,82 | **1,52** |
| Faturalanan sayfa/oyun | 2,67 | **2,18** |
| **Taşma oranı** | **1/3 = %33** | **1/11 = %9** |
| **Toplam** | **316** | **268** |
| **Sapma** | **+%23,4** ⛔ | **+%4,7** ✅ |

### 7.1 Sebep: bir örneklem hatası

Faz 2'nin 316 sayfalık projeksiyonu **tek bir aykırı değerin** eseriydi.
Üç oyunluk örneklemde `tablut` çift sayfayı aşıyordu ve taşma oranı
**%33 sanıldı**. On bir oyunda gerçek oran **%9** çıktı — taşan hâlâ
yalnızca `tablut`.

Sayfa sayısını belirleyen tek değişken taşma oranıdır ve üç oyun onu
belirleyemez. Faz 2 raporu bunu zaten söylemişti:

> *"Örneklem ÜÇ oyundur ve taşma oranını (1/3) tek başına belirleyemez."*

Faz 3 o uyarıyı **doğruladı** ve sayıyı düzeltti.

### 7.2 Faz 2'nin ikinci iddiası da zayıfladı

Faz 2 şunu yazmıştı: *"Metin oyundan oyuna neredeyse sabittir — fark
0,01 sayfa."* On bir oyunda **metin farkı 0,41 sayfaya çıktı**
(500–764 kelime).

Diyagram farkı (0,62) hâlâ metin farkından büyük, yani **"sayfa bütçesi
bir diyagram bütçesidir" sonucu yönü itibarıyla doğru** — ama Faz 2'nin
ifade ettiği kadar **mutlak değil**.

> Üç oyun bir eğilimi gösterir, bir sabiti kanıtlamaz.
> Bu cümle kendi raporumuz için de geçerliydi.

### 7.3 Sapma şerhi KAPANDI

Faz 2, +%23,4 sapma için § 15 şerhi yazmış ve üç seçenek önermişti.
**Hiçbiri uygulanmadı ve uygulanmasına gerek kalmadı:** sapmanın sebebi
bir tasarım sorunu değil bir ölçüm sorunuydu.

- Kelime hedefi **650'de kaldı** — Faz 2'nin önerisi buydu ve doğruydu.
- Kapsam **100'de kaldı**.
- Diyagram bütçesi **150 mm olarak yürürlükte** — sapma çözülse de bütçe
  kalır, çünkü taşan tek madde hâlâ **diyagram yüzünden** taşıyor.

Şerh silinmedi; `resolvedDeviation` olarak kayda geçti.

### 7.4 Ekonomik sonuç

| Sürüm | 316 sayfa (yanlış) | **268 sayfa (ölçülen)** |
|---|---:|---:|
| Ciltli telif | 9,97 $ | **10,43 $** |
| **Ciltsiz telif** | **7,42 $** | **8,24 $** |
| Başabaş ACOS (ciltli) | %28,5 | **%29,8** |

Yanlış projeksiyona göre karar verilseydi, kitap gereksiz yere
kapsam ya da kelime kısıtlamasına gidecekti.

---

## 8 · 150 mm diyagram bütçesi (K19)

Kurucu Karar A onaylandı ve **bağlayıcı** hâle geldi.

### 8.1 Ölçüm render edilmiş çıktıdandır

`qa_diagram.py § ⑨` tanımlayıcıya değil **çizilmiş dosyaya** bakar.
Gerekçe: bir tanımlayıcı *"9×9 tahta"* der ve bu bir **boyut vermez** —
boyutu adım aralığı, efsane satır sayısı, panel dizilimi ve altyazı
belirler.

> **Render edilmemiş bir diyagram denetlenmemiştir ve geçemez.**

### 8.2 Cat's Cradle — bütçe değil DİYAGRAM düzeltildi

Faz 2'nin 182,5 mm'lik üç panelli ip figürü yeni bütçeyi 32,5 mm aşıyordu.

| | v1.1 | **v1.2** |
|---|---:|---:|
| Genişlik | 70 mm | 70 mm |
| **Yükseklik** | **182,5 mm** ⛔ | **111,5 mm** ✅ |

İki israf bulundu: **her panel kendi efsanesini basıyordu** (aynı efsane
üç kez, 27 mm) ve **gövdenin yarısı boş kenar payıydı** (ip figürü
±10 mm'lik bir alanda yaşıyor, 46 mm ayrılmıştı).

**Çizgi kalınlığı (0,75 pt) ve glif boyu (7 pt) değişmedi.** Giden şey
tekrar ve boşluktur — yani bu bir **sadeleştirmedir**, § 10'un yasakladığı
"okunmaz hâle gelene kadar küçültme" değildir.

### 8.3 On altı diyagramın ölçümü

| | |
|---|---:|
| Render edilen diyagram | **16** |
| En küçük | 36,1 mm (`olinda-setup`) |
| En büyük | 111,5 mm (`gonggi-toss`, `catscradle-cradle`) |
| Ortalama | **72,9 mm** |
| **150 mm'yi aşan** | **0** |

---

## 9 · Diyagram dili v1.3 — düzensiz tahtalar

Faz 3'ün ilk gerçek batch'i dili **kırdı**.

Beş yeni tahta ızgara **değildir**: pong-hau-ki (5 nokta), picaria
(9 nokta), nerenchi (üç iç içe kare, 24 nokta), diviyan-keliya (kare +
köşegen + dört üçgen, 13 nokta), awithlaknannai (19 noktalı uzun zincir).
Izgara varsayan bir çizici bunların **hiçbirini** doğru çizemez.

Yaklaşık bir ızgarayla idare etmek reddedildi. Gerekçe kitabın ölüm
biçimidir: **okur kuralı okur, tahtaya bakar, ikisi uyuşmaz ve oyun
çalışmaz.**

**Çözüm:** `point` sınıfı artık açık **düğüm ve kenar** listesi taşıyor
(`nodes` + `edges`, 0–1 normalize). Sınır denetimi **sıkılaştı**: bir taş
yalnızca **tanımlı bir düğümde** durabilir, ve kopuk kenar (tanımsız
düğüme bağlanan) ayrı bir denetimle yakalanır. Render deterministik kalır.

### 9.1 Bir diyagramda kabul edilen sınır

`pong-hau-ki-setup` altyazısında şu yazar: Culin'in metni kapalı kenarı
**adlandırır** ama dijital nüshadaki şekil, tek tek kenarları okunacak
çözünürlükte değildir. Tahta **prozadan** çizildi ve bu sınır
altyazıda ve doğrulama kaydında **açıkça** duruyor.

---

## 10 · İngilizce editoryal durum

Sekiz madde de **doğrudan İngilizce** yazıldı. Türkçe hiçbir aşamada ara
dil olarak kullanılmadı.

Her madde yedi başlıkta bağımsız doğrulama kaydı taşır: kaynak · kural ·
oynanabilirlik · netlik · terminoloji · kültürel sadakat · diyagram.

**Tekrar eden AI kalıbından kaçınıldı:** sekiz kültürel hikâyenin hiçbiri
aynı kalıpla açılmıyor. Biri bir müze envanter numarasıyla, biri bir
atasözüyle, biri bir tohumun zehriyle, biri Culin'in çeviremediği bir
kelimeyle başlıyor.

**Terminoloji kararları kayda geçti.** Örnek: `demala-diviyan-keliya`
maddesinde 'cattle' ve 'leopards' korundu, 'tiger/goat' **kullanılmadı** —
çünkü o, Güney Asya'nın başka bir oyun kümesinin (Bagh-Chal) dilidir ve
kitap ikisini karıştırmaz.

---

## 11 · Türkçe test malzemesinin yalıtımı

| | |
|---|---|
| Ticari katmanda Türkçe | **0** |
| Türkçe pilot işareti ticari katmanda | **0** |
| Çeviri beyanı taşıyan ticari kayıt | **0** |
| `qa_language_split.py` | ✅ 13 denetim yeşil |

Türkçe pilot paketi Faz 2'den beri `01_SOURCE/pilot_tr/` içinde,
`.gitignore` ile korumalı ve `TEST-ONLY / TURKISH PILOT` işaretli.
Faz 3'te **hiç Türkçe ticari içerik üretilmedi**.

---

## 12 · Kültürel bulgular — atıf düzeltmeleri

Sayfa doğrulaması iki maddede kültürel atfı **değiştirdi**.

### 12.1 Awithlaknannai ve Picaria

Culin, Zuni oyununu **"EUROPEAN GAMES: ZUNI"** başlığı altında verir.
Picaria için kaynağın kendisi (Dozier) *"Pueblo kökenli olduğu söylenir
ama şüphesiz İspanyol girişidir"* der.

**Kitap bunu gizlemedi.** İki maddenin kültürel hikâyesi de İspanyol
bağını ve yerli dönüşümü **birlikte** anlatıyor.

> "Kadim yerli oyunu" çerçevesi hem yanlış olurdu hem de asıl ilginç
> olanı — uyarlamanın kendisini — silerdi.

### 12.2 Zohn Ahl bir kadın oyunudur

Culin, oyunun *"çift sayıda kız ya da kadın tarafından oynandığını,
erkeklerin ve oğlanların ASLA oynamadığını"* özellikle kaydeder. Bu,
prozada bir dipnot değil kültürel hikâyenin **merkezinde** duruyor.

### 12.3 Aktarılmayan iddialar

- **Kurna Tapınağı, MÖ 1400.** Parker bunu anıyor; Faz 1 kaydı
  tartışmalı olduğunu işaretlemişti. Kitap yalnızca Mihintale'nin kendi
  yazıtlarına dayanan tarihi bastı.
- **Culin'in "erkek çocuklar oynar" notu** (gonggi). 1895'in bir anlık
  gözlemi bir kural değildir ve kural gibi basılmadı.

---

## 13 · Aile ve kültür dengesi

| Aile | Hedef | Kilitli |
|---|---:|---:|
| Ekim · Av-kuşatma · Yarış | 14 · 10 · 15 | ✅ aynı |
| Çizgi-toprak · Savaş tahtası | 14 · 17 | ✅ aynı |
| Şans · Tahtasız | 15 · 15 | ✅ aynı |
| **Toplam** | **100** | **100** ✅ |

71 kültür · 29 bölge · oyuncu dağılımı: 68 iki kişilik · 8 üç-dört ·
24 beş+ kişilik.

### 13.1 Tahtasız ailenin çerçeve kusuru — DÜZELTİLDİ

Faz 2 bir editoryal zayıflık işaret etmişti: tahtasız ailenin 15 oyunundan
**5'i "English"**, ve aile **11 kültürle** yedinin en düşüğü.

Faz 3 § 25 uyarınca ailenin **açılış iddiasına** baktı ve bir çelişki
buldu:

> v1 açılış açısı: *"Malzemesi olmayan oyun, **en çok kültüre yayılmış**
> oyundur."*

Kitabın **en geniş yayılım iddiasını** taşıyan aile, **en dar kültür
kümesine** sahipti. Bir açılış denemesi, altındaki maddelerin
kanıtlamadığı bir iddiada bulunamaz — okur listeye bakar ve iddiayı
yalanlar.

**Düzeltme (çerçeve):** iddia *yayılma*dan **tekrar bulunuş**a çevrildi —
aynı malzemesizliğin birbirinden habersiz yerlerde tekrar keşfedilmesi.
Bu, eldeki maddelerle desteklenir.

**Öneri (kapsam · karar kurucunun):** yedek havuzda 19 uygun oyun var.
Tahtasız ailedeki beş İngiliz maddesinden ikisinin yerine temsil
edilmeyen kültürlerden iki oyun koymak kültür sayısını **11'den 13'e**
çıkarır. Bu bir **scope amendment** gerektirir ve ajan tarafından
yapılamaz. Kapsam **değiştirilmedi**.

---

## 14 · Malzeme ve güvenlik

**Olinda Keliya** güvenlik ayrımını Faz 3'te bir adım ileri taşıdı.
Parker'ın s. 93'ü tohumun kimliğini (*Abrus precatorius*) sayfa
seviyesinde doğrulamıştı; Faz 3'te aynı kitabın oyun bölümü bulununca
**kural kaynağı da açıldı**.

Yani bu madde artık ikisini birden taşıyor ve ikisi **ayrı** kapılardır:

| | Durum |
|---|---|
| **Güvenlik** doğrulaması | ✅ künyeli olgu |
| **Oynanabilirlik** doğrulaması | ⛔ dış test bekliyor |

Prozada özgün malzeme **anlatılıyor** ama oynamak için **yasaklanıyor**:
oyunun adı tohumdan geliyor, yani ikame oyunun adını da bir tarihe
çeviriyor — ve bu gizlenmedi.

---

## 15 · Yeniden kurgulama

Bu batch'te **yeniden kurgulanmış oyun yazılmadı** ve bu bir eksik değil
bir karardır (§ 5.2): erişilebilir tek kaynakları Viktorya
yeniden kurgulamalarıdır ve **eski bir kurgu, yeni bir kurgu kadar kesin
görünür**.

On `reconstructed` kayıt `reconstructionPlan`'larını koruyor. Faz 2'de
yazılan `tablut` bu kategorinin örneği olarak duruyor ve orada dayanak
bir **birinci elden tanık günlüğüdür**, bir derleme değil.

---

## 16 · Manuscript gizliliği

| | |
|---|---:|
| Takip edilen manuscript dosyası | **0** |
| Takip edilen korumalı kural bloğu | **0** |
| Takip edilen Türkçe pilot metni | **0** |
| Sızıntı fikstürü | 5 · hepsi beklendiği gibi |

Faz 2'nin bulduğu gerçek sızıntı (altı oyunun tam İngilizce kural metni
public depoda) düzeltilmiş durumda. Faz 3'ün sekiz yeni maddesi
**baştan** korumalı katmana yazıldı: `02_MANUSCRIPT/` ve
`01_SOURCE/rules/` takip edilmiyor.

Dört hatlı dedektör (yapısal etiket · içerik imzası · yoğunluk · pilot
işareti) yürürlükte ve `validate_structure.py` korumalı katmanın
**gerçekten** takip edilmediğini olgu olarak doğruluyor.

---

## 17 · Kasıtlı kusur testleri

`selftest.py` **126 denetim** koşuyor (Faz 2: 117). Yedinci bölüm Faz 3
kapılarını sınar.

| Kusur sınıfı | Yakalanıyor mu |
|---|---|
| Bütçeyi 1 mm aşan diyagram | ✅ |
| Render edilmemiş diyagram | ✅ |
| Tanımsız düğümde duran taş | ✅ |
| Kopuk kenar (graph tahta) | ✅ |
| Uydurulmuş locator (`verified` kaydı yok) | ✅ |
| Erişilemeyen kaynağın locator taşıması | ✅ |
| Sıfır doğrulanmış kaynakla yazılmış `draft` | ✅ |
| Dış testsiz `locked` | ✅ |
| Ticari metne giren Türkçe cümle | ✅ |
| Public depoya sızan kural prozası (etiketli/etiketsiz) | ✅ |
| Beyansız yeniden kurgulama | ✅ |
| Kısıtlı oyunun kapsama girmesi | ✅ |
| Eksik oyuncu/süre/malzeme alanı | ✅ |
| Sayfa modeli uyuşmazlığı | ✅ |

---

## 18 · CI ve Git

| | |
|---|---|
| Dal | `faz/3-blok-1` |
| CI | ✅ **YEŞİL** |
| Açık gereksiz PR | yok |
| `.gate` | **`phase1`** — yükseltilmedi |

Faz 2 `main`'e merge edilmiş ve dalı silinmiş durumda. Faz 3 çalışması
tek bir dalda toplandı ve her anlamlı adımdan sonra CI beklendi.

---

## 19 · Faz 3 Definition of Done

| | Ölçüt | Durum |
|---|---|---|
| ✅ | Yazılan oyunlar onaylı 100 kapsamından | tamam |
| ✅ | Ticari içerik İngilizce | tamam |
| ✅ | Türkçe test içeriği yalıtılmış | tamam |
| ✅ | Erişilebilir kaynaklı oyunlar önceliklendi | tamam |
| ✅ | Engelli oyunlar doğru ertelendi | 4 engelli · 82 sırada |
| ✅ | Uydurulmuş kaynak kanıtı yok | tamam |
| ✅ | Kurallar tam | 8/8 |
| ⚠ | Oynanabilirlik denetimleri | iç kontroller geçti · **dış test yok** |
| ✅ | İç simülasyon politikası uygulandı | kullanılmadı, gerekmedi |
| ✅ | Yeniden kurgulananlar belgeli | plan korundu; yenisi yazılmadı |
| ✅ | Diyagramlar v1.3'e uygun | 16/16 |
| ✅ | Her diyagram ≤150 mm | 16/16 · azami 111,5 |
| ✅ | Diyagramlar render edilip ÖLÇÜLDÜ | tamam |
| ⚠ | İlk 10 oyun gerçek dizgide ölçüldü | **11 oyun ölçüldü**, 8'i yeni |
| ✅ | Kitap sayfa tahmini yeniden hesaplandı | 316 → **268** |
| ✅ | Aile dengesi izlendi | 100/100 |
| ✅ | Kültür dengesi izlendi | 71 kültür · çerçeve kusuru düzeltildi |
| ✅ | Güvenlik/malzeme kuralları | tamam |
| ✅ | Manuscript sızıntısı = 0 | tamam |
| ✅ | Türkçe sızıntısı = 0 | tamam |
| ✅ | Kasıtlı kusur testleri geçiyor | 126 denetim |
| ✅ | Selftest yeşil | tamam |
| ✅ | CI yeşil | tamam |
| ⏳ | Faz 3 işi `main`'e merge | bu rapordan sonra |
| ✅ | Gereksiz açık PR yok | tamam |
| ✅ | Faz 3 raporu | bu belge |

### ÜRETİM TAMAM ≠ RESMÎ KAPI TAMAM

| | |
|---|---|
| **PRODUCTION COMPLETE** | ✅ bu batch için **EVET** |
| **FORMAL PHASE GATE COMPLETE** | ⛔ **HAYIR** |

Roadmap'in Faz 3 kapısı **57 oyun** ve **57 oynanabilirlik testi** ister.
Yazılan 11, geçen test 0. Faz 3 **üretim şeridi** açıldı ve ilk batch'ini
verdi; **resmî kapı açılmadı** ve `.gate` `phase1` olarak kaldı.

---

## 20 · Kalan bloklayıcılar

| # | Blok | Kimde |
|---|---|---|
| 1 | **Dış insan oynanabilirlik testi** | kurucu — paket hazır |
| 2 | **Telifli kaynak erişimi** | kurucu — 4 oyun engelli, 82 sırada |
| 3 | Tahtasız aile kültür dengesi kararı | kurucu — öneri hazır |
| 4 | Totolospi aile/kaynak çelişkisi | araştırma |
| **A5** | `STYLE.md` v2.0 onayı | kurucu |

Birinci blok değişmedi ve Faz 2'den beri aynı: **ajan oyun testi
yapamaz.** Sekiz yeni madde bu yüzden `draft` seviyesinde duruyor.

---

## 21 · Faz 4 hazırlığı

Faz 4'e geçilmedi ve geçilmeyecek.

Faz 3 üretim şeridi devam edebilir: kuyruk hazır, öncelikler ölçülmüş,
diyagram dili düzensiz tahtaları taşıyor, sayfa modeli gerçek ve bant
içinde. **Üretim hızını belirleyen tek şey kaynak erişimidir.**

| Hazır | Değil |
|---|---|
| Üretim kuyruğu ve öncelikler | Dış test kanıtı |
| Diyagram dili v1.3 + 150 mm bütçesi | Telifli kaynak erişimi |
| Kalibre sayfa modeli (268) | `locked` oyun (0) |
| Yazım şablonu 11 oyunda sınandı | Resmî kapı |

---

## 22 · Bu fazın kendi hakkında bilmediği

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| Sekiz madde masada çalışıyor mu | **dış test** — açık |
| Taşma oranı %9'da kalıyor mu | Faz 4 · daha büyük örneklem |
| 82 "denenmemiş" oyunun kaçı erişilebilir | sıraya geldikçe |
| Graph notasyonu POD baskıda okunuyor mu | Faz 5 · prova kopya |
| Pong-hau-ki'nin kapalı kenarı doğru mu | şeklin daha iyi bir nüshası |

İlk satır Faz 2'den beri aynı yerde duruyor ve durmaya devam ediyor.
**On bir madde yazıldı, sıfırı test edildi.**

---

**⛔ FAZ 4 BAŞLAMADI.** `.gate` = `phase1`. Ajan durdu.
