# TESLİM İSTEĞİ — Yoté (`yote`)

<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/founder_delivery_ingest.py --scaffold -->

| | |
|---|---|
| **oyun** | Yoté |
| **kültür** | Wolof · West Africa |
| **aile** | war-board |
| **öncelik** | C · bileşik puan 20.6 |
| **engel** | `P2` — SOURCE TEXT UNAVAILABLE |
| **durum** | `SOURCE-PENDING` |

## NEDEN YAZILAMIYOR

Birincil künye Dakar basımı dar dağıtımlı bir eserdir ve HİÇ DENENMEDİ; ikinci künye (Zaslavsky) engelli.

## ZATEN DENETLENDİ — BUNLARI TEKRAR ARAMAYIN

- Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı tek tek tarandı — isabet yok
- Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor
- Béart 1955 · Mémoires de l'IFAN 42 — HİÇ denenmedi
- Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı

## ARANACAK

1. Béart, Charles, Jeux et jouets de l'Ouest africain (Dakar: IFAN, 1955) — yoté bölümü (Fransızca)
2. 5×6 ızgara, elde tutulan taşların sırayla girmesi, atlayarak alma ve ALINAN HER TAŞLA BİRLİKTE İKİNCİ BİR TAŞIN DA KALDIRILMASI kuralı — oyunun ayırt edici mekaniği budur (distinct=5)
3. Wolof atfını veren bir kaynak

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

Béart 1955 — Batı Afrika oyunlarının en iyi saha kaydı; zamma ile AYNI kaynak, tek teslim iki oyun açar.

## ARAMA KALIPLARI

*Bunlar birer stratejidir; bu adreslerin var olduğu iddia edilmez.*

- `Béart "Jeux et jouets de l'Ouest africain" IFAN 1955 PDF`
- `"yoté" OR "yote" Wolof Senegal game rules double capture`
- `jeux ouest africain yoté règles IFAN Dakar`

## BU KLASÖRE NE KOYULUR

```
yote/
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
