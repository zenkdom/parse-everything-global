/**
 * 03_batch_scrape.js
 * Asynchronous batch scraping with Node.js SDK
 */

const { ParseEverything } = require('../../packages/nodejs/index');

const client = new ParseEverything('pe_live_9a8b7c6d5e4f3a2b1c0d');

async function main() {
    try {
        console.log('Dispatching batch job...');
        const job = await client.batch([
            'https://example.com',
            'https://httpbin.org/html'
        ]);

        console.log('Batch Job Created. ID:', job.batch_id);

        let completed = false;
        while (!completed) {
            const status = await client.getBatchStatus(job.batch_id);
            console.log(`Progress: ${status.progress_percent}% (State: ${status.job_status})`);

            if (status.job_status === 'completed' || status.job_status === 'failed') {
                completed = true;
                console.log('Finished processing URLs:', status.completed_urls);
            } else {
                await new Promise(r => setTimeout(r, 2000));
            }
        }
    } catch (err) {
        console.error('Batch job error:', err.message);
    }
}

main();
