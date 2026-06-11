from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.deal import Deal
from app.schemas.deal import DealResponse, DealUpdate
from app.services.notifier import send_telegram_alert

router = APIRouter()

@router.get("/", response_model=List[DealResponse])
def read_deals(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: str = None
) -> Any:
    query = db.query(Deal)
    if status:
        query = query.filter(Deal.status == status)
    deals = query.offset(skip).limit(limit).all()
    return deals

@router.put("/{deal_id}", response_model=DealResponse)
def update_deal(
    deal_id: str,
    deal_in: DealUpdate,
    db: Session = Depends(get_db),
) -> Any:
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    update_data = deal_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(deal, field, value)
    
    db.commit()
    db.refresh(deal)
    
    # If approved, publish via Telegram
    if update_data.get("status") == "APPROVED":
        send_telegram_alert(deal)
        
    return deal
