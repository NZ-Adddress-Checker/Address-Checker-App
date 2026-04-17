from fastapi import APIRouter, HTTPException, status

from ..config import MOCK_PASSWORD, MOCK_USERNAME
from ..models import LoginRequest, LoginResponse

router = APIRouter(tags=['auth'])


@router.post('/login', response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(request: LoginRequest):
    """
    Authenticate user with username and password.
    """
    if request.username == MOCK_USERNAME and request.password == MOCK_PASSWORD:
        return LoginResponse(message='Login successful')

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials',
    )
