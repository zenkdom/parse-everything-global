# Hacker News Launch Kit (Show HN)

> **The Hacker News Playbook:**  
> HN readers reject superficial marketing slogans. They appreciate **deep technical details, protocol breakdowns, honest engineering trade-offs, and transparent pricing**.  
> A well-crafted Show HN post can easily hit the front page and drive **thousands of targeted developers**.

---

### 1. Title Options
- `Show HN: Parse Everything – Anti-bot bypass API via TLS JA3/JA4 browser impersonation`
- `Show HN: Parse Everything – Bypassing Cloudflare Turnstile without heavy headless Chromium`

**URL:** `https://parse-everything.com`

---

### 2. Founder's First Comment (Post immediately after submitting):

```markdown
Hey HN, I'm the creator of Parse Everything (https://parse-everything.com).

For the past couple of years, web scraping has turned into an escalating arms race. The old playbook of spinning up Puppeteer/Selenium in a Docker container (like FlareSolverr) is fundamentally broken for three reasons:

1. **Memory & CPU Bloat:** A single headless Chromium instance easily eats 1.2–1.8 GB of RAM and takes 6–12 seconds to boot, resolve challenges, and extract DOM. Scaling this to thousands of URLs gets absurdly expensive.
2. **CDP Fingerprinting:** Modern Cloudflare Turnstile and DataDome actively detect runtime bindings left behind by the Chrome DevTools Protocol (`Runtime.enable`, execution context delays, and missing audio/webgl entropy).
3. **TLS JA3/JA4 Handshakes:** Python's `requests` or `urllib3` compile against system OpenSSL. The cipher suite preference and TLS extension permutation in the `Client Hello` packet is a dead giveaway that immediately triggers an HTTP 403 before a single byte of HTML is served.

### What we built differently:

Instead of launching heavy browsers on every request, we built a hybrid engine:

- **Protocol-Level TLS Impersonation:** We use custom BoringSSL bindings via `curl_cffi` to match Google Chrome 120+ byte-for-byte at the socket level. We replicate Chrome's exact cipher suite ordering, supported groups, elliptic curves, and HTTP/2 pseudo-header order (`:method`, `:authority`, `:scheme`, `:path`), as well as `SETTINGS` frame values (`SETTINGS_HEADER_TABLE_SIZE: 65536`, `SETTINGS_INITIAL_WINDOW_SIZE: 6291456`).
- **The Result on Speed:** About 85% of Cloudflare-protected targets drop their 403 shields and serve raw HTML in **250–400ms** without needing a browser engine at all.
- **Stealth Headless Fallback:** For targets with aggressive interactive challenges (Turnstile checkbox clicks, DataDome slider telemetry), we route requests to an ephemeral cluster running a stealth Playwright engine with CDP patches completely removed at the C++ level and human-like Bezier mouse curves.
- **Batch Processing & HMAC Webhooks:** You can submit up to 100 URLs in a single async POST call, and our queue dispatches completed payloads to your webhook with an HMAC-SHA256 signature.

### Pricing philosophy:
We got frustrated with legacy scraping APIs that advertise "100k requests for $49", but then hit you with a **25x credit multiplier** as soon as you toggle anti-bot or residential proxies (turning 100k credits into just 4,000 real URLs). Furthermore, if a page returns a 403 or fails, they still deduct credits.

We operate on two strict guarantees:
1. **1:1 Flat Credit Model:** 1 URL = 1 credit.
2. **100% Free Failures:** Blocked or failed requests cost **0 credits**.

There is a permanent free tier with 1,000 credits/month upon sign-up (no credit card required) if you want to benchmark your toughest targets against it.

GitHub Repository & SDKs:  
https://github.com/zenkdom/parse-everything-global

I'd love to hear your feedback on latency, edge cases where your scrapers still get stuck, or general thoughts on where the anti-bot ecosystem is heading!
```
