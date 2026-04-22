import requests


def autocomplete_address(query: str) -> list:
    url = "https://nominatim.openstreetmap.org/search"
    response = requests.get(
        url,
        params={
            "q": query,
            "countrycodes": "nz",
            "format": "json",
            "addressdetails": 0,
            "limit": 10,
        },
        headers={"User-Agent": "NZ-Address-Checker/1.0"},
        timeout=5,
    )
    response.raise_for_status()
    return [{"formatted": item["display_name"]} for item in response.json()]
