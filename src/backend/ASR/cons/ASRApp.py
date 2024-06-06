import whisperx
from ASR import ASR
import pika

#initialize asr model interface
asr = ASR()

#process messages
def recognition_callback(ch, method, properties, body):
    print(f"recognition received {body}")

    #load audio with whisperx
    audio = whisperx.load_audio(f'audios/{body.decode()}')

    # get audio transcribed
    response = asr.transcribation(audio)

    #publish into temp queue
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


#initialize basic consumer
def start_recognition_worker():
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='recognition', durable=True)
    channel.basic_consume(queue='recognition', on_message_callback=recognition_callback)
    print('Worker1 waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    start_recognition_worker()