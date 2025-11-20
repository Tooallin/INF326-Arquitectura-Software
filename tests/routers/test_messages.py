from unittest.mock import patch
from ..base_tests import BaseApiTestCase

MOCK_MESSAGE = {
	"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
	"content": "Hola, buscame en el test",
	"user_id": "123e4567-e89b-12d3-a456-426614174000",
	"thread_id": "987fcdeb-51a2-43fb-9876-543210987654",
	"type": "text",
	"paths": [
	  "imagen_adjunta.jpg"
	],
	"created_at": "2025-11-20T21:49:49.082Z",
	"updated_at": "2025-11-20T21:49:49.082Z",
	"deleted_at": None
}

class TestMessagesEndpoints(BaseApiTestCase):
	@patch("mensajes.services.search_message") 
	def test_search_messages_success(self, mock_search):
		mock_search.return_value = [MOCK_MESSAGE]

		response = self.client.get("/api/message/search_message", params={"q": "Hola"})

		self.assertEqual(response.status_code, 200)
		data = response.json()
		
		self.assertIsInstance(data, list)
		self.assertEqual(len(data), 1)
 
		mensaje = data[0]
		self.assertEqual(mensaje["content"], "Hola, buscame en el test")
		self.assertEqual(mensaje["type"], "text")
		
		self.assertIsInstance(mensaje["paths"], list)
		self.assertEqual(mensaje["paths"][0], "imagen_adjunta.jpg")

	@patch("mensajes.services.search_message")
	def test_search_messages_empty(self, mock_search):
		mock_search.return_value = []

		response = self.client.get("/api/message/search_message", params={"q": "texto_inexistente"})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 0)