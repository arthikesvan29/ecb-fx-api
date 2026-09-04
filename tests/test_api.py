from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_exchange_rate():
    response = client.get(
        "/rate",
        params={
            "date": "2025-01-02",
            "from_currency": "USD",
            "to_currency": "INR"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["date"] == "2025-01-02"
    assert data["from_currency"] == "USD"
    assert data["to_currency"] == "INR"
    assert data["rate"] > 0


def test_get_exchange_rate_with_eur():
    response = client.get(
        "/rate",
        params={
            "date": "2025-01-02",
            "from_currency": "EUR",
            "to_currency": "USD"
        }
    )

    assert response.status_code == 200
    assert response.json()["rate"] > 0


def test_same_currency_rate():
    response = client.get(
        "/rate",
        params={
            "date": "2025-01-02",
            "from_currency": "USD",
            "to_currency": "USD"
        }
    )

    assert response.status_code == 200
    assert response.json()["rate"] == 1.0


def test_invalid_currency():
    response = client.get(
        "/rate",
        params={
            "date": "2025-01-02",
            "from_currency": "XXX",
            "to_currency": "INR"
        }
    )

    assert response.status_code == 400


def test_invalid_date():
    response = client.get(
        "/rate",
        params={
            "date": "2030-01-01",
            "from_currency": "USD",
            "to_currency": "INR"
        }
    )

    assert response.status_code == 404


def test_get_exchange_rates():
    response = client.get(
        "/rates",
        params={
            "from_date": "2025-01-02",
            "to_date": "2025-01-03",
            "from_currency": "USD",
            "to_currency": "INR"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0
    assert data[0]["from_currency"] == "USD"
    assert data[0]["to_currency"] == "INR"
    assert data[0]["rate"] > 0


def test_invalid_date_range():
    response = client.get(
        "/rates",
        params={
            "from_date": "2025-01-03",
            "to_date": "2025-01-02",
            "from_currency": "USD",
            "to_currency": "INR"
        }
    )

    assert response.status_code == 400