"""
Example: Using ParseEverythingLoader with LangChain for Web-based RAG
"""

import os
from parse_everything_loader import ParseEverythingLoader

API_KEY = os.getenv("PARSE_EVERYTHING_API_KEY", "pe_live_YOUR_API_KEY")

# 1. Load protected web pages with automatic Cloudflare/DataDome bypass
loader = ParseEverythingLoader(
    urls=[
        "https://nopecha.com/demo/cloudflare",
        "https://quotes.toscrape.com"
    ],
    api_key=API_KEY,
    extract_text=True  # Strips HTML tags, saving up to 85% of LLM prompt tokens
)

docs = loader.load()

for doc in docs:
    print("=" * 60)
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Title:  {doc.metadata.get('title')}")
    print(f"Bypassed: {doc.metadata.get('protection_bypassed')}")
    print(f"Content preview:\n{doc.page_content[:250]}...")
