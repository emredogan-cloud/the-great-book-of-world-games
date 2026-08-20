# PROJECT CONTEXT — The Great Book of World Games

> **Bu dosya, projeye yeni giren her ajanın ve her insanın okuyacağı ilk
> belgedir.** Hafızası olmayan bir ajan buradan başlar ve projenin nerede
> olduğunu, neyin kilitli neyin açık olduğunu buradan öğrenir.
>
> Son güncelleme: **20 Ağustos 2026** · Faz: **6 · TAMAMLANDI** · Kapı: `phase1`

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

> ⚠ **FAZ 6 TAMAMLANDI · KDP YÜKLEMESİ KURUCUYU BEKLİYOR.**
>
> ```
> PHASE 6      : COMPLETE (technically executable work)
> INTERIOR     : READY  · 160 sayfa · ciltsiz + ciltli + EPUB
> COVER        : BLOCKED · kurucu sanatı yok
> A+           : BLOCKED · dokuz görsel yok
> PUBLISHED    : NO
> ```

| | |
|---|---|
| Faz | **6 · TAMAMLANDI** — ajan DURDU |
| Kapı (`.gate`) | **`phase1`** — yükseltilmedi |
| Kilitli kapsam | **100 oyun · 68 kültür** (şerhler A1–A3) |
| **Yazılmış oyun** | **56** / 100 |
| Kültür · bölge · aile | **39** · 22 · 7 |
| `reconstructed` madde | 7 (yedisinin de beyanı var) |
| Doğrulama kaydı | **74** · `verified` **55** · uydurulmuş künye **0** |
| **Basılan sayfa** | **160** (SAYILDI) · ciltsiz 8,5×11 · ciltli 8,25×11 |
| **Basılan kelime** | **65.395** |
| Çift sayfa sözü | **56 / 56 madde SOL sayfada başlıyor** |
| Sırt | ciltsiz **0,3603 in** · ciltli **0,4600 in** |
| Birim telif (160 s.) | ciltsiz **10,07 $** · ciltli **12,62 $** · Kindle 7,19 $ |
| Diyagram | **51 render · 51'i gözle denetlendi** · dil v1.5 |
| Ön madde + aile açılışları | **YAZILDI** (2.039 + 2.415 kelime) |
| Kindle | **EPUB 3 · reflowable** · 50 diyagram satır içi SVG |
| A+ | metin **hazır** · görsel **yok** |
| Selftest | **192** denetim ✅ |
| **Paket kapılarının testi** | **37 kasıtlı kusurun 37'si yakalandı** ✅ |
| Yerel kapılar | `qa_all.sh` → **HEPSİ YEŞİL** |
| CI | temiz klonda **simüle edildi ve YEŞİL** · ⛔ **push YAPILMADI** |
| **Sonraki adım** | **KURUCU: kapak sanatı · A+ görselleri · yazar biyografisi · AI beyanı · dış test** |

Faz raporları: [`06_REPORTS/PHASE_6_FINAL_REPORT.md`](06_REPORTS/PHASE_6_FINAL_REPORT.md) ·
[`06_REPORTS/PHASE_5_REPORT.md`](06_REPORTS/PHASE_5_REPORT.md) ·
[`06_REPORTS/FINAL_WRITING_PHASE_CLOSURE.md`](06_REPORTS/FINAL_WRITING_PHASE_CLOSURE.md)

**Faz 6 kitabı BASILABİLİR hâle getirdi ve dört oyun daha açtı.** Kurucunun
teslim ettiği Murray 1952 sayfa seviyesinde tarandı; boşluk kaydı o eseri
"denendi ve açılamadı" diye tutuyordu ve bu, teslimden sonra doğru değildi.
Alquerque, Ashta Kashte, Rimau-rimau ve Go yazıldı (52 → 56); yazılmayan
sekiz aday için gerekçe **tahmin değil ölçüm** olarak kayda geçti.

**Faz 6'nın en değerli çıktısı yine bir düzeltmeler kümesidir** — hepsi
sayısal kapılar YEŞİLKEN bulundu:

- **65 Türkçe efsane etiketi** İngilizce kitabın diyagramlarında basılacaktı.
  İkisinde Türkçeye özgü **tek bir harf yok**tu, yani aksan taraması da kördü.
- **Üç gömülmemiş font** (Helvetica · Times-Roman · ZapfDingbats) — KDP üçünü
  de reddederdi.
- **Baskı fontunda olmayan bir efsane sembolü** (U+2312): sayfada yer boş
  kalacaktı.
- **`mbube-formation` diyagramı "buffalo" diyordu**; oyunda impala vardır.
- **Bir künye hatası**: "folio 916" — Murray'in sayfası render edilip okundu,
  metin "(Alf. 91b)" diyor.
- **CI 51 diyagramın 33'ünü hiç görmüyordu**: Faz 4 ve 5 tanımlayıcılarını
  izin listesine eklememişti. Bakacak dosyası olmayan bir kapı yeşil yanar.
- **BOOK_STATS beş fazdır "Yazılmış oyun 0" diyordu**; sayıyı envanterin
  `status` alanından okuyordu ve orada asla yazmayacaktı.

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
| [`06_REPORTS/FOUNDER_DELIVERY_INTAKE_REPORT.md`](06_REPORTS/FOUNDER_DELIVERY_INTAKE_REPORT.md) | Teslim edilen her dosyanın **gerçekte ne olduğu** · sağlama toplamları | teslim başına |
| [`06_REPORTS/FINAL_WRITING_COMPLETION_REPORT.md`](06_REPORTS/FINAL_WRITING_COMPLETION_REPORT.md) | Yazım fazının **ölçülen** durumu · nihai kapsam kararı | batch başına |
| [`06_REPORTS/FINAL_WRITING_PHASE_CLOSURE.md`](06_REPORTS/FINAL_WRITING_PHASE_CLOSURE.md) | **Yazım fazı kapanışı** · nihai kapsam · yedek havuz ölçümü | faz sonu |
| [`06_REPORTS/FINAL_SOURCE_AUDIT.md`](06_REPORTS/FINAL_SOURCE_AUDIT.md) | Her maddenin künye · kültür · kurgulama denetimi | faz sonu |

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
> Faz 6 **bitti**. Kurucu nihai kapak ve A+ sanatını teslim etti; üçü de
> üretildi ve doğrulandı: ciltsiz · ciltli · Kindle. `main` temiz,
> `origin/main` ile eşit, **CI yeşil**. Önceki fazda engellenen push bu
> fazda **denendi ve geçti** (`9441ec1..887a97e`).
>
> **Yüklemeyi BLOKLAYAN iki madde kaldı** ve ikisi de ajanın
> üretemeyeceği şeylerdir:
>
> 1. **AI beyanı** hukuki bir bildirimdir ve kurucunundur. Karar için
>    gereken olgular `08_OUTPUT/KDP_AI_DISCLOSURE_NOTES.md` içinde hazır;
>    **beyanın kendisi yazılmadı ve uydurulmadı.**
> 2. **Dış oynanabilirlik testi: 0 oturum.** Bu blok Faz 2'den beri aynı
>    yerde duruyor ve kitabın alt başlığındaki sözü ölçen tek kanıttır.
>
> **Bloklamayanlar:** APLUS-05 sanatı (A+ projesi 5 modülle yüklenebilir) ·
> ISBN ×2 (KDP atar; hiçbir yerde uydurulmadı) · ciltli şablon doğrulaması
> (sırt formülü **hipotez**) · KDP Previewer.
>
> **Kapsam kararı — kurucuya ait.** `release` kapısı **≥100 kilitli oyun**
> ister; kitapta **56** var ve bu sayı her ticari yüzeyde dürüstçe duruyor.
> Kapı bilerek kırmızıdır. Ya eşik 56'ya çekilir (Faz 6 kapanır) ya da 100
> hedefi korunur (Faz 7 açılır, 44 oyun için kaynak gerekir). **Ajan
> hiçbirini seçmedi** — seçmek kapsamı değiştirmektir.
> Gerekçeler: `06_REPORTS/PHASE_6_BRUTAL_AUDIT.md § 6`.
>
> Açık kurucu kararları: **A4** (büyük punto) · **A5** (`STYLE.md` bandı) ·
> **A8** (kapsam eşiği). **A6 KAPANDI** — biyografi kardeş projeden birebir
> kopyalandı (`06_REPORTS/AUTHOR_BIO_PROVENANCE.md`).
