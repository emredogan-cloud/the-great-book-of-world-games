#!/usr/bin/env python3
"""
KURUCU ARAŞTIRMA BOŞLUK KAYDI — The Great Book of World Games
================================================================================
Kurucunun § 3 direktifi: "Yazılamayan HER oyunu, NEDEN yazılamadığını ve
kurucunun TAM OLARAK neyi bulması gerektiğini tek bir yetkili kayda topla."

Bu betik ÜÇ dosya üretir:

  01_SOURCE/founder_research_gap_register.json   makine okunur kayıt
  06_REPORTS/FOUNDER_RESEARCH_GAP_REGISTER.md    oyun oyun kayıt
  06_REPORTS/FOUNDER_RESEARCH_PACK.md            kaynak kaynak araştırma paketi

⚠ İKİ AYRI EKSEN VARDIR VE KARIŞTIRILMAZ (kurucu § 5):

    status  = KAYNAK AVININ kanıt durumu
              BLOCKED        → kaynak DENENDİ ve açılamadı
              SOURCE-PENDING → künye var, HENÜZ denenmedi (engel DEĞİL)
              UNRESOLVED     → kaynak AÇIK ve tam, ama kimlik/kültür uyuşmuyor

    primary = oyunun YAZILAMAMA sebebi (P1…P10)

Bir oyun SOURCE-PENDING olup P2 taşıyabilir: "künyesi var, denenmedi, ama
denendiğinde açılabilir metin bulunma ihtimali düşük". Bunu 'engelli'
demek, Faz 3'ün 'denenmedi = engelli' hatasını tekrarlamak olurdu.

⚠ SAYFA NUMARASI UYDURULMAZ. Bu dosyadaki HER locator, projenin kendi
`source_verification.json` kaydından ya da batch raporundan gelir. Bir
eserin İÇİNDE bir bölümün nerede olduğu BİLİNMİYORSA, bölüm adı verilir
ve sayfa BOŞ bırakılır.

Çıkış kodları:  0 = üretildi / güncel   1 = --check ve dosya bayat
"""
from __future__ import annotations
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

# Faz 5 · Batch 6 kaynak duvarı taramasının A kümesi: elde bulunan kamusal
# alan derlemelerinde GERÇEK isabeti olan ve kurucu müdahalesi GEREKTİRMEYEN
# oyunlar. Bunlar bir ENGEL değil bir SIRA meselesidir ve kayda GİRMEZ.
WRITABLE_NOW = {
    "gilli-danda":        "Culin 1907 · 'Tipcat' — ⚠ kültür tuzağı riski: isabet İNGİLİZ/Kuzey Amerika kaydıdır, sayfa açılmadan yazılamaz",
    "chaupar":            "Culin 1895 · 'Chausar' — ⚠ kültür tuzağı riski: isabet Culin'in KORE cildindedir, sayfa açılmadan yazılamaz",
    "tabula":             "Fiske 1905",
    "nine-holes":         "Gomme 1894",
    "alquerque":          "Fiske 1905",
    "tuknanavuhpi":       "Culin 1907",
    "ludus-latrunculorum": "Falkener 1892 — ⚠ yeniden kurgulama beyanı zorunlu",
}

# Projenin DENEDİĞİ ve AÇAMADIĞI eserler. Bir eser bir kez bu listeye
# girdiyse, ona bağlı HER oyun için engel kanıtlanmış sayılır — aynı
# engelli kaynağa tekrar tekrar zaman harcanmaz (§ 26).
BLOCKED_WORKS = {"Murray, H. J. R., A History of Board-Games",
                 "Murray, H. J. R., A History of Chess",
                 "Bell, R. C.", "Parlett", "Zaslavsky", "de Voogt", "Russ",
                 "Finkel", "Pollux"}

E_RULE = ["setup", "player count", "materials", "board / topology", "first move",
          "legal moves", "turn order", "capture", "objective", "end condition",
          "scoring", "draw condition", "variants"]
E_SRC  = ["author", "title", "edition", "publication year", "exact page",
          "stable locator", "public-domain status"]
E_CULT = ["culture identity", "region", "attribution", "historical context"]
E_RECON = ["reconstruction source", "uncertainty statement", "competing interpretation"]

BLOCKER_NAMES = {
    "P1":  "SOURCE ACCESS BLOCKED",
    "P2":  "SOURCE TEXT UNAVAILABLE",
    "P3":  "RULES INCOMPLETE",
    "P4":  "GAME IDENTITY UNRESOLVED",
    "P5":  "CULTURAL IDENTITY / ATTRIBUTION UNRESOLVED",
    "P6":  "RECONSTRUCTION TOO UNCERTAIN",
    "P7":  "VARIANT CONFLICT",
    "P8":  "SOURCE LOCATOR MISSING",
    "P9":  "FOUNDER-SUPPLIED BUT INCOMPLETE",
    "P10": "OTHER DOCUMENTED BLOCKER",
}


# ═══════════════════════════════════════════════════════════════════════════
# KAYNAK DOSYALARI — kurucunun ALIŞVERİŞ LİSTESİ
# ═══════════════════════════════════════════════════════════════════════════
# İnsan araştırmacı oyun oyun çalışmaz, ESER ESER çalışır: bir kitabı bulur,
# içindeki sekiz maddeyi birden çıkarır. Paket bu birime göre düzenlenir.
#
# `attemptEvidence` alanı DÜRÜSTLÜK KAPISIDIR:
#   attempted-and-refused → proje bu esere erişmeyi DENEDİ ve reddedildi
#   never-attempted       → proje bu eseri HİÇ denemedi; engel VARSAYIMDIR
# Bir eserin erişilemez OLDUĞUNU söylemek ile erişilemez OLABİLECEĞİNİ
# söylemek aynı şey değildir ve bu kayıt ikisini karıştırmaz.

WORKS = {
"murray-1952": dict(
    citation="Murray, H. J. R., A History of Board-Games Other Than Chess "
             "(Oxford: Clarendon Press, 1952)",
    attemptEvidence="attempted-and-refused",
    evidence="archive.org nüshası yalnızca ÖDÜNÇ erişimine açık — HTTP 401 "
             "(source_verification.json · tablut kaydı, 2026-08-13)",
    why="1952 tarihli ve telif altındadır; tam metin indirilemez.",
    route=["Üniversite kütüphanesi — kapalı raf ya da ödünç",
           "archive.org ödünç hesabı (1 saatlik ödünç, sayfa görüntüsü)",
           "İkinci el nüsha — Oxford/Clarendon 1952 ya da Hacker 1978 tıpkıbasımı"],
    ask="Aşağıdaki oyunların GEÇTİĞİ sayfaların taraması ya da fotoğrafı. "
        "Murray oyunları bölüm bölüm ve numaralı alt başlıklarla verir; "
        "her oyun için ilgili alt başlığın TAMAMI gerekir.",
    note="KİTABIN EN YÜKSEK GETİRİLİ TEK KAYNAĞIDIR. Tek başına kayıttaki "
         "52 oyunun 24'ünü açar — geri kalan bütün eserlerin toplamından fazla."),

"parlett-1999": dict(
    citation="Parlett, David, The Oxford History of Board Games "
             "(Oxford: Oxford University Press, 1999)",
    attemptEvidence="attempted-and-refused",
    evidence="telif altında — açık tam metin yok "
             "(source_verification.json · mahjong kaydı, 2026-08-13)",
    why="Telif altındadır; açık erişimli tam metni yoktur.",
    route=["Üniversite kütüphanesi", "archive.org ödünç hesabı",
           "İkinci el nüsha (OUP 1999 ya da Echo Point 2018 tıpkıbasımı)"],
    ask="İlgili oyunların bölümleri. Parlett oyunları AİLE başlıkları altında "
        "toplar; oyun adının geçtiği bölümün tamamı gerekir.",
    note="Şans ailesi tek başına buna bağlıdır ve aile 4/4 hedefinde 3 yazılmıştır."),

"bell-1960": dict(
    citation="Bell, R. C., Board and Table Games from Many Civilizations "
             "(Oxford: Oxford University Press, 1960–1969; Dover tıpkıbasımı 1979)",
    attemptEvidence="attempted-and-refused",
    evidence="telif altında — açık tam metin yok (blockedSources kaydı)",
    why="Telif altındadır. Dover tıpkıbasımı yaygın ve ucuzdur.",
    route=["Dover 1979 tıpkıbasımı — ikinci el piyasada bol ve ucuz",
           "Üniversite kütüphanesi", "archive.org ödünç hesabı"],
    ask="İlgili oyunların maddeleri. Bell her oyunu tahta diyagramıyla ve "
        "kısa kural metniyle verir; madde + diyagram birlikte gerekir.",
    note="EN UCUZ ÇÖZÜM. Dover tıpkıbasımı hâlâ basılıyor."),

"zaslavsky-1973": dict(
    citation="Zaslavsky, Claudia, Africa Counts: Number and Pattern in African "
             "Culture (Boston: Prindle, Weber & Schmidt, 1973)",
    attemptEvidence="attempted-and-refused",
    evidence="telif altında — açık tam metin yok "
             "(source_verification.json · mbube-mbube kaydı, 2026-08-13)",
    why="Telif altındadır.",
    route=["Lawrence Hill Books 1999 üçüncü baskısı — hâlâ basılıyor",
           "Üniversite kütüphanesi", "archive.org ödünç hesabı"],
    ask="Oyun bölümleri (kitabın oyunlara ayrılmış kısmı). Ampe, pilolo ve "
        "shisima için bu eser oyunların TEK künyesidir.",
    note="Afrika kültürlerinin çoğu buna bağlıdır ve altı oyun için TEK kaynaktır — "
         "yani ikinci bağımsız kaynak ayrıca gerekir."),

"russ-2000": dict(
    citation="Russ, Laurence, The Complete Mancala Games Book "
             "(New York: Marlowe & Company, 2000)",
    attemptEvidence="attempted-and-refused",
    evidence="telif altında — açık tam metin yok "
             "(source_verification.json · olinda-keliya kaydı, 2026-08-13)",
    why="Telif altındadır.",
    route=["İkinci el nüsha", "Üniversite kütüphanesi"],
    ask="İlgili ekim oyunlarının maddeleri.",
    note="Ekim ailesinin ikinci en yüksek getirili eseri."),

"devoogt-1997": dict(
    citation="de Voogt, Alex, Mancala Board Games "
             "(London: British Museum Press, 1997)",
    attemptEvidence="attempted-and-refused",
    evidence="telif altında; kamusal alan alternatifi tarandı ve uygun bulunmadı "
             "(source_verification.json · bao-la-kiswahili kaydı)",
    why="Telif altındadır.",
    route=["British Museum Press nüshası", "Üniversite kütüphanesi"],
    ask="oware ve toguz-kumalak maddeleri.",
    note="bao-la-kiswahili İÇİN ARTIK GEREKMİYOR — o oyun kurucu teslimiyle yazıldı."),

"townshend-1979": dict(
    citation="Townshend, Philip, 'Mankala in Eastern and Southern Africa: "
             "A Distributional Analysis', Azania: Journal of the British Institute "
             "in Eastern Africa 14 (1979)",
    attemptEvidence="never-attempted",
    evidence="proje bu makaleyi HİÇ denemedi",
    why="Hakemli dergi makalesi; erişimi kurumsal abonelik gerektirebilir.",
    route=["Taylor & Francis / Azania dergi arşivi (kurumsal erişim)",
           "British Institute in Eastern Africa", "Yazar kopyası / akademik ağ"],
    ask="Makalenin tamamı. Dört ekim oyunu (gebeta, hus, mefuvha, omweso) "
        "için ikinci bağımsız kaynaktır.",
    note="DENENMEDİ — engelli DEĞİL. Kurucu denemeden önce ajan da deneyebilir."),

"beart-1955": dict(
    citation="Béart, Charles, Jeux et jouets de l'Ouest africain, "
             "Mémoires de l'IFAN 42 (Dakar: IFAN, 1955), 2 cilt",
    attemptEvidence="never-attempted",
    evidence="proje bu eseri HİÇ denemedi",
    why="Dakar basımı, dar dağıtımlı, muhtemelen yalnızca basılı.",
    route=["IFAN (Institut Fondamental d'Afrique Noire) — Dakar",
           "Fransız üniversite kütüphaneleri · BnF",
           "Gallica dijital arşivi"],
    ask="yoté ve zamma/sig maddeleri. Béart oyunları saha kaydı olarak verir.",
    note="Fransızca. Batı Afrika savaş tahtası oyunlarının en iyi birinci el kaydı."),

"culin-1900-philippine": dict(
    citation="Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900)",
    attemptEvidence="never-attempted",
    evidence="proje bu makaleyi denemedi; AYNI DERGİNİN 1899 sayısı (Hawaiian "
             "Games) denendi ve yalnızca JSTOR nüshası bulundu",
    why="Dergi makalesi. 1900 tarihlidir ve ABD'de KAMUSAL ALANDADIR — "
        "yani bu bir telif engeli değil, bir dağıtım meselesidir.",
    route=["archive.org — American Anthropologist cilt 2 (1900) ciltli sayısı",
           "Wiley Online Library (eski seri, açık olabilir)",
           "HathiTrust — kamusal alan cildi tam görünür olmalı"],
    ask="sungka ve tapatan bölümleri, sayfa numaralarıyla.",
    note="YÜKSEK GETİRİ · DÜŞÜK MALİYET. Kamusal alandadır ve iki oyun açar."),

"culin-1899-hawaiian": dict(
    citation="Culin, Stewart, 'Hawaiian Games', American Anthropologist 1:2 (1899)",
    attemptEvidence="attempted-and-refused",
    evidence="yalnızca JSTOR nüshası bulundu; tam metin indirilemedi "
             "(sourceHunts · phase5-batch4, 2026-08-16)",
    why="1899 tarihlidir ve KAMUSAL ALANDADIR; engel telif değil DAĞITIMDIR.",
    route=["archive.org — American Anthropologist cilt 1 (1899) ciltli sayısı",
           "HathiTrust tam görünüm", "JSTOR (kurumsal erişim)"],
    ask="kōnane bölümü, sayfa numarasıyla.",
    note="Kamusal alan bir metnin JSTOR arkasında durması bir erişim sorunudur, "
         "bir telif sorunu değil — ve kütüphane erişimiyle çözülür."),

"pollux-onomasticon": dict(
    citation="Pollux, Julius, Onomasticon, Book IX — denetlenebilir modern "
             "edisyon: E. Bethe (ed.), Pollucis Onomasticon (Leipzig: Teubner, 1900–1937)",
    attemptEvidence="attempted-and-refused",
    evidence="açık erişimli denetlenebilir edisyon bulunamadı; Yunanca metin ve "
             "satır numarası olmadan locator verilemez "
             "(source_verification.json · astragaloi kaydı)",
    why="Teubner edisyonunun açık tam metni bulunamadı.",
    route=["archive.org — Bethe Teubner cildi (kamusal alan, 1900–1937)",
           "Perseus Digital Library", "TLG (kurumsal erişim)",
           "Üniversite klasik filoloji kütüphanesi"],
    ask="myinda ve ephedrismos'un geçtiği pasajlar — Yunanca metin + kitap/"
        "bölüm/satır numarası + bir modern çeviri.",
    note="Pollux bir OYUN LİSTESİ verir, bir kural kitabı değildir; kural boşluğu "
         "muhtemelen kaynakla KAPANMAYACAKTIR ve bu ayrıca kaydedilmiştir."),

"alfonso-1283": dict(
    citation="Alfonso X, Libro de los juegos (Libro de acedrex, dados e tablas), "
             "1283 — El Escorial MS T.I.6",
    attemptEvidence="attempted-and-refused",
    evidence="archive.org başlık taraması sonuç vermedi; denetlenebilir açık "
             "transkripsiyon bulunamadı (sourceHunts · phase5-batch4)",
    why="El yazmasının açık erişimli denetlenebilir transkripsiyonu bulunamadı.",
    route=["Real Biblioteca del Monasterio de El Escorial — dijital nüsha",
           "Sonja Musser Golladay, 'Los Libros de Acedrex Dados E Tablas' "
           "(doktora tezi, University of Arizona, 2007) — tam transkripsiyon ve çeviri",
           "Tıpkıbasım edisyonları (Vicent Garcia Editores)"],
    ask="'cercar la liebre' (tavşan kovalama) faslı — folio numarası, "
        "transkripsiyon ve çeviri.",
    note="Golladay tezi ProQuest/üniversite arşivinde AÇIK olabilir ve "
         "hem catch-the-hare hem alquerque için tek kaynakta çözüm olur."),

"best-1925": dict(
    citation="Best, Elsdon, Games and Pastimes of the Maori, Dominion Museum "
             "Bulletin No. 8 (Wellington: Dominion Museum, 1925)",
    attemptEvidence="attempted-and-refused",
    evidence="archive.org'da bulunamadı; NZETC adresi çözülmedi "
             "(sourceHunts · phase5-batch4)",
    why="Dijital nüshası bulunamadı.",
    route=["NZETC — New Zealand Electronic Text Collection (Victoria Univ. of Wellington)",
           "Te Papa Tongarewa / Dominion Museum yayın arşivi",
           "National Library of New Zealand"],
    ask="mū tōrere bölümü — tahta, taş sayısı, hareket kısıtı, kazanma koşulu.",
    note="⚠ mu-torere `attributed` taranmıştır: Māori atfı ZORUNLUDUR. "
         "Kayıt ayrıca ÇAĞDAŞ Māori kaynaklı bir künye istiyor."),

"volpicelli-weiqi": dict(
    citation="Volpicelli, Z., 'Wei-ch'i', Journal of the China Branch of the "
             "Royal Asiatic Society, N.S. XXVI (1894)",
    attemptEvidence="never-attempted",
    evidence="Smith 1908'in KENDİ künyesinde geçiyor; proje henüz aramadı",
    why="Eski dergi cildi; dijital nüshası aranmadı.",
    route=["archive.org — JCBRAS cilt XXVI", "HathiTrust",
           "Royal Asiatic Society China arşivi"],
    ask="Makalenin tamamı — ÇİN biçimini ve ÇİN alan sayımını veren bölüm.",
    note="go'nun kültür uyuşmazlığını çözecek TEK adaydır: Smith 1908 tam bir "
         "kural kitabıdır ama JAPON kodifikasyonunu ve JAPON sayımını verir."),

"murray-1913": dict(
    citation="Murray, H. J. R., A History of Chess (Oxford: Clarendon Press, 1913)",
    attemptEvidence="attempted-and-refused",
    evidence="archive.org — HTTP 401 (ödünç kısıtı) "
             "(source_verification.json · shogi kaydı)",
    why="1913 tarihlidir ve ABD'de KAMUSAL ALANDADIR; engel TELİF değil "
        "DAĞITIMDIR — nüsha ödünç kısıtı altındadır.",
    route=["HathiTrust tam görünüm (kamusal alan cildi)",
           "Google Books tam görünüm", "Üniversite kütüphanesi",
           "Oxford 1913 / Benjamin Press 1985 tıpkıbasımı"],
    ask="makruk (Siyam satrancı) bölümü — taşlar, kurulum, sayma (nap) kuralları.",
    note="Kamusal alan olduğu hâlde açılamayan tek eser bu değildir; bu sınıf "
         "kütüphane erişimiyle en kolay çözülen sınıftır."),

"specialist-articles": dict(
    citation="Uzmanlık makaleleri — tek oyunu açan dar künyeler",
    attemptEvidence="never-attempted",
    evidence="proje bunların hiçbirini denemedi",
    why="Hakemli dergi ya da dar dağıtımlı monografi.",
    route=["Board Game Studies Journal — eski sayıları açık arşivde olabilir",
           "JSTOR / Taylor & Francis (kurumsal erişim)",
           "Yazar kopyası / akademik ağ", "Üniversite kütüphanesi"],
    ask="Aşağıdaki her künye TEK bir oyunu açar:\n"
        "  · Verbeeck, Lieve, 'Bul: A Patolli Game in Maya Lowland', "
        "Board Game Studies 1 (1998) → bul\n"
        "  · Michaelsen, Peter, daldøs ve kuzey yarış oyunları üzerine "
        "çalışmalar, Board Game Studies → daldos\n"
        "  · Schädler, Ulrich, Roma tahta oyunları üzerine çalışmalar, "
        "Board Game Studies → ludus-duodecim-scriptorum\n"
        "  · Davies, R., 'Some Arab Games and Puzzles', Sudan Notes and "
        "Records 8 (1925) → li-b-el-merafib\n"
        "  · Herskovits, Melville J., 'Wari in the New World', Journal of the "
        "Royal Anthropological Institute 62 (1932) → adji-boto\n"
        "  · Pankhurst, Richard, 'Gabata and Related Board Games of Ethiopia "
        "and the Horn of Africa', Ethiopia Observer 14 (1971) → gebeta\n"
        "  · Odeleye, A. O., Ayo: A Popular Yoruba Game (Ibadan: OUP Nigeria, "
        "1977) → ayoayo\n"
        "  · Nsimbi, M. B., Omweso: A Game People Play in Uganda (Los Angeles: "
        "UCLA African Studies Center, 1968) → omweso\n"
        "  · Ascher, Marcia, 'Mu Torere: An Analysis of a Maori Game', "
        "Mathematics Magazine 60:2 (1987) → mu-torere\n"
        "  · Seville, Adrian, The Cultural Legacy of the Royal Game of the "
        "Goose (Amsterdam University Press, 2019) → game-of-the-goose\n"
        "  · Austin, R. G., \"Zeno's Game of τάβλη\", Journal of Hellenic "
        "Studies 54 (1934) → tabula (destek)\n"
        "  · Stanwick, Michael, mahjong kökeni üzerine çalışmalar, "
        "The Playing-Card (IPCS) → mahjong (destek)",
    note="Board Game Studies eski sayıları ve Amsterdam University Press "
         "başlıklarının bir bölümü AÇIK ERİŞİMLİDİR. Denenmeden engelli "
         "sayılmazlar — bu yüzden hepsi SOURCE-PENDING'dir, BLOCKED değil."),

"record-not-found": dict(
    citation="Kaydın KENDİSİ bulunamayan oyunlar — arama görevi kurucuya aittir",
    attemptEvidence="attempted-and-refused",
    evidence="archive.org tam metin + katalog taraması; Thurston 1906 tarandı, "
             "oyun bölümü yok (source_verification.json, 2026-08-14)",
    why="Bir erişim engeli DEĞİLDİR: erişilemeyen bir kayıt yok, HENÜZ UYGUN "
        "BİR KAYIT BULUNAMADI. Hiçbir kütüphane izni bunu var edemez.",
    route=["Kannada/Marathi dilinde dönem folklor derlemeleri",
           "Hindistan bölgesel devlet arşivleri · Karnataka & Maharashtra",
           "Deccan Gymkhana (Pune) arşivi — 1914 kural komitesi",
           "Akhil Maharashtra Shareerik Shikshan Mandal — 1935 kural kitabı",
           "Üniversite Güney Asya koleksiyonları (SOAS · Chicago · Penn)"],
    ask="lagori → 20. yy başı bir saha kaydı ya da dönem folklor derlemesi.\n"
        "kho-kho → 1935 Akhil Maharashtra kural kitabının denetlenebilir nüshası "
        "(ya da 1914 Deccan Gymkhana komite kaydı).",
    note="⚠ Bu iki oyun kapsama K23 kapsam değişikliğiyle GİRDİ ve kaynağı "
         "bulunamadı. Kaynak gelmezse çözüm bir kapsam değişikliğidir, bir "
         "araştırma değil."),

"living-codifications": dict(
    citation="Yaşayan federasyon/kodifikasyon kuralları",
    attemptEvidence="never-attempted",
    evidence="proje FIPJP kural kitabını denemedi",
    why="Yayımlanmış ve erişilebilir; eksik olan KÜNYE (baskı · yıl · madde no) "
        "ve tarihsel çerçevedir.",
    route=["FIPJP resmî kural kitabı (fipjp.org) — sürüm ve yürürlük tarihi ile",
           "Pétanque'ın 1907 La Ciotat kökeni için dönem kaydı ya da "
           "akademik bir spor tarihi çalışması"],
    ask="petanque → (a) FIPJP kural kitabının SÜRÜMÜ ve madde numaraları, "
        "(b) jeu provençal / pétanque ayrımını ve 1907 kodifikasyonunu veren "
        "bağımsız bir tarihsel künye.",
    note="Kayıt zaten uyarıyor: 'modern kodifikasyon 1907'dir; geleneksel "
         "etiketi dikkatle kullanılmalıdır.'"),
}


# ═══════════════════════════════════════════════════════════════════════════
# OYUN KAYITLARI — 52 madde
# ═══════════════════════════════════════════════════════════════════════════
# `need` alanı § 8'in kapısıdır: YALNIZCA o oyun için GERÇEKTEN eksik olan
# maddeler işaretlenir. § 15: elde olan bir şey yeniden istenmez.
#
# Kaynağı hiç açılmamış bir oyun için kural listesinin TAMAMI gerekir —
# çünkü elde yalnızca künye seviyesinde bilgi vardır, kural metni değil.
# Kaynağı KISMEN açılmış oyunlarda (morra · go · oware · halatafl ·
# twelve-mens-morris) liste DARALTILMIŞTIR ve neyin elde olduğu yazılıdır.

ALL_RULES = list(E_RULE)
NO_SCORE  = [x for x in E_RULE if x != "scoring"]
SRC_FULL  = ["author", "title", "edition", "publication year", "exact page",
             "stable locator"]
CULT_MIN  = ["culture identity", "attribution"]
CULT_FULL = list(E_CULT)


def g(st, p, ease, works, why, checked, missing, find,
      s=(), rule=None, src=None, cult=None, recon=None, ideal=None, pat=()):
    return dict(status=st, primary=p, secondary=list(s), ease=ease,
                works=list(works), why=why, checked=list(checked),
                missing=missing, find=list(find),
                need=dict(rule=list(ALL_RULES if rule is None else rule),
                          source=list(SRC_FULL if src is None else src),
                          cultural=list(CULT_MIN if cult is None else cult),
                          reconstruction=list(recon or [])),
                ideal=ideal or "Sayfa-doğrulanmış tarama ya da kararlı kamusal "
                               "adres; künye tam (yazar · başlık · baskı · yıl · sayfa).",
                patterns=list(pat))


# ── ORTAK GEREKÇELER ───────────────────────────────────────────────────────
W_ACCESS = ("Kural metni elde YOKTUR. Envanterdeki `rules-complete` yargısı "
            "KÜNYE seviyesindedir (`sourceVerification: bibliographic`): "
            "kuralların o eserlerde DURDUĞU bilinir, metni okunmamıştır. "
            "§ 5 uyarınca doğrulanmamış araştırmadan tek cümle bile yazılamaz.")
C_SCAN = ["Faz 5 · Batch 6: elde bulunan on kamusal alan derlemesine karşı "
          "tek tek tarandı — isabet yok",
          "Künye seviyesindeki kayıt Faz 1'de kuruldu ve korunuyor"]

ENTRIES = {

# ── BOARDLESS ──────────────────────────────────────────────────────────────
"ampe": g("BLOCKED", "P1", 4, ["zaslavsky-1973"], W_ACCESS,
    C_SCAN + ["Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı"],
    "Zaslavsky bu oyunun TEK künyesidir; açılamadığı için ne kural ne de "
    "ikinci bağımsız kaynak vardır.",
    ["Zaslavsky 1973'te ampe maddesi — sıçrama/ayak biçimi, puanlama, tur, bitiş",
     "GANA KAYNAKLI ikinci bağımsız künye (Akan çocuk oyunları derlemesi)"],
    s=["P2"], pat=['"ampe" Ghana game rules', '"ampe" Akan children\'s game ethnography']),

"ephedrismos": g("BLOCKED", "P6", 0, ["pollux-onomasticon"],
    "Yeniden kurgulama BELİRSİZDİR: kaç atış yapıldığı ve taşıma mesafesi "
    "bilinmiyor; bilinenler heykel ve vazolardan çıkarılmıştır. "
    "§ 13 zayıf kanıtla yazmayı yasaklar.",
    C_SCAN + ["Pollux Onomasticon IX — denetlenebilir açık edisyon bulunamadı",
              "Müze terracotta kayıtları oyunun VARLIĞINI verir, kuralını değil"],
    "Atış sayısı, taşıma mesafesi ve bitiş koşulu hiçbir kaynakta yok.",
    ["Pollux IX'da ephedrismos pasajı — Yunanca metin + satır numarası",
     "Oyunu bir KURAL olarak tarif eden herhangi bir antik pasaj",
     "Modern bir akademik yeniden kurgulama — belirsizlik beyanıyla birlikte"],
    s=["P1"], rule=["first move", "turn order", "scoring", "end condition"],
    recon=E_RECON,
    ideal="Bir klasik filoloji çalışması ya da müze sergi künyesi ki hem "
          "pasajı hem ikonografiyi tartışsın ve NE BİLİNMEDİĞİNİ söylesin.",
    pat=['"ephedrismos" Greek game reconstruction', 'Pollux Onomasticon IX games Bethe edition']),

"kho-kho": g("BLOCKED", "P2", 1, ["record-not-found"],
    "Oyunun oynanabilir biçimi 20. yüzyıl KODİFİKASYONUDUR ve o kodifikasyonun "
    "denetlenebilir bir nüshası bulunamadı. Kayıt VARDIR (1914 komite · 1935 "
    "kural kitabı) ama nüshası yok.",
    ["archive.org katalog + web taraması (2026-08-14) — denetlenebilir edisyon yok",
     "Kayıt kapsama K23 kapsam değişikliğiyle girdi"],
    "1935 Akhil Maharashtra Shareerik Shikshan Mandal kural kitabının nüshası.",
    ["1935 Akhil Maharashtra kural kitabı — tarama ya da kütüphane künyesi",
     "1914 Deccan Gymkhana (Pune) kural komitesinin kaydı",
     "Sekiz kişiden az oyuncuyla oynanan bir UYARLAMA gerekiyorsa, "
     "uyarlamanın MODERN olduğunu söyleyen bir kaynak"],
    ideal="1935 kural kitabının taranmış nüshası, künyesi tam.",
    pat=['"kho kho" 1935 rulebook Akhil Maharashtra', '"kho-kho" Deccan Gymkhana 1914 rules',
         'kho kho indigenous games India codification archive']),

"lagori": g("BLOCKED", "P2", 1, ["record-not-found"],
    "Dönem birinci-el kaydı ARANDI ve BULUNAMADI. Hiçbir kural iddiası "
    "doğrulanmamıştır.",
    ["archive.org tam metin + katalog taraması (2026-08-14)",
     "Thurston 1906 · Ethnographic Notes in Southern India tarandı — oyun bölümü yok",
     "archive.org 1850–1930 başlık taraması sonuç vermedi"],
    "Kannada/Karnataka bağlamında oyunu KURAL seviyesinde veren dönem kaydı.",
    ["20. yy başı bir Güney Hindistan saha kaydı ya da folklor derlemesi",
     "Kannada dilinde bir çocuk oyunları derlemesi",
     "İkinci bağımsız künye"],
    ideal="Dönem etnografyası, sayfa-doğrulanmış, Kannada/Karnataka atfıyla.",
    pat=['"lagori" OR "pittu" OR "lingocha" Karnataka game ethnography',
         'seven stones game South India folklore 1900s archive']),

"morra": g("BLOCKED", "P3", 4, ["parlett-1999"],
    "Erişilebilir kaynak AÇILDI ve mekaniği verdi ama PUANLAMA ve KAZANMA "
    "KOŞULU yoktur. Bir oyun bitişi olmadan basılamaz.",
    ["Falkener 1892 § Atep/Mora, ss. 103–105 AÇILDI: iki biçim kayıtlı "
     "(ikisi birden parmak atar ve ikisi de tahmin eder; ya da biri atar öteki "
     "tahmin eder) ve İTALYAN oyunu adlandırılıyor",
     "Cicero De Officiis III.77 — bir ATASÖZÜDÜR, kural değil",
     "Parlett 1999 telif altında"],
    "Puanlama, kazanma koşulu, tur yapısı ve berabere kuralı.",
    ["Morra'nın PUANLAMASINI ve KAZANMA koşulunu veren herhangi bir künye",
     "Tur yapısı: kaç el oynanır, puan nasıl birikir",
     "Berabere durumunda ne olduğu"],
    s=["P1"],
    rule=["turn order", "scoring", "end condition", "draw condition", "variants"],
    ideal="Bir İtalyan halk oyunları derlemesi ya da Parlett'in morra bölümü.",
    pat=['"morra" Italian finger game rules scoring', '"micatio" mora game history rules',
         'morra gioco regole punteggio storico']),

"myinda": g("BLOCKED", "P1", 2, ["pollux-onomasticon"],
    "Elde açılabilir tek kayıt Gomme'un İNGİLİZ 'Blind Man's Buff' maddesidir "
    "ve bu bir KÜLTÜR TUZAĞIDIR: Antik Yunan maddesini İngiliz kaydından "
    "yazmak kitabın kültür künyesini yalanlar.",
    C_SCAN + ["Gomme 1894 cilt I AÇILDI: 'Blind Man's Buff' İNGİLİZ oyunudur — "
              "kullanılmadı (Batch 4 kaynak avı bunu açıkça kaydetti)",
              "Pollux Onomasticon IX — denetlenebilir açık edisyon bulunamadı"],
    "Antik Yunan biçimini KURAL seviyesinde veren bir kaynak.",
    ["Pollux IX'da myinda/muinda pasajı — Yunanca metin + satır numarası + çeviri",
     "Oyunun Yunan biçimini tarif eden başka bir antik pasaj ya da akademik çalışma",
     "Yunan biçimi ile İngiliz biçimi arasındaki farkı söyleyen bir kaynak"],
    s=["P5"], cult=CULT_FULL,
    pat=['"myinda" OR "muinda" Greek game Pollux', 'ancient Greek blind man\'s buff game evidence']),

"petanque": g("SOURCE-PENDING", "P8", 4, ["living-codifications", "parlett-1999"],
    "Kural metni yayımlanmıştır ve erişilebilir; eksik olan PROJE STANDARDIDIR: "
    "künye (baskı · yıl · madde numarası) ve bağımsız ikinci kaynak. "
    "'Geleneksel' etiketi 1907 kodifikasyonu yüzünden gerekçe ister.",
    ["Parlett 1999 telif altında", "FIPJP kural kitabı HİÇ DENENMEDİ"],
    "FIPJP kural kitabının sürüm künyesi ve oyunun tarihsel çerçevesini "
    "veren bağımsız bir kaynak.",
    ["FIPJP resmî kural kitabı — SÜRÜM, yürürlük tarihi ve madde numaraları",
     "Pétanque'ın 1907 La Ciotat kökenini veren bağımsız tarihsel künye",
     "Jeu provençal ile pétanque arasındaki farkı söyleyen bir kaynak"],
    s=["P1"], rule=["scoring", "end condition", "variants"],
    src=["title", "edition", "publication year", "stable locator"],
    cult=["culture identity", "historical context"],
    ideal="FIPJP kural kitabının PDF'i (sürüm ve tarih görünür) + bir spor "
          "tarihi çalışmasının pétanque bölümü.",
    pat=['FIPJP official rules of petanque PDF version',
         'petanque 1907 La Ciotat origin history jeu provençal']),

"pilolo": g("BLOCKED", "P1", 4, ["zaslavsky-1973"], W_ACCESS,
    C_SCAN + ["Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı"],
    "Zaslavsky bu oyunun TEK künyesidir; ne kural ne ikinci bağımsız kaynak var.",
    ["Zaslavsky 1973'te pilolo maddesi — saklama/arama sırası, puanlama, bitiş",
     "GANA KAYNAKLI ikinci bağımsız künye (Ga çocuk oyunları)"],
    s=["P2"], pat=['"pilolo" Ghana Ga children\'s game rules',
                   'Ga people traditional children games Ghana ethnography']),

# ── CHANCE ─────────────────────────────────────────────────────────────────
"mahjong": g("BLOCKED", "P1", 2, ["parlett-1999", "specialist-articles"],
    "Kaynak DENENDİ ve erişilemedi. Ayrıca puanlama sistemleri bölgeye göre "
    "TAMAMEN farklıdır: doğrulanmamış bir kaynaktan tek sistem seçmek, "
    "seçimin GEREKÇESİNİ de doğrulanamaz kılar.",
    ["Parlett 1999 DENENDİ — telif altında, açık tam metin yok (2026-08-13)",
     "Foster's Complete Hoyle 1897 tarandı — mahjong yok (Batch 4 avı)"],
    "Tek bir DETERMİNİSTİK ruleset ve onun künyesi.",
    ["1920'lerin BİRİNCİ ELDEN bir kural kitabı (Babcock 1920 ve çağdaşları — "
     "ABD'de kamusal alanda olabilir)",
     "Ya da: kitabın basacağı ruleset için kurucu KARARI + o rulesetin künyesi",
     "Puanlamanın sadeleştirilebileceği bir temel biçim (§ K19 sayfa bütçesi: "
     "madde 650 kelimeye SIĞMIYOR ve dört sayfa isteyebilir)"],
    s=["P7"],
    ideal="1920'lerin kamusal alandaki bir kural kitabı + hangi bölgesel "
          "sistemin basılacağına dair açık bir gerekçe.",
    pat=['mahjong 1920 rulebook Babcock public domain archive',
         '"rules for mah-jongg" 1923 archive.org', 'Stanwick mahjong origins Playing-Card']),
}

ENTRIES.update({

# ── HUNT AND SIEGE ─────────────────────────────────────────────────────────
"aadu-puli-attam": g("BLOCKED", "P1", 4, ["bell-1960", "murray-1952"], W_ACCESS,
    C_SCAN + ["Bell ve Murray 1952 proje genelinde DENENDİ ve açılamadı"],
    "İki künyenin ikisi de engelli; kural metni elde yok.",
    ["Bell ya da Murray 1952'de aadu puli attam / puli meka maddesi",
     "Tahta çizimi (üçgen ızgara), keçi ve kaplan sayıları, yerleştirme aşaması, "
     "atlama-alma kuralı, kaplanın kilitlenme koşulu"],
    s=["P4"],
    ideal="Bir madde ki hem tahtayı hem de KAPLAN KİLİTLENMESİ koşulunu versin — "
          "Bagh-Chal ile farkı buradadır ve kitap iki maddeyi ayırmak için "
          "bu farkı yazmak zorundadır.",
    pat=['"aadu puli attam" rules board tigers goats Tamil',
         '"puli meka" game rules South India']),

"bagh-chal": g("BLOCKED", "P1", 4, ["bell-1960", "parlett-1999"], W_ACCESS,
    C_SCAN + ["Bell ve Parlett proje genelinde DENENDİ ve açılamadı"],
    "İki künyenin ikisi de engelli.",
    ["Bell ya da Parlett'te bagh-chal maddesi",
     "5×5 köşegenli tahta, 4 kaplan / 20 keçi, yerleştirme aşaması, "
     "atlama-alma, kaplanların kilitlenmesi, kaç keçi kaybı kaplan galibiyeti"],
    ideal="Nepal kaynaklı çağdaş bir künye ile birlikte olursa kültür atfı da güçlenir.",
    pat=['"bagh chal" rules tigers goats Nepal board game',
         'bagh-chal Nepali traditional game rules ethnography']),

"halatafl": g("BLOCKED", "P3", 2, ["murray-1952"],
    "Erişilebilir kaynak AÇILDI ve oyunun yalnızca ADINI verdi: Fiske 1905'te "
    "halatafl bir SÖZLÜK GÖNDERMESİDİR, kural değil. Ayrıca oyunun "
    "fox-and-geese'ten AYRI bir madde olup olmadığı çözülmemiştir — "
    "fox-and-geese ZATEN YAZILDI ve tekrar riski gerçektir.",
    ["Fiske 1905 'Stray Notes', s. 59 AÇILDI: terimin VARLIĞI doğrulandı, "
     "kural yok (source_verification.json, 2026-08-14)",
     "Fiske'in kitabındaki TEK belgelenmiş tafl oyunu tablut'tur ve o yazıldı",
     "Murray 1952 DENENDİ ve açılamadı"],
    "Kural metninin tamamı ve halatafl'ın fox-and-geese'ten farkı.",
    ["Halatafl'ın KURALINI veren bir kaynak — tahta, taş sayıları, hareket, alma",
     "İzlanda saga/sözlük geleneğinde halatafl'ın ne olduğunu söyleyen bir çalışma",
     "KARAR MALZEMESİ: halatafl fox-and-geese'ten AYRI bir oyun mu? Ayrı değilse "
     "kapsam kaydı bir yedekle değiştirilmelidir"],
    s=["P1", "P4"], cult=CULT_FULL,
    ideal="Bir İskandinav oyun tarihi çalışması ki halatafl ile fox-and-geese "
          "ilişkisini AÇIKÇA tartışsın.",
    pat=['"halatafl" Icelandic fox game rules', 'halatafl saga reference fox and geese Iceland',
         'Icelandic board games hnefatafl halatafl scholarship']),

"len-choa": g("BLOCKED", "P1", 4, ["bell-1960"], W_ACCESS,
    C_SCAN + ["Bell proje genelinde DENENDİ ve açılamadı"],
    "Bell bu oyunun TEK künyesidir; ne kural ne ikinci bağımsız kaynak var.",
    ["Bell'de len choa maddesi — tahta, leopar/hayvan sayıları, hareket, alma, bitiş",
     "TAYLAND KAYNAKLI ikinci bağımsız künye"],
    s=["P2"], pat=['"len choa" Thai leopard game rules', 'Thai traditional board games leopard tiger rules']),

"rimau-rimau": g("BLOCKED", "P1", 4, ["murray-1952", "bell-1960"], W_ACCESS,
    C_SCAN + ["Murray 1952 ve Bell proje genelinde DENENDİ ve açılamadı"],
    "İki künyenin ikisi de engelli.",
    ["Murray 1952 ya da Bell'de rimau-rimau / main rimau maddesi",
     "Tahta (alquerque temelli), kaplan sayısı, av taşı sayısı, çoklu alma kuralı"],
    ideal="Malezya kaynaklı çağdaş bir künye kültür atfını güçlendirir.",
    pat=['"rimau rimau" Malay tiger game rules', '"main rimau" Malaysia traditional board game']),

# ── RACE HOME ──────────────────────────────────────────────────────────────
"ashta-kashte": g("BLOCKED", "P1", 4, ["murray-1952", "bell-1960"], W_ACCESS,
    C_SCAN + ["Murray 1952 ve Bell proje genelinde DENENDİ ve açılamadı"],
    "İki künyenin ikisi de engelli.",
    ["Murray 1952 ya da Bell'de ashta-kashte maddesi",
     "7×7 tahta, işaretli güvenli kareler, dört kavrukemik/deniz kabuğu atışı, "
     "iz yönü, alma, eve giriş koşulu"],
    pat=['"ashta kashte" Bengali race game rules board',
         'ashtapada cowrie race game Bengal rules']),

"bul": g("SOURCE-PENDING", "P2", 3, ["specialist-articles", "bell-1960"],
    "Birincil künye bir hakemli dergi makalesidir ve HİÇ DENENMEDİ; ikinci "
    "künye (Bell) engelli. Oyun `attributed` taranmıştır: Kekchi Maya atfı ZORUNLUDUR.",
    C_SCAN + ["Verbeeck 1998 · Board Game Studies 1 — HİÇ denenmedi",
              "Bell proje genelinde DENENDİ ve açılamadı"],
    "Makale metni: iz uzunluğu, mısır tanesi atışı, çarpışma/öldürme kuralı.",
    ["Verbeeck, Lieve, 'Bul: A Patolli Game in Maya Lowland', Board Game Studies 1 "
     "(1998) — makalenin tamamı",
     "Kekchi Maya atfını ve çağdaş bağlamı veren bir kaynak"],
    s=["P1"], cult=CULT_FULL,
    ideal="Board Game Studies cilt 1 PDF'i — dergi eski sayılarını açık arşivde "
          "tutuyor olabilir.",
    pat=['Verbeeck "Bul" Patolli Maya Board Game Studies 1998 PDF',
         '"bul" OR "boolik" Kekchi Maya game rules']),

"daldos": g("SOURCE-PENDING", "P2", 3, ["specialist-articles", "parlett-1999"],
    "Birincil künye bir dergi çalışmasıdır ve HİÇ DENENMEDİ; ikinci künye "
    "(Parlett) engelli.",
    C_SCAN + ["Michaelsen · Board Game Studies — HİÇ denenmedi",
              "Parlett proje genelinde DENENDİ ve açılamadı"],
    "Kural metni: tahta biçimi, dört yüzlü çubuk zar, taş hareketi, alma.",
    ["Michaelsen, Peter — daldøs ve ilgili kuzey yarış oyunları üzerine "
     "Board Game Studies makalesi",
     "Daldøs ile Sámi sáhkku arasındaki ilişkiyi TARTIŞAN ama KÖKEN İDDİASI "
     "YAPMAYAN bir kaynak (kayıt bu iddiayı açıkça yasaklıyor)"],
    s=["P1"],
    ideal="Board Game Studies makalesi PDF'i + Danimarka müze nesne kaydı.",
    pat=['Michaelsen daldøs Board Game Studies PDF', '"daldøs" OR "daldosa" game rules Denmark',
         'sáhkku daldøs Nordic race game scholarship']),

"game-of-the-goose": g("SOURCE-PENDING", "P1", 3, ["parlett-1999", "specialist-articles"],
    "Her iki künye de telif altındadır; biri (Parlett) DENENDİ ve açılamadı, "
    "öteki (Seville 2019) hiç denenmedi.",
    C_SCAN + ["Parlett DENENDİ ve açılamadı", "Seville 2019 — HİÇ denenmedi"],
    "Kanonik 63 haneli izin hane hane anlamı ve ceza kuralları.",
    ["Seville, Adrian, The Cultural Legacy of the Royal Game of the Goose "
     "(Amsterdam University Press, 2019) — AUP başlıklarının bir bölümü AÇIK ERİŞİMLİDİR",
     "63 hanenin kanonik listesi: kaz haneleri, köprü, han, kuyu, labirent, "
     "hapishane, ölüm ve her birinin cezası",
     "Fazla atışın geri sayılması kuralı"],
    ideal="AUP açık erişim PDF'i ya da bir dönem oyun tahtasının müze künyesi + "
          "basılı kural metni.",
    pat=['Seville "Cultural Legacy of the Royal Game of the Goose" open access PDF',
         '"game of the goose" 63 spaces rules historical', 'giuoco dell\'oca regole storiche 63']),

"li-b-el-merafib": g("SOURCE-PENDING", "P2", 3, ["specialist-articles", "bell-1960"],
    "Birincil künye 1925 tarihli bir bölgesel dergidir ve HİÇ DENENMEDİ; "
    "ikinci künye (Bell) engelli.",
    C_SCAN + ["Davies 1925 · Sudan Notes and Records 8 — HİÇ denenmedi",
              "Bell proje genelinde DENENDİ ve açılamadı"],
    "Sarmal izin uzunluğu, sırtlan ve anne taşlarının kuralı, kuyu kuralı.",
    ["Davies, R., 'Some Arab Games and Puzzles', Sudan Notes and Records 8 (1925) — "
     "makalenin tamamı",
     "Sarmal iz, 'anne' taşı, sırtlanın serbest kalma koşulu ve kuyuya varma kuralı"],
    s=["P1"],
    ideal="1925 tarihli makale kamusal alanda olabilir; ciltli dergi taraması ideal.",
    pat=['Davies "Some Arab Games and Puzzles" Sudan Notes Records 1925',
         '"hyena game" Sudan spiral race game rules', '"li\'b el merafib" rules']),

"ludus-duodecim-scriptorum": g("SOURCE-PENDING", "P6", 1, ["specialist-articles", "murray-1952"],
    "Yeniden kurgulama BELİRSİZDİR: taşların iz üzerindeki YÖNÜ ve başlangıç "
    "yerleşimi kesin bilinmiyor. Tahta yazıtları kural değil, SÖZ OYUNUDUR — "
    "yani en çok bulunan kanıt en az kural taşıyan kanıttır.",
    C_SCAN + ["Murray 1952 DENENDİ ve açılamadı",
              "Schädler · Board Game Studies — HİÇ denenmedi"],
    "İz yönü, başlangıç yerleşimi ve alma kuralı — hiçbiri kesin değil.",
    ["Schädler, Ulrich — Roma tahta oyunları üzerine Board Game Studies çalışması",
     "XII scripta için önerilmiş yeniden kurgulamalar ve ARALARINDAKİ FARK",
     "Tabula ile XII scripta arasındaki tarihsel geçişi veren bir kaynak"],
    s=["P1"], recon=E_RECON,
    ideal="Rakip yeniden kurgulamaları KARŞILAŞTIRAN bir çalışma — kitap tek "
          "yorum seçecek ve seçtiğini beyan edecek.",
    pat=['Schädler ludus duodecim scriptorum reconstruction Board Game Studies',
         'XII scripta Roman game reconstruction rules scholarship']),

"nard": g("SOURCE-PENDING", "P2", 3, ["murray-1952"],
    "Birincil künye engelli (Murray 1952); ikinci künye bir Orta Farsça "
    "ANLATIDIR (Wizārišn ī Chatrang), kural metni değil, ve hiç denenmedi.",
    C_SCAN + ["Murray 1952 DENENDİ ve açılamadı",
              "Wizārišn ī Chatrang ud Nihišn ī Nēw-Ardaxšīr — HİÇ denenmedi"],
    "Nard'ın DÖNEM kural metni: tahta, taş sayısı, zar, iz yönü, alma, bitiş.",
    ["Nard'ın ORTAÇAĞ kural metni — Arapça/Farsça bir dönem kaydı ya da onu "
     "aktaran akademik bir çalışma",
     "Wizārišn ī Chatrang'ın çevirisi — oyunun kozmolojik çerçevesi için "
     "(kültürel hikâye bölümüne girer)",
     "KARAR MALZEMESİ: nard, tabula ve tavla kitapta ÜÇ ayrı madde mi olmalı? "
     "Kayıt tekrar riskini işaretliyor"],
    s=["P1"], cult=CULT_FULL,
    ideal="Bir Fars/Arap oyun tarihi çalışması ki hem kuralı hem kozmolojik "
          "çerçeveyi versin.",
    pat=['"nard" Persian backgammon medieval rules text',
         'Wizarisn i Chatrang translation nard chess Middle Persian',
         'nardshir medieval Arabic backgammon rules scholarship']),
})

ENTRIES.update({

# ── SOWING ─────────────────────────────────────────────────────────────────
# ⚠ KİTABIN EN BÜYÜK AÇIĞI. Aile hedefi 14, yazılan 2, engelli 12.
"adji-boto": g("SOURCE-PENDING", "P2", 3, ["specialist-articles", "russ-2000"],
    "Birincil künye 1932 tarihli bir antropoloji dergisidir ve HİÇ DENENMEDİ; "
    "ikinci künye (Russ 2000) engelli. Oyun `attributed` taranmıştır: "
    "Ndyuka Maroon atfı ZORUNLUDUR.",
    C_SCAN + ["Herskovits 1932 · JRAI 62 — HİÇ denenmedi",
              "Russ 2000 proje genelinde DENENDİ ve açılamadı"],
    "Çukur dizilimi, ekim yönü, alma kuralı ve Ndyuka bağlamı.",
    ["Herskovits, Melville J., 'Wari in the New World', Journal of the Royal "
     "Anthropological Institute 62 (1932) — makalenin tamamı",
     "Ndyuka Maroon topluluğunun oyunla ilişkisini veren çağdaş bir kaynak "
     "(atıf zorunluluğu için)"],
    s=["P1"], cult=CULT_FULL,
    ideal="1932 makalesi kamusal alanda olabilir; JRAI ciltli sayısı ideal.",
    pat=['Herskovits "Wari in the New World" JRAI 1932 PDF',
         '"adji boto" Ndyuka Maroon Suriname game rules']),

"ayoayo": g("SOURCE-PENDING", "P2", 3, ["specialist-articles", "zaslavsky-1973"],
    "Birincil künye Nijerya basımı dar dağıtımlı bir monografidir ve HİÇ "
    "DENENMEDİ; ikinci künye (Zaslavsky) engelli.",
    C_SCAN + ["Odeleye 1977 — HİÇ denenmedi",
              "Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı"],
    "Ayò'nun ekim ve alma kuralı ve Oware'den FARKI.",
    ["Odeleye, A. O., Ayo: A Popular Yoruba Game (Ibadan: Oxford University "
     "Press Nigeria, 1977) — kural bölümü",
     "KARAR MALZEMESİ: Ayòayò ile Oware kitapta AYRI maddeler mi? Kayıt "
     "mekanik yakınlığı ve tekrar riskini işaretliyor — farkı yazan bir kaynak gerekir"],
    s=["P1"],
    pat=['Odeleye "Ayo: A Popular Yoruba Game" 1977', '"ayoayo" OR "ayò" Yoruba mancala rules']),

"bohnenspiel": g("BLOCKED", "P1", 4, ["murray-1952", "bell-1960"], W_ACCESS,
    C_SCAN + ["Murray 1952 ve Bell proje genelinde DENENDİ ve açılamadı"],
    "İki künyenin ikisi de engelli.",
    ["Murray 1952 ya da Bell'de Bohnenspiel maddesi — 2×6 çukur, 6'şar tohum, "
     "ekim yönü, 2/4/6 alma kuralı, zincirli alma",
     "Oyunun Avrupa'ya nasıl ulaştığına dair BİR İDDİA DEĞİL, bir kayıt "
     "(kayıt köken iddiasını açıkça yasaklıyor)"],
    ideal="Alman kaynaklı bir dönem kaydı köken sorununu da hafifletir.",
    pat=['"Bohnenspiel" German mancala rules Murray', 'das Bohnenspiel Regeln historisch Saatspiel']),

"congklak": g("BLOCKED", "P1", 4, ["murray-1952", "russ-2000"], W_ACCESS,
    C_SCAN + ["Murray 1952 ve Russ 2000 proje genelinde DENENDİ ve açılamadı"],
    "İki künyenin ikisi de engelli.",
    ["Murray 1952 ya da Russ 2000'de congklak/congkak/dakon maddesi",
     "Çukur sayısı, depo (rumah) kuralı, eş zamanlı başlangıç olup olmadığı, "
     "ekim yönü, alma, tur sonu ve yeniden dizme kuralı",
     "KARAR MALZEMESİ: sungka ile mekanik farkı — kitap ikisini ayrı madde "
     "yapacaksa farkı yazmalı"],
    pat=['"congklak" OR "congkak" OR "dakon" Javanese mancala rules',
         'congkak Malay Indonesian sowing game rules ethnography']),

"gebeta": g("SOURCE-PENDING", "P2", 3, ["specialist-articles", "townshend-1979"],
    "İki künyenin ikisi de hakemli dergi makalesidir ve İKİSİ DE HİÇ DENENMEDİ. "
    "Bu oyun kayıtta engelli KANITI olmayan az sayıdaki maddeden biridir.",
    C_SCAN + ["Pankhurst 1971 · Ethiopia Observer 14 — HİÇ denenmedi",
              "Townshend 1979 · Azania 14 — HİÇ denenmedi"],
    "Gabata biçimlerinin hangisinin basılacağı ve o biçimin kural metni.",
    ["Pankhurst, Richard, 'Gabata and Related Board Games of Ethiopia and the "
     "Horn of Africa', Ethiopia Observer 14 (1971) — makalenin tamamı",
     "Townshend 1979 · Azania 14 — ikinci bağımsız kaynak olarak",
     "⚠ Kayıt uyarıyor: kaya oyulmuş tahtaların TARİHLENDİRMESİ tartışmalıdır; "
     "kitap kesin tarih VERMEYECEK — kaynak bunu desteklemeli"],
    cult=CULT_FULL,
    ideal="Pankhurst makalesi + Amhara atfını veren çağdaş bir kaynak.",
    pat=['Pankhurst "Gabata" Ethiopia Observer 1971 board games',
         '"gebeta" OR "gabata" Ethiopian mancala rules Amhara',
         'Townshend Mankala Eastern Southern Africa Azania 1979']),

"hus": g("SOURCE-PENDING", "P2", 3, ["murray-1952", "townshend-1979"],
    "Birincil künye (Murray 1952) engelli; ikincisi (Townshend 1979) HİÇ "
    "DENENMEDİ. Oyun `attributed` taranmıştır: Nama atfı ZORUNLUDUR.",
    C_SCAN + ["Murray 1952 DENENDİ ve açılamadı", "Townshend 1979 — HİÇ denenmedi"],
    "Dört sıralı tahtanın kural metni ve Nama bağlamı.",
    ["Murray 1952 ya da Townshend 1979'da hus/ǁhus maddesi — dört sıra, "
     "ekim yönü, alma koşulu, bitiş",
     "Nama topluluğu atfını veren bir kaynak (atıf zorunluluğu için)"],
    s=["P1"], cult=CULT_FULL,
    pat=['"hus" Nama mancala four row rules Namibia',
         'Townshend Mankala Azania 1979 hus ohus']),

"mefuvha": g("SOURCE-PENDING", "P2", 3, ["zaslavsky-1973", "townshend-1979"],
    "Birincil künye (Zaslavsky) engelli; ikincisi (Townshend 1979) HİÇ "
    "DENENMEDİ. Oyun `attributed` taranmıştır: Venda atfı ZORUNLUDUR.",
    C_SCAN + ["Zaslavsky 1973 DENENDİ ve açılamadı", "Townshend 1979 — HİÇ denenmedi"],
    "Dört sıralı tahtanın kural metni ve Venda bağlamı.",
    ["Zaslavsky 1973 ya da Townshend 1979'da mefuvha/muravharavha maddesi",
     "Venda topluluğu atfını veren bir kaynak"],
    s=["P1"], cult=CULT_FULL,
    pat=['"mefuvha" OR "muravharavha" Venda game rules South Africa',
         'Venda traditional board game four row mancala']),

"omweso": g("SOURCE-PENDING", "P2", 3, ["specialist-articles", "townshend-1979", "russ-2000"],
    "Birincil künye 1968 tarihli dar dağıtımlı bir monografidir ve HİÇ "
    "DENENMEDİ; üçüncü künye (Russ 2000) engelli. Oyun `attributed` "
    "taranmıştır: Ganda atfı ZORUNLUDUR.",
    C_SCAN + ["Nsimbi 1968 — HİÇ denenmedi", "Townshend 1979 — HİÇ denenmedi",
              "Russ 2000 DENENDİ ve açılamadı"],
    "Dört sıralı tahtanın tam kural metni — omweso alma kuralları karmaşıktır.",
    ["Nsimbi, M. B., Omweso: A Game People Play in Uganda (Los Angeles: UCLA "
     "African Studies Center, 1968) — kural bölümü",
     "Başlangıç dizilimi, ekim yönü, alma koşulu, emitwe (özel hamle) kuralı, bitiş",
     "Ganda atfını veren çağdaş bir kaynak"],
    s=["P1"], cult=CULT_FULL,
    ideal="Nsimbi 1968 — oyunun en yetkili tek kaynağıdır ve UCLA yayınıdır.",
    pat=['Nsimbi "Omweso: A Game People Play in Uganda" 1968 PDF',
         '"omweso" OR "mweso" Ganda Uganda mancala rules four row']),

"sungka": g("SOURCE-PENDING", "P2", 4, ["culin-1900-philippine", "murray-1952"],
    "Birincil künye 1900 tarihli bir dergi makalesidir — KAMUSAL ALANDADIR — "
    "ama proje onu HİÇ DENEMEDİ; ikinci künye (Murray 1952) engelli.",
    C_SCAN + ["Culin 1900 · 'Philippine Games', American Anthropologist 2:4 — "
              "HİÇ denenmedi (AYNI derginin 1899 Hawaiian sayısı denendi ve "
              "yalnızca JSTOR nüshası bulundu)",
              "Murray 1952 DENENDİ ve açılamadı"],
    "Culin'in sungka bölümü — çukur sayısı, depo kuralı, ekim yönü, alma.",
    ["Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900) — "
     "sungka bölümü, SAYFA NUMARASIYLA (proje bu makalenin sayfa aralığını "
     "henüz görmedi ve tahmin etmiyor)",
     "KARAR MALZEMESİ: congklak ile mekanik farkı — varyant kutusuna mı sığar, "
     "ayrı madde mi olmalı?"],
    s=["P1"],
    ideal="American Anthropologist cilt 2 (1900) ciltli sayısının taraması — "
          "kamusal alandadır ve archive.org/HathiTrust'ta olması beklenir.",
    pat=['Culin "Philippine Games" American Anthropologist 1900 archive.org',
         'American Anthropologist volume 2 1900 full text archive',
         '"sungka" Visayan Philippine mancala rules Culin']),

"toguz-kumalak": g("BLOCKED", "P1", 3, ["russ-2000", "devoogt-1997"],
    W_ACCESS + " Ayrıca MODERN SPOR KURALLARI ile 19. yüzyıl derlemeleri "
    "arasındaki fark ÖLÇÜLMEMİŞTİR ve kitabın hangisini basacağı belirsizdir.",
    C_SCAN + ["Russ 2000 ve de Voogt 1997 proje genelinde DENENDİ ve açılamadı"],
    "Kural metni ve hangi kural katmanının (dönem mi, modern spor mu) basılacağı.",
    ["Russ 2000 ya da de Voogt 1997'de toguz kumalak maddesi — 2×9 çukur, "
     "9'ar tohum, tuzdyk (kutsal çukur) kuralı, kazan, alma koşulu, bitiş",
     "19. yüzyıl bir Orta Asya kaydı — modern spor kodifikasyonuyla FARKI ölçmek için",
     "Kazak atfını veren bir kaynak"],
    s=["P7"], cult=CULT_FULL,
    ideal="Hem dönem kaydını hem modern kodifikasyonu tartışan bir çalışma.",
    pat=['"toguz kumalak" OR "togyz kumalak" rules tuzdyk Kazakh',
         'toguz korgool Kyrgyz Kazakh mancala historical rules']),
})

ENTRIES.update({

# ── LINE AND TERRITORY ─────────────────────────────────────────────────────
"go": g("UNRESOLVED", "P5", 3, ["volpicelli-weiqi", "murray-1952"],
    "KAYNAK TAM AMA KÜLTÜR UYUŞMUYOR. Smith 1908 (ss. 24–26) EKSİKSİZ bir "
    "kural kitabıdır — sıra, yerleştirme, ko, taşların bir daha oynanmaması, "
    "toprak amacı — ama JAPON kodifikasyonunu ve JAPON SAYIMINI (alınan "
    "taşlarla toprağı doldurma) verir, Çin ALAN sayımını değil. Kapsam kaydı "
    "HAN ÇİNLİSİ der. § 9'un 'kaynak iddia edilen kültürü desteklemeli' şartı "
    "KARŞILANMIYOR.",
    ["Smith 1908 'Rules of Play' ss. 24–26 AÇILDI ve TAM kural seti doğrulandı",
     "Falkener 1892 Bölüm XXIII ss. 239–240 AÇILDI: 19×19, taşlar konduktan "
     "sonra hareket etmez, bağlantı yalnızca çizgi boyunca",
     "Murray 1952 · Parlett 1999 · Shotwell 2003 — üçü de erişilemedi",
     "Culin 1895 tarandı — Çin biçimi için kural seti yok"],
    "ÇİN biçimini ve ÇİN ALAN SAYIMINI veren bir kaynak.",
    ["Volpicelli, Z., 'Wei-ch'i', Journal of the China Branch of the Royal "
     "Asiatic Society N.S. XXVI (1894) — Smith'in KENDİ künyesinde geçiyor",
     "Ya da: Çin alan sayımını (taş + çevrelenen boş kesişim) veren başka "
     "herhangi bir denetlenebilir kaynak",
     "⚠ ALTERNATİF ÇÖZÜM — KURUCU KARARI: maddenin kültür künyesi JAPON "
     "olarak değiştirilirse Smith 1908 ZATEN YETERLİDİR ve oyun BUGÜN yazılır. "
     "Bu bir araştırma değil bir karardır.",
     "KARAR MALZEMESİ: kitap 9×9 mı 19×19 mu basacak? 650 kelimede 19×19 "
     "öğretilemez; 9×9 seçimi EDİTORYALDİR ve gerekçesi yazılmalıdır"],
    s=["P7"],
    rule=["scoring"], src=["author", "title", "publication year", "exact page", "stable locator"],
    cult=CULT_FULL,
    ideal="Volpicelli makalesi — hem Çin biçimini hem Çin sayımını verir ve "
          "kültür uyuşmazlığını tek hamlede kapatır.",
    pat=['Volpicelli "Wei-chi" Journal China Branch Royal Asiatic Society 1894',
         'weiqi Chinese area scoring rules 19th century source',
         'wei-ch\'i Chinese go rules historical article archive.org']),

"luk-tsut-kei": g("BLOCKED", "P2", 3, ["murray-1952"],
    "Elde bulunan derlemelerde KULLANILABİLİR isabet yok. Culin 1895 Kore "
    "cildidir ve Çin maddeleri yalnızca KARŞILAŞTIRMA notudur — aynı sınıf "
    "tuzak xiangqi, tien-gow ve jianzi'de üç kez ölçüldü.",
    C_SCAN + ["Culin 1895 · Korean Games tarandı — Kanton biçimi için "
              "kullanılabilir kural seti bulunamadı",
              "Murray 1952 DENENDİ ve açılamadı"],
    "Kanton kaynaklı ya da Çin biçimini açıkça veren bir kural kaydı.",
    ["Murray 1952'de luk tsut k'i maddesi",
     "Ya da: Çin/Kanton kaynaklı bir üç-taş oyunu kaydı",
     "KARAR MALZEMESİ: Morris ailesiyle TEKRAR RİSKİ yüksek (kayıt distinct=2 "
     "veriyor, kayıttaki en düşük ayırt edicilik puanlarından biri). Kitapta "
     "zaten nine-mens-morris, achi ve picaria var. Bu madde bir yedekle "
     "değiştirilmeye EN UYGUN adaydır"],
    s=["P1"], cult=CULT_FULL,
    pat=['"luk tsut kei" Chinese six men\'s game rules',
         'Cantonese six men morris game rules Culin']),

"morabaraba": g("BLOCKED", "P1", 4, ["zaslavsky-1973", "murray-1952"],
    W_ACCESS + " Oyun `attributed` taranmıştır: Sotho atfı ZORUNLUDUR.",
    C_SCAN + ["Zaslavsky 1973 ve Murray 1952 proje genelinde DENENDİ ve açılamadı"],
    "Kural metni ve Sotho atfı.",
    ["Zaslavsky 1973 ya da Murray 1952'de morabaraba/umlabalaba maddesi",
     "12'şer taş, köşegenli morris tahtası, değirmen kuralı, 'uçma' kuralı "
     "(üç taşa düşünce serbest hamle) ve bitiş",
     "Sotho topluluğu atfını veren bir kaynak",
     "KARAR MALZEMESİ: twelve-mens-morris ile AYNI tahta — kitap ikisini "
     "birden basarsa tekrar riski ciddidir"],
    cult=CULT_FULL,
    pat=['"morabaraba" Sotho rules twelve pieces mill game',
         '"umlabalaba" OR "mmela" Southern Africa morris rules']),

"shax": g("BLOCKED", "P1", 4, ["murray-1952", "zaslavsky-1973"],
    W_ACCESS + " Kayıt ayrıca SOMALİ KAYNAKLI çağdaş bir künye istiyor.",
    C_SCAN + ["Murray 1952 ve Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı"],
    "Kural metni ve Somali kaynaklı künye.",
    ["Murray 1952 ya da Zaslavsky 1973'te shax/jare maddesi",
     "12'şer taş, yerleştirme aşaması, ilk değirmenin ÖZEL kuralı, kaydırma "
     "aşaması, bitiş",
     "Somali kaynaklı çağdaş bir künye"],
    cult=CULT_FULL,
    pat=['"shax" Somali game rules twelve pieces', '"jare" OR "shantarad" Somali board game rules']),

"shisima": g("BLOCKED", "P1", 4, ["zaslavsky-1973"], W_ACCESS,
    C_SCAN + ["Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı"],
    "Zaslavsky bu oyunun TEK künyesidir; ne kural ne ikinci bağımsız kaynak var.",
    ["Zaslavsky 1973'te shisima maddesi — sekizgen tahta, 3'er taş, "
     "hareket kısıtı, üçlü sıra, bitiş",
     "KENYA KAYNAKLI ikinci bağımsız künye (Luhya)"],
    s=["P2"], cult=CULT_FULL,
    pat=['"shisima" Luhya Kenya game rules octagon', 'shisima Kenyan traditional game three in a row']),

"tapatan": g("BLOCKED", "P2", 4, ["culin-1900-philippine", "murray-1952"],
    "Birincil künye 1900 tarihli bir dergi makalesidir — KAMUSAL ALANDADIR — "
    "ama açık nüshası bulunmadı; ikinci künye (Murray 1952) engelli.",
    C_SCAN + ["Culin 1900 · 'Philippine Games' — açık nüsha bulunamadı; AYNI "
              "derginin 1899 sayısı denendi ve yalnızca JSTOR nüshası çıktı",
              "Murray 1952 DENENDİ ve açılamadı"],
    "Culin'in tapatan bölümü.",
    ["Culin, Stewart, 'Philippine Games', American Anthropologist 2:4 (1900) — "
     "tapatan bölümü, sayfa numarasıyla",
     "KARAR MALZEMESİ: kitapta ZATEN achi ve picaria var ve nine-holes yazılabilir "
     "durumda. Kayıt uyarıyor: 'kitapta en fazla üç üç-taş oyunu olmalı'. "
     "Bu maddenin yerine bir yedek düşünülebilir"],
    s=["P1"],
    ideal="American Anthropologist cilt 2 (1900) taraması — sungka ile AYNI "
          "kaynak, tek teslim iki oyun açar.",
    pat=['Culin "Philippine Games" American Anthropologist 1900 tapatan',
         'American Anthropologist volume 2 1900 archive.org full text']),

"terni-lapilli": g("BLOCKED", "P6", 0, ["murray-1952"],
    "Yeniden kurgulama BELİRSİZDİR: taşların yerleştirmeden sonra KAYDIRILIP "
    "kaydırılmadığı kaynaklardan kesin çıkmaz — yani oyunun temel mekaniği "
    "bilinmiyor. Ovid bir GÖNDERMEDİR, kural değil.",
    C_SCAN + ["Ovid, Ars Amatoria III — üç taşlı bir oyuna GÖNDERME, kural yok",
              "Murray 1952 DENENDİ ve açılamadı"],
    "Taşların yerleştirmeden sonra kaydırılıp kaydırılmadığı.",
    ["Roma üç-taş oyununun MEKANİĞİNİ tartışan bir arkeoloji/klasik filoloji çalışması",
     "Roma kazı buluntularındaki oyun ızgaralarını yorumlayan bir kaynak",
     "⚠ Kayıt uyarıyor: modern 'XOX' ile ilişkisi KESİN DEĞİLDİR ve kitap "
     "köken iddiası YAPMAYACAK",
     "KARAR MALZEMESİ: üç-taş kümesi kitapta zaten kalabalık (achi · picaria · "
     "nine-holes · tapatan). Kaynak gelmezse bu madde yedekle değiştirilmeye uygundur"],
    s=["P1", "P4"], recon=E_RECON,
    ideal="Rakip yorumları KARŞILAŞTIRAN bir çalışma; kitap tek yorum seçip beyan edecek.",
    pat=['terni lapilli Roman three stone game archaeology reconstruction',
         'Roman game boards graffiti three in a row scholarship']),

"twelve-mens-morris": g("BLOCKED", "P1", 3, ["murray-1952", "bell-1960"],
    "Erişilebilir kaynak AÇILDI ve YALNIZCA dokuz taşlı biçimi verdi — o biçim "
    "zaten YAZILDI. ON İKİ taşlı biçim için ayrı bir kayıt bulunamadı.",
    C_SCAN + ["Gomme 1894 cilt I § Nine Men's Morris AÇILDI: dokuz taşlı biçim "
              "var (yazıldı), ON İKİ taşlı biçim için ayrı kayıt YOK "
              "(Batch 4 kaynak avı)",
              "Murray 1952 ve Bell proje genelinde DENENDİ ve açılamadı"],
    "On iki taşlı biçimin tahtası (köşegenli) ve o biçime özgü kurallar.",
    ["Murray 1952 ya da Bell'de twelve men's morris maddesi — KÖŞEGENLİ tahta "
     "ve 12'şer taş",
     "Dokuz taşlı biçimden FARKI: köşegenler, berabere sıklığı, 'uçma' kuralı",
     "KARAR MALZEMESİ: bu madde nine-mens-morris içinde bir VARYANT KUTUSU mu "
     "olmalı? Kayıt tekrar riskini işaretliyor (distinct=2) ve morabaraba ile "
     "AYNI tahtayı paylaşıyor"],
    s=["P3", "P7"],
    pat=['"twelve men\'s morris" rules diagonal board history',
         'twelve mens morris larger merels rules Murray']),
})

ENTRIES.update({

# ── WAR BOARD ──────────────────────────────────────────────────────────────
"jeu-de-dames": g("BLOCKED", "P1", 4, ["murray-1952", "parlett-1999"],
    W_ACCESS,
    C_SCAN + ["Murray 1952 ve Parlett proje genelinde DENENDİ ve açılamadı"],
    "İki künyenin ikisi de engelli.",
    ["Murray 1952 ya da Parlett'te international/Polish draughts maddesi — "
     "10×10 tahta, 20'şer taş, geriye alma, dama taşının uzun menzili, "
     "AZAMİ ALMA ZORUNLULUĞU",
     "Oyunun 1723 Paris kökeni ve 'Polonya daması' adının hikâyesi",
     "KARAR MALZEMESİ: kayıt uyarıyor — 'okur damayı zaten biliyor; kitaba "
     "girmesi ancak Alquerque–Dama–Türk Daması hattını göstermek içinse "
     "anlamlıdır'. alquerque YAZILABİLİR durumda; hat bu maddeyle tamamlanır"],
    pat=['international draughts rules 10x10 majority capture history',
         'jeu de dames polonaises 1723 histoire règles']),

"konane": g("BLOCKED", "P2", 3, ["culin-1899-hawaiian", "bell-1960"],
    "Birincil künye KAMUSAL ALANDADIR ama yalnızca JSTOR nüshası bulundu ve "
    "tam metin indirilemedi; ikinci künye (Bell) engelli. Oyun `attributed` "
    "taranmıştır: Hawaii atfı ZORUNLUDUR ve kayıt ÇAĞDAŞ Kānaka Maoli kaynaklı "
    "bir künye istiyor.",
    C_SCAN + ["Culin 1899 · 'Hawaiian Games', American Anthropologist 1:2 — "
              "yalnızca JSTOR nüshası, tam metin indirilemedi (Batch 4 avı)",
              "Culin 1898 · Chess and Playing-Cards AÇILDI (pachisi ve patolli "
              "buradan doğrulandı) — kōnane maddesi taranmadı",
              "Bell proje genelinde DENENDİ ve açılamadı"],
    "Culin'in kōnane bölümü ve çağdaş Hawaii atfı.",
    ["Culin, Stewart, 'Hawaiian Games', American Anthropologist 1:2 (1899) — "
     "kōnane bölümü, SAYFA NUMARASIYLA (KAMUSAL ALAN; ciltli dergi taraması "
     "aranmalı — proje bu makalenin sayfa aralığını henüz görmedi)",
     "Tahta ölçüsü, ilk iki taşın kaldırılması, YALNIZCA atlayarak alma, "
     "çoklu atlama kuralı ve hamlesiz kalanın kaybetmesi",
     "ÇAĞDAŞ Kānaka Maoli kaynaklı bir künye — atıf zorunluluğu için "
     "(Bishop Museum · Hawaiian kültür kurumları)"],
    s=["P1", "P5"], cult=CULT_FULL,
    ideal="American Anthropologist cilt 1 (1899) taraması + Bishop Museum kaydı.",
    pat=['Culin "Hawaiian Games" American Anthropologist 1899 archive.org',
         'American Anthropologist volume 1 1899 full text HathiTrust',
         'konane Hawaiian checkers rules Bishop Museum']),

"makruk": g("BLOCKED", "P1", 3, ["murray-1913", "parlett-1999"],
    W_ACCESS + " Ayrıca SAYMA (nap) kuralları karmaşıktır ve tam basılırsa "
    "sayfa bütçesini zorlar (§ K19).",
    C_SCAN + ["Murray 1913 DENENDİ — archive.org HTTP 401 (ödünç kısıtı). "
              "Eser KAMUSAL ALANDADIR; engel telif değil DAĞITIMDIR",
              "Parlett proje genelinde DENENDİ ve açılamadı",
              "Falkener 1892 Burma satrancı bölümü AÇILDI (sittuyin yazıldı) — "
              "Siyam biçimi için ayrı kural seti vermiyor"],
    "Murray 1913'ün Siyam satrancı bölümü ve sayma kurallarının basılabilir biçimi.",
    ["Murray, A History of Chess (1913) — Siyam satrancı bölümü "
     "(HathiTrust ya da Google Books TAM GÖRÜNÜM; eser kamusal alandadır)",
     "Taşların adı ve hareketi, ERLERİN ÜÇÜNCÜ SIRADAN başlaması, "
     "erin terfi karesi, med (vezir) hareketi",
     "Sayma (nap) kurallarının SADELEŞTİRİLEBİLİR bir özeti — kitap iki sayfaya sığmalı"],
    s=["P3"],
    ideal="Murray 1913 kamusal alan tam görünümü — HathiTrust bu sınıf eserde "
          "en yüksek başarı şansını veriyor.",
    pat=['Murray "A History of Chess" 1913 HathiTrust full view Siamese',
         'makruk Thai chess rules counting nap', 'makruk rules promotion third rank']),

"surakarta": g("UNRESOLVED", "P5", 2, ["parlett-1999"],
    "OYUNUN GELENEKSEL Mİ YOKSA 20. YÜZYIL İCADI MI OLDUĞU KESİN DEĞİLDİR. "
    "Kayıt bunu açıkça yazıyor: bu netleşmeden madde kitaba 'geleneksel' diye "
    "GİREMEZ. Ayrıca tek künyesi (Parlett) engellidir ve ikinci bağımsız "
    "kaynağı yoktur — yani hem kimlik hem kaynak açıktır.",
    C_SCAN + ["Parlett proje genelinde DENENDİ ve açılamadı",
              "İkinci bağımsız kaynak Faz 1'den beri aranıyor ve bulunamadı"],
    "Oyunun Java'daki geleneksel varlığına dair BİR KANIT — ya da tersi.",
    ["Surakarta'nın Java'daki geleneksel varlığını gösteren bir DÖNEM kaydı "
     "(20. yy öncesi ya da erken 20. yy saha kaydı)",
     "Ya da tersi: oyunun modern bir icat/ticari yayın olduğunu gösteren bir kayıt",
     "Kural metni: 8×8 ızgara, köşe halkaları, HALKADAN GEÇEREK ALMA kuralı",
     "⚠ ALTERNATİF ÇÖZÜM — KURUCU KARARI: kimlik netleşmezse madde kapsamdan "
     "çıkarılıp yedekle değiştirilebilir. Kayıt source=2 veriyor: bu kapsamın "
     "EN ZAYIF kaynak puanlarından biridir"],
    s=["P1", "P4"], cult=CULT_FULL,
    ideal="Java kaynaklı bir dönem saha kaydı — oyunun geleneksel olduğunu "
          "ya da OLMADIĞINI kesin söyleyen herhangi bir kanıt.",
    pat=['surakarta game origin traditional Javanese evidence',
         'permainan surakarta Jawa asal usul permainan tradisional',
         'surakarta board game history invented 20th century']),

"turkish-dama": g("BLOCKED", "P1", 4, ["murray-1952", "parlett-1999"], W_ACCESS,
    C_SCAN + ["Murray 1952 ve Parlett proje genelinde DENENDİ ve açılamadı"],
    "İki künyenin ikisi de engelli.",
    ["Murray 1952 ya da Parlett'te Turkish draughts maddesi — 8×8 tahta, "
     "16'şar taş İKİNCİ ve ÜÇÜNCÜ sırada, taşların İLERİ VE YANA gitmesi "
     "(köşegen DEĞİL), dama taşının uzun menzili, alma zorunluluğu",
     "Anadolu kaynaklı bir dönem kaydı"],
    ideal="Osmanlı/Türk kaynaklı bir dönem kaydı kültür künyesini güçlendirir.",
    pat=['Turkish draughts dama rules orthogonal capture',
         'Türk daması kuralları tarihi kaynak', 'Murray Turkish draughts rules 1952']),

"yote": g("SOURCE-PENDING", "P2", 3, ["beart-1955", "zaslavsky-1973"],
    "Birincil künye Dakar basımı dar dağıtımlı bir eserdir ve HİÇ DENENMEDİ; "
    "ikinci künye (Zaslavsky) engelli.",
    C_SCAN + ["Béart 1955 · Mémoires de l'IFAN 42 — HİÇ denenmedi",
              "Zaslavsky 1973 proje genelinde DENENDİ ve açılamadı"],
    "Béart'ın yoté kaydı — özellikle ÇİFT ALMA kuralı.",
    ["Béart, Charles, Jeux et jouets de l'Ouest africain (Dakar: IFAN, 1955) — "
     "yoté bölümü (Fransızca)",
     "5×6 ızgara, elde tutulan taşların sırayla girmesi, atlayarak alma ve "
     "ALINAN HER TAŞLA BİRLİKTE İKİNCİ BİR TAŞIN DA KALDIRILMASI kuralı — "
     "oyunun ayırt edici mekaniği budur (distinct=5)",
     "Wolof atfını veren bir kaynak"],
    s=["P1"], cult=CULT_FULL,
    ideal="Béart 1955 — Batı Afrika oyunlarının en iyi saha kaydı; "
          "zamma ile AYNI kaynak, tek teslim iki oyun açar.",
    pat=['Béart "Jeux et jouets de l\'Ouest africain" IFAN 1955 PDF',
         '"yoté" OR "yote" Wolof Senegal game rules double capture',
         'jeux ouest africain yoté règles IFAN Dakar']),

"zamma": g("SOURCE-PENDING", "P2", 3, ["murray-1952", "beart-1955"],
    "Birincil künye (Murray 1952) engelli; ikincisi (Béart 1955) HİÇ DENENMEDİ. "
    "Ayrıca TAŞ SAYISI kaynaklara göre DEĞİŞİYOR ve kitap bir sayı seçip "
    "gerekçesini yazmak zorundadır. Oyun `attributed` taranmıştır: "
    "Amazigh atfı ZORUNLUDUR.",
    C_SCAN + ["Murray 1952 DENENDİ ve açılamadı", "Béart 1955 — HİÇ denenmedi"],
    "Kural metni ve taş sayısı çelişkisini çözecek bir künye.",
    ["Murray 1952 ya da Béart 1955'te zamma/sig maddesi",
     "Tahta (9×9 köşegenli ızgara), taş sayısı, hareket, atlayarak alma, "
     "'mollah' (dama) taşının menzili",
     "TAŞ SAYISI için bir karar dayanağı: kaynaklar farklı sayı veriyor ve "
     "kitap birini seçip gerekçesini yazacak",
     "Amazigh atfını veren bir kaynak"],
    s=["P1", "P7"], cult=CULT_FULL,
    pat=['"zamma" Berber Amazigh draughts rules North Africa',
         '"sig" OR "kharbga" North African board game rules',
         'Béart jeux ouest africain zamma sig règles']),
})


# ═══════════════════════════════════════════════════════════════════════════
# ÖLÇÜM — bileşik öncelik puanı
# ═══════════════════════════════════════════════════════════════════════════
# § 9: "Puanları yapay olarak şişirmeyin." Bu yüzden BEŞ bileşenin DÖRDÜ
# projenin KENDİ verisinden okunur ve yalnızca biri (unlockEase) bu kayıtta
# verilir — o da açık bir cetvele bağlıdır:
#
#   5 → tek eser · bölümü projenin kaydında ADI GEÇİYOR · tek teslim yeter
#   4 → tek eser · standart bir referans · bölüm başlığından bulunur
#   3 → tek eser ama uzmanlık künyesi ya da locator bilinmiyor
#   2 → iki şey birden gerekiyor (kaynak + kimlik kararı)
#   1 → kaydın KENDİSİ bulunamadı; asıl iş aramanın kendisi
#   0 → yeniden kurgulama tartışması; tek kaynak çözmez

def compose(root, gi, sc, fam_targets):
    fam_written = {}
    out = []
    for gid, e in ENTRIES.items():
        rec = gi.get(gid, {})
        s = sc[gid]
        sco = rec.get("scores", {})
        target = fam_targets[s["family"]]["target"]
        deficit = fam_targets[s["family"]]["deficit"]
        fdef = round(5.0 * deficit / target, 1) if target else 0.0
        cultural = sco.get("cultural", 0)
        distinct = sco.get("distinct", 0)
        pagefit = sco.get("explain", 0)
        composite = round(e["ease"] + fdef + cultural + distinct + pagefit, 1)
        # Öncelik SINIFI baskın gerekçeye göre verilir (§ 9).
        if e["ease"] >= 4:
            pri, pri_why = "A", "tek iyi kaynak maddeyi HEMEN yazılabilir yapar"
        elif fdef >= 4.0:
            pri, pri_why = "B", "ciddi biçimde eksik bir aileyi doldurur"
        elif cultural >= 5:
            pri, pri_why = "C", "kaybedilen bir kültürü geri getirir"
        elif distinct >= 5:
            pri, pri_why = "D", "portföyde eşi olmayan bir mekanik taşır"
        else:
            pri, pri_why = "E", "yararlı ama kritik değil"
        out.append(dict(
            gameId=gid, title=s["name"], altNames=rec.get("altNames", []),
            culture=s["culture"], region=s["region"],
            countryOrArea=s.get("countryOrArea"), period=s.get("period"),
            family=s["family"], restrictionStatus=s["restrictionStatus"],
            status=e["status"], primaryBlocker=e["primary"],
            primaryBlockerName=BLOCKER_NAMES[e["primary"]],
            secondaryBlockers=[{"code": c, "name": BLOCKER_NAMES[c]} for c in e["secondary"]],
            currentStatusNote=s["playabilityStatus"],
            whyAgentCannotWrite=e["why"], alreadyChecked=e["checked"],
            sourcesAttempted=[WORKS[w]["citation"] for w in e["works"] if w in WORKS],
            whatWasMissing=e["missing"], founderMustFind=e["find"],
            minimumEvidence=e["need"], idealEvidence=e["ideal"],
            searchPatterns=e["patterns"], works=e["works"],
            expectedFileFormat="PDF · tarama · kararlı URL · künye notu "
                               "(.md ya da .txt) — JSON'a çevirmek GEREKMEZ",
            expectedSourceLocation="06_FOUNDER_DELIVERY/%s/" % gid,
            howAgentWillUseIt="04_BUILD/founder_delivery_ingest.py alır → "
                              "hash'ler → kanıt listesini denetler → "
                              "source_verification kaydı açar → engeli çözer → "
                              "üretim kuyruğuna alır → yazar → diyagram → QA → CI",
            unlockEase=e["ease"], familyDeficitScore=fdef,
            culturalValue=cultural, mechanicalUniqueness=distinct,
            pageEconomy=pagefit, compositeScore=composite,
            priorityClass=pri, priorityReason=pri_why,
            sourceRefs=[x["ref"] for x in rec.get("sources", [])],
            unresolvedQuestions=rec.get("unresolvedQuestions", []),
        ))
    out.sort(key=lambda r: (-r["compositeScore"], r["gameId"]))
    return out


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def read_state(root):
    gi = {x["gameId"]: x for x in load(os.path.join(root, "01_SOURCE", "game_index.json"))["games"]}
    sc = {x["gameId"]: x for x in load(os.path.join(root, "01_SOURCE", "scope_lock.json"))["entries"]}
    fam = load(os.path.join(root, "01_SOURCE", "family_index.json"))
    bp = os.path.join(root, "02_MANUSCRIPT", "book.json")
    written = set()
    if os.path.exists(bp):
        written = {x["gameId"] for x in load(bp)["games"]}
    return gi, sc, fam, written


def family_rollup(sc, written, writable):
    """Aile açığı — kapsamdan ÖLÇÜLÜR, elle yazılmaz."""
    out = {}
    for e in sc.values():
        f = e["family"]
        r = out.setdefault(f, dict(target=0, written=0, writable=0, blocked=0))
        r["target"] += 1
        if e["gameId"] in written:
            r["written"] += 1
        elif e["gameId"] in writable:
            r["writable"] += 1
        else:
            r["blocked"] += 1
    for r in out.values():
        r["deficit"] = r["target"] - r["written"]
    return out


def integrity(sc, written, writable):
    """Kayıt KAPSAMLA örtüşüyor mu — bu bir KAPIDIR.

    Üç küme kapsamı TAM olarak bölmelidir. Bir oyun yazıldığında kayıttan
    düşmezse ya da yeni bir oyun hiçbir kümeye girmezse burası kırmızı yanar.
    """
    errs = []
    scope = set(sc)
    reg = set(ENTRIES)
    wn = set(writable)
    overlap = (reg & wn) | (reg & written) | (wn & written)
    if overlap:
        errs.append("küme çakışması: %s" % sorted(overlap))
    missing = scope - reg - wn - written
    if missing:
        errs.append("hiçbir kümede olmayan oyun: %s" % sorted(missing))
    extra = (reg | wn) - scope
    if extra:
        errs.append("kapsamda olmayan kayıt: %s" % sorted(extra))
    return errs


# ═══════════════════════════════════════════════════════════════════════════
# KAYIT — 06_REPORTS/FOUNDER_RESEARCH_GAP_REGISTER.md
# ═══════════════════════════════════════════════════════════════════════════

FAM_EN = {"sowing": "The Sowing Games", "hunt-siege": "The Hunt and the Siege",
          "race": "The Race Home", "territory": "The Line and the Territory",
          "war-board": "The War Board", "chance": "Chance and Nerve",
          "boardless": "Games Without a Board"}


def checkbox(need):
    lines = []
    for label, key in (("RULE EVIDENCE", "rule"), ("SOURCE EVIDENCE", "source"),
                       ("CULTURAL EVIDENCE", "cultural"),
                       ("RECONSTRUCTION EVIDENCE", "reconstruction")):
        items = need.get(key) or []
        if not items:
            continue
        lines.append("%s" % label)
        lines.append("  " + "  ".join("[ ] %s" % i for i in items))
    return "\n".join(lines)


def render_register(rows, fam, written, writable, generated_at):
    L = []
    A = L.append
    A("# FOUNDER RESEARCH GAP REGISTER")
    A("")
    A("<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/build_gap_register.py · ELLE DÜZENLEMEYİN -->")
    A("")
    A("> **The Great Book of World Games** · kurucu araştırma teslim kaydı")
    A("> ")
    A("> Bu dosya İNGİLİZCE alan adlarıyla yazılmıştır çünkü kurucu direktifi")
    A("> (§ 6 · § 13) alan listesini İngilizce verir ve paket bir kütüphaneciye")
    A("> ya da araştırmacıya doğrudan uzatılabilir olmalıdır. Gerekçe metinleri")
    A("> deponun dili olan Türkçedir.")
    A("")
    A("> ⛔ **Bu bir 'kalan oyunlar' listesi DEĞİLDİR.** Yalnızca kurucunun")
    A("> müdahalesi olmadan yazılamayacak maddeleri taşır. Kaynağı elde olan")
    A("> ve yalnızca sıra bekleyen oyunlar § 2'de AYRI durur.")
    A("")
    A("---")
    A("")
    A("## 1 · TEK BAKIŞTA")
    A("")
    A("| | ölçülen |")
    A("|---|---:|")
    A("| Nihai kapsam | **100** |")
    A("| Yazılmış | **%d** |" % len(written))
    A("| Kurucu MÜDAHALESİ OLMADAN yazılabilir | **%d** |" % len(writable))
    A("| **KURUCU ARAŞTIRMASI GEREKEN** | **%d** |" % len(rows))
    A("| ↳ `BLOCKED` — kaynak denendi, açılamadı | **%d** |"
      % sum(1 for r in rows if r["status"] == "BLOCKED"))
    A("| ↳ `SOURCE-PENDING` — künye var, HENÜZ denenmedi | **%d** |"
      % sum(1 for r in rows if r["status"] == "SOURCE-PENDING"))
    A("| ↳ `UNRESOLVED` — kaynak açık, kimlik/kültür uyuşmuyor | **%d** |"
      % sum(1 for r in rows if r["status"] == "UNRESOLVED"))
    A("| `UNATTEMPTED` — hiç denenmemiş ve engelsiz | **0** |")
    A("")
    A("> `UNATTEMPTED` **sıfırdır** ve bu kasıtlıdır: Batch 6'da kalan 59 oyunun")
    A("> **tamamı** elde bulunan kamusal alan derlemelerine karşı tek tek tarandı.")
    A("> Artık 'henüz bakılmadı' diyebileceğimiz bir oyun yok. Bu, Faz 3'ün")
    A("> 'denenmedi = engelli' hatasının TERSİ yönde kapatılmasıdır.")
    A("")
    A("### Engel sınıflarının dağılımı")
    A("")
    A("| sınıf | ad | sayı |")
    A("|---|---|---:|")
    cnt = {}
    for r in rows:
        cnt[r["primaryBlocker"]] = cnt.get(r["primaryBlocker"], 0) + 1
    for code in sorted(cnt, key=lambda c: int(c[1:])):
        A("| `%s` | %s | %d |" % (code, BLOCKER_NAMES[code], cnt[code]))
    A("")
    A("---")
    A("")
    A("## 2 · KURUCU MÜDAHALESİ GEREKTİRMEYEN %d OYUN" % len(writable))
    A("")
    A("Bunlar **engelli değildir** — sıra beklerler. Kaynakları elde bulunan")
    A("kamusal alan derlemelerindedir ve ajan bunları kurucu beklemeden yazar.")
    A("")
    A("| oyun | aile | isabet |")
    A("|---|---|---|")
    for gid in sorted(writable):
        A("| `%s` | %s | %s |" % (gid, FAM_EN.get(SCOPE_CACHE[gid]["family"], ""), writable[gid]))
    A("")
    A("> ⚠ İlk ikisi **kültür tuzağı riski** taşır ve sayfa açılmadan yazılamaz.")
    A("> Totolospi, sugoroku, tien-gow, jianzi ve xiangqi'de aynı tuzak beş kez")
    A("> ölçüldü: bir derlemenin başka bir kültüre ait bölümünden yazmak,")
    A("> kitabın kültür künyesini yalanlar.")
    A("")
    A("---")
    A("")
    A("## 3 · AİLE AÇIĞI")
    A("")
    A("| aile | hedef | yazılan | yazılabilir | **engelli** | açık | tamamlanma |")
    A("|---|---:|---:|---:|---:|---:|---|")
    for f in sorted(fam, key=lambda x: -fam[x]["blocked"]):
        r = fam[f]
        bar = "█" * int(12 * r["written"] / r["target"]) + "·" * (12 - int(12 * r["written"] / r["target"]))
        A("| %s | %d | %d | %d | **%d** | %d | `%s` %d%% |"
          % (FAM_EN[f], r["target"], r["written"], r["writable"], r["blocked"],
             r["deficit"], bar, round(100 * r["written"] / r["target"])))
    A("")
    A("> **Ekim ailesi kitabın en büyük açığıdır ve tek bir sebebi vardır:**")
    A("> on iki maddenin on ikisi de Murray · Bell · Zaslavsky · Russ ·")
    A("> de Voogt · Townshend hattına bağlıdır ve o hattın beşi engellidir.")
    A("> Aile 14 hedefinde **2** yazılmıştır — kitabın kendi adını taşıyan")
    A("> ailelerinden biri, açık ara en zayıfıdır.")
    A("")
    return L


def render_register_2(L, rows, lev, lost_cultures, lost_regions):
    A = L.append
    A("---")
    A("")
    A("## 4 · KÜLTÜR VE BÖLGE AÇIĞI")
    A("")
    A("Kapsam **68 kültür** vaat ediyor; yazılan **27**. Kalan **%d kültürün**"
      % len(lost_cultures))
    A("tamamı bu kayıttaki maddelerdedir — yani bu kayıt çözülmezse kitap")
    A("kültür vaadini **68'de değil 27'de** kapatır.")
    A("")
    A("Bölge olarak **dokuz bölge** YALNIZCA engelli kümede yaşıyor ve")
    A("çözülmezse kitaptan tamamen düşer:")
    A("")
    for r in sorted(lost_regions):
        gs = sorted(x["gameId"] for x in rows if x["region"] == r)
        A("- **%s** — %s" % (r, " · ".join("`%s`" % x for x in gs)))
    A("")
    A("---")
    A("")
    A("## 5 · MEKANİK AÇIK")
    A("")
    A("Engelli küme yalnızca kültür değil **mekanik** de taşıyor. Aşağıdaki")
    A("yapılar kitapta **hiç yoktur** ve yalnızca bu kayıttaki maddelerdedir:")
    A("")
    A("| mekanik | taşıyan madde | not |")
    A("|---|---|---|")
    A("| dört sıralı ekim (four-row mancala) | `omweso` · `hus` · `mefuvha` | "
      "yazılan iki ekim oyununun ikisi de iki sıralıdır |")
    A("| ekimde tur sonu yeniden dizme | `pallanguzhi` · `congklak` | yok |")
    A("| kutsal çukur / tuzdyk | `toguz-kumalak` | yok |")
    A("| alırken ikinci taşı da kaldırma | `yote` | kitapta eşi yok |")
    A("| dikey-yatay (köşegensiz) dama | `turkish-dama` | yazılan damaların "
      "hepsi köşegendir |")
    A("| halkadan geçerek uzaktan alma | `surakarta` | kitapta eşi yok |")
    A("| kıstırarak alma (custodial capture) | `hasami-shogi` | seega yazıldı "
      "ama tahta oyunu olarak tek örnektir |")
    A("| kilitlenme galibiyeti (hamlesiz kalan kaybeder) | `mu-torere` · "
      "`konane` | yok |")
    A("| sarmal iz + serbest bırakma koşulu | `li-b-el-merafib` | yok |")
    A("| saf şans yarışı (karar yok) | `game-of-the-goose` | tarihsel önem "
      "gerekçesi prozada yazılmalı |")
    A("| taş dizme + set toplama (yığın devirme) | `lagori` | yok |")
    A("| yön kısıtlı kovalamaca + devir | `kho-kho` | yok |")
    A("")
    A("---")
    A("")
    A("## 6 · KALDIRAÇ — HANGİ TEK KAYNAK KAÇ OYUN AÇAR")
    A("")
    A("> **Bu tablonun ilk satırı bu belgenin en önemli cümlesidir.**")
    A("")
    A("| eser | açtığı madde | durum |")
    A("|---|---:|---|")
    for k, v in lev:
        w = WORKS.get(k, {})
        ae = w.get("attemptEvidence", "")
        tag = "⛔ denendi · açılamadı" if ae == "attempted-and-refused" else "◻ HİÇ denenmedi"
        A("| %s | **%d** | %s |" % (w.get("citation", k).split(" (")[0], len(v), tag))
    A("")
    A("**Kümülatif:** Murray 1952 tek başına **24** madde açar. Ona Parlett,")
    A("Zaslavsky, Bell ve Russ eklenirse **52 maddenin 46'sı** açılır. Geri")
    A("kalan altısı ayrı ayrı avlanmak zorundadır.")
    A("")
    A("---")
    A("")
    A("## 7 · ÖNCELİK SIRALAMASI")
    A("")
    A("Bileşik puan **beş bileşenden** oluşur ve dördü projenin KENDİ")
    A("verisinden okunur — yalnızca `unlockEase` bu kayıtta verilir:")
    A("")
    A("```")
    A("compositeScore = unlockEase        (0–5 · açık cetvel, aşağıda)")
    A("               + familyDeficit     (0–5 · aile açığı ÷ hedef, ölçülen)")
    A("               + culturalValue     (0–5 · game_index scores.cultural)")
    A("               + mechanicalUnique  (0–5 · game_index scores.distinct)")
    A("               + pageEconomy       (0–5 · game_index scores.explain)")
    A("```")
    A("")
    A("| sınıf | anlamı | sayı |")
    A("|---|---|---:|")
    for c, name in (("A", "YÜKSEK GETİRİ — tek iyi kaynak maddeyi hemen açar"),
                    ("B", "AİLE DENGESİ — ciddi eksik bir aileyi doldurur"),
                    ("C", "KÜLTÜREL ÇEŞİTLİLİK — kaybedilen bir kültürü geri getirir"),
                    ("D", "MEKANİK ÇEŞİTLİLİK — eşi olmayan bir mekanik taşır"),
                    ("E", "DÜŞÜK ETKİ — yararlı ama kritik değil")):
        A("| **%s** | %s | %d |" % (c, name, sum(1 for r in rows if r["priorityClass"] == c)))
    A("")
    A("| # | oyun | aile | kültür | sınıf | puan | durum | engel |")
    A("|---:|---|---|---|:---:|---:|---|---|")
    for i, r in enumerate(rows, 1):
        A("| %d | **%s** `%s` | %s | %s | %s | **%.1f** | `%s` | `%s` |"
          % (i, r["title"], r["gameId"], FAM_EN[r["family"]], r["culture"],
             r["priorityClass"], r["compositeScore"], r["status"], r["primaryBlocker"]))
    A("")
    return L


def render_entries(L, rows):
    A = L.append
    A("---")
    A("")
    A("## 8 · KAYIT — OYUN OYUN")
    A("")
    A("Her madde kurucu direktifi § 6'nın istediği on beş alanı taşır.")
    A("")
    for i, r in enumerate(rows, 1):
        A("---")
        A("")
        A("### %d · %s" % (i, r["title"]))
        A("")
        A("| | |")
        A("|---|---|")
        A("| **GAME ID** | `%s` |" % r["gameId"])
        A("| **TITLE** | %s |" % r["title"])
        A("| **ALTERNATE NAME(S)** | %s |" % (", ".join(r["altNames"]) or "—"))
        A("| **CULTURE** | %s |" % r["culture"])
        A("| **REGION** | %s%s |" % (r["region"],
                                     " · %s" % r["countryOrArea"] if r["countryOrArea"] else ""))
        A("| **FAMILY** | %s |" % FAM_EN[r["family"]])
        A("| **PRIMARY BLOCKER** | `%s` — %s |" % (r["primaryBlocker"], r["primaryBlockerName"]))
        A("| **SECONDARY BLOCKERS** | %s |"
          % (" · ".join("`%s` %s" % (c["code"], c["name"]) for c in r["secondaryBlockers"]) or "—"))
        A("| **CURRENT STATUS** | `%s` · kısıt taraması: `%s` · öncelik %s · puan %.1f |"
          % (r["status"], r["restrictionStatus"], r["priorityClass"], r["compositeScore"]))
        A("")
        A("**WHY THE AGENT CANNOT WRITE IT**")
        A("")
        A(r["whyAgentCannotWrite"])
        A("")
        A("**WHAT HAS ALREADY BEEN CHECKED**")
        A("")
        for c in r["alreadyChecked"]:
            A("- %s" % c)
        A("")
        A("**WHAT SOURCE WAS ATTEMPTED**")
        A("")
        for s in r["sourcesAttempted"]:
            A("- %s" % s)
        A("")
        A("**WHAT WAS MISSING**")
        A("")
        A(r["whatWasMissing"])
        A("")
        A("**RESEARCH REQUEST — EXACTLY WHAT THE FOUNDER MUST FIND**")
        A("")
        for j, f in enumerate(r["founderMustFind"], 1):
            A("%d. %s" % (j, f))
        A("")
        A("**MINIMUM ACCEPTABLE EVIDENCE**")
        A("")
        A("```")
        A(checkbox(r["minimumEvidence"]))
        A("```")
        A("")
        A("**IDEAL EVIDENCE** — %s" % r["idealEvidence"])
        A("")
        A("**EXPECTED FILE FORMAT** — %s" % r["expectedFileFormat"])
        A("")
        A("**EXPECTED SOURCE LOCATION** — `%s`" % r["expectedSourceLocation"])
        A("")
        A("**HOW THE AGENT WILL USE THE DELIVERY** — %s" % r["howAgentWillUseIt"])
        A("")
        if r["searchPatterns"]:
            A("**SEARCH PATTERNS** (bunlar birer STRATEJİDİR, kanıt değil —")
            A("bu adreslerin var olduğu İDDİA EDİLMEZ)")
            A("")
            for p in r["searchPatterns"]:
                A("- `%s`" % p)
            A("")
    return L


# ═══════════════════════════════════════════════════════════════════════════
# PAKET — 06_REPORTS/FOUNDER_RESEARCH_PACK.md
# ═══════════════════════════════════════════════════════════════════════════
# Kayıt OYUNA göre düzenlenir çünkü direktif § 6 öyle ister.
# Paket KAYNAĞA göre düzenlenir çünkü insan araştırmacı öyle çalışır:
# kütüphaneye bir OYUN için değil bir KİTAP için gidilir ve o kitap
# masaya oturduğunda içinden sekiz madde birden çıkar.

def render_pack(rows, lev):
    by_work = {}
    for r in rows:
        for w in r["works"]:
            by_work.setdefault(w, []).append(r)
    order = [k for k, _ in lev if k in by_work]
    order += [k for k in by_work if k not in order]

    L = []
    A = L.append
    A("# FOUNDER RESEARCH PACK")
    A("")
    A("<!-- ÜRETİLMİŞ DOSYA — 04_BUILD/build_gap_register.py · ELLE DÜZENLEMEYİN -->")
    A("")
    A("> **The Great Book of World Games** · insan araştırmacı için çalışma paketi")
    A("> ")
    A("> Tam kayıt: [`FOUNDER_RESEARCH_GAP_REGISTER.md`](FOUNDER_RESEARCH_GAP_REGISTER.md)")
    A("")
    A("Bu paket **kaynağa göre** düzenlenmiştir, oyuna göre değil. Sebebi")
    A("pratiktir: kütüphaneye bir oyun için değil bir **kitap** için gidilir,")
    A("ve o kitap masaya oturduğunda içinden birden çok madde çıkar.")
    A("")
    A("---")
    A("")
    A("## 0 · ÖNCE BUNU OKUYUN — ÜÇ SATIRLIK ÖZET")
    A("")
    A("1. **Murray 1952'yi bulun.** Tek başına %d maddenin **24'ünü** açar."
      % len(rows))
    A("2. Sonra **Parlett 1999 · Zaslavsky 1973 · Bell 1960–69 · Russ 2000**.")
    A("   Beşi birlikte **46 madde** açar.")
    A("3. Geri kalan altı madde tek tek avlanır ve § 3'te ayrı listelenmiştir.")
    A("")
    A("**Bell 1960–69 en ucuz başlangıçtır**: Dover tıpkıbasımı hâlâ basılıyor")
    A("ve ikinci el piyasada bol. **Murray 1952 en yüksek getirilidir** ama")
    A("kütüphane gerektirir.")
    A("")
    A("---")
    A("")
    A("## 1 · TESLİM BİÇİMİ — HER ŞEY İÇİN AYNI")
    A("")
    A("```")
    A("06_FOUNDER_DELIVERY/")
    A("    <GAME_ID>/                  ← kayıttaki gameId, birebir")
    A("        source.pdf              ← tarama · PDF · ekran görüntüsü (opsiyonel)")
    A("        source.md               ← metin ya da kural özeti (opsiyonel)")
    A("        bibliography.md         ← ZORUNLU · yazar · başlık · baskı · yıl · sayfa")
    A("        notes.md                ← ne bulundu · ne bulunamadı (opsiyonel)")
    A("```")
    A("")
    A("Birden çok oyunu açan bir kitap teslim ediliyorsa **her oyun için ayrı")
    A("klasör** açın ve ilgili sayfaları o klasöre koyun. Aynı taramayı iki")
    A("klasöre kopyalamak sorun değildir — alım betiği hash'e bakar ve")
    A("yinelenen dosyayı tanır.")
    A("")
    A("### Ne göndermeniz GEREKMİYOR")
    A("")
    A("- JSON'a çevirmek **gerekmez**. Alım betiği bunu yapar.")
    A("- Kuralı yeniden yazmak **gerekmez**. Ham metin/tarama yeterlidir.")
    A("- Zaten elimizde olan bir şeyi tekrar bulmak **gerekmez** — her maddede")
    A("  `WHAT HAS ALREADY BEEN CHECKED` alanı neyin elde olduğunu söyler.")
    A("")
    A("### ⚠ İki dürüstlük kuralı")
    A("")
    A("1. **Sayfa numarası olmayan bir teslim de kabul edilir** — ama kayıt")
    A("   `bibliographyStatus: incomplete` taşır ve o oyun `locked` olamaz.")
    A("   Uydurulmuş bir sayfa numarası kitabın tek denetlenebilir iddiasını")
    A("   yıkar; **eksik künye bunu yıkmaz**.")
    A("2. **Kurucu teslimi bağımsız doğrulama DEĞİLDİR.** Kayıt bunu")
    A("   `founderSupplied: true · independentVerification: false` olarak")
    A("   taşır ve prozada gizlenmez.")
    A("")
    A("---")
    A("")
    A("## 2 · KAYNAK KAYNAK ÇALIŞMA LİSTESİ")
    A("")
    for k in order:
        w = WORKS[k]
        games = sorted(by_work[k], key=lambda r: -r["compositeScore"])
        A("---")
        A("")
        A("### ▸ %s" % w["citation"])
        A("")
        A("| | |")
        A("|---|---|")
        A("| **AÇTIĞI MADDE** | **%d** |" % len(games))
        A("| **DURUM** | %s |" % ("⛔ **DENENDİ ve açılamadı**"
                                  if w["attemptEvidence"] == "attempted-and-refused"
                                  else "◻ **HİÇ DENENMEDİ** — engelli değil, sırası gelmedi"))
        A("| **KANIT** | %s |" % w["evidence"])
        A("| **NEDEN** | %s |" % w["why"])
        A("")
        A("**NEREDE ARANIR**")
        A("")
        for rt in w["route"]:
            A("- %s" % rt)
        A("")
        A("**NE İSTİYORUZ**")
        A("")
        A(w["ask"])
        A("")
        if w.get("note"):
            A("> %s" % w["note"])
            A("")
        A("**AÇTIĞI MADDELER**")
        A("")
        A("| oyun | aile | kültür | sınıf | puan | ne çıkarılacak |")
        A("|---|---|---|:---:|---:|---|")
        for r in games:
            first = r["founderMustFind"][0] if r["founderMustFind"] else "—"
            first = first.replace("|", "·")
            if len(first) > 150:
                first = first[:147] + "…"
            A("| `%s` | %s | %s | %s | %.1f | %s |"
              % (r["gameId"], FAM_EN[r["family"]], r["culture"],
                 r["priorityClass"], r["compositeScore"], first))
        A("")
        A("**ARAMA KALIPLARI** — *bunlar strateji önerisidir; bu adreslerin")
        A("var olduğu iddia edilmez*")
        A("")
        pats = []
        for r in games:
            for p in r["searchPatterns"]:
                if p not in pats:
                    pats.append(p)
        for p in pats[:8]:
            A("- `%s`" % p)
        A("")
        A("**BUNLARI ŞURAYA BIRAKIN**")
        A("")
        A("```")
        for r in games:
            A("06_FOUNDER_DELIVERY/%s/" % r["gameId"])
        A("```")
        A("")
    return L


def render_pack_tail(L, rows):
    A = L.append
    A("---")
    A("")
    A("## 3 · EN YÜKSEK ÖNCELİKLİ ON MADDE — TEK TEK")
    A("")
    A("Kaynak kaynak liste verimlidir; bu bölüm ise **tek bir maddeyi**")
    A("bitirmek isteyen bir araştırmacı içindir.")
    A("")
    for r in rows[:10]:
        A("---")
        A("")
        A("```")
        A("GAME     : %s (%s)" % (r["title"], r["gameId"]))
        A("CULTURE  : %s · %s" % (r["culture"], r["region"]))
        A("FAMILY   : %s" % FAM_EN[r["family"]])
        A("PRIORITY : %s · composite %.1f" % (r["priorityClass"], r["compositeScore"]))
        A("BLOCKER  : %s — %s" % (r["primaryBlocker"], r["primaryBlockerName"]))
        A("```")
        A("")
        A("**SEARCH FOR:**")
        A("")
        for j, f in enumerate(r["founderMustFind"], 1):
            A("%d. %s" % (j, f))
        A("")
        A("**MINIMUM ACCEPTABLE SOURCE:**")
        A("")
        A("Kanıt listesi aşağıdadır; hepsi tek bir kaynaktan gelmek zorunda")
        A("değildir. `bibliography.md` hangi kanıtın hangi kaynaktan geldiğini")
        A("söylediği sürece iki ayrı kaynak birleştirilebilir.")
        A("")
        A("```")
        A(checkbox(r["minimumEvidence"]))
        A("```")
        A("")
        A("**PREFERRED SOURCE:** %s" % r["idealEvidence"])
        A("")
        A("**WHAT TO RETURN:** PDF · tarama · kararlı URL · künye (yazar ·")
        A("başlık · baskı · yıl · **sayfa**) · ilgili sayfa aralığı · gerekirse")
        A("kısa bir kural özeti")
        A("")
        A("**SAVE AS / DROP INTO:**")
        A("")
        A("```")
        A("06_FOUNDER_DELIVERY/%s/source.pdf" % r["gameId"])
        A("06_FOUNDER_DELIVERY/%s/bibliography.md" % r["gameId"])
        A("```")
        A("")
    A("---")
    A("")
    A("## 4 · TESLİMDEN SONRA NE OLUR")
    A("")
    A("Kurucu direktifi § 18 bunu bağlayıcı kılar. Teslim geldiğinde ajan")
    A("**durmaz ve onay beklemez**:")
    A("")
    A("```")
    A("  ./04_BUILD/founder_delivery_ingest.py        ← alır · hash'ler · denetler")
    A("        ↓")
    A("  kanıt listesi karşılandı mı?  ── hayır ──▶  eksik kanıt raporu · beklemede")
    A("        ↓ evet")
    A("  source_verification kaydı açılır (founderSupplied bayrağıyla)")
    A("        ↓")
    A("  engel çözülür · üretim kuyruğuna alınır")
    A("        ↓")
    A("  YAZ → DİYAGRAM → kaynak QA → oynanabilirlik QA → kültürel QA")
    A("        ↓")
    A("  dizgi · ölçüm · sayfa modeli · indeksler · arka madde")
    A("        ↓")
    A("  commit · push · CI YEŞİL → SONRAKİ OYUN")
    A("```")
    A("")
    A("> Bir oyunun engeli çözüldüğünde **yarım bırakılmaz** (§ 19).")
    A("> Hedef `KAYNAK → TAM OYUN → QA → CI`'dır, `KAYNAK → TASLAK` değil.")
    A("")
    return L



# ═══════════════════════════════════════════════════════════════════════════
# ÇÖZÜLDÜ — kurucu teslimi (Faz 5 · Batch 7 · 19 Ağustos 2026)
# ═══════════════════════════════════════════════════════════════════════════
# Bu altı oyun kayıttan ÇIKTI çünkü YAZILDILAR. Kayıtları burada durur:
# bir engelin bir zamanlar var olduğu, çözülmesiyle yanlış olmaz (§23).
#
# Üç eser geldi (Murray 1952 · Bell · kısmi Parlett), ikisi gelmedi
# (Zaslavsky indirilemedi; "Russ" dosyası bir yapay zekâ çıktısıydı).
RESOLVED_BY_DELIVERY = {
 "oware":          "Murray 1952 § 7.5.12 ss.181–182 (Ashanti = Akan) + Bell ss.116–117 — İKİSİ DE Rattray 1927'den türer, BİR bağımsız kaynak sayılır",
 "pallanguzhi":    "Bell ss.115–116 — 'played by the Tamil women of southern India'",
 "dara":           "Bell ss.95–96 — 'Dara of the Dakarkari people, Nigeria'",
 "mu-torere":      "Murray 1952 § 4.8.3 s.93 — 'Maoris, New Zealand', Elsdon Best'e dayanır",
 "catch-the-hare": "Murray 1952 § 5.1.1 s.99 — 'Spain: De cercar la liebre', Alfonso X (Alf. 916)",
 "hasami-shogi":   "Bell s.97 'Hasami Shogi (1)' — 'also from Japan'; Bell'in (2) biçimi VARYANT olarak anıldı",
}

SCOPE_CACHE = {}


def leverage(rows):
    lev = {}
    for r in rows:
        for w in r["works"]:
            lev.setdefault(w, []).append(r["gameId"])
    return sorted(lev.items(), key=lambda x: (-len(x[1]), x[0]))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true",
                    help="üretmez, BAYAT MI diye bakar (CI kapısı)")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    print("=" * 74)
    print("  KURUCU ARAŞTIRMA BOŞLUK KAYDI%s" % (" (--check)" if args.check else ""))
    print("=" * 74)

    gi, sc, fam, written_disk = read_state(root)
    SCOPE_CACHE.clear()
    SCOPE_CACHE.update(sc)

    # ── YAZILMIŞ KÜME: kapsamdan TÜRETİLİR, manuscript'ten DEĞİL ──────────
    # Manuscript depoda yoktur (K12). Kayıt CI'da da üretilebilmeli, yoksa
    # yalnızca yerelde doğrulanan bir belge olurdu ve o belge sessizce bayatlar.
    written = set(sc) - set(ENTRIES) - set(WRITABLE_NOW)

    errs = integrity(sc, written, WRITABLE_NOW)
    # Manuscript ELDE VARSA türetim onunla karşılaştırılır. Bu kapı, bir oyun
    # yazıldığı hâlde kayıttan düşmediğinde kırmızı yanar.
    if written_disk:
        if written_disk != written:
            only_book = sorted(written_disk - written)
            only_derived = sorted(written - written_disk)
            if only_book:
                errs.append("manuscript'te YAZILMIŞ ama kayıtta hâlâ engelli: %s" % only_book)
            if only_derived:
                errs.append("kayıtta yazılmış sayılıyor ama manuscript'te YOK: %s" % only_derived)
        else:
            print("  ✓ manuscript ile türetilen küme birebir örtüşüyor (%d oyun)"
                  % len(written))
    else:
        print("  · manuscript depoda yok — küme kapsamdan TÜRETİLDİ (%d oyun)"
              % len(written))

    if errs:
        for e in errs:
            print("  ✗ %s" % e)
        print("\n  ⛔ KAYIT KAPSAMLA ÖRTÜŞMÜYOR")
        print("=" * 74)
        return 1

    fam_roll = family_rollup(sc, written, WRITABLE_NOW)
    fam_targets = {k: dict(target=v["target"], deficit=v["deficit"])
                   for k, v in fam_roll.items()}
    rows = compose(root, gi, sc, fam_targets)
    lev = leverage(rows)

    lost_cultures = sorted({r["culture"] for r in rows}
                           - {sc[g]["culture"] for g in written})
    lost_regions = sorted({r["region"] for r in rows}
                          - {sc[g]["region"] for g in written})

    # ── MAKİNE OKUNUR KAYIT ───────────────────────────────────────────────
    payload = {
        "$comment": [
            "KURUCU ARAŞTIRMA BOŞLUK KAYDI — ÜRETİLMİŞ DOSYA",
            "(04_BUILD/build_gap_register.py). ELLE DÜZENLEMEYİN.",
            "",
            "Bu dosya YALNIZCA kurucu müdahalesi olmadan yazılamayan oyunları",
            "taşır. Kaynağı elde olan ve sıra bekleyen oyunlar `writableNow`",
            "alanındadır ve bir ENGEL değildir.",
            "",
            "İKİ EKSEN: `status` kaynak avının KANIT durumudur (BLOCKED /",
            "SOURCE-PENDING / UNRESOLVED); `primaryBlocker` oyunun YAZILAMAMA",
            "sebebidir (P1…P10). Denenmemiş bir kaynağı 'engelli' saymak",
            "Faz 3'ün hatasıydı ve bu ayrım onu tekrarlamayı imkânsız kılar.",
            "",
            "SAYFA NUMARASI UYDURULMAZ: buradaki her locator projenin kendi",
            "source_verification.json kaydından ya da bir batch raporundan gelir.",
        ],
        "version": "1.0",
        "generatedBy": "04_BUILD/build_gap_register.py",
        "scopeTarget": len(sc),
        "written": len(written),
        "writableWithoutFounder": len(WRITABLE_NOW),
        "founderResearchRequired": len(rows),
        "unattempted": 0,
        "statusCounts": {
            s: sum(1 for r in rows if r["status"] == s)
            for s in ("BLOCKED", "SOURCE-PENDING", "UNRESOLVED")},
        "blockerCounts": {
            c: sum(1 for r in rows if r["primaryBlocker"] == c)
            for c in sorted(BLOCKER_NAMES, key=lambda x: int(x[1:]))
            if any(r["primaryBlocker"] == c for r in rows)},
        "priorityCounts": {
            c: sum(1 for r in rows if r["priorityClass"] == c)
            for c in "ABCDE"},
        "familyGap": fam_roll,
        "culturesLostIfUnresolved": lost_cultures,
        "regionsLostIfUnresolved": lost_regions,
        "sourceLeverage": [
            {"work": k, "citation": WORKS[k]["citation"],
             "attemptEvidence": WORKS[k]["attemptEvidence"],
             "unlocks": len(v), "games": sorted(v)} for k, v in lev],
        "writableNow": [{"gameId": k, "hit": v} for k, v in sorted(WRITABLE_NOW.items())],
        "deliveryRoot": "06_FOUNDER_DELIVERY/",
        "ingestTool": "04_BUILD/founder_delivery_ingest.py",
        "games": rows,
    }

    # ── BELGELER ──────────────────────────────────────────────────────────
    L = render_register(rows, fam_roll, written, WRITABLE_NOW, None)
    L = render_register_2(L, rows, lev, lost_cultures, lost_regions)
    L = render_entries(L, rows)
    L.append("---")
    L.append("")
    L.append("## 9 · TESLİM VE ALIM")
    L.append("")
    L.append("Teslim yapısı ve alım hattı için:")
    L.append("[`FOUNDER_RESEARCH_PACK.md`](FOUNDER_RESEARCH_PACK.md) § 1 ve § 4.")
    L.append("")
    L.append("Alım aracı: `04_BUILD/founder_delivery_ingest.py`")
    L.append("")
    reg_md = "\n".join(L) + "\n"

    P = render_pack(rows, lev)
    P = render_pack_tail(P, rows)
    pack_md = "\n".join(P) + "\n"

    targets = [
        (os.path.join(root, "01_SOURCE", "founder_research_gap_register.json"),
         json.dumps(payload, ensure_ascii=False, indent=2) + "\n"),
        (os.path.join(root, "06_REPORTS", "FOUNDER_RESEARCH_GAP_REGISTER.md"), reg_md),
        (os.path.join(root, "06_REPORTS", "FOUNDER_RESEARCH_PACK.md"), pack_md),
    ]

    stale = []
    for p, body in targets:
        old = None
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                old = fh.read()
        if old != body:
            stale.append(os.path.relpath(p, root))
            if not args.check:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(body)

    print()
    print("  kapsam hedefi                 : %d" % len(sc))
    print("  yazılmış                      : %d" % len(written))
    print("  kurucusuz yazılabilir         : %d" % len(WRITABLE_NOW))
    print("  KURUCU ARAŞTIRMASI GEREKEN    : %d" % len(rows))
    print("      BLOCKED                   : %d" % payload["statusCounts"]["BLOCKED"])
    print("      SOURCE-PENDING            : %d" % payload["statusCounts"]["SOURCE-PENDING"])
    print("      UNRESOLVED                : %d" % payload["statusCounts"]["UNRESOLVED"])
    print("  UNATTEMPTED                   : 0")
    print()
    print("  en yüksek kaldıraç            : %s → %d madde"
          % (WORKS[lev[0][0]]["citation"].split(" (")[0], len(lev[0][1])))
    print("  kaybedilecek kültür           : %d" % len(lost_cultures))
    print("  kaybedilecek bölge            : %d" % len(lost_regions))
    print()

    if args.json:
        dump(os.path.join(root, args.json), {k: v for k, v in payload.items() if k != "games"})

    if args.check and stale:
        for s in stale:
            print("  ✗ BAYAT: %s" % s)
        print("\n  ⛔ kayıt bayat — ./04_BUILD/build_gap_register.py koşturun")
        print("=" * 74)
        return 1
    for p, _ in targets:
        print("  ✓ %s" % os.path.relpath(p, root))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
