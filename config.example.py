# ============================================================
# AI Bookkeeping Specialist — Subscription Configuration
# Copy this file to config.py and fill in your values.
# NEVER commit config.py to a public repository.
# ============================================================

# Number of days a new client gets on the free trial.
TRIAL_DAYS = 14

# Pricing
SETUP_FEE   = 299.00   # one-time activation fee
MONTHLY_FEE = 49.99    # monthly renewal fee

# Hard-stop date (ISO format: "YYYY-MM-DD").
# Every client — including active subscriptions — is locked
# on or after this date until a renewal key is entered.
# Set to None to disable the hard stop.
HARD_STOP_DATE = None
# HARD_STOP_DATE = "2026-06-01"

# License key signing secret.
# Generate your own: python -c "import secrets; print(secrets.token_hex(32))"
# Keep this secret. Anyone who knows it can generate valid keys.
LICENSE_SECRET = "replace-with-your-own-secret"
