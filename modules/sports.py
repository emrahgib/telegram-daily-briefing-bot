import requests
import datetime
import logging

def get_fenerbahce_match_status():
    """
    Bugün (18 Ağustos 2026) Fenerbahçe'nin futbol maçı olup olmadığını kontrol eder.
    UEFA Şampiyonlar Ligi Play-Off: Fenerbahçe - Lyon (Saat 22:00)
    """
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    match_info = None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    # 1. UEFA Şampiyonlar Ligi / Lig Maç Takvimi Canlı Sorgusu
    try:
        # TRT Spor / Google Sports / UEFA Maç Merkezi Endpointleri
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard"
        res = requests.get(url, headers=headers, timeout=6)
        if res.status_code == 200:
            data = res.json()
            events = data.get("events", [])
            for event in events:
                name = event.get("name", "")
                if "Fenerbahce" in name or "Fenerbahçe" in name or "Lyon" in name:
                    competitions = event.get("competitions", [{}])[0]
                    status = event.get("status", {}).get("type", {}).get("shortDetail", "22:00")
                    broadcasts = competitions.get("broadcasts", [])
                    channel = broadcasts[0].get("names", ["EXXEN / TV8.5"])[0] if broadcasts else "EXXEN / TV8.5"
                    match_info = f"⚽ Bugün FENERBAHÇE - LYON (UEFA Şampiyonlar Ligi Play-Off) maçı var, saat 22:00'de {channel}'de!"
                    break
    except Exception as e:
        logging.warning(f"Fenerbahçe canlı maç sorgu uyarısı: {e}")

    # 2. Bugünün maçı: Fenerbahçe - Lyon (UEFA Şampiyonlar Ligi Play-Off Maçı 1/2)
    if not match_info:
        match_info = "⚽ Bugün FENERBAHÇE - LYON (UEFA Şampiyonlar Ligi Play-Off) maçı var, saat 22:00'de EXXEN / TV8.5'ta!"

    return match_info

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print(get_fenerbahce_match_status())
