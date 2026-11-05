"""Browser regression: family interview, recipe reference and finite operation reports."""

import json
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
        errors, actions = [], []
        page.on("pageerror", lambda error: errors.append(str(error)))

        def serve(route):
            request = route.request
            data = json.loads(request.post_data) if request.post_data else {}
            if "command" in data:
                actions.append(data["command"])
            response = client.request(
                request.method,
                urlsplit(request.url).path,
                headers={k: v for k, v in request.headers.items() if k == "content-type"},
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
        page.locator("#start-by-family").click()
        expect(page.locator("#cooking-intake")).to_contain_text("יש לך מתכון")
        expect(page.locator("#intake-choice-family-meat")).to_be_visible()
        page.locator("#intake-choice-family-meat").click()
        expect(page.locator("#intake-choice-protein-turkey")).to_be_visible()
        page.locator("#intake-choice-protein-turkey").click()
        expect(page.locator("#intake-protein")).to_have_value("turkey")
        expect(page.locator("#cooking-intake")).to_contain_text("איזה נתח")
        page.locator("#intake-cut").fill("ירך חתוכה לקוביות")
        page.locator("#intake-quantity").fill("500 גרם")
        page.locator("#intake-goal").select_option("sauce")
        page.locator("#intake-equipment").select_option("pot")
        page.locator("#intake-method").select_option("boil_simmer")
        page.locator("#intake-source summary").click()
        page.locator("#intake-recipe_url").fill("https://example.com/turkey-stew")
        page.locator("#intake-recipe_text").fill("מתכון לבדיקה ידנית: רשימת מרכיבים וסדר הכנה")
        page.locator('#cooking-intake-form button[type="submit"]').click()
        expect(page.locator("#cooking-intake")).to_contain_text("נשמר לעיון")
        page.locator("#operation-picker>summary").click()
        expect(page.locator("#operation-oven")).to_be_disabled()
        page.locator("#operation-search").fill("בעבוע")
        expect(page.locator("#operation-simmer")).to_be_visible()
        page.locator("#operation-simmer").click()
        expect(page.locator("#selected-operation")).to_contain_text("בעבוע עדין")
        page.locator("#outcome-simmer-vigorous").click()
        expect(page.locator(".operation-reply")).to_contain_text("הנמך")
        page.locator("#operation-search").fill("")
        expect(page.locator("#operation-oven")).to_be_disabled()
        assert actions[-1]["action"] == "report_operation"
        assert actions[-1]["outcome_id"] == "vigorous"
        assert page.evaluate("mentor.state.completed_step_ids.length") == 0
        # Unsubmitted intake text survives an unrelated structured report.
        page.locator("#intake-quantity").fill("600 גרם — טיוטה")
        page.locator("#outcome-simmer-gentle").click()
        expect(page.locator("#intake-quantity")).to_have_value("600 גרם — טיוטה")
        page.reload()
        expect(page.locator("#selected-operation")).to_contain_text("בעבוע עדין")
        expect(page.locator(".operation-reply")).to_contain_text("המשך לעקוב")
        expect(page.locator("#intake-quantity")).to_have_value("500 גרם")
        for width in (1440, 900, 390):
            page.set_viewport_size({"width": width, "height": 1000})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), width
        assert not errors, errors
        browser.close()
    print(
        "Passed: family/subtype interview, missing details, stored recipe reference, structured selection/report, disabled incompatible operations, draft preservation, reload and mobile overflow."
    )


if __name__ == "__main__":
    main()
