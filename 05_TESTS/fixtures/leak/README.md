# SIZINTI FİKSTÜRLERİ — kasıtlı olarak bozuk

Bu dizindeki dosyalar **kasıtlı sızıntılardır**. Dedektörün onları
yakalaması **beklenir**.

`validate_structure.py` bu dizini depo taramasından çıkarır (aksi hâlde CI
kalıcı kırmızı olurdu). Muafiyet korumayı zayıflatmaz çünkü
`05_TESTS/selftest.py § 6` aynı dosyaları `scan_for_leak()` fonksiyonuna
**doğrudan** verir ve her koşuda şunu ispatlar:

| Fikstür | Beklenen |
|---|---|
| `bad-*.md` | sızıntı **VAR** → CI KIRMIZI olurdu |
| `clean-*.md` | sızıntı **YOK** → CI YEŞİL |

Bir muafiyet ancak kanıt üretiyorsa hak edilmiştir. Bunlar üretir.
