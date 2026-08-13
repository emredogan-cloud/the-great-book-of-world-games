# OYNANABİLİRLİK TEST KAYITLARI

> **Bu dizin şu anda BOŞTUR ve boş olması bir kusur değil, bir DURUMDUR.**

## Neden boş

Dış oynanabilirlik testi **gerçek insanlarla** yapılır. Faz 2 test
paketini üretti (`01_SOURCE/pilot_tr/`), ama oturumlar **henüz
yapılmadı**. Sonuç gelmeden buraya hiçbir kayıt yazılmaz.

**Sahte kayıt üretmek bu projede iş bitiren bir ihlaldir** (K15).
`04_BUILD/qa_playable.py` kayıtsız hiçbir oyunun `locked` olmasına izin
vermez — yani boş bir dizin kitabı bloklar, ve bloklaması gerekir.

## Kanıt türleri karıştırılamaz

| `evidenceType` | Kim üretir | `locked` kapısında sayılır mı |
|---|---|---|
| `external` | gerçek insan testçi | **EVET** |
| `internal` | ajan · alt-ajan · doğrulayıcı | **HAYIR** |

Ajanın ürettiği her şey `internal`dır. Bu bir aşağılama değil bir
tanımdır: bir kural metnini yazan zihin, o metni okuyup **anlamadığını**
keşfedemez.

## Kayıt biçimi

Dosya adı `<gameId>.json`, içinde `sessions` dizisi:

```json
{
  "gameId": "tablut",
  "sessions": [
    {
      "gameId": "tablut",
      "testerId": "T01",
      "evidenceType": "external",
      "testedVersion": "tr-pilot-v1",
      "language": "tr",
      "startedAt": "2026-08-20T19:05",
      "finishedAt": "2026-08-20T19:47",
      "setupCompletedAt": "2026-08-20T19:14",
      "playerCount": 2,
      "result": "playable",
      "usedOnlyBookText": true,
      "setupConfusion": null,
      "firstMoveClear": true,
      "legalMoveClear": true,
      "victoryClear": true,
      "edgeCasesSeen": {"tie": false, "stalemate": false, "illegalMove": true},
      "edgeCasesAnswered": {"tie": true, "stalemate": true, "illegalMove": true},
      "materialProblems": [],
      "diagramProblems": [],
      "quotedConfusions": [],
      "revisionTriggered": false,
      "freeComment": ""
    }
  ]
}
```

## Yasak alanlar

Testçiyi tanımlayan hiçbir alan yazılmaz: ad, soyad, e-posta, telefon,
adres, doğum tarihi, yaş, fotoğraf, sosyal medya adı, IP, konum.
`qa_playable.py` bunları taşıyan bir kaydı **reddeder**. Testçiyi
korumak da bir kapıdır.

## Bir oturumdan sonra ne olur

1. Testçi `KAYIT_FORMU.md`'yi doldurur.
2. Form buraya JSON olarak işlenir.
3. `result` `ambiguous` ya da `unplayable` ise **kural metni düzeltilir**.
4. Düzeltilen sürüm yeni bir `testedVersion` alır ve **yeniden test edilir**.
5. `revisionTriggered: true` olan her kaydın bir düzeltme karşılığı olmalıdır.

Belirsizlik bir kusurdur, bir yorum farkı değil.
