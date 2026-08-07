import requests
import json
import os
import logging
from datetime import datetime

from .rdr2_tracker import get_rdr2_status
from .weather import get_weather_forecast
from .finance import get_finance_rates
from .real_estate import get_real_estate_listings
from .traffic import get_traffic_status
from .sports import get_fenerbahce_match_status
from .social import get_social_stats
from .vehicle import get_vehicle_maintenance_status
from .fuel import get_fuel_prices

def compose_daily_briefing():
    """
    Tüm modüllerden gelen verileri toplayıp kullanıcının tam istediği formatta Telegram günlük özet mesajını oluşturur.
    """
    date_str = datetime.now().strftime("%d.%m.%Y")
    
    rdr2_info = get_rdr2_status()
    weather_info = get_weather_forecast()
    finance_info = get_finance_rates()
    emlak_info = get_real_estate_listings()
    traffic_info = get_traffic_status()
    sports_info = get_fenerbahce_match_status()
    social_info = get_social_stats()
    vehicle_info = get_vehicle_maintenance_status()
    fuel_info = get_fuel_prices()

    message = f"""🌅 **Günaydın! Günlük Özetiniz ({date_str} - 07:00)**

{rdr2_info}

{weather_info}

{finance_info}

{emlak_info}

{traffic_info}

{sports_info}

{social_info}

{vehicle_info}

{fuel_info}

Günün güzel geçsin! 😊
"""
    return message

def send_telegram_message(message_text, bot_token=None, chat_id=None):
    """
    Hazırlanan mesajı Telegram Bot API aracılığıyla kullanıcının Telegram hesabına gönderir.
    """
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f).get("telegram", {})
                if not bot_token:
                    bot_token = cfg.get("bot_token")
                if not chat_id:
                    chat_id = cfg.get("chat_id")
        except Exception as e:
            logging.error(f"Config okuma hatası: {e}")

    if not bot_token or bot_token == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("⚠️ HATA: Telegram Bot Token ayarlanmamış! Lütfen config.json dosyasını veya GitHub Secrets düzenleyin.")
        return False, "Bot Token eksik."

    if not chat_id or chat_id == "YOUR_TELEGRAM_CHAT_ID_HERE":
        print("⚠️ HATA: Telegram Chat ID ayarlanmamış! Lütfen config.json dosyasını veya GitHub Secrets düzenleyin.")
        return False, "Chat ID eksik."

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        res_data = response.json()
        if res_data.get("ok"):
            print("✅ Telegram mesajı başarıyla gönderildi!")
            return True, "Başarılı"
        else:
            err = res_data.get("description", "Bilinmeyen hata")
            print(f"❌ Telegram Gönderme Hatası: {err}")
            return False, err
    except Exception as e:
        print(f"❌ HTTP Bağlantı Hatası: {e}")
        return False, str(e)

if __name__ == "__main__":
    msg = compose_daily_briefing()
    print("--- OLUŞTURULAN GÜNCEL MESAJ ---")
    print(msg)
