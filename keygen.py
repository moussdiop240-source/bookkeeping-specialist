"""
Admin tool — generate license keys for paying customers.
Run this on your machine; share only the generated key with the customer.

Usage:
    python keygen.py          # generate one SETUP + one RENEW key
    python keygen.py setup    # generate a SETUP key only
    python keygen.py renew    # generate a RENEW key only
    python keygen.py 5        # generate 5 SETUP keys
"""
import sys
from config import LICENSE_SECRET
from license_utils import generate_key

def main():
    args   = sys.argv[1:]
    plan   = "SETUP"
    count  = 1

    for a in args:
        if a.lower() in ("setup", "renew"):
            plan = a.upper()
        elif a.isdigit():
            count = int(a)

    print()
    print("  AI Bookkeeping Specialist - License Key Generator")
    print("  " + "=" * 50)
    print()

    if "renew" not in [a.lower() for a in args] and "setup" not in [a.lower() for a in args]:
        # Default: one of each
        print(f"  SETUP KEY : {generate_key(LICENSE_SECRET, 'SETUP')}")
        print(f"  RENEW KEY : {generate_key(LICENSE_SECRET, 'RENEW')}")
    else:
        for i in range(count):
            print(f"  {plan} KEY : {generate_key(LICENSE_SECRET, plan)}")

    print()
    print("  Send the key to the customer after payment is confirmed.")
    print()

if __name__ == "__main__":
    main()
