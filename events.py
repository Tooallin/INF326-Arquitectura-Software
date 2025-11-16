import json
import pika
import logging
import os
import requests

from mensajes.consumer import create as message_create, update as message_update, delete as message_delete
from canales.consumer import create as channel_create, update as channel_update, delete as channel_delete
from files.consumer import create_file as file_create, delete_file as file_delete
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
		# self.channel.exchange_declare(exchange='messages', exchange_type='topic')
		self.channel.exchange_declare(exchange='channel_service_exchange', exchange_type='topic', durable=True)
		self.channel.exchange_declare(exchange="files", exchange_type="topic", durable=True)
		self.channel.exchange_declare(exchange='platform.events', exchange_type='topic', durable=True)

		# Declaración de cola para mensajes
		self.channel.queue_declare(queue="messages_service", durable=True)
		
		# Declaración de cola para canales
		self.channel.queue_declare('search_service_of_channel_service', durable=True)
		self.channel.queue_bind(exchange='channel_service_exchange', queue="search_service_of_channel_service", routing_key="channelService.v1.channel.*")

		# Declaración de cola para archivos
		self.channel.queue_declare("search_service_of_files_service", durable=True)
		self.channel.queue_bind(exchange="files", queue="search_service_of_files_service", routing_key="files.*.*")

		# Declaración de cola para hilos
		self.channel.queue_declare(queue='search_service_of_threads_service', durable=True)
		self.channel.queue_bind(exchange='platform.events', queue='search_service_of_threads_service', routing_key="thread.*")
		
		# Consumidores y callbacks (separados)
		self.channel.basic_consume(queue='messages_service', on_message_callback=self.callback_messages)
		self.channel.basic_consume(queue='search_service_of_channel_service', on_message_callback=self.callback_channels)
		self.channel.basic_consume(queue="search_service_of_files_service", on_message_callback=self.callback_files)
		self.channel.basic_consume(queue="search_service_of_threads_service", on_message_callback=self.callback_threads)

		self.channel.start_consuming()

	def callback_messages(self, ch, method, properties, body):
		body = json.loads(body)
		routing_key = method.routing_key 

		if routing_key.startswith("messages_service"):
			logging.info(f"Evento de creación de mensaje recibido: {body['id']}")
			try:
				message_create(body)
				logging.info(f"Nuevo mensaje creado: {body['id']}")
			except Exception as e:
				logging.error(f"⚠️ Ocurrió un error: {e}")
		# elif routing_key.startswith("messages.update"):
		# 	logging.info(f"Evento de actualización de mensaje recibido: {body['id']}")
		# 	try:
		# 		message_update(body)
		# 		logging.info(f"Mensaje actualizado: {body['id']}")
		# 	except Exception as e:
		# 		logging.error(f"⚠️ Ocurrió un error: {e}")
		# elif routing_key.startswith("messages.delete"):
		# 	logging.info(f"Evento de eliminación de mensaje recibido: {body['name']}")
		# 	try:
		# 		message_delete(body)
		# 		logging.info(f"Mensaje eliminado: {body['name']} 👋")
		# 	except Exception as e:
		# 		logging.error(f"⚠️ Ocurrió un error: {e}")
		else:
			logging.warning(f"Evento no reconocido: {routing_key}")

		ch.basic_ack(delivery_tag=method.delivery_tag)
		
	def callback_channels(self, ch, method, properties, body):
		body = json.loads(body)
		routing_key = method.routing_key 

		if routing_key.startswith("channelService.v1.channel.created"):
			logging.info(f"Evento de creación de canal recibido: {body['channel_id']}")
			try:
				response = requests.get(f"https://channel-api.inf326.nur.dev/v1/channels/{body['channel_id']}")
				payload = response.json()
				channel_create(payload)
				logging.info(f"Nuevo canal creado: {body['channel_id']}")
			except Exception as e:
				logging.error(f"⚠️ Ocurrió un error: {e}")
		elif routing_key.startswith("channelService.v1.channel.updated") or routing_key.startswith("channelService.v1.channel.reactivated"):
			logging.info(f"Evento de actualización de canal recibido: {body['channel_id']}")
			try:
				if routing_key.startswith("channelService.v1.channel.updated"):
					updated_fields = body.pop("updated_fields", {})  # lo sacamos del diccionario

					# aplanar el payload recibido
					flattened = {
						**body,
						**updated_fields,
					}
					channel_update(flattened)
				else:
					channel_update(body)
				logging.info(f"Canal actualizado: {body['channel_id']}")
			except Exception as e:
				logging.error(f"⚠️ Ocurrió un error: {e}")
		elif routing_key.startswith("channelService.v1.channel.deleted"):
			logging.info(f"Evento de eliminación de canal recibido: {body['channel_id']}")
			try:
				channel_delete(body)
				logging.info(f"Canal eliminado: {body['channel_id']} 👋")
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
			if rk.startswith("files.added.v1"):
				p = payload.get("data")
				logging.info(f"[files.added.v1] id={p['file_id']}")
				try:
					response = requests.get(f"http://134.199.176.197/v1/files/{p['file_id']}")
					payload = response.json()
					file_create(payload)
					logging.info(f"Nuevo archivo creado: {payload.get("id")}")
				except Exception as e:
					logging.error(f"Error al crear un archivo: {e}")
			# elif rk.startswith("files.update"):
			# 	logging.info(f"[files.update] id={payload.get("id")} name={payload.get("name")}")
			# 	# TODO file_update(payload)
			elif rk.startswith("files.deleted.v1"):
				p = payload.get("data")
				p["deleted_at"] = payload.get("occurred_at")
				logging.info(f"[files.deleted.v1] id={p['file_id']}")
				file_delete(p)
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
			if rk.startswith("thread.created"):
				logging.info(f"[thread.created] id={payload.get("id")} title={payload.get("title")}")
				create_thread(payload)
			elif rk.startswith("thread.updated") or rk.startswith("thread.archieved"):
				logging.info(f"[thread.updated] id={payload.get("id")} title={payload.get("title")}")
				update_thread(payload)
			elif rk.startswith("thread.deleted"):
				logging.info(f"[thread.deleted] id={payload.get("id")}")
				delete_thread(payload)
			else:
				logging.warning(f"[threads.*] routing no reconocido: {rk}")
			ch.basic_ack(delivery_tag=method.delivery_tag)
		except Exception as e:
			logging.error(f"Error en callback_files: {e}")
			ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
	def close(self):
		self.connection.close()