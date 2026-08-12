# KAYNAK STANDARDI — The Great Book of World Games

> Bestiarium'un `SOURCING_STANDARD.md` disiplininin **oyunlara uyarlanmış**
> hâli. Neyin kaynak sayıldığını, neyin sayılmadığını ve kısıt taramasının
> nasıl işlediğini tanımlar.
>
> Sürüm 1.0 · Faz 1'de onaylanır

---

## 1 · Kaynak sayılan

| Tip | Örnek | Güven |
|---|---|---|
| `book` | Akademik oyun tarihi monografisi | yüksek |
| `journal` | Hakemli makale | yüksek |
| `museum` | Müze envanter kaydı, sergi künyesi | yüksek |
| `ethnography` | Saha etnografyası, derleme | orta–yüksek |
| `archive` | Arşiv belgesi, tarihsel kural metni | orta–yüksek |
| `field-record` | Doğrudan aktarım kaydı | değişken — künye zorunlu |

## 2 · Kaynak SAYILMAYAN

- Kaynak göstermeyen oyun kuralı siteleri
- Wiki maddeleri (**izleri takip edilebilir**, kendisi kaynak değildir)
- Ticari oyun yayıncılarının pazarlama metni
- Bir başka popüler oyun kitabının kural özeti (ikincil aktarım)
- LLM çıktısı — **hiçbir koşulda**

---

## 3 · İki bağımsız kaynak kuralı

Bir oyun `locked` olabilmek için **≥2 bağımsız** kaynağa dayanmalıdır.

*Bağımsız* = biri diğerinden türememiş. Aynı monografinin iki baskısı
**bir** kaynaktır. Aynı yazarın iki kitabı **bir** kaynaktır.

Tek kaynağı olan oyun `sourceConfidence: low` alır ve ancak kültürel
çeşitlilik gerekçesiyle, prozada açık uyarıyla girebilir.

---

## 4 · Kısıt taraması — bu projenin etik kapısı

Her oyun **dört durumdan birini** alır. Taranmamış oyun envantere giremez.

| Durum | Anlam | Kitapta |
|---|---|---|
| `open` | Serbest; eğlence bağlamında anlatılabilir | ✅ |
| `attributed` | Anlatılabilir ama **kültürel atıf zorunlu** | ✅ + atıf |
| `restricted` | Yaşayan veya kutsal gelenek | ⛔ eğlenceye çevrilemez |
| `excluded` | Kitaba giremez | ⛔ gerekçe kayıtta kalır |

### Neden bu kapı var

Bazı geleneksel "oyunlar" oyun değildir: ritüeldir, kehanettir, yas
uygulamasıdır ya da belirli bir topluluğa ait bir haktır. Bunları
*"bu akşam ailece oynayın"* çerçevesine koymak, kitabın kültürel
otorite iddiasını ilk sayfada yalanlar.

**Tarama araştırmanın İLK adımıdır, son adımı değil.** Bir oyunun
`excluded` olduğunu 130. adayda öğrenmek, ona harcanan bütün araştırmayı
çöpe atar.

### Şüphe hâlinde

Şüphe `excluded` lehine çözülür. 140 adaylık havuz tam olarak bunun için
vardır: bir maddeyi elemek ucuzdur, yanlış bir maddeyi yayımlamak değildir.

---

## 5 · Araştırma → yazım kilidi

```
research.verified != true  →  YAZILAMAZ
```

`validate_research.py` bunu denetler, `qa_crossref.py` manuscript ile
envanteri karşılaştırır. Doğrulanmamış araştırmaya dayanan hiçbir cümle
prozaya giremez.
