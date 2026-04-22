import pytest
import requests
from jsonschema import validate
from schemas.addressable_schema import ADDRESSABLE_SCHEMA


URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "NZ-Address-Checker/1.0"}
BASE_PARAMS = {"countrycodes": "nz", "format": "json", "addressdetails": 0}


@pytest.mark.external
@pytest.mark.contract
def test_nominatim_returns_list():
    """Nominatim returns a non-empty list for a known NZ query."""
    res = requests.get(URL, params={**BASE_PARAMS, "q": "1 Main Street", "limit": 3}, headers=HEADERS)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.external
@pytest.mark.contract
def test_nominatim_items_have_display_name():
    """Each result from Nominatim includes a display_name string."""
    res = requests.get(URL, params={**BASE_PARAMS, "q": "Auckland", "limit": 3}, headers=HEADERS)
    assert res.status_code == 200
    for item in res.json():
        assert "display_name" in item
        assert isinstance(item["display_name"], str)
        assert len(item["display_name"]) > 0


@pytest.mark.external
@pytest.mark.contract
def test_nominatim_schema():
    """Nominatim response matches the expected JSON schema (formatted field mapped)."""
    res = requests.get(URL, params={**BASE_PARAMS, "q": "Wellington", "limit": 3}, headers=HEADERS)
    assert res.status_code == 200
    mapped = [{"formatted": item["display_name"]} for item in res.json()]
    validate(instance=mapped, schema=ADDRESSABLE_SCHEMA)