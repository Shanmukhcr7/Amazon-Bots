import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Deal(Base):
    __tablename__ = "deals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id"))
    deal_score = Column(Float)
    ai_summary = Column(Text, nullable=True)
    pros = Column(JSON, nullable=True)
    cons = Column(JSON, nullable=True)
    status = Column(String, default="PENDING") # PENDING, APPROVED, REJECTED, PUBLISHED
    detected_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)

    product = relationship("Product", back_populates="deals")
