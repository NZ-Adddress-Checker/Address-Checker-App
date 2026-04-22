import jwt

def tamper_token(token):
    parts = token.split(".")

    # fake payload change (no signature fix)
    return parts[0] + ".tampered_payload." + parts[2]