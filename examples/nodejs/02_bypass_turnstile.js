/**
 * 02_bypass_turnstile.js
 * Bypass Cloudflare Turnstile challenge using Node.js SDK
 */

const { ParseEverything } = require('../../packages/nodejs/index');

const client = new ParseEverything('pe_live_YOUR_API_KEY');

async function main() {
    try {
        const res = await client.scrape({
            target_url: 'https://nopecha.com/demo/cloudflare',
            bypass_cloudflare: true,
            render_js: true,
            selectors: {
                title: 'h1',
                desc: 'p'
            }
        });

        console.log('Protection Bypassed:', res.data.protection_bypassed);
        console.log('Selectors Result:', res.data.selectors_data);
    } catch (err) {
        console.error('Error:', err.message);
    }
}

main();
