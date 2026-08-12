# CHANGELOG — The Great Book of World Games

Bu dosya **ne zaman ne değişti ve neden** sorusunu yanıtlar.
Her faz kendi girdisini ekler. Format: ters kronolojik.

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
