import faust
from kafka import KafkaProducer
from typing import List
import numpy as np
import pandas as pd
pickle_faust = faust.serializers.codecs.pickle()

# Project imports
from cfg import PORT_PREPROCESSOR, TOPIC_BATCH_TICKS, PREPROCESS_CONSUMER_GROUP_ID, TOPIC_ML
from modelling.tick import Tick
from modelling.transform import mock_assign_label, mock_transform

# class BatchTicks(faust.Record):
#     batch: List[Tick]

# class OnlineDataset(faust.Record):
#     labels: np.ndarray
#     data: np.ndarray

app = faust.App(
    id=PREPROCESS_CONSUMER_GROUP_ID,
    broker='kafka://localhost:9092',
    autodiscover=False,
    topic_partitions=1,
    # broker_commit_every=100,
    # stream_buffer_maxsize=65536,
)
app.conf.web_port = PORT_PREPROCESSOR
topic_batch = app.topic(TOPIC_BATCH_TICKS,
key_type=None, 
# value_type=BatchTicks, 
value_serializer='raw'  
)


@app.agent(topic_batch)
async def echo_batches(batches: faust.Stream):
    prod = KafkaProducer()
    async for batch in batches:
        # mock preprocessing and labelling
        batch=pickle_faust.loads(batch)
        label = mock_assign_label(batch)
        print(f'echo from app 2 that wrote to ml topic: {label}')
        
        # send to new kafka topic
        prod.send(topic=TOPIC_ML,
        value=faust.serializers.codecs.pickle().dumps(mock_transform(batch)),
        key=faust.serializers.codecs.pickle().dumps(label))
