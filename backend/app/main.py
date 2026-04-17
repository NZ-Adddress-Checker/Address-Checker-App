import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .config import DEBUG, HOST, PORT
from .routes import address, auth

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title='NZ Address Checker API',
    description='API for validating New Zealand addresses',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router)
app.include_router(address.router)


@app.get('/health', tags=['health'])
async def health_check():
    """Health check endpoint."""
    return {'status': 'healthy', 'message': 'Service is running'}


@app.get('/', tags=['root'])
async def root():
    """Root endpoint."""
    return {
        'message': 'NZ Address Checker API',
        'docs': '/docs',
        'version': '1.0.0',
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {'detail': exc.detail}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level='info',
    )
