from fastapi.testclient import TestClient

from main import app

client: TestClient = TestClient(app)


def test_get_invoice_returns_second_invoice():
    response = client.get("/invoices/3")

    assert response.status_code == 200
    assert response.json() == {"id": 3, "title": "AB"}
