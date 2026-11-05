'use strict';
// A presentation layer over existing commands: completion and safety remain server-owned.
(() => {
 let mode='prepare',workId=null,lastHeard='',microExplanation='';
 const bar=el('nav','','cooking-mode-bar');bar.setAttribute('aria-label','מצב עבודה במטבח');
 const prepare=actionButton('mode-prepare','① תכנון והכנה',()=>setMode('prepare'));
 const live=actionButton('mode-live','② בישול חי',()=>setMode('live'));
 const dish=actionButton('choose-cooking-dish','🍽 בחירת מנה / מנה חדשה',openDishSelection);
 bar.append(dish,prepare,live);workspace.insertAdjacentElement('beforebegin',bar);
 const dishDialog=el('dialog','','dish-selection-dialog');dishDialog.id='dish-selection-dialog';dishDialog.setAttribute('aria-labelledby','dish-selection-title');
 const dialogTitle=el('h2','מה תרצה להכין?');dialogTitle.id='dish-selection-title';
 dishDialog.append(dialogTitle,actionButton('close-dish-selection','סגור וחזור לבישול',()=>dishDialog.close()));document.body.append(dishDialog);
 let setupPosition=null;
 function openDishSelection(){
   const setup=$('kitchen-setup');if(!setup)return;
   setupPosition=document.createComment('dish setup position');setup.before(setupPosition);dishDialog.append(setup);setup.open=true;startWork.hidden=false;
   startWork.textContent=mentor.state?'התחל מנה חדשה':'התחל להכין את המנה';dishDialog.showModal();customTitle.focus();customTitle.select();
 }
 dishDialog.addEventListener('close',()=>{const setup=$('kitchen-setup');if(setupPosition&&setup){setupPosition.replaceWith(setup);setupPosition=null;setup.open=!mentor.state;}startWork.textContent='התחל עבודה';requestAnimationFrame(sizeWorkspace);});
 function setMode(next){mode=next;paint();}
 function pills(select){
   if(select.dataset.touchChoices)return;select.dataset.touchChoices='1';
   const group=el('div','','touch-choices');group.setAttribute('role','group');group.setAttribute('aria-label',select.getAttribute('aria-label')||document.querySelector(`label[for="${select.id}"]`)?.textContent||'בחירה');
   select.insertAdjacentElement('afterend',group);select.classList.add('touch-select');
   function sync(){group.replaceChildren();for(const option of select.options){if(!option.value)continue;const button=el('button',option.textContent);button.type='button';button.disabled=select.disabled||option.disabled;button.setAttribute('aria-pressed',String(select.value===option.value));button.addEventListener('click',()=>{select.value=select.value===option.value?'':option.value;select.dispatchEvent(new Event('input',{bubbles:true}));select.dispatchEvent(new Event('change',{bubbles:true}));sync();});group.append(button);}group.hidden=select.hidden||!group.children.length;}
   select.addEventListener('change',sync);new MutationObserver(sync).observe(select,{childList:true,attributes:true,subtree:true});sync();
 }
 function speak(text){
   document.dispatchEvent(new Event('coach-stop-dictation'));
   if(!window.speechSynthesis||!window.SpeechSynthesisUtterance){announcement('הקראה אינה נתמכת בדפדפן הזה.');return;}
   const voices=speechSynthesis.getVoices().filter(v=>v.lang.toLowerCase().startsWith('he'));
   if(!voices.length){announcement('לא נמצא קול בעברית במכשיר. ההסבר מופיע על המסך.');return;}
   speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(text);utterance.lang='he-IL';utterance.voice=voices.find(v=>v.localService)||voices[0];speechSynthesis.speak(utterance);
 }
 function announcement(text){let message=$('cooking-announcement');if(!message){message=el('p');message.id='cooking-announcement';message.setAttribute('role','status');const voice=$('cockpit-voice');if(voice)voice.append(message);else bar.insertAdjacentElement('afterend',message);}message.textContent=text;}
 function explainCurrentStep(){
   if(!microExplanation)return;
   const response=$('voice-explanation');if(response){response.hidden=false;response.textContent=microExplanation;}
   speak(microExplanation);
 }
 function shortExplanation(step,tip){
   const text=step?.instruction||step?.title||'';
   if(tip?.text&&(!step||tip.text.split(/\s+/).length<=60))return tip.text;
   if(/קיצוץ|קוצצים|חותכים|חיתוך|קיצוץ|שיני שום/.test(text))return 'חתיכות בגודל דומה מתבשלות בקצב דומה, ולכן קל יותר לקבל הכנה אחידה.';
   if(/גריל|מנגל|צריבה|צלייה/.test(text))return 'בדוק את מרכז הנתח במדחום; השחמה לבדה אינה מעידה על מוכנות.';
   if(/בעבוע|רתיחה/.test(text))return 'שמור על בעבוע עדין ובדוק את מפלס הנוזל במהלך הבישול.';
   if(/תיבול|מתבלים/.test(text))return 'הוספת תיבול בהדרגה נותנת שליטה בטעם, בהתאם לכמויות ולשלב שנקבעו במתכון.';
   const first=(step?.why||tip?.text||'').split(/(?<=[.!?])\s/)[0];
   return first&&first.split(/\s+/).length<=15?first:'';
 }
 document.addEventListener('chef-why-requested',explainCurrentStep);
 document.addEventListener('chef-voice-transcript',event=>{lastHeard=event.detail.text;const transcript=$('voice-last-transcript');if(transcript)transcript.textContent=lastHeard;});
 let modalInert=[];
 window.addEventListener('message',event=>{
   const frame=window.chefReportFrame;if(event.origin!==location.origin||!frame||event.source!==frame.contentWindow||event.data?.type!=='chef-report-modal')return;
   const open=event.data.open===true;if(open&&!document.body.classList.contains('action-modal-open'))document.dispatchEvent(new Event('coach-stop-dictation'));document.body.classList.toggle('action-modal-open',open);
   if(open&&!modalInert.length){const nodes=[document.querySelector('body>header'),document.querySelector('main>nav'),home,bar,...workspace.children].filter(node=>node&&node!==companion);modalInert=nodes.map(node=>[node,node.inert]);for(const [node]of modalInert)node.inert=true;}
   if(!open){for(const [node,prior]of modalInert)node.inert=prior;modalInert=[];}
 });
 function paint(){
   const state=mentor.state,custom=state?.workflow==='user';
   bar.hidden=false;prepare.disabled=!custom;live.disabled=!custom||state.status!=='active';
   if(workId!==state?.id){if(dishDialog.open)dishDialog.close();mode='prepare';workId=state?.id;lastHeard='';if(custom&&$('kitchen-setup'))$('kitchen-setup').open=false;}
   document.body.classList.toggle('cooking-live',custom&&mode==='live');
   prepare.setAttribute('aria-pressed',String(mode==='prepare'));live.setAttribute('aria-pressed',String(mode==='live'));
   document.querySelectorAll('#cooking-intake-form select,#custom-method').forEach(pills);
   if(!custom)return;
   const oldVoice=$('cockpit-voice');if(oldVoice){const form=oldVoice.querySelector('#user-report-form');if(form)companion.append(form);oldVoice.remove();}
   const settings=$('coach-settings'),setup=$('kitchen-setup');if(settings&&setup&&settings.parentElement!==setup)setup.append(settings);
   // The structured reporter is the single action-entry surface.
   $('add-user-step')?.remove();
   const legacyPicker=$('operation-picker');if(legacyPicker)legacyPicker.hidden=true;
   // All active countdowns are shown in the report panel, including any older reminder.
   const legacyTimer=$('kitchen-timer');if(legacyTimer)legacyTimer.hidden=true;
   const questionForm=$('user-report-form');if(questionForm){mentor.inputMode='ask';questionForm.querySelector('.composer-modes')?.remove();questionForm.querySelector('.quick-reports')?.remove();const label=questionForm.querySelector('label[for="work-report"]');if(label)label.textContent='שאלה לשף — לא חובה';const text=$('work-report');if(text){text.placeholder='שאלה על ההכנה? אפשר לכתוב או לדבר לשף.';text.setAttribute('aria-label','שאלה לשף');}const submit=questionForm.querySelector('button[type="submit"]');if(submit)submit.textContent='שלח שאלה לשף';}
   $('cooking-live-stage')?.remove();
   const stage=el('section','','cooking-live-stage');stage.id='cooking-live-stage';
   const step=selectedStep(),steps=state.custom_steps||[];
   const stepper=el('ol','','cooking-stepper');stepper.setAttribute('aria-label','שלבי ההכנה');
   steps.forEach((entry,index)=>{const item=el('li',`${index+1}. ${entry.title}`);if(index===state.current_step)item.setAttribute('aria-current','step');if(state.completed_step_ids.includes(entry.id))item.classList.add('completed');stepper.append(item);});
   stage.append(stepper);
   if(step)stage.append(el('strong',`שלב ${state.current_step+1} מתוך ${steps.length}`,'live-step-counter'));
   stage.append(el('p',state.dish_title,'live-dish'),el('h2',step?.title||'לפני שמתחילים לחמם'));
   const instruction=state.station_protocol?.text||step?.instruction||state.intake_guidance?.missing?.[0]?.label||'בחר פעולה לדיווח, או חזור להכנה כדי להשלים תוכנית למנה.';
   if(state.station_protocol?.blocks?.length)renderStationProtocol(stage,state.station_protocol);else stage.append(el('p',instruction,'live-instruction'));
   if(!step){const back=actionButton('live-complete-preparation','השלם פרטי הכנה',()=>setMode('prepare'));stage.append(back);}
   const controls=el('div','','live-controls');
   if(step){const done=actionButton('live-done','✓ בוצע / השלב הבא',()=>coachCommand('complete'));done.disabled=state.status!=='active'||state.safety_hold;controls.append(done);}
   controls.append(actionButton('live-read','🔊 הקרא את השלב',()=>speak(instruction)));
   stage.append(controls);
   const stepText=(step?.instruction||'')+' '+(step?.title||'');const tip=(state.context?.tips||[]).find(t=>t.practical&&(t.origin!=='OBSIDIAN_SUPPLIED'||t.step_keywords?.some(word=>stepText.includes(word))));microExplanation=shortExplanation(step,tip);
   if(microExplanation){const tipBox=el('details','','micro-tip');tipBox.append(el('summary','טיפ שף'),el('p',microExplanation));stage.append(tipBox);}
   if(state.safety_hold||state.method_warning){const warning=el('p',state.method_warning||'הליווי מושהה: יש לטפל בסיכון שדווח לפני שממשיכים.','live-warning');warning.setAttribute('role','alert');stage.append(warning);}
   journey.prepend(stage);
   if(mode==='live'){
     const voice=el('section','','panel cockpit-voice');voice.id='cockpit-voice';voice.append(el('h2','דבר עם השף'));
     const listening=el('p','המיקרופון כבוי','live-listening');listening.id='live-listening';listening.setAttribute('role','status');voice.append(listening);
     const wave=el('div','','voice-wave');wave.setAttribute('aria-hidden','true');for(let i=0;i<5;i++)wave.append(el('span'));voice.append(wave);
     voice.append(actionButton('live-microphone','🎙 דבר לשף',()=>document.dispatchEvent(new CustomEvent('coach-dictate',{detail:{target:'work-report'}}))));
     voice.append(el('h3','התמלול האחרון'));const transcript=el('p',lastHeard||'הדיבור שלך יופיע כאן.','voice-transcript');transcript.id='voice-last-transcript';voice.append(transcript);
     voice.append(el('small','אמור ״השף, למה?״ להסבר קצר. שאלה אחרת תישלח רק בלחיצה על שליחה.'));
     const form=$('user-report-form');if(form){const edit=el('details','','voice-question-editor');edit.append(el('summary','עריכה או הקלדת שאלה'),form);voice.append(edit);voice.append(actionButton('voice-send-question','שלח את השאלה לשף',()=>{if(!$('work-report').value.trim()){edit.open=true;$('work-report').focus();}else form.requestSubmit();}));}
     const response=el('p','','voice-explanation');response.id='voice-explanation';response.hidden=true;response.setAttribute('role','status');voice.append(response,coachNotice);if(typeof voiceStatus!=='undefined')voice.append(voiceStatus);workspace.append(voice);
   }
   const plan=$('kitchen-plan');if(plan)plan.open=false;
   const form=$('cooking-intake-form');
   if(form){const groups=el('div','','intake-pages');const fields=[...form.querySelectorAll(':scope > label')];let shown=0;
     for(const label of fields){const control=document.getElementById(label.htmlFor);if(!control||control.hidden)continue;const choices=control.nextElementSibling;const page=el('details','','intake-page');const selected=control.selectedOptions?.[0]?.value?control.selectedOptions[0].textContent:'טרם נבחר';page.open=!control.value&&shown++===0;const summary=el('summary',label.textContent+' · '+selected);control.addEventListener('change',()=>{summary.textContent=label.textContent+' · '+(control.selectedOptions?.[0]?.textContent||'טרם נבחר');});page.append(summary,label,control);if(choices?.classList.contains('touch-choices'))page.append(choices);groups.append(page);}if(fields.length)form.prepend(groups);
   }
   const reporter=$('inline-action-reporter');if(reporter){reporter.querySelector('h3').textContent='דיווח פעולה';reporter.querySelector('p').textContent='לחץ על פעולה, בחר פרטים וקבל שאלת בדיקה.';}
   syncMic();
   arrangePreparation();
   requestAnimationFrame(sizeWorkspace);
 }
 function arrangePreparation(){
   // Move existing controls, preserving their values and event handlers.
   let flow=$('preparation-workflow'),offers=$('dish-offers');
   if(flow){flow.querySelector(':scope > h2')?.remove();while(flow.firstChild){const child=flow.firstChild;if(child.nodeType===1&&child.classList.contains('decision-question')&&$('cooking-intake'))$('cooking-intake').append(child);else journey.append(child);}flow.remove();}
   if(offers){while(offers.firstChild)learning.append(offers.firstChild);offers.remove();}
   if(mode!=='prepare'||mentor.state?.workflow!=='user')return;
   offers=el('section','','dish-offers');offers.id='dish-offers';
   while(learning.firstChild)offers.append(learning.firstChild);
   flow=el('section','','preparation-workflow');flow.id='preparation-workflow';
   const intake=$('cooking-intake'),form=$('cooking-intake-form');if(intake&&form){let below=false;for(const child of [...intake.children]){if(below)flow.append(child);if(child===form)below=true;}}
   for(const child of [...journey.children])if(!['cooking-intake','cooking-live-stage'].includes(child.id))flow.append(child);
   if(flow.children.length)learning.append(flow);
   function place(){
     if(mode!=='prepare'||!offers.isConnected)return;
     offers.remove();
     const columns=[journey,companion,learning];
     const height=column=>[...column.children].filter(child=>getComputedStyle(child).display!=='none').reduce((sum,child)=>{const style=getComputedStyle(child);return sum+child.getBoundingClientRect().height+parseFloat(style.marginTop||0)+parseFloat(style.marginBottom||0);},0);
     const target=window.innerWidth>1000?columns.reduce((shortest,column)=>height(column)<height(shortest)?column:shortest):learning;
     target.append(offers);offers.dataset.column=target.id;
   }
   if(offers.children.length){learning.append(offers);requestAnimationFrame(place);}
   window.placeDishOffers=place;
 }
 function sizeWorkspace(){
   if(!mentor.state||workspace.hidden)return;
   // Reserve the actual remaining viewport, instead of accumulating card heights.
   const top=workspace.getBoundingClientRect().top+window.scrollY;
   workspace.style.setProperty('--kitchen-height',Math.max(320,window.innerHeight-top-12)+'px');
 }
 window.addEventListener('resize',sizeWorkspace);
 window.addEventListener('resize',()=>window.placeDishOffers?.());
 workspace.addEventListener('toggle',()=>requestAnimationFrame(()=>window.placeDishOffers?.()),true);
 new ResizeObserver(()=>requestAnimationFrame(sizeWorkspace)).observe(home);
 function syncMic(){const listening=$('voice-input')?.getAttribute('aria-pressed')==='true';const button=$('live-microphone');if(button){button.setAttribute('aria-pressed',String(listening));button.textContent=listening?'🎙 מקשיב… לחץ לעצירה':'🎙 דבר לשף';}const indicator=$('live-listening');if(indicator)indicator.textContent=listening?'● ● ● המערכת מאזינה — הדיבור יופיע בשדה הדיווח':'המיקרופון כבוי';}
 if($('voice-input'))new MutationObserver(syncMic).observe($('voice-input'),{attributes:true,attributeFilter:['aria-pressed']});
 const render=renderCoach;renderCoach=function(){
   // The base renderer owns rebuilding suggestions; discard any previously relocated copy.
   $('dish-offers')?.remove();render();paint();
 };renderCoach();
})();
