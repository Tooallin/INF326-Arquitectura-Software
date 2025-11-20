from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
base_url = "/api"
# base_url = os.getenv("BASE_URL", "http://search_service:8000/api")

def test_read_files():
    response = client.get(base_url+"/files/search_files")
    assert response.status_code == 200
    data = response.json()
    # Verificamos que la respuesta sea un array
    assert isinstance(data, list)

    # Verificamos que dentro del array haya un objeto con diversos campos
    assert any(
		item.get("id") == "file_1" and
		item.get("filename") == "documento.pdf" and
		item.get("mime_type") == "application/pdf" and
		item.get("size") == 1024 and
		item.get("bucket") == "uploads" and
		item.get("object_key") == "documents/documento.pdf" and
		item.get("message_id") == "msg_123" and
		item.get("thread_id") == "thread_456" and
		item.get("checksum_sha256") == "abc123def456..." and
		item.get("created_at") == "2025-11-20T12:00:00" and
		item.get("deleted_at") is None
		for item in data
	)

def test_read_inexistent_file():
    response = client.get(base_url+"/files/search_files"+"?q=holamundo")
    assert response.status_code == 200
    data = response.json()
    # Verificamos que la respuesta sea un array
    assert isinstance(data, list)

    # Verificamos que no exista un channel con dichas características
    assert len(data) == 0