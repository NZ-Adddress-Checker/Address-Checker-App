import logging
import logging.config

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from auth import get_user_groups, require_address_validator, require_jwt
from config import settings
from schemas import (
    AddressCheckRequest,
    AddressCheckResponse,
    AddressSuggestionsResponse,
    UserAuthorizationResponse,
)
from services.nzpost import (
    NZPostServiceError,
    NZPostServiceTimeout,
    get_address_suggestions,
    validate_address,
)

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "default"}
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "auth": {"level": "DEBUG"},
        "services": {"level": "DEBUG"},
    },
})

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("App '%s' started in env=%s (mock=%s)", settings.app_name, settings.app_env, settings.nzpost_mock)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "env": settings.app_env, "mock": settings.nzpost_mock}


@app.get("/auth/check-access", response_model=UserAuthorizationResponse)
def check_access(claims: dict = Depends(require_jwt)) -> UserAuthorizationResponse:
    """Return group membership and access status for the authenticated user."""
    groups = get_user_groups(claims)
    has_access = settings.allowed_group in groups
    username = claims.get("cognito:username") or claims.get("email") or claims.get("sub")
    logger.info("check-access: user=%s has_access=%s groups=%s", username, has_access, groups)
    return UserAuthorizationResponse(has_access=has_access, groups=groups, username=username)


@app.get("/address-suggestions", response_model=AddressSuggestionsResponse)
def address_suggestions(_claims: dict = Depends(require_address_validator)) -> AddressSuggestionsResponse:
    return AddressSuggestionsResponse(items=get_address_suggestions())


@app.post("/address-check", response_model=AddressCheckResponse)
async def address_check(
    payload: AddressCheckRequest,
    _claims: dict = Depends(require_address_validator),
) -> AddressCheckResponse:
    address = payload.address.strip()
    if not address:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Address cannot be empty")

    try:
        result = await validate_address(address)
    except NZPostServiceTimeout as exc:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(exc)) from exc
    except NZPostServiceError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return AddressCheckResponse(**result)
