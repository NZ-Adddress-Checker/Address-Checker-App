from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from auth import require_jwt
from config import settings
from schemas import AddressCheckRequest, AddressCheckResponse
from services.nzpost import NZPostServiceError, NZPostServiceTimeout, validate_address

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "env": settings.app_env}


@app.post("/address-check", response_model=AddressCheckResponse)
async def address_check(
    payload: AddressCheckRequest,
    _claims: dict = Depends(require_jwt),
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
