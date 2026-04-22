from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import address
from app.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(address.router, prefix="/api/address")
