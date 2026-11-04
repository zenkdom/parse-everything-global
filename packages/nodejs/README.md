# parse-everything

Official Node.js and TypeScript client for [Parse Everything](https://parse-everything.com) — Anti-Bot Bypass & Web Scraping API.

Bypass **Cloudflare Turnstile**, **Akamai Bot Manager**, and **DataDome** using authentic browser TLS JA3/JA4 impersonation.

> 🛡️ **Zero Risk Policy:** Failed, blocked, or unreachable requests cost **0 credits**. You only pay for successful extractions (HTTP 200–399).

---

## 📦 Installation

```bash
npm install parse-everything
```

*(Works with Node.js 18+ out of the box with zero external dependencies).*

---

## ⚡ Usage

```javascript
const { ParseEverything } = require('parse-everything');

const client = new ParseEverything('pe_live_YOUR_API_KEY');

async function run() {
    const res = await client.scrape({
        target_url: 'https://nopecha.com/demo/cloudflare',
        bypass_cloudflare: true
    });

    console.log('Status:', res.data.http_status);
    console.log('Title:', res.data.page_title);
    console.log('Engine:', res.engine_used);
}

run();
```

### POST / PUT Request Forwarding (APIs & Web Forms)
```javascript
// Scrape protected POST APIs or submit forms with anti-bot bypass
const postRes = await client.post('https://example.com/api/search', {
    category: 'hardware',
    page: 1
});
console.log('API Status:', postRes.data.http_status);
console.log('Result:', postRes.data.full_html);
```

### TypeScript / ES Modules
```typescript
import { ParseEverything } from 'parse-everything';

const client = new ParseEverything(process.env.PARSE_EVERYTHING_API_KEY!);

const data = await client.scrape({
    target_url: 'https://example.com/items',
    selectors: {
        titles: 'h2',
        prices: '.price'
    }
});
console.log(data.data.selectors_data);
```

---

## 🚀 How to Publish to npm

```bash
cd AD/04_sdks_and_packages/nodejs_npm
npm login
npm publish --access public
```
