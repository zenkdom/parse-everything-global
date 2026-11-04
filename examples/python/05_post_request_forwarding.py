"""
05_post_request_forwarding.py
Forwarding POST / PUT payloads directly to protected targets or internal APIs.
"""

from parse_everything import ParseEverything

client = ParseEverything("pe_live_YOUR_API_KEY")

# Forwarding a JSON POST payload to a protected API endpoint
response = client.scrape(
    target_url="https://httpbin.org/post",
    method="POST",
    body={
        "search_term": "laptops",
        "page": 1,
        "filters": {"brand": "Lenovo"}
    },
    custom_headers={
        "X-Custom-Client": "ParseEverythingSDK"
    }
)

print("HTTP Status:", response["data"]["http_status"])
print("Payload forwarded successfully!")
