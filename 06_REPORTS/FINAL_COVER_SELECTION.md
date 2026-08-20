# NİHAİ KAPAK SEÇİMİ

> **The Great Book of World Games** · Faz 6 · 20 Ağustos 2026
>
> Kurucu iki metinsiz kapak sanatı teslim etti. Biri seçildi.
> **Seçim dosya adına göre değil, ÖLÇÜLEREK yapıldı.**

---

## 1 · Karar

```
SEÇİLEN : COVER-02 — "THE BOARD THAT IS A MAP"
YÖN     : TESLİM EDİLDİĞİ GİBİ (aynalanmadı)
```

| | |
|---|---|
| Ham dosya | `07_ASSETS/raw/cover/<TAB>COVER-02.png` |
| SHA-256 (ilk 16) | `6c5d379257851f88` |
| Ham boyut | 1569 × 1003 px · PNG/RGBA |
| İstem | `IMAGE_PROMPT_LIBRARY.html § COVER OPTION 02` |

Reddedilen: **COVER-01 — "THE WORLD GAME TABLE"** (`7b8e4056c0b826a6`,
1570 × 1002 px). Silinmedi; `07_ASSETS/raw/cover/` içinde **kayıt olarak
duruyor**.

---

## 2 · Yöntem

Her aday, **gerçek sarım geometrisinin** üstüne oturtuldu (160 sayfadan
hesaplanan sırt: 0,3603 in · sarım 17,6103 × 11,2500 in) ve tipografinin
gireceği her bölge tek tek ölçüldü:

- `mean` — parlaklık ortalaması (mürekkep rengini belirler)
- `sd` — standart sapma (**kalabalık**: tipografinin gerçek düşmanı)
- `grad` — ortalama kenar yoğunluğu (ince detay)
- 130 px'lik **gerçek küçük resim** (Amazon raf görünümü)

Her aday **iki yönde** ölçüldü: teslim edildiği gibi ve **aynalanmış**.
Aynalama meşru bir seçenektir çünkü boş alanın hangi panele düştüğünü
değiştirir.

---

## 3 · Ölçüm

### Ön kapak başlık bölgesi

| aday · yön | mean | sd | grad | yorum |
|---|---:|---:|---:|---|
| COVER-01 · teslim | 42,9 | 30,0 | 21,4 | başlık **mankala ve morris tahtasının üstüne** düşüyor |
| COVER-01 · ayna | 74,3 | 22,1 | 23,8 | sakin — ama § 4'e bakın |
| **COVER-02 · teslim** | **200,3** | **12,8** | **19,9** | ✅ **en sakin** ölçülen başlık alanı |
| COVER-02 · ayna | 198,0 | 34,8 | 35,9 | — |

### Sırt

| aday · yön | sd | yorum |
|---|---:|---|
| COVER-01 · her iki yön | 48,2 | sırt **kamış çubukların ve domino taşlarının üstünden** geçiyor |
| **COVER-02 · teslim** | **37,4** | üç bölümü **sd ≤ 9,3** ile tamamen temiz (§ 5) |

### Barkod boş alanı

| aday · yön | sd | yorum |
|---|---:|---|
| COVER-01 · teslim | 45,4 | barkod alanına **domino taşları** giriyor |
| **COVER-02 · teslim** | **7,9** | ✅ açık okyanus — bütün kapağın en temiz alanı |

### Küçük resim (ön panel, gerçek 130 px)

| aday · yön | sd | grad | gözle |
|---|---:|---:|---|
| COVER-01 · teslim | 34,9 | 31,0 | kahverengi bir nesne yığını; nesneler birbirine karışıyor |
| COVER-01 · ayna | **22,8** | **17,7** | ⛔ **neredeyse boş bir tahta**: hiçbir şey okunmuyor |
| **COVER-02 · teslim** | 22,1 | **33,7** | ✅ **anında dünya haritası olarak okunuyor** |
| COVER-02 · ayna | 21,7 | 31,0 | ⛔ harita **ters** — coğrafya yanlış |

---

## 4 · Neden COVER-01 değil

COVER-01 güzel bir fotoğraf ve isteme sadık: tepeden çekim, eskimiş masa,
malzeme çeşitliliği, metin yok. **Sorun kompozisyonun sarıma oturmaması.**

Boş alan **sol %38'de**, yani **arka kapakta**. Nesneler ön kapakta ve
sırtta. Sonuç: başlık mankala tahtasının, yazar adı ip yumağının, sırt
yazısı kamış çubukların üstüne düşüyor.

**Aynalamak da çözmüyor** — ve neden çözmediği ölçüldü: aynalandığında
başlık alanı sakinleşiyor (sd 30,0 → 22,1) ama ön kapak **boş bir tahtaya**
dönüşüyor ve 130 px'te kenar yoğunluğu 31,0'dan **17,7'ye** düşüyor. Rafta
hiçbir şey görünmeyen bir kapak, güzel bir kapak değildir.

**Bu bir kalite yargısı değil, bir yerleşim ölçümüdür.** COVER-01, tek
panelli bir ön kapak olarak kullanılsaydı güçlü olurdu; tam sarım olarak
negatif alanı yanlış tarafta.

---

## 5 · Neden COVER-02

1. **Küçük resimde okunuyor.** 130 px'te kıtalar tanınıyor. Kitabın rafta
   yaptığı tek iş budur.
2. **Sarım OLARAK kurgulanmış.** Ortada bir kırım gölgesi var, sırt açık
   okyanusa düşüyor, barkod köşesi boş.
3. **Başlık ve yazar alanları gerçekten sakin** (sd 12,8 ve 13,7). Bu, § 7'nin
   *"beyaz panel yok"* şartını **kontrast desteği olmadan** karşılıyor:
   tipografi doğrudan parşömenin üstüne oturuyor.
4. **Açık zemin.** Ortalama parlaklık ~195; koyu mürekkep her yerde okunur.
   COVER-01'in ön kapağı 42,9 ortalamayla koyu ve **kemik beyazı domino**
   ile **neredeyse siyah ahşap** arasında uç yerel kontrast taşıyor.
5. **Sırtın üç bölümü tamamen temiz** — aşağıda.
6. **Kültürel bütünlük.** Kıtalar gerçek oyun geometrisinden kurulu; uydurma
   yazı sistemi, kutsal nesne ya da karma artefakt yok.

---

## 6 · Ölçülen tipografi yerleşimi

Bölgeler tahmin edilmedi; **sarım üzerinde tarandı** ve en sakin bantlar
seçildi (inç, sarımın sol-alt köşesinden):

| eleman | konum (in) | sd | kontrast desteği |
|---|---|---:|---|
| **Ön başlık** | x 9,60–16,85 · y 9,35–10,85 | **12,8** | **gerek yok** |
| **Ön yazar** | x 9,60–16,85 · y 0,45–1,55 | **13,7** | **gerek yok** |
| **Sırt başlığı** | y 8,60–10,60 | **9,3 / 8,9** | **gerek yok** |
| **Sırt yazarı** | y 0,60–1,60 | **8,6** | **gerek yok** |
| **Arka kapak metni** | x 0,70–5,90 · y 0,60–4,60 | 27,7 | **gerek yok** (açık zemin) |
| **Barkod boş alanı** | x 6,375–8,375 · y 0,375–1,575 | 7,9 | — boş bırakılır |

### Sırt: ortası kalabalık, iki ucu temiz

Sırt boydan boya ölçüldü ve **üç bölgeye ayrıldığı** görüldü:

| y (in) | sd |
|---|---:|
| 0,60–1,60 | **8,6** ✅ |
| 1,60–8,60 | 32,4 – 47,4 ⛔ (Afrika kıyısı ve pachisi haçı buradan geçiyor) |
| 8,60–10,60 | **9,3 / 8,9** ✅ |

Bu yüzden sırt yazısı **ortadan geçirilmiyor**: başlık üstteki temiz iki
inçlik koşuya, yazar adı alttaki temiz bir inçlik koşuya yerleştiriliyor.
Kalabalık orta bölge **boş bırakılıyor**. Bu bir uzlaşma değil, ölçümün
söylediği yerleşimdir.

---

## 7 · Metin denetimi

İstem **mutlak metin yasağı** koyuyordu. İki aday da bu yönden incelendi:

| aday | sonuç |
|---|---|
| COVER-01 | Mankala tahtasının iki ucundaki **oyma kabartma** yakınlaştırılıp incelendi: soyut çentik ve şevron deseni, **harf biçimi yok**. Yine de aday seçilmedi. |
| **COVER-02** | Haritanın dört kenarı, dört köşesi ve Asya bölgesi **yakınlaştırılıp incelendi**: yer adı, kartuş, ölçek çubuğu, pusula harfi, etiket **YOK**. Yalnızca tahta geometrisi. ✅ |

Ticari kapak metninin tamamı sonradan **vektör tipografiyle** basılıyor.

---

## 8 · İşleme

| | |
|---|---|
| Yöntem | `ASSET_UPSCALING_REPORT.md § 4.1` — Real-ESRGAN ncnn-vulkan (`upscayl-bin`) |
| Model | `digital-art-4x` (§ 6.4'ün illüstrasyon önerisi) |
| Ölçek | 4× |
| Ham | 1569 × 1003 px · efektif **89,1 DPI** |
| Yükseltilmiş | 6276 × 4012 px · efektif **356,4 DPI** ✅ |
| Ölçek çarpanı | 4,00 |
| Hedef | 5283 × 3375 px @ 300 ppi (17,6103 × 11,2500 in) |
| Pay | %18,8 fazla piksel — küçültülerek kullanılıyor, büyütülerek değil |
| Çıktı | `07_ASSETS/processed/cover/cover-02-4x-300dpi.png` |

**Ham dosyaya yazılmadı.** DPI etiketi yazıldı ama **karar etiketten değil
bölmeden verildi**: 6276 ÷ 17,6103 = 356,4.

---

## 9 · Reddedilen adayın durumu

`COVER-01` **silinmedi**. `07_ASSETS/raw/cover/` içinde duruyor ve bu rapor
onun neden kullanılmadığını sayılarla kaydediyor. Bir sonraki ajan aynı
değerlendirmeyi baştan yapmak zorunda kalmasın diye.
