# STYLE — The Great Book of World Games

> Sürüm **2.1 · Faz 4 · ÖLÇÜM 22 OYUNA ÇIKARILDI.**
>
> v1.0'ın sayıları hedefti. Buradakiler **ölçüldü**: yirmi iki madde gerçek
> trimde (8,5 × 11), gerçek fontla (Times-Roman 10,5/13,5), gerçek sütun
> genişliğinde (181 mm) dizildi ve satırlar sayıldı. Örneklem üç fazda
> 3 → 11 → 22 oyuna çıktı ve her seferinde bir sayıyı düzeltti.
> Ölçüm: `06_REPORTS/phase4-typeset-measurement.json` (22 oyun)
>
> Kurucu onayı bekliyor (AÇIK KARAR A5) · `project_config.json § style` ile
> senkron kalmalıdır.

---

## 0 · Ölçüm — ve Faz 2'nin cümlesinin nasıl düzeldiği

> **Faz 2 (3 oyun) şunu yazdı:** *"Sayfa bütçesi bir KELİME bütçesi değil,
> bir DİYAGRAM bütçesidir."*
>
> **Faz 4 (22 oyun) bunu ölçtü ve YANLIŞLADI.** Cümle bir bulgu değil, bir
> **örneklem eseriydi**.

| Ölçülen | Faz 1 hipotezi | Faz 2 (3) | Faz 3 (11) | **Faz 4 (22)** |
|---|---:|---:|---:|---:|
| Kelime / dizilmiş sayfa | 320 | 389 | 405 | **447** |
| Kelime / oyun | 650 | 708 | 616 | **686** |
| **Metin** sayfa / oyun | — | 1,37 | 1,18 | **1,25** |
| **Metin** farkı (oyunlar arası) | — | **0,01** | 0,41 | **0,69** |
| **Diyagram** farkı (oyunlar arası) | — | **0,55** | 0,62 | **0,63** |
| Toplam sayfa / oyun | 2,00 | 1,82 | 1,52 | **1,53** |
| Taşma oranı | — | %33 | %9 | **%4,5** |

Faz 2'de üç oyunun metni birbirinden yüzde bir farklıydı ve bu, metnin
**sabit** olduğu anlamına geliyor sanıldı. Yirmi iki oyunda metin farkı
**0,69 sayfaya** çıktı ve diyagram farkını (0,63) **geçti**.

**Tek bir sürücü yoktur.** Sayfa bütçesi hem kelimeyi hem diyagramı
denetlemek zorundadır ve `calibrate_pages.py` sürücüyü artık **ölçümden
türetir**; koda gömülü bir cümleden okumaz.

**Yazım için sonucu değişmedi:** 650 kelime hedefi doğrudur ve
daraltılmasına gerek yoktur (ölçülen 686, bant 480–900). 150 mm diyagram
bütçesi de **yürürlükte kalır** — ama gerekçesi değişti: artık "tek sürücü
diyagramdır" diye değil, **iki sürücüden birinin sert bir tavanı olmadığı**
için. Faz 4 o tavanı ayrıca **oyun başına** bağladı.

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

| Ölçüt | Hedef | **Faz 4'te ÖLÇÜLEN (22 oyun)** | Kapı |
|---|---|---|---|
| Oyun başına kelime | 650 (bant 480–900) | **686** ✓ | `qa_length` |
| Kültürel hikâye | ~120 kelime | **118–130** ✓ | `qa_length` |
| Anlatı cümle ortalaması | 12,0–19,0 kelime | — | `qa_drift` |
| **Kural metni cümle azamisi** | **22 kelime** | **en uzun 21** ✓ | `qa_rules` |
| Kural adımı | numaralı, **tek eylem** | — | `qa_rules` |
| Aile portresi | ~600 kelime | Faz 3 | `qa_length` |
| **Diyagram alanı / madde** | **≤150 mm** | 36,1 – 144,0 mm ✓ | `qa_diagram` |

Son satır Faz 2'de eklendi, bir maddede (Tablut) aşıldı ve **Faz 4'te
kapatıldı**. Bütçe artık **oyun başına** denetlenir: Faz 4 ölçümü, adı
`maxDiagramMmPerGame` olan bütçenin diyagram başına denetlendiğini buldu —
iki diyagramlı bir madde onu ikiye katlayabiliyordu.

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
