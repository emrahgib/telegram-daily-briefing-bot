import requests
import logging
from bs4 import BeautifulSoup
import re

def get_fuel_prices():
    """
    İstanbul güncel Motorin ve Benzin akaryakıt litre fiyatlarını canlı sorgular.
    """
    benzin_price = "64.45"
    motorin_price = "79.67"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    # 1. Opet Canlı Akaryakıt API Sorgusu (İstanbul / 34)
    try:
        url = "https://api.opet.com.tr/api/fuelprices/prices?ProvinceCode=34"
        res = requests.get(url, headers=headers, timeout=8).json()
        if isinstance(res, list) and len(res) > 0:
            for item in res:
                product_name = item.get("ProductName", "").lower()
                amount = item.get("Amount")
                if amount and amount > 0:
                    if "benzin" in product_name or "kurşunsuz" in product_name:
                        benzin_price = f"{amount:.2f}"
                    elif "motorin" in product_name or "dizel" in product_name or "ultraforce" in product_name:
                        motorin_price = f"{amount:.2f}"
    except Exception as e:
        logging.warning(f"Opet akaryakıt API sorgu uyarısı: {e}")

    # 2. Petrol Ofisi / Shell Canlı Web Parsing Fallback
    if benzin_price == "64.45":
        try:
            po_url = "https://www.petrolofisi.com.tr/akaryakit-fiyatlari"
            res = requests.get(po_url, headers=headers, timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                rows = soup.select("table tbody tr")
                for row in rows:
                    txt = row.get_text().lower()
                    if "istanbul" in txt or "34" in txt:
                        cols = row.select("td")
                        if len(cols) >= 3:
                            benzin_price = re.search(r'\d+[.,]\d+', cols[1].text).group(0) if re.search(r'\d+[.,]\d+', cols[1].text) else cols[1].text.strip()
                            motorin_price = re.search(r'\d+[.,]\d+', cols[2].text).group(0) if re.search(r'\d+[.,]\d+', cols[2].text) else cols[2].text.strip()
                            break
        except Exception as e:
            logging.warning(f"PO akaryakıt parsing uyarısı: {e}")

    # Boşluk ve yeni satır temizliği
    benzin_clean = re.search(r'\d+[.,]\d+', str(benzin_price))
    motorin_clean = re.search(r'\d+[.,]\d+', str(motorin_price))
    
    benzin_final = benzin_clean.group(0) if benzin_clean else benzin_price
    motorin_final = motorin_clean.group(0) if motorin_clean else motorin_price

    return f"⛽ Akaryakıt fiyatları listesi: motorin {motorin_final} benzin {benzin_final}"


if __name__ == "__main__":
    print(get_fuel_prices())
