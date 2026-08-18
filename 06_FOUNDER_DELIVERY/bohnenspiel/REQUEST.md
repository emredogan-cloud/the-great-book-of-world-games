# TESLİM İSTEĞİ — Bohnenspiel (`bohnenspiel`)

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/founder_delivery_ingest.py --scaffold -->

| | |
|---|---|
| **oyun** | Bohnenspiel |
| **kültür** | German · Central Europe |
| **aile** | sowing |
| **öncelik** | A · bileşik puan 21.6 |
| **engel** | `P1` — SOURCE ACCESS BLOCKED |
| **durum** | `BLOCKED` |

## NEDEN YAZILAMIYOR

Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı KÜNYE seviyesindedir (`sourceVerification: bibliographic`): kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. § 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.

## ZATEN DENETLENDİ — BUNLARI TEKRAR ARAMAYIN

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Murray 1952 ve Bell proje genelinde DENENDİ ve açılamadı

## ARANACAK

1. Murray 1952 ya da Bell'de Bohnenspiel maddesi — 2×6 çukur, 6'şar tohum, ekim yönü, 2/4/6 alma kuralı, zincirli alma
2. Oyunun Avrupa'ya nasıl ulaştığına dair BİR İDDİA DEĞİL, bir kayıt (kayıt köken iddiasını açıkça yasaklıyor)

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

Alman kaynaklı bir dönem kaydı köken sorununu da hafifletir.

## ARAMA KALIPLARI

*Bunlar birer stratejidir; bu adreslerin var olduğu iddia edilmez.*

- `"Bohnenspiel" German mancala rules Murray`
- `das Bohnenspiel Regeln historisch Saatspiel`

## BU KLASÖRE NE KOYULUR

```
bohnenspiel/
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
