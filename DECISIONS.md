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

Durum tablosu · 12 Ağustos 2026 (bootstrap)

| # | Soru | Aciliyet | Ne zaman kapanmalı | Durum |
|---|---|---|---|---|
| **A1** | Manuscript public depoda mı duracak? | **YÜKSEK** | **Faz 1 başlamadan** | AÇIK (bootstrap varsayımı: hayır) |
| **A2** | 7 aile taksonomisi onayı | YÜKSEK | Faz 1 sonu | AÇIK |
| **A3** | 100 oyunun nihai listesi | YÜKSEK | Faz 1 sonu | AÇIK |
| **A4** | Büyük punto sürümü v1.0'a girecek mi | DÜŞÜK | Faz 4 | AÇIK (bootstrap varsayımı: hayır) |
| **A5** | Kalibre edilmiş `STYLE.md` onayı | ORTA | Faz 2 | AÇIK |
| **A6** | Yazar biyografisi metni | ORTA | Faz 5 | AÇIK |
| **A7** | Oyun testçileri kim | **YÜKSEK** | **Faz 2 başlamadan** | AÇIK |

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
