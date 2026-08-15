# FAZ 5 RAPORU — Kapsam değişikliği, arka madde, K24 istisnası ve yedi kapı kusuru

> **The Great Book of World Games** · Faz 5 · Dal: `faz/5-uretim`
>
> Bu rapor Faz 5'in **iki koşusunu** birlikte anlatır ve birincisinin
> başarısızlığını **silmez**.
>
> ```
> FAZ 5 · KOŞU 1 SONUNDA :  20 / 100
> FAZ 5 · KOŞU 2 SONUNDA :  23 / 100
> FAZ 5 · KOŞU 3 SONUNDA :  25 / 100
> HEDEF                  : 100 / 100
> ```
>
> ⛔ **FAZ 5 KENDİ ANA HEDEFİNİ TUTTURAMADI.** Kalan **75 oyun**
> yazılmadı. Rapor bunu ilk sayfada söylüyor ve § 4'te tek tek gerekçesini
> veriyor.

---

## 0 · Tek bakışta

| | Faz 4 | Faz 5 · koşu 1 | **Faz 5 · koşu 2** |
|---|---:|---:|---:|
| **Yazılmış oyun** | 22 | 20 | **25** |
| Kapsamdaki oyun | 100 | 100 | **100** |
| Kapsamdaki kültür | 71 | 73 | **73** |
| Manuscript'teki kültür | 14 | 14 | **17** |
| Doğrulama kaydı | 37 | 44 | **54** |
| `verified` kayıt | 28 | 29 | **31** |
| Arka madde | yok | altı bölüm | **altı bölüm · güncel** |
| Sayfa göndermesi ölçülmüş oyun | — | 20 | **25** |
| Sayfa modeli | 258 | 260 | **258** |
| Hedeften sapma | +%0,8 | +%1,6 | **+%0,8** ✅ |
| Ciltsiz birim telif | 8,41 $ | 8,37 $ | **8,41 $** |
| Ciltli birim telif | 10,96 $ | 10,92 $ | **10,96 $** |
| Diyagram (render) | 27 | 25 | **26** |
| Oyun başına azami diyagram | 144,0 mm | 144,0 mm | **144,0 mm** |
| **K24 istisnası** | — | — | **kayıtlı + etkin** |
| Selftest denetimi | 148 | 172 | **177** |
| Kuyruk öncelik seviyesi | 5 | 6 | **6** |
| **Dış insan testi** | **0** | **0** | **0** ⛔ |
| **`.gate`** | `phase1` | `phase1` | **`phase1`** |
| CI | yeşil | yeşil | **yeşil** |

---

## 1 · NİHAİ KAPSAM DEĞİŞİKLİĞİ (K23) — KORUNDU

Koşu 1'in kapsam değişikliği **açılmadı, dokunulmadı, doğrulandı**.

| | ÇIKARILAN | EKLENEN |
|---|---|---|
| 1 | **Fivestones** · İngiliz · `distinct 2` | **Lagori** · Kannada |
| 2 | **Marbles** · İngiliz · `distinct 3` | **Kho-Kho** · Marathi |

| ölçüt | önce | sonra |
|---|---:|---:|
| kitap · oyun | 100 | **100** |
| kitap · kültür | 71 | **73** |
| tahtasız · kültür | 11 | **13** |
| tahtasız · İngiliz madde | 5 | **3** |
| aile hedefleri | — | **değişmedi** |
| yedek havuz | 19 | **19** |

Aile dağılımı kilitte birebir: sowing 14 · hunt-siege 10 · race 15 ·
territory 14 · war-board 17 · chance 15 · boardless 15 = **100**.

Fivestones ve Marbles manuscript'te **yok**; Lagori ve Kho-Kho kapsamda
**var**. Yinelenen oyun **yok**. Kilit özeti (sha256) her koşuda
denetleniyor ve **şerh bir muafiyet değildir** (§ 12.1).

---

## 2 · FAZ 5 ÖNCESİ VE SONRASI YAZILMIŞ SAYI

| | |
|---|---:|
| Faz 4 sonunda | 22 |
| K23 ile geri alınan (yazılmıştı) | −2 |
| **Koşu 1 sonunda** | **20** |
| Koşu 2'de yazılan | **+3** |
| Koşu 3'te yazılan | **+2** |
| **ŞU AN** | **25 / 100** |

Geri alınan iki maddenin prozası **silinmedi**:
`02_MANUSCRIPT/retired_phase5.json` (korumalı katman) tam metni ve iki
diyagram tanımını taşıyor.

---

## 3 · KALAN OYUNLAR

**75 oyun.**

| | |
|---|---:|
| Kapsam | 100 |
| Yazılmış | 25 |
| **Kalan** | **75** |

### 3.1 Koşu 2'de yazılan üç oyun

| oyun | aile | kültür | kaynak | sayfa |
|---|---|---|---|---|
| **Cat's Cradle** | tahtasız | İngiliz | Jayne 1906 | ss. 324–338 |
| **Shogi** | savaş tahtası | Japon | Culin 1895 | ss. 90–91 |
| **Pachisi** | eve dönüş | Hindustani | Culin 1898 | ss. 851–854 |

Üçü de **doğrudan İngilizce** yazıldı, üçünün de kaynağı **açıldı ve
pasajı alındı**, üçü de yedi başlıkta doğrulama kaydı taşıyor.

Manuscript kültür sayısı **14 → 15** (Hindustani ilk kez).

### 3.2 İki künye zinciri AÇIKÇA beyan edildi

Bu batch'in en önemli editoryal kararı budur:

- **Shogi** — Culin, hesabı *"Mr. Falkener's Games, Ancient and Oriental,
  from which the above account was extracted"* diyerek Falkener'dan
  aldığını **kendisi söyler**. Künye ikisini de adlandırır ve K20 uyarınca
  **tek kanıt hattı** sayar, iki bağımsız kaynak değil.
- **Pachisi** — Culin'in pasajı **Herklots, Qanoon-e-Islam (1832)**
  alıntısıdır. Gözlemci Herklots, aktaran Culin; künye ikisini de yazar ve
  yine **tek hat** sayar.

> Bir kaynağı alıntılayan kaynak, iki kaynak değildir. Aksini saymak,
> künye sayısını iki katına çıkarmanın en kolay ve en sessiz yoludur.

### 3.3 Koşu 3 (batch 2) — iki savaş tahtası oyunu

| oyun | aile | kültür | kaynak | sayfa |
|---|---|---|---|---|
| **Xiangqi** | savaş tahtası | Han Çinlisi | Falkener 1892 | ss. 143–149 |
| **Sittuyin** | savaş tahtası | Birmanya | Falkener 1892 | ss. 177–179 |

İkisi de **tam kural seti** taşıyor. **K20 şerhi künyede açıkça yazılı:**
Falkener bir **Viktorya derlemesidir**, birinci elden gözlem değil; kendi
kaynaklarını (Hyde 1694 · Irwin 1793 · Cox 1801) adlandırır. Erişilebilir
kamusal alanda Çin ve Birmanya kaynaklı **birinci el kural kaydı
bulunamadı** ve künye bunu gizlemiyor.

**İkisi de DİYAGRAMSIZ ve bu bir karardır** (§ 8.2).

Manuscript kültür sayısı **15 → 17**.

---

## 4 · ERTELENEN OYUNLAR — SAYFA SEVİYESİNDE GEREKÇELİ

Faz 5 toplam **on oyunun** kaynağını açtı. Üçü yazıldı, **yedisi
yazılamaz** çıktı. Hiçbiri ikincil bilgiyle ertelenmedi.

| oyun | kaynak | sayfa | bulgu |
|---|---|---|---|
| **hnefatafl** | Fiske 1905 | ss. 58–59 | erişilebilir ama **kural vermiyor** |
| **halatafl** | Fiske 1905 | s. 59 | yalnızca **sözlük göndermesi** |
| **oware** | Culin 1896 | ss. 594, 597–598 | **kimlik tuzağı** — Şam ve Vei kayıtları |
| **jianzi** | Culin 1895 | ss. 39–43 | **nesne anlatılıyor, kural yok** |
| **xiangqi** | Culin 1895 | ss. 82–89 | bölüm **KORE satrancıdır** (Wilkinson) |
| **tien-gow** | Culin 1895 | § LXXXI | bölüm **KORE dominosudur** |
| **patolli** | Culin 1898 | ss. 854–856 | Durán'ın **resmi**, kural metni değil |
| **gomoku** | Smith 1908 | ss. 24–25 | **amaç var, kural seti yok** |
| **go** | Smith 1908 | ss. 24–26 | kural TAM ama **kültür uyuşmuyor** |

### 4.1 `go` — tam bir kaynak, yanlış kültür

Smith 1908 eksiksiz bir kural kitabıdır: sıra, yerleştirme, `ko`, taşların
bir daha oynanmaması, toprak amacı ve sayım. Ama **Japon
kodifikasyonudur** ve sayım yöntemi Japondur (alınan taşlarla toprağı
doldurma), Çin alan sayımı değil. Kapsam kaydı ise **Han Çinlisi** der.

Kurucunun § 9 ölçütü açıktır: *"source supports the claimed culture."*
Karşılanmıyor. Çin biçimi için Smith'in kendi künyesindeki
**Z. Volpicelli, Journal of the China Branch of the Royal Asiatic Society
XXVI** gerekir; bulunamadı.

> Bu, kitabın en kolay yazılabilecek oyunuydu ve tam da bu yüzden en
> öğretici olanı: **kaynağın tam olması yetmez, doğru oyunun kaynağı
> olması gerekir.**

### 4.2 Culin 1895 bir KORE kitabıdır ve üç oyun aynı tuzağa düştü

`xiangqi`, `tien-gow` ve (Faz 4'te) `sugoroku`, `jianzi` — dördü de
Culin'in *Korean Games* cildine bağlıydı. Cildin adı zaten söylüyor:
Kore oyunları, **Çin ve Japon karşılıklarına NOTLARLA**. Notlar
karşılaştırmadır, kural seti değil.

Faz 4 bunu iki oyunda bulmuştu; Faz 5 sayfayı açarak **dördünü de**
doğruladı. Bu artık bir tesadüf değil bir **desen**dir ve kuyruğun
"erişilebilir" etiketinin ne kadar iyimser olabileceğini gösterir.

---

## 5 · KAYNAK DURUMU DAĞILIMI

| durum | koşu 1 | **koşu 2** |
|---|---:|---:|
| `verified` — ≥2 doğrulanmış künye | 3 | **4** |
| `partially-verified` — 1 künye | 20 | **20** |
| `access-blocked` — denendi, erişilemedi | 5 | **5** |
| `record-not-found` — arandı, kayıt yok | 2 | **2** |
| `not-attempted` — sıraya gelmedi | 70 | **69** |

Doğrulama kaydı: **37 → 51** (14 yeni). Durum dağılımı:
`verified` 31 · `pending` 11 · `blocked` 9.

**On bir `pending` kayıt bu fazın asıl birikimidir:** her biri açılmış bir
sayfayı, alınmış bir pasajı ve *neden yazılamadığını* taşır. Bir sonraki
faz aynı on kaynağı yeniden açmayacak.

---

## 6 · KUYRUK

| P | anlamı | sayı |
|---|---|---:|
| 1 | erişilebilir · sayfa-doğrulanmış · kural tam | **23** |
| 2 | erişilebilir · doğrulama tamamlanabilir | **64** |
| 3 | yeniden kurgulanmış · plan belgeli | **5** |
| 4 | **DENENDİ ve erişilemedi** (telif / ödünç) | **5** |
| 5 | çözülmemiş kural kimliği | **1** |
| 6 | **ARANDI ve KAYIT BULUNAMADI** | **2** |

**Erişilebilir 92 · ertelenmiş 8.** Sıra kapıya bağlı, CI'da koşuyor,
P1→P2→P3 önce, P4/P5/P6 sonda.

Lagori ve Kho-Kho **P6'da kaldı** ve **yazılmadı** — kurucunun § 6 talimatı
aynen uygulandı: kapsam kararı bir yazım izni değildir.

---

## 7 · K24 · CATS-CRADLE DİYAGRAM İSTİSNASI

Kurucu 150 mm tavanının **yalnızca cats-cradle** için aşılmasını onayladı.
İstisna **kayıtlı, mekanik ve dar**dır.

| | |
|---|---|
| Genel tavan | **150 mm — DEĞİŞMEDİ** |
| İstisna kapsamı | **yalnızca `cats-cradle`** |
| İstisna tavanı | 340 mm |
| Biçim | genel bayrak **DEĞİL**, `overrides.get(gameId, 150)` kimlik eşlemesi |
| Kayıt | `project_config.json § diagram.diagramBudgetOverrides` + DECISIONS K24 |

### 7.1 Dört kasıtlı kusur testi

| kurgu | beklenen | sonuç |
|---|---|---|
| cats-cradle > 150 mm | **GEÇER** | ✅ |
| başka bir oyun > 150 mm | **KIRMIZI** | ✅ |
| sözlüğe **ikinci** oyun eklenir | **KIRMIZI** | ✅ |
| istisna silinir, cats-cradle aşar | **KIRMIZI** | ✅ |

Üçüncüsü asıl koruyucudur: bir istisna listesi, bir kez *liste* hâline
geldiği anda tavanın kendisi bir **öneriye** dönüşür — ve bu, hiçbir şey
kırmızı yanmadan olur.

### 7.2 ⚠ İSTİSNA ŞU AN KULLANILMIYOR — ve sebebi önemli

| ölçüm | değer |
|---|---:|
| cats-cradle · gerçek footprint | **107,0 mm** |
| normal tavan | 150 mm |
| istisna tavanı | 340 mm |
| **istisna kullanımı** | **0 mm** |

İstisna verildi, uygulandı, test edildi — ve **gerekmedi**.

Sebep, kurucunun beklediği yerde değildi. Sekiz figür 150 mm'ye
sığmıyordu, doğru; ama asıl kısıt **milimetre değil NOTASYON** çıktı:

> **Diyagram dili v1.4 ip figürlerini ÇİZEMİYOR.**

`bodily/hands` çerçevesi soyut bir parmak-ip şeması üretir: üç panel,
daireler ve bir ok. Bu şema *Beşik* ile *Asker Yatağı*'nı birbirinden
**ayırt edemez**. Sekiz figür için üç diyagram üretildi (334,5 mm — istisna
içinde) ve görsel denetimde üçünün de **aynı şemayı** gösterdiği görüldü.

Üç özdeş şemayı basmak, istisnayı **tüketmek** olurdu ama okunabilirliği
**artırmazdı** — ve kurucunun kendi cümlesi şudur: *"The objective is
MAXIMUM LEGIBILITY, not MAXIMUM SIZE."* Bu yüzden cats-cradle **tek**
diyagramla (Beşik, 107 mm) basılıyor; kalan yedi figür metinde **sırayla**
verilmiştir ve diyagram altyazısı bunu **açıkça söylüyor**.

**İstisna kaldırılmadı.** Kurucu kararıdır, kayıtlıdır ve dil bir gün
figürleri çizebildiğinde hazır duruyor.

> **AÇIK KARAR:** sekiz ip figürünün çizilebilmesi için diyagram dili
> **v1.5** gerekir (yeni bir `bodily` çerçevesi ya da figür notasyonu).
> Dili büyütmek bir **mimari karardır** (§ 16) ve ajan tek başına yapamaz.
> v1.2→v1.3 ve v1.3→v1.4 geçişleri de böyleydi.

---

## 8 · DİYAGRAM ÖLÇÜMLERİ

| | koşu 1 | **koşu 2** |
|---|---:|---:|
| Render edilen diyagram | 25 | **26** |
| En küçük | 36,1 mm | **36,1 mm** |
| En büyük | 111,5 mm | **111,5 mm** |
| **150 mm'yi aşan DİYAGRAM** | 0 | **0** |
| **Kendi tavanını aşan OYUN** | 0 | **0** |
| Azami oyun toplamı | 144,0 (tablut) | **144,0** (tablut) |
| Diyagram dili | v1.4 | **v1.4 — değişmedi** |

### 8.1 GÖRSEL DENETİM ÜÇ GERÇEK KUSUR BULDU

Ölçüm sayıları **tertemizdi**. Üçü de yalnızca diyagramlara **bakınca**
görüldü — Faz 4'ün tilki dersinin aynısı.

**① Pachisi tahtası HAÇ değil IZGARA çiziliyordu.**
Pachisi tahtası dört kollu bir haçtır; köşeler **boştur**. `cell` sınıfı
11×11 dolu bir ızgara çizdi. Bu, § 17'nin yasakladığı *"düzensiz tahtayı
uygun bir ızgarayla idare etme"*nin tam kendisidir ve kural metniyle
**çelişiyordu**.
→ Diyagram **kaldırıldı**. v1.4 hücre-maskeli bir tahtayı ifade edemiyor
ve yeni notasyon bir mimari karardır (§ 16). Kurulum metni haçı zaten
tarif ediyor: *"four arms, each three squares wide and eight long."*

**② Shogi kurulumunda yirmi taşın hepsi AYNI çiziliyordu.**
Okur diyagrama bakıp kurulumu yapamazdı: bir mızrağı bir piyondan ayırt
edemiyordu.
→ Şah ve karşı şah ayrı gliflere alındı ve altyazı artık diyagramın **ne
gösterdiğini** dürüstçe söylüyor: *nerede*, **hangisi değil** — ve hangi
karede hangi taşın durduğu **kurulum listesindedir**.

**③ Cats-cradle efsanesinde iki sembol BİREBİR AYNI daireydi.**
*"ipin tutulduğu parmak"* ve *"ip yolu"* satırları ayırt edilemiyordu.

### 8.2 v1.4 ÜÇ KURAL-TAŞIYAN TAHTA UNSURUNU ÇİZEMİYOR

Tek bir fazda **üç ayrı** tahta özelliği çizilemedi ve üçü de **kural
taşıyor** — yani eksik çizmek, kuralla **çelişen** bir tahta üretir:

| unsur | oyun | neden kural taşır | v1.4 |
|---|---|---|---|
| **haç biçimli tahta** | pachisi | köşeler yoktur; iz haçın kollarını dolaşır | `cell` dolu ızgara çizer |
| **nehir + hisar köşegeni** | xiangqi | fil nehri geçemez; general hisarı terk edemez | `point` düz ızgara çizer |
| **terfi köşegeni** | sittuyin | er köşegene varınca terfi eder | `cell` köşegen çizemez |
| **ip figürleri** | cats-cradle | oyunun kendisi figür dizisidir | `bodily/hands` soyut şema |

Dördü de **diyagramsız** basılıyor ve dördünde de gerekçe maddenin
`englishValidation.diagram` alanında yazılı.

> **AÇIK KARAR — diyagram dili v1.5.** Bu dört unsur bir eğilim değil bir
> **desen**dir: kitabın kalan 75 oyununun büyük kısmı düzensiz tahtalıdır.
> Dili büyütmek bir **mimari karardır** (§ 16) ve ajan tek başına yapamaz.

---

## 9 · YENİ KAPI: EFSANEDE AYIRT EDİLEMEYEN SEMBOL

Faz 4, efsane sembolünün **çizilmesini** sağlamıştı (font bağımlılığı
gitti). Ama çizimlerin **birbirinden farklı** olduğunu **kimse
denetlemiyordu**.

Efsane bir glifi yalnızca üç şeyle çizer: **dolgu · halka · çarpı**.
Dolayısıyla şu kümeler efsanede **birebir aynıdır**:

| küme | çizim |
|---|---|
| `light` · `empty` · `lightAlt` · `seedCount` · `inHand` | boş daire |
| `dark` · `darkAlt` | dolu daire |
| `king` · `lightSpecial` | halkalı boş daire |
| `promoted` · `blindfolded` | gri daire |

Yeni denetim **beş diyagramda** kusur buldu — ve biri (`gonggi-toss`)
**Faz 3'ten beri basılıydı**.

> Bir sembolün çizilmesi, **okunabilir** olduğu anlamına gelmez. Faz 4
> font bağımlılığını kaldırdı; Faz 5 aynı cümlenin ikinci yarısını yazdı.

---

## 10 · SAYFA MODELİ

| | Faz 4 (22) | koşu 1 (20) | **koşu 2 (23)** |
|---|---:|---:|---:|
| Kelime / sayfa | 447 | 444 | **447** |
| Kelime / oyun | 686 | 682 | **700** |
| Ölçülen sayfa/oyun | 1,53 | 1,54 | **1,57** |
| Faturalanan sayfa/oyun | 2,09 | 2,10 | **2,09** |
| **Taşma oranı** | 1/22 | 1/20 | **1/23** |
| **Toplam** | **258** | **260** | **258** |
| **Sapma** | +%0,8 | +%1,6 | **+%0,8** ✅ |
| Sürücü | both | both | **both** |

### 10.1 Model bir ara +%10,9'a fırladı ve düzeltildi

İlk yazımda üç madde birden çift sayfayı aştı ve model **284 sayfaya
(+%10,9)** çıktı — bandın (±%6) ve roadmap'in 272 sayfa tavanının
dışında. Sebep iki gerçek kusurdu ve ikisi de **benim yazımımdaydı**:

| kusur | ölçüm | düzeltme |
|---|---|---|
| **shogi 1045 kelime** — 480–900 bandının dışında | 415 mm metin | 926 kelimeye indirildi |
| pachisi + cats-cradle diyagramları çift sayfayı aşıyordu | 115,5 + 346,5 mm | § 8.1'deki görsel düzeltmeler |

Düzeltme sonrası **258 sayfa · +%0,8 · taşma 1/23**.

**Shogi 926 kelimede bırakıldı** ve bu bilinçli bir karardır: sekiz ayrı
taş hareketi olan bir kural seti 900 kelimeye ancak kural budayarak
sığar, ve kurucunun § 14 talimatı açıktır — *"Do not chase a fixed word
count at the expense of clarity."* Madde **çift sayfasına sığıyor**
(1,98), yani bandın koruduğu şey korunmuş durumda.

---

## 11 · EKONOMİK MODEL

| sürüm | Faz 4 | koşu 1 (260 s.) | **koşu 2 (258 s.)** |
|---|---:|---:|---:|
| Ciltli telif | 10,96 $ | 10,92 $ | **10,96 $** |
| **Ciltsiz telif** | **8,41 $** | 8,37 $ | **8,41 $** |
| Kindle telif | 7,19 $ | 7,19 $ | **7,19 $** |
| Başabaş ACOS (ciltli) | %31,3 | %31,2 | **%31,3** |

Sayfa modeli ile ekonomi **senkron**: `calibrate_pages --check` config'in
ölçümden kaymasını her koşuda denetliyor (koşu 1'de eklendi).

---

## 12 · KAPSAM KİLİDİ KORUMASI

Koşu 1'in bütün düzeltmeleri **yürürlükte**:

| koruma | durum |
|---|---|
| şerh varken kilit özeti **denetleniyor** | ✅ |
| model ↔ kilit ayrışması **şerhle açıklanmak zorunda** | ✅ |
| kapsamdan çıkarılan oyun manuscript'te **kalamaz** | ✅ |
| yinelenen oyun | ✅ kırmızı |
| çıkarılan oyunun geri sızması | ✅ kırmızı |

### 12.1 Şerh bir muafiyet değildir

`validate_scope.py` eskiden `have == want or amendments` diyordu: **bir
tane** şerh, sha256 denetimini **ömür boyu** kapatıyordu. Faz 5'in kendi
kapsam değişikliği o deliği açacaktı. Artık şerh, özetin **neden**
değiştiğini açıklar; **denetlenmemesini** sağlamaz.

---

## 13 · OYNANABİLİRLİK

| | |
|---|---:|
| Yazılmış madde | **23** |
| Beş öğesi tam (kurulum · ilk hamle · hamleler · hedef · bitiş) | **23/23** ✅ |
| Üç sorusu cevaplı (berabere · kilit · kural dışı) | **23/23** ✅ |
| Yedi başlıkta doğrulama kaydı | **23/23** ✅ |
| **Dış insan testi** | **0** ⛔ |
| `locked` madde | **0** |

Üç yeni maddenin editoryal tamamlamaları **adlandırılarak** beyan edildi:
shogi'nin tekrar/kilit/düşürme kısıtları ve pachisi'nin iki kişilik bitiş
kuralı, prozada *"editorial ruling"* diye işaretli.

---

## 14 · DIŞ TEST DURUMU

### EXTERNAL PLAYTEST: **NOT PERFORMED**

| | |
|---|---:|
| Dış (insan) oynanabilirlik testi | **0** |
| Test kaydı | **0** |
| `locked` oyun | **0** |
| Uydurulmuş testçi / süre / puan / ebeveyn raporu | **0** |

```
PRODUCTION        : AUTHORIZED   (A10 Founder Override)
FORMAL VALIDATION : PENDING
```

`01_SOURCE/playtests/` **hâlâ boştur**. A10 üretimi **durdurmamak**
demektir; **kanıt uydurmak** demek değildir. `qa_manuscript.py § ⑤` kaydı
olmayan bir `locked` maddeyi mekanik olarak reddediyor.

---

## 15 · ARKA MADDE

Altı bölüm **tam ve güncel** — yeni üç oyunla birlikte **yeniden
üretildi**, elle düzenlenmedi.

| # | bölüm | koşu 1 | **koşu 2** |
|---|---|---:|---:|
| ① | Tahta şablonları | 18 | **19** |
| ② | Malzeme rehberi | 85 | **85** |
| ③ | Sözlük | 61 | **61** (28'i prozada geçiyor) |
| ④ | Kaynakça | 100 | **100** (24'ü sayfa-doğrulanmış) |
| ⑤ | **Üç indeks** | 100 oyun | **100 oyun** |
| ⑥ | Uydurulmuş gelenekler | 5 | **5** |

**Sayfa göndermeleri:** 23/100 oyun **ölçüldü**; 77'si
`awaiting-typesetting` taşıyor. **Uydurulmuş sayfa numarası: 0.**

`qa_index.py` 31 denetim koşuyor ve kovaları **üreteçten almaz**,
envanterden **yeniden hesaplar**.

---

## 16 · MANUSCRIPT KORUMASI VE DİL

| | |
|---|---:|
| Takip edilen manuscript dosyası | **0** |
| Takip edilen arka madde | **0** (yalnızca public özet) |
| Ticari katmanda Türkçe | **0** |
| `translatedFrom` dolu ticari kayıt | **0** |
| `qa_language_split.py` | ✅ 13 denetim yeşil |

Koşu 1'de dil kapısı **iki gerçek sızıntı** yakaladı (arka madde üreteci
envanterin Türkçe `substitutionHint` ve `locator` alanlarını ticari
katmana taşıyordu). Kapı **zayıflatılmadı**, üreteç düzeltildi: 86
terimlik ticari İngilizce eşleme, ve **eşlenmemiş bir ipucunda üreteç
çöküyor**.

---

## 17 · CI VE GİT

| | |
|---|---|
| Dal | `faz/5-uretim` (koşu 1: `faz/5-yakinsama`, merge edildi) |
| CI | ✅ **YEŞİL** |
| Açık gereksiz PR | **yok** |
| `.gate` | **`phase1`** — yükseltilmedi |

### 17.1 Etiket düzeltmesi KORUNUYOR

`v0.5.0`, `v0.4.0` ve `v0.3.0` **hiç var olmamıştır**
(`git ls-remote --tags origin` boş döner). Faz raporları kilometre taşını
*yazıyordu*; **etiket yazmakla oluşmaz.**

### 17.2 Koşu 1'de CI bir kez KIRMIZI yandı

Sebep koşu 1'in **kendi eklediği** bayatlık denetimiydi: korumalı katman
CI'da görünmediği için her tanımı "hayalet" sayıyordu. Düzeltildi
(manuscript yereldeyse tam, CI'da boş koşar) ve **merge CI yeşile dönene
kadar yapılmadı**.

---

## 18 · RESMÎ KAPI

```
.gate = phase1
```

**Yükseltilmedi ve yükseltilmeyecek.** Roadmap'in kapıları 100 oyun ve
100 oynanabilirlik testi ister; yazılan **23**, geçen test **0**.

> **PRODUCTION ≠ FORMAL VALIDATION.** Üretim ilerledi; kapı ilerlemedi.

---

## 19 · KALAN BLOKLAYICILAR

| # | blok | kimde | durum |
|---|---|---|---|
| 1 | **75 oyun yazılmadı** | üretim + kaynak | ⛔ **ana blok** |
| 2 | **Dış insan testi** | kurucu — paket hazır | ⛔ Faz 2'den beri aynı |
| 3 | Telifli kaynak erişimi (Parlett · Bell · Murray · Zaslavsky) | kurucu | 5 oyun P4 + kuyruğun büyük kısmı |
| 4 | **Diyagram dili v1.5 — ip figürleri** | kurucu | 🆕 açık karar (§ 7.2) |
| 5 | **Hücre-maskeli (haç) tahta notasyonu** | kurucu | 🆕 açık karar (§ 8.1) |
| 6 | lagori · kho-kho kaynak kaydı | araştırma | P6 |
| 7 | ~~cats-cradle 150 mm çatışması~~ | — | ✅ **ÇÖZÜLDÜ (K24)** |
| **A4** | Büyük punto sürümü | kurucu | açık |
| **A5** | `STYLE.md` onayı | kurucu | açık |
| **A6** | Yazar biyografisi | kurucu | açık |

### 19.1 Kalan 75 oyunun gerçek engeli

Faz 5 on kaynak açtı ve **yedisi kural taşımıyordu**. Bu küçük bir
örneklemdir ama deseni nettir:

- Kuyruğun **P2'sindeki 64 oyunun** çoğu **telifli** eserlere (Parlett,
  Bell, Murray, Zaslavsky) künyelidir — yani "erişilebilir" etiketi
  **künyenin varlığını** anlatır, **kaynağın açılabilirliğini** değil.
- Elde bulunan kamusal alan derlemeleri (Culin, Gomme, Fiske, Jayne,
  Smith) belirli kültürleri derinlemesine, ötekileri **hiç** kapsar.

> Bu yüzden kalan iş bir **yazım** işi değil, önce bir **kaynak edinme**
> işidir. Kurucunun kütüphane erişimi, üretim hızını belirleyen tek
> değişkendir.

---

## 20 · FAZ 6 HAZIRLIĞI

**Faz 6'ya GEÇİLMEDİ ve geçilmeyecek.**

| hazır | değil |
|---|---|
| Kapsam kilitli · şerhli · denetlenen (100 · 73 kültür) | **75 oyun yazılmadı** |
| Arka madde tam ve **üretilen** · üç indeks doğrulanmış | **Dış test kanıtı (0)** |
| Kalibre sayfa modeli (258 · +%0,8) ve senkron ekonomi | `locked` oyun (0) |
| K24 istisnası kayıtlı, dar ve **dört testle kilitli** | Ön madde ve giriş denemesi |
| 177 kasıtlı kusur testi · yedi kapı kusuru kapatıldı | ~130 görsel |
| Erişilebilir-önce kuyruk · altı seviye | Telifli kaynak erişimi |
| Yazım şablonu 25 oyunda sınandı | **Diyagram dili v1.5 kararı** |

---

## 21 · BU FAZIN KENDİ HAKKINDA BİLMEDİĞİ

| bilinmeyen | ne zaman öğrenilir |
|---|---|
| Yirmi beş madde masada çalışıyor mu | **dış test** — açık |
| Kalan 75'in kaçı gerçekten yazılabilir | Faz 5 on iki kaynaktan beşini yazabildi |
| Taşma oranı %4–5'te kalıyor mu | daha büyük örneklem |
| İp figürleri çizilebilir mi | diyagram dili v1.5 kararı |
| Haç tahtası çizilebilir mi | aynı karar |
| Kaç oyun daha "Kore cildinden Çin oyunu" tuzağı taşıyor | sıraya geldikçe |

**En rahatsız edici satır ikincisidir.** Faz 5 on kaynak açtı ve üç madde
yazdı. Eğer bu oran devam ederse, kuyruğun "erişilebilir" saydığı 92
oyunun önemli bir bölümü **kural taşımayan kaynaklara** bağlıdır ve
kitabın gerçek üretim kapasitesi kuyruğun gösterdiğinden **düşüktür**.

> Faz 3 engeli **abarttı**, Faz 4 **küçümsedi**, Faz 5 engelin **türünü**
> yanlış bildiğimizi buldu — ve koşu 2'de bunu **ölçtü**.

---

**⛔ FAZ 6 BAŞLAMADI.** `.gate` = `phase1`. KDP'ye dokunulmadı. Prova
sipariş edilmedi. Ajan durdu.
