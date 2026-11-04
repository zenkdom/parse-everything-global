<div align="center">

# ⚡ Parse Everything — Enterprise Anti-Bot Bypass API & Web Extraction Engine

**Bypass Cloudflare Turnstile, Cloudflare WAF, Akamai Bot Manager, and DataDome at wire speed.**  
Powered by real **TLS JA3/JA4 browser fingerprint impersonation**, **Playwright stealth execution**, **Batch processing**, and **HMAC-SHA256 Webhooks**.

[![PyPI version](https://img.shields.io/badge/pypi-v1.1.1-blue.svg?logo=pypi)](https://pypi.org/project/parse-everything/)
[![npm version](https://img.shields.io/badge/npm-v1.1.1-red.svg?logo=npm)](https://www.npmjs.com/package/parse-everything)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-brightgreen.svg?logo=python)](https://python.org)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg?logo=node.js)](https://nodejs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Free Tier](https://img.shields.io/badge/Free_Tier-1%2C000_Credits%2Fmo-purple.svg)](https://parse-everything.com)

[**Website & Live Dashboard**](https://parse-everything.com) • [**Python SDK**](#1-python-sdk) • [**Node.js SDK**](#2-nodejs--typescript-sdk) • [**cURL Quickstart**](#3-curl--rest-api) • [**Use Cases**](#-common-developer-use-cases)

</div>

---

## ⚡ The Problem: Why Scrapers Fail in 2026

Modern anti-bot systems (Cloudflare 2026 Turnstile, Akamai Bot Manager, DataDome) no longer just inspect HTTP headers. Over **80% of blocks occur before HTML is even transmitted**:

1. **TLS / JA3 / JA4 Fingerprinting:** Python `requests`, `urllib3`, Go `http.Client`, and Node.js `axios` use standard OpenSSL/cryptolib handshakes. Cloudflare inspects the exact order of cipher suites, elliptic curves, and extension hashes, flagging you instantly.
2. **The "FlareSolverr Trap":** Running headless Chromium instances consumes **1.5 GB to 3 GB of RAM per worker**, crashes under load, leaks memory, and is increasingly caught by Cloudflare's CDP (Chrome DevTools Protocol) runtime timing heuristics.
3. **Credit Multiplier Traps:** Typical scraping APIs advertise cheap credits, but charge **20x to 50x multipliers** when residential proxies or JavaScript rendering are enabled. Worse: **they charge you full price even if the extraction fails or gets blocked**.

---

## 💡 The Solution: How Parse Everything Works

Parse Everything uses a high-performance **hybrid extraction architecture**:

```
 ┌──────────────────────────────────────────────────────────────┐
 │                Target URL Request (GET/POST)                 │
 └──────────────────────────────┬───────────────────────────────┘
                                │
                 Is it protected by Anti-Bot?
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼ (Fast Path ~300ms)                            ▼ (Interactive Fallback)
┌────────────────────────────────┐            ┌───────────────────────────────────┐
│  BoringSSL / JA3/JA4 Emulation │            │  Playwright Stealth Cluster       │
│  - Real Chrome 120+ TLS/HTTP/2 │            │  - Solves interactive Turnstile   │
│  - Spoofed H2 frame order      │            │  - Human mouse & slider movements │
│  - Bypasses 85% of shields     │            │  - Zero CDP runtime leaks         │
└────────────────┬───────────────┘            └─────────────────┬─────────────────┘
                 │                                              │
                 └──────────────────────┬───────────────────────┘
                                        ▼
               ┌─────────────────────────────────────────────────┐
               │  Parsed Output (HTML, CSS Selectors, Clean Text)│
               │  + 100% Free Failures (0 credits if blocked!)   │
               └─────────────────────────────────────────────────┘
```

1. **Wire-Speed TLS / JA3 / JA4 Impersonation:** Emulates authentic Chrome 120+, Safari 15+, and Firefox HTTP/2 and TLS signatures via custom BoringSSL handshakes. Bypasses Cloudflare WAF, Akamai, and DataDome in **~300ms without spinning up a heavy browser**.
2. **Stealth Headless Fallback:** If a target page requires an interactive challenge (Turnstile checkbox click, DataDome puzzle), requests seamlessly route to an isolated stealth browser pool that passes the challenge and captures the clearance cookies.
3. **🛡️ 100% Free Failures (Zero-Risk Guarantee):** If a scrape fails, gets blocked, or returns a 4xx/5xx from the target, **you are charged exactly 0 credits**. You only pay for successful 200-OK extractions.
4. **Strict 1:1 Pricing:** No sneaky 25x multipliers. 1 target URL = 1 credit.

---

## 📊 Feature Comparison

| Feature | FlareSolverr | ScrapingBee | ZenRows | **Parse Everything** |
| :--- | :---: | :---: | :---: | :---: |
| **Cloudflare Turnstile (2026)** | ❌ Often Breaks | ✅ Supported | ✅ Supported | **✅ Instant Bypass** |
| **Akamai & DataDome** | ❌ Blocked | ⚠️ 25x Credit Cost | ⚠️ 20x Credit Cost | **✅ Supported (1 credit)** |
| **RAM per Worker** | ~2 GB | Cloud | Cloud | **Cloud / ~30MB Local SDK** |
| **Latency** | 6–15 seconds | 4–10 seconds | 3–8 seconds | **~300ms (TLS fast-path)** |
| **Failed Scrape Cost** | N/A (Self-hosted) | Full Price | Full Price | **🛡️ 0 Credits (100% Free)** |
| **Credit Multiplier** | Free (Self-host) | 5x–25x | 10x–30x | **1:1 Flat (No surprise fee)** |
| **POST / Payload Forwarding** | ❌ Limited | ⚠️ Complex | ⚠️ Complex | **✅ Full (GET, POST, PUT, DEL)** |
| **LLM & RAG Ready Mode** | ❌ Raw only | ❌ Extra plugin | ❌ Raw only | **✅ Auto Text / Markdown Clean** |
| **Free Monthly Tier** | DIY | 1,000 calls (once) | 1,000 calls (once) | **🎁 1,000 calls / month recurring** |

---

## 🚀 Quick Start

### 1. Python SDK

Zero external dependencies (uses standard library under the hood). Works with Python 3.8+.

```bash
pip install parse-everything
```

```python
from parse_everything import ParseEverything

# Initialize with your API key (get 1,000 free credits at https://parse-everything.com)
client = ParseEverything("pe_live_9a8b7c6d5e4f3a2b1c0d")

# 1. Scrape a Cloudflare Turnstile protected site
res = client.scrape(
    target_url="https://nopecha.com/demo/cloudflare",
    bypass_cloudflare=True,
    selectors={
        "heading": "h1",
        "description": "p"
    }
)

print("HTTP Status:", res["data"]["http_status"])
print("Protection Bypassed:", res["data"]["protection_bypassed"])
print("Extracted Data:", res["data"]["selectors_data"])
```

### 2. Node.js / TypeScript SDK

Native `fetch` support with full TypeScript definitions (`index.d.ts`).

```bash
npm install parse-everything
```

```typescript
import { ParseEverything } from 'parse-everything';

const client = new ParseEverything('pe_live_9a8b7c6d5e4f3a2b1c0d');

async function run() {
  const result = await client.scrape({
    target_url: 'https://nopecha.com/demo/cloudflare',
    bypass_cloudflare: true,
    extract_text: true
  });

  console.log('Status:', result.data.http_status);
  console.log('Clean Content:', result.data.cleaned_text);
}

run();
```

### 3. cURL / REST API

Ideal for scripts, terminal pipelines, Docker containers, n8n, Zapier, or Make.

#### Simple GET Request
```bash
curl "https://parse-everything.com/api/v1/extract?target_url=https://example.com" \
     -H "Authorization: Bearer pe_live_9a8b7c6d5e4f3a2b1c0d"
```

#### Advanced POST Request (with Selectors & Anti-Bot Bypass)
```bash
curl -X POST "https://parse-everything.com/api/v1/extract" \
     -H "Authorization: Bearer pe_live_9a8b7c6d5e4f3a2b1c0d" \
     -H "Content-Type: application/json" \
     -d '{
       "target_url": "https://nopecha.com/demo/cloudflare",
       "bypass_cloudflare": true,
       "country_code": "US",
       "selectors": {
         "title": "h1",
         "button": ".challenge-btn"
       }
     }'
```

---

## 🌟 Killer Features

### 1. Forwarding POST / PUT Payloads to Protected APIs
Need to submit a login form, query a search engine, or query an internal GraphQL/REST endpoint that sits behind Cloudflare? Forward the payload directly:

```python
response = client.scrape(
    target_url="https://target-store.com/api/v2/search",
    method="POST",
    body={
        "query": "mechanical keyboard",
        "in_stock_only": True
    },
    custom_headers={"X-Requested-With": "XMLHttpRequest"}
)
```

### 2. AI & RAG Pipeline Extraction
Stop wasting tokens sending 200 KB of navigation bars, SVG icons, and tracking scripts to your LLMs. Enable `extract_text: true` to get clean, semantic text ready for vector embeddings:

```python
res = client.scrape(
    target_url="https://news.ycombinator.com",
    extract_text=True
)
# Returns clean plain text / markdown representation
clean_text = res["data"]["cleaned_text"]
```

### 3. Asynchronous Batch Scraping (up to 100 URLs)
Process large URL queues without keeping hundreds of client connections open:

```python
batch_job = client.batch(
    target_urls=[
        "https://example.com/item/1",
        "https://example.com/item/2",
        "https://example.com/item/3"
    ],
    webhook_url="https://your-server.com/api/webhook"
)

print("Batch ID:", batch_job["batch_id"])

# Poll status or wait for Webhook callback
status = client.get_batch_status(batch_job["batch_id"])
print("Progress:", status["progress_percent"])
```

### 4. HMAC-SHA256 Signed Webhooks
Receive push notifications the moment your batch extraction completes. All payloads are cryptographically signed with HMAC-SHA256 in the `X-Parse-Signature` header so you can verify integrity:

```http
POST /api/webhook HTTP/1.1
Host: your-server.com
X-Parse-Signature: sha256=d41d8cd98f00b204e9800998ecf8427e...
X-Parse-Event: batch.completed
Content-Type: application/json

{
  "event": "batch.completed",
  "batch_id": "batch_98124b81c",
  "total_urls": 3,
  "successful": 3,
  "results": [...]
}
```

---

## 📦 Packages & Ecosystem

| Package / Integration | Platform | Install Command / Directory | Status |
| :--- | :--- | :--- | :--- |
| **`parse-everything`** | **PyPI** (Python) | `pip install parse-everything` ([`packages/python`](packages/python)) | Stable |
| **`parse-everything`** | **npm** (Node.js/TS) | `npm install parse-everything` ([`packages/nodejs`](packages/nodejs)) | Stable |
| **LangChain DocumentLoader** | **Python** | [LangChain Integration Guide](integrations/langchain) | Ready |
| **n8n Community Node** | **n8n** | [n8n Node Guide](integrations/n8n) | Ready |
| **OpenAPI 3.0 Spec** | **REST / Swagger** | [`openapi.json`](openapi.json) | Production |

*(Note: The PHP client and backend services are maintained in a separate repository).*

---

## 💡 Common Developer Use Cases

Parse Everything solves the headache of maintaining brittle scraping setups across common developer workflows:

- **FlareSolverr Drop-in Replacement:** Replace crashing FlareSolverr Docker containers on low-spec VPS with a lightweight API call.
- **RAG & AI Ingestion:** Scrape documentation sites, knowledgebases, and protected portals to feed vector databases (LangChain / LlamaIndex / Chroma).
- **Price Monitoring & Arbitrage:** Scrape e-commerce portals that enforce strict TLS JA3 checks (Amazon, Walmart, BestBuy, Zillow).
- **No-Code Automation:** Seamless workflow triggers in n8n, Make, and Zapier via direct REST endpoints and HMAC webhooks.

---

## 🎁 Free Tier & Instant Testing

Every account receives **1,000 free requests every single month**, no credit card required.

1. Create a free account at [https://parse-everything.com](https://parse-everything.com).
2. Copy your secret API key from the dashboard.
3. Start scraping!

**Interactive Demo Key:**  
For quick offline testing and local sandbox verification, the public sandbox key is:
```text
pe_live_9a8b7c6d5e4f3a2b1c0d
```

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).
Parse Everything API & Services © 2026.
