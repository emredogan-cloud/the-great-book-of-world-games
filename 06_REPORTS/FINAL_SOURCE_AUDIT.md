# FINAL SOURCE AUDIT

> **The Great Book of World Games** · Faz 5 · yazım fazı kapanış denetimi
> Tarih: 19 Ağustos 2026 · dal: `main` · denetlenen madde: **52**

Kurucu direktifi § 23: yazılmış her madde için kaynağın **var olduğu**,
**kuralı desteklediği**, **kültürü desteklediği** ve **uydurulmuş kanıt
bulunmadığı** denetlenir. Bu dosyanın bütün sayıları `book.json`,
`source_verification.json` ve `scope_lock.json`'dan **ölçülmüştür**.

---

## 1 · TEK BAKIŞTA

| denetim | sonuç |
|---|---|
| Yazılmış madde | **52** |
| Künyesiz madde | **0** ✅ |
| Sayfa numarası veren madde | **41** |
| Sayfa veren ama DOĞRULANMIŞ kaydı olmayan madde | **0** ✅ |
| En az bir `verified` kaydı olan madde | **41** |
| **İki BAĞIMSIZ** `verified` kaydı olan madde | **4** ⚠ |
| Yeniden kurgulanmış madde | **7** (hepsi beyanlı) |
| Beyan uyuşmazlığı (madde ↔ envanter) | **0** ✅ |
| Kültür uyuşmazlığı (madde ↔ kapsam) | **0** ✅ |
| Diyagramsız madde | **11** (hepsinin sebebi kayıtlı) |
| Kültürel atıf ZORUNLU madde (`attributed`) | **15** |
| **Uydurulmuş sayfa numarası** | **0** ✅ |
| **Uydurulmuş künye** | **0** ✅ |

---

## 2 · HAYALET KÜNYE DENETİMİ — sıfır

`qa_manuscript` § ④ şunu denetler: *bir madde sayfa numarası veriyorsa,
o oyunun `source_verification.json` içinde `verified` bir kaydı olmak
ZORUNDADIR.* Sayfa numarası vermek, sayfayı açtığını iddia etmektir.

```
sayfa numarası veren madde        : 41
bunlardan doğrulanmış kaydı olan  : 41
HAYALET KÜNYE                     :  0
```

Sayfa vermeyen 11 madde, sayfası olmayan kaynaklara dayanır (kurucu
kütüphaneci teslimi, K29) ve künyelerinde **sayfa iddia etmezler**.
Bu bir kusur değil bir **tutarlılıktır**: elde olmayan sayfa yazılmaz.

---

## 3 · BAĞIMSIZLIK — kitabın en zayıf noktası, açıkça

**Yalnızca 4 madde iki bağımsız `verified` kayda sahiptir.**

`SOURCING_STANDARD` § 3 bir oyunun `locked` olabilmesi için ≥2 bağımsız
kaynak ister. Bu kitapta **hiçbir oyun `locked` değildir** ve bunun iki
sebebi vardır: dış test yok (§ 7) ve çoğu maddenin ikinci bağımsız
künyesi yok.

### Ölçülen bağımsızlık tuzağı

`oware` iki künye taşır ama **bir** bağımsız kaynağı vardır:

| künye | kökü |
|---|---|
| Murray 1952, ss. 181–182 | Bennett, *in* Rattray, *Religion and Art in Ashanti* (1927) |
| Bell, ss. 116–117 | fig. 106 künyesi: *"redrawn from Rattray's Religion and Art in Ashanti"* |

İkisi de **Rattray 1927'den türer**. § 3 uyarınca bu **BİR** kaynaktır.
Kayıt bunu söyler ve madde `locked` sayılmaz.

Aynı denetim `omweso` için de yapıldı: Zaslavsky'nin kural seti
**Nsimbi 1968 temellidir ve Zaslavsky bunu künyesinde kendisi söyler**.
Wernham'ın *International Omweso Society* özeti de Nsimbi'ye dayanır —
yani **ikinci bağımsız kaynak DEĞİLDİR** ve öyle sayılmadı.

---

## 4 · KÜLTÜR DESTEĞİ — her madde kaynağın KENDİ cümlesiyle

Kurucu direktifi § 11 sert bir kapıdır: *kaynak, iddia edilen kültürü
desteklemelidir.* Bu fazda yazılan on maddenin kültür kanıtı:

| oyun | kaynağın kendi cümlesi |
|---|---|
| `oware` | *"Ashanti, Gold Coast: Wari"* |
| `pallanguzhi` | *"played by the Tamil women of southern India"* |
| `dara` | *"Dara of the Dakarkari people, Nigeria"* |
| `mu-torere` | *"Maoris, New Zealand"* |
| `catch-the-hare` | *"Spain: De cercar la liebre"* |
| `hasami-shogi` | *"This game, also from Japan"* |
| `li-b-el-merafib` | *"played by the Baggara Arabs of the Sudan"* |
| `omweso` | *"played by the Ganda of Uganda"* (Figure 11-4) |
| `jeu-de-dames` | *"first played in the cafés of Paris in 1727"* |
| `turkish-dama` | Bell'in başlığı: *"Turkish draughts"* |
| `bul` | *"the Kekchi Indians of Central America who are descended from the Mayas"* |

### Kültür kapısının REDDETTİKLERİ

Aynı kapı bu fazda **dört maddeyi durdurdu** — dördü de yazılabilirdi:

| oyun | bulunan | neden reddedildi |
|---|---|---|
| `bagh-chal` | Murray'de dört kaplan-keçi maddesi | **dördü de Hindistan**; kapsam Nepalli |
| `game-of-the-goose` | Bell'de TAM kural seti | kurallar **1725 İngiliz levhasından**; kapsam İtalyan |
| `ayoayo` | Zaslavsky'de Yoruba künyesi | *"rules are similar to … wari"* — **çapraz gönderme**, kural seti değil |
| `congklak` | Murray § 7.4.8 (Dakon, Java) | yalnızca çukur ve tohum sayısı; **ekim/alma/bitiş yok** |

### Tek "uyuşmazlık" ve neden uyuşmazlık değil

`set-dilth`: madde **White Mountain Apache** der, kapsam **Apache** der.
Bu bir çelişki değil bir **daraltmadır** — madde kaynağın verdiği daha
dar kültürü yazar. Kayıt korunuyor.

---

## 5 · YENİDEN KURGULAMA — yedi madde, hepsi beyanlı

```
tablut · chaturanga · hnefatafl · patolli · royal-game-of-ur · polis · senet
```

Yedisinin de `reconstructed: true` bayrağı ve `reconstructionNotice`
metni vardır; yedisinin de envanter kaydı `reconstructed` der.
**Beyan uyuşmazlığı: 0.**

### Bu fazın kısmi-kanıt beyanları

Yeniden kurgulama bayrağı taşımayan ama **kaynak boşluğu prozada
söylenen** iki madde:

- **`bul`** — Bell TEK sarı yüz için puan **vermez** (2/3/5/4 var, 1 yok).
  Kitap onu *"hamle yok"* sayar ve bunun **editoryal** olduğunu atış
  bloğunda açıkça yazar.
- **`alquerque`** (henüz yazılmadı) — Bell'in kendi cümlesi:
  *"These rules from the Alfonso manuscript are not sufficient to play a
  game"* ve ardından kendi *"Suggested Additional Rules"*ını verir.
  Yazılırsa **reconstructed** işaretlenmek zorundadır; bu kayıt onu
  şimdiden not eder.

---

## 6 · DİYAGRAMSIZ ON BİR MADDE — sebepleri

| madde | sebep |
|---|---|
| `jan-ken` · `conkers` | tahtasız; diyagram gerekmiyor |
| `shatranj` · `chaturanga` · `tien-gow` · `jianzi` · `sugoroku` · `mbube-mbube` · `astragaloi` | önceki fazlardan; kaynak/dil sınırı kayıtlı |
| **`li-b-el-merafib`** | `track` sınıfının render'ı **yut-nori devresini SABİT çizer** ve `size.stations` okumaz — Sudan sarmalı çizilemedi (K32) |
| **`omweso`** | `pit` sınıfının koordinatı (`row-pit`) **yalnızca A ve B sırasını** tanır; DÖRT sıralı tahta adreslenemiyor |

İkisi de **sayısal kapıdan YEŞİL geçti** ve görsel denetimle yakalandı.
Yanlış bir tahta basmaktansa diyagramsız basmak seçildi (§ 13).

---

## 7 · KÜLTÜREL ATIF ZORUNLU ON BEŞ MADDE

```
tablut · yut-nori · fanorona · awithlaknannai · picaria · zohn-ahl
totolospi · set-dilth · patolli · bao-la-kiswahili · astragaloi · senet
mu-torere · omweso · bul
```

On beşinin de kısıt taraması `attributed`tır ve prozası kültürü
**adıyla** anar. `mu-torere` ayrıca kuralları ortak mal gibi sunmadığını
açıkça söyler.

---

## 8 · KAYNAK KAYITLARI

| | |
|---|---:|
| Toplam doğrulama kaydı | **69** |
| `verified` | **50** |
| `pending` (açıldı, kural yok / kimlik uyuşmuyor) | **10** |
| `blocked` (denendi, erişilemedi) | **9** |
| Kurucu kütüphaneci kaydı | 11 |
| ↳ bağımsız doğrulanmış | **0** (ve kayıt bunu söyler) |

`blocked` kayıtlar **silinmedi**. Finkel, de Voogt, Pollux ve Russ için
projenin erişilemedi kayıtları olduğu gibi durur; hiçbir madde o
eserlerin okunduğunu iddia etmez.

---

## 9 · SONUÇ

```
UYDURULMUŞ KÜNYE      : 0
UYDURULMUŞ SAYFA      : 0
HAYALET SAYFA İDDİASI : 0
DESTEKSİZ KÜLTÜR      : 0
BEYANSIZ KURGULAMA    : 0
```

**52 maddenin 52'si denetimden geçti.** Kitabın zayıf noktası
uydurma değil **bağımsızlıktır**: 52 maddenin 48'inin ikinci bağımsız
künyesi yoktur ve bu, hiçbir oyunun `locked` olamamasının ikinci
sebebidir (birincisi dış testin hiç yapılmamış olmasıdır).
