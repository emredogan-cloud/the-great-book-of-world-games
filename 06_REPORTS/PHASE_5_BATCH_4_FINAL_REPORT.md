# FAZ 5 · BATCH 4 RAPORU — Kütüphaneci teslimi ve K28'in aritmetiği

> **The Great Book of World Games** · Faz 5 · Batch 4 · dal: `main`
>
> ```
> BATCH 4 ÖNCESİ :  29 / 100
> BATCH 4 SONRASI:  34 / 100
> SAYFA MODELİ   : 256 · sapma %0,0
> ```
>
> ⚠ **K28 UYGULANMADI VE UYGULANAMAZ — ARİTMETİĞİ TUTMUYOR.** Sebep § 2'de.

---

## 1 · Yazılan beş oyun

Beşi de kurucunun kütüphaneci teslimindendir.

| oyun | kültür | aile | not |
|---|---|---|---|
| **Tien Gow** | Kanton | şans | K5 uygulandı — ödeme puana çevrildi |
| **Jianzi** | Han Çinlisi | tahtasız | çember biçimi; ağ oyunu **ayrı varyant** |
| **Gomoku** | Japon | çizgi-toprak | Japon kuralı; Renju **ayrı varyant** |
| **The Royal Game of Ur** | Sümer | eve dönüş | `reconstructed` — kurallar bir **okumadır** |
| **Bao la Kiswahili** | Swahili | ekim | nyumba · kichwa · namua · mtaji korundu |

Manuscript kültür sayısı **20**'ye çıktı. Hiçbiri çift sayfayı aşmadı.

### 1.1 Varyantlar KARIŞTIRILMADI

Kurucunun § 11 ve § 13 talimatı harfiyen uygulandı:

- **Jianzi** — parktaki **işbirlikçi çember** basıldı; ağlı spor biçimi
  *"ayrı bir oyundur"* denerek varyanta kondu. İşbirlikçi oyunun başarı
  koşulu boş bırakılmadı: grup kendi rekorunu kırar.
- **Gomoku** — **Japon** kuralı basıldı (tam beş · Siyahın üç yasağı ·
  Beyazın serbestliği). **Renju** açılış protokolü ayrı varyanttır.
- **Sugoroku** yazılmadı: E-Sugoroku ile Ban-Sugoroku ayrımı batch 5'e
  bırakıldı ve **karıştırılmadı**.

---

## 2 · ⛔ K28 ARİTMETİĞİ TUTMUYOR

Kurucu 11 Şans oyununun çıkarılmasını ve 11 oyunla değiştirilmesini
onayladı. **Değiştirme listesinin dokuzu ZATEN kapsamdadır.**

| oyun | nerede |
|---|---|
| tien-gow · jianzi · sugoroku · gomoku · royal-game-of-ur · bao-la-kiswahili · mbube-mbube · astragaloi · senet | **ZATEN KAPSAMDA** |
| **achi** | yedek havuzda |
| **polis** | **projede hiç yok** |

```
100 − 11 çıkarılan + 2 eklenebilir = 91
EKSİK: 9 SLOT
```

### 2.1 Yedek havuz bu boşluğu KAPATAMAZ

Şans ailesinin dört yedeği vardır ve **üçü aynı duvara çarpar**:

| yedek | kaynak | durum |
|---|---|---|
| crown-and-anchor | Parlett 1999 | **engelli** |
| tarocchini | Parlett 1991 · Dummett 1980 | **engelli** |
| cho-han | Bell | **engelli** |
| cuarenta | Pagat (web) | erişilebilir |

Şans ailesini yedekten doldurmak, **aynı tıkanmayı yeniden üretir**.

### 2.2 Aile mimarisi de bozulur

11 oyun çıkarsa şans ailesi **15 → 4** düşer. Dokuz slotu başka
ailelerden doldurmak `family_index.json` hedeflerini **yeniden yazmayı**
gerektirir — yani yedi aile mimarisinin kendisi değişir.

> **Bu yüzden K28 UYGULANMADI.** Kurucunun § 38 kuralı açıktır:
> *"NEVER reduce scope below 100"* ve *"Do NOT silently change the final
> scope."* İkisini birden tutmanın tek yolu 9 slotu kurucunun onaylaması.
> **Bu bir karar, bir hesap değildir ve ajan tek başına veremez.**

**İyi haber:** dokuz oyun zaten kapsamda olduğu için **kapsam değişikliği
olmadan yazılabildiler**. Batch 4 tam olarak bunu yaptı.

---

## 3 · K29 · Kütüphaneci teslimi üçüncü bir dayanaktır

Proje iki durum tanıyordu: `verified` ya da yazılamaz. Kurucu teslimi
üçüncüsüdür.

```
founderSupplied         = true
independentVerification = false
bibliographyStatus      = incomplete
```

**Üretim için yeterlidir** (kurucu yetkisi) ama **`verified` değildir**.

### 3.1 Sayfa numarası UYDURULMADI

Teslim dosyası URL veriyor, **baskı ve sayfa vermiyor**. Beş kaydın
beşinde de `sourcePages` **boştur**. Doğrulayıcıyı yeşile boyamak için
künye uydurmak, kitabın tek denetlenebilir iddiasını yıkardı.

Ur ve Bao için projenin kendi **ENGELLİ** kayıtları (Finkel 2007,
de Voogt) **olduğu gibi duruyor** — maddeler o kitapların okunduğunu
iddia etmiyor.

### 3.2 Yeni kapı ve dört kasıtlı kusur

`04_BUILD/librarian_ingest.py`:

| kurgu | beklenen | sonuç |
|---|---|---|
| kurucu özetini "bağımsız doğrulanmış" göstermek | KIRMIZI | ✅ |
| künye eksikken sayfa uydurmak | KIRMIZI | ✅ |
| `founderSupplied` bayrağını silmek | KIRMIZI | ✅ |
| yinelenen kayıt | KIRMIZI | ✅ |

### 3.3 Üç kapı genişletildi, hiçbiri zayıflatılmadı

`build_queue` · `qa_rules` · `selftest` artık üçüncü dayanağı tanıyor —
ama **dayanağı olmayan** bir yazılmış oyunu hâlâ reddediyor.

### 3.4 Üç oyunun engeli KALKTI

| oyun | eskiden | çözüm |
|---|---|---|
| **jianzi** | P5 · Culin'in cildi Kore/Japon **nesnesini** anlatıyordu | **Çin** kuralları geldi |
| **tien-gow** | P5 · Culin'in cildi **Kore** dominosuydu | **Kanton** kuralları geldi |
| **gomoku** | P6 · amaç vardı, **kural seti yoktu** | tam Japon kural seti geldi |

`go` ve `sugoroku` **P5'te kaldı**: teslim onların doğru kültür kaynağını
içermiyor.

---

## 4 · GÖRSEL DENETİM BİR GEOMETRİ HATASI BULDU

v1.5'in hücre çizimi **her cell tahtasının en üst sırasını bir adım
yukarı** kaydırıyordu — yani tuvalin dışına. Ur tahtasında görüldü ve
düzeltme **bütün cell diyagramlarını** etkiledi: pachisi'nin üst kolu da
kırpıkmış ve önceki denetimlerde fark edilmemişti.

> Sayılar temizdi: 34 diyagramın hepsi bütçe içindeydi. Hata yalnızca
> **bakınca** görülüyordu — Faz 4'ün tilki dersinin dördüncü tekrarı.

Yeni diyagramlar: `ur-board` (v1.5 `omitCells` ile 3×4 blok + köprü +
3×2 blok), `gomoku-fouls`, `bao-board`.

---

## 5 · CI KIRMIZI YANDI VE DÜZELTİLDİ

Kök sebep: `librarian_delivery.json` **korumalı katmandadır** ve CI'da
yoktur; kapılar dosyayı bulamayınca beş oyunu "dayanaksız" saydı.

**Düzeltme iki katmanlıdır:** tam kayıt (kurallar) korumalı kalır, public
özet (yalnızca **kimlikler**) takip edilir, kapı korumalıyı deneyip
public'e düşer.

> Bu sınıf Faz 5'te **üçüncü kez** çıktı. Korumalı bir dosyayı CI'da
> varsayan her kapı kırmızı yanar.

Temiz klonda CI koşulları yeniden üretilerek doğrulandı.

---

## 6 · SAYFA MODELİ VE EKONOMİ

| | batch 3 | **batch 4** |
|---|---:|---:|
| Yazılmış oyun | 29 | **34** |
| Toplam sayfa | 256 | **256** |
| Sapma | %0,0 | **%0,0** ✅ |
| Taşma | 1/29 | **1/34** |
| Sürücü | both | **both** |
| Ciltsiz telif | 8,41 $ | **8,41 $** |
| Ciltli telif | 10,96 $ | **10,96 $** |

---

## 7 · KUYRUK

| P | anlamı | sayı |
|---|---|---:|
| 1 | erişilebilir · doğrulanmış · kural tam | 25 |
| 2 | erişilebilir · doğrulama tamamlanabilir | 60 |
| 3 | yeniden kurgulanmış · plan belgeli | 5 |
| 4 | telif engelli | 5 |
| 5 | kimlik/kaynak uyuşmazlığı | 3 |
| 6 | kayıt bulunamadı | 2 |

Erişilebilir ve yazılmamış: **58**.

---

## 8 · DIŞ TEST

### EXTERNAL PLAYTEST: **NOT PERFORMED** — 0 oturum · 0 kayıt · 0 `locked`

```
PRODUCTION        : AUTHORIZED
FORMAL VALIDATION : PENDING
```

`.gate` = `phase1`, yükseltilmedi.

---

## 9 · KALAN İŞ VE KURUCU KARARI

| # | konu | kimde |
|---|---|---|
| 1 | **K28'in 9 slotu** | **kurucu** — § 2 |
| 2 | Batch 5: sugoroku · mbube-mbube · astragaloi · senet · achi · polis | ajan |
| 3 | `go` için Volpicelli · `sugoroku` için Japon kaydı | kurucu |
| 4 | 66 oyun daha | kaynak arzına bağlı |
| 5 | Dış insan testi | kurucu — Faz 2'den beri |

**Batch 5 K28'i beklemez:** kalan librarian oyunları da zaten kapsamdadır
ve kapsam değişikliği olmadan yazılabilir.

---

**⛔ FAZ 6 BAŞLAMADI.** KDP'ye dokunulmadı. Ajan durmadı — batch 5 sırada.
