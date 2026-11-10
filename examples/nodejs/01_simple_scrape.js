/**
 * 01_simple_scrape.js
 * Basic scraping with Parse Everything Node.js SDK
 */

const { ParseEverything } = require('../../packages/nodejs/index');

const client = new ParseEverything('pe_live_YOUR_API_KEY');

async function main() {
    try {
        const res = await client.scrape({
            target_url: 'https://example.com',
            country_code: 'US',
            render_js: true
        });

        console.log('Status:', res.status);
        console.log('Page Title:', res.data.page_title);
        console.log('Execution Time:', res.data.execution_time_seconds, 's');
    } catch (err) {
        console.error('Scrape failed:', err.message);
    }
}

main();
