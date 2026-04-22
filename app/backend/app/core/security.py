from jose import jwt, JWTError
import requests
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

JWKS_URL = f"https://cognito-idp.{settings.COGNITO_REGION}.amazonaws.com/{settings.USER_POOL_ID}/.well-known/jwks.json"
_jwks_cache = None


def _get_jwks(force_refresh: bool = False):
    global _jwks_cache
    if _jwks_cache is None or force_refresh:
        try:
            resp = requests.get(JWKS_URL, timeout=5)
            resp.raise_for_status()
            _jwks_cache = resp.json()
        except Exception as e:
            logger.error("Failed to fetch JWKS from Cognito: %s", e)
            raise RuntimeError("Unable to fetch JWKS") from e
    return _jwks_cache


def verify_token(token: str):
    jwks = _get_jwks()
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")
    matching = [k for k in jwks["keys"] if k["kid"] == kid]
    if not matching:
        # Key not in cache — refresh once to handle Cognito key rotation
        jwks = _get_jwks(force_refresh=True)
        matching = [k for k in jwks["keys"] if k["kid"] == kid]
        if not matching:
            raise JWTError("No matching key found in JWKS")
    return jwt.decode(
        token,
        matching[0],
        algorithms=["RS256"],
        audience=settings.CLIENT_ID,
        options={"verify_at_hash": False},
    )
