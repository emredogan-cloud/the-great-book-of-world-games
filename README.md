# The Great Book of World Games

**100 Games from 5,000 Years of Human Play — Rules, Boards, and Stories
from 45 Cultures, Ready to Play Tonight**

---

## Bu depo nedir

Bu depo bir **kitap üretim sistemidir**, kitabın kendisi değil.

Oyun rafı ikiye ayrılmış: bir yanda akademik oyun tarihi — otoriter,
güzel, **oynanamaz**. Öbür yanda 9,99 $'lık aile oyunu listeleri —
ucuz, hızlı, **içeriksiz**. Arada hiçbir şey yok.

Bu kitap o boşluğu doldurur: 45 kültürden 100 oyunu **bölgeye göre değil
mekaniğe göre** dizer, her birini kaynak künyesine bağlar ve
**gerçekten oynanabilir** hâlde verir.

Depoda duran şey: **araştırma künyeleri, oyun şeması, doğrulama kapıları,
CI/CD, oynanabilirlik test kayıtları, dizgi ve KDP üretim hattı, ölçüm
raporları ve belgeler.**

Depoda **durmayan** şey: **kitabın prozası.** Yayımlanmamış kural metni
depo dışında yaşar — `.gitignore § ①` ve
[`DECISIONS.md § A1`](DECISIONS.md). Bir yol kalıbı yeni bir ada konan
dosyayı yakalamaz, bu yüzden ikinci bir hat vardır: CI takip edilen
dosyaların **içeriğine** bakar ve kural metni görürse kırmızı yanar.

---

## Durum

| | |
|---|---|
| Faz | **0 · Bootstrap** |
| Kapı (`.gate`) | `phase0` |
| Aday oyun | 0 / ≥140 |
| Kilitli oyun | 0 / 100 |
| Yazılmış oyun | 0 / 100 |
| Görsel | 0 / ~130 |
| **Sonraki adım** | **Faz 1 — kurucu onayı bekliyor** |

Ölçülmüş güncel durum: [`BOOK_STATS.md`](BOOK_STATS.md) ·
[`ROADMAP_PROGRESS.md`](ROADMAP_PROGRESS.md)

---

## Bu kitabın ölüm biçimi

Her kitabın kendine has bir başarısızlık biçimi vardır. Bu kitabınki tektir:

> ### OYUN ÇALIŞMIYOR.

Okur masaya oturur, kuralı okur, oynayamaz. Bu tek kusur alt başlıktaki
vaadi — *Ready to Play Tonight* — doğrudan yalanlar.

Bu yüzden burada oynanabilirlik bir ek denetim değil, **birinci sınıf bir
sistemdir**: [`00_CONTEXT/PLAYABILITY_STANDARD.md`](00_CONTEXT/PLAYABILITY_STANDARD.md)

Hiçbir oyun, **bir insan yalnızca kitaptaki metinle onu oynayana kadar**
`locked` olamaz.

---

## Hızlı başlangıç

```bash
git clone https://github.com/emredogan-cloud/the-great-book-of-world-games.git
cd the-great-book-of-world-games

# Bütün kalite kapıları — CI'ın koştuğu komutun birebir aynısı.
# Hiçbiri venv gerektirmez; hepsi Python standart kütüphanesiyle koşar.
./04_BUILD/qa_all.sh

# Ağır işler (görsel ölçümü, dizgi) için:
python3 -m venv 04_BUILD/.venv
04_BUILD/.venv/bin/pip install -r 04_BUILD/requirements.txt
```

Yeşilse CI de yeşil olur. Kırmızıysa ilerleme yoktur.

---

## Dizin yapısı

```
00_CONTEXT/     proje bağlamı, üslup, kaynak ve oynanabilirlik standardı
01_SOURCE/      oyun envanteri, aile taksonomisi, şema, araştırma, test kayıtları
02_MANUSCRIPT/  kitabın prozası — DEPO DIŞINDA (bkz. README)
03_COVER/       kapak çalışması
03_APLUS/       A+ içerik modülleri
04_BUILD/       doğrulayıcılar, kalite kapıları, üretim hattı
05_TESTS/       kapıların kendi testi ve kurgu üreteci
06_REPORTS/     ölçüm raporları, faz raporları ve kurucu araştırma kaydı
06_FOUNDER_DELIVERY/  kurucunun bulduğu kaynaklar — ham teslim DEPO DIŞINDA
07_ASSETS/      görseller: raw (salt okunur) → processed → print/kindle/web
08_OUTPUT/      üretilmiş yayın dosyaları — depoda durmaz
09_ARCHIVE/     düşen maddeler ve devre dışı sürümler
```

---

## Altı faz

| Faz | Ad | Kapı |
|---|---|---|
| 1 | Envanter, tasnif ve oynanabilirlik mimarisi | `phase1` |
| 2 | Pilot: 12 oyun + kalibrasyon | `phase2` |
| 3 | Üretim bloğu I — Aileler I–IV | `phase3` |
| 4 | Üretim bloğu II — Aileler V–VII + arka madde | `phase4` |
| 5 | Editoryal yakınsama + görsel üretim | `phase5` |
| 6 | Nihai üretim + KDP paketi | `release` |

Tam yol haritası:
[`THE_GREAT_BOOK_OF_WORLD_GAMES_IMPLEMENTATION_ROADMAP.md`](THE_GREAT_BOOK_OF_WORLD_GAMES_IMPLEMENTATION_ROADMAP.md)

---

## İzolasyon

Bu proje `CODEX_BESTIARIUM`, `THE-GREAT-BOOK-OF-WORLD-MYTHS`,
`THE-MYTH-HUNTERS-FIELD-BOOK` ve `CODEX-ENIGMATICA`'dan **tamamen ayrıdır**.
Ortak dosya, ortak build, ortak `.gate` yoktur. Bu depo tek başına
klonlanabilir, test edilebilir ve üretilebilir.

Taşınan disiplin ve gerekçeleri:
[`00_CONTEXT/LESSONS_FROM_CODEX.md`](00_CONTEXT/LESSONS_FROM_CODEX.md)

---

## Lisans ve künye

Yayıncı: **Vâliçe Press** · Belgeler Türkçe, kitap İngilizcedir.
