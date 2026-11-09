# Release v1.1.2 — Unified Auto-Detect Anti-Bot Engine & Modernized SDKs

**Tag:** `v1.1.2`  
**Date:** November 2026  
**Target:** API Backend, Python SDK (PyPI), Node.js SDK (npm), PHP Client (Packagist), Documentation & Examples

---

## 🚀 Summary of Changes

In this release, all documentation, SDK interfaces, and code examples have been upgraded to the modern **Unified `auto_detect` Engine**. The legacy `bypass_cloudflare` and `bypass_akamai` parameters have been officially deprecated in favor of an autonomous anti-bot detection and escalation pipeline.

### 1. Autonomous Anti-Bot Engine (`auto_detect: true`)
- **Zero Configuration Needed:** You no longer need to know which anti-bot provider protects a website before making a request. The engine autonomously detects Cloudflare (Turnstile, Managed Challenge, WAF 5s Shield), Akamai BMP, DataDome, PerimeterX / HUMAN, and DDoS-Guard.
- **Two-Stage Intelligent Escalation:**
  1. *Sub-300ms TLS Fast-Path:* Simulates authentic Google Chrome 120+ JA3/JA4 fingerprints and HTTP/2 pseudo-header frames via `curl_cffi`.
  2. *Headless Stealth Escalation:* If an interactive Turnstile or CAPTCHA challenge is detected, the request automatically escalates to a stealth browser cluster with Turnstile solving.
- **Anti-Bot Clearance Sessions (`use_session: true`):**
  - Solved `cf_clearance` cookies and session credentials are systematically cached and reused for subsequent queries against the same domain, slashing latency down to **0.1s – 0.3s**.

### 2. 100% Backward Compatibility Guaranteed
- The API backend continues to accept `bypass_cloudflare` (and `bypass_akamai`) without errors. Existing client scripts, Zapier webhooks, and legacy integrations will continue to function seamlessly.

---

## 📦 Client SDK Updates (v1.1.2)

### Python SDK (`pip install parse-everything>=1.1.2`)
- `bypass_cloudflare` is now optional (`None` by default) and will not be sent unless explicitly passed.
- `auto_detect: bool = True` is the standard anti-bot resolution path.
```python
from parse_everything import ParseEverything

client = ParseEverything("pe_live_YOUR_API_KEY")
res = client.scrape(
    target_url="https://example.com/protected",
    auto_detect=True,  # Default: automatically solves Cloudflare, Akamai, DataDome
    selectors={"title": "h1"}
)
print(res["data"]["http_status"], res["data"]["page_title"])
```

### Node.js / TypeScript SDK (`npm install parse-everything@1.1.2`)
- Updated TypeScript types (`index.d.ts`) marking `bypass_cloudflare` as `@deprecated`.
- Native type support for `auto_detect?: boolean`.
```javascript
const { ParseEverything } = require('parse-everything');
const client = new ParseEverything('pe_live_YOUR_API_KEY');

const res = await client.scrape({
    target_url: 'https://example.com/protected',
    auto_detect: true
});
console.log(res.data.page_title);
```

### PHP SDK (`composer require parse-everything/client:^1.1.2`)
- Updated usage examples and documentation to reflect `auto_detect`.
```php
use ParseEverything\Client;

$client = new Client('pe_live_YOUR_API_KEY');
$res = $client->scrape([
    'target_url' => 'https://example.com/protected',
    'auto_detect' => true
]);
echo $res['data']['page_title'];
```

---

## 📝 Updated Documentation & Tutorials
- **`README.md`**: All quickstarts and SDK snippets now use `auto_detect: true`.
- **API Reference**: `POST /api/v1/extract` and GET query parameter samples standardized.
- **Guides & Articles**: Updated Habr tutorial, Zillow Turnstile walkthrough, and Reddit/HN launch kits.
- **RapidAPI OpenAPI Spec**: `rapidapi_openapi.json` examples refreshed.
