from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class PriceHistoryBase(BaseModel):
    price: float
    original_price: float
    discount_percentage: float
    availability: bool
    timestamp: datetime

class PriceHistoryResponse(PriceHistoryBase):
    id: UUID
    product_id: UUID

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    source: str
    source_id: str
    name: str
    brand: str
    category: str
    url: str
    image_url: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    price_history: List[PriceHistoryResponse] = []

    class Config:
        from_attributes = True
