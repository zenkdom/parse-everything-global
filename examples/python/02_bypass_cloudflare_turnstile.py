"""
02_bypass_cloudflare_turnstile.py
Bypassing Cloudflare Turnstile & WAF challenge pages.
"""

from parse_everything import ParseEverything

API_KEY = "pe_live_9a8b7c6d5e4f3a2b1c0d"
client = ParseEverything(api_key=API_KEY)

# Scrape a known Cloudflare Turnstile demo page
response = client.scrape(
    target_url="https://nopecha.com/demo/cloudflare",
    bypass_cloudflare=True,
    render_js=True,  # Wait for JS execution and challenge completion
    timeout=45,
    selectors={
        "title": "h1",
        "description": "p"
    }
)

if response.get("status") == "success":
    data = response["data"]
    print("Success!")
    print("Protection Bypassed:", data.get("protection_bypassed"))
    print("Engine Used:", response.get("engine_used"))
    print("Selectors Data:", data.get("selectors_data"))
else:
    print("Scrape failed (0 credits charged):", response.get("message"))
