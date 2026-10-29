import hashlib
import hmac
from django.contrib.auth.hashers import make_password, check_password as django_check_password

def verify_password(stored_hash, password):
    """
    Verifies passwords against stored hashes.
    Supports:
    1. Werkzeug scrypt format: scrypt:32768:8:1$<salt>$<hash_hex>
    2. Django default hash formats: pbkdf2_sha256$..., scrypt$..., etc.
    3. Werkzeug check_password_hash fallback
    """
    if not stored_hash or not password:
        return False

    # Check Werkzeug scrypt format via standard library hashlib.scrypt
    if stored_hash.startswith('scrypt:'):
        try:
            parts = stored_hash.split('$')
            if len(parts) == 3:
                params = parts[0].split(':')
                n, r, p = int(params[1]), int(params[2]), int(params[3])
                salt = parts[1].encode('utf-8')
                expected_hex = parts[2]
                computed_hex = hashlib.scrypt(
                    password.encode('utf-8'),
                    salt=salt,
                    n=n,
                    r=r,
                    p=p,
                    maxmem=128 * 1024 * 1024
                ).hex()
                if hmac.compare_digest(computed_hex, expected_hex):
                    return True
        except Exception:
            pass

    # Check Django format
    try:
        if django_check_password(password, stored_hash):
            return True
    except Exception:
        pass

    # Werkzeug check_password_hash fallback if installed
    try:
        from werkzeug.security import check_password_hash
        if check_password_hash(stored_hash, password):
            return True
    except Exception:
        pass

    return False

def hash_password(password):
    """
    Hashes password using Django's secure password hasher.
    """
    return make_password(password)
