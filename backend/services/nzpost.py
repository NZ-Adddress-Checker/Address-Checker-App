import httpx

from config import settings

# Valid addresses - only these from the dropdown will be accepted
VALID_ADDRESSES = {
    "10 queen street, auckland 1010",
    "120 queen street, auckland 1010",
    "1 viaduct harbour avenue, auckland 1010",
    "34 customs street west, auckland 1010",
    "167 victoria street west, auckland 1010",
    "2 quay street, auckland 1010",
    "1 queen street, auckland 1010",
    "100 lambton quay, wellington 6011",
    "25 cuba street, wellington 6011",
    "15 courtenay place, wellington 6011",
    "150 willis street, wellington 6011",
    "1 cathedral square, christchurch 8011",
    "120 hereford street, christchurch 8011",
    "200 colombo street, christchurch 8011",
    "8 the octagon, dunedin 9016",
    "70 george street, dunedin 9016",
    "45 cameron road, tauranga 3110",
    "67 victoria street, hamilton 3204",
    "3 marine parade, napier 4110",
    "20 trafalgar street, nelson 7010",
}


def _normalize_address_key(address: str) -> str:
    return " ".join(address.split()).casefold()


def _normalize_address_display(address: str) -> str:
    return " ".join(address.split()).title()


class NZPostServiceError(Exception):
    pass


class NZPostServiceTimeout(Exception):
    pass


async def validate_address(address: str) -> dict:
    if settings.nzpost_mock:
        normalized_key = _normalize_address_key(address)
        is_valid = normalized_key in VALID_ADDRESSES

        return {
            "is_valid": is_valid,
            "normalized_address": _normalize_address_display(address),
            "source": "mock",
        }

    if not settings.nzpost_api_url or not settings.nzpost_api_key:
        raise NZPostServiceError("NZ Post API is not configured")

    headers = {
        "Authorization": f"Bearer {settings.nzpost_api_key}",
        "Content-Type": "application/json",
    }
    payload = {"address": address}

    try:
        async with httpx.AsyncClient(timeout=settings.nzpost_timeout_seconds) as client:
            response = await client.post(settings.nzpost_api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException as exc:
        raise NZPostServiceTimeout("NZ Post request timed out") from exc
    except httpx.HTTPError as exc:
        raise NZPostServiceError("NZ Post API request failed") from exc

    return {
        "is_valid": bool(data.get("is_valid", False)),
        "normalized_address": data.get("normalized_address"),
        "source": "nzpost",
    }
