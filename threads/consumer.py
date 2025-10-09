import pika, sys, os
import json

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='threads', exchange_type='fanout')

    channel.queue_declare(queue='search_threads_indexation')

    channel.queue_bind(exchange='threads', queue='search_threads_indexation')

    def callback(ch, method, properties, body):
        hilo = json.loads(body)
        print(f"    [°] Recibido: {hilo}")
    
    channel.basic_consume(queue='search_threads_indexation', on_message_callback=callback, auto_ack=True)
    
    print('[°] Esperando mensajes. Para salir presiona CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)