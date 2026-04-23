import os

BASE_URL = "http://localhost:5002"
API_URL = "http://localhost:5001/api"

USERS = {
    "valid": {
        "username": "testapp",
        "password": "Test@1996!"
    },
    "invalid": {
        "username": "jeffcj",
        "password": "Test@1996!"
    }
}

# In CI environments (GitHub Actions sets CI=true), run headless automatically
HEADLESS = os.environ.get("CI", "false").lower() == "true" or os.environ.get("HEADLESS", "false").lower() == "true"
SLOW_MO = 0 if HEADLESS else 300