from app.models.schemas import OrderBook, Level

def test_orderbook_model():
    ob = OrderBook(symbol="BTC-USDT", exchange="bybit", bids=[Level(price=1, qty=2)], asks=[Level(price=2, qty=3)], depth=1)
    assert ob.symbol == "BTC-USDT"
    assert ob.bids[0].price == 1

