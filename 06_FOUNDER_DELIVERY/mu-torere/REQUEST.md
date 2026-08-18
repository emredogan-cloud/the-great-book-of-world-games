# TESLİM İSTEĞİ — Mū Tōrere (`mu-torere`)

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/founder_delivery_ingest.py --scaffold -->

| | |
|---|---|
| **oyun** | Mū Tōrere |
| **kültür** | Māori · Oceania |
| **aile** | territory |
| **öncelik** | C · bileşik puan 21.2 |
| **engel** | `P2` — SOURCE TEXT UNAVAILABLE |
| **durum** | `BLOCKED` |

## NEDEN YAZILAMIYOR

Birincil künye ARANDI ve BULUNAMADI (archive.org'da yok, NZETC adresi çözülmedi); ikinci künye bir dergi makalesidir ve hiç denenmedi. Oyun `attributed` taranmıştır: Māori atfı ZORUNLUDUR ve kayıt ayrıca ÇAĞDAŞ Māori kaynaklı bir künye ve MÜMKÜNSE TOPLULUK ONAYI istiyor.

## ZATEN DENETLENDİ — BUNLARI TEKRAR ARAMAYIN

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Best 1925 · Games and Pastimes of the Maori — archive.org'da yok, NZETC adresi çözülmedi (Batch 4 kaynak avı, 2026-08-16)
- Ascher 1987 · Mathematics Magazine — HİÇ denenmedi

## ARANACAK

1. Best, Elsdon, Games and Pastimes of the Maori (1925) — mū tōrere bölümü (NZETC ya da National Library of New Zealand)
2. Ascher, Marcia, 'Mu Torere: An Analysis of a Maori Game', Mathematics Magazine 60:2 (1987) — ikinci bağımsız kaynak
3. ÇAĞDAŞ Māori kaynaklı bir künye — atıf zorunluluğu için
4. Sekiz uçlu yıldız tahtası, 4'er taş, YALNIZCA komşu boşluğa hareket, merkeze girme kısıtı ve kilitlenme galibiyeti

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

NZETC üzerinden Best 1925 tam metni + bir Māori kurumunun (Te Papa · iwi) çağdaş anlatımı.

## ARAMA KALIPLARI

*Bunlar birer stratejidir; bu adreslerin var olduğu iddia edilmez.*

- `Elsdon Best "Games and Pastimes of the Maori" NZETC full text`
- `Ascher "Mu Torere" Mathematics Magazine 1987 PDF`
- `mu torere Maori game rules Te Papa`

## BU KLASÖRE NE KOYULUR

```
mu-torere/
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
