# EDİTORYAL MİMARİ — The Great Book of World Games

> Kitabın **yapısı**, **sayfa modeli**, **görsel sistemi** ve **aday seçim
> modeli**. Faz 1 teslimatı.
>
> Sürüm 1.0 · Faz 1 · Sayfa modeli **KALİBRE EDİLMEMİŞTİR** ve Faz 2'de
> gerçek dizgiyle ölçülür.
>
> Bu belgedeki hiçbir sayı bir betiğe gömülmez. Makine okunur karşılıkları
> `project_config.json § scope` ve `§ production.pageModel` içindedir;
> `04_BUILD/page_budget.py` ve `04_BUILD/editions.py` oradan okur.

---

## 1 · Kitabın omurgası

Kitap **bölgeye göre değil mekaniğe göre** dizilir. Bu, ürünün kendisidir:
okur "Hindistan bölümü"nü değil, *aynı fikrin sekiz kültürdeki hâlini* görür.

```
ÖN MADDE                      14 s.
│
├── Başlık · künye · içindekiler
├── Giriş denemesi — "İnsan neden oynar"
├── Bu kitap nasıl kullanılır
└── Yedi ailenin haritası — tek sayfalık tasnif şeması

GÖVDE                        214 s.
│
├── AİLE I    Ekim oyunları              2 s. açılış + 14 oyun
├── AİLE II   Av ve kuşatma              2 s. açılış + 10 oyun
├── AİLE III  Eve dönüş yarışı           2 s. açılış + 15 oyun
├── AİLE IV   Çizgi ve toprak            2 s. açılış + 14 oyun
├── AİLE V    Savaş tahtası              2 s. açılış + 17 oyun
├── AİLE VI   Şans ve cesaret            2 s. açılış + 15 oyun
└── AİLE VII  Tahtasız oyunlar           2 s. açılış + 15 oyun

ARKA MADDE                    21 s.
│
├── Tahta şablonları — fotokopiye uygun          8 s.
├── Malzeme rehberi ve yerine koyma tablosu      2 s.
├── Sözlük — 60 terim                            3 s.
├── Kaynakça — oyun başına künye                 4 s.
├── ÜÇ İNDEKS                                    3 s.
└── Uydurulmuş gelenekler kutusu                 1 s.
                                          ────────
TOPLAM (model)                                250 s.
```

> **Aile başına oyun sayıları hipotezdir.** Yukarıdaki dağılım, Faz 1'in
> ölçtüğü *uygun aday* havuzuna göre önerilmiş biçimdir (§ 6) ve kurucu
> onayı bekler (AÇIK KARAR A2/A3).

---

## 2 · Oyun maddesinin sayfa mimarisi

Her oyun **iki sayfalık bir açılıştır** (bir çift sayfa). Okur kitabı masaya
açar ve sayfa çevirmeden oynar. Bu, "bu akşam oynanabilir" vaadinin
tipografik karşılığıdır: sayfa çevirmek zorunda kalan okur, kuralı kaybeder.

```
SOL SAYFA                          SAĞ SAYFA
┌────────────────────────┐         ┌────────────────────────┐
│ OYUN ADI               │         │                        │
│ kültür · dönem         │         │   TAHTA / KURULUM      │
│                        │         │   DİYAGRAMI            │
│ ┌────────────────────┐ │         │                        │
│ │ KÜNYE ŞERİDİ       │ │         │   (gravür dilinde)     │
│ │ oyuncu · süre ·    │ │         │                        │
│ │ yaş · malzeme ·    │ │         ├────────────────────────┤
│ │ zorluk             │ │         │ tur sırası — numaralı  │
│ └────────────────────┘ │         │ kazanma koşulu         │
│                        │         │ örnek tur              │
│ kültürel hikâye        │         ├────────────────────────┤
│ ~120 kelime            │         │ VARYANTLAR             │
│                        │         │ İLK OYUNUNUZ           │
│ malzeme ve yerine      │         │ kaynak künyesi         │
│ koyma · kurulum        │         │                        │
└────────────────────────┘         └────────────────────────┘
```

Kural metninin sekiz sabit bloğu ve bunların denetimi
[`PLAYABILITY_STANDARD.md`](PLAYABILITY_STANDARD.md) § 2'dedir. Bu belge
yalnızca o blokların **sayfadaki yerini** tanımlar.

**Sığmayan oyun.** Bazı maddeler iki sayfaya sığmaz (Şogi, Mahjong,
Xiangqi). Üç çıkış yolu vardır ve seçim madde madde yapılır:
1. **Dört sayfalık madde** — sayfa bütçesinden düşülür, en fazla altı madde.
2. **Basitleştirilmiş biçim** — Go'da 9×9, Şogi'de mini-shogi. Uyarlama
   olduğu prozada söylenir.
3. **Madde düşer** — havuzda yedek vardır.

---

## 3 · Sayfa modeli

| | |
|---|---:|
| Trim (ciltsiz) | 8,5 × 11 in |
| Trim (ciltli) | 8,25 × 11 in |
| Mürekkep | siyah-beyaz (karar K3) |
| Oyun başına faturalanan sayfa | 2 |
| Gövde | 200 |
| Aile açılışları (7 × 2) | 14 |
| Ön madde | 14 |
| Arka madde | 21 |
| **Model toplamı** | **250** |
| Yol haritası hedefi | 256 |
| Sapma | −2,3 % |

Model `04_BUILD/page_budget.py` tarafından hesaplanır ve
`06_REPORTS/page-budget.json` dosyasına yazılır.

**Çapraz denetim.** İki bağımsız tahmin aynı gövdeyi vermelidir:
100 oyun × 650 kelime = 65.000 kelime; 320 kelime/sayfa varsayımıyla
≈ 203 sayfa. Sayfa modeli 200 diyor. Fark **%2** — iki tahmin aynı kitabı
tarif ediyor. Bu, modelin ilk ve tek sağlamasıdır.

> ⚠ **KALİBRE EDİLMEDİ.** 320 kelime/sayfa bir varsayımdır ve diyagram
> alanını hesaba katmaz. Gerçek değer Faz 2'de 12 oyunluk pilotun dizgisiyle
> ölçülür. Ölçüm sayfa/oyun oranını 2,5'in üstüne çıkarırsa kapsam ya da
> tasarım değişir — sayfa sayısı kapağın sırtını belirler ve geç düzeltilemez.

---

## 4 · Görsel sistem

Bu kitapta bir diyagram süs değildir: **kuralın parçasıdır.** Yanlış oyuna
bağlanmış kusursuz bir tahta diyagramı, oyunu oynanamaz yapar ve bütün
kalite kapılarından geçer (Codex dersi D6). Bu yüzden görsel envanteri
kalite ölçümünden **önce** koşar.

### Yedi görsel tipi

| Tip | Ne gösterir | Kim ister |
|---|---|---|
| `board-diagram` | Tahtanın geometrisi — nokta, çizgi, çukur | Tahtası olan her oyun |
| `setup-illustration` | Başlangıç dizilimi, taş taş | Kurulumu sözle anlatılamayan oyun |
| `move-diagram` | Bir hamlenin öncesi ve sonrası | Alma/atlama kuralı sözle belirsiz kalan oyun |
| `piece-diagram` | Taşların biçimi ve işareti | Taşları ayırt edilmesi gereken oyun |
| `map` | Oyunun coğrafi yayılımı | Aile açılışları ve taşınma anlatıları |
| `cultural-plate` | Gravür açılış levhası | Aile açılışları ve seçilmiş maddeler |
| `none` | Görsel gerekmez | Malzemesiz oyunlar |

### Yoğunluk — Faz 1 envanterinden ölçülen

Envanterdeki her kayıt hangi görselleri istediğini `visualNeeds` alanında
taşır. Öneri listesinin ölçümü:

- **Her madde en az bir görsel ister** — tahtasız oyunlar bile hareket
  diyagramı ya da kültürel levha istiyor.
- Tahta diyagramı: gövdedeki maddelerin büyük çoğunluğu.
- Kültürel gravür levhası: yedi aile açılışı + seçilmiş maddeler ≈ 30.
- Toplam üretim hedefi ≈ **130 görsel** (yol haritası Faz 5).

### Notasyon — Faz 2'de dondurulur

Diyagram dili (sembol sözlüğü, çizgi kalınlıkları, taş işaretleri)
`DIAGRAM_LANGUAGE.md` içinde **Faz 2'de** tanımlanır ve orada donar.
Gerekçe: 60. oyunda notasyon değiştirmek önceki 59 diyagramı geçersiz kılar.

**Faz 1'de üretim görseli üretilmez.** `IMAGE_PROMPT_LIBRARY.html` Faz 5
teslimatıdır; Faz 1 yalnızca *ne gerektiğini* ölçer.

---

## 5 · Arka madde ve üç indeks

Arka madde bu kitabın **en çok kullanılacak** kısmıdır ve son iş olarak
görülmez.

**Tahta şablonları (8 s.).** Fotokopiye uygun, kenar boşluklu, tam ölçekli.
8,5 × 11 trim tam da bunun için seçildi: bir ebeveyn sayfayı fotokopi
makinesine koyar ve tahtayı alır.

**Malzeme rehberi (2 s.).** Neyin yerine ne konur: yumurta kolisi ↔ mankala
tahtası, düğme ↔ taş, bozuk para ↔ atma çubuğu. Envanterdeki
`substitutionHint` alanlarından üretilir.

**Sözlük (3 s.).** 60 terim: *sowing lap*, *custodian capture*, *mill*,
*approach capture*, *stave dice*. Mekanik tasnifin dili budur ve okur bu
dili kitaptan öğrenir.

**Üç indeks (3 s.).** Ebeveyn rafta "20 dakikalık, 2 kişilik, 8 yaş" diye
arar. Kitap bu aramaya üç ayrı kapıdan cevap verir:

| İndeks | Anahtar | Kaynak alan |
|---|---|---|
| Kültüre göre | kültür → oyun | `culture` |
| Oyuncu sayısına göre | 2 · 3–4 · 5+ | `players` |
| Süre ve yaşa göre | ≤15 dk · ≤30 dk · 30+ dk × yaş | `durationMinutes` · `ageMinEstimate` |

Üçü de envanterden **üretilir**, elle yazılmaz. `qa_index.py` (Faz 4) her
oyunun üç indekste de doğru yerde olduğunu denetler.

**Uydurulmuş gelenekler kutusu (1 s.).** Kalah'ın 1940'lar Amerikan icadı
olduğu, "Chinese Checkers"ın 1892 Almanya'sından geldiği, kubb'un "Viking"
iddiasının dayanaksız olduğu, seksekin "Roma askerleri" hikâyesinin
kaynaksız olduğu burada yazar. Bir oyun kitabının okuruna verebileceği en
yararlı tek sayfa budur.

---

## 6 · Aday seçim modeli — sekiz ölçüt

`04_BUILD/score_candidates.py` bu tanımları uygular. Her ölçüt **1–5**
arasıdır ve **açıklanabilir olmak zorundadır**: bir puan, gerekçesi
yazılamıyorsa verilemez.

### Uygunluk filtresi — puandan ÖNCE

Bir oyun şu üç şartı geçmeden puanı ne olursa olsun öneriye giremez:

1. `status` ≠ `dropped`
2. `restrictionStatus` ∈ {`open`, `attributed`}
3. `playabilityStatus` ∈ {`rules-complete`, `reconstructed`}

### Sekiz ölçüt ve ağırlıkları

| Ölçüt | Ağırlık | 1 | 5 |
|---|---:|---|---|
| `playability` | **0,22** | temel bir kural bilinmiyor | beş öğe de bilinir, taze okur oynar |
| `source` | **0,18** | tek ikincil künye | ≥2 bağımsız, biri birincil ya da müze |
| `cultural` | **0,12** | anlatılacak somut ayrıntı yok | ad, nesne, bağlam ve tarih birlikte var |
| `distinct` | **0,12** | kitapta zaten sekiz benzeri var | mekaniği kitapta tek |
| `access` | **0,10** | özel malzeme şart | evdeki nesnelerle kurulur |
| `explain` | **0,10** | 650 kelimeye sığmaz | bir paragrafta öğretilir |
| `play` | **0,10** | karar yok, saf şans | her tur anlamlı bir karar |
| `visual` | **0,06** | çizilecek bir şey yok | tahtası tek bakışta okunur |

Ağırlıklar keyfî değildir: yol haritası § 1'in öncelik sırasından türer.
Oynanabilirlik önceliği 1'dir ve en yüksek ağırlığı alır; sayfa/görsel
kaygısı en düşüğünü.

### Çeşitlilik bonusu

Aynı ailede henüz temsil edilmemiş bir kültür seçim sırasında **+0,15**
alır. Bonus **ham puanı değiştirmez**, yalnızca seçim sırasını etkiler ve
raporda ayrı gösterilir. Gerekçe: alt başlık 45 kültür vaat eder ve bu vaat
`validate_spec.py`'de bir kapıdır, pazarlama süsü değildir.

### Model karar vermez

Betik bir **öneri** üretir. Nihai 100'lük liste kurucu kararıdır
(AÇIK KARAR A3). Bir modelin çıktısını karar sanmak, bu projede
yapılabilecek en pahalı hatadır.

---

## 7 · Aile hedeflerinin yeniden dengelenmesi — Faz 1 bulgusu

Faz 1 ölçtü: **av ve kuşatma ailesinde yalnızca 10 uygun aday var**, hedef
14'tü. Sebep veri hatası değil, araştırma gerçeğidir — bu ailenin
adaylarının büyük bölümü ya kuralsızdır (tafl kümesi) ya tek kaynaklıdır
(kaplan-keçi kümesi).

`score_candidates.py` şu yeniden dengelemeyi **önerir**:

| Aile | Mevcut hedef | Önerilen |
|---|---:|---:|
| Av ve kuşatma | 14 | **10** |
| Savaş tahtası | 13 | **17** |
| *(diğer beş aile)* | *değişmez* | *değişmez* |

Toplam 100 korunur. Gerekçe: savaş tahtası ailesinde 20 uygun aday vardır
ve satranç akrabalarının çeşitliliği kitabın en güçlü karşılaştırma
tablosunu üretir.

**Karşı gerekçe de kayda geçer:** av-kuşatma ailesini küçültmek, kitabın en
görsel ve en çocuk-dostu ailesini zayıflatır. Alternatif, hedefi korumak ve
Faz 2'de dört kaplan-keçi oyununa ikinci bağımsız kaynak aramaktır.

**Karar kurucunundur (A2).** Bu belge iki yolu da yazar; birini seçmez.

---

## 8 · Bu mimarinin bilmediği şeyler

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| Kelime/sayfa gerçek değeri | Faz 2 · gerçek dizgi |
| Diyagramın kapladığı gerçek alan | Faz 2 · gerçek dizgi |
| Şogi/Mahjong iki sayfaya sığar mı | Faz 2 · pilot en zorları seçer |
| Diyagram notasyonu POD baskıda okunuyor mu | Faz 5 · prova kopya |
| Arka madde 21 sayfaya sığar mı | Faz 4 · arka madde yazıldığında |
