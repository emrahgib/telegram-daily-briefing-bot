# 🤖 Kişisel Telegram Günlük Bildirim Botu

Her sabah saat **07:00**'de (Türkiye Saati - TSI) Telegram hesabınıza kişiselleştirilmiş gün özetini otomatik gönderen Python ve GitHub Actions tabanlı bot.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-green)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot%20API-0088cc)

---

## 📌 Özellikler

1. **🎮 Red Dead Redemption 2 (RDR 2) Fiyat Takibi:** Steam ve Epic Games fiyatları & indirim alarmı.
2. **🌤️ Hava Durumu Tahmini:** İstanbul / Silivri için gündüz/akşam sıcaklıkları, nem oranı ve yağış durumu.
3. **💰 Altın ve Bitcoin (BTC):** Canlı Gram Altın (TRY) ve BTC (USD/TRY) fiyatları.
4. **🏠 Silivri Emlak İlan Takibi:** 1.400.000 TL altı satılık 1+1 / 2+1 ev ilan takibi.
5. **🚗 Kozyatağı - Kartal E5 Trafik Süresi:** Canlı seyahat süresi ve yoğunluk durumu.
6. **⚽ Fenerbahçe Maç Takvimi:** Maç günü, saati ve yayın kanalı (BeIN Sports, ATV vb.).
7. **📲 NEXUSVIDEOS İstatistikleri:** Abone sayısı ve yüklenen video sayısı takibi.
8. **🏍️ Motosiklet Yağ Değişim Sayacı:** Günde 30 km baz alınarak 1600 km'den düşen ve otomatik kaydedilen km sayacı.
9. **⛽ Akaryakıt Fiyatları:** İstanbul güncel Benzin ve Motorin litre fiyatları.

---

## 🚀 GitHub Actions İle 7/24 Ücretsiz ve Bilgisayarı Açmadan Çalıştırma

Bu projeyi bilgisayarınızı açık tutmaya gerek kalmadan tamamen **ücretsiz** olarak GitHub sunucularında çalıştırabilirsiniz.

### 1. Projeyi GitHub'a Yükleyin
- GitHub'da yeni bir repo (Örn: `telegram-daily-briefing-bot`) oluşturun.
- Projenizdeki kodları repoya yükleyin.

### 2. GitHub Secrets (Şifrelerinizi) Ekleyin
GitHub reponuzda **Settings > Secrets and variables > Actions > New repository secret** adımlarını izleyin ve şu 2 gizli değişkeni tanımlayın:

| Secret Adı | Açıklama |
| :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | @BotFather'dan aldığınız bot tokenı |
| `TELEGRAM_CHAT_ID` | @myidbot ile öğrendiğiniz sayısal Chat ID |

### 3. Otomatik Çalışma
- GitHub Actions her sabah saat **07:00 TSI (04:00 UTC)**'de otomatik olarak çalışır ve bildirim atar.
- İsterseniz **Actions** sekmesinden **"Run workflow"** butonuna basarak anında test bildirimi gönderebilirsiniz.

---

## 💻 Yerel (Local) Çalıştırma

```bash
# 1. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 2. config.example.json dosyasını config.json olarak kopyalayın ve bilgilerinizi girin
cp config.example.json config.json

# 3. Anlık test mesajı göndermek için:
python main.py --now

# 4. Yerel zamanlayıcıyı başlatmak için (Her sabah 07:00):
python main.py
```

---

## 📁 Proje Yapısı

```
.
├── .github/workflows/
│   └── daily_briefing.yml   # GitHub Actions otomatik sabah 07:00 zamanlayıcısı
├── modules/                 # Modüler veri kaynakları
│   ├── rdr2_tracker.py      # Steam & Epic Games RDR2 takibi
│   ├── weather.py           # Hava durumu (Open-Meteo API)
│   ├── finance.py           # Altın ve BTC canlı fiyatları
│   ├── real_estate.py       # Silivri emlak ilan takibi
│   ├── traffic.py           # Kozyatağı-Kartal E-5 trafik süresi
│   ├── sports.py            # Fenerbahçe maç takvimi
│   ├── social.py            # NEXUSVIDEOS kanal istatistikleri
│   ├── vehicle.py           # Motosiklet km/yağ sayacı
│   ├── fuel.py              # Akaryakıt fiyatları
│   └── telegram_service.py  # Telegram bildirim oluşturucu
├── config.example.json      # Örnek yapılandırma şablonu
├── main.py                  # Ana zamanlayıcı ve çalıştırıcı
├── test_briefing.py         # Anlık test çalıştırma betiği
└── requirements.txt         # Gerekli Python kütüphaneleri
```
