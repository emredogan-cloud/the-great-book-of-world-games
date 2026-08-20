# -*- coding: utf-8 -*-
"""Tek bir dizgi (typesetting) geçişi — üç çıktı da buradan geçer.

NEDEN AYRI BİR MODÜL: aynı kural üç yerde ayrı ayrı duruyordu (interior.py,
epub.py, render_diagrams.py). Üçünden ikisi düzeltildiğinde üçüncüsü sessizce
daktilo kesme işaretiyle basmaya devam etti ve bunu ne göz ne de kapı gördü;
kusur ancak BASILMIŞ PDF'in metni taranınca çıktı.

Manuscript DÜZ ASCII kesme işareti taşır ve öyle KALMALIDIR — JSON'da arama,
karşılaştırma ve diff düz karakterle çalışır. Dönüşüm dizgi anındadır, veride
değil.
"""

import re

_RULES = (
    # ‘açılış — harften önce gelmeyen düz tırnak
    (r"(?<![A-Za-zÀ-ÿ0-9])'(?=[A-Za-zÀ-ÿ])", "‘"),
    # don’t — harfler arasında
    (r"(?<=[A-Za-zÀ-ÿ])'(?=[A-Za-zÀ-ÿ])", "’"),
    # pieces’ — harf/rakamdan sonra, boşluk ya da noktalamadan önce
    (r"(?<=[A-Za-zÀ-ÿ0-9])'(?=\s|$|[,.;:!?)\]])", "’"),
    # game.’ ve (Mweso)’ — NOKTALAMANIN ardından gelen kapanış.
    # Üstteki kurallar kendinden önce HARF arıyordu; alıntı bir noktayla
    # ya da parantezle bittiğinde kapanış düz kalıyordu.
    (r"(?<=[.,;:!?)\]])'(?=\s|$|[,.;:!?)\]])", "’"),
    # “çift açılış” ve kapanış
    (r'(?<![A-Za-zÀ-ÿ0-9])"(?=[^\s])', "“"),
    (r'"', "”"),
)


def smart(t):
    """Düz daktilo tırnaklarını dizgi tırnaklarına çevirir.

    Dönüşemeyen düz tırnak kalırsa YÜKSELİR. Sessizce karışık tırnakla
    basmaktansa yapıyı kırmak yeğdir: karışık tırnak (bir yanı daktilo,
    öteki yanı dizgi) hiç dönüştürmemekten daha kötü görünür ve sayfada
    gözle fark edilmez.
    """
    t = str(t)
    for pat, rep in _RULES:
        t = re.sub(pat, rep, t)
    leftover = [c for c in t if c in "'\""]
    if leftover:
        raise ValueError(
            "dizgiye dönüştürülemeyen düz tırnak kaldı: %r içinde %r"
            % (t[:120], leftover))
    return t


def xml_text(t):
    """SVG/XHTML metin düğümü için: önce kaçış, SONRA dizgi.

    Sıra ZORUNLU. `&` kaçışı `&amp;` üretir; dizgi geçişi bunu bozmaz,
    ama ters sırada `&amp;` içindeki `;` kapanış tırnağı kuralını
    yanlış tetikleyebilir.
    """
    t = (str(t).replace("&", "&amp;").replace("<", "&lt;")
         .replace(">", "&gt;"))
    return smart(t)
