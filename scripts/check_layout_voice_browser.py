"""Focused checks for action guidance, mentor placement, choice labels and dictation."""

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
        errors, posts = [], []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("dialog", lambda dialog: dialog.accept())
        page.add_init_script("""
            window.voiceStarts=0;window.voiceAborts=0;
            window.SpeechRecognition=class {
                start(){window.testRecognizer=this;document.documentElement.dataset.voiceStarts=String(++window.voiceStarts);this.onstart();}
                abort(){window.voiceAborts++;this.onend();}
            };
            Object.defineProperty(window,'speechSynthesis',{value:{cancel(){},getVoices(){return []}},configurable:true});
        """)

        def serve(route):
            request = route.request
            url = urlsplit(request.url)
            if request.method == "POST":
                posts.append(url.path)
            response = client.request(
                request.method,
                url.path,
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
        expect(page.locator("#active-work-guidance #current-chef-message")).to_contain_text("קורקבנים")
        for button in page.locator(".decision-question button").all():
            assert not re.match(r"^\d+[.)]", button.inner_text())
        assert "מספר" not in page.locator("#status-question").inner_text()
        page.locator("#new-step-title").fill("הפעולה הנוכחית")
        page.locator("#add-user-step button").click()
        expect(page.locator(".user-step-card.selected #active-work-guidance")).to_be_visible()
        for width in (1440, 900, 390):
            page.set_viewport_size({"width": width, "height": 1000})
            mode = page.locator("#mentor-settings").bounding_box()
            dish = page.locator("#custom-dish-title").bounding_box()
            assert mode["y"] + mode["height"] <= dish["y"] + 1
            assert page.locator("#mentor-settings #chef-personality").count() == 1
            card = page.locator(".user-step-card.selected").bounding_box()
            guidance = page.locator("#active-work-guidance").bounding_box()
            assert (
                card["y"] <= guidance["y"]
                and guidance["y"] + guidance["height"] <= card["y"] + card["height"]
            )
            assert guidance["width"] <= card["width"]

        page.set_viewport_size({"width": 1440, "height": 1000})
        assert page.locator("#voice-target").count() == 0
        page.locator("#work-report-dictate").click()
        expect(page.locator("#voice-input")).to_have_attribute("aria-pressed", "true")
        assert page.evaluate("testRecognizer.continuous && testRecognizer.interimResults")
        initial_posts = len(posts)
        page.evaluate(
            "testRecognizer.onresult({resultIndex:0,results:[Object.assign([{transcript:'דיווח בקול'}],{isFinal:true})]})"
        )
        expect(page.locator("#work-report")).to_have_value("דיווח בקול")
        page.evaluate(
            "testRecognizer.onresult({resultIndex:0,results:[Object.assign([{transcript:'דיווח בקול'}],{isFinal:true})]})"
        )
        expect(page.locator("#work-report")).to_have_value("דיווח בקול")
        assert page.locator("#coach-question").input_value() == ""
        assert len(posts) == initial_posts  # Dictation never sends automatically.
        aborts = page.evaluate("voiceAborts")
        page.locator("#choice-goal-sauce").click()
        expect(page.locator("#current-chef-message")).to_contain_text("בחרת תבשיל רך ברוטב")
        expect(page.locator("#voice-input")).to_have_attribute("aria-pressed", "true")
        assert page.evaluate("voiceAborts") == aborts
        expect(page.locator("#work-report")).to_have_value("דיווח בקול")

        page.evaluate("testRecognizer.onend()")
        expect(page.locator("html")).to_have_attribute("data-voice-starts", "2")
        page.evaluate("testRecognizer.onend()")
        expect(page.locator("html")).to_have_attribute("data-voice-starts", "3")
        page.evaluate("testRecognizer.onend()")
        expect(page.locator("#voice-input")).to_have_attribute("aria-pressed", "false")
        expect(page.locator("#voice-status")).to_contain_text("הטקסט נשמר")

        page.locator("#coach-talk").click()
        page.evaluate("testRecognizer.onerror({error:'network'})")
        expect(page.locator("#voice-status")).to_contain_text("אינו זמין ברשת")
        expect(page.locator("#voice-input")).to_have_attribute("aria-pressed", "false")
        page.locator("#coach-talk").click()
        page.evaluate("testRecognizer.onerror({error:'not-allowed'})")
        expect(page.locator("#voice-status")).to_contain_text("אין הרשאה")
        page.locator("#coach-talk").click()
        page.evaluate(
            "testRecognizer.onresult({results:[Object.assign([{transcript:'שאלה בקול'}],{isFinal:true})]})"
        )
        expect(page.locator("#coach-question")).to_have_value("שאלה בקול")
        expect(page.locator("#work-report")).to_have_value("דיווח בקול")
        page.locator("#coach-talk").click()
        expect(page.locator("#voice-input")).to_have_attribute("aria-pressed", "false")
        page.locator(".optional-journeys > summary").click()
        page.locator("#dish-shakshuka").click()
        expect(page.locator(".current-step #active-work-guidance")).to_be_visible()
        assert not errors, errors
        browser.close()
    engine.dispose()
    print(
        "Passed: action-adjacent guidance at 1440/900/390px, mentor placement, unnumbered choices, voice targets/restarts/errors/no automatic send. Speech service mocked; physical microphone not tested."
    )


if __name__ == "__main__":
    main()
