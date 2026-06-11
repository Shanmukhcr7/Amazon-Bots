from fastapi import APIRouter
from app.api.endpoints import products, deals

router = APIRouter()
router.include_router(products.router, prefix="/products", tags=["products"])
router.include_router(deals.router, prefix="/deals", tags=["deals"])
