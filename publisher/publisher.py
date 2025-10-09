import os
import json
import logging
import pika
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import time
import random

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger("pika").setLevel(logging.ERROR)


class Publisher:
	def __init__(self, exchange_durable: bool = True):
		self.exchange_durable = exchange_durable
		self.connection = None
		self.channel = None

	def connect(self):
		if self.connection and self.connection.is_open and self.channel and self.channel.is_open:
			return

		url = os.getenv("RABBITMQ_URL")
		if url:
			params = pika.URLParameters(url)
		else:
			host = os.getenv("RABBITMQ_HOST", "localhost")
			params = pika.ConnectionParameters(
				host=host,
				heartbeat=30,
				blocked_connection_timeout=30
			)

		self.connection = pika.BlockingConnection(params)
		self.channel = self.connection.channel()

		# Exchanges topic (mismo nombre que en tu consumidor)
		self.channel.exchange_declare(exchange="messages", exchange_type="topic", durable=self.exchange_durable)
		self.channel.exchange_declare(exchange="files", exchange_type="topic", durable=self.exchange_durable)

		# Publisher confirms
		self.channel.confirm_delivery()

	def close(self):
		try:
			if self.channel and self.channel.is_open:
				self.channel.close()
		finally:
			if self.connection and self.connection.is_open:
				self.connection.close()

	def _publish(self, domain: str, action: str, entity_id: Optional[str], payload: Dict[str, Any], headers: Optional[Dict[str, Any]] = None):
		if domain not in ("messages", "files"):
			raise ValueError("domain debe ser 'messages' o 'files'")
		if not action:
			raise ValueError("action no puede ser vacío")
		if not isinstance(payload, dict):
			raise ValueError("payload debe ser dict")

		self.connect()

		routing_key = f"{domain}.{action}.{entity_id or 'none'}"
		body = json.dumps(payload, ensure_ascii=False)

		props = pika.BasicProperties(
			delivery_mode=2,  # persistente (si la cola es durable)
			headers=headers or {}
		)

		log.info(f"→ publish ex={domain} rk={routing_key}")
		ok = self.channel.basic_publish(
			exchange=domain,
			routing_key=routing_key,
			body=body.encode("utf-8"),
			properties=props,
			mandatory=False
		)
		if not ok:
			raise RuntimeError(f"No se pudo confirmar publicación: {domain}:{routing_key}")

	# ==== HELPERS: MESSAGES ====
	def message_create(self, payload: Dict[str, Any], headers: Optional[Dict[str, Any]] = None):
		self._publish("messages", "create", str(payload.get("id")), payload, headers)

	def message_update(self, payload: Dict[str, Any], headers: Optional[Dict[str, Any]] = None):
		self._publish("messages", "update", str(payload.get("id")), payload, headers)

	def message_delete(self, message_id: int, headers: Optional[Dict[str, Any]] = None):
		self._publish("messages", "delete", str(message_id), {"id": int(message_id)}, headers)

	# ==== HELPERS: FILES ====
	def file_create(self, payload: Dict[str, Any], headers: Optional[Dict[str, Any]] = None):
		self._publish("files", "create", str(payload.get("id")), payload, headers)

	def file_update(self, payload: Dict[str, Any], headers: Optional[Dict[str, Any]] = None):
		self._publish("files", "update", str(payload.get("id")), payload, headers)

	def file_delete(self, file_id: int, headers: Optional[Dict[str, Any]] = None):
		self._publish("files", "delete", str(file_id), {"id": int(file_id)}, headers)

	def __enter__(self):
		self.connect()
		return self

	def __exit__(self, exc_type, exc, tb):
		self.close()


# =========================
# SEED DE EVENTOS DE PRUEBA
# =========================
def iso(dt: datetime) -> str:
	# ISO 8601 con 'Z' (UTC). Ajusta si prefieres offset local.
	return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def seed_test_events():
	now = datetime.utcnow()
	trace = f"seed-{int(now.timestamp())}"

	# Datos de prueba coherentes con tus mappings
	# MESSAGES mapping:
	#   id (integer), content (text), sent_at (date), author_id (integer), thread_id (integer)
	messages = [
		{
			"id": 1001,
			"content": "Hola, este es un mensaje de prueba.",
			"sent_at": iso(now - timedelta(minutes=5)),
			"author_id": 10,
			"thread_id": 501
		},
		{
			"id": 1002,
			"content": "¿Puedes revisar el archivo que subí?",
			"sent_at": iso(now - timedelta(minutes=4)),
			"author_id": 11,
			"thread_id": 501
		},
		{
			"id": 1003,
			"content": "Actualicé el contenido del documento.",
			"sent_at": iso(now - timedelta(minutes=3)),
			"author_id": 12,
			"thread_id": 502
		},
	]

	# FILES mapping:
	#   id (integer), thread_id (integer), message_id (integer),
	#   name (text), content (text), pages (integer), uploaded_at (date)
	files = [
		{
			"id": 7001,
			"thread_id": 501,
			"message_id": 1002,
			"name": "examen_hematologia.pdf",
			"content": "Informe de hematología básico con hemograma completo.",
			"pages": 3,
			"uploaded_at": iso(now - timedelta(minutes=4, seconds=30))
		},
		{
			"id": 7002,
			"thread_id": 502,
			"message_id": 1003,
			"name": "rehabilitacion_hombro.pdf",
			"content": "Rutina de ejercicios de rehabilitación del manguito rotador.",
			"pages": 5,
			"uploaded_at": iso(now - timedelta(minutes=2, seconds=10))
		},
	]

	with Publisher() as pub:
		# ---- creates ----
		for m in messages:
			pub.message_create(m, headers={"trace_id": trace, "domain": "seed"})
			time.sleep(0.05)

		for f in files:
			pub.file_create(f, headers={"trace_id": trace, "domain": "seed"})
			time.sleep(0.05)

		# ---- updates (ejemplos mínimos) ----
		# Solo campos modificados + id
		pub.message_update({"id": 1003, "content": "Actualicé el contenido del documento. (v2)"}, headers={"trace_id": trace})
		time.sleep(0.05)
		pub.file_update({"id": 7002, "pages": 6}, headers={"trace_id": trace})
		time.sleep(0.05)

		# ---- deletes (ejemplos) ----
		pub.message_delete(1001, headers={"trace_id": trace})
		time.sleep(0.05)
		pub.file_delete(7001, headers={"trace_id": trace})

	logging.info("✅ Seed de eventos enviado.")


if __name__ == "__main__":
	# Opcional: fija host por defecto para desarrollo en Docker
	os.environ.setdefault("RABBITMQ_HOST", "message_broker")
	seed_test_events()