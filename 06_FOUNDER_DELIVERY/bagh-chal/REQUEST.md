# TESLİM İSTEĞİ — Bagh-Chal (`bagh-chal`)

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/founder_delivery_ingest.py --scaffold -->

| | |
|---|---|
| **oyun** | Bagh-Chal |
| **kültür** | Nepali · South Asia |
| **aile** | hunt-siege |
| **öncelik** | A · bileşik puan 20.5 |
| **engel** | `P1` — SOURCE ACCESS BLOCKED |
| **durum** | `BLOCKED` |

## NEDEN YAZILAMIYOR

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

## ZATEN DENETLENDİ — BUNLARI TEKRAR ARAMAYIN

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Bell ve Parlett proje genelinde DENENDİ ve açılamadı

## ARANACAK

1. Bell ya da Parlett'te bagh-chal maddesi
2. 5×5 köşegenli tahta, 4 kaplan / 20 keçi, yerleştirme aşaması, atlama-alma, kaplanların kilitlenmesi, kaç keçi kaybı kaplan galibiyeti

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

Nepal kaynaklı çağdaş bir künye ile birlikte olursa kültür atfı da güçlenir.

## ARAMA KALIPLARI

*Bunlar birer stratejidir; bu adreslerin var olduğu iddia edilmez.*

- `"bagh chal" rules tigers goats Nepal board game`
- `bagh-chal Nepali traditional game rules ethnography`

## BU KLASÖRE NE KOYULUR

```
bagh-chal/
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
