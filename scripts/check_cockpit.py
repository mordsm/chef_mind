"""Cockpit layout, modal dials and deterministic voice command integration."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1518,'height':900})
    errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
    page.add_init_script('''
      window._spoken=[];
      window.SpeechSynthesisUtterance=class{constructor(text){this.text=text;}};
      speechSynthesis.getVoices=()=>[{lang:'he-IL',localService:true}];
      speechSynthesis.cancel=()=>{};speechSynthesis.speak=u=>window._spoken.push(u.text);
      window.SpeechRecognition=class{constructor(){window._recognizer=this;}start(){this.onstart();}abort(){}};
    ''')
    page.goto(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8800')
    page.locator('#custom-dish-title').fill('עוף בגריל')
    page.locator('#start-work').click()
    expect(page.locator('#cooking-intake')).to_be_visible(timeout=45000)
    page.locator('#intake-source summary').click()
    page.locator('#intake-recipe_text').fill('קוצצים את שיני השום ומוסיפים לקערית.\nצולים את העוף בגריל לפי המתכון.')
    page.locator('#import-selected-recipe').click()
    expect(page.locator('#adopt-imported-recipe')).to_be_visible()
    page.locator('#adopt-imported-recipe').click()
    expect(page.locator('#attached-recipe')).to_be_visible()
    page.locator('#mode-live').click()
    expect(page.locator('.live-step-counter')).to_have_text('שלב 1 מתוך 2')
    expect(page.locator('#live-done')).to_be_visible()
    expect(page.locator('#live-done')).to_be_enabled()
    expect(page.locator('.micro-tip')).to_have_count(0)
    page.wait_for_timeout(300)
    right=page.locator('#cooking-live-stage').bounding_box()
    middle=page.locator('#inline-action-reporter').bounding_box()
    left=page.locator('#cockpit-voice').bounding_box()
    assert right['x']>middle['x']>left['x'],(right,middle,left)
    assert page.locator('.live-instruction').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')>=24
    frame=page.frame_locator('#action-report-frame')
    for action in ['cook','fry','cut','add']:expect(frame.locator(f'[data-action="{action}"]')).to_be_visible()
    frame.locator('[data-action="cook"]').click()
    expect(frame.locator('#parameter-dialog')).to_be_visible()
    expect(page.locator('body')).to_have_class(__import__('re').compile('action-modal-open'))
    assert page.locator('#cooking-live-stage').bounding_box()==right
    dial=frame.locator('[data-field="duration"] .round-dial')
    expect(dial).to_have_attribute('role','slider')
    dial.focus();dial.press('ArrowRight')
    expect(frame.locator('#number-duration')).to_have_value('31')
    before=frame.locator('#number-temperature').input_value()
    temperature=frame.locator('[data-field="temperature"] .round-dial')
    box=temperature.bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+10);page.mouse.down();page.mouse.move(box['x']+box['width']-10,box['y']+box['height']/2,steps=5);page.mouse.up()
    assert frame.locator('#number-temperature').input_value()!=before
    page.screenshot(path=str(root/'.runtime/cockpit-modal.png'),full_page=True)
    frame.locator('#cancel-report').click()
    expect(frame.locator('#parameter-dialog')).not_to_be_visible()
    expect(page.locator('#mode-prepare')).to_be_enabled()
    assert not page.locator('#cockpit-voice').evaluate('e=>e.inert')
    page.locator('#live-explain').click()
    assert page.evaluate('window._spoken.at(-1).split(/\\s+/).length')<=26
    assert 'חתיכות' in page.evaluate('window._spoken.at(-1)')
    page.locator('#live-microphone').click()
    expect(page.locator('#live-microphone')).to_have_attribute('aria-pressed','true')
    page.evaluate("window._recognizer.onresult({resultIndex:0,results:[{isFinal:true,0:{transcript:'השף, למה?'}}]})")
    expect(page.locator('#voice-last-transcript')).to_have_text('השף, למה?')
    assert page.locator('#work-report').input_value()==''
    assert page.evaluate('window._spoken.length')==2
    page.locator('#live-done').click()
    expect(page.locator('.live-step-counter')).to_have_text('שלב 2 מתוך 2')
    expect(page.locator('#live-done')).to_be_enabled()
    page.screenshot(path=str(root/'.runtime/cockpit-three-stations.png'),full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert not errors,errors
    browser.close()
print('Passed: three fixed stations, large current step, four shortcuts, modal drag/keyboard dials, preserved layout, short speech and spoken why command.')
