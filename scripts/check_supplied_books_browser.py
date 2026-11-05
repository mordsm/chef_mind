"""Exercise source defaults and the compact action bar through the real UI/API."""

import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.config import Settings
from app.db import Base, make_engine
from app.main import create_app
from fastapi.testclient import TestClient
from playwright.sync_api import expect, sync_playwright


def main():
    settings = Settings(_env_file=None, database_url="sqlite+pysqlite:///:memory:", sync_enabled=False)
    engine = make_engine(settings.database_url)
    Base.metadata.create_all(engine)
    with TestClient(create_app(settings, engine)) as client, sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        def serve(route):
            request = route.request
            response = client.request(request.method, urlsplit(request.url).path,
                                      headers={k: v for k, v in request.headers.items() if k == "content-type"},
                                      content=request.post_data)
            route.fulfill(status=response.status_code, body=response.content,
                          headers={k: v for k, v in response.headers.items()
                                   if k not in ("content-length", "transfer-encoding")})

        page.route("http://127.0.0.1:8800/**", serve)
        page.goto("http://127.0.0.1:8800/")
        expect(page.locator("#learning-panel")).not_to_be_visible()
        page.locator("#custom-dish-title").fill("סלק בתנור")
        page.locator("#start-work").click()
        expect(page.locator(".cooking-defaults strong")).to_contain_text("220°C", timeout=30000)
        expect(page.locator(".cooking-defaults strong")).to_contain_text("60")
        page.evaluate("coachCommand('add_step',{step_title:'צלייה בתנור',step_instruction:'בדוק רכות בסכין'})")
        expect(page.locator("#step-continue")).to_have_text("אישור ביצוע")
        expect(page.locator("#step-explain")).to_have_text("הסבר ביצוע")
        expect(page.locator("#step-wait")).to_have_text("בדיקת מוכנות")
        for width in (1440, 900, 390):
            page.set_viewport_size({"width": width, "height": 1000})
            boxes = [page.locator(selector).bounding_box()
                     for selector in ("#step-continue", "#step-explain", "#step-wait")]
            assert all(box and box["height"] >= 48 and box["x"] >= 0
                       and box["x"] + box["width"] <= width for box in boxes), boxes
            assert max(box["y"] for box in boxes) - min(box["y"] for box in boxes) < 2, boxes
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        page.evaluate("mentor.state.context.suggestions=[];renderCoach()")
        expect(page.locator("#suggested-actions")).to_have_count(0)
        page.locator("#step-wait").click()
        expect(page.locator("#current-chef-message")).to_contain_text("סכין")
        frame = page.frame_locator("#action-report-frame")
        frame.locator("#action-pages button").click()
        frame.locator('[data-catalog-action="roast"]').click()
        expect(frame.locator("#number-temperature")).to_have_value("220")
        expect(frame.locator("#number-duration")).to_have_value("60")
        frame.locator("#cancel-report").click()
        frame.locator("#action-pages button").click()
        frame.locator('[data-catalog-action="measure"]').click()
        expect(frame.locator("#number-temperature")).to_have_value("")
        assert not errors, errors
        browser.close()
    print("Passed: defaults, source checks, empty suggestions, 48px action row at 1440/900/390px")


if __name__ == "__main__":
    main()
