import requests
import logging

def get_fuel_prices():
    """
    İstanbul güncel Benzin ve Motorin akaryakıt litre fiyatlarını getirir.
    """
    benzin_price = "64.45"
    motorin_price = "79.67"

    try:
        # Akaryakıt API / Web scraping sorgusu
        url = "https://api.opet.com.tr/api/fuelprices/prices?ProvinceCode=34"
        res = requests.get(url, timeout=10).json()
        if isinstance(res, list) and len(res) > 0:
            for item in res:
                product_name = item.get("ProductName", "").lower()
                price = item.get("Amount")
                if price:
                    if "benzin" in product_name or "kurşunsuz" in product_name:
                        benzin_price = f"{price:.2f}"
                    elif "motorin" in product_name or "dizel" in product_name:
                        motorin_price = f"{price:.2f}"
    except Exception as e:
        logging.warning(f"Akaryakıt fiyat sorgusu varsayılan modda: {e}")

    return f"⛽ Akaryakıt: Motorin {motorin_price} TL | Benzin {benzin_price} TL"

if __name__ == "__main__":
    print(get_fuel_prices())
