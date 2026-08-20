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
| ~~A6~~ | Yazar biyografisi metni | — | — | ✅ **KAPANDI · Faz 6** — kardeş projeden birebir kopyalandı, yazılmadı; künye: `06_REPORTS/AUTHOR_BIO_PROVENANCE.md` |
| **A8** | **Kapsam eşiği: 56 mı 100 mü?** | **YÜKSEK** | **Faz 6 sonu** | AÇIK — `release` kapısı ≥100 ister, kitapta 56 var; kapı bilerek kırmızı |

Dört yüksek öncelikli karar Faz 2 girişinde kapandı. **A6** Faz 6'da kapandı.

**A8 Faz 6'da doğdu ve YÜKLEMEYİ ETKİLER.** Kapsam modeli 100 oyun öngördü;
56'sı için kaynak açılabildi ve kalan 44 **uydurulmadı**. `release` kapısı
hâlâ ≥100 istediği için geçilemez durumda — bu bir kusur değil, kapsamın
küçüldüğünün kaydıdır. Eşiği düşürmek ya da Faz 7'yi açmak **kurucu
kararıdır**; ajan hiçbirini seçmedi. Gerekçeler:
`06_REPORTS/PHASE_6_BRUTAL_AUDIT.md § 6`.

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

---

### K23 · KAPSAM DEĞİŞİKLİĞİ — tahtasız ailede iki çıkarma, iki terfi

**Karar veren:** kurucu · **Faz:** 5 · **Tarih:** 14 Ağustos 2026
**Uygulayan kayıt:** `01_SOURCE/scope_lock.json § amendments[0]`

Kurucu, tahtasız ailenin **iki ayrı** kusurunu kapatmak için iki İngiliz
maddenin çıkarılmasını ve yedek havuzdan iki terfiyi yetkilendirdi.

| | ÇIKARILAN | EKLENEN |
|---|---|---|
| 1 | **Fivestones** · İngiliz | **Lagori** · Kannada |
| 2 | **Marbles** · İngiliz | **Kho-Kho** · Marathi |

**Seçim gerekçesi bir tercih değil bir TÜRETMEDİR.** Projenin kendi
`scores.distinct` alanı (mekanik ayırt edicilik) tahtasız ailenin beş
İngiliz maddesini şöyle sıralar:

| madde | distinct | kaynak | not |
|---|---:|---:|---|
| **fivestones** | **2** | 5 | Faz 1 kaydı: *"Gonggi ile aynı mekanik; ikisinden biri elenmelidir."* |
| **marbles** | **3** | 5 | petanque ile "hedefe atma" kümesinde; özü bahis (K5 dönüşümü şart) |
| conkers | 4 | 5 | kitapta eşsiz: vurmalı düello |
| hopscotch | 4 | 5 | `bed` sınıfının tek maddesi + efsane düzeltmesi |
| cats-cradle | **5** | 5 | **ailenin en ayırt edici ve TEK sayfa-doğrulanmış** maddesi |

En düşük iki ayırt edicilik çıkarıldı. **Cats-cradle korundu** — yazılmamış
olduğu için çıkarmak "ucuz" olurdu ama mekanik çeşitliliği ve kaynak
kalitesini birlikte **düşürürdü**; ikisi de kurucunun ölçütleri arasında.

**Gonggi değil fivestones çıkarıldı**, çünkü gonggi'yi çıkarmak İngiliz
sayısını düşürmez ve kapsamdan bir kültürü tamamen silerdi.

#### Ölçülen etki — iddia değil, sayı

| | ÖNCE | SONRA |
|---|---:|---:|
| kitap · oyun | 100 | **100** |
| kitap · kültür | 71 | **73** |
| tahtasız · oyun | 15 | **15** |
| **tahtasız · kültür** | **11** | **13** |
| **tahtasız · İngiliz madde** | **5** | **3** |
| yedek havuz | 19 | 19 |

Aile hedefleri **dokunulmadı** (14/10/15/14/17/15/15 = 100): dört maddenin
dördü de tahtasız ailedendir ve değişiklik ailenin **içindedir**.

#### Ödenen bedel — gizlenmez

Fivestones ve marbles **Faz 4'te yazılmıştı**. Yazılmış oyun sayısı
**22 → 20** düştü. Prozaları silinmedi; korumalı katmanda
`02_MANUSCRIPT/retired_phase5.json` içinde duruyor ve ikisi de yedek
havuza geri kondu. *"Zaten yazılmıştı" kurucunun ölçütleri arasında
değildir.*

#### Terfi bir YAZIM İZNİ DEĞİLDİR

İki yeni maddenin kaynağı **arandı ve bulunamadı**:

- **kho-kho** — kuralları ilk kez **1914**'te Deccan Gymkhana komitesince
  çerçevelendi, ilk basılı kural kitabı **1935**. Dönem etnografik kaydı
  yok; oynanabilir biçim bir **20. yüzyıl kodifikasyonudur**.
- **lagori** — Thurston 1906 tam metni tarandı (oyun bölümü yok);
  archive.org 1850–1930 başlık taraması sonuç vermedi.

İkisi de kuyrukta **P6**'dadır ve **yazılamazlar** (§13). Yeni bir
öncelik seviyesi bunun için açıldı:

> **P4 ≠ P6.** P4 bir **erişim** engelidir: kayıt vardır, nüshası
> kapalıdır, kurucunun kütüphane kartı onu açar. P6 bir **varlık**
> sorunudur: denetlenebilir bir kayıt henüz yoktur ve hiçbir izin onu
> var etmez. İkisini aynı kovaya atmak, Faz 3'ün *"denenmedi = engelli"*
> hatasının bir seviye derindeki tekrarı olurdu.

#### Sayfa modeline etkisi — ölçüldü (§20)

| | Faz 4 (22 oyun) | **Faz 5 (20 oyun)** |
|---|---:|---:|
| toplam sayfa | 258 | **260** |
| sapma | +%0,8 | **+%1,6** ✅ |
| ciltsiz telif | 8,41 $ | **8,37 $** |
| ciltli telif | 10,96 $ | **10,92 $** |

Çıkan iki madde kısa metinli ve küçük diyagramlıydı; gitmeleri ortalamayı
yukarı itti. Sayfa **hedefi** değiştirilmedi (yol haritası § 15).

---

### K24 · CATS-CRADLE DİYAGRAM İSTİSNASI — tekil, kurucu onaylı

**Karar veren:** kurucu · **Faz:** 5 · **Tarih:** 14 Ağustos 2026
**Uygulayan kayıt:** `project_config.json § diagram.diagramBudgetOverrides`

Faz 5, cats-cradle maddesini yazamamıştı ve sebebi kaynak değil **bütçeydi**:
kaynak (Jayne 1906, ss. 324–338) tam ve sayfa-doğrulanmış; ama oyunun kendisi
**sekiz adlandırılmış figürün sırayla alınmasıdır** ve sekiz figür 150 mm'ye
sıkıştırılırsa figür başına **~18 mm** düşer. O boyutta parmak ve ip yolu
okunmaz — yani madde "sığar" ama **oynanamaz**.

Kurucu istisnayı onayladı:

> **CATS-CRADLE 150 mm tavanını AŞABİLİR.**

#### İstisna DAR ve MEKANİKTİR

| | |
|---|---|
| Genel tavan | **150 mm — DEĞİŞMEDİ** |
| İstisna kapsamı | **yalnızca `cats-cradle`** |
| İstisna tavanı | 340 mm |
| Biçim | genel bir "muafiyet bayrağı" **DEĞİL**, bir **kimlik eşlemesi** |

Mantık bilerek şöyledir:

```
limit = overrides.get(gameId, 150)
```

`allowOverBudget: true` gibi bir **bayrak asla eklenmedi**. Bir bayrak her
maddeye yazılabilir; bir kimlik eşlemesi her yeni satır için bir **karar**
ister.

#### Dört kasıtlı kusur testi istisnayı kilitliyor

| kurgu | beklenen |
|---|---|
| cats-cradle > 150 mm | **GEÇER** — istisna gerçekten uygulanıyor |
| başka bir oyun > 150 mm | **KIRMIZI** — istisna genelleşmiyor |
| sözlüğe **ikinci** oyun eklenir | **KIRMIZI** — tavan bir "listeye" dönüşemez |
| istisna silinir, cats-cradle aşar | **KIRMIZI** — istisna bir varsayım değil bir **kayıt** |

Üçüncü satır bu kararın asıl koruyucusudur. Bir istisna listesi, bir kez
*liste* hâline geldiği anda tavanın kendisi bir **öneriye** dönüşür ve bu,
hiçbir şey kırmızı yanmadan olur.

#### İstisna BOYUT için değil OKUNABİLİRLİK için

> Amaç **azami boyut** değil **azami okunabilirliktir**. Ölçülen gerçek
> footprint raporda, normal 150 mm karşılığıyla birlikte yazılıdır.

`source_access_pending.json § editorialHolds[cats-cradle]` bu kararla
**kapandı**.

---

### K25 · DİYAGRAM DİLİ v1.5 — dört yeni yetenek, kurucu yetkisiyle

**Karar veren:** kurucu · **Faz:** 5 · **Tarih:** 15 Ağustos 2026

Faz 5 tek fazda **dört** tahta unsurunun çizilemediğini ölçtü ve dördü de
**kural taşıyordu** — yani eksik çizmek, kuralla **çelişen** bir tahta
üretir. Dört madde bu yüzden **diyagramsız** basılmıştı.

| unsur | oyun | v1.4 ne yapıyordu |
|---|---|---|
| haç biçimli tahta | pachisi | 11×11 **dolu ızgara** çiziyordu |
| nehir + hisar köşegeni | xiangqi | düz kesişim ızgarası |
| terfi köşegeni | sittuyin | köşegen çizemiyordu |
| ip figürleri | cats-cradle | iki figürü **ayırt edemiyordu** |

**v1.5 dört yetenek ekler:**

| # | alan | ne yapar |
|---|---|---|
| ① | `omitCells` | tahtada **bulunmayan** kareler — haç, artı, L |
| ② | `lines` | tahtanın üstüne açık çizgiler — hisar, terfi köşegeni |
| ③ | `gapAfterRow` | bir sıradan sonra boşluk ve kesilen dikey çizgiler — **nehir** |
| ④ | `bodily/figure` | ip figürü: düğümler + `strings` polilinleri |

**EKLEME GERİYE DÖNÜK DEĞİLDİR.** Mevcut hiçbir tanımlayıcı değişmedi ve
yirmi altı diyagramın çıktısı **byte düzeyinde aynı kaldı**; yalnızca dört
yeni diyagram eklendi. Dondurma, dilin **büyümesini** değil mevcut
notasyonun **değişmesini** yasaklar — v1.2→v1.3 (graph) ve v1.3→v1.4 (bed)
geçişleri de böyleydi.

**Dört yeni alan dört yeni SESSİZ YALAN yolu açtı** ve dördü de kapıya
bağlandı: olmayan bir kareye taş koymak · tanımsız bir koordinata çizgi
çekmek · tahta dışında bir nehir açmak · tanımsız bir düğümden ip
geçirmek. Dördü de render'da **sessizce yok sayılırdı**.

**Ölçülen sonuç:** dört diyagram geri geldi, hiçbiri çift sayfayı aşmadı,
sayfa modeli **256 · sapma %0,0**.

> ⚠ **K24 hâlâ KULLANILMIYOR.** cats-cradle artık **58,8 mm**'dir. İstisna
> kayıtlı ve etkin kalıyor; gerekmedi çünkü asıl kısıt milimetre değil
> **notasyondu** ve v1.5 onu çözdü.

---

### K26 · FORBES 1860 — kuralı alınır, tarihi ALINMAZ

**Karar veren:** kurucu · **Faz:** 5 · **Tarih:** 15 Ağustos 2026

Forbes 1860 shatranj ve chaturanga için **erişilebilir ve ayrıntılı** bir
kamusal alan kaynağıdır. Ama kitabın merkezî tezi — *dört elli zarlı
chaturanga bütün satrançların atasıdır* — **H. J. R. Murray tarafından 1913'te
çürütülmüştür**.

**Karar:** Forbes'tan **kurallar** alınır, **tarih tezi** alınmaz; ve tez
sessizce atlanmaz, **açıkça düzeltilir**.

Arka maddedeki *uydurulmuş gelenekler* kutusuna **iki düzeltme** eklendi:

1. *"Satranç dört elli zarlı bir Hint oyunu olarak başladı."* → **Oyun
   gerçek, soyağacı değil.** Dört elli biçim ata değil, sonraki bir
   varyanttır.
2. *"Erken Hint satrancında fil vezir gibi hareket ederdi."* → **Bir
   çeviri hatası, sonraki çevirmen tarafından düzeltildi.** Jones ve Radha
   Kant yanlış çevirdi; `chatushtayam` "dört ana yönde" demektir ve fil
   **kale** gibi hareket eder. Bu düzeltmeyi yapan **Forbes'un kendisidir**.

İkinci madde bilerek eklendi: birincisi Forbes'un yanıldığı, ikincisi
**haklı olduğu** yerdir.

> Bir kaynak gördüğü şeyde haklı, çıkardığı sonuçta haksız olabilir. Bir
> oyun kitabının okuruna bunu göstermesi, doğru kuralı vermek kadar
> değerlidir.

---

### K27 · YENİDEN KURGULAMA POLİTİKASI — kurucu onaylı

**Karar veren:** kurucu · **Faz:** 5 · **Tarih:** 16 Ağustos 2026

Çekirdek mekaniği **tarihsel olarak belgelenmiş** ama belirli kuralları
(puanlama, tur sırası, bitiş) **kayıp ya da erişilemez** olan oyunlar
editoryal olarak tamamlanıp **oynanabilir** hâle getirilebilir.

**ŞART — üçü de bağlayıcı:**

1. Madde **`reconstructed`** olarak işaretlenir (envanter ve manuscript
   **iki yönlü** uyuşmak zorunda; `qa_manuscript § ③` denetler).
2. Prozada **hangi kuralın kaynaklı, hangisinin editoryal** olduğu
   satır satır söylenir — `(Editorial ruling)` işaretiyle.
3. `reconstructionNotice` maddenin **başında** neyin bilinmediğini yazar.

**Politika neyi DEĞİŞTİRMEZ:**

- Kaynağın **ne söylediği** yine sayfa seviyesinde doğrulanır.
- **Başka bir kültürün oyunundan kural ÖDÜNÇ ALINMAZ** — bu yasak
  patolli maddesinde ayrıca yazılıdır (pachisi benzetmesi tam olarak bu
  yüzden reddedildi).
- Çekirdek mekanik **belgelenmemişse** politika uygulanmaz; oyun
  Kütüphaneci listesine gider.

#### `verified` ne demektir — bir açıklık

K27 bir belirsizliği ortaya çıkardı ve kayıt düzeltildi:

> **`verified` = "pasaj açıldı ve yazıldığı gibi okunuyor".**
> **`verified` ≠ "pasaj tam kural veriyor".**

Neyi desteklediği `supportedClaim` alanında **sınırlarıyla** yazılıdır.
Fiske hnefatafl için yalnızca terminoloji verir ve kaydı bunu söyler;
kayıt yine de `verified`dir çünkü pasaj gerçekten öyle okunmaktadır.

#### İlk uygulama

| oyun | belgelenen | editoryal olan |
|---|---|---|
| **hnefatafl** | ad, iki oyuncu, tek kral, iki taraf (Fiske ss. 58–59) | **bütün mekanik** — Linnaeus'un tablut kaydından aktarıldı |
| **patolli** | hasır, fasulye zarı, bahis, çağrı (Culin ss. 854–856) | tur mantığı, yasal hamle, puanlama, bitiş |

---

### K28 · KÜTÜPHANECİ YOLU — kurucu kaynak sağlar

**Karar veren:** kurucu · **Faz:** 5 · **Tarih:** 16 Ağustos 2026

Ne yeniden kurgulanabilen ne de değiştirilebilen oyunlar için kurucu
**kaynak metni doğrudan sağlar**. Ajan bu durumda **tam künyeyi ve
ihtiyaç duyduğu bölümü** listeler; uydurmaz, tahmin etmez, bekler.

**Liste:** `06_REPORTS/LIBRARIAN_REQUEST_LIST.md` — üretilen dosya,
kuyruktan türetilir.

> Bir kaynağı istemek, onu uydurmaktan her zaman ucuzdur.

---

### K29 · KÜTÜPHANECİ TESLİMİ ÜÇÜNCÜ BİR ÜRETİM DAYANAĞIDIR

**Karar veren:** kurucu · **Faz:** 5 · **Tarih:** 18 Ağustos 2026

Kurucu, engellenmiş oyunlar için **kural özetlerini doğrudan sağladı**
(`games-lib-screenshots/Tien gow Tin Kau 天九 ve.txt`). Bu, projenin
kaynak modelinde **yeni bir durum** açtı.

Proje bugüne kadar **iki** durum tanıyordu:

| durum | anlamı |
|---|---|
| `verified` | pasaj açıldı, sayfa okundu, künye tam |
| değil | yazılamaz |

Kurucu teslimi **üçüncüsüdür** ve ikisinin de yerine geçmez:

```
founderSupplied         = true
independentVerification = false
bibliographyStatus      = incomplete
```

**Üretim için YETERLİDİR** (kurucu yetkisi) ama **`verified` DEĞİLDİR** ve
asla öyle gösterilmez. Kurucunun § 24 talimatı bağlayıcıdır:
*"DO NOT UPGRADE IT INTO AN INDEPENDENTLY VERIFIED SOURCE WITHOUT ACTUAL
EVIDENCE."*

#### Sayfa numarası UYDURULMADI

Teslim dosyası URL veriyor, **baskı ve sayfa vermiyor**. Beş kaydın
beşinde de `sourcePages` **boştur** ve `bibliographyStatus`
**`incomplete`** yazar. Doğrulayıcıyı yeşile boyamak için künye
uydurmak, kitabın tek denetlenebilir iddiasını yıkardı.

#### Üç kapı bu yüzden değişti — ve zayıflamadı

| kapı | eski | yeni |
|---|---|---|
| `build_queue --check` | yazılmış oyun **`verified` künye** ister | **`verified` VEYA kütüphaneci kaydı** ister; ikisi de yoksa hâlâ kırmızı |
| `qa_rules` | `01_SOURCE/rules/*.json` = oyun başına bir kayıt | çok oyunlu teslim dosyası **muaf**; kendi kapısı var |
| `selftest` | aynı ikili varsayım | aynı üçlü ayrım |

**Yeni kapı:** `04_BUILD/librarian_ingest.py` — kanonik kaydı üretir ve
**dürüstlüğünü denetler**. Dört kasıtlı kusur testi:

| kurgu | beklenen |
|---|---|
| kurucu özetini "bağımsız doğrulanmış" göstermek | **KIRMIZI** |
| künye eksikken sayfa uydurmak | **KIRMIZI** |
| `founderSupplied` bayrağını silmek | **KIRMIZI** |
| kütüphaneci kaydında yinelenen oyun | **KIRMIZI** |

#### Üç oyunun engeli KALKTI

Teslim, üç oyunun **tam olarak eksik olan şeyini** verdi:

| oyun | eski durum | çözüm |
|---|---|---|
| **jianzi** | P5 · Culin'in cildi Kore/Japon nesnesini anlatıyordu | **Çin** kuralları sağlandı |
| **tien-gow** | P5 · Culin'in cildi Kore dominosuydu | **Kanton** kuralları sağlandı |
| **gomoku** | P6 · amaç vardı, kural seti yoktu | tam Japon kural seti sağlandı |

`go` ve `sugoroku` **P5'te kaldı**: teslim onların doğru kültür kaynağını
içermiyor.

---

### K35 · ÖLÇÜLEN BİR KAPI, GÖRDÜĞÜ DOSYA KADAR VARDIR

**Karar.** Bir kalite kapısının denetlediği dosya kümesi, kapının kendisi
kadar denetlenir. `.gitignore` bir kapıyı kör edebilir ve ettiği anda kapı
**yeşil** yanar.

**Neden.** Faz 6 ölçtü: CI'da diyagram kapıları **51 diyagramın 18'ini**
görüyordu. Faz 4 ve Faz 5 kendi tanımlayıcı dosyalarını izin listesine
eklememişti; dosyalar `.gitignore` tarafından dışarıda bırakılmıştı. Kapı
her push'ta koştu, her push'ta yeşil yandı ve **33 diyagrama hiç bakmadı**.
Bakacak dosyası olmayan bir kapı, kusuru olmayan bir kapı gibi görünür.

**Sonuç.** Faz 4/5/6 tanımlayıcıları izin listesine alındı. Bundan sonra
CI'da koşan her kapı için tek soru şudur: *bu kapı bugün kaç dosya gördü?*

---

### K34 · KÜLTÜR ADI, MADDEDE NE YAZIYORSA İNDEKSTE DE ODUR

**Karar.** Bir maddenin başlığındaki kültür adı ile o oyunun kültür
indeksindeki kova adı **birebir aynı** olmak zorundadır. Ayrışırlarsa
envanter düzeltilir ve kapsam kilidine şerh düşülür.

**Neden.** Basılı sayfa okunduğunda bulundu: `set-dilth` maddesi
*White Mountain Apache* diyor, kültür indeksi *Apache* diyordu — indeks
envanterden üretiliyor ve envanterde dar ad yoktu. Okur maddede gördüğü adı
indekste arar. Bu bir tasnif tartışması değil, bir **kullanılabilirlik**
kusurudur; ayrıca Culin'in kaydı Albert Reagan'ın White River gözlemine
dayanır ve dar ad kaynağa daha yakındır.

**Mekanizma.** `qa_index.py ③` kültür kovalarını kilitle karşılaştırır ve
ayrışmayı kırmızı yakar. Kapsam kilidi ayrıca **sessiz kaymayı** yakaladı ve
düzeltmenin şerhsiz geçmesine izin vermedi (şerh A3).

---

### K33 · ENVANTERİN KAYNAK ATFI, KAYNAĞIN KENDİSİ DEĞİLDİR

**Karar veren:** kurucu (§ 4 · § 26 yetkisiyle ajan) · **Faz:** 5 · **Tarih:** 19 Ağustos 2026

Kurucu, boşluk kaydının istediği iki eserden birini teslim etti:
Zaslavsky'nin *Africa Counts*'ı. Kitap **gerçekti**, 369 sayfaydı ve
metin katmanı tamdı. Kayıt onun **altı** oyun açacağını söylüyordu.

**Açtığı oyun: bir.**

| oyun | *Africa Counts* içinde |
|---|---:|
| `ampe` · `pilolo` · `shisima` · `morabaraba` · `mefuvha` | **0 geçiş** |
| `ayoayo` | künye var, kural **çapraz gönderme** |
| `omweso` | **tam kural seti** ✅ |

Beş oyun bu kitapta **yoktur**. Projenin envanteri onları *Africa
Counts*'a atfetmişti ve atıf **yanlıştı** — büyük olasılıkla
Zaslavsky'nin 1998 tarihli *Math Games and Activities from Around the
World* adlı AYRI kitabıyla karışmış.

#### Dersin kendisi

Faz 1'den beri her boşluk kaydı şu biçimdeydi: *"bu oyun şu esere
bağlıdır."* O cümlenin iki yarısı vardır ve proje yalnızca birini
denetliyordu:

```
[oyun] ←──── ATIF ────→ [eser]
        ↑                  ↑
   denetlendi         DENETLENMEDİ
   (oyun kapsamda)    (eser oyunu GERÇEKTEN içeriyor mu?)
```

Bir eserin **erişilebilir olması**, o eserin **aranan oyunu içermesi**
demek değildir. K31 *"teslim edilen bir dosya, teslim edilen bir kaynak
değildir"* diyordu; K33 bir adım daha gider:

> **Bir künye, bir kaynak değildir.** Atıf ancak sayfa açıldığında
> kaynak olur.

#### Aynı hata bu fazda üç kez daha ölçüldü

`bagh-chal` (Murray'de var, **yanlış kültürde**) · `game-of-the-goose`
(Bell'de tam kural, ama **İngiliz levhası**) · `congklak` (Murray'de
madde var, **kural yok**). Dördü de envanterde *"kaynağı var"*
görünüyordu.

#### Yedek havuz da ölçüldü ve bir gölge çıktı

| yedek havuz (19 kayıt) | |
|---|---:|
| Zaten KAPSAMDA | **10** (ikisi zaten basılmış: `achi` · `janggi`) |
| Gerçekten kapsam dışı | 9 |
| Elimdeki kaynaklarla yazılabilir | **2** |
| ↳ biri (`puluc`) **`bul` ile AYNI OYUN** | |
| **Kullanılabilir gerçek yedek** | **1** |

Havuz bir **sigorta** değil, kapsamın **gölgesidir**. 48 boş slot için
bir aday sunar. Bu yüzden § 10'un verdiği değiştirme yetkisi
**kullanılmadı**: değiştirilecek bir şey yoktu, eksik olan aday değil
**arz**dı.

`puluc` ile `bul`'un aynı oyun olması ayrıca bir envanter kusurudur ve
ikisini de yazmak **yinelenen madde** üretirdi.

#### Karar

1. Envanterdeki kaynak atıfları **kanıt sayılmaz**; yalnızca sayfa
   açıldığında kanıt olur.
2. Bir eser teslim edildiğinde **önce içindekiler/dizin okunur** —
   bu fazın en verimli hamlesi Bell'in 43 bölüm başlığını basılı sayfa
   numaralarıyla çıkarmak oldu ve üç oyun oradan geldi.
3. `puluc` ↔ `bul` yinelenmesi kayda geçirildi; `bul` basıldı, `puluc`
   yedekte **yazılmadan** durur.
4. **FINAL VERIFIED SCOPE = 52 / 100** ilan edilir. 100 uydurulmaz.

---

### K31 · TESLİM EDİLEN BİR DOSYA, TESLİM EDİLEN BİR KAYNAK DEĞİLDİR

**Karar veren:** kurucu (§ 4 · § 6 · § 11) · **Faz:** 5 · **Tarih:** 19 Ağustos 2026

Kurucu altı dosya teslim etti. **İkisi adının söylediği şey değildi** ve
ikisi de dosya adına bakılarak kabul edilseydi kitaba girecekti.

| dosya | adı ne diyor | gerçekte ne |
|---|---|---|
| `africa-counts-…pdf` | Zaslavsky 1973 | **1.5 KB'lık PHP hata sayfası** |
| `Laurence Russ … (2000).txt` | Russ 2000 | **yapay zekâ sohbet çıktısı** |
| `B-001-002-771.pdf` | hiçbir şey | **Bell, Board and Table Games** |

Üçüncü satır ikisi kadar önemlidir: **adı hiçbir şey söylemeyen dosya
teslimin en iyi kaynağı çıktı.** Dosya adı ne olumlu ne olumsuz bir
kanıttır; PDF künyesi ve içerik kanıttır.

#### Yapay zekâ çıktısı neden reddedildi

`SOURCING_STANDARD.md` § 2 zaten yazıyordu: *"LLM çıktısı — hiçbir
koşulda"*. Bu karar o satırı bir **olaya** bağlar.

Dosya beş oyunun (adji-boto · congklak · omweso · toguz-kumalak ·
pallanguzhi) kurallarını iddia ediyor ve iddiaları **makul görünüyor**.
Tehlikesi tam olarak budur: doğrulanamaz bir metin, doğru bir metinden
ayırt edilemez. Ölçülen parmak izleri: üç kez *"The information for the
question you asked…"* açılışı, 34 asistan alıntı işareti, **sıfır**
birebir pasaj, **sıfır** sayfa numarası.

`pallanguzhi` ve `omweso` o dosya **olmadan** açıldı — Bell'den ve
Murray'den, sayfa numaralarıyla. Yani dosyanın reddedilmesi hiçbir oyunu
kaybettirmedi; kabul edilmesi ise beş maddeyi doğrulanamaz kılardı.

#### İki kez "sayfayı aç" kuralı kitabı kurtardı

| oyun | beklenen | sayfa açılınca çıkan |
|---|---|---|
| `konane` | Murray açar | Murray'in bölüm başlığı: **"WAR-GAMES OF WHICH WE HAVE NO CERTAIN KNOWLEDGE"** ve *"none of which gives any clear indication of how it is played"* → **FINAL SOURCE BLOCKED** |
| `bagh-chal` | Murray açar | Murray'in dört kaplan-keçi maddesi de **Hindistan** (Bengal · United Provinces · Punjab · Manipur); kapsam **Nepalli** der → kültür tuzağı |
| `game-of-the-goose` | Bell açar | Bell'in kuralları **1725 İngiliz levhasından** (Tyburn · Jack Shepherd); kapsam **İtalyan** der → kültür tuzağı |

Üçü de yazılabilirdi ve üçü de yanlış olurdu.

#### Bağımsızlık, künye sayısıyla ölçülmez

`oware` iki künye taşır (Murray ss.181–182 · Bell ss.116–117) ama
**bir** bağımsız kaynağı vardır: Murray'in kaynağı Rattray içindeki
Bennett'tir, Bell'in çizimi *"redrawn from Rattray"* der. § 3 uyarınca
ikisi **bir** sayılır ve `oware` `locked` **olamaz**. Kayıt bunu söyler.

**Sonuç:** teslim → **alım** → **açma** → **kültür denetimi** →
**bağımsızlık denetimi** → yazım. Dört adımın üçü bu teslimde bir şeyi
durdurdu.

---

### K32 · ÖLÇÜLEN BİR DİYAGRAM, DOĞRU BİR DİYAGRAM DEĞİLDİR

**Karar veren:** kurucu (§ 14) · **Faz:** 5 · **Tarih:** 19 Ağustos 2026

Batch 7 altı diyagram üretti ve sayısal kapı **altısını da yeşil
geçirdi**. Görsel denetim **altı kusur** buldu.

| # | kusur | sayısal kapı |
|---|---|---|
| 1 | `markers` alanı tahtaya **hiç çizilmiyor** — dört diyagram efsanede olmayan bir sembol vaat ediyordu | YEŞİL |
| 2 | `dara` üçlüye bitişik bir taş yüzünden **dörtlü** okunuyordu — Bell dörtlünün saymadığını söyler | YEŞİL |
| 3 | `hasami` hareket eden taşı hem çıkışta hem varışta çiziyordu | YEŞİL |
| 4 | `hasami` `panels: 2` diyordu, tek tahta çiziliyordu | YEŞİL |
| 5 | üç efsane sağ kenardan **kırpılıyordu** | YEŞİL |
| 6 | `merafib-spiral` **Kore yut tahtası** çiziyordu | YEŞİL |

#### Altıncısı bir kural hatasıdır, bir çizim hatası değil

`li'b el-merafib` bir **sarmal** yarış oyunudur. `track` sınıfının
render kodu:

```python
elif cls == "track":
    n = 20          # ← SABİT, ve hiç kullanılmıyor
    ...             # yut-nori devresi çizilir
```

`size.stations` **okunmuyor**. Diyagram 54,0 × 76,5 mm ölçüldü, bütçe
denetiminden geçti — ve basılacak olan şey Sudan sarmalı değil **Kore
yut tahtasıydı**.

**Karar:** diyagram **geri çekildi**, madde diyagramsız basıldı ve
sebebi `englishValidation.diagram` içine yazıldı. § 13 genel bir tahtayla
yaklaştırmayı açıkça yasaklar; yanlış bir tahta basmak, tahta basmamaktan
**kötüdür**.

**Diyagram dili DEĞİŞMEDİ** (v1.5 dondurulmuş kalır). `track` sınıfının
sarmal desteği bir **açık iştir** ve kurucu yetkisi gerektirir (K25 ile
aynı sınıf).

> `mutorere-star` ise v1.5'in `nodes`/`edges` grafiğiyle çizildi:
> sekiz ışınlı yıldız bir ızgarayla yaklaştırılamaz ve dilin bu yeteneği
> `achi-wheel`den beri vardı.

---

### K30 · KURUCU ARAŞTIRMA BOŞLUK KAYDI — "kalan" ile "engelli" AYRI ŞEYLERDİR

**Karar veren:** kurucu · **Faz:** 5 · **Tarih:** 18 Ağustos 2026

Kurucu, kalan 59 oyunun **tek tek** ne durumda olduğunu ve **kendisinin
tam olarak neyi araştırması gerektiğini** istedi. Bu, projenin en sık
yaptığı iki hatanın ikisini birden kapatan bir karardır.

#### İki hata, iki yönde

Faz 3 **denenmemiş** bir oyuna *engelli* dedi. Faz 5 raporu ise tersini
riske attı: 59 oyunu tek bir "kaynak duvarı" olarak sundu ve kurucuya
**hangisinin gerçekten kendi müdahalesini gerektirdiğini** söylemedi.

Kayıt bunu **iki ayrı eksenle** çözer ve eksenler karıştırılmaz:

| eksen | ne ölçer | değerler |
|---|---|---|
| `status` | kaynak avının **kanıt** durumu | `BLOCKED` · `SOURCE-PENDING` · `UNRESOLVED` |
| `primaryBlocker` | oyunun **yazılamama sebebi** | `P1`…`P10` |

Bir oyun `SOURCE-PENDING` olup `P2` taşıyabilir: *künyesi var, HENÜZ
denenmedi, ama denendiğinde açılabilir metin bulunması beklenmiyor.*
Buna "engelli" demek Faz 3'ün hatasını tekrarlardı; "sırada" demek Faz
5'in hatasını tekrarlardı. **İkisi de söylenmiyor; ölçülen söyleniyor.**

#### Ölçüm

| | |
|---|---:|
| Kapsam | 100 |
| Yazılmış | 41 |
| **Kurucu müdahalesi OLMADAN yazılabilir** | **7** |
| **Kurucu araştırması GEREKEN** | **52** |
| ↳ `BLOCKED` — denendi, açılamadı | 34 |
| ↳ `SOURCE-PENDING` — künye var, denenmedi | 16 |
| ↳ `UNRESOLVED` — kaynak açık, kültür uyuşmuyor | 2 |
| `UNATTEMPTED` | **0** |

`UNATTEMPTED` **sıfırdır**: Batch 6'da kalan 59 oyunun tamamı elde
bulunan kamusal alan derlemelerine karşı tarandı. Artık "henüz
bakılmadı" diyebileceğimiz bir oyun yok.

#### En önemli tek bulgu

**Murray 1952 tek başına 52 maddenin 24'ünü açar.** Ona Parlett 1999,
Zaslavsky 1973, Bell 1960–69 ve Russ 2000 eklenirse **46'sı** açılır.
Yani kurucunun önündeki iş 52 ayrı araştırma değil, **beş kitaptır**.

Bu, K28'in kütüphaneci yolunu **ölçülebilir** kılar: teslim istekleri
artık oyun oyun değil **eser eser** düzenlenir, çünkü kütüphaneye bir
oyun için değil bir kitap için gidilir.

#### Yeni kapılar

| kapı | ne yapar |
|---|---|
| `build_gap_register.py --check` | kayıt bayat mı · **kapsam = yazılmış + yazılabilir + engelli** örtüşme denetimi |
| `founder_delivery_ingest.py --check` | teslimi alır · hash'ler · künye denetler; **teslim yoksa BOŞ KOŞAR** |

Örtüşme denetimi bir dürüstlük kapısıdır: bir oyun **yazıldığı hâlde**
kayıttan düşmezse CI kırmızı yanar — yani kurucu **çözülmüş** bir engeli
araştırmaya gönderilmez.

Kayıt manuscript'e **bakmadan** üretilebilir: yazılmış küme kapsamdan
türetilir (kapsam − kayıt − yazılabilir) ve manuscript **eldeyse**
türetim onunla karşılaştırılır. Bu kasıtlıdır — manuscript depoda yoktur
(K12) ve kayıt yalnızca yerelde doğrulanan bir belge olsaydı sessizce
bayatlardı.

#### Ham teslim depoya GİRMEZ

`06_FOUNDER_DELIVERY/` telifli tarama taşır ve `.gitignore`dadır;
gerekçe K12 ile aynıdır. Depoda yalnızca **dizinin yapısı** (`README.md`),
**ne istendiği** (`REQUEST.md`) ve **ölçüm** (`06_REPORTS/founder-delivery-ingest.json`
içindeki hash + künye durumu) durur. Teslimin **varlığı** denetlenebilir,
**içeriği** sızmaz.

#### Makine bir PDF'in içinde kural olup olmadığına karar VEREMEZ

Alım betiği mekanik doğrulama yapar ve orada **durur**:
`awaiting-agent-extraction`. Kanıt listesini ajan **sayfayı okuyarak**
işaretler. Bir taramayı görüp "kural tam" demek, sayfayı açmadan künye
yazmakla aynı hatadır — K17'nin kendisi budur.

#### Kapılar KANITLANDI — yedi kasıtlı kusur

Bir kapının VARLIĞI yetmez, ISIRMASI gerekir (K18). `selftest` § ⑩:

| kurgu | beklenen |
|---|---|
| kayıt BAYAT (üretilen ≠ diskteki) | **KIRMIZI** |
| kayıttaki bir oyun kapsamdan düşer | **KIRMIZI** |
| kapsama giren yeni oyun hiçbir kümede değil | **KIRMIZI** |
| yazılabilir oyun kapsamdan düşer | **KIRMIZI** |
| teslim YOKKEN alım kapısı | **YEŞİL** — boş koşar (§ 17) |
| kayıtta OLMAYAN gameId ile teslim klasörü | **KIRMIZI** |
| güncel kayıt | **YEŞİL** |

Sondan ikincisi bir teslim kaybını önler: yanlış yazılmış bir klasör
adı, teslimin **sessizce buharlaşmasıdır** — kurucu kaynağı bulmuş
olur ve kimse görmez.

**Belgeler:** `06_REPORTS/FOUNDER_RESEARCH_GAP_REGISTER.md` (oyun oyun) ·
`06_REPORTS/FOUNDER_RESEARCH_PACK.md` (kaynak kaynak) ·
`01_SOURCE/founder_research_gap_register.json` (makine okunur)

> Kurucuya "52 oyun kaldı" demek bir rapordur.
> "Beş kitap bul, 46'sı açılır" demek bir **plandır**.

---

### K28 · ŞANS AİLESİ 15 → 4 · ON BİR SLOT YEDEKTEN DOLDURULDU

**Karar veren:** kurucu · **Faz:** 5 · **Tarih:** 18 Ağustos 2026
**Uygulayan kayıt:** `scope_lock.json § amendments[1]`

Şans ailesinin on bir oyununun **tamamı** David Parlett'in telifli
eserlerine bağlıydı. Kütüphaneci teslimi onları kapsamıyordu ve
**hiçbiri yeniden kurgulanamaz**: bir kart ya da zar oyununun kural seti
mekanikten **türetilemez**, ezberlenir.

| ÇIKARILAN (11) | kültür |
|---|---|
| shagai · hanafuda-koi-koi · durak · karnoffel · dreidel · mus · truco · briscola · tali · schafkopf · passe-dix | Moğol · Japon · Rus · Alman · Aşkenaz · Bask · Río de la Plata · İtalyan · Roma · Bavyera · Fransız |

Arşiv: `09_ARCHIVE/blocked-chance/` — **silinmediler**, envanterde
duruyorlar ve kütüphane erişimi gelirse geri alınabilirler.

| EKLENEN (11) | aile | kaynak |
|---|---|---|
| **janggi** | savaş tahtası | Culin 1895 § LXXIV (Wilkinson) |
| **tuknanavuhpi** | savaş tahtası | Culin 1907 |
| **ludus-latrunculorum** | savaş tahtası | Falkener · Forbes · Fiske |
| **polis** | savaş tahtası | kurucu teslimi |
| **nine-holes** | çizgi-toprak | Gomme 1894 |
| **luk-tsut-kei** | çizgi-toprak | Culin 1895 |
| **achi** | çizgi-toprak | kurucu teslimi |
| **chaupar** | eve dönüş | Culin 1895/1898 · Falkener · Forbes |
| **ludus-duodecim-scriptorum** | eve dönüş | Fiske · Forbes |
| **daldos** | eve dönüş | *kaynaksız — kapsamda, yazılmamış* |
| **ephedrismos** | tahtasız | *kaynaksız — kapsamda, yazılmamış* |

#### Aile hedefleri YENİDEN YAZILDI

| aile | önce | **sonra** |
|---|---:|---:|
| ekim | 14 | **14** |
| av-kuşatma | 10 | **10** |
| eve dönüş | 15 | **18** |
| çizgi-toprak | 14 | **17** |
| savaş tahtası | 17 | **21** |
| **şans** | **15** | **4** |
| tahtasız | 15 | **16** |
| **toplam** | **100** | **100** ✅ |

#### BEDELİ ÖLÇÜLDÜ VE GİZLENMEDİ

**Kültür: 73 → 68.** Kaybedilen altı kültür: **Aşkenaz Yahudi · Bask ·
Bavyera · Moğol · Rus · Río de la Plata**. Kazanılan: **Danca**.

Yedek havuz bu kaybı **karşılayamadı**: havuzun dört şans oyununun
**üçü** aynı telif duvarına çarpıyor (crown-and-anchor ve tarocchini
Parlett, cho-han Bell).

> Alt başlığın **≥45 kültür** vaadi hâlâ fazlasıyla tutuluyor (68), ama
> altı kültür geri alınamaz biçimde kapsamdan çıktı ve bu, telifli bir
> kaynağın bir kitaba ödettiği gerçek bedeldir.

#### İKİ OYUN BİLEREK ALINMADI

Seçim modeli **puluc** ve **quoits** önerdi; kitap ikisini de almadı:

- **puluc** — kültürü (Kekchi Maya) kapsamda `bul` ile zaten temsil
  ediliyor ve elde kaynağı yok. Yerine **daldos** alındı (Danca —
  kapsamda **hiç** olmayan bir kültür).
- **quoits** — İngiliz'dir ve tahtasız ailede İngiliz yoğunlaşmasını
  **yeniden üretirdi**; **K23 tam olarak onu düzeltmişti**. Ayrıca kendi
  kaydı petanque ile "hedefe atma" çakışmasını adlandırıyor.

Ayrışmanın tamamı şerhte tek tek yazılıdır. **Model bir öneridir; kapsam
bir karardır.**
