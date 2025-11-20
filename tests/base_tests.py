import unittest
from fastapi.testclient import TestClient

from main import app

class BaseApiTestCase(unittest.TestCase):
	"""
	Clase base para tests de API.
	Configura el cliente una sola vez para todos los tests que hereden de aquí.
	"""
	def setUp(self):
		# Aquí puedes poner lógica de "antes de cada test" global
		# Por ejemplo: limpiar base de datos de prueba, resetear mocks, etc.
		self.client = TestClient(app)

	def tearDown(self):
		# Lógica de limpieza después de cada test
		pass