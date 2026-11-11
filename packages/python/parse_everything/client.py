import urllib.request
import urllib.parse
import json
import time
from typing import Optional, Dict, Any, List

class ParseEverythingError(Exception):
    """Base exception for Parse Everything API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

class ParseEverything:
    """
    Client for Parse Everything Web Scraping & Anti-Bot Bypass API.
    
    Usage:
        from parse_everything import ParseEverything
        client = ParseEverything(api_key="pe_live_...")
        res = client.scrape("https://parse-everything.com/demo/cloudflare")
        print(res['data']['page_title'])
    """
    def __init__(self, api_key: str, base_url: str = "https://parse-everything.com"):
        if not api_key:
            raise ValueError("api_key is required. Get 1,000 free credits at https://parse-everything.com")
        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip("/")

    def scrape(
        self,
        target_url: str,
        render_js: bool = True,
        bypass_cloudflare: Optional[bool] = None,
        country_code: str = "US",
        extract_text: bool = False,
        selectors: Optional[Dict[str, str]] = None,
        custom_headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: int = 40,
        method: str = "GET",
        body: Optional[Any] = None,
        post_data: Optional[Any] = None,
        auto_detect: bool = True,
        wait_for_selector: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract web data from any protected target URL.
        Supports GET, POST, PUT, DELETE requests with body forwarding.
        Note: Failed or blocked requests cost 0 credits.
        """
        target_method = (method or "GET").strip().upper()
        target_body = body if body is not None else post_data

        payload = {
            "target_url": target_url,
            "method": target_method,
            "render_js": render_js,

            "auto_detect": auto_detect,
            "country_code": country_code,
            "extract_text": extract_text,
            "timeout": timeout
        }
        if bypass_cloudflare is not None:
            payload["bypass_cloudflare"] = bypass_cloudflare
        if target_body is not None:
            payload["body"] = target_body
        if selectors:
            payload["selectors"] = selectors
        if wait_for_selector:
            payload["wait_for_selector"] = wait_for_selector
        if custom_headers:
            payload["custom_headers"] = custom_headers
        if cookies:
            payload["cookies"] = cookies
        if session_id:
            payload["session_id"] = session_id

        url = f"{self.base_url}/api/v1/extract"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "ParseEverything-PythonSDK/1.1.4"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout + 5) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body_resp = e.read().decode("utf-8", errors="replace")
            try:
                err_json = json.loads(body_resp)
                msg = err_json.get("message") or err_json.get("detail") or str(e)
            except Exception:
                msg = body_resp or str(e)
            raise ParseEverythingError(f"API Error ({e.code}): {msg}", status_code=e.code, response_body=body_resp)
        except Exception as e:
            raise ParseEverythingError(f"Request failed: {str(e)}")

    def get(self, url: str, **kwargs) -> Dict[str, Any]:
        """Convenience helper for GET extraction."""
        return self.scrape(target_url=url, method="GET", **kwargs)

    def post(self, url: str, data: Optional[Any] = None, json_body: Optional[Any] = None, **kwargs) -> Dict[str, Any]:
        """Convenience helper for POST extraction with body forwarding."""
        body = json_body if json_body is not None else data
        return self.scrape(target_url=url, method="POST", body=body, **kwargs)

    def put(self, url: str, data: Optional[Any] = None, json_body: Optional[Any] = None, **kwargs) -> Dict[str, Any]:
        """Convenience helper for PUT extraction with body forwarding."""
        body = json_body if json_body is not None else data
        return self.scrape(target_url=url, method="PUT", body=body, **kwargs)

    def batch(
        self,
        target_urls: List[str],
        render_js: bool = True,
        country_code: str = "US",
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit a batch of up to 100 URLs for background extraction.
        """
        payload = {
            "target_urls": target_urls,
            "render_js": render_js,
            "country_code": country_code
        }
        if webhook_url:
            payload["webhook_url"] = webhook_url

        url = f"{self.base_url}/api/v1/batch"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "ParseEverything-PythonSDK/1.1.4"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise ParseEverythingError(f"Batch Error ({e.code}): {body}", status_code=e.code, response_body=body)

    def get_batch(self, batch_id: str) -> Dict[str, Any]:
        """
        Poll progress and results for a batch job.
        """
        url = f"{self.base_url}/api/v1/batch/{batch_id}"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "ParseEverything-PythonSDK/1.1.4"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise ParseEverythingError(f"Batch poll failed ({e.code}): {body}", status_code=e.code, response_body=body)
