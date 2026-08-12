# ROADMAP PROGRESS — The Great Book of World Games

<!-- Faz 1'den itibaren 04_BUILD/update_docs.py tarafından ÜRETİLİR -->

> Kapı: `phase0` · Son güncelleme: **12 Ağustos 2026**
>
> Bu dosya şu an **elle yazılmış bootstrap iskeletidir**. Faz 1'de
> `update_docs.py` devreye girer ve buradaki her sayı **ölçülmüş** olur.

---

## Faz durumu

| Faz | Ad | Durum | Kapı | Dal | Etiket |
|---|---|---|---|---|---|
| **0** | Bootstrap | ✅ **TAMAM** | `phase0` | `main` | — |
| **1** | Envanter, tasnif ve oynanabilirlik mimarisi | ⏸ **BAŞLAMADI** | `phase1` | `faz/1-envanter` | v0.1.0 |
| **2** | Pilot: 12 oyun + kalibrasyon | ⏸ beklemede | `phase2` | `faz/2-pilot` | v0.2.0 |
| **3** | Üretim bloğu I — Aileler I–IV | ⏸ beklemede | `phase3` | `faz/3-blok-1` | v0.3.0 |
| **4** | Üretim bloğu II — Aileler V–VII | ⏸ beklemede | `phase4` | `faz/4-blok-2` | v0.4.0 |
| **5** | Editoryal yakınsama + görsel üretim | ⏸ beklemede | `phase5` | `faz/5-yakinsama` | v0.5.0 |
| **6** | Nihai üretim + KDP paketi | ⏸ beklemede | `release` | `faz/6-uretim` | v1.0.0 |

---

## Faz 0 · Bootstrap — tamamlanan

- [x] Dizin yapısı (24 dizin)
- [x] `project_config.json` — tek doğruluk kaynağı
- [x] Altı fazlık uygulama yol haritası
- [x] `PROJECT_CONTEXT.md` · `BRIEF.md` · `DECISIONS.md` · `CHANGELOG.md`
- [x] `00_CONTEXT/`: STYLE · SOURCING_STANDARD · PLAYABILITY_STANDARD · LESSONS_FROM_CODEX
- [x] `01_SOURCE/game.schema.json` — veri şeması
- [x] Test altyapısı: `validate_spec.py` · `validate_structure.py` · `selftest.py`
- [x] `04_BUILD/qa_all.sh` — CI'ın birebir aynısı
- [x] `.github/workflows/validate.yml` — CI iskeleti
- [x] `.gitignore` + iki hatlı manuscript koruması
- [x] `.gate` = `phase0`
- [x] Git deposu ve `main` dalı

---

## Ölçülen ilerleme

| | Ölçülen | Hedef |
|---|---:|---:|
| Aday oyun | **0** | ≥140 |
| Kilitli oyun | **0** | 100 |
| Yazılmış oyun | **0** | 100 |
| Oynanabilirlik testi geçen | **0** | 100 |
| Kültür | **0** | ≥45 |
| Görsel | **0** | ~130 |
| Kelime | **0** | ~78.000 |

---

## Sonraki izinli eylem

> ⛔ **FAZ 1 BAŞLAMADI ve kurucu onayı olmadan başlamaz.**
>
> Onay geldiğinde ilk üç iş:
> 1. `faz/1-envanter` dalını aç
> 2. A1 (manuscript politikası) kararını kapat
> 3. Oyun adayı envanterini üretmeye başla — kısıt taraması **ilk** adımdır
