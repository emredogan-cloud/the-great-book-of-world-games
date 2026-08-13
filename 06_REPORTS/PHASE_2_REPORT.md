# FAZ 2 RAPORU — Pilot, sayfa doğrulaması, diyagram dili ve dizgi kalibrasyonu

> **The Great Book of World Games** · Faz 2 · Dal: `faz/2-pilot`
>
> Bu faz bir üretim fazı değil bir **ölçüm** fazıdır. Ürettiği en değerli
> şey metin değil, **üç sayı ve üç hayır**dır.
>
> Ölçülen her sayı `06_REPORTS/*.json` içinde durur ve **üretilir**;
> bu rapor onları yorumlar.

---

## 0 · Tek bakışta

| | Ölçülen | Hedef | Durum |
|---|---:|---:|---|
| Kilitli kapsam | **100 oyun · 71 kültür** | 100 · ≥45 | ✅ |
| Aile dengesi (A2) | **10 / 17 uygulandı** | 10 / 17 | ✅ |
| Pilot oyun | **12** | 12 | ✅ |
| Pilot aile kapsaması | **7/7** | 7/7 | ✅ |
| Yeniden kurgulanan pilot | **2** | ≥2 | ✅ |
| Tahtasız · 5+ oyunculu · asimetrik | **2 · 3 · 1** | ≥1 her biri | ✅ |
| **Sayfa doğrulaması denendi** | **12/12** | 12/12 | ✅ |
| **Sayfa doğrulaması BAŞARILI** | **7/12** | 12/12 | ⛔ |
| **≥2 doğrulanmış kaynak (locked eşiği)** | **2/12** | 12/12 | ⛔ |
| Diyagram dili donduruldu | **v1.1** | v1.0 | ✅ |
| Gerçek dizgi ölçümü | **3 oyun** | 12 oyun | ⚠ |
| Sayfa modeli | **316** | 256 ± %6 | ⛔ **+%23,4** |
| **DIŞ İNSAN TESTİ** | **0** | 12 | ⛔ **YAPILMADI** |
| Kapıların kendi testi | **117 denetim** | 0 hata | ✅ |
| CI | **YEŞİL** | yeşil | ✅ |

### Faz 2 KAPANMADI — ve kapanmaması doğrudur

`.gate` **`phase1` olarak kaldı.** Yol haritasının `phase2` kapısı
12 `locked` oyun ister; **sıfır oyun `locked` olabildi** ve sebebi
disiplin değil **kanıt eksikliğidir**:

1. **Dış insan testi yapılmadı.** Ajan test yapamaz; sahte kayıt üretilmedi.
2. **12 pilot oyunun 2'si ≥2 sayfa-doğrulanmış kaynağa sahip.**

Bu iki cümle bu raporun en önemli iki cümlesidir. İkisi de **ölçümdür**,
mazeret değil.

---

## 1 · Kurucu kararları — dördü de kapandı

| # | Karar | Kayıt | Mekanizma |
|---|---|---|---|
| **A1** | Manuscript public olmaz, iş durmaz | K12 | 4 hatlı sızıntı dedektörü + fikstürler |
| **A2** | Av-kuşatma 14→10 · Savaş tahtası 13→17 | K13 | `family_index.json` + `validate_scope.py` |
| **A3** | Nihai 100 oyun kilitli | K14 | `scope_lock.json` + sha256 + şerh zorunluluğu |
| **A7** | Dış testçi var; iç ≠ dış kanıt | K15 | `qa_playable.py` evidenceType ayrımı |

Ek olarak Faz 2'de üç karar daha alındı: **K16** (dil ayrımı),
**K17** (sayfa doğrulaması bir kayıttır), ve diyagram dilinin
dondurulması.

---

## 2 · A2 · Yeniden dengeleme uygulandı

| Aile | Faz 1 | **Kilitli** | Uygun aday |
|---|---:|---:|---:|
| Ekim | 14 | 14 | 14 |
| **Av ve kuşatma** | 14 | **10** | 10 |
| Eve dönüş yarışı | 15 | 15 | 19 |
| Çizgi ve toprak | 14 | 14 | 18 |
| **Savaş tahtası** | 13 | **17** | 20 |
| Şans ve cesaret | 15 | 15 | 19 |
| Tahtasız | 15 | 15 | 19 |
| **Toplam** | 100 | **100** | 119 |

Yeniden dengeleme uygulandığında seçim modeli **tam 100** oyun üretti ve
yedi ailenin hedefi de doldu. Yani liste bir tercih değil bir **sonuçtur**:
aynı girdi her makinede aynı listeyi üretir.

**Savaş tahtası şişirilmedi.** Ailede 20 uygun aday var; 17 seçildi. Seçim
hâlâ bir seçimdir, doldurma değil.

---

## 3 · A3 · Nihai 100 oyun — ve kilidin nasıl korunduğu

`01_SOURCE/scope_lock.json` · **100 oyun · 71 kültür · 19 yedek**
sha256 `71158f75e0fb…`

Alt başlığın vaadi (45 kültür) **%58 fazlasıyla** karşılanıyor.

### Kilit iki yönlü korunur ve ikincisi daha önemlidir

| Sessiz bozulma | Nasıl yakalanır |
|---|---|
| **Liste değişir** | kimlik özeti tutmaz |
| **Envanter kayar** | kilit, kaydın *karar anındaki* aile · kültür · bölge · oynanabilirlik · kısıt · araştırma değerlerini saklar ve her koşuda karşılaştırır |

İkincisi olmadan bir oyun sessizce `dropped` olabilir, kısıt taramasından
`restricted` çıkabilir ve **hiçbir dosyada değişiklik görünmezdi.**
Fikstürle kanıtlandı: `konane` envanterde `restricted` yapıldığında kapı
üç ayrı denetimde birden ısırdı.

### Kapsam bulgusu — tahtasız ailede kültürel yoğunlaşma

Kilitli listede **tahtasız ailenin 15 oyunundan 5'i "English"** kültürüne
ait (hopscotch · marbles · conkers · cats-cradle · fivestones). Aile
başına kültür sayısı 11 ve bu, yedi ailenin **en düşüğü**.

Bu bir kural ihlali değil ama bir **editoryal zayıflıktır**: "malzemesi
olmayan oyun en çok kültüre yayılmış oyundur" diyen bir aile açılışının
altında beş İngiliz oyunu durursa, açılış kendi tezini zayıflatır.
Faz 3 kararı olarak kayda geçirildi.

---

## 4 · Pilot — 12 oyun ve neden bunlar

Seçim ölçütü kolay oyunlar değil **zor** oyunlardı. Her pilot oyun
`pilot_lock.json § whyHard` alanında **hangi mimari varsayımı sınadığını**
yazmak zorundadır; gerekçesiz seçim kapıdan geçemez.

| # | Oyun | Aile | Sınadığı varsayım |
|---|---|---|---|
| 1 | Bao la Kiswahili | ekim | en karmaşık kural seti 650 kelimeye sığar mı |
| 2 | **Tablut** | av-kuşatma | yeniden kurgulama + asimetri |
| 3 | **Yut Nori** | yarış | 2→8 oyuncu ölçeklemesi |
| 4 | **Fanorona** | savaş tahtası | çift yönlü alma tek eyleme bölünebilir mi |
| 5 | Go | çizgi-toprak | uyarlama (9×9) görünür kılınabilir mi |
| 6 | Shogi | savaş tahtası | sayfa bütçesi krizi |
| 7 | Royal Game of Ur | yarış | yeniden kurgulama + en eski madde |
| 8 | Olinda Keliya | ekim | zehirli malzeme → güvenli ikame |
| 9 | Mahjong | şans | malzeme evde yok + puanlama patlaması |
| 10 | Astragaloi | şans | bahsin puana çevrilmesi (K5) |
| 11 | Cat's Cradle | tahtasız | diyagram dilinin yıkım testi |
| 12 | Mbube-Mbube | tahtasız | 6–20 kişi + gözetim + tek kaynak |

**Şartların hepsi karşılandı:** 7/7 aile · 2 yeniden kurgulanmış
(Tablut, Ur) · 2 tahtasız · 3 beş+ oyunculu · 1 asimetrik.
Batch dağılımı 4/4/4.

---

## 5 · SAYFA DOĞRULAMASI — bu fazın en sert bulgusu

Faz 1 şunu yazmıştı: *160/160 kayıt `bibliographic` taşıyor; sayfa
açılmadı.* Faz 2'nin ilk işi pilotu `page-verified` seviyesine çıkarmaktı.

**Denendi: 12/12. Başarıldı: 7/12. `locked` eşiğini geçen: 2/12.**

### 5.1 Gerçekten açılan kaynaklar

Dokuz künye açıldı, pasajı okundu ve **kaynağın kendi cümlesiyle** kayda
geçti (`01_SOURCE/source_verification.json`).

| Oyun | Kaynak | Locator |
|---|---|---|
| Yut Nori | Culin, *Korean Games* (1895) | § LXX, ss. 66–69 |
| Tablut | Linnaeus, *Lachesis Lapponica* (1811) | c. II, ss. 55–58 |
| Fanorona | Montgomery, *Antananarivo Annual* XI (1887) | ss. 151–153 |
| Go | Falkener, *Games Ancient and Oriental* (1892) | ss. 239–240 |
| Go | Culin, *Korean Games* (1895) | ss. 91–92 |
| Shogi | Falkener (1892) | ss. 155–157 |
| Cat's Cradle | Jayne, *String Figures* (1906) | ss. 324–333 |
| Cat's Cradle | Haddon, *Cat's Cradles* (1911) | s. 1 |
| Olinda Keliya | Parker, *Ancient Ceylon* (1909) | ss. 93, 225–226 |

### 5.2 Doğrulamanın ÜÇ yan ürünü — hiçbiri beklenmiyordu

**① Bir yeniden kurgulama kararı SINANDI ve ONAYLANDI.**
Faz 1, Tablut'ta kralın kaçış hedefini "kenar" olarak okumuştu. Linnaeus'un
3. maddesi bunu doğruluyor: *"If the king should stand in b… he may escape
by that road."* Aynı doğrulama boşluğu da teyit etti: **metinde berabere
kuralı YOKTUR.** Kitabın berabere kuralı editoryaldir ve prozada öyle yazar.

**② Bir kaynak zinciri KISALDI.**
Fanorona'nın Faz 1 künyeleri Bell (1960) ve Murray (1952) idi; ikisi de
telif altında. Doğrulama sırasında **1887 tarihli birincil saha kaydı**
bulundu ve tam metni açık. Kitap artık bir derlemeye değil, kaydın
kendisine dayanıyor.

**③ Bir editoryal karar ZORUNLU hâle geldi.**
Falkener ve Culin, Go tahtasının **19×19** olduğunu söylüyor. Kitabın 9×9
basma niyeti bir kolaylık değil bir **uyarlamadır** ve artık prozada da
diyagram altyazısında da öyle yazmak zorunda.

### 5.3 Engellenen dokuz künye — ve dürüst sebepleri

| Oyun | Kaynak | Sebep |
|---|---|---|
| Bao la Kiswahili | de Voogt (1997) | telif · açık tam metin yok |
| Royal Game of Ur | Finkel (2007) + BM 33333b | telif · müze kaydı HTTP 403 |
| Mahjong | Parlett (1999) | telif |
| Astragaloi | Pollux, *Onomasticon* | denetlenebilir açık edisyon yok |
| Mbube-Mbube | Zaslavsky (1973) | telif · **zaten tek kaynak** |
| Tablut (2.) | Murray (1952) | telif · ödünç kısıtı |
| Shogi (2.) | Murray (1913) | kamusal alan ama **erişim** kısıtlı (HTTP 401) |
| Olinda Keliya (kural) | Russ (2000) | telif |
| Yut Nori (2.) | Culin (1907) | **aynı yazar** — bağımsız sayılmaz |

Son satır bir erişim sorunu değil bir **sayım kuralıdır** ve kaydın
kendisi bunu söylüyor.

### 5.4 Bulgunun anlamı

> **Sayfa doğrulaması, pilotu 12 kilitlenebilir oyundan 2'ye indirdi.**

Faz 1'de 122 oyunun "≥2 bağımsız kaynağı" vardı. O sayı **künye**
seviyesindeydi. Sayfa seviyesinde bar çok daha yüksek çıktı ve sebebi
tek cümlede özetlenebilir:

> Oyun tarihinin omurgası **20. yüzyıl telifli monografileridir**
> (Murray 1952 · Bell 1960 · Parlett 1999 · de Voogt 1997), ve bunların
> hiçbiri açık tam metin değildir.

Doğrulanabilen her şey **1887–1912 arası kamusal alan literatüründen**
geldi. Bu, kitap için bir fırsat da olabilir — birincil kayıtlar daha
eski ve daha yakın — ama **kütüphane erişimi olmadan 100 oyunun
sayfa doğrulaması yapılamaz.**

**Faz 3 için bloklayıcı öneri:** kurucu bir kütüphane erişimi (üniversite
kütüphanesi ya da archive.org ödünç hesabı) sağlamadıkça, `locked` eşiği
100 oyunda karşılanamaz.

---

## 6 · Kural doğrulaması ve yazılan pilot

`ruleCompleteness` beş öğe kapısı Faz 1'den değişmeden yürürlükte;
119 oyun üretime hazır, `qa_rules` 20 denetimle yeşil.

**Yazılan: 3 oyun** (Tablut · Yut Nori · Fanorona).

Neden üç? Çünkü kural metni **yalnızca sayfa seviyesinde doğrulanmış
kaynağa dayanabilir** ve tam kural setini veren üç kaynak açılabildi.
Öteki dokuz oyunda:

- 5 oyunun kaynağı **hiç açılamadı**
- 4 oyunda kaynak **tahtayı verdi, tur kurallarını vermedi**
  (Falkener shogi'nin taş hareketlerini tabloyla verir ama OCR üzerinden
  denetlenemedi; Parker açıkça başka bir esere yönlendirir)

**Uydurulmadı.** Bu, Faz 1'in Mehen kararının aynısıdır: bir aile oyunu
kitabı için bu maddeleri "çalışır hâle getirmek" kolaydı ve yanlış olurdu.

### Faz 1'in bir veri kusuru bulundu ve düzeltildi

`tablut` ve `patolli`, üç indeksi besleyen alanları taşımıyordu
(`players` · `durationMinutes` · `ageMinEstimate` · `materialsHint`).
Kayıtlar `candidate` olduğu için hiçbir Faz 1 kapısı bunu istemiyordu.
Sonuç: iki oyun **oyuncu sayısı ve süre indekslerinden sessizce
kaybolurdu** — kitabın en çok kullanılan bölümünden.

Düzeltildi ve `validate_scope.py` artık kilitli her oyun için bu dört
alanı şart koşuyor.

---

## 7 · TÜRKÇE DIŞ TEST — paket hazır, oturum YAPILMADI

**Bu bölüm bu raporun en kısa ve en önemli bölümüdür.**

| | |
|---|---|
| Test paketi | ✅ hazır — 3 oyun + testçi kılavuzu + kayıt formu |
| Kayıt şeması | ✅ hazır — `qa_playable.py` denetliyor |
| **Gerçek oturum** | ⛔ **SIFIR** |
| **Test kaydı** | ⛔ **SIFIR** |

`01_SOURCE/playtests/` **boştur ve boş kalmıştır.** Ajan oyun testi
yapamaz; testçi insandır ve yalnızca kitaptaki metni okur.

> **Sahte kayıt üretilmedi.** Üretilseydi bu proje biterdi.

Paket Türkçedir çünkü testçiler Türkçe konuşuyor. Malzeme
`TEST-ONLY / TURKISH PILOT` işaretini taşır, ticari manuscript'e giremez
ve mekanizma bunu denetler.

### Kanıt türleri karışmadı

`qa_playable.py` `internal` (ajan) ve `external` (insan) kanıtı ayrı sayar
ve yalnızca `external` kaydı kapı olarak kabul eder. Fikstürle kanıtlandı:
bir `internal` kayıt kilitli bir oyunu **açmıyor**.

Gerekçe bir aşağılama değil bir tanımdır:

> **Bir kural metnini yazan zihin, o metni okuyup anlamadığını
> keşfedemez.**

### Kurucudan beklenen

1. Testçilere `01_SOURCE/pilot_tr/` paketini vermek
2. Üç oyunu gerçekten oynatmak
3. Formları `01_SOURCE/playtests/<gameId>.json` olarak işlemek
4. `result: ambiguous` çıkan her oyunda **kural metnini düzeltmek** ve
   yeniden test etmek

Bu dört adım tamamlanmadan **hiçbir oyun `locked` olamaz** ve Faz 3
başlayamaz.

---

## 8 · İngilizce ticari sürüm — ve neden çeviri değil

Üç oyunun ticari sürümü **doğrudan İngilizce yazıldı**. Türkçe pilot bir
çeviri kaynağı olarak kullanılmadı.

Fark bir iddia değil, kayıtta duran bir **veridir**. Örnek:

| | Türkçe pilot | İngilizce ticari |
|---|---|---|
| Fanorona alma | "çekilerek alma" — tek başlık, iki paragraf | `capture by withdrawal` — **altı ayrı tek eylemli cümle** |
| Tablut kaçış | "en dış kenardaki herhangi bir kare" | "any square of the outer edge" + ayrı bir `kingCapture` bloğu |
| Yut Nori yön | "saat yönünün tersine" | "against the sun" — **Culin'in kendi ifadesi korundu** |

Son satır bir üslup tercihi değil bir **doğruluk kararıdır**:
"anticlockwise" tahtanın hangi yüzünden bakıldığına göre değişir;
Culin'in "against the sun"u değişmez.

### Bağımsız doğrulama

Her ticari kayıt yedi başlıkta ayrı doğrulama kaydı taşır: kaynak · kural ·
oynanabilirlik · netlik · terminoloji · kültürel sadakat · diyagram.
Eksik bir başlık `qa_language_split.py` kapısını kırmızı yakar.

> ⚠ **İngilizce sürümün oynanabilirliği de test EDİLMEDİ.** İç doğrulama
> geçti; dış test yapılmadı. Türkçe pilotun geçmesi İngilizce sürümü
> kanıtlamaz ve İngilizce sürüm de henüz kanıtlanmadı.

---

## 9 · DİYAGRAM DİLİ — donduruldu (v1.1)

`00_CONTEXT/DIAGRAM_LANGUAGE.md` + `07_ASSETS/diagrams/diagram_language.json`

### 9.1 Beş tahta sınıfı — ve dördün neden yetmediği

Tahta merkezli tek bir koordinat sistemi bu kitabı **taşımıyor**:

| Sınıf | Koordinat | Sınadığı pilot |
|---|---|---|
| `cell` | sütun-satır (`e5`) | Tablut · Shogi |
| `point` | sütun-satır, kesişimde | Go · Fanorona |
| `pit` | sıra-çukur (`A'5`) · **rakamla** | Bao · Olinda |
| `track` | durak numarası (`21a`) | Yut Nori · Ur |
| `bodily` | referans çerçevesi | **Cat's Cradle · Mbube-Mbube** |

Beşinci sınıf olmadan ip figürleri ve yirmi kişilik çember
anlatılamıyordu. `bodily/hands` çerçevesi **Jayne'in 1906'da çözdüğü**
sorunu (yön adları kimin bakışına göre) doğrudan devralıyor — yani
sayfa doğrulaması diyagram dilini de besledi.

### 9.2 Ölçüm dilin KENDİ kuralında bir kusur buldu

> Cat's Cradle'ın üç paneli yan yana **214 mm**. Tam genişlik sınırı **180 mm**.

§ 2.5a üç panel şart koşuyordu, § 7 ise 180 mm sınır koyuyordu ve ikisi
aynı anda sağlanamıyordu. **Kusur bir tanımlayıcıda değil dilin
kendisindeydi** ve onu bir insan gözü değil **render ölçümü** buldu.

Düzeltme: `bodily/hands` panelleri **dikey** dizilir → 70 mm.
Notasyon değişmedi, dizilim değişti. Sürüm v1.0 → v1.1.

### 9.3 En sert denetim: yeniden kurgulama tutarlılığı

Bir oyun kayıtta `reconstructed` ama diyagramı öyle demiyorsa, kusursuz
çizilmiş bir tahta prozanın dürüstlüğünü **sessizce** bozar: okur
diyagrama bakar ve tarihsel kesinlik görür. `qa_diagram.py` bunu iki
yönlü denetler ve fikstürle kanıtlandı.

Ayrıca **ölü efsane sembolü** yasak: efsane, kullanılan sembollerin *tam*
kümesidir. Kullanılmayan bir sembol okuru tahtada olmayan bir şeyi
aramaya gönderir.

**8 diyagram gerçek SVG'ye render edildi** — üretim varlığı değil,
**ölçüm girdisi**. Diyagramın kapladığı alan artık tahmin değil.

---

## 10 · GERÇEK DİZGİ ÖLÇÜMÜ — bu fazın asıl teslimatı

8,5 × 11 trim · Times-Roman 10,5/13,5 · 181 mm sütun · gerçek satır kırma.

| | Faz 1 hipotezi | **Faz 2 ölçümü** | |
|---|---:|---:|---|
| Kelime / sayfa | 320 | **389** | hipotez **%18 düşük** |
| Kelime / oyun | 650 | **708** | bantta ✅ |
| **Metin** sayfa/oyun | — | **1,37** | fark **0,01** |
| **Diyagram** sayfa/oyun | — | **0,45** | fark **0,55** |
| Toplam sayfa/oyun | 2,00 | **1,82** | bantta ✅ |
| Faturalanan sayfa/oyun | 2,00 | **2,67** | çift sayfa mimarisi |

### 10.1 Asıl bulgu

> ## Sayfa bütçesi bir KELİME bütçesi değil, bir DİYAGRAM bütçesidir.

Üç oyunun metni birbirinden **yüzde bir** farklı çıktı (1,37 · 1,37 · 1,38).
Diyagram alanı **üç katına kadar** değişti (0,24 – 0,78).

Bir maddeyi çift sayfadan taşıran şey uzun proza değil, **büyük ya da çok
sayıda diyagramdır**. Tablut iki diyagram taşıyor (biri 2 panelli) ve
189,5 mm ile tek taşan madde oldu.

**Türetilen üretim kuralı:** madde başına diyagram alanı **≤150 mm**.
Bu sayı bir tasarım tercihi değil bir **artıktır**: 484 mm çift sayfa
alanı − 332 mm metin = 152 mm.

**Yazım için sonucu:** 650 kelime hedefi **doğrudur ve daraltılmasına
gerek yoktur.** Kısıt diyagram tarafındadır.

### 10.2 Örneklem uyarısı

Örneklem **üç oyundur** ve bu bir tercih değil bir **kapının sonucudur**:
yalnızca üç oyun sayfa seviyesinde doğrulanmış kaynağa dayanabildi.

Taşma oranı (1/3) kitabın sayfa sayısını belirleyen **tek değişkendir** ve
üç oyun onu belirleyemez. Faz 3'ün ilk on maddesi ölçülmelidir.

---

## 11 · Sayfa modeli ve ekonomik sonuç

| | Faz 1 modeli | **Faz 2 ölçümü** |
|---|---:|---:|
| Gövde (100 oyun) | 200 | **267** |
| Aile açılışları + ön + arka madde | 49 | 49 |
| **Toplam** | **250** | **316** |
| Hedef 256'ya sapma | −%2,3 ✅ | **+%23,4** ⛔ |

**Sayfa hedefi DEĞİŞTİRİLMEDİ.** Yol haritası § 15 sessiz yeniden yazmayı
yasaklar; sapma bir **şerhle** belgelendi ve `page_budget.py` artık
şerhsiz bir sapmada **kırmızı yanıyor** (fikstürle kanıtlandı).

### Ekonomik sonuç — ölçülmüş

| Sürüm | 250 sayfa | **316 sayfa** | Fark |
|---|---:|---:|---:|
| Ciltli baskı | 9,90 $ | 11,02 $ | +1,12 $ |
| **Ciltli telif** | **11,09 $** | **9,97 $** | **−1,12 $** |
| Ciltsiz baskı | 5,25 $ | 6,37 $ | +1,12 $ |
| **Ciltsiz telif** | **8,54 $** | **7,42 $** | **−1,12 $** |
| Başabaş ACOS (ciltli) | %31,7 | **%28,5** | daralıyor |

Her iki sürüm de **pozitif telif üretiyor** ve KDP sayfa sınırları
aşılmıyor (ciltli azami 550). Kitap basılabilir; **pahalılaşır.**
1.000 kopyada 1.120 $ kayıp.

### Önerilen cevap (karar kurucunun · Faz 3)

| # | Seçenek | Ölçümün dediği |
|---|---|---|
| **1** | **Diyagram bütçesi 150 mm** | **ÖNERİLEN** — metne dokunmaz, ölçüm tam olarak bunu işaret ediyor |
| 2 | Kelime hedefini 560'a indirmek | **GEREKSİZ** — metin taşırmıyor |
| 3 | Kapsamı 88 oyuna indirmek | son çare — alt başlıktaki sayıyı bozar |

---

## 12 · MANUSCRIPT KORUMASI — ve bulunan gerçek sızıntı

### 12.1 Dedektör güçlendirildi (K12)

Faz 1'in dedektörü **beş yapısal etikete** bakıyordu. Yetersizdi ve
gerekçesi tek cümledir:

> **Etiketleri silmek, prozayı silmez.**

Dört hat eklendi: yapısal etiket · **içerik imzası** · **yoğunluk** ·
Türkçe pilot işareti. Yoğunluk kritiktir: bir belge kural dilini *örnek*
olarak anabilir; onu manuscript yapan **orandır**.

### 12.2 GERÇEK BİR SIZINTI BULUNDU

Yeni dedektör ilk koşusunda `01_SOURCE/games/*.json` dosyalarını işaretledi.
İnceleme doğruladı: **altı oyunun tam İngilizce kural metni public depoda
duruyordu.**

```
"setup": "Mark the centre square. Stand the king on it. Place the eight
          defenders around him in a diamond…"
```

Bu, kitabın **ticari çekirdeğidir** ve Faz 1'in dedektörü onu göremezdi —
çünkü etiket taşımıyordu.

**Düzeltme:** kural blokları `01_SOURCE/rules/` altına taşındı ve takip
edilmiyor. Public katman yalnızca **metadata** tutar (`ruleCompleteness` ·
`clarity` · `playabilityStatus` · `reconstructionPlan`). Kural kapıları
yerelde tam güçle koşar, CI'da boş koşar ve körlüğü selftest kapatır.

Ayrıca `.gitignore` bir **niyettir**; yeni bir denetim korumalı katmanın
gerçekten takip edilmediğini **olgu olarak** doğruluyor.

### 12.3 Fikstürlerle kanıt

| Fikstür | Beklenen | Sonuç |
|---|---|---|
| `bad-labelled.md` | sızıntı | ✅ 3 etiket |
| **`bad-unlabelled.md`** | sızıntı | ✅ **0 etiket · 10 imza · yoğunluk 1,0** |
| `bad-turkish-pilot.md` | pilot işareti | ✅ |
| `clean-documentation.md` | temiz | ✅ yanlış alarm yok |
| `clean-data-record.md` | temiz | ✅ |

İkinci satır kanıtın kendisidir: **Faz 1 hattının kaçıracağı proza, Faz 2
hattı tarafından yakalanıyor.**

---

## 13 · Dil ayrımı (K16)

`qa_language_split.py` üç şeyi denetler: ticari katmanda Türkçe yok ·
test katmanı işaretli · çeviri beyanı yasak + bağımsız doğrulama zorunlu.

**Makine çevirisini metinden kanıtlamak mümkün değildir** ve kapı bu
iddiada bulunmaz. Ölçebildiğini ölçer, ölçemediğini beyana bağlar ve
beyanı denetlenebilir kılar: `translatedFrom` Türkçe pilotu gösteriyorsa
kapı kırmızı yanar.

### Kapı kendi kusurunu buldu

İlk sürüm tek eşikliydi (≥4 işlev sözcüğü) ve **kendi fikstürünü kaçırdı**:
ticari metne sokulan tek bir Türkçe kural cümlesi üç sözcük taşıyor ve
eşiğin altında kalıyordu. Bir paragraf için doğru olan eşik, bir cümle
için yanlıştı. İki eşikli hâle getirildi; İngilizce metinde yanlış alarm
üretmediği ayrıca kanıtlandı (oyun adları dâhil).

---

## 14 · Kültürel kısıt ve güvenlik

**Faz 1'in kısıt taraması değişmeden korundu.** Altı `restricted` ve üç
`excluded` kayıt kilitli listenin dışında ve `validate_scope.py` bunu her
koşuda doğruluyor (10 kayıt taranıyor).

- `restricted`: Dehontsigwa'ehs · Toli · Pitz · Na'atl'o' · Ayaraaq · Chunkey
- `excluded`: Kalah · Kubb · Buzkashi

**Güvenlik ve malzeme:** pilot, zehirli tohumlu **Olinda Keliya**'yı
kasten seçti. Parker'ın 1909 kaydı *Abrus precatorius* kimliğini
**sayfa seviyesinde doğruladı** — yani güvenlik uyarısı artık bir
genel bilgi değil, künyeli bir olgu.

Aynı kayıt kuralları **vermiyor** ve bu yüzden oyun yazılamadı: güvenlik
doğrulandı, oynanabilirlik doğrulanamadı.

---

## 15 · Kusurlar, kök nedenler, düzeltmeler

| # | Kusur | Kök neden | Düzeltme |
|---|---|---|---|
| 1 | Public depoda tam kural prozası | dedektör yalnızca etikete bakıyordu | 4 hatlı dedektör + korumalı katman |
| 2 | Diyagram dili kendi genişlik sınırını aşıyordu | üç panel kuralı ile 180 mm sınırı çatışıyordu | `hands` dikey dizilir (v1.1) |
| 3 | Dil kapısı tek Türkçe cümleyi kaçırıyordu | eşik paragraf için ayarlıydı | iki eşikli ölçüt |
| 4 | `tablut`/`patolli` üç indeksten düşerdi | alanlar yalnızca `locked` için isteniyordu | kilitli kapsam için şart |
| 5 | `page_budget` kalibre modda hipotezi okuyordu | ölçüm eklendi, model okumadı | ölçüm kazanır + selftest fikstürü |
| 6 | **selftest kendi regresyonumu yakaladı** | girdi değişti, fikstür değişmedi | fikstürler kalibre/hipotez modlarına bölündü |
| 7 | `07_ASSETS/diagrams/**` diyagram dilini de gizliyordu | ignore kalıbı çok genişti | spec dosyaları negasyonla açıldı |
| 8 | CI dizgi ölçümünde kırmızıydı | çıkış kodu 2 (ATLANDI) kusur sayılıyordu | `run_optional` sözleşmesi CI'a taşındı |

**6 numara bu listenin en değerli satırıdır:** selftest, benim yaptığım bir
değişikliğin bir kapıyı körleştirdiğini yakaladı. Bir kapının girdisini
değiştirmek, o kapının testini de değiştirmeyi gerektirir.

---

## 16 · Test altyapısı

| Betik | Denetim | Durum |
|---|---:|---|
| `build_index.py --check` | 1 | ✅ |
| `validate_spec.py` | 26 | ✅ |
| `validate_structure.py` | 58 | ✅ |
| `validate_research.py` | **13** | ✅ (⑦ sayfa doğrulaması eklendi) |
| `qa_taxonomy.py` | 20 | ✅ |
| `qa_rules.py` | 20 | ✅ |
| **`validate_scope.py`** | **22** | ✅ **yeni** |
| **`qa_playable.py`** | 2 | ✅ **yeni** (boş koşuyor) |
| **`qa_language_split.py`** | **13** | ✅ **yeni** |
| **`qa_diagram.py`** | **25** | ✅ **yeni** |
| `page_budget.py` · `editions.py` | — | ✅ |
| **`calibrate_pages.py`** | — | ✅ **yeni** |
| **`selftest.py`** | **117** | ✅ (85 → 117) |

**CI körlüğü kapatıldı:** metin kapıları artık elle yazılmış bir liste
değil, `04_BUILD/qa_*.py` **taramasıyla** koşuyor. Yeni bir kapı yazılıp
listeye eklenmeyi unutmak artık mümkün değil.

Selftest'in altıncı bölümü Faz 2 kapılarını sınar. Bu bölüm kritiktir
çünkü Faz 2'nin koruma kapıları **tasarımı gereği** depoda göremeyecekleri
şeyleri korur: manuscript yok, Türkçe pilot yok, test kaydı yok, kilitli
oyun yok. **Dört kapı birden gerçek veriyle boş koşuyor.**

---

## 17 · Git ve CI

| | |
|---|---|
| Faz 1 PR | ✅ merge edildi (#1), dal silindi |
| Açık gereksiz PR | ✅ yok |
| Dal | `faz/2-pilot` |
| CI | ✅ **YEŞİL** |
| `.gate` | **`phase1`** — yükseltilmedi |

`.gate` yükseltilmedi çünkü `phase2` kapısı 12 `locked` oyun ister ve
sıfır oyun kilitlenebildi. **Kapıyı yükseltip kapsamı sağlamamak
sessizce geçemez** — `validate_spec.py` bunu reddeder ve reddetmesi
doğrudur.

---

## 18 · Faz 2 Definition of Done — dürüst tablo

| | Ölçüt | Durum |
|---|---|---|
| ✅ | A2 yeniden dengeleme uygulandı (10/17) | tamam |
| ✅ | A3 nihai 100 oyun kilitlendi | tamam |
| ✅ | 12 pilot oyun seçildi ve gerekçelendirildi | tamam |
| ✅ | Her aile temsil ediliyor · zor oyunlar seçildi | tamam |
| ✅ | ≥2 reconstructed · ≥1 tahtasız · ≥1 beş oyunculu · ≥1 asimetrik | tamam |
| ⛔ | **Pilot kaynakları sayfa-doğrulandı** | **7/12 kısmi · 2/12 tam** |
| ⚠ | Pilot kuralları tam | 3 yazıldı · 9 kaynak yetersiz |
| ✅ | Ticari üretim dili İngilizce | tamam |
| ⛔ | **Gerçek dış oynanabilirlik testi** | **YAPILMADI** |
| ⛔ | Test kusurları düzeltildi | test yok, kusur yok |
| ⛔ | İngilizce sürümler bağımsız test edildi | iç doğrulama var, dış yok |
| ✅ | `DIAGRAM_LANGUAGE.md` donduruldu | v1.1 |
| ✅ | Gerçek dizgi yapıldı | 3 oyun ölçüldü |
| ✅ | Sayfa modeli yeniden kalibre edildi | 316 · şerhli |
| ✅ | Malzeme/güvenlik uyarlamaları belgelendi | tamam |
| ✅ | Kültürel kısıtlar korundu | 6+3 kayıt kilit dışında |
| ✅ | Manuscript koruması test edildi | fikstürler + gerçek sızıntı bulundu |
| ✅ | Türkçe sızıntı testi geçiyor | tamam |
| ✅ | Selftest yeşil | 117 denetim |
| ✅ | CI yeşil | tamam |
| ✅ | Gereksiz açık PR yok | tamam |
| ✅ | Faz 2 raporu | bu belge |

**Faz 2 KISMEN TAMAM.** Ölçüm ve mimari işleri bitti; **kanıt işleri
bitmedi** ve bitmemesinin sebebi ajanın yapamayacağı iki şeydir:
gerçek insanla test etmek ve telifli kaynaklara erişmek.

---

## 19 · Riskler

| Risk | Durum | Azaltma |
|---|---|---|
| Oyun testçisi yok | ⛔ **hâlâ açık** | paket hazır; kurucu oturum düzenlemeli |
| **Kaynaklara erişilemiyor** | ⛔ **YENİ VE BÜYÜK** | kütüphane erişimi gerekli |
| Sayfa modeli bandı aşıyor | ⚠ şerhli | diyagram bütçesi 150 mm |
| Örneklem küçük (3 oyun) | ⚠ | Faz 3'ün ilk 10 maddesi ölçülmeli |
| Tahtasız ailede kültür yoğunlaşması | ⚠ **yeni** | 5/15 İngiliz; Faz 3 kararı |
| Cat's Cradle diyagram bütçesini aşıyor | ⚠ ölçüldü | 4 sayfalık madde ya da eleme |
| Mahjong malzemesi evde yok | ⚠ açık | uyarlama ya da eleme kararı |
| 38 oyun tek kaynaklı | ⚠ açık | `locked` olamazlar |

### En büyük risk yeni ve Faz 1'de görünmüyordu

> **Kitabın kaynak omurgası telifli 20. yüzyıl monografileridir ve
> hiçbiri açık tam metin değildir.**

Faz 1'in "122 oyunun ≥2 bağımsız kaynağı var" ölçümü künye seviyesindeydi
ve doğruydu. Sayfa seviyesinde aynı havuz **çok daha ince**. Bu risk,
100 oyunu `locked` yapma hedefini doğrudan tehdit ediyor.

---

## 20 · Faz 3 hazırlığı — ve neden HENÜZ BAŞLAYAMAZ

Faz 3'e girmek için yol haritası şunu ister: 12/12 oynanabilir ·
`STYLE.md` v2.0 onaylı · sayfa modeli gerçek ölçümle güncel ·
`.gate` = `phase2`.

**Dördünden ikisi hazır:**

| | |
|---|---|
| ✅ | `STYLE.md` v2.0 ölçümle yazıldı (kurucu onayı bekliyor — A5) |
| ✅ | Sayfa modeli gerçek ölçümle güncel |
| ⛔ | 12/12 oynanabilir — **0/12** |
| ⛔ | `.gate` = `phase2` — **`phase1`** |

### Faz 3 öncesi kapanması gereken üç şey

1. **Dış oynanabilirlik testleri.** Paket hazır; oturum kurucunun.
2. **Kütüphane erişimi.** Sayfa doğrulaması olmadan `locked` yok.
3. **Sayfa modeli kararı.** Üç seçenek yazıldı; öneri diyagram bütçesi.

---

## 21 · Bu fazın kendi hakkında bilmediği

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| Kural metni masada çalışıyor mu | **dış test** — açık |
| İngilizce metin Türkçeden farklı bir yerde bulanıklaşıyor mu | **dış test** — açık |
| Taşma oranı gerçekten 1/3 mü | Faz 3 · ilk 10 madde |
| 0,75 pt çizgi POD baskıda kopuyor mu | Faz 5 · prova kopya |
| Shogi ve Mahjong kitaba girebilir mi | kaynak erişimi çözülünce |
| 100 oyunun kaçı sayfa-doğrulanabilir | kütüphane erişimiyle |

İlk iki satır bu fazın en dürüst kısmıdır: **12 oyunluk pilot seçildi,
üçü yazıldı, sıfırı test edildi.** Notasyon donduruldu ama kanıtlanmadı;
sayfa ölçüldü ama örneklem küçük; koruma güçlendirildi ve **bir gerçek
sızıntı buldu**.

---

## 22 · Kurucudan bekleyen

| # | Ne | Aciliyet |
|---|---|---|
| — | **Dış oynanabilirlik test oturumları** | ⛔ **BLOKLAYICI** |
| — | **Kütüphane / telifli kaynak erişimi** | ⛔ **BLOKLAYICI** |
| — | Sayfa modeli kararı (üç seçenek · § 11) | **YÜKSEK** |
| **A5** | `STYLE.md` v2.0 onayı | ORTA |
| — | Tahtasız ailede kültür yoğunlaşması kararı | ORTA |
| **A4** | Büyük punto | DÜŞÜK (Faz 4) |
| **A6** | Yazar biyografisi | DÜŞÜK (Faz 5) |

---

**⛔ FAZ 3 BAŞLAMADI ve başlayamaz.** `.gate` = `phase1`.
Ajan durdu ve kurucu kararını bekliyor.
