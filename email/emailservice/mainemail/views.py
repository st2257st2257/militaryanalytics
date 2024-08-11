from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from confluent_kafka import Consumer, KafkaError
from confluent_kafka import Producer

@csrf_exempt
def index_kafka_send(request):
    # localhost:9092 kafka1:19091
    config = {
        'bootstrap.servers': 'kafka1:19091',
        'broker.address.family': 'v4'
    }

    producer = Producer(config)
    # producer = Producer({"bootstrap.servers": os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")})
    producer.produce(
        'light_new',
        value='Hello Kafka Worldbjkjhbkjb123!',
        key="new")
    producer.flush(30)

    return JsonResponse({"result": True})


@csrf_exempt
def index_kafka_get(request):
    c = Consumer({
        'bootstrap.servers': 'kafka1:19091',
        'group.id': 'counting-group',
        'enable.auto.commit': True,
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'}
    })

    c.subscribe(['light_new'])
    while True:
        msg = c.poll(0.1)
        if msg is None:
            continue
        elif not msg.error():
            return JsonResponse({"result": str(msg.value()),
                                 "topic": msg.topic(),
                                 "offset": msg.offset()})
        elif msg.error().code() == KafkaError._PARTITION_EOF:
            return JsonResponse({"result": "End of partition reached"})
        else:
            return JsonResponse({"result": "Error"})
    return JsonResponse({"result": False})
