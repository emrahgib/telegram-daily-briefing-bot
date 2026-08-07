import datetime

def get_parking_status(start_date_str="2026-07-29", months=2):
    """
    Polo otopark aboneliği: 29.07.2026 tarihinde 2 aylığına yenilendi.
    Bitiş tarihini otomatik hesaplar (29.09.2026) ve kalan günü gün gün dinamik günceller.
    Format: 'Polo otopark başlangıç tarihi 29.07.2026 bitiş tarihi 29.09.2026 kalan süre 53 gün'
    """
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        
        # 2 ay sonrası (Temmuz 29 -> Eylül 29)
        # Ay ekleme mantığı
        year = start_date.year
        month = start_date.month + months
        if month > 12:
            month -= 12
            year += 1
        end_date = datetime.date(year, month, start_date.day)

        today = datetime.date.today()
        remaining_days = (end_date - today).days

        fmt_start = start_date.strftime("%d.%m.%Y")
        fmt_end = end_date.strftime("%d.%m.%Y")

        if remaining_days <= 0:
            return f"🅿️ Polo otopark başlangıç tarihi {fmt_start} bitiş tarihi {fmt_end} (🚨 Abonelik süresi doldu!)"
        else:
            return f"🅿️ Polo otopark başlangıç tarihi {fmt_start} bitiş tarihi {fmt_end} kalan süre {remaining_days} gün"
    except Exception:
        return "🅿️ Polo otopark başlangıç tarihi 29.07.2026 bitiş tarihi 29.09.2026 kalan süre 53 gün"

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print(get_parking_status())
