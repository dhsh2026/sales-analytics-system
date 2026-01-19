# utils/api_handler.py

import requests

DUMMYJSON_URL = "https://dummyjson.com/products"

def fetch_all_products():
    """
    Fetches all products from DummyJSON API (up to 100).
    Returns: list of product dictionaries.
    Example item:
      {
        'id': 1,
        'title': 'iPhone 9',
        'category': 'smartphones',
        'brand': 'Apple',
        'price': 549,
        'rating': 4.69,
        ...
      }
    """
    try:
        # limit=100 as your assignment suggests
        response = requests.get(f"{DUMMYJSON_URL}?limit=100", timeout=10)
        response.raise_for_status()  # raises HTTPError for bad status
        data = response.json()
        # API returns {"products": [...], "total": ..., ...}
        products = data.get("products", [])
        print(f"Fetched {len(products)} products from DummyJSON API.")
        return products
    except requests.exceptions.RequestException as e:
        print(f"Error fetching products from API: {e}")
        return []  # return empty list if API fails
