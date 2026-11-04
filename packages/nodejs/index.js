/**
 * Parse Everything — Official Node.js SDK
 * https://parse-everything.com
 */

class ParseEverythingError extends Error {
    constructor(message, statusCode = null, responseBody = null) {
        super(message);
        this.name = 'ParseEverythingError';
        this.statusCode = statusCode;
        this.responseBody = responseBody;
    }
}

class ParseEverything {
    /**
     * @param {string} apiKey - Your secret API key (starts with pe_live_)
     * @param {object} [options]
     * @param {string} [options.baseUrl='https://parse-everything.com']
     */
    constructor(apiKey, options = {}) {
        if (!apiKey) {
            throw new Error('API key is required. Get 1,000 free credits at https://parse-everything.com');
        }
        this.apiKey = apiKey.trim();
        this.baseUrl = (options.baseUrl || 'https://parse-everything.com').replace(/\/$/, '');
    }

    /**
     * Scrape a target URL with anti-bot bypass.
     * Failed or blocked requests cost 0 credits.
     * @param {object} params
     * @param {string} params.target_url - Target URL to extract (or params.url)
     * @param {string} [params.method='GET'] - HTTP method: GET, POST, PUT, DELETE
     * @param {any} [params.body] - Request body/payload for POST/PUT
     * @param {boolean} [params.render_js=false] - Execute dynamic JS and wait for DOM
     * @param {boolean} [params.bypass_cloudflare=true]
     * @param {string} [params.country_code='US']
     * @param {boolean} [params.extract_text=false]
     * @param {Record<string, string>} [params.selectors] - CSS selectors
     * @param {number} [params.timeout=40]
     */
    async scrape(params) {
        const targetUrl = params?.target_url || params?.url;
        if (!targetUrl) {
            throw new Error('params.target_url (or params.url) is required');
        }

        const payload = {
            ...params,
            target_url: targetUrl,
            method: (params.method || 'GET').toUpperCase()
        };

        const url = `${this.baseUrl}/api/v1/extract`;
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`,
                'User-Agent': 'ParseEverything-NodeSDK/1.1.0'
            },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const body = await res.text();
            throw new ParseEverythingError(`API Error (${res.status}): ${body}`, res.status, body);
        }

        return await res.json();
    }

    /**
     * Shorthand GET scrape.
     */
    async get(targetUrl, options = {}) {
        return this.scrape({ target_url: targetUrl, method: 'GET', ...options });
    }

    /**
     * Shorthand POST scrape with payload forwarding.
     */
    async post(targetUrl, body = null, options = {}) {
        return this.scrape({ target_url: targetUrl, method: 'POST', body, ...options });
    }

    /**
     * Submit asynchronous batch extraction (up to 100 URLs).
     * @param {string[]} targetUrls
     * @param {object} [options]
     */
    async batch(targetUrls, options = {}) {
        const url = `${this.baseUrl}/api/v1/batch`;
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`,
                'User-Agent': 'ParseEverything-NodeSDK/1.0'
            },
            body: JSON.stringify({
                target_urls: targetUrls,
                ...options
            })
        });

        if (!res.ok) {
            const body = await res.text();
            throw new ParseEverythingError(`Batch Error (${res.status}): ${body}`, res.status, body);
        }

        return await res.json();
    }

    /**
     * Poll status of a batch job.
     * @param {string} batchId
     */
    async getBatch(batchId) {
        const url = `${this.baseUrl}/api/v1/batch/${batchId}`;
        const res = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'User-Agent': 'ParseEverything-NodeSDK/1.0'
            }
        });

        if (!res.ok) {
            const body = await res.text();
            throw new ParseEverythingError(`Batch Poll Error (${res.status}): ${body}`, res.status, body);
        }

        return await res.json();
    }
}

module.exports = { ParseEverything, ParseEverythingError };
