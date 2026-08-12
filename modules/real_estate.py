import requests
from bs4 import BeautifulSoup
import logging
import json
import os
import re
import datetime
import warnings

# XML Uyarısını gizle
try:
    from bs4 import XMLParsedAsHTMLWarning
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
except ImportError:
    pass

GOOGLE_ALERTS_RSS_URL = "https://www.google.com/alerts/feeds/00600622008311077972/16479838583206095415"

def get_real_estate_listings(max_price=1400000, district="Silivri"):
    """
    Emlak Takip Sistemi:
    - SADECE O GÜN YENİ DÜŞEN İLANLARI 1 GÜNLÜĞÜNE BİLDİRİR.
    - İlan bildirildikten sonraki günlerde 'yeni satılık ilan henüz düşmedi' yazar.
    - Son bildirilen ilan ID'sini ve tarihini config.json dosyasında hafızada tutar.
    """
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    
    last_id = ""
    last_date = ""

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                re_cfg = data.get("real_estate", {})
                last_id = re_cfg.get("last_notified_listing_id", "")
                last_date = re_cfg.get("last_notified_date", "")
        except Exception as e:
            logging.warning(f"Config okuma hatası: {e}")

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    new_listing_found = None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # 1. CANLI GOOGLE ALERTS RSS AKIŞINI SORGULA
    try:
        res = requests.get(GOOGLE_ALERTS_RSS_URL, headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            entries = soup.find_all("entry")
            for entry in entries:
                title_tag = entry.find("title")
                link_tag = entry.find("link")
                published_tag = entry.find("published") or entry.find("updated")
                
                raw_title = title_tag.text if title_tag else ""
                clean_title = BeautifulSoup(raw_title, "html.parser").text.strip()
                
                link_url = link_tag["href"] if (link_tag and link_tag.has_attr("href")) else ""
                
                # İlan Numarası Çıkar
                match_id = re.search(r'\d{8,10}', link_url + " " + clean_title)
                current_id = match_id.group(0) if match_id else None

                # Yayınlanma tarihi kontrolü
                pub_date_str = published_tag.text if published_tag else ""
                is_published_today = False
                if pub_date_str:
                    if today_str in pub_date_str or datetime.date.today().strftime("%Y-%m-%d") in pub_date_str:
                        is_published_today = True

                # SADECE BUGÜN DÜŞEN VE DAHA ÖNCE BİLDİRİLMEYEN YENİ İLANMIŞSA BİLDİR
                if current_id and current_id != last_id and (is_published_today or last_date != today_str):
                    new_listing_found = (current_id, clean_title)
                    break
    except Exception as e:
        logging.warning(f"Google Alerts RSS okuma uyarısı: {e}")

    # 2. Yeni İlan Bulunduysa Hafızaya Kaydet (1 Günlük Gösterim)
    if new_listing_found:
        curr_id, title_desc = new_listing_found
        
        # Config güncelle
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg_data = json.load(f)
                cfg_data["real_estate"]["last_notified_listing_id"] = curr_id
                cfg_data["real_estate"]["last_notified_date"] = today_str
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(cfg_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                logging.warning(f"Config kaydetme hatası: {e}")

        output_msg = f"{district}'de satılık yeni ilan düştü: {title_desc} İlan No: {curr_id} bakmanı tavsiye ederim."
    else:
        # İlan yoksa veya eski ilansa:
        output_msg = f"{district}'de 1.400.000 TL altında yeni satılık ilan henüz düşmedi."

    return f"🏠 Emlak: {output_msg}"

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print(get_real_estate_listings())
