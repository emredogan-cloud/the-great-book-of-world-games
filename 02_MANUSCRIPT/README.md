# 02_MANUSCRIPT — bu dizin neden boş

Bu depo **public**tir. Ama "depo public" ile "manuscript public" aynı şey
değildir.

Yayımlanmamış kural prozası ve kültürel hikâyeler bu depoda **durmaz**:

- `.gitignore § ①` `02_MANUSCRIPT/*` yolunu yok sayar
- `04_BUILD/validate_structure.py → check_manuscript_leak()` takip edilen
  dosyaların **içeriğine** bakar ve kural metni görürse CI'ı kırmızı yakar

İkinci hat neden var: bir yol kalıbı, **yeni bir ada konan** dosyayı
yakalamaz. Politikayı disipline değil mekanizmaya bağlarız.

Manuscript `02_MANUSCRIPT/book.json` olarak **yerelde** yaşar ve ayrıca
yedeklenir. Depoda yalnızca **ölçümleri** durur (`06_REPORTS/`).

Karar ve alternatifler: [`../DECISIONS.md`](../DECISIONS.md) § A1.
