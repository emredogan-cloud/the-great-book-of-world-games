# TESLİM İSTEĞİ — Morra (`morra`)

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/founder_delivery_ingest.py --scaffold -->

| | |
|---|---|
| **oyun** | Morra |
| **kültür** | Italian · Mediterranean |
| **aile** | boardless |
| **öncelik** | A · bileşik puan 21.8 |
| **engel** | `P3` — RULES INCOMPLETE |
| **durum** | `BLOCKED` |

## NEDEN YAZILAMIYOR

Erişilebilir kaynak AÇILDI ve mekaniği verdi ama PUANLAMA ve KAZANMA KOŞULU yoktur. Bir oyun bitişi olmadan basılamaz.

## ZATEN DENETLENDİ — BUNLARI TEKRAR ARAMAYIN

- Falkener 1892 § Atep/Mora, ss. 103–105 AÇILDI: iki biçim kayıtlı (ikisi birden parmak atar ve ikisi de tahmin eder; ya da biri atar öteki tahmin eder) ve İTALYAN oyunu adlandırılıyor
- Cicero De Officiis III.77 — bir ATASÖZÜDÜR, kural değil
- Parlett 1999 telif altında

## ARANACAK

1. Morra'nın PUANLAMASINI ve KAZANMA koşulunu veren herhangi bir künye
2. Tur yapısı: kaç el oynanır, puan nasıl birikir
3. Berabere durumunda ne olduğu

## ASGARİ KABUL EDİLEBİLİR KANIT

```
RULE EVIDENCE
  [ ] turn order  [ ] scoring  [ ] end condition  [ ] draw condition  [ ] variants
SOURCE EVIDENCE
  [ ] author  [ ] title  [ ] edition  [ ] publication year  [ ] exact page  [ ] stable locator
CULTURAL EVIDENCE
  [ ] culture identity  [ ] attribution
```

## İDEAL KANIT

Bir İtalyan halk oyunları derlemesi ya da Parlett'in morra bölümü.

## ARAMA KALIPLARI

*Bunlar birer stratejidir; bu adreslerin var olduğu iddia edilmez.*

- `"morra" Italian finger game rules scoring`
- `"micatio" mora game history rules`
- `morra gioco regole punteggio storico`

## BU KLASÖRE NE KOYULUR

```
morra/
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
