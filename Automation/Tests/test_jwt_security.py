import requests
from utils.jwt_helper import tamper_token
from config import API_URL


def test_tampered_jwt_rejected():
    """A JWT with a tampered payload must be rejected."""
    fake_token = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ1c2VyIn0.signature"
    tampered = tamper_token(fake_token)

    res = requests.get(
        f"{API_URL}/address/suggest",
        params={"q": "Auckland"},
        headers={"Authorization": f"Bearer {tampered}"},
    )

    assert res.status_code in [401, 403]


def test_no_bearer_prefix_rejected():
    """Authorization header without Bearer prefix must be rejected."""
    res = requests.get(
        f"{API_URL}/address/suggest",
        params={"q": "Auckland"},
        headers={"Authorization": "Token somevalue"},
    )
    assert res.status_code == 401


def test_empty_token_rejected():
    """Empty bearer token must be rejected."""
    res = requests.get(
        f"{API_URL}/address/suggest",
        params={"q": "Auckland"},
        headers={"Authorization": "Bearer "},
    )
    assert res.status_code == 401