from sqlalchemy.orm import Session
from app.core.database import engine, Base
from app.models import product, deal

def init_db():
    Base.metadata.create_all(bind=engine)
