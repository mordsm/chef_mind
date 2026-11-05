"""User flow: attach original instructions, report baking, see record and recipe feedback."""
import sys
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1518,'height':900})
    errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8800')
    page.locator('#custom-dish-title').fill('עוף בתנור')
    page.locator('#start-work').click()
    expect(page.locator('#cooking-intake')).to_be_visible(timeout=45000)
    page.locator('#intake-source summary').click()
    page.locator('#intake-recipe_text').fill('אופים את העוף בתנור לפי המתכון.\nבודקים את מרכז הנתח במדחום לפני ההגשה.')
    page.locator('#import-selected-recipe').click()
    expect(page.locator('#recipe-import-preview')).to_contain_text('2 שלבי הכנה נקלטו')
    page.locator('#adopt-imported-recipe').click()
    expect(page.locator('#attached-recipe')).to_contain_text('המתכון שלי')
    assert page.evaluate('mentor.state.recipe_snapshot.steps.length')==2
    page.locator('#mode-live').click()
    expect(page.locator('#kitchen-timer')).not_to_be_visible()
    frame=page.frame_locator('#action-report-frame')
    frame.locator('#action-pages button').click()
    expect(frame.locator('[data-catalog-action]')).to_have_count(13)
    for action in ['roast','bake','fry','grill']:
        expect(frame.locator('[data-catalog-action="'+action+'"]').first).to_be_visible()
    frame.locator('[data-catalog-action="bake"]').click()
    frame.locator('#save-report').click()
    expect(frame.locator('#parameter-dialog')).not_to_be_visible()
    expect(frame.locator('#latest-report')).to_contain_text('לאפות')
    expect(frame.locator('#action-check')).to_contain_text('במתכון שלך')
    expect(frame.locator('#action-check')).to_contain_text('אופים את העוף')
    expect(frame.locator('#action-check')).to_contain_text('הקפד')
    expect(frame.locator('.timer')).to_have_count(1)
    frame.locator('#latest-report button').click()
    expect(frame.locator('#history li')).to_have_count(1)
    assert not errors,errors
    browser.close()
print('Passed: recipe review/adoption, 13-action catalog, visible report record, recipe-linked chef guidance and one timer area.')
