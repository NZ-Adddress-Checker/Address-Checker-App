from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def _mock_auth() -> dict:
    return {"sub": "test-user"}


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_address_check_success() -> None:
    main.app.dependency_overrides[main.require_jwt] = _mock_auth
    response = client.post("/address-check", json={"address": "10 Queen Street, Auckland"})

    assert response.status_code == 200
    data = response.json()
    assert "is_valid" in data
    assert data["source"] in {"mock", "nzpost"}

    main.app.dependency_overrides = {}


def test_address_check_empty_input() -> None:
    main.app.dependency_overrides[main.require_jwt] = _mock_auth
    response = client.post("/address-check", json={"address": "   "})
    assert response.status_code == 400
    main.app.dependency_overrides = {}


def test_address_check_unauthorized() -> None:
    response = client.post("/address-check", json={"address": "10 Queen Street, Auckland"})
    assert response.status_code == 401
