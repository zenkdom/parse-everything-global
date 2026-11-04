# Tutorial: How to Bypass Cloudflare Turnstile on Protected Sites in Python

Targeting sites protected by **Cloudflare Turnstile** (Zillow, NopeCHA, OpenAI, crypto exchanges) often results in 403 Forbidden errors or endless challenge loops when using standard Python libraries like `requests`, `httpx`, or `urllib3`.

This tutorial explains why this happens and demonstrates how to bypass Turnstile with the `parse-everything` client in a few lines of code.

---

## 1. Why Standard Requests Fail

When you fetch a Turnstile-protected page with standard Python:

1. **TCP/TLS Handshake Inspection (JA4):** Cloudflare evaluates the cipher suite order and TLS extension permutation in your client's `Client Hello` packet against known browser signatures.
2. **HTTP/2 Frame Fingerprinting:** Cloudflare verifies frame priority, initial window size, and header casing.
3. **Turnstile Interstitial:** If any anomaly is detected, an interactive or invisible challenge is rendered, requiring a valid `cf_clearance` cookie before granting access.

---

## 2. Solution: Using the `parse-everything` SDK

Instead of maintaining proxy rotators and heavyweight Chromium containers, use the `parse-everything` Python SDK:

```bash
pip install parse-everything
```

```python
from parse_everything import ParseEverything

# Initialize client (1,000 free monthly credits at https://parse-everything.com)
client = ParseEverything("pe_live_YOUR_API_KEY")

# Extract data directly from a Turnstile protected site
response = client.scrape(
    target_url="https://nopecha.com/demo/cloudflare",
    bypass_cloudflare=True,
    render_js=True,  # Wait for JS challenge resolution
    selectors={
        "heading": "h1",
        "description": "p",
        "badge": ".badge"
    }
)

if response.get("status") == "success":
    data = response["data"]
    print("Page Title:", data.get("page_title"))
    print("Protection Bypassed:", data.get("protection_bypassed"))
    print("Extracted Data:", data.get("selectors_data"))
else:
    print("Failed (0 credits charged):", response.get("message"))
```

### Key Advantages:
- **Zero Heavy Binaries:** Pure Python standard library under the hood.
- **100% Free Failures:** Failed or blocked requests cost 0 credits.
- **Fast Execution:** Protocol-level TLS impersonation finishes in ~300ms when interactive challenge solving is not needed.
