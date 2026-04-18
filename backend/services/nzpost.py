import httpx

from config import settings

# Reusable canonical suggestions for mock mode.
MOCK_ADDRESS_SUGGESTIONS: tuple[str, ...] = (
    "10 Queen Street, Auckland 1010",
    "120 Queen Street, Auckland 1010",
    "1 Viaduct Harbour Avenue, Auckland 1010",
    "34 Customs Street West, Auckland 1010",
    "167 Victoria Street West, Auckland 1010",
    "2 Quay Street, Auckland 1010",
    "1 Queen Street, Auckland 1010",
    "100 Lambton Quay, Wellington 6011",
    "25 Cuba Street, Wellington 6011",
    "15 Courtenay Place, Wellington 6011",
    "150 Willis Street, Wellington 6011",
    "1 Cathedral Square, Christchurch 8011",
    "120 Hereford Street, Christchurch 8011",
    "200 Colombo Street, Christchurch 8011",
    "8 The Octagon, Dunedin 9016",
    "70 George Street, Dunedin 9016",
    "45 Cameron Road, Tauranga 3110",
    "67 Victoria Street, Hamilton 3204",
    "3 Marine Parade, Napier 4110",
    "20 Trafalgar Street, Nelson 7010",
)


def _normalize_address_key(address: str) -> str:
    return " ".join(address.split()).casefold()


def _normalize_address_display(address: str) -> str:
    return " ".join(address.split()).title()


MOCK_ADDRESS_KEYS = frozenset(_normalize_address_key(address) for address in MOCK_ADDRESS_SUGGESTIONS)


def get_address_suggestions() -> list[str]:
    if settings.nzpost_mock:
        return list(MOCK_ADDRESS_SUGGESTIONS)
    return []


class NZPostServiceError(Exception):
    pass


class NZPostServiceTimeout(Exception):
    pass


async def validate_address(address: str) -> dict:
    if settings.nzpost_mock:
        normalized_key = _normalize_address_key(address)
        is_valid = normalized_key in MOCK_ADDRESS_KEYS

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
