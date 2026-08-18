# PROJECT CONTEXT — The Great Book of World Games

> **Bu dosya, projeye yeni giren her ajanın ve her insanın okuyacağı ilk
> belgedir.** Hafızası olmayan bir ajan buradan başlar ve projenin nerede
> olduğunu, neyin kilitli neyin açık olduğunu buradan öğrenir.
>
> Son güncelleme: **14 Ağustos 2026** · Faz: **5 · ÜRETİM AÇIK** · Kapı: `phase1`

---

## 1 · Proje kimliği

| | |
|---|---|
| Başlık | **The Great Book of World Games** |
| Alt başlık (hipotez) | 100 Games from 5,000 Years of Human Play — Rules, Boards, and Stories from 45 Cultures, Ready to Play Tonight |
| Seri | **"The Great Book of…"** · Cilt 2 |
| Depo | `emredogan-cloud/the-great-book-of-world-games` |
| Kitle | Aile (yetişkin + 8 yaş üstü çocuk birlikte) · hediye alıcısı · öğretmen |
| Kaynak | `AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html` § 11 · Kitap A |
| Portföy yeri | **Kitap A · ilk yazılacak** · yeni kitle motoru |


> **Pazar raporu bu depoda DEĞİLDİR.** `AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html`
> kurucunun çalışma dizininde duran **özel bir strateji belgesidir** ve üç
> public depoya kopyalanmaz. Bu belgede ona **künyeyle** atıf yapılır, bağ
> verilmez: bir depoyu klonlayan kişi o dosyaya ulaşamaz ve kırık bir bağ
> görmemelidir.

---

## 2 · Amaç

İnsanlığın oyun mirasını **bölgeye göre değil mekaniğe göre** tasnif eden,
kaynak künyeli ve **gerçekten oynanabilir** bir başvuru cildi üretmek.

Pazar gerekçesi: 2026 H1'de yetişkin kurgu-dışının 16 alt kategorisinden
yalnızca ikisi büyüdü ve biri **el işi / hobi / oyun (+%9,6)**. Raf ikiye
ayrılmış — akademik oyun tarihi (oynanamaz) ve jenerik aile oyunu listeleri
(içeriksiz). **Arada hiçbir şey yok.**

---

## 3 · Bu proje ne DEĞİLDİR

| Değildir | Neden |
|---|---|
| *Bir oyun tarihi monografisi* | Okur oynamak istiyor, okumak değil. Tarih **çerçevedir**, ürün değil |
| *Bir aile aktivite listesi* | Kaynak künyesi ve tasnif tezi ürünün kendisidir |
| *Codex serisinin üçüncü cildi* | Ayrı seri, ayrı kitle, ayrı raf. Codex rafı iki ciltle **tutuldu** |
| *Bestiarium'un oyunlara uyarlanmış hâli* | Tez ortaktır (yapıya göre tasnif), **kitap yeni bir yazımdır** |

---

## 4 · Şu anki durum

> ⚠ **ÜRETİM AÇIK · RESMÎ KAPI KAPALI.** İkisi ayrı şeylerdir ve bu
> ayrım kasıtlıdır (kararlar K18 · K21). Kurucu Faz 4 üretim işini de
> yetkilendirdi; resmî faz kapısı **yalnızca gerçek kanıtla** açılır.
>
> ```
> PRODUCTION       : AUTHORIZED
> FORMAL VALIDATION: PENDING
> ```

| | |
|---|---|
| Faz | **5 · ÜRETİM ŞERİDİ AÇIK** (koşullu · K21 · A10) |
| Kapı (`.gate`) | **`phase1`** — yükseltilmedi ve yükseltilmeyecek |
| Kilitli kapsam | **100 oyun · 73 kültür · 19 yedek** ✅ (K23 şerhli) |
| **Yazılmış oyun** | **23** / 100 ⛔ |
| Kilitli oyun | **0** / 100 |
| Doğrulanmış künye | **31** · doğrulama kaydı **51** |
| Kaynak: denendi-erişilemedi | **5** oyun (P4) |
| Kaynak: arandı-kayıt yok | **2** oyun (P6 · K23 terfileri) |
| Kaynak: henüz denenmedi | **69** oyun |
| **Erişilebilir · yazılmamış** | **72** oyun — kuyrukta sıralı |
| **K24 istisnası** | cats-cradle · kayıtlı + dört testle kilitli |
| **Dış oynanabilirlik testi** | **0** ⛔ **BLOKLAYICI** |
| Diyagram | **26 render · hepsi tavan içinde** ✅ |
| **Oyun başına diyagram** | **azami 144,0 mm** ✅ |
| Diyagram dili | **v1.4** |
| **Arka madde** | **ALTI BÖLÜM TAM** ✅ · üç indeks üretildi |
| **Sayfa modeli** | **258** (hedef 256, **+%0,8**) ✅ **BANTTA** |
| Birim telif | ciltsiz **8,41 $** · ciltli **10,96 $** |
| Selftest | **177 denetim** ✅ |
| Depo | public · `main` · CI **YEŞİL** |
| **Sonraki adım** | **KURUCU: kaynak erişimi · dış test · diyagram dili v1.5** |

Faz raporları: [`06_REPORTS/PHASE_2_REPORT.md`](06_REPORTS/PHASE_2_REPORT.md) ·
[`06_REPORTS/PHASE_3_REPORT.md`](06_REPORTS/PHASE_3_REPORT.md) ·
[`06_REPORTS/PHASE_4_REPORT.md`](06_REPORTS/PHASE_4_REPORT.md) ·
[`06_REPORTS/PHASE_5_REPORT.md`](06_REPORTS/PHASE_5_REPORT.md)

**Faz 5 kendi ana hedefini tutturamadı ve bunu gizlemiyor.** Hedef 100
oyundu; yazılan **23**'tür. Faz iki koşuda çalıştı: birincisi kapsam
değişikliğini, arka maddeyi ve altı kapı kusurunu tamamladı ama **hiç oyun
yazmadı**; ikincisi K24 istisnasını kurdu ve **üç oyun yazdı**
(cats-cradle · shogi · pachisi).

**Faz 5'in en değerli çıktısı yine bir düzeltmedir** — yedi kapı kusuru,
yedisi de gerçek veriyle **yeşil koşuyordu**. En sertleri:

- `scope_lock.json`'ın başlığı *"model ayrışırsa bu KAPI ISIRIR"* diye
  **vaat ediyordu**; öyle bir denetim **hiç yazılmamıştı**.
- **Bir tane** şerh, kilit özetinin denetimini **ömür boyu** kapatıyordu.
- Kapsamdan **çıkarılmış** bir oyun **basılmaya devam edebiliyordu**.
- Kalibre config ölçümden kayınca **ekonomi eski sayıyla** hesaplanıyordu.
- Efsanedeki iki sembol **birebir aynı** çizilebiliyordu — beş diyagramda
  bulundu, biri **Faz 3'ten beri basılıydı**.

⚠ **KALAN 77 OYUN BİR YAZIM İŞİ DEĞİL, ÖNCE BİR KAYNAK İŞİDİR.** Faz 5 on
kaynak açtı ve **yedisi kural taşımıyordu**: Culin'in *Korean Games* cildi
Çin ve Japon oyunlarına yalnızca **karşılaştırma notu** verir (xiangqi ·
tien-gow · jianzi · sugoroku), Fiske filolojidir (hnefatafl · halatafl),
Culin'in mancala'sı Şam ve Vei kayıtlarıdır (oware), ve Smith'in go
kitabı **Japon** kodifikasyonudur — kapsam ise **Han Çinlisi** der.

## 5 · Bu projenin risk profili

Her kitabın kendine has bir ölüm biçimi vardır. World Myths'inki *yaş
uygunluğuydu*. Bestiarium'unki *illüstrasyon tutarlılığıydı*.

**Bu kitabınki: OYUN ÇALIŞMIYOR.**

Okur masaya oturur, kuralı okur ve oynayamaz. Bu tek kusur alt başlıktaki
vaadi — *Ready to Play Tonight* — doğrudan yalanlar ve o yorum silinmez.

Öncelik sırası — çakışmada yukarıdaki kazanır:

1. **Oynanabilirlik**
2. Kültürel doğruluk ve kısıt taraması
3. Kaynak izlenebilirliği
4. Diyagram doğruluğu
5. Okunabilirlik ve anlatı keyfi
6. Sayfa / kelime bütçesi
7. Üretim hızı

**Sayfa sayısı hiçbir zaman ilk dördünü ezmez.**

---

## 6 · İzolasyon kuralı

Bu depo `CODEX_BESTIARIUM`, `THE-GREAT-BOOK-OF-WORLD-MYTHS`,
`THE-MYTH-HUNTERS-FIELD-BOOK` ve `CODEX-ENIGMATICA`'dan **tamamen ayrıdır**.

- Onların dosyaları **değiştirilmez**
- Ortak dosya, ortak build çıktısı, ortak rapor, ortak `.gate` **yoktur**
- Bu depodaki hiçbir betik başka bir projeye yazmaz
- Kardeş dizinde bulunmaları **zorunlu değildir**; bu proje onlarsız çalışır

Okunan dersler: [`00_CONTEXT/LESSONS_FROM_CODEX.md`](00_CONTEXT/LESSONS_FROM_CODEX.md)

---

## 7 · Altı faz — özet

| Faz | Ad | Yazım | Kapı |
|---|---|---|---|
| 1 | Envanter, tasnif ve oynanabilirlik mimarisi | yok | `phase1` |
| 2 | Pilot: 12 oyun + kalibrasyon | ~7.800 kelime | `phase2` |
| 3 | Üretim bloğu I — Aileler I–IV | ~28.000 | `phase3` |
| 4 | Üretim bloğu II — Aileler V–VII + arka madde | ~29.000 | `phase4` |
| 5 | Editoryal yakınsama + görsel üretim | ~13.000 | `phase5` |
| 6 | Nihai üretim + KDP paketi | yok | `release` |

Tam yol haritası: [`THE_GREAT_BOOK_OF_WORLD_GAMES_IMPLEMENTATION_ROADMAP.md`](THE_GREAT_BOOK_OF_WORLD_GAMES_IMPLEMENTATION_ROADMAP.md)

---

## 8 · Belge haritası

| Belge | Ne söyler | Kim değiştirir |
|---|---|---|
| [`THE_GREAT_BOOK_OF_WORLD_GAMES_IMPLEMENTATION_ROADMAP.md`](THE_GREAT_BOOK_OF_WORLD_GAMES_IMPLEMENTATION_ROADMAP.md) | **Tek doğruluk kaynağı** — altı faz, kapılar, DoD | kurucu onayıyla |
| [`BRIEF.md`](BRIEF.md) | Ürün, kitle, konumlanma, ticari model | kurucu |
| [`00_CONTEXT/PLAYABILITY_STANDARD.md`](00_CONTEXT/PLAYABILITY_STANDARD.md) | **Oynanabilirlik sözleşmesi** | kurucu onayıyla |
| [`00_CONTEXT/SOURCING_STANDARD.md`](00_CONTEXT/SOURCING_STANDARD.md) | Neyin kaynak sayıldığı · kısıt taraması | kurucu onayıyla |
| [`00_CONTEXT/EDITORIAL_ARCHITECTURE.md`](00_CONTEXT/EDITORIAL_ARCHITECTURE.md) | Kitabın yapısı · sayfa modeli · görsel sistem · **seçim modeli** | Faz 1'de yazıldı |
| [`01_SOURCE/family_index.json`](01_SOURCE/family_index.json) | **Yedi aile · sınır kuralları · tasnif yordamı** | kurucu onayıyla |
| `01_SOURCE/games/family-*.json` | Aday kayıtları — **elle yazılır** | her faz |
| `01_SOURCE/game_index.json` | Birleştirilmiş envanter — **üretilir** | `build_index.py` |
| [`00_CONTEXT/STYLE.md`](00_CONTEXT/STYLE.md) | Ses, ritim, kural dili, yasak kalıp | Faz 2'de kalibre |
| [`00_CONTEXT/LESSONS_FROM_CODEX.md`](00_CONTEXT/LESSONS_FROM_CODEX.md) | Taşınan disiplin ve nedenleri | sabit |
| [`DECISIONS.md`](DECISIONS.md) | Alınmış kararlar + **AÇIK KARARLAR** | her faz |
| [`CHANGELOG.md`](CHANGELOG.md) | Ne zaman ne değişti, neden | her faz |
| [`BOOK_STATS.md`](BOOK_STATS.md) | Ölçülen sayılar | **üretilir** |
| [`ROADMAP_PROGRESS.md`](ROADMAP_PROGRESS.md) | Faz ilerlemesi | **üretilir** |
| `project_config.json` | Makine okunur tek doğruluk kaynağı | kurucu onayıyla |
| [`06_REPORTS/FOUNDER_RESEARCH_GAP_REGISTER.md`](06_REPORTS/FOUNDER_RESEARCH_GAP_REGISTER.md) | **Yazılamayan her oyun** · engel sınıfı · kurucunun tam olarak neyi araması gerektiği | **üretilir** |
| [`06_REPORTS/FOUNDER_RESEARCH_PACK.md`](06_REPORTS/FOUNDER_RESEARCH_PACK.md) | Aynı kayıt **kaynağa göre** — insan araştırmacı için çalışma paketi | **üretilir** |
| `01_SOURCE/founder_research_gap_register.json` | Kaydın makine okunur biçimi | `build_gap_register.py` |
| [`06_FOUNDER_DELIVERY/README.md`](06_FOUNDER_DELIVERY/README.md) | Teslim biçimi ve alım hattı | sabit |

---

## 9 · Bir ajan işe nasıl başlar

```bash
cd THE-GREAT-BOOK-OF-WORLD-GAMES

# 1. Nerede olduğumu öğren
cat .gate                            # aktif faz kapısı
cat ROADMAP_PROGRESS.md              # ilerleme
grep -n "AÇIK KARAR" DECISIONS.md    # kurucudan yanıt bekleyenler

# 2. Kapıları çalıştır — yeşilse CI de yeşil olur
./04_BUILD/qa_all.sh

# 3. Yol haritasının O fazına bak, YALNIZCA o fazın işini yap
```

**Kural:** kapı seviyesi `.gate`ten okunur, tahmin edilmez. Bir faz
kapanmadan sonrakine geçilmez. CI kırmızıyken hiçbir şey ilerlemez.

---

## 10 · Açık bağımlılıklar

| # | Ne | Kimden | Ne zaman |
|---|---|---|---|
| A1 | Manuscript public depoda mı duracak? | kurucu | **Faz 1 başlamadan** |
| A2 | 7 aile taksonomisi onayı | kurucu | Faz 1 sonu |
| A3 | 100 oyunun nihai listesi | kurucu | Faz 1 sonu |
| A4 | Büyük punto sürümü | kurucu | Faz 4 |
| A5 | Kalibre edilmiş `STYLE.md` onayı | kurucu | Faz 2 |
| A6 | Yazar biyografisi metni | kurucu | Faz 5 |
| — | **2 oyun testçisi** | kurucu | Faz 2'den itibaren |
| — | ~130 görselin üretilmesi | kurucu | Faz 5 |
| — | KDP paneli işlemleri | kurucu | Faz 6 sonrası |

---

## 11 · Sonraki izinli eylem

> **KURUCU EYLEMİ BEKLENİYOR — onay değil, EYLEM.**
>
> Faz 5 kapsam değişikliğini (K23), arka maddeyi ve altı kapı kusurunu
> tamamladı; **oyun yazımını tamamlayamadı: 20/100.**
>
> Bekleyen dört BLOKLAYICI:
>
> 1. **80 oyun yazılmadı.** Faz 5 beş oyunun kaynağını sayfa seviyesinde
>    açtı ve beşi de yazılamaz çıktı. Bu küçük bir örneklemdir ama
>    "erişilebilir" sayılan 92 oyunun bir bölümünün **kural taşımayan**
>    kaynaklara bağlı olabileceğini gösteriyor.
> 2. **Dış oynanabilirlik test oturumları.** Paket `01_SOURCE/pilot_tr/`
>    içinde hazır. Ajan bu adımı yapamaz ve sahte kayıt üretmez.
>    **Bu blok Faz 2'den beri aynı yerde.**
> 3. **cats-cradle · 150 mm çatışması.** Kaynak (Jayne 1906, ss. 324–338)
>    **tam ve sayfa-doğrulanmış**; sekiz figür oyun başına 150 mm tavanına
>    sığmıyor. Üç seçenek `source_access_pending.json § editorialHolds`
>    içinde. **Kurucu kararı gerekir.**
> 4. **Telifli kaynaklara erişim.** Beş oyun engelli (P4). Ayrıca iki
>    oyun (lagori · kho-kho) **P6**'dadır: kaynakları arandı ve
>    denetlenebilir bir kayıt **bulunamadı** — bu bir erişim engeli
>    değildir ve kütüphane kartıyla açılmaz.
>
> Açık kurucu kararları: **A4** (büyük punto) · **A5** (`STYLE.md` onayı) ·
> **A6** (yazar biyografisi).
