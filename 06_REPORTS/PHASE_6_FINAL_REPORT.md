# FAZ 6 · NİHAİ RAPOR

> **The Great Book of World Games** · dal: `main` · kapı: `phase1`
> Tarih: 20 Ağustos 2026
>
> ```
> BAŞLANGIÇ  :  52 / 100 oyun · iç blok YOK · kapak YOK · A+ YOK
> BİTİŞ      :  56 / 100 oyun · 160 sayfa × 2 baskı sürümü · EPUB · A+ metni
> ```

> ⛔ **BU RAPOR "PUBLISHED" DEMİYOR.** KDP paneline dokunulmadı, hiçbir dosya
> yüklenmedi, Previewer açılmadı, fiyat girilmedi, A+ moderasyona gönderilmedi
> ve prova sipariş edilmedi. Beş **bloklayıcı kurucu eylemi** açıktır ve § 21'de
> tek tek sayılmıştır.

---

## 1 · Başlangıç durumu

Faz 5 kapanışı şunu devretti:

| | |
|---|---:|
| Yazılmış oyun | 52 / 100 |
| Ön madde | **YAZILMAMIŞ** |
| Aile açılışları | **YAZILMAMIŞ** (7 × 2 sayfa) |
| İç blok PDF | **YOK** |
| Kapak | **YOK** |
| A+ | **YOK** |
| İstem kütüphanesi | **YOK** (Faz 5 teslimatıydı, üretilmedi) |
| Metadata paketi | **YOK** |
| Dış oynanabilirlik testi | 0 oturum |

---

## 2 · Nihai içerik durumu

```
FINAL VERIFIED SCOPE = 56 / 100
```

| | Ölçülen |
|---|---:|
| **Yazılmış oyun** | **56** |
| Kültür | **39** |
| Bölge | 22 |
| Aile | 7 / 7 |
| `reconstructed` madde | 7 (yedisinin de beyanı var) |
| En eski oyun | ~4.600 yıl (Ur, y. MÖ 2600) |
| **Basılan kelime** | **65.395** (PDF'ten çıkarıldı) |
| Ön madde | 2.039 kelime |
| Aile açılışları | 2.415 kelime |
| Kurucu müdahalesi olmadan yazılabilir | 6 (gerekçeleri ölçüldü) |
| Kurucu araştırması gereken | 38 |

### Dört oyun eklendi — ve neden

Kurucunun teslim ettiği **Murray 1952** sayfa seviyesinde tarandı. Boşluk
kaydı bu eseri `BLOCKED_WORKS` içinde "denendi ve açılamadı" diye
tutuyordu; teslimden sonra o gerekçe **doğru değildi**.

| oyun | kültür | kaynak | not |
|---|---|---|---|
| **Alquerque** | Andalusi Arap | Murray ss. 65–66 (§ 4.2 · § 4.2.1) | Faz 5 "Bell yetersiz → reconstructed olmalı" demişti; o yargı **Bell'e** aitti. Murray'in kural seti TAMDIR. |
| **Ashta Kashte** | Bengalli | Murray ss. 129 ve 131 (§ 6.3 · § 6.3.3) | Aile girişi (s. 129) maddenin yarısıdır; iki sayfa birlikte okunmadan oyun "yazılamaz" görünür. |
| **Rimau-rimau** | Malay | Murray s. 108 (§ 5.6.1) | Tek kaplan, TEK sayılı diziyi atlayarak alma. |
| **Go** | Han Çinlisi | Murray ss. 89–91 (§ 4.7.1) | Envanterin UNRESOLVED düğümü **kaynakla** çözüldü: Murray künyeyi Çin adıyla (wei-k'i) açar ve 19×19 tahtayı bir Çin kaydına (Chao Wu King, 970–1127) bağlar. |

Üç şekil PDF sayfası **400 dpi render edilip GÖZLE okundu** — metin katmanı
şekil içeriğini vermez: Fig. 27 (alquerque köşegen deseni), Fig. 52
(rimau-rimau'nun iki gunung'u), Fig. 56 (ashta-kashte'nin beş işaretli karesi).

### Yazılmayanlar — ve neden (ölçüldü, tahmin edilmedi)

| oyun | bulunan | neden yazılmadı |
|---|---|---|
| `twelve-mens-morris` | Murray s. 43 · **kural seti TAM** | Zaten `nine-mens-morris`in "Twelve men" **varyantı olarak basılı**. Engel kaynak değil **tekrar**. |
| `nine-holes` | Murray s. 39 · **kural seti TAM** | Envanterin kendi puanı `distinct: 1` ve kendi şerhi bu maddeyi kitabın beşinci üç-taş oyunu olarak **elenecek aday** sayıyor. Engel **editoryal**. |
| `zamma` | Murray ss. 66, 69 · zengin ve ayrı bir oyun | Murray terfi etmiş taşın **alma gücü** için açıkça *"nothing is said"* der. Oyunun bitişini belirleyen kural **kaynakta yok**. |
| `tabula` · `ludus-duodecim-scriptorum` | Murray ss. 29–31 | ⛔ Murray'in **metni ile kendi şekli çelişiyor**: metin taşların *table D*'den toplandığını söyler, aynı sayfadaki Fig. 16 (Ostia levhası) **beş** tablo gösterir. Bir yarış oyununun BİTİŞ çeyreği tahminle yazılamaz. |
| `tapatan` | Murray s. 42 | Yalnızca *"Philippines: Tapatan (Culin, f, 648). Widely played."* — bu bir künyedir, kaynak değil. |
| `luk-tsut-kei` | Murray s. 42 | Tarih var, oyuna ÖZEL kural yok. |
| `hus` | Murray ss. 207, 209 | 4×16 = 64 çukur malzeme eşiğinin üstünde; ayrıca Schultze ile ILN çizimi tahta boyutunda çelişiyor. |

---

## 3 · Alınan kurucu varlıkları

**HİÇBİRİ.** `07_ASSETS/raw/cover/` ve `07_ASSETS/raw/aplus/` **boştur**.

Alım hattı (`04_BUILD/cover_artwork.py`) yazıldı, **boş koştu** ve boş
koştuğunu söyledi. Hat ayrıca **sentetik bir dosyayla uçtan uca denendi**:
440 × 281 px bir test görseli onaylı motorla (upscayl-bin ·
`digital-art-4x` · GPU) 1760 × 1124 px'e çıkarıldı, 300 dpi etiketi yazıldı
ve araç **doğru sonucu** verdi — dört kat büyütmeden sonra efektif DPI
**99,9**, yani hâlâ yetersiz. Araç başarıyı uydurmadı. Test dosyaları silindi.

---

## 4 · Kapak istemleri

`07_ASSETS/IMAGE_PROMPT_LIBRARY.html` **oluşturuldu** (Faz 5 bu teslimatı
üretmemişti).

- **COVER OPTION 01 — THE WORLD GAME TABLE**: tek sürekli tepeden çekim,
  müze çalışma masası.
- **COVER OPTION 02 — THE BOARD THAT IS A MAP**: kıtaların tahta
  geometrisinden kurulduğu arşiv dilinde dünya haritası.

İkisi de **METİNSİZ** ister ve dokuz maddelik mutlak yasak listesi taşır.
Çıktı sözleşmesi ölçümden **basılır**: varlık kimliği, dosya adı, ham konum,
biçim, en-boy oranı, 300 ppi piksel hedefi, yükseltme öncesi asgari boyut,
bleed, kırpma-güvenli alan ve **dört tipografi bölgesi** (ön başlık · yazar ·
sırt · arka kapak) ile barkod boş alanı — hepsi inç ve piksel olarak.

Dosya **bölüm işaretleriyle** yazılır: betik yalnızca kendi bölümünü
yeniler, geçmişi silmez. Bu davranış test edildi.

---

## 5 · A+ istemleri

Altı modül, her biri **metinsiz**, her biri ayrı amaçlı ve ayrı ölçülü:

| # | modül | Amazon tipi | boyut |
|---|---|---|---|
| 01 | HERO / WORLD OF GAMES | Standard Image Header with Text | 970 × 600 |
| 02 | CULTURAL DIVERSITY | Standard Image & Text Overlay | 970 × 600 |
| 03 | HOW THE BOOK WORKS | Standard Single Image & Sidebar | 300 × 400 |
| 04 | TYPES OF GAMES | Standard Four Image & Text | 4 × 220 × 220 |
| 05 | PLAY / FAMILY / DISCOVERY | Standard Image & Light Text Overlay | 970 × 300 |
| 06 | THE COMPLETE COLLECTION | Standard Image Header with Text | 970 × 600 |

Kütüphane ayrıca **A+ görselleri YÜKSELTİLMEZ** diye yazar ve gerekçesini
verir: en büyüğü 970 px'tir ve küçültülecek bir görsele 4× uygulamak yalnızca
artefakt üretir.

---

## 6 · Kapak işleme

**YAPILMADI** — sanat yok. Yapıldığı iddia edilmiyor.

Yapılan: **geometri**, ve o geometri ölçülen sayfa sayısından türetiliyor.

---

## 7 · Yükseltme sonuçları

| | |
|---|---|
| Yöntem | `ASSET_UPSCALING_REPORT.md` § 4.1 — Real-ESRGAN ncnn-vulkan (`upscayl-bin`) + Pillow pHYs |
| Model | `digital-art-4x` (raporun § 6.4'ünün illüstrasyon için önerdiği model) |
| Ölçek | 4× |
| Efektif DPI tanımı | **piksel ÷ fiziksel inç** — etiket DEĞİL |
| Uçtan uca test | 440 × 281 → 1760 × 1124 px · ×4,00 · efektif DPI 25,0 → **99,9** |
| Gerçek varlık işlendi | **0** (ham varlık yok) |

---

## 8 · Tipografi

Kapak tipografisi **yazılmadı** çünkü üzerine yazılacak sanat yok. İç blok
tipografisi tamamlandı ve ölçüldü:

| | |
|---|---|
| Font | **Liberation Serif** (SIL OFL 1.1) · dört yüz · **GÖMÜLÜ ve subset** |
| Neden | reportlab'ın Times-Roman'ı bir Type-1 taban fontudur ve **PDF'e gömülmez**; KDP gömülmemiş fontu reddeder. Liberation Serif Times metrikleriyle uyumludur, yani Faz 2'den beri ölçülen sayfa modeli **kaymadı**. |
| Gövde | 10,5 / 13,5 pt |
| Kesme işareti | dizgi anında tipografik (`’`), veride düz kalır |

⛔ **İlk koşuda ÜÇ gömülmemiş font vardı** — Helvetica (reportlab taban
fontu), Times-Roman (diyagram efsanesinin sabit fontu) ve ZapfDingbats
(ParagraphStyle'ın varsayılan madde imi fontu). Üçü de kaldırıldı; `pdffonts`
artık yalnızca dört gömülü yüz gösteriyor.

---

## 9 · Sırt geometrisi

Sırt **sayılan** sayfa sayısından hesaplanır; hiçbir sayfa sayısı gömülü değil.

| | ciltsiz | ciltli |
|---|---:|---:|
| Sayfa | **160** | **160** |
| Trim | 8,5 × 11 in | 8,25 × 11 in |
| Sırt | **0,3603 in** | **0,4600 in** |
| Tam sarım | 17,6103 × 11,25 in | 17,2100 × 11,25 in |
| 300 ppi hedefi | 5283 × 3375 px | 5163 × 3375 px |
| Sırta yazı | evet (KDP eşiği 79 s.) | evet |

`covers.py --check` iç blok değişirse **"SIRT BAYAT"** diye kırmızı yanar;
bu davranış paket testinde kasıtlı kusurla doğrulandı.

⚠ **Ciltli geometri HİPOTEZDİR.** KDP ciltli kapak şablonu tahta kalınlığı,
menteşe ve sarım paylarını içerir ve bunlar sayfa sayısından türetilemez.
Kurucu şablonu indirmeden ciltli kapak üretilmemelidir.

---

## 10 · A+ modülleri

`03_APLUS/aplus_content.json` üretildi: **MODÜL → GÖRSEL → BAŞLIK → GÖVDE**.

- Altı modülün altısının **başlık ve gövde metni hazır** ve alan
  sınırlarının içinde (en uzun başlık 48/160, en uzun gövde 410/1000).
- **İddia taraması yeşil**: yedi yasak kalıp (bestseller · ödül · test
  edilmiş · garanti edilmiş eğitsel sonuç · sıralama · bütünlük) ve
  **metindeki her sayı** kitabın ölçülen değerleriyle karşılaştırıldı.
  "100 games" yazılsaydı kapı kırmızı yanardı — bu, paket testinde kasıtlı
  kusurla doğrulandı.
- **Görsel: 9 dosya eksik.** Paket TAM DEĞİL ve tam olduğu iddia edilmiyor.

---

## 11 · Desteklenen biçimler

| biçim | durum | dosya |
|---|---|---|
| **Ciltsiz** | ✅ iç blok hazır · ⛔ kapak yok | `08_OUTPUT/PAPERBACK/GreatBookOfWorldGames_interior_paperback.pdf` |
| **Ciltli** | ✅ iç blok hazır · ⛔ kapak yok · ⚠ şablon doğrulanmadı | `08_OUTPUT/HARDCOVER/GreatBookOfWorldGames_interior_hardcover.pdf` |
| **Kindle** | ✅ EPUB 3 hazır · ⛔ kapak yok | `08_OUTPUT/KINDLE/GreatBookOfWorldGames.epub` |
| **A+** | ✅ metin hazır · ⛔ 9 görsel yok | `03_APLUS/aplus_content.json` |

Her paket dizininde `SHA256SUMS` vardır.

### Kindle SABİT DÜZEN DEĞİL — gerekçesi

Kitabın çift sayfa mimarisi bir **baskı kısıtına** verilmiş cevaptır: kâğıtta
bir maddeyi bölen şey yaprağın kendisidir. Kaydırılan bir ekranda o kısıt
**yoktur**; madde tek ve kesintisiz akar, yani söz ihlal edilmez, konusuz
kalır. Sabit düzen ise 8,5 × 11'lik bir çift sayfayı telefona sıkıştırır,
10,5 punto gövdeyi okunamaz kılar ve okurun erişilebilirlik ayarlarını
kilitler. Diyagramlar **satır içi SVG** olarak gömüldü: her ekran
yoğunluğunda keskin, 50 diyagram için toplam 216 KB.

---

## 12 · Desteklenmeyen biçimler

| biçim | neden |
|---|---|
| **Büyük punto** | `project_config.json` içinde `enabled: false`. Diyagram ağırlıklı bir kitapta punto büyütmek sayfa sayısını patlatır; karar A4 ile kurucuya bırakılmıştır. |
| **Audiobook** | Kural metni ve diyagram sesli anlatılamaz. |
| **Sabit düzen Kindle** | § 11'de gerekçelendirildi. |

---

## 13 · Nihai sayfa sayısı

**160** (her iki baskı sürümü de). Bu sayı `interior.py` tarafından
**SAYILMIŞTIR**, model tarafından tahmin edilmemiştir.

| | |
|---|---:|
| Ön madde | 9 sayfa |
| Boş (mimarî) | 18 |
| Aile açılışları | 7 |
| Oyun maddeleri | 112 (56 × 2) |
| Arka madde | 14 |
| **Toplam** | **160** |

**56 / 56 madde SOL (çift) sayfada başlıyor.** Dört sayfaya taşan madde: **0**.

⚠ Kapsam modeli (`page_budget.py`) 254 sayfa der ve öyle kalır: o sayı
**100 oyunluk kilitli kapsamın** izdüşümüdür ve kapsam sessizce yeniden
yazılmaz. Kitabın kendisi 160 sayfadır.

---

## 14 · Nihai kelime sayısı

**65.395** — PDF'ten çıkarılarak sayıldı (yani gerçekten basılan kelime).

---

## 15 · Nihai oyun sayısı

**56.** Kitabın hiçbir yerinde "100 oyun" yazmıyor.

Alt başlık **ölçümden türetiliyor**:

> *56 Games from 4,600 Years of Human Play — Rules, Boards and Stories from
> 39 Cultures, Ready to Play Tonight*

Hipotez (*"100 Games … 45 Cultures"*) `project_config.json` içinde **duruyor**
ve silinmedi; neyin değiştiği görünsün diye. `metadata.py` alt başlıktaki iki
sayının kitabın ölçülen değerleriyle aynı olmasını **denetler**.

---

## 16 · Kaynak doğrulama

| | |
|---|---:|
| Doğrulama kaydı | **74** |
| `verified` | **55** |
| Faz 6'da eklenen | 6 (dört yeni oyun + nine-mens-morris'in Murray şerhinin kalkması) |
| Uydurulmuş sayfa / künye | **0** |

### Bir künye hatası bulundu ve düzeltildi

`catch-the-hare` künyesi **"folio 916"** basıyordu. Murray'in sayfası
400 dpi **render edilip gözle okundu**: metin **"(Alf. 91b)"** diyor. OCR'nin
`b`'yi `6` okuması basılı künyeye geçmişti. Uydurulmuş bir sayfa numarası
kadar zararlıdır: denetlenebilir biçimde yanlıştır.

Ayrıca üç yeni oyunun envanter kaydı **`page-verified` YAPILMADI** ve
`bibliographic` bırakıldı: projenin kendi tanımı iki bağımsız locator'lı
künye ister, üçünde de bir tane var. Murray kaydı sayfa seviyesindedir;
**oyunun kendisi** değil.

---

## 17 · Satır edit sonuçları

Yeni kapı: **`04_BUILD/qa_lineedit.py`** · **12 denetim · 1.891 metin bloğu**.

Bulunan ve düzeltilen kusurlar:

| ne | kaç |
|---|---:|
| Türkçe efsane etiketi (ilk tarama) | **63** |
| Türkçe efsane etiketi (aksansız — ikinci tarama) | **2** |
| Efsane ↔ kural terminoloji ayrışması | **13** |
| Basılan metinde markdown işareti | 2 (bir **güvenlik uyarısının** içinde) |
| Basılan künyede projenin iç sözlüğü | 12 maddede |
| Künye hatası (OCR) | 1 |
| Terminoloji karışıklığı (`line of three` / `row of three`) | 7 |
| Aykırı cümle uzunluğu | 1 (`set-dilth`, 41 kelime/cümle) |
| Arka maddede iç kimlik basımı (`li-b-el-merafib`) | tüm malzeme ve sözlük listeleri |
| Tahta şablonlarının rastgele sırası | 33 satır |
| `used by 1 games` | 1 |
| Bölüm açılışında üstbilgi tekrarı | her bölüm |
| Karışık düz/eğri kesme işareti | kitap geneli |
| Sözlüğün yanlış tanıklık iddiası | `eye` → cat's cradle, hopscotch |

⚠ **Ölçülüp DÜZELTİLMEYEN bir şey var ve kasıtlıdır.** Kültürel hikâyelerin
cümle ortalaması **ortanca 22,4 kelime**; `project_config.json § style` bandı
**12–19** diyor ve 56 maddenin **48'i** o bandın dışında. İki yanlış yol
reddedildi: (a) 48 hikâyeyi metriği tutturmak için yeniden yazmak — yol
haritası § 3 bunu açıkça yasaklar; (b) bandı sessizce ölçüme çekmek — `style`
bloğu **kurucu onayına** bağlıdır (**AÇIK KARAR A5**). Kapı ölçümü **raporlar**
ve yalnızca gerçek aykırı değerde ısırır.

---

## 18 · Diyagram denetimi

**51 diyagramın 51'i** render edildi ve **gözle** incelendi (üç kontakt sayfası).

Yeni kapı: **`04_BUILD/qa_visual.py`** · **11 denetim** · tanımlayıcıyı değil
**RENDER EDİLMİŞ SVG'yi** denetler.

Bulunanlar — hepsinde sayısal kapılar **yeşildi**:

1. **63 + 2 Türkçe efsane etiketi.** İngilizce kitabın diyagramlarında
   *"kale — buradaki taş alınamaz"* basılacaktı. `qa_language_split` bunu
   göremez çünkü o kapı **JSON alanlarına** bakar, **çizilmiş metne** değil.
   İkinci taramadaki iki etikette Türkçeye özgü **tek bir harf yok**
   (*"alttaki oyuncunun generali"*), yani harf tabanlı denetim de kördü.
2. **Baskı fontunda olmayan sembol.** Efsanedeki `ring` sembolü (U+2312)
   Liberation Serif'te **yok**; basılı sayfada yer boş kalacaktı. Diyagram
   dili bu dersi v1.3'te **gliflere** yazmıştı ("sembol yazılmaz, çizilir")
   ama **marker** yolu hâlâ metin yazıyordu. Üç marker sembolünün **üçü de**
   fontta yok. Artık çiziliyorlar.
3. **Tuvalden taşan efsane** — iki diyagramda ölçüldü (3,1 mm ve 1,4 mm).
4. **`mbube-formation` efsanesi "lion and BUFFALO" diyordu.** Oyunda manda
   yoktur; **impala** vardır ve "buffalo" maddede **sıfır** kez geçer.
5. **İki yetim SVG** — tanımlayıcısı olmayan, geri çekilmiş diyagram dosyaları.
6. **CI KÖRDÜ**: Faz 4 ve Faz 5 kendi diyagram tanımlayıcılarını `.gitignore`
   izin listesine **eklememişti**. CI'da 51 diyagramın **18'i** denetleniyordu,
   **33'ü hiç görülmedi**. Kapı yeşil yanıyordu çünkü **bakacak dosya yoktu**.
7. `mbube-mbube`'nin render edilmiş diyagramı vardı ama **maddesi onu
   kullanmıyordu**; bağlandı. Diyagramsız madde 11 → **10**.

---

## 19 · KDP ön denetimi

Yeni kapı: **`04_BUILD/kdp_preflight.py`** · **18 denetim** · iki sürüm.

| denetim | sonuç |
|---|---|
| Font gömme | ✅ dört yüz, hepsi gömülü ve subset |
| Sayfa ölçüsü | ✅ 160/160 sayfa tam trimde, hepsi aynı |
| **Mürekkep kutusu** (sayfa RASTERLENİP ölçüldü) | ✅ en dar pay **0,333 in** (KDP asgarisi 0,25) |
| Basılan metinde belge dili | ✅ yok |
| Raster görsel çözünürlüğü | ✅ raster görsel **yok** — her diyagram vektör |
| Sayfa bandı ve parite | ✅ 160 ∈ [110, 828] · çift |
| Art arda boş sayfa | ✅ ikiden fazla yok |

⚠ Bu kapı **Amazon KDP Previewer'ın yerine geçmez** ve geçtiğini iddia etmez.

---

## 20 · Git / CI

| | |
|---|---|
| Dal | `main` · açık PR **yok** |
| Bu fazın commit'i | **6** |
| Değişen | 71 dosya · +31.887 / −16.655 satır |
| Yeni üretim betiği | 16 |
| Çalışma ağacı | **temiz** |
| Yerel kapılar | `./04_BUILD/qa_all.sh` → **BÜTÜN KAPILAR YEŞİL** |
| **CI** | **temiz bir klonda uçtan uca simüle edildi ve YEŞİL** (22 + 13 adım) |
| **⛔ PUSH** | **YAPILMADI** — ortam uzak depoya yazmayı engelledi (§ 21) |

Yeni CI işi: **`package-gates`**. Üçüncü taraf paket kurar (reportlab ·
Pillow) ve bu bilinçli bir istisnadır: Faz 6 kapıları **basılacak dosyaya**
bakar. Ticari manuscript depoda olmadığı için hepsi orada **boş koşar ve 0
döner** — bu, temiz bir klonda tek tek doğrulandı.

### Kapıların kendi testi

| test | sonuç |
|---|---|
| `05_TESTS/selftest.py` | **192 denetim yeşil** |
| `05_TESTS/package_selftest.py` (**yeni**) | **37 kasıtlı kusurun 37'si yakalandı** |

Paket testi her durum için projeyi geçici bir kopyaya açar, **tek bir kusur**
enjekte eder ve ilgili kapının **kırmızı** yanmasını bekler. Örnekler: sırtın
bayatlaması, bir maddenin sol sayfada başlamaması, iç marjın KDP asgarisinin
altına düşmesi, A+ metnine `bestseller` girmesi, ölçülmemiş bir sayının
(`100 games`) A+ metnine sızması, **aksansız** Türkçe bir efsane etiketi,
tuvalden taşan efsane, kuralda geçmeyen efsane terimi, kılavuzun bayatlaması.

---

## 21 · Kalan kurucu eylemleri

Beşi **BLOKLAYICI**:

| # | ne | nerede |
|---|---|---|
| ⛔ 1 | **Kapak sanatı** — iki konseptten biri üretilecek | `07_ASSETS/raw/cover/` · istemler `07_ASSETS/IMAGE_PROMPT_LIBRARY.html` |
| ⛔ 2 | **A+ görselleri** — dokuz dosya | `07_ASSETS/raw/aplus/` · aynı dosyada |
| ⛔ 3 | **Yazar biyografisi** — KDP kardeş bir başlıkta yer tutucu metni REDDETTİ (12 Ağustos 2026) | `project_config.json → founder.authorBio` |
| ⛔ 4 | **AI beyanı** — hukuki bildirim; ajan seçemez. Gereken olgular `metadata.json → aiProductionFacts` içindedir | KDP paneli |
| ⛔ 5 | **Dış oynanabilirlik testi** — 0 oturum. `PLAYABILITY_STANDARD § 4` testçinin **insan** olmasını şart koşar | `01_SOURCE/playtests/` |

Bloklayıcı olmayanlar:

| # | ne |
|---|---|
| 6 | **`git push`** — altı commit yerelde duruyor. Bu oturumun ortamı uzak depoya yazmayı engelledi; komut çalıştırılmadı ve çalıştırıldığı iddia edilmiyor. |
| 7 | **Ciltli kapak şablonu** — KDP'den indirilip § 9'daki sırt ve sarım ölçüleriyle karşılaştırılacak |
| 8 | **ISBN** — KDP atadıktan sonra `founder.isbn.*` içine yazılırsa künye sayfası gerçek numarayı basar |
| 9 | **AÇIK KARAR A5** — `style` bandı (§ 17): bant mı ölçüme çekilecek, proza mı yeniden yazılacak |
| 10 | **A+ modül ölçüleri** — Amazon modül setini zaman zaman değiştirir; panelden doğrulanmalı |

**KDP paneline dokunulmadı.** Yükleme, Previewer, fiyat girişi, bölge seçimi,
telif planı, A+ gönderimi, prova siparişi ve **Publish** kurucunundur.

---

## 22 · Hazırlık durumu

```
PHASE 6      : COMPLETE (technically executable work)
BOOK CONTENT : 56 / 100 · yazım kaynak duvarında kapandı
INTERIOR     : READY   · 160 sayfa · iki baskı sürümü · EPUB
COVER        : BLOCKED · sanat yok
A+           : BLOCKED · dokuz görsel yok
KDP UPLOAD   : WAITING FOR FOUNDER ACTION
PUBLISHED    : NO
```

`.gate` = **`phase1`** · **yükseltilmedi**. `release` kapısı dış
oynanabilirlik testi ve dolu bir `authorBio` ister; ikisi de yok ve ikisi de
ajanın üretebileceği şeyler değil. `metadata.py --gate release` bugün
**kırmızı** yanar ve bu doğrudur.

Bu rapor **"KDP READY"** demiyor. **"KDP UPLOAD READY, WAITING FOR FOUNDER
ACTION"** diyor — ve aradaki fark beş bloklayıcı maddedir.
