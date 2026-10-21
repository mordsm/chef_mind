"""Focused UI checks for the requested duplicate guidance, icons and problem rules."""

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
            response = client.request(
                request.method,
                urlsplit(request.url).path,
                headers={k: v for k, v in request.headers.items() if k in ("authorization", "content-type")},
                content=request.post_data,
            )
            route.fulfill(
                status=response.status_code,
                body=response.content,
                headers={
                    k: v
                    for k, v in response.headers.items()
                    if k not in ("content-length", "transfer-encoding")
                },
            )

        page.route("http://127.0.0.1:8800/**", serve)
        page.goto("http://127.0.0.1:8800/")
        page.locator("#custom-dish-title").fill("קוקבנים")
        page.locator("#start-work").click()
        expect(page.locator("#active-work-guidance")).to_contain_text("לפני שמתחילים")
        text = page.locator("#active-work-guidance").inner_text()
        assert text.count("לפני שמתחילים בדוק") == 1
        assert text.count("סף הבישול הכללי") == 1
        assert "ולא כבד" not in text and "זוהו קורקבנים" not in text
        assert page.get_by_role("button", name="יש בעיה", exact=True).count() == 1
        page.locator("#open-inventory").click()
        for key in ("eggplant", "zucchini", "ground beef", "chicken"):
            icon = page.locator(f'[data-ingredient="{key}"]')
            expect(icon).to_be_visible()
            icon.click()
            expect(icon.locator(".ingredient-count")).to_have_text("1")
        assert page.locator(".inventory-item").count() == 4
        page.locator("#coach-problem").click()
        expect(page.locator("#problem-chooser")).to_be_visible()
        page.locator("#problem-too_thick").click()
        expect(page.locator("#current-chef-message")).to_contain_text("מעט נוזל")
        assert page.locator("#active-work-guidance").inner_text().count("מעט נוזל") == 1
        page.locator("#problem-too_dry").click()
        expect(page.locator(".missing-rule-alert")).to_be_visible()
        expect(page.locator("#current-chef-message")).to_contain_text("too_dry")
        page.set_viewport_size({"width": 390, "height": 844})
        page.locator("#edit-missing-rule").click()
        expect(page.locator("#problem-rules-yaml")).to_have_value(__import__("re").compile("too_thick:"))
        assert page.locator("#problem-rules-yaml").get_attribute("readonly") is not None
        assert not errors, errors
        browser.close()
    engine.dispose()
    print(
        "Passed: single guidance/safety text, no identification preamble, one problem button, four inventory icons, matched/missing rule responses and rule editor link."
    )


if __name__ == "__main__":
    main()
