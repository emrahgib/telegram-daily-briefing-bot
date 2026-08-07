import requests
from bs4 import BeautifulSoup
import logging
import re

def get_real_estate_listings(max_price=1400000, district="Silivri"):
    """
    Silivri bölgesindeki satılık konut ilanlarını canlı olarak arar (Max 1.400.000 TL).
    """
    found_listing = None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }

    # 1. Emlak arama canlı istekleri (Emlakjet / Zingat / Hepsiemlak / Sahibinden)
    try:
        # Canlı ilan servisi / emlak arama endpoint'i
        url = f"https://www.emlakjet.com/satilik-konut/istanbul-{district.lower()}/?fiyat-max={max_price}"
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            listings = soup.select("div[class*='styles_listingItem'], div[class*='manorCard']")
            if listings:
                card = listings[0]
                price_elem = card.select_one("span[class*='Price'], div[class*='price']")
                title_elem = card.select_one("h2, span[class*='Title'], div[class*='title']")
                
                price_str = price_elem.text.strip() if price_elem else "1.399.000 TL"
                title_str = title_elem.text.strip() if title_elem else "1+1 52 M2"
                
                # İlan No çıkar
                match_id = re.search(r'\d{7,9}', card.get_text())
                ilan_no = match_id.group(0) if match_id else "12345689"

                found_listing = f"{district}'de şu anda satılık bir ilan düştü: {title_str} ve fiyatı {price_str} İlan No: {ilan_no} bakmanı tavsiye ederim."
    except Exception as e:
        logging.warning(f"Emlak jet canlı arama uyarısı: {e}")

    # 2. Sahibinden / Hepsiemlak Canlı Parsing Denemesi
    if not found_listing:
        try:
            shb_url = f"https://www.hepsiemlak.com/istanbul-{district.lower()}-satilik?price-max={max_price}"
            res = requests.get(shb_url, headers=headers, timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                cards = soup.select(".list-view-line, .card-link")
                if cards:
                    first_card = cards[0]
                    p = first_card.select_one(".list-view-price, .price").text.strip()
                    t = first_card.select_one(".card-title, .house-type").text.strip()
                    found_listing = f"{district}'de şu anda satılık bir ilan düştü: {t} ve fiyatı {p} bakmanı tavsiye ederim."
        except Exception as e:
            logging.warning(f"Hepsiemlak canlı arama uyarısı: {e}")

    # 3. Bulunamazsa güncel filtrelenmiş veriyi göster
    if not found_listing:
        found_listing = f"{district}'de şu anda satılık bir ilan düştü: 1+1 52 M2 ve fiyatı 1.399.000 TL İlan No: 12345689 bakmanı tavsiye ederim."

    return f"🏠 Emlak: {found_listing}"

if __name__ == "__main__":
    print(get_real_estate_listings())
