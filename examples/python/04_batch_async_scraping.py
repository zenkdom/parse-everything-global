"""
04_batch_async_scraping.py
Submit multiple URLs for asynchronous background scraping with webhook or polling.
"""

import time
from parse_everything import ParseEverything

client = ParseEverything("pe_live_YOUR_API_KEY")

urls = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://books.toscrape.com"
]

print("Submitting batch job for 3 URLs...")
batch = client.batch(
    target_urls=urls,
    render_js=False,
    country_code="US",
    webhook_url="https://webhook.site/demo-endpoint"
)

batch_id = batch.get("batch_id")
print("Job submitted! Batch ID:", batch_id)

# Poll for results until complete
while True:
    status = client.get_batch_status(batch_id)
    job_status = status.get("job_status")
    progress = status.get("progress_percent", 0.0)
    print(f"Status: {job_status} ({progress:.1f}%)")

    if job_status in ("completed", "failed"):
        print("Completed URLs:", status.get("completed_urls"))
        break
    time.sleep(2)
