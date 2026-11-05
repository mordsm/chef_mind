import {all, read, write, put, meta, queue, pending} from './storage.js';

const $=id=>document.getElementById(id);
const node=(tag,text='',cls='')=>{const value=document.createElement(tag);value.textContent=text;value.className=cls;return value;};
const button=(text,fn)=>{const value=node('button',text);value.type='button';value.addEventListener('click',()=>guard(fn));return value;};
const uuid=()=>crypto.randomUUID();
const GUEST='guest-local';
let config,owner='',token='',authenticatedOwner='',sessionId='',epoch=0,flushing=false,poller=null,offset=0,editing=null,chosen=null,values={},audio=null,wake=null,wantWake=false,installPrompt=null,saving=false;
const channel='BroadcastChannel'in window?new BroadcastChannel('chef-action-log'):null;
let entries=[],sessionRows=[],lastValues={},alerts=new Set();
let pushState={enabled:false};
let connecting=false;
let actionPage=0;
let recipeContext={recipe:null,defaults:null,step_id:'',legacy_timer:null};
const now=()=>Date.now()+offset;
const stamp=()=>new Date(now()).toISOString();
const message=(text,error=false)=>{$('status').textContent=text;$('status').classList.toggle('error',error);$('status').classList.toggle('important',error||/אין רשת|ממתין לחיבור|ההתחברות פגה|התחבר שוב/.test(text));if($('parameter-dialog')?.open){$('parameter-error').textContent=error?text:'';}};
async function guard(fn){try{await fn();}catch(error){message(error.message||'הפעולה לא הושלמה. הדיווחים שנשמרו נשארים במכשיר.',true);}}
async function api(path,options={}){
 const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),30000);
 const signal=options.signal||controller.signal;
 try{const response=await fetch(path,{...options,signal,headers:{'Content-Type':'application/json',Authorization:'Bearer '+token,...options.headers},cache:'no-store'});const data=await response.json();if(!response.ok){const error=new Error(data.message||({REPORT_CONFLICT:'הפעולה נערכה גם במכשיר אחר.',CONFIG_CHANGED:'הגדרות הפעולה השתנו. הדיווח המקומי נשמר לבירור.'}[data.code])||'לא ניתן לסנכרן כרגע.');Object.assign(error,{status:response.status,code:data.code,current:data.current});throw error;}return data;}finally{clearTimeout(timeout);}
}
const inputFor=row=>({action_type:row.action_type,config_version:row.config_version,parameters:row.parameters,started_at:row.started_at,ended_at:row.ended_at||null,notes:row.notes||'',recipe_snapshot_id:row.recipe_snapshot_id||'',recipe_step_id:row.recipe_step_id||''});
const definition=id=>config.actions.find(action=>action.id===id);
const date=value=>new Date(value).toLocaleString('he-IL');
function deadline(row){const action=definition(row.action_type);return row.scheduled_end_at||(action?.auto_timer?new Date(Date.parse(row.started_at)+Number(row.parameters.duration)*60000).toISOString():null);}
function summary(row){const action=definition(row.action_type);if(!action)return 'הגדרה חסרה לפעולה '+row.action_type;return action.fields.map(field=>{const value=row.parameters[field.id];const options=field.type==='ingredient'?config.ingredients:field.options;const display=value===null?'לא דווח':options?options.find(item=>item.id===value)?.label||value:value;return field.label+': '+display;}).join('\n');}

async function loadLocal(){
 sessionRows=(await all('sessions',owner)).sort((a,b)=>Date.parse(b.created_at)-Date.parse(a.created_at));
 entries=(await all('entries',owner)).filter(row=>row.cooking_id===sessionId).sort((a,b)=>Date.parse(a.started_at)-Date.parse(b.started_at)||a.id.localeCompare(b.id));
}
async function draw(){
 if(!owner){$('workspace').hidden=true;return;}
 const who=owner;await loadLocal();if(who!==owner)return;
 $('workspace').hidden=false;$('identity').textContent=owner===GUEST?'דיווח מקומי · נשמר במכשיר הזה':'החשבון: '+owner+(token?' · מחובר לסנכרון':' · שמירה מקומית, התחבר לסנכרון');$('logout').hidden=owner===GUEST;
 $('session').replaceChildren();for(const row of sessionRows){const option=node('option','בישול '+date(row.created_at)+(row.pending?' · ממתין לסנכרון':''));option.value=row.id;$('session').append(option);}$('session').value=sessionId;
 let pager=$('action-pages');if(!pager){pager=node('nav','','action-pages');pager.id='action-pages';$('actions').insertAdjacentElement('beforebegin',pager);}pager.replaceChildren(button(`כל ${config.actions.length} הפעולות · צלייה, אפייה, טיגון ועוד`,openCatalog));
 $('actions').replaceChildren();for(const id of ['cook','fry','cut','add']){const action=definition(id);if(!action)continue;const choice=button('',()=>openForm(action));choice.dataset.action=action.id;choice.append(node('span',action.icon,'icon'),node('span',action.label));choice.disabled=!sessionId||connecting;$('actions').append(choice);}
 $('history').replaceChildren();
 for(const row of entries.filter(row=>!row.deleted||row.conflict)){
   const card=node('li','',''+(row.pending?'pending ':'')+(row.conflict?'conflict':''));card.dataset.reportId=row.id;
   card.append(node('h3',(definition(row.action_type)?.icon||'')+' '+(definition(row.action_type)?.label||row.action_type)),node('time',date(row.started_at)),node('p',summary(row),'entry-details'));
   if(row.ended_at)card.append(node('p','סיום שדווח: '+date(row.ended_at)));
   if(row.notes)card.append(node('p',row.notes,'entry-notes'));
   if(row.pending)card.append(node('small',row.conflict?'נדרשת בחירה לפני סנכרון':'נשמר במכשיר · ממתין לסנכרון'));
   const controls=node('div','','row');
   if(row.conflict){card.append(node('p','הדיווח המקומי נשמר. יש שינוי בשרת או פרט שדורש תיקון.'));controls.append(button('קבל את גרסת השרת',()=>resolveConflict(row,false)));if(!row.deleted)controls.append(button('שמור את שלי כפעולה חדשה',()=>resolveConflict(row,true)));}
   else{controls.append(button('עריכה',()=>openForm(definition(row.action_type),row)),button('מחיקה',()=>removeReport(row)));if(!row.ended_at)controls.append(button('סיימתי עכשיו',()=>finishReport(row)));}
   card.append(controls);$('history').append(card);
 }
 if(!entries.some(row=>!row.deleted))$('history').append(node('li','עדיין לא דווחו פעולות בבישול הזה.'));
 const records=entries.filter(row=>!row.deleted);$('history-title').textContent=`יומן הפעולות (${records.length}) · צפייה ועריכה`;
 let latest=$('latest-report');if(!latest){latest=node('section','','latest-report');latest.id='latest-report';latest.setAttribute('role','status');$('status').insertAdjacentElement('afterend',latest);}latest.replaceChildren();latest.hidden=!records.length;
 if(records.length){const row=records.at(-1),action=definition(row.action_type);latest.append(node('strong','✓ נרשם: '+(action?.icon||'')+' '+(action?.label||row.action_type)+' · '+new Date(row.started_at).toLocaleTimeString('he-IL',{hour:'2-digit',minute:'2-digit'})),button('פתח יומן',()=>{$('report-history').open=true;$('report-history').scrollIntoView({block:'nearest'});}));}
 drawTimers();
}

function openCatalog(){
 let dialog=$('action-catalog');if(!dialog){dialog=node('dialog','','action-catalog');dialog.id='action-catalog';dialog.setAttribute('aria-label','כל פעולות הבישול');document.body.append(dialog);}dialog.replaceChildren(node('h2','איזו פעולה עשית?'),button('סגור',()=>dialog.close()));const grid=node('div','','catalog-grid');
 config.actions.forEach((action,index)=>{const choice=button(action.icon+' '+action.label,async()=>{actionPage=Math.floor(index/3);dialog.close();await draw();openForm(action);});choice.dataset.catalogAction=action.id;grid.append(choice);});dialog.append(grid);dialog.onclose=notifyModal;dialog.showModal();notifyModal();
}

function notifyModal(){if(window.parent!==window)window.parent.postMessage({type:'chef-report-modal',open:!!document.querySelector('dialog[open]')},location.origin);}
function parameterDialog(){let dialog=$('parameter-dialog');if(!dialog){dialog=node('dialog','','parameter-dialog');dialog.id='parameter-dialog';dialog.setAttribute('aria-labelledby','parameter-title');const error=node('p');error.id='parameter-error';error.setAttribute('role','alert');dialog.append(error,$('parameters'));document.body.append(dialog);dialog.addEventListener('cancel',event=>{event.preventDefault();closeForm();});dialog.addEventListener('close',notifyModal);}return dialog;}

function roundDial(field,input){
 const box=node('div','','dial-control'),dial=node('div','','round-dial');dial.tabIndex=0;dial.setAttribute('role','slider');dial.setAttribute('aria-label',field.label);dial.style.touchAction='none';const output=node('span','','dial-value');dial.append(output);
 const current=()=>input.value===''?field.min:Number(input.value);
 const maxValue=()=>Math.max(field.id==='duration'?Math.min(field.max,180):field.max,Number(input.value)||field.min);
 const sync=()=>{const value=input.value===''?null:Number(input.value),max=maxValue();dial.setAttribute('aria-valuemin',field.min);dial.setAttribute('aria-valuemax',max);dial.setAttribute('aria-valuenow',value??field.min);dial.setAttribute('aria-valuetext',value===null?'לא הוגדר':String(value)+(field.id==='duration'?' דקות':' מעלות'));dial.style.setProperty('--dial-angle',((value===null?0:(value-field.min)/(max-field.min))*270)+'deg');output.textContent=value===null?'לא הוגדר':String(value)+(field.id==='duration'?' דק׳':'°');};
 const set=value=>{const step=field.step||1;input.value=String(Number((Math.round(Math.min(field.max,Math.max(field.min,value))/step)*step).toFixed(2)));values[field.id]=Number(input.value);input.dispatchEvent(new Event('input',{bubbles:true}));sync();};
 const move=event=>{const bounds=dial.getBoundingClientRect();let angle=(Math.atan2(event.clientY-bounds.top-bounds.height/2,event.clientX-bounds.left-bounds.width/2)*180/Math.PI-135+360)%360;if(angle>270)angle=angle>315?0:270;set(field.min+angle/270*(maxValue()-field.min));};
 dial.addEventListener('pointerdown',event=>{if(event.button!==0)return;event.preventDefault();dial.setPointerCapture(event.pointerId);move(event);});dial.addEventListener('pointermove',event=>{if(dial.hasPointerCapture(event.pointerId))move(event);});dial.addEventListener('pointerup',event=>{if(dial.hasPointerCapture(event.pointerId))dial.releasePointerCapture(event.pointerId);});
 dial.addEventListener('keydown',event=>{const increment=(field.step||1)*(event.shiftKey?10:1),value=current();if(['ArrowUp','ArrowRight','ArrowDown','ArrowLeft','Home','End'].includes(event.key)){event.preventDefault();set(event.key==='Home'?field.min:event.key==='End'?maxValue():value+(['ArrowUp','ArrowRight'].includes(event.key)?increment:-increment));}});
 const minus=button('−',()=>set(current()-(field.step||1)));minus.setAttribute('aria-label','הקטן '+field.label);const plus=button('+',()=>set(current()+(field.step||1)));plus.setAttribute('aria-label','הגדל '+field.label);box.append(minus,dial,plus);input.addEventListener('input',sync);sync();return box;
}

function openForm(action,row=null){
 if(connecting)return;
 if(!action){message('הגדרת הפעולה חסרה. אפשר לשמור אותה בהערות של פעולה נתמכת.',true);return;}
 chosen=action;editing=row?structuredClone(row):null;values={};
 if($('action-check'))$('action-check').hidden=true;
 for(const field of action.fields){
   const defaults=!recipeContext.recipe&&['roast','bake'].includes(action.id)?recipeContext.defaults:null;
   const key={temperature:'temperature',duration:'minutes'}[field.id];
   const suggested=defaults&&key?defaults[key]:undefined;
   const valid=typeof suggested==='number'&&Number.isFinite(suggested)&&suggested>=field.min&&suggested<=field.max;
   values[field.id]=row&&Object.hasOwn(row.parameters,field.id)?row.parameters[field.id]
     :defaults&&key?(valid?suggested:null)
     :lastValues[action.id]&&Object.hasOwn(lastValues[action.id],field.id)?lastValues[action.id][field.id]:field.default;
 }
 $('parameter-title').textContent=(row?'עריכת דיווח: ':'דיווח: ')+action.label;$('notes').value=row?.notes||'';$('fields').replaceChildren();
 for(const field of action.fields){
   const group=node('fieldset','','parameter-field');group.dataset.field=field.id;group.append(node('legend',field.label));const choices=node('div','','choices');group.append(choices);
   const update=()=>{for(const child of choices.querySelectorAll('button'))child.setAttribute('aria-pressed',String(child.dataset.value===String(values[field.id])));};
   if(field.type==='number'){
     const input=document.createElement('input');input.type='number';input.id='number-'+field.id;input.min=field.min;input.max=field.max;input.step=field.step;input.required=!field.nullable;input.value=values[field.id]??'';
     for(const preset of field.presets||[]){const choice=button(String(preset),()=>{values[field.id]=preset;input.value=preset;input.dispatchEvent(new Event('input'));update();});choice.dataset.value=String(preset);choices.append(choice);}
     if(field.nullable){const unknown=button('לא כוונתי / לא ידוע',()=>{values[field.id]=null;input.value='';input.dispatchEvent(new Event('input'));update();});unknown.dataset.value='null';choices.append(unknown);}
     if(['duration','temperature'].includes(field.id))group.insertBefore(roundDial(field,input),choices);
     const custom=node('div','','custom-number');const label=node('label','ערך מספרי אחר');label.htmlFor=input.id;custom.append(label,input);group.append(custom);
     input.addEventListener('input',()=>{values[field.id]=input.value===''?null:Number(input.value);update();});
   }else{
     const options=field.type==='ingredient'?config.ingredients:field.options;
     for(const item of options){const choice=button(item.label,()=>{values[field.id]=item.id;update();});choice.dataset.value=item.id;choices.append(choice);}
   }update();$('fields').append(group);
 }
 $('parameters').hidden=false;const dialog=parameterDialog();$('parameter-error').textContent='';if(!dialog.open)dialog.showModal();notifyModal();
}
function closeForm(){$('parameters').hidden=true;if($('parameter-dialog')?.open)$('parameter-dialog').close();chosen=null;editing=null;notifyModal();}
async function saveReport(event){
 event.preventDefault();if(saving||!chosen||!sessionId)return;saving=true;$('save-report').disabled=true;
 try{
   for(const field of chosen.fields){const value=values[field.id];if(field.type==='number'&&!(value===null&&field.nullable)&&(!Number.isFinite(value)||value<field.min||value>field.max))throw new Error('בדוק את השדה '+field.label);}
   if(chosen.id==='measure'&&values.temperature===null)throw new Error('הזן את הטמפרטורה שמדדת בפועל לפני שמירת מדידה.');
   if(editing){const current=await read('entries',[owner,editing.id]);if(current?.revision!==editing.revision||current.conflict)throw new Error('הדיווח השתנה בזמן העריכה. פתח אותו שוב לפני שמירה.');}
   const base=editing;const report={action_type:chosen.id,config_version:config.version,parameters:{...values},started_at:base?.started_at||stamp(),ended_at:base?.ended_at||null,notes:$('notes').value.trim(),recipe_snapshot_id:base?base.recipe_snapshot_id||'':recipeContext.recipe?.id||'',recipe_step_id:base?base.recipe_step_id||'':recipeContext.step_id||''};
   const id=base?.id||uuid();await saveEntry({...report,id,cooking_id:sessionId,revision:base?.revision||0,deleted:false});
   lastValues[chosen.id]={...values};await meta('last-values:'+owner,lastValues);closeForm();message('✓ הפעולה נשמרה במכשיר.');await draw();showActionCheck(report);void flush();
 }finally{saving=false;$('save-report').disabled=false;}
}
// Finite checks use only action IDs and explicit choices, never notes or an LLM.
function showActionCheck(report){
 const checks={
 cook:{question:'הבישול נרשם והטיימר התחיל. מה המצב עכשיו?',options:[['עדיין מתחמם','המשך לחמם ובדוק שוב כשמופיעות בועות.'],['בעבוע עדין','אם המטרה ריכוך בסיר, שמור על בעבוע עדין ובדוק שיש מספיק נוזל.'],['רתיחה חזקה','אם המטרה ריכוך ממושך, הנמך עד לבעבוע עדין.'],['בישול בתנור','בדוק שהכלי מתאים לתנור. בסיום הזמן בדוק את המזון עצמו; הטיימר אינו אישור מוכנות.']]},
 cut:{question:'החיתוך נרשם. החתיכות בגודל דומה?',options:[['כן','אפשר להמשיך לשלב הבא במתכון.'],['לא','חתוך את החתיכות הגדולות יותר כדי שיתבשלו באופן דומה.']]},
 add:{question:'ההוספה נרשמה. האם הכמות והיחידה נכונות?',options:[['כן','המשך לשלב הבא במתכון; אם הוספת נוזל קר, בדוק שוב את מצב הבעבוע.'],['צריך לתקן','פתח עריכה בשורת הדיווח ועדכן את הכמות או היחידה.']]}
 };
 const check=checks[report.action_type]||definition(report.action_type)?.check||{question:'הפעולה נרשמה. בדקת את התוצאה?',options:[['כן, אפשר להמשיך','המשך לשלב הבא במתכון שבחרת.'],['עדיין צריך לבדוק','בדוק את מצב המזון בפועל לפני שמתקדמים; הזמן לבדו אינו אישור מוכנות.']]};
 let panel=$('action-check');if(!panel){panel=document.createElement('section');panel.id='action-check';panel.setAttribute('aria-live','polite');$('parameters').insertAdjacentElement('afterend',panel);}panel.hidden=false;panel.replaceChildren();panel.append(node('strong','🧑‍🍳 השף · בדיקה אחרי הדיווח'));
 const recipe=recipeContext.recipe,step=recipe?.id===report.recipe_snapshot_id?recipe.steps.find(step=>step.id===report.recipe_step_id):null;
 if(step){panel.append(node('p','במתכון שלך — '+recipe.title+': '+step.text,'recipe-comparison'));if(step.action_type&&step.action_type!==report.action_type)panel.append(node('p','דיווחת פעולה מסוג אחר מהפעולה שזוהתה בטקסט השלב. בדוק שבחרת את הפעולה ואת השלב המתאימים.','recipe-mismatch'));}
 else panel.append(node('p','אין שלב מתכון מקושר לדיווח הזה; זו הכוונה כללית. כדי להשוות למקור, צרף את המתכון ובחר את השלב הנוכחי.'));
 const reminders={cook:'הקפד להתאים את עוצמת החום למתכון ולעקוב אחר מפלס הנוזל.',grill:'הקפד לעקוב אחר להבות והשחמה. סימני רשת אינם בדיקת מוכנות.',roast:'הקפד לבדוק את מיקום התבנית ואת ההשחמה לפני תום הזמן.',bake:'הקפד על מצב התנור ומיקום התבנית לפי המתכון. בדוק את התוצאה בסיום הזמן.',fry:'הקפד שהשמן לא יעשן. אם המזון משחים מהר מדי, בדוק את עוצמת החום.'};if(reminders[report.action_type])panel.append(node('p',reminders[report.action_type]));
 const question=document.createElement('h3');question.textContent='✓ '+check.question;panel.append(question);panel.tabIndex=-1;panel.focus({preventScroll:true});panel.scrollIntoView({block:'nearest',behavior:'smooth'});
 for(const [label,reply]of check.options){const button=document.createElement('button');button.type='button';button.textContent=label;button.style.minHeight='48px';button.addEventListener('click',()=>{panel.replaceChildren();const answer=document.createElement('p');answer.textContent=reply;panel.append(answer);});panel.append(button);}
}
async function saveEntry(row,kind='put'){
 if(connecting)throw new Error('ממתין לסיום החיבור לחשבון לפני שמירת דיווח.');
 const request_id=uuid();const body={request_id,kind,cooking_id:row.cooking_id,report_id:row.id,expected_revision:row.revision};if(kind==='put')body.report=inputFor(row);
 const local={...row,revision:row.revision+1,last_request:request_id,deleted:kind==='delete',scheduled_end_at:deadline(row)};
 if(owner===GUEST)await put('entries',{...local,owner,pending:false});else await queue(owner,body,local);channel?.postMessage('changed');
}
async function removeReport(row){if(!confirm('למחוק את הדיווח?'))return;await saveEntry(row,'delete');if(editing?.id===row.id)closeForm();await draw();void flush();}
async function finishReport(row){await saveEntry({...row,ended_at:stamp()});await draw();void flush();}

async function newSession(){
 if(!owner)throw new Error('התחבר פעם אחת כדי לשייך את הדיווחים לחשבון.');
 const id=uuid(),request_id=uuid();const query=new URLSearchParams(location.search);const linked_cooking_id=query.get('server_link')==='1'?query.get('cooking_id')||'':'',recipe_id=query.get('recipe_id')||'';
 const row={id,recipe_id,linked_cooking_id,local_link:query.get('cooking_id')||'',revision:0,created_at:stamp(),last_request:request_id};
 if(owner===GUEST)await put('sessions',{...row,owner,pending:false});else await queue(owner,{request_id,kind:'create_session',cooking_id:id,recipe_id,linked_cooking_id},row,'sessions');sessionId=id;await meta('session:'+owner,id);closeForm();await draw();startPoll();void flush();
}
async function mergeSnapshot(data,who){
 await write(['sessions','entries'],tx=>{
   const sessions=tx.objectStore('sessions'),records=tx.objectStore('entries');
   const saved=sessions.get([who,data.session.id]);saved.onsuccess=()=>{const local=saved.result;if(!local||!local.pending)sessions.put({...data.session,owner:who});};
   for(const row of data.reports){const request=records.get([who,row.id]);request.onsuccess=()=>{const local=request.result;if(!local?.pending&&(!local||local.revision<=row.revision))records.put({...row,owner:who});};}
 });
}
async function flush(){
 if(flushing||!token||!owner||authenticatedOwner!==owner)return;flushing=true;const who=owner,scope=epoch;let changed=false;
 try{
   for(const item of await pending(who)){
     if(scope!==epoch||!token)break;
     const local=await read(item.store,[who,item.entity]);if(local?.conflict)continue;
     try{
       const result=await api('/v1/action-log/mutations',{method:'POST',body:JSON.stringify(item.body)});
       const remote=item.store==='sessions'?result.session:result.report;
       await write([item.store,'outbox'],tx=>{const store=tx.objectStore(item.store);const request=store.get([who,item.entity]);request.onsuccess=()=>{if(request.result?.last_request===item.body.request_id)store.put({...remote,owner:who,pending:false});};tx.objectStore('outbox').delete(item.seq);});
       changed=true;
     }catch(error){
       if(error.status===401){if(scope===epoch){token='';authenticatedOwner='';message('ההתחברות פגה. הדיווחים נשמרו במכשיר; התחבר שוב לסנכרון.',true);}break;}
       if((error.status===409||error.status===422)&&item.store==='entries'){
         const row=await read('entries',[who,item.entity]);await put('entries',{...row,conflict:{code:error.code,remote:error.current||null}});changed=true;message(error.message,true);continue;
       }
       message('הדיווחים נשמרים במכשיר. ממתין לחיבור כדי לסנכרן.');break;
     }
   }
   if(scope===epoch&&changed){await draw();const left=await pending(who);if(!left.length&&token)message('כל הדיווחים סונכרנו.');}
 }finally{flushing=false;}
}
async function resolveConflict(row,copy){
 const who=owner;const queued=(await pending(who)).filter(item=>item.store==='entries'&&item.entity===row.id);
 await write(['entries','outbox'],tx=>{for(const item of queued)tx.objectStore('outbox').delete(item.seq);if(row.conflict.remote)tx.objectStore('entries').put({...row.conflict.remote,owner:who});else tx.objectStore('entries').delete([who,row.id]);});
 if(copy){const action=definition(row.action_type);openForm(action);if(action){values={...row.parameters};openForm(action,{...row,id:uuid(),revision:0,conflict:undefined,started_at:row.started_at});editing=null;$('parameter-title').textContent='שמירת עותק חדש: '+action.label;}}
 await draw();message(copy?'הפרטים המקומיים פתוחים כעותק חדש לאישור.':'גרסת השרת נבחרה.');
}
function startPoll(){
 poller?.abort();if(!token||!owner||!sessionId||authenticatedOwner!==owner)return;const controller=new AbortController();poller=controller;const who=owner,id=sessionId,scope=epoch;
 void (async()=>{while(!controller.signal.aborted&&scope===epoch&&token){try{
   const local=await read('sessions',[who,id]);if(local?.pending){await new Promise(resolve=>setTimeout(resolve,1000));continue;}
   const data=await api('/v1/action-log/sessions/'+id+'?after='+(local?.revision??-1)+'&wait=20',{signal:controller.signal});
   if(!data.unchanged){await mergeSnapshot(data,who);if(scope===epoch&&id===sessionId)await draw();}
 }catch(error){if(controller.signal.aborted)break;if(error.status===401){token='';authenticatedOwner='';message('התחבר שוב כדי לקבל עדכונים מהמכשיר השני.',true);break;}await new Promise(resolve=>setTimeout(resolve,2500));}}})().catch(error=>message(error.message,true));
}
async function connect(event){
 event.preventDefault();if(connecting)return;connecting=true;$('new-session').disabled=true;$('session').disabled=true;for(const choice of $('actions').querySelectorAll('button'))choice.disabled=true;closeForm();epoch++;poller?.abort();authenticatedOwner='';const candidate=$('access-token').value.trim();token=candidate;
 try{const identity=await api('/v1/session');owner=identity.user_id;authenticatedOwner=owner;await meta('last-owner',owner);$('access-token').value='';sessionId=await meta('session:'+owner)||'';lastValues=await meta('last-values:'+owner)||{};
   const remote=await api('/v1/action-log/sessions');offset=Date.parse(remote.server_time)-Date.now();await meta('clock:'+owner,offset);
   for(const row of remote.items){const local=await read('sessions',[owner,row.id]);if(!local)await put('sessions',{...row,revision:-1,owner});}
   const linked=new URLSearchParams(location.search).get('cooking_id');const matched=linked&&remote.items.find(row=>row.linked_cooking_id===linked);if(matched)sessionId=matched.id;
   if(!sessionId){const rows=await all('sessions',owner);sessionId=rows.sort((a,b)=>Date.parse(b.created_at)-Date.parse(a.created_at))[0]?.id||'';}
   if(!sessionId)await newSession();else{await meta('session:'+owner,sessionId);await draw();startPoll();}
   void flush();message('מחובר. הדיווחים יתעדכנו בשני המכשירים.');void syncPushSubscription();
 }catch(error){token='';authenticatedOwner='';throw error;}finally{connecting=false;$('new-session').disabled=false;$('session').disabled=false;await draw();}
}
async function disconnect(){await disablePush();epoch++;poller?.abort();token='';authenticatedOwner='';owner='';sessionId='';entries=[];await meta('last-owner','');closeForm();$('workspace').hidden=true;$('identity').textContent='';$('logout').hidden=true;message('מנותק. הנתונים המקומיים נשמרו בחשבון שאליו שויכו.');}

async function syncPushSubscription(){try{if(!pushState.enabled||!token||authenticatedOwner!==owner||!('serviceWorker'in navigator))return;const registration=await navigator.serviceWorker.ready;const subscription=await registration.pushManager?.getSubscription();if(subscription)await api('/v1/action-log/push/subscriptions',{method:'POST',body:JSON.stringify(subscription.toJSON())});}catch{message('הדיווחים זמינים. יש להפעיל שוב את התראות הרקע כדי לרשום את המכשיר.',true);}}
async function enablePush(){
 if(!token||authenticatedOwner!==owner)throw new Error('התחבר כדי לשייך התראות למכשיר הזה.');
 if(!pushState.enabled)throw new Error('התראות רקע מחכות להפעלת מפתחות Web Push בשרת. ההתראה בתוך המסך כבר זמינה.');
 if(!('Notification'in window)||!('PushManager'in window))throw new Error('הדפדפן אינו תומך בהתראות רקע כאן. באייפון הוסף את האפליקציה למסך הבית ופתח אותה משם.');
 const permission=await Notification.requestPermission();if(permission!=='granted')throw new Error('לא ניתנה הרשאה להתראות. אפשר לשנות אותה בהגדרות האתר.');
 const registration=await navigator.serviceWorker.ready;const raw=atob(pushState.public_key.replaceAll('-','+').replaceAll('_','/'));
 const key=Uint8Array.from(raw,char=>char.charCodeAt(0));let subscription=await registration.pushManager.getSubscription();if(!subscription)subscription=await registration.pushManager.subscribe({userVisibleOnly:true,applicationServerKey:key});
 await api('/v1/action-log/push/subscriptions',{method:'POST',body:JSON.stringify(subscription.toJSON())});$('enable-push').textContent='📱 התראות רקע הופעלו';message('המכשיר נרשם להתראות כשהאפליקציה סגורה. נדרשים רשת ושרת פעיל; מצב שקט והגדרות המכשיר עשויים להשתיק צליל.');
}
async function disablePush(){try{if(!('serviceWorker'in navigator))return;const registration=await navigator.serviceWorker.getRegistration('/report/');const subscription=await registration?.pushManager?.getSubscription();if(subscription){if(token)await api('/v1/action-log/push/unsubscribe',{method:'POST',body:JSON.stringify(subscription.toJSON())}).catch(()=>{});await subscription.unsubscribe();}}catch{/* Browser invalidation is retried at the next disconnect. */}}

async function refreshSessions(){
 if(!token||authenticatedOwner!==owner)return;const who=owner,scope=epoch;
 try{const remote=await api('/v1/action-log/sessions');if(scope!==epoch)return;let changed=false;for(const row of remote.items){if(!await read('sessions',[who,row.id])){await put('sessions',{...row,owner:who,revision:-1});changed=true;}}if(changed)await draw();}catch{/* Keep the existing offline session list. */}
}

function drawTimers(){
 $('timers').replaceChildren();for(const row of entries){const end=deadline(row);if(!end||row.deleted||row.ended_at||row.conflict)continue;const remaining=Date.parse(end)-now(),expired=remaining<=0;const box=node('article','','timer'+(expired?' expired':''));box.dataset.timerId=row.id;box.append(node('strong',(definition(row.action_type)?.label||row.action_type)+(expired?' · הגיע זמן לבדוק':'')));const seconds=Math.max(0,Math.ceil(remaining/1000));box.append(node('output',String(Math.floor(seconds/3600)).padStart(2,'0')+':'+String(Math.floor(seconds/60)%60).padStart(2,'0')+':'+String(seconds%60).padStart(2,'0')));
   const key=owner+':'+row.id+':'+end;if(expired&&!alerts.has(key)){box.setAttribute('role','alert');if(audio?.state==='running'){beep();alerts.add(key);void meta('alerts:'+owner,[...alerts].slice(-1000));}}
   box.append(button('סיימתי פעולה',()=>finishReport(row)));$('timers').append(box);
 }const legacy=recipeContext.legacy_timer;if(legacy){const remaining=legacy.paused?Math.max(0,Math.ceil(legacy.remaining||0)):Math.max(0,Math.ceil(legacy.deadline-Date.now()/1000));const box=node('article','','timer');box.append(node('strong','תזכורת כללית'+(legacy.paused?' · מושהית':'')),node('output',String(Math.floor(remaining/60)).padStart(2,'0')+':'+String(remaining%60).padStart(2,'0')),button('בטל תזכורת',()=>window.parent.postMessage({type:'chef-cancel-legacy-timer'},location.origin)));$('timers').append(box);}if(!$('timers').children.length){const empty=node('div','','clock-empty');empty.append(node('output','00:00'),node('p','בחר פעולה עם משך להפעלת טיימר'));$('timers').append(empty);}
}
function beep(){for(let i=0;i<3;i++){const sound=audio.createOscillator(),volume=audio.createGain();sound.frequency.value=700;volume.gain.value=.12;sound.connect(volume);volume.connect(audio.destination);sound.start(audio.currentTime+i*.3);sound.stop(audio.currentTime+i*.3+.18);}}
async function enableSound(){const Audio=window.AudioContext||window.webkitAudioContext;if(!Audio)throw new Error('צליל אינו זמין בדפדפן הזה. ההתראה החזותית נשארת פעילה.');audio=audio||new Audio();await audio.resume();$('enable-sound').setAttribute('aria-pressed','true');$('enable-sound').textContent='🔔 צליל מופעל';beep();drawTimers();}
async function acquireWake(){if(!wantWake||document.hidden)return;if(!navigator.wakeLock)throw new Error('שמירת מסך ער אינה נתמכת בדפדפן הזה.');wake=await navigator.wakeLock.request('screen');wake.addEventListener('release',()=>{wake=null;});}

async function boot(){
 if(window.parent!==window){document.body.classList.add('embedded');const tools=document.querySelector('.tools');const options=node('details');options.append(node('summary','צליל, התראות וסנכרון'),tools);$('workspace').append(options);}
 try{config=await (await fetch('/assets/report/actions.json')).json();await meta('config',config);}catch{config=await meta('config');if(!config)throw new Error('נדרשת פתיחה ראשונה עם חיבור לרשת.');}
 if('serviceWorker'in navigator)navigator.serviceWorker.register('/report/sw.js',{scope:'/report/'}).catch(()=>message('התקנה ללא רשת אינה זמינה בדפדפן הזה.',true));
 try{pushState=await (await fetch('/v1/action-log/push/status')).json();}catch{}
 owner=await meta('last-owner')||GUEST;sessionId=await meta('session:'+owner)||'';offset=await meta('clock:'+owner)||0;lastValues=await meta('last-values:'+owner)||{};alerts=new Set(await meta('alerts:'+owner)||[]);
 const link=new URLSearchParams(location.search).get('cooking_id');if(owner===GUEST&&link){sessionId=(await all('sessions',owner)).find(item=>item.local_link===link)?.id||'';}
 if(!sessionId)await newSession();else await draw();message(owner===GUEST?'בחר פעולה ודווח. הדיווחים נשמרים במכשיר הזה; התחבר לסנכרון בין מכשירים.':'הדיווחים המקומיים זמינים. התחבר כדי לסנכרן בין המכשירים.');
 if(window.parent!==window)window.parent.postMessage({type:'chef-report-ready'},location.origin);
 $('login').querySelector('button').disabled=false;
}
$('login').addEventListener('submit',event=>guard(()=>connect(event)));
$('logout').addEventListener('click',()=>guard(disconnect));
$('new-session').addEventListener('click',()=>guard(newSession));
$('report-form').addEventListener('submit',event=>guard(()=>saveReport(event)));
$('cancel-report').addEventListener('click',closeForm);
$('session').addEventListener('change',()=>guard(async()=>{sessionId=$('session').value;await meta('session:'+owner,sessionId);closeForm();await draw();startPoll();}));
$('retry').addEventListener('click',()=>guard(async()=>{if(!token)throw new Error('התחבר כדי לסנכרן.');await flush();startPoll();}));
$('enable-sound').addEventListener('click',()=>guard(enableSound));
$('enable-push').addEventListener('click',()=>guard(enablePush));
$('wake').addEventListener('click',()=>guard(async()=>{wantWake=!wantWake;if(wantWake)await acquireWake();else await wake?.release();$('wake').setAttribute('aria-pressed',String(wantWake));$('wake').textContent=wantWake?'☀ המסך נשאר ער':'☀ השאר מסך ער';}));
document.addEventListener('visibilitychange',()=>{if(!document.hidden){guard(acquireWake);drawTimers();void flush();}});
window.addEventListener('online',()=>{void flush();startPoll();});
window.addEventListener('offline',()=>message('אין רשת. כל דיווח חדש נשמר במכשיר ויסונכרן לאחר החיבור.'));
window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();installPrompt=event;$('install').hidden=false;});
$('install').addEventListener('click',()=>guard(async()=>{if(installPrompt){await installPrompt.prompt();installPrompt=null;$('install').hidden=true;}}));
setInterval(drawTimers,1000);setInterval(()=>void flush(),3000);setInterval(()=>void refreshSessions(),10000);
if(channel)channel.onmessage=()=>guard(draw);
window.addEventListener('message',event=>{if(event.origin!==location.origin||event.source!==window.parent)return;if(event.data?.type==='chef-recipe-context'){recipeContext={recipe:event.data.recipe||null,defaults:event.data.defaults||null,step_id:event.data.step_id||'',legacy_timer:event.data.legacy_timer||null};if(config&&owner)drawTimers();return;}if(event.data?.type==='chef-report-logout'){guard(async()=>{await disconnect();location.reload();});return;}if(event.data?.type!=='chef-report-auth'||typeof event.data.token!=='string'||!event.data.token)return;$('access-token').value=event.data.token;guard(()=>connect({preventDefault(){}}));});
if(window.parent!==window){new ResizeObserver(()=>window.parent.postMessage({type:'chef-report-height',height:document.body.scrollHeight},location.origin)).observe(document.body);}
guard(boot);
