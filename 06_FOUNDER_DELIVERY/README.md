# 06_FOUNDER_DELIVERY — kurucu kaynak teslim dizini

> Kurucu direktifi § 16 · § 17. Bu dizin **kurucunun bulduğu kaynakların
> bırakıldığı yerdir**. Ajan buradan alır, doğrular, engeli çözer ve oyunu
> yazar.

## Yapı

```
06_FOUNDER_DELIVERY/
    <GAME_ID>/                  ← kayıttaki gameId, BİREBİR
        REQUEST.md              ← ÜRETİLİR · ne aranacağı burada yazar
        source.pdf              ← tarama · PDF · ekran görüntüsü   (opsiyonel)
        source.md               ← metin ya da kural özeti          (opsiyonel)
        bibliography.md         ← ZORUNLU · künye
        notes.md                ← ne bulundu · ne bulunamadı       (opsiyonel)
```

Klasör açmak için:

```bash
./04_BUILD/founder_delivery_ingest.py --scaffold 10        # ilk 10 öncelik
./04_BUILD/founder_delivery_ingest.py --scaffold-game oware
```

Teslimi almak için:

```bash
./04_BUILD/founder_delivery_ingest.py
```

## `bibliography.md` şablonu

**Sayfa bilinmiyorsa BOŞ BIRAKIN. Uydurmayın.**

```
author  :
title   :
edition :
year    :
pages   :
locator :
```

Sayfa yoksa teslim **yine de alınır**; kayıt `bibliographyStatus: incomplete`
taşır ve o oyun yazılabilir ama `locked` olamaz. Uydurulmuş bir sayfa
numarası kitabın tek denetlenebilir iddiasını yıkar; eksik künye yıkmaz.

## ⚠ Ham teslim depoda TAKİP EDİLMEZ

`REQUEST.md` ve bu `README.md` dışındaki her şey `.gitignore`dadır.
Gerekçe `01_SOURCE/rules/` ile aynıdır (karar K12): telifli bir taramayı
public bir depoya koymak, kaynak standardının kendisini ihlal eder.
Teslim **yerelde durur**, ajan **yerelde okur**, depoya yalnızca
`06_REPORTS/founder-delivery-ingest.json` içindeki **hash ve künye durumu**
girer.

## Ne göndermeniz GEREKMİYOR

- JSON'a çevirmek **gerekmez** — alım betiği yapar.
- Kuralı yeniden yazmak **gerekmez** — ham metin/tarama yeterlidir.
- `REQUEST.md`'deki *"ZATEN DENETLENDİ"* başlığı altındaki hiçbir şeyi
  tekrar aramak **gerekmez**.

## Teslimden sonra ne olur

```
ALIM → HASH → KÜNYE DENETİMİ → ajan KAYNAĞI OKUR → kanıt listesi işaretlenir
   → source_verification kaydı → engel çözülür → üretim kuyruğu
   → YAZ → DİYAGRAM → QA → dizgi → CI YEŞİL → SONRAKİ OYUN
```

Bir oyunun engeli çözüldüğünde **yarım bırakılmaz** (§ 19).
