"""Focused verification of method restrictions and submitting a dictated report."""

import json
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


def main():
    settings = Settings(_env_file=None, database_url="sqlite+pysqlite:///:memory:", sync_enabled=False)
    engine = make_engine(settings.database_url)
    Base.metadata.create_all(engine)
    with TestClient(create_app(settings, engine)) as client, sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        errors, reports = [], []
        failure = {"enabled": True}
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.add_init_script("""
            window.SpeechRecognition=class {
                start(){window.testRecognizer=this;this.onstart();}
                abort(){this.onend();}
            };
            Object.defineProperty(window,'speechSynthesis',{value:{cancel(){},getVoices(){return []}},configurable:true});
        """)

        def serve(route):
            request = route.request
            data = json.loads(request.post_data) if request.post_data else {}
            if data.get("command", {}).get("action") == "report":
                reports.append(data["command"]["message"])
                if failure["enabled"]:
                    route.fulfill(
                        status=503, content_type="application/json", body='{"code":"STORAGE_UNAVAILABLE"}'
                    )
                    return
            response = client.request(
                request.method,
                urlsplit(request.url).path,
                headers={k: v for k, v in request.headers.items() if k in ("content-type", "authorization")},
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
        expect(page.locator('#custom-method option[value="boil_simmer"]')).to_have_count(1)
        assert page.locator('#custom-method option[value="oven_roast"]').count() == 0
        assert page.locator('#custom-method option[value="pan_sear"]').count() == 0
        page.locator("#method-policy-info summary").click()
        expect(page.locator("#method-policy-info")).to_contain_text("עשיר בקולגן")
        page.locator("#custom-method").select_option("boil_simmer")
        page.locator("#start-work").click()
        expect(page.locator("#work-report")).to_be_visible()
        page.locator("#work-report-dictate").click()
        page.evaluate(
            "testRecognizer.onresult({results:[Object.assign([{transcript:'הוספתי נוזלים'}],{isFinal:true})]})"
        )
        expect(page.locator("#work-report")).to_have_value("הוספתי נוזלים")
        page.locator('#user-report-form button[type="submit"]').click()
        expect(page.locator("#work-report-status")).to_have_class("error")
        expect(page.locator("#work-report")).to_have_value("הוספתי נוזלים")
        expect(page.locator("#voice-input")).to_have_attribute("aria-pressed", "false")
        failure["enabled"] = False
        page.locator('#user-report-form button[type="submit"]').click()
        expect(page.locator("#work-report-status")).to_contain_text("הדיווח התקבל אצל השף")
        expect(page.locator("#work-report")).to_have_value("")
        expect(page.locator("#current-chef-message")).to_contain_text("הדיווח התקבל: הוספתי נוזלים")
        assert reports == ["הוספתי נוזלים", "הוספתי נוזלים"]
        page.locator('[data-view="knowledge"]').click()
        page.locator("#method-policy-editor > summary").click()
        expect(page.locator("#method-policy-yaml")).to_have_value(re.compile("gizzards"))
        assert page.locator("#method-policy-yaml").get_attribute("readonly") is not None
        page.locator("#culinary-engine-editor > summary").click()
        expect(page.locator("#culinary-engine-yaml")).to_have_value(re.compile("dense_collagen_lean"))
        assert page.locator("#culinary-engine-yaml").get_attribute("readonly") is not None
        page.locator("#culinary-engine-editor select").select_option("registry")
        expect(page.locator("#culinary-engine-yaml")).to_have_value(re.compile("chicken_gizzard"))
        assert not errors, errors
        browser.close()
    engine.dispose()
    print(
        "Passed: configured-only method dropdown, exclusion reasons, policy editor, dictated report submit/failure preservation/retry/acknowledgement."
    )


if __name__ == "__main__":
    main()
