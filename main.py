import time
import sys
import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from modules.telegram_service import compose_daily_briefing, send_telegram_message

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def job_send_briefing():
    logging.info("⏰ Sabah 07:00 Günlük Bildirim Görevi Başlatıldı...")
    briefing_msg = compose_daily_briefing()
    print("\n--- OLUŞTURULAN GÜNLÜK BİLDİRİM ---")
    print(briefing_msg)
    print("-----------------------------------")
    
    success, note = send_telegram_message(briefing_msg)
    if success:
        logging.info("✅ Günlük bildirim Telegram'a başarıyla iletildi.")
    else:
        logging.warning(f"⚠️ Bildirim gönderilemedi: {note}")

def main():
    print("==================================================")
    print("🤖 Kişisel Telegram Günlük Bildirim Botu Başlatıldı")
    print("⏰ Zamanlayıcı: Her Gün Saat 07:00")
    print("==================================================")

    # CLI komut kontrolü: python main.py --now
    if len(sys.argv) > 1 and sys.argv[1] == "--now":
        print("⚡ Test Modu: Anlık özet mesajı oluşturuluyor ve gönderiliyor...")
        job_send_briefing()
        return

    scheduler = BlockingScheduler(timezone="Europe/Istanbul")
    # Her sabah 07:00'ye görev ekle
    scheduler.add_job(job_send_briefing, 'cron', hour=7, minute=0)

    try:
        logging.info("Zamanlayıcı dinlemede... Çıkmak için Ctrl+C tuşlayın.")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot durduruldu.")

if __name__ == "__main__":
    main()
