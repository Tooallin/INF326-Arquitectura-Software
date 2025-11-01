import json
import pika
import logging
import os

from mensajes.consumer import create as message_create, update as message_update, delete as message_delete
from canales.consumer import create as channel_create, update as channel_update, delete as channel_delete
from files.consumer import create_file as file_create
from threads.consumer import *

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

		# Declaración de exchanges de tipo topic*
		self.channel.exchange_declare(exchange='messages', exchange_type='topic')
		self.channel.exchange_declare(exchange='channels', exchange_type='topic')
		self.channel.exchange_declare(exchange="files", exchange_type="topic")
		self.channel.exchange_declare(exchange='threads', exchange_type='topic')

		# Declaración de cola para mensajes
		self.channel.queue_declare('messages', durable=True)
		self.channel.queue_bind(exchange='messages', queue="messages", routing_key="messages.*.*")
		
		# Declaración de cola para canales
		self.channel.queue_declare('channels', durable=True)
		self.channel.queue_bind(exchange='channels', queue="channels", routing_key="channels.*.*")

		# Declaración de cola para archivos
		self.channel.queue_declare("files", durable=True)
		self.channel.queue_bind(exchange="files", queue="files", routing_key="files.*.*")

		# Declaración de cola para hilos
		self.channel.queue_declare(queue='threads', durable=True)
		self.channel.queue_bind(exchange='threads', queue='threads', routing_key="threads.*.*")
		
		# Consumidores y callbacks (separados)
		self.channel.basic_consume(queue='messages', on_message_callback=self.callback_messages)
		self.channel.basic_consume(queue='channels', on_message_callback=self.callback_channels)
		self.channel.basic_consume(queue="files", on_message_callback=self.callback_files)
		self.channel.basic_consume(queue="threads", on_message_callback=self.callback_threads)

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
			try:
				message_update(body)
				logging.info(f"Mensaje actualizado: {body['id']}")
			except Exception as e:
				logging.error(f"⚠️ Ocurrió un error: {e}")
		elif routing_key.startswith("messages.delete"):
			logging.info(f"Evento de eliminación de mensaje recibido: {body['name']}")
			try:
				message_delete(body)
				logging.info(f"Mensaje eliminado: {body['name']} 👋")
			except Exception as e:
				logging.error(f"⚠️ Ocurrió un error: {e}")
		else:
			logging.warning(f"Evento no reconocido: {routing_key}")

		ch.basic_ack(delivery_tag=method.delivery_tag)
		
	def callback_channels(self, ch, method, properties, body):
		body = json.loads(body)
		routing_key = method.routing_key 

		if routing_key.startswith("channels.create"):
			logging.info(f"Evento de creación de canal recibido: {body['id']}")
			try:
				channel_create(body)
				logging.info(f"Nuevo canal creado: {body['id']}")
			except Exception as e:
				logging.error(f"⚠️ Ocurrió un error: {e}")
		elif routing_key.startswith("channels.update"):
			logging.info(f"Evento de actualización de canal recibido: {body['id']}")
			try:
				channel_update(body)
				logging.info(f"Canal actualizado: {body['id']}")
			except Exception as e:
				logging.error(f"⚠️ Ocurrió un error: {e}")
		elif routing_key.startswith("channels.delete"):
			logging.info(f"Evento de eliminación de canal recibido: {body['name']}")
			try:
				channel_delete(body)
				logging.info(f"Canal eliminado: {body['name']} 👋")
			except Exception as e:
				logging.error(f"⚠️ Ocurrió un error: {e}")
		else:
			logging.warning(f"Evento no reconocido: {routing_key}")

		ch.basic_ack(delivery_tag=method.delivery_tag)

	def callback_files(self, ch, method, properties, body):
		try:
			payload = json.loads(body)
		except Exception as e:
			logging.error(f"[files.*] body inválido (no JSON): {e}")
			# No se puede procesar → NACK sin requeue para no quedar en loop
			ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
			return
		
		rk = method.routing_key
		try:
			if rk.startswith("files.create"):
				logging.info(f"[files.create] id={payload.get("id")} name={payload.get("name")}")
				try:
					file_create(payload)
					logging.info(f"Nuevo archivo creado: {payload.get("id")}")
				except Exception as e:
					logging.error(f"Error al crear un archivo: {e}")
			elif rk.startswith("files.update"):
				logging.info(f"[files.update] id={payload.get("id")} name={payload.get("name")}")
				# TODO file_update(payload)
			elif rk.startswith("files.delete"):
				logging.info(f"[files.delete] id={payload.get("id")} name={payload.get("name")}")
				# TODO file_delete(payload)
			else:
				logging.warning(f"[files.*] routing no reconocido: {rk}")
			ch.basic_ack(delivery_tag=method.delivery_tag)
		except Exception as e:
			logging.error(f"Error en callback_files: {e}")
			ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

	def callback_threads(self, ch, method, properties, body):
		try:
			payload = json.loads(body)
		except Exception as e:
			logging.error(f"[files.*] body inválido (no JSON): {e}")
			# No se puede procesar → NACK sin requeue para no quedar en loop
			ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
			return
		
		rk = method.routing_key
		try:
			if rk.startswith("threads.create"):
				logging.info(f"[threads.create] id={payload.get("id")} title={payload.get("title")}")
				create_thread(payload)
			elif rk.startswith("threads.update"):
				logging.info(f"[threads.update] id={payload.get("id")} title={payload.get("title")}")
				update_thread(payload)
			elif rk.startswith("threads.delete"):
				logging.info(f"[threads.delete] id={payload.get("id")} title={payload.get("title")}")
				delete_thread(payload)
			else:
				logging.warning(f"[threads.*] routing no reconocido: {rk}")
			ch.basic_ack(delivery_tag=method.delivery_tag)
		except Exception as e:
			logging.error(f"Error en callback_files: {e}")
			ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
	def close(self):
		self.connection.close()