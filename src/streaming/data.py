"""
1. Launch Kafka:
 - $KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties
 - $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties

run via python3 -m faust -A <filename> worker -l info 
consumer1 run via faust -A <filename> worker -l info -p 6066
consumer2 run via faust -A <filename> worker -l info -p 6067
etc...

2. Faust library:
  faust.App.agent: - main processing actor in Faust App
                   - unary async function - receives stream as its argument

  faust.Stream:    - async python generator
                   - abstractions over a kafka topic
                   - can apply operations on the stream (filter(), take(5))

  faust.Record:    - data transfer object: Represents events via python classes inheriting it
                   - serialization, deserialization

From: https://faust.readthedocs.io/en/latest/userguide/settings.html#guide-settings

app configuration:
  broker: - only supported production transport is kafka://,
          - uses the aiokafka client under the hood, for consuming and producing messages
          - can specify multiple hosts, e.g. broker='kafka://kafka1.example.com:9092;kafka2.example.com:9092' [fault tolerance]
  store:  - default is memory://
          - production should use rocksdb://

  processing_guarantee: “at_least_once” (default) and “exactly_once”.
  Note that if exactly-once processing is enabled consumers are configured with isolation.level="read_committed"
  and producers are configured with retries=Integer.MAX_VALUE and enable.idempotence=true per default.
  Note that by default exactly-once processing requires a cluster of at least three brokers what is the recommended setting for production.
  For development you can change this, by adjusting broker setting transaction.state.log.replication.factor to the number of brokers you want to use.

  autodiscover: set to false, see https://faust.readthedocs.io/en/latest/userguide/settings.html#autodiscover
"""
import time
from kafka import KafkaProducer
import websockets
import asyncio
from websockets.client import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosed

# Project imports
from cfg import SOCK_ADDR, TOPIC_RAW_TICKS


class WebSocketClient():

    def __init__(self, sock_addr, **kwargs):
        self.producer = KafkaProducer()
        self.sock_addr = sock_addr

    # need to implement as service when we want to gracefully shutdown

    async def connect(self):
        '''
            returns a WebSocketClientProtocol, used to send and receive messages
        '''
        self.connection = await websockets.client.connect(self.sock_addr)
        if self.connection.open:
            print('Connection stablished. Client correcly connected')
            return self.connection

    async def sendMessage(self, message):
        await self.connection.send(message)

    async def receiveMessage(self, connection: WebSocketClientProtocol):
        while True:
            try:
                msg = await connection.recv()
                # self.producer.send(topic=TOPIC_RAW_TICKS, value=json.dumps(msg))
                self.producer.send(topic=TOPIC_RAW_TICKS, value=f'{msg}'.encode())
                print(msg)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                # gracefully shutdown and restart service
                self.reconnect()

    async def reconnect(self):
        try:
            self.connection.close()                
        except Exception as e:
            print(e)
        time.sleep(5)
        return self.connect()


def main():
    client = WebSocketClient(SOCK_ADDR)
    loop = asyncio.get_event_loop()
    # Start connection and get client connection protocol
    connection = loop.run_until_complete(client.connect())
    # Start listener
    tasks = [
        asyncio.ensure_future(client.receiveMessage(connection)),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
        

if __name__ == '__main__':
    main()
