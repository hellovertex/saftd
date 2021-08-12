import pytest

# Just a stub, add your tests below
def test_data():
    assert True

test_data()

# from unittest import TestCase
# from unittest import patch, MagicMock
# #from functools import partial
# from kafka import KafkaConsumer
# class AsyncMock(MagicMock):
#     async def __call__(self, *args, **kwargs):
#         return super().__call__(*args, **kwargs)


# class Tests(TestCase):
    
    
#     @patch('rcvmsg_fn', new_callable=AsyncMock)
#     def test_websocket_client():

#         # test if streaming.data.WebsocketClient.receiveMessage correctly fills kafka topic
#         from streaming.cfg import TOPIC_RAW_TICKS
#         # runs streaming.data.WebsocketClient.receiveMessage in eventloop
#         from streaming.data import main
#         main()
#         consumer = KafkaConsumer(TOPIC_RAW_TICKS)
#         data = consumer.poll()
