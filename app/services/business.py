from typing import Dict, List, Optional
from app.core.config import settings
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

WILAYAS_DATA = {
    1: {"name": "Adrar", "shipping": 1200},
    2: {"name": "Chlef", "shipping": 500},
    3: {"name": "Laghouat", "shipping": 800},
    4: {"name": "Oum El Bouaghi", "shipping": 700},
    5: {"name": "Batna", "shipping": 700},
    6: {"name": "Béjaïa", "shipping": 500},
    7: {"name": "Biskra", "shipping": 800},
    8: {"name": "Béchar", "shipping": 1200},
    9: {"name": "Blida", "shipping": 350},
    10: {"name": "Bouira", "shipping": 500},
    11: {"name": "Tamanrasset", "shipping": 1500},
    12: {"name": "Tébessa", "shipping": 700},
    13: {"name": "Tlemcen", "shipping": 600},
    14: {"name": "Tiaret", "shipping": 600},
    15: {"name": "Tizi Ouzou", "shipping": 450},
    16: {"name": "Alger", "shipping": 350},
    17: {"name": "Djelfa", "shipping": 800},
    18: {"name": "Jijel", "shipping": 500},
    19: {"name": "Sétif", "shipping": 600},
    20: {"name": "Saïda", "shipping": 700},
    21: {"name": "Skikda", "shipping": 500},
    22: {"name": "Sidi Bel Abbès", "shipping": 600},
    23: {"name": "Annaba", "shipping": 500},
    24: {"name": "Guelma", "shipping": 600},
    25: {"name": "Constantine", "shipping": 600},
    26: {"name": "Médéa", "shipping": 500},
    27: {"name": "Mostaganem", "shipping": 500},
    28: {"name": "M'Sila", "shipping": 700},
    29: {"name": "Mascara", "shipping": 600},
    30: {"name": "Ouargla", "shipping": 1000},
    31: {"name": "Oran", "shipping": 450},
    32: {"name": "El Bayadh", "shipping": 1000},
    33: {"name": "Illizi", "shipping": 1500},
    34: {"name": "Bordj Bou Arréridj", "shipping": 600},
    35: {"name": "Boumerdès", "shipping": 350},
    36: {"name": "El Tarf", "shipping": 600},
    37: {"name": "Tindouf", "shipping": 1500},
    38: {"name": "Tissemsilt", "shipping": 700},
    39: {"name": "El Oued", "shipping": 900},
    40: {"name": "Khenchela", "shipping": 700},
    41: {"name": "Souk Ahras", "shipping": 600},
    42: {"name": "Tipaza", "shipping": 350},
    43: {"name": "Mila", "shipping": 600},
    44: {"name": "Aïn Defla", "shipping": 550},
    45: {"name": "Naâma", "shipping": 1000},
    46: {"name": "Aïn Témouchent", "shipping": 500},
    47: {"name": "Ghardaïa", "shipping": 1000},
    48: {"name": "Relizane", "shipping": 550},
    49: {"name": "El M'Ghair", "shipping": 900},
    50: {"name": "El Menia", "shipping": 1000},
    51: {"name": "Ouled Djellal", "shipping": 900},
    52: {"name": "Bordj Baji Mokhtar", "shipping": 1500},
    53: {"name": "Béni Abbès", "shipping": 1200},
    54: {"name": "Timimoun", "shipping": 1200},
    55: {"name": "Touggourt", "shipping": 1000},
    56: {"name": "Djanet", "shipping": 1500},
    57: {"name": "In Salah", "shipping": 1500},
    58: {"name": "In Guezzam", "shipping": 1500},
}

def get_shipping_fee(wilaya_code: int, quantity: int) -> float:
    # Business rule: Free shipping for 2 or more chairs
    if quantity >= 2:
        return 0.0
    return float(WILAYAS_DATA.get(wilaya_code, {}).get("shipping", 500))

def get_wilaya_name(wilaya_code: int) -> str:
    return WILAYAS_DATA.get(wilaya_code, {}).get("name", "Inconnue")

def send_email(to_email: str, subject: str, body: str):
    if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASSWORD]):
        print(f"Email skip (no config): To {to_email}, Subject: {subject}")
        return

    msg = MIMEMultipart()
    msg['From'] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        if settings.SMTP_TLS:
            server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_telegram_message(message: str):
    if not all([settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID]):
        print("Telegram skip (no config)")
        return

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    try:
        data = urlencode(payload).encode("utf-8")
        request = Request(url, data=data, method="POST")
        with urlopen(request, timeout=10) as response:
            response.read()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
