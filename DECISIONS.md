# DECISIONS — karar kaydı

> Bu dosya iki şey taşır:
>
> 1. **Alınmış kararlar** (`K##`) — gerekçesiyle, tarihiyle
> 2. **AÇIK KARARLAR** (`A#`) — kurucudan yanıt bekleyen sorular
>
> Kural: bir varsayım sessizce proje gerekliliğine dönüşemez. Pazar
> raporunun vermediği her şey **önce buraya** yazılır.

---

## AÇIK KARARLAR — kurucudan yanıt bekleyen

Durum tablosu · 13 Ağustos 2026 (Faz 1 sonu)

| # | Soru | Aciliyet | Ne zaman kapanmalı | Durum |
|---|---|---|---|---|
| **A1** | Manuscript public depoda mı duracak? | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK — **K9 ile mekanizmaya bağlandı**; onay bekliyor |
| **A2** | 7 aile taksonomisi onayı **+ yeniden dengeleme** | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK — taksonomi yazıldı; öneri hazır |
| **A3** | 100 oyunun nihai listesi | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK — 96 oyunluk **öneri** + 23 yedek üretildi |
| **A4** | Büyük punto sürümü v1.0'a girecek mi | DÜŞÜK | Faz 4 | AÇIK (bootstrap varsayımı: hayır) |
| **A5** | Kalibre edilmiş `STYLE.md` onayı | ORTA | Faz 2 | AÇIK |
| **A6** | Yazar biyografisi metni | ORTA | Faz 5 | AÇIK |
| **A7** | Oyun testçileri kim | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK — **Faz 2 sert bloklayıcısı** |

### A2 · Faz 1 bulgusu — aile hedefleri yeniden dengelensin mi

Av ve kuşatma ailesi 21 aday taşıyor (taban 16 ✅) ama yalnızca **10'u
uygun** — hedef 14'tü. Sebep veri hatası değil araştırma gerçeğidir: tafl
kümesinin kuralları yoktur, kaplan-keçi kümesi tek kaynaklıdır.

| Aile | Mevcut hedef | Önerilen |
|---|---:|---:|
| Av ve kuşatma | 14 | **10** |
| Savaş tahtası | 13 | **17** |

Toplam 100 korunur. **Karşı gerekçe:** av-kuşatma kitabın en görsel ve en
çocuk-dostu ailesidir; küçültmek onu zayıflatır. Alternatif hedefi korumak
ve Faz 2'de dört kaplan-keçi oyununa ikinci bağımsız kaynak aramaktır.

Ayrıntı: [`06_REPORTS/PHASE_1_REPORT.md`](06_REPORTS/PHASE_1_REPORT.md) § 5.

---

### A1 · Manuscript public depoda mı duracak?

Talimat depoyu **public** yapmayı emrediyor. Aynı talimat, yayımlanmamış
manuscript'in "repository public diye otomatik olarak public olmaması"nı da
emrediyor. Üç şık:

| Şık | Ne demek | Sonuç |
|---|---|---|
| **(a)** | Depo public; **proza depo dışında yaşar** (`.gitignore` + içerik denetimi) | Bestiarium D8/D29 ve World Myths K21 kararı. **Bootstrap bunu varsaydı.** |
| (b) | Depo public; proza şifreli/ayrı private submodule'de | Karmaşık; iki depo yönetimi |
| (c) | Depo private; yalnızca yayından sonra public | Talimatın "public repository" emriyle çelişir |

**Bootstrap'ın varsayımı: (a)** — iki önceki projede de bu seçildi ve çalıştı.

### A7 · Oyun testçileri kim

**Bu, Faz 2'nin sert bloklayıcısıdır.** Ajan oynanabilirlik testi yapamaz;
testçi insandır ve yalnızca kitaptaki metni okur.

Testçi bulunamazsa **Faz 2 bloklanır**. Bu kabul edilen bir bloktur:
**sahte test kaydı üretilmez.** `qa_playable.py` `usedOnlyBookText: false`
olan kaydı geçersiz sayar.

---

## ALINMIŞ KARARLAR

### K1 · Ortak kütüphane YOK — üç proje tam izole

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

Üç yeni proje benzer şekilli araçlar kullanır. Yine de ortak bir Python
paketi oluşturulmadı ve her proje kendi kopyasını taşır.

**Gerekçe:** talimat § 31 bir ajanın tek klasörle çalışabilmesini şart
koşuyor. Ortak kütüphane bu kuralı ihlal eder: paylaşılan bir dosyadaki
değişiklik üç projeyi birden kırar ve bir projenin CI'ı başka bir deponun
durumuna bağlanır. **Kopyalanan kod biraz fazlalıktır; bağımlılık ise bir
kırılganlıktır.**

### K2 · Faz kapısı `.gate` dosyasından okunur

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

Kapı seviyesi tahmin edilmez. `qa_all.sh` ve CI aynı dosyayı okur.
`--fix` bayrağı kapıya **dokunmaz** (Bestiarium D3 dersi).

### K3 · İç blok siyah-beyaz

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

KDP premium renk büyük trimde sayfa başına **0,080 $**; 256 sayfa = 21,48 $
baskı maliyeti. 34,99 $ listede telif negatife düşer.

Renk KDP'de bir strateji değil bir **vergidir**. DK/Usborne ile aynı sahada
savaşmak KDP ekonomisiyle mümkün değildir. Cevabımız renk değil,
**gravür dili** — hem maliyet hem marka olarak.

### K4 · Ciltli öncelikli fiyatlama

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

Birim telif ciltlide 10,99 $, ciltsizde 8,44 $. Pazar raporu § 16'nın
bulgusu: reklamın hata payı doğrudan birim teliftir. Ciltli **lansmanla
birlikte** açılır, sonradan eklenmez — sonradan eklenen sürüm biriken
yorumları paylaşamaz.

### K5 · Kumar çerçevesi kullanılmaz

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

Bahis mekaniği taşıyan oyunlar **puanla yeniden yazılarak** girer.
Gerekçe editoryaldir, ahlaki değil: kitabın kanalları aile, okul ve
kütüphanedir ve kumar çerçevesi o üç kanalı birden kapatır.

Yeniden yazılan oyun `gamblingReframed: true` taşır ve prozada bunun
yapıldığı **açıkça** söylenir. Gizlenmez.

### K6 · KDP Select / KU'ya girilmez

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

256 sayfalık tam okuma ≈ 1,23 $ (KENP 0,00482 $ · Nisan 2026), ciltsiz
telif 8,44 $. Münhasırlık karşılığında satış başına **6,9 kat** kayıp.
KU yalnızca hızlı tüketilen seri kurgu için doğru kanaldır.

### K7 · Kalite kapıları üçüncü taraf paket kullanmaz

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

`validate.yml` saniyeler içinde biter. Yazım fazlarında günde onlarca push
olur ve iki dakikalık kurulum beklemek disiplini öldürür. Ağır bağımlılıklar
(Pillow, reportlab) yalnızca görsel ve dizgi işlerine aittir ve
`run_optional` sözleşmesiyle **atlanabilir**.

### K8 · Kapsam sayıları Faz 1'e kadar HİPOTEZDİR

**Tarih:** 12 Ağustos 2026 · **Faz:** bootstrap

Pazar raporunun 100 / 45 / 7 / 256 sayıları `project_config.json § scope`
içinde durur ve `locked: false` taşır. Faz 1 bunları **doğrular veya
değiştirir**. Bir sayıyı Faz 1'de düzeltmek ucuz; Faz 4'te düzeltmek üç
aylık iştir.

**Faz 1 sonucu:** 100 ✅ (119 uygun aday) · 45 ✅ (89 kültür) · 7 ✅ ·
256 ✅ (model 250, −%2,3). Dört sayı da doğrulandı. `scope.locked` **hâlâ
`false`** ve A2/A3 kapanana kadar öyle kalır.

---

### K9 · Veri katmanı public, proza katmanı özel — sınır MEKANİKTİR

**Tarih:** 13 Ağustos 2026 · **Faz:** 1

Faz 1, "manuscript public depoda durmaz" ilkesini bir ayrıma çevirdi:

| Katman | Nerede | Biçim | Depo |
|---|---|---|---|
| **Veri** | `01_SOURCE/` | alanlara bölünmüş kayıt | **public** |
| **Proza** | `02_MANUSCRIPT/` | sekiz sabit blokta sürekli metin | **özel** |

**Sınırı disiplin değil mekanizma çizer.** `validate_structure.py →
check_manuscript_leak()` proza şablonunun etiketlerini arar; takip edilen
bir dosya bunlardan ikisini birden taşırsa CI kırmızı yanar.

**Sonuç iki yönlüdür.** Veri katmanı proza etiketlerini taşıyamaz — bu,
kural kayıtlarının *data* kalmasını zorlar. Aynı zamanda araştırma
künyeleri, taksonomi ve ölçüm raporları public kalabilir; kitabın kaynak
iddiası denetlenebilir olur.

Bu karar A1'i **kapatmaz**, ama A1'in hangi seçenekle cevaplanırsa
cevaplansın mekanik olarak uygulanmasını sağlar.

---

### K10 · Yeniden kurgulama BEYAN EDİLMEDEN yapılamaz

**Tarih:** 13 Ağustos 2026 · **Faz:** 1

Şemanın ilk hâlinde `reconstructed` tek başına bir **etiketti**. Faz 1
pilotu şunu gösterdi: bir etiket, **uydurma ile yeniden kurgulama arasında
mekanik bir fark üretmez.** İkisi de aynı görünür.

Eklenen alan: **`reconstructionPlan`**. Netlik testinden düşen her
`reconstructed` kayıt üç şeyi yazmak zorundadır:

> **hangi boşluk** · **hangi kaynağa dayanarak** · **hangi editoryal kararla**

`qa_rules.py` bunu şart koşar ve planın yalnızca `reconstructed`
kayıtlarda durmasını da denetler (ölü kural yasağı). Sonuç: yeniden
kurgulama **kayıt tutmadan yapılamaz**.

Bu, `STYLE.md § 5`'in ("belirsizlik gizlenmez, yazılır") mekanik
karşılığıdır.

---

### K11 · Kaynak doğrulaması iki seviyelidir

**Tarih:** 13 Ağustos 2026 · **Faz:** 1

Bir eserin adını yazmak, o eseri açıp sayfayı görmekle **aynı şey
değildir**. Faz 1 künye seviyesinde çalıştı ve bunu gizlemek yerine bir
alana bağladı:

| Seviye | Anlamı | Nerede zorunlu |
|---|---|---|
| `bibliographic` | Eser ve içerdiği oyun künyelendi | Faz 1 · aday |
| `page-verified` | Kaynak açıldı, sayfa/locator doğrulandı | **`locked` kapısı** |

`validate_research.py` `locked` bir oyun için `page-verified` ve her
künyede bir `locator` şart koşar. **Doğrulanmamış bir künyenin doğrulanmış
gibi görünmesi mekanik olarak imkânsızdır.**

Aynı betik bağımsızlık sayımını da yapar: aynı yazarın iki eseri **bir**
kaynaktır, ve `lineage` alanı taşıyan türetilmiş bir kaynak bağımsız
sayılmaz.
