from typing import Optional
from fastapi import Header, HTTPException
from jose import JWTError
from app.core.security import verify_token


def get_current_user(authorization: Optional[str] = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    try:
        return verify_token(parts[1])
    except (JWTError, RuntimeError):
        raise HTTPException(status_code=401, detail="Invalid token")
