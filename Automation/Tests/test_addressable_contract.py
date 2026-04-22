import pytest
import requests
from jsonschema import validate
from schemas.addressable_schema import ADDRESSABLE_SCHEMA
from config import NZPOST_API_KEY


URL = "https://api.addressable.dev/v2/autocomplete"


# Note: These tests consume daily API quota (100 requests/day free tier)
# Skip by default. Run with: pytest -m external or pytest -m contract
@pytest.mark.skip(reason="Skipped by default to preserve API quota. Run with: pytest -m external")
@pytest.mark.external
@pytest.mark.contract
def test_addressable_returns_list():
    """Addressable API returns a non-empty list for a known NZ query."""
    res = requests.get(URL, params={"q": "1 Main Street", "country_code": "NZ", "api_key": NZPOST_API_KEY, "max_results": 3})
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.skip(reason="Skipped by default to preserve API quota. Run with: pytest -m external")
@pytest.mark.external
@pytest.mark.contract
def test_addressable_items_have_formatted_field():
    """Each result from Addressable API includes a formatted address string."""
    res = requests.get(URL, params={"q": "Auckland", "country_code": "NZ", "api_key": NZPOST_API_KEY, "max_results": 3})
    assert res.status_code == 200
    for item in res.json():
        assert "formatted" in item
        assert isinstance(item["formatted"], str)
        assert len(item["formatted"]) > 0


@pytest.mark.skip(reason="Skipped by default to preserve API quota. Run with: pytest -m external")
@pytest.mark.external
@pytest.mark.contract
def test_addressable_schema():
    """Addressable API response matches the expected JSON schema."""
    res = requests.get(URL, params={"q": "Wellington", "country_code": "NZ", "api_key": NZPOST_API_KEY, "max_results": 3})
    assert res.status_code == 200
    validate(instance=res.json(), schema=ADDRESSABLE_SCHEMA)