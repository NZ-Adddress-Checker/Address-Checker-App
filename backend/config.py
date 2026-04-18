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
    nzpost_timeout_seconds: int = 3
    nzpost_mock: bool = True

    @property
    def allowed_frontend_origins(self) -> list[str]:
        configured = [item.strip() for item in self.frontend_origins.split(",") if item.strip()]
        return configured or [self.frontend_origin]


settings = Settings()
