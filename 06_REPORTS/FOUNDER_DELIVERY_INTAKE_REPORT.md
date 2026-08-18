# FOUNDER DELIVERY INTAKE REPORT

> **The Great Book of World Games** · Faz 5 · kurucu teslim alımı
> Tarih: 19 Ağustos 2026 · dal: `main`

Kurucu direktifi § 3: teslim edilen HER dosya, adına bakılmadan
açılacak ve içeriğine göre sınıflandırılacak.

**Bu kuralın karşılığı hemen çıktı: altı dosyanın ikisi adının söylediği
şey DEĞİL.** Biri boş bir hata sayfası, öteki bir yapay zekâ sohbet
çıktısı. İkisi de dosya adına bakılarak kabul edilseydi kitaba
girecekti.

---

## 1 · ALINAN DOSYALAR — altı kalem, 33 MB

> Not: teslim edilen bir dosya adında geçen 13 haneli ISBN dizisi bu
> raporda `«isbn»` ile değiştirilmiştir. Depo `kdp-free` stratejisindedir
> ve ISBN benzeri diziler `validate_structure` tarafından reddedilir;
> kapıyı gevşetmek yerine dizi kısaltıldı.

| # | dosya | boyut | sha256 (ilk 20) | GERÇEKTE NE |
|---|---|---:|---|---|
| 1 | `619290767-A-History-of-Board-games-Other-Than-Chess.pdf` | 16.0 MB | `7baedcee3ad01ceff4f1…` | ✅ **Murray 1952** — gerçek, 296 s., metin katmanı var |
| 2 | `1036688786-Parlett-The-Oxford-History-of-Board-Games-Uno.pdf` | 7.8 MB | `0cd6885f7ced8a1b49a1…` | ⚠ **Parlett 1999** — gerçek ama **KISMİ** tarama (157 s.) |
| 3 | `B-001-002-771.pdf` | 7.6 MB | `ea0022b26cfb3ef5e77b…` | ✅ **Bell**, *Board and Table Games*, 2. baskı — 269 s. |
| 4 | `africa-counts-…-«isbn».pdf` | **1.5 KB** | `62fdfb50761ace06e0f1…` | ⛔ **PDF DEĞİL** — PHP hata sayfası |
| 5 | `Laurence Russ - The Complete Mancala Games Book (2000).txt` | 27 KB | `8c1b5145a036673108e3…` | ⛔ **KİTAP DEĞİL** — yapay zekâ sohbet çıktısı |
| 6 | `ERICThesaurus2025.zip` | 1.0 MB | `6e5460976a29d07415aa…` | ◻ **İLGİSİZ** — ERIC eğitim tezaurusu (XML) |

---

## 2 · ⛔ DOSYA 4 — *Africa Counts* İNDİRİLEMEMİŞ

Dosya `.pdf` uzantısı taşıyor ama **ASCII metin**. İçeriği bir sunucu
hata sayfasıdır:

```
A PHP Error was encountered
Message: filesize(): stat failed for /home/obar.info/public_html/downloads/
         …/africa-counts-number-and-pattern-in-african-cultures-….pdf
Message: readfile(…): failed to open stream: No such file or directory
```

**Sonuç:** Zaslavsky 1973 **teslim edilmemiştir**. İndirme sunucuda
başarısız olmuş ve tarayıcı hata sayfasını `.pdf` adıyla kaydetmiştir.

**Etkisi — altı oyun açılmadan kaldı:** `ampe` · `pilolo` · `shisima` ·
`morabaraba` · `mefuvha` · `ayoayo`. Bunların hepsinde Zaslavsky ya tek
künyedir ya da ikinci bağımsız kaynaktır.

> Bu bir kurucu hatası değil bir **indirme hatası**dır ve tek satırlık
> bir kontrolle görülür: 1.5 KB'lık bir dosya 300 sayfalık bir kitap
> olamaz.

---

## 3 · ⛔ DOSYA 5 — *Russ, Complete Mancala Games Book* DEĞİL

Dosya adı Laurence Russ'ın 2000 tarihli kitabını söylüyor. İçerik **bir
yapay zekâ asistanının Türkçe cevabı**:

```
The information for the question you asked has been looked up and is now
ready to be viewed. Here's a response to the question:
Adji-boto, Güney Amerika'da (Surinam ve Fransız Guyanası) yaşayan …
```

Ölçülen parmak izleri:

| kanıt | sayı |
|---|---:|
| *"The information for the question you asked…"* açılışı | **3** |
| `[1, 2, 3]` biçimli asistan alıntı işaretleri | **34** |
| Türkçe gövde metni | tamamı |
| Birebir kaynak pasajı | **0** |
| Sayfa numarası | **0** |
| Kitabın kendi metninden tek cümle | **0** |

**Bu kaynak KULLANILAMAZ ve kullanılmadı.** Gerekçe projenin kendi
standardıdır — `SOURCING_STANDARD.md` § 2, *Kaynak SAYILMAYAN*:

> LLM çıktısı — **hiçbir koşulda**

Dosya beş oyunun (adji-boto · congklak · omweso · toguz-kumalak ·
pallanguzhi) kurallarını **iddia ediyor** ve iddiaları makul görünüyor.
Tam olarak bu yüzden tehlikelidir: doğrulanamaz bir metin, doğru
görünen bir metinden ayırt edilemez. Kitabın tek denetlenebilir iddiası
"her kural bir sayfada durur"dur ve bu dosyada sayfa yoktur.

> ⚠ `pallanguzhi` ve `omweso` bu dosya olmadan da açıldı — Bell ve
> Murray'den, sayfa numaralarıyla. `congklak`, `adji-boto` ve
> `toguz-kumalak` açılmadı ve **açılmamış sayılıyor**.

---

## 4 · ◻ DOSYA 6 — ERIC tezaurusu, ilgisiz

`ERICThesaurus2025.xml` (9.3 MB) bir eğitim-araştırma terim
sözlüğüdür. `mancala`, `oware`, `board game` taraması **sıfır** sonuç
verdi. Muhtemelen yanlışlıkla kopyalanmış. Zarar yok.

---

## 5 · ✅ KULLANILABİLİR ÜÇ ESER

### 5.1 Murray 1952 — teslimin omurgası

```
Murray, H. J. R., A History of Board-Games Other Than Chess
(Oxford: Clarendon Press, 1952) · Internet Archive taraması · 296 s.
```

Metin katmanı sağlam. Kitap oyunları **bölüm numaralarıyla**
düzenler (`4.11.4` gibi) ve arkasında bir `INDEX OF GAMES` taşır;
alım bu indeksi ayrıştırdı (**665 künye**) ve bölüm → sayfa eşlemesi
kurdu.

**Sayfa denklemi doğrulandı:** `basılı sayfa = pdf sayfası − 19`
(pdf 116'nın üst satırında basılı `97` görünür).

⚠ **Murray bir KURAL KİTABI DEĞİL bir TARİH kitabıdır.** Bazı
maddeleri tam kural verir, bazıları yalnızca künye ve bir cümledir.
Fark ancak sayfa açılarak görülür — ve görüldü (§ 6).

### 5.2 Bell — kitabın amacına EN UYGUN eser

```
Bell, R. C., Board and Table Games from Many Civilizations, 2nd ed.
· Internet Archive taraması · 269 s.
```

Dosya adı (`B-001-002-771.pdf`) hiçbir şey söylemiyordu; PDF künyesi
söyledi. Bell **oynanabilir kurallar** yazar ve her oyuna diyagram
verir — yani bu kitabın ihtiyacına Murray'den daha yakındır.

**Sayfa denklemi:** `basılı = pdf − 36` (pdf 131 = basılı 95, üst
satırda `DARA 95` görünür).

### 5.3 Parlett 1999 — GERÇEK ama KISMİ

```
Parlett, David, The Oxford History of Board Games
(Oxford: OUP, 1999) · 157 sayfalık KISMİ tarama
```

Tam eser ~390 sayfadır. Teslim edilen tarama yalnızca şu bölümleri
taşıyor (sayfa üst başlıklarından ölçüldü):

```
Preface → Welcome Aboard → RACE GAMES → SPACE GAMES → DISPLACE GAMES
```

**Eksik olan:** şans/kart bölümleri ve avlanma (chase) bölümünün
tamamı. Bu yüzden `mahjong` ve şans ailesi Parlett'ten **açılmadı**.

---

## 6 · SAYFA AÇILDI — ve iki kez "HAYIR" dedi

Kurucu direktifi § 4 dosya adına ve önceki nota güvenmeyi yasaklıyor.
İki örnek bu yasağın neden var olduğunu gösteriyor:

### 6.1 `konane` — Murray onu AÇMIYOR, KAPATIYOR

Boşluk kaydı Murray'i konane için bir umut olarak listeliyordu.
Sayfa açıldı: **Murray 4.11.4, basılı s. 97** — ve bölümün başlığı

> **WAR-GAMES OF WHICH WE HAVE NO CERTAIN KNOWLEDGE**

Murray'in kendi cümlesi:

> "Ko-na-ne (Culin, e, 243, who quotes various mentions, **none of
> which gives any clear indication of how it is played**). There seems
> **no fixed size of board** … Nor is there any **fixed number of men**."

**Sonuç:** Murray konane'yi açmaz; kuralın kurtarılamaz olduğunu
**doğrular**. `konane` FINAL SOURCE BLOCKED.

### 6.2 `bagh-chal` — Murray'de var, ama YANLIŞ KÜLTÜRDE

Murray dört "kaplan ve keçi" maddesi taşır ve **dördü de Hindistan**:

| Murray | oyun | kültür |
|---|---|---|
| 5.6.9 | Bagh bandi | Lower Bengal |
| 5.6.10 | Bagh guti | United Provinces |
| 5.6.11 | Sher-bakar | Punjab |
| 5.6.12 | (adsız) | Manipur, Assam |

Kapsam kaydı `bagh-chal` için **NEPALLİ** der. Bengal maddesinden
Nepal oyunu yazmak, projenin beş kez ölçtüğü **kültür tuzağının**
aynısıdır (totolospi · sugoroku · tien-gow · jianzi · xiangqi).

**Sonuç:** `bagh-chal` açılmadı. Nepal kaynağı hâlâ gerekiyor.

---

## 7 · SONUÇ — teslimin gerçek getirisi

| | |
|---|---:|
| Teslim edilen dosya | 6 |
| **Kullanılabilir eser** | **3** |
| Kullanılamaz (bozuk indirme) | 1 |
| Kullanılamaz (yapay zekâ çıktısı) | 1 |
| İlgisiz | 1 |

Kurucu **beş kitap** istemişti; teslimin **üçü geldi** (Murray · Bell ·
kısmi Parlett), **ikisi gelmedi** (Zaslavsky · Russ).

Açılan oyunların dökümü ve her birinin sayfa künyesi:
[`FINAL_WRITING_COMPLETION_REPORT.md`](FINAL_WRITING_COMPLETION_REPORT.md)

---

## 8 · KURUCUYA İKİ SATIRLIK İSTEK

Bir sonraki teslimde yalnızca iki dosya eksik:

1. **Zaslavsky, *Africa Counts*** — indirme başarısız oldu, tekrar
   denenmeli (1.5 KB'lık dosya bir kitap değildir). **Altı oyun** açar.
2. **Russ, *The Complete Mancala Games Book*** — kitabın KENDİSİ
   (tarama/PDF), bir asistan özeti değil. **Üç oyun** açar.

> Bir yapay zekâ özeti bir kaynak değildir — ne kadar doğru görünürse
> görünsün. Kitabın tek denetlenebilir iddiası sayfadır.
