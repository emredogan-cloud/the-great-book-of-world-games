# KDP GUTTER CORRECTION REPORT

> **The Great Book of World Games** · dal: `main` · kapı: `phase1`
> Tarih: 21 Ağustos 2026 · commit: `9902e01` · **CI: gerçekten koştu ve YEŞİL**
> (bkz. § 15 — `gh run view` ile doğrulandı)

> ⛔ Bu rapor "KDP READY" demiyor. Bu rapor **"LOCAL PREFLIGHT PASSED"**
> diyor — kurucunun kendi talimatının ayırdığı iki cümle. KDP paneline
> dokunulmadı, hiçbir dosya yüklenmedi, prova sipariş edilmedi. Sıradaki
> adım kurucunun gerçek KDP Previewer'ı **yeniden** çalıştırmasıdır.

---

## 0 · Neden bu tur var

Gerçek Amazon KDP Print Previewer'dan gelen bir ret, yerel testlerin
YEŞİL olmasına rağmen geldi:

> *"Insufficient gutter. Books with 160 pages require at least 0.5"
> (12.700mm) for the gutter (inside margin) and at least 0.25" (6.35mm)
> for the outside, top and bottom margins."* — **sayfa 159**

Kurucu talimatı açıktı: **GERÇEK KDP > yerel önceki ön denetim.** Kök
neden kaynakta düzeltildi; sayfa 159 elle yamanmadı.

---

## 1 · Tam KDP hatası

Yukarıdaki alıntı, birebir. Previewer bunu ciltsiz iç blokta, sayfa
159'da bildirdi.

## 2 · Sayfa 159 incelemesi

400 dpi'de render edilip taraf-farkında (sayfa 159 TEK = SAĞ/recto,
iç marj SOL kenardır) ölçüldü:

| | Ölçülen |
|---|---:|
| Sol (gutter) mürekkep mesafesi | **0,4900 in** |
| Gerekli (160 sayfa, 151–300 kademesi) | 0,5000 in |
| Açık | **0,0100 in** |

Tek bir sızıntı bulundu: sayfanın en soldaki mürekkep pikseli y≈5,22 in'de,
3 piksel yükseklikte tek bir glif — bir paragraf bloğu değil. Yakınlaştırma
onu birebir gösterdi: **"Invented Traditions" bölümündeki bir alıntıyı
açan tek tırnak işareti ' ** ("'the Elephant moves in all directions as
far as the driver pleases'"). Aynı 20 pt kalın bölüm başlığı stilini
kullanan önceki iki sayfa (155, 157) TAM 0,5000 in ölçtü — sıfır açık.
Yani stil suçlu değildi; **o tek glif** suçluydu.

## 3 · Kök neden

**İki bağımsız kusur:**

1. **Dizgi.** `04_BUILD/interior.py` iç marjı KDP'nin çıplak asgarisinde,
   **sıfır emniyet payıyla** diziyordu. Liberation Serif'te bazı
   gliflerin (açılış tek tırnağı, italik büyük harf) mürekkebi nominal
   başlangıç noktasının hafifçe SOLUNA taşıyor — bu bir dizgi hatası
   değil, normal bir font çizim gerçeği. Marj tam asgaride durduğu için
   bu küçük taşma yasal sınırı aşabiliyordu. **İkinci bir örnek bağımsızca
   bulundu**: sayfa 15'in standfirst'ündeki italik büyük "A" harfi, aynı
   büyüklükte (0,0100 in) bir açık üretti — desen tek bir glifle sınırlı
   değildi.
2. **Doğrulayıcı.** `04_BUILD/kdp_preflight.py`'nin basılmış PDF'i ölçen
   denetimi `pages` parametresini ALIYOR ama hiç KULLANMIYORDU — dört
   kenarı da çıplak 0,25 in'e karşı ölçüyordu (iç marjı dış/üst/alt'tan
   AYIRMADAN) ve 72 dpi'de rasterliyordu, ki orada 1 piksel ≈ 0,0139 in'dir
   — 0,0100 in'lik bir açık **pikselin altında kalıp yuvarlanarak
   kaybolurdu**. Bu kapı, doğru eşiği bilse bile bu kusuru GÖREMEZDİ.

## 4 · Kaynak seviyesi düzeltme

`04_BUILD/interior.py`:
```python
GUTTER_SAFETY_IN = 0.05   # en kötü ölçülen taşmanın (0,01 in) 5 katı
```
`geometry()` artık `gutter_in(pages) + GUTTER_SAFETY_IN` kullanıyor.
KDP'nin çıplak asgari tablosu (`KDP_GUTTER_IN` / `gutter_in()`, zaten
sayfa-sayısı-türevliydi ve DOĞRUYDU) dokunulmadı — doğrulayıcı hâlâ ona
karşı ölçüyor.

`04_BUILD/kdp_preflight.py`'nin `check_ink()`'i yeniden yazıldı:
sayfa tarafına (tek=recto=iç marj SOL · çift=verso=iç marj SAĞ) göre
gutter/outer'ı AYRI ölçer, gutter asgarisini `interior.gutter_in(pages)`'ten
okur (kopya tablo YOK — tek doğruluk kaynağı), varsayılan çözünürlük
72→300 dpi.

## 5 · Yeni marj modeli

| Alan (160 sayfa) | Önce | Sonra |
|---|---:|---:|
| Ciltsiz iç marj (nominal) | 0,500 in | **0,550 in** (0,500 asgari + 0,050 pay) |
| Ciltli iç marj (nominal) | 0,625 in | **0,675 in** (0,500 asgari + 0,050 pay + 0,125 cilt payı) |
| Dış / üst / alt | 0,500 / 0,625 / 0,625 in | değişmedi (zaten bol boşluklu, hiç başarısız olmadı) |

Kademe tablosu (`gutter_in()`, değişmedi, doğrulandı):

| Sayfa | Asgari |
|---:|---:|
| 149–150 | 0,375 in |
| **151–300** (bu kitap: 160) | **0,500 in** |
| 301–500 | 0,625 in |
| 501–700 | 0,750 in |
| 701–828 | 0,875 in |

## 6 · Nihai ciltsiz sayfa sayısı

**160** (önce: 160). Fazladan 0,05 in gutter, dizgi motorunun mevcut
esnekliği (diyagram bütçesi, sol/sağ dengeleme) tarafından sayfa sayısı
DEĞİŞMEDEN yutuldu. Sayı zorlanmadı — ÖLÇÜLDÜ.

## 7 · Nihai ciltli sayfa sayısı

**160** (önce: 160). Aynı şekilde ölçüldü, zorlanmadı.

## 8 · Ciltsiz gutter sonucu

| | Önce | Sonra |
|---|---:|---:|
| En kötü ölçülen gutter (160 sayfanın tamamı, 300 dpi) | **0,4900 in** (sayfa 15 ve 159) | **0,5400 in** (sayfa 15) |
| Başarısız sayfa sayısı | **16** | **0** |
| Sayfa 159 özelinde | 0,4900 in ⛔ | **0,5400 in** ✅ |

**GUTTER: PASS** (0/160 sayfa başarısız, `kdp_preflight.py` + bağımsız
tam-belge taraması ikisi de doğruladı)

## 9 · Ciltli gutter sonucu

| | Önce | Sonra |
|---|---:|---:|
| En kötü ölçülen gutter (160 sayfanın tamamı, 300 dpi) | 0,6133 in | **0,6633 in** |
| Başarısız sayfa sayısı | 0 (zaten geçiyordu — kendi +0,125 in cilt payı tesadüfen yeterliydi) | **0** |

**GUTTER: PASS**

## 10 · Dış / üst / alt sonuçları

| | Ciltsiz (önce → sonra) | Ciltli (önce → sonra) |
|---|---|---|
| En kötü dış | 0,49 in → 0,49 in (değişmedi — hiç sorun yoktu) | aynı |
| En kötü üst | 0,36 in → 0,36 in | aynı |
| En kötü alt | 0,3467 in → 0,3467 in | aynı |
| Asgari | 0,25 in | 0,25 in |

**OUTSIDE/TOP/BOTTOM: PASS** (ikisinde de, önce ve sonra — bu kenarlar
hiçbir zaman kusurlu değildi; sorun yalnızca gutter'daydı).

## 11 · Regresyon testleri

- **`05_TESTS/selftest.py § ⑬`** (15 yeni denetim, tam süit **229/229**
  yeşil): `gutter_in()` KDP kademe tablosunun her sınırı
  (149/150/**151**/160/300/**301**/500/**501**/700/**701**/828) doğru
  değeri seçiyor; emniyet payı ölçülen en kötü taşmadan (0,01 in) küçük
  değil; `kdp_preflight.py` gutter kuralını `interior.py`'den okuyor,
  kopya tablo yok.
- **`05_TESTS/package_selftest.py`** (2 yeni durum, tam süit **42/42**
  yeşil):
  - *Gerçek kitap regresyonu*: `GUTTER_SAFETY_IN=-0,01` ile ciltsiz
    GERÇEKTEN yeniden dizildi (kaynaktan) ve `kdp_preflight.py`
    çalıştırıldı — **KIRMIZI** (sayfa 159 sınıfı hatanın uçtan uca
    tekrarı; glif taşması yalnızca kötüleştirir, asla iyileştirmez, bu
    yüzden kırılgan değil).
  - *Sentetik eşik hassasiyeti* (§14'ün tam istediği): font glifine
    değil dolgu bir dikdörtgene dayanan minimal bir PDF, `check_ink()`'e
    doğrudan verildi. **0,49 in → KIRMIZI. 0,50 in → YEŞİL.** İkisi de
    doğrulandı. (Gerçek kitaba karşı "tam 0,50 in nominal" testi
    KASITLI OLARAK kullanılmadı: § 2–3'ün kendi bulgusu, gerçek içerikle
    tam nominal asgarinin KIRILGAN bir sınır olduğuydu — bu zaten
    ispatlanmış bir olguyu "geçmeli" diye iddia etmek kırılgan bir test
    üretirdi.)

## 12 · Kapak yeniden üretimi

Sayfa sayısı değişmediği için sırt geometrisi **sayısal olarak aynı**,
ama iç blok sağlama toplamı değiştiği andan itibaren `covers.py --check`
kapağı GEÇERSİZ saydı — ikisi de **kaynaktan yeniden üretildi**, varsayılmadı.

| | Ciltsiz | Ciltli |
|---|---:|---:|
| Sırt (sayfa sayısından, BAĞIMSIZ formül) | 0,3603 in | 0,4600 in |
| Tam sarım | 17,6103 × 11,2500 in | 17,2100 × 11,2500 in |
| Gömülü sanat çözünürlüğü (ÖLÇÜLDÜ) | 5283×3375 px @ 300 ppi | 5163×3375 px @ 300 ppi |
| Güvenli alan / barkod / başlık / yazar / arka kapak | değişmedi, `covers.py --check` ile yeniden doğrulandı | aynı |

Ciltli sırt ciltsizden TÜRETİLMEDİ — `covers.py`'nin iki ayrı formülü
okunarak doğrulandı (`0,002252 in/sayfa` vs `0,0025 in/sayfa + 0,06 in
tahta payı`).

## 13 · Kindle doğrulaması

Kindle'ın baskı gutter'ı YOKTUR ve kural ona UYGULANMADI. Yeniden
dizilmeden sonra bağımsızca doğrulandı:
- Kapak: değişmedi (1600×2560 px, vektör tipografi sağlam).
- EPUB: yeniden üretildi, `epub.py --check` geçti; akışkan biçimde
  baskı gutter kavramı yoktur.
- Bayat sayfa-sayısı iddiası: EPUB/Kindle metadata'sı sayfa sayısı
  basmaz (akışkan biçim), yani bayatlayacak bir şey yoktu.

## 14 · A+ senkronizasyonu

Gerekmedikçe DEĞİŞTİRİLMEDİ. A+ metni oyun/kültür sayısına (56/39) atıf
yapar, sayfa sayısına değil — o sayılar değişmedi. `aplus.py --check`
geçti; `03_APLUS/aplus_content.json` diskte dokunulmadı.

## 15 · CI sonucu

| | Sonuç |
|---|---|
| `interior.py --check` (iki sürüm) | ✅ |
| `covers.py --check` | ✅ |
| `kdp_preflight.py` (yeniden yazıldı, 300 dpi, gutter/dış ayrımı) | ✅ 20/20, iki sürüm |
| `05_TESTS/selftest.py` | ✅ **229/229** (önce 214 — 15 yeni gutter-kademesi denetimi) |
| `05_TESTS/package_selftest.py` | ✅ **42/42** (önce 39 — 2 yeni gutter regresyonu) |
| `./04_BUILD/qa_all.sh --fix` | ✅ **BÜTÜN KAPILAR YEŞİL** |
| Git commit | `9902e01` — 15 dosya, +615/−64 satır |
| Push | ✅ `origin/main` — `fe28537..9902e01` |
| **GitHub Actions (gerçek, uzak)** | ✅ `conclusion: success` — run [`32503011274`](https://github.com/emredogan-cloud/the-great-book-of-world-games/actions/runs/32503011274), `gh run view` ile doğrulandı |

## 16 · Kurucu sonraki eylemi

Yerel boru hattı — sayfa 159'da gerçekten başarısız olan KURALI şimdi
uygulayan yeniden yazılmış bir ön denetim dahil — yeşil. **Bu "yerel ön
denetim geçti" demektir, "KDP hazır" demek DEĞİLDİR.**

**Sonraki eylem:** Gerçek Amazon KDP Print Previewer'ı, yeniden üretilen
`08_OUTPUT/PAPERBACK/GreatBookOfWorldGames_interior_paperback.pdf` (+
kapak) ve ciltli eşdeğerlerine karşı **yeniden çalıştır** ve sayfa 159'un
— ve tüm belgenin — gutter denetimini gerçekten geçtiğini doğrula. Bu
düzeltme turunda hiçbir şey yüklenmedi, gönderilmedi ya da prova sipariş
edilmedi.

---

## Ek — talimatta adı geçen, bu projede bulunmayan araç

Talimat § 19 `qa_design`'i çalıştırılacak kapılar arasında sayıyor.
`git grep` ve `ls 04_BUILD/` bu adda bir dosya olmadığını doğruladı —
muhtemelen kardeş bir projenin adlandırmasından. Kapsadığı alan (tasarım/
düzen denetimi) burada `qa_visual.py` (diyagram/render kapısı) ve şimdi
güçlendirilmiş `kdp_preflight.py`'nin (marj/gutter) birleşimi tarafından
karşılanıyor; bu iki gerçek kapı bu tur boyunca koşturuldu ve yeşil.
