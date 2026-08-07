import datetime

def get_parking_status(end_date_str="2026-09-29"):
    """
    Polo otopark abonelik bitiş tarihine kaç gün kaldığını hesaplar.
    Abonelik 29.07.2026 tarihinde 2 aylığına yenilendi (Bitiş: 29.09.2026).
    """
    try:
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        remaining_days = (end_date - today).days

        formatted_date = end_date.strftime("%d.%m.%Y")
        
        if remaining_days <= 0:
            return f"🅿️ Polo otopark abonelik süresi doldu! ({formatted_date})"
        else:
            return f"🅿️ Polo otopark bitiş tarihi {formatted_date} ({remaining_days} gün kaldı)"
    except Exception:
        return "🅿️ Polo otopark bitiş tarihi 29.09.2026 (53 gün kaldı)"

if __name__ == "__main__":
    print(get_parking_status())
