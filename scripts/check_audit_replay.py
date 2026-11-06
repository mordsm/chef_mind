"""Replay saved six-scenario audit inputs against isolated, model-disabled code.

This checks software behavior, not physical cooking or deployed production.
The baseline directory contains the original audit's per-scenario snapshots.
"""

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


def main(baseline, output):
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
    results, pilot = [], None
    with TestClient(create_app(settings, engine)) as client:
        for name in ("beef", "fish", "legumes", "soup", "salad", "bread"):
            folder = baseline / name
            initial = json.loads((folder / "01-start.json").read_text(encoding="utf-8"))["state"]
            facts = json.loads((folder / "02-intake.json").read_text(encoding="utf-8"))["state"][
                "intake_facts"
            ]
            state, transcript = None, []

            def command(action, _scenario=name, _transcript=transcript, **extra):
                nonlocal state
                response = client.post(
                    "/v1/coach/preview",
                    json={
                        "state": state,
                        "command": {
                            "action": action,
                            "expected_revision": state["revision"] if state else 0,
                            **extra,
                        },
                    },
                )
                assert response.status_code == 200, (_scenario, action, response.text[:500])
                state = response.json()
                _transcript.append({"action": action, "input": extra, "state": state})
                assert len(state["station_protocol"]["blocks"]) == 6

            command(
                "start_custom",
                dish_title=initial["dish_title"],
                ingredients=initial["ingredients"],
                method=initial["method"],
            )
            command("intake", intake_facts=facts)
            if name == "salad":
                pilot = state
                assert len(state["custom_steps"]) == 4
            for snapshot in sorted(folder.glob("*.json")):
                if not "03-" <= snapshot.name[:3] <= "12-":
                    continue
                saved = json.loads(snapshot.read_text(encoding="utf-8"))
                message = saved.get("simulated_user_message")
                if message:
                    command("ask", message=message)
            result = {
                "scenario": name,
                "dish": state["dish_title"],
                "steps": len(state["custom_steps"]),
                "six_blocks": True,
                "timer_started": state["timer_deadline"] is not None,
                "guided_scope": "pilot" if name == "salad" else "not_implemented",
                "memory": state.get("cooking_memory", {}),
            }
            results.append(result)
            (output / f"{name}.json").write_text(
                json.dumps(transcript, ensure_ascii=False, indent=2), encoding="utf-8"
            )

        # Real UI requests and actual wall-clock countdown, without mock time.
        errors = []
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="msedge", headless=True)
            try:
                for width in (1440, 390):
                    page = browser.new_page(viewport={"width": width, "height": 1000})
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    offline = {"enabled": False}

                    def serve(route, _request, network=offline):
                        request = route.request
                        if urlsplit(request.url).netloc != "127.0.0.1:8800" or network["enabled"]:
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

                    page.route("**/*", serve)
                    page.goto("http://127.0.0.1:8800/")
                    # The older broad coach harness assumes removed custom-step
                    # controls. Keep built-in regression independent of that UI.
                    page.evaluate(
                        "async () => {if(!await coachCommand('start'))throw Error('start failed');}"
                    )
                    expect(
                        page.locator(".current-step").get_by_role(
                            "heading", name="הכנת חומרי הגלם", exact=True
                        )
                    ).to_be_visible()
                    page.locator("#coach-done").click()
                    page.wait_for_function("() => !mentor.busy")
                    assert page.evaluate("mentor.state.current_step") == 0
                    page.locator('[data-answer="ready"]').click()
                    page.wait_for_function("() => !mentor.busy")
                    page.locator("#coach-done").click()
                    expect(
                        page.locator(".current-step").get_by_role("heading", name="טיגון הבצל", exact=True)
                    ).to_be_visible()
                    page.evaluate(
                        "async () => {await coachCommand('start_custom',{dish_title:'בקר ושמנת',ingredients:['בקר','שמנת'],forbid_meat_dairy:true});}"
                    )
                    expect(page.locator("#coach-notice")).to_contain_text("בחרת הפרדה בין בשר לחלב")
                    page.evaluate(
                        "async () => {await coachCommand('start_custom',{dish_title:'סלט',ingredients:['מלפפון','רוטב מוכן'],allergies:['שומשום']});}"
                    )
                    expect(page.locator("#coach-notice")).to_contain_text("רשימת הרכיבים")
                    page.evaluate(
                        "state => localStorage.setItem('chef-coach-guest-v1', JSON.stringify(state))", pilot
                    )
                    page.reload()
                    page.wait_for_function("() => mentor.state?.custom_steps?.length === 4")
                    page.locator("#mode-live").click()
                    stage = page.locator("#cooking-live-stage")
                    expect(stage.locator(".station-full-protocol")).not_to_have_attribute("open", "")
                    expect(stage.locator(".station-block")).to_have_count(6)
                    expect(stage.locator(".station-current-action")).to_be_visible()
                    await_command = "async message => { const state=await coachCommand('ask',{message}); if(!state)throw Error('command failed'); return state; }"
                    page.evaluate(await_command, "הרוטב חמוץ מדי והסלט מתחיל להוציא מים")
                    expect(stage.locator(".station-current-action")).to_contain_text("כף מהרוטב")
                    page.evaluate(await_command, "אין לי לימון. יש חומץ. איך להחליף?")
                    page.evaluate(await_command, "מה פירוש שליקה? זו שאלה צדדית")
                    page.evaluate(await_command, "חזור לבישול: מה התקלה ומה חסר לי?")
                    expect(stage.locator(".station-current-action")).to_contain_text("אין לי לימון")
                    # Simulate an unavailable API and preserve the typed text.
                    editor = page.locator(".voice-question-editor")
                    editor.locator(":scope > summary").click()
                    page.locator("#work-report").fill("שאלה שנשמרת גם כשהרשת נותקה")
                    offline["enabled"] = True
                    page.locator("#user-report-form button[type=submit]").click()
                    page.wait_for_function("() => !mentor.busy")
                    expect(page.locator("#work-report")).to_have_value("שאלה שנשמרת גם כשהרשת נותקה")
                    offline["enabled"] = False
                    page.evaluate(await_command, "הפעל תזכורת אמיתית בעוד שתי שניות")
                    page.wait_for_function("() => mentor.state?.asked.includes('time')", timeout=15000)
                    expect(stage.locator(".station-current-action")).to_contain_text("מה מצב המנה")
                    page.reload()
                    page.wait_for_function("() => mentor.state?.cooking_memory?.missing_ingredient_report")
                    page.locator("#mode-live").click()
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), width
                    for _ in range(4):
                        page.locator("#live-done").click()
                        page.wait_for_function("() => !mentor.busy")
                    assert page.evaluate("mentor.state.completed_step_ids.length") == 4
                    page.evaluate(await_command, "איך להגיש ולשמור מה שנשאר?")
                    expect(stage.locator(".station-current-action")).to_contain_text("מתחת ל־4°C")
                    page.screenshot(path=str(output / f"pilot-{width}.png"), full_page=True)
                    page.close()
            finally:
                browser.close()
        assert not errors, errors
    summary = {
        "environment": "isolated TestClient + Edge; model disabled; not deployed",
        "scenarios": results,
        "browser_widths": [1440, 390],
        "real_timer_expired": True,
        "refresh_memory": True,
        "offline_typed_text": True,
        "built_in_shakshuka": True,
        "physical_cooking_and_voice": "NOT_VERIFIED",
        "remaining": [
            "Five non-pilot dishes lack a generated full plan",
            "CM-007",
            "CM-013",
            "Authorized live retrieval verification",
        ],
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    main(args.baseline, args.output)
