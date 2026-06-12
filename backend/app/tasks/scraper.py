import os
import random
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from app.core.database import SessionLocal
from app.models.product import Product, PriceHistory
from app.models.deal import Deal
from app.services.analyzer import analyze_deal_with_ai
from app.core.config import settings

# Diverse search keywords to rotate through for finding deals across Amazon
KEYWORDS = [
    "tech deals", "laptop deals", "smart home deals", 
    "kitchen appliance deals", "discount electronics", 
    "gaming accessory deals", "headphones on sale",
    "fitness equipment deals", "mens fashion sale",
    "womens fashion sale", "home decor deals"
]

def clean_price(price_str: str) -> float:
    try:
        # Remove anything that isn't a digit or a period (handles ₹, $, commas)
        clean_str = re.sub(r'[^\d.]', '', price_str)
        return float(clean_str) if clean_str else 0.0
    except Exception:
        return 0.0

def scrape_amazon_dummy():
    """
    Real Amazon Scraper powered by ScraperAPI
    """
    if not settings.SCRAPER_API_KEY:
        print("Missing SCRAPER_API_KEY. Skipping scrape task.")
        return

    # Pick a random keyword to monitor a different category each time
    keyword = random.choice(KEYWORDS).replace(" ", "+")
    
    # Switch to Amazon India to solve shipping/availability issues!
    amazon_url = f"https://www.amazon.in/s?k={keyword}"
    
    payload = {
        'api_key': settings.SCRAPER_API_KEY,
        'url': amazon_url,
        'render': 'true', # Ensures Amazon's JS renders the prices properly
        'country_code': 'in' # Forces ScraperAPI to use an Indian IP so products are available
    }
    
    print(f"Scraping category: {keyword}")
    try:
        response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
        response.raise_for_status()
    except Exception as e:
        print(f"ScraperAPI request failed: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all("div", {"data-component-type": "s-search-result"})
    
    db = SessionLocal()
    try:
        for item in items[:15]: # Process up to 15 products
            asin = item.get("data-asin")
            # Strictly validate the ASIN so links are never broken
            if not asin or len(asin) != 10:
                continue
                
            title_elem = item.find("h2")
            title = title_elem.text.strip() if title_elem else "Unknown Product"
            url = f"https://www.amazon.in/dp/{asin}"
            
            image_elem = item.find("img", {"class": "s-image"})
            image_url = image_elem.get("src") if image_elem else ""

            # Extract Current Price
            price_elem = item.find("span", {"class": "a-price"})
            if not price_elem:
                continue
            
            current_price_str = price_elem.find("span", {"class": "a-offscreen"})
            current_price_str = current_price_str.text if current_price_str else ""
            current_price = clean_price(current_price_str)
            
            if current_price == 0.0:
                continue

            # Extract Original Price (List Price)
            original_price = current_price
            strike_elem = item.find("span", {"class": "a-text-price"})
            if strike_elem:
                offscreen_strike = strike_elem.find("span", {"class": "a-offscreen"})
                if offscreen_strike:
                    original_price = clean_price(offscreen_strike.text)

            # Only process if there is a detected discount
            if original_price <= current_price:
                continue
                
            discount_percentage = ((original_price - current_price) / original_price) * 100

            # 1. Update or Create Product
            product = db.query(Product).filter(Product.source_id == asin, Product.source == "amazon").first()
            if not product:
                product = Product(
                    source="amazon",
                    source_id=asin,
                    name=title,
                    brand="Amazon Search",
                    category=keyword.replace("+", " ").title(),
                    url=url,
                    image_url=image_url
                )
                db.add(product)
                db.commit()
                db.refresh(product)
                
            # 2. Record Price History
            history = PriceHistory(
                product_id=product.id,
                price=current_price,
                original_price=original_price,
                discount_percentage=discount_percentage,
                availability=True
            )
            db.add(history)
            db.commit()
            
            # 3. AI Deal Detection & Telegram Alert
            if discount_percentage > 15.0: # Only analyze if discount is > 15%
                deal_score = min(100.0, discount_percentage * 2.5) 
                
                # Check if we already alerted about this product recently (24 hours)
                recent_deal = db.query(Deal).filter(Deal.product_id == product.id).order_by(Deal.detected_at.desc()).first()
                if not recent_deal or (datetime.utcnow() - recent_deal.detected_at).total_seconds() > 86400:
                    
                    analysis = analyze_deal_with_ai(
                        product_name=product.name,
                        product_desc=f"{product.brand} {product.category}",
                        current_price=current_price,
                        original_price=original_price,
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
                    
                    # Auto-publish to Telegram
                    if is_genuine:
                        from app.services.notifier import send_telegram_alert
                        send_telegram_alert(deal)

    except Exception as e:
        db.rollback()
        print(f"Scraper task failed: {e}")
    finally:
        db.close()
