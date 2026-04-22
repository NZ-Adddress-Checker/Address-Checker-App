import requests
from app.core.config import settings


def autocomplete_address(query: str) -> list:
    url = "https://api.addressable.dev/v2/autocomplete"
    response = requests.get(
        url,
        params={
            "q": query,
            "country_code": "NZ",
            "api_key": settings.NZPOST_API_KEY,
            "max_results": 10,
        },
        timeout=5,
    )
    response.raise_for_status()
    return response.json()
