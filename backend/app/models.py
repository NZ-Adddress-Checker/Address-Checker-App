from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str


class AddressValidationRequest(BaseModel):
    address: str


class AddressValidationResponse(BaseModel):
    status: str
    address: str
    message: str = None
