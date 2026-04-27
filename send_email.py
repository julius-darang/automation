import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- Config (loaded from GitHub Secrets) ---
SENDER_EMAIL    = os.environ["SENDER_EMAIL"]
SENDER_PASSWORD = os.environ["SENDER_PASSWORD"]
RECEIVER_EMAIL  = os.environ["RECEIVER_EMAIL"]

# --- Email content ---
subject = "Daily Check-in 👋"
body = f"""
Hey Julius,

This is your automated daily email — sent at 2PM PH time via GitHub Actions.

Date: {datetime.utcnow().strftime('%B %d, %Y')}

This is just a test. We'll make this more useful soon.

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

print(f"Email sent to {RECEIVER_EMAIL}")