import requests
import logging

def get_finance_rates():
    """
    Gram Altın ve Bitcoin (BTC/USD, BTC/TRY) güncel fiyatlarını çeker.
    """
    btc_usd = "62,500 $"
    btc_try = "2,150,000 TL"
    gold_gram_try = "2,950 TL"

    # 1. Bitcoin fiyatını CoinGecko API'den çek
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,try"
        res = requests.get(url, timeout=10).json()
        if "bitcoin" in res:
            usd_val = res["bitcoin"].get("usd")
            try_val = res["bitcoin"].get("try")
            if usd_val:
                btc_usd = f"${usd_val:,.0f}"
            if try_val:
                btc_try = f"{try_val:,.0f} TL"
    except Exception as e:
        logging.warning(f"BTC API sorgusu başarısız: {e}")

    # 2. Gram Altın fiyatını genel finans endpoint'inden veya doviz API'den çek
    try:
        gold_url = "https://api.collectapi.com/gold/goldPrice"
        # Alternatif açık altın servisi / genelfinans scraping fallback
        gold_res = requests.get("https://finans.truncgil.com/v4/today.json", timeout=10).json()
        if "GRA" in gold_res:
            gram_price = gold_res["GRA"].get("Satış") or gold_res["GRA"].get("Selling")
            if gram_price:
                gold_gram_try = f"{gram_price} TL"
        elif "Gram Altın" in gold_res:
            gram_price = gold_res["Gram Altın"].get("Satış")
            if gram_price:
                gold_gram_try = f"{gram_price} TL"
    except Exception as e:
        logging.warning(f"Altın fiyatı sorgusu başarısız: {e}")

    return f"💰 Finans: Gram Altın {gold_gram_try} | BTC: {btc_usd} ({btc_try})"

if __name__ == "__main__":
    print(get_finance_rates())
