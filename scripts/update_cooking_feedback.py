from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
def edit(name, old, new):
    p = root / name
    text = p.read_text(encoding='utf-8')
    assert old in text, (name, old[:80])
    p.write_text(text.replace(old, new), encoding='utf-8')

edit('backend/app/static/cooking-support.js', "learning.prepend(section);", "journey.prepend(section);")
edit('backend/app/static/cooking-support.js', "section.append(el('h3','מתכון, משפחה והפרטים שחסרים')", "section.append(el('h3','פרטי המנה וההכנה')")
edit('backend/app/static/cooking-support.js', "add('main_ingredient');", "add('main_ingredient',{'קורקבנים':'קורקבנים','חזה עוף':'חזה עוף','כרעיים':'כרעיים','בקר':'בקר','סלמון':'סלמון','גזר':'גזר','תפוח אדמה':'תפוח אדמה','אורז':'אורז','עדשים':'עדשים'});")
edit('backend/app/static/cooking-support.js', "for(const key of ['cut','quantity'])add(key);", "add('cut',{'שלם':'שלם','חצוי':'חצוי','קוביות קטנות':'קוביות קטנות','קוביות גדולות':'קוביות גדולות','פרוסות':'פרוסות','רצועות':'רצועות'});add('quantity',{'250 גרם':'250 גרם','500 גרם':'500 גרם','750 גרם':'750 גרם','1 ק״ג':'1 ק״ג','2 ק״ג':'2 ק״ג','1 כוס':'1 כוס','2 כוסות':'2 כוסות','4 יחידות':'4 יחידות'});")
edit('backend/app/static/cooking-support.js', "source.append(el('summary','הבא מתכון, קישור או תיאור מנה דומה'));", "source.append(el('summary','שמירת מתכון לעיון בלבד'),el('p','קישור נשמר כקיצור דרך לפתיחה. טקסט נשמר כפי שנכתב. אין כאן קריאה אוטומטית של האתר או פענוח טקסט לשלבי בישול; הבחירות המובנות למעלה הן שמשנות את ההכוונה.'));")
edit('backend/app/static/cooking-support.js', "const facts=Object.fromEntries(Object.entries(controls).map(([key,control])=>[key,control.value.trim()]));", "const facts={...state.intake_facts,...Object.fromEntries(Object.entries(controls).map(([key,control])=>[key,control.value.trim()]))};")
edit('backend/app/static/cooking-support.js', "supportDrafts.delete(state.id);renderCoach();", "supportDrafts.delete(state.id);renderCoach();const saved=el('p','הפרטים נשמרו. ההכוונה עודכנה לפי הבחירות שלך; הפרט הבא שחסר מופיע כאן.','intake-saved');saved.setAttribute('role','status');$('cooking-intake')?.prepend(saved);")
edit('backend/app/static/cooking-support.js', "control.value=draft[key]||((key==='family')?info.family:'');", "const current=draft[key]||((key==='family')?info.family:'');if(choices&&current&&![...control.options].some(option=>option.value===current)){const existing=el('option',current+' (נשמר קודם)');existing.value=current;control.append(existing);}control.value=current;")
# Keep one preparation area. Existing chef-specific questions retain their handlers.
edit('backend/app/static/cooking-support.js', "journey.prepend(section);", "journey.prepend(section);const questions=$('status-question')||statusQuestion;for(const group of [...questions.querySelectorAll('.decision-question')])section.append(group);")
edit('backend/app/static/cooking-support.js', "if(info.recipe_search_url?.startsWith", "for(const item of info.recipe_search_links||[]){const link=el('a',item.label);link.href=item.url;link.target='_blank';link.rel='noopener noreferrer';section.append(link,el('br'));}\n if(!info.recipe_search_links?.length&&info.recipe_search_url?.startsWith")
edit('backend/app/cooking_intake.py', '    state["intake_guidance"] = {', '''    exact_query = facts["main_ingredient"].strip() or state["dish_title"]
    if exact_query in ("מנה לבחירה", ""):
        exact_query = FAMILIES.get(family, "מנה")
    search_links = [
        {"label": "חיפוש מתכונים בעברית: " + exact_query, "url": "https://www.google.com/search?" + urlencode({"q": exact_query + " מתכון"})},
        {"label": "חיפוש ב־השולחן", "url": "https://www.google.com/search?" + urlencode({"q": "site:hashulchan.co.il " + exact_query + " מתכון"})},
        {"label": "חיפוש ב־mako אוכל", "url": "https://www.google.com/search?" + urlencode({"q": "site:mako.co.il/food " + exact_query + " מתכון"})},
    ]
    state["intake_guidance"] = {
        "recipe_search_links": search_links,''')
edit('backend/app/static/kitchen-focus.js', "if(!safety&&!tip.classList.contains('book-knowledge-tip'))background.append(tip);", "if(!tip.classList.contains('book-knowledge-tip'))background.append(tip);")
edit('backend/app/static/kitchen-focus.js', "למה ומה לבדוק בפעולה הזאת", "הסבר נוסף ובדיקת מוכנות לפני הגשה")
edit('backend/app/culinary_context.py', 'safety_text = f"סף הבישול הכללי לחומרי הגלם שזוהו: {minimum:g}°C."', 'safety_text = f"לפני הגשה: מדוד במדחום בחלק העבה של המזון, בלי לגעת בעצם. נדרשים לפחות {minimum:g}°C."')
edit('backend/app/culinary_context.py', 'safety_text += " אין להשתמש בטמפרטורת המרקם שבמסמך כאישור בטיחות."', 'safety_text += " חום התנור או הנוזל וזמן הבישול אינם מדידה של פנים המזון."')
edit('backend/app/static/report/sw.js', 'chef-report-shell-v4', 'chef-report-shell-v5')
edit('backend/app/static/report/app.js', "closeForm();message('הפעולה נשמרה במכשיר.');await draw();void flush();", "closeForm();message('הפעולה נשמרה במכשיר.');await draw();showActionCheck(report);void flush();")
edit('backend/app/static/report/app.js', "async function saveEntry(row,kind='put'){", '''// Finite checks use only action IDs and explicit choices, never notes or an LLM.
function showActionCheck(report){
 const checks={
 cook:{question:'הבישול נרשם והטיימר התחיל. מה המצב עכשיו?',options:[['עדיין מתחמם','המשך לחמם ובדוק שוב כשמופיעות בועות.'],['בעבוע עדין','אם המטרה ריכוך בסיר, שמור על בעבוע עדין ובדוק שיש מספיק נוזל.'],['רתיחה חזקה','אם המטרה ריכוך ממושך, הנמך עד לבעבוע עדין.'],['בישול בתנור','בדוק שהכלי מתאים לתנור. בסיום הזמן בדוק את המזון עצמו; הטיימר אינו אישור מוכנות.']]},
 cut:{question:'החיתוך נרשם. החתיכות בגודל דומה?',options:[['כן','אפשר להמשיך לשלב הבא במתכון.'],['לא','חתוך את החתיכות הגדולות יותר כדי שיתבשלו באופן דומה.']]},
 add:{question:'ההוספה נרשמה. האם הכמות והיחידה נכונות?',options:[['כן','המשך לשלב הבא במתכון; אם הוספת נוזל קר, בדוק שוב את מצב הבעבוע.'],['צריך לתקן','פתח עריכה בשורת הדיווח ועדכן את הכמות או היחידה.']]}
 };
 const check=checks[report.action_type];if(!check)return;
 let panel=$('action-check');if(!panel){panel=document.createElement('section');panel.id='action-check';panel.setAttribute('aria-live','polite');$('parameters').insertAdjacentElement('afterend',panel);}panel.replaceChildren();
 const question=document.createElement('h3');question.textContent=check.question;panel.append(question);
 for(const [label,reply]of check.options){const button=document.createElement('button');button.type='button';button.textContent=label;button.style.minHeight='48px';button.addEventListener('click',()=>{panel.replaceChildren();const answer=document.createElement('p');answer.textContent=reply;panel.append(answer);});panel.append(button);}
}
async function saveEntry(row,kind='put'){''')
print('Updated cooking preparation, precise searches, action checks and safety notes.')
