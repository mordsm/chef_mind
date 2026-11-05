"""Verify desktop controls share one viewport; mobile keeps touch-friendly flow."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1518,'height':810})
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto('http://127.0.0.1:8800')
    page.locator('#custom-dish-title').fill('קורקבנים')
    page.locator('#start-work').click()
    expect(page.locator('#cooking-intake')).to_be_visible(timeout=45000)
    expect(page.locator('#learning-panel > #preparation-workflow')).to_be_visible()
    expect(page.locator('#dish-offers')).to_have_count(1)
    page.wait_for_timeout(250)
    assert page.locator('#learning-panel').bounding_box()['x'] < page.locator('#journey-panel').bounding_box()['x']
    page.screenshot(path=str(root/'.runtime/kitchen-preparation-columns.png'),full_page=True)
    page.locator('#mode-live').click()
    page.locator('#choose-cooking-dish').click()
    expect(page.locator('#dish-selection-dialog')).to_be_visible()
    expect(page.locator('#custom-dish-title')).to_be_visible()
    expect(page.locator('#start-work')).to_have_text('התחל מנה חדשה')
    page.locator('#close-dish-selection').click()
    expect(page.locator('#dish-selection-dialog')).not_to_be_visible()
    frame=page.frame_locator('#action-report-frame')
    expect(frame.locator('[data-action="cook"]')).to_be_visible()
    page.wait_for_timeout(500)
    for width,height in [(1518,810),(1366,768),(1920,1080)]:
        page.set_viewport_size({'width':width,'height':height})
        page.wait_for_timeout(250)
        for selector in ['#cooking-live-stage','#live-microphone','#inline-action-reporter','#user-report-form']:
            box=page.locator(selector).bounding_box()
            assert box and box['y']>=0 and box['y']+box['height']<=height+2,(selector,box,height)
        assert page.evaluate('document.documentElement.scrollHeight <= innerHeight + 2'),page.evaluate('({height:innerHeight,scroll:document.documentElement.scrollHeight})')
    page.set_viewport_size({'width':1518,'height':810})
    frame.locator('[data-action="cook"]').click()
    expect(frame.locator('#number-duration')).to_be_visible()
    expect(frame.locator('#save-report')).to_be_visible()
    for width,height in [(1518,810),(1366,768),(1920,1080)]:
        page.set_viewport_size({'width':width,'height':height})
        page.wait_for_timeout(250)
        save_box=frame.locator('#save-report').bounding_box()
        frame_box=page.locator('#action-report-frame').bounding_box()
        assert save_box['y']+save_box['height']<=frame_box['y']+frame_box['height'],(save_box,frame_box)
    page.set_viewport_size({'width':1518,'height':810})
    page.screenshot(path=str(root/'.runtime/kitchen-viewport-desktop.png'),full_page=True)
    frame.locator('#save-report').click()
    expect(frame.locator('#action-check')).to_be_visible()
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    expect(page.locator('#live-microphone')).to_be_visible()
    assert not errors,errors
    browser.close()
print('Passed: desktop cockpit fits 1518×810, 1366×768 and 1920×1080; action form, feedback and mobile work.')
