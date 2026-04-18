import httpx

from config import settings


class NZPostServiceError(Exception):
    pass


class NZPostServiceTimeout(Exception):
    pass


async def validate_address(address: str) -> dict:
    if settings.nzpost_mock:
        normalized = " ".join(address.split())
        return {
            "is_valid": len(normalized) >= 6,
            "normalized_address": normalized.title(),
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
