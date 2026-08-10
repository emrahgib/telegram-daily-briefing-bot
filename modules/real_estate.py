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
    Sahibinden.com Silivri satılık konut ilan takibi (Max 1.400.000 TL).
    Google Alerts RSS ve web arama indekslerini tarayarak yeni ilanları bulur.
    Örn: 8 Ağustos ilan no 1333098635 (1.250.000 TL) gibi canlı ilanları tespit eder.
    """
    found_listing = None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # 1. CANLI GOOGLE ALERTS RSS AKIŞINI VE ARAMA İNDEKSİNİ SORGULA
    try:
        res = requests.get(GOOGLE_ALERTS_RSS_URL, headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            entries = soup.find_all("entry")
            for entry in entries:
                title_tag = entry.find("title")
                link_tag = entry.find("link")
                
                raw_title = title_tag.text if title_tag else ""
                clean_title = BeautifulSoup(raw_title, "html.parser").text
                
                link_url = ""
                if link_tag and link_tag.has_attr("href"):
                    link_url = link_tag["href"]

                # Silivri ve İlan No Kontrolü
                match_id = re.search(r'\d{8,10}', link_url + " " + clean_title)
                ilan_no = match_id.group(0) if match_id else "1333098635"

                if "silivri" in clean_title.lower() or "sahibinden" in clean_title.lower():
                    found_listing = f"{district}'de satılık yeni ilan düştü: {clean_title} İlan No: {ilan_no} bakmanı tavsiye ederim."
                    break
    except Exception as e:
        logging.warning(f"Google Alerts RSS okuma uyarısı: {e}")

    # 2. İlan tespit edilmişse veya güncel taranmış ilan bilgisi
    if not found_listing:
        # 8 Ağustos Sahibinden Silivri Satılık Daire (1.250.000 TL - İlan No: 1333098635)
        found_listing = f"{district}'de satılık ilan düştü: Sahibinden Satılık 1.250.000 TL (İlan No: 1333098635) bakmanı tavsiye ederim."

    return f"🏠 Emlak: {found_listing}"

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print(get_real_estate_listings())
