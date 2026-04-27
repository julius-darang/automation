import smtplib
import os
import urllib.request
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz

# --- Config ---
SENDER_EMAIL    = os.environ["SENDER_EMAIL"]
SENDER_PASSWORD = os.environ["SENDER_PASSWORD"]
RECEIVER_EMAIL  = os.environ["RECEIVER_EMAIL"]

# --- Date & Time (PH) ---
ph_tz   = pytz.timezone("Asia/Manila")
now     = datetime.now(ph_tz)
date_str = now.strftime("%B %d, %Y")
day_str  = now.strftime("%A")

# --- Weather (Davao City) ---
def get_weather():
    try:
        # Open-Meteo — free, no API key needed
        url = "https://api.open-meteo.com/v1/forecast?latitude=7.0707&longitude=125.6087&current=temperature_2m,weathercode,windspeed_10m,relative_humidity_2m&timezone=Asia%2FManila"
        with urllib.request.urlopen(url, timeout=10) as res:
            data = json.loads(res.read())
        current  = data["current"]
        temp     = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind     = current["windspeed_10m"]
        code     = current["weathercode"]

        # Map weather code to description
        weather_map = {
            0: "Clear sky ☀️", 1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅",
            3: "Overcast ☁️", 45: "Foggy 🌫️", 48: "Foggy 🌫️",
            51: "Light drizzle 🌦️", 53: "Drizzle 🌦️", 55: "Heavy drizzle 🌧️",
            61: "Light rain 🌧️", 63: "Rain 🌧️", 65: "Heavy rain 🌧️",
            80: "Rain showers 🌦️", 81: "Rain showers 🌦️", 82: "Heavy showers ⛈️",
            95: "Thunderstorm ⛈️", 96: "Thunderstorm ⛈️", 99: "Thunderstorm ⛈️",
        }
        description = weather_map.get(code, "Unknown")

        return f"{description} | {temp}°C | Humidity: {humidity}% | Wind: {wind} km/h"
    except Exception as e:
        return f"Weather unavailable ({e})"

# --- Motivational Quote (ZenQuotes — free, no API key) ---
def get_quote():
    try:
        url = "https://zenquotes.io/api/random"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read())
        quote  = data[0]["q"]
        author = data[0]["a"]
        return f'"{quote}"\n— {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"

# --- Fetch data ---
weather = get_weather()
quote   = get_quote()

# --- Email content ---
subject = f"Daily Brief — {day_str}, {date_str}"
body = f"""
Good afternoon, Julius!

━━━━━━━━━━━━━━━━━━━━━━━━
📅  {day_str}, {date_str}
━━━━━━━━━━━━━━━━━━━━━━━━

🌤  WEATHER — Davao City
{weather}

━━━━━━━━━━━━━━━━━━━━━━━━

💬  QUOTE OF THE DAY
{quote}

━━━━━━━━━━━━━━━━━━━━━━━━

More upgrades coming soon.

— Your Agent
"""

# --- Build and send ---
msg = MIMEMultipart()
msg["From"]    = SENDER_EMAIL
msg["To"]      = RECEIVER_EMAIL
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

print(f"✅ Email sent to {RECEIVER_EMAIL}")
print(f"   Weather: {weather}")
print(f"   Quote: {quote[:60]}...")