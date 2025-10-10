import os
import json
import logging
from datetime import datetime
from typing import Optional

import pika
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger("pika").setLevel(logging.ERROR)
log = logging.getLogger(__name__)


# =========================
# Models (Create-only)
# =========================
class MessageCreate(BaseModel):
	id: int
	content: str
	sent_at: datetime
	author_id: int
	thread_id: int


class FileCreate(BaseModel):
	id: int
	thread_id: int
	message_id: int
	name: str
	content: str
	pages: int
	uploaded_at: datetime


class ThreadCreate(BaseModel):
	id: int
	title: str
	content: str
	author_id: int
	creation_date: datetime = Field(default_factory=datetime.utcnow)
	tags: list[str] = Field(default_factory=list)
	category: Optional[str] = None


# =========================
# Publisher
# =========================
class Publisher:
	def __init__(self, exchange_durable: bool = True, auto_provision_threads_queue: bool = False):
		self.exchange_durable = exchange_durable
		self.auto_provision_threads_queue = auto_provision_threads_queue
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

		# Exchanges
		self.channel.exchange_declare(exchange="messages", exchange_type="topic", durable=self.exchange_durable)
		self.channel.exchange_declare(exchange="files", exchange_type="topic", durable=self.exchange_durable)
		self.channel.exchange_declare(exchange="threads", exchange_type="fanout", durable=self.exchange_durable)

		if self.auto_provision_threads_queue:
			self.channel.queue_declare(queue="search_threads_indexation", durable=False, exclusive=False, auto_delete=False)
			self.channel.queue_bind(exchange="threads", queue="search_threads_indexation")

		self.channel.confirm_delivery()

	def close(self):
		try:
			if self.channel and self.channel.is_open:
				self.channel.close()
		finally:
			if self.connection and self.connection.is_open:
				self.connection.close()

	def publish_message_create(self, item: MessageCreate):
		self._publish_topic("messages", "create", str(item.id), item.model_dump())

	def publish_file_create(self, item: FileCreate):
		self._publish_topic("files", "create", str(item.id), item.model_dump())

	def publish_thread_create(self, item: ThreadCreate):
		self._publish_fanout("threads", item.model_dump())

	def _publish_topic(self, domain: str, action: str, entity_id: str, payload: dict):
		self.connect()
		routing_key = f"{domain}.{action}.{entity_id}"
		body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
		props = pika.BasicProperties(delivery_mode=2)
		log.info(f"→ publish ex={domain} rk={routing_key}")
		ok = self.channel.basic_publish(exchange=domain, routing_key=routing_key, body=body, properties=props, mandatory=False)
		if not ok:
			raise RuntimeError(f"No se pudo confirmar publicación: {domain}:{routing_key}")

	def _publish_fanout(self, exchange: str, payload: dict):
		self.connect()
		body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
		props = pika.BasicProperties(delivery_mode=2)
		log.info(f"→ broadcast ex={exchange} (fanout)")
		ok = self.channel.basic_publish(exchange=exchange, routing_key="", body=body, properties=props, mandatory=False)
		if not ok:
            # This indent block must be tabs; ensure proper indentation
			raise RuntimeError("No se pudo confirmar publicación en fanout '{exchange}'.")


# =========================
# FastAPI App
# =========================
app = FastAPI(title="Events Publisher", version="1.0.0")

publisher = Publisher()

@app.get("/health")
def health():
	try:
		publisher.connect()
		return {"ok": True}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/events/messages", status_code=202)
def create_message_event(item: MessageCreate):
	try:
		publisher.publish_message_create(item)
		return {"status": "queued", "exchange": "messages", "routing_key": f"messages.create.{item.id}"}
	except Exception as e:
		log.exception("Error publicando mensaje")
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/events/files", status_code=202)
def create_file_event(item: FileCreate):
	try:
		publisher.publish_file_create(item)
		return {"status": "queued", "exchange": "files", "routing_key": f"files.create.{item.id}"}
	except Exception as e:
		log.exception("Error publicando file")
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/events/threads", status_code=202)
def create_thread_event(item: ThreadCreate):
	try:
		publisher.publish_thread_create(item)
		return {"status": "queued", "exchange": "threads", "routing_key": ""}
	except Exception as e:
		log.exception("Error publicando thread")
		raise HTTPException(status_code=500, detail=str(e))
