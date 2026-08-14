# FAZ 5 RAPORU — Kapsam değişikliği, arka madde ve altı kapı kusuru

> **The Great Book of World Games** · Faz 5 · Dal: `faz/5-yakinsama`
>
> ⛔ **BU FAZ KENDİ ANA HEDEFİNİ TUTTURAMADI.** Hedef 100 oyundu; yazılan
> **20**'dir ve bu sayı Faz 4'ün 22'sinden **iki eksiktir**. Rapor bunu
> gizlemiyor ve baştan söylüyor.
>
> Faz 5 üç şeyi tamamladı — **kapsam değişikliği**, **arka madde** ve
> **altı kapı kusurunun düzeltilmesi** — ve bir şeyi tamamlayamadı:
> **oyun yazımı**.

---

## 0 · Tek bakışta

| | Faz 4 | **Faz 5** | |
|---|---:|---:|---|
| **Yazılmış oyun** | 22 | **20** | **−2** ⛔ |
| Kapsamdaki oyun | 100 | **100** | değişmedi |
| **Kapsamdaki kültür** | 71 | **73** | **+2** |
| **Tahtasız aile · kültür** | 11 | **13** | **+2** |
| **Tahtasız aile · İngiliz madde** | 5 | **3** | **−2** |
| Doğrulama kaydı | 37 | **44** | +7 |
| `verified` kayıt | 28 | **29** | +1 |
| Arka madde | **yazılmadı** | **ALTI BÖLÜM TAM** | ✅ |
| Üç indeks | yok | **üretildi + kapıya bağlandı** | ✅ |
| Sözlük | yok | **61 terim** | ✅ |
| Sayfa modeli | 258 | **260** | +2 |
| Hedeften sapma | +%0,8 | **+%1,6** | ✅ bantta |
| Ciltsiz birim telif | 8,41 $ | **8,37 $** | −0,04 $ |
| Ciltli birim telif | 10,96 $ | **10,92 $** | −0,04 $ |
| Diyagram (render) | 27 | **25** | −2 |
| Oyun başına azami diyagram | 144,0 mm | **144,0 mm** | ✅ |
| Selftest denetimi | 148 | **172** | +24 |
| Kuyruk öncelik seviyesi | 5 | **6** | +P6 |
| **Dış insan testi** | **0** | **0** | ⛔ değişmedi |
| **`.gate`** | `phase1` | **`phase1`** | yükseltilmedi |
| CI | yeşil | **yeşil** | |

---

## 1 · Faz 5 kapsamı

Kurucu talimatı yedi iş tanımladı:

| # | İş | Durum |
|---|---|---|
| 1 | Kapsam değişikliği (2 çıkarma + 2 terfi) | ✅ **TAM** |
| 2 | Gonggi/Fivestones çakışmasını çözmek | ✅ **TAM** |
| 3 | Tahtasız kültür yoğunlaşmasını ölçülebilir biçimde iyileştirmek | ✅ **TAM** |
| 4 | Kuyruğu yeniden kurmak (erişilebilir önce) | ✅ **TAM** |
| 5 | **Kalan oyunları yazmak (20 → 100)** | ⛔ **YAPILMADI** |
| 6 | Arka maddeyi tamamlamak | ✅ **TAM** |
| 7 | Kapsam sonrası yeniden kalibrasyon | ✅ **TAM** |

Beşinci satır bu fazın başarısızlığıdır ve § 8'de ayrıca ele alınıyor.

---

## 2 · KAPSAM DEĞİŞİKLİĞİ (K23)

Kurucu iki İngiliz tahtasız maddenin çıkarılmasını ve yedek havuzdan iki
terfiyi yetkilendirdi. Değişiklik `scope_lock.json § amendments[0]` içinde
**altı zorunlu alanla** kayıtlıdır ve `validate_scope.py` alanların
doluluğunu her koşuda denetler.

### 2.1 Seçim bir tercih değil, bir TÜRETMEDİR

Projenin kendi `scores.distinct` alanı (mekanik ayırt edicilik, 1–5)
tahtasız ailenin beş İngiliz maddesini şöyle sıralıyordu:

| madde | distinct | kaynak | yazılmış | karar |
|---|---:|---:|:---:|---|
| **fivestones** | **2** | 5 | evet | **ÇIKARILDI** |
| **marbles** | **3** | 5 | evet | **ÇIKARILDI** |
| conkers | 4 | 5 | evet | kaldı |
| hopscotch | 4 | 5 | evet | kaldı |
| cats-cradle | **5** | 5 | hayır | **kaldı** |

En düşük iki ayırt edicilik çıkarıldı.

**cats-cradle'ı çıkarmak "ucuz" olurdu** — tek yazılmamış maddeydi — ve
tam olarak bu yüzden yapılmadı. `distinct 5` ile ailenin en ayırt edici
maddesidir ve ailenin **tek sayfa-doğrulanmış** kaydıdır; çıkarmak
kurucunun iki ölçütünü birden (mekanik çeşitlilik · kaynak kalitesi)
**düşürürdü**.

---

## 3 · ÇIKARILAN OYUNLAR

### REMOVED_GAME_1 — **Fivestones** (İngiliz · tahtasız)

**Neden:** Faz 1'in kendi envanter kaydı şunu yazıyordu ve hiç
çözülmemişti:

> *"Gonggi ile aynı mekanik; ikisinden biri elenmelidir."*

Faz 4 ikisini de yazdı ve ayrımı **biçimde** yaptı (gonggi beş taşla ve
halkasız, fivestones halka + top biçimiyle). Kendi raporu bunu
*"bir çözüm değil bir azaltma"* diye adlandırdı. Faz 5 çözdü.

**Neden gonggi değil fivestones:** gonggi'yi çıkarmak İngiliz sayısını
düşürmez ve kapsamdan **bir kültürü tamamen silerdi** (Korece tahtasız
tek madde). fivestones'u çıkarmak ikisini birden düzeltir.

### REMOVED_GAME_2 — **Marbles** (İngiliz · tahtasız)

**Neden — iki gerekçe:**

1. **Mekanik çakışma.** Petanque ile aynı *"hedefe nişan alıp atma"*
   kümesindedir. Bu çakışmayı **projenin kendi kaydı adlandırıyor**:
   yedek havuzdaki `quoits` maddesinin `unresolvedQuestions` alanı
   *"Pétanque ile aynı kitapta iki 'hedefe atma' oyunu tekrar riski
   taşır"* der. Marbles o kümenin üçüncü üyesiydi.
2. **Basılan biçim kaynaktaki oyun değil.** Kaydın kendi ifadesiyle
   oyunun özü *"kazandığını alıkoymaktır"* — yani bir bahistir ve K5
   uyarınca puana çevrilmek zorundaydı.

---

## 4 · EKLENEN OYUNLAR

### ADDED_GAME_1 — **Lagori** (Kannada · tahtasız)

- Kapsamda **hiç bulunmayan** bir kültür (Kannada).
- Kitapta eşi olmayan **iki aşamalı** mekanik: yığını devir → kaçarken
  yeniden kur.
- 4–12 oyuncu · aile akşamına uyar.

### ADDED_GAME_2 — **Kho-Kho** (Marathi · tahtasız)

- Kapsamda **hiç bulunmayan** bir kültür (Marathi).
- Kovalamaca kümesinde **körlemesine olmayan tek yapı**: yön kısıtlı
  kovalayıcı + `kho` devri. (myinda ve mbube-mbube gözü bağlı oyunlardır.)
- 8–18 oyuncu — **kitabın en büyük grup oyunu**, oyuncu sayısı
  çeşitliliğini genişletir.

### 4.1 Seçim NEDEN bu ikisi — ve bu bir bulgudur

Yedek havuzda **dört** tahtasız oyun vardı. İkisi elendi:

| aday | neden ELENDİ |
|---|---|
| **quoits** | **İngiliz** — değişikliğin amacını doğrudan bozar. Ayrıca kendi kaydı petanque çakışmasını adlandırıyor (`distinct 2`). |
| **ephedrismos** | **Ancient Greek** — aile o kültürü zaten taşıyor (myinda). Ayrıca `reconstructed`: `play`, `turnLogic` ve `endCondition` alanları **partial**, ve kendi kaydı taşıma riskini işaretliyor. § 25 böyle bir maddeyi ertelemeyi şart koşar. |

> **BULGU: yedek havuz tahtasız ailede DERİN DEĞİL.** Dört adayın ikisi
> mekanik olarak elendiğinde geriye **tam olarak iki** aday kaldı — yani
> seçim bir tercih değil, bir **zorunluluktu**. Bir yedek havuzun görevi
> seçenek sunmaktır; bu ailede sunamadı. Bu, gelecekteki bir kapsam
> değişikliği için **kayıtlı bir risktir**.

---

## 5 · GONGGI / FIVESTONES ÇÖZÜMÜ

| | önce | sonra |
|---|---|---|
| Kümede madde | **2** (gonggi · fivestones) | **1** (gonggi) |
| Ayrım biçimi | biçimsel (halka/halkasız) | **kümede tek madde** |
| Faz 1 uyarısı | açık | **kapandı** |

Gonggi manuscript'te **yazılı olarak duruyor** ve etkilenmedi.

---

## 6 · TAHTASIZ AİLE KÜLTÜR DENGESİ — ÖNCE / SONRA

Kurucu § 5 ölçüm istedi; ölçüldü:

| ölçüt | **ÖNCE** | **SONRA** | fark |
|---|---:|---:|---:|
| tahtasız · oyun sayısı | 15 | 15 | 0 |
| **tahtasız · kültür** | **11** | **13** | **+2** |
| **tahtasız · İngiliz madde** | **5** | **3** | **−2** |
| kitap geneli · kültür | 71 | **73** | **+2** |

Aile artık kitabın **en dar kültür kümesi değildir**.

Kannada ve Marathi kapsama **ilk kez** giriyor.

---

## 7 · NİHAİ 100 OYUNLUK KAPSAM

| | |
|---|---:|
| Toplam oyun | **100** ✅ |
| Kültür | **73** (vaat: ≥45) |
| Yedek havuz | **19** (fivestones ve marbles geri döndü) |
| Yinelenen oyun | **0** |
| Değişiklik şerhi | **1** (K23) |

### Aile dağılımı — DEĞİŞMEDİ

| aile | hedef | kilitli |
|---|---:|---:|
| ekim (sowing) | 14 | 14 ✅ |
| av-kuşatma | 10 | 10 ✅ |
| eve dönüş (race) | 15 | 15 ✅ |
| çizgi-toprak | 14 | 14 ✅ |
| savaş tahtası | 17 | 17 ✅ |
| şans | 15 | 15 ✅ |
| **tahtasız** | **15** | **15** ✅ |

Dört maddenin dördü de tahtasız ailedendir; değişiklik ailenin
**içindedir** ve `family_index.json` hedeflerine **dokunulmadı**.

---

## 8 · YAZILAN OYUNLAR — ⛔ SIFIR

**Faz 5'te hiçbir yeni oyun yazılmadı.**

Yazılmış oyun sayısı **22 → 20** düştü, çünkü K23 iki **yazılmış** maddeyi
kapsamdan çıkardı.

| | |
|---|---:|
| Faz 5'te yazılan yeni oyun | **0** |
| K23 ile geri alınan yazılmış oyun | **2** |
| **Net yazılmış oyun** | **20 / 100** |
| Kalan | **80** |

### 8.1 Geri alınan iki madde SİLİNMEDİ

`02_MANUSCRIPT/retired_phase5.json` (korumalı katman) fivestones ve
marbles'ın **tam prozasını** ve **iki diyagram tanımını** taşıyor. Kurucu
kararı tersine çevirirse iş kaybolmuş değildir.

### 8.2 Neden hiç oyun yazılmadı — dürüst hesap

Bu fazın bütçesi üç yere gitti:

1. **Kapsam değişikliği** — kurucunun açıkça ilk sıraya koyduğu iş
   (§ 38 · adım 9–15). On dokuz alt adımın hepsi yapıldı.
2. **Altı kapı kusuru** — değişikliğin kendisi üç yeni yalan sınıfı açtı
   ve üçü de düzeltilmeden ilerlemek, kapsam kilidini bir tiyatroya
   çevirirdi (§ 11).
3. **Arka madde** — Faz 4'ün yazmadığı ve roadmap'in Faz 4 DoD'sinde
   duran iş (§ 12).

Dördüncüsüne — yazıma — sıra geldiğinde **beş oyunun kaynağı sayfa
seviyesinde açıldı ve beşi de yazılamaz çıktı** (§ 10).

> **Bu bir mazeret değil bir hesaptır.** Kurucunun § 7 hedefi 100 oyundu
> ve tutturulmadı. Kalan 80 oyun, üretimin **tek gerçek darboğazıdır**.

---

## 9 · ERTELENEN OYUNLAR — SAYFA SEVİYESİNDE GEREKÇELİ

Faz 5, beş oyunun kaynağını **açtı ve okudu**. Hiçbiri ikincil bilgiyle
ertelenmedi; beşinin de gerekçesi bir **sayfa ve bir pasajdır**.

| oyun | kaynak | sayfa | bulgu |
|---|---|---|---|
| **hnefatafl** | Fiske 1905 | ss. 58–59 | kaynak **erişilebilir** ama **kural vermiyor** |
| **halatafl** | Fiske 1905 | s. 59 | yalnızca bir **sözlük göndermesi** |
| **cats-cradle** | Jayne 1906 | ss. 324–338 | **kural TAM** — engel **editoryal** |
| **oware** | Culin 1896 | ss. 594, 597–598 | **kimlik tuzağı** |
| **jianzi** | Culin 1895 | ss. 39–43 | **nesne anlatılıyor, kural yok** |

### 9.1 Hnefatafl — erişilebilir bir kaynak, olmayan bir kural

Fiske 1905 bir **filoloji** incelemesidir. Verdiği her şey şudur: iki
oyuncu, tek kral (*hnefi*, "silahsız efendi"), iki renk taş, biri saldırır
biri kralı savunur. **Hareket yok, alma yok, tahta ölçüsü yok, kazanma
koşulu yok.** Fiske'nin kendi cümlesi:

> *"For whatever we may not know about hnefatafl, we do know that it could
> never have lain in the same cradle as chess."*

> Erişilebilir bir kaynak, **yeterli** bir kaynak demek değildir. Faz 4'ün
> K20 dersi (*"erişilebilir ≠ güvenilir"*) burada ikinci bir biçim aldı:
> **erişilebilir ≠ kural taşıyor.**

Kitabın **tek belgelenmiş tafl oyunu tablut'tur** (Linnaeus 1732) ve o
**yazıldı**.

### 9.2 Cats-cradle — kaynak yeterli, engel KİTABIN İÇİNDE

Jayne 1906 tam bir kural kaydıdır: iki oyuncu, tek ip halkası, sırayla
ipi birbirinin elinden alma, **sekiz adlandırılmış figür**, ve bitiş
(*Clock*, yazarın babasının tanıklığıyla). Hatta bir varyant bile verir
(Filipinli Linao Moro biçiminde *Cat's Eye* → *Manger*).

**Engel K19'dur:** sekiz figür, oyun başına 150 mm diyagram tavanına
sığmıyor — figür başına **~18 mm** düşer ve o boyutta parmak hareketi
okunmaz. Faz 1 kaydı bu riski zaten işaretlemişti.

Üç seçenek de **kurucu kararıdır** ve ajan tek başına seçemez:

- **(a)** bu madde için tavanı **açıkça** aş (K19'da istisna kaydı gerekir);
- **(b)** maddeyi ilk üç figürle bas (kaynaktan **eksik** olur, beyan şart);
- **(c)** figürleri metinle anlat (`explain` puanı 2 — en riskli seçenek).

Bu, `source_access_pending.json § editorialHolds` içinde **açık karar**
olarak kayıtlıdır.

### 9.3 Oware — kimlik tuzağı, üçüncü kez

Culin 1896'nın **ayrıntılı kural kayıtları** Şam (Suriye) ve Vei
(Liberya) biçimlerinindir; ikisi de Culin'e **bizzat anlatılmıştır**.
Gold Coast/Akan *wari*'si yalnızca Bent'ten yapılan bir alıntıda **anılır**
ve kuralı verilmez.

Akan oyununu Şam kaydından yazmak, kitabın kültür künyesini yalanlar —
**Totolospi ve Sugoroku ile aynı sınıf**, üçüncü örnek.

### 9.4 Jianzi — Faz 4'ün kararı sayfa açılarak DOĞRULANDI

Faz 4 jianzi'yi ikincil bilgiyle ertelemişti. Faz 5 sayfayı okudu:
Culin § XXXIII **nesneyi** anlatıyor (pamuk bezi, kil, sülün tüyü) ve
bağlamı veriyor (dükkâncılar ayaklarını ısıtmak için sokakta oynar).
**Puanlama yok, tur yok, oyuncu sayısı yok, bitiş yok.** Üstelik kayıt
**Kore** (*Tjye-ki*) ve **Japon** (*hago*) biçimlerinindir; kapsamdaki
madde **Han Çinlisidir**.

Faz 4'ün kararı **aynen geçerli** ve artık sayfa dayanağı var.

---

## 10 · KAYNAK DURUMU

| durum | Faz 4 | **Faz 5** |
|---|---:|---:|
| `verified` — ≥2 doğrulanmış künye | 3 | **3** |
| `partially-verified` — 1 künye | 22 | **20** |
| `access-blocked` — denendi, erişilemedi | 5 | **5** |
| **`record-not-found` — arandı, kayıt yok** | — | **2** |
| `not-attempted` — sıraya gelmedi | 70 | **70** |

Doğrulama kaydı **37 → 44** (7 yeni: 5 soruşturma + 2 terfi).

### 10.1 Terfi eden iki oyunun kaynağı ARANDI ve BULUNAMADI

Bu, terfinin **dürüst** kaydıdır:

- **kho-kho** — kuralları ilk kez **1914**'te Deccan Gymkhana (Pune)
  komitesince çerçevelendi, ilk basılı kural kitabı **1935**. Dönem
  etnografik kaydı bulunamadı. Yani oyunun oynanabilir biçimi bir
  **20. yüzyıl kodifikasyonudur**, "kadim" çerçevesi kaynaksızdır ve
  prozada bu açıkça söylenmelidir.
- **lagori** — Thurston 1906 (*Ethnographic Notes in Southern India*) tam
  metni tarandı: **oyun bölümü yok**. archive.org 1850–1930 "games +
  India" başlık taraması kullanılabilir kayıt vermedi.

> **Terfi bir KAPSAM kararıdır, bir YAZIM izni değil.** İkisi de kuyrukta
> **P6**'dadır ve zayıf kanıtla yazılamazlar (§ 13).

---

## 11 · ENGELLİ OYUN KUYRUĞU — ve YENİ BİR AYRIM

| P | anlamı | sayı |
|---|---|---:|
| 1 | erişilebilir · sayfa-doğrulanmış · kural tam | **22** |
| 2 | erişilebilir · doğrulama tamamlanabilir | **65** |
| 3 | yeniden kurgulanmış · plan belgeli | **5** |
| 4 | **DENENDİ ve erişilemedi** (telif / ödünç) | **5** |
| 5 | çözülmemiş kural kimliği | **1** |
| **6** | **ARANDI ve KAYIT BULUNAMADI** | **2** |

**Erişilebilir: 92 · ertelenmiş: 8.** Sıra kapıya bağlıdır ve CI'da koşar.

### 11.1 P6 neden AYRI bir seviye

Faz 3 *"denenmedi = engelli"* hatasını düzeltmişti. Faz 5 aynı hatanın
**bir seviye derindekini** buldu:

> **P4 ≠ P6.**
> **P4 bir ERİŞİM engelidir:** kayıt **vardır**, nüshası kapalıdır ve
> kurucunun bir kütüphane kartı onu **açar**.
> **P6 bir VARLIK sorunudur:** denetlenebilir bir kayıt **henüz yoktur**
> ve hiçbir erişim izni onu **var etmez**.

İkisini aynı kovaya atmak, kurucuya *"kütüphane erişimi bul, iki oyun daha
açılır"* demek olurdu. Açılmazlar.

### 11.2 ÜÇÜNCÜ bir engel türü: `editorialHolds`

cats-cradle ne P4 ne P6'dır: **kaynağı tam ve sayfa-doğrulanmış**. Engel
kitabın **kendi üretim kuralındadır** (K19 · 150 mm).

Kuyrukta **P1'de kalıyor** ama askısı **görünür** — yoksa bir sonraki
üretici onu listenin başında görüp duvara çarpardı. `build_queue --check`
artık askının **belgeli** olmasını ve askıdaki bir oyunun **yazılmamış**
olmasını şart koşuyor.

---

## 12 · İNGİLİZCE EDİTORYAL DURUM

Faz 5 **yeni ticari proza yazmadı**; ama **arka madde ticari içeriktir**
ve doğrudan İngilizce üretildi.

| | |
|---|---:|
| Ticari katmanda Türkçe | **0** |
| `translatedFrom` dolu ticari kayıt | **0** |
| `qa_language_split.py` | ✅ 13 denetim yeşil |

### 12.1 DİL KAPISI İKİ GERÇEK SIZINTI YAKALADI

Arka madde üretecinin ilk sürümü **iki ayrı yoldan Türkçe sızdırdı** ve
ikisini de kapı yakaladı:

1. **Malzeme rehberi** envanterin `substitutionHint` alanlarını **doğrudan**
   ticari katmana taşıyordu (*"yumurta kolisi"*, *"kuru fasulye"*).
2. **Kaynakça** doğrulama kaydının `locator` alanını basıyordu
   (*"'Ring-taw', cilt II, ss. 113–114"*).

**Kapı zayıflatılmadı; üreteç düzeltildi.** 86 terimlik ticari İngilizce
eşleme eklendi ve **eşlenmemiş bir ipucu görülürse üreteç çöküyor** —
sessizce Türkçe basmak ya da satırı atlamak yerine **duruyor**. Kaynakça
artık yazılmış maddenin **kendi İngilizce künyesini** kullanıyor.

> Envanterin Türkçe olması **doğrudur** (veri katmanı). Yanlış olan, o
> katmanı ticari katmana **köprüsüz bağlamaktı**.

---

## 13 · OYNANABİLİRLİK DURUMU

| | |
|---|---:|
| Yazılmış madde | **20** |
| Beş öğesi tam | **20 / 20** ✅ |
| Üç sorusu cevaplı | **20 / 20** ✅ |
| Yedi başlıkta doğrulama kaydı | **20 / 20** ✅ |
| **Dış insan testi** | **0** ⛔ |
| `locked` madde | **0** |

`qa_manuscript.py` **16 denetim** koşuyor (Faz 4: 15) — Faz 5 sekizinci
bölümü ekledi (§ 14.3).

---

## 14 · ALTI KAPI KUSURU

Bu, Faz 5'in en değerli çıktısıdır. **Altı kusur da gerçek veriyle YEŞİL
koşuyordu** — hiçbiri hata vermiyordu.

### 14.1 Şerh, kilit özetini ÖMÜR BOYU devre dışı bırakıyordu

`validate_scope.py` şöyle diyordu:

```python
rep.check(have == want or bool(lock.get("amendments")), ...)
```

Yani **bir tane** değişiklik şerhi düşüldüğü anda sha256 denetimi
**sonsuza kadar** kapanıyordu ve liste ondan sonra sessizce
değiştirilebiliyordu. Faz 5'in kendi kapsam değişikliği bu deliği
**açacaktı**.

**Doğru ayrım:** şerh, özetin **neden** değiştiğini açıklar;
**denetlenmemesini** sağlamaz.

### 14.2 "Model ayrışırsa kapı ısırır" — öyle bir kapı YOKTU

`scope_lock.json`'ın kendi başlığı şunu **vaat ediyordu**:

> *"Model bir gün başka bir liste üretirse bu KAPI ISIRIR; liste sessizce
> güncellenmez."*

**Isırmıyordu.** Böyle bir denetim **hiç yazılmamıştı**: seçim modeli her
koşuda kendi 100'ünü üretiyor, kilit kendi 100'ünü taşıyor ve ikisi
**karşılaştırılmıyordu**. Faz 5'in değişikliği ikisini gerçekten ayrıştırdı
ve hiçbir kapı fark etmedi.

**Düzeltme:** ayrışmanın **tamamı** kayıtlı bir şerhle açıklanmak zorunda.
Açıklanmayan tek bir kimlik bile kapıyı kırar.

> Bir belgede yazan kapı, kodda yoksa **yoktur**. Faz 1'in D5 dersi
> (*"bir kapının VARLIĞI, KOŞTUĞU anlamına gelmez"*) burada bir adım
> öteye gitti: **bir kapının İDDİA EDİLMESİ, VAR OLDUĞU anlamına gelmez.**

### 14.3 Kapsamdan çıkarılan oyun BASILMAYA devam edebiliyordu

`qa_manuscript.py` manuscript'i kapsam kilidiyle **hiç karşılaştırmıyordu**.
Amendment'tan sonra fivestones ve marbles manuscript'te duruyordu, kapı
**22 madde** sayıp **yeşil** koştu.

Kurucunun § 32 listesindeki *"removed game remains in final scope"* kusuru
tam olarak budur. Yeni **§ ⑧ KAPSAM** bölümü eklendi.

### 14.4 Dizgi ölçümü manuscript altından değişince BAYAT kalıyordu

`calibrate_pages.py --check` yalnızca **kendi içinde** tutarlılık
denetliyordu. Manuscript 22'den 20'ye düştüğünde ölçüm hâlâ **"22 oyun ·
258 sayfa"** diyordu ve *"dizgi ölçümü tutarlı"* diye **yeşil** yanıyordu.

**Düzeltme:** manuscript yereldeyse ölçümün kapsadığı madde kümesi **canlı
manuscript'le** karşılaştırılıyor.

### 14.5 Kalibre config, ölçümden KAYINCA ekonomi eski sayıyla hesaplanıyordu

Ölçüm raporunu `calibrate_pages.py` yazar; **ekonomiyi** hesaplayan
`page_budget.py` ve `editions.py` sayıyı **rapordan değil**
`project_config.json § production.pageModel.measured` içinden okur.
İkisini bağlayan tek şey, ölçümden sonra config'i güncellemeyi
**hatırlamaktı**.

Faz 5'te koptu: yeni ölçüm **260** dedi, config **258** demeye devam etti,
iki betik **eski sayıyla telif hesapladı** ve hiçbir kapı itiraz etmedi.

> Sayfa sayısı kapak **sırtını** ve **birim telifi** belirler. Sessizce
> eski kalması, kitabın ekonomisini **eski kitaptan** hesaplamaktır.

### 14.6 Emekliye ayrılan diyagram, BÜTÇEDE sayılmaya devam ediyordu

`qa_diagram.py` tek yönlü soruyordu: *"her tanımın ölçümü var mı?"*
Tersi — *"ölçümde durup tanımı olmayan var mı?"* — **sorulmuyordu**.

K23 iki diyagramı emekliye ayırdı, tanımları silindi, ama
`diagram-render.json` ikisini de **saymaya devam etti** ve kapı yeşil
yandı. Bu bir muhasebe hatası değil bir **bütçe** hatasıdır: 150 mm
toplamı o dosyadan hesaplanır.

### 14.7 Ayrıca — üç küçük düzeltme

| kusur | düzeltme |
|---|---|
| `validate_research.py` `VALID_VERIFICATION` listesini config'le **ikinci kez** yazıyordu; config'e üçüncü seviye eklenince kapı **geçerli veriyi reddetti** | tek kaynak; sabit yalnızca taban |
| `validate_scope.py`'nin **`--root` sözleşmesi yoktu**; selftest'in kapsam testleri kapı ısırdığı için değil **argparse hatası verdiği için** geçiyordu | eklendi — testler artık gerçekten ısırıyor |
| `render_diagrams.py` raporu yalnızca `--json` verilince yazıyor | § 14.6 kapısı bayatlığı artık **yakalıyor** |

> **En rahatsız edici olan ikincisidir.** Kendi yazdığım kasıtlı kusur
> testleri, **yanlış sebeple** yeşil yanıyordu. Yeşil yanan ama hiçbir şey
> sınamayan bir test, testsizlikten **daha kötüdür**: koruma olmadığı hâlde
> koruma **var sanılır**.

---

## 15 · DİYAGRAM ÖLÇÜMLERİ

| | Faz 4 | **Faz 5** |
|---|---:|---:|
| Render edilen diyagram | 27 | **25** |
| En küçük | 36,1 mm | **36,1 mm** |
| En büyük | 111,5 mm | **111,5 mm** |
| Ortalama | 66,1 mm | **67,1 mm** |
| Diyagram dili | v1.4 | **v1.4** (değişmedi) |

İki diyagram (`fivestones-ring` · `marbles-ring`) K23 ile emekliye ayrıldı;
tanımları `retired_phase5.json` içinde korunuyor.

---

## 16 · 150 MM OYUN SEVİYESİ SONUÇLARI

| | |
|---|---:|
| 150 mm'yi aşan **DİYAGRAM** | **0** |
| 150 mm'yi aşan **OYUN** | **0** |
| Azami oyun toplamı | **144,0 mm** (tablut) |

Faz 4'ün oyun-seviyesi kapısı yürürlükte ve **bayat ölçüm** kusuru
(§ 14.6) kapatıldıktan sonra artık **gerçek** kitabı denetliyor.

⚠ **cats-cradle bu tavanla çatışıyor** ve açık karardır (§ 9.2).

---

## 17 · SAYFA MODELİ

| | Faz 4 (22 oyun) | **Faz 5 (20 oyun)** |
|---|---:|---:|
| Kelime / sayfa | 447 | **444** |
| Kelime / oyun | 686 | **682** |
| Metin sayfa/oyun | 1,24 | **1,24** |
| Diyagram sayfa/oyun | 0,293 | **0,298** |
| Ölçülen sayfa/oyun | 1,53 | **1,54** |
| Faturalanan sayfa/oyun | 2,09 | **2,10** |
| **Taşma oranı** | %4,5 (1/22) | **%5,0** (1/20) |
| **Toplam** | **258** | **260** |
| **Sapma** | +%0,8 | **+%1,6** ✅ |

Çıkan iki madde kısa metinli ve küçük diyagramlıydı; gitmeleri ortalamayı
**yukarı** itti. Sayfa **hedefi** değiştirilmedi (yol haritası § 15).

### 17.1 Faz 4'ün "BOTH" bulgusu ikinci örneklemde DOĞRULANDI

| | metin farkı | diyagram farkı | sürücü |
|---|---:|---:|---|
| Faz 4 (22) | 0,686 | 0,628 | **both** |
| **Faz 5 (20)** | **0,686** | **0,628** | **both** |

Tek bir sürücü yoktur. *"Sayfa bütçesi bir diyagram bütçesidir"* cümlesi
Faz 4'te yanlışlanmıştı; Faz 5 onu **tekrar** ölçtü ve sonuç aynı.

---

## 18 · EKONOMİK MODEL

| sürüm | Faz 4 (258 s.) | **Faz 5 (260 s.)** |
|---|---:|---:|
| Ciltli telif | 10,96 $ | **10,92 $** |
| **Ciltsiz telif** | **8,41 $** | **8,37 $** |
| Kindle telif | 7,19 $ | **7,19 $** |
| Başabaş ACOS (ciltli) | %31,3 | **%31,2** |

Üç sürüm de pozitif telif üretiyor. KDP Select/KU kontrolü (K6) yürürlükte.

---

## 19 · ARKA MADDE — ALTI BÖLÜM TAM

Faz 4'ün yazmadığı iş **tamamlandı**. `EDITORIAL_ARCHITECTURE § 5`'in
istediği altı bölümün **altısı da** var:

| # | bölüm | model | **üretilen** |
|---|---|---:|---|
| ① | Tahta şablonları | 8 s. | **18 şablon** |
| ② | Malzeme rehberi | 2 s. | **85 satır** |
| ③ | Sözlük | 3 s. | **61 terim** (şart: ≥60) |
| ④ | Kaynakça | 4 s. | **100 madde** |
| ⑤ | **Üç indeks** | 3 s. | **73 kültür · 3 oyuncu kovası · 3 süre kovası** |
| ⑥ | Uydurulmuş gelenekler | 1 s. | **5 düzeltme** |

### 19.1 Üç indeks

| indeks | kovalar |
|---|---|
| **Kültüre göre** | 73 kültür |
| **Oyuncu sayısına göre** | 2 kişi: **68** · 3–4 kişi: **8** · 5+ kişi: **24** |
| **Süre ve yaşa göre** | ≤15 dk: **10** · ≤30 dk: **46** · 30+ dk: **44** |

Üçü de **100 oyunun tamamını** taşıyor ve her oyun her indekste **tam bir
kez** görünüyor.

### 19.2 Uydurulmuş gelenekler kutusu

Beş kaynaksız iddia düzeltiliyor: seksek/Roma askerleri · Kurna Tapınağı
MÖ 1400 · Kalah'ın "kadim Afrika" iddiası · "Chinese Checkers"ın 1892
Almanya'sı · ve **her kazınmış ızgaranın bir oyun tahtası sayılması**.

---

## 20 · ÜRETİLEN İNDEKSLER — ZİNCİR VE DOĞRULAMA

Kurucu § 27'nin istediği zincir kuruldu:

```
KAYNAK      scope_lock · game_index · source_verification ·
            diagram kayıtları · book.json · dizgi ölçümü
   ↓
ÜRETEÇ      04_BUILD/build_backmatter.py
   ↓
ÇIKTI       02_MANUSCRIPT/backmatter.json  (korumalı · tam metin)
            06_REPORTS/backmatter.json     (public · yapısal özet)
   ↓
DOĞRULAMA   04_BUILD/qa_index.py  ·  31 denetim
```

### 20.1 SAYFA NUMARASI UYDURULMUYOR

Kurucu § 27 şunu şart koşar: *"Page references must be tested against
actual rendered output."* Karşılanma biçimi:

| | |
|---|---:|
| Sayfa göndermesi **ölçülmüş** oyun | **20 / 100** |
| `awaiting-typesetting` taşıyan oyun | **80 / 100** |
| **Uydurulmuş sayfa numarası** | **0** |

Sayfa göndermeleri, gerçek dizgi ölçümünün `billedPages` değerinden
**birikimli** türetiliyor. Dizilmemiş bir oyunun sayfası `null`dır.

> Ölçülmemiş bir sayfa numarası, **test edilemeyen bir iddiadır**.

### 20.2 Kapı, üretecin kovalarını İÇE AKTARMIYOR

`qa_index.py` kova atamalarını **envanterden yeniden hesaplıyor**. Gerekçe:
üreteç yanlış hesaplarsa indeks de özet de **aynı yanlışı** taşır ve dosya
kendi içinde **tutarlı görünür**.

---

## 21 · KÜLTÜREL DENGE

| | Faz 4 | **Faz 5** |
|---|---:|---:|
| Kapsamdaki kültür | 71 | **73** |
| Manuscript'teki kültür | 14 | **14** |
| Tahtasız aile kültür | 11 | **13** |
| Tahtasız aile İngiliz madde | 5 | **3** |
| Arka madde kültür indeksi | — | **73 kovası** |

Manuscript kültür sayısı **14'te sabit**: çıkan iki madde de İngilizdi ve
İngilizce başka maddelerle (hopscotch, conkers, fox-and-geese) temsil
edilmeye devam ediyor.

---

## 22 · AİLE DENGESİ

| aile | hedef | kilitli | yazılmış | erişilebilir · yazılmamış |
|---|---:|---:|---:|---:|
| Ekim | 14 | 14 | 1 | 12 |
| Av-kuşatma | 10 | 10 | 3 | 7 |
| Eve dönüş | 15 | 15 | 4 | 10 |
| Çizgi-toprak | 14 | 14 | 4 | 9 |
| Savaş tahtası | 17 | 17 | 3 | 14 |
| Şans | 15 | 15 | 1 | 12 |
| **Tahtasız** | **15** | **15** | **4** | **8** |
| **Toplam** | **100** | **100** | **20** | **72** |

Yedi ailenin **yedisi** manuscript'te temsil ediliyor.

---

## 23 · MANUSCRIPT KORUMASI

| | |
|---|---:|
| Takip edilen manuscript dosyası | **0** |
| Takip edilen arka madde | **0** (yalnızca public özet) |
| Takip edilen Türkçe pilot metni | **0** |
| Ticari katmanda Türkçe | **0** |
| Sızıntı fikstürü | 5 · hepsi beklendiği gibi |

`git ls-files 02_MANUSCRIPT/` yalnızca `.gitkeep` ve `README.md` döndürür.
Yeni üretilen `backmatter.json` ve `retired_phase5.json` de korumalı
katmandadır.

### 23.1 CI'da azalan kapsama — bilinen ve kabul edilen

`07_ASSETS/diagrams/**` yok sayıldığı için CI'da **yalnızca** `pilot` ve
`phase3` diyagram kayıtları görünür; `phase4_diagrams.json` görünmez.
`qa_diagram` CI'da **16 diyagram** denetler, yerelde **25**. Aynı şekilde
`qa_index` CI'da **public özeti** (5 denetim), yerelde **tam arka maddeyi**
(31 denetim) denetler.

Bu bir kusur değil bir **takas**tır (A1) ve körlüğü `selftest` kapatır.

---

## 24 · CI VE GİT

| | |
|---|---|
| Dal | `faz/5-yakinsama` |
| Commit | 5 |
| CI | ✅ **YEŞİL** — ama bir kez KIRMIZI yandı (§ 24.2) |
| Açık gereksiz PR | **yok** |
| `.gate` | **`phase1`** — yükseltilmedi |

### 24.1 CI BİR KEZ KIRMIZI YANDI — ve sebebi bu fazın kendi kusuruydu

Dördüncü push'ta CI kırmızı yandı. Sebep, § 14.6'da eklediğim **bayatlık
denetiminin kendisiydi**: `07_ASSETS/diagrams/**` korumalı katmandadır ve
CI'da yalnızca `pilot` ile `phase3` kayıtları görünür. Denetim, görünmeyen
her tanımı **hayalet** sayıp **doğru** bir ölçümü kırmızı yaktı.

> Kapının öğrettiği ders kapının kendisine uygulandı: **eksik veriyle koşan
> bir denetim, denetlediğini sanıp başka bir şeyi denetler.**

Daha kötüsü, aynı koşuda benim yeni kasıtlı kusur testim **yanlış sebeple
geçiyordu** — kapı zaten kırmızıydı, yani mutasyon sınanmamıştı. § 14.7'nin
`--root` kusuruyla **aynı sınıf**, aynı fazda **ikinci kez**.

**Düzeltme:** denetim manuscript yereldeyse **tam**, CI'da **açıkça boş**
koşuyor (`qa_manuscript` ile aynı sözleşme) ve selftest testi de aynı
koşula bağlandı. Temiz bir klonda CI koşulları **yeniden üretilerek**
doğrulandı: `qa_diagram` 30 · `qa_index` 5 · `selftest` 157 — hepsi yeşil.

Kurucu § 33 *"CI RED → STOP. Fix. Test. Push. Wait."* diyordu ve aynen
uygulandı: merge **CI yeşile dönene kadar yapılmadı**.

### 24.2 Bir düzeltme: `v0.4.0` etiketi YOKTU

Faz 4 raporu kilometre taşı olarak `v0.4.0` etiketini yazıyordu. Faz 5
denetledi: **ne yerelde ne uzakta böyle bir etiket var**
(`git ls-remote --tags origin` boş döner). Faz 3'ün `v0.3.0`'ı da yok.

> Bir rapor bir etiketi **yazmakla** oluşturmuş olmaz. Kurucu § 33
> *"Verify; do not assume"* diyordu ve doğru çıktı.

---

## 25 · RESMÎ KAPI DURUMU — A10

```
PRODUCTION        : AUTHORIZED
FORMAL VALIDATION : PENDING
```

| | durum |
|---|---|
| Faz 5 üretim işi | ✅ **YETKİLİ** (A10 Founder Override) |
| Resmî faz kapısı | ⛔ **AÇILMADI — `.gate` = `phase1`** |

### EXTERNAL PLAYTEST: **NOT PERFORMED**

| | |
|---|---:|
| Dış (insan) oynanabilirlik testi | **0** |
| İç (ajan) test kaydı | **0** |
| `locked` oyun | **0** |
| Uydurulmuş testçi / süre / puan | **0** |

`01_SOURCE/playtests/` **hâlâ boştur**. A10 Override üretimi
**durdurmamak** demektir; **kanıt uydurmak** demek değildir.
`qa_manuscript.py § ⑤` kaydı olmayan bir `locked` maddeyi mekanik olarak
reddediyor ve `selftest` bunu her koşuda sınıyor.

---

## 26 · KALAN BLOKLAYICILAR

| # | blok | kimde | değişti mi |
|---|---|---|---|
| 1 | **Dış insan oynanabilirlik testi** | kurucu — paket hazır | ⛔ Faz 2'den beri aynı |
| 2 | **80 oyun yazılmadı** | üretim | ⛔ **Faz 5'in başarısızlığı** |
| 3 | Telifli kaynak erişimi | kurucu | 5 oyun (değişmedi) |
| 4 | **cats-cradle · 150 mm çatışması** | kurucu | 🆕 **açık karar** |
| 5 | **lagori · kho-kho kaynak kaydı** | araştırma | 🆕 P6 |
| 6 | ~~Tahtasız kültür dengesi + gonggi/fivestones~~ | — | ✅ **ÇÖZÜLDÜ (K23)** |
| 7 | ~~Arka madde~~ | — | ✅ **ÇÖZÜLDÜ** |
| **A4** | Büyük punto sürümü | kurucu | **açık** |
| **A5** | `STYLE.md` onayı | kurucu | **açık** |
| **A6** | Yazar biyografisi | kurucu | Faz 5'te isteniyordu, **açık** |

---

## 27 · FAZ 6 HAZIRLIĞI

**Faz 6'ya GEÇİLMEDİ ve geçilmeyecek.**

| hazır | değil |
|---|---|
| Kapsam **kilitli + şerhli + denetlenen** (100 · 73 kültür) | **80 oyun yazılmadı** |
| **Arka madde tam** · üç indeks üretilip doğrulandı | **Dış test kanıtı (0)** |
| Kalibre sayfa modeli (260 · +%1,6) | `locked` oyun (0) |
| Ekonomik model güncel (8,37 $ / 10,92 $) | Ön madde ve giriş denemesi yazılmadı |
| 172 kasıtlı kusur testi · 6 yeni kapı kusuru kapatıldı | ~130 görsel üretilmedi |
| Erişilebilir-önce kuyruk · 6 seviye · 92 erişilebilir | Telifli kaynak erişimi |

### 27.1 Roadmap'in Faz 5 tanımıyla farkı

Roadmap'in Faz 5'i *"editoryal yakınsama + görsel üretim"*tir ve **yeni
oyun yazılmaz** der. Kurucunun Faz 5 talimatı ise **bir üretim fazıdır**
(20 → 100). İkisi **aynı fazın adını** taşıyor ama **farklı iş** istiyor.

Bu rapor **kurucunun talimatını** ölçüt aldı ve ona göre **başarısız**
sayıyor.

---

## 28 · BU FAZIN KENDİ HAKKINDA BİLMEDİĞİ

| bilinmeyen | ne zaman öğrenilir |
|---|---|
| Yirmi madde masada çalışıyor mu | **dış test** — açık |
| Kalan 80 oyunun kaçı gerçekten yazılabilir | sıraya geldikçe · Faz 5 beşte beş **yazılamaz** buldu |
| Taşma oranı %5'te kalıyor mu | daha büyük örneklem |
| cats-cradle 150 mm'ye sığdırılabilir mi | kurucu kararı |
| Üç indeks POD baskıda kullanışlı mı | prova kopya |
| 70 "denenmemiş" oyunun kaçı kural taşıyan kaynağa bağlı | sıraya geldikçe |

İkinci satır bu fazın en rahatsız edici bulgusudur. **Beş oyunun kaynağı
açıldı; beşi de yazılamaz çıktı.** Örneklem küçük, ama küçük olması onu
yok saymanın gerekçesi değildir: eğer bu oran devam ederse, "erişilebilir"
sayılan 92 oyunun önemli bir bölümü **kural taşımayan kaynaklara**
bağlıdır ve gerçek üretim kapasitesi kuyruğun gösterdiğinden **düşüktür**.

> Faz 3 engeli **abarttı**, Faz 4 **küçümsedi**, Faz 5 ise engelin
> **türünü** yanlış bildiğimizi buldu.

---

**⛔ FAZ 6 BAŞLAMADI.** `.gate` = `phase1`. KDP'ye dokunulmadı. Ajan durdu.
