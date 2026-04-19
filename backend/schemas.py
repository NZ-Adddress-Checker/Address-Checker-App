from pydantic import BaseModel, Field


class AddressCheckRequest(BaseModel):
    address: str = Field(min_length=1, max_length=300)


class AddressCheckResponse(BaseModel):
    is_valid: bool
    normalized_address: str | None = None
    source: str


class AddressSuggestionsResponse(BaseModel):
    items: list[str]


class UserAuthorizationResponse(BaseModel):
    has_access: bool
    groups: list[str]
    username: str | None = None
