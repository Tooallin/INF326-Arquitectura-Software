from unittest.mock import patch
from ..base_tests import BaseApiTestCase

MOCK_FILE = {
	"id": "file_1",
	"filename": "contrato.pdf",
	"mime_type": "application/pdf",
	"size": 10240,
	"bucket": "aws-s3-main",
	"object_key": "2023/documentos/contrato.pdf",
	"message_id": "55",
	"thread_id": "12",
	"checksum_sha256": "a1b2c3d4...",
	"created_at": "2023-10-27T10:00:00",
	"deleted_at": None
}

class TestFilesEndpoints(BaseApiTestCase):
	@patch("files.services.svc_searchfiles") 
	def test_search_files_success(self, mock_search):
		
		mock_search.return_value = [MOCK_FILE]

		response = self.client.get("/api/files/search_files", params={"q": "contrato"})

		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertIsInstance(data, list)
		self.assertEqual(data[0]["filename"], "contrato.pdf")

	@patch("files.services.svc_searchfiles")
	def test_search_files_empty(self, mock_search):
		mock_search.return_value = []
		
		response = self.client.get("/api/files/search_files", params={"q": "inexistente"})
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 0)