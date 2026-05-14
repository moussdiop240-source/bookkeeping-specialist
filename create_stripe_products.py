"""
Create Stripe products and payment links for AI Bookkeeping Specialist.
Run once: python create_stripe_products.py sk_live_YOUR_KEY_HERE
"""
import sys
import stripe

if len(sys.argv) < 2 or not sys.argv[1].startswith("sk_"):
    print("\nUsage: python create_stripe_products.py sk_live_YOUR_KEY_HERE\n")
    sys.exit(1)

stripe.api_key = sys.argv[1]

print("\nCreating Stripe products and payment links...\n")

# ── 1. One-time setup product ($299) ──────────────────────────────────────────
setup_product = stripe.Product.create(
    name="AI Bookkeeping Specialist — Setup",
    description="One-time activation. Includes license key, full app, and PDF user guide.",
)
setup_price = stripe.Price.create(
    product=setup_product.id,
    unit_amount=29900,
    currency="usd",
)
setup_link = stripe.PaymentLink.create(
    line_items=[{"price": setup_price.id, "quantity": 1}],
    after_completion={
        "type": "hosted_confirmation",
        "hosted_confirmation": {
            "custom_message": (
                "Thank you! You will receive your license key and download link "
                "at the email address you provided within 24 hours."
            ),
        },
    },
    metadata={"product": "setup"},
)

# ── 2. Monthly renewal subscription ($49.99/mo) ───────────────────────────────
renew_product = stripe.Product.create(
    name="AI Bookkeeping Specialist — Monthly Renewal",
    description="Monthly renewal key. Keeps your license active.",
)
renew_price = stripe.Price.create(
    product=renew_product.id,
    unit_amount=4999,
    currency="usd",
    recurring={"interval": "month"},
)
renew_link = stripe.PaymentLink.create(
    line_items=[{"price": renew_price.id, "quantity": 1}],
    after_completion={
        "type": "hosted_confirmation",
        "hosted_confirmation": {
            "custom_message": (
                "Thank you! Your renewal key will be emailed within 24 hours."
            ),
        },
    },
    metadata={"product": "renewal"},
)

print("=" * 60)
print(f"  SETUP LINK  : {setup_link.url}")
print(f"  RENEWAL LINK: {renew_link.url}")
print("=" * 60)
print()
print("Paste SETUP LINK on your landing page (index.html) Buy Now button.")
print("Paste RENEWAL LINK in renewal emails to existing customers.")
print()
