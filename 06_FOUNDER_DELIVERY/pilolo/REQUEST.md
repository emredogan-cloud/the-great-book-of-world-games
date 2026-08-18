# TESLİM İSTEĞİ — Pilolo (`pilolo`)

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/founder_delivery_ingest.py --scaffold -->

| | |
|---|---|
| **oyun** | Pilolo |
| **kültür** | Ga · West Africa |
| **aile** | boardless |
| **öncelik** | A · bileşik puan 19.8 |
| **engel** | `P1` — SOURCE ACCESS BLOCKED |
| **durum** | `BLOCKED` |

## NEDEN YAZILAMIYOR

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

## ZATEN DENETLENDİ — BUNLARI TEKRAR ARAMAYIN

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı

## ARANACAK

1. Zaslavsky 1973'te pilolo maddesi — saklama/arama sırası, puanlama, bitiş
2. GANA KAYNAKLI ikinci bağımsız künye (Ga çocuk oyunları)

## ASGARİ KABUL EDİLEBİLİR KANIT

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

## İDEAL KANIT

Sayfa-doğrulanmış tarama ya da kararlı kamusal adres; künye tam (yazar · başlık · baskı · yıl · sayfa).

## ARAMA KALIPLARI

*Bunlar birer stratejidir; bu adreslerin var olduğu iddia edilmez.*

- `"pilolo" Ghana Ga children's game rules`
- `Ga people traditional children games Ghana ethnography`

## BU KLASÖRE NE KOYULUR

```
pilolo/
    source.pdf          tarama · PDF · ekran görüntüsü        (opsiyonel)
    source.md           metin ya da kural özeti               (opsiyonel)
    bibliography.md     ZORUNLU — aşağıdaki şablon            (zorunlu)
    notes.md            ne bulundu · ne bulunamadı            (opsiyonel)
```

`bibliography.md` şablonu — **sayfa yoksa boş bırakın, UYDURMAYIN**:

```
author  :
title   :
edition :
year    :
pages   :
locator :
```
