from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
from concurrent.futures import ThreadPoolExecutor
import json

@dataclass
class Product:
    name: str
    price: float
    website: str
    url: str
    size: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    in_stock: bool = True
    shipping_time: Optional[int] = None
    return_policy: Optional[str] = None

# Global variables (former class attributes)
WEBSITES = ['amazon.com', 'walmart.com', 'target.com', 'ebay.com', 'flipkart.com']
PROMO_CODES = {
    'SAVE10': 0.10,
    'SUMMER20': 0.20,
    'FLASH30': 0.30,
    'FIRSTORDER': 0.15
}

def get_user_agent():
    """Create and return a new UserAgent instance."""
    return UserAgent()

def clean_url(url: str, site: str) -> str:
    """Clean and validate product URLs."""
    if not url:
        return ''
        
    if not url.startswith(('http://', 'https://')):
        url = f'https://www.{site}{url if url.startswith("/") else "/" + url}'
    
    return url

def clean_price(price_str: str) -> float:
    """Extract and clean price from string."""
    try:
        price_str = re.sub(r'[^\d.]', '', re.sub(r'[^\d.,]', '', price_str))
        return float(price_str)
    except (ValueError, TypeError):
        return 0.0

def matches_filters(product: Product, filters: Optional[Dict] = None) -> bool:
    """Check if product matches given filters."""
    if not filters:
        return True
        
    for key, value in filters.items():
        if key == 'max_price' and product.price > value:
            return False
        if key == 'min_price' and product.price < value:
            return False
        if key == 'size' and product.size != value:
            return False
        if key == 'color' and product.color != value:
            return False
    return True

def search_site(site: str, query: str, filters: Dict = None) -> List[Product]:
    """Search a single site for products."""
    headers = {'User-Agent': get_user_agent().random}
    search_query_url_tag = {
        "amazon.com": "s?k=", 
        "walmart.com": "search?q=", 
        "target.com": "s?searchTerm=", 
        "ebay.com" :"sch/i.html?_nkw=", 
        "flipkart.com": "search?q="
    }
    search_url = f"https://www.{site}/{search_query_url_tag[site]}{query.replace(' ', '+')}"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        selectors = {
            'amazon.com': {
                'container': 's-result-item',
                'title': 'a-text-normal',
                'price': 'a-price-whole',
                'url': 'a.a-link-normal'
            },
            'walmart.com': {
                'container': 'search-result-product',
                'title': 'product-title-link',
                'price': 'price-main',
                'url': 'product-title-link'
            }
        }
        
        site_selectors = selectors.get(site)
        if not site_selectors:
            return []
            
        products = []
        for item in soup.find_all(class_=site_selectors['container']):
            try:
                name_elem = item.find(class_=site_selectors['title'])
                price_elem = item.find(class_=site_selectors['price'])
                url_elem = item.find(site_selectors['url'])
                
                if name_elem and price_elem and url_elem:
                    price_text = price_elem.text.strip()
                    price = clean_price(price_text)
                    
                    if price > 0:
                        product = Product(
                            name=name_elem.text.strip(),
                            price=price,
                            website=site,
                            url=clean_url(url_elem.get('href'), site),
                            in_stock=True
                        )
                        
                        if matches_filters(product, filters):
                            products.append(product)
            
            except Exception as e:
                continue
                
        return products[:5]
        
    except requests.RequestException as e:
        print(f"Error searching {site}: {str(e)}")
        return []

def search_products(query: str, filters: Dict = None) -> List[Product]:
    """Search for products across multiple e-commerce sites."""
    with ThreadPoolExecutor(max_workers=len(WEBSITES)) as executor:
        all_results = list(executor.map(
            lambda site: search_site(site, query, filters), 
            WEBSITES
        ))
    
    products = []
    for result in all_results:
        products.extend(result)
    
    products.sort(key=lambda x: x.price)
    return products

def estimate_shipping(product: Product, zip_code: str, target_date: Optional[datetime] = None) -> Dict:
    """Estimate shipping time and cost."""
    shipping_options = {
        'standard': {
            'cost': 5.99,
            'days': 5,
            'carrier': 'USPS'
        },
        'expedited': {
            'cost': 12.99,
            'days': 2,
            'carrier': 'FedEx'
        },
        'overnight': {
            'cost': 24.99,
            'days': 1,
            'carrier': 'UPS'
        }
    }
    
    if target_date:
        days_needed = (target_date - datetime.now()).days
        available_options = {
            key: value for key, value in shipping_options.items()
            if value['days'] <= days_needed
        }
        return {
            'available_options': available_options,
            'meets_deadline': len(available_options) > 0,
            'cheapest_option': min(available_options.items(), key=lambda x: x[1]['cost']) if available_options else None
        }
    
    return {'available_options': shipping_options}

def check_promo(code: str, base_price: float) -> Dict:
    """Validate and calculate discounted price."""
    code = code.upper()
    if code in PROMO_CODES:
        discount = PROMO_CODES[code]
        final_price = base_price * (1 - discount)
        return {
            'valid': True,
            'discount_percentage': discount * 100,
            'original_price': base_price,
            'final_price': final_price,
            'savings': base_price - final_price
        }
    return {
        'valid': False,
        'message': 'Invalid promo code'
    }

def compare_prices(product_name: str) -> List[Dict]:
    """Compare prices across different stores."""
    products = search_products(product_name)
    return sorted([{
        'store': p.website,
        'price': p.price,
        'url': p.url,
        'in_stock': p.in_stock
    } for p in products], key=lambda x: x['price'])

def get_return_policy(website: str) -> Dict:
    """Get return policy details for a store."""
    return_policies = {
        'amazon.com': {
            'window': '30 days',
            'free_returns': True,
            'conditions': 'Items must be unused and in original packaging',
            'process': 'Initiate through your account or contact customer service'
        },
        'walmart.com': {
            'window': '90 days',
            'free_returns': True,
            'conditions': 'Receipt required, items must be unused',
            'process': 'Return to store or ship back with provided label'
        }
    }
    
    return return_policies.get(website, {
        'window': 'Policy not found',
        'free_returns': None,
        'conditions': 'Please check store website',
        'process': 'Contact store customer service'
    })