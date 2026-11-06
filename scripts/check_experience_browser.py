"""Real UI smoke: explicit recipe setup, safety, measurements and responsive layout."""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.config import Settings
from app.db import Base, make_engine
from app.main import create_app
from fastapi.testclient import TestClient
from playwright.sync_api import expect, sync_playwright


def main(output, live_url=None):
    output.mkdir(parents=True, exist_ok=True)
    settings = Settings(
        _env_file=None,
        database_url="sqlite+pysqlite:///:memory:",
        sync_enabled=False,
        dish_model_provider="disabled",
        model_enabled=False,
    )
    engine = make_engine(settings.database_url)
    Base.metadata.create_all(engine)
    errors, checked = [], []
    with TestClient(create_app(settings, engine)) as client, sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        try:
            for width in (1440, 390):
                page = browser.new_page(viewport={"width": width, "height": 1000})
                page.on("pageerror", lambda error: errors.append(str(error)))

                def serve(route):
                    request = route.request
                    if urlsplit(request.url).netloc != "127.0.0.1:8800":
                        route.abort()
                        return
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

                if not live_url:
                    page.route("**/*", serve)
                page.goto(live_url or "http://127.0.0.1:8800/", timeout=45000)
                expect(page.locator(".ux-meal")).to_have_count(6)
                expect(page.locator("#ux-welcome")).to_be_visible()
                assert not page.evaluate("document.documentElement.scrollWidth > innerWidth")
                page.screenshot(path=str(output / f"home-{width}.png"), full_page=True)
                # A canceled dialog must not start a journey and returns focus.
                page.locator("#meal-bread").click()
                page.keyboard.press("Escape")
                expect(page.locator("#meal-bread")).to_be_focused()
                assert page.evaluate("mentor.state === null")
                for key, count in (
                    ("salad", 4),
                    ("beef", 6),
                    ("fish", 4),
                    ("legumes", 5),
                    ("soup", 5),
                    ("bread", 5),
                ):
                    if page.evaluate("Boolean(mentor.state)"):
                        page.locator("#choose-cooking-dish").click()
                        page.locator("#choose-meal-" + key).click()
                    else:
                        page.locator("#meal-" + key).click()
                    expect(page.locator("#ux-meal-dialog")).to_be_visible()
                    expect(page.locator("#ux-meal-confirm")).not_to_be_checked()
                    page.locator("#ux-meal-confirm").check()
                    if key == "fish":
                        page.locator("#ux-meal-allergies").fill("דגים")
                        page.locator("#ux-meal-start").click()
                        expect(page.locator("#ux-meal-status")).to_contain_text("אלרגן", timeout=60000)
                        expect(page.locator("#ux-meal-dialog")).to_be_visible()
                        page.locator("#ux-meal-allergies").fill("")
                    page.locator("#ux-meal-start").click()
                    expect(page.locator("#ux-meal-dialog")).not_to_be_visible(timeout=90000)
                    page.wait_for_function(
                        "n => mentor.state?.custom_steps.length === n && !mentor.busy", arg=count
                    )
                    expect(page.locator("#cooking-live-stage .station-current-action")).to_be_visible()
                    expect(page.locator("#ux-cooking-reference .station-full-protocol")).not_to_have_attribute(
                        "open", ""
                    )
                    expect(page.locator("#ux-report-tools")).not_to_have_attribute("open", "")
                    expect(page.locator("#ux-report-tools")).to_be_visible()
                    expect(page.locator("#work-report")).to_be_visible()
                    if width >= 1100:
                        columns=page.evaluate("['.journey-panel','#cockpit-voice','.companion-panel'].map(s => Math.round(document.querySelector(s).getBoundingClientRect().x))")
                        assert len(set(columns)) == 3, columns
                    assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), (
                        width,
                        key,
                    )
                    if key == "salad":
                        page.locator("#work-report").fill("הרוטב חמוץ מדי")
                        page.locator("#user-report-form button[type=submit]").click()
                        expect(page.locator("#cooking-live-stage .station-current-action")).to_contain_text(
                            "כף מהרוטב", timeout=30000
                        )
                        expect(page.locator("#voice-explanation")).to_be_visible()
                        expect(page.locator("#voice-explanation")).to_contain_text("כף מהרוטב")
                        page.screenshot(path=str(output / f"cooking-{width}.png"), full_page=True)
                        page.locator("#ux-report-tools > summary").click()
                        frame = page.frame_locator("#action-report-frame")
                        expect(frame.locator('[data-action="cut"]')).to_be_enabled(timeout=30000)
                        frame.locator('[data-action="cut"]').click()
                        page.wait_for_function("() => document.body.classList.contains('action-modal-open')")
                        frame.locator("#cancel-report").click()
                        page.wait_for_function("() => !document.body.classList.contains('action-modal-open')")
                        page.locator("#ux-report-tools > summary").click()
                    if key == "fish":
                        for _ in range(2):
                            page.locator("#live-done").click()
                            page.wait_for_function("() => !mentor.busy")
                        expect(page.locator("#work-temperature")).to_be_visible()
                        page.locator("#live-done").click()
                        page.wait_for_function("() => !mentor.busy")
                        assert page.evaluate("mentor.state.completed_step_ids.length") == 2
                        page.locator("#work-temperature").fill("63")
                        page.locator("#work-temperature-submit").click()
                        page.wait_for_function("() => !mentor.busy")
                        page.locator("#live-done").click()
                        page.wait_for_function("() => !mentor.busy")
                        page.locator("#live-done").click()
                        expect(page.locator("#ux-finish")).to_be_visible()
                        page.locator("#ux-finish").click()
                        page.wait_for_function("() => mentor.state.status === 'completed'")
                    checked.append({"width": width, "dish": key, "steps": count})
                page.close()
        finally:
            browser.close()
    assert not errors, errors
    report = {
        "passed": True,
        "url": live_url,
        "checks": checked,
        "explicit_confirmation": True,
        "allergen_block": True,
        "visible_measurement_and_finish": True,
        "console_errors": errors,
        "physical_voice": "NOT_VERIFIED",
    }
    (output / "result.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--url")
    args = parser.parse_args()
    main(args.output, args.url)
