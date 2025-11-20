from unittest.mock import patch
from tests.base_tests import BaseApiTestCase # Importamos la base

class TestChannelsEndpoint(BaseApiTestCase): # Heredamos de la base
	
	@patch('canales.services.search_channel')  # parcheamos la función real
    def test_search_channel_empty(self, mock_search):
        """
        Testea que el endpoint devuelva 200 y lista vacía cuando search_channel retorna vacío.
        """
        mock_search.return_value = []
        response = self.client.get("/search_channel")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('canales.services.search_channel')
    def test_search_channel_with_data(self, mock_search):
        """
        Testea que el endpoint devuelva datos correctamente.
        """
        mock_search.return_value = [
            {
                "id": "channel_1",
                "owner_id": "owner_123",
                "name": "Canal de prueba",
                "users": [
                    {"id": "user_1", "joined_at": "2025-11-20T12:00:00"}
                ],
                "channel_type": "public",
                "is_active": True,
                "created_at": "2025-11-01T10:00:00",
                "updated_at": "2025-11-15T12:00:00",
                "deleted_at": None
            }
        ]
        response = self.client.get("/search_channel", params={"q": "prueba"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], "channel_1")
        self.assertTrue(data[0]["is_active"])
