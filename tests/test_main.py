from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_root() -> None:
    response = client.get("/api/v1")

    assert response.status_code == 200
    assert response.json() == {
        "name": "CodeSmith Agent",
        "status": "running",
    }

def test_health()->None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status":"Ok",
        "service":"CodeSmith Agent",
           }   