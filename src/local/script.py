import numpy as np
# from functools import partial
import pandas as pd
import pickle
from collections import namedtuple
# mock_assign_label=partial(np.random.binomial,n=1,p=.5,size=1)
# print(mock_assign_label())

# Tick = namedtuple('Tick',['a', 'p','q'])
# chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# batch = [Tick(chars[i], i/10, i) for i in range(5)]
with open('pickledbatch', 'rb') as f:
    batch = pickle.load(f)

arr = np.array(batch)[:3]
#print(np.frompyfunc(lambda tick: tick.p, 1,1)(arr))
prices = np.frompyfunc(lambda tick: tick.p, 1,1)(arr)
quantities = np.frompyfunc(lambda tick: tick.q, 1,1)(arr)
buyer_ids = np.frompyfunc(lambda tick: tick.b, 1,1)(arr)
seller_ids = np.frompyfunc(lambda tick: tick.a, 1,1)(arr)
ismaker = np.frompyfunc(lambda tick: tick.m, 1,1)(arr).astype(int)
arr2 = np.concatenate([prices, quantities, buyer_ids, seller_ids, ismaker])
print(arr2)
print(len(arr2))