from unittest.mock import patch
from ..base_tests import BaseApiTestCase

MOCK_CHANNEL_RESPONSE = {
	"id": "channel_1",
	"owner_id": "owner_123",
	"name": "Canal de prueba",
	"channel_type": "public",
	"is_active": True,
	"created_at": "2025-11-20T21:53:23.430Z",
	"updated_at": "2025-11-20T21:53:23.430Z",
	"deleted_at": None,
	"users": [
		{
			"id": "user_1",
			"joined_at": "2025-11-20T12:00:00"
		}
	]
}

class TestChannelsEndpoints(BaseApiTestCase):
	@patch("canales.services.search_channel") 
	def test_read_channels_success(self, mock_search):
		mock_search.return_value = [MOCK_CHANNEL_RESPONSE]

		response = self.client.get("/api/channel/search_channel")

		self.assertEqual(response.status_code, 200)
		data = response.json()
		
		self.assertIsInstance(data, list)
		self.assertTrue(len(data) > 0, "La lista no debería estar vacía")

		channel = data[0]
		self.assertEqual(channel["id"], "channel_1")
		self.assertEqual(channel["name"], "Canal de prueba")
		self.assertTrue(channel["is_active"])

		self.assertIsInstance(channel["users"], list)
		self.assertTrue(len(channel["users"]) > 0)
		
		user = channel["users"][0]
		self.assertEqual(user["id"], "user_1")
		self.assertEqual(user["joined_at"], "2025-11-20T12:00:00")

	@patch("canales.services.search_channel")
	def test_read_inexistent_channel(self, mock_search):
		mock_search.return_value = []

		response = self.client.get("/api/channel/search_channel", params={"q": "holamundo"})
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 0)