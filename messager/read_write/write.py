from confluent_kafka import Producer

# p = Producer({'bootstrap.servers': 'localhost:9091'})

config = {
    'bootstrap.servers': 'localhost:9092',
}

producer = Producer(config)

def send_message(topic, message):
    producer.produce(topic, value=message, key="new")
    producer.flush(30)

send_message('light_new', 'Hello Kafka World!')
