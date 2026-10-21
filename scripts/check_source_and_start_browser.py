"""Exercise source reading, real sign-in, inventory editing and gizzard startup."""

import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.config import Settings
from app.db import Base, make_engine
from app.main import create_app
from fastapi.testclient import TestClient
from playwright.sync_api import expect, sync_playwright

TOKEN = "source-browser-test-token-at-least-24"


def main():
    settings = Settings(
        _env_file=None,
        database_url="sqlite+pysqlite:///:memory:",
        sync_enabled=False,
        api_keys={TOKEN: {"user_id": "owner", "role": "reviewer"}},
    )
    engine = make_engine(settings.database_url)
    Base.metadata.create_all(engine)
    with TestClient(create_app(settings, engine)) as client, sync_playwright() as playwright:
        headers = {"Authorization": "Bearer " + TOKEN}
        assert (
            client.put(
                "/v1/inventory",
                headers=headers,
                json={"items": [{"name": "onion", "quantity": 3, "unit": "pieces"}]},
            ).status_code
            == 200
        )
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        errors, dialogs = [], []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("dialog", lambda dialog: (dialogs.append(dialog.message), dialog.accept()))

        def serve(route):
            request = route.request
            url = urlsplit(request.url)
            response = client.request(
                request.method,
                url.path + ("?" + url.query if url.query else ""),
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
        page.locator('[data-view="knowledge"]').click()
        page.locator("#culinary-sources").locator("..").locator("summary").click()
        source = page.locator("#culinary-source-yaml")
        expect(source).to_have_value(re.compile("preparations:"))
        assert source.get_attribute("readonly") is not None
        page.locator("#culinary-source-select").select_option("domain")
        expect(source).to_have_value(re.compile("archetypes:"))
        expect(page.locator("#culinary-source-status")).to_contain_text("המקור המקורי")

        page.locator('[data-view="cook"]').click()
        page.locator("#open-inventory").click()
        page.locator("#add-item").click()
        page.locator('#inventory [data-field="name"]').fill("אורז")
        page.locator('#inventory [data-field="quantity"]').fill("2")
        page.locator('#inventory [data-field="unit"]').fill("כוסות")
        page.locator("#add-item").click()
        page.locator('#inventory [data-field="name"]').nth(1).fill("עגבניה")
        page.locator('#inventory [data-field="quantity"]').nth(1).fill("3")
        expect(page.locator('[data-ingredient="tomato"] .ingredient-count')).to_have_text("3")
        page.locator('[data-ingredient="tomato"]').click()
        expect(page.locator('[data-ingredient="tomato"] .ingredient-count')).to_have_text("4")
        assert page.locator(".inventory-item").count() == 2
        page.reload()
        page.locator("#open-inventory").click()
        expect(page.locator('#inventory [data-field="name"]').first).to_have_value("אורז")
        expect(page.locator('[data-ingredient="tomato"] .ingredient-count')).to_have_text("4")

        page.locator("#custom-dish-title").fill("קוקבנים")
        page.locator("#start-work").click()
        expect(page.locator("#current-chef-message")).to_contain_text("קורקבנים")
        expect(page.locator("#current-chef-message")).to_contain_text("74")
        expect(page.locator("#status-question")).to_contain_text("מנוקים")
        expect(page.locator("#status-question")).to_contain_text("ברוטב")
        assert not dialogs
        page.locator("#start-work").click()
        expect(page.locator("#start-work")).to_be_enabled()
        assert not dialogs
        page.reload()
        expect(page.locator("#restored-work")).to_contain_text("שוחזרה העבודה הקודמת")
        page.locator("#coach-question").fill("תבשיל רך ברוטב")
        page.locator("#coach-question").press("Enter")
        expect(page.locator("#current-chef-message")).to_contain_text("בחרת תבשיל רך ברוטב")
        expect(page.locator('[data-question-id="goal"]')).to_have_count(0)
        number = page.locator("#choice-method-simmer").get_attribute("data-choice-number")
        page.locator("#coach-question").fill(number)
        page.locator("#coach-ask").click()
        expect(page.locator("#current-chef-message")).to_contain_text("נבחר בישול בנוזל")
        page.locator("#choice-condition-thawed_clean").click()
        expect(page.locator("#current-chef-message")).to_contain_text("מופשרים ומנוקים")
        expect(page.locator(".decision-question")).to_have_count(0)
        page.locator("#new-step-title").fill("הפעולה שלי")
        page.locator("#add-user-step button").click()
        expect(page.locator("#user-step-list")).to_contain_text("הפעולה שלי")
        page.locator("#custom-dish-title").fill("מרק ירקות")
        page.locator("#start-work").click()
        expect(page.locator("#journey-panel")).to_contain_text("מרק ירקות")
        assert len(dialogs) == 1

        page.locator(".connection-details > summary").click()
        page.locator("#token").fill(TOKEN)
        page.locator("#connect-form button").first.click()
        expect(page.locator("#identity")).to_contain_text("owner")
        page.locator("#open-inventory").click()
        expect(page.locator('#inventory [data-field="name"]')).to_have_value("onion")
        expect(page.locator('#inventory [data-field="quantity"]')).to_have_value("3")
        page.locator('#inventory [data-field="quantity"]').fill("4")
        expect(page.locator("#inventory-status")).to_contain_text("מחובר")
        page.locator('[data-view="knowledge"]').click()
        page.locator("#culinary-sources").locator("..").locator("summary").click()
        page.locator("#culinary-source-select").select_option("graph")
        expect(source).to_have_value(re.compile("preparations:"))
        expect(source).to_be_editable()
        page.locator("#culinary-sources input").fill("browser_vegetable")
        page.locator("#culinary-sources textarea").nth(1).fill(
            "name: Browser vegetable\ncategory: vegetables\n"
        )
        page.locator("#culinary-sources button").nth(2).click()
        expect(source).to_have_value(re.compile("browser_vegetable:"))
        page.locator(".connection-details > summary").click()
        page.locator("#disconnect").click()
        expect(source).not_to_have_value(re.compile("browser_vegetable:"))
        assert not errors, errors
        browser.close()
    engine.dispose()
    print(
        "Browser passed: public YAML, automatic selection, inventory persistence, startup guidance, restoration, real sign-in and private editing."
    )


if __name__ == "__main__":
    main()
