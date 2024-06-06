from OCR import OCR
import pika

#initialize ocr pipeline interface
ocr = OCR()

#process messages
def ocr_callback(ch, method, properties, body):

    # get audio transcribed
    response = ocr.recognize(f'images/{body.decode()}')

    #publish into temp queue, consumer exmpl: ASR_gateway/main_cons.py
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

#initialize basic consumer
def start_ocr_worker():
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='i2t', durable=True)
    channel.basic_consume(queue='i2t', on_message_callback=ocr_callback)
    print('Worker1 waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    start_ocr_worker()