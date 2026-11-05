"""Browser-based HTTPS health probe for Windows installations with restricted TLS clients."""

import json
import sys
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

url = sys.argv[1].rstrip("/")
parsed = urlsplit(url)
if parsed.scheme != "https" or not (parsed.hostname or "").endswith((".workers.dev", ".trycloudflare.com")) or parsed.username or parsed.password or parsed.path or parsed.query or parsed.fragment:
    raise SystemExit("Expected the public Chef Cloudflare origin")
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel="msedge", headless=True)
    try:
        page = browser.new_page()
        response = page.goto(url + "/health", timeout=20000)
        payload = json.loads(page.locator("body").inner_text())
        healthy = response.status == 200 and payload.get("service") == "chef-core"
        if parsed.hostname.endswith(".workers.dev"):
            healthy = healthy and response.headers.get("x-chef-gateway") == "permanent"
    finally:
        browser.close()
raise SystemExit(0 if healthy else 1)
