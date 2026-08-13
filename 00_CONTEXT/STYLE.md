# STYLE — The Great Book of World Games

> Sürüm **2.0 · Faz 2 · ÖLÇÜMLE KALİBRE EDİLDİ.**
>
> v1.0'ın sayıları hedefti. Buradakiler **ölçüldü**: üç oyun gerçek trimde
> (8,5 × 11), gerçek fontla (Times-Roman 10,5/13,5), gerçek sütun
> genişliğinde (181 mm) dizildi ve satırlar sayıldı.
> Ölçüm: `06_REPORTS/phase2-typeset-measurement.json`
>
> Kurucu onayı bekliyor (AÇIK KARAR A5) · `project_config.json § style` ile
> senkron kalmalıdır.

---

## 0 · Faz 2 ölçümü — kalibrasyonun tek cümlesi

> **Sayfa bütçesi bir KELİME bütçesi değil, bir DİYAGRAM bütçesidir.**

| Ölçülen | Faz 1 hipotezi | **Faz 2 ölçümü** | Sonuç |
|---|---:|---:|---|
| Kelime / dizilmiş sayfa | 320 | **389** | hipotez %18 düşüktü |
| Kelime / oyun | 650 | **708** | bantta (480–900) |
| **Metin** sayfa / oyun | — | **1,37** | oyunlar arası fark **0,01** |
| **Diyagram** sayfa / oyun | — | **0,45** | oyunlar arası fark **0,55** |
| Toplam sayfa / oyun | 2,00 | **1,82** | bantta (2,0 ± 0,25) |

Üç oyunun metni birbirinden **yüzde bir** farklı çıktı. Diyagram alanı ise
üç katına kadar değişti. Yani bir maddeyi çift sayfadan taşıran şey uzun
proza değil, **büyük ya da çok sayıda diyagramdır**.

**Yazım için sonucu:** 650 kelime hedefi doğrudur ve **daraltılmasına gerek
yoktur**. Kısıt diyagram tarafındadır ve `DIAGRAM_LANGUAGE.md § 7.1`de
150 mm'lik bir bütçeye bağlanmıştır.

---

## 1 · İki ayrı kayıt

Bu kitap **iki farklı dille** yazılır ve ikisi bilinçli olarak ayrıdır.

| Kayıt | Nerede | Ses |
|---|---|---|
| **Anlatı** | kültürel hikâye · aile portresi · giriş denemesi | bilgili ama gösterişsiz bir rehber |
| **Talimat** | kural metni · kurulum · tur sırası | kuru, kesin, numaralı, tek eylemli |

Talimat kaydında güzel cümle kurma zorunluluğu **yoktur**. Anlaşılmayan
adım ise kusurdur.

---

## 2 · Ölçülen bantlar

| Ölçüt | Hedef | Faz 2'de ÖLÇÜLEN | Kapı |
|---|---|---|---|
| Oyun başına kelime | 650 (bant 480–900) | **708** ✓ | `qa_length` |
| Kültürel hikâye | ~120 kelime | **118–122** ✓ | `qa_length` |
| Anlatı cümle ortalaması | 12,0–19,0 kelime | — | `qa_drift` |
| **Kural metni cümle azamisi** | **22 kelime** | **en uzun 21** ✓ | `qa_rules` |
| Kural adımı | numaralı, **tek eylem** | — | `qa_rules` |
| Aile portresi | ~600 kelime | Faz 3 | `qa_length` |
| **Diyagram alanı / madde** | **≤150 mm** | 57,5 – 189,5 mm ⚠ | `qa_diagram` |

Son satır Faz 2'de **eklendi** ve bir maddede (Tablut) aşıldı. Kısıt buradan
gelir, kelime sayısından değil.

---

## 3 · Kural metni şablonu

Kural blokları sabittir ve şu etiketlerle başlar:

```
Setup: Place the board between the two players…
Turn sequence: 1. Take one seed from any pit on your side…
Win condition: The player with the most seeds when the last pit empties…
```

*On your turn,* kalıbı ikinci tekil şahsı kurar ve oyuncunun **ne
yapabileceğini** anlatır. *The game ends when* kalıbı bitiş koşulunu
belirsizlik bırakmadan kapatır.

---

## 4 · Yasak kalıplar

`qa_voice` bunları arar ve bulursa kırmızı yanar:

- "sadece … değil, aynı zamanda" / "not only … but also"
- "in today's world"
- "dive into" · "unlock the secrets" · "embark on a journey"
- Üçlü liste ritminin ard arda üç paragrafta tekrarı
- Aynı geçiş ifadesinin bir aile içinde üçten fazla kullanımı

> Bunlar estetik tercih değil. 2026'da okur AI metnini tanımayı öğrendi ve
> tanıdığı anda güvenini geri çekiyor. Bu liste o riski azaltır.

---

## 5 · Belirsizlik gizlenmez, yazılır

Kaynaklar çelişiyorsa veya kurallar eksikse, metin bunu **söyler**:

> *"Bu oyunun özgün kuralları bilinmiyor. Aşağıdaki kural, [kaynak]'a
> dayanarak yeniden kurgulanmıştır."*

Bu bir zaaf değil **imzadır**. AI metninin en tanınır işareti her şeyi eşit
güvenle söylemesidir; bu kitap bunun tersini yapar.

`sourceConfidence: reconstructed` taşıyan her oyun prozada bu etiketi
**görünür** biçimde taşır. `qa_rules` bunu denetler.

---

## 6 · Somut ayrıntı kotası

Her kültürel hikâyede **en az bir doğrulanabilir somut ayrıntı** bulunur:
bir müze envanter numarası, bir tarih, bir yer adı, bir kelimenin anlamı.

Genelleme AI'nin doğal çıktısıdır; somutluk insan araştırmasının izidir.

---

## 7 · Editoryal karar görünür kılınır

"Bu oyunda bahis mekaniği puanla değiştirildi", "Go için 9×9 tahta seçildi
çünkü…" gibi **kararlar yazılır**. AI karar vermez, seçenek sunar.
Görünür karar, insan yazarlığının en ucuz kanıtıdır.
