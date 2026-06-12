import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SCRAPER_API_KEY")

def test_scraper():
    keyword = "laptop+deals"
    amazon_url = f"https://www.amazon.com/s?k={keyword}"
    
    payload = {
        'api_key': API_KEY,
        'url': amazon_url,
        'render': 'true' # important for amazon JS pages
    }
    
    print("Fetching via ScraperAPI...")
    response = requests.get('http://api.scraperapi.com', params=payload)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
        
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Amazon search result items
    items = soup.find_all("div", {"data-component-type": "s-search-result"})
    print(f"Found {len(items)} products.")
    
    for item in items[:3]:
        asin = item.get("data-asin")
        title_elem = item.find("h2")
        title = title_elem.text.strip() if title_elem else "Unknown"
        
        price_elem = item.find("span", {"class": "a-price"})
        price = price_elem.find("span", {"class": "a-offscreen"}).text if price_elem and price_elem.find("span", {"class": "a-offscreen"}) else "N/A"
        
        print(f"ASIN: {asin} | Price: {price} | Title: {title[:50]}...")

if __name__ == "__main__":
    test_scraper()
