'use strict';
// A shared, editable dictionary. Definitions use everyday language.
const culinaryTerms=[
 {term:'שמרי אינסטנט',meaning:'סוג של שמרים יבשים שבדרך כלל אפשר לערבב ישירות בקמח. בדוק גם את הוראות האריזה. הם אינם שמרים טריים, ולכן לא מחליפים ביניהם לפי אותו משקל.'},
 {term:'שמרים יבשים פעילים',meaning:'סוג של שמרים יבשים שעשוי לפעול לאט יותר משמרי אינסטנט. בדוק אם האריזה מבקשת להמיס אותם קודם במים; אל תוסיף זמן קבוע בלי לבדוק את תפיחת הבצק.'},
 {term:'תפיחה',meaning:'הבצק גדל ונעשה אוורירי בגלל גז שהשמרים יוצרים. בודקים התרחבות ובועות; שעון לבדו אינו אומר שהבצק מוכן לשלב הבא.'},
 {term:'HACCP',meaning:'שיטה למניעת בעיות במזון: מזהים מה עלול להשתבש, קובעים מה לבדוק ומתעדים את הבדיקה. למשל, מודדים חום במרכז הדג ובודקים שהמקרר קר מספיק.'},
 {term:'FDA',meaning:'רשות המזון והתרופות של ארצות הברית. כאן משתמשים במדריכים שלה כמקור למידע על הכנה ואחסון של מזון.'},
 {term:'שליקה',meaning:'בישול בתוך נוזל חם שאינו רותח בחוזקה. מכוונים את האש לפי מדידת חום הנוזל. בדגים זו דרך לבשל בעדינות בלי לפרק את הנתח.'},
 {term:'קולגן',meaning:'חלק מהרקמה שמחזיקה את בשר הדג יחד. הוא מתרכך בחימום, ולכן הדג עלול להתפרק אם מבשלים אותו יותר מדי.'},
 {term:'גיאוזמין',aliases:['גאוסמין','geosmin'],meaning:'חומר בעל ריח אדמתי שעשוי להימצא בחלק מהדגים. הופעת המילה כאן אינה אומרת שהוא נמצא בדג שלך.'},
 {term:'2-MIB',meaning:'שם מקוצר של חומר שעשוי לתת ריח אדמתי לחלק מהדגים. אין כאן המלצה להשריה שמבטיחה להסיר אותו.'},
 {term:'טמפרטורת ליבה',aliases:['יעד הליבה','ליבת הדג'],meaning:'החום במרכז החלק העבה של המזון. מודדים במדחום בתוך הנתח, ולא ברוטב שסביבו.'},
 {term:'חום שיורי',meaning:'הדג עשוי להמשיך להתחמם מעט גם אחרי שמוציאים אותו מהסיר. בהנחיה שלנו מסיימים למדוד ולבשל בסיר, ולא סומכים על ההמשך הזה.'},
 {term:'זמן החזקה',meaning:'הזמן שבו מרכז המזון צריך להישאר בחום המבוקש, אחרי שכבר הגיע אליו. הוא אינו כולל את הזמן שלקח להתחמם.'},
 {term:'מדחום מחט',meaning:'מדחום בעל קצה דק שמכניסים למרכז הנתח. הקצה אינו צריך לגעת בסיר או בעצם.'},
 {term:'תמלחת',meaning:'מים עם מלח שמשרים בהם מזון. משתמשים רק בכמות ובמשך שמתאימים למתכון; בהכנת הדג הנוכחית אין צורך בכך.'},
 {term:'אלרגנים',meaning:'מרכיבים שעלולים לגרום לתגובה אלרגית אצל מי שרגיש להם, למשל דגים, חלב או חיטה.'},
 {term:'חומצה',meaning:'בתיבול הכוונה בדרך כלל ללימון או לחומץ. מוסיפים מעט וטועמים. זה לא אותו דבר כמו השריית דג לפני הבישול.'},
 {term:'אמולסיה',meaning:'תערובת של שמן ונוזל שמפוזרים זה בזה בטיפות קטנות, כמו במיונז. במילים פשוטות: רוטב אחיד במקום שמן שצף בנפרד.'},
 {term:'דנטורציה',meaning:'שינוי במבנה של חלבונים, למשל בזמן חימום. זה חלק ממה שגורם לביצה להתייצב ולבשר דג להשתנות בזמן בישול.'},
 {term:'קרמליזציה',meaning:'השחמה של סוכר בחימום שנותנת צבע וטעם, כמו בקרמל. לא כל השחמה במחבת היא קרמליזציה.'},
 {term:'תגובת מייאר',meaning:'תגובות בין סוכרים לחלבונים בחימום שיוצרות צבע חום וטעמי קלייה, למשל בקרום של לחם.'},
 {term:'חליטה',meaning:'הכנסה קצרה למים חמים או רותחים, לעיתים כדי לרכך מעט או לעזור לקלף. משך הזמן תלוי במזון.'},
 {term:'צמצום רוטב',meaning:'בישול רוטב ללא מכסה כדי שחלק מהמים יתאדו והוא יהיה סמיך יותר. טועמים לפני שמוסיפים מלח, כי גם המליחות מתחזקת.'},
 {term:'Mise en place',meaning:'להכין מראש את מה שצריך: כלי עבודה, חומרי גלם מדודים ומשטח מסודר, לפני שמתחילים לבשל.'},
 {term:'Knowledge Base Extension Needed',meaning:'סימון פנימי שאומר שחסר במאגר פרט מעשי. הוא אינו אומר שצריך להוסיף שוב ספר שכבר נמצא במאגר.'}
];
let culinaryGlossaryDialog,culinaryGlossaryTitle,culinaryGlossaryBody,culinaryGlossaryReturn;
function openCulinaryTerm(entry,origin){
 culinaryGlossaryReturn=origin;culinaryGlossaryTitle.textContent=entry?.term||'מילון בישול בשפה פשוטה';culinaryGlossaryBody.replaceChildren();
 for(const item of entry?[entry]:culinaryTerms){const title=document.createElement('h3'),text=document.createElement('p');title.textContent=item.term;text.textContent=item.meaning;culinaryGlossaryBody.append(title,text);}
 culinaryGlossaryDialog.showModal();
}
document.addEventListener('DOMContentLoaded',()=>{
 culinaryGlossaryDialog=document.createElement('dialog');culinaryGlossaryDialog.id='culinary-glossary-dialog';culinaryGlossaryDialog.dir='rtl';culinaryGlossaryDialog.setAttribute('aria-labelledby','culinary-glossary-title');
 culinaryGlossaryTitle=document.createElement('h2');culinaryGlossaryTitle.id='culinary-glossary-title';culinaryGlossaryBody=document.createElement('div');
 const close=document.createElement('button');close.type='button';close.textContent='סגור הסבר';close.addEventListener('click',()=>culinaryGlossaryDialog.close());
 culinaryGlossaryDialog.addEventListener('close',()=>culinaryGlossaryReturn?.focus());culinaryGlossaryDialog.append(culinaryGlossaryTitle,close,culinaryGlossaryBody);document.body.append(culinaryGlossaryDialog);
 const all=document.createElement('button');all.type='button';all.id='culinary-glossary-open';all.textContent='מילון בישול';all.addEventListener('click',()=>openCulinaryTerm(null,all));(document.querySelector('header .tools')||document.body).append(all);
 const aliases=new Map();for(const entry of culinaryTerms)for(const label of [entry.term,...(entry.aliases||[])])aliases.set(label.toLowerCase(),entry);
 const escaped=[...aliases.keys()].sort((a,b)=>b.length-a.length).map(s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'));
 const pattern=new RegExp(escaped.join('|'),'gi');
 const scopes='#active-work-guidance,#decision,#cooking-intake,#kitchen-dialog,.book-knowledge-tip';
 function annotate(){
  for(const root of document.querySelectorAll(scopes)){
   const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
   for(const node of nodes){
    if(node.parentElement.closest('button,a,summary,script,style,textarea,select,[data-station-block="5"],#culinary-glossary-dialog'))continue;
    const matches=[...node.textContent.matchAll(pattern)];if(!matches.length)continue;
    const fragment=document.createDocumentFragment();let offset=0;
    for(const match of matches){const before=node.textContent[match.index-1]||'',after=node.textContent[match.index+match[0].length]||'';if(/[\p{L}\p{N}]/u.test(before)||/[\p{L}\p{N}]/u.test(after))continue;
     fragment.append(document.createTextNode(node.textContent.slice(offset,match.index)));const button=document.createElement('button');button.type='button';button.className='culinary-term';button.textContent=match[0];button.setAttribute('aria-label','הסבר: '+match[0]);button.setAttribute('aria-haspopup','dialog');button.addEventListener('click',()=>openCulinaryTerm(aliases.get(match[0].toLowerCase()),button));fragment.append(button);offset=match.index+match[0].length;
    }
    if(offset){fragment.append(document.createTextNode(node.textContent.slice(offset)));node.replaceWith(fragment);}
   }
  }
 }
 let pending=false;const observer=new MutationObserver(()=>{if(!pending){pending=true;queueMicrotask(()=>{pending=false;observer.disconnect();annotate();observer.observe(document.body,{childList:true,subtree:true});});}});
 annotate();observer.observe(document.body,{childList:true,subtree:true});
});
