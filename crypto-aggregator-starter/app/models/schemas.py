from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List
from datetime import datetime, timezone

class Level(BaseModel):
    price: Decimal
    qty: Decimal

class OrderBook(BaseModel):
    symbol: str
    exchange: str
    ts: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    bids: List[Level] = Field(default_factory=list)
    asks: List[Level] = Field(default_factory=list)
    depth: int = 50

class CombinedOrderBook(BaseModel):
    symbol: str
    ts: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    bids: List[Level]
    asks: List[Level]

