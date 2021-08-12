"""
1. Launch Kafka:
 - $KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties
 - $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties

run via faust -A <filename> worker -l info

2. Faust library:
  faust.App.agent: - main processing actor in Faust App
"""

import faust
from datetime import datetime
from kafka import KafkaProducer


# Project imports
from cfg import PORT_DB, TOPIC_RAW_TICKS,DB_CONSUMER_GROUP_ID
from modelling.tick import Tick

# todo: serialize incoming data and write to database
DB_MAX_ROWS = 1e6
ECHO_BUFFER_SIZE=100



app = faust.App(
    id=DB_CONSUMER_GROUP_ID,
    broker='kafka://localhost:9092',
    autodiscover=False,
    topic_partitions=1,
    # broker_commit_every=100,
    # stream_buffer_maxsize=65536,
)
app.conf.web_port = PORT_DB
topic_raw = app.topic(TOPIC_RAW_TICKS,
key_type=None, 
value_type=Tick, 
value_serializer='json'
)

def db_stuff():
    # implement your database logic here
    pass

@app.agent(topic_raw)
async def echo_ticks(ticks: faust.Stream):
    n_tx = 0
    producer = KafkaProducer()
    async for tick in ticks.take(ECHO_BUFFER_SIZE, within=None):  # consider within>0
        
        # Write Ticks to database
        db_stuff()
        print(f'DATABASE {n_tx}: {type(tick)}: {tick} has been written to database')
        n_tx += ECHO_BUFFER_SIZE
        

# ts=0
# try:
#     date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#     print(date)
# except Exception:
#     date = datetime.utcfromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S')
#     print(date)
# n_tx = 0
# nn_tx = 0
