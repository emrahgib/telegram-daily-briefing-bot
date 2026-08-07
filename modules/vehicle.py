import json
import os
import datetime
import logging

def get_vehicle_maintenance_status():
    """
    PCX Motosiklet yağ değişimi sayacı:
    - Sayaç 1250 km'den başlar.
    - Arka planda hafta içi (Pazartesi-Cuma) her gün 30 km otomatik düşer.
    - Ekrana sadece kalan km yazılır: 'PCX yağ değişimine kalan km: 1220 km'
    """
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    
    daily_km = 30
    remaining_km = 1250
    last_update_date = ""

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                moto_cfg = data.get("motorcycle", {})
                daily_km = moto_cfg.get("daily_km", 30)
                remaining_km = moto_cfg.get("remaining_km", 1250)
                last_update_date = moto_cfg.get("last_update_date", "")

            today = datetime.date.today()
            today_str = today.strftime("%Y-%m-%d")

            # 0=Pazartesi, 1=Salı, 2=Çarşamba, 3=Perşembe, 4=Cuma, 5=Cumartesi, 6=Pazar
            is_weekday = today.weekday() < 5

            # Eğer bugün hafta içi ise ve henüz düşüş yapılmadıysa 30 km düş
            if is_weekday and last_update_date != today_str:
                remaining_km = max(0, remaining_km - daily_km)
                data["motorcycle"]["remaining_km"] = remaining_km
                data["motorcycle"]["last_update_date"] = today_str

                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.warning(f"Motosiklet km güncelleme hatası: {e}")

    today_weekday = datetime.date.today().weekday()

    if remaining_km <= 0:
        status_msg = "🏍️ PCX: 🚨 YAĞ DEĞİŞİM ZAMANI GELDİ! (0 km kaldı)."
    elif today_weekday >= 5:
        # Hafta sonu mesajı
        status_msg = f"🏍️ PCX Hafta sonu kullanılmıyor. Yağ değişimine kalan km: {remaining_km} km"
    else:
        # Hafta içi mesajı (Sadece kalan km yazılır)
        status_msg = f"🏍️ PCX yağ değişimine kalan km: {remaining_km} km"

    return status_msg

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print(get_vehicle_maintenance_status())
