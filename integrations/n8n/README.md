# n8n-nodes-parse-everything

n8n Community Node for [Parse Everything](https://parse-everything.com) — Anti-Bot Bypass & Web Extraction API.

Scrape any Cloudflare Turnstile, Akamai, or DataDome protected website directly inside your n8n automation workflows!

---

## 📦 Installation

In your n8n instance:
1. Go to **Settings** > **Community Nodes**.
2. Select **Install**.
3. Enter `n8n-nodes-parse-everything`.
4. Accept the risks and click **Install**.

---

## 🔑 Setup Credentials

1. Go to [parse-everything.com](https://parse-everything.com) and create a free account (1,000 free monthly requests).
2. Copy your API Key (`pe_live_...`).
3. In n8n, create a new credential for **Parse Everything API** and paste your key.

---

## 🚀 How to Publish to npm

```bash
cd AD/07_launches_and_integrations/n8n_node
npm install
npm run build
npm publish --access public
```
