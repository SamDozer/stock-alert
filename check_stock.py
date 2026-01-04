import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import os

URL = "https://drinkyerbanow.com/pd/941292?src=/shop"

EMAIL_FROM = "yourgmail@gmail.com"
EMAIL_TO = "lipophilicbanana12@duck.com"
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

def send_email():
    msg = MIMEText(f"Item is back in stock:\n{URL}")
    msg["Subject"] = "Back in Stock Alert"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

r = requests.get(URL, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

if "out of stock" not in soup.get_text().lower():
    send_email()
