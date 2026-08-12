# THE GREAT BOOK OF WORLD GAMES — UYGULAMA YOL HARİTASI

> **Bu belge tek doğruluk kaynağıdır.** Altı faz, kapılar, testler, DoD.
> Bir ajan bu dosyayı altı ay sonra açtığında ne yapacağını, hangi sırayla
> yapacağını, neyin PASS neyin FAIL olduğunu buradan öğrenir.
>
> Sürüm: **1.0 · bootstrap** · Tarih: **12 Ağustos 2026** · Kapı: `phase0`
> Depo: `emredogan-cloud/the-great-book-of-world-games`
>
> **Bu proje diğer iki yeni projeden ve iki Codex cildinden TAMAMEN İZOLEDİR.**
> Ortak dosya, ortak build çıktısı, ortak `.gate`, ortak rapor yoktur.
> Codex projeleri yalnızca **referans uygulama** olarak okunmuştur:
> [`00_CONTEXT/LESSONS_FROM_CODEX.md`](00_CONTEXT/LESSONS_FROM_CODEX.md)

---

## 0 · Bu kitap nedir, neden bu kitap

**The Great Book of World Games** — insanlığın 5.000 yıllık oyun mirasını,
bölgeye göre değil **mekaniğe göre** tasnif eden, kaynak künyeli, oynanabilir
bir başvuru cildi.

Pazar gerekçesi tek cümlede: 2026'nın ilk yarısında yetişkin kurgu-dışının
**16 alt kategorisinden yalnızca ikisi büyüdü** ve biri
**el işi / hobi / antika / oyun (+%9,6)**. Aynı dönemde Circana ekransız
kümenin tamamında büyüme ölçüyor. Rafta ise iki kutup var — akademik oyun
tarihi (otoriter, oynanamaz) ve jenerik aile oyunu listeleri (9,99 $,
içeriksiz). **Arada hiçbir şey yok.**

Kaynak: `AMAZON-KDP-2026-MARKET-OPPORTUNITY-REPORT.html` § 8 · WS-1 ve § 11 · Kitap A.

| | |
|---|---|
| Fırsat skoru | **8,6 / 10** — portföyün en yükseği |
| Sıra | **#1 · ilk yazılacak kitap** |
| Ciltli birim telif (hipotez) | **10,99 $** · başabaş ACOS %31,4 |
| AI hendeği | **9 / 10** |
| Üretim zorluğu | 7 / 10 |

---

## 1 · BU KİTABIN BENZERSİZ BAŞARISIZLIK BİÇİMİ

Her kitabın kendine has bir ölüm biçimi vardır. World Myths'inki
*yaş uygunluğuydu*. Bestiarium'unki *illüstrasyon tutarlılığıydı*.

**Bu kitabınki tektir ve acımasızdır:**

> ## OYUN ÇALIŞMIYOR.

Bir okur kitabı açar, masaya oturur, kuralları okur ve **oynayamaz**.
Kural eksiktir, çelişkilidir, berabere durumunu tanımlamamıştır ya da
tahta diyagramı kuralla uyuşmuyordur.

Bu tek kusur, kitabın alt başlığındaki vaadi — *"Ready to Play Tonight"* —
doğrudan yalanlar. Ve o yorumu silemezsiniz.

**Bu yüzden bu projede oynanabilirlik bir ek denetim değil, birinci sınıf
bir sistemdir ve CI'da kapısı vardır.** Faz 1 ve Faz 2 bu mimariyi kurar;
Faz 3'ten sonra tek bir oyun bile test edilmeden `locked` olamaz.

Öncelik sırası — çakışma olduğunda yukarıdaki kazanır:

1. **Oynanabilirlik** — kural metniyle oyun gerçekten oynanıyor mu
2. **Kültürel doğruluk ve kısıt taraması** — yaşayan/kutsal gelenek eğlenceye çevrilmez
3. **Kaynak izlenebilirliği** — oyun başına ≥2 bağımsız kaynak
4. **Diyagram doğruluğu** — tahta, kuralla birebir uyuşur
5. **Okunabilirlik ve anlatı keyfi**
6. **Sayfa / kelime bütçesi**
7. **Üretim hızı**

**Sayfa sayısı hiçbir zaman ilk dördünü ezmez.**

---

## 2 · Altı faz · tek bakışta

| Faz | Ad | Yazım | Kapı | Dal |
|---|---|---|---|---|
| **1** | Envanter, tasnif ve oynanabilirlik mimarisi | **yok** | `phase1` | `faz/1-envanter` |
| **2** | Pilot: 12 oyun + oynanabilirlik kalibrasyonu | ~7.800 kelime | `phase2` | `faz/2-pilot` |
| **3** | Üretim bloğu I — Aileler I–IV | ~28.000 kelime | `phase3` | `faz/3-blok-1` |
| **4** | Üretim bloğu II — Aileler V–VII + arka madde | ~29.000 kelime | `phase4` | `faz/4-blok-2` |
| **5** | Editoryal yakınsama + diyagram/levha üretimi | ~13.000 kelime | `phase5` | `faz/5-yakinsama` |
| **6** | Nihai üretim + KDP paketi | **yok** | `release` | `faz/6-uretim` |

**Faz 4 sonunda manuscript ÖZÜNDE TAMAMDIR.** Faz 5 yakınsama ve üretim,
Faz 6 format ve paket. Faz 6'da yeni içerik yazılmaz — yalnızca bir üretim
kusuru gerektirirse.

---

# FAZ 1 — ENVANTER, TASNİF VE OYNANABİLİRLİK MİMARİSİ

### 1. Faz amacı
Kitabın **veri omurgasını** kurmak ve pazar raporunun sayılarını
(100 oyun · 45 kültür · 7 aile · 256 sayfa) **doğrulamak veya değiştirmek**.
Bu fazda tek bir cümle proza yazılmaz.

### 2. Kapsam
- ≥140 oyun adayı envanteri (100'lük hedefin %40 fazlası — düşenler olacak)
- 7 mekanik ailesinin tanımı ve sınır kuralları
- Oyun veri şeması (`game.schema.json`)
- Kaynak standardı ve kısıt tarama çerçevesi
- Oynanabilirlik doğrulama mimarisi
- Sayfa/kelime modeli — **ölçümle, tahminle değil**

### 3. Teslimatlar
| Dosya | Ne |
|---|---|
| `01_SOURCE/game_index.json` | ≥140 aday · şemaya uygun · durum `candidate` |
| `01_SOURCE/game.schema.json` | Oyun kaydı JSON Schema'sı |
| `01_SOURCE/family_index.json` | 7 aile · tanım · sınır kuralı · hedef sayı |
| `00_CONTEXT/EDITORIAL_ARCHITECTURE.md` | Kitabın yapısı, sayfa modeli, blok mimarisi |
| `00_CONTEXT/SOURCING_STANDARD.md` | Neyin kaynak sayıldığı · kısıt taraması |
| `00_CONTEXT/PLAYABILITY_STANDARD.md` | **Oynanabilirlik sözleşmesi** |
| `00_CONTEXT/STYLE.md` | v1.0 → kalibre edilecek (Faz 2) |
| `04_BUILD/validate_spec.py` | Şema + kapsam + kapı doğrulaması |
| `04_BUILD/validate_research.py` | Kaynak künyesi doğrulaması |
| `04_BUILD/qa_rules.py` | Kural bütünlüğü kapısı |
| `04_BUILD/qa_taxonomy.py` | Tasnif kapısı |
| `05_TESTS/selftest.py` | **Kapıların kendi testi** |
| `06_REPORTS/PHASE_1_REPORT.md` | Faz raporu |

### 4. Yazım hedefi
**YOK.** Bu faz araştırma ve mimari fazıdır. `qa_length` boş koşar.

### 5. Yaklaşık kelime hedefi
0 (proza). Belgeler ~12.000 kelime.

### 6. Yaklaşık sayfa hedefi
0 manuscript sayfası. Faz sonunda **sayfa modeli** üretilir:
oyun başına 2 sayfa × 100 + ön madde 14 + arka madde 21 + aile açılışları 14
= **249 sayfa hipotezi** → `06_REPORTS/page-budget.json`.

### 7. Araştırma gereksinimleri
- Her aday oyun için **≥1** kaynak (aday aşaması); `locked` için **≥2 bağımsız**
- Kamusal alan literatürü önceliklidir (Murray, Parlett, Bell, müze envanterleri,
  etnografik derlemeler) — künye zorunlu
- **Kısıt taraması:** her oyun `open` / `attributed` / `restricted` / `excluded`
  etiketini alır. `restricted` = yaşayan veya kutsal gelenek; eğlence
  çerçevesine çevrilemez. `excluded` = kitaba giremez, gerekçe kayıtta kalır.
- Kuralları belirsiz oyunlar `confidence: reconstructed` alır ve prozada
  **açıkça** "yeniden kurgulanmış kural" olarak işaretlenir.

### 8. Test altyapısı
| Betik | Ne denetler |
|---|---|
| `validate_spec.py` | Şema uyumu, kimlik tekilliği, kapsam sayıları, kapı seviyesi |
| `validate_research.py` | Kaynak künyesi var mı, tip geçerli mi, güven seviyesi geçerli mi |
| `qa_taxonomy.py` | Her oyun **tam bir** aileye ait mi; aile dengesi hedeften ne kadar sapıyor |
| `qa_rules.py` | Zorunlu kural alanları dolu mu (bu fazda `candidate` için gevşek) |
| `validate_structure.py` | Depo yapısı, belge bağları, **gömülü sabit değer**, manuscript sızıntısı |
| `selftest.py` | **Kapılar gerçekten ısırıyor mu** |

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase1
```
Hepsi yeşil olmadan faz kapanmaz.

### 10. Definition of Done
- [ ] `game_index.json` ≥140 aday içeriyor ve şemayı geçiyor
- [ ] Her adayın ailesi, kültürü, bölgesi, dönemi, ≥1 kaynağı var
- [ ] 7 ailenin tanımı ve **sınır kuralı** yazılı (bir oyun neden A ailesinde, B'de değil)
- [ ] Kısıt taraması **140/140** tamamlandı, muafiyetsiz
- [ ] `PLAYABILITY_STANDARD.md` onaylı
- [ ] Sayfa modeli üretildi ve `page-budget.json`'a yazıldı
- [ ] `selftest.py` yeşil — her kapı en az bir kusurlu kurguda ısırıyor
- [ ] `06_REPORTS/PHASE_1_REPORT.md` yazıldı
- [ ] CI **YEŞİL**
- [ ] `.gate` → `phase1`

### 11. PASS kriterleri
- ≥140 aday, ≥45 farklı kültür, 7 ailenin **her biri** ≥16 aday taşıyor
- Kısıt taraması tam; `restricted` ve `excluded` gerekçeli
- Sayfa modeli hedeften **±%6** içinde
- `selftest.py` 0 hata

### 12. FAIL kriterleri
- Aday sayısı <140 → **kapsam gerçekçi değil, hedef düşürülür veya araştırma sürer**
- Bir aile <16 aday → **tasnif tezi zayıf; aile birleştirilir veya değiştirilir**
- Farklı kültür sayısı <45 → **alt başlık yalan söyler; sayı düşürülür**
- Kısıt taraması eksik → faz **kapanamaz**, muafiyet yok
- Sayfa modeli hedeften >%6 sapıyor → kapsam veya trim yeniden hesaplanır

> **Bu FAIL'ler proje ölümü değildir.** Bunların hepsi *hipotez düzeltmesidir* ve
> Faz 1'in varlık sebebi tam olarak budur. Bir sayıyı burada düzeltmek ucuz;
> Faz 4'te düzeltmek üç aylık iştir.

### 13. Ajan öz-notları
- Pazar raporunun sayıları **hipotezdir**. `project_config.json § scope.locked`
  `false`tur ve bu fazın sonunda `true` olur. Sayıyı savunmak zorunda değilsin;
  **ölçmek** zorundasın.
- Aile sınır kuralı en zor iştir. "Tavla ailesi" ile "yarış oyunları" nerede
  ayrılır? Bu kararın gerekçesi `family_index.json` içinde durur, kafanda değil.
- Kısıt taramasını sona bırakma. Bir oyunun `excluded` olduğunu 130. adayda
  öğrenmek, ona harcanan araştırmayı çöpe atar.

### 14. Kurucu bağımlılıkları
| # | Ne | Ne zaman |
|---|---|---|
| A1 | Manuscript public depoda mı duracak? (bootstrap varsayımı: **hayır**) | **Faz 1 başlamadan** |
| A2 | 7 aile taksonomisi onayı | Faz 1 sonu |
| A3 | 100 oyunun nihai listesi onayı | Faz 1 sonu |
| A4 | Büyük punto sürümü v1.0'a girecek mi | Faz 4 |

### 15. Git kilometre taşı
```
dal:     faz/1-envanter
etiket:  v0.1.0
commit:  "faz 1: oyun envanteri, tasnif ve oynanabilirlik mimarisi"
```

### 16. CI gereksinimleri
`validate.yml` yeşil: `gate` · `data` · `structure` · `gates-selftest` ·
`production-model` · `generated`. `text` işi bu fazda **boş koşar**
(manuscript yok) — körlüğü `selftest` kapatır.

### 17. Beklenen çıktılar
`game_index.json` · `family_index.json` · `game.schema.json` ·
`page-budget.json` · `spec-validation.json` · `research.json` ·
`PHASE_1_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| 45 farklı kültür bulunamaz | Aday havuzu 140; kültür çeşitliliği aday seçiminde birinci ölçüt |
| Kural kaynakları çelişiyor | `confidence: reconstructed` + prozada açık etiket; çelişki kayıtta durur |
| Bir aile zayıf çıkar | Faz 1'in işi bunu bulmaktır; aile birleştirme Faz 1'de ucuz |
| Kısıt taraması bir oyunu geç eler | Tarama araştırmanın **ilk** adımıdır, son adımı değil |

### 19. Faz devri
Faz 2'ye girmek için: `.gate` = `phase1`, CI yeşil, A2 ve A3 kapalı.
Faz 2, Faz 1'in kilitlediği envanterden **12 pilot oyun** seçer —
her aileden en az bir tane, ve **en zor** olanlardan.

---

# FAZ 2 — PİLOT: 12 OYUN + OYNANABİLİRLİK KALİBRASYONU

### 1. Faz amacı
Yazım kurallarını, kural metni şablonunu, diyagram dilini ve **oynanabilirlik
testini** 12 oyunda kalibre etmek. Bu faz bir üretim fazı değil, bir
**ölçüm fazıdır**.

### 2. Kapsam
7 aileden 12 oyun. Seçim ölçütü **kolay olanlar değil, zor olanlar**:
- her aileden ≥1
- ≥2 tanesi `confidence: reconstructed`
- ≥1 tanesi tahtasız (diyagramsız anlatım testi)
- ≥1 tanesi asimetrik (en karmaşık kural yapısı)
- ≥1 tanesi 5+ oyunculu (ölçekleme testi)

> **Neden en zorlar?** Kolay oyunlarla kalibre edilen bir şablon, zor oyunda
> kırılır ve bunu 60. oyunda öğrenirsiniz. Bestiarium dersi: *pilot, en kötü
> durumu örneklemelidir.*

### 3. Teslimatlar
| Dosya | Ne |
|---|---|
| `02_MANUSCRIPT/book.json` | 12 oyun · tam kural metni · **depo dışı** |
| `01_SOURCE/playtests/*.json` | 12+ oynanabilirlik testi kaydı |
| `00_CONTEXT/STYLE.md` v2.0 | **Ölçümle kalibre edilmiş** |
| `00_CONTEXT/DIAGRAM_LANGUAGE.md` | Diyagram notasyonu ve sembol sözlüğü |
| `04_BUILD/qa_playable.py` | Oynanabilirlik kapısı |
| `04_BUILD/qa_length.py` `qa_voice.py` `qa_echo.py` `qa_drift.py` | Metin kapıları |
| `04_BUILD/calibrate_pages.py` | Gerçek dizgiyle sayfa ölçümü |
| `06_REPORTS/PHASE_2_REPORT.md` | **Kalibrasyon raporu** |

### 4. Yazım hedefi
12 oyun · tam kural metni + kültürel hikâye + varyantlar + kaynak künyesi.

### 5. Yaklaşık kelime hedefi
**~7.800** (12 × 650). Bant: 5.760 – 10.800.

### 6. Yaklaşık sayfa hedefi
**~24 sayfa** dizilmiş (12 × 2). Bu ölçüm, 256 sayfalık modelin
**ilk gerçek doğrulamasıdır**.

### 7. Araştırma gereksinimleri
12 oyunun tamamı `locked` seviyesine çıkar: **≥2 bağımsız kaynak**,
kısıt taraması tamam, güven seviyesi atanmış.

### 8. Test altyapısı
Faz 1'in kapıları + yeni metin kapıları + **`qa_playable.py`**:

```
qa_playable.py  →  her `locked` oyun için:
                   · ≥1 playtest kaydı var mı
                   · playtest YALNIZCA kitap metniyle mi yapıldı
                   · sonuç `playable` mi
                   · berabere/kilit/kural-dışı üç edge case cevaplı mı
                   · oyuncu sayısı ve süre ölçülmüş mü
```

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase2
```

### 10. Definition of Done
- [ ] 12 oyun yazıldı, şemaya uygun, `locked`
- [ ] **12/12 oynanabilirlik testi geçti** — kitap metniyle oynandı
- [ ] Üç edge case (berabere · kilit · kural dışı) 12/12 cevaplı
- [ ] `STYLE.md` ölçümle güncellendi
- [ ] Diyagram dili tanımlandı, 12 diyagram taslağı üretildi
- [ ] Gerçek dizgi ölçümü yapıldı → sayfa modeli güncellendi
- [ ] `selftest.py` yeni kapıları da kapsıyor
- [ ] CI **YEŞİL** · `.gate` → `phase2`

### 11. PASS kriterleri
- 12/12 oyun oynanabilir
- Kelime ortalaması 480–900 bandında
- Ölçülen sayfa/oyun **2,0 ± 0,25**
- Kural metni cümle ortalaması ≤22 kelime

### 12. FAIL kriterleri
- **≥2 oyun oynanamıyor** → kural şablonu bozuk. **ŞABLONU DÜZELT, oyunları zorlama.**
- Sayfa/oyun >2,5 → 100 oyun 256 sayfaya sığmaz; kapsam veya tasarım değişir
- Kelime ortalaması banttan taşıyor → hedef yeniden hesaplanır

> **Bu fazın en önemli kuralı:** pilot bozuk bir yazım kuralını açığa
> çıkarırsa **KURALI DÜZELT**. Sonraki 88 oyunu bozuk kurala uydurmak,
> hatayı sekiz katına çıkarmaktır.

### 13. Ajan öz-notları
- Oynanabilirlik testini **sen yapamazsın**. Testçi insandır ve yalnızca
  kitaptaki metni okur. Test kaydı olmadan `locked` yok.
- Diyagram dilini burada dondur. 60. oyunda notasyon değiştirmek, önceki
  59 diyagramı geçersiz kılar.
- Kural metni bir dilbilgisi işi değil, bir **kullanılabilirlik** işidir.
  Güzel cümle kuramazsan sorun değil; anlaşılmayan adım sorundur.

### 14. Kurucu bağımlılıkları
| # | Ne |
|---|---|
| — | **2 oyun testçisi** (kurucu bulur; ajan test yapamaz) |
| A5 | Kalibre edilmiş `STYLE.md` onayı |

### 15. Git kilometre taşı
```
dal:     faz/2-pilot
etiket:  v0.2.0
commit:  "faz 2: 12 oyunluk pilot ve oynanabilirlik kalibrasyonu"
```

### 16. CI gereksinimleri
`text` işi artık **gerçek metinle** koşar (yerelde; depoda manuscript yok).
`gates-selftest` `qa_playable`'ı da kapsamalı.

### 17. Beklenen çıktılar
`book.json` (12 oyun) · `playtests/*.json` · `STYLE.md` v2.0 ·
`DIAGRAM_LANGUAGE.md` · `phase2-typeset-measurement.json` · `PHASE_2_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Testçi bulunamıyor | Faz 2 **bloklanır**. Bu, kabul edilen bir bloktur; sahte test kaydı üretilmez |
| Kural şablonu zor oyunda kırılıyor | Pilot zaten en zorları seçti — kırılma **burada** olsun diye |
| Diyagram POD baskıda okunmuyor | Faz 5'te prova; ama notasyon kalınlığı burada muhafazakâr seçilir |

### 19. Faz devri
Faz 3'e girmek için: 12/12 oynanabilir, `STYLE.md` v2.0 onaylı,
sayfa modeli gerçek ölçümle güncel, `.gate` = `phase2`.

---

# FAZ 3 — ÜRETİM BLOĞU I · AİLELER I–IV

### 1. Faz amacı
İlk büyük üretim bloğu: dört ailenin tamamı. Pilotun kalibre ettiği şablonun
**ölçekte** çalıştığını kanıtlamak.

### 2. Kapsam
Aileler I–IV: `sowing` · `hunt-siege` · `race` · `territory`
≈ 14 + 14 + 15 + 14 = **57 oyun** (12 pilot dahil → net ~45 yeni)

### 3. Teslimatlar
- `book.json` → 57 oyun
- 57 oynanabilirlik testi kaydı
- 4 aile açılış denemesi (~600 kelime × 4)
- 4 karşılaştırma tablosu
- `06_REPORTS/PHASE_3_REPORT.md`

### 4. Yazım hedefi
45 yeni oyun + 4 aile portresi + 4 karşılaştırma tablosu.

### 5. Yaklaşık kelime hedefi
**~28.000** kümülatif ≈ 35.800.

### 6. Yaklaşık sayfa hedefi
~114 dizilmiş sayfa (57 × 2).

### 7. Araştırma gereksinimleri
57/57 `locked`: ≥2 bağımsız kaynak + kısıt taraması + güven seviyesi.
**Araştırma kilidi:** `research.verified != true` olan hiçbir oyun yazılamaz.

### 8. Test altyapısı
Faz 2'nin tamamı + `qa_crossref.py` (aile ↔ oyun ↔ diyagram eşlemesi) +
`qa_diagram.py` (diyagram gerektiren her oyunun diyagram kimliği var mı).

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase3
```

### 10. Definition of Done
- [ ] 57 oyun yazıldı ve `locked`
- [ ] **57/57 oynanabilirlik testi geçti**
- [ ] 4 aile portresi yazıldı
- [ ] Sürüklenme ölçüldü: pilot ↔ blok I arası fark raporlandı
- [ ] CI **YEŞİL** · `.gate` → `phase3`

### 11. PASS kriterleri
- 57/57 oynanabilir · kelime bandı korunuyor
- `qa_drift` pilot ile blok I arasında **anlamlı sapma** göstermiyor
- Ölçülen sayfa/oyun hâlâ 2,0 ± 0,25

### 12. FAIL kriterleri
- Herhangi bir oyun oynanamıyor → **o oyun `candidate`'a düşer**, yedekle değiştirilir
- Sürüklenme eşiği aşıldı → **ölç, yorumla, sonra düzelt** (§ 12 · sürüklenme disiplini)
- Sayfa/oyun 2,5'i aşıyor → kapsam kararı Faz 4'ten önce alınır

### 13. Ajan öz-notları
- Sürüklenme metriğini **mekanik olarak tatmin etmeye çalışma**. Önce ölç,
  sonra yorumla, sonra düzelt. Metrik için yeniden yazılan proza kötüleşir.
- Yedek oyunlar Faz 1'in 140'lık havuzundan gelir. Bir oyun düşerse
  panik yok — havuz bunun için var.

### 14. Kurucu bağımlılıkları
Oyun testçileri (süregelen). Görsel üretimi **bu fazda gerekmez**.

### 15. Git kilometre taşı
```
dal:  faz/3-blok-1   ·   etiket: v0.3.0
```

### 16. CI gereksinimleri
Tam `validate.yml`. Sürüklenme raporu artefakt olarak yüklenir.

### 17. Beklenen çıktılar
`book.json` (57) · `qa-drift.json` · `qa-crossref.json` · `PHASE_3_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Oyun testi darboğaz olur | Test **yazımla paralel** yürür, sonuna bırakılmaz |
| Aynı mekanik tekrar ediyor gibi okunuyor | `qa_echo` tekrar taraması + aile portrelerinde bilinçli karşıtlık |

### 19. Faz devri
Faz 4: kalan üç aile + arka madde. Faz 3 kapanmadan başlamaz.

---

# FAZ 4 — ÜRETİM BLOĞU II · AİLELER V–VII + ARKA MADDE

### 1. Faz amacı
**Manuscript'i özünde tamamlamak.** Faz 4 sonunda kitabın bütün içeriği vardır.

### 2. Kapsam
Aileler V–VII: `war-board` · `chance` · `boardless` = **43 oyun**
\+ arka madde: tahta şablonları · malzeme rehberi · sözlük · kaynakça · **üç indeks**

### 3. Teslimatlar
- `book.json` → **100 oyun**
- 100 oynanabilirlik testi kaydı
- 3 aile portresi + 3 karşılaştırma tablosu
- Arka madde: 12 tahta şablonu · malzeme rehberi · 60 terimlik sözlük ·
  oyun başına kaynak künyesi · **kültüre / oyuncu sayısına / süre-yaşa göre üç indeks**
- `06_REPORTS/PHASE_4_REPORT.md`

### 4. Yazım hedefi
43 oyun + 3 aile portresi + arka maddenin tamamı.

### 5. Yaklaşık kelime hedefi
**~29.000** · kümülatif **~65.000** (hedef 78.000'in %83'ü; kalan Faz 5'te
ön madde ve girişle tamamlanır).

### 6. Yaklaşık sayfa hedefi
~200 gövde + 21 arka madde = **~221**.

### 7. Araştırma gereksinimleri
100/100 `locked`. **Kısıt taraması 100/100 muafiyetsiz.**
`chance` ailesi özel dikkat ister: kumar çerçevesi kullanılmaz, bahis
mekaniği puanla yeniden yazılır (K5).

### 8. Test altyapısı
Tam kapı seti + `qa_index.py` (üç indeksin bütünlüğü: her oyun üç indekste de
doğru yerde mi).

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase4
```

### 10. Definition of Done
- [ ] **100 oyun yazıldı ve `locked`**
- [ ] **100/100 oynanabilirlik testi geçti**
- [ ] 7 aile portresi tamam
- [ ] Arka madde tamam · üç indeks üretildi ve doğrulandı
- [ ] Kısıt taraması 100/100 muafiyetsiz
- [ ] **Manuscript özünde tamam**
- [ ] CI **YEŞİL** · `.gate` → `phase4`

### 11. PASS kriterleri
- 100 oyun · 7 aile · ≥45 kültür — **alt başlıktaki üç sayı doğrulandı**
- Toplam kelime 78.000 ± %10
- Sayfa modeli 256 ± %6

### 12. FAIL kriterleri
- Oyun sayısı <100 → **alt başlık değişir** (kurucu kararı) veya havuzdan tamamlanır
- Kültür sayısı <45 → alt başlık değişir
- Sayfa >272 → trim, punto veya kapsam kararı; Faz 5'e taşınmaz

### 13. Ajan öz-notları
- Alt başlıktaki **her sayı doğrulanabilir bir vaattir**, pazarlama süsü değil.
  Kitap 97 oyunla çıkarsa alt başlık yalan söyler. `validate_spec.py` bunu
  kapıya bağlar — World Myths'in `45 hikâye / 22 kültür` disiplininin aynısı.
- Üç indeks bu kitabın **en çok kullanılacak** kısmıdır (ebeveyn "20 dakikalık,
  2 kişilik, 8 yaş" diye arar). Sonuncu iş olarak görme.

### 14. Kurucu bağımlılıkları
| # | Ne |
|---|---|
| A4 | Büyük punto kararı (sayfa sayısı belli olduğunda) |
| — | Oyun testçileri (süregelen) |

### 15. Git kilometre taşı
```
dal:  faz/4-blok-2   ·   etiket: v0.4.0   ·   "manuscript özünde tamam"
```

### 16. CI gereksinimleri
Tam set. `validate_spec.py --gate phase4` kapsam sayılarını **sert** denetler.

### 17. Beklenen çıktılar
`book.json` (100) · üç indeks · `qa-index.json` · `PHASE_4_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Son 43 oyunda kalite düşer | `qa_drift` blok I ↔ blok II karşılaştırması |
| Arka madde sayfa bütçesini patlatır | Arka madde **Faz 1 modelinde** bütçelendi; ölçüm her fazda güncellenir |
| `chance` ailesi kumar çerçevesine kayar | K5 kararı + `qa_voice` yasak kalıp listesi |

### 19. Faz devri
Faz 5'e girmek için manuscript tam, CI yeşil, `.gate` = `phase4`.

---

# FAZ 5 — EDİTORYAL YAKINSAMA + DİYAGRAM VE LEVHA ÜRETİMİ

### 1. Faz amacı
Metni **yakınsamak** (tek ses, tek terminoloji, tek kural dili), görsel
varlıkların tamamını üretmek ve üretim hattını hazırlamak.

### 2. Kapsam
- Ön madde ve giriş denemesi (~13.000 kelime)
- **LINE EDITOR alt-ajanı** — tam manuscript okuması
- ~130 görsel: 100 kurulum/tahta diyagramı + ~30 kültürel gravür açılış levhası
- `IMAGE_PROMPT_LIBRARY.html` üretimi
- İç blok dizgisi · EPUB · metadata paketi

### 3. Teslimatlar
| Dosya | Ne |
|---|---|
| `07_ASSETS/IMAGE_PROMPT_LIBRARY.html` | Kopyalanabilir prompt kütüphanesi |
| `07_ASSETS/raw/` | Kurucunun ürettiği PNG'ler — **SALT OKUNUR** |
| `07_ASSETS/processed/` `print/` `kindle/` `web/` | CLI dönüşümleri |
| `04_BUILD/interior.py` | İç blok PDF üretimi |
| `04_BUILD/epub.py` | Kindle EPUB |
| `04_BUILD/metadata.py` | KDP metadata paketi |
| `06_REPORTS/LINE_EDITOR_REPORT.md` | Alt-ajan bulguları |
| `06_REPORTS/PHASE_5_REPORT.md` | Faz raporu |

### 4. Yazım hedefi
Ön madde · giriş denemesi · yedi aile haritası açıklaması · nasıl-kullanılır.
**Yeni oyun yazılmaz.**

### 5. Yaklaşık kelime hedefi
**~13.000** · kümülatif **~78.000** — hedefe ulaşılır.

### 6. Yaklaşık sayfa hedefi
14 ön madde → toplam **~256**.

### 7. Araştırma gereksinimleri
Yeni araştırma yok. Kaynakça bütünlüğü doğrulanır: 100 oyun × ≥2 kaynak.

### 8. Test altyapısı
Tam kapı seti + görsel hattı:
`asset_inventory.py` (ham varlık envanteri — dosya var mı, bozuk mu,
**doğru oyuna mı bağlı**) · `convert_images.py --check` · `images.py`
(görsel tutarlılığı) · `interior.py --check` · `epub.py --check` ·
`metadata.py --check`

> **Envanter ölçümden ÖNCE koşar.** Yanlış oyuna bağlanmış kusursuz bir
> diyagram bütün kalite kapılarından geçer — World Myths dersi.

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh phase5
```

### 10. Definition of Done
- [ ] Ön madde ve giriş yazıldı
- [ ] **LINE EDITOR raporu alındı ve geçerli düzeltmeler uygulandı**
- [ ] 130/130 görsel üretildi, işlendi, doğru oyuna bağlandı
- [ ] Diyagramlar **kuralla birebir uyuşuyor** (`qa_diagram` sert modda)
- [ ] İç blok PDF üretildi ve ölçüldü — **gerçek sayfa sayısı**
- [ ] EPUB üretildi ve doğrulandı
- [ ] CI **YEŞİL** · `.gate` → `phase5`

### 11. PASS kriterleri
- Gerçek sayfa sayısı 256 ± %6
- Görsel envanteri 130/130 · çözünürlük ≥300 dpi efektif
- Line Editor'ın **bloklayıcı** bulgusu kalmadı

### 12. FAIL kriterleri
- Diyagram ↔ kural uyuşmazlığı → **bloklayıcı**, düzeltilmeden ilerlenmez
- Sayfa sayısı bandı aşıyor → kapak geometrisi geçersiz olur; önce sayfa düzelir
- Görsel eksik → Faz 6'ya taşınmaz

### 13. Ajan öz-notları
- **Line Editor bir alt-ajandır ve körü körüne kabul edilmez.** Bulgularını
  incele, geçerli olanları uygula, reddettiklerini gerekçesiyle raporla.
- Bu kitapta Line Editor'ın özel görevi: **kural netliği ve kaynak kesinliği**.
- Görsel üretimi kurucuya bağlıdır. Kurucu "varlıklar hazır" dediğinde
  CLI hattı devreye girer. **RAW asla üzerine yazılmaz.**

### 14. Kurucu bağımlılıkları
| # | Ne |
|---|---|
| — | **130 görselin GPT Image ile üretilmesi** |
| — | Kapak sanatı yönü onayı |
| A6 | Yazar biyografisi metni (`authorBio` null ise Faz 6 kırmızı) |

### 15. Git kilometre taşı
```
dal:  faz/5-yakinsama   ·   etiket: v0.5.0
```

### 16. CI gereksinimleri
`validate.yml` + `images.yml` + `build.yml` yeşil.

### 17. Beklenen çıktılar
`IMAGE_PROMPT_LIBRARY.html` · işlenmiş varlıklar · iç blok PDF ·
EPUB · `LINE_EDITOR_REPORT.md` · `PHASE_5_REPORT.md`

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Diyagram POD baskıda okunmuyor | Faz 5'te **prova kopya**; notasyon kalınlığı muhafazakâr |
| Görseller geç geliyor | Yazım fazları görsele bağlı değildi — blok yalnızca Faz 5'te |
| Line Editor çok fazla değişiklik öneriyor | Bloklayıcı / öneri ayrımı; yalnızca bloklayıcılar zorunlu |

### 19. Faz devri
Faz 6: format üretimi ve KDP paketi. Yeni içerik yok.

---

# FAZ 6 — NİHAİ ÜRETİM + KDP PAKETİ

### 1. Faz amacı
Yüklemeye hazır dosyaları üretmek ve kurucuya **eksiksiz bir teslim paketi**
vermek. Ajan KDP paneline dokunmaz.

### 2. Kapsam
Ciltli · ciltsiz · Kindle üretimi · kapak geometrisi · A+ varlıkları ·
metadata paketi · teslim kılavuzu · nihai rapor.

### 3. Teslimatlar
| Dosya | Ne |
|---|---|
| `08_OUTPUT/PAPERBACK/` | İç blok PDF + kapak PDF |
| `08_OUTPUT/HARDCOVER/` | İç blok PDF + kapak PDF (case laminate) |
| `08_OUTPUT/KINDLE/` | EPUB + kapak JPG |
| `03_APLUS/` | A+ modülleri |
| `06_REPORTS/tracked/metadata.json` | Denetlenen metadata nüshası |
| `KDP_UPLOAD_PLAYBOOK.md` | Adım adım kurucu kılavuzu |
| `06_REPORTS/FINAL_RELEASE_REPORT.md` | Nihai rapor |

### 4–6. Yazım / kelime / sayfa
**Yeni yazım yok.** Sayfa sayısı **ölçülür ve dondurulur** — kapak sırtı
buna bağlıdır.

### 7. Araştırma gereksinimleri
Yok. Kaynakça dondurulur.

### 8. Test altyapısı
`package_selftest.py` (**paket kapılarının kendi testi**) · `covers.py --check` ·
`aplus.py --check` · `handoff.py --check` · `cover_artwork.py --check`

> **Kapak kapısı iç blok kapısından SONRA koşar:** sayfa sayısı değişirse
> sırt kayar ve eski kapak GEÇERSİZ olur.

### 9. QA kapıları
```bash
./04_BUILD/qa_all.sh release
```

### 10. Definition of Done
- [ ] Üç formatın tamamı üretildi ve doğrulandı
- [ ] Gerçek sayfa sayısı ölçüldü, sırt hesaplandı
- [ ] Kapak geometrisi · bleed · güvenli alan doğrulandı
- [ ] Fontlar gömülü · marjlar geçerli
- [ ] EPUB ve PDF doğrulandı
- [ ] Metadata paketi tam · **`authorBio` dolu** · ISBN stratejisi doğru
- [ ] `KDP_UPLOAD_PLAYBOOK.md` yazıldı
- [ ] CI **YEŞİL** · `.gate` → `release`
- [ ] **AJAN DURUR**

### 11. PASS kriterleri
Bütün üretim kapıları yeşil · teslim paketi eksiksiz · nihai rapor yazıldı.

### 12. FAIL kriterleri
- `authorBio` null → **kırmızı** (World Myths'te KDP bunu reddetti)
- Sahte ISBN → kırmızı
- Sırt hesabı sayfa sayısıyla uyuşmuyor → kırmızı

### 13. Ajan öz-notları
- **KDP paneline dokunma.** Yükleme, Previewer, prova siparişi, fiyat girişi,
  AI beyanı seçimi ve **Publish** kurucunundur.
- Nihai raporu yazdıktan sonra **DUR**.

### 14. Kurucu bağımlılıkları
KDP paneli işlemlerinin tamamı · prova kopya siparişi · yayın kararı.

### 15. Git kilometre taşı
```
dal:  faz/6-uretim   ·   etiket: v1.0.0   ·   "release candidate"
```

### 16. CI gereksinimleri
`validate.yml` + `build.yml` + `release.yml` yeşil.

### 17. Beklenen çıktılar
Yüklemeye hazır üç format · kapaklar · A+ · metadata · playbook · nihai rapor.

### 18. Riskler
| Risk | Azaltma |
|---|---|
| Sayfa sayısı son anda değişir | Faz 5'te donduruldu; Faz 6 yalnızca ölçer |
| KDP metadata reddi | World Myths dersi: yer tutucu metin YASAK |
| Kapak çözünürlüğü yetersiz | Faz 5 prova kopyasında ölçülür |

### 19. Faz devri
**YOK — proje burada biter.** Sonraki adım kurucunundur.

---

## 3 · Sürekli kurallar — her fazda geçerli

### Git akışı
1. Faz dalında çalış (`faz/N-slug`)
2. Yerelde `./04_BUILD/qa_all.sh` — hepsi yeşil olmadan commit yok
3. Commit · push
4. PR aç → `main`
5. **CI'ı bekle. GitHub Actions'ı incele.**
6. **YEŞİL değilse faz ilerlemez.** Teşhis · düzelt · test · push · tekrar
7. Merge · etiketle · `.gate` yükselt

**CI asla atlanmaz.** Kırmızı CI'da hiçbir şey ilerlemez.

### Araştırma → yazım kilidi
`research.verified != true` olan hiçbir oyun prozaya giremez.
`validate_research.py` bunu denetler ve `qa_crossref.py` manuscript ile
envanteri karşılaştırır.

### Public depo / özel içerik
| Public | Korumalı |
|---|---|
| kod · CI · şema · doğrulayıcı · üretim aracı | **oyun prozası** (`02_MANUSCRIPT/*`) |
| belgeler · araştırma künyeleri · ölçüm raporları | ham görseller · kurucu notları |
| aile taksonomisi · indeks önizlemesi | `.env` · kimlik bilgileri |

İki hat: `.gitignore` **yol** kalıplarını yakalar; `validate_structure.py →
check_manuscript_leak()` takip edilen dosyaların **içeriğine** bakar ve
kural metni görürse CI'ı kırmızı yakar. *Politikayı disipline değil
mekanizmaya bağlarız.*

### Sürüklenme disiplini
**Ölç → yorumla → düzelt.** Metriği tatmin etmek için proza yeniden yazılmaz.

### Görsel hattı
`07_ASSETS/raw/` **değişmez**. Dönüşümler `processed/` `print/` `kindle/`
`web/` altına yazar. RAW üzerine asla yazılmaz.

---

## 4 · Bu yol haritasının sahip olmadığı şeyler

Dürüstlük gereği: bu yol haritası aşağıdakileri **bilmiyor** ve
bilmediğini gizlemiyor.

| Bilinmeyen | Ne zaman öğrenilir |
|---|---|
| 45 farklı kültürden 100 oynanabilir oyun gerçekten bulunabilir mi | **Faz 1** |
| 7 ailenin sınırları temiz çizilebilir mi | **Faz 1** |
| Oyun başına 2 sayfa modeli tutuyor mu | **Faz 2** (gerçek dizgi) |
| Kural şablonu asimetrik oyunlarda kırılıyor mu | **Faz 2** (pilot en zorları seçer) |
| Diyagram notasyonu POD baskıda okunuyor mu | **Faz 5** (prova kopya) |
| Gerçek CPC ve dönüşüm oranı | Yayından sonra — **bu yol haritasının kapsamı dışında** |

Pazar raporunun kendi uyarısı burada da geçerlidir: bu kitabın en büyük
belirsizliği, "el işi/hobi/oyun +%9,6" büyümesinin ne kadarının **oyun
kitaplarına** gittiğinin kamuya açık olmamasıdır.
