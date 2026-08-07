import json
import os
import datetime
import logging

def get_vehicle_maintenance_status():
    """
    Motosiklet yağ değişimi kalan km sayacını hesaplar ve config.json dosyasını gün gün günceller.
    """
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    
    daily_km = 30
    remaining_km = 1600
    last_update_date = ""

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                moto_cfg = data.get("motorcycle", {})
                daily_km = moto_cfg.get("daily_km", 30)
                remaining_km = moto_cfg.get("remaining_km", 1600)
                last_update_date = moto_cfg.get("last_update_date", "")

            today_str = datetime.date.today().strftime("%Y-%m-%d")

            # Eğer bugün henüz düşüş yapılmadıysa 30 km düş ve kaydet
            if last_update_date != today_str:
                remaining_km = max(0, remaining_km - daily_km)
                data["motorcycle"]["remaining_km"] = remaining_km
                data["motorcycle"]["last_update_date"] = today_str

                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.warning(f"Motosiklet km güncelleme hatası: {e}")

    if remaining_km <= 0:
        status_msg = "🚨 UYARI: Motosikletinizin yağ değişim zamanı geldi! (0 km kaldı)"
    else:
        status_msg = f"🏍️ Motosiklet: Günde {daily_km} km yol yapıyor. Yağ değişimine {remaining_km} km kaldı."

    return status_msg

if __name__ == "__main__":
    print(get_vehicle_maintenance_status())
