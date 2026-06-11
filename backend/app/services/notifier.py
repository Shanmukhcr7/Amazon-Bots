import requests
from app.core.config import settings

def send_telegram_alert(deal) -> bool:
    """
    Sends an alert to the Telegram channel.
    """
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        print("Telegram credentials not configured.")
        return False
        
    product = deal.product
    
    # Calculate discount
    if product.price_history:
        latest_price = product.price_history[-1]
        price_text = f"Current Price: ${latest_price.price} (Original: ${latest_price.original_price})"
    else:
        price_text = "Price info missing"
        
    message = (
        f"🔥 **New Deal Alert: {product.name}**\n\n"
        f"Brand: {product.brand}\n"
        f"Category: {product.category}\n"
        f"Deal Score: {deal.deal_score}/100\n\n"
        f"{price_text}\n\n"
        f"**AI Summary:**\n{deal.ai_summary}\n\n"
        f"[View Product]({product.url})"
    )
    
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")
        return False
