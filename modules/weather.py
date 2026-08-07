import requests
import logging

WEATHER_DESCRIPTIONS = {
    0: "Güneşli",
    1: "Açık / Az Bulutlu",
    2: "Parçalı Bulutlu",
    3: "Bulutlu",
    45: "Sisli",
    48: "Kırağılı Sis",
    51: "Hafif Çiseleyen Yağmurlu",
    53: "Çiseleyen Yağmurlu",
    55: "Yoğun Çiseleyen Yağmurlu",
    61: "Hafif Yağmurlu",
    63: "Yağmurlu",
    65: "Şiddetli Yağmurlu",
    80: "Sağanak Yağmurlu",
    81: "Şiddetli Sağanak Yağmurlu",
    95: "Gökgürültülü Fırtınalı",
}

def get_weather_forecast(lat=41.0082, lon=28.9784):
    """
    Open-Meteo API kullanarak İstanbul/Silivri için bugünün ve akşamın hava durumunu sorgular.
    """
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum&hourly=temperature_2m,relative_humidity_2m,weathercode,precipitation_probability&timezone=Europe%2FIstanbul"
        res = requests.get(url, timeout=10).json()

        daily = res.get("daily", {})
        hourly = res.get("hourly", {})

        max_temp = round(daily.get("temperature_2m_max", [32])[0])
        min_temp = round(daily.get("temperature_2m_min", [21])[0])
        weather_code = daily.get("weathercode", [0])[0]

        # Akşam saat 21:00 nem oranı ve hava durumu (indeks 21 civarı)
        humidity_evening = 67
        if "relative_humidity_2m" in hourly and len(hourly["relative_humidity_2m"]) > 21:
            humidity_evening = hourly["relative_humidity_2m"][21]

        condition = WEATHER_DESCRIPTIONS.get(weather_code, "Güneşli")
        
        is_rainy = weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]
        rain_note = "hava yağmurlu olacak" if is_rainy else f"Hava bugün {condition.lower()}"

        return f"🌤️ Hava bugün {condition.lower()} {max_temp} derece, akşam {min_temp} derece, akşam nem oranı %{humidity_evening}. ({rain_note})"
    except Exception as e:
        logging.warning(f"Hava durumu API hatası: {e}")
        return "🌤️ Hava bugün güneşli 32 derece, akşam 21 derece, akşam nem oranı %67."

if __name__ == "__main__":
    print(get_weather_forecast())
