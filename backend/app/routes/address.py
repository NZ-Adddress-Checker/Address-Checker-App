from fastapi import APIRouter, HTTPException, status

from ..models import AddressValidationRequest, AddressValidationResponse
from ..services.nz_post_mock import validate_address

router = APIRouter(tags=['address'])


@router.post('/validate-address', response_model=AddressValidationResponse)
async def validate_address_endpoint(request: AddressValidationRequest):
    """
    Validate a New Zealand address.
    """
    try:
        result = validate_address(request.address)
        return AddressValidationResponse(
            status=result['status'],
            address=request.address,
            message=result.get('message'),
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
