from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from .product import ProductResponse

class DealBase(BaseModel):
    product_id: UUID
    deal_score: float
    ai_summary: Optional[str] = None
    pros: Optional[List[str]] = None
    cons: Optional[List[str]] = None
    status: str = "PENDING"

class DealCreate(DealBase):
    pass

class DealUpdate(BaseModel):
    status: Optional[str] = None
    ai_summary: Optional[str] = None
    pros: Optional[List[str]] = None
    cons: Optional[List[str]] = None

class DealResponse(DealBase):
    id: UUID
    detected_at: datetime
    published_at: Optional[datetime] = None
    product: Optional[ProductResponse] = None

    class Config:
        from_attributes = True
