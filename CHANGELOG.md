# CHANGELOG — The Great Book of World Games

Bu dosya **ne zaman ne değişti ve neden** sorusunu yanıtlar.
Her faz kendi girdisini ekler. Format: ters kronolojik.

---

## [0.5.8] — 2026-08-19 · FAZ 5 · BATCH 7 — KURUCU TESLİMİ ALINDI

**Yazılan: 7 oyun** (manuscript **41 → 48**).

| oyun | aile | kültür | kaynak |
|---|---|---|---|
| **Oware** | ekim | Akan | Murray ss.181–182 · Bell ss.116–117 |
| **Pallanguzhi** | ekim | Tamil | Bell ss.115–116 |
| **Dara** | çizgi-toprak | Dakarkari | Bell ss.95–96 |
| **Mū Tōrere** | çizgi-toprak | Māori | Murray s.93 |
| **Catch the Hare** | av-kuşatma | Kastilya | Murray s.99 (Alfonso X) |
| **Hasami Shogi** | savaş tahtası | Japon | Bell s.97 |
| **Li'b el-Merafib** | eve dönüş | Sudan Arabı | Bell ss.12–14 |

**Ekim ailesi 2 → 4.** Kitabın en büyük açığı açılmaya başladı.

### Teslim: altı dosya, üçü kullanılabilir

`Murray 1952` ✅ · `Bell` ✅ · `Parlett 1999` ⚠ kısmi tarama (açtığı
oyun **sıfır**) · `Africa Counts` ⛔ **1.5 KB'lık PHP hata sayfası** ·
`"Russ 2000"` ⛔ **yapay zekâ sohbet çıktısı** · `ERIC zip` ◻ ilgisiz.

Adı hiçbir şey söylemeyen dosya (`B-001-002-771.pdf`) teslimin **en iyi
kaynağı** çıktı: Bell'in *Board and Table Games*'i. Dosya adı ne olumlu
ne olumsuz bir kanıttır. **Karar K31.**

`"Russ"` dosyası beş oyunun kurallarını iddia ediyor ve **makul
görünüyor** — tehlikesi budur. Sıfır birebir pasaj, sıfır sayfa, 34
asistan alıntı işareti. `SOURCING_STANDARD § 2` uyarınca **kullanılmadı**;
`pallanguzhi` ve `omweso` zaten onsuz açıldı.

### Sayfa açmak üç maddeyi DURDURDU

`konane` → Murray'in bölümü *"WAR-GAMES OF WHICH WE HAVE NO CERTAIN
KNOWLEDGE"* başlığı altında ve kuralın kurtarılamaz olduğunu söylüyor →
**FINAL SOURCE BLOCKED**. `bagh-chal` → Murray'in dört kaplan-keçi
maddesi de **Hindistan**, kapsam **Nepalli** der. `game-of-the-goose` →
Bell'in kuralları **1725 İngiliz levhasından**, kapsam **İtalyan** der.
Üçü de yazılabilirdi ve üçü de yanlış olurdu.

### Görsel denetim, sayısal kapının geçirdiği ALTI kusur buldu

En ciddisi: `track` sınıfının render kodu `size.stations` alanını
**okumuyor** ve yut-nori devresini **sabit** çiziyor. `li'b el-merafib`in
sarmalı 54,0 × 76,5 mm ölçüldü, bütçeden geçti — ve basılacak olan şey
**Kore yut tahtasıydı**. Diyagram **geri çekildi**; madde diyagramsız
basıldı. **Karar K32.**

Öteki beşi: `markers` alanı tahtaya hiç çizilmiyor (dört diyagram
olmayan bir sembol vaat ediyordu) · `dara` **dörtlü** okunuyordu ·
`hasami` taşı iki kez çiziyordu · `hasami` panel sayısı yanlıştı · üç
efsane **kırpılıyordu**. Hepsi düzeltildi ve gözle doğrulandı.

### Dürüstlük kayıtları

`oware` iki künye taşır ama **bir** bağımsız kaynağı vardır: ikisi de
Rattray 1927'den türer (§ 3) → `locked` **olamaz**.
Bell'in sayfa kayması **değişkendir** (pdf−31 … pdf−36); bütün Bell
künyeleri sayfa **üst satırından** okundu, aritmetikle türetilmedi.

### Ölçüm

254 sayfa (−%0,8) · 48 madde · 34 929 kelime · 728 kelime/oyun ·
44 diyagram · 46 `verified` kaynak kaydı · uydurulmuş sayfa **0**.
`project_config` sampleSize 41 → 48 senkronlandı.

**Boşluk kaydı 52 → 45.** Eksik iki eser (Zaslavsky · Russ) **dokuz
oyun** açar.

**FINAL VERIFIED SCOPE = 48 / 100.** Kapsam değişikliği **yapılmadı**:
eksik olan aday kalitesi değil **kaynak arzıdır** (§ 16 gerekçesi
raporda).

**Rapor:** `06_REPORTS/FINAL_WRITING_COMPLETION_REPORT.md` ·
`06_REPORTS/FOUNDER_DELIVERY_INTAKE_REPORT.md`
**Kararlar:** K31 · K32.

---

## [0.5.7] — 2026-08-18 · FAZ 5 · KURUCU ARAŞTIRMA BOŞLUK KAYDI

**Yazılan oyun: 0.** Bu bir üretim değil bir **ölçüm** teslimidir:
kurucunun § 3 direktifi, yazılamayan her oyunun **neden** yazılamadığını
ve kurucunun **tam olarak neyi** araması gerektiğini tek bir yetkili
kayda toplamayı istedi.

### Ölçüm — 59 değil, 52

| | |
|---|---:|
| Kapsam | 100 |
| Yazılmış | 41 |
| **Kurucu müdahalesi OLMADAN yazılabilir** | **7** |
| **Kurucu araştırması GEREKEN** | **52** |

Batch 6 raporu *"kalan 59 oyunun 52'sinin kaynağı erişilemez"* diyordu.
Bu doğruydu ama **eksikti**: kurucuya hangi yedisinin kendi müdahalesini
gerektirmediğini söylemiyordu. Yedi oyun (`gilli-danda` · `chaupar` ·
`tabula` · `nine-holes` · `alquerque` · `tuknanavuhpi` ·
`ludus-latrunculorum`) elde bulunan derlemelerde **gerçek isabete**
sahiptir ve kurucu beklemeden yazılır. Onları engelli listesinde
göstermek, kurucuyu **gereksiz** bir araştırmaya göndermekti.

### İki eksen — karıştırılmıyor

`status` kaynak avının **kanıt** durumudur (`BLOCKED` 34 ·
`SOURCE-PENDING` 16 · `UNRESOLVED` 2); `primaryBlocker` oyunun
**yazılamama sebebidir** (`P1`…`P10`). Denenmemiş bir kaynağa *engelli*
demek Faz 3'ün hatasıydı; 59 maddeyi tek bir duvar olarak sunmak Faz
5'in riskiydi. **İkisi de yapılmadı.**

`UNATTEMPTED` **sıfırdır** ve bu ölçülmüştür: Batch 6'da kalan 59 oyunun
tamamı elde bulunan on kamusal alan derlemesine karşı tarandı.

### En önemli tek bulgu — 52 araştırma değil, 5 kitap

**Murray 1952 tek başına 24 madde açar.** Parlett 1999 · Zaslavsky 1973 ·
Bell 1960–69 · Russ 2000 eklenirse **46/52**. Kayıt bu yüzden **iki
biçimde** basıldı: oyun oyun (kayıt) ve **kaynak kaynak** (paket) —
çünkü kütüphaneye bir oyun için değil bir **kitap** için gidilir.

Kalan altısı (`ephedrismos` · `kho-kho` · `lagori` · `mu-torere` ·
`myinda` · `gebeta`) ayrı ayrı avlanmak zorundadır.

### Ne kaybediliyor — ölçüldü

Çözülmezse kitap **38 kültür** ve **dokuz bölge** kaybeder (Oceania ·
Central Asia · Iberia · Horn of Africa · South America · Central
Europe · Southern Europe · North-East Africa · Anatolia). Ekim ailesi
14 hedefinde **2**'de kalır.

### Yeni dosyalar

| dosya | ne |
|---|---|
| `06_REPORTS/FOUNDER_RESEARCH_GAP_REGISTER.md` | oyun oyun · § 6'nın on beş alanı |
| `06_REPORTS/FOUNDER_RESEARCH_PACK.md` | kaynak kaynak · insan araştırmacı için |
| `01_SOURCE/founder_research_gap_register.json` | makine okunur |
| `04_BUILD/build_gap_register.py` | üretir + `--check` |
| `04_BUILD/founder_delivery_ingest.py` | teslim alır · hash'ler · künye denetler |
| `06_FOUNDER_DELIVERY/` | teslim dizini — **ham teslim `.gitignore`da** |

### Yeni kapılar — ikisi de CI'da

`build_gap_register --check` bir **örtüşme** denetimi yapar:
kapsam = yazılmış + yazılabilir + engelli. Bir oyun **yazıldığı hâlde**
kayıttan düşmezse CI kırmızı yanar — yani kurucu **çözülmüş** bir engeli
araştırmaya gönderilmez. Kayıt manuscript'e **bakmadan** üretilir
(yazılmış küme kapsamdan türetilir) ama manuscript **eldeyse** türetim
onunla karşılaştırılır.

`founder_delivery_ingest --check` teslim yoksa **boş koşar** (§ 17).

Kapılar **kanıtlandı**: `selftest` § ⑩ yedi kasıtlı kusur sınar ve
yedisi de kırmızı yanar (**185 → 192** denetim). Aralarında en sinsisi
*"kayıtta olmayan gameId ile teslim klasörü"*: yanlış yazılmış bir
klasör adı, kurucunun bulduğu kaynağın **sessizce buharlaşmasıdır**.

### Aşılan ve düzeltilen kayıtlar

- `06_REPORTS/LIBRARIAN_REQUEST_LIST.md` **aşılmış** olarak işaretlendi:
  iki sayısı da yanlıştı (71 → 59; şans ailesi listesi K28 öncesiydi).
  **Silinmedi** — K28 yolunun tarihidir.
- `01_SOURCE/source_access_pending.json` bir **durum notu** aldı:
  beş engelli kaydın dördü (`mbube-mbube` · `astragaloi` ·
  `bao-la-kiswahili` · `royal-game-of-ur`) kütüphaneci teslimiyle
  çözülmüştü ve dosya hâlâ *"deferred"* diyordu. Kayıt dizilerine
  **dokunulmadı** (§ 23: engelli-oyun tarihi silinmez).

**Karar:** K30.

---

## [0.5.1] — 2026-08-14 · FAZ 5 · ÜRETİM — K24 istisnası ve üç oyun

**Yazılan: 3 oyun** (manuscript **20 → 23**).

| oyun | aile | kültür | kaynak |
|---|---|---|---|
| **Cat's Cradle** | tahtasız | İngiliz | Jayne 1906, ss. 324–338 |
| **Shogi** | savaş tahtası | Japon | Culin 1895, ss. 90–91 |
| **Pachisi** | eve dönüş | Hindustani | Culin 1898, ss. 851–854 |

**Karar K24 — CATS-CRADLE DİYAGRAM İSTİSNASI.** Kurucu 150 mm tavanının
**yalnızca** cats-cradle için aşılmasını onayladı. Genel tavan
**değişmedi**. Biçim bir *muafiyet bayrağı* değil bir **kimlik
eşlemesidir** (`overrides.get(gameId, 150)`) ve dört kasıtlı kusur testiyle
kilitlidir — özellikle *"sözlüğe ikinci bir oyun eklemek"* kırmızı yanar,
çünkü bir istisna listesi tavanı bir **öneriye** dönüştürür.

⚠ **İSTİSNA ŞU AN KULLANILMIYOR** (cats-cradle 107 mm < 150 mm). Bağlayıcı
kısıt milimetre değil **notasyon** çıktı: v1.4 `bodily/hands` çerçevesi ip
figürlerini **çizemiyor** ve üç özdeş şema basmak istisnayı tüketirdi ama
okunabilirliği artırmazdı. **Açık karar:** diyagram dili v1.5.

**GÖRSEL DENETİM ÜÇ GERÇEK KUSUR BULDU** (ölçüm sayıları temizdi):
pachisi tahtası **haç değil ızgara** çiziliyordu (§17 ihlali — diyagram
kaldırıldı); shogi'de yirmi taşın hepsi **aynı** çiziliyordu ve okur
kurulumu yapamazdı; cats-cradle efsanesinde iki sembol **birebir aynı**
daireydi.

**YENİ KAPI: efsanede ayırt edilemeyen sembol.** Faz 4 sembolün
*çizilmesini* sağlamıştı; **farklı** olduğunu kimse denetlemiyordu.
`light`/`empty`/`lightAlt` ve `king`/`lightSpecial` efsanede aynıdır. Kapı
beş diyagramda kusur buldu — biri (`gonggi-toss`) **Faz 3'ten beri
basılıydı**.

**YEDİ OYUN AÇILDI VE YAZILAMADI** — hepsi sayfa seviyesinde gerekçeli:
hnefatafl · halatafl (Fiske: kural yok) · oware (Şam/Vei kaydı) · jianzi
(nesne, kural değil) · **xiangqi** ve **tien-gow** (Culin'in cildi KORE
oyunlarıdır) · patolli (Durán'ın resmi) · gomoku (amaç var, kural yok) ·
**go** (kaynak TAM ama **Japon** kodifikasyonu; kapsam **Han Çinlisi** der
— §9 kültür şartı karşılanmıyor).

**KENDİ YAZIMIMDA İKİ KUSUR:** shogi **1045 kelimeyle** 480–900 bandını
aştı ve üç madde birden çift sayfayı aşınca model **284 sayfaya (+%10,9)**
fırladı — bandın ve roadmap'in 272 tavanının dışında. Trim + görsel
düzeltme sonrası **258 sayfa · +%0,8 · taşma 1/23**. Shogi 926'da bırakıldı
(§14: kelime sayısı için kural budanmaz) ve çift sayfasına sığıyor.

Arka madde **yeniden üretildi** (19 şablon · 23 ölçülmüş sayfa göndermesi).
Doğrulama kaydı **44 → 51**. Selftest **172 → 177**. CI **yeşil**.
`.gate` = `phase1` — **yükseltilmedi**. **Dış insan testi: 0.**

---

## [0.5.0] — 2026-08-14 · FAZ 5 · Kapsam değişikliği, arka madde, altı kapı kusuru

**Yazılan oyun: 0.** Manuscript **22 → 20**, çünkü K23 iki *yazılmış*
maddeyi kapsamdan çıkardı. **Faz 5 kendi ana hedefini (100 oyun)
tutturamadı** ve rapor bunu ilk satırında söylüyor.

**KAPSAM DEĞİŞİKLİĞİ — K23** (`scope_lock.json § amendments[0]`)

| çıkarılan | eklenen |
|---|---|
| **Fivestones** · İngiliz · `distinct 2` | **Lagori** · Kannada |
| **Marbles** · İngiliz · `distinct 3` | **Kho-Kho** · Marathi |

Ölçülen etki: kitap kültürü **71 → 73** · tahtasız aile kültürü
**11 → 13** · tahtasız İngiliz madde **5 → 3** · aile hedefleri
**değişmedi** · yedek havuz **19** (çıkanlar geri döndü). Gonggi/Fivestones
mekanik çakışması **çözüldü**. Geri alınan prozalar silinmedi
(`02_MANUSCRIPT/retired_phase5.json`).

**ARKA MADDE — Faz 4'ün yazmadığı iş tamamlandı.** Altı bölüm, hepsi
canonical veriden **üretiliyor**: 18 tahta şablonu · 85 malzeme satırı ·
**61 terimlik sözlük** · 100 maddelik kaynakça · **üç indeks**
(73 kültür / oyuncu sayısı / süre-yaş) · 5 uydurulmuş gelenek düzeltmesi.
Yeni kapı `qa_index.py` (31 denetim). **Sayfa numarası uydurulmuyor:**
20/100 oyun ölçüldü, 80'i `awaiting-typesetting` taşıyor.

**ALTI KAPI KUSURU — altısı da gerçek veriyle YEŞİL koşuyordu:**

1. **Şerh, kilit özetini ömür boyu devre dışı bırakıyordu** — bir tane
   `amendments[]` girdisi sha256 denetimini sonsuza kadar kapatıyordu.
2. **"Model ayrışırsa kapı ısırır" vaadinin kapısı YOKTU** — dosyanın
   kendi başlığı iddia ediyordu, öyle bir denetim hiç yazılmamıştı.
3. **Kapsamdan çıkarılan oyun basılmaya devam edebiliyordu** —
   `qa_manuscript.py` manuscript'i kapsam kilidiyle hiç karşılaştırmıyordu.
4. **Dizgi ölçümü manuscript altından değişince bayat kalıyordu** —
   22 oyunluk eski ölçüm "tutarlı" ilan ediliyordu.
5. **Kalibre config ölçümden kayınca ekonomi eski sayıyla hesaplanıyordu**
   — ölçüm 260 dedi, config 258 dedi, telif eski sayıdan çıktı.
6. **Emekliye ayrılan diyagram 150 mm bütçesinde sayılmaya devam
   ediyordu** — denetim tek yönlüydü.

Ayrıca: `validate_research.py`'nin gömülü doğrulama-seviyesi listesi
config'le birleştirildi; **`validate_scope.py`'nin `--root` sözleşmesi
yoktu** ve kapsam kilidine yazılmış kasıtlı kusur testleri kapı ısırdığı
için değil *argparse hatası verdiği için* geçiyordu.

**BEŞ OYUNUN KAYNAĞI SAYFA SEVİYESİNDE AÇILDI — beşi de yazılamaz:**
hnefatafl · halatafl (Fiske 1905: kaynak erişilebilir, **kural yok**) ·
cats-cradle (Jayne 1906: **kural tam**, engel **editoryal** — 150 mm) ·
oware (Culin 1896: **kimlik tuzağı** — Şam ve Vei kayıtları, Akan değil) ·
jianzi (Culin 1895: nesne anlatılıyor, kural yok — Faz 4'ün kararı
**doğrulandı**).

**YENİ KUYRUK SEVİYESİ P6** — *"kaynak ARANDI, KAYIT BULUNAMADI"*.
P4'ten ayrıdır: P4 bir **erişim** engelidir (kayıt var, nüsha kapalı,
kütüphane kartı açar); P6 bir **varlık** sorunudur (kayıt henüz yok).
**Üçüncü tür: `editorialHolds`** — kaynağı tam olduğu hâlde kitabın kendi
üretim kuralı yüzünden yazılamayan madde (cats-cradle).

**DİL AYRIMI KAPISI İKİ GERÇEK SIZINTI YAKALADI** — arka madde üreteci
envanterin Türkçe `substitutionHint` ve `locator` alanlarını ticari
katmana taşıyordu. Kapı zayıflatılmadı; üreteç düzeltildi (86 terimlik
ticari İngilizce eşleme; eşlenmemiş ipucunda üreteç **çöküyor**).

**Sayfa modeli:** 258 → **260** (+%1,6 · bantta). Ciltsiz telif
8,41 → **8,37 $**, ciltli 10,96 → **10,92 $**. Sürücü yine **`both`** —
Faz 4'ün bulgusu ikinci örneklemde doğrulandı.

**Düzeltme:** `v0.4.0` ve `v0.3.0` etiketleri **hiç var olmamış**
(`git ls-remote --tags origin` boş). Faz raporları kilometre taşını
yazmıştı; etiket yazmakla oluşmaz.

**Selftest:** 148 → **172** denetim. **CI yeşil.** `.gate` = `phase1`
(yükseltilmedi). **Dış insan testi: 0 — değişmedi.**

---

## [0.4.0] — 2026-08-14 · FAZ 4 · Erişilebilir havuz, beş kapı kusuru, 258 sayfa

**Yazılan:** 11 oyun (manuscript 11 → **22**). Doğrulanmış künye 17 → **28**.

| Batch | Oyunlar |
|---|---|
| 1 · kalibrasyon | seega · tab · nine-mens-morris · fox-and-geese · fivestones · hopscotch · totolospi · set-dilth |
| 2 · tahtasız | jan-ken · conkers · marbles |

**Kararlar:** K21 (Faz 4 üretim istisnası — üretim ilerler, kapı ilerlemez)
· K22 (kuyruk bir SIRA kapısıdır: erişilebilir önce, engelli sona).

**Beş kapı kusuru bulundu ve düzeltildi:**

1. **150 mm bütçesi oyun başına tanımlı, diyagram başına denetleniyordu.**
   Tablut iki diyagramla 181,5 mm ediyor ve geçiyordu. Kapı düzeltildi;
   `tablut-capture` bir ayrıntıya daraltıldı (144,0 mm).
2. **Efsane sembolü bir font karakteriydi** ve font taşımayınca boş
   basılıyordu — tilki efsanede sembolsüzdü. Efsane artık çiziliyor.
3. **Alma çarpısı (×) hiçbir efsanede açıklanmıyordu** ve koyu taşta
   siyah üstüne siyah çiziliyordu. Üçü birden düzeltildi.
4. **`calibrate_pages.py` sonucu koda gömülü basıyordu.** Faz 2'nin
   cümlesi 22 oyunda yanlışlandı ama yine de basılıyordu. Artık türetiliyor.
5. **`fivestones` maddesinin kurulum bloğu yoktu** — yeni `qa_manuscript.py`
   kapısı ilk koşusunda buldu.

**Ölçüm:** sayfa modeli 268 → **258** (sapma +%4,7 → **+%0,8**). Taşma
%9 → **%4,5**. Kelime/sayfa 405 → **447**. Ciltsiz telif 8,24 → **8,41 $**.

**Kuyruk:** "engelli" gösterilen oyun **80 → 5**; erişilebilir **20 → 94**.
`royal-game-of-ur` engelli kuyruğa eklendi (Faz 3 verisinde eksikti).

**Çözülen:** Totolospi kural kimliği çelişkisi — Culin aynı adı iki farklı
oyun için kullanıyor ve bunu s. 796 dipnotunda kendisi söylüyor.

**Yeni kapı:** `04_BUILD/qa_manuscript.py` (7 denetim) ·
`04_BUILD/build_queue.py --check`. Diyagram dili **v1.4** (`bodily/bed`).
Selftest **126 → 148** denetim.

**Değişmeyen:** `.gate` = `phase1` · `locked` oyun 0 · dış test 0 ·
kapsam 100 oyun.

---


## [0.3.0] — 2026-08-13 · FAZ 3 · Üretim, erişilebilir kaynakla ölçek, sayfa düzeltmesi

> Faz 3 sekiz oyun yazdı ve **Faz 2'nin en önemli sayısının yanlış
> olduğunu kanıtladı.** İkincisi birincisinden değerlidir.

### SAYFA MODELİ DÜZELTİLDİ — 316 → 268
- örneklem **3 → 11 oyun**; taşma oranı **%33 → %9**
- sapma **+%23,4 → +%4,7** · **hedef bandına girdi**
- Faz 2'nin 316'sı tek bir aykırı değerin (tablut) eseriydi
- sapma şerhi KAPANDI; önerilen üç müdahalenin hiçbiri gerekmedi
- kelime hedefi **650'de kaldı**, kapsam 100'de kaldı
- ciltsiz telif 7,42 $ → **8,24 $**
- ⚠ Faz 2'nin "metin sabittir (fark 0,01)" iddiası da zayıfladı: 0,41

### ÜRETİM — 8 yeni oyun (manuscript 3 → 11)
Pong Hau K'i · Gonggi · Olinda Keliya · Nerenchi · Demala Diviyan Keliya ·
Awithlaknannai · Picaria · Zohn Ahl — hepsi **birinci elden** kaynaktan
(Culin 1895 · Culin 1907 · Parker 1909). Hiçbiri LOCKED değil.

### KARARLAR
- **K18** koşullu üretim şeridi: üretim yetkili, `.gate` `phase1` KALIR
- **K19** 150 mm diyagram bütçesi bağlayıcı, RENDER ölçümünden denetlenir
- **K20** erişilebilir ≠ güvenilir — Viktorya derlemesi tek başına kural taşıyamaz

### DİYAGRAM
- Cat's Cradle **182,5 → 111,5 mm** (efsane tekrarı + boş kenar payı)
- dil **v1.3**: `point` sınıfı düzensiz tahtaları taşır (nodes + edges)
- 16 diyagram render edildi, **hepsi ≤150 mm**, azami 111,5

### BULGULAR
- Falkener 1892 Faz 1'in Pachisi uyarısını **doğruladı**
- Culin, Zuni ve Tewa oyunlarını **İspanyol kökenli** sayıyor — atıf düzeltildi
- Zohn Ahl bir **kadın oyunudur** ve bu hikâyenin merkezinde
- totolospi ertelendi: kaynak, kaydın ailesinden başka bir oyun anlatıyor
- olinda-keliya'nın Faz 2'de "blocked" olan kural kaynağı **bulundu**
- tahtasız aile açılışı, listesinin taşımadığı bir yayılma iddiasındaydı → düzeltildi

### YAPILMAYANLAR
- **Dış oynanabilirlik testi: SIFIR.** Değişmedi.
- **`locked` oyun: 0.** Resmî kapı açılmadı.
- Yeniden kurgulanmış yeni oyun yazılmadı (erişilebilir kaynaklar geçersiz)

selftest 117 → **126**.

## [0.2.0] — 2026-08-13 · FAZ 2 · Pilot, sayfa doğrulaması, diyagram dili, dizgi

> Faz 2 bir üretim fazı değil bir **ölçüm** fazıdır. Ürettiği en değerli
> şey üç sayı ve üç hayırdır. **Faz KISMEN tamamdır** ve `.gate` `phase1`
> olarak kaldı: 12 `locked` oyun isteyen kapı, sıfır kilitli oyunla açılamaz.

### Kurucu kararları kapandı
- **K12 · A1** — manuscript public olmaz, iş durmaz; koruma güçlendirildi
- **K13 · A2** — av-kuşatma 14→10, savaş tahtası 13→17 (toplam 100)
- **K14 · A3** — nihai 100 oyun `scope_lock.json` içinde KİLİTLİ
- **K15 · A7** — dış testçi var; iç kanıt dış kanıtın yerine geçmez
- **K16** — ticari dil İngilizce, Türkçe yalnızca test malzemesi
- **K17** — sayfa doğrulaması bir etiket değil bir KAYITTIR

### Ölçülenler
- **kelime/sayfa 389** (Faz 1 hipotezi 320 · %18 düşüktü)
- **metin 1,37 sayfa/oyun ve SABİT** (oyunlar arası fark 0,01)
- **diyagram 0,45 sayfa/oyun ve DEĞİŞKEN** (fark 0,55)
- → **sayfa bütçesi bir KELİME bütçesi değil, bir DİYAGRAM bütçesidir**
- sayfa modeli 250 → **316** (+%23,4); hedef DEĞİŞTİRİLMEDİ, şerhle belgelendi
- birim telif her sürümde **1,12 $ düşüyor**

### Bulunan kusurlar
- **GERÇEK SIZINTI:** altı oyunun tam İngilizce kural metni public depodaydı.
  Faz 1 dedektörü göremezdi (etiket taşımıyordu). Korumalı katmana taşındı.
- Diyagram dili kendi genişlik sınırını aşıyordu → v1.1 (dikey panel)
- Dil kapısı tek Türkçe cümleyi kaçırıyordu → iki eşikli ölçüt
- `tablut`/`patolli` üç indeksten sessizce düşerdi → alanlar dolduruldu
- **selftest kendi regresyonumu yakaladı** (page_budget kalibre modu)

### Yeni kapılar
`validate_scope.py` · `qa_diagram.py` · `qa_playable.py` ·
`qa_language_split.py` · `calibrate_pages.py` · `render_diagrams.py`
Selftest **85 → 117** denetim. CI metin kapılarını artık **tarayarak**
koşuyor — elle liste tutmak bir körlük kaynağıydı.

### YAPILMAYANLAR — açıkça
- **Dış oynanabilirlik testi: SIFIR.** Paket hazır, oturum yapılmadı.
  Sahte kayıt üretilmedi.
- **Sayfa doğrulaması 2/12 tam.** Telifli monografilere erişilemedi.
- **Yazılan oyun: 3/12.** Dokuzunda kaynak kural metnini vermiyor; uydurulmadı.

## [0.1.0] — 2026-08-13 · Faz 1 · Envanter, tasnif ve oynanabilirlik mimarisi

Kitabın **veri omurgası** kuruldu. **Hiçbir proza yazılmadı.**

### Eklendi

- **`01_SOURCE/games/family-*.json`** — yedi aile parçası, **160 oyun
  kaydı**. Elle yazılır; indeks bunlardan üretilir
- **`01_SOURCE/game_index.json`** — birleştirilmiş envanter · **ÜRETİLİR**
- **`01_SOURCE/family_index.json`** — yedi mekanik aile; her biri tanım,
  giriş kuralı, dışlama kuralı ve **sınır kuralı** taşır. Ayrıca
  **deterministik tasnif yordamı**: sabit sıralı yedi soru
- **`00_CONTEXT/EDITORIAL_ARCHITECTURE.md`** — kitabın yapısı, iki sayfalık
  madde mimarisi, sayfa modeli, yedi görsel tipi, arka madde ve üç indeks,
  **sekiz ölçütlü aday seçim modeli**
- **`04_BUILD/build_index.py`** — parça → indeks; `--check` ile üretilen
  artefakt tutarlılığı
- **`04_BUILD/qa_taxonomy.py`** — aile tanımı, sınır, kısıt taraması, denge
- **`04_BUILD/qa_rules.py`** — kural bütünlüğü, netlik, durum tutarlılığı
- **`04_BUILD/validate_research.py`** — künye, yasaklı kaynak, bağımsızlık,
  araştırma → yazım kilidi
- **`04_BUILD/score_candidates.py`** — seçim modeli + **yeniden dengeleme
  önerisi**
- **`04_BUILD/page_budget.py`** · **`editions.py`** — sayfa ve telif modeli
- **`04_BUILD/update_docs.py`** — `BOOK_STATS.md` ve `ROADMAP_PROGRESS.md`
  artık **üretilir**; `--check` bayatlığı CI'da kırmızı yakar
- **JSON Schema doğrulayıcı** — `validate_spec.py` içinde, stdlib ile
  (karar K7). Desteklenmeyen şema anahtarı da ayrıca taranır
- **`05_TESTS/selftest.py` § ⑤** — Faz 1'in sekiz kapısının her biri
  kusurlu kurguyla sınanır. Toplam **83 denetim**
- **`06_REPORTS/PHASE_1_REPORT.md`** — faz raporu

### Değişti

- **`01_SOURCE/game.schema.json`** — aday seviyesi araştırma alanları:
  `taxonomyRationale` · `ruleCompleteness` · `clarity` · `playabilityStatus`
  · `reconstructionPlan` · `sourceVerification` · `sources[].lineage` ·
  `scores` · `visualNeeds` · güvenlik ve uyarlama alanları
- **`project_config.json`** — `production.pageModel` bloğu; Kindle telif
  oranı ve dosya boyutu hipotezi
- **`04_BUILD/qa_all.sh`** — envanter tazeliği **en başta** koşar
- **`.gate`** → `phase1`

### Ölçülen

153 aday · **119 uygun** · 89 kültür · 34 bölge · 7 aile ·
kısıt taraması **160/160** · 300 kaynak künyesi · sayfa modeli **250**
(hedef 256, −%2,3) · selftest **83 denetim yeşil**

### Bulgular

- **Kapsam bulgusu:** av ve kuşatma ailesinde yalnızca **10 uygun aday**
  var (hedef 14). Yeniden dengeleme **önerildi**, karar kurucuya bırakıldı
- **Şema iki kez kırıldı:** `gameId` kalıbı iki harfli "go"yu reddediyordu;
  `reconstructed` etiketi beyansız kurguya izin veriyordu
- **Pilot sekiz aşırı uzun kural adımı buldu** ve şablonu düzeltti
- **Otuz iki oyunun kuralı eksik ve TAMAMLANMADI** — dokuzunda kural hiç yok

### Kararlar

K9 (veri/proza sınırı mekaniktir) · K10 (beyansız yeniden kurgulama yok) ·
K11 (kaynak doğrulaması iki seviyeli)

### Durum

`.gate` = `phase1` · **Faz 1 PASS** · Faz 2 için A1 · A2 · A3 · **A7**
kapanmalı

---

## [0.0.1] — 2026-08-12 · Bootstrap

Proje altyapısı kuruldu. **Hiçbir kitap içeriği üretilmedi.**

### Eklendi

- **Dizin mimarisi** — 24 dizin, `00_CONTEXT` … `09_ARCHIVE` şemasına uygun,
  bu projeye özgü eklerle: `01_SOURCE/games`, `01_SOURCE/playtests`,
  `07_ASSETS/diagrams`
- **`project_config.json`** — makine okunur tek doğruluk kaynağı. Pazar
  raporunun sayıları `scope.locked: false` ile **hipotez** olarak işaretlendi
- **`THE_GREAT_BOOK_OF_WORLD_GAMES_IMPLEMENTATION_ROADMAP.md`** — altı faz,
  her fazda 19 alan: amaç, kapsam, teslimatlar, yazım hedefi, kelime/sayfa
  hedefi, araştırma, test altyapısı, QA kapıları, DoD, PASS, FAIL, ajan
  notları, kurucu bağımlılıkları, git kilometre taşı, CI, çıktılar, riskler,
  faz devri
- **`00_CONTEXT/PLAYABILITY_STANDARD.md`** — bu kitabın benzersiz başarısızlık
  biçimine (*oyun çalışmıyor*) karşı kurulan sözleşme: sekiz bloklu kural
  şablonu, üç zorunlu edge case, insan testçi kuralı
- **`00_CONTEXT/SOURCING_STANDARD.md`** — iki bağımsız kaynak kuralı ve
  dört durumlu kısıt taraması (`open` / `attributed` / `restricted` / `excluded`)
- **`00_CONTEXT/STYLE.md`** v1.0 — iki ayrı kayıt (anlatı / talimat),
  yasak kalıplar, belirsizliğin gizlenmemesi kuralı
- **`00_CONTEXT/LESSONS_FROM_CODEX.md`** — iki referans projeden taşınan
  yedi mekanizma ve altı ders; **kod taşınmadı, disiplin taşındı**
- **`01_SOURCE/game.schema.json`** — oyun kaydı şeması; `rules` ve
  `playtests` blokları `locked` durumu için zorunlu
- **Test altyapısı** — `validate_spec.py` (veri + kapsam + kapı),
  `validate_structure.py` (dosya + gömülü değer + sızıntı + sır),
  `selftest.py` (**kapıların kendi testi**, dört bölüm)
- **`04_BUILD/qa_all.sh`** — CI'ın birebir aynısı; Faz 1–5'te doğacak
  kapılar için satırlar şimdiden yazıldı (K18 dersi: ölü betik olmasın)
- **`.github/workflows/validate.yml`** — altı iş: gate · data · structure ·
  gates-selftest · text · production-model
- **`.gitignore`** — iki hatlı manuscript koruması

### Kararlar

K1 (ortak kütüphane yok) · K2 (`.gate`) · K3 (siyah-beyaz iç blok) ·
K4 (ciltli öncelikli) · K5 (kumar çerçevesi yok) · K6 (KU'ya girilmez) ·
K7 (kapılar üçüncü taraf paket kullanmaz) · K8 (kapsam sayıları hipotez)

### Açık kararlar

A1 (manuscript politikası · **Faz 1 başlamadan**) · A2 (aile taksonomisi) ·
A3 (100 oyun listesi) · A4 (büyük punto) · A5 (STYLE onayı) ·
A6 (yazar biyografisi) · A7 (**oyun testçileri · Faz 2 bloklayıcısı**)

### Durum

`.gate` = `phase0` · **Faz 1 BAŞLAMADI** · kurucu onayı bekleniyor

