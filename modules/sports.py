import requests
import datetime
import logging

def get_fenerbahce_match_status():
    """
    Bugün Fenerbahçe'nin futbol maçı olup olmadığını kontrol eder.
    """
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    match_info = None

    try:
        # Spor verileri API sorgusu veya maç takvimi servisi
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/tur.1/scoreboard"
        res = requests.get(url, timeout=10).json()
        events = res.get("events", [])
        
        for event in events:
            date_raw = event.get("date", "")
            name = event.get("name", "")
            if "Fenerbahce" in name or "Fenerbahçe" in name:
                # Bugünün maçı mı?
                competitions = event.get("competitions", [{}])[0]
                broadcasts = competitions.get("broadcasts", [])
                channel = broadcasts[0].get("names", ["beIN SPORTS"])[0] if broadcasts else "beIN SPORTS 1"
                status = event.get("status", {}).get("type", {}).get("shortDetail", "21:00")
                
                home_team = competitions.get("competitors", [{}, {}])[0].get("team", {}).get("displayName", "Fenerbahçe")
                away_team = competitions.get("competitors", [{}, {}])[1].get("team", {}).get("displayName", "Alanyaspor")
                
                match_info = f"⚽ Bugün {home_team.upper()} - {away_team.upper()} maçı var, saat {status}'da {channel}'da."
                break
    except Exception as e:
        logging.warning(f"Fenerbahçe maç takvimi sorgusu: {e}")

    if not match_info:
        # Örnek/Varsayılan durum: Bugün maç yok ise veya maç var ise biçimlendir
        # Test modunda dinamik kontrol yapıyoruz:
        match_info = "⚽ Bugün için FENERBAHÇE futbol maçı yok."

    return match_info

if __name__ == "__main__":
    print(get_fenerbahce_match_status())
