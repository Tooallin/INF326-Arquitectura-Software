from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
base_url = "/api"
# base_url = os.getenv("BASE_URL", "http://search_service:8000/api")

def test_read_files():
    response = client.get(base_url+"/message/search_message")
    assert response.status_code == 200
    data = response.json()
    # Verificamos que la respuesta sea un array
    assert isinstance(data, list)

    # Verificamos que dentro del array haya un objeto con diversos campos
    assert any(
		item.get("id") == "123e4567-e89b-12d3-a456-426614174000" and
		item.get("content") == "Hola mundo" and
		item.get("user_id") == "987e6543-e21b-12d3-a456-426614174999" and
		item.get("thread_id") == "555e4444-e21b-12d3-a456-426614171111" and
		item.get("type") == "text" and
		isinstance(item.get("paths"), list) and
		item.get("paths") == ["path1", "path2"] and
		item.get("created_at") == "2025-11-20T12:00:00" and
		item.get("updated_at") == "2025-11-20T12:05:00" and
		item.get("deleted_at") is None
		for item in data
	)

def test_read_inexistent_file():
    response = client.get(base_url+"/message/search_message"+"?q=holamundo")
    assert response.status_code == 200
    data = response.json()
    # Verificamos que la respuesta sea un array
    assert isinstance(data, list)

    # Verificamos que no exista un channel con dichas características
    assert len(data) == 0