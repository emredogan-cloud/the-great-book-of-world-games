# FAZ 6 · ACIMASIZ DENETİM

> Bu belge kitabın **iyi** olduğunu söylemek için yazılmadı. Faz 6'nın ikinci
> yarısında **ne bulunduğunu** ve **neyin hâlâ yapılmadığını** yazmak için
> yazıldı. Bulguların hepsi ölçülmüştür; hiçbiri izlenimden gelmez.

**Denetim tarihi:** 20 Ağustos 2026 · **commit:** `887a97e` · **CI:** yeşil

---

## 0 · Yöntem — neden bu tur bir şey buldu

Önceki turlar **kaynağı** okudu. Bu tur **basılacak dosyayı** okudu.

```
pdftotext → 160 sayfanın metni → örüntü taraması
```

Fark önemsiz görünüyor ama değil: aradaki her şey (dizgi, kaçış, üstbilgi,
SVG etiketi) kaynağı görmez. **Kusurların üçü de tam orada yaşıyordu.**

---

## 1 · BULUNAN KUSURLAR

### ① Kitap 36 daktilo kesme işaretiyle basılmaya hazırdı — KAPANDI

Manuscript düz ASCII kesme işareti taşır; dizgi tırnağına dönüşüm **render
anında** olur. Dönüşüm kuralı kapanış tırnağından önce **harf** arıyordu:

| sayfa | basılacak olan | olması gereken |
|---|---|---|
| 106 | `…rules of the game.'` | `…rules of the game.’` |
| 21, 99, 148, 149 | `‘Rules for Playing Omweso (Mweso)',` | `…(Mweso)’,` |
| 49 | `Li'b el-Merafib` (üstbilgi) | `Li’b el-Merafib` |
| 81 | `Nine Men's Morris` (üstbilgi) | `Nine Men’s Morris` |

Alıntı bir **noktayla** ya da **parantezle** bittiğinde kural tetiklenmiyordu.
Sonuç, hiç dönüştürmemekten kötüdür: **açan kıvrık, kapayan daktilo.**

**Kök neden tek bir regex değildi.** Aynı kural **üç ayrı yerde** duruyordu:

| metin yolu | dosya | durumu |
|---|---|---|
| Paragraph gövdesi | `interior.esc()` | ilk turda düzeltildi |
| SVG diyagram etiketi | `render_diagrams.text()` | **kaçtı** |
| doğrudan tuval üstbilgisi | `drawString()` | **kaçtı** |

İlk ikisi düzeltilince üçüncü sessizce daktiloyla basmaya devam etti. Kusur
ancak PDF metni **üçüncü kez** tarandığında bitti.

**Çözüm:** `04_BUILD/typo.py` — tek kural, tek yer, üç çağıran. Dönüşemeyen
düz tırnak artık **yükseltir**; sessizce basmaz.

**Yan bulgu:** `render_diagrams.text()` **hiç XML kaçışı yapmıyordu**.
Etiketteki bir `&` geçersiz SVG üretirdi. Aynı yamada kapandı.

### ② EPUB kapaksızdı ve yazar biyografisi yoktu — KAPANDI

Künye sayfasında kanonik biyografi eksikti ve dosya kendi kapağını
taşımıyordu. Kindle kapağı KDP formunda ayrıca yüklenir, ama EPUB başka bir
okuyucuda açıldığında kapaksız kalırdı. Şimdi EPUB 3
(`properties="cover-image"`) **ve** EPUB 2 (`<meta name="cover">`) — KDP'nin
dönüştürücüsü ikincisini okur.

### ③ Kapak kapısı kendi körlüğünü gösterdi — KAPANDI

`covers.py --build` yalnızca `cover-build.json`'u tazeliyordu; `--check` ise
`cover-geometry.json`'u okur. İç blok yeniden üretilince kapak **taze**,
kayıt **bayat** kaldı ve kapı haklı olarak kırmızı yandı. `--build` artık
önce geometriyi tazeliyor.

### ④ CI, push edilince kırıldı — üç kez — KAPANDI

Faz 6 commit'leri **hiç push edilmemişti**, yani CI onları ilk kez gördü.

| # | kusur | neden yerelde görünmedi |
|---|---|---|
| 1 | `qa_lineedit`, `qa_visual` `--verbose` kabul etmiyordu | `qa_all.sh` onları bayraksız çağırıyor; CI `--verbose --json` ile çağırır |
| 2 | `kdp_preflight`'ın "ATLANDI" sinyali (çıkış 2) kırmızı sayılıyordu | yerelde `pdfinfo` **kurulu** |
| 3 | aynı kusur iş akışında **altı** ayrı yerde | yerelde `reportlab` **kurulu**; atlama yolu hiç koşmuyordu |

**Kök neden hepsinin altında aynıydı:** elle yazılmış bir "CI simülasyonu"
gerçek komutları **tahmin** ediyordu. İki kaynak varsa biri bayatlar.

**Çözüm iki parçalı:**

- `04_BUILD/ci_run.sh` — `0 yeşil · 1 KIRMIZI · 2 ATLANDI` konvansiyonu **tek
  yerde**. Her kapı çağrısı bundan geçer.
- `05_TESTS/ci_simulate.py` — komutları **tarif etmez**, `validate.yml`
  içindeki `run:` bloklarının kendisini, yalnızca `git ls-files`
  dosyalarından kurulu geçici bir ağaçta koşturur. `--without reportlab,PIL`
  bağımlılığı olmayan runner'ı taklit eder.

Üçüncü kusuru **bu ikinci mod buldu**, GitHub değil.

---

## 2 · YENİ KAPILAR — bulunan her kusur bir kapıya dönüştü

| kapı | ne yapar | nerede |
|---|---|---|
| daktilo tırnağı | **basılmış PDF'te** düz tırnak arar | `kdp_preflight.py` |
| dizgi birimi | 7 dönüşüm + kaçış sırası + dönüşemeyene yükseltme | `selftest.py § ⑪` |
| kopya kural yasağı | üç render yolu da `typo`'dan almalı | `selftest.py § ⑪` |
| CI tarama sözleşmesi | her `qa_*.py` `--verbose --json` kabul etmeli | `selftest.py § ⑫` |
| uçtan uca dizgi | `typo.smart` etkisizleştir → iç bloğu yeniden üret → ön denetim ısırmalı | `package_selftest.py` |

> Denetim **kaynakta değil çıktıda** durur — kusur tam da orada doğmuştu.

**Kapı sayısı:** `selftest` 192 → **214** · `package_selftest` 38 → **39**

---

## 3 · İNCELENDİ VE KUSUR ÇIKMADI

Bunlar "bakılmadı" değil, **bakıldı ve temiz çıktı** demektir.

| tarama | sonuç |
|---|---|
| dengesiz parantez | 17 aday — **hepsi satır kaydırma yanılması**; sayfa düzeyinde denge tam |
| `Mbube Mbube` tekrarı | **oyunun gerçek adı** (`book.json § title`) |
| yasak iddia (bestseller, ödül, çocuk testi, garanti) | 6 yüzeyin 6'sında **temiz** |
| uydurma ISBN / barkod | **yok** — her yerde `PENDING — KDP-PROVIDED ISBN` |
| sayı tutarlılığı | kapak · iç blok · EPUB · A+ · metadata → **56 oyun / 39 kültür**, sapma yok |
| iç bloktaki diğer sayılar | içindekiler sayfa numaraları + malzeme dizini (`15 games` = o malzemeyi isteyen oyun sayısı) — **hepsi gerçek** |
| gömülü font | 4 yüz, hepsi gömülü + altküme; Helvetica taban kaynağı **yok** |
| mürekkep payı | en dar 0.486 in (KDP asgarisi 0.25) |
| tırnak taraması (nihai) | 4 çıktının 4'ünde **0 daktilo tırnağı** |

---

## 4 · GÜVENLİK DENETİMİ

**İzlenen depo — 194 dosya**

| örüntü | bulgu |
|---|---|
| API anahtarı, gizli, jeton, özel anahtar | **0** |
| AWS / GitHub / OpenAI kimlik biçimleri | **0** |
| özel e-posta | **0** |
| yerel mutlak yol | **1** — `ASSET_UPSCALING_REPORT.md` içinde `/home/emre/…` |

Tek bulgu **kurucunun kendi çalıştırma kılavuzudur** ve upscayl ikilisinin
yerini gösterir. Gizli bilgi değildir, kimlik bilgisi değildir; belge altı
kardeş projeye aynı biçimde kopyalanmıştır. **Bilerek bırakıldı**, çünkü
burada değiştirmek kopyalarla ayrıştırır.

**Teslimatlar — KDP'ye giden dosyalar**

Ham tarama sekiz bulgu verdi; **sekizi de doğrulandı ve yanlış pozitif çıktı**:

| görünen bulgu | gerçeği |
|---|---|
| `token` (iç blok, EPUB) | oyun sözlüğü — *"move your token that many squares"* |
| `placeholder` (previewer listesi) | İngilizce düzyazı — *"KDP rejected a placeholder biography"* |
| Türkçe karakter (kapak, iç blok) | **EMRE DOĞAN** ve **Vâliçe Press** — yazar ve yayıncı adı |
| Türkçe metin (`aplus_content.json`) | yalnızca `$comment` / `$note` anahtarlarında; Amazon'a giden **12 metin alanının 12'si İngilizce** |
| Türkçe metin (`KDP_UPLOAD_HANDBOOK.md`) | kurucunun kendi kılavuzu — Amazon'a yüklenmez |

**PDF künyesi denetlendi:** `Title`, `Author`, `Subject` doğru; `Creator`
alanı `04_BUILD/interior.py` yazıyor — **göreli** bir betik adı, mutlak yol
ya da kullanıcı adı **değil**. İncelendi, kabul edildi.

---

## 5 · YAPILMAYANLAR — açıkça

### Ajanın yapamayacağı (kurucu eylemi)

| # | ne | neden ajan yapamaz |
|---|---|---|
| 1 | **AI beyanı** (`founder.aiDisclosure.founderConfirmed`) | hukuki bir beyandır, seçim kurucunundur. Olgular `08_OUTPUT/KDP_AI_DISCLOSURE_NOTES.md` içinde hazır — **beyanın kendisi yazılmadı** |
| 2 | **Dış oyun testi** (`01_SOURCE/playtests/`) | kitabı gerçek bir masada oynayacak insan gerekir. `qa_playable`: *dış kanıt 0* |
| 3 | **APLUS-05 sanatı** | teslim edilmedi (bloklamaz — A+ projesi 5 modülle yüklenebilir) |
| 4 | **ISBN ×2** | KDP atar. Uydurulmadı |
| 5 | **Ciltli şablon doğrulaması** | sırt hesabı (`0.0025 in/sayfa + 0.06 in tahta`) **hipotezdir**; KDP şablonuyla karşılaştırılmadı |
| 6 | KDP Previewer · yükleme · fiziksel prova | Amazon hesabı gerektirir |

### Ajanın yapmadığı — ve nedeni

| ne | neden |
|---|---|
| **Kalan 44 oyun yazılmadı** | kaynak yok. Uydurmak yasaktı ve uydurulmadı |
| **`.gate` `release`'e alınmadı** | release kapısı **≥100 kilitli oyun** ister; ölçülen 56. Kapıyı geçirmenin tek yolu ya 44 oyun uydurmak ya da eşiği düşürmekti. **İkisi de yapılmadı** — eşik bir kurucu kararıdır (aşağı bkz.) |
| **Sürüm etiketi atılmadı** | yol haritası Faz 6 için `etiket: yok` diyor |

---

## 6 · KURUCU KARARI BEKLEYEN ÇELİŞKİ

`project_config.json` üç yerde **100 oyun** yazıyor
(`gates.requirements.{phase4,phase5,release}`), `scope.games` da 100.
**Basılan kitapta 56 oyun var** ve bu sayı her yüzeyde dürüstçe duruyor.

Yani `release` kapısı **tasarımı gereği** geçilemez durumda. Bu bir kusur
değil, **kapsamın küçüldüğünün kaydıdır** ve kapı bunu saklamıyor.

**Karar kurucunundur:**

- **(a)** 56 oyunu nihai kabul et → eşikleri 56'ya çek, `.gate` → `release`
- **(b)** 100 hedefini koru → Faz 7 açılır, 44 oyun için kaynak gerekir

Ajan **hiçbirini seçmedi**. Seçmek kapsamı değiştirmektir.

---

## 7 · DURUM

| | |
|---|---|
| basılan kitap | **160 sayfa** · 56 oyun · 39 kültür · 7 aile |
| biçim | ciltsiz · ciltli · Kindle — **üçü de üretildi ve doğrulandı** |
| kapak | ciltsiz sırt **0.3603 in** · ciltli **0.4600 in** — ölçülen sayfadan |
| tipografi | güvenli alan ihlali **0** · daktilo tırnağı **0** |
| A+ | **5 / 6** modül yüklenebilir |
| kapılar | `qa_all` yeşil · selftest **214** · paket testi **39/39** |
| CI | **yeşil** (`887a97e`) |
| git | `main` temiz · `origin/main` ile eşit |
| checksum | 4 dizinde `SHA256SUMS` **doğrulandı** |

**Ajan Amazon'a dokunmadı. Yükleme yapılmadı, yayın yapılmadı, prova
sipariş edilmedi.**
