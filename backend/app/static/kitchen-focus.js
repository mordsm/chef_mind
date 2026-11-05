'use strict';
// Presentation layer: preserve the existing commands, drafts and safety checks.
(() => {
 const setup=el('details','','kitchen-setup');setup.id='kitchen-setup';setup.open=true;
 setup.append(el('summary','פרטי המנה ושיטת ההכנה'));
 const preferences=el('details','','kitchen-preferences');preferences.append(el('summary','אופן הליווי וסגנון השף'),mentorSettings);
 const ingredients=el('details','','kitchen-ingredients');ingredients.append(el('summary','רכיבים נוספים — לא חובה'));
 const ingredientLabel=el('label','רכיבים למנה, מופרדים בפסיקים');ingredientLabel.htmlFor='custom-ingredients';ingredients.append(ingredientLabel,ingredientInput);
 const dishLabel=el('label','1. מה מבשלים?');dishLabel.htmlFor='custom-dish-title';
 const methodLabel=el('label','2. איך מכינים?');methodLabel.htmlFor='custom-method';
 const methodHelp=el('p','בחר שיטה מתוך ההמלצות למנה, או התחל ובחר בהמשך.','field-help');
 customStart.replaceChildren(dishLabel,customTitle,quickStarts,methodLabel,customMethod,methodHelp,methodReason,ingredients,preferences,startWork,updateDish);
 setup.append(customStart,examples);home.insertBefore(setup,guestBanner);
 startWork.textContent='התחל עבודה';
 publicIntro.hidden=true;connection.classList.add('compact-connection');
 connectionSummary.textContent='המטבח האישי · התחברות ושחזור';
 setup.append(openInventory,guestBanner,connection);guestBanner.classList.add('kitchen-secondary');
 const newWork=actionButton('kitchen-new-work','מנה חדשה',()=>{setup.open=true;startWork.hidden=false;customTitle.focus();});newWork.hidden=true;home.append(newWork);
 // Keep the three work areas visible together, as in the original workbench.
 let previousWork=null,inputMode='report';

 function compose(form){
   const text=$('work-report');if(!form||!text)return;
   form.querySelector('h3').textContent='מקום אחד לדיווח ולשאלה';
   const modes=el('div','','composer-modes');modes.setAttribute('role','group');modes.setAttribute('aria-label','סוג ההודעה לשף');
   const report=actionButton('composer-report','דיווח מהמטבח',()=>choose('report'));
   const ask=actionButton('composer-ask','שאלה לשף',()=>choose('ask'));modes.append(report,ask);text.insertAdjacentElement('beforebegin',modes);
   const label=el('label');label.htmlFor='work-report';text.insertAdjacentElement('beforebegin',label);
   function choose(mode){inputMode=mode;mentor.inputMode=mode;report.setAttribute('aria-pressed',String(mode==='report'));ask.setAttribute('aria-pressed',String(mode==='ask'));label.textContent=mode==='report'?'מה השתנה במנה?':'מה תרצה לשאול?';text.placeholder=mode==='report'?'למשל: הנוזל רתח':'למשל: מתי להוסיף מלח?';form.querySelector('button[type="submit"]').textContent=mode==='report'?'שלח דיווח לשף':'שלח שאלה לשף';}
   choose(inputMode);const dictate=$('work-report-dictate');dictate.textContent='🎙 דבר לשף';
   const sendRow=el('div','','kitchen-send-row');dictate.insertAdjacentElement('beforebegin',sendRow);sendRow.append(dictate,form.querySelector('button[type="submit"]'));
   const stop=actionButton('kitchen-stop-voice','■ עצור הקשבה',()=>document.dispatchEvent(new Event('coach-stop-dictation')));stop.hidden=true;dictate.insertAdjacentElement('afterend',stop);
   const hint=el('small','לחץ למיקרופון, דבר ושלח. אפשר גם להקליד.');form.append(hint);
   form.append(speechTarget,coachNotice);
   function syncVoice(){const listening=$('voice-input')?.getAttribute('aria-pressed')==='true';dictate.textContent=listening?'🎙 מקשיב… לחץ לעצירה':'🎙 דבר לשף';dictate.setAttribute('aria-pressed',String(listening));stop.hidden=!listening;}
   const voiceObserver=new MutationObserver(syncVoice);syncVoice();
   if(window.kitchenVoiceObserver)window.kitchenVoiceObserver.disconnect();window.kitchenVoiceObserver=voiceObserver;
   if($('voice-input'))voiceObserver.observe($('voice-input'),{attributes:true,attributeFilter:['aria-pressed']});
 }

 function organize(){
   const state=mentor.state,hasWork=!!state,custom=state?.workflow==='user';
   document.body.classList.toggle('kitchen-has-work',hasWork);document.body.classList.toggle('kitchen-user-work',custom);
   workspace.hidden=!hasWork;userToolbar.hidden=!custom;resumeButton.hidden=true;newWork.hidden=!hasWork;
   if(previousWork!==state?.id){setup.open=true;previousWork=state?.id||null;inputMode='report';}
   startWork.hidden=false;updateDish.hidden=!custom||state.status!=='active';
   home.querySelector('h2').textContent=hasWork?'המטבח שלך':'מה מבשלים היום?';
   if(!hasWork)return;
   const voiceInputButton=$('voice-input');if(voiceInputButton)voiceInputButton.hidden=custom;
   const voiceSummary=speechTarget.querySelector('.voice-tools summary');if(voiceSummary)voiceSummary.textContent=custom?'הקראת ההנחיה':'כלי קול — הקלדה בקול והקראת ההנחיה';
   if(!custom){chatForm.hidden=state.status!=='active';return;}
   chatForm.hidden=true;talkButton.hidden=true;
   companionHeading.querySelector('h2').textContent='השף שלך';
   const dock=$('active-work-guidance');
   // The current step stays on stage; the editable plan is opened on demand.
   const list=$('user-step-list'),selected=list?.querySelector('.selected');
   if(selected)list.insertAdjacentElement('beforebegin',selected);
   const plan=el('details','','kitchen-plan');plan.id='kitchen-plan';plan.open=true;plan.append(el('summary','תוכנית ההכנה · השלבים הנוכחיים'));
   if(list)plan.append(list);
   if($('suggested-actions'))plan.append($('suggested-actions'));journey.append(plan);
   if(!state.custom_steps.length&&state.decision_questions?.length){const message=journey.querySelector('.work-empty');if(message)message.textContent=state.station_protocol?.blocks?.length?'פקודת התחנה מוצגת לצד תוכנית ההכנה; השלם רק את הפרט הבא לביצוע.':'השף יתחיל בהדרכה אחרי בחירת הפרטים שמופיעים מימין.';
     // All available cooking paths are shown as explicit choices in the guidance dock.
   }
   if(dock){
     const reply=compactConversation.querySelector('p');
     if(reply&&!state.station_protocol?.blocks?.length){let text=reply.textContent;for(const q of state.decision_questions||[])text=text.replace(q.text,'');
       if(state.decision_answers?.goal||(state.decision_questions||[]).some(q=>q.id==='goal')){
         for(const question of state.context?.questions||[])text=text.replaceAll(question,'');
       }
       const lines=text.split(/\n\s*\n/).map(x=>x.trim()).filter(Boolean);reply.replaceChildren();
       const instructions=el('ol','','kitchen-guidance-lines');for(const line of lines)instructions.append(el('li',line));reply.append(instructions);
     }
     const background=el('details','','kitchen-action-background');background.append(el('summary','הסבר נוסף ובדיקת מוכנות לפני הגשה'));
     for(const tip of [...dock.querySelectorAll('.context-tip')]){
       const safety=state.context?.tips.some(item=>item.origin==='SAFETY_POLICY'&&tip.textContent.includes(cleanGuidance(item.text)));
       if(!tip.classList.contains('book-knowledge-tip'))background.append(tip);
     }
     if(background.children.length>1)dock.append(background);
     companion.append(statusQuestion);
     if(state.problem_rule_status==='clarify'){
       const heading=statusQuestion.querySelector('h3');if(heading)heading.textContent='כדי להתאים את הטיפול למנה';
     }
     if(state.problem_rule_match?.variant_id&&state.problem_rule_match.variant_id!=='fallback'){
       const provenance=el('small','הטיפול נבחר לפי פרטי המנה והתשובה שבחרת.','problem-provenance');
       for(const source of state.problem_rule_match.sources||[]){if(source.startsWith('https://')){const link=el('a',' מקור');link.href=source;link.target='_blank';link.rel='noopener noreferrer';provenance.append(link);}}
       dock.append(provenance);
     }
     const groups=[...statusQuestion.querySelectorAll('.decision-question')];groups.forEach(group=>group.hidden=false);
     if(state.problem_rule_status==='choose'||mentor.problemOpen)for(const group of groups)group.hidden=true;
     const stepChoices=$('cooking-step-choices');if(stepChoices)dock.append(stepChoices);
     if(state.status==='active'){companion.append(actions);if(stepChoices)doneButton.hidden=true;}
   }
   const form=$('user-report-form');if(form){companion.append(form);compose(form);}
   companion.append(topicDetails);photoButton.hidden=true;
   const attachments=el('details','','kitchen-attachments');attachments.append(el('summary','תמונה לצפייה אישית'),photoInput,photoPreview,actionButton('kitchen-photo','📷 הוסף תמונה',()=>photoInput.click()));companion.append(attachments);
   const quick=journey.querySelector('.quick-reports');if(quick&&form)form.insertBefore(quick,form.querySelector('textarea'));
   const measurement=journey.querySelector('.measurement-report');if(measurement){const detail=el('details','','kitchen-measurement');detail.open=selectedStep()?.title==='אפייה ובדיקת המרכז';detail.append(el('summary','דיווח מדידת טמפרטורה'),measurement);journey.append(detail);}
   const clock=$('coach-clock'),timerRow=$('user-timer-start')?.parentElement;
   if(clock&&timerRow){
     const timer=el('section','','kitchen-timer');timer.id='kitchen-timer';
     timer.append(el('strong','תזכורת · '+(selectedStep()?.title||'המנה הנוכחית')),clock);
     const seconds=timerRow.querySelector('input');seconds.id='kitchen-timer-seconds';
     const label=el('label','משך בשניות');label.htmlFor=seconds.id;
     const duration=el('details','','kitchen-timer-duration');duration.append(el('summary','שינוי משך התזכורת'),label,seconds);timer.append(duration);
     $('user-timer-start').textContent=state.timer_deadline?'↻ הפעל מחדש':'▶ הפעל טיימר';$('user-pause').textContent=state.status==='paused'?'▶ המשך':'Ⅱ השהה';
     $('user-pause').hidden=!state.timer_deadline&&state.status!=='paused';
     const cancel=actionButton('kitchen-timer-stop','■ בטל',()=>coachCommand('timer_cancel'));cancel.hidden=!state.timer_deadline&&state.paused_remaining===null;timerRow.append(cancel);
     timer.append(timerRow);journey.insertBefore(timer,selected||dock||journey.firstChild);
   }
   const finish=actionButton('kitchen-finish','סיום הבישול',()=>{if(confirm('לסיים את הבישול ולפתוח סיכום?'))void coachCommand('finish');});finish.hidden=state.status==='completed';plan.append(finish);
 }
 const render=renderCoach;renderCoach=function(){
   // Put the draft back where the existing renderer captures it before replacing DOM.
   const priorForm=$('user-report-form');if(priorForm)journey.append(priorForm);
   if(typeof voiceStatus!=='undefined')speechTarget.append(voiceStatus);
   companion.append(speechTarget,coachNotice);
   for(const old of companion.querySelectorAll('.kitchen-attachments'))old.remove();
   render();organize();
 };renderCoach();
})();
