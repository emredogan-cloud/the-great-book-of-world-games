# KDP HTML HANDOFF RAPORU

> **The Great Book of World Games** · dal: `main` · kapı: `phase1`
> Tarih: 21 Ağustos 2026 · commit: `93ee8c7` · **CI: gerçekten koştu ve YEŞİL**
> (bkz. § 8 — `gh run view` ile doğrulandı, iddia edilmedi)

> ⛔ Bu rapor "PUBLISHED" demiyor. KDP paneline dokunulmadı, hiçbir dosya
> yüklenmedi. Üretilen tek şey, kurucunun kendi tarayıcısında açacağı
> **çevrimdışı bir kontrol paneli**dir.

---

## 0 · Görev

`08_OUTPUT/KDP_UPLOAD_HANDBOOK.md`'nin **tüm operasyonel içeriğini**, sırasını
ve talimatlarını kaybetmeden, tek bir kendi kendine yeterli
`08_OUTPUT/KDP_UPLOAD_GUIDE.html` dosyasına dönüştürmek — kopyala düğmeleri,
kalıcı ilerleme takibi, kenar çubuğu gezinmesi ve bir "Yüklemeye Hazır"
panosuyla.

---

## 1 · Kaynak okundu, tam olarak

`08_OUTPUT/KDP_UPLOAD_HANDBOOK.md` **528 satır, tamamı** okundu (kısmi değil)
önce herhangi bir HTML yazılmadan. Kılavuz üç bölümden oluşuyordu: durum
özeti + bloklayıcı eylemler, üç format (ciltsiz/ciltli/Kindle, 21'er adım),
A+ içerik (10 adım). Hiçbir talimat atlanmadı, yeniden yazılmadı ya da
icat edilmedi — her adımın metni kaynaktan **birebir** aktarıldı.

---

## 2 · Ön koşul düzeltmesi — kaynağı HTML'e geçirmeden önce

Kılavuzu okurken kendi içinde bir **çelişki** bulundu: "Status at a glance"
tablosu kapağı ✅ ve A+'ı 5/6 ✅ gösterirken, hemen altındaki "Blocking
founder actions" bloğu hâlâ *"no cover artwork exists"* / *"no A+ artwork
exists"* diyordu. Kaynağa inildi: `04_BUILD/handoff.py`'de bu blok kapak/A+
sanatı gelmeden ÖNCE yazılmış **sabit metindi** ve hiç güncellenmemişti —
`handoff.json` için aynı bilginin zaten KOŞULLU hesaplandığı fark edildi
ama markdown kılavuzu o hesaba hiç bakmıyordu.

Bu, HTML dönüştürmesine başlamadan önce **düzeltildi** (commit `428fccb`):
`build_handbook()` artık aynı `pkgs` verisinden okuyor. Kılavuz yeniden
üretildi, `qa_all.sh` yeşil kaldı. **HTML kılavuzu bu düzeltilmiş, tutarlı
handbook'tan üretildi** — düzeltilmemiş hâliyle dönüştürülseydi aynı yanlış
iddiayı HTML'e de taşırdı.

Künye: `git log -1 428fccb`.

---

## 3 · Ne üretildi

`08_OUTPUT/KDP_UPLOAD_GUIDE.html` — **73 KB, tek dosya**, harici hiçbir
istek yok (font, script, stylesheet, resim — hepsi satır içi). 1180+ satır.

### İçerik eşlemesi (talimat § A–G)

| Bölüm | Kaynak | Adım sayısı |
|---|---:|---:|
| A · Before You Start | Status + Blocking founder actions + AI disclosure facts | — |
| B · Paperback | Kılavuz "PAPERBACK" § 1–21 | 21 |
| C · Hardcover | Kılavuz "HARDCOVER" § 1–21 | 21 |
| D · Kindle | Kılavuz "KINDLE / EBOOK" § 1, 2–13, 14–21 | 7 (kılavuzun kendi birleşik numaralandırması korunarak) |
| E · A+ Content | Kılavuz "A+ CONTENT" § 1–10 (§6 altı modül metnine bölündü: 6a–6f) | 15 |
| F · Final Verification | Talimat § 14'ün 10 maddesi ("Final Safety Check") | 10 |
| G · Files to Upload | `handoff.json` + gerçek dosya boyutu/sha256 | 12 satır tablo |
| — · Ready to Upload | Talimat § 10'un 9 satırı, bölüm ilerlemesinden CANLI hesaplanır | 9 kart |

**Toplam izlenebilir görev: 74** (21+21+7+15+10) — sayaç bunu koddan
sayıyor, elle yazılmıyor.

### Her adımda (talimat § 5 şablonu, kaynağın desteklediği kadarıyla)

STEP NUMBER · ACTION · KDP LOCATION (varsa) · WHAT TO ENTER (kopyala
düğmesiyle) · WHAT FILE TO SELECT (Aç düğmesiyle, sha256 + boyutla) ·
WHAT TO CHECK · EXPECTED RESULT. Bir adımın kaynakta karşılığı olmayan bir
alanı (ör. "Contributors" adımının dosyası yoktur) **boş bırakıldı**,
uydurulmadı.

### Kurucu-özel değerler (talimat § 4 — hepsi projenin ÜRETTİĞİ dosyalardan)

| Alan | Kaynak dosya |
|---|---|
| Başlık, alt başlık, yazar, yayıncı | `project_config.json → founder` |
| Yazar biyografisi | `project_config.json → founder.authorBio` |
| Oyun/kültür/aile sayısı | `06_REPORTS/tracked/metadata.json → measured` |
| Sayfa sayısı, dosya boyutu, sha256 | `06_REPORTS/handoff.json` + `sha256sum` ile bağımsız doğrulandı |
| Açıklama, anahtar kelime, kategori | `06_REPORTS/tracked/metadata.json` |
| ISBN durumu | `PENDING — KDP-PROVIDED ISBN` (kurucu değeri boş olduğu için) |
| AI beyanı olguları | `metadata.json → aiProductionFacts` + `KDP_AI_DISCLOSURE_NOTES.md` |
| Fiyatlandırma | `06_REPORTS/editions.json` |
| A+ modül başlık/gövde | `03_APLUS/aplus_content.json` |

---

## 4 · Etkileşim (talimat § 8–9, § 6–7)

- **Kopyala düğmeleri** — üç katmanlı: `navigator.clipboard.writeText()` →
  başarısız olursa gizli `<textarea>` + `execCommand("copy")` yedeği →
  o da başarısız olursa "select the text and press Ctrl/Cmd+C" mesajı.
  Üç katman kasıtlı: bu dosya `file://` üzerinden açılacak ve bazı
  tarayıcılarda Clipboard API `file://`'de güvenli bağlam sayılmayabilir.
- **☐ Tamam kutuları** — her adımda bir tane, toplam 74. Durum
  `localStorage` anahtarı `kdpGuideProgress_gbwg` altında JSON olarak
  saklanır; sayfa yenilenince kaybolmaz (gerçek tarayıcıda test edildi,
  § 7).
- **İlerleme sayacı** — TOPLAM/TAMAMLANAN/KALAN/% kenar çubuğunda canlı;
  ayrıca her bölümün kendi "n / toplam" sayacı.
- **Yüklemeye Hazır panosu** — 9 kart, ilgili adımların kutu durumundan
  CANLI hesaplanır (elle işaretlenen ikinci bir kayıt DEĞİL — tek doğruluk
  kaynağı adım kutularıdır, çift bakım riski yok).
- **Açılır/kapanır bölümler** — yerel HTML `<details>/<summary>`; JS
  gerektirmez, klavye erişilebilir.
- **Aç düğmeleri** — kılavuzun kendi klasörüne göre GÖRECELİ yol
  (`PAPERBACK/...`, `../06_REPORTS/...`); kurucunun kullanıcı adı ya da
  mutlak `/home/...` yolu **hiçbir yerde** basılmaz (§ 6'da doğrulandı).
- **Sabit kenar çubuğu** — Paperback/Hardcover/Kindle/A+/Verification/
  Files/Ready arasında tek tıkla geçiş (§ 7'de bir kusur bulunup
  düzeltildi).

---

## 5 · Tasarım

Masaüstü öncelikli "Founder Control Center": sol sabit kenar çubuğu + canlı
ilerleme kartı, sağda kart tabanlı adımlar. Üç renk kodu talimat § 6'yı
birebir karşılar: yeşil = 🟢 FOUNDER ACTION, mavi = 🔵 AGENT PREPARED,
kırmızı = 🔴 WARNING (uyarı kutuları ayrıca metin içinde de belirir, ör.
barkod alanına dokunma, KDP Select'e girme, boş katkıda bulunan satırı
bırakma). Tipografi: başlıklar serif (kitabın kendi "gravür" kimliğiyle
tutarlı), gövde/arayüz sistem sans-serif — **Google Fonts dahil hiçbir
harici font yüklenmez**, çünkü talimat § 18 çevrimdışı çalışmayı şart
koşuyor.

---

## 6 · Doğrulama — statik

| Denetim | Sonuç |
|---|---|
| JS söz dizimi (`node --check`, iki kez — ilk yazımda ve düzeltmelerden sonra) | ✅ temiz |
| HTML iskelet bütünlüğü (`<!DOCTYPE>`, `</html>`, `<script>` sayısı eşleşiyor) | ✅ |
| Yinelenen `id` denetimi (kopyala düğmeleri sayaçla üretiliyor) | ✅ 0 çakışma |
| Sır/anahtar deseni taraması (`sk-…`, `gh[pousr]_…`, `AKIA…`, private key) | ✅ 0 isabet |
| Sahte ISBN deseni (978/979-…) | ✅ 0 isabet — yalnızca `PENDING` metni var |
| `/home/emre` gibi mutlak yerel yol sızıntısı | ✅ 0 isabet |
| Bayat "100 games" / "45 cultures" iddiası | ✅ 0 isabet (bulunan iki eşleşme, "no stale … claim" doğrulama adımlarının KENDİ başlığıydı — § 14'ün istediği gibi, iddia değil kontrol) |

---

## 7 · Doğrulama — gerçek tarayıcıda (statik okuma YETMEZ)

`file://` URL'leri Claude-in-Chrome uzantısı tarafından erişilemez
(güvenlik kısıtı — denendi, reddedildi). Dosyanın gerçekte nasıl
çalıştığını görmek için `08_OUTPUT/` üzerinde **geçici, yalnızca test
amaçlı** bir yerel HTTP sunucusu açıldı (`python3 -m http.server`,
localhost) ve dosya orada gerçek bir Chrome sekmesinde açılıp etkileşime
girildi. Bu, teslim edilen dosyayı DEĞİŞTİRMEDİ — yalnızca doğrulama
yöntemiydi.

**İki gerçek kusur bulundu ve düzeltildi** — ikisi de yalnızca gerçek
etkileşimle ortaya çıktı, statik okumayla görünmezdi:

1. **Kenar çubuğu gezinmesi sessizce kırıktı.** `html{scroll-behavior:
   smooth}` ayarı, A+ Content bölümüne (~15.000 px aşağıda) tıklandığında
   kaydırmayı yalnızca **24 pikselde** durduruyordu ve bir daha
   ilerlemiyordu — `window.scrollTo` ile doğrudan denendi, aynı sonuç;
   `behavior:'instant'` ile denendiğinde ANINDA ve TAM çalıştı. Kök neden
   bu test ortamının animasyonlu kaydırmayı düzgün sürmemesiydi;
   düzeltme — CSS'ten `scroll-behavior:smooth` **tamamen kaldırıldı** —
   gerçek insan tarayıcılarında da güvenilirliği artırır: uzun bir sayfada
   çalışan bir anlık atlama, duran bir animasyondan iyidir.
2. **A+ modül metni adımlarının altısı da "6" numarasını taşıyordu**
   (APLUS-01…06 için ayrı kartlar, hepsi aynı basamak numarasıyla) —
   kenar çubuğunda ve ilerleme sayısında karışıklık yaratırdı.
   **6a–6f**'ye ayrıldı.

Ayrıca doğrulandı (gerçek fare tıklamasıyla, JS'den sentetik tıklama
DEĞİL — sentetik tıklamalar Clipboard API'nin güven gerektirmesi yüzünden
kasıtlı olarak reddedilir, bu da yedek mekanizmanın gerçekten test
edildiği anlamına gelir):

- Kopyala düğmesi → panoya gerçekten yazdı (buton "✓ Copied" oldu, toast
  belirdi).
- ☐ Tamam kutusu işaretlendi → `localStorage` güncellendi, ilerleme sayacı
  ve kenar çubuğu noktası anında değişti.
- **Sayfa YENİDEN yüklendi** → kutu hâlâ işaretliydi, sayaç hâlâ doğruydu
  (kalıcılık kanıtlandı, varsayılmadı).
- "Aç" bağlantısı → doğru göreli yolu çözüp gerçek PDF'i yeni sekmede açtı.
- A+, Files, Ready, Verification bölümleri gözle incelendi — içerik,
  hiyerarşi ve renk kodlaması doğru.

**Test edilmeyen/sınırlı:** mobil dar ekran görünümü (`resize_window`
aracı bu ortamda pencereyi görünürde değiştirmedi; duyarlı CSS kuralları
yazıldı ve söz dizimi doğru ama etkileşimli olarak doğrulanamadı — talimat
zaten "masaüstü öncelikli" istiyordu, bu ikincil bir eksikliktir). Panoyu
GERİ OKUMA (`clipboard.readText()`) test edilmedi çünkü bu, otomasyonun
kilitlenmesine neden olan engelleyici bir izin iletişim kutusu tetikledi;
kopyalamanın çalıştığı görsel/durum kanıtıyla (yukarıda) zaten kanıtlandı.

---

## 8 · Proje QA'sı ve CI

| | Sonuç |
|---|---|
| `./04_BUILD/qa_all.sh` (yeni dosya eklendikten SONRA) | ✅ **BÜTÜN KAPILAR YEŞİL** |
| `validate_structure.py` manuscript sızıntı taraması | ✅ 119 dosya tarandı (yeni `.html` dahil — `LEAK_SCAN_EXT` zaten `.html` kapsıyordu), 0 sızıntı |
| `validate_structure.py` sır/sahte-ISBN taraması | ✅ 0 isabet |
| `trackedFiles` sayacı | 200 → 201 (yeni dosya + `.gitignore` istisnası birlikte doğrulandı) |
| GitHub Actions (`428fccb` — handoff.py düzeltmesi) | ✅ ayrıca push edildi ve yeşil |
| GitHub Actions (`93ee8c7` — HTML kılavuzu) | ✅ `conclusion: success` — run [`32473621110`](https://github.com/emredogan-cloud/the-great-book-of-world-games/actions/runs/32473621110), `gh run view` ile doğrulandı |

---

## 9 · Git

| | |
|---|---|
| Commit 1 | `428fccb` — kılavuzun kendi kendiyle çelişen bloklayıcı-eylem listesi düzeltmesi (ön koşul) |
| Commit 2 | `93ee8c7` — `KDP_UPLOAD_GUIDE.html` + `.gitignore` istisnası |
| Push | ✅ ikisi de `origin/main`'e gönderildi, `git rev-parse HEAD origin/main` eşit |
| Çalışma ağacı | temiz |

---

## 10 · Bilinen sınır — bu bir ANLIK GÖRÜNTÜDÜR

`KDP_UPLOAD_GUIDE.html` **elle yazıldı**, `handoff.py` gibi otomatik
yeniden üretilen bir dosya DEĞİLDİR (bilinçli karar — görev tek seferlik
bir dönüştürmeydi, kalıcı bir CI kapısı eklemek istenmedi). Şu değerlerden
biri değişirse (ISBN atanırsa, APLUS-05 sanatı gelirse, fiyat modeli
yeniden çalışırsa) **bu HTML kendiliğinden güncellenmez** — dosyanın
altbilgisinde bu açıkça yazılıdır: *"This is a snapshot… re-derive this
file from the handbook again."* Bir sonraki ajan/kurucu bu değerlerden biri
değiştiğinde HTML'i yeniden üretmeyi (ya da en azından ilgili adımı elle
güncellemeyi) hatırlamalı.

---

## 11 · Nihai durum

```
HANDBOOK PARITY   : 74/74 iz sürülebilir görev · hiçbir talimat atlanmadı
PREREQUISITE FIX  : handoff.py'nin çelişen bloklayıcı-eylem listesi (428fccb)
REAL BUGS FOUND   : 2 (scroll-behavior stall · A+ adım numarası çakışması) — İKİSİ DE gerçek tarayıcı testinde bulundu, statik okumada GÖRÜNMEZDİ
STATIC VALIDATION : sır/ISBN/mutlak-yol/bayat-sayı taramaları temiz
LIVE VALIDATION   : kopyalama · kutu kalıcılığı · gezinme · dosya açma — gerçek tıklamayla doğrulandı
QA                : qa_all.sh YEŞİL (yeni dosya dahil edilerek)
GIT               : 428fccb + 93ee8c7 — commit edildi VE push edildi
UPLOADED          : HAYIR — dokunulmadı
PUBLISHED         : HAYIR — dokunulmadı

PROJECT: The Great Book of World Games
STATUS: KDP UPLOAD READY
"Nothing in this guide means Amazon KDP actions have already been performed."
```
