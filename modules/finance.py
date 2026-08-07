import requests
from bs4 import BeautifulSoup
import logging
import re

def get_finance_rates():
    """
    Doviz.com ve CoinGecko üzerinden canlı Gram Altın, Gram Gümüş ve Bitcoin (BTC/USD & BTC/TRY) fiyatlarını çeker.
    """
    gold_gram_try = "6.616,17 TL"
    silver_gram_try = "98,79 TL"
    btc_usd = "$64,850"
    btc_try = "3,090,000 TL"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    # 1. Doviz.com Canlı Serbest Piyasa Gram Altın & Gram Gümüş
    try:
        res = requests.get("https://www.doviz.com/", headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            gold_el = soup.find("span", {"data-socket-key": "gram-altin"})
            silver_el = soup.find("span", {"data-socket-key": "gumus"})
            
            if gold_el and gold_el.text.strip():
                gold_gram_try = f"{gold_el.text.strip()} TL"
            if silver_el and silver_el.text.strip():
                silver_gram_try = f"{silver_el.text.strip()} TL"
    except Exception as e:
        logging.warning(f"Doviz.com canlı sorgu uyarısı: {e}")

    # 2. Bitcoin Canlı Fiyat (CoinGecko API)
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,try"
        res_btc = requests.get(url, headers=headers, timeout=6).json()
        if "bitcoin" in res_btc:
            usd_val = res_btc["bitcoin"].get("usd")
            try_val = res_btc["bitcoin"].get("try")
            if usd_val:
                btc_usd = f"${usd_val:,.0f}"
            if try_val:
                btc_try = f"{try_val:,.0f} TL"
    except Exception as e:
        logging.warning(f"BTC API uyarısı: {e}")

    return f"💰 Finans: Gram Altın {gold_gram_try} | Gram Gümüş {silver_gram_try} | BTC: {btc_usd} ({btc_try})"

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print(get_finance_rates())
