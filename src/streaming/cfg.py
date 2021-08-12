# WEBSOCKET ADDR TO STREAM DATA FROM, see data.py
SOCK_ADDR = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# Size of chunks that go from kafka topic into ML pipeline, equivalent to batch size in ml training
BATCH_SIZE=10

# Kafka Topics
TOPIC_RAW_TICKS='raw_ticks'
TOPIC_BATCH_TICKS='batch_ticks'
TOPIC_ML='ml'

# Kafka Consumer Ports
PORT_AGGREGATOR  =6066
PORT_DB          =PORT_AGGREGATOR+1
PORT_PREPROCESSOR=PORT_DB+1
PORT_ML          =PORT_PREPROCESSOR+1

# KAFKA CONSUMER GROUP IDS
AGGREGATE_CONSUMER_GROUP_ID='raw_ticks'
DB_CONSUMER_GROUP_ID='db'
PREPROCESS_CONSUMER_GROUP_ID='preprocessor'
ML_CONSUMER_GROUP_ID='ml'


