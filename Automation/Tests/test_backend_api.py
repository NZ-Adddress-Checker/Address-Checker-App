import requests
from config import API_URL


def test_suggest_requires_auth():
    """Calling /api/address/suggest without a token must return 401."""
    res = requests.get(f"{API_URL}/address/suggest", params={"q": "Auckland"})
    assert res.status_code == 401


def test_validate_requires_auth():
    """Calling /api/address/validate without a token must return 401."""
    res = requests.post(f"{API_URL}/address/validate", json={"address": "Auckland"})
    assert res.status_code == 401


def test_invalid_token_rejected():
    """A completely forged token must be rejected with 401."""
    res = requests.get(
        f"{API_URL}/address/suggest",
        params={"q": "Auckland"},
        headers={"Authorization": "Bearer forged.token.value"},
    )
    assert res.status_code == 401