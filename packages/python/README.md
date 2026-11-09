# Parse Everything — Python SDK

[![PyPI version](https://img.shields.io/badge/pypi-v1.1.0-blue.svg)](https://pypi.org/project/parse-everything/)
[![Free Credits](https://img.shields.io/badge/Free%20Tier-1%2C000%20Requests-green.svg)](https://parse-everything.com)
[![Python Versions](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://pypi.org/project/parse-everything/)

Official lightweight Python client for [Parse Everything](https://parse-everything.com) — Enterprise Web Scraping & Anti-Bot Bypass API.

Effortlessly bypass **Cloudflare Turnstile**, **Cloudflare WAF (403 Forbidden)**, **Akamai Bot Manager**, **DataDome**, and **DDoS-Guard** with authentic TLS JA3/JA4 fingerprint impersonation.

> 🛡️ **Zero Risk Policy:** Failed, blocked, or unreachable requests cost **0 credits**. You only pay for successful extractions (HTTP 200–399).

---

## 🚀 Quick Install

```bash
pip install parse-everything
```

*(Zero heavy browser or binary dependencies required. Uses built-in standard library).*

---

## 🔑 Get Your API Key

Sign up at [parse-everything.com](https://parse-everything.com) to receive **1,000 free API credits** instantly.

---

## 💡 Usage Examples

### 1. Simple Scrape (Bypass Cloudflare Turnstile & WAF)
```python
from parse_everything import ParseEverything

client = ParseEverything(api_key="pe_live_YOUR_API_KEY")

result = client.scrape(
    target_url="https://parse-everything.com/demo/cloudflare",
    auto_detect=True,
    render_js=False  # Handled via ultra-fast TLS impersonation in ~300ms
)

print("HTTP Status:", result["data"]["http_status"])
print("Page Title:", result["data"]["page_title"])
print("Protection Bypassed:", result["data"]["protection_bypassed"])
print("HTML:", result["data"]["full_html"][:200])
```

### 2. Extract Structured Data with CSS Selectors (LLM / RAG Ready)
```python
result = client.scrape(
    target_url="https://example.com/products",
    selectors={
        "titles": "h2.product-title",
        "prices": ".price",
        "links": "a.buy-btn"
    }
)

print(result["data"]["selectors_data"])
```

### 3. Extract Clean Text Only (Save 85% LLM Tokens)
```python
result = client.scrape(
    target_url="https://news-site.com/article",
    extract_text=True
)

print(result["data"]["clean_text"])
```

### 4. POST / PUT Request Forwarding (Scrape Internal APIs & Forms)
```python
# Easily scrape protected POST APIs or submit search forms:
result = client.post(
    url="https://target-store.com/api/v1/search",
    json_body={"category": "electronics", "in_stock": True},
    country_code="US"
)

print("HTTP Status:", result["data"]["http_status"])
print("Payload:", result["data"]["full_html"])
```

### 5. Asynchronous Batch Scraping (Up to 100 URLs)
```python
batch_job = client.batch(
    target_urls=[
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ]
)
print("Batch ID:", batch_job["batch_id"])

# Poll progress
status = client.get_batch(batch_job["batch_id"])
print(f"Status: {status['job_status']} ({status['completed_urls']}/{status['total_urls']})")
```
