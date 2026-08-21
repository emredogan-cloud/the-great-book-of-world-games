# NİHAİ DÜZELTME TURU — Kapak · A+ · DPI

> **The Great Book of World Games** · dal: `main` · kapı: `phase1`
> Tarih: 21 Ağustos 2026 · commit: `ef9c2d2` · **CI: gerçekten koştu ve YEŞİL**
> (GitHub Actions run [`32468968390`](https://github.com/emredogan-cloud/the-great-book-of-world-games/actions/runs/32468968390) · `conclusion: success`)

> ⛔ **BU RAPOR "PUBLISHED" DEMİYOR.** KDP paneline dokunulmadı, yükleme
> yapılmadı, Previewer açılmadı, A+ moderasyona gönderilmedi, prova
> sipariş edilmedi. Bu bir **düzeltme turu** raporudur — [`PHASE_6_FINAL_REPORT.md`](PHASE_6_FINAL_REPORT.md)
> ve [`PHASE_6_BRUTAL_AUDIT.md`](PHASE_6_BRUTAL_AUDIT.md)'nin devamıdır, onların yerine geçmez.

---

## 0 · Kurucu talimatının kapsamı — ne yapıldı, ne yapılmadı

| Talimat | Uygulandı mı |
|---|---|
| Kindle kapağına tipografi ekle | ✅ |
| Kapak/A+ sanat konseptini yeniden tasarlama | ✅ (dokunulmadı) |
| Kurucu sanatını yeniden üretme (gerekmedikçe) | ✅ (gerekmedi, dokunulmadı) |
| Başka varlık isteme | ✅ (istenmedi) |
| Yeni araştırma fazı başlatma | ✅ (başlatılmadı) |
| Amazon'a yükleme / yayın / A+ moderasyon / prova siparişi | ✅ (hiçbiri yapılmadı) |

**Talimatta adı geçen dört dosya bu projede YOKTUR** — ölçüldü, tahmin edilmedi:
`APLUS_MODULE_MAP.md`, `03_COVER/COVER_SPEC.md`, `03_COVER/COVER_PRODUCTION_PLAN.md`,
`03_APLUS/APLUS_PRODUCTION_PLAN.md`. `git grep` bu dört ada tüm depoda **sıfır**
isabet verdi; `03_COVER/` ve `03_APLUS/` içinde yalnızca `.gitkeep` ve
`03_APLUS/aplus_content.json` durur. Bu dört ad muhtemelen kardeş projelerin
(Bestiarium, Mythologica) dosya adlandırmasından geliyor ve bu projede hiç
üretilmedi. Onların **işlevini gören gerçek dosyalar** kullanıldı:
`06_REPORTS/FINAL_COVER_SELECTION.md` (kapak spesifikasyonu/seçim kaydı),
`06_REPORTS/cover-geometry.json` + `cover-build.json` (kapak üretim planı/kaydı),
`03_APLUS/aplus_content.json` (A+ modül haritası). Talimatın istediği
`ASSET_UPSCALING_REPORT.md` **tam okundu** (§ 1 zorunluluğu).

---

## 1 · Kindle kapağı — ÖNCE

Sanat vardı, **tipografi hiç yoktu**. Kod bunu kendi çıktısında zaten
itiraf ediyordu (`kindle_cover()` docstring: *"Bu dosyada tipografi
YOKTUR: Kindle kapağı ayrıca dizilir"*) ve `08_OUTPUT/KDP_UPLOAD_HANDBOOK.md`
aynı uyarıyı kurucuya taşıyordu: *"⚠ This file carries no typography… ask
for a typeset Kindle cover as a follow-up."* Bu tur o takip talebidir.

Görsel doğrulama (render edilip gözle bakıldı): dünya haritası + oyun
taşları sanatı tam çerçeveyi dolduruyordu, başlık/alt başlık/yazar adı
**hiçbir yerde** yoktu.

| | ÖNCE |
|---|---|
| Boyut | 1600 × 2560 px · JPEG · 300×300 dpi etiketi |
| İçerik | yalnızca kırpılmış ön panel sanatı |
| Metin | **YOK** |

## 2 · Kindle kapağı — SONRA

Aynı sanat, aynı kırpma; üstüne **vektör anahat** tipografi eklendi.
Beyaz kutu yok, AI-üretilmiş metin yok.

| | SONRA |
|---|---|
| Boyut | **1600 × 2560 px** (değişmedi) · JPEG kalite 95 (92'den yükseltildi — ince serif kenarları için) |
| SHA-256 | `9b1f14c4069092e0610c1e162962361491a756a43c3a28576a98348253cc880d` |
| Dosya | 1.031.472 bayt (1007,3 KB) |
| Basılan metin | THE GREAT BOOK OF · WORLD GAMES · *56 games from 4,600 years of human play* · *Rules, boards and stories from 39 cultures* · EMRE DOĞAN |

## 3 · Nihai Kindle boyutları

**1600 × 2560 px**, en-boy 1:1,6 (Amazon'un önerdiği oran). Amazon Kindle
kapaklarını **piksel boyutuyla** değerlendirir, fiziksel baskı DPI'ı ile
değil — ekranın bir "inç"i yoktur. Dosyanın 300×300 dpi etiketi yalnızca
uyumluluk amaçlıdır; gerçek içerik yoğunluğu **~227,6 px/in**
(2560 px ÷ 11,25 gerçek-dünya inç = sarımın kendi yüksekliği). Bu bir
yanıltma değildir çünkü hiçbir fiziksel baskı boyutu iddia edilmiyor —
KDP_UPLOAD_HANDBOOK.md'ye bu ayrım artık açıkça yazılıyor (§ 15). Piksel
boyutu Amazon'un asgarisinin (1000 × 625) kat kat üstünde.

## 4 · Kindle tipografi yöntemi

**Deterministik, vektör-anahat, CLI tabanlı — AI DEĞİL.**

- Motor: Pillow `ImageDraw` + `ImageFont.truetype`, aynı font ailesi
  (**LiberationSerif** Regular/Bold/Italic, `/usr/share/fonts/truetype/liberation/`)
  kapağın ve iç bloğun her yerinde kullandığı fontla **birebir aynı**.
- Yerleşim **icat edilmedi**: sarımın `FINAL_COVER_SELECTION.md § 6`'da
  ÖLÇÜLEN sakin bantlarıyla (ön başlık sd 12,8 · ön yazar sd 13,7 — ikisi
  de "gerek yok" düzeyinde sakin) **aynı dikey konumlar** kullanıldı;
  yalnızca bu görselin kendi px/in oranına (~227,6) ölçeklendi.
- Punto **tahmin edilmedi**: `_pil_fit_tracked()` — sırt başlığının
  kullandığı `fit_tracked()` ile aynı ilke — metni ölçülen genişliğe
  sığdıran punto ve harf aralığını hesaplayarak bulur; taşma riski yoksa
  bile otomatik-küçültme güvenlik ağı olarak çalışır.
- Beyaz kutu / opak panel **yok**. Kontrast desteği gerekmedi (aynı ölçüm
  gerekçesiyle — bu bölge sarımda zaten en sakin bölgeydi).
- Basılan beş öge ve gerçekleşen punto (px): "THE GREAT BOOK OF" 62px ·
  "WORLD GAMES" 182px (kalın) · alt başlık×2 38px (italik) ·
  "EMRE DOĞAN" 73px (kalın). Tam kayıt: `06_REPORTS/cover-build.json → kindle.typography`.
- Kod: `04_BUILD/covers.py` içinde `kindle_typography()`, `_pil_tracked()`,
  `_pil_fit_tracked()` — yeni `--kindle-only` bayrağıyla (`covers.py --build
  --kindle-only`) yalnızca Kindle yeniden üretilebilir; ciltsiz/ciltli
  PDF'lere **dokunmaz** (SHA-256'ları bu turda değişmedi).

Zum denetimi (200% büyütme, iki bölge) yapıldı: harfler keskin, Ğ
aksanı doğru, JPEG artefaktı yok. Alt başlığın "39 cultures" kelimesi
sanattaki bir piyonun kenarına hafifçe değiyor — aynı örtüşme sarımda
(basılı ciltsiz/ciltli kapakta) zaten vardı ve `FINAL_COVER_SELECTION.md`
tarafından ölçülüp kabul edilmişti; burada yeni icat edilmedi, aynı
onaylı bant ölçeklendi.

---

## 5–8 · Baskı kapağı çözünürlük denetimi — PAPERBACK + HARDCOVER

**Yöntem:** dosya adına ("300dpi", "4x") güvenilmedi. `pdfimages -list`
ile **basılacak PDF içindeki gömülü rasterin gerçek piksel/inç**'i
ölçüldü — bu, poppler'ın sayfa fiziksel boyutundan (KDP'ye giden gerçek
inç) türettiği bir bölme sonucudur, bir metadata etiketi değil.

| | Ciltsiz (PAPERBACK) | Ciltli (HARDCOVER) |
|---|---:|---:|
| Kurucunun ham sanatı | 1569 × 1003 px | (aynı ham dosya) |
| **Ham efektif DPI** (tam sarıma göre) | **89,1** ⛔ (300'ün altında) | **89,1** ⛔ |
| 4× AI yükseltme sonrası | 6276 × 4012 px | (aynı işlenmiş dosya) |
| **Yükseltme sonrası efektif DPI** | **356,4** ✅ | **356,4** ✅ |
| Sarıma kırpılmış/indirgenmiş dosya | 5283 × 3375 px | 5163 × 3375 px |
| **PDF içine gömülü raster (pdfimages ÖLÇÜMÜ)** | **5283 × 3375 px @ 300 × 300 ppi** | **5163 × 3375 px @ 300 × 300 ppi** |
| Fiziksel sarım | 17,6103 × 11,2500 in | 17,2100 × 11,2500 in |
| Bu turda yeniden yükseltme gerekti mi | **HAYIR — zaten 300,0 gerçek** | **HAYIR — zaten 300,0 gerçek** |
| En düşük çözünürlüklü bölge | yok — tek bir arka plan görseli, tekdüze 300 ppi; tipografi vektör (sonsuz çözünürlük) | aynı |
| Font gömme (`pdffonts`) | 3/3 gömülü + altkümeli (LiberationSerif Regular/Bold/Italic) | 3/3 gömülü + altkümeli |
| Beyaz panel / kutu | yok (görsel render + kod denetimi) | yok |

**Sonuç: ikisi de gerçekten 300 DPI — metadata değil, ölçüm.** `pdfimages`
bu sayıyı PDF'in fiziksel sayfa boyutundan (KDP'ye giden gerçek inç)
türetir; bir etiketin doğruluğuna güvenmez. Talimatın istediği "yeniden
yükseltme" bu yüzden **uygulanmadı** — zaten eşiğin üstünde olan bir
görseli yeniden işlemek talimatın kendisinin yasakladığı bir şey
(gereksiz sanat üretimi) olurdu.

Her iki sarım da bu turda **render edilip gözle incelendi**
(`pdftoppm -r 100`) → başlık/alt başlık/sırt/yazar/arka kapak metni
doğru yerde, barkod alanı boş, beyaz panel yok, sırt optik olarak
sarımın **ölçülen** iki temiz koşusuna yerleşmiş (bkz. `FINAL_COVER_SELECTION.md § 6`).

**Sırt geometrisi bağımsız hesaplanıyor** (talimat § 9'un istediği gibi —
ciltli, ciltsizden TÜRETİLMİYOR): ciltsiz `160 × 0,002252 = 0,3603 in`;
ciltli `160 × 0,0025 + 0,06 (tahta payı) = 0,4600 in`. Trim'ler de ayrı:
ciltsiz 8,5×11 in, ciltli 8,25×11 in (`project_config.json → production`
içinden okundu, varsayılmadı). ⚠ Ciltli sırt formülü **hâlâ hipotezdir**
(`founderConfirmedTemplate: null`) — KDP'nin indirilebilir ciltli
şablonuyla karşılaştırma bu turun kapsamında değil, önceden bilinen ve
hâlâ açık bir kurucu eylemidir (§ 17).

## 9 · Upscaling metodolojisi (kullanılan — bu turda TEKRAR uygulanmadı)

`ASSET_UPSCALING_REPORT.md § 4.1` (zorunlu okuma tamamlandı):
**Real-ESRGAN ncnn-vulkan** (`~/Applications/upscayl-cli/upscayl-bin`) ·
model `digital-art-4x` · ölçek 4× · GPU (NVIDIA GTX 1660 Ti, Vulkan) ·
ardından Pillow ile `pHYs` 300×300 dpi etiketi. Piksel SAYISI gerçekten
arttı (1569×1003 → 6276×4012); bu bir metadata hilesi değildi ve
bu turda **bağımsızca doğrulandı** (§ 5–8).

---

## 10 · A+ modül sayısı

**6** — `01 HERO/WORLD OF GAMES` · `02 CULTURAL DIVERSITY` ·
`03 HOW THE BOOK WORKS` · `04 TYPES OF GAMES` · `05 PLAY/FAMILY/DISCOVERY` ·
`06 THE COMPLETE COLLECTION`. Kaynak: `03_APLUS/aplus_content.json`
(`APLUS_MODULE_MAP.md` yoktu — § 0'a bakın).

## 11 · A+ görsel sayısı

**8 işlenmiş dosya · 5/6 modül sanatlı.** Modül 04 tek bir 2×2 bileşik
görselden **ölçülerek** (piksel üretilmeden, ayraç sütunları ölçülerek)
dört kareye bölündüğü için 4 dosya üretiyor; diğer dört hazır modül
(01,02,03,06) birer dosya. **Modül 05'in görseli hiç teslim edilmedi** —
bu turda da teslim edilmedi ve talimat gereği (§0 "başka varlık isteme")
**istenmedi**. `aplus-05-play-family-discovery.png` adlı dosyanın asıl
İÇERİĞİ modül 06'nın istemiyle eşleşiyor (soluk zeminde sıralı nesneler);
Faz 6'da dosya adına değil içeriğe göre modül 06'ya bağlanmıştı — bu tur
bunu **yeniden doğruladı**, değiştirmedi.

## 12 · A+ başlık/gövde eşleme durumu

**6/6 modülün 6'sında da başlık VE gövde metni Amazon'un kendi alanlarına
eşlenmiş, görsellerin İÇİNE hiçbir metin gömülmemiş.** Bu, doğrudan JSON
okunarak ve altı modülün **hepsi için** yerel önizleme kompoziti
(görsel + başlık + gövde + hiyerarşi, `PIL` ile üretildi) render edilip
gözle denetlenerek **bağımsızca** doğrulandı — yalnızca "görsel var mı"
diye durulmadı.

| Modül | Görsel | Başlık (karakter) | Gövde (karakter) |
|---|---|---:|---:|
| APLUS-01 | ✅ | 33 / 160 | 337 / 1000 |
| APLUS-02 | ✅ | 51 / 160 | 368 / 1000 |
| APLUS-03 | ✅ | 48 / 160 | 410 / 1000 |
| APLUS-04 | ✅ (4 kare) | 18 / 160 | 279 / 1000 |
| APLUS-05 | ⛔ **görsel yok** | 43 / 160 (metin HAZIR) | 281 / 1000 (metin HAZIR) |
| APLUS-06 | ✅ | 45 / 160 | 391 / 1000 |

Modül 05'in metni **hazır ve doğru** — yalnızca görseli eksik. Bu,
talimat § 10–12'nin sorduğu asıl soruyu ("görseller metinsiz kalsa da
BAŞLIK/GÖVDE doğru eşlendi mi?") olumlu yanıtlıyor: paket "metinsiz
görsellerden ibaret, kopyası eksik" bir küme **değil**.

## 13 · Stale/incorrect A+ claims — bulunan ve düzeltilen

**A+ metninin kendisinde sıfır kusur bulundu** (bu tur bağımsızca
tarandı): `claimScan.hits = []` (7 yasak kalıp — bestseller, ödül, test
edilmiş, garanti, sıralama, bütünlük — hiçbiri yok), sayılar `git grep`
ile bağımsızca tekrar tarandı, **56 oyun / 39 kültür** her yerde tutarlı,
"100 games"/"45 cultures" hiçbir A+ metninde geçmiyor. İç blok PDF'leri
ve EPUB de aynı taramadan geçirildi (`pdftotext` + `unzip` ile ham metin
çıkarılıp arandı) — **sıfır isabet**.

**Bulunan tek stale-sayı kusuru A+ ya da kapakta DEĞİL, `README.md`'deydi**
(depo kökü, GitHub'ın herkese gösterdiği ilk sayfa). Dosya hâlâ **Faz 0 /
Bootstrap** durumunu ("Yazılmış oyun 0/100", "Faz 1 — kurucu onayı
bekliyor") ve eski **"100 Games … 45 Cultures"** hipotez alt başlığını
taşıyordu — 18 Ağustos'tan (Faz 5) beri hiç güncellenmemiş. Bu dosya
`qa_language_split`/`aplus.py`'nin denetlediği "ticari yüzeyler"
kapsamında olmadığı için (K16 — mühendislik belgesi sayılır) hiçbir
otomatik kapı bunu yakalamıyordu. **Düzeltildi**: alt başlık, durum
tablosu (Faz 6 · TAMAMLANDI · 56/100 yazılmış oyun · kapak+A+ üretildi)
ve gövde metni ölçülen değerlere çekildi; kilitli 100/45 hedefinin hâlâ
`DECISIONS.md § A8`'de açık bir kapsam kararı olduğu da **açıkça**
yazıldı (sessizce silinmedi).

---

## 14 · Testler

| | Sonuç |
|---|---|
| `./04_BUILD/qa_all.sh --fix` | ✅ **BÜTÜN KAPILAR YEŞİL** · kapı seviyesi `phase1` (32 kapı grubu) |
| `05_TESTS/selftest.py` | ✅ **214 / 214** denetim yeşil |
| `05_TESTS/package_selftest.py` | ✅ **39 / 39** kasıtlı kusur yakalandı |
| `BOOK_STATS.md` / `ROADMAP_PROGRESS.md` | değişmedi (byte-eşit yeniden üretildi — oyun/kültür sayıları bu turda değişmedi) |

## 15 · Ön denetim (preflight)

`04_BUILD/kdp_preflight.py` — **20/20 denetim yeşil**, iki sürüm:

| | Ciltsiz | Ciltli |
|---|---:|---:|
| Font gömme | 4/4 gömülü | 4/4 gömülü |
| En dar mürekkep payı | 0,333 in (sol 0,486 · sağ 0,486 · üst 0,361) | 0,333 in (sol 0,486 · sağ 0,500 · üst 0,361) |
| KDP asgarisi | 0,25 in — **ikisi de üstünde** | aynı |
| Belge dili sızıntısı | yok | yok |
| Daktilo tırnağı | 0 | 0 |
| Raster görsel <300ppi | 0 (diyagramlar vektör) | 0 |
| Sayfa sayısı/parite | 160 · çift · bantta | 160 · çift · bantta |

⚠ Bu, Amazon KDP Previewer'ın **yerine geçmez** — kurucu tarafından
açılmalı (`08_OUTPUT/KDP_PREVIEWER_CHECKLIST.md`).

## 16 · CI

**Hem yerel simülasyon HEM gerçek uzak CI çalıştırıldı ve ikisi de yeşil:**

| | Sonuç |
|---|---|
| `05_TESTS/ci_simulate.py` (tam bağımlılıklı) | ✅ **22 / 22** adım — `.github/workflows/validate.yml`'in kendi `run:` bloklarından okunarak, temiz bir `git ls-files` ağacında |
| `05_TESTS/ci_simulate.py --without reportlab,PIL` | ✅ **22 / 22** adım — bağımlılıksız runner taklidi |
| **GitHub Actions (gerçek, uzak)** | ✅ run [`32468968390`](https://github.com/emredogan-cloud/the-great-book-of-world-games/actions/runs/32468968390) · `conclusion: success` · `headSha: ef9c2d2` — **`gh run view` ile doğrulandı, iddia edilmedi** |

---

## 17 · Git

| | |
|---|---|
| Commit | `ef9c2d2` — *"faz 6 düzeltme: kindle kapağına vektör tipografi + README bayat durum"* |
| Değişen dosya | 7 · +256 / −51 satır (`04_BUILD/covers.py` · `04_BUILD/handoff.py` · `06_REPORTS/cover-build.json` · `06_REPORTS/handoff.json` · `06_REPORTS/structure.json` · `08_OUTPUT/KDP_UPLOAD_HANDBOOK.md` · `README.md`) |
| Çalışma ağacı | temiz |
| **Push** | ✅ **BAŞARILI** — `0dc8522..ef9c2d2 main -> main`. Ortam bu turda uzak depoya yazmayı **engellemedi** (önceki fazda engellemişti; bu farkı gizlemek yerine kaydediyoruz). |
| `origin/main` | `ef9c2d2` — yerel `HEAD` ile **birebir eşit** (`git rev-parse` ile doğrulandı) |

⚠ Kapak/A+/Kindle **ikili dosyaları** (`08_OUTPUT/**`, `07_ASSETS/{raw,processed,print,kindle,web}/**`)
`.gitignore` gereği hiç git'e girmez (yalnızca üç kılavuz `.md` istisna) —
bu proje kararıdır, bu turda değişmedi. Yani `git push` PDF/JPG
dosyalarını taşımaz; onları üreten **kod** ve onları **tarif eden JSON/MD**
taşınır. Kurucu kendi diskindeki `08_OUTPUT/` klasörünü zaten taşıyor;
yeniden üretmek isterse `python3 04_BUILD/covers.py --build --kindle-only`
aynı Kindle dosyasını **byte-byte aynı** üretir (deterministik).

---

## 18 · Kalan kurucu-özel eylemler

Hiçbiri bu tur tarafından yapılmadı, yapıldığı iddia edilmiyor — hepsi
zaten `PHASE_6_FINAL_REPORT.md § 21`'den bilinen kalemler, bu turda
**yeniden doğrulandı**:

| # | Ne | Bloklayıcı mı | Nerede |
|---|---|---|---|
| 1 | **AI-üretilmiş içerik beyanı** — hukuki beyan, ajan seçemez | ⛔ EVET | KDP paneli · olgular `08_OUTPUT/KDP_AI_DISCLOSURE_NOTES.md` |
| 2 | **Dış oynanabilirlik testi** — 0 oturum, insan gerekir | ⛔ EVET | `01_SOURCE/playtests/` |
| 3 | APLUS-05 sanatı | hayır (5/6 modülle yüklenebilir) | `07_ASSETS/raw/aplus/` |
| 4 | ISBN × 2 (KDP atar) | hayır | `founder.isbn.*` |
| 5 | Ciltli kapak şablonu doğrulaması (§ 5–8'de hipotez olarak işaretli) | hayır (ama prova öncesi önerilir) | KDP ciltli şablon üreteci |
| 6 | KDP Previewer / yükleme / fiyatlandırma / A+ moderasyon / prova / Publish | — (hiçbiri denenmedi) | KDP paneli |
| 7 | **Kapsam kararı A8** — 56 mi 100 mü (`.gate` → `release`) | bu turun kapsamı DIŞINDA | `DECISIONS.md § A8` |

---

## 19 · Nihai durum

```
KINDLE COVER   : FIXED — vektör tipografi eklendi, sanat/kavram değişmedi
PRINT DPI      : AUDITED, GENUINE 300×300 — yeniden yükseltme gerekmedi
A+ MAPPING     : VERIFIED — 6/6 başlık+gövde doğru, 5/6 görsel (1 kurucu eylemi)
STALE COUNTS   : SWEPT — README.md'de bulunan tek kusur düzeltildi
TESTS          : selftest 214/214 · package_selftest 39/39 · preflight 20/20
CI             : local 22/22 (×2 mod) · GERÇEK GitHub Actions YEŞİL (doğrulandı)
GIT            : ef9c2d2 — commit edildi VE push edildi (origin/main eşit)
UPLOADED       : HAYIR — dokunulmadı
PUBLISHED      : HAYIR — dokunulmadı

PHASE 6 TECHNICALLY COMPLETE + KDP UPLOAD READY
(iki bloklayıcı kurucu eylemi hariç: AI beyanı · dış oynanabilirlik testi)
```
