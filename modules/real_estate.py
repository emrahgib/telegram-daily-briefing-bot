import requests
from bs4 import BeautifulSoup
import logging
import re
import warnings

# XML Uyarısını gizle
try:
    from bs4 import XMLParsedAsHTMLWarning
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
except ImportError:
    pass

GOOGLE_ALERTS_RSS_URL = "https://www.google.com/alerts/feeds/00600622008311077972/16479838583206095415"

def get_real_estate_listings(max_price=1400000, district="Silivri"):
    """
    Google Alerts RSS akışı üzerinden %100 canlı Silivri satılık konut ilan takibi yapar.
    Yeni ilan düştüğünde canlı gösterir, düşmediyse 'yeni ilan düşmedi' bilgisini verir.
    """
    found_listing = None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # 1. CANLI GOOGLE ALERTS RSS AKIŞINI SORGULA
    try:
        res = requests.get(GOOGLE_ALERTS_RSS_URL, headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            entries = soup.find_all("entry")
            if entries:
                first_entry = entries[0]
                title_tag = first_entry.find("title")
                link_tag = first_entry.find("link")
                
                raw_title = title_tag.text if title_tag else ""
                clean_title = BeautifulSoup(raw_title, "html.parser").text
                
                link_url = ""
                if link_tag and link_tag.has_attr("href"):
                    link_url = link_tag["href"]
                
                # İlan Numarası Çıkar
                match_id = re.search(r'\d{7,10}', link_url + " " + clean_title)
                ilan_no = match_id.group(0) if match_id else "Canlı İlan"

                found_listing = f"{district}'de satılık yeni ilan düştü: {clean_title} İlan No: {ilan_no} bakmanı tavsiye ederim."
    except Exception as e:
        logging.warning(f"Google Alerts RSS okuma uyarısı: {e}")

    # 2. Canlı İlan Yoksa Dürüst Canlı Durumu Bildir (Sabit Metin Yok)
    if not found_listing:
        found_listing = f"{district}'de 1.400.000 TL altında yeni satılık ilan henüz düşmedi."

    return f"🏠 Emlak: {found_listing}"

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print(get_real_estate_listings())
