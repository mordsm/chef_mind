'use strict';
// Only explicit browser actions: no sensing, inferred completion, or provider calls.
Object.assign(words.he, {
 kitchen:'מצב מטבח', kitchenClose:'חזרה לטופס', kitchenCurrent:'ההנחיה הנוכחית', kitchenWhy:'הסבר ומקורות', kitchenReport:'מה קרה בפועל?', kitchenAddReport:'הוספת הדיווח לטופס', kitchenReportHint:'כתוב תצפית אמיתית. הדיווח יישלח רק עם השאלה הבאה.', kitchenReportAdded:'הדיווח נוסף לטופס; הוא עדיין לא נשלח.', kitchenReportRequired:'יש לכתוב דיווח ולא לחרוג מ־30 שורות.', reminder:'תזכורת ידנית בלבד', reminderSeconds:'מספר שניות — לבחירתך', reminderStart:'הפעלת תזכורת', reminderCancel:'ביטול תזכורת', reminderHelp:'זו אינה הערכת זמן בישול ואינה הוכחה שהמזון בטוח. אין להסתמך עליה ברקע או כשהמכשיר נעול.', reminderDone:'הגיע הזמן שבחרת. בדוק ודווח על המצב בפועל.', reminderInvalid:'יש להזין מספר שלם בין 1 ל־14400 שניות.', reminderCancelClose:'סגירת מצב מטבח תבטל את התזכורת הפעילה. להמשיך?', readLocal:'הקראה מקומית', stopReading:'עצירת הקראה', localVoiceUnavailable:'אין קול מקומי מתאים לשפת ההנחיה במכשיר זה.', localVoiceHelp:'הקראה משתמשת רק בקול שמסומן כמקומי בדפדפן. הטקסט אינו נשלח ל־OpenAI.', keepAwake:'השארת המסך ער', releaseAwake:'שחרור המסך', awakeHelp:'בקשה לדפדפן בלבד. היא עשויה להתבטל במעבר לאפליקציה אחרת.', awakeUnavailable:'שמירת המסך ער אינה זמינה כרגע.', awakeOn:'הדפדפן אישר בקשה להשארת המסך ער.', awakeOff:'שמירת המסך ער בוטלה.', kitchenNoGuidance:'יש לקבל הנחיה תחילה.'
});
Object.assign(words.en, {
 kitchen:'Kitchen view', kitchenClose:'Back to form', kitchenCurrent:'Current guidance', kitchenWhy:'Reason and sources', kitchenReport:'What actually happened?', kitchenAddReport:'Add report to form', kitchenReportHint:'Describe an actual observation. It is sent only with your next question.', kitchenReportAdded:'Report added to the form; it has not been sent.', kitchenReportRequired:'Enter a report and keep the total within 30 lines.', reminder:'Manual reminder only', reminderSeconds:'Seconds — choose your own', reminderStart:'Start reminder', reminderCancel:'Cancel reminder', reminderHelp:'This is not a cooking-time estimate or proof that food is safe. Do not rely on it in the background or while the device is locked.', reminderDone:'Your selected time elapsed. Check and report the actual condition.', reminderInvalid:'Enter a whole number from 1 to 14400 seconds.', reminderCancelClose:'Closing kitchen view cancels the active reminder. Continue?', readLocal:'Read aloud locally', stopReading:'Stop reading', localVoiceUnavailable:'No local voice matches the guidance language on this device.', localVoiceHelp:'Uses only a voice reported as local by your browser. Text is not sent to OpenAI.', keepAwake:'Keep screen awake', releaseAwake:'Release screen', awakeHelp:'A browser request only. It may be released when you switch apps.', awakeUnavailable:'Keeping the screen awake is unavailable right now.', awakeOn:'The browser accepted the screen-awake request.', awakeOff:'Screen-awake request released.', kitchenNoGuidance:'Get guidance first.'
});

const kitchenButton=translated('button','kitchen','kitchen-launch');
kitchenButton.id='kitchen-open';kitchenButton.type='button';kitchenButton.disabled=true;
$('cook').append(kitchenButton);
const kitchen=el('dialog','','kitchen-dialog');kitchen.id='kitchen-dialog';
kitchen.setAttribute('aria-labelledby','kitchen-heading');
const kitchenHeader=el('div','','row');
const kitchenHeading=translated('h2','kitchenCurrent');kitchenHeading.id='kitchen-heading';
const kitchenClose=translated('button','kitchenClose','secondary');kitchenClose.id='kitchen-close';
kitchenHeader.append(kitchenHeading,kitchenClose);
const kitchenStatus=el('span','','badge');
const kitchenAction=el('p','','kitchen-action');kitchenAction.id='kitchen-action';
const kitchenSignal=el('p');kitchenSignal.id='kitchen-signal';
const kitchenSafety=el('div','','kitchen-safety');
const kitchenWhy=el('details');const whyTitle=translated('summary','kitchenWhy');
const whyContent=el('div');kitchenWhy.append(whyTitle,whyContent);
const report=el('textarea');report.id='kitchen-report';report.rows=2;report.maxLength=1000;
const addReport=translated('button','kitchenAddReport');addReport.id='kitchen-add-report';
const reportHint=translated('p','kitchenReportHint','kitchen-note');
const reminder=el('fieldset');reminder.id='kitchen-reminder';
const seconds=el('input');seconds.id='reminder-seconds';seconds.type='number';seconds.min='1';seconds.max='14400';seconds.step='1';
const startReminder=translated('button','reminderStart');startReminder.id='reminder-start';
const cancelReminder=translated('button','reminderCancel','secondary');cancelReminder.id='reminder-cancel';cancelReminder.disabled=true;
const countdown=el('output','00:00','kitchen-clock');countdown.id='reminder-clock';
const reminderNotice=el('p');reminderNotice.id='reminder-notice';reminderNotice.setAttribute('role','status');
const timerRow=el('div','','row');timerRow.append(startReminder,cancelReminder,countdown);
reminder.append(translated('legend','reminder'),field('reminderSeconds',seconds),timerRow,translated('p','reminderHelp','kitchen-note'),reminderNotice);
const read=translated('button','readLocal','secondary');read.id='kitchen-read';
const stopReading=translated('button','stopReading','secondary');stopReading.id='kitchen-stop-reading';
const awake=translated('button','keepAwake','secondary');awake.id='kitchen-awake';awake.setAttribute('aria-pressed','false');
const helpers=el('div','','row');helpers.append(read,stopReading,awake);
const kitchenNotice=el('p');kitchenNotice.id='kitchen-notice';kitchenNotice.setAttribute('role','status');
kitchen.append(kitchenHeader,kitchenStatus,kitchenAction,translated('h3','success'),kitchenSignal,kitchenSafety,kitchenWhy,reminder,
 field('kitchenReport',report),reportHint,addReport,helpers,translated('p','localVoiceHelp','kitchen-note'),translated('p','awakeHelp','kitchen-note'),kitchenNotice);
document.body.append(kitchen);
let kitchenDecision=null, reminderDeadline=null, reminderInterval=null, wakeHandle=null;

function kitchenMessage(key){kitchenNotice.dataset.i18n=key;kitchenNotice.textContent=t(key);}
function cancelManualReminder(){if(reminderInterval!==null)clearInterval(reminderInterval);reminderInterval=null;reminderDeadline=null;countdown.textContent='00:00';cancelReminder.disabled=true;startReminder.disabled=false;}
function stopLocalReading(){if('speechSynthesis' in window)window.speechSynthesis.cancel();}
async function releaseScreen(){const old=wakeHandle;wakeHandle=null;if(old){try{await old.release();}catch{}}awake.dataset.i18n='keepAwake';awake.textContent=t('keepAwake');awake.setAttribute('aria-pressed','false');}
function closeKitchen(force=false){if(!force&&reminderDeadline!==null&&!confirm(t('reminderCancelClose')))return;cancelManualReminder();stopLocalReading();void releaseScreen();kitchen.close();kitchenButton.focus();}
function resetKitchen(){closeKitchen(true);kitchenDecision=null;kitchenButton.disabled=true;report.value='';seconds.value='';kitchenAction.textContent='';kitchenSignal.textContent='';kitchenSafety.replaceChildren();whyContent.replaceChildren();kitchenNotice.textContent='';reminderNotice.textContent='';}
function paintKitchen(){if(!kitchenDecision)return;kitchenAction.textContent=kitchenDecision.instruction;kitchenSignal.textContent=kitchenDecision.success_signal;kitchenStatus.dataset.i18n='decision_'+kitchenDecision.decision_type;kitchenStatus.textContent=t(kitchenStatus.dataset.i18n);kitchenSafety.replaceChildren();section(kitchenSafety,'safety',kitchenDecision.safety_flags);whyContent.replaceChildren();section(whyContent,'principle',kitchenDecision.culinary_reason);for(const citation of kitchenDecision.citations){const entry=el('div','','citation');entry.append(el('p',citation.supporting_text),el('small',citation.attribution));reference(entry,citation.source_reference);whyContent.append(entry);}reminder.hidden=kitchenDecision.decision_type!=='action';}
document.addEventListener('chef-decision',event=>{cancelManualReminder();stopLocalReading();kitchenDecision=event.detail;kitchenButton.disabled=false;paintKitchen();});
document.addEventListener('chef-session-reset',resetKitchen);
kitchenButton.addEventListener('click',()=>{if(!kitchenDecision){notice('kitchenNoGuidance',true);return;}paintKitchen();kitchen.showModal();kitchenClose.focus();});
kitchenClose.addEventListener('click',()=>closeKitchen());
kitchen.addEventListener('cancel',event=>{event.preventDefault();closeKitchen();});
addReport.addEventListener('click',()=>{const value=report.value.trim();const lines=$('reports').value.split('\n').map(line=>line.trim()).filter(Boolean);const additions=value.split('\n').map(line=>line.trim()).filter(Boolean);if(!value||lines.length+additions.length>30){kitchenMessage('kitchenReportRequired');return;}$('reports').value=[...lines,...additions].join('\n');report.value='';kitchenMessage('kitchenReportAdded');});
startReminder.addEventListener('click',()=>{const value=Number(seconds.value);if(!kitchenDecision||kitchenDecision.decision_type!=='action'||!Number.isInteger(value)||value<1||value>14400){kitchenMessage('reminderInvalid');return;}cancelManualReminder();reminderNotice.textContent='';delete reminderNotice.dataset.i18n;reminderDeadline=performance.now()+value*1000;startReminder.disabled=true;cancelReminder.disabled=false;
 const tick=()=>{if(reminderDeadline===null)return;const remaining=Math.max(0,Math.ceil((reminderDeadline-performance.now())/1000));countdown.textContent=String(Math.floor(remaining/60)).padStart(2,'0')+':'+String(remaining%60).padStart(2,'0');if(!remaining){cancelManualReminder();reminderNotice.dataset.i18n='reminderDone';reminderNotice.textContent=t('reminderDone');}};
 reminderInterval=setInterval(tick,250);tick();});
cancelReminder.addEventListener('click',cancelManualReminder);
read.addEventListener('click',()=>{stopLocalReading();if(!kitchenDecision||!('speechSynthesis' in window)||!('SpeechSynthesisUtterance' in window)){kitchenMessage('localVoiceUnavailable');return;}
 const isHebrew=/[\u0590-\u05ff]/.test(kitchenDecision.instruction);const locale=isHebrew?'he':'en';
 const voice=window.speechSynthesis.getVoices().find(candidate=>candidate.localService&&candidate.lang.toLowerCase().startsWith(locale));
 if(!voice){kitchenMessage('localVoiceUnavailable');return;}
 const utterance=new SpeechSynthesisUtterance(kitchenDecision.instruction.replace(/[*#\[\]<>`]/g,'').replace(/https?:\/\/\S+/g,''));utterance.voice=voice;utterance.lang=voice.lang;utterance.onerror=()=>kitchenMessage('localVoiceUnavailable');window.speechSynthesis.speak(utterance);});
stopReading.addEventListener('click',stopLocalReading);
awake.addEventListener('click',async()=>{if(wakeHandle){await releaseScreen();kitchenMessage('awakeOff');return;}if(!('wakeLock' in navigator)||document.visibilityState!=='visible'){kitchenMessage('awakeUnavailable');return;}awake.disabled=true;try{const handle=await navigator.wakeLock.request('screen');if(!kitchen.open){await handle.release();return;}wakeHandle=handle;awake.dataset.i18n='releaseAwake';awake.textContent=t('releaseAwake');awake.setAttribute('aria-pressed','true');handle.addEventListener('release',()=>{if(wakeHandle===handle){wakeHandle=null;awake.dataset.i18n='keepAwake';awake.textContent=t('keepAwake');awake.setAttribute('aria-pressed','false');kitchenMessage('awakeOff');}});kitchenMessage('awakeOn');}catch{kitchenMessage('awakeUnavailable');}finally{awake.disabled=false;}});
document.addEventListener('visibilitychange',()=>{if(document.hidden){stopLocalReading();void releaseScreen();}});
window.addEventListener('pagehide',()=>{stopLocalReading();void releaseScreen();});
localize();
