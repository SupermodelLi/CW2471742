import pytest
from main import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, dict)
    assert data.get("status") == "ok"


def test_stories_endpoint(client):
    resp = client.get("/api/stories")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)


def test_generate_requires_location(client):
    resp = client.post("/api/generate", json={})
    assert resp.status_code == 400