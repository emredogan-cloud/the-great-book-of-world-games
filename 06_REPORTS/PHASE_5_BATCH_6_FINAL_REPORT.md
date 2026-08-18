# FAZ 5 · BATCH 6 RAPORU — Kütüphaneci teslimi tükendi, kaynak duvarı ölçüldü

> **The Great Book of World Games** · Faz 5 · Batch 6 · dal: `main`
>
> ```
> BATCH 5 SONRASI :  38 / 100
> BATCH 6 SONRASI :  41 / 100
> HEDEF           : 100 / 100
> ```
>
> ⛔ **KRİTİK KAYNAK SORUNU — kurucunun § 5'te istediği rapor budur.**
> Kalan **59 oyunun 52'sinin** kaynağı erişilemez. Otonomi verildi ve
> kullanıldı; duran şey ajan değil, **arz**.

---

## 1 · Bu batch'te yazılan üç oyun

| oyun | kültür | aile | kaynak | tür |
|---|---|---|---|---|
| **Astragaloi** | Antik Yunan | şans | kurucu teslimi | K5 uygulandı |
| **Senet** | Eski Mısır | eve dönüş | kurucu teslimi | **reconstructed** |
| **Janggi** | Kore | savaş tahtası | **Culin 1895, ss. 82–89** | **sayfa-doğrulanmış birinci el** |

**Kütüphaneci teslimindeki on bir oyunun on biri de işlendi.** Onu
yazıldı; `go` teslimde yoktu ve P5'te kaldı.

### 1.1 Janggi bu fazın en güçlü kaynağıdır

W. H. Wilkinson Seul'de görevli İngiliz konsolos vekiliydi ve bölümü
Culin için **kendisi yazdı**; örnek olarak Britanya Elçiliği bahçesinde
oynanan bir oyunu verir. Derleme değil, **birinci el gözlem** — Falkener
ve Forbes'tan bir sınıf yukarısı.

İki genel yasa kural bloğunun başına kondu çünkü kalan her hareket
onlardan türer: **taşlar hareket ettikleri gibi alır**, ve **taşlar
çizili her çizgi boyunca gidebilir**. İkincisi hisar köşegenlerini
gerçek yollara çevirir. Wilkinson köşegenlerin Kore tahtasından
**çıkarılamayacağını** açıkça söyler; `janggi-camp` onları v1.5 `lines`
ile çiziyor.

Başka hiçbir satrançta olmayan **kaybeden taraf ayrıcalıkları** da
aktarıldı: kendi şahıyla şah çekerek berabere zorlama — Wilkinson'un
deyişiyle *"aşağılık itirafı"* — ve tek kalan şahın pas geçmesi.

---

## 2 · ⛔ KAYNAK DUVARI — 59 oyunun tam dökümü

Kalan her oyun elimdeki on kamusal alan derlemesine karşı **tek tek**
tarandı. Sonuç:

| küme | sayı | anlamı |
|---|---:|---|
| **A · şimdi yazılabilir** | **7** | derlemede gerçek isabet var |
| **B · bütün kaynakları engelli** | **22** | Parlett · Bell · Murray · Zaslavsky · de Voogt · Pollux |
| **C · isabet yok / karışık** | **30** | künye var, açılabilir metin yok |

### 2.1 A · Şimdi yazılabilir (7)

| oyun | aile | kültür | kaynak |
|---|---|---|---|
| gilli-danda | tahtasız | Pencap | Culin 1907 (*Tipcat*) |
| chaupar | eve dönüş | Hindustani | Culin 1895 (*Chausar*) |
| tabula | eve dönüş | Bizans | Fiske 1905 |
| nine-holes | çizgi-toprak | İngiliz | Gomme 1894 |
| alquerque | savaş tahtası | Endülüs Arabı | Fiske 1905 |
| tuknanavuhpi | savaş tahtası | Hopi | Culin 1907 |
| ludus-latrunculorum | savaş tahtası | Roma | Falkener 1892 |

⚠ **İkisi kültür tuzağı riski taşıyor ve açılmadan yazılamaz:**
`gilli-danda` Pencap'tır ama isabet Culin'in **Tipcat**'idir (İngiliz/
Kuzey Amerika); `chaupar` Hindustani'dir ve isabet Culin'in Kore
cildindedir. İkisi de sayfa açılmadan yazılırsa **Totolospi hatası**
tekrarlanır.

### 2.2 B · Bütün kaynakları engelli (22)

```
ampe · pilolo · aadu-puli-attam · bagh-chal · len-choa · rimau-rimau
ashta-kashte · bohnenspiel · congklak · oware · pallanguzhi
toguz-kumalak · dara · morabaraba · shax · shisima
twelve-mens-morris · hasami-shogi · jeu-de-dames · makruk
surakarta · turkish-dama
```

**Ekim ailesi bu kümede çöküyor:** oware, congklak, pallanguzhi,
toguz-kumalak, bohnenspiel — beşi de tek tek Zaslavsky/Bell/Murray'e
bağlı. Aile hedefi 14, yazılan 1.

### 2.3 C · İsabet yok (30)

Otuz oyunun künyesi var ama **açılabilir metni yok**. Aralarında
`morra`, `myinda`, `nard`, `konane`, `mu-torere`, `tapatan`, `yote`,
`zamma`, `go` ve K23'ün iki terfisi (`kho-kho`, `lagori`) var.

> **Bu bir çaba sorunu değil.** Faz 5 boyunca üç ayrı kaynak avı yapıldı
> (Alfonso X · Elsdon Best · Culin Hawaiian · Gomme cilt II · Foster's
> Hoyle · JSTOR) ve **hiçbiri bir oyun açmadı**. Kalan kaynaklar ya
> telifli, ya JSTOR'da, ya da yalnızca basılı.

---

## 3 · KAYNAK DÜRÜSTLÜĞÜ — sayılarla

| | |
|---|---:|
| Doğrulama kaydı | **57** |
| `verified` | **38** |
| `pending` (açıldı, kural yok / kimlik uyuşmuyor) | **10** |
| `blocked` (denendi, erişilemedi) | **9** |
| **Kütüphaneci kaydı** | **11** |
| **bunlardan bağımsız doğrulanmış** | **0** |
| **künyesi tam** | **0** |
| **uydurulmuş sayfa numarası** | **0** |

On bir kütüphaneci kaydının **on biri de** `founderSupplied=true`,
`independentVerification=false`, `bibliographyStatus=incomplete` taşıyor
ve `sourcePages` **boş**. Finkel, de Voogt, Zaslavsky ve Pollux için
projenin **ENGELLİ** kayıtları olduğu gibi duruyor; hiçbir madde o
kitapların okunduğunu iddia etmiyor.

Manuscript'teki **yedi madde** `reconstructed` işaretli ve her birinin
prozası hangi kuralın kaynaklı hangisinin editoryal olduğunu **satır
satır** söylüyor.

---

## 4 · SAYFA MODELİ VE EKONOMİ — kilitlenmeye hazır

| | batch 5 | **batch 6** |
|---|---:|---:|
| Yazılmış oyun | 38 | **41** |
| **Toplam sayfa** | 254 | **254** |
| **Sapma** | −%0,8 | **−%0,8** ✅ |
| Çift sayfayı aşan | 1/38 | **1/41** (tablut) |
| Sürücü | both | **both** |
| **Ciltsiz telif** | 8,48 $ | **8,48 $** |
| **Ciltli telif** | 11,03 $ | **11,03 $** |
| Kindle telif | 7,19 $ | **7,19 $** |

Model **41 oyunluk gerçek dizgiyle** ölçülüyor ve dört batch'tir
±%1 içinde duruyor. **Kilitlenebilir durumda — ama kilitlenmedi**,
çünkü kalan 59 madde ortalamayı değiştirebilir.

---

## 5 · DİYAGRAM VE ARKA MADDE

| | |
|---|---:|
| Render edilen diyagram | **38** |
| Oyun başına azami | **144,0 mm** (tablut) |
| 150 mm'yi aşan (K24 dışında) | **0** |
| Diyagram dili | **v1.5** |
| Tahta şablonu | **28** |
| Sözlük | **61 terim** (34'ü prozada geçiyor) |
| Kaynakça | **100 madde** (31'i sayfa-doğrulanmış) |
| Uydurulmuş gelenek | **7** |
| **Ölçülmüş sayfa göndermesi** | **41 / 100** |
| **Uydurulmuş sayfa numarası** | **0** |

---

## 6 · KAPSAM

| | |
|---|---:|
| Kilitli oyun | **100** ✅ |
| Kültür | **68** (vaat ≥45) |
| Değişiklik şerhi | **2** (K23 · K28) |
| Aileler | boardless 16 · chance 4 · hunt-siege 10 · race 18 · sowing 14 · territory 17 · war-board 21 |

---

## 7 · DIŞ TEST

### EXTERNAL PLAYTEST: **NOT PERFORMED** — 0 oturum · 0 kayıt · 0 `locked`

```
PRODUCTION        : AUTHORIZED
FORMAL VALIDATION : PENDING
```

`.gate` = `phase1`, yükseltilmedi.

---

## 8 · KURUCU KARARI GEREKEN ÜÇ YOL

Kalan 52 oyun için üç yol var ve üçü de **kurucunundur**:

| # | yol | ne açar |
|---|---|---|
| **1** | **Kütüphaneci teslimini sürdürmek** | En verimlisi. On bir oyunluk teslim **on oyun** yazdırdı. B kümesinin 22'si ve C'nin çoğu bu yolla açılır. |
| **2** | **Kütüphane / JSTOR erişimi** | Parlett · Bell · Murray · Zaslavsky · de Voogt · Culin *Hawaiian Games* · Pollux açık edisyonu. |
| **3** | **İkinci bir kapsam değişikliği** | Erişilemeyen oyunları, kaynağı elde olanlarla değiştirmek. **Ama yedek havuz artık 8 oyuna indi** ve K28 en iyilerini zaten aldı. |

**En yüksek getirili istek — ekim ailesi:** oware · congklak ·
pallanguzhi · toguz-kumalak · bohnenspiel. Beşi tek teslimde gelirse
aile 1/14'ten 6/14'e çıkar.

---

## 9 · FAZ 6 HAZIRLIĞI

| hazır | değil |
|---|---|
| Kapsam 100 · kilitli · iki şerhli · denetlenen | **59 oyun yazılmadı** |
| Sayfa modeli dört batch'tir ±%1 (254) | **Dış test kanıtı (0)** |
| Ekonomi senkron (8,48 $ / 11,03 $) | `locked` oyun (0) |
| Diyagram dili v1.5 · 38 diyagram · bütçe içinde | Ön madde ve giriş denemesi |
| Arka madde üretilen · 100 maddelik kaynakça | ~130 görsel |
| 185 kasıtlı kusur testi · CI yeşil | **52 oyunun kaynağı** |

---

**⛔ FAZ 6 BAŞLAMADI.** KDP'ye dokunulmadı, prova sipariş edilmedi.
Ajan **kaynağı olan her oyunu yazdı** ve kaynağı olmayanı uydurmadı.
