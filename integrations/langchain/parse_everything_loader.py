"""
Parse Everything Document Loader for LangChain & LlamaIndex
Extracts clean, unblocked web content from Cloudflare, Akamai, and DataDome protected sites.
"""

from typing import List, Optional, Dict, Any
import requests

try:
    from langchain_core.document_loaders import BaseLoader
    from langchain_core.documents import Document
except ImportError:
    # Minimal standalone fallback if langchain is not installed
    class BaseLoader:
        pass

    class Document:
        def __init__(self, page_content: str, metadata: Optional[Dict[str, Any]] = None):
            self.page_content = page_content
            self.metadata = metadata or {}

        def __repr__(self):
            return f"Document(page_content='{self.page_content[:40]}...', metadata={self.metadata})"

class ParseEverythingLoader(BaseLoader):
    """
    Load web pages using the Parse Everything Anti-Bot Bypass API.
    
    Example:
        loader = ParseEverythingLoader(
            urls=["https://nopecha.com/demo/cloudflare", "https://example.com"],
            api_key="pe_live_...",
            extract_text=True
        )
        docs = loader.load()
        print(docs[0].page_content)
    """

    def __init__(
        self,
        urls: List[str],
        api_key: str,
        extract_text: bool = True,
        render_js: bool = False,
        bypass_cloudflare: bool = True,
        country_code: str = "US",
        base_url: str = "https://parse-everything.com",
        method: str = "GET",
        body: Optional[Any] = None
    ):
        if not api_key:
            raise ValueError("api_key is required. Get free credits at https://parse-everything.com")
        self.urls = urls if isinstance(urls, list) else [urls]
        self.api_key = api_key
        self.extract_text = extract_text
        self.render_js = render_js
        self.bypass_cloudflare = bypass_cloudflare
        self.country_code = country_code
        self.base_url = base_url.rstrip("/")
        self.method = method
        self.body = body

    def load(self) -> List[Document]:
        documents = []
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        for url in self.urls:
            payload = {
                "target_url": url,
                "method": self.method,
                "extract_text": self.extract_text,
                "render_js": self.render_js,
                "bypass_cloudflare": self.bypass_cloudflare,
                "country_code": self.country_code
            }
            if self.body is not None:
                payload["body"] = self.body

            try:
                resp = requests.post(
                    f"{self.base_url}/api/v1/extract",
                    json=payload,
                    headers=headers,
                    timeout=60
                )
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    content = data.get("clean_text") if self.extract_text else data.get("full_html", "")
                    meta = {
                        "source": url,
                        "title": data.get("page_title", ""),
                        "status_code": data.get("http_status", 200),
                        "protection_bypassed": data.get("protection_bypassed", "none"),
                        "execution_time": data.get("execution_time_seconds", 0.0)
                    }
                    documents.append(Document(page_content=content or "", metadata=meta))
                else:
                    documents.append(Document(
                        page_content="",
                        metadata={"source": url, "error": f"HTTP {resp.status_code}", "body": resp.text}
                    ))
            except Exception as e:
                documents.append(Document(
                    page_content="",
                    metadata={"source": url, "error": str(e)}
                ))

        return documents
