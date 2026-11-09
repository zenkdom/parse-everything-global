# LangChain Document Loader for Parse Everything

Load web pages cleanly into your LangChain & LlamaIndex RAG pipelines, automatically bypassing Cloudflare Turnstile, Akamai, and DataDome.

## Features

- **Anti-Bot Immune:** Extracts content behind Cloudflare Turnstile, WAF, and DataDome.
- **RAG-Optimized:** Strips scripts, ads, and boilerplate — returns clean semantic markdown/text.
- **Zero Heavy Dependencies:** Direct HTTP integration, no local Chromium or Selenium required.

## Installation

```bash
pip install langchain parse-everything
```

## Quick Start

```python
from parse_everything_loader import ParseEverythingLoader

# Load protected URLs directly into LangChain Documents
loader = ParseEverythingLoader(
    urls=[
        "https://nopecha.com/demo/cloudflare",
        "https://news.ycombinator.com"
    ],
    api_key="pe_live_YOUR_KEY",
    extract_text=True,
    auto_detect=True
)

docs = loader.load()

for doc in docs:
    print(f"URL: {doc.metadata['source']}")
    print(f"Title: {doc.metadata.get('page_title')}")
    print(f"Content preview: {doc.page_content[:200]}...\n")
```

## Vector Store Ingestion Example

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from parse_everything_loader import ParseEverythingLoader

# 1. Load protected web page
loader = ParseEverythingLoader(
    urls=["https://target-portal.com/knowledgebase"],
    api_key="pe_live_YOUR_KEY",
    extract_text=True
)
docs = loader.load()

# 2. Split and index
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
print(f"Indexed {len(splits)} chunks into Chroma DB.")
```
