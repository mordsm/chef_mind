'use strict';
Object.assign(words.he,{title:'השף שלצידך',subtitle:'מבשלים, שואלים ולומדים — צעד אחר צעד.'});
Object.assign(words.en,{title:'Your cooking companion',subtitle:'Cook, ask and learn — one step at a time.'});
// The coach owns the primary experience. Existing review/knowledge tools remain available.
const mentor={recipes:[],state:null,busy:false,lastActive:Date.now(),image:null};
const cookView=$('cook'),oldGrid=cookView.querySelector('.grid');
const advanced=el('details','','coach-advanced');advanced.id='coach-settings';advanced.append(el('summary','המלאי שלי, התאמות ומקורות'));advanced.append(oldGrid);
const home=el('section','','coach-home');home.id='coach-home';home.append(el('h2','מה מבשלים היום?'));
const dishChoices=el('div','','dish-choices');home.append(dishChoices);
const guestBanner=el('p','','coach-mode');guestBanner.id='coach-mode';home.append(guestBanner);
const workspace=el('div','','coach-workspace');workspace.id='coach-workspace';
const journey=el('section','','panel journey-panel');journey.id='journey-panel';
const companion=el('section','','panel companion-panel');companion.id='companion-panel';
const learning=el('aside','','panel learning-panel');learning.id='learning-panel';
workspace.append(journey,companion,learning);
cookView.prepend(home,workspace);cookView.append(advanced);
const connection=document.querySelector('.connection');const connectionDetails=el('details','','connection-details');
const connectionSummary=el('summary','חיבור למטבח האישי ושחזור מלאי');connectionDetails.append(connectionSummary);
while(connection.firstChild)connectionDetails.append(connection.firstChild);connection.append(connectionDetails);
const publicIntro=el('p','אפשר להתחיל לבשל מיד. התחברות נדרשת לשחזור המלאי והבישולים האישיים.','connection-intro');connection.prepend(publicIntro);
const speechTarget=el('div');speechTarget.id='coach-voice-slot';
const companionHeading=el('div','','companion-heading');companionHeading.append(el('span','🧑‍🍳','chef-avatar'),el('h2','השף שלך'));
const personality=el('select');personality.id='chef-personality';personality.setAttribute('aria-label','סגנון השף');
for(const [value,label] of [['supportive','מעודד'],['professional','מקצועי'],['tough','ישיר וקשוח']]){const option=el('option',label);option.value=value;personality.append(option);}personality.value='professional';companionHeading.append(personality);
const conversation=el('div','','chef-conversation');conversation.id='chef-conversation';conversation.setAttribute('role','log');conversation.setAttribute('aria-live','polite');
const statusQuestion=el('div','','status-question');statusQuestion.id='status-question';
const actions=el('div','','coach-actions');
function actionButton(id,text,fn,className='secondary'){const button=el('button',text,className);button.id=id;button.type='button';button.addEventListener('click',fn);return button;}
const doneButton=actionButton('coach-done','✓ סיימתי',()=>coachCommand('complete'),'');
const problemButton=actionButton('coach-problem','יש בעיה',()=>{mentor.problemOpen=true;void coachCommand('problem');});
const photoButton=actionButton('coach-photo','📷 תמונה',()=>photoInput.click());
const talkButton=actionButton('coach-talk','🎙 דבר איתי',()=>document.dispatchEvent(new CustomEvent('coach-dictate',{detail:{target:'coach-question'}})));
actions.append(doneButton,problemButton,photoButton,talkButton);
const photoInput=el('input');photoInput.type='file';photoInput.accept='image/jpeg,image/png,image/webp';photoInput.hidden=true;photoInput.id='coach-photo-input';
const photoPreview=el('div','','photo-preview');photoPreview.id='coach-photo-preview';
const chatForm=el('form','','coach-chat');chatForm.id='coach-chat';
const chatInput=el('textarea');chatInput.id='coach-question';chatInput.rows=2;chatInput.maxLength=2000;chatInput.placeholder='תשובה או שאלה לשף';chatInput.setAttribute('aria-label','תשובה או שאלה לשף');
const sendQuestion=el('button','שלח תשובה / שאלה לשף');sendQuestion.type='submit';sendQuestion.id='coach-ask';
chatForm.append(el('label','התשובה שלך לשף'),chatInput,sendQuestion);
chatForm.firstChild.htmlFor='coach-question';
talkButton.textContent='🎙 הקלד שאלה בקול';chatForm.insertBefore(talkButton,chatInput);
chatInput.addEventListener('keydown',event=>{if(event.key==='Enter'&&!event.shiftKey&&!event.isComposing){event.preventDefault();if(!mentor.busy)chatForm.requestSubmit();}});
const coachNotice=el('p','','coach-notice');coachNotice.id='coach-notice';coachNotice.setAttribute('role','status');
companion.append(companionHeading,conversation,statusQuestion,actions,photoInput,photoPreview,chatForm,speechTarget,coachNotice);
const resumeButton=actionButton('coach-resume','המשך בישול',()=>{workspace.scrollIntoView({block:'start',behavior:'smooth'});if(mentor.state?.status==='paused')void coachCommand('resume');});home.append(resumeButton);resumeButton.hidden=true;
const inventoryDrawer=el('details','','inventory-drawer');inventoryDrawer.id='inventory-drawer';const inventorySummary=el('summary','המלאי שלי — צפייה ועריכה');inventoryDrawer.append(inventorySummary,$('inventory').closest('fieldset'));advanced.insertBefore(inventoryDrawer,oldGrid);
const openInventory=actionButton('open-inventory','המלאי שלי — צפייה, הוספה ועדכון',()=>{advanced.open=true;inventoryDrawer.open=true;inventoryDrawer.scrollIntoView({block:'start',behavior:'smooth'});});home.append(openInventory);
const inventoryShortcut=actionButton('settings-inventory','פתיחת המלאי שלי',()=>openInventory.click());oldGrid.insertAdjacentElement('beforebegin',inventoryShortcut);
const newDish=actionButton('coach-new-dish','מנה לבחירתך',()=>{$('custom-dish-title')?.focus();});dishChoices.append(newDish);
const inventoryStatus=el('p','','inventory-status');inventoryStatus.id='inventory-status';
const palette=el('div','','ingredient-palette');
const history=el('select');history.id='inventory-history';history.setAttribute('aria-label','שחזור מלאי קודם');history.hidden=true;
$('inventory').insertAdjacentElement('beforebegin',inventoryStatus);inventoryStatus.insertAdjacentElement('afterend',palette);$('inventory').insertAdjacentElement('afterend',history);document.querySelector('.inventory-header')?.remove();
const knownIngredients=[['בצל','onion','🧅','יח׳'],['שום','garlic','🧄','שיניים'],['עגבנייה','tomato','🍅','יח׳'],['גזר','carrot','🥕','יח׳'],['תפוח אדמה','potato','🥔','יח׳'],['ביצה','egg','🥚','יח׳'],['עוף','chicken','🍗','יח׳'],['כנפי הודו','turkey wings','🦃','יח׳'],['בקר','beef','🥩','יח׳'],['דג','fish','🐟','יח׳'],['חלב','milk','🥛','כוסות'],['אורז','rice','🍚','כוסות'],['קמח חיטה','wheat flour','🌾','כוסות'],['שמן זית','olive oil','🫒','כפות'],['מלח','salt','🧂','כפיות']];
const matchIngredient=(value,entry)=>{const normalize=value=>value.normalize('NFC').trim().toLowerCase();const names=[entry[0],entry[1],...(entry[1]==='tomato'?['עגבניה','עגבניות','tomatoes']:[])];const node=graphIngredientCatalog.find(node=>node.aliases.some(alias=>names.some(name=>normalize(name)===normalize(alias))));return [...names,...(node?.aliases||[])].some(alias=>normalize(alias)===normalize(value));};
knownIngredients.splice(5,0,['חציל','eggplant','🍆','יח׳'],['קישוא','zucchini','🥒','יח׳'],['בשר טחון','ground beef','🥩','ק״ג']);
for(const entry of knownIngredients){const button=el('button','','ingredient-choice');button.type='button';button.dataset.ingredient=entry[1];const badge=el('span','0','ingredient-count');button.append(el('span',entry[2],'ingredient-emoji'),el('span',entry[0]),badge);palette.append(button);button.addEventListener('click',()=>{let row=[...$('inventory').children].find(row=>matchIngredient(row.querySelector('[data-field="name"]').value,entry));if(row){const quantity=row.querySelector('[data-field="quantity"]');quantity.value=String((Number(quantity.value)||0)+1);}else addInventory({name:entry[0],quantity:1,unit:entry[3]});saveInventory();paintInventory();});}
let historicalInventories=[];
function paintInventory(){
 const items=inventory();inventoryStatus.textContent=identityUser?'המלאי האישי מחובר. שינויים נשמרים אוטומטית.':'המלאי האישי ייטען אחרי התחברות למעלה. אפשר להוסיף רכיבים לבישול המקומי.';
 inventorySummary.textContent=`המלאי שלי · ${items.length} רכיבים`;
 knownIngredients.forEach((entry,index)=>{const matches=items.filter(item=>matchIngredient(item.name,entry)),item=matches[0],units=[...new Set(matches.map(item=>item.unit||entry[3]))];const amount=units.length<=1?String(matches.reduce((sum,item)=>sum+(item.quantity??0),0)):matches.map(item=>`${item.quantity??0} ${item.unit||entry[3]}`).join(' · ');const button=palette.children[index];button.querySelector('.ingredient-count').textContent=amount;button.classList.toggle('selected',matches.length>0);button.setAttribute('aria-label',`${entry[0]}: ${amount} ${units.length<=1?(item?.unit||entry[3]):''}; לחיצה מוסיפה אחת ביחידת הרשומה הקיימת`);});
}
async function loadInventoryArchive(){
 const epoch=authEpoch;if(!identityUser)return;
 try{const result=await api('/v1/inventory/history');if(epoch!==authEpoch)return;historicalInventories=result.items||[];history.replaceChildren(el('option','שחזור מלאי מבישול קודם…'));history.firstElementChild.value='';historicalInventories.forEach((entry,index)=>{const option=el('option',`${entry.goal||'בישול קודם'} · ${entry.inventory.length} רכיבים`);option.value=String(index);history.append(option);});history.hidden=!historicalInventories.length;
 let hasCopy=true;try{hasCopy=!!localStorage.getItem(inventoryKey());}catch{}
 if(!inventory().length&&!hasCopy&&historicalInventories.length){historicalInventories[0].inventory.forEach(addInventory);saveInventory();}paintInventory();
 }catch{notice('inventorySaveFailed',true);}
}
history.addEventListener('change',()=>{if(history.value==='')return;const selected=historicalInventories[Number(history.value)];if(!selected)return;$('inventory').replaceChildren();selected.inventory.forEach(addInventory);saveInventory();paintInventory();history.value='';});
$('inventory').addEventListener('input',()=>queueMicrotask(paintInventory));$('inventory').addEventListener('click',()=>queueMicrotask(paintInventory));
document.addEventListener('chef-inventory-loaded',()=>{connectionDetails.open=false;connectionSummary.textContent='מחובר למטבח האישי · '+identityUser;publicIntro.textContent='המלאי וההתקדמות משוחזרים מהמטבח האישי.';paintInventory();void loadInventoryArchive();void restoreCoach();});
async function publicApi(path,body){const controller=new AbortController();const deadline=setTimeout(()=>controller.abort(),15000);try{const response=await fetch(path,{method:body?'POST':'GET',headers:{'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined,signal:controller.signal,cache:'no-store'});if(!response.ok){let code='',message='';try{const payload=await response.json();code=payload.code;message=payload.message;}catch{}if(code==='METHOD_NOT_RECOMMENDED'){const error=new Error(message);error.methodPolicy=true;throw error;}throw new Error(code==='ALLERGEN_CONFLICT'?'allergenConflict':code==='SAFETY_HOLD'?'safetyHold':response.status===409?'stateConflict':'error');}return await response.json();}finally{clearTimeout(deadline);}}
function currentRecipe(){if(mentor.state?.workflow==='user')return {id:'custom',title:mentor.state.dish_title,steps:mentor.state.custom_steps};return mentor.recipes.find(recipe=>recipe.id===mentor.state?.recipe_id);}
function currentSmartStep(){return currentRecipe()?.steps[mentor.state.current_step];}
async function coachCommand(action,extra={}){
 if(mentor.busy){coachNotice.textContent='ממתין לסיום הבקשה הקודמת. הדיווח טרם נשלח.';return null;}
 const existing=mentor.state;
 const progressed=existing&&(existing.workflow==='user'?(existing.custom_steps.length>0||existing.report_count>0||existing.safety_hold):existing.current_step>0||existing.stage_valid||existing.safety_hold);
 if(['start','start_custom'].includes(action)&&existing&&['active','paused'].includes(existing.status)&&progressed&&!confirm('להתחיל עבודה חדשה במקום ״'+(existing.dish_title||currentRecipe()?.title||'העבודה הקודמת')+'״?'))return;
 const epoch=authEpoch;mentor.busy=true;coachNotice.textContent='מעדכן…';setCoachBusy(true);
 try{
   const command={action,forbid_meat_dairy:$('kosher').checked,expected_revision:mentor.state?.revision||0,journey_id:mentor.state?.id||'',chefPersonality:personality.value,allergies:$('allergies').value.split(',').map(value=>value.trim()).filter(Boolean),hazard_resolved:!!$('coach-hazard-resolved')?.checked,...extra};
   const state=identityUser?await api('/v1/coach/events','POST',command):await publicApi('/v1/coach/preview',{state:['start','start_custom'].includes(action)?null:mentor.state,command});
   if(epoch!==authEpoch)return;mentor.state=state;if(extra.problem_id)mentor.problemOpen=false;
   if(!identityUser){try{localStorage.setItem('chef-coach-guest-v1',JSON.stringify(state));}catch{coachNotice.textContent='הדפדפן אינו מאפשר שמירה מקומית.';}}
   if(['start','start_custom'].includes(action)){$('goal').value=currentRecipe().title;restoredWork.textContent='';restoredWork.hidden=true;}
   coachNotice.textContent='';renderCoach();document.dispatchEvent(new CustomEvent('coach-guidance',{detail:{instruction:state.messages.at(-1)?.text||'',safety_flags:[]}}));return state;
 }catch(error){if(epoch!==authEpoch)return;coachNotice.textContent=error.methodPolicy?error.message:error.message==='stateConflict'?'הבישול השתנה בלשונית אחרת. המצב ייטען מחדש.':error.message==='allergenConflict'?'המנה מכילה אלרגן שסימנת להימנעות. בחר מנה מתאימה.':error.message==='safetyHold'?'יש לטפל בסיכון ולאשר שטופל לפני שממשיכים.':'לא ניתן לעדכן כרגע. השלב לא קודם; נסה שוב.';if(error.methodPolicy)document.dispatchEvent(new CustomEvent('chef-method-policy-error',{detail:error.message}));if(error.message==='stateConflict')void restoreCoach();}
 finally{mentor.busy=false;setCoachBusy(false);}
}
function setCoachBusy(value){for(const button of workspace.querySelectorAll('button'))button.disabled=value;}
function renderCoach(){
 const state=mentor.state,recipe=currentRecipe(),step=currentSmartStep();
 guestBanner.textContent=identityUser?'מחובר למטבח האישי — ההתקדמות נשמרת בשרת.':'בישול מקומי — ההתקדמות נשמרת בדפדפן הזה. לשחזור מלאי קודם יש להתחבר.';
 resumeButton.hidden=!state;
 journey.replaceChildren();learning.replaceChildren();conversation.replaceChildren();statusQuestion.replaceChildren();
 if(state?.workflow==='user'&&typeof renderUserWorkbench==='function'){renderUserWorkbench();return;}
 if(!state||!recipe||!step){journey.append(el('h2','בוחרים מנה ומתחילים'),el('p','השלב הנוכחי, בדיקות המצב וההמשך יופיעו כאן.'));conversation.append(el('p','אני כאן כדי ללוות אותך. בחר מנה, ובכל שלב ספר מה קורה בפועל.'));learning.append(el('h2','💡 יסוד ברגע הנכון'),el('p','כאן יופיע הסבר קצר שמתאים לשלב שלך.'));actions.hidden=true;chatForm.hidden=true;return;}
 actions.hidden=false;chatForm.hidden=state.status==='completed';personality.value=state.chefPersonality;
 const completed=state.status==='completed'?recipe.steps.length:state.current_step,percentage=Math.round(completed/recipe.steps.length*100);
 journey.append(el('span',state.status==='paused'?'מושהה':state.status==='completed'?'המסלול הושלם':'בישול בתהליך','badge'),el('h2',recipe.title));
 const progress=el('progress');progress.max=100;progress.value=percentage;progress.setAttribute('aria-label','התקדמות לפי שלבים שאושרו');journey.append(progress,el('p',`${percentage}% · ${completed} מתוך ${recipe.steps.length} שלבים הושלמו`,'journey-progress'));
 const steps=el('ol','','journey-steps');recipe.steps.forEach((entry,index)=>{const item=el('li',`${index<completed?'✓ ':index===state.current_step&&state.status!=='completed'?'▶ ':''}${entry.title}`);if(index===state.current_step)item.setAttribute('aria-current','step');if(index<completed)item.className='completed-step';steps.append(item);});journey.append(steps);
 if(state.status!=='completed'){
   const current=el('div','','current-step');current.append(el('small','השלב הנוכחי'),el('h3',step.title),el('p',step.instruction));journey.append(current);
   const timer=el('output','00:00','coach-clock');timer.id='coach-clock';timer.setAttribute('aria-label','זמן עד בדיקת המצב');journey.append(timer);
   const timerTools=el('div','','row');const seconds=el('input');seconds.type='number';seconds.min=1;seconds.max=14400;seconds.value='180';seconds.id='coach-timer-seconds';seconds.setAttribute('aria-label','תזכורת לבדיקה בשניות');
   const timerStart=actionButton('coach-timer-start','הפעל תזכורת',()=>{const value=Number(seconds.value);if(!Number.isInteger(value)||value<1||value>14400){coachNotice.textContent='יש להזין מספר שניות בין 1 ל־14400.';return;}void coachCommand('timer',{seconds:value});});
   const pause=actionButton('coach-pause',state.status==='paused'?'המשך':'השהה ליווי',()=>coachCommand(state.status==='paused'?'resume':'pause'));timerTools.append(seconds,timerStart,pause);journey.append(timerTools);
   if(state.safety_hold){const confirm=el('input');confirm.type='checkbox';confirm.id='coach-hazard-resolved';const label=el('label');label.append(confirm,document.createTextNode('טיפלתי בסיכון ודיווחתי שהמצב מאפשר לחזור לבישול'));journey.append(label);}
   journey.append(el('p',recipe.steps[state.current_step+1]?'הבא: '+recipe.steps[state.current_step+1].title:'הבא: סיום והגשה','next-step'));
   const remaining=recipe.steps.slice(state.current_step).reduce((total,item)=>total+item.estimated_seconds,0);journey.append(el('small',remaining?`אומדן זמני בדיקה שנותרו: כ־${Math.ceil(remaining/60)} דקות; לא זמן סיום מובטח.`:'ההתקדמות נקבעת לפי בדיקת המצב.'));
 }
 for(const message of state.messages.slice(-6)){const bubble=el('p',message.text,message.role==='user'?'chat-bubble user-bubble':'chat-bubble chef-bubble');conversation.append(bubble);}conversation.scrollTop=conversation.scrollHeight;
 doneButton.hidden=state.status!=='active';doneButton.textContent=state.stage_valid?'✓ סיימתי — לשלב הבא':'✓ סיימתי — בדיקת מצב';problemButton.hidden=state.status!=='active';chatForm.hidden=state.status!=='active';
 if(state.status==='active'){
   statusQuestion.append(el('h3',step.chefQuestions[0]));
   if(step.minimum_temperature!==null){const temperature=el('input');temperature.type='number';temperature.min=-50;temperature.max=300;temperature.step='0.1';temperature.id='coach-temperature';temperature.placeholder='°C';temperature.setAttribute('aria-label','טמפרטורה שנמדדה בחלקים העבים');const submit=actionButton('coach-temperature-submit','דיווח מדידה',()=>{if(!temperature.value||!Number.isFinite(Number(temperature.value))){coachNotice.textContent='יש להזין מדידה אמיתית.';return;}void coachCommand('answer',{temperature:Number(temperature.value)});});statusQuestion.append(temperature,submit);}
   else for(const option of step.options){const button=actionButton('answer-'+option.id,option.label,()=>coachCommand('answer',{answer:option.id}));button.dataset.answer=option.id;statusQuestion.append(button);}
 }
 learning.append(el('h2','💡 '+step.title),el('h3','למה עושים את זה?'),el('p',step.why),el('h3','טעות נפוצה'),el('p',step.commonMistakes[0]),el('h3','מה לבדוק'),el('p',step.successCriteria[0]));
 const recovery=el('details');recovery.append(el('summary','אם משהו השתבש'),el('p',step.recoveryInstructions[0]));learning.append(recovery);const source=el('a','מקור והרחבה');source.href=step.source;source.target='_blank';source.rel='noopener noreferrer';learning.append(source,el('small','מסלול פתיחה לימודי. הזמנים הם תזכורות משוערות לבדיקה.'));
 paintClock();
}
function paintClock(){const clock=$('coach-clock');if(!clock||!mentor.state)return;const state=mentor.state;const seconds=state.status==='paused'?Math.ceil(state.paused_remaining||0):Math.max(0,Math.ceil((state.timer_deadline||Date.now()/1000)-Date.now()/1000));clock.textContent=String(Math.floor(seconds/60)).padStart(2,'0')+':'+String(seconds%60).padStart(2,'0');}
const restoredWork=el('p','','restored-work');restoredWork.id='restored-work';restoredWork.hidden=true;home.prepend(restoredWork);
async function restoreCoach(){const epoch=authEpoch;try{if(identityUser){const result=await api('/v1/coach/current');if(epoch!==authEpoch)return;mentor.state=result.journey;}else{try{mentor.state=JSON.parse(localStorage.getItem('chef-coach-guest-v1')||'null');if(mentor.state&&(!currentRecipe()||!Array.isArray(mentor.state.messages)||!Array.isArray(mentor.state.asked)))mentor.state=null;if(!$('inventory').children.length){const guestItems=JSON.parse(localStorage.getItem('chef-inventory-guest-v1')||'[]');if(Array.isArray(guestItems))guestItems.slice(0,100).forEach(addInventory);}}catch{mentor.state=null;}}restoredWork.hidden=!mentor.state;restoredWork.textContent=mentor.state?'שוחזרה העבודה הקודמת: '+(mentor.state.dish_title||currentRecipe()?.title||'בישול קודם')+'. אפשר להמשיך בה, לעדכן פרטים או לבחור מנה חדשה.':'';renderCoach();paintInventory();}catch{coachNotice.textContent='טעינת הבישול לא הושלמה. אפשר לנסות שוב.';}}
personality.addEventListener('change',()=>{if(mentor.state)void coachCommand('personality',{chefPersonality:personality.value});});
chatForm.addEventListener('submit',event=>{event.preventDefault();const text=chatInput.value.trim();if(!text){coachNotice.textContent='מה תרצה לשאול?';return;}void coachCommand('ask',{message:text}).then(()=>{if(!coachNotice.textContent&&chatInput.value.trim()===text)chatInput.value='';});});
photoInput.addEventListener('change',()=>{const file=photoInput.files[0];if(!file)return;if(!['image/jpeg','image/png','image/webp'].includes(file.type)||file.size>8*1024*1024){coachNotice.textContent='בחר תמונת JPG, PNG או WebP עד 8MB.';return;}if(mentor.image)URL.revokeObjectURL(mentor.image);mentor.image=URL.createObjectURL(file);const img=el('img');img.src=mentor.image;img.alt='תמונה שהמשתמש צירף';photoPreview.replaceChildren(img,el('small','התמונה מוצגת אצלך בלבד; ניתוח תמונות אינו מופעל. תאר בשאלה מה דורש בדיקה.'));});
document.addEventListener('chef-session-reset',()=>queueMicrotask(()=>{if(!identityUser){history.hidden=true;historicalInventories=[];if(mentor.image)URL.revokeObjectURL(mentor.image);mentor.image=null;photoPreview.replaceChildren();}paintInventory();void restoreCoach();}));
setInterval(()=>{paintClock();if(document.hidden||mentor.busy||mentor.state?.status!=='active')return;const state=mentor.state,now=Date.now()/1000;if((state.check_due_at&&now>=state.check_due_at&&!state.asked.includes('time'))||(state.workflow!=='user'&&now-state.last_user_at>=(state.checkin_seconds||180)&&!state.asked.includes('idle')))void coachCommand('check_in');},1000);
publicApi('/v1/coach/recipes').then(result=>{mentor.recipes=result.items;for(const recipe of mentor.recipes){const button=actionButton('dish-'+recipe.id,`${recipe.icon} ${recipe.title}`,()=>coachCommand('start',{recipe_id:recipe.id}),'dish-choice');dishChoices.insertBefore(button,newDish);}return restoreCoach();}).catch(()=>{coachNotice.textContent='לא ניתן לטעון את מסלולי הבישול. רענן או בדוק שהשירות פועל.';});
paintInventory();renderCoach();localize();
