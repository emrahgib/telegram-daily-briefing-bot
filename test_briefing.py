import sys
import io

# Windows terminali için stdout UTF-8 yapılandırması
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from modules.telegram_service import compose_daily_briefing, send_telegram_message

if __name__ == "__main__":
    print("==================================================")
    print("GÜNLÜK BİLDİRİM BOTU TEST ÇALIŞTIRMASI")
    print("==================================================")
    
    msg = compose_daily_briefing()
    print("\n--- OLUŞTURULAN TEST MESAJI ---\n")
    print(msg)
    print("--------------------------------\n")
    
    # Telegram'a göndermeyi dene
    success, note = send_telegram_message(msg)
    print(f"Gönderim Sonucu: {success} ({note})")

