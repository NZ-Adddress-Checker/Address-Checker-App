import logging

import httpx

from config import settings

logger = logging.getLogger(__name__)

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


MOCK_ADDRESS_KEYS = frozenset(_normalize_address_key(a) for a in MOCK_ADDRESS_SUGGESTIONS)


class NZPostServiceError(Exception):
    pass


class NZPostServiceTimeout(Exception):
    pass


def get_address_suggestions() -> list[str]:
    if settings.nzpost_mock:
        return list(MOCK_ADDRESS_SUGGESTIONS)
    return []


async def _call_nzpost_suggest(address: str) -> dict:
    """Call the real NZ Post suggest API with retry on transient errors."""
    if not settings.nzpost_api_url or not settings.nzpost_api_key:
        raise NZPostServiceError("NZ Post API is not configured")

    headers = {
        "Authorization": f"Bearer {settings.nzpost_api_key}",
        "Accept": "application/json",
    }
    url = f"{settings.nzpost_api_url}/addresschecker/1.0/suggest"
    params = {"q": address, "max": 10}

    last_exc: Exception | None = None
    for attempt in range(1, 3):  # 2 attempts
        try:
            async with httpx.AsyncClient(timeout=settings.nzpost_timeout_seconds) as client:
                logger.debug("NZ Post suggest attempt %d for address=%r", attempt, address)
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                logger.debug("NZ Post suggest returned %d addresses", len(data.get("addresses", [])))
                return data
        except httpx.TimeoutException as exc:
            logger.warning("NZ Post suggest timed out (attempt %d)", attempt)
            last_exc = exc
        except httpx.HTTPStatusError as exc:
            logger.error("NZ Post suggest HTTP %s: %s", exc.response.status_code, exc)
            raise NZPostServiceError(f"NZ Post API error: {exc.response.status_code}") from exc
        except httpx.HTTPError as exc:
            logger.error("NZ Post suggest request failed: %s", exc)
            last_exc = exc

    raise NZPostServiceTimeout("NZ Post request timed out after retries") from last_exc


async def validate_address(address: str) -> dict:
    if settings.nzpost_mock:
        normalized_key = _normalize_address_key(address)
        is_valid = normalized_key in MOCK_ADDRESS_KEYS
        logger.debug("Mock validation for %r: %s", address, is_valid)
        return {
            "is_valid": is_valid,
            "normalized_address": _normalize_address_display(address),
            "source": "mock",
        }

    data = await _call_nzpost_suggest(address)

    addresses = data.get("addresses") or []
    if not addresses:
        return {"is_valid": False, "normalized_address": None, "source": "nzpost"}

    # Exact match check against returned suggestions
    address_key = _normalize_address_key(address)
    matched = next(
        (a for a in addresses if _normalize_address_key(a.get("FullAddress", "")) == address_key),
        None,
    )

    return {
        "is_valid": matched is not None,
        "normalized_address": matched.get("FullAddress") if matched else addresses[0].get("FullAddress"),
        "source": "nzpost",
    }
