# Tutorial: Scraping DataDome-Protected Sites in Python

Extracting B2B SaaS reviews, product comparisons, or pricing tiers from sites like **G2**, **Capterra**, or **Ticketmaster** often leads straight into a **403 Forbidden** wall or an interactive DataDome slider challenge.

---

## 1. What Makes DataDome Difficult?

DataDome operates across multiple detection layers:

### A. TLS / JA3 / JA4 Fingerprinting
Before the HTTP request is even processed, the client performs a TLS handshake. Standard Python libraries (`requests`, `httpx`) rely on system OpenSSL, which presents cipher suites in an automated signature order that DataDome flags immediately.

### B. Device & Mouse Telemetry
When rendered in a headless browser, DataDome monitors:
- `navigator.webdriver` flags
- `window.chrome` object bindings
- Cursor movement entropy (linear automated trajectories vs human Bezier curves)
- Missing audio, canvas, or WebGL context values

---

## 2. Extraction with `parse-everything`

The `parse-everything` client handles JA3/JA4 TLS impersonation, challenge clearing, and residential IP routing behind a single API call:

```python
from parse_everything import ParseEverything

client = ParseEverything("pe_live_YOUR_API_KEY")

response = client.scrape(
    target_url="https://www.g2.com/categories/project-management",
    bypass_cloudflare=True,
    country_code="US",
    selectors={
        "products": "div[itemprop='itemListElement'] h3",
        "ratings": ".fw-semibold.text-neutral-80"
    }
)

if response.get("status") == "success":
    print("Extracted Products:", response["data"]["selectors_data"])
```

### Highlights:
- **Zero Local Puppeteer/Chromium Required:** Saves 1.5–2 GB RAM per process.
- **Direct CSS Selectors:** Get clean JSON directly without writing regex or parsing massive DOM trees.
- **Fail-Safe Guarantee:** If blocked, 0 credits are deducted.
