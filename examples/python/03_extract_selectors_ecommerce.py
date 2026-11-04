"""
03_extract_selectors_ecommerce.py
Extracting structured product data from e-commerce catalog pages.
"""

from parse_everything import ParseEverything

client = ParseEverything("pe_live_9a8b7c6d5e4f3a2b1c0d")

response = client.scrape(
    target_url="https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
    selectors={
        "book_titles": "article.product_pod h3 a",
        "prices": "article.product_pod .price_color",
        "in_stock": "article.product_pod .instock.availability"
    }
)

if response.get("status") == "success":
    data = response["data"]["selectors_data"]
    titles = data.get("book_titles", [])
    prices = data.get("prices", [])
    for title, price in zip(titles, prices):
        print(f"Book: {title.strip()} | Price: {price.strip()}")
