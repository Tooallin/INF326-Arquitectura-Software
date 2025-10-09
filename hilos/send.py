import pika
import json
from datetime import datetime


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='threads',
                        exchange_type='fanout')

channel.queue_declare(queue='search_threads_indexation')

channel.queue_bind(exchange='threads',
                   queue='search_threads_indexation')

#publicar evento:
hilo = {
    "id": 12345,
    "titulo": "Consulta sobre tarea de matemáticas",
    "contenido": "¿Alguien sabe cómo resolver el ejercicio 5 del capítulo 3?",
    "autor_id": 678,
    "fecha_creacion": datetime.utcnow().isoformat() + "Z",
    "tags": ["matematicas", "tarea"],
    "categoria": "foros_matematicas"
}
channel.basic_publish(exchange='threads',
                    routing_key='',
                    body=json.dumps(hilo))
print(" [°] Hilo enviado.")
connection.close()
    
