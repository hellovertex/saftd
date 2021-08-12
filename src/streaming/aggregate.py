"""
1. Launch Kafka:
 - $KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties
 - $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties

run via faust -A <filename> worker -l info

2. Faust library:
  faust.App.agent: - main processing actor in Faust App
"""

import faust
from kafka import KafkaProducer

# Project imports
from cfg import TOPIC_RAW_TICKS, TOPIC_BATCH_TICKS, PORT_AGGREGATOR, AGGREGATE_CONSUMER_GROUP_ID, BATCH_SIZE
from modelling.tick import Tick


app = faust.App(
    id=AGGREGATE_CONSUMER_GROUP_ID,
    broker='kafka://localhost:9092',
    autodiscover=False,
    topic_partitions=1,
    # broker_commit_every=100,
    # stream_buffer_maxsize=65536,
)
app.conf.web_port = PORT_AGGREGATOR
topic_raw = app.topic(TOPIC_RAW_TICKS,
key_type=None, 
value_type=Tick, 
value_serializer='json'
)

@app.agent(topic_raw)
async def echo_ticks(ticks: faust.Stream):
    producer = KafkaProducer() 
    n_tx=0
    async for tick in ticks.take(BATCH_SIZE, within=None):  # consider within>0
        
        # Send Ticks to ML topic
        print(f'{n_tx}: {type(tick)}: {tick} has been written')
        producer.send(
            topic=TOPIC_BATCH_TICKS,
            value=faust.serializers.codecs.pickle().dumps(tick)
        )
        n_tx+=BATCH_SIZE