"""Exercise the user's dish recognition, save guidance and structured grill report."""
from playwright.sync_api import sync_playwright, expect
import sys

with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1518,'height':900})
    errors=[];calls=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda request:calls.append(request.url) if '/v1/coach/preview' in request.url else None)
    page.goto(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8800')
    page.locator('#custom-dish-title').fill('עוף בגריל')
    page.locator('#start-work').click()
    expect(page.locator('#cooking-intake')).to_be_visible(timeout=45000)
    assert page.evaluate('mentor.state.method')=='גריל ישיר'
    assert page.evaluate('mentor.state.dish_identity.status')=='recognized'
    assert page.evaluate('mentor.state.dish_identity.provider')=='local'
    assert page.locator('#intake-goal option[value="sauce"]').count()==0
    assert page.locator('#intake-main_ingredient').count()==0
    assert page.locator('#add-user-step').count()==0
    for id,value in [('cut','שלם'),('quantity','500 גרם')]:
        details=page.locator('.intake-page').filter(has=page.locator('#intake-'+id))
        if details.get_attribute('open') is None:details.locator('summary').click()
        details.get_by_role('button',name=value,exact=True).click()
    page.get_by_role('button',name='שמור פרטים וקבל הכוונה',exact=True).click()
    expect(page.locator('#intake-save-result')).to_be_visible()
    expect(page.locator('#intake-save-result')).to_contain_text('500 גרם')
    expect(page.locator('#intake-save-result')).to_contain_text('בגריל')
    assert page.evaluate('mentor.state.dish_identity.status')=='recognized'
    frame=page.frame_locator('#action-report-frame')
    frame.locator('#action-pages button').click()
    frame.locator('[data-catalog-action="grill"]').click()
    expect(frame.locator('#number-duration')).to_have_value('10')
    frame.locator('#save-report').click()
    expect(frame.locator('#history li')).to_have_count(1)
    expect(frame.locator('.timer')).to_have_count(1)
    page.locator('#choose-cooking-dish').click()
    page.locator('#custom-dish-title').fill('מרק ירקות')
    assert page.locator('#custom-method').input_value()==''
    page.locator('#close-dish-selection').click()
    assert not errors,errors
    print('Passed: real local recognition, grill-only intent, visible saved guidance, no text action form, structured grill report and timer.')
    browser.close()
