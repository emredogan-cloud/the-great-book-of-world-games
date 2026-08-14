# DECISIONS — karar kaydı

> Bu dosya iki şey taşır:
>
> 1. **Alınmış kararlar** (`K##`) — gerekçesiyle, tarihiyle
> 2. **AÇIK KARARLAR** (`A#`) — kurucudan yanıt bekleyen sorular
>
> Kural: bir varsayım sessizce proje gerekliliğine dönüşemez. Pazar
> raporunun vermediği her şey **önce buraya** yazılır.

---

## AÇIK KARARLAR — kurucudan yanıt bekleyen

Durum tablosu · 13 Ağustos 2026 (Faz 2 girişi)

| # | Soru | Aciliyet | Ne zaman kapanmalı | Durum |
|---|---|---|---|---|
| ~~A1~~ | Manuscript public depoda mı duracak? | — | — | ✅ **KAPANDI · K12** — hayır; koruma güçlendirildi |
| ~~A2~~ | 7 aile taksonomisi + yeniden dengeleme | — | — | ✅ **KAPANDI · K13** — onaylandı; 10/17 kilitlendi |
| ~~A3~~ | 100 oyunun nihai listesi | — | — | ✅ **KAPANDI · K14** — `scope_lock.json` |
| ~~A7~~ | Oyun testçileri kim | — | — | ✅ **KAPANDI · K15** — dış testçi VAR |
| **A4** | Büyük punto sürümü v1.0'a girecek mi | DÜŞÜK | Faz 4 | AÇIK (bootstrap varsayımı: hayır) |
| **A5** | Kalibre edilmiş `STYLE.md` onayı | ORTA | **Faz 2 sonu** | AÇIK — v2.0 ölçümle yazıldı, onay bekliyor |
| **A6** | Yazar biyografisi metni | ORTA | Faz 5 | AÇIK |

Dört yüksek öncelikli karar Faz 2 girişinde kapandı. Kalan üçünün hiçbiri
Faz 2'yi bloklamaz.

---

## ALINMIŞ KARARLAR

### K1 · Ortak kütüphane YOK — üç proje tam izole

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

Üç yeni proje benzer şekilli araçlar kullanır. Yine de ortak bir Python
paketi oluşturulmadı ve her proje kendi kopyasını taşır.

**Gerekçe:** talimat § 31 bir ajanın tek klasörle çalışabilmesini şart
koşuyor. Ortak kütüphane bu kuralı ihlal eder: paylaşılan bir dosyadaki
değişiklik üç projeyi birden kırar ve bir projenin CI'ı başka bir deponun
durumuna bağlanır. **Kopyalanan kod biraz fazlalıktır; bağımlılık ise bir
kırılganlıktır.**

### K2 · Faz kapısı `.gate` dosyasından okunur

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

Kapı seviyesi tahmin edilmez. `qa_all.sh` ve CI aynı dosyayı okur.
`--fix` bayrağı kapıya **dokunmaz** (Bestiarium D3 dersi).

### K3 · İç blok siyah-beyaz

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

KDP premium renk büyük trimde sayfa başına **0,080 $**; 256 sayfa = 21,48 $
baskı maliyeti. 34,99 $ listede telif negatife düşer.

Renk KDP'de bir strateji değil bir **vergidir**. DK/Usborne ile aynı sahada
savaşmak KDP ekonomisiyle mümkün değildir. Cevabımız renk değil,
**gravür dili** — hem maliyet hem marka olarak.

### K4 · Ciltli öncelikli fiyatlama

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

Birim telif ciltlide 10,99 $, ciltsizde 8,44 $. Pazar raporu § 16'nın
bulgusu: reklamın hata payı doğrudan birim teliftir. Ciltli **lansmanla
birlikte** açılır, sonradan eklenmez — sonradan eklenen sürüm biriken
yorumları paylaşamaz.

### K5 · Kumar çerçevesi kullanılmaz

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

Bahis mekaniği taşıyan oyunlar **puanla yeniden yazılarak** girer.
Gerekçe editoryaldir, ahlaki değil: kitabın kanalları aile, okul ve
kütüphanedir ve kumar çerçevesi o üç kanalı birden kapatır.

Yeniden yazılan oyun `gamblingReframed: true` taşır ve prozada bunun
yapıldığı **açıkça** söylenir. Gizlenmez.

### K6 · KDP Select / KU'ya girilmez

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

256 sayfalık tam okuma ≈ 1,23 $ (KENP 0,00482 $ · Nisan 2026), ciltsiz
telif 8,44 $. Münhasırlık karşılığında satış başına **6,9 kat** kayıp.
KU yalnızca hızlı tüketilen seri kurgu için doğru kanaldır.

### K7 · Kalite kapıları üçüncü taraf paket kullanmaz

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

`validate.yml` saniyeler içinde biter. Yazım fazlarında günde onlarca push
olur ve iki dakikalık kurulum beklemek disiplini öldürür. Ağır bağımlılıklar
(Pillow, reportlab) yalnızca görsel ve dizgi işlerine aittir ve
`run_optional` sözleşmesiyle **atlanabilir**.

### K8 · Kapsam sayıları Faz 1'e kadar HİPOTEZDİR

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

Pazar raporunun 100 / 45 / 7 / 256 sayıları `project_config.json § scope`
içinde durur ve `locked: false` taşır. Faz 1 bunları **doğrular veya
değiştirir**. Bir sayıyı Faz 1'de düzeltmek ucuz; Faz 4'te düzeltmek üç
aylık iştir.

**Faz 1 sonucu:** 100 ✅ (119 uygun aday) · 45 ✅ (89 kültür) · 7 ✅ ·
256 ✅ (model 250, −%2,3). Dört sayı da doğrulandı. `scope.locked` **hâlâ
`false`** ve A2/A3 kapanana kadar öyle kalır.

---

### K9 · Veri katmanı public, proza katmanı özel — sınır MEKANİKTİR

**Tarih:** 13 Ağustos 2026 · **Faz:** 1

Faz 1, "manuscript public depoda durmaz" ilkesini bir ayrıma çevirdi:

| Katman | Nerede | Biçim | Depo |
|---|---|---|---|
| **Veri** | `01_SOURCE/` | alanlara bölünmüş kayıt | **public** |
| **Proza** | `02_MANUSCRIPT/` | sekiz sabit blokta sürekli metin | **özel** |

**Sınırı disiplin değil mekanizma çizer.** `validate_structure.py →
check_manuscript_leak()` proza şablonunun etiketlerini arar; takip edilen
bir dosya bunlardan ikisini birden taşırsa CI kırmızı yanar.

**Sonuç iki yönlüdür.** Veri katmanı proza etiketlerini taşıyamaz — bu,
kural kayıtlarının *data* kalmasını zorlar. Aynı zamanda araştırma
künyeleri, taksonomi ve ölçüm raporları public kalabilir; kitabın kaynak
iddiası denetlenebilir olur.

Bu karar A1'i **kapatmaz**, ama A1'in hangi seçenekle cevaplanırsa
cevaplansın mekanik olarak uygulanmasını sağlar.

---

### K10 · Yeniden kurgulama BEYAN EDİLMEDEN yapılamaz

**Tarih:** 13 Ağustos 2026 · **Faz:** 1

Şemanın ilk hâlinde `reconstructed` tek başına bir **etiketti**. Faz 1
pilotu şunu gösterdi: bir etiket, **uydurma ile yeniden kurgulama arasında
mekanik bir fark üretmez.** İkisi de aynı görünür.

Eklenen alan: **`reconstructionPlan`**. Netlik testinden düşen her
`reconstructed` kayıt üç şeyi yazmak zorundadır:

> **hangi boşluk** · **hangi kaynağa dayanarak** · **hangi editoryal kararla**

`qa_rules.py` bunu şart koşar ve planın yalnızca `reconstructed`
kayıtlarda durmasını da denetler (ölü kural yasağı). Sonuç: yeniden
kurgulama **kayıt tutmadan yapılamaz**.

Bu, `STYLE.md § 5`'in ("belirsizlik gizlenmez, yazılır") mekanik
karşılığıdır.

---

### K11 · Kaynak doğrulaması iki seviyelidir

**Tarih:** 13 Ağustos 2026 · **Faz:** 1

Bir eserin adını yazmak, o eseri açıp sayfayı görmekle **aynı şey
değildir**. Faz 1 künye seviyesinde çalıştı ve bunu gizlemek yerine bir
alana bağladı:

| Seviye | Anlamı | Nerede zorunlu |
|---|---|---|
| `bibliographic` | Eser ve içerdiği oyun künyelendi | Faz 1 · aday |
| `page-verified` | Kaynak açıldı, sayfa/locator doğrulandı | **`locked` kapısı** |

`validate_research.py` `locked` bir oyun için `page-verified` ve her
künyede bir `locator` şart koşar. **Doğrulanmamış bir künyenin doğrulanmış
gibi görünmesi mekanik olarak imkânsızdır.**

Aynı betik bağımsızlık sayımını da yapar: aynı yazarın iki eseri **bir**
kaynaktır, ve `lineage` alanı taşıyan türetilmiş bir kaynak bağımsız
sayılmaz.

---

### K12 · A1 KAPANDI — manuscript public olmaz, iş durmaz

**Tarih:** 13 Ağustos 2026 · **Faz:** 2 · **Karar:** kurucu

Kurucu §25'te şıkkı seçti: **DEVAM ET + MANUSCRIPT'İ KORU.** Bu, K9'un
kurduğu (a) hattının onayıdır: depo public kalır, proza depo dışında yaşar.

**Faz 2'nin eklediği şey bir politika değil, bir mekanizma güçlendirmesidir.**
K9'un sızıntı dedektörü yalnızca **beş yapısal etikete** bakıyordu
(`Setup:`, `Turn sequence:`, `Win condition:`, `On your turn,`,
`The game ends when`). Bu yeterli değildi ve gerekçesi tek cümledir:

> **Etiketleri silmek, prozayı silmez.**

Etiketsiz yazılmış bir kural metni — "Place the board between you. Each
player takes twelve seeds…" — beş etiketin hiçbirini taşımaz ve eski
dedektörden **temiz geçerdi**. Faz 2 bu deliği dört hatla kapattı:

| Hat | Ne arar | Neden gerekli |
|---|---|---|
| `structural-marker` | sekiz bloğun etiketleri | K9'un mevcut hattı |
| `content-signature` | ikinci tekil talimat dili + oyun terimleri | etiketler silinse de proza kalır |
| `density` | bir dosyadaki kural cümlesi **yoğunluğu** | tek örnek cümle ≠ manuscript |
| `pilot-marker` | Türkçe pilot işareti | test malzemesi ticari metne giremez |

Dedektör **yalnızca dosya adına** güvenmez; `git ls-files` ile takip edilen
her dosyanın **içeriğini** okur. Kanıt disipline değil fikstüre bağlıdır:
`05_TESTS/fixtures/` altındaki kasıtlı sızıntı kurguları CI'da
**KIRMIZI**, temiz durum **YEŞİL** üretir ve bu ispat `selftest.py` § 6'da
her koşuda tekrarlanır.

Sırlar (`.env`, kimlik bilgileri, API anahtarları) K9'daki gibi taranmaya
devam eder.

---

### K13 · A2 KAPANDI — aile hedefleri yeniden dengelendi (10 / 17)

**Tarih:** 13 Ağustos 2026 · **Faz:** 2 · **Karar:** kurucu

| Aile | Faz 1 hedefi | **Kilitli hedef** |
|---|---:|---:|
| Av ve kuşatma | 14 | **10** |
| Savaş tahtası | 13 | **17** |

Toplam 100 korunur. **Karar kilitlidir ve yeniden açılmaz.**

**Gerekçe tek cümledir: veri hipotezi yendi.** Av-kuşatma ailesi 21 aday
taşıyor ama yalnızca 10'u uygun; iki kümesi de ayrı bir duvara çarpıyor
(tafl kümesinin kuralı yok, kaplan-keçi kümesi tek kaynaklı). Hedefi 14'te
tutmak, kitaba dört zayıf oyun **zorlamak** demekti.

Karşı gerekçe kayda geçmişti (av-kuşatma en görsel ve en çocuk-dostu aile)
ve kurucu tarafından tartılıp reddedildi. Bu belgede kalmasının sebebi
şudur: bir kararın hangi itiraza rağmen alındığı, kararın kendisi kadar
değerlidir.

**Ek talimat:** av-kuşatma ailesi bir daha 14'e çıkarılmaz ve savaş tahtası
yapay olarak şişirilmez. 17'nin tamamı **mevcut uygun havuzdan** gelir —
20 uygun aday vardır, yani seçim hâlâ seçimdir, doldurma değil.

---

### K14 · A3 KAPANDI — nihai 100 oyun KİLİTLİ

**Tarih:** 13 Ağustos 2026 · **Faz:** 2 · **Karar:** kurucu

Nihai liste `01_SOURCE/scope_lock.json` içinde durur: **100 oyun ·
71 kültür · 19 yedek**. Türetimi denetlenebilirdir — Faz 1'in 96'lık
önerisi + 23 yedek havuzu + uygunluk verisi + K13 yeniden dengelemesi
modele geri verildiğinde model **tam 100** üretir ve yedi ailenin hedefi de
dolar. Bu, listenin bir tercih değil bir **sonuç** olduğunu gösterir.

Her kayıt on alan taşır: kimlik · aile · kültür · bölge · ülke/alan ·
dönem · kaynak eşlemesi · kural bütünlüğü · oynanabilirlik · araştırma
durumu · uygunluk.

**Kilit iki yönlü korunur** (`04_BUILD/validate_scope.py`):

1. **Liste değişirse** — kimlik özeti (sha256) tutmaz, kapı ısırır.
2. **Envanter kayarsa** — kilit, her kaydın *karar anındaki* aile,
   kültür, bölge, oynanabilirlik, kısıt ve araştırma değerlerini de saklar
   ve her koşuda envanterle karşılaştırır.

İkincisi birincisinden **daha önemlidir**: bir oyun sessizce `dropped`
olsa ya da kısıt taramasından `restricted` çıksa, liste hâlâ o kimliği
taşıdığı için hiçbir dosyada değişiklik görünmezdi. Artık görünür.

Değişiklik yasak değildir; **sessiz** değişiklik yasaktır. Bir oyunun
yerine başkası ancak `amendments[]` şerhiyle konur ve şerh altı alanı
birden yazmak zorundadır: tarih · gerekçe · çıkarılan · yerine konan ·
aile dengesine etkisi · kültür dengesine etkisi. Eksik şerh CI'ı kırar.

---

### K15 · A7 KAPANDI — dış testçi VAR; iç ve dış kanıt AYRI sayılır

**Tarih:** 13 Ağustos 2026 · **Faz:** 2 · **Karar:** kurucu

Faz 2'nin sert bloklayıcısı kalktı: kurucu gerçek insan testçi buldu.
Testçiler Türkçe konuşuyor, bu yüzden **tester-facing** malzeme Türkçedir
(K16).

Bu karar bir şeyi **kolaylaştırmaz**: kanıt türleri birbirine karışamaz.

| Kanıt | Kim üretir | `locked` kapısında sayılır mı |
|---|---|---|
| `internal` | ana ajan · alt-ajan · doğrulayıcı | **HAYIR** |
| `external` | gerçek insan testçi | **EVET** |

Ajanın ürettiği her şey `internal`dır ve bu bir aşağılama değil bir
**tanımdır**: bir kural metnini yazan zihin, o metni okuyup anlamadığını
keşfedemez. `qa_playable.py` yalnızca `external` kaydı kapı olarak sayar
ve iki türü aynı toplamda göstermez.

**Sahte kayıt üretmek bu projede iş bitiren bir ihlaldir.** Ajan test
oturumu düzenleyemez; teslimatı **test paketidir**, test sonucu değil.
Sonuçlar gerçek oturumlardan gelene kadar oyunlar `locked` **olamaz** ve
bu, kabul edilmiş ve raporlanan bir bloktur.

Kişisel veri toplanmaz: yalnızca anonim testçi kimliği (`T01`…) tutulur.
`qa_playable.py` ad, e-posta, telefon gibi alanları taşıyan bir kaydı
**reddeder** — testçiyi korumak da bir kapıdır.

---

### K16 · TİCARİ DİL İNGİLİZCEDİR — Türkçe yalnızca TEST malzemesidir

**Tarih:** 13 Ağustos 2026 · **Faz:** 2 · **Karar:** kurucu

| Katman | Dil | Ticari mi |
|---|---|---|
| Ticari ürünün tamamı | **İngilizce** | evet |
| Mühendislik belgeleri (bu dosya dâhil) | Türkçe | hayır |
| **Dış test paketi** | **Türkçe** | **hayır** |

Türkçe pilot yalnızca **mevcut testçiler Türkçe konuştuğu için** vardır.
Geçicidir, ticari değildir, ve ticari manuscript'e giremez.

**En önemli madde budur:**

> Türkçe pilotun BAŞARISI, İngilizce sürümün DOĞRULUĞUNU KANITLAMAZ.

Sebep mekaniktir, kültürel bir incelik değil: bir kuralın belirsizliği
**dilin içinde yaşar**. Türkçe "taşı al" ile İngilizce "take the piece"
farklı yerlerde bulanıklaşır; kelime oyunu, terim seçimi, edilgen çatı ve
gönderim zamiri oyunu **değiştirebilir**. Bu yüzden:

1. Türkçe pilot **çeviri kaynağı değildir**. İngilizce sürüm doğrudan
   İngilizce yazılır; makine çevirisi ya da birebir aktarım yasaktır.
2. İngilizce sürüm **bağımsız olarak** yeniden doğrulanır: kaynak · kural ·
   oynanabilirlik · netlik · terminoloji · kültürel sadakat · diyagram.
3. Oyunu etkileyen her kelime değişikliği **yeniden doğrulama tetikler**.

Mekanik karşılığı `04_BUILD/qa_language_split.py`: ticari manuscript'te
Türkçe pilot metni ya da Türkçeye özgü karakter/kalıp yoğunluğu bulursa
CI kırmızı yanar. Kasıtlı fikstür bu ispatı `selftest.py` içinde tutar.

---

### K17 · SAYFA DOĞRULAMASI BİR KAYITTIR, BİR ETİKET DEĞİL

**Tarih:** 13 Ağustos 2026 · **Faz:** 2

K11 iki seviyeyi ayırmıştı (`bibliographic` ↔ `page-verified`). Faz 2
ikincisinin **ne anlama geldiğini** kayda bağladı.

`sourceVerification: "page-verified"` yazmak bir iddiadır ve tek başına
denetlenemez. Bu yüzden her doğrulama `01_SOURCE/source_verification.json`
içinde dokuz alan taşır:

```
gameId · sourceRef · edition · locator · supportingPassage ·
supportedClaim · verifiedOn · accessMethod · status
```

`supportingPassage` alanı belirleyicidir: **kaynağın kendi cümlesi**
kayda geçer. Bir sayfa numarası uydurulabilir; o sayfada duran cümle
uydurulamaz — ve uydurulursa denetlenebilir biçimde yanlıştır.

Üç durum vardır ve üçü de dürüsttür:

| Durum | Anlamı |
|---|---|
| `verified` | Kaynak açıldı, pasaj okundu, iddia karşılandı |
| `blocked` | Kaynağa **erişilemedi** — telif, ödünç kısıtı, dijitalleşmemiş |
| `pending` | Henüz denenmedi |

**`blocked` bir başarısızlık değil, bir ölçümdür.** Erişilemeyen bir
kaynağı "doğrulandı" saymak, kitabın tek denetlenebilir iddiasını yıkar.
`validate_research.py` `locked` bir oyun için ≥2 `verified` kayıt şart
koşar; `blocked` sayılmaz. Sonuç: **erişilemeyen kaynağa dayanan bir oyun
kilitlenemez.**

---

### K18 · FAZ 3 KOŞULLU ÜRETİM ŞERİDİ — kapı AÇILMADAN üretim

**Tarih:** 13 Ağustos 2026 · **Faz:** 3 · **Karar:** kurucu

Faz 2'nin resmî kapısı **kapanmadı** ve kapanmamış olarak kalıyor. Kurucu
buna rağmen **üretim işinin başlamasını** açıkça yetkilendirdi.

İki şey birbirinden ayrılır ve ayrı kalır:

| | Durum |
|---|---|
| **Faz 3 üretim işi** | **YETKİLİ** |
| **Resmî faz kapısı** (`.gate`) | **AÇILMADI — `phase1`** |
| `locked` durumu | **UYDURULAMAZ** |

**`.gate` yalnızca gerçek kanıt yükseltir.** Sistemi tamamlanmış
göstermek için kapı yükseltilmez. Bu, projenin en pahalı yalanı olurdu:
kapı seviyesi, kitabın ne kadar hazır olduğunu okuyan tek makine
okunur sayıdır.

Bu şeridin amacı tek cümledir: **kaynak erişimi ve insan testi ayrı
ayrı çözülürken, çözülebilir oyunlarda üretim durmasın.**

Yetki şunları KAPSAMAZ: test uydurmak · kaynak uydurmak · doğrulanmamış
oyunu kilitlemek · erişilemeyen kaynağı doğrulanmış saymak · CI'ı
atlamak · araştırma standardını gevşetmek.

---

### K19 · DİYAGRAM BÜTÇESİ 150 MM — BAĞLAYICI ve ÖLÇÜLEREK denetlenir

**Tarih:** 13 Ağustos 2026 · **Faz:** 3 · **Karar:** kurucu (Karar A)

Faz 2 ölçümünün türettiği 150 mm bütçesi **onaylandı ve bağlayıcıdır**.

Önceki 180 mm genişlik sınırı bir **genişlik** sınırıydı; 150 mm bir
**yükseklik/alan bütçesidir** ve ondan daha serttir. Geri alınmaz.

**Ölçüm kaynağı metadata DEĞİL, RENDER EDİLMİŞ ÇIKTIDIR.**

Gerekçe: bir tanımlayıcı "9×9 tahta" der ve bu bir boyut vermez. Boyutu
belirleyen şey adım aralığı, efsane satır sayısı, panel dizilimi ve
altyazıdır — yani ancak çizildikten sonra bilinir. "Daha küçük
görünüyor" bir kanıt değildir.

Bütçeyi aşan bir madde için beş yol vardır ve **küçültüp okunmaz hâle
getirmek bunlardan biri değildir**: diyagramı yeniden tasarla ·
sadeleştir · kompakt panellere böl · sayfa mimarisi içinde yerleşimi
değiştir · oyunu dürüstçe temsil edilemiyorsa ertele.

---

### K20 · ERİŞİLEBİLİR KAYNAK ÖNCE — ve erişilebilir ≠ güvenilir

**Tarih:** 13 Ağustos 2026 · **Faz:** 3 · **Karar:** kurucu (Karar C)

Telifli kaynaklara erişim kurucunun üzerinde çalıştığı ayrı bir iştir.
Proje beklemez: **erişilebilir ve doğrulanabilir oyunlarla devam eder.**

Engellenen oyunlar `01_SOURCE/source_access_pending.json` kuyruğunda
durur ve erişim geldiğinde normal hatta geri girer.

**Faz 3'ün kendi bulgusu buna bir şart ekledi:**

> **Erişilebilir olmak, güvenilir olmak demek değildir.**

Kamusal alan derlemeleri (Falkener 1892 gibi) Murray'den ÖNCEDİR ve
yeniden kurgulamaları bugün geçersizdir. Faz 3 sayfa doğrulaması bunu
iki yerde somut olarak gördü: Falkener'ın Pachisi bölümü Akbar'ın
"canlı taşlar" anlatısını ikincil bir dergiden aktarır ve yazarın kendisi
*"I applied at the India Office, but could get no information"* der —
yani Faz 1'in bu anlatı için koyduğu uyarı doğrulanmıştır.

Bu yüzden Faz 3 kaynakları **türüne göre** sıralar:

| Öncelik | Tip | Örnek |
|---|---|---|
| 1 | **birinci elden saha kaydı / müze envanteri** | Culin 1895 · Culin 1907 · Parker 1909 |
| 2 | birinci elden gözlemci günlüğü | Linnaeus 1811 · Montgomery 1887 |
| 3 | dönemin derlemesi — yalnızca DESTEK olarak | Falkener 1892 |

**Bir Viktorya derlemesi tek başına bir kural metnini taşıyamaz.**
Özellikle `reconstructed` oyunlarda kullanılamaz: eski bir yeniden
kurgulama, yeni bir yeniden kurgulama kadar kesin görünür ve okur ikisini
ayırt edemez.

---

### K21 · FAZ 4 ÜRETİM İSTİSNASI — üretim ilerler, RESMÎ KAPI ilerlemez

**Tarih:** 14 Ağustos 2026 · **Faz:** 4 · **Karar:** kurucu

Kurucu talimatı iki cümledir:

> *"Testlerin halledildiğini varsay ve Faz 4 üretimine devam et —
> kalan oyunları yaz. Engelli oyunları sona bırak."*

Bu, K18'in Faz 4'e uzatılmasıdır ve **aynı sınırı taşır**:

| | Durum |
|---|---|
| **Faz 4 üretim işi** | ✅ **YETKİLİ** |
| **Resmî faz kapısı** (`.gate`) | ⛔ **`phase1` — yükseltilmez** |
| **Dış oynanabilirlik testi** | ⛔ **`pending` kalır** |
| `locked` oyun | **0 — uydurulamaz** |

**"Testleri halledilmiş say" ne demektir ve ne demek DEĞİLDİR.**

Demektir: *dış test oturumunun yürütülmesini bekleyerek üretimi durdurma.*

Demek DEĞİLDİR: *test kaydı uydur.* `externalPlaytest = pending` alanı
`passed` yapılmaz, testçi adı yazılmaz, süre uydurulmaz. Bir üretim
yetkisi bir kanıt üretmez; ikisini karıştırmak bu projede iş bitiren
ihlaldir (K15).

Sonuç, projenin baştan beri sürdürdüğü ayrımın Faz 4'teki hâlidir:

```
PRODUCTION      : AUTHORIZED
FORMAL VALIDATION: PENDING
```

Bu iki satır `PROJECT_CONTEXT.md`, `ROADMAP_PROGRESS.md` ve
`06_REPORTS/PHASE_4_REPORT.md` içinde **açıkça** durur.

---

### K22 · FAZ 4 KUYRUĞU BİR SIRA KAPISIDIR — erişilebilir önce, engelli sona

**Tarih:** 14 Ağustos 2026 · **Faz:** 4 · **Karar:** kurucu (§ 4 · § 8)

Kapsam kilidi (K14) listenin **ne** olduğunu korur. Faz 4 buna ikinci bir
koruma ekler: listenin **hangi sırayla işlendiği**.

`04_BUILD/build_queue.py` beş öncelik türetir ve `--check` sırayı CI'da
denetler. Engelli bir oyun erişilebilir bir oyunun önüne geçerse kapı
kırmızı yanar — çünkü o durumda üretim, **açık bir kaynak dururken kapalı
bir kaynağı bekler**.

| P | Anlamı |
|---|---|
| 1 | erişilebilir · sayfa-doğrulanmış künye · kural tam |
| 2 | erişilebilir · doğrulama Faz 4 içinde tamamlanabilir |
| 3 | yeniden kurgulanmış · `reconstructionPlan` belgeli |
| 4 | **DENENDİ ve erişilemedi** — telif / ödünç kısıtı |
| 5 | çözülmemiş kural kimliği ya da kaynak uyuşmazlığı |

**P4'ün tanımı dardır ve bilerek dardır.** Bir oyun P4'e yalnızca
`source_access_pending.json` içindeyse — yani gerçekten denenip
erişilememişse — girer. Henüz sıraya gelmemiş bir oyun P2'de durur.

Faz 3 bu ayrımı kurmuştu; Faz 4 onu bir **kapıya** bağladı ve ölçtü:

| | Faz 3 kuyruğu | **Faz 4 kuyruğu** |
|---|---:|---:|
| "öncelik 4" gösterilen | **80** | **5** |
| gerçekten engelli | 4 | **5** |
| erişilebilir | 20 | **94** |

Faz 3'ün kuyruğu 80 oyunu en alt önceliğe koyuyordu çünkü
"denenmedi" ile "engellendi" aynı kovaya düşüyordu. Sayı yanlış değildi,
**anlamı** yanlıştı: bir üretim planlayıcısı ona bakıp kitabın dörtte
üçünün kaynak beklediğini okurdu.

> Bir engeli abartmak, onu küçümsemek kadar yanlıştır.
> İkisi de aynı şeyi yapar: kararı yanlış veriye dayandırır.
