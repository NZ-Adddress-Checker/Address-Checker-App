from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "NZ Address Checker API"
    app_env: str = "dev"
    frontend_origin: str = "http://localhost:5173"
    frontend_origins: str = ""

    jwt_issuer: str = ""
    jwt_audience: str = ""
    jwks_url: str = ""

    nzpost_api_url: str = ""
    nzpost_api_key: str = ""
    nzpost_timeout_seconds: int = Field(default=5, ge=1, le=30)
    nzpost_mock: bool = True

    # Group required for address validation access - configurable per environment
    allowed_group: str = "AddressValidators"

    @field_validator("nzpost_timeout_seconds", mode="before")
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        v = int(v)
        if v < 1:
            return 1
        if v > 30:
            return 30
        return v

    @property
    def allowed_frontend_origins(self) -> list[str]:
        configured = [item.strip() for item in self.frontend_origins.split(",") if item.strip()]
        return configured or [self.frontend_origin]

    @property
    def jwt_configured(self) -> bool:
        return bool(self.jwks_url and self.jwt_issuer and self.jwt_audience)


settings = Settings()
