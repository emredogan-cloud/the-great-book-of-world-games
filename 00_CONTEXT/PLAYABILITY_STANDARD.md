# OYNANABİLİRLİK STANDARDI

> Bu kitabın **tek vaadi** alt başlığındadır: *Ready to Play Tonight.*
> Bu belge o vaadi bir mekanizmaya bağlar.
>
> Sürüm: 1.0 · Faz 1'de onaylanır · Değişiklik kurucu kararı gerektirir

---

## 1 · Sözleşme

> **Bir okur, kitaptan başka hiçbir kaynağa bakmadan, evde bulunan
> malzemeyle oyunu kurabilmeli ve sonuna kadar oynayabilmelidir.**

Bu cümle ölçülebilir olmalıdır. Aşağıdaki dört kural onu ölçülebilir kılar.

---

## 2 · Kural metninin sabit blokları

Her oyun **aynı sekiz blokta** yazılır. Blok atlanmaz, sırası değişmez.

| # | Blok | Zorunlu | Denetleyen |
|---|---|---|---|
| 1 | Künye (oyuncu · süre · yaş · malzeme · zorluk) | evet | `qa_rules` |
| 2 | Kültürel hikâye (~120 kelime) | evet | `qa_length` |
| 3 | Malzeme ve yerine koyma | evet | `qa_rules` |
| 4 | `Setup: ` — kurulum | evet | `qa_rules` |
| 5 | `Turn sequence: ` — tur sırası, numaralı | evet | `qa_rules` |
| 6 | `Win condition: ` — kazanma koşulu | evet | `qa_rules` |
| 7 | Örnek tur + varyantlar | evet | `qa_rules` |
| 8 | Kaynak künyesi | evet | `validate_research` |

Kural metni ikinci tekil şahısla yazılır: *On your turn, you may…*
Bir tur bittiğinde ne olduğu belirsiz kalmaz.

---

## 3 · Üç soru — cevabı olmayan kural EKSİKTİR

Her oyun bu üç soruyu **açıkça** cevaplar. `edgeCases` bloğu üçü için de
zorunludur ve boş bırakılamaz.

| Soru | Alan | Neden |
|---|---|---|
| **Berabere olursa?** | `edgeCases.tie` | Masadaki en sık tartışma |
| **Kimse hamle yapamazsa?** | `edgeCases.stalemate` | Oyunu kilitleyen durum |
| **Kural dışı hamle yapılırsa?** | `edgeCases.illegalMove` | Çocuklu masada kaçınılmaz |

Bu üçü cevapsızsa oyun `locked` olamaz — ne kadar güzel yazılmış olursa olsun.

---

## 4 · Oynanabilirlik testi

**Ajan bu testi yapamaz.** Testçi insandır.

| Kural | Gerekçe |
|---|---|
| Test **yalnızca kitap metniyle** yapılır | Yazarın kafasındaki bilgi kitapta yoksa yoktur |
| `usedOnlyBookText: false` ise test **geçersizdir** | Yarı-bilgiyle oynanan oyun kanıt değildir |
| Her `locked` oyun için **≥1** geçmiş test | Kapsam kapısı |
| Her ailenin en zor örneği için **≥2** test | Şablonun ölçekte kırılıp kırılmadığı |
| Sonuç `ambiguous` ise **kural metni düzeltilir**, test tekrarlanır | Belirsizlik bir kusurdur |

Test kaydı `01_SOURCE/playtests/<gameId>.json` altında durur ve
`qa_playable.py` tarafından denetlenir.

---

## 5 · "Güzel ama oynanamaz" — bu kitabın ölüm biçimi

Bir maddenin gravürü olağanüstü, kültürel hikâyesi büyüleyici, kaynak
künyesi kusursuz olabilir — ve oyun **çalışmayabilir**.

Bu durumda madde **düşer**. Kitabın kalitesi güzellikte değil,
masada kanıtlanır.

> Faz 1'in 140 adaylık havuzu tam olarak bunun içindir: bir oyun düştüğünde
> yerine koyacak bir şey olsun diye. Havuz bir lüks değil, bir **sigortadır**.

---

## 6 · Kumar çerçevesi kullanılmaz (karar K5)

Bahis mekaniği taşıyan geleneksel oyunlar kitaba **puanla yeniden yazılarak**
girer. Gerekçe editoryaldir, ahlaki değil: bu kitabın kanalları aile, okul ve
kütüphanedir ve kumar çerçevesi o üç kanalı birden kapatır.

Yeniden yazılan her oyun `gamblingReframed: true` taşır ve prozada
bunun yapıldığı **açıkça** söylenir. Gizlenmez.
