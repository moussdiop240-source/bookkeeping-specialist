"""License key generation and verification using HMAC-SHA256."""
import hmac
import hashlib
import secrets

def _sign(secret: str, payload: str) -> str:
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()[:12].upper()

def generate_key(secret: str, plan: str) -> str:
    """Generate a cryptographically signed license key for the given plan."""
    nonce = secrets.token_hex(4).upper()
    sig   = _sign(secret, f"{plan.upper()}:{nonce}")
    return f"{plan.upper()}-{nonce}-{sig}"

def verify_key(secret: str, key: str, plan: str) -> bool:
    """Return True if the key is a valid signed key for the given plan."""
    try:
        parts = key.strip().upper().split("-")
        if len(parts) != 3:
            return False
        prefix, nonce, sig = parts
        if prefix != plan.upper():
            return False
        expected = _sign(secret, f"{plan.upper()}:{nonce}")
        return hmac.compare_digest(sig, expected)
    except Exception:
        return False
