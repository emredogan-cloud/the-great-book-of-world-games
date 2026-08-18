# TESLİM İSTEĞİ — Kōnane (`konane`)

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/founder_delivery_ingest.py --scaffold -->

| | |
|---|---|
| **oyun** | Kōnane |
| **kültür** | Hawaiian · Oceania |
| **aile** | war-board |
| **öncelik** | C · bileşik puan 20.6 |
| **engel** | `P2` — SOURCE TEXT UNAVAILABLE |
| **durum** | `BLOCKED` |

## NEDEN YAZILAMIYOR

Birincil künye KAMUSAL ALANDADIR ama yalnızca JSTOR nüshası bulundu ve tam metin indirilemedi; ikinci künye (Bell) engelli. Oyun `attributed` taranmıştır: Hawaii atfı ZORUNLUDUR ve kayıt ÇAĞDAŞ Kānaka Maoli kaynaklı bir künye istiyor.

## ZATEN DENETLENDİ — BUNLARI TEKRAR ARAMAYIN

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Culin 1899 · 'Hawaiian Games', American Anthropologist 1:2 — yalnızca JSTOR nüshası, tam metin indirilemedi (Batch 4 avı)
- Culin 1898 · Chess and Playing-Cards AÇILDI (pachisi ve patolli buradan doğrulandı) — kōnane maddesi taranmadı
- Bell proje genelinde DENENDİ ve açılamadı

## ARANACAK

1. Culin, Stewart, 'Hawaiian Games', American Anthropologist 1:2 (1899) — kōnane bölümü, SAYFA NUMARASIYLA (KAMUSAL ALAN; ciltli dergi taraması aranmalı — proje bu makalenin sayfa aralığını henüz görmedi)
2. Tahta ölçüsü, ilk iki taşın kaldırılması, YALNIZCA atlayarak alma, çoklu atlama kuralı ve hamlesiz kalanın kaybetmesi
3. ÇAĞDAŞ Kānaka Maoli kaynaklı bir künye — atıf zorunluluğu için (Bishop Museum · Hawaiian kültür kurumları)

## ASGARİ KABUL EDİLEBİLİR KANIT

```
RULE EVIDENCE
  [ ] setup  [ ] player count  [ ] materials  [ ] board / topology  [ ] first move  [ ] legal moves  [ ] turn order  [ ] capture  [ ] objective  [ ] end condition  [ ] scoring  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] region  [ ] attribution  [ ] historical context
```

## İDEAL KANIT

American Anthropologist cilt 1 (1899) taraması + Bishop Museum kaydı.

## ARAMA KALIPLARI

*Bunlar birer stratejidir; bu adreslerin var olduğu iddia edilmez.*

- `Culin "Hawaiian Games" American Anthropologist 1899 archive.org`
- `American Anthropologist volume 1 1899 full text HathiTrust`
- `konane Hawaiian checkers rules Bishop Museum`

## BU KLASÖRE NE KOYULUR

```
konane/
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
