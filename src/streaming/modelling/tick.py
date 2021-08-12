import faust

class Tick(faust.Record):
    """
        "e": "trade",     // Event type
        "E": 123456789,   // Event time
        "s": "BNBBTC",    // Symbol
        "t": 12345,       // Trade ID
        "p": "0.001",     // Price
        "q": "100",       // Quantity
        "b": 88,          // Buyer order ID
        "a": 50,          // Seller order ID
        "T": 123456785,   // Trade time
        "m": true,        // Is the buyer the market maker?
        "M": true         // ignore
    """
    e: str                  # event_type
    E: int                  # event_time
    s: str                  # symbol
    t: int                  # trade_id
    p: float                # price
    q: float                # quantity
    b: int                  # buyer_order_id
    a: int                  # seller_order_id
    T: int                  # trade time
    m: bool                 # is_market_maker
    M: bool                 # ignore

