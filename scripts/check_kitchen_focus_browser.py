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
        expect(page.locator("#active-work-guidance .book-knowledge-tip").first).to_be_visible()
        expect(page.locator("#active-work-guidance")).not_to_contain_text("McGee")
        expect(page.locator("#active-work-guidance")).not_to_contain_text("The Food Lab")
        expect(page.locator("#active-work-guidance")).not_to_contain_text("חומציות וריכוך ירקות")
        expect(page.locator("#custom-start")).to_be_visible()
        assert page.locator("#cook textarea:visible").count() == 1
        assert page.locator(".decision-question:visible").count() >= 2
        chef = page.locator('#companion-panel').bounding_box()
        action = page.locator('#journey-panel').bounding_box()
        suggestions = page.locator('#learning-panel').bounding_box()
        assert suggestions['x'] < action['x'] < chef['x']
        assert max(chef['y'], action['y'], suggestions['y']) - min(chef['y'], action['y'], suggestions['y']) < 2
        expect(page.locator("#coach-problem")).to_be_visible()
        for width in (1440, 900, 390):
            page.set_viewport_size({"width": width, "height": 1000})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), width
            assert page.locator("#work-report-dictate").bounding_box()["height"] >= 56
        page.set_viewport_size({"width": 1440, "height": 1000})
        page.locator("#work-report-dictate").click()
        expect(page.locator("#kitchen-stop-voice")).to_be_visible()
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
        page.locator("#composer-ask").click()
        page.locator("#work-report").fill("When should I add salt?")
        page.locator('#user-report-form button[type="submit"]').click()
        expect(page.locator("#work-report")).to_have_value("")
        page.locator("#user-timer-start").click()
        expect(page.locator("#coach-clock")).not_to_have_text("00:00")
        page.locator("#kitchen-timer-stop").click()
        expect(page.locator("#coach-clock")).to_have_text("00:00")
        page.locator("#kitchen-plan").evaluate("node => node.open = true")
        page.locator("#new-step-title").fill("Prepare ingredients")
        page.locator('#add-user-step button[type="submit"]').click()
        expect(page.locator(".user-step-card.selected")).to_be_visible()
        page.locator("#composer-report").click()
        page.locator("#work-report").fill("draft preserved across refresh")
        page.locator("#user-timer-start").click()
        expect(page.locator("#work-report")).to_have_value("draft preserved across refresh")
        assert page.locator("#user-report-form").count() == 1
        assert page.locator("#cook textarea:visible").count() == 1
        page.screenshot(path=".test-tmp/kitchen-focus-desktop.png",full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        page.screenshot(path=".test-tmp/kitchen-focus-mobile.png",full_page=True)
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
        page.evaluate("localStorage.removeItem('chef-coach-guest-v1')")
        page.reload()
        page.locator('#custom-dish-title').fill('סלמון')
        expect(page.locator('#custom-method option[value="steam"]')).to_have_count(1)
        page.locator('#start-work').click()
        expect(page.locator('#cooking-path-choices button')).to_have_count(3)
        expect(page.locator('#current-chef-message')).to_contain_text('עצמות')
        page.locator('#start-path-salmon_oven_roast').click()
        expect(page.locator('#choice-salmon_condition-thawed')).to_be_visible()
        page.locator('#choice-salmon_condition-thawed').click()
        page.locator('#choice-salmon_cut-fillets').click()
        page.locator('#choice-salmon_thickness-thin').click()
        page.locator('#choice-salmon_style-open').click()
        page.locator('#choice-salmon_flavor-herbs').click()
        expect(page.locator('#current-chef-message')).to_contain_text('180°C')
        expect(page.locator('.guidance-links a')).to_have_count(2)
        page.locator('#step-wait').click()
        expect(page.locator('#current-chef-message')).to_contain_text('לפני המשך')
        page.locator('#step-continue').click()
        expect(page.locator('#current-chef-message')).to_contain_text('שום')
        page.set_viewport_size({'width':390,'height':844})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        expect(page.locator('#step-explain')).to_be_visible()
        assert not errors, errors
        browser.close()
    engine.dispose()
    print(
        "Passed: three-column RTL workbench, visible setup and choices, single composer, responsive layout, voice stop indicator, failed-send preservation, question routing, timer start/cancel, plan editing, salmon choices and draft persistence."
    )


if __name__ == "__main__":
    main()
