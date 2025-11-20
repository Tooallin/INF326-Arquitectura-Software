from unittest.mock import patch
from tests.base_tests import BaseApiTestCase # Importamos la base

class TestThreadsEndpoint(BaseApiTestCase): # Heredamos de la base
	
	@patch('app.services.thread_service.search_thread')
	def test_search_thread(self, mock_search):
		# Ya tienes self.client disponible gracias a BaseApiTestCase
		mock_search.return_value = []
		response = self.client.get("/search_thread")
		self.assertEqual(response.status_code, 200)