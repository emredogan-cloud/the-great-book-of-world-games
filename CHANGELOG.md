# CHANGELOG — The Great Book of World Games

Bu dosya **ne zaman ne değişti ve neden** sorusunu yanıtlar.
Her faz kendi girdisini ekler. Format: ters kronolojik.

---

## [0.2.0] — 2026-08-13 · FAZ 2 · Pilot, sayfa doğrulaması, diyagram dili, dizgi

> Faz 2 bir üretim fazı değil bir **ölçüm** fazıdır. Ürettiği en değerli
> şey üç sayı ve üç hayırdır. **Faz KISMEN tamamdır** ve `.gate` `phase1`
> olarak kaldı: 12 `locked` oyun isteyen kapı, sıfır kilitli oyunla açılamaz.

### Kurucu kararları kapandı
- **K12 · A1** — manuscript public olmaz, iş durmaz; koruma güçlendirildi
- **K13 · A2** — av-kuşatma 14→10, savaş tahtası 13→17 (toplam 100)
- **K14 · A3** — nihai 100 oyun `scope_lock.json` içinde KİLİTLİ
- **K15 · A7** — dış testçi var; iç kanıt dış kanıtın yerine geçmez
- **K16** — ticari dil İngilizce, Türkçe yalnızca test malzemesi
- **K17** — sayfa doğrulaması bir etiket değil bir KAYITTIR

### Ölçülenler
- **kelime/sayfa 389** (Faz 1 hipotezi 320 · %18 düşüktü)
- **metin 1,37 sayfa/oyun ve SABİT** (oyunlar arası fark 0,01)
- **diyagram 0,45 sayfa/oyun ve DEĞİŞKEN** (fark 0,55)
- → **sayfa bütçesi bir KELİME bütçesi değil, bir DİYAGRAM bütçesidir**
- sayfa modeli 250 → **316** (+%23,4); hedef DEĞİŞTİRİLMEDİ, şerhle belgelendi
- birim telif her sürümde **1,12 $ düşüyor**

### Bulunan kusurlar
- **GERÇEK SIZINTI:** altı oyunun tam İngilizce kural metni public depodaydı.
  Faz 1 dedektörü göremezdi (etiket taşımıyordu). Korumalı katmana taşındı.
- Diyagram dili kendi genişlik sınırını aşıyordu → v1.1 (dikey panel)
- Dil kapısı tek Türkçe cümleyi kaçırıyordu → iki eşikli ölçüt
- `tablut`/`patolli` üç indeksten sessizce düşerdi → alanlar dolduruldu
- **selftest kendi regresyonumu yakaladı** (page_budget kalibre modu)

### Yeni kapılar
`validate_scope.py` · `qa_diagram.py` · `qa_playable.py` ·
`qa_language_split.py` · `calibrate_pages.py` · `render_diagrams.py`
Selftest **85 → 117** denetim. CI metin kapılarını artık **tarayarak**
koşuyor — elle liste tutmak bir körlük kaynağıydı.

### YAPILMAYANLAR — açıkça
- **Dış oynanabilirlik testi: SIFIR.** Paket hazır, oturum yapılmadı.
  Sahte kayıt üretilmedi.
- **Sayfa doğrulaması 2/12 tam.** Telifli monografilere erişilemedi.
- **Yazılan oyun: 3/12.** Dokuzunda kaynak kural metnini vermiyor; uydurulmadı.

## [0.1.0] — 2026-08-13 · Faz 1 · Envanter, tasnif ve oynanabilirlik mimarisi

Kitabın **veri omurgası** kuruldu. **Hiçbir proza yazılmadı.**

### Eklendi

- **`01_SOURCE/games/family-*.json`** — yedi aile parçası, **160 oyun
  kaydı**. Elle yazılır; indeks bunlardan üretilir
- **`01_SOURCE/game_index.json`** — birleştirilmiş envanter · **ÜRETİLİR**
- **`01_SOURCE/family_index.json`** — yedi mekanik aile; her biri tanım,
  giriş kuralı, dışlama kuralı ve **sınır kuralı** taşır. Ayrıca
  **deterministik tasnif yordamı**: sabit sıralı yedi soru
- **`00_CONTEXT/EDITORIAL_ARCHITECTURE.md`** — kitabın yapısı, iki sayfalık
  madde mimarisi, sayfa modeli, yedi görsel tipi, arka madde ve üç indeks,
  **sekiz ölçütlü aday seçim modeli**
- **`04_BUILD/build_index.py`** — parça → indeks; `--check` ile üretilen
  artefakt tutarlılığı
- **`04_BUILD/qa_taxonomy.py`** — aile tanımı, sınır, kısıt taraması, denge
- **`04_BUILD/qa_rules.py`** — kural bütünlüğü, netlik, durum tutarlılığı
- **`04_BUILD/validate_research.py`** — künye, yasaklı kaynak, bağımsızlık,
  araştırma → yazım kilidi
- **`04_BUILD/score_candidates.py`** — seçim modeli + **yeniden dengeleme
  önerisi**
- **`04_BUILD/page_budget.py`** · **`editions.py`** — sayfa ve telif modeli
- **`04_BUILD/update_docs.py`** — `BOOK_STATS.md` ve `ROADMAP_PROGRESS.md`
  artık **üretilir**; `--check` bayatlığı CI'da kırmızı yakar
- **JSON Schema doğrulayıcı** — `validate_spec.py` içinde, stdlib ile
  (karar K7). Desteklenmeyen şema anahtarı da ayrıca taranır
- **`05_TESTS/selftest.py` § ⑤** — Faz 1'in sekiz kapısının her biri
  kusurlu kurguyla sınanır. Toplam **83 denetim**
- **`06_REPORTS/PHASE_1_REPORT.md`** — faz raporu

### Değişti

- **`01_SOURCE/game.schema.json`** — aday seviyesi araştırma alanları:
  `taxonomyRationale` · `ruleCompleteness` · `clarity` · `playabilityStatus`
  · `reconstructionPlan` · `sourceVerification` · `sources[].lineage` ·
  `scores` · `visualNeeds` · güvenlik ve uyarlama alanları
- **`project_config.json`** — `production.pageModel` bloğu; Kindle telif
  oranı ve dosya boyutu hipotezi
- **`04_BUILD/qa_all.sh`** — envanter tazeliği **en başta** koşar
- **`.gate`** → `phase1`

### Ölçülen

153 aday · **119 uygun** · 89 kültür · 34 bölge · 7 aile ·
kısıt taraması **160/160** · 300 kaynak künyesi · sayfa modeli **250**
(hedef 256, −%2,3) · selftest **83 denetim yeşil**

### Bulgular

- **Kapsam bulgusu:** av ve kuşatma ailesinde yalnızca **10 uygun aday**
  var (hedef 14). Yeniden dengeleme **önerildi**, karar kurucuya bırakıldı
- **Şema iki kez kırıldı:** `gameId` kalıbı iki harfli "go"yu reddediyordu;
  `reconstructed` etiketi beyansız kurguya izin veriyordu
- **Pilot sekiz aşırı uzun kural adımı buldu** ve şablonu düzeltti
- **Otuz iki oyunun kuralı eksik ve TAMAMLANMADI** — dokuzunda kural hiç yok

### Kararlar

K9 (veri/proza sınırı mekaniktir) · K10 (beyansız yeniden kurgulama yok) ·
K11 (kaynak doğrulaması iki seviyeli)

### Durum

`.gate` = `phase1` · **Faz 1 PASS** · Faz 2 için A1 · A2 · A3 · **A7**
kapanmalı

---

## [0.0.1] — 2026-08-12 · Bootstrap

Proje altyapısı kuruldu. **Hiçbir kitap içeriği üretilmedi.**

### Eklendi

- **Dizin mimarisi** — 24 dizin, `00_CONTEXT` … `09_ARCHIVE` şemasına uygun,
  bu projeye özgü eklerle: `01_SOURCE/games`, `01_SOURCE/playtests`,
  `07_ASSETS/diagrams`
- **`project_config.json`** — makine okunur tek doğruluk kaynağı. Pazar
  raporunun sayıları `scope.locked: false` ile **hipotez** olarak işaretlendi
- **`THE_GREAT_BOOK_OF_WORLD_GAMES_IMPLEMENTATION_ROADMAP.md`** — altı faz,
  her fazda 19 alan: amaç, kapsam, teslimatlar, yazım hedefi, kelime/sayfa
  hedefi, araştırma, test altyapısı, QA kapıları, DoD, PASS, FAIL, ajan
  notları, kurucu bağımlılıkları, git kilometre taşı, CI, çıktılar, riskler,
  faz devri
- **`00_CONTEXT/PLAYABILITY_STANDARD.md`** — bu kitabın benzersiz başarısızlık
  biçimine (*oyun çalışmıyor*) karşı kurulan sözleşme: sekiz bloklu kural
  şablonu, üç zorunlu edge case, insan testçi kuralı
- **`00_CONTEXT/SOURCING_STANDARD.md`** — iki bağımsız kaynak kuralı ve
  dört durumlu kısıt taraması (`open` / `attributed` / `restricted` / `excluded`)
- **`00_CONTEXT/STYLE.md`** v1.0 — iki ayrı kayıt (anlatı / talimat),
  yasak kalıplar, belirsizliğin gizlenmemesi kuralı
- **`00_CONTEXT/LESSONS_FROM_CODEX.md`** — iki referans projeden taşınan
  yedi mekanizma ve altı ders; **kod taşınmadı, disiplin taşındı**
- **`01_SOURCE/game.schema.json`** — oyun kaydı şeması; `rules` ve
  `playtests` blokları `locked` durumu için zorunlu
- **Test altyapısı** — `validate_spec.py` (veri + kapsam + kapı),
  `validate_structure.py` (dosya + gömülü değer + sızıntı + sır),
  `selftest.py` (**kapıların kendi testi**, dört bölüm)
- **`04_BUILD/qa_all.sh`** — CI'ın birebir aynısı; Faz 1–5'te doğacak
  kapılar için satırlar şimdiden yazıldı (K18 dersi: ölü betik olmasın)
- **`.github/workflows/validate.yml`** — altı iş: gate · data · structure ·
  gates-selftest · text · production-model
- **`.gitignore`** — iki hatlı manuscript koruması

### Kararlar

K1 (ortak kütüphane yok) · K2 (`.gate`) · K3 (siyah-beyaz iç blok) ·
K4 (ciltli öncelikli) · K5 (kumar çerçevesi yok) · K6 (KU'ya girilmez) ·
K7 (kapılar üçüncü taraf paket kullanmaz) · K8 (kapsam sayıları hipotez)

### Açık kararlar

A1 (manuscript politikası · **Faz 1 başlamadan**) · A2 (aile taksonomisi) ·
A3 (100 oyun listesi) · A4 (büyük punto) · A5 (STYLE onayı) ·
A6 (yazar biyografisi) · A7 (**oyun testçileri · Faz 2 bloklayıcısı**)

### Durum

`.gate` = `phase0` · **Faz 1 BAŞLAMADI** · kurucu onayı bekleniyor
