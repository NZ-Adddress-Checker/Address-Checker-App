import logging
import threading
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient
from jwt.exceptions import PyJWKClientError

from config import settings

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)
_jwks_client: PyJWKClient | None = None
_jwks_lock = threading.Lock()


def _get_jwks_client() -> PyJWKClient:
    global _jwks_client
    if _jwks_client is None:
        with _jwks_lock:
            if _jwks_client is None:
                logger.info("Initialising JWKS client for %s", settings.jwks_url)
                _jwks_client = PyJWKClient(settings.jwks_url, cache_jwk_set=True, lifespan=300)
    return _jwks_client


def _decode_jwt(token: str) -> dict[str, Any]:
    if not settings.jwt_configured:
        logger.error("JWT validation is not configured (jwks_url/jwt_issuer/jwt_audience missing)")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT validation is not configured on server",
        )

    try:
        signing_key = _get_jwks_client().get_signing_key_from_jwt(token)
    except PyJWKClientError as exc:
        logger.warning("JWKS key fetch failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to validate token at this time",
        ) from exc

    return jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )


def get_user_groups(claims: dict[str, Any]) -> list[str]:
    """Extract Cognito group memberships from JWT claims."""
    groups = claims.get("cognito:groups", [])
    return groups if isinstance(groups, list) else []


def require_jwt(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict[str, Any]:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    try:
        claims = _decode_jwt(credentials.credentials)
        logger.debug("Token validated for sub=%s", claims.get("sub"))
        return claims
    except HTTPException:
        raise
    except jwt.ExpiredSignatureError as exc:
        logger.info("Expired token received")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired") from exc
    except jwt.InvalidTokenError as exc:
        logger.warning("Invalid token: %s", exc)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


def require_address_validator(claims: dict[str, Any] = Depends(require_jwt)) -> dict[str, Any]:
    """Require user to be a member of the configured allowed group."""
    groups = get_user_groups(claims)
    if settings.allowed_group not in groups:
        logger.warning(
            "Access denied for sub=%s — not in group '%s' (has: %s)",
            claims.get("sub"),
            settings.allowed_group,
            groups,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. You are not a member of the '{settings.allowed_group}' group.",
        )
    return claims
