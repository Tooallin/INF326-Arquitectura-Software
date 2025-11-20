import unittest
from fastapi.testclient import TestClient
from main import app

class BaseApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)