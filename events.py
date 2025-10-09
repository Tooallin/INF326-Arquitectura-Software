import json
import pika
import logging
import os 

from mensajes.consumer import create as message_create
from files.consumer import create_file as file_create

logging.getLogger("pika").setLevel(logging.ERROR)

'''
class Emit:
	def send(self, id, action, payload):
		self.connect()
		self.publish(id, action, payload)
		self.close()

	def connect(self):
		self.connection = pika.BlockingConnection(
			pika.ConnectionParameters(host='demo_04_message_broker')
		)

		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange='players',
									  exchange_type='topic')

	def publish(self, id, action, payload):
		routing_key = f"player.{action}.{id}"
		message = json.dumps(payload)

		self.channel.basic_publish(exchange='players',
								   routing_key=routing_key,
								   body=message)

	def close(self):
		self.connection.close()
'''

class Receive:
	def __init__(self):
		logging.info("Waiting for messages...")
		self.connection = pika.BlockingConnection(
			pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST"))
		)
		self.channel = self.connection.channel()

		# Declaración de exchanges de tipo topic
		self.channel.exchange_declare(exchange='messages', exchange_type='topic')
		self.channel.exchange_declare(exchange="files", exchange_type="topic")

		# Declaración de cola para mensajes
		self.channel.queue_declare('messages', exclusive=True)
		self.channel.queue_bind(exchange='messages', queue="messages", routing_key="messages.*.*")

		# Declaración de cola para archivos
		self.channel.queue_declare("q.files", exclusive=True)
		self.channel.queue_bind(exchange="files", queue="q.files", routing_key="files.*.*")

		# Consumidores y callbacks (separados)
		self.channel.basic_consume(queue='messages', on_message_callback=self.callback_messages)
		self.channel.basic_consume(queue="q.files", on_message_callback=self.callback_files)

		self.channel.start_consuming()

	def callback_messages(self, ch, method, properties, body):
		body = json.loads(body)
		routing_key = method.routing_key 

		if routing_key.startswith("messages.create"):
			logging.info(f"Evento de creación de mensaje recibido: {body['id']}")
			try:
				message_create(body)
				logging.info(f"Nuevo mensaje creado: {body['id']}")
			except Exception as e:
				logging.error(f"⚠️ Ocurrió un error: {e}")
				
		elif routing_key.startswith("messages.update"):
			logging.info(f"Evento de actualización de mensaje recibido: {body['id']}")
			logging.info(f"Mensaje actualizado: {body['id']}")
		elif routing_key.startswith("messages.delete"):
			logging.info(f"Evento de eliminación de mensaje recibido: {body['name']}")
			logging.info(f"Mensaje eliminado: {body['name']} 👋")
		else:
			logging.warning(f"Evento no reconocido: {routing_key}")

		ch.basic_ack(delivery_tag=method.delivery_tag)

	def callback_files(self, ch, method, properties, body):
		try:
			payload = json.loads(body)
			rk = method.routing_key
			if rk.startswith("files.create"):
				logging.info(f"[files.create] id={payload.get("id")} name={payload.get("name")}")
				file_create(payload)
			if rk.startswith("files.update"):
				logging.info(f"[files.update] id={payload.get("id")} name={payload.get("name")}")
				# TODO file_update(payload)
			if rk.startswith("files.delete"):
				logging.info(f"[files.delete] id={payload.get("id")} name={payload.get("name")}")
				# TODO file_delete(payload)
			else:
				logging.warning(f"[files.*] routing no reconocido: {rk}")
			ch.basic_ack(delivery_tag=method.delivery_tag)
		except Exception as e:
			logging.error(f"Error en callback_files: {e}")
			ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

	def close(self):
		self.connection.close()