import requests as http_requests
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.services.nzpost import autocomplete_address

router = APIRouter()


class ValidateRequest(BaseModel):
    address: str


def _check_access(user):
    groups = user.get("cognito:groups", [])
    if "AddressValidators" not in groups:
        raise HTTPException(status_code=403, detail="Access denied")


@router.get("/suggest")
def suggest(q: str, user=Depends(get_current_user)):
    _check_access(user)
    try:
        return autocomplete_address(q)
    except http_requests.RequestException:
        raise HTTPException(status_code=502, detail="Address lookup service unavailable")


@router.post("/validate")
def validate(data: ValidateRequest, user=Depends(get_current_user)):
    _check_access(user)
    try:
        results = autocomplete_address(data.address)
    except http_requests.RequestException:
        raise HTTPException(status_code=502, detail="Address lookup service unavailable")
    query = data.address.strip().lower()
    matched = next((r for r in results if r.get("formatted", "").strip().lower() == query), None)
    return {"valid": matched is not None, "address": matched}
