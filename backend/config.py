from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "NZ Address Checker API"
    app_env: str = "dev"

    # Comma-separated list of allowed frontend origins.
    # Example: http://localhost:5173 or https://app.example.com,https://www.example.com
    frontend_origins: str = "http://localhost:5173"

    jwt_issuer: str = ""
    jwt_audience: str = ""
    jwks_url: str = ""

    nzpost_api_url: str = ""
    nzpost_api_key: str = ""
    nzpost_timeout_seconds: int = 3
    nzpost_mock: bool = True

    @property
    def allowed_frontend_origins(self) -> list[str]:
        return [item.strip() for item in self.frontend_origins.split(",") if item.strip()]


settings = Settings()
