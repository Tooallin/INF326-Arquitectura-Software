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

def default_serializer(obj):
	if isinstance(obj, datetime):
		return obj.isoformat() + "Z"
	raise TypeError(f"Type {type(obj)} not serializable")

# =========================
# Models (Create-only)
# =========================
class MessageCreate(BaseModel):
	id: int
	content: str
	sent_at: datetime
	author_id: int
	thread_id: int

class ChannelCreate(BaseModel):
	id: int
	title: str = Field(..., min_length=1, max_length=120)
	created_at: datetime

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
	channel_id: int
	creation_date: datetime
	tags: list[str]
	category: str


# =========================
# Publisher
# =========================
class Publisher:
	def __init__(self, exchange_durable: bool = False, auto_provision_threads_queue: bool = False):
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

		# Exchanges (todos topic)
		self.channel.exchange_declare(exchange="messages", exchange_type="topic", durable=self.exchange_durable)
		self.channel.exchange_declare(exchange="files", exchange_type="topic", durable=self.exchange_durable)
		self.channel.exchange_declare(exchange="threads", exchange_type="topic", durable=self.exchange_durable)
		self.channel.exchange_declare(exchange="channels", exchange_type="topic", durable=self.exchange_durable)

		# (opcional) provisionar cola/binding para threads con topic
		if self.auto_provision_threads_queue:
			self.channel.queue_declare(queue="search_threads_indexation", durable=False, exclusive=False, auto_delete=False)
			self.channel.queue_bind(exchange="threads", queue="search_threads_indexation", routing_key="threads.*")

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
		# Ahora threads también usa topic (no fanout)
		self._publish_topic("threads", "create", str(item.id), item.model_dump())

	def publish_channel_create(self, item: ChannelCreate):
		self._publish_topic("channels", "create", str(item.id), item.model_dump())

	def _publish_topic(self, domain: str, action: str, entity_id: str, payload: dict):
		self.connect()
		routing_key = f"{domain}.{action}.{entity_id}"
		body = json.dumps(payload, ensure_ascii=False, default=default_serializer).encode("utf-8")
		props = pika.BasicProperties(delivery_mode=2)  # persistente si las colas son durables
		log.info(f"→ publish ex={domain} rk={routing_key}")
		ok = self.channel.basic_publish(exchange=domain, routing_key=routing_key, body=body, properties=props, mandatory=False)


# =========================
# FastAPI App
# =========================
app = FastAPI(title="Events Publisher", version="1.0.0")

# Nota: por compatibilidad con exchanges existentes no durables
publisher = Publisher(exchange_durable=False)

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
		return {"status": "queued", "exchange": "threads", "routing_key": f"threads.create.{item.id}"}
	except Exception as e:
		log.exception("Error publicando thread")
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/events/channels", status_code=202)
def create_channel_event(item: ChannelCreate):
	try:
		publisher.publish_channel_create(item)
		return {
			"status": "queued",
			"exchange": "channels",
			"routing_key": f"channels.create.{item.id}"
		}
	except Exception as e:
		log.exception("Error publicando channel")
		raise HTTPException(status_code=500, detail=str(e))