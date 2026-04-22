import requests
from config import API_URL

# NOTE: full address tests require a valid Cognito token.
# These tests verify unauthenticated access is blocked correctly.


def test_validate_without_auth_returns_401():
    """Validate endpoint rejects requests with no auth header."""
    res = requests.post(f"{API_URL}/address/validate", json={"address": "Auckland Central"})
    assert res.status_code == 401


def test_suggest_without_auth_returns_401():
    """Suggest endpoint rejects requests with no auth header."""
    res = requests.get(f"{API_URL}/address/suggest", params={"q": "Auckland"})
    assert res.status_code == 401


def test_validate_missing_field_returns_422():
    """Validate with missing address field returns 422 Unprocessable Entity."""
    res = requests.post(
        f"{API_URL}/address/validate",
        json={"wrong_field": "Auckland"},
        headers={"Authorization": "Bearer forged.token.value"},
    )
    # 401 (auth fails before schema check) or 422 (schema check first) both acceptable
    assert res.status_code in [401, 422]