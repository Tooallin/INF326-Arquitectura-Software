from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
base_url = "/api"
# base_url = os.getenv("BASE_URL", "http://search_service:8000/api")

def test_read_channels():
    response = client.get(base_url+"/channel/search_channel")
    assert response.status_code == 200
    data = response.json()
    # Verificamos que la respuesta sea un array
    assert isinstance(data, list)

    # Verificamos que dentro del array haya un objeto con diversos campos
    assert any(
        item.get("id") == "channel_1" and
        item.get("owner_id") == "owner_123" and
        item.get("name") == "Canal de prueba" and
        item.get("channel_type") == "public" and
        item.get("is_active") is True and
        isinstance(item.get("users"), list) and
        any(
            user.get("id") == "user_1" and
            user.get("joined_at") == "2025-11-20T12:00:00"
            for user in item.get("users", [])
        )
        for item in data
    )

def test_read_inexistent_channel():
    response = client.get(base_url+"/channel/search_channel"+"?q=holamundo")
    assert response.status_code == 200
    data = response.json()
    # Verificamos que la respuesta sea un array
    assert isinstance(data, list)

    # Verificamos que no exista un channel con dichas características
    assert len(data) == 0