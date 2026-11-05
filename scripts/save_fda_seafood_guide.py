"""Save a readable, script-free local copy of the public FDA consumer guide."""
from datetime import date
from hashlib import sha256
from html import escape
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://www.fda.gov/food/buy-store-serve-safe-food/selecting-and-serving-fresh-and-frozen-seafood-safely"
ROOT = Path(__file__).resolve().parents[1]


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        try:
            page = browser.new_page()
            response = page.goto(URL, timeout=45000)
            if response.status != 200:
                raise RuntimeError(f"FDA returned {response.status}; existing snapshot preserved")
            content = page.locator("main").inner_text() if page.locator("main").count() == 1 else page.locator("body").inner_text()
            if not all(term in content for term in ("Selecting and Serving", "Prepare Safely", "Store Properly")):
                raise RuntimeError("FDA article incomplete; existing snapshot preserved")
        finally:
            browser.close()
    destination = ROOT / "vault/Culinary-Knowledge/09_Sources/FDA-Seafood-Consumer-Guide.html"
    document = (
        '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
        '<title>FDA — Seafood consumer guide</title><style>body{max-width:850px;margin:2em auto;padding:1em;font:18px/1.6 system-ui}pre{white-space:pre-wrap}</style>'
        f'<h1>FDA seafood consumer guide</h1><p>Saved {date.today().isoformat()}. '
        f'<a href="{escape(URL)}">Original source</a>. Readable text copy; original images and layout omitted.</p>'
        f'<pre>{escape(content)}</pre></html>'
    )
    destination.write_text(document, encoding="utf-8")
    print(f"Saved complete readable FDA text; sha256={sha256(document.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
