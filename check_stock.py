import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import os
from pathlib import Path

URL = "https://drinkyerbanow.com/pd/941292?src=/shop"

EMAIL_FROM = "mohamedshely01@gmail.com"
EMAIL_TO = "lipophilicbanana12@duck.com"
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

FLAG_FILE = Path("sent.flag")

def send_email():
    msg = MIMEText(f"The item is BACK IN STOCK:\n\n{URL}")
    msg["Subject"] = "Back in Stock Alert"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

def is_in_stock():
    r = requests.get(URL, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return "out of stock" not in soup.get_text().lower()

try:
    if is_in_stock() and not FLAG_FILE.exists():
        send_email()
        FLAG_FILE.touch()
        print("Email sent. Flag created.")
    else:
        print("Not in stock or already notified.")
except Exception as e:
    print("Error:", e)
