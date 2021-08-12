from cfg import BATCH_SIZE
import numpy as np
from typing import List

# Project imports
from modelling.tick import Tick
from cfg import BATCH_SIZE

NUM_COLUMNS=len(['p','q','b','s','m']) * BATCH_SIZE
# mock preprocessing
def mock_transform(batch: List[Tick]):
    arr = np.array(batch)
    # Fast conversion from List[Tick] to np.ndarray(5*BATCH_SIZE,)
    prices = np.frompyfunc(lambda tick: tick.p, 1,1)(arr)
    quantities = np.frompyfunc(lambda tick: tick.q, 1,1)(arr)
    buyer_ids = np.frompyfunc(lambda tick: tick.b, 1,1)(arr)
    seller_ids = np.frompyfunc(lambda tick: tick.a, 1,1)(arr)
    ismaker = np.frompyfunc(lambda tick: tick.m, 1,1)(arr).astype(int)
    return np.concatenate(
        [prices, quantities, buyer_ids, seller_ids, ismaker])

# mock labelling
def mock_assign_label(batch):
    return np.random.binomial(n=1,p=.5,size=1)[0]