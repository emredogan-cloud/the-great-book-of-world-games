# DİYAGRAM DİLİ — The Great Book of World Games

> **Sürüm 1.2 · Faz 3 · DONDURULMUŞTUR.**
>
> v1.0 → v1.1: gerçek dizgi ölçümü dilin KENDİ kuralında bir kusur
> buldu (§ 5.1) ve bir ÖLÇÜLMÜŞ bütçe ekledi (§ 7.1).
> v1.1 → v1.2: bütçe **150 mm** olarak bağlayıcılaştı (K19) ve dikey
> panellerde efsane **bir kez** basılır oldu (§ 5.2). Cat's Cradle
> 182,5 mm → **111,5 mm**.
>
> Makine okunur karşılığı: `07_ASSETS/diagrams/diagram_language.json`
> Denetleyen kapı: `04_BUILD/qa_diagram.py`
>
> Değişiklik kurucu kararı **ve** bir sürüm yükseltmesi gerektirir.

---

## 0 · Bu belge neden Faz 2'de yazıldı ve neden burada donuyor

Kitapta bir diyagram süs değildir: **kuralın parçasıdır.** Okur kuralı
okuyup tahtaya bakar ve ikisi uyuşmuyorsa oyun çalışmaz.

Notasyonu geç dondurmanın maliyeti tek cümlede ölçülür:

> **60. oyunda notasyonu değiştirmek, önceki 59 diyagramı geçersiz kılar.**

Bu yüzden dil, üretimden **önce** ve kitabın **en zor** oyunlarıyla
sınanarak donar. Faz 2 pilotu tam bunun için seçildi: bir kâğıt satranç
tahtası çizmek kolaydır; **ip figürü**, **yirmi kişilik çember** ve
**dört sıralı bao tahtası** aynı dille anlatılamıyorsa dil eksiktir.

### Dilin geçmesi gereken beş sınav

| Sınav | Pilot oyun | Ne kırabilirdi |
|---|---|---|
| Karmaşık tahta | `bao-la-kiswahili` | 32 çukur + iki aşama + tohum sayısı |
| Asimetri | `tablut` | iki taraf, iki hedef, muaf taş |
| Ölçek kararı | `go` | 19×19 vs 9×9 — uyarlamanın görünürlüğü |
| **Tahtasızlık** | `cats-cradle` | tahta yok, koordinat yok, eller var |
| **Grup ölçeği** | `mbube-mbube` | 6–20 kişi, konum değil ROL |

Dördüncü ve beşinci sınav, tahta merkezli bir notasyonu **yıkar**. Bu
belgenin dört yerine **beş tahta sınıfı** tanımlamasının sebebi budur.

---

## 1 · Değişmezler — her diyagramda geçerli

| # | Kural | Gerekçe |
|---|---|---|
| D1 | **Renk yoktur.** Ayrım yalnızca doluluk, kontur ve doku ile yapılır | K3: iç blok siyah-beyaz; renk KDP'de bir vergidir |
| D2 | Gri yalnızca **dört seviyede** kullanılır: %0 · %25 · %55 · %100 | POD baskı ara tonları güvenilir basmaz |
| D3 | En ince çizgi **0,75 pt** | Daha incesi POD'da kopar |
| D4 | En küçük harf/rakam **7 pt** | Daha küçüğü 8,5×11'de okunmaz |
| D5 | Hiçbir bilgi **yalnızca** konuma ya da boyuta bağlı olamaz | Fotokopiyle ölçek değişir; arka madde tahta şablonu fotokopiye göre tasarlandı |
| D6 | Her diyagram **kendi başına** okunabilir olmalı | Okur kuralı unutup diyagrama döner |
| D7 | Her diyagramın **efsanesi** (legend) diyagramın içindedir | Ayrı bir sembol sayfasına bakmak masada olmaz |

> **D1 bir estetik tercih değil, bir erişilebilirlik kuralıdır.** Renk körü
> bir okur ve siyah-beyaz bir fotokopi aynı sorunu yaşar; ikisini birden
> çözen tek yol renge hiç güvenmemektir.

---

## 2 · Beş tahta sınıfı — ve her birinin koordinat kuralı

Tek bir koordinat sistemi bu kitabın oyunlarını taşımaz. Beş sınıf
vardır; her oyun kaydı `diagram.boardClass` alanında **tam birini**
taşır ve sınıf, koordinat kuralını **belirler**.

### 2.1 `cell` — taş KARENİN İÇİNDE durur

Örnek: Tablut · Shogi · Seega · Fox and Geese

```
   a  b  c  d  e            · Sütunlar SOLDAN SAĞA: a, b, c…
 5 ·  ·  ·  ·  ·            · Satırlar AŞAĞIDAN YUKARI: 1, 2, 3…
 4 ·  ·  ○  ·  ·            · Referans: sütun + satır, küçük harf → c4
 3 ·  ●  ◎  ●  ·            · Kaynak kendi harflendirmesini kullanıyorsa
 2 ·  ·  ○  ·  ·              (Linnaeus'un a–m'si gibi) kitap KENDİ
 1 ·  ·  ·  ·  ·              sistemini basar ve kaynağınkini dipnotta anar
```

### 2.2 `point` — taş KESİŞİMİN ÜSTÜNDE durur

Örnek: Go · Fanorona · Nine Men's Morris · Bagh-Chal

Koordinat kuralı `cell` ile **aynıdır**; ayrım yalnızca çizimdedir:
taş çizginin kesiştiği yere oturur, karenin ortasına değil.

> **Bu ayrım kural düzeyindedir, çizim düzeyinde değil.** Go'da kenar
> çizgisi oynanabilir bir yerdir; Tablut'ta kenar karesi oynanabilir bir
> yerdir ama ikisi farklı sayıda yer üretir. Diyagram bunu **göstermek**
> zorundadır, yoksa okur tahtayı yanlış çizer.

### 2.3 `pit` — tohum ÇUKURA ekilir

Örnek: Oware · Bao · Olinda Keliya · Toguz Kumalak

```
        A6  A5  A4  A3  A2  A1      · Sıralar oyuncuya göre A ve B
       ┌───┬───┬───┬───┬───┬───┐    · A = ÜST oyuncu (diyagramın uzağı)
  [A]  │ 4 │ 4 │ 4 │ 4 │ 4 │ 4 │    · B = ALT oyuncu (okura yakın)
       ├───┼───┼───┼───┼───┼───┤    · Çukurlar her sıranın KENDİ
       │ 4 │ 4 │ 4 │ 4 │ 4 │ 4 │      ekim yönünde 1'den başlar
       └───┴───┴───┴───┴───┴───┘    · Ambar: [A] ve [B]
        B1  B2  B3  B4  B5  B6      · RAKAM = tohum sayısı, zorunlu
                            [B]
```

**Zorunlu kural:** çukurun içindeki **rakam** tohum sayısıdır ve
**hiçbir zaman** noktacıklarla gösterilmez. Gerekçe: dört noktacık ile
beş noktacık POD baskıda ayırt edilmez; `4` ile `5` her zaman ayırt edilir.

Dört sıralı tahtalar (Bao, Omweso) `A1–A8` · `A′1–A′8` · `B′1–B′8` ·
`B1–B8` kullanır; üssü işareti **iç sıra** demektir.

### 2.4 `track` — taş İZ ÜZERİNDE ilerler

Örnek: Royal Game of Ur · Yut Nori · Patolli · Game of the Goose

İzin **her durağı numaralanır**: `1`'den `n`'e, **hareket yönünde**.
Giriş `0`, çıkış `n+1` ve bu ikisi her zaman etiketlidir.

Dallanan izlerde (Ur, Yut, Patolli) her dal bir **harf** alır:
`1–8` ortak, `9a–12a` ve `9b–12b` dallar. Kısayol bağlantısı **noktalı
çizgi** ile gösterilir.

> Yut Nori'nin diyagramı bu kuralın en sert sınavıdır: yirmi çember ve
> dokuz haç işareti, üç farklı çıkış yolu üretir. Kaynak (Culin 1895,
> s. 69) yolları `A`–`E` harfleriyle anlatır; kitap **durak numarası**
> basar ve harfleri **köşe kutusunda** verir, çünkü okur "otuz iki
> adım" saymaz, "beşinci durak" arar.

### 2.5 `bodily` — TAHTA YOKTUR

Örnek: Cat's Cradle · Mbube-Mbube · Hopscotch · Jan-Ken

Koordinat yoktur; **referans çerçevesi** vardır. İki alt biçim:

**(a) `hands` — el ve ip figürleri**

Jayne'in 1906'da çözdüğü sorun aynen alınır ve kaynak künyesiyle
anılır: yön adları **figürün ALINDIĞI kişinin bakışına** göredir.

| Terim | Anlamı |
|---|---|
| `near` | oyuncuya yakın ip |
| `far` | oyuncudan uzak ip |
| `left` / `right` | oyuncunun soluna / sağına |
| `L1…L5` · `R1…R5` | parmaklar; 1 = başparmak |

İp figürü diyagramı **her zaman** üç panel taşır: `başlangıç` →
`hareket` → `sonuç`. Tek panel yasaktır — çünkü ip figüründe *ara adım*
kuralın kendisidir.

**(b) `formation` — beden ve grup oyunları**

Konum değil **ROL** gösterilir.

| Sembol | Rol |
|---|---|
| ○ | oyuncu (nötr) |
| ● | avcı / ebe / aktif rol |
| ◍ | gözü bağlı oyuncu |
| ⌒ | çember (kişi sayısı değişken) |
| ↔ | yer değiştirme |

> **Grup diyagramında oyuncu sayısı ÇİZİLMEZ, YAZILIR.** Mbube-Mbube
> 6–20 kişiyle oynanır; on üç daire çizmek okura "on üç kişi gerekir"
> der ve bu **yanlıştır**. Çember bir yay olarak çizilir, sayı künye
> şeridinde durur.

---

## 3 · Taş notasyonu

Ayrım **doluluk ve kontur** iledir; renk ve boyut **bilgi taşımaz** (D1, D5).

| Sembol | Anlam | Gri |
|---|---|---|
| ○ | açık taraf, sıradan taş | %0 dolgu, %100 kontur |
| ● | koyu taraf, sıradan taş | %100 dolgu |
| ◎ | **ayrıcalıklı taş** — kral, kaplan, terfi etmiş | %0 dolgu, çift kontur |
| ◉ | ayrıcalıklı taş, koyu taraf | %100 dolgu, beyaz iç halka |
| □ ■ | **ikinci taş tipi** (aynı tarafta iki tür varsa) | ○ ● ile aynı mantık |
| ◍ | gözü bağlı / kör oyuncu (`formation`) | %25 dolgu |
| ▤ | terfi etmiş / ters çevrilmiş taş (Shogi) | %25 dolgu + yatay tarama |
| `4` | çukurdaki tohum sayısı (`pit`) | rakam, dolgu yok |

**Shogi istisnası ve neden bir istisnaya izin verildi.** Sekiz taş tipi
sembolle ayrılamaz. Shogi'de taşlar **iki harfli Latin kısaltma** taşır
(`K` `R` `B` `G` `S` `N` `L` `P`) ve taşın **yönü** sahipliği belirtir —
tam olarak özgün oyundaki gibi. Bu bir uyarlamadır ve prozada söylenir:
kaynak (Falkener 1892, s. 155) taşların Çince/Japonca karakter taşıdığını
ve okunmalarının zor olduğunu **zaten** yazar.

---

## 4 · Hareket, alma ve yasak hamle

| Gösterim | Anlam |
|---|---|
| **→** düz ok, kesintisiz | Gösterilen hamle |
| **⇢** noktalı ok | Alternatif ya da olası hamle |
| **⤳** kıvrık ok | Ekim yönü (`pit`) ya da iz yönü (`track`) |
| **⊣** ucu çubuklu ok | **Yasak** hamle — neden diyagram efsanesinde yazılır |
| **×** taşın üstünde | Bu hamlede **alınan** taş |
| **⊘** taşın üstünde | Tahtadan **çıkmış** taş (%55 gri) |
| **[ ]** köşeli ayraç | Elde / ambarda tutulan taş |
| **↺ ×3** | **Tekrar eden konum** — üçüncü kez |
| **⟦ ⟧** | Puan şeridi |

### 4.1 Alma yönü — Fanorona kuralı

İki yönlü alma (yaklaşma / çekilme) tek okla anlatılamaz. Kural:

- **Yaklaşma:** ok taşın gittiği yöne bakar, `×`'ler okun **önündedir**
- **Çekilme:** ok taşın gittiği yöne bakar, `×`'ler okun **arkasındadır**

Bu, kaynağın (Montgomery 1887, s. 152) kendi ayrımını korur ve okurun
"hangi taşlar gitti" sorusunu tek bakışta cevaplar.

### 4.2 Zorunlu alma

Zorunlu bir alma varsa ok **kalın** (1,5 pt) çizilir ve efsanede
`zorunlu` yazar. İsteğe bağlı alma normal kalınlıktadır.

---

## 5 · Başlangıç ve bitiş konumu

| Diyagram tipi | Etiket | Ne zaman zorunlu |
|---|---|---|
| Başlangıç dizilimi | `KURULUM` | Kurulumu sözle anlatılamayan her oyun |
| Bir hamlenin öncesi/sonrası | `1` → `2` | Alma/atlama kuralı sözle belirsiz kalan her oyun |
| Bitiş konumu | `BİTİŞ` | Kazanma koşulu bir DİZİLİŞ ise (territory ailesi) |

**İki panelden fazlası yasaktır** — `bodily/hands` alt biçimi hariç,
orada **tam üç** panel zorunludur (§ 2.5a).

### 5.1 · v1.1 düzeltmesi — dilin kendi kuralı kendi sınırını aşıyordu

Faz 2'nin gerçek render ölçümü şunu buldu:

> Cat's Cradle'ın üç paneli **yan yana** dizilince **214 mm** ediyor.
> Tam genişlik sınırı **180 mm**.

Kusur bir tanımlayıcıda değil, **dilin kendisindeydi**: § 2.5a üç panel
şart koşuyor, § 7 ise 180 mm sınır koyuyordu ve ikisi aynı anda
sağlanamıyordu. Bunu bir insan gözü değil, **render ölçümü** buldu.

**Düzeltme:** `bodily/hands` panelleri **dikey** dizilir.

| | v1.0 | v1.1 |
|---|---:|---:|
| Genişlik | 214 mm ✗ | **70 mm** ✓ |
| Yükseklik | 59,5 mm | 182,5 mm |

Notasyon değişmedi, **dizilim** değişti.

### 5.2 · v1.2 düzeltmesi — efsane üç kez basılıyordu

v1.1'in dikey dizilimi 182,5 mm üretti ve Faz 3'ün **150 mm** bütçesini
aştı (K19). İki kusur bulundu ve ikisi de israftı:

1. **Her panel kendi efsanesini taşıyordu.** Aynı efsane üç kez basılıyor,
   27 mm yiyor ve okura aynı şeyi üç kez okutuyordu. D7 efsaneyi
   *diyagramın* içinde ister, *her panelin* içinde değil.
2. **Gövde yarı yarıya boştu.** İp figürü ±10 mm'lik bir alanda yaşıyor;
   gövde 46 mm ayrılmıştı.

| | v1.0 | v1.1 | **v1.2** |
|---|---:|---:|---:|
| Genişlik | 214 mm ✗ | 70 mm ✓ | **70 mm** ✓ |
| Yükseklik | 59,5 mm | 182,5 mm ✗ | **111,5 mm** ✓ |

**Çizgi kalınlığı (0,75 pt) ve glif boyu (7 pt) değişmedi.** Giden şey
boş kenar payı ve tekrarlanan efsanedir — yani bu bir **sadeleştirmedir**,
"okunmaz hâle gelene kadar küçültme" değildir. Aradaki fark § 10'un
yasakladığı şeydir.

Gerekçe: üç panelli bir hamle diyagramı iki sayfalık maddenin
diyagram bütçesini aşar ve okur zaten kuralı okumuştur. İstisna ip
figürlerindedir çünkü orada ara adım **kuralın kendisidir**, örneği değil.

Panel numarası her zaman **sol üst köşede**, kutu içinde durur.

---

## 6 · Efsane (legend)

Her diyagramın kendi efsanesi vardır ve **yalnızca o diyagramda geçen**
sembolleri listeler (D7).

```
┌─────────────────────────────┐
│ ○ savunan   ◎ kral          │
│ ● kuşatan   × bu hamlede alındı │
└─────────────────────────────┘
```

**Kullanılmayan bir sembol efsanede duramaz.** Gerekçe Codex dersi D28'in
aynısıdır: ölü bir kural sessizce yanlış güven verir. `qa_diagram.py`
efsane ile diyagram içeriğini karşılaştırır ve fazladan sembolü reddeder.

---

## 7 · Baskıya uygunluk

| Ölçüt | Değer | Neden |
|---|---:|---|
| Mürekkep | siyah | K3 |
| En ince çizgi | 0,75 pt | POD'da kopma sınırı |
| En küçük glif | 7 pt | 8,5×11'de okunma sınırı |
| Gri seviyeleri | %0 · %25 · %55 · %100 | ara tonlar güvenilir basmaz |
| Taş çapı ÷ hücre | 0,62–0,72 | daha büyüğü çizgiyi yer, daha küçüğü kaybolur |
| Diyagram genişliği | ≤ 88 mm (tek sütun) · ≤ 180 mm (tam) | dizgi ızgarası |
| Fotokopi testi | %100 ve %71 (A4→A5) | arka madde tahta şablonları fotokopiye gider |

### 7.1 · Diyagram bütçesi — ÖLÇÜLMÜŞ, seçilmemiş

| | |
|---|---:|
| Çift sayfanın toplam metin alanı | 2 × 242 mm = **484 mm** |
| Metnin ölçülen payı | **~332 mm** (1,37 sayfa) |
| **Diyagrama kalan** | **~152 mm** |
| **Bütçe** | **150 mm** — kurucu Karar A ile BAĞLAYICI (K19) |

Bu sayı bir tasarım tercihi değil bir **artıktır**. Faz 2 dizgisi üç oyunu
gerçek fontla dizdi ve şunu ölçtü:

> **Metin oyundan oyuna neredeyse sabittir** (1,37 sayfa · fark 0,01).
> **Değişken olan diyagramdır** (0,24 – 0,78 sayfa).

Yani sayfa bütçesi bir **kelime** bütçesi değil, bir **diyagram**
bütçesidir. Bir maddeyi çift sayfadan taşıran şey uzun proza değil, çok
ya da büyük diyagramdır.

**Bütçeyi aşan madde dört sayfa alır** ve sayfa modelinden düşülür
(en fazla altı madde — `EDITORIAL_ARCHITECTURE.md § 2`).

### 7.2 · Bütçe RENDER EDİLMİŞ ÇIKTIDAN ölçülür

`qa_diagram.py § ⑨` tanımlayıcıya değil **çizilmiş dosyaya** bakar.

Gerekçe: bir tanımlayıcı *"9×9 tahta"* der ve bu bir **boyut vermez**.
Boyutu adım aralığı, efsane satır sayısı, panel dizilimi ve altyazı
belirler — yani ancak çizildikten sonra bilinir.

> **Render edilmemiş bir diyagram denetlenmemiştir ve geçemez.**

Aksi hâlde bütçe, çizilmeyen her diyagram için sessizce boş koşardı —
ve bir kapının en tehlikeli hâli boş koşarken yeşil yanmasıdır.

**Fotokopi testi neden bir kapı:** kitabın arka maddesi tahta
şablonlarını **fotokopiye uygun** basmayı vaat ediyor. %71 küçültmede
okunmayan bir diyagram o vaadi yalanlar. Ölçüm Faz 5'te prova kopyayla
tekrarlanır; Faz 2 yalnızca **notasyonu** muhafazakâr seçer.

---

## 8 · Yeniden kurgulanan oyunların diyagramı

Bir diyagram, tarihsel bir kaydı **olduğundan kesin** gösterebilir. Bu,
prozadaki "yeniden kurgulanmıştır" etiketini sessizce yalanlar.

**Kural:** `playabilityStatus: reconstructed` olan her oyunun diyagramı
`diagram.reconstructed: true` taşır ve diyagramın altında şu satır basılır:

> *Bu diyagram [kaynak]'a dayanarak yeniden kurgulanmıştır; [boşluk]
> kaynakta yer almaz.*

Ayrıca **kaynakta olmayan** her öğe — kaçış karesi, berabere işareti,
tahmin edilen bir taş — **noktalı konturla** çizilir.

> Tablut bunun örneğidir. Linnaeus'un 1811 çevirisi (c. II, ss. 55–58)
> kralın kaçış hedefini **kenar** olarak verir ve bu doğrulanmıştır; ama
> **berabere kuralı metinde yoktur.** Kitabın berabere işareti bu yüzden
> noktalı konturla çizilir: okur neyin kayıttan, neyin editörden geldiğini
> **diyagrama bakarak** ayırabilmelidir.

---

## 9 · Uyarlanmış tahtalar

Kitap özgün olandan farklı bir tahta basıyorsa diyagram bunu **söyler**:

`diagram.adaptedFrom` alanı doldurulur ve diyagram başlığı şu biçimi alır:

> **Go — 9×9 (uyarlama)** · *özgün tahta 19×19'dur*

Go'nun 9×9 basılması bir kolaylık değil bir **karardır** ve kaynak
(Falkener 1892, s. 239 · Culin 1895, s. 91) 19×19 der. Kararı görünür
kılmak, kitabın kaynak iddiasını korur.

---

## 10 · Makine okunur karşılık ve kapı

Her diyagram bir **tanımlayıcı** (descriptor) ile tarif edilir:

```json
{
  "diagramId": "tablut-setup",
  "gameId": "tablut",
  "type": "setup-illustration",
  "boardClass": "cell",
  "size": {"cols": 9, "rows": 9},
  "reconstructed": true,
  "pieces": [{"at": "e5", "glyph": "king"}, ...],
  "legend": [{"glyph": "king", "label": "kral"}, ...]
}
```

`04_BUILD/qa_diagram.py` şunları denetler:

1. `boardClass` beş sınıftan biri mi
2. Kullanılan her glif **sözlükte** var mı
3. Her koordinat, o sınıfın koordinat kuralına uyuyor mu
4. Koordinat tahtanın **içinde** mi
5. Efsane, kullanılan gliflerin **tam kümesi** mi (eksik yok, **fazla yok**)
6. `reconstructed` diyagram, kaydın `playabilityStatus`'üyle **tutarlı** mı
7. Panel sayısı kurala uyuyor mu (≤2; `hands` için tam 3)
8. Renk kullanılmamış, gri yalnızca izinli dört seviyede mi

**6. denetim en önemlisidir:** bir oyun kayıtta `reconstructed` ama
diyagramı öyle demiyorsa, diyagram prozanın dürüstlüğünü **sessizce**
bozar. Kapı bunu imkânsız kılar.

---

## 11 · Bu dilin bilmediği şeyler

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| POD baskıda 0,75 pt gerçekten kopuyor mu | Faz 5 · prova kopya |
| %25 gri ile %0 gri fotokopide ayrışıyor mu | Faz 5 · prova kopya |
| İp figürü üç panelde gerçekten anlatılabiliyor mu | **dış insan testi** — açık |
| Shogi'nin Latin kısaltmaları okuru yavaşlatıyor mu | **dış insan testi** — açık |

Son iki satır bu belgenin en dürüst kısmıdır: notasyon **donduruldu**
ama **kanıtlanmadı**. Kanıt masadan gelir ve henüz gelmemiştir.
