from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_wallet_info_endpoint():
    response = client.post("/wallet/info", json={"address": "TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy"})
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == "TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy"
    assert "balance_trx" in data
    assert "bandwidth" in data
    assert "energy" in data

def test_logs_endpoint():
    response = client.get("/wallet/logs?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
