"""Browser integration against the real FastAPI workflow and an isolated SQLite database."""

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

TOKEN = "synthetic-coach-owner-token-only-12345"


def main():
    settings = Settings(
        _env_file=None,
        database_url="sqlite+pysqlite:///:memory:",
        sync_enabled=False,
        api_keys={TOKEN: {"user_id": "synthetic-owner", "role": "reviewer"}},
    )
    engine = make_engine(settings.database_url)
    Base.metadata.create_all(engine)
    with TestClient(create_app(settings, engine)) as client, sync_playwright() as playwright:
        headers = {"Authorization": "Bearer " + TOKEN}
        client.post(
            "/v1/chef/respond",
            headers=headers,
            json={
                "cooking_id": "historical-inventory",
                "message": "onion",
                "state": {"current_goal": "Old dinner"},
                "inventory": [
                    {"name": "onion", "quantity": 4, "unit": "pieces"},
                    {"name": "rice", "quantity": 2, "unit": "cups"},
                ],
            },
        )
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        errors, calls = [], []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("dialog", lambda dialog: dialog.accept())
        page.add_init_script("""
            Object.defineProperty(crypto,'randomUUID',{value:undefined});
            window.testSpoken=[];Object.defineProperty(window,'speechSynthesis',{value:{cancel(){},getVoices(){return [{lang:'he-IL',localService:true}]},speak(item){testSpoken.push(item.text)}},configurable:true});
            window.SpeechSynthesisUtterance=function(text){this.text=text;};
            window.SpeechRecognition=class {start(){window.testRecognizer=this;this.onstart();}abort(){} };
        """)

        def serve(route):
            request = route.request
            path = urlsplit(request.url).path
            calls.append((request.method, path))
            response = client.request(
                request.method,
                path,
                headers={
                    key: value
                    for key, value in request.headers.items()
                    if key in ("authorization", "content-type")
                },
                content=request.post_data,
            )
            route.fulfill(
                status=response.status_code,
                body=response.content,
                headers={
                    key: value
                    for key, value in response.headers.items()
                    if key not in ("content-length", "transfer-encoding")
                },
            )

        page.route("http://127.0.0.1:8800/**", serve)
        page.goto("http://127.0.0.1:8800/")
        page.locator(".optional-journeys").evaluate("node=>node.open=true")
        expect(page.locator("#dish-shakshuka")).to_be_visible()
        expect(page.locator("#coach-mode")).to_contain_text("בישול מקומי")
        page.locator("#dish-shakshuka").click()
        expect(page.locator(".current-step h3")).to_have_text("הכנת חומרי הגלם")
        page.locator("#coach-done").click()
        expect(page.locator(".current-step h3")).to_have_text("הכנת חומרי הגלם")
        page.locator('[data-answer="ready"]').click()
        page.locator("#coach-done").click()
        expect(page.locator(".current-step h3")).to_have_text("טיגון הבצל")
        page.locator('[data-answer="white"]').click()
        page.locator("#coach-done").click()
        expect(page.locator(".current-step h3")).to_have_text("טיגון הבצל")
        page.locator('[data-answer="golden"]').click()
        expect(page.locator("#learning-panel")).to_contain_text("טעות נפוצה")
        page.locator("#coach-question").fill("למה עושים את זה?")
        page.locator("#coach-ask").click()
        expect(page.locator("#chef-conversation")).to_contain_text("מידת ההשחמה משתנה")
        page.locator("#chef-personality").select_option("tough")
        expect(page.locator("#chef-personality")).to_have_value("tough")
        page.locator("#coach-problem").click()
        expect(page.locator("#chef-conversation")).to_contain_text("הפחת חום")
        page.locator("#coach-timer-seconds").fill("1")
        page.locator("#coach-timer-start").click()
        expect(page.locator("#chef-conversation")).to_contain_text("הגיע זמן לבדיקה", timeout=6000)
        expect(page.locator(".current-step h3")).to_have_text("טיגון הבצל")
        page.locator("#coach-pause").click()
        expect(page.locator("#journey-panel .badge")).to_have_text("מושהה")
        page.reload()
        expect(page.locator(".current-step h3")).to_have_text("טיגון הבצל")
        expect(page.locator("#journey-panel .badge")).to_have_text("מושהה")
        page.locator("#coach-pause").click()
        page.locator("#voice-input").click()
        page.evaluate(
            "testRecognizer.onresult({results:[Object.assign([{transcript:'מה לעשות עכשיו'}],{isFinal:true})]})"
        )
        expect(page.locator("#coach-question")).to_have_value("מה לעשות עכשיו")
        assert not any(path == "/v1/chef/respond" for method, path in calls)
        page.locator("#voice-stop").click()
        page.locator("#voice-read").click()
        assert page.evaluate("testSpoken.length") == 1
        page.locator("#open-inventory").click()
        page.locator('[data-ingredient="onion"]').click(click_count=2)
        expect(page.locator('[data-ingredient="onion"] .ingredient-count')).to_have_text("2")
        assert page.locator(".inventory-item").count() == 1
        page.reload()
        page.locator("#open-inventory").click()
        expect(page.locator('[data-ingredient="onion"] .ingredient-count')).to_have_text("2")
        # A legacy empty copy must not override recovered server inventory.
        page.evaluate("localStorage.setItem('chef-inventory-v2:synthetic-owner','[]')")
        page.locator(".connection-details").evaluate("node=>node.open=true")
        page.locator("#token").fill(TOKEN)
        page.locator("#connect-form button").first.click()
        expect(page.locator("#identity")).to_contain_text("synthetic-owner")
        expect(page.locator(".inventory-item")).to_have_count(2)
        expect(page.locator('[data-field="quantity"]').first).to_have_value("4")
        expect(page.locator("#inventory-history")).to_be_visible()
        page.locator(".optional-journeys").evaluate("node=>node.open=true")
        page.locator("#dish-pasta").click()
        expect(page.locator(".current-step h3")).to_have_text("הכנה")
        page.locator('[data-answer="ready"]').click()
        page.locator("#coach-done").click()
        expect(page.locator(".current-step h3")).to_have_text("הכנת הרוטב")
        current = client.get("/v1/coach/current", headers=headers).json()["journey"]
        assert current["current_step"] == 1
        page.locator("#custom-dish-title").fill("כנפי הודו")
        page.locator("#custom-method").select_option(label="צלייה בתנור")
        page.locator("#start-work").click()
        expect(page.locator("#user-step-list")).to_have_count(1)
        expect(page.locator(".user-step-card")).to_have_count(0)
        expect(page.locator("#learning-panel")).to_contain_text("74°C")
        page.locator("#new-step-title").fill("תיבול הכנפיים")
        page.locator("#add-user-step button").click()
        expect(page.locator(".user-step-card")).to_have_count(1)
        expect(page.locator("#new-step-title")).to_have_value("")
        page.locator("#new-step-title").fill("צלייה")
        page.locator("#add-user-step button").click()
        expect(page.locator(".user-step-card")).to_have_count(2)
        page.locator("#work-report").fill("הכנסתי את הכנפיים לתנור")
        page.locator("#user-report-form button").click()
        expect(page.locator("#work-report")).to_have_value("")
        current = client.get("/v1/coach/current", headers=headers).json()["journey"]
        assert current["completed_step_ids"] == []
        page.locator("#coach-question").fill("הרוטב סמיך מדי")
        page.locator("#coach-ask").click()
        expect(page.locator("#current-chef-message")).to_contain_text("נוזל")
        page.locator("#coach-done").click()
        expect(page.locator("#journey-panel")).to_contain_text("1 מתוך 2")
        page.locator("#coach-role").select_option("consultant")
        page.locator("#new-step-title").fill("טיוטה שלא נשלחה")
        page.locator("#report-צריך-עזרה").click()
        expect(page.locator("#new-step-title")).to_have_value("טיוטה שלא נשלחה")
        page.locator("#voice-target").select_option("report")
        page.locator("#voice-input").click()
        page.evaluate(
            "testRecognizer.onresult({results:[Object.assign([{transcript:'הוספתי תיבול'}],{isFinal:true})]})"
        )
        expect(page.locator("#work-report")).to_have_value("הוספתי תיבול")
        page.locator("#voice-stop").click()
        page.locator("#toolbar-finish").click()
        expect(page.locator("#work-debrief")).to_contain_text("אינו אישור")
        current = client.get("/v1/coach/current", headers=headers).json()["journey"]
        assert current["workflow"] == "user" and current["mode"] == "consultant"
        assert current["status"] == "completed" and len(current["completed_step_ids"]) == 1
        page.locator("#custom-dish-title").fill("פילה סלמון")
        page.locator("#custom-method").select_option(label="צריבה במחבת")
        page.locator("#start-work").click()
        expect(page.locator(".user-step-card")).to_have_count(0)
        page.get_by_text("מתווים מתאימים מעץ הידע — לבחירתך", exact=True).click()
        page.locator("#graph-path-path_02").click()
        expect(page.locator(".user-step-card")).to_have_count(4)
        expect(page.locator("#user-step-list")).to_contain_text("בדוק עצמות")
        page.get_by_text("דיווח מהיר לפי שיטת ההכנה", exact=True).click()
        page.locator("[id^='graph-report-']").first.click()
        expect(page.locator("#current-chef-message")).not_to_be_empty()
        current = client.get("/v1/coach/current", headers=headers).json()["journey"]
        assert current["applied_graph_rules"] and current["completed_step_ids"] == []
        assert current["custom_steps"][0]["next_step_prep"]
        for width in (1440, 900, 390):
            page.set_viewport_size({"width": width, "height": 1000})
            assert page.evaluate("document.documentElement.scrollWidth<=innerWidth"), width
            Path(".runtime").mkdir(exist_ok=True)
            page.screenshot(path=f".runtime/coach-{width}.png", full_page=True)
        page.locator(".connection-details").evaluate("node=>node.open=true")
        page.locator("#disconnect").click()
        expect(page.locator("#identity")).to_have_text("")
        expect(page.locator("#coach-mode")).to_contain_text("בישול מקומי")
        assert not errors, errors
        assert TOKEN not in page.evaluate("JSON.stringify(localStorage)")
        browser.close()
    engine.dispose()
    print(
        json.dumps(
            {
                "status": "passed",
                "viewports": [1440, 900, 390],
                "backend": "real workflow / isolated SQLite",
                "checks": [
                    "guest start/resume",
                    "stage validation",
                    "recovery",
                    "timer without auto advance",
                    "personality",
                    "voice input/output mocked",
                    "inventory icons/counts",
                    "legacy-empty recovery",
                    "authenticated persistence",
                    "privacy",
                    "no randomUUID dependency",
                ],
            }
        )
    )


if __name__ == "__main__":
    main()
