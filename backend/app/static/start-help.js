'use strict';
Object.assign(words.he, {
 basicKnowledge:'כדאי לדעת — שיטות הכנה ומנות דומות',inventoryAllergens:'אלרגנים מזוהים ברכיבים',noKnownAllergens:'לא זוהו אלרגנים בקטלוג; אין בכך אישור היעדר אלרגנים',
 'allergen_milk':'חלב','allergen_eggs':'ביצים','allergen_fish':'דגים','allergen_peanuts':'בוטנים','allergen_sesame':'שומשום','allergen_soy':'סויה','allergen_wheat':'חיטה','allergen_tree nuts':'אגוזים',
 details:'הסבר ומקורות',inventorySaveFailed:'שמירת המלאי בשרת לא הושלמה; הנתונים המקומיים נשמרו ככל האפשר.',ingredientHint:'',
 question:'מה תרצה לדעת? אפשר להשאיר ריק כדי לבקש איך להתחיל',
 reports:'מה כבר עשית או ראית? — לא חובה בתחילת הבישול',
 reportsHelp:'לפני שמתחילים אפשר להשאיר ריק. בהמשך כתוב, למשל: „חתכתי את הבצל” או „הרוטב עדיין דליל”. תנאי הוא עובדה שצריך לוודא לפני שימוש בשיטה; אין צורך לנחש מה לכתוב.',
 questionPlaceholder:'למשל: איך מתחילים להכין את המנה?',goalPlaceholder:'למשל: להכין כנפי הודו בתנור',
 firstMessage:'איך מתחילים להכין: ', working:'מכין הנחיה…',
 verified:'זמינות אומתה',labelVerified:'תווית נבדקה',ingredientAllergens:'אלרגנים',
 topicHeading:'הנושאים שיש לגביהם ידע מאושר כרגע',
 actualConditions:'האם העובדות הבאות נכונות עכשיו?',confirmCondition:'אני מאשר שזה המצב: ',
 scopeHelp:'הגרסה הנוכחית תומכת במספר נושאים נקודתיים, ולא בכל מנה. אם חסר ידע, יוצגו הנושאים הזמינים והסבר להמשך.',
 initialHelp:'מבקש הנחיה ראשונה? כתוב מה רוצים להכין והוסף מצרכים וכמויות. אין צורך לדווח על פעולות שעוד לא עשית.',
 requestSent:'הבקשה נשלחה. ההנחיה תופיע מיד בהמשך העמוד.',
 received:'התשובה מוכנה — כאן מופיעה ההנחיה או השאלה הבאה.',
 invalidForm:'יש למלא את מטרת הבישול ולבדוק שהכמויות תקינות.',
 topicSelected:'הנושא נבחר. אפשר לבקש הנחיה; אין לסמן עובדות שעדיין אינן נכונות.'
});
Object.assign(words.en, {
 basicKnowledge:'Cooking basics and similar dishes',inventoryAllergens:'Detected ingredient allergens',noKnownAllergens:'None identified in the catalog; this does not certify absence of allergens',
 'allergen_milk':'Milk','allergen_eggs':'Eggs','allergen_fish':'Fish','allergen_peanuts':'Peanuts','allergen_sesame':'Sesame','allergen_soy':'Soy','allergen_wheat':'Wheat','allergen_tree nuts':'Tree nuts',
 details:'Explanation and sources',inventorySaveFailed:'Server inventory save failed; local data retained where possible.',ingredientHint:'',
 question:'What would you like to know? Leave blank to ask how to start',
 reports:'What have you already done or observed? — optional before starting',
 reportsHelp:'Leave this empty before you start. Later, report facts such as “I chopped the onion” or “the sauce is still thin”. A condition is a fact that must hold before applying a technique; you do not need to guess the right wording.',
 questionPlaceholder:'For example: how do I start this dish?',goalPlaceholder:'For example: oven-roasted turkey wings',
 firstMessage:'How do I start preparing: ',working:'Preparing guidance…',
 verified:'Availability verified',labelVerified:'Label checked',ingredientAllergens:'Allergens',
 topicHeading:'Currently supported knowledge topics',actualConditions:'Are these facts true right now?',confirmCondition:'I confirm this is true: ',
 scopeHelp:'The current version supports a small set of specific topics, not every dish. Missing knowledge will show available topics and explain what is needed next.',
 initialHelp:'Asking for your first instruction? Enter the dish and add ingredients and quantities. You do not need to report actions you have not taken.',
 requestSent:'Request sent. Guidance will appear below.',received:'Your response is ready — guidance or the next clarification appears here.',
 invalidForm:'Enter a cooking goal and check ingredient quantities.',topicSelected:'Topic selected. Ask for guidance; confirm only facts that are already true.'
});
$('question').required=false;
const initialHelp=translated('p','initialHelp','form-help');
const scopeHelp=translated('small','scopeHelp');
$('cook-form').insertBefore(initialHelp,$('goal').previousElementSibling);
$('reports').insertAdjacentElement('afterend',translated('small','reportsHelp'));
$('cook-form').insertBefore(scopeHelp,$('ask').parentElement);
$('decision').setAttribute('aria-live','polite');$('decision').setAttribute('tabindex','-1');
function paintStartHelp(){ $('goal').placeholder=t('goalPlaceholder');$('question').placeholder=t('questionPlaceholder'); }
$('language').addEventListener('click',paintStartHelp);
$('cook-form').addEventListener('invalid',()=>notice('invalidForm',true),true);
for(const id of ['goal','question'])$(id).addEventListener('input',()=>document.querySelectorAll('[data-confirm-condition]').forEach(n=>n.checked=false));
document.addEventListener('chef-decision',event=>{
 const d=event.detail;
 // renderDecision emits this event before building its core content; append after that turn.
 queueMicrotask(()=>{
   if(d.missing_conditions?.length&&d.requires_confirmation!==false){const block=el('details','','condition-list');block.append(translated('summary','actualConditions'));
     for(const condition of d.missing_conditions){const input=el('input');input.type='checkbox';input.dataset.confirmCondition=condition;
       const label=el('label');label.append(input,translated('span','confirmCondition'),document.createTextNode(condition));block.append(label);}
     $('decision').append(block);
   }
   if(d.available_topics?.length){const block=el('details','','topic-list');block.append(translated('summary','topicHeading'));
     for(const topic of d.available_topics){const button=el('button',topic,'secondary');button.type='button';button.addEventListener('click',()=>{$('goal').value=topic;$('question').value='';document.querySelectorAll('[data-confirm-condition]').forEach(n=>n.checked=false);notice('topicSelected');$('goal').focus();});block.append(button);}
     $('decision').append(block);
   }
   $('decision').focus({preventScroll:true});$('decision').scrollIntoView({behavior:'instant',block:'start'});
 });
});
paintStartHelp();localize();

const inventoryHeader=el('div','','inventory-header');
for(const key of ['name','quantity','unit'])inventoryHeader.append(translated('span',key));
$('inventory').insertAdjacentElement('beforebegin',inventoryHeader);
const allergenSummary=el('div','','inventory-allergen-summary');allergenSummary.append(translated('strong','inventoryAllergens'),document.createTextNode(': '));
const allergenValue=el('span');allergenValue.id='inventory-allergens';allergenValue.setAttribute('aria-live','polite');allergenSummary.append(allergenValue);
$('inventory').insertAdjacentElement('afterend',allergenSummary);
$('language').addEventListener('click',()=>{displayInventoryAllergens();document.querySelectorAll('.inventory-item [data-field]').forEach(input=>input.setAttribute('aria-label',t(input.dataset.field)));});
displayInventoryAllergens();
document.addEventListener('chef-session-reset',()=>queueMicrotask(displayInventoryAllergens));
