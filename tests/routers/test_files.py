from unittest.mock import patch
from tests.base_tests import BaseApiTestCase # Importamos la base

class TestFilesEndpoint(BaseApiTestCase): # Heredamos de la base
	
	@patch('app.services.files_service.search_file')
	def test_search_file(self, mock_search):
		# Ya tienes self.client disponible gracias a BaseApiTestCase
		mock_search.return_value = []
		response = self.client.get("/search_file")
		self.assertEqual(response.status_code, 200)