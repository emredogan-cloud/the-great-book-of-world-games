# Ciltli kapak — case-wrap güvenli alan onarımı · 2026-09-17

KDP ciltli kapağı (`B0HG41F21F`, ISBN **9798194081950**) **case-wrap safe-area**
ve **hinge safe-area** ihlaliyle reddetmişti. Onarım bu depoda değil, kapağı
üreten ortak hatta yapıldı:

- `COMMON-AREA/covers/founder_wrap_2026_09_12.py` — `wrap_safe()`, `_bleed_out()`,
  `build_spine(end_safe_in=…)`
- `COMMON-AREA/covers/build_founder_wraps.py` — ciltlide `wrap_safe`, `HINGE_PAD`

## Kök neden

Ciltli kaplama her dış kenardan **0,591 in**'i tahtanın arkasına katlar, KDP
bunun içine **0,125 in** daha ister: sayfanın **0,716 in**'i görünen yüzde değil.
Comp paneli sayfaya kenardan kenara yatırılıyordu, yani harfler katlanan bölgeye
gidiyordu. Ayrıca sırt yazısının uç payı her cilt için sabit 0,55 in'di —
ciltsizde doğru, ciltlide kısa.

## Ölçüm (basılan mürekkep üzerinden, `COMMON-AREA/qa/`)

| Ölçü | ÖNCE | SONRA | Gereken |
|---|---|---|---|
| Canlı yazı — üst / alt tahta kenarı | **0,545 / 0,492 in** | 1,345 / 1,167 in | ≥ 0,716 |
| — sol / sağ | 1,185 / 2,124 in | 1,415 / 2,459 in | ≥ 0,716 |
| **Menteşeden (arka kapak)** | **0,2335 in** | **0,954 in** | ≥ 0,400 |
| Sırt yazısı — uçlardan | **0,557 / 1,140 in** | **0,722 / 0,725 in** | ≥ 0,716 |
| Barkod alanı (min lum / std) | 0,0 / 55,6 | **241,7 / 0,00** | ≥ 225 / ≤ 3,0 |

Tam kapak **18,624 × 12,417 in**, sırt **0,549 in** — KDP Print Cover Calculator'dan
2026-09-17'de canlı okundu (Ciltli · S/B · beyaz kâğıt · 8,25 × 11 in · 160 sayfa)
ve üretilen dosyayla **birebir** eşleşti.

| | SHA-256 |
|---|---|
| eski | `961de7fb51a87b668cda27a607f2a99fe136e4b761b0825eb2acbd473e11eaed` |
| yeni | `ceaf0344079b2433a5ec6b5522667c40bcb8f0423e72d0a7bdaec207978b22bd` |

## KDP

Yüklendi (8,01 MB) · Previewer **"No Issue"** · yayımlandı · Bookshelf:
**Live · Updates publishing** · fiyat **$34,99 değişmedi** · kopya oluşmadı.

Ciltsiz ve büyük punto kapakları aynı üretici tarafından yeniden yazıldı ancak
ciltsiz kod yolu hiç değişmediği için piksel karşılaştırması **%0,00 değişim**
verdi — bu iki canlı listeleme etkilenmedi.

Ayrıntı: `../../KDP-GEOMETRY-REPAIR-FINAL-REPORT-TR-2026-09-16.md`
