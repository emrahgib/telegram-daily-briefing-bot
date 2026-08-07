import requests
import logging

def get_rdr2_status():
    """
    Steam ve Epic Games üzerinden RDR 2 (Red Dead Redemption 2) fiyat ve indirim durumunu sorgular.
    """
    steam_price = "30 $"
    epic_price = "2500 TL"
    discount_status = "indirim gelmedi."
    
    # 1. Steam Store API Query for AppID 1174180 (Red Dead Redemption 2)
    try:
        url = "https://store.steampowered.com/api/appdetails?appids=1174180&cc=us"
        res = requests.get(url, timeout=10).json()
        if res.get("1174180", {}).get("success"):
            price_data = res["1174180"]["data"].get("price_overview", {})
            if price_data:
                final_price = price_data.get("final_formatted", "")
                discount = price_data.get("discount_percent", 0)
                if final_price:
                    steam_price = final_price
                if discount > 0:
                    discount_status = f"%{discount} İNDİRİM VAR! Fiyat: {final_price}"
    except Exception as e:
        logging.warning(f"Steam RDR2 sorgusu başarısız: {e}")

    # 2. Epic Games Store GraphQL Query
    try:
        epic_url = "https://graphql.epicgames.com/graphql"
        query = {
            "query": """
            {
              Catalog {
                searchStore(keywords: "Red Dead Redemption 2", category: "games", limit: 1) {
                  elements {
                    title
                    price(country: "TR") {
                      totalPrice {
                        fmtPrice(discountPrice: "0") {
                          originalPrice
                          discountPrice
                        }
                      }
                    }
                  }
                }
              }
            }
            """
        }
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.post(epic_url, json=query, headers=headers, timeout=10).json()
        elements = res.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])
        if elements:
            price_info = elements[0].get("price", {}).get("totalPrice", {}).get("fmtPrice", {})
            disc_price = price_info.get("discountPrice", "")
            orig_price = price_info.get("originalPrice", "")
            if disc_price:
                epic_price = f"{disc_price} TL" if not disc_price.endswith("TL") and not "$" in disc_price else disc_price
                if orig_price and disc_price != orig_price:
                    discount_status = f"EPİC'TE İNDİRİM VAR! Yeni Fiyat: {epic_price} (Eski: {orig_price})"
    except Exception as e:
        logging.warning(f"Epic Games RDR2 sorgusu başarısız: {e}")

    return f"🎮 RDR2: Epic'te {epic_price}, Steam'de {steam_price}. {discount_status}"

if __name__ == "__main__":
    print(get_rdr2_status())
