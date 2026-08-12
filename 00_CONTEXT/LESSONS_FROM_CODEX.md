# CODEX PROJELERİNDEN DERSLER — bu projeye taşınanlar

> Bu proje `CODEX_BESTIARIUM` ve `THE-GREAT-BOOK-OF-WORLD-MYTHS`'ten
> **tamamen izoledir**. Ortak dosya, ortak build çıktısı, ortak `.gate`,
> ortak rapor yoktur. Onlar yalnızca **referans uygulama** olarak okundu.
>
> Bu belge, okunan sistemden **neyin taşındığını** ve **neden** taşındığını
> kaydeder. Kod taşınmadı; **disiplin** taşındı.

---

## 1 · Taşınan yedi mekanizma

| # | Mekanizma | Nereden | Bu projede karşılığı |
|---|---|---|---|
| 1 | **`.gate` faz kapısı** | ikisi de | `phase0…release`; CI ve `qa_all.sh` buradan okur |
| 2 | **Tek doğruluk kaynağı** | World Myths `project_config.json` | Gömülü sabit değer CI'ı kırmızı yakar |
| 3 | **Kapıların kendi testi** | World Myths `05_TESTS/selftest.py` | Kusurlu kurguyla her kapının ısırdığı kanıtlanır |
| 4 | **İki hatlı sızıntı koruması** | Bestiarium D8/D29 → World Myths | `.gitignore` (yol) + içerik taraması (mekanizma) |
| 5 | **Üretilen belge bayatlık kapısı** | World Myths `--check` | Disiplin unutulur, mekanizma unutmaz |
| 6 | **`run_optional` sözleşmesi** | World Myths `qa_all.sh` | Çıkış 2 = ATLANDI, kalite düşüşü değil |
| 7 | **Ölü muafiyet yasağı** | Bestiarium D28 → World Myths K14 | Her muafiyet selftest'te iki kez denetlenir |

---

## 2 · Taşınan altı ders — bedeli ödenmiş hatalar

### D1 · Yazar adı üç betikte gömülüydü
World Myths Faz 6'da `covers.py`, `epub.py` ve `handoff.py` yazar adını ayrı
ayrı taşıyordu; `metadata.py` yer tutucu basıyordu. Sonuç: aynı kitabın
**kapağı ile metadatası farklı yazar taşıyordu**. Aynı kusur Bestiarium
D17'de de vardı.

→ **Bu projede:** `project_config.json § founder` tek kaynaktır ve
`validate_structure.py § check_embedded` her betiği tarar.

### D2 · Yer tutucu metin KDP tarafından reddedildi
World Myths'te s.231'de `[AUTHOR BIO — founder copy pending]` basılıydı ve
KDP bunu "şablon metni" diye **reddetti**.

→ **Bu projede:** `founder.authorBio` `null` olduğu sürece Faz 6 kapısı
kırmızıdır. Yer tutucu asla üretime giremez.

### D3 · `--fix` kapıyı sessizce düşürüyordu
Bestiarium'da `qa_all.sh --fix` kapı seviyesini `draft`a düşürüyordu — yani
belgeleri tazeleyen koşu **açılmış kapıları hiç denetlemiyordu**.

→ **Bu projede:** kapı yalnızca AÇIKÇA verilirse değişir; `--fix` ona dokunmaz.

### D4 · Muafiyetler sessizce ölüyordu
`.gitignore`'da son eşleşen kural kazanır. World Myths'te muafiyetler yanlış
sırada durduğu için manuscript politikasını **anlatan** README hiç depoya
girmedi — ve o dosya için yazılmış tarama muafiyeti **ölü muafiyet** oldu.

→ **Bu projede:** muafiyetler dosyanın SONUNDA durur ve `selftest § ④`
her muafiyeti iki kez denetler: dosya var mı, muafiyet gerçekten gerekli mi.

### D5 · Bir kapının varlığı, koştuğu anlamına gelmiyordu
World Myths'te `calibrate_pages.py` yazılmıştı ama `qa_all.sh` onu
çağırmıyordu — **ölü betik**. Karar K18 bunu kapattı.

→ **Bu projede:** `qa_all.sh` her betiğin varlığını kontrol edip **koşturur**;
Faz 1–2'de doğacak kapılar için satırlar şimdiden yazılıdır.

### D6 · Yanlış nesneye bağlanmış kusursuz görsel bütün kapılardan geçer
World Myths'te varlık envanteri kalite ölçümünden **önce** koşar: doğru
kültüre bağlanmamış kusursuz bir vinyet, bütün görsel kalite kapılarından
geçiyordu.

→ **Bu projede:** `asset_inventory.py` her zaman `images.py`'den **önce**
koşar; ve bu kitapta risk daha büyüktür — **yanlış oyuna bağlanmış bir tahta
diyagramı, oyunu oynanamaz yapar.**

---

## 3 · Taşınmayanlar — ve nedeni

| Taşınmadı | Neden |
|---|---|
| Bestiarium'un `kin_map` akrabalık sistemi | Bu kitabın tasnifi **mekanik ailesi**dir, motif akrabalığı değil |
| World Myths'in `qa_age.py` yaş politikası | Bu kitabın okuru aile; yaş kapısı yerine **oynanabilirlik** kapısı var |
| Ortak Python kütüphanesi | § 4'e bakınız |

---

## 4 · Neden ortak kütüphane YOK

Üç yeni proje benzer şekilli araçlar kullanır. Yine de **ortak bir paket
oluşturulmadı**. Gerekçe:

> Talimat § 31: *"Bir ajan `THE-GREAT-BOOK-OF-WORLD-GAMES` klasörünü açtığında
> diğer projelere ihtiyaç duymamalıdır."*

Ortak kütüphane bu kuralı ihlal eder: paylaşılan bir dosyadaki değişiklik üç
projeyi birden kırar ve bir projenin CI'ı başka bir deponun durumuna bağlanır.
Kopyalanan kod biraz fazlalıktır; **bağımlılık ise bir kırılganlıktır.**

Karar: `DECISIONS.md § K1`.
