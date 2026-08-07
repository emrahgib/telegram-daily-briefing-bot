import requests
import logging

def get_rdr2_status():
    """
    RDR 2 (Red Dead Redemption 2) fiyat durumunu kontrol eder.
    600 TL altına düşmediği sürece: 'RDR 2 epic ve steamde indirim yok.' yazar.
    600 TL altına düştüğünde ise özel İNDİRİM ALARMI mesajı gönderir.
    """
    rdr2_message = "🎮 RDR 2 epic ve steamde indirim yok."
    target_price_limit_tl = 600

    # 1. Steam Live Query
    try:
        steam_url = "https://store.steampowered.com/api/appdetails?appids=1174180&cc=us"
        res = requests.get(steam_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8).json()
        if res.get("1174180", {}).get("success"):
            price_overview = res["1174180"]["data"].get("price_overview", {})
            if price_overview:
                discount_percent = price_overview.get("discount_percent", 0)
                final_cents = price_overview.get("final", 5999)
                final_usd = final_cents / 100.0
                
                # Tahmini Dolar/TL kuru 34 TL kabul edildiğinde USD -> TL çevrimi
                estimated_tl = final_usd * 34.0
                
                if estimated_tl < target_price_limit_tl or discount_percent >= 50:
                    rdr2_message = f"🎮 🚨 MÜJDE! RDR 2 Steam'de indirime girdi! Fiyat: ${final_usd:.2f} (%{discount_percent} indirim)."
    except Exception as e:
        logging.warning(f"Steam RDR2 kontrol hatası: {e}")

    # 2. Epic Games Live Query
    try:
        epic_gql = "https://graphql.epicgames.com/graphql"
        payload = {
            "query": "{ Catalog { searchStore(keywords: \"Red Dead Redemption 2\", country: \"TR\", locale: \"tr-TR\", limit: 1) { elements { title price(country: \"TR\") { totalPrice { fmtPrice(discountPrice: \"0\") { originalPrice discountPrice } } } } } } }"
        }
        res = requests.post(epic_gql, json=payload, headers={"User-Agent": "Mozilla/5.0"}, timeout=8).json()
        elems = res.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])
        if elems:
            p_info = elems[0].get("price", {}).get("totalPrice", {}).get("fmtPrice", {})
            dp = p_info.get("discountPrice", "")
            op = p_info.get("originalPrice", "")
            
            # Fiyattaki rakamları çıkar (Örn: 500 TL -> 500)
            if dp and dp != op:
                import re
                num_match = re.search(r'\d+', dp.replace(".", "").replace(",", ""))
                if num_match:
                    price_val = int(num_match.group(0))
                    if price_val <= target_price_limit_tl:
                        rdr2_message = f"🎮 🚨 MÜJDE! RDR 2 Epic Games'te {price_val} TL'ye düştü! Kaçırma!"
    except Exception as e:
        logging.warning(f"Epic Games RDR2 kontrol hatası: {e}")

    return rdr2_message

if __name__ == "__main__":
    print(get_rdr2_status())
