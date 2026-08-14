# FAZ 4 RAPORU — Erişilebilir havuzun açılması ve ölçümün üç kapı kusuru bulması

> **The Great Book of World Games** · Faz 4 · Dal: `faz/4-blok-2`
>
> Bu faz on bir oyun yazdı ve **beş kapı kusuru** buldu. İkincisi
> birincisinden daha değerlidir; bu cümle Faz 3 raporunda da vardı ve
> tekrar doğru çıktı.
>
> **En önemli tek sonuç bir sayı değil bir düzeltmedir:** Faz 2'nin
> *"sayfa bütçesi bir diyagram bütçesidir"* cümlesi **yanlışlandı**.

---

## 0 · Tek bakışta

| | Faz 3 | **Faz 4** | |
|---|---:|---:|---|
| Yazılmış oyun | 11 | **22** | +11 |
| Doğrulanmış künye | 17 | **28** | +11 |
| Doğrulanmış oyun | 14 | **25** | +11 |
| Dizgi örneklemi | 11 oyun | **22 oyun** | ×2 |
| Ölçülen kelime/sayfa | 405 | **447** | |
| Ölçülen sayfa/oyun | 1,52 | **1,53** | |
| Çift sayfa taşma oranı | %9 | **%4,5** | 1/22 |
| **Kitap sayfa modeli** | **268** | **258** | −10 |
| **Hedeften sapma** | +%4,7 | **+%0,8** ✅ | |
| Ciltsiz birim telif | 8,24 $ | **8,41 $** | +0,17 $ |
| Ciltli birim telif | 10,79 $ | **10,96 $** | +0,17 $ |
| Diyagram (render) | 16 | **27** | hepsi ≤150 mm |
| Diyagram dili | v1.3 | **v1.4** | `bodily/bed` |
| Selftest denetimi | 126 | **148** | +22 |
| **Kuyrukta "engelli" gösterilen** | **80** | **5** | −75 |
| Erişilebilir oyun | 20 | **94** | +74 |
| CI | yeşil | **yeşil** | |
| **Dış insan testi** | **0** | **0** | ⛔ değişmedi |
| **`.gate`** | `phase1` | **`phase1`** | yükseltilmedi |

---

## 1 · Faz 4 kapsamı — roadmap ne diyor

Yol haritasının Faz 4 tanımı iki şey söyler ve ikisi de burada geçerlidir:

| Roadmap § | Ne diyor |
|---|---|
| § 2 · Kapsam | Aileler **V–VII**: `war-board` · `chance` · `boardless` + arka madde |
| § 10 · DoD | **100 oyun yazıldı ve `locked`** — manuscript özünde tamam |

K13 yeniden dengelemesinden sonra aileler V–VII **47 oyundur**
(17 + 15 + 15), roadmap'in yazdığı 43 değil. Sayı yeniden hesaplandı,
**uydurulmadı**: roadmap 43'ü K13 öncesi hedeflerle (war-board 13) yazmıştı.

**Devralınan borç açıkça kaydedilir.** Faz 3'ün kendi kapısı 57 oyun
istiyordu ve 11 yazıldı. O borç silinmedi; Faz 4 kuyruğu **yüz oyunun
tamamını** taşıyor ve aileler I–IV'ün yazılmamış maddeleri orada
duruyor. Faz 4'ün ilan edilen kapsamı V–VII'dir; kalibrasyon batch'i
çeşitlilik gereği (§ 20) I–IV'ten de madde içerdi ve bunlar **Faz 3
borcunun kapatılması** olarak sayıldı, Faz 4 kapsamı olarak değil.

---

## 2 · Kurucu istisnası — K21

Kurucu talimatı iki cümleydi: *"Testlerin halledildiğini varsay ve Faz 4
üretimine devam et. Engelli oyunları sona bırak."*

| | Durum |
|---|---|
| **Faz 4 üretim işi** | ✅ **YETKİLİ ve YAPILDI** |
| **Resmî faz kapısı** | ⛔ **AÇILMADI — `.gate` = `phase1`** |
| **Dış oynanabilirlik testi** | ⛔ **`pending` — 0 oturum** |
| **`locked` oyun** | **0 — uydurulmadı** |

```
PRODUCTION       : AUTHORIZED
FORMAL VALIDATION: PENDING
```

"Testleri halledilmiş say" **üretimi durdurmamak** demektir; **kanıt
uydurmak** demek değildir. Hiçbir maddede `externalPlaytest = passed`
yazmıyor, hiçbir testçi adı yok, hiçbir süre kaydı yok.
`01_SOURCE/playtests/` **hâlâ boştur** ve `qa_manuscript.py` artık kaydı
olmayan bir `locked` maddeyi mekanik olarak reddediyor (§ 17).

---

## 3 · Yazılan on bir oyun

Hepsi **doğrudan İngilizce** yazıldı; hepsi sayfa seviyesinde doğrulanmış
**birinci elden** bir kaynağa dayanıyor.

### Batch 1 — kalibrasyon (8 oyun)

| Oyun | Aile | Kültür | Kaynak | Çeşitlilik rolü |
|---|---|---|---|---|
| **Seega** | savaş tahtası | Mısır Arabı | Lane 1846 II, ss. 188–189 | ızgara, iki editoryal kural |
| **Tab** | eve dönüş | Mısır Arabı | Lane 1846 II, ss. 185–188 | **en karmaşık** — beş kural bloğu |
| **Nine Men's Morris** | çizgi-toprak | Ortaçağ Avrupası | Gomme 1894 I, ss. 414–417 | **iki aşamalı**, 24 düğümlü graph |
| **Fox and Geese** | av-kuşatma | İngiliz | Gomme 1894 I, ss. 141–142 | **ASİMETRİK** — 17'ye 1 |
| **Fivestones** | tahtasız | İngiliz | Gomme 1894 I, ss. 122–126 | **tahtasız**, dokuz figür |
| **Hopscotch** | tahtasız | İngiliz | Gomme 1894 I, ss. 223–227 | **çok oyunculu**, yatak = yeni tahta sınıfı |
| **Totolospi** | eve dönüş | Hopi | Culin 1907, ss. 160–162 | 2–4 kişi · **Faz 3 çelişkisi çözüldü** |
| **Set-dilth** | şans | White Mountain Apache | Culin 1907, ss. 88–89 | **çok oyunculu**, ortaklı, K5 |

### Batch 2 — tahtasız aile (3 oyun)

| Oyun | Aile | Kültür | Kaynak | Rol |
|---|---|---|---|---|
| **Jan-ken** | tahtasız | Japon | Culin 1895, ss. 44–46 | kitabın **en basit** oyunu · diyagramsız |
| **Conkers** | tahtasız | İngiliz | Gomme 1894 I ss. 77–78 · 1898 II s. 471 | diyagramsız · devralınan puan |
| **Marbles** | tahtasız | İngiliz | Gomme 1898 II, ss. 113–114 | K5 · "fat" kuralı |

Yedi ailenin **yedisi** de manuscript'te temsil edildi. Kültür sayısı
**14**'e çıktı.

### 3.1 Kaynak türü — K20 uygulandı

Üç kaynak da **birinci eldendir** ve üçü de farklı bir birinci ellik
türünü temsil eder:

| Kaynak | Türü | Neden birinci el |
|---|---|---|
| **Lane 1846** | yerleşik gözlemci | Kahire'de Mısırlı bir evde yaşadı; oynanırken gördü |
| **Gomme 1894/98** | muhabir ağı + kendi gözlemi | Fivestones'u Richmond istasyonunda **kendisi izledi** |
| **Culin 1907** | müze envanterli saha kaydı | levhalar Chicago ve Philadelphia koleksiyonlarında |

Falkener 1892 (Viktorya derlemesi) bu batch'te **hiçbir maddenin
dayanağı olmadı** — Faz 3'ün K20 kararı yürürlükte kaldı.

---

## 4 · TOTOLOSPI ÇELİŞKİSİ ÇÖZÜLDÜ

Faz 3, Totolospi'yi bir kural kimliği çelişkisi yüzünden ertelemişti:
envanter kaydı `race` ailesindeydi ama bulunan sayfa bir **atlamalı dama**
anlatıyordu.

**Çelişki bir hata değildi; iki ayrı oyundu — ve bunu söyleyen Culin'in
kendisidir.** s. 796'daki dipnot şöyle der:

> *"The same name, totolospi, is applied by the Tewa at Hano to the foreign
> Mexican (Spanish) game like Fox and Geese."*

| | Hopi totolospi | Tewa (Hano) totolospi |
|---|---|---|
| Nerede | Culin 1907, **ss. 160–162** | Culin 1907, ss. 795–797 |
| Ne | **zar yarışı** — çubuk zar, tek taş, çizgi çizgi ilerleme | atlamalı dama |
| Envanter kaydı | **`race` · Hopi** ✅ | kapsamda değil |

Faz 3 Tewa kaydına bakmıştı. Kitap Hopi yarışını basıyor ve **hangisini
bastığını prozanın ilk cümlelerinde söylüyor**.

Bu, `source_access_pending.json § resolvedInPhase4` içinde kayıtlıdır.

---

## 5 · Kaynak durumu ve KUYRUK — en büyük düzeltme

| Durum | Faz 3 | **Faz 4** |
|---|---:|---:|
| `verified` — ≥2 doğrulanmış künye | 3 | **3** |
| `partially-verified` — 1 doğrulanmış künye | 11 | **22** |
| `access-blocked` — denendi, erişilemedi | 4 | **5** |
| `not-attempted` — henüz sıraya gelmedi | 82 | **70** |

### 5.1 Kuyruk beş seviyeye ayrıldı (K22)

Faz 3 kuyruğu **80 oyunu en düşük önceliğe** koyuyordu, çünkü "denenmedi"
ile "engellendi" aynı kovaya düşüyordu. Sayı yanlış değildi; **anlamı**
yanlıştı. Bir üretim planlayıcısı ona bakıp kitabın dörtte üçünün kaynak
beklediğini okurdu.

| P | Anlamı | Faz 3 | **Faz 4** |
|---|---|---:|---:|
| 1 | erişilebilir · sayfa-doğrulanmış · kural tam | 13 | **24** |
| 2 | erişilebilir · doğrulama tamamlanabilir | 1 | **65** |
| 3 | yeniden kurgulanmış · plan belgeli | 6 | **5** |
| 4 | **DENENDİ ve erişilemedi** | **80** | **5** |
| 5 | çözülmemiş kural kimliği | — | **1** |

**Erişilebilir oyun sayısı 20 → 94.**

Sıra artık bir **kapıdır**: `build_queue.py --check` engelli bir oyunun
erişilebilir bir oyunun önüne geçmesini reddeder ve CI'da koşar. Gerekçe
tek cümledir: o durumda üretim, **açık bir kaynak dururken kapalı bir
kaynağı bekler**.

### 5.2 Faz 3 verisinde bir düzeltme

`royal-game-of-ur` iki kaynağı da denenmiş ve erişilememişti (Finkel 2007
telifli; British Museum nesne kaydı HTTP 403) ama engelli kuyrukta
**görünmüyordu**. Eklendi.

> Denenip erişilemeyen bir oyunun engelli kuyruğunda görünmemesi, engeli
> **küçümsemenin** bir biçimidir. Faz 3 abartmayı düzeltmişti; Faz 4
> küçümsemeyi düzeltti.

---

## 6 · Ertelenen oyunlar — gerekçeleriyle

| Oyun | Neden ertelendi |
|---|---|
| **Sugoroku** (Japon) | Culin'in `ssang-ryouk` bölümü **Kore** oyununu anlatıyor ve hamleler için *"the English game of Backgammon"*a gönderiyor; Japon kaydı yalnızca bir tahta resmidir. Japon oyununu Kore bölümünden yazmak tam olarak **Totolospi tuzağıdır**. |
| **Jianzi** (Han Çinlisi) | Culin'in tüylü top bölümü **nesneyi** anlatıyor, kuralı değil. Puanlama yok, tur yok, bitiş yok. Kural metni yazılamaz. |
| **Xiangqi** (Han Çinlisi) | Culin 1895 § LXXIV **Kore** satrancıdır; Çin satrancı karşılaştırma notudur. Aynı gerekçe. |
| **Marbles → "Marbles" başlığı** | Gomme'nin `Marbles` maddesi bir **sözlük** maddesidir, kural vermez. Kural `Ring-taw` başlığındadır ve madde oradan yazıldı; künye bunu söylüyor. |

**Hiçbiri silinmedi.** Dördü de kuyrukta kendi öncelik seviyesinde bekliyor.

---

## 7 · ÖLÇÜM ÜÇ KAPI KUSURU BULDU

Bu, Faz 4'ün en değerli çıktısıdır. Üç kusur da **gerçek veriyle yeşil
koşan** kapılardaydı — yani hiçbiri bir hata mesajı vermiyordu.

### 7.1 150 mm bütçesi OYUN BAŞINA tanımlı, DİYAGRAM BAŞINA denetleniyordu

Ayarın adı zaten `maxDiagramMmPerGame` ve türetimi de oyun başınadır
(çift sayfanın metinden artan 152 mm'si). Kapı ise her diyagramı tek tek
ölçüyordu.

**Tablut tam olarak bunu yapıyordu:** 88,5 + 93,0 = **181,5 mm**, bütçeyi
%21 aşıyor ve kapıdan **geçiyordu**. Üstelik on dokuz maddelik örneklemde
çift sayfayı aşan **tek madde** oydu — yani bütçe, tutması gereken şeyi
tutmuyordu.

**Düzeltme iki taraflıdır:**

1. `qa_diagram.py § ⑨` artık oyun başına **toplamı** da denetliyor.
2. `tablut-capture` bir **ayrıntıya** daraltıldı (9×9 → 3×3).

| | önce | sonra |
|---|---:|---:|
| tablut-setup | 88,5 mm | 88,5 mm |
| tablut-capture | 93,0 mm | **55,5 mm** |
| **oyun toplamı** | **181,5** ⛔ | **144,0** ✅ |

**Adım aralığı (7 mm), çizgi kalınlığı (0,75 pt) ve glif boyu (7 pt)
DEĞİŞMEDİ.** Giden şey tahtanın oyunla ilgisi olmayan altı sırasıdır —
alma, tafl tahtasında üç karelik bir olaydır. Bu bir **sadeleştirmedir**,
K19'un yasakladığı "okunmaz hâle gelene kadar küçültme" değildir.

### 7.2 Efsane sembolü bir FONT KARAKTERİYDİ

Efsane satırı `lang.glyphs[...].symbol` metnini basıyordu (◉, ◎, ⤳ …).
Font o karakteri taşımıyorsa **yer boş kalıyordu**: `foxgeese-setup`
diyagramında **tilki efsanede sembolsüz duruyordu** ve okur hangi taşın
tilki olduğunu efsaneden öğrenemiyordu.

Bu, render denetimi **görsel olarak** yapıldığı için bulundu; ölçüm
sayıları temizdi.

**Düzeltme:** efsane sembolü artık **çiziliyor** — tahtadaki glifin aynı
çizim yolundan. Font bağımlılığı kalmadı.

### 7.3 Alma çarpısı (×) hiçbir efsanede AÇIKLANMIYORDU

`captured: true` bir **bayraktır** ama okur için bir **semboldür**: taşın
üstüne bir çarpı basar. Bayrak olduğu için "kullanılan semboller"
kümesine girmiyordu, dolayısıyla:

- efsaneye eklenemiyordu (kapı "ölü sembol" hatası veriyordu),
- eklenmediği için × **açıklamasız** kalıyordu,
- ve koyu taşta **siyah üstüne siyah** çiziliyordu — yani en çok
  kullanıldığı yerde görünmüyordu.

**Düzeltme üç taraflıdır:** `captured` artık kullanılanlar kümesine
giriyor (yani efsane onu **açıklamak ZORUNDA**), çarpı taşın mürekkebinin
tersine çiziliyor, ve efsanedeki sembol de çarpılı çiziliyor.

Beş diyagram etkilendi: `tablut-capture` · `go-9x9-capture` ·
`fanorona-withdrawal` · `seega-capture` · `morris-mill`.

### 7.4 `calibrate_pages.py` sonucu KODA GÖMÜLÜ basıyordu (§ 8)

### 7.5 `fivestones` maddesinde KURULUM BLOĞU YOKTU

`qa_manuscript.py` ilk koşusunda buldu. Madde figürlerle başlıyordu ve
okur halkayı nasıl kuracağını **hiçbir yerde** bulamıyordu — beş öğeden
biri eksikti ve proza okunurken **fark edilmemişti**. Eklendi.

> Bu, kitabın ölüm biçiminin tam örneğidir: kusursuz görünen bir madde,
> masada oynanamaz. Bir insan okuması bunu kaçırdı; bir kapı kaçırmadı.

---

## 8 · SAYFA MODELİ — Faz 2'nin bulgusu TERSİNE DÖNDÜ

| | Faz 2 (3) | Faz 3 (11) | **Faz 4 (22)** |
|---|---:|---:|---:|
| Kelime / sayfa | 389 | 405 | **447** |
| Kelime / oyun | 708 | 616 | **686** |
| Metin sayfa/oyun | 1,37 | 1,18 | **1,25** |
| **Metin farkı** | **0,01** | 0,41 | **0,69** |
| **Diyagram farkı** | **0,55** | 0,62 | **0,63** |
| Ölçülen sayfa/oyun | 1,82 | 1,52 | **1,53** |
| Faturalanan sayfa/oyun | 2,67 | 2,18 | **2,09** |
| **Taşma oranı** | %33 | %9 | **%4,5** |
| **Toplam** | **316** | **268** | **258** |
| **Sapma** | +%23,4 ⛔ | +%4,7 ✅ | **+%0,8** ✅ |

### 8.1 Gömülü bir sonuç, ölçümü olmayan bir iddiadır

Faz 2 üç oyunda *"metin sabittir (fark 0,01), değişken diyagramdır (fark
0,55)"* buldu ve bu cümle `calibrate_pages.py` içine **sabit metin**
olarak gömüldü. Her koşuda basıldı.

Faz 3'te metin farkı 0,41'e çıktı ve cümle zayıfladı — rapor bunu yazdı
ama **kod değişmedi**. Faz 4'te metin farkı **0,69** oldu ve diyagram
farkını (0,63) **geçti**: yani gömülü cümle artık kendi verisini
yalanlıyordu ve **yine de her koşuda basılıyordu**.

**Düzeltme:** `calibrate_pages.py` sürücüyü artık **ölçümden türetiyor**
ve üç sonuçtan birini yazıyor (`diagram` · `text` · `both`). 22 oyunda
sonuç **`both`**: tek bir sürücü yoktur.

Aynı koşuda iki gömülü değer daha bulundu ve ikisi de türetmeye çevrildi:
`measuredOn` her ölçümde `"phase2"` yazıyordu, ve `sampleCaveat` her
ölçümde *"örneklem 3 oyundur"* diyordu — Faz 3'ün 11 oyunluk dosyası bile
öyle yazıyordu.

### 8.2 150 mm bütçesi neden hâlâ duruyor

Sürücü tek değilse bütçe neden kalıyor? Çünkü iki sürücünün **yalnızca
biri** bir tavan taşıyor:

| Sürücü | Tavanı |
|---|---|
| Kelime | 900 kelime bandı · `qa_length` |
| Diyagram | **150 mm** · `qa_diagram` |

Gerekçe değişti, kural kalmalı: bütçe artık "tek sürücü diyagramdır" diye
değil, **iki sürücüden birinin sert bir tavana ihtiyacı olduğu** için var.

### 8.3 Ekonomik sonuç

| Sürüm | Faz 3 (268 s.) | **Faz 4 (258 s.)** |
|---|---:|---:|
| Ciltli telif | 10,79 $ | **10,96 $** |
| **Ciltsiz telif** | **8,24 $** | **8,41 $** |
| Başabaş ACOS (ciltli) | %30,8 | **%31,3** |

---

## 9 · Diyagram dili v1.4 — `bodily/bed`

Faz 3, `point` sınıfını düzensiz tahtalar için genişletmişti (v1.3).
Faz 4'ün ilk batch'i dili yine kırdı — bu sefer **bölmelerde**.

Seksek yatağı bir ızgara **değildir**: sekiz bölme, kimi tek kimi yan yana
çift. İki sütunlu bir ızgarayla çizmek **on iki** bölme üretir ve okur o
yatağı zemine çizip **oynayamaz**.

**Çözüm:** `bodily` sınıfına üçüncü bir çerçeve eklendi. `bed` bölmeleri
**açıkça listeler** (kimlik · sol üst köşe · genişlik · yükseklik ·
etiket) ve sınır denetimi tanımlı bölme kümesidir.

**Ekleme geriye dönük DEĞİLDİR** — mevcut hiçbir tanımlayıcı değişmedi.
Dondurma, dilin **büyümesini** değil mevcut notasyonun **değişmesini**
yasaklar; v1.2 → v1.3 geçişi de böyleydi.

### 9.1 Yirmi yedi diyagramın ölçümü

| | |
|---|---:|
| Render edilen diyagram | **27** |
| En küçük | 36,1 mm (`olinda-setup`) |
| En büyük | 111,5 mm (`gonggi-toss`, `catscradle-cradle`) |
| Ortalama | **66,1 mm** |
| **150 mm'yi aşan DİYAGRAM** | **0** |
| **150 mm'yi aşan OYUN** | **0** (azami: tablut 144,0) |

### 9.2 İki madde DİYAGRAMSIZ ve bu bir karardır

`jan-ken` üç el biçimidir; `conkers` ipe geçirilmiş iki meyvedir. İkisini
de bir cümle, bu kitabın diyagram dilinden daha iyi anlatır.

> Çizilemeyen bir şeyi çizilmiş gibi göstermek, kuralla diyagram arasında
> **sahte bir uyum** üretir — ve bu kitapta diyagram doğruluğu dördüncü
> önceliktir.

`marbles-ring` diyagramı halkayı ve atış çizgisini çiziyor ama **atış
duruşunu çizmiyor**; aynı gerekçe.

---

## 10 · İç simülasyon ve dış insan kanıtı

| Kanıt türü | Sayı |
|---|---:|
| `internal` — ajan / doğrulayıcı | 0 |
| **`external` — gerçek insan** | **0** |

`01_SOURCE/playtests/` **hâlâ boştur.** Sahte kayıt üretilmedi ve iç
doğrulama dış kanıt diye sunulmadı.

Faz 4 buna bir **mekanizma** ekledi: `qa_manuscript.py § ⑤` kaydı olmayan
bir `locked` maddeyi reddediyor ve `selftest` bunu her koşuda sınıyor.
Yani bundan sonra bir maddeyi testsiz kilitlemek **kod düzeyinde**
imkânsızdır, disiplin düzeyinde değil.

Her madde `EXTERNAL PLAYTEST PENDING` durumundadır ve yirmi ikisi de
`draft` seviyesindedir.

---

## 11 · İngilizce editoryal durum

On bir madde de **doğrudan İngilizce** yazıldı. Türkçe hiçbir aşamada ara
dil olarak kullanılmadı.

Her madde yedi başlıkta bağımsız doğrulama kaydı taşır ve
`qa_manuscript.py` yedisinin de dolu olmasını **şart koşuyor**.

**Tekrar eden AI kalıbından kaçınıldı.** On bir kültürel hikâyenin hiçbiri
aynı kalıpla açılmıyor: biri Büyük Piramit'in tepesine kazınmış tahtalarla,
biri bir gazete çocuğunun Richmond istasyonunda oynadığı oyunla, biri
jinrikişa çekicilerinin müşteri paylaşmasıyla, biri bir kelimenin üç ayrı
anlamıyla, biri yaygın bir efsanenin düzeltilmesiyle başlıyor.

### 11.1 Bir efsane düzeltildi

Seksek maddesi, "Roma askerlerinin talim için icat ettiği" iddiasının
**hiçbir kaynağa dayanmadığını** açıkça yazıyor ve bunu kültürel hikâyenin
**açılışına** koyuyor. Envanter kaydı bunu bir düzeltme fırsatı olarak
işaretlemişti.

> Yaygın bir iddianın nasıl kaynaksız olabileceğini göstermek, bir oyun
> kitabının okuruna verebileceği en yararlı şeylerden biridir.

### 11.2 Terminoloji kararları

- **Tab:** Lane'in kaydettiği `Nasara` (Hristiyanlar) → `Muslimeen`
  (Müslümanlar) taş adlandırması **aktarılmadı**. Bir kural metninde din
  adları taş adı olarak basılamaz ve terim oyunun mekaniğini değil 19.
  yüzyıl Mısır'ının bir söz oyununu anlatır. Yerine `asleep` / `wake`
  seçildi. Terim kaynakta durur, kitapta durmaz.
- **Marbles:** kaynağın `taw` kelimesi üç şeyi birden anlatıyor (çizgi ·
  atış taşı · atmak). Kural metninde **hiç kullanılmadı**; üç ayrı kelime
  kondu ve belirsizlik kültürel hikâyede **açıklandı**.
- **Seega ↔ Morris:** `hole` ile `point` bilinçli olarak ayrıldı ve gerekçe
  iki maddede de yazılı — Lane'in tahtası yere kazılmış çukurlardır,
  morris tahtası bir çizgi ağıdır.

---

## 12 · Türkçe test malzemesinin yalıtımı

| | |
|---|---|
| Ticari katmanda Türkçe | **0** |
| Türkçe pilot işareti ticari katmanda | **0** |
| Çeviri beyanı taşıyan ticari kayıt | **0** |
| `qa_language_split.py` | ✅ 13 denetim yeşil |

Faz 4'te **hiç Türkçe ticari içerik üretilmedi**. `qa_manuscript.py § ⑦`
artık `translatedFrom` dolu bir ticari maddeyi de reddediyor.

---

## 13 · Kültürel bulgular

### 13.1 Set-dilth bir kadın oyunudur

Culin'in **ilk cümlesi** oyunun kadınlar tarafından oynandığını ve
erkeklerin oynadığına dair bir kayıt bulunmadığını söyler. Bu, Zohn Ahl
maddesindeki ilkeyle aynı: kültürel hikâyenin **ortasına** kondu, dipnota
değil.

### 13.2 Fox and Geese — aynı ad, iki oyun

Gomme'nin cildinde bu adı taşıyan **iki ayrı oyun** vardır: biri tahta
oyunu, biri kırda oynanan bir kovalamaca. Kitap tahta oyununu basıyor ve
öteki maddeyi kültürel hikâyede **anıyor** — aynı ad iki oyun demektir ve
kitap bunu gizlemez.

### 13.3 Aktarılmayan iddialar

- **Kurna Tapınağı, MÖ 1400** (nine-mens-morris). Envanter kaydı bunun
  tarihlendirilemez olduğunu işaretlemişti. **Basılmadı.**
- **"Roma askerleri seksek icat etti."** Açıkça yanlışlandı (§ 11.1).
- **Voth'un "tam olarak incelenmemiş" koşulları** (totolospi). Kaynağın
  kendi ifadesiyle prozada bırakıldı; uydurulmadı.

---

## 14 · Malzeme ve güvenlik

| Madde | Karar |
|---|---|
| **Conkers** | Sertleştirme (fırınlama, ıslatma) **yasaklandı** — eski bir hile ve oyunu bir kimya yarışına çevirir. Parçalanan malzeme yasak. |
| **Marbles** | Sert, düz zemin şartı yazıldı; çim "her şeyi yutar". |
| **Set-dilth** | Yeşil dal yerine dondurma çubuğu ikamesi verildi. |
| **Tab** | Dört kişilik biçimin **ayak tabanına sopa vurma** cezası basılmadı ve puana çevrildi (K5). |

**Olinda Keliya**'nın Faz 3'te kurulan güvenlik/oynanabilirlik ayrımı
korunuyor: güvenlik künyeli bir olgudur, oynanabilirlik dış test bekler.

---

## 15 · K5 — kumar çerçevesi

Üç maddede bahis mekaniği vardı ve üçünde de **görünür** biçimde
değiştirildi:

| Oyun | Kaynakta | Kitapta |
|---|---|---|
| **Set-dilth** | boncuk, kumaş, bazen para; ortaya konan merkez taşın altına konur | bahis **basılmadı**, sayım korundu; değişiklik prozada söylendi |
| **Marbles** | misketler ortaya konur, kazanan **alır** | **puana** çevrildi, herkes kendi misketini geri alır; özgün biçim kaynak notunda |
| **Tab** | kaybeden kahveyi öder; dört kişilik biçimde dayak | ikisi de basılmadı; dört kişilik biçim puanlandı |

**Hiçbiri gizlenmedi.** Üçünde de değişikliğin yapıldığı ve **neden**
yapıldığı yazıyor.

---

## 16 · Yeniden kurgulama

Bu batch'te `reconstructed` bayrağı taşıyan **yeni oyun yazılmadı**; beş
`reconstructed` kayıt `reconstructionPlan`'larını koruyor ve kuyrukta
P3'te duruyor.

Üç maddede **kısmi** editoryal tamamlama vardır ve üçü de prozada
**adlandırılarak** beyan edildi:

| Oyun | Kaynağın bıraktığı boşluk | Editoryal karar |
|---|---|---|
| **Seega** | Lane *"These are the only rules"* der; hareket kuralı ve bitiş yok | tek adım / boş çukura hareket · tek taşa düşen kaybeder — ikisi de adım içinde işaretli |
| **Tab** | bitiş koşulu yok | rakibin bütün taşlarını almak |
| **Conkers** | tur sırası adım adım verilmemiş | tekerlemelerden türetildi, beyan edildi |
| **Totolospi** | Voth: bazı koşullar *"have not yet been fully studied"* | **uydurulmadı**; eksik olduğu yazıldı |

`qa_manuscript.py § ③` beyanı **iki yönlü** denetliyor: madde
`reconstructed` derken envanter demiyorsa da, tersi de kapıyı kırar.

---

## 17 · Manuscript koruması

| | |
|---|---:|
| Takip edilen manuscript dosyası | **0** |
| Takip edilen korumalı kural bloğu | **0** |
| Takip edilen Türkçe pilot metni | **0** |
| Sızıntı fikstürü | 5 · hepsi beklendiği gibi |

Faz 4'ün on bir yeni maddesi **baştan** korumalı katmana yazıldı.
`git ls-files 02_MANUSCRIPT/` yalnızca `.gitkeep` ve `README.md` döndürür.

---

## 18 · Yeni kapı: `qa_manuscript.py`

Diğer kapılar veri katmanına bakar; bu kapı **prozanın yazıldığı katmana**
bakar. Manuscript depoda olmadığı için CI'da **boş koşar** ve 0 döner;
körlüğü `selftest` kapatır.

| Denetim | Ne arar |
|---|---|
| ① beş öğe | kurulum · hamle · hedef · **bitiş** |
| ② üç soru | berabere · kilit · kural dışı |
| ③ beyan | `reconstructed` ↔ envanter, **iki yönlü** |
| ④ kaynak | künye var mı; sayfa numarası **doğrulanmış** mı |
| ⑤ dış test | kaydı olmayan `locked` var mı |
| ⑥ **ölçülen bloklar** | manuscript'teki her blok sayfa ölçümünde **sayılıyor mu** |
| ⑦ dil | ticari maddede `translatedFrom` dolu mu |

**⑥ bir SINIFI kapatır.** `calibrate_pages.py` ölçtüğü blokların listesini
elle taşıyor. Yeni bir blok yazılıp listeye eklenmezse madde **olduğundan
kısa** ölçülür ve sayfa modeli **sessizce** küçülür — sayfa modeli ise bu
kitabın fiyat modelidir. Faz 3 üç blok (`stages`, `legalMoves`,
`firstMove`), Faz 4 üç blok daha (`placement`, `figures`, `scoring`)
ekledi; ikisinde de hatırlamak **disipline** bağlıydı. Artık kapı listeyi
**kaynaktan okuyor**.

---

## 19 · Kasıtlı kusur testleri

`selftest.py` **148 denetim** koşuyor (Faz 3: 126). Sekizinci bölüm Faz 4
kapılarını sınar.

| Kusur sınıfı | Yakalanıyor mu |
|---|---|
| Engelli oyun erişilebilirin önüne geçiyor | ✅ |
| Denenmemiş oyun "engelli" gösteriliyor | ✅ |
| Kuyrukta yinelenen oyun | ✅ |
| Doğrulanmamış kaynakla yazılmış oyun | ✅ |
| Tek tek geçip TOPLAMDA bütçeyi aşan iki diyagram | ✅ |
| Efsane × işaretini açıklamıyor | ✅ |
| Bitiş koşulu olmayan madde | ✅ |
| Kurulumu olmayan madde | ✅ |
| Hedefi olmayan madde | ✅ |
| Hamle bloğu olmayan madde | ✅ |
| Üç sorudan biri cevapsız | ✅ |
| Kaynaksız madde | ✅ |
| Beyansız yeniden kurgulama (iki yön) | ✅ |
| Çeviri beyanı taşıyan ticari madde | ✅ |
| Doğrulama kaydı eksik madde | ✅ |
| Doğrulanmamış sayfa numarası | ✅ |
| **Ölçülmeyen kural bloğu** | ✅ |
| Dış test kaydı olmadan `locked` | ✅ |

Faz 1–3'ün bütün fikstürleri korundu ve yeşil koşuyor.

---

## 20 · Aile ve kültür dengesi

| Aile | Hedef | Yazılmış | Erişilebilir · yazılmamış |
|---|---:|---:|---:|
| Ekim | 14 | 1 | 12 |
| Av-kuşatma | 10 | 3 | 7 |
| Eve dönüş (race) | 15 | 4 | 10 |
| Çizgi-toprak | 14 | 4 | 9 |
| **Savaş tahtası** | 17 | 3 | **14** |
| **Şans** | 15 | 1 | **12** |
| **Tahtasız** | 15 | 6 | **8** |
| **Toplam** | **100** | **22** | **72** |

Kapsam **değişmedi**: 100 oyun · 71 kültür · 19 yedek. Kilit
`validate_scope.py` tarafından her koşuda doğrulanıyor.

Manuscript'teki kültür sayısı **14**. Yedi ailenin **yedisi** de temsil
edildi.

### 20.1 Tahtasız ailede açık bir editoryal soru KALDI

Faz 3, tahtasız ailenin 15 oyunundan 5'inin İngiliz olduğunu ve ailenin
11 kültürle en dar küme olduğunu işaretlemişti. Faz 4 o beşin **dördünü**
yazdı (cats-cradle hariç) ve sorun **çözülmedi**, yalnızca görünür oldu.

Ayrıca Faz 1'in `fivestones` kaydında duran uyarı hâlâ geçerlidir:
*"Gonggi ile aynı mekanik; ikisinden biri elenmelidir."* Faz 4 ikisini de
yazdı ve ayrımı **biçimde** yaptı — gonggi beş taşla ve halkasız,
fivestones Wakefield'ın **halka + top** biçimiyle. Bu bir çözüm değil bir
**azaltmadır**.

> **KURUCU KARARI GEREKİR.** Yedek havuzda 19 uygun oyun var. Tahtasız
> ailedeki İngiliz maddelerden ikisinin yerine temsil edilmeyen
> kültürlerden iki oyun koymak kültür sayısını 11'den 13'e çıkarır ve
> gonggi/fivestones çakışmasını da çözer. Bu bir **scope amendment**
> gerektirir ve ajan tarafından yapılamaz. **Kapsam değiştirilmedi.**

---

## 21 · CI ve Git

| | |
|---|---|
| Dal | `faz/4-blok-2` |
| CI | ✅ **YEŞİL** (her push'ta beklendi) |
| Açık gereksiz PR | yok |
| `.gate` | **`phase1`** — yükseltilmedi |

Faz 3 `main`'e merge edilmiş durumda. Faz 4 çalışması tek bir dalda
toplandı ve her anlamlı batch'ten sonra CI beklendi.

CI'a bir kapı eklendi (`build_queue.py --check`, `data` işinde) ve
`qa_manuscript.py` mevcut **tarama** sayesinde elle eklemeye gerek
kalmadan koşuyor — Faz 1'in "elle tutulan liste unutulur" dersi burada
kendini ödedi.

---

## 22 · Faz 4 Definition of Done

| | Ölçüt | Durum |
|---|---|---|
| ⚠ | Bütün Faz 4 üretim oyunları yazıldı | **11/47** — kapsam tamamlanmadı |
| ✅ | Yazılan oyunlar onaylı 100 kapsamından | 22/22 |
| ✅ | Erişilebilir oyunlar engellilerden ÖNCE | kapıya bağlandı (K22) |
| ✅ | Engelli oyunlar sona bırakıldı | 5 engelli · P4 |
| ✅ | Kaynak durumu dürüst | 5 engelli · 70 denenmemiş · ayrı sayılıyor |
| ✅ | Uydurulmuş kanıt yok | locator · pasaj · künye üçü de denetleniyor |
| ✅ | Ticari içerik İngilizce | 22/22 |
| ✅ | Türkçe test katmanı yalıtılmış | 0 sızıntı |
| ✅ | Kurallar tam | 22/22 · kapı denetliyor |
| ✅ | İç oynanabilirlik denetimleri | 22/22 |
| ⛔ | **Dış test durumu dürüstçe kaydedildi** | **0 test · PENDING** |
| ✅ | Yeniden kurgulama beyan edildi | iki yönlü kapı |
| ✅ | Aile dengesi izlendi | 7/7 aile temsil edildi |
| ✅ | Kültür dengesi izlendi | 14 kültür · **açık soru § 20.1** |
| ✅ | Diyagramlar v1.4'e uygun | 27/27 |
| ✅ | Her diyagram ≤150 mm | 27/27 · azami 111,5 |
| ✅ | **Her OYUN ≤150 mm** | 22/22 · azami 144,0 |
| ✅ | Diyagramlar render edilip ÖLÇÜLDÜ | 27/27 · görsel denetim dahil |
| ✅ | Sayfa modeli yeniden hesaplandı | 268 → **258** |
| ✅ | Güvenlik/malzeme kuralları | 4 madde |
| ✅ | Manuscript sızıntısı = 0 | tamam |
| ✅ | Türkçe sızıntısı = 0 | tamam |
| ✅ | Kasıtlı kusur testleri | **148 denetim** |
| ✅ | Selftest yeşil | tamam |
| ✅ | CI yeşil | tamam |
| ✅ | Gereksiz açık PR yok | tamam |
| ✅ | Faz 4 raporu | bu belge |
| ⛔ | Arka madde (üç indeks · sözlük · şablonlar) | **yazılmadı** |

### ÜRETİM İLERLEDİ ≠ FAZ 4 TAMAM

| | |
|---|---|
| **BU BATCH'İN ÜRETİMİ** | ✅ **TAMAM** |
| **FAZ 4 KAPSAMI** | ⛔ **TAMAM DEĞİL — 11/47** |
| **FORMAL PHASE GATE** | ⛔ **AÇILMADI** |

Roadmap'in Faz 4 kapısı **100 oyun** ve **100 oynanabilirlik testi**
ister. Yazılan 22, geçen test 0.

---

## 23 · Kalan bloklayıcılar

| # | Blok | Kimde | Değişti mi |
|---|---|---|---|
| 1 | **Dış insan oynanabilirlik testi** | kurucu — paket hazır | ⛔ Faz 2'den beri aynı |
| 2 | **Telifli kaynak erişimi** | kurucu | 5 oyun engelli (Faz 3: 4) |
| 3 | Tahtasız aile kültür dengesi + gonggi/fivestones çakışması | kurucu | öneri güncellendi (§ 20.1) |
| 4 | ~~Totolospi kural kimliği~~ | — | ✅ **ÇÖZÜLDÜ** |
| **A4** | Büyük punto sürümü | kurucu | Faz 4'te karar bekleniyordu, **açık** |
| **A5** | `STYLE.md` onayı | kurucu | v2.1 yazıldı, onay bekliyor |

**Üretim hızını belirleyen tek şey kaynak erişimidir** — ve Faz 4 bunu
ölçtü: 72 erişilebilir oyun kuyrukta bekliyor, engelli olan yalnızca 5.

---

## 24 · Faz 5 hazırlığı

Faz 5'e **geçilmedi ve geçilmeyecek.**

| Hazır | Değil |
|---|---|
| Erişilebilir-önce kuyruk (72 oyun sırada) | **78 oyun yazılmadı** |
| Diyagram dili v1.4 + oyun başına 150 mm bütçe | **Arka madde yazılmadı** |
| Kalibre sayfa modeli (258, +%0,8) | **Dış test kanıtı (0)** |
| Manuscript kapısı + 148 kusur testi | Telifli kaynak erişimi |
| Yazım şablonu 22 oyunda sınandı | `locked` oyun (0) |

---

## 25 · Bu fazın kendi hakkında bilmediği

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| Yirmi iki madde masada çalışıyor mu | **dış test** — açık |
| Taşma oranı %4,5'te kalıyor mu | daha büyük örneklem |
| 70 "denenmemiş" oyunun kaçı erişilebilir | sıraya geldikçe |
| Metin farkının diyagram farkını geçmesi kalıcı mı | Faz 5 · 40+ madde |
| Graph ve `bed` notasyonu POD baskıda okunuyor mu | Faz 5 · prova kopya |
| Seega'nın hareket kuralı doğru mu | ikinci bir birinci elden kayıt |

İlk satır Faz 2'den beri aynı yerde duruyor ve durmaya devam ediyor.
**Yirmi iki madde yazıldı, sıfırı test edildi.**

---

**⛔ FAZ 5 BAŞLAMADI.** `.gate` = `phase1`. Ajan durdu.
