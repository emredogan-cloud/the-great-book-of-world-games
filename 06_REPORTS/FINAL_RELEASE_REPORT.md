# NİHAİ YAYIN RAPORU

**The Great Book of World Games** · Vâliçe Press · 2026
**Durum:** kurucu teslimine hazır — **yayınlanmadı**
**commit:** `887a97e` · **CI:** yeşil · 20 Ağustos 2026

> Yol haritası § Faz 6 · Teslimat listesi bu dosyayı istiyor. Ne üretildiğini,
> neyin doğrulandığını ve **neyin hâlâ kurucuya bağlı** olduğunu tek sayfada
> toplar. Ayrıntılı bulgular: [`PHASE_6_BRUTAL_AUDIT.md`](PHASE_6_BRUTAL_AUDIT.md).

---

## 1 · Kitap

| | |
|---|---|
| oyun | **56** — hepsi kaynağa bağlı, hiçbiri uydurma |
| kültür | 39 |
| oyun ailesi | 7 |
| yeniden kurgulanmış kural | 7 — **prozada açıkça işaretli** |
| en eski oyun | MÖ 2600 (Ur Kraliyet Oyunu) |
| basılan sayfa | **160** — sayıldı, tahmin edilmedi |
| çıkarılan kelime | 65.419 |
| diyagram | 51 · hepsi vektör SVG, veriden deterministik çizilir |

> **56, 100 değildir.** Kapsam modeli 100 oyun öngörüyordu; 56'sı için kaynak
> açılabildi. Kalan 44 **yazılmadı ve var gibi gösterilmedi**. Ticari her
> yüzeyde yazan sayı 56'dır.

---

## 2 · Üretilen dosyalar

**Ciltsiz** — 8.25 × 11.00 in

| dosya | boyut | sha256 |
|---|---|---|
| `GreatBookOfWorldGames_interior_paperback.pdf` | 506.0 KB | `474eda034194` |
| `GreatBookOfWorldGames_cover_paperback.pdf` | 20.2 MB | `93ce1c389e79` |

sırt **0.3603 in** (160 × 0.002252) · sarım 17.6103 × 11.2500 in

**Ciltli** — 8.25 × 11.00 in

| dosya | boyut | sha256 |
|---|---|---|
| `GreatBookOfWorldGames_interior_hardcover.pdf` | 506.5 KB | `855adcacf16b` |
| `GreatBookOfWorldGames_cover_hardcover.pdf` | 19.4 MB | `f6972c22fe9d` |

sırt **0.4600 in** (160 × 0.0025 + 0.06 tahta) · sarım 17.2100 × 11.2500 in

> Ciltli sırt geometrisi ciltsizden **türetilmedi**. Ayrı formül, ayrı tahta
> payı. Ama formül **hipotezdir**: KDP şablonuyla karşılaştırılması bir
> kurucu eylemidir.

**Kindle**

| dosya | boyut | sha256 |
|---|---|---|
| `GreatBookOfWorldGames.epub` | 925.5 KB | `ba916ec1449f` |
| `GreatBookOfWorldGames_cover_kindle.jpg` | 713.5 KB | `5f68c2b4e16b` |

EPUB 3 akışkan · 75 belge · 50 SVG diyagram · kapak gömülü (EPUB 3 + EPUB 2)

> Kindle kapağı **ön panelden** türetildi (1600 × 2560), baskı sarımından
> kırpılarak değil.

**A+ içerik** — `08_OUTPUT/APLUS/` · 8 işlenmiş PNG + `aplus_content.json`
**5 / 6 modül yüklenebilir.** APLUS-05'in sanatı teslim edilmedi.

**Kurucu belgeleri** — `KDP_UPLOAD_HANDBOOK.md` · `KDP_PREVIEWER_CHECKLIST.md`
· `KDP_AI_DISCLOSURE_NOTES.md`

Dört dizinin dördünde `SHA256SUMS` var ve **doğrulandı**.

---

## 3 · Doğrulama

| kapı | sonuç |
|---|---|
| `qa_all.sh` | ✅ bütün kapılar yeşil |
| `selftest.py` | ✅ **214** denetim |
| `package_selftest.py` | ✅ **39 kasıtlı kusurun 39'u yakalandı** |
| `kdp_preflight.py` | ✅ 20 denetim |
| `ci_simulate.py` | ✅ 22/22 adım — tam bağımlılık **ve** bağımlılıksız |
| GitHub Actions | ✅ yeşil |

**Ölçülen değerler**

- gömülü font: 4 yüz, hepsi altkümelenmiş · gömülü olmayan kaynak **yok**
- en dar mürekkep payı: 0.486 in (KDP asgarisi 0.25)
- güvenli alan ihlali: **0** — kapaktaki her metin parçasının kutusu kayıtlı
- daktilo tırnağı: **0** — dört çıktının dördünde
- çift sayfa mimarisi: 56 maddenin 56'sı **sol (çift) sayfada** başlıyor

---

## 4 · Ekonomi — 160 sayfayla

| sürüm | liste | baskı | telif | b.e. ACOS |
|---|---|---|---|---|
| ciltli | 34.99 $ | 8.37 $ | **12.62 $** | 36.1 % |
| ciltsiz | 22.99 $ | 3.72 $ | **10.07 $** | 43.8 % |
| Kindle | 11.99 $ | 1.20 $ | **7.19 $** | 60.0 % |

**KDP Select / KU dışarıda** (karar K6): 160 sayfalık tam okuma ≈ 0.77 $;
ciltsiz telifin **13.1 katı** kayıp.

---

## 5 · KURUCU EYLEMLERİ — hiçbiri yapılmış gibi gösterilmiyor

### Yüklemeyi BLOKLAYAN

1. **AI beyanı.** Hukuki beyandır; seçim kurucunundur. Karar için gereken
   olgular `08_OUTPUT/KDP_AI_DISCLOSURE_NOTES.md` içinde — **beyan
   yazılmadı, uydurulmadı**.
2. **Dış oyun testi.** `01_SOURCE/playtests/` boş. Kitabı gerçek bir masada
   oynayacak insan gerekir; `qa_playable` bunu *kusur değil DURUM* olarak
   raporluyor ve `locked` seviyesini bloklar.

### Bloklamayan

3. **APLUS-05 sanatı** — A+ projesi 5 modülle yüklenebilir.
4. **ISBN ×2** — KDP ücretsiz atar; yazılınca yeniden üret, künye sayfası
   `PENDING` yerine gerçek numarayı basar. **Hiçbir yerde ISBN uydurulmadı.**
5. **Ciltli şablon doğrulaması** — sırt hipotezini KDP şablonuyla karşılaştır.
6. **KDP Previewer** — `KDP_PREVIEWER_CHECKLIST.md` neye bakılacağını yazıyor.

### Kapsam kararı

`release` kapısı **≥100 kilitli oyun** ister; kitapta 56 var. Kapı bilerek
kırmızıdır. Seçenekler ve gerekçeleri:
[`PHASE_6_BRUTAL_AUDIT.md § 6`](PHASE_6_BRUTAL_AUDIT.md).

---

## 6 · Ajanın yapmadıkları

- Amazon KDP paneline **dokunulmadı**
- **Yükleme yapılmadı**, yayın yapılmadı, A+ moderasyona gönderilmedi
- Fiziksel prova **sipariş edilmedi**
- ISBN, barkod, ödül, çok satan iddiası, çocuk testi iddiası **uydurulmadı**
- Eksik 44 oyun **uydurulmadı**
- Yazar biyografisi **yazılmadı** — kardeş projeden birebir kopyalandı
  ([`AUTHOR_BIO_PROVENANCE.md`](AUTHOR_BIO_PROVENANCE.md))
- Faz 7 **başlatılmadı**
