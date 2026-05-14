"""
One-time SMTP setup. Run: python setup_smtp.py
"""
import json, os, smtplib, sys

BASE          = os.path.dirname(os.path.abspath(__file__))
VAULT         = os.path.join(BASE, "vault")
SETTINGS_FILE = os.path.join(VAULT, "settings.json")

PROVIDERS = {
    "1": ("Gmail",       "smtp.gmail.com",      587),
    "2": ("Outlook/365", "smtp.office365.com",  587),
    "3": ("Yahoo",       "smtp.mail.yahoo.com", 587),
    "4": ("iCloud",      "smtp.mail.me.com",    587),
    "5": ("Custom",      "",                    587),
}

print()
print("  AI Bookkeeping Specialist — SMTP Setup")
print("  " + "=" * 40)
print(f"  Saving to: {SETTINGS_FILE}")
print()
for k, (name, _, _) in PROVIDERS.items():
    print(f"    {k}. {name}")
print()

choice = input("  Provider [1=Gmail]: ").strip() or "1"
_, host, port = PROVIDERS.get(choice, PROVIDERS["1"])

if choice == "5":
    host = input("  SMTP host: ").strip()
    port = int(input("  SMTP port [587]: ").strip() or "587")

print()
user     = input(f"  Email address: ").strip()
password = input("  App Password (visible — delete history after): ").strip()
print()

print("  Testing connection…")
try:
    with smtplib.SMTP(host, port, timeout=12) as srv:
        srv.ehlo()
        srv.starttls()
        srv.login(user, password)
    print("  Connection OK")
except smtplib.SMTPAuthenticationError:
    print("  Auth failed — check your App Password.")
    sys.exit(1)
except Exception as e:
    print(f"  Connection error: {e}")
    sys.exit(1)

os.makedirs(VAULT, exist_ok=True)
try:
    with open(SETTINGS_FILE) as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {}

data.update({
    "smtp_host":      host,
    "smtp_port":      port,
    "smtp_user":      user,
    "smtp_password":  password,
    "smtp_from_addr": user,
})
with open(SETTINGS_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"  Saved to: {SETTINGS_FILE}")
print()
