"""Headless UI smoke with synthetic intercepted API data; never uses real credentials."""

import json
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def main():
    state = {"requests": [], "reviewed": False, "inventory": None}
    unit = {
        "title": "Onion browning",
        "principle": "Lower heat slows browning.",
        "recommended_action": "Lower the heat and monitor the onion.",
        "conditions": [],
        "observations": ["Report browning."],
        "exceptions": [],
        "safety_notes": [],
        "kashrut_notes": [],
        "required_ingredients": [],
        "conflicts_with": [],
        "tags": ["onion"],
        "confidence": 70,
        "verified_on": "2026-10-19",
    }
    document = {
        "title": "Synthetic onion note",
        "source_reference": "https://example.com/source",
        "license_reference": "Original synthetic fixture",
        "attribution": "Test author",
        "adaptation_notes": "Synthetic UI test only",
        "units": [unit],
    }

    def mock(route):
        request = route.request
        path = request.url.split("8800", 1)[1]
        draft = {
            "id": "fixture-revision",
            "revision": 1,
            "status": "active" if state["reviewed"] else "pending_review",
            "document": document,
        }
        if path == "/v1/inventory":
            if request.method == "PUT":
                state["inventory"] = request.post_data_json["items"]
            data = {
                "items": state["inventory"] or [],
                "origin": "saved" if state["inventory"] is not None else "empty",
            }
        elif path == "/v1/session":
            data = {"user_id": "synthetic-owner", "role": "reviewer"}
        elif path.startswith("/v1/knowledge/sources"):
            data = {
                "items": [
                    {
                        "source_id": "synthetic-source",
                        "title": '<img src=x onerror="window.injected=true">',
                        "status": "active",
                        "latest_revision_id": "fixture-revision",
                        "conditions": [],
                    }
                ],
                "has_more": False,
            }
        elif path == "/v1/knowledge/pending":
            data = {"items": [] if state["reviewed"] else [draft]}
        elif path == "/v1/knowledge/fixture-revision/revisions":
            data = {"items": [draft], "active_revision_id": "fixture-revision" if state["reviewed"] else None}
        elif path == "/v1/knowledge/fixture-revision/approve":
            state["reviewed"] = True
            data = {"status": "active"}
        elif path == "/v1/knowledge/fixture-revision":
            data = draft
        elif path == "/v1/chef/respond":
            body = request.post_data_json
            state["requests"].append(body)
            data = {
                "decision_type": "action",
                "instruction": unit["recommended_action"],
                "culinary_reason": unit["principle"],
                "success_signal": "Report browning.",
                "safety_flags": [],
                "alternatives": [],
                "engine_version": "extractive-hash-v1",
                "policy_flags": [],
                "citations": [],
                "state_revision": len(state["requests"]),
            }
            if body["message"] == "unsupported-fixture":
                data.update(
                    decision_type="insufficient_evidence",
                    instruction="No approved source for this dish.",
                    available_topics=["Onion browning"],
                )
            if body["message"] == "self-check":
                data.update(
                    decision_type="clarify",
                    instruction="בדוק שהנתח עשיר ברקמת חיבור.",
                    requires_confirmation=False,
                    missing_conditions=["cut identified"],
                    basic_knowledge=[
                        {
                            "title": "Cooking methods",
                            "text": "Educational background.",
                            "source": "https://example.com/source",
                        }
                    ],
                )
            if (
                body["message"] == "needs-condition"
                and "onion is browning" not in body["confirmed_conditions"]
            ):
                data.update(
                    decision_type="clarify",
                    instruction="Please confirm the actual condition.",
                    missing_conditions=["onion is browning"],
                )
        else:
            route.fulfill(status=404, json={"code": "NOT_FOUND"})
            return
        route.fulfill(json=data)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.add_init_script("""
            window.testSpoken=[];window.testVoices=[{localService:false,lang:'en-US'}];
            window.testWakeReleases=0;
            Object.defineProperty(window,'speechSynthesis',{value:{cancel(){},getVoices(){return window.testVoices;},speak(item){window.testSpoken.push(item.text);}},configurable:true});
            window.SpeechSynthesisUtterance=function(text){this.text=text;};
            Object.defineProperty(navigator,'wakeLock',{value:{async request(){let listener;return {addEventListener(type,fn){listener=fn;},async release(){window.testWakeReleases++;if(listener)listener();}};}},configurable:true});
        """)
        page.route("**/v1/**", mock)
        # Serve the exact local assets without requiring a running database/service.
        static = Path(__file__).resolve().parents[1] / "backend/app/static"

        def asset(route):
            name = route.request.url.rsplit("/", 1)[-1] or "index.html"
            # This suite exercises the retained legacy console controls independently;
            # check_coach_browser.py covers the complete new interface and backend.
            if name in ("coach.js", "voice.js", "coach.css", "workbench.js", "workbench.css"):
                route.fulfill(
                    body="", content_type="text/css" if name.endswith(".css") else "text/javascript"
                )
                return
            path = static / name
            if path.is_file() and path.parent == static:
                mime = {"html": "text/html", "js": "text/javascript", "css": "text/css"}[path.suffix[1:]]
                route.fulfill(body=path.read_bytes(), content_type=mime + "; charset=utf-8")
            else:
                route.fulfill(status=404)

        page.route("http://127.0.0.1:8800/", asset)
        page.route("**/assets/*", asset)
        page.goto("http://127.0.0.1:8800/")
        expect(page.locator("html")).to_have_attribute("dir", "rtl")
        page.locator("#language").click()
        expect(page.locator("html")).to_have_attribute("dir", "ltr")
        page.locator("#token").fill("synthetic-test-token-never-real")
        page.locator("#connect-form button[type=submit]").count()  # Submit button has implicit type.
        page.locator("#connect-form button").first.click()
        expect(page.locator("#identity")).to_contain_text("synthetic-owner")
        expect(page.locator("#token")).to_have_value("")
        assert "synthetic-test-token" not in page.evaluate("JSON.stringify(localStorage)")
        assert page.evaluate("sessionStorage.length") == 0
        page.locator('[data-view="knowledge"]').click()
        expect(page.locator("#sources .card")).to_have_count(1)
        assert page.locator("#sources img").count() == 0
        assert not page.evaluate("Boolean(window.injected)")
        page.locator('[data-view="review"]').click()
        page.locator("#pending button").click()
        expect(page.locator("#review-detail h2")).to_have_text("Synthetic onion note")
        page.locator("#review-detail textarea").fill("Reviewed synthetic test fixture")
        page.on("dialog", lambda dialog: dialog.accept())
        page.locator('#review-detail [data-i18n="approve"]').click()
        expect(page.locator('#review-detail [data-i18n="status_active"]')).to_be_visible()
        assert state["reviewed"]
        page.locator('[data-view="cook"]').click()
        page.locator("#ask").click()
        expect(page.locator("#notice")).to_contain_text("Enter a cooking goal")
        page.locator("#goal").fill("Soft onion")
        expect(page.locator("#question")).to_have_value("")
        expect(page.locator("#reports")).to_have_value("")
        page.locator("#add-item").click()
        page.locator('[data-field="name"]').fill("onion")
        page.locator('[data-field="quantity"]').fill("1.5")
        page.locator('[data-field="unit"]').fill("pieces")
        expect(page.locator('[data-field="food_class"]')).to_have_value("pareve")
        expect(page.locator('[data-field="food_class"]')).not_to_be_visible()
        expect(page.locator('[data-field="allergens"]')).not_to_be_visible()
        assert page.locator(".inventory-item label span:not(.sr-only)").count() == 0
        expect(page.locator('[data-field="verified"]')).to_have_count(0)
        expect(page.locator('[data-field="label_verified"]')).to_have_count(0)
        page.locator("#ask").click()
        expect(page.locator("#decision .instruction")).to_have_text(unit["recommended_action"])
        assert state["requests"][0]["inventory"][0]["quantity"] == 1.5
        assert not state["requests"][0]["allow_external_model"]
        assert state["requests"][0]["message"].startswith("How do I start preparing:")
        assert state["requests"][0]["state"]["reports"] == []
        assert page.locator("#decision").evaluate("node=>node===document.activeElement")
        assert page.locator(".inventory-item").first.bounding_box()["height"] < 125
        page.locator("#kitchen-open").click()
        expect(page.locator("#kitchen-dialog")).to_be_visible()
        expect(page.locator("#kitchen-action")).to_have_text(unit["recommended_action"])
        page.locator("#kitchen-read").click()
        assert page.evaluate("testSpoken.length") == 0  # Never fall back to a remote voice.
        page.evaluate("testVoices=[{localService:true,lang:'en-US'}]")
        page.locator("#kitchen-read").click()
        assert page.evaluate("testSpoken[0]") == unit["recommended_action"]
        page.locator("#kitchen-awake").click()
        expect(page.locator("#kitchen-awake")).to_have_attribute("aria-pressed", "true")
        page.locator("#reminder-seconds").fill("0")
        page.locator("#reminder-start").click()
        expect(page.locator("#kitchen-notice")).to_contain_text("whole number")
        page.locator("#reminder-seconds").fill("1")
        page.locator("#reminder-start").click()
        expect(page.locator("#reminder-notice")).to_contain_text("selected time elapsed", timeout=5000)
        page.locator("#kitchen-report").fill("Onion is softer but still browning.")
        page.locator("#kitchen-add-report").click()
        assert len(state["requests"]) == 1  # Reporting does not silently send a request.
        page.locator("#kitchen-close").click()
        expect(page.locator("#kitchen-dialog")).not_to_be_visible()
        expect(page.locator("#reports")).to_have_value("Onion is softer but still browning.")
        assert page.evaluate("testWakeReleases") == 1
        page.locator("#kitchen-open").click()
        page.locator("#reminder-seconds").fill("30")
        page.locator("#reminder-start").click()
        page.keyboard.press("Escape")
        expect(page.locator("#kitchen-dialog")).not_to_be_visible()
        expect(page.locator("#reminder-clock")).to_have_text("00:00")
        page.locator("#add-item").click()
        expect(page.locator(".inventory-item")).to_have_count(2)
        page.locator(".inventory-item .remove-item").last.click()
        expect(page.locator(".inventory-item")).to_have_count(1)
        page.locator("#question").fill("unsupported-fixture")
        page.locator("#ask").click()
        page.locator(".topic-list summary").click()
        expect(page.locator(".topic-list button")).to_have_text("Onion browning")
        page.locator(".topic-list button").click()
        expect(page.locator("#goal")).to_have_value("Onion browning")
        expect(page.locator("#question")).to_have_value("")
        page.locator("#question").fill("needs-condition")
        page.locator("#ask").click()
        page.locator(".condition-list summary").click()
        expect(page.locator("[data-confirm-condition]")).to_be_visible()
        expect(page.locator("[data-confirm-condition]")).not_to_be_checked()
        page.locator("[data-confirm-condition]").check()
        page.locator("#ask").click()
        expect(page.locator("#decision .instruction")).to_have_text(unit["recommended_action"])
        assert "onion is browning" in state["requests"][-1]["confirmed_conditions"]
        page.locator("#question").fill("self-check")
        page.locator("#ask").click()
        expect(page.locator("#decision .instruction")).to_have_text("בדוק שהנתח עשיר ברקמת חיבור.")
        expect(page.locator("[data-confirm-condition]")).to_have_count(0)
        expect(page.locator(".guidance-details")).to_have_count(0)
        expect(page.locator(".basic-card")).to_have_count(1)
        Path(".runtime").mkdir(exist_ok=True)
        for width in (1440, 800, 390):
            page.set_viewport_size({"width": width, "height": 1000})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#kitchen-open").click()
            assert page.locator("#kitchen-dialog").evaluate("node=>node.scrollWidth<=node.clientWidth")
            page.screenshot(path=f".runtime/kitchen-{width}.png", full_page=True)
            page.locator("#kitchen-close").click()
        Path(".runtime").mkdir(exist_ok=True)
        page.screenshot(path=".runtime/console-mobile.png", full_page=True)
        page.set_viewport_size({"width": 1440, "height": 1000})
        page.screenshot(path=".runtime/console-desktop.png", full_page=True)
        page.locator('[data-field="name"]').fill("milk")
        expect(page.locator('[data-field="food_class"]')).to_have_value("dairy")
        expect(page.locator('[data-field="allergens"]')).to_have_value("milk")
        expect(page.locator("#inventory-allergens")).to_have_text("Milk")
        page.reload()
        expect(page.locator(".inventory-item")).to_have_count(0)
        page.locator("#token").fill("synthetic-test-token-never-real")
        page.locator("#connect-form button").first.click()
        expect(page.locator('[data-field="name"]')).to_have_value("milk")
        expect(page.locator('[data-field="allergens"]')).to_have_value("milk")
        assert "synthetic-test-token" not in page.evaluate("JSON.stringify(localStorage)")
        page.locator("#disconnect").click()
        expect(page.locator("#goal")).to_have_value("")
        expect(page.locator(".inventory-item")).to_have_count(0)
        expect(page.locator("#identity")).to_have_text("")
        expect(page.locator("#kitchen-open")).to_be_disabled()
        expect(page.locator("#kitchen-action")).to_have_text("")
        assert not errors, errors
        browser.close()
    print(
        json.dumps(
            {
                "status": "passed",
                "browser": "headless Edge",
                "viewports": [1440, 390],
                "checks": [
                    "RTL/English",
                    "login/privacy",
                    "catalog text escaping",
                    "review approval",
                    "decimal inventory",
                    "local-only cooking",
                    "add/remove inventory",
                    "responsive width",
                    "disconnect",
                    "kitchen dialog and Escape",
                    "manual reminder validation/completion/cancellation",
                    "explicit unsent outcome report",
                    "local-only speech selection (mocked)",
                    "screen wake lock/release (mocked)",
                    "first guidance without reports or question",
                    "visible validation and focused response",
                    "single-row desktop inventory",
                    "supported topic selection and explicit condition confirmation",
                ],
            }
        )
    )


if __name__ == "__main__":
    main()
