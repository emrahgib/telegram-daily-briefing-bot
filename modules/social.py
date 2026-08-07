import json
import os
import requests
import logging

def get_social_stats(channel_name="NEXUSVIDEOS"):
    """
    NEXUSVIDEOS kanalı için abone sayısı ve yüklenen video sayısını getirir.
    """
    subscribers = 150
    total_videos = 147

    # Config dosyasından mevcut değerleri oku
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                social_cfg = data.get("social", {})
                subscribers = social_cfg.get("subscribers", subscribers)
                total_videos = social_cfg.get("total_videos", total_videos)
                channel_name = social_cfg.get("channel_name", channel_name)
        except Exception as e:
            logging.warning(f"Social config okuma hatası: {e}")

    return f"📲 X / Platform: {channel_name} kanalınızın abone sayısı {subscribers}, yüklenen video toplam: {total_videos}"

if __name__ == "__main__":
    print(get_social_stats())
