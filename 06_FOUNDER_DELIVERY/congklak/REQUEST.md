# TESLİM İSTEĞİ — Congklak (`congklak`)

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/founder_delivery_ingest.py --scaffold -->

| | |
|---|---|
| **oyun** | Congklak |
| **kültür** | Javanese · Southeast Asia |
| **aile** | sowing |
| **öncelik** | A · bileşik puan 20.3 |
| **engel** | `P1` — SOURCE ACCESS BLOCKED |
| **durum** | `BLOCKED` |

## NEDEN YAZILAMIYOR

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

## ZATEN DENETLENDİ — BUNLARI TEKRAR ARAMAYIN

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 ve Russ 2000 proje genelinde DENENDİ ve açılamadı

## ARANACAK

1. Murray 1952 ya da Russ 2000'de congklak/congkak/dakon maddesi
2. Çukur sayısı, depo (rumah) kuralı, eş zamanlı başlangıç olup olmadığı, ekim yönü, alma, tur sonu ve yeniden dizme kuralı
3. KARAR MALZEMESİ: sungka ile mekanik farkı — kitap ikisini ayrı madde yapacaksa farkı yazmalı

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

- `"congklak" OR "congkak" OR "dakon" Javanese mancala rules`
- `congkak Malay Indonesian sowing game rules ethnography`

## BU KLASÖRE NE KOYULUR

```
congklak/
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
