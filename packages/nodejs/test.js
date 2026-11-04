const assert = require('assert');
const { ParseEverything, ParseEverythingError } = require('./index');

console.log('Testing ParseEverything Node.js SDK...');

const client = new ParseEverything('pe_live_test_key_123');
assert.strictEqual(client.apiKey, 'pe_live_test_key_123');
assert.strictEqual(client.baseUrl, 'https://parse-everything.com');

assert.throws(() => {
    new ParseEverything('');
}, /API key is required/);

console.log('All Node.js SDK local unit tests passed successfully!');
