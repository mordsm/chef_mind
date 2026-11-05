"""Read-only live UI check using an isolated guest browser context."""

from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def main():
    root = Path(__file__).resolve().parents[1]
    url = (root / ".runtime/permanent-cloudflare-url.txt").read_text().strip()
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.on("pageerror", lambda error: errors.append(str(error)))
        response = page.goto(url, timeout=30000)
        assert response.status == 200
        page.locator("#custom-dish-title").fill("קורקבנים")
        expect(page.locator('#custom-method option[value="boil_simmer"]')).to_have_count(1)
        method_label=page.locator('#custom-method option[value="boil_simmer"]').inner_text()
        page.locator('#custom-method + .touch-choices').get_by_role('button',name=method_label,exact=True).click()
        page.locator("#start-work").click()
        expect(page.locator("#active-work-guidance .book-knowledge-tip")).to_contain_text("הקורקבנים",timeout=45000)
        expect(page.locator("#active-work-guidance")).not_to_contain_text("חומציות וריכוך ירקות")
        for text in ("McGee", "The Food Lab", "ללא אימות מדעי", "העשרת לחות"):
            expect(page.locator("#active-work-guidance")).not_to_contain_text(text)
        frame = page.frame_locator("#action-report-frame")
        expect(frame.locator('[data-action="cook"]')).to_be_visible()
        frame.locator('[data-action="cook"]').click()
        expect(frame.locator("#number-duration")).to_have_value("30")
        expect(frame.locator("#number-temperature")).to_be_visible()
        frame.locator("#number-duration").fill("45")
        # Re-rendering the chef's parent screen must retain the unsubmitted form.
        page.evaluate('renderCoach()')
        expect(frame.locator("#number-duration")).to_have_value("45")
        frame.locator("#save-report").click()
        expect(frame.locator("#history li[data-report-id]")).to_have_count(1)
        expect(frame.locator(".timer")).to_have_count(1)
        expect(frame.locator("#action-check")).to_contain_text("מה המצב עכשיו")
        frame.locator("#action-check button").filter(has_text="בעבוע עדין").click()
        expect(frame.locator("#action-check")).to_contain_text("מספיק נוזל")
        expect(page.locator("#intake-cut")).to_have_js_property("tagName", "SELECT")
        expect(page.locator("#intake-quantity")).to_have_js_property("tagName", "SELECT")
        expect(page.locator("#cooking-intake")).to_contain_text("אמהות מבשלות")
        expect(page.locator("#intake-source")).not_to_have_attribute("open", "")
        page.locator('#mode-live').click()
        expect(page.locator('#cooking-live-stage')).to_be_visible()
        expect(page.locator('#cooking-intake')).not_to_be_visible()
        expect(page.locator('#live-microphone')).to_be_visible()
        expect(frame.locator('[data-action="cook"]')).to_be_visible()
        assert frame.locator('[data-action="cook"]').bounding_box()['height'] >= 76
        page.locator('#mode-prepare').click()
        expect(page.locator('#cooking-intake')).to_be_visible()
        expect(page.locator('#intake-family')).not_to_be_visible()
        page.locator('#mode-live').click()
        for width in (1440, 390):
            page.set_viewport_size({"width": width, "height": 1000})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        assert not errors, errors
        browser.close()
    print(
        "Passed on the live Cloudflare address: relevant practical cards, no visible book references, embedded action icons, heat/time controls, local report/timer and form preservation."
    )


if __name__ == "__main__":
    main()
