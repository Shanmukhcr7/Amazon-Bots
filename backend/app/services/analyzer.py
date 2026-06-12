from openai import OpenAI
from app.core.config import settings
import json

client = OpenAI(
  base_url=settings.NVIDIA_BASE_URL,
  api_key=settings.NVIDIA_API_KEY
)

def analyze_deal_with_ai(product_name: str, product_desc: str, current_price: float, original_price: float, discount: float) -> dict:
    """
    Uses NVIDIA's Llama 3.3 70B Instruct model to analyze a deal and return a structured summary.
    """
    prompt = f"""
    Analyze the following product deal from Amazon India:
    Product Name: {product_name}
    Description: {product_desc}
    Current Price: ₹{current_price} INR
    Original Price: ₹{original_price} INR
    Discount: {discount}%

    Is this likely a genuine and good deal for a consumer in India? 
    CRITICAL WARNING: Amazon sellers frequently inflate the 'Original Price' (MSRP) to make a normal price look like a massive discount. If you suspect this is a 'fake discount' and the current price is actually the normal everyday price (or even a price hike), you MUST mark "is_genuine": false.
    
    Please return ONLY a JSON object with the following keys:
    - "is_genuine" (boolean)
    - "summary" (string: a short explanation of the deal and whether it's worth it)
    - "pros" (list of strings: pros of the product/deal)
    - "cons" (list of strings: cons or reasons to be cautious)
    """

    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )
        
        response_text = completion.choices[0].message.content.strip()
        # Clean up in case the model returns markdown like ```json ... ```
        if response_text.startswith("```json"):
            response_text = response_text[7:-3]
        elif response_text.startswith("```"):
            response_text = response_text[3:-3]
            
        return json.loads(response_text.strip())
        
    except Exception as e:
        print(f"Error calling NVIDIA AI: {e}")
        return {
            "is_genuine": False,
            "summary": "AI Analysis failed.",
            "pros": [],
            "cons": []
        }
