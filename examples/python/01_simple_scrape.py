"""
01_simple_scrape.py
Basic scraping with Parse Everything Python SDK.
"""

from parse_everything import ParseEverything

# Use your API key or the public sandbox key
API_KEY = "pe_live_YOUR_API_KEY"

client = ParseEverything(api_key=API_KEY)

# Simple scrape with automatic anti-bot detection
response = client.scrape(
    target_url="https://example.com",
    country_code="US",
    render_js=True
)

if response.get("status") == "success":
    data = response["data"]
    print("Page Title:", data.get("page_title"))
    print("HTTP Status:", data.get("http_status"))
    print("Execution Time:", data.get("execution_time_seconds"), "seconds")
    print("Credits Charged:", response.get("credits_charged"))
else:
    print("Error:", response.get("message"))
