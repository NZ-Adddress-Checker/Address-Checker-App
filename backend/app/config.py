import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', 'False') == 'True'
PORT = int(os.getenv('PORT', '8000'))
HOST = os.getenv('HOST', '127.0.0.1')
NZ_POST_API_KEY = os.getenv('NZ_POST_API_KEY', 'mock')

MOCK_USERNAME = 'user123'
MOCK_PASSWORD = 'password123'
