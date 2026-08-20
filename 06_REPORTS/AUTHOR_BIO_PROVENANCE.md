# YAZAR BİYOGRAFİSİ — KÜNYE

> **The Great Book of World Games** · Faz 6 · 20 Ağustos 2026
>
> Kurucu talimatı (§ 9): *"Use the SAME AUTHOR BIO already used for the other
> books. Do NOT invent a new biography. Do NOT improvise. … Reuse the
> established canonical author bio verbatim."*

---

## 1 · Kullanılan metin

> Emre is a puzzle designer, mythologist, and game archivist dedicated to
> preserving ancient cultures, codes, and stories for the next generation.

| | |
|---|---:|
| Kelime | 21 |
| Karakter | 142 |
| SHA-256 (ilk 16) | `5e56de5a7221b811` |

**Tek kelimesi değiştirilmedi.** Kopyalama, kaynak dosyadan okunan metnin
buradaki metinle **birebir eşit** olduğu doğrulanarak yapıldı; eşitlik
sağlanmasaydı betik durur ve yazma işlemi hiç gerçekleşmezdi.

---

## 2 · Kaynak

| | |
|---|---|
| **Proje** | `THE-MYTH-HUNTERS-FIELD-BOOK` |
| **Dosya** | `project_config.json` → `founder.authorBio` |
| **Onay kararı** | `DECISIONS.md § K36` — *"A6 kapandı — yazar biyografisi kurucu metnidir"* |
| **Onay tarihi** | 16 Ağustos 2026 (Faz 6 talimatı § 2) |
| **Kararın kendi ifadesi** | *"Metin **kurucunun kendi cümlesidir** ve tek kelimesi değiştirilmedi."* |
| **Sevk edilen kopya** | `08_OUTPUT/PAPERBACK/metadata.json` · `06_REPORTS/tracked/metadata.json` (18 Ağustos 2026) |

---

## 3 · Aday havuzu — dördü de bulundu, biri seçildi

Beş kardeş proje tarandı (`CODEX_MYTHOLOGICA`, `CODEX_BESTIARIUM`,
`THE-GREAT-BOOK-OF-WORLD-MYTHS`, `THE-MYTH-HUNTERS-FIELD-BOOK`,
`CODEX-ENIGMATICA`); `project_config.json`, KDP metadata, A+ manifestleri,
kitap kaynakları ve karar defterleri okundu. **Dört farklı biyografi** bulundu:

| # | proje | dosya | tarih | metin |
|---|---|---|---|---|
| 1 | CODEX_MYTHOLOGICA | `03_APLUS/spec/aplus-manifest.json` | 5 Ağu 2026 | *"…came to mythology… CODEX MYTHOLOGICA, his first book, gathers seventy-six myths from nineteen traditions…"* |
| 2 | CODEX_BESTIARIUM | `03_APLUS/spec/aplus-manifest.json` | 9 Ağu 2026 | *"…came to folklore… CODEX BESTIARIUM, the second volume… one hundred and twelve creatures from forty traditions…"* |
| 3 | THE-GREAT-BOOK-OF-WORLD-MYTHS | `project_config.json` | 12 Ağu 2026 | *"Emre Doğan is the author of Codex Mythologica and Codex Bestiarium… his first book for young readers…"* |
| **4** | **THE-MYTH-HUNTERS-FIELD-BOOK** | **`project_config.json`** | **16 Ağu 2026** | **seçilen metin** |

### Neden dördüncüsü

Kurucunun talimatı *"newest/current approved version"* der. Üç ölçüt de aynı
metni gösteriyor:

1. **En yeni onaylı sürüm.** 16 Ağustos 2026; ötekiler 5, 9 ve 12 Ağustos.
2. **Tek AÇIKÇA ONAYLANMIŞ metin.** Yalnızca bu metnin arkasında bir karar
   kaydı var (`K36`) ve o karar metnin **kurucunun kendi cümlesi** olduğunu
   söylüyor. Ötekiler ajan tarafından yazılmış ve karar defterinde onay kaydı
   taşımıyor.
3. **Aynı bağımlılığı kapatan tek metin.** `K36` tam olarak bu projede de
   açık olan **A6**'yı kapatmak için yazıldı; gerekçesi de aynı: *World
   Myths'te KDP bir yer tutucu biyografiyi reddetti.*

İlk üçü ayrıca **bu kitap için kullanılamazdı**: üçü de kendi ciltlerinin
içerik sayılarını (yetmiş altı mit, yüz on iki yaratık) ya da başka bir
kitabın konumlanmasını (*"his first book for young readers"*) taşıyor. Bir
oyun kitabının künyesinde duran bu cümleler **yanlış** olurdu.

---

## 4 · Uydurulmayan şeyler

- Yeni bir biyografi **yazılmadı**.
- Var olan metin **kısaltılmadı, uzatılmadı, süslenmedi**.
- Oyun kitabına uydurmak için **tek kelime eklenmedi** — metinde zaten
  *"game archivist"* geçiyor ve bu bir tesadüftür, bir düzenleme değil.
- Ödül, satış, uzmanlık ya da kurum iddiası **eklenmedi**.

---

## 5 · Nerede basılıyor

| yer | durum |
|---|---|
| `project_config.json → founder.authorBio` | ✅ |
| İç blok künye sayfası (her iki baskı sürümü) | ✅ |
| Kindle EPUB künye sayfası | ✅ |
| `06_REPORTS/tracked/metadata.json` | ✅ |
| KDP yükleme kılavuzu | ✅ |
| Arka kapak | ✅ |

---

## 6 · Kapı etkisi

`metadata.py` `authorBio` boşken **`release` kapısında KIRMIZI** yanıyordu
(yol haritası Faz 6 § 12). Bu bağımlılık artık **kapalıdır**.
