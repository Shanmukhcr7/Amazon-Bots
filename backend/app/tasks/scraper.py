import random
import uuid
from datetime import datetime
from app.core.database import SessionLocal
from app.models.product import Product, PriceHistory
from app.models.deal import Deal
from app.services.analyzer import analyze_deal_with_ai

MOCK_PRODUCTS = [
    {"source_id": "B08N5WRWNW", "name": "Apple MacBook Air M1", "brand": "Apple", "category": "Laptops", "url": "https://amazon.com/dp/B08N5WRWNW", "image_url": "https://m.media-amazon.com/images/I/71jG+e7roXL._AC_SL1500_.jpg", "base_price": 999.0},
    {"source_id": "B09G9FPHY6", "name": "Sony WH-1000XM5 Headphones", "brand": "Sony", "category": "Electronics", "url": "https://amazon.com/dp/B09G9FPHY6", "image_url": "https://m.media-amazon.com/images/I/51aXvjzcukL._AC_SL1000_.jpg", "base_price": 398.0},
]

def scrape_amazon_dummy():
    """
    A dummy scraper task that simulates fetching products from Amazon,
    updating price history, and triggering deal analysis.
    """
    db = SessionLocal()
    try:
        for mock_item in MOCK_PRODUCTS:
            product = db.query(Product).filter(Product.source_id == mock_item["source_id"], Product.source == "amazon").first()
            
            if not product:
                product = Product(
                    source="amazon",
                    source_id=mock_item["source_id"],
                    name=mock_item["name"],
                    brand=mock_item["brand"],
                    category=mock_item["category"],
                    url=mock_item["url"],
                    image_url=mock_item["image_url"]
                )
                db.add(product)
                db.commit()
                db.refresh(product)
                
            # Simulate a current price (maybe a random discount between 0% and 40%)
            discount_percentage = random.uniform(0, 40)
            current_price = round(mock_item["base_price"] * (1 - discount_percentage / 100), 2)
            
            # Record price history
            history = PriceHistory(
                product_id=product.id,
                price=current_price,
                original_price=mock_item["base_price"],
                discount_percentage=discount_percentage,
                availability=True
            )
            db.add(history)
            db.commit()
            
            # Deal Detection Logic
            # If discount is greater than 20%, consider it a potential deal and analyze
            if discount_percentage > 20.0:
                # Calculate simple deal score based on discount
                deal_score = min(100.0, discount_percentage * 2.5) 
                
                # Check if a pending/approved deal already exists recently to avoid spam
                recent_deal = db.query(Deal).filter(Deal.product_id == product.id).order_by(Deal.detected_at.desc()).first()
                if not recent_deal or (datetime.utcnow() - recent_deal.detected_at).total_seconds() > 86400:
                    # AI Analysis
                    analysis = analyze_deal_with_ai(
                        product_name=product.name,
                        product_desc=f"{product.brand} {product.category}",
                        current_price=current_price,
                        original_price=mock_item["base_price"],
                        discount=round(discount_percentage, 2)
                    )
                    
                    is_genuine = analysis.get("is_genuine", False)
                    status = "PUBLISHED" if is_genuine else "REJECTED"
                    
                    deal = Deal(
                        product_id=product.id,
                        deal_score=deal_score,
                        ai_summary=analysis.get("summary", ""),
                        pros=analysis.get("pros", []),
                        cons=analysis.get("cons", []),
                        status=status
                    )
                    
                    if is_genuine:
                        deal.published_at = datetime.utcnow()
                        
                    db.add(deal)
                    db.commit()
                    db.refresh(deal)
                    
                    # Send telegram alert automatically!
                    if is_genuine:
                        from app.services.notifier import send_telegram_alert
                        send_telegram_alert(deal)

    except Exception as e:
        db.rollback()
        print(f"Scraper task failed: {e}")
    finally:
        db.close()
