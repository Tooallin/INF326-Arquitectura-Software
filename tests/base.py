from fastapi.testclient import TestClient

from main import app

base_url = "/api"
base_remote_url = "https://searchservice.inf326.nursoft.dev/api"
client = TestClient(app)