from unittest.mock import patch
from tests.base_tests import BaseApiTestCase # Importamos la base

class TestMessagesEndpoint(BaseApiTestCase): # Heredamos de la base
	
	@patch('app.services.message_service.search_message')
	def test_search_message(self, mock_search):
		# Ya tienes self.client disponible gracias a BaseApiTestCase
		mock_search.return_value = []
		response = self.client.get("/search_message")
		self.assertEqual(response.status_code, 200)