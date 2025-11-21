from unittest.mock import patch
from ..base_tests import BaseApiTestCase

MOCK_THREAD = {
    "id": "thread_001",
    "channel_id": "channel_123",
    "title": "Discusión general",
    "created_by": "user_789",
    "status": "open",
    "meta": {
        "priority": "high",
        "tags": ["soporte", "general"],
        "extra_info": {"origin": "web"}
    },
    "created_at": "2025-01-10T15:30:00",
    "updated_at": "2025-01-10T16:00:00",
    "deleted_at": None
}

class TestThreadsEndpoints(BaseApiTestCase):
	@patch("threads.services.get_by_id") 
	def test_search_threads_by_id_success(self, mock_search):
		mock_search.return_value = [MOCK_THREAD]

		response = self.client.get("/api/threads/id/"+"thread_001")

		self.assertEqual(response.status_code, 200)
		data = response.json()
		
		self.assertIsInstance(data, list)
		self.assertEqual(len(data), 1)
 
		thread = data[0]
		self.assertEqual(thread["id"], "thread_001")
		self.assertEqual(thread["channel_id"], "channel_123")
		self.assertEqual(thread["title"], "Discusión general")
		self.assertEqual(thread["created_by"], "user_789")
		self.assertEqual(thread["status"], "open")

		self.assertIsInstance(thread["meta"], dict)
		self.assertEqual(thread["meta"]["priority"], "high")
		self.assertEqual(thread["meta"]["tags"], ["soporte", "general"])
		self.assertEqual(thread["meta"]["extra_info"], {"origin": "web"})

		self.assertEqual(thread["created_at"], "2025-01-10T15:30:00")
		self.assertEqual(thread["updated_at"], "2025-01-10T16:00:00")
		self.assertIsNone(thread["deleted_at"])

	@patch("threads.services.get_by_id") 
	def test_search_threads_by_id_empty(self, mock_search):
		mock_search.return_value = []

		response = self.client.get("/api/threads/id/"+"thread_-12")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 0)


	# -------------------------- AUTHOR ------------------------------
	@patch("threads.services.get_by_author") 
	def test_search_threads_by_author_success(self, mock_search):
		mock_search.return_value = [MOCK_THREAD]

		response = self.client.get("/api/threads/author/"+"user_789")

		self.assertEqual(response.status_code, 200)
		data = response.json()
		
		self.assertIsInstance(data, list)
		self.assertEqual(len(data), 1)
 
		thread = data[0]
		self.assertEqual(thread["id"], "thread_001")
		self.assertEqual(thread["channel_id"], "channel_123")
		self.assertEqual(thread["title"], "Discusión general")
		self.assertEqual(thread["created_by"], "user_789")
		self.assertEqual(thread["status"], "open")

		self.assertIsInstance(thread["meta"], dict)
		self.assertEqual(thread["meta"]["priority"], "high")
		self.assertEqual(thread["meta"]["tags"], ["soporte", "general"])
		self.assertEqual(thread["meta"]["extra_info"], {"origin": "web"})

		self.assertEqual(thread["created_at"], "2025-01-10T15:30:00")
		self.assertEqual(thread["updated_at"], "2025-01-10T16:00:00")
		self.assertIsNone(thread["deleted_at"])

	@patch("threads.services.get_by_author") 
	def test_search_threads_by_author_empty(self, mock_search):
		mock_search.return_value = []

		response = self.client.get("/api/threads/author/"+"user_-12")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 0)

	# -------------------------- DATE ------------------------------
	@patch("threads.services.get_by_date_range") 
	def test_search_threads_by_date_success(self, mock_search):
		mock_search.return_value = [MOCK_THREAD]

		response = self.client.get("/api/threads/daterange/", params={"start_date": "2025-01-10T14:30:00", "end_date": "2025-01-10T17:30:00"})

		self.assertEqual(response.status_code, 200)
		data = response.json()
		
		self.assertIsInstance(data, list)
		self.assertEqual(len(data), 1)
 
		thread = data[0]
		self.assertEqual(thread["id"], "thread_001")
		self.assertEqual(thread["channel_id"], "channel_123")
		self.assertEqual(thread["title"], "Discusión general")
		self.assertEqual(thread["created_by"], "user_789")
		self.assertEqual(thread["status"], "open")

		self.assertIsInstance(thread["meta"], dict)
		self.assertEqual(thread["meta"]["priority"], "high")
		self.assertEqual(thread["meta"]["tags"], ["soporte", "general"])
		self.assertEqual(thread["meta"]["extra_info"], {"origin": "web"})

		self.assertEqual(thread["created_at"], "2025-01-10T15:30:00")
		self.assertEqual(thread["updated_at"], "2025-01-10T16:00:00")
		self.assertIsNone(thread["deleted_at"])

	@patch("threads.services.get_by_date_range") 
	def test_search_threads_by_date_empty(self, mock_search):
		mock_search.return_value = []

		response = self.client.get("/api/threads/daterange/", params={"start_date": "2025-01-10T14:30:00", "end_date": "2025-01-10T17:30:00"})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 0)

	# -------------------------- KEYWORD ------------------------------
	@patch("threads.services.get_by_keyword") 
	def test_search_threads_by_keyword_success(self, mock_search):
		mock_search.return_value = [MOCK_THREAD]

		response = self.client.get("/api/threads/keyword/"+"Discusión")

		self.assertEqual(response.status_code, 200)
		data = response.json()
		
		self.assertIsInstance(data, list)
		self.assertEqual(len(data), 1)
 
		thread = data[0]
		self.assertEqual(thread["id"], "thread_001")
		self.assertEqual(thread["channel_id"], "channel_123")
		self.assertEqual(thread["title"], "Discusión general")
		self.assertEqual(thread["created_by"], "user_789")
		self.assertEqual(thread["status"], "open")

		self.assertIsInstance(thread["meta"], dict)
		self.assertEqual(thread["meta"]["priority"], "high")
		self.assertEqual(thread["meta"]["tags"], ["soporte", "general"])
		self.assertEqual(thread["meta"]["extra_info"], {"origin": "web"})

		self.assertEqual(thread["created_at"], "2025-01-10T15:30:00")
		self.assertEqual(thread["updated_at"], "2025-01-10T16:00:00")
		self.assertIsNone(thread["deleted_at"])

	@patch("threads.services.get_by_keyword") 
	def test_threads_by_keyword_empty(self, mock_search):
		mock_search.return_value = []

		response = self.client.get("/api/threads/keyword/"+"Discusión")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 0)

	# -------------------------- STATUS ------------------------------
	@patch("threads.services.get_by_status") 
	def test_search_threads_by_status_success(self, mock_search):
		mock_search.return_value = [MOCK_THREAD]

		response = self.client.get("/api/threads/status/"+"open")

		self.assertEqual(response.status_code, 200)
		data = response.json()
		
		self.assertIsInstance(data, list)
		self.assertEqual(len(data), 1)
 
		thread = data[0]
		self.assertEqual(thread["id"], "thread_001")
		self.assertEqual(thread["channel_id"], "channel_123")
		self.assertEqual(thread["title"], "Discusión general")
		self.assertEqual(thread["created_by"], "user_789")
		self.assertEqual(thread["status"], "open")

		self.assertIsInstance(thread["meta"], dict)
		self.assertEqual(thread["meta"]["priority"], "high")
		self.assertEqual(thread["meta"]["tags"], ["soporte", "general"])
		self.assertEqual(thread["meta"]["extra_info"], {"origin": "web"})

		self.assertEqual(thread["created_at"], "2025-01-10T15:30:00")
		self.assertEqual(thread["updated_at"], "2025-01-10T16:00:00")
		self.assertIsNone(thread["deleted_at"])

	@patch("threads.services.get_by_status") 
	def test_search_threads_by_status_empty(self, mock_search):
		mock_search.return_value = []

		response = self.client.get("/api/threads/keyword/"+"closed")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 0)