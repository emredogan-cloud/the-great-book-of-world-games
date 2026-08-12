# STYLE — The Great Book of World Games

> Sürüm **1.0 · bootstrap**. Bu belge Faz 2'de **ölçümle** kalibre edilir ve
> v2.0 olur. Buradaki sayılar şu an *hedeftir*, ölçüm değil.
>
> Değişiklik kurucu onayı gerektirir · `project_config.json § style` ile
> senkron kalmalıdır.

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

| Ölçüt | Hedef | Kapı |
|---|---|---|
| Oyun başına kelime | 650 (bant 480–900) | `qa_length` |
| Kültürel hikâye | ~120 kelime | `qa_length` |
| Anlatı cümle ortalaması | 12,0–19,0 kelime | `qa_drift` |
| **Kural metni cümle azamisi** | **22 kelime** | `qa_rules` |
| Kural adımı | numaralı, **tek eylem** | `qa_rules` |
| Aile portresi | ~600 kelime | `qa_length` |

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
