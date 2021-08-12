import faust
import numpy as np
#import tensorflow_io as tfio
import tensorflow as tf
pickle_faust = faust.serializers.codecs.pickle()

# Project imports
from cfg import PORT_ML, ML_CONSUMER_GROUP_ID, TOPIC_ML
from modelling.model import mdl


app = faust.App(
    id=ML_CONSUMER_GROUP_ID,
    broker='kafka://localhost:9092',
    autodiscover=False,
    topic_partitions=1,
    # broker_commit_every=100,
    # stream_buffer_maxsize=65536,
)
app.conf.web_port = PORT_ML
topic_ml = app.topic(TOPIC_ML,
key_type=None, 
# value_type=BatchTicks, 
value_serializer='raw'  
)

@app.agent(topic_ml)
async def echo_train_data(batches: faust.Stream):
    n_tx = 0
    async for k,v in batches.items():    
        label = tf.reshape(
            tensor=tf.convert_to_tensor(pickle_faust.loads(k), dtype=tf.int8),
            shape=[1, -1])
        data = tf.reshape(
            tensor=tf.convert_to_tensor(pickle_faust.loads(v), dtype=tf.float32), 
            shape=[1, -1])
        #print(f'echo from ML: batch = {label, data}')
        n_tx += 1
        #print(data.shape, label.shape)
        print(f'fitting model on live-dataset: {data} and label {label}')
        # mdl.fit(x=data, y=label)


# online_train_ds = tfio.experimental.streaming.KafkaGroupIODataset(
#     topics=[TOPIC_ML],
#     group_id=KAFKA_CONSUMER_GROUP_ID,
#     servers="127.0.0.1:9092",
#     stream_timeout=-1, # in milliseconds, to block indefinitely, set it to -1.
#     message_poll_timeout=3000,
#     configuration=[
#         "session.timeout.ms=120000",
#         "max.poll.interval.ms=120000",  # max allowed time between calls to consume, after that a rebalance is initiated
#         "auto.offset.reset=earliest"
#         #"enable.auto.offset.store=false"
#     ],
# )
# for (msg, key) in online_train_ds:
#   print(msg)
#   a=1

# for (message, key) in online_train_ds:
#   label = tf.Tensor(pickle_faust.loads(key.numpy()))
#   data = tf.Tensor(pickle_faust.loads(message.numpy()))
#   print(label, data)
#   a=1
#   model.fit(x=data,y=label,epochs=2)
# #   break
# # exit(0)