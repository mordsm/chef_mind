'use strict';
// User-owned planning is the default; authored journeys remain optional examples.
const customStart=el('form','','custom-start');customStart.id='custom-start';
const customTitle=el('input');customTitle.id='custom-dish-title';customTitle.maxLength=200;customTitle.required=true;customTitle.placeholder='למשל: כנפי הודו בתנור, אורז עם ירקות, דג ברוטב';
customTitle.setAttribute('aria-label','מה אתה מתכנן להכין?');
const customMethod=el('select');customMethod.id='custom-method';customMethod.setAttribute('aria-label','שיטת הכנה לבחירתך');
const emptyMethod=el('option','בחר מנה כדי לראות שיטות מומלצות');emptyMethod.value='';customMethod.append(emptyMethod);customMethod.disabled=true;
const ingredientInput=el('input');ingredientInput.id='custom-ingredients';ingredientInput.maxLength=2000;ingredientInput.placeholder='מרכיבים שבהם תשתמש — לא חובה, מופרדים בפסיקים';ingredientInput.setAttribute('aria-label','המרכיבים המתוכננים למנה');
const roleMode=el('select');roleMode.id='coach-role';roleMode.setAttribute('aria-label','אופן הליווי');for(const [value,label] of [['mentor','מנטור — ליווי קרוב'],['consultant','יועץ — ליווי מרווח']]){const option=el('option',label);option.value=value;roleMode.append(option);}
const mentorSettings=el('div','','mentor-settings');mentorSettings.id='mentor-settings';for(const [title,control] of [['אופן הליווי',roleMode],['סגנון השף',personality]]){const label=el('label');label.append(el('span',title),control);mentorSettings.append(label);}
const startWork=el('button','התחל עבודה');startWork.id='start-work';startWork.type='submit';customStart.append(customTitle,customMethod,ingredientInput,startWork);home.insertBefore(mentorSettings,dishChoices);home.insertBefore(customStart,dishChoices);
const methodReason=el('div','','method-policy-info');methodReason.id='method-policy-info';methodReason.setAttribute('aria-live','polite');customStart.insertAdjacentElement('afterend',methodReason);
let methodChoiceRequest=0,methodChoiceTimer,methodChoiceTitle='';
function setSelectedMethod(value){const option=[...customMethod.options].find(option=>option.value===value||option.textContent===value);customMethod.value=option?.value||'';}
async function refreshMethodChoices(){const ticket=++methodChoiceRequest,title=customTitle.value.trim(),selected=title===methodChoiceTitle?customMethod.value:'';methodChoiceTitle=title;customMethod.disabled=true;if(!title){customMethod.replaceChildren(el('option','בחר מנה כדי לראות שיטות מומלצות'));customMethod.firstChild.value='';methodReason.replaceChildren();return;}try{const body={dish_title:title,ingredients:ingredientInput.value.split(',').map(value=>value.trim()).filter(Boolean)};const result=identityUser?await api('/v1/coach/method-policy/my-options','POST',body):await publicApi('/v1/coach/method-policy/options',body);if(ticket!==methodChoiceRequest)return;customMethod.replaceChildren();const empty=el('option','אבחר בהמשך');empty.value='';customMethod.append(empty);for(const method of result.allowed){const option=el('option',method.label);option.value=method.id;customMethod.append(option);}setSelectedMethod(selected||(mentor.state?.dish_title===title?mentor.state.method:''));customMethod.disabled=!result.allowed.length;methodReason.replaceChildren(el('p','פרופיל ההמלצות: '+result.profile_title));if(!result.allowed.length)methodReason.append(el('p',result.reason,'error'));const reasons=el('details');reasons.append(el('summary','למה שיטות אחרות אינן מומלצות?'));for(const item of result.blocked)reasons.append(el('p',item.label+': '+item.reason));methodReason.append(reasons);}catch{if(ticket===methodChoiceRequest){customMethod.replaceChildren(el('option','לא ניתן לטעון המלצות'));customMethod.firstChild.value='';methodReason.replaceChildren(el('p','המלצות ההכנה לא נטענו. בדוק חיבור והרשאות לפני בחירת שיטה.','error'));}}}
function queueMethodChoices(){if(customTitle.value.trim()!==methodChoiceTitle)customMethod.value='';clearTimeout(methodChoiceTimer);methodChoiceTimer=setTimeout(()=>void refreshMethodChoices(),200);}
customTitle.addEventListener('input',queueMethodChoices);ingredientInput.addEventListener('input',queueMethodChoices);customTitle.addEventListener('change',()=>void refreshMethodChoices());ingredientInput.addEventListener('change',()=>void refreshMethodChoices());document.addEventListener('chef-auth-changed',()=>void refreshMethodChoices());document.addEventListener('chef-method-policy-changed',()=>void refreshMethodChoices());document.addEventListener('chef-method-policy-error',event=>methodReason.prepend(el('p',event.detail,'error')));
const updateDish=actionButton('update-dish','עדכן פרטי מנה',()=>{if(customTitle.value.trim())void coachCommand('update_plan',{dish_title:customTitle.value.trim(),method:customMethod.value,ingredients:ingredientInput.value.split(',').map(value=>value.trim()).filter(Boolean)});});updateDish.hidden=true;customStart.append(updateDish);
const examples=el('details','','optional-journeys');examples.append(el('summary','מתווים לדוגמה — אפשרות נוספת'),dishChoices);home.insertBefore(examples,guestBanner);
const quickStarts=el('div','','custom-quick-starts');
for(const title of ['כנפי הודו','דג ברוטב','אורז עם ירקות','מרק ירקות']){const button=actionButton('quick-'+title.replaceAll(' ','-'),title,()=>{customTitle.value=title;customTitle.dispatchEvent(new Event('input'));customTitle.focus();},'secondary');quickStarts.append(button);}customStart.insertAdjacentElement('afterend',quickStarts);
customStart.addEventListener('submit',event=>{event.preventDefault();if(!customTitle.value.trim()){customTitle.focus();return;}void coachCommand('start_custom',{dish_title:customTitle.value.trim(),method:customMethod.value,ingredients:ingredientInput.value.split(',').map(value=>value.trim()).filter(Boolean),mode:roleMode.value});});
roleMode.addEventListener('change',()=>{if(mentor.state?.workflow==='user')void coachCommand('mode',{mode:roleMode.value});});
const userToolbar=el('div','','user-toolbar');userToolbar.id='user-toolbar';
userToolbar.append(actionButton('toolbar-start','התחל עבודה',()=>customTitle.focus()),
 actionButton('toolbar-report','דיווח על שלב',()=>$('work-report')?.focus()),
 actionButton('toolbar-help','בקשת עזרה',()=>chatInput.focus()),
 actionButton('toolbar-finish','סיום',()=>{if(mentor.state&&confirm('לסיים את העבודה ולפתוח סיכום?'))void coachCommand('finish');}));
workspace.insertAdjacentElement('beforebegin',userToolbar);userToolbar.hidden=true;
const topicDetails=el('details','','chef-history');topicDetails.append(el('summary','היסטוריית השיחה'));conversation.insertAdjacentElement('beforebegin',topicDetails);
const compactConversation=el('div','','current-chef-message');compactConversation.id='current-chef-message';topicDetails.insertAdjacentElement('beforebegin',compactConversation);
compactConversation.setAttribute('role','status');compactConversation.setAttribute('aria-live','polite');
topicDetails.append(conversation);
function selectedStep(){return mentor.state?.custom_steps?.[mentor.state.current_step];}
function reportWork(text){return coachCommand('report',{message:text});}
function cleanGuidance(text){return (text||'').replaceAll('זוהו קורקבנים, ולא כבד עוף. ','');}
function appendContextTip(parent,tip){const text=cleanGuidance(tip.text);if(!text.trim()||text.split(/\s+/).length>(tip.practical?60:15))return;const card=el('details','','context-tip');card.append(el('summary',tip.practical?tip.title:'טיפ שף'),el('p',text));parent.append(card);}
let renderedWorkId=null;
let workDraftState={};
function renderUserWorkbench(){
 document.querySelectorAll('#add-user-step').forEach(form=>form.remove());
 const state=mentor.state,context=state.context,steps=state.custom_steps,active=state.status==='active',current=selectedStep();
 const drafts=workDraftState.id===state.id?workDraftState:{};
 if(renderedWorkId!==state.id){customTitle.value=state.dish_title;setSelectedMethod(state.method);ingredientInput.value=state.ingredients.join(', ');void refreshMethodChoices();}
 renderedWorkId=state.id;userToolbar.hidden=false;roleMode.value=state.mode;personality.value=state.chefPersonality;
 compactConversation.hidden=false;compactConversation.replaceChildren();topicDetails.hidden=false;
 const guidanceDock=el('aside','','active-work-guidance');guidanceDock.id='active-work-guidance';guidanceDock.append(el('h3','הנחיות לפעולה הנוכחית'),compactConversation);
 if(state.method_warning)guidanceDock.append(el('p',state.method_warning,'error'));
 const latestReply=state.messages.filter(message=>message.role==='chef').at(-1);const latestText=cleanGuidance(latestReply?.text);if(state.station_protocol?.blocks?.length)renderStationProtocol(compactConversation,state.station_protocol);else if(latestReply)compactConversation.append(el('p',latestText,'chat-bubble chef-bubble'));
 const inlineTips=[state.learning_focus||context?.tips[0],...(context?.tips||[]).filter(tip=>['SAFETY_POLICY','OBSIDIAN_MCGEE','OBSIDIAN_FOODLAB'].includes(tip.origin))].filter(Boolean);
 if(!state.station_protocol?.blocks?.length)for(const tip of inlineTips.filter((tip,index,all)=>all.findIndex(item=>cleanGuidance(item.text)===cleanGuidance(tip.text))===index)){if(!latestText.includes(cleanGuidance(tip.text)))appendContextTip(guidanceDock,tip);}
 journey.append(el('span',state.status==='completed'?'העבודה הסתיימה':state.status==='paused'?'הליווי מושהה':'השף מוביל · אתה בוחר ומבשל','badge'),el('h2',state.dish_title),el('p','אבנה איתך את סדר ההכנה ואדריך בכל צעד. אפשר להתאים את הבחירות ולבקש עזרה בכל שלב.','work-ownership'));
 const checked=state.completed_step_ids.length;
 if(steps.length){const progress=el('progress');progress.max=steps.length;progress.value=checked;progress.setAttribute('aria-label','פעולות שסימנת כהושלמו');journey.append(progress,el('small',`${checked} מתוך ${steps.length} פעולות סומנו על ידך`));}
 const list=el('div','','user-step-list');list.id='user-step-list';
 steps.forEach((entry,index)=>{
   const card=el('article','',index===state.current_step?'user-step-card selected':'user-step-card');card.dataset.stepId=entry.id;const actionBody=el('div','','step-action-body');card.append(actionBody);
   const select=actionButton('select-step-'+index,(state.completed_step_ids.includes(entry.id)?'✓ ':'')+entry.title,()=>coachCommand('select_step',{step_id:entry.id}),'user-step-title');actionBody.append(select);
   if(entry.instruction!==entry.title)actionBody.append(el('p',entry.instruction));
   if(entry.source?.startsWith('USER_GRAPH_ADAPTED:')){const detail=el('details');detail.open=index===state.current_step;detail.append(el('summary','למה, מה לבדוק והכנה להמשך'),el('p',entry.why));for(const line of [...entry.successCriteria,...entry.commonMistakes])detail.append(el('p',line));if(entry.next_step_prep)detail.append(el('p','להמשך: '+entry.next_step_prep));detail.append(el('small','מעץ הידע · בניסוח מותאם'));actionBody.append(detail);}
   if(active){const controls=el('div','','step-controls');
     controls.append(actionButton('edit-step-'+index,'עריכה',()=>{const form=el('form','','step-edit-form'),title=el('input'),instruction=el('textarea');title.value=entry.title;title.maxLength=160;title.required=true;title.setAttribute('aria-label','שם הפעולה');instruction.value=entry.instruction;instruction.maxLength=1000;instruction.setAttribute('aria-label','הוראות שלך לפעולה');const save=el('button','שמירה');save.type='submit';form.append(title,instruction,save);form.addEventListener('submit',event=>{event.preventDefault();void coachCommand('edit_step',{step_id:entry.id,step_title:title.value.trim(),step_instruction:instruction.value.trim()});});actionBody.append(form);title.focus();}));
     if(index>0)controls.append(actionButton('move-step-'+index,'↑',()=>coachCommand('move_step',{step_id:entry.id,target_index:index-1})));
     controls.append(actionButton('remove-step-'+index,'×',()=>coachCommand('remove_step',{step_id:entry.id})));actionBody.append(controls);
   }
   if(index===state.current_step)card.append(guidanceDock);list.append(card);
 });journey.append(list);
 if(!steps.length)journey.append(guidanceDock,el('p',state.intake_guidance?'אפשר לבחור פעולה במאגר למטה ולקבל הדרכה. הפרטים והמתכון שחסרים מופיעים באזור ההכוונה.':'ענה על הבחירות של השף כדי להתחיל בהכנה מותאמת.','work-empty'));
 if(state.guidance_links?.length){const links=el('section','','guidance-links');links.append(el('h3','מדריכים ומתכונים להמחשה'));for(const item of state.guidance_links){if(!item.url.startsWith('https://'))continue;const link=el('a',item.title);link.href=item.url;link.target='_blank';link.rel='noopener noreferrer';links.append(link);}guidanceDock.append(links);}
 if(active){
   const addForm=el('form','','add-user-step');addForm.id='add-user-step';const input=el('input');input.id='new-step-title';input.maxLength=160;input.required=true;input.placeholder='פעולה שלי — למשל: לתבל את הכנפיים';input.setAttribute('aria-label','פעולה חדשה לבחירתך');const add=el('button','+ הוסף פעולה');add.type='submit';addForm.append(input,add);addForm.addEventListener('submit',event=>{event.preventDefault();if(input.value.trim()){const sent=input.value.trim();void coachCommand('add_step',{step_title:sent}).then(()=>{const field=$('new-step-title');if(field&&!coachNotice.textContent&&field.value===sent)field.value='';});}});journey.append(addForm);
   const reportForm=el('form','','user-report-form');reportForm.id='user-report-form';const text=el('textarea');text.id='work-report';text.rows=2;text.maxLength=2000;text.required=true;text.placeholder='מה עשית ומה המצב?';text.setAttribute('aria-label','דיווח מהמטבח');const submit=el('button','דווח לשף');submit.type='submit';const reportStatus=el('p');reportStatus.id='work-report-status';reportStatus.setAttribute('role','status');reportForm.append(el('h3','דיווח מהמטבח'),text,reportStatus,submit);reportForm.addEventListener('invalid',()=>{reportStatus.textContent='יש להזין או להקליט טקסט לפני שליחה.';},true);reportForm.addEventListener('submit',event=>{event.preventDefault();if(text.value.trim()){const sent=text.value.trim();document.dispatchEvent(new Event('coach-stop-dictation'));reportStatus.textContent='שולח את הדיווח…';void (mentor.inputMode==='ask'?coachCommand('ask',{message:sent}):reportWork(sent)).then(result=>{const field=$('work-report'),status=$('work-report-status');if(result){if(field&&field.value.trim()===sent)field.value='';if(status){status.textContent=mentor.inputMode==='ask'?'\u05d4\u05e9\u05d0\u05dc\u05d4 \u05d4\u05ea\u05e7\u05d1\u05dc\u05d4.':'\u05d4\u05d3\u05d9\u05d5\u05d5\u05d7 \u05d4\u05ea\u05e7\u05d1\u05dc \u05d0\u05e6\u05dc \u05d4\u05e9\u05e3.';status.className='';}}else if(status){status.textContent=coachNotice.textContent||'הדיווח לא נשלח. הטקסט נשמר; נסה שוב.';status.className='error';}});}});journey.append(reportForm);
   reportForm.insertBefore(actionButton('work-report-dictate','🎙 הקלד דיווח בקול',()=>document.dispatchEvent(new CustomEvent('coach-dictate',{detail:{target:'work-report'}}))),submit);
   const quickReports=el('div','','quick-reports');for(const text of ['המנה נראית טוב','בדוק את ההתקדמות שלי'])quickReports.append(actionButton('report-'+text.replaceAll(' ','-'),text,()=>reportWork(text)));journey.append(quickReports);
   if(context?.minimum_temperature!==null&&context?.minimum_temperature!==undefined){const measurement=el('div','','measurement-report');const temperature=el('input');temperature.id='work-temperature';temperature.type='number';temperature.step='0.1';temperature.min=-50;temperature.max=300;temperature.placeholder='°C בחלקים העבים';temperature.setAttribute('aria-label','מדידה אמיתית בחלקים העבים');const record=actionButton('work-temperature-submit','דווח מדידה',()=>{if(temperature.value&&Number.isFinite(Number(temperature.value)))void coachCommand('report',{temperature:Number(temperature.value)});else coachNotice.textContent='יש להזין מדידה אמיתית.';});measurement.append(temperature,record);journey.append(measurement);}
 }
 if(state.status!=='completed'){
   const timer=el('output','00:00','coach-clock');timer.id='coach-clock';timer.setAttribute('aria-label','זמן עד התזכורת שבחרת');journey.append(timer);
   const timerRow=el('div','','row');const seconds=el('input');seconds.type='number';seconds.min=1;seconds.max=14400;seconds.value=300;seconds.setAttribute('aria-label','שניות לתזכורת');timerRow.append(seconds,actionButton('user-timer-start','תזכורת לבחירתי',()=>{const value=Number(seconds.value);if(Number.isInteger(value)&&value>=1&&value<=14400)void coachCommand('timer',{seconds:value});}),actionButton('user-pause',state.status==='paused'?'חזרה לליווי':'השהה ליווי',()=>coachCommand(state.status==='paused'?'resume':'pause')));journey.append(timerRow);
   if(state.safety_hold){const checkbox=el('input');checkbox.type='checkbox';checkbox.id='coach-hazard-resolved';const label=el('label');label.append(checkbox,document.createTextNode('טיפלתי בסיכון והמצב מאפשר לחזור לבישול'));journey.append(label);}
 }
 for(const message of state.messages){conversation.append(el('p',message.text,message.role==='user'?'chat-bubble user-bubble':'chat-bubble chef-bubble'));}
 actions.hidden=false;doneButton.hidden=!active||!current;problemButton.hidden=!active;doneButton.textContent='✓ סיימתי את הפעולה';chatForm.hidden=!active;
 statusQuestion.replaceChildren();statusQuestion.classList.toggle('attention',state.issues.length>0||state.safety_hold);if(state.safety_hold)statusQuestion.append(el('p','נרשם סיכון; הליווי מושהה עד טיפול ודיווח.'));
 if(active&&(mentor.problemOpen||state.problem_rule_status==='choose')){const choices=el('section','','problem-chooser');choices.id='problem-chooser';choices.append(el('h3','מה הבעיה?'));for(const problem of state.problem_options||[]){const button=actionButton('problem-'+problem.id,problem.label+(problem.rule_available?'':' — חסר חוק'),()=>coachCommand('problem',{problem_id:problem.id,message:problem.id==='other'?chatInput.value.trim():''}));choices.append(button);}statusQuestion.append(choices);}
 if(state.problem_rule_status==='missing'){const alert=el('p','חסר חוק מתאים. הבעיה נשמרה להשלמה.','missing-rule-alert');alert.setAttribute('role','alert');statusQuestion.append(alert,actionButton('edit-missing-rule','פתח כללי טיפול בבעיות',()=>{show('knowledge');document.dispatchEvent(new Event('chef-open-problem-rules'));}));}
 const concreteQuestions=state.station_protocol?.blocks?.length?[]:(state.decision_questions||[]).filter(question=>question.id!=='progress');
 if(active&&concreteQuestions.length){statusQuestion.append(el('h3','כדי להתאים לך את ההמשך'));for(const question of concreteQuestions){const group=el('fieldset','','decision-question');group.dataset.questionId=question.id;group.append(el('legend',question.text));for(const option of question.options){const button=actionButton('choice-'+question.id+'-'+option.id,option.label,()=>void coachCommand('answer',{question_id:question.id,answer:option.id}));button.dataset.choiceNumber=option.number;group.append(button);}statusQuestion.append(group);}}
 else if(active&&!state.decision_questions){statusQuestion.append(actionButton('load-decisions','טען אפשרויות בחירה',()=>coachCommand('check_in')));}
 else if(active&&!current&&state.decision_questions?.length){statusQuestion.append(el('p','בחר מסלול הכנה כדי לקבל את הפעולה הראשונה.'));}
 if(active&&!steps.length&&!state.decision_questions?.some(question=>question.id.startsWith('salmon_'))){
   const chosenMethod=(state.method_recommendations?.allowed||[]).find(method=>method.label===state.method||method.id===state.method)?.id;
   const paths=(context?.graph?.paths||[]).filter(path=>path.selectable&&(!chosenMethod||path.method_ref===chosenMethod)&&(state.method_recommendations?.allowed||[]).some(method=>method.id===path.method_ref));
   if(paths.length){const choices=el('section','','cooking-path-choices');choices.id='cooking-path-choices';choices.append(el('h3','איך תרצה להכין?'));for(const path of paths)choices.append(actionButton('start-path-'+path.id,'התחל · '+path.title,()=>coachCommand('adopt_path',{graph_path_id:path.id})));statusQuestion.append(choices);}
 }
 if(active&&current&&!state.safety_hold){
   const choices=el('section','','cooking-step-choices');choices.id='cooking-step-choices';
   const remaining=steps.some(entry=>!state.completed_step_ids.includes(entry.id));
   if(remaining)choices.append(actionButton('step-continue','אישור ביצוע',()=>coachCommand('complete')),
     actionButton('step-explain','הסבר ביצוע',()=>coachCommand('ask',{message:'איך לבצע את הפעולה הנוכחית?'})),
     actionButton('step-wait','בדיקת מוכנות',()=>coachCommand('ask',{message:'מה לבדוק לפני שממשיכים?'})));
   else choices.append(actionButton('step-season','בדיקת תיבול והגשה',()=>coachCommand('ask',{message:'איך לתבל ולהגיש?'})));
   statusQuestion.append(choices);
 }
 const visibleTips=inlineTips;
 const otherTips=(context?.tips||[]).filter(tip=>!visibleTips.includes(tip)&&tip.text?.trim());if(otherTips.length){const more=el('details');more.append(el('summary','טיפים למנה'));for(const tip of otherTips)appendContextTip(more,tip);if(more.children.length>1)learning.append(more);}
 if(active&&context?.suggestions?.length){const suggestions=el('details','','suggested-actions');suggestions.id='suggested-actions';suggestions.append(el('summary','פעולות אפשריות — להוספה רק אם תרצה'));for(const [index,title] of (context?.suggestions||[]).entries())suggestions.append(actionButton('suggestion-'+index,'+ '+title,()=>coachCommand('add_step',{step_title:title})));learning.append(suggestions);}
 if(state.completion_summary.length){const summary=el('section','','work-debrief');summary.id='work-debrief';summary.append(el('h3','סיכום לפי הדיווחים שלך'));for(const text of state.completion_summary)summary.append(el('p',text));journey.append(summary);}
 renderGraphAdvice(state);
 if(typeof renderCookingSupport==='function')renderCookingSupport(state);
 paintClock();
 if($('work-report'))$('work-report').value=drafts.report||'';
 if($('new-step-title'))$('new-step-title').value=drafts.step||'';
 if($('work-temperature'))$('work-temperature').value=drafts.temperature||'';
}
const originalRenderCoach=renderCoach;
function renderGuidedGuidance(){const box=journey.querySelector('.current-step'),step=currentSmartStep();if(!box||!step)return;const body=el('div','','step-action-body');while(box.firstChild)body.append(box.firstChild);const guide=el('aside','','active-work-guidance');guide.id='active-work-guidance';guide.append(el('h3','הנחיות לפעולה הנוכחית'),compactConversation,el('p',step.why));for(const line of [...step.successCriteria,...step.commonMistakes])guide.append(el('p',line));box.classList.add('step-with-guidance');box.append(body,guide);}
renderCoach=function(){const custom=mentor.state?.workflow==='user';workDraftState=custom&&renderedWorkId===mentor.state.id?{id:mentor.state.id,report:$('work-report')?.value||'',step:$('new-step-title')?.value||'',temperature:$('work-temperature')?.value||''}:{};userToolbar.hidden=!custom;updateDish.hidden=!custom||mentor.state.status!=='active';compactConversation.hidden=false;topicDetails.hidden=!mentor.state;originalRenderCoach();if(!custom){topicDetails.insertAdjacentElement('beforebegin',compactConversation);const latest=mentor.state?.messages.filter(message=>message.role==='chef').at(-1);compactConversation.replaceChildren(el('p',latest?.text||'מה תרצה להכין? אתה בוחר את המנה והפעולות; אני כאן לייעץ.','chat-bubble chef-bubble'));renderGuidedGuidance();}};
renderCoach();

function renderGraphAdvice(state){
 const graph=state.context?.graph;if(!graph)return;
 const inherited=graph.ingredients.filter(node=>node.inherited_advice);if(inherited.length){const box=el('details');box.append(el('summary','יסודות לפי משפחת חומר הגלם'));for(const node of inherited)box.append(el('h3',node.name),el('p',node.inherited_advice),el('p',node.inherited_warning),el('small','מעץ הידע הנוסף · בניסוח מותאם'));learning.append(box);}
 if(state.status==='active'&&graph.method){const box=el('details');box.append(el('summary','דיווח מהיר לפי שיטת ההכנה'));for(const rule of graph.method.observations)box.append(actionButton('graph-report-'+rule.id,rule.label,()=>coachCommand('report',{observation:rule.id})));journey.append(box);}
 if(graph.paths.length){const box=el('details');box.append(el('summary','מתווים מתאימים מעץ הידע — לבחירתך'));for(const path of graph.paths){const card=el('article');card.append(el('h3',path.title));if(path.selectable&&state.status==='active')card.append(actionButton('graph-path-'+path.id,'הוסף מתווה לתוכנית שלי',()=>coachCommand('adopt_path',{graph_path_id:path.id})));else card.append(el('small',path.reason||'העבודה הסתיימה'));box.append(card);}learning.append(box);}
 if(graph.preparations.length){const box=el('details');box.append(el('summary','הכנות מקדימות אפשריות'));for(const prep of graph.preparations)box.append(el('h3',prep.name),el('p',prep.advice));learning.append(box);}
 if(state.status==='active'&&state.context.minimum_rest_seconds){const button=actionButton('report-rest','דווח זמן מנוחה',()=>{const value=prompt('כמה שניות מנוחה לאחר הבישול מדדת?');if(value!==null&&value.trim()&&Number.isInteger(Number(value))&&Number(value)>=0&&Number(value)<=3600)void coachCommand('report',{rest_seconds:Number(value)});});journey.append(button);}
}
publicApi('/v1/coach/graph/catalog').then(catalog=>{
 graphIngredientCatalog=catalog.ingredients;
 const box=el('details'),search=el('input'),choices=el('div','','ingredient-palette');box.append(el('summary','חומרי גלם נוספים מעץ הידע'),search,choices);search.placeholder='חיפוש חומר גלם';search.setAttribute('aria-label','חיפוש בעץ חומרי הגלם');choices.style.maxHeight='18rem';choices.style.overflowY='auto';palette.insertAdjacentElement('afterend',box);
 function draw(){choices.replaceChildren();for(const node of catalog.ingredients.filter(item=>item.aliases.some(alias=>alias.toLowerCase().includes(search.value.trim().toLowerCase())))){const item=inventory().find(item=>node.aliases.some(alias=>alias.toLowerCase()===item.name.trim().toLowerCase()));const icon=node.food_class==='meat'?'🥩':node.food_class==='dairy'?'🥛':node.allergens.includes('fish')?'🐟':'🥣';choices.append(actionButton('ingredient-'+node.id,`${icon} ${node.name} · ${item?.quantity||0}`,()=>{const row=[...$('inventory').children].find(row=>node.aliases.some(alias=>alias.toLowerCase()===row.querySelector('[data-field="name"]').value.trim().toLowerCase()));if(row){const quantity=row.querySelector('[data-field="quantity"]');quantity.value=String((Number(quantity.value)||0)+1);}else addInventory({name:node.name,quantity:1,unit:'יח׳'});saveInventory();paintInventory();draw();}));}}
 search.addEventListener('input',draw);box.addEventListener('toggle',()=>{if(box.open)draw();});draw();
}).catch(()=>{});
