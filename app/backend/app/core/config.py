import os

class Settings:
    COGNITO_REGION = os.getenv("COGNITO_REGION")
    USER_POOL_ID = os.getenv("USER_POOL_ID")
    CLIENT_ID = os.getenv("CLIENT_ID")
    NZPOST_API_KEY = os.getenv("NZPOST_API_KEY")
    CORS_ORIGIN = os.getenv("CORS_ORIGIN", "http://localhost:8085")

settings = Settings()
