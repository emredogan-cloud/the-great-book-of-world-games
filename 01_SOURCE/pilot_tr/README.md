# TÜRKÇE PİLOT — DIŞ OYNANABİLİRLİK TESTİ PAKETİ

> **TEST-ONLY / TURKISH PILOT**
>
> ⚠ Bu dizindeki metinler **ticari ürünün parçası değildir.**
> Kitabın dili **İNGİLİZCEDİR** (karar K16).

## Bu dizin nedir

Kitabın tek vaadi alt başlığındadır: *Ready to Play Tonight.* O vaadi
yalnızca **masada oturan bir insan** doğrulayabilir. Ajan doğrulayamaz.

Bu paket, mevcut testçiler Türkçe konuştuğu için Türkçedir. Başka hiçbir
sebebi yoktur ve geçicidir.

## Neyi kanıtlar, neyi kanıtlamaz

| Kanıtlar | Kanıtlamaz |
|---|---|
| Mekanik çalışıyor mu | İngilizce metnin anlaşılır olduğunu |
| Kurulum yapılabiliyor mu | İngilizce terim seçiminin doğruluğunu |
| İlk hamle atılabiliyor mu | İngilizce cümlenin oyunu değiştirmediğini |
| Kazanan belirlenebiliyor mu | — |
| Berabere / kilit / kural dışı cevaplı mı | — |

> **Türkçe pilotun geçmesi, İngilizce sürümün geçtiği anlamına GELMEZ.**
> Bir kuralın belirsizliği **dilin içinde** yaşar. İki sürüm ayrı ayrı
> test edilir (K16).

## Depoda neden yalnızca bu dosya var

Türkçe pilot da **tam oynanabilir kural metni** taşır — yani yayımlanmamış
prozadır. A1/K12 uyarınca korunur: metinler `.gitignore` ile depo dışında
tutulur, burada yalnızca paketin **yapısı** durur.

## Paketin içeriği

| Dosya | Ne |
|---|---|
| `00_TESTCI_KILAVUZU.md` | Testçinin okuyacağı ilk sayfa |
| `<gameId>.md` | Tek bir oyunun kuralları — testçiye verilen metnin TAMAMI |
| `KAYIT_FORMU.md` | Oturumdan sonra doldurulan form |

## Kayıt nereye gider

Doldurulan formlar `01_SOURCE/playtests/<gameId>.json` dosyalarına
işlenir ve `04_BUILD/qa_playable.py` tarafından denetlenir.

**Sahte kayıt üretmek bu projede iş bitiren bir ihlaldir.** Kayıtlar
yalnızca gerçek oturumlardan doğar.
