# TESLİM İSTEĞİ — Oware (`oware`)

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/founder_delivery_ingest.py --scaffold -->

| | |
|---|---|
| **oyun** | Oware |
| **kültür** | Akan · West Africa |
| **aile** | sowing |
| **öncelik** | A · bileşik puan 21.3 |
| **engel** | `P1` — SOURCE ACCESS BLOCKED |
| **durum** | `BLOCKED` |

## NEDEN YAZILAMIYOR

Üç künyenin ÜÇÜ de engelli. Erişilebilir kamusal alan alternatifi AÇILDI ve KÜLTÜR TUZAĞI çıktı: Culin 1896'nın ayrıntılı kural kayıtları SURİYE (Şam) ve VEI (Liberya) biçimlerinindir; Gold Coast/Akan wari'si yalnızca Bent'in alıntısında ANILIR ve kuralı verilmez. Akan oyununu Şam kaydından yazmak kitabın kültür künyesini yalanlar.

## ZATEN DENETLENDİ — BUNLARI TEKRAR ARAMAYIN

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Culin 1896 · 'Mancala, the National Game of Africa' AÇILDI: ss. 597–598 Suriye biçimi, s. 594 Vei biçimi — Akan kuralı YOK (source_verification.json, 2026-08-14)
- Murray 1952 · de Voogt 1997 · Zaslavsky 1973 — üçü de DENENDİ ve açılamadı

## ARANACAK

1. Murray 1952'de wari/awele maddesi — Gold Coast biçimi
2. Ya da: Gana/Akan kaynaklı herhangi bir dönem ya da çağdaş kural kaydı
3. Alma kuralı (son tohumun düştüğü çukurda 2 ya da 3), 'aç bırakmama' kuralı ve döngü/bitiş kuralı — kayıt sonsuz döngüyü GERÇEK bir risk olarak işaretliyor ve kitabın basacağı bitiş kuralının EDİTORYAL olduğunu söylüyor; kaynak bunu desteklemeli

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

Bir Akan/Gana kaynağı ki hem kuralı hem de oyunun adının tartışmalı halk etimolojisini tek bir hikâyeye indirgemesin.

## ARAMA KALIPLARI

*Bunlar birer stratejidir; bu adreslerin var olduğu iddia edilmez.*

- `Murray 1952 wari awele Gold Coast rules mancala`
- `"oware" Akan Ghana rules ethnography`
- `awale wari Gold Coast traditional rules 19th century`

## BU KLASÖRE NE KOYULUR

```
oware/
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
