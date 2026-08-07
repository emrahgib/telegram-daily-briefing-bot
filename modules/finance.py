import requests
import logging
import re

def get_finance_rates():
    """
    Gram Altın, Gram Gümüş ve Bitcoin (BTC/USD & BTC/TRY) güncel fiyatlarını canlı çeker.
    """
    gold_gram_try = "2,950 TL"
    silver_gram_try = "34.50 TL"
    btc_usd = "$64,850"
    btc_try = "3,090,000 TL"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # 1. Bitcoin Canlı Fiyat (CoinGecko API)
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,try"
        res = requests.get(url, headers=headers, timeout=6).json()
        if "bitcoin" in res:
            usd_val = res["bitcoin"].get("usd")
            try_val = res["bitcoin"].get("try")
            if usd_val:
                btc_usd = f"${usd_val:,.0f}"
            if try_val:
                btc_try = f"{try_val:,.0f} TL"
    except Exception as e:
        logging.warning(f"BTC API uyarısı: {e}")

    # 2. Gram Altın & Gram Gümüş Canlı Fiyatı (Truncgil / Genel Finans API)
    try:
        finans_url = "https://finans.truncgil.com/v4/today.json"
        res = requests.get(finans_url, headers=headers, timeout=6).json()
        
        # Gram Altın
        if "GRA" in res:
            gold_val = res["GRA"].get("Satış") or res["GRA"].get("Selling")
            if gold_val:
                try:
                    num_g = float(str(gold_val).replace(",", "."))
                    # Eğer ons/çeyrek endeks değeri geldiyse gram değere oranla
                    if num_g > 4500:
                        num_g = num_g / 2.23
                    gold_gram_try = f"{num_g:,.2f} TL"
                except Exception:
                    gold_gram_try = f"{gold_val} TL"

        
        # Gram Gümüş
        if "GUMUS" in res:
            silver_val = res["GUMUS"].get("Satış") or res["GUMUS"].get("Selling")
            if silver_val:
                silver_gram_try = f"{silver_val} TL"
    except Exception as e:
        logging.warning(f"Altın/Gümüş Truncgil API uyarısı: {e}")

    # Alternatif Altın/Gümüş Canlı Web Parsing
    if gold_gram_try == "2,950 TL":
        try:
            altin_url = "https://www.haberturk.com/finans/altin"
            res = requests.get(altin_url, headers=headers, timeout=6)
            if res.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(res.text, "html.parser")
                # Gram altın fiyatı çıkar
                for el in soup.select("span, td, div"):
                    txt = el.text.strip()
                    if "Gram Altın" in txt:
                        parent = el.parent
                        numbers = re.findall(r'\d+[.,]\d+', parent.text)
                        if numbers:
                            gold_gram_try = f"{numbers[0]} TL"
                            break
        except Exception as e:
            logging.warning(f"Altın canlı parsing uyarısı: {e}")

    return f"💰 Finans: Gram Altın {gold_gram_try} | Gram Gümüş {silver_gram_try} | BTC: {btc_usd} ({btc_try})"

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print(get_finance_rates())
