# PROJECT CONTEXT — The Great Book of World Games

> **Bu dosya, projeye yeni giren her ajanın ve her insanın okuyacağı ilk
> belgedir.** Hafızası olmayan bir ajan buradan başlar ve projenin nerede
> olduğunu, neyin kilitli neyin açık olduğunu buradan öğrenir.
>
> Son güncelleme: **14 Ağustos 2026** · Faz: **4 · ÜRETİM AÇIK** · Kapı: `phase1`

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
| Faz | **4 · ÜRETİM ŞERİDİ AÇIK** (koşullu · K21) |
| Kapı (`.gate`) | **`phase1`** — yükseltilmedi ve yükseltilmeyecek |
| Kilitli kapsam | **100 oyun · 71 kültür · 19 yedek** ✅ |
| **Yazılmış oyun** | **22** / 100 |
| Kilitli oyun | **0** / 100 |
| Doğrulanmış künye | **28** (25 oyunda ≥1, 3 oyunda ≥2) |
| Kaynak: denendi-erişilemedi | **5** oyun |
| Kaynak: henüz denenmedi | **70** oyun |
| **Erişilebilir · yazılmamış** | **72** oyun — kuyrukta sıralı |
| **Dış oynanabilirlik testi** | **0** ⛔ **BLOKLAYICI** |
| Diyagram | **27 render · hepsi ≤150 mm** ✅ |
| **Oyun başına diyagram** | **azami 144,0 mm** ✅ (Faz 4'te kapıya bağlandı) |
| Diyagram dili | **v1.4** (`bodily/bed` — zemine çizilen bölmeler) |
| **Sayfa modeli** | **258** (hedef 256, **+%0,8**) ✅ **BANTTA** |
| Selftest | **148 denetim** ✅ |
| Depo | public · `faz/4-blok-2` · CI **YEŞİL** |
| **Sonraki adım** | **KURUCU: dış test + kaynak erişimi + § 20.1 kapsam kararı** |

Faz raporları: [`06_REPORTS/PHASE_2_REPORT.md`](06_REPORTS/PHASE_2_REPORT.md) ·
[`06_REPORTS/PHASE_3_REPORT.md`](06_REPORTS/PHASE_3_REPORT.md) ·
[`06_REPORTS/PHASE_4_REPORT.md`](06_REPORTS/PHASE_4_REPORT.md)

**Faz 4'ün en önemli çıktısı yine bir düzeltmedir:** Faz 2'nin
*"sayfa bütçesi bir diyagram bütçesidir"* cümlesi **yanlışlandı**. Üç
oyunda metin farkı 0,01'di ve metin sabit sanıldı; yirmi iki oyunda 0,69
oldu ve diyagram farkını (0,63) **geçti**. Cümle bir bulgu değil bir
**örneklem eseriydi** ve `calibrate_pages.py` içine gömülü olduğu için
verisini yalanlarken bile basılmaya devam ediyordu. Artık ölçümden
türetiliyor.

Faz 4 ayrıca **beş kapı kusuru** buldu — beşi de gerçek veriyle yeşil
koşan kapılardaydı. En sertleri: 150 mm bütçesi **oyun başına** tanımlı
olduğu hâlde **diyagram başına** denetleniyordu (tablut 181,5 mm ile
geçiyordu), ve `fivestones` maddesinin **kurulum bloğu yoktu**.

⚠ **FAZ 4 KAPSAMI TAMAMLANMADI.** Yazılan 22, hedef 100. Üç sert
bloklayıcı sürüyor:

1. **Dış insan testi yapılmadı.** Ajan test yapamaz; sahte kayıt
   üretilmez. Paket hazır (`01_SOURCE/pilot_tr/`), oturum kurucunundur.
2. **Telifli kaynaklara erişim.** Beş oyun denendi ve erişilemedi.
   Ama **72 oyun erişilebilir** ve yalnızca sıra bekliyor — bu sayı
   Faz 3'te 20 görünüyordu ve düzeltildi (K22).
3. **Arka madde yazılmadı** — üç indeks, sözlük, tahta şablonları.

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
> A1 · A2 · A3 · A7 kapandı (K12–K15). Faz 4 on bir oyun yazdı, beş kapı
> kusuru buldu, sayfa modelini 258'e indirdi ve durdu.
>
> **Üretim ilerleyebilir: 72 erişilebilir oyun kuyrukta sıralı bekliyor.**
> Kaynak erişimi bir tıkanma değil bir hız sınırıdır — engelli olan
> yalnızca **5** oyundur.
>
> Bekleyen üç BLOKLAYICI:
> 1. **Dış oynanabilirlik test oturumları.** Paket `01_SOURCE/pilot_tr/`
>    içinde hazır: üç oyun, testçi kılavuzu, kayıt formu. Ajan bu adımı
>    yapamaz ve sahte kayıt üretmez. **Bu blok Faz 2'den beri aynı yerde.**
> 2. **Telifli kaynaklara erişim.** Murray (1913/1952) · Bell (1960) ·
>    Parlett (1999) · de Voogt (1997) · Zaslavsky (1973) · Finkel (2007)
>    açık tam metin değil. Beş oyun bunlara bağlı.
> 3. **Arka madde** — üç indeks, sözlük, tahta şablonları — yazılmadı.
>
> Bir KARAR bekliyor: **tahtasız ailenin kültür dengesi ve
> gonggi/fivestones mekanik çakışması** (PHASE_4_REPORT § 20.1). Yedek
> havuzdan iki değişiklik ikisini birden çözer; bir **scope amendment**
> gerektirir ve ajan yapamaz.
