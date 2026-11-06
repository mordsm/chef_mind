'use strict';
// Presentation and explicit starter choices; all cooking decisions stay on the server.
(() => {
 Object.assign(words.he,{disconnected:'מצב מקומי'});
 if($('notice')?.textContent.trim()==='מנותק')$('notice').textContent='מצב מקומי';
 const meals=[
  {id:'beef',title:'תבשיל בקר',dish:'תבשיל בקר בבישול ארוך',kind:'בסיר',note:'6 צעדים · ריכוך ובדיקת מוכנות',ingredients:['שוק בקר','בצל','גזר','שמן זית','מלח','מים'],facts:{family:'meat',protein:'beef',equipment:'pot',method:'boil_simmer',quantity:'1 ק״ג',cut:'קוביות שוק בקר כ־3 ס״מ',goal:'soft'}},
  {id:'fish',title:'סלמון בתנור',dish:'פילה סלמון בתנור',kind:'בתנור',note:'4 צעדים · פילה מופשר ומדחום',ingredients:['סלמון','לימון','שמן זית','מלח'],facts:{family:'fish',equipment:'oven',method:'oven_roast',quantity:'500 גרם',cut:'פילה מופשר בעובי כ־3 ס״מ',goal:'soft'}},
  {id:'legumes',title:'עדשים וירקות',dish:'תבשיל עדשים וירקות',kind:'בסיר',note:'5 צעדים · עדשים ירוקות יבשות',ingredients:['עדשים ירוקות יבשות','גזר','בצל','עגבניות','מים','מלח'],facts:{family:'legumes',equipment:'pot',method:'boil_simmer',quantity:'500 גרם',goal:'soft'}},
  {id:'soup',title:'מרק ירקות',dish:'מרק ירקות עשיר',kind:'בסיר',note:'5 צעדים · חיתוך, בישול ותיבול',ingredients:['גזר','קישוא','תפוח אדמה','בצל','שמן זית','מים','מלח'],facts:{family:'soup',equipment:'pot',method:'boil_simmer',quantity:'1 ק״ג',goal:'soft'}},
  {id:'salad',title:'סלט ירקות',dish:'סלט ירקות עם רוטב לימון ושמן',kind:'ללא חימום',note:'4 צעדים · ירקות ורוטב פשוט',ingredients:['מלפפון','עגבנייה','חסה','שמן זית','לימון','מלח'],facts:{family:'vegetables',equipment:'other',method:'',quantity:'500 גרם',goal:'crisp'}},
  {id:'bread',title:'לחם שמרים',dish:'לחם שמרים פשוט',kind:'בתנור',note:'5 צעדים · כיכר קטנה ללא לישה',ingredients:['קמח חיטה','שמרים יבשים','מים','מלח','שמן'],facts:{family:'starch',equipment:'oven',method:'',quantity:'500 גרם',cut:'כיכר קטנה',goal:'soft'}}
 ];
 const welcome=el('section','','ux-welcome');welcome.id='ux-welcome';
 welcome.append(el('p','המטבח שלך, צעד אחר צעד','ux-eyebrow'),el('h2','מה מבשלים היום?'),el('p','בחר מנה להתחלה מודרכת, או כתוב בהמשך מה תרצה להכין.','ux-intro'));
 const cards=el('div','','ux-meals');cards.setAttribute('aria-label','מנות עם תוכנית הכנה');
 for(const meal of meals){const button=actionButton('meal-'+meal.id,'',()=>openMeal(meal),'ux-meal');button.append(el('span',meal.kind,'ux-meal-kind'),el('strong',meal.title),el('span',meal.note,'ux-meal-note'),el('span','לבחירת המנה ←','ux-meal-link'));cards.append(button);}
 welcome.append(cards);home.prepend(welcome);
 const dialog=el('dialog','','ux-meal-dialog');dialog.id='ux-meal-dialog';dialog.setAttribute('aria-labelledby','ux-meal-title');
 const heading=el('h2');heading.id='ux-meal-title';heading.tabIndex=-1;
 const close=actionButton('ux-meal-close','סגירה',()=>dialog.close(),'secondary');
 const form=el('form','','ux-meal-form');form.id='ux-meal-form';
 const intro=el('p','בדוק את הפרטים והרכיבים לפני שמתחילים. אפשר לשנות את הכמות והנתח.');
 function field(id,label,type='text'){const wrap=el('label',label),input=el('input');input.id=id;input.type=type;wrap.htmlFor=id;wrap.append(input);return {wrap,input};}
 const quantity=field('ux-meal-quantity','כמות');quantity.input.required=true;quantity.input.maxLength=120;
 const cut=field('ux-meal-cut','נתח, עובי ומצב חומר הגלם');cut.input.maxLength=200;
 const equipment=el('p','','ux-equipment'),ingredients=el('ul','','ux-ingredients');
 const allergy=field('ux-meal-allergies','אלרגיות או רכיבים שצריך להימנע מהם');allergy.input.placeholder='למשל: דגים, חיטה, אגוזים';
 const preference=field('ux-meal-kosher','ללא ערבוב בשר וחלב','checkbox');
 const confirm=field('ux-meal-confirm','בדקתי שהרכיבים מתאימים לי וזמינים להכנה','checkbox');confirm.input.required=true;
 const status=el('p');status.id='ux-meal-status';status.setAttribute('role','status');
 const submit=el('button','מתחילים לבשל');submit.type='submit';submit.id='ux-meal-start';
 form.append(intro,quantity.wrap,cut.wrap,equipment,el('h3','מה צריך להכין'),ingredients,allergy.wrap,preference.wrap,confirm.wrap,status,submit);
 dialog.append(close,heading,form);document.body.append(dialog);
 let selected=null,opener=null;
 function openMeal(meal){
  if(mentor.busy)return;selected=meal;const chooser=$('dish-selection-dialog');opener=chooser?.open?$('choose-cooking-dish'):document.activeElement;if(chooser?.open)chooser.close();
  heading.textContent=meal.title;quantity.input.value=meal.facts.quantity;
  quantity.wrap.firstChild.textContent=meal.id==='bread'?'משקל בצק לכיכר קטנה — 400–540 גרם':meal.id==='beef'?'משקל הבשר':meal.id==='fish'?'משקל הדג':'כמות חומרי הגלם למנה';
  cut.wrap.hidden=!['fish','beef'].includes(meal.id);cut.input.value=meal.facts.cut||'';
  equipment.textContent='כלים: '+({pot:'סיר עם מכסה',oven:'תנור ותבנית',other:'קרש, סכין וקערה'}[meal.facts.equipment])+(meal.id==='fish'||meal.id==='beef'?' ומדחום מזון':'');
  ingredients.replaceChildren(...meal.ingredients.map(name=>el('li',name)));
  allergy.input.value=$('allergies').value;preference.input.checked=$('kosher').checked;confirm.input.checked=false;status.textContent='';submit.disabled=false;
  dialog.showModal();heading.focus();
 }
 dialog.addEventListener('close',()=>{if(opener?.isConnected)opener.focus();});
 const chooser=$('dish-selection-dialog');if(chooser){const choices=el('section','','ux-quick-choices');choices.append(el('h3','או בחר מנה עם תוכנית מוכנה'));const grid=el('div','','ux-meals');for(const meal of meals){const button=actionButton('choose-meal-'+meal.id,meal.title,()=>openMeal(meal),'secondary');grid.append(button);}choices.append(grid);chooser.append(choices);}
 form.addEventListener('submit',async event=>{
  event.preventDefault();if(!selected||mentor.busy)return;
  const meal=selected;
  if(meal.id==='bread'&&!/^\s*(?:4\d\d|5[0-3]\d|540)\s*(?:גרם|g)\s*$/.test(quantity.input.value)){status.textContent='למסלול הזה בחר משקל בצק בין 400 ל־540 גרם, למשל 500 גרם.';return;}
  submit.disabled=true;status.textContent='מכין את סדר העבודה…';
  $('allergies').value=allergy.input.value;$('kosher').checked=preference.input.checked;
  const started=await coachCommand('start_custom',{dish_title:meal.dish,ingredients:meal.ingredients,method:meal.facts.method,allergies:allergy.input.value.split(',').map(v=>v.trim()).filter(Boolean),forbid_meat_dairy:preference.input.checked});
  if(!started){status.textContent=coachNotice.textContent||'לא ניתן להתחיל כרגע. הפרטים נשמרו כאן.';submit.disabled=false;return;}
  const ready=await coachCommand('intake',{intake_facts:{...meal.facts,quantity:quantity.input.value.trim(),cut:cut.input.value.trim()}});
  if(!ready){status.textContent=coachNotice.textContent||'הפרטים טרם נשמרו. נסה שוב.';submit.disabled=false;return;}
  dialog.close();
  if(ready.custom_steps.length)$('mode-live')?.click();
  workspace.scrollIntoView({behavior:'instant',block:'start'});
 });
 function paint(){
  const state=mentor.state;welcome.hidden=!!state;
  document.body.classList.add('chef-experience');
  const setup=$('kitchen-setup');if(setup){setup.querySelector(':scope > summary').textContent=state?'פרטי המנה והעדפות':'מבשלים משהו אחר? כתוב את המנה';}
  const oldHeading=home.querySelector(':scope > h2');if(oldHeading)oldHeading.hidden=true;
  $('mode-prepare').textContent='פרטי ההכנה';$('mode-live').textContent='בישול צעד אחר צעד';$('choose-cooking-dish').textContent='＋ מנה חדשה';
  if(!state)return;
  const stage=$('cooking-live-stage'),measurement=document.querySelector('.kitchen-measurement');
  if(stage&&measurement&&document.body.classList.contains('cooking-live')){stage.append(measurement);measurement.open=selectedStep()?.minimum_temperature!=null;}
  if(stage&&state.custom_steps.length){
   const allDone=state.custom_steps.every(step=>state.completed_step_ids.includes(step.id));
   const done=$('live-done');if(done){done.hidden=allDone;done.textContent='בדקתי וביצעתי — לשלב הבא';}
   if(allDone&&state.status==='active'&&!$('ux-finish'))stage.append(actionButton('ux-finish','סיום ושמירת סיכום',()=>coachCommand('finish')));
   const count=stage.querySelector('.live-step-counter');if(count)count.textContent=allDone?'כל פעולות ההכנה סומנו כהושלמו':`שלב ${state.current_step+1} מתוך ${state.custom_steps.length}`;
  }
  const reporter=$('inline-action-reporter');
  if(reporter){let tools=$('ux-report-tools');if(!tools){tools=el('details','','ux-report-tools');tools.id='ux-report-tools';tools.append(el('summary','יומן פעולות וטיימרים'),el('p','לתיעוד פעולות ולתזכורות נוספות, פתח את היומן.'));companion.append(tools);}if(reporter.parentElement!==tools)tools.append(reporter);}
  const voice=$('cockpit-voice');if(voice){
   voice.querySelector(':scope > h2').textContent='צריך עזרה? שאל את השף';
   const transcript=$('voice-last-transcript');if(transcript)transcript.hidden=transcript.textContent==='הדיבור שלך יופיע כאן.';
   const hint=voice.querySelector(':scope > small');if(hint)hint.textContent='אפשר לדבר או להקליד. השאלה נשלחת רק בלחיצה על שליחה.';
   const editor=voice.querySelector('.voice-question-editor');if(editor){editor.open=true;editor.querySelector(':scope > summary').textContent='כתיבת שאלה לשף';}
  }
 }
 document.addEventListener('chef-layout-updated',paint);
 document.addEventListener('chef-voice-transcript',()=>{const transcript=$('voice-last-transcript');if(transcript)transcript.hidden=false;});
 const render=renderCoach;renderCoach=function(){render();paint();};paint();
})();
