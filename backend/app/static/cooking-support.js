'use strict';
// IDs and responses come from the server's finite operation catalog.
const supportDrafts=new Map();
let operationSearch='',operationGroup='',operationOpen=false;
const intakeLabels={family:'משפחת המנה',protein:'סוג הבשר',cut:'נתח, גודל וחיתוך',quantity:'כמות ויחידות',goal:'התוצאה הרצויה',equipment:'כלי הבישול',method:'שיטת ההכנה',recipe_url:'קישור למתכון',recipe_text:'המתכון או תיאור מנה דומה'};
const intakeChoices={family:{meat:'בשר ועוף',fish:'דגים',vegetables:'ירקות',starch:'אורז, פסטה ודגנים',legumes:'קטניות',eggs:'ביצים',soup:'מרקים ותבשילים',other:'אחר'},protein:{chicken:'עוף',turkey:'הודו',beef:'בקר',other:'אחר'},goal:{sauce:'תבשיל ברוטב',brown:'השחמה',soft:'רך',crisp:'פריך',other:'אחר'},equipment:{pot:'סיר רגיל',pan:'מחבת',oven:'תנור',steamer:'אידוי',pressure:'סיר לחץ',other:'אחר'}};
quickStarts.append(actionButton('start-by-family','עוד אין מנה — נבחר לפי משפחה',()=>coachCommand('start_custom',{dish_title:'מנה לבחירה',method:'',ingredients:[],mode:roleMode.value}),'secondary'));

function renderCookingSupport(state){
 let logLink=$('open-action-log');if(!logLink){logLink=el('a','דיווח פעולות בזמן אמת');logLink.id='open-action-log';logLink.target='_blank';logLink.rel='noopener';userToolbar.append(logLink);}logLink.href='/report/?'+new URLSearchParams({cooking_id:state.id,recipe_id:state.recipe_id});
 const info=state.intake_guidance;if(!info)return;
 const active=state.status==='active';
 if(active){let reporter=$('inline-action-reporter');if(!reporter){reporter=el('section','','inline-action-reporter');reporter.id='inline-action-reporter';reporter.append(el('h3','מה עשית עכשיו?'),el('p','בחר פעולה. למשל, לחיצה על בישול תפתח בחירת חום, זמן וכלי.'));companionHeading.insertAdjacentElement('afterend',reporter);}reporter.hidden=false;let frame=window.chefReportFrame;if(!frame||frame.dataset.cookingId!==state.id){if(frame)frame.remove();frame=el('iframe');frame.id='action-report-frame';frame.title='דיווח פעולות בישול';frame.src='/report/?'+new URLSearchParams({cooking_id:state.id,recipe_id:state.recipe_id,server_link:identityUser?'1':'0'});frame.dataset.cookingId=state.id;frame.height='600';window.chefReportFrame=frame;reporter.append(frame);}}
 const section=el('section','','cooking-intake');section.id='cooking-intake';section.append(el('h3','פרטי המנה וההכנה'),el('p',info.family_label));
 if(info.defaults?.temperature){
   const d=info.defaults,recommendation=el('section','','cooking-defaults');
   const values=[`חום: ${d.temperature}°C`];if(d.program)values.push(`תוכנית: ${d.program}`);if(d.minutes)values.push(`זמן משוער: ${d.minutes} דק׳`);
   recommendation.append(el('strong',values.join(' | ')));if(d.equipment)recommendation.append(el('p',d.equipment));if(d.assumption)recommendation.append(el('small',d.assumption));
   for(const check of d.checkpoints||[])recommendation.append(el('p',check));
   if(d.source)recommendation.append(el('small',d.source));
   if(d.minutes)recommendation.append(actionButton('start-default-timer','הפעל תזכורת',()=>coachCommand('timer',{seconds:d.minutes*60})));
   const edit=el('details');edit.append(el('summary','עריכת ההמלצה'));const form=el('form'),fields={};
   for(const [key,label,value,min,max] of [['oven_temperature','חום התנור',d.temperature,100,250],['estimated_minutes','זמן משוער בדקות',d.minutes||'',1,240]]){const input=el('input');input.type='number';input.min=min;input.max=max;input.value=value;input.required=key==='oven_temperature';input.setAttribute('aria-label',label);const wrapper=el('label',label);wrapper.append(input);form.append(wrapper);fields[key]=input;}
   const program=el('select');program.setAttribute('aria-label','תוכנית תנור');const unset=el('option','לא צוינה במקור');unset.value='';program.append(unset);for(const name of ['טורבו','חום עליון ותחתון']){const option=el('option',name);option.value=name;program.append(option);}program.value=d.program||'';form.append(program);
   const save=el('button','שמור המלצה');save.type='submit';form.append(save);form.addEventListener('submit',event=>{event.preventDefault();const facts={...state.intake_facts,oven_temperature:Number(fields.oven_temperature.value),defaults_edited:['temperature']};if(fields.estimated_minutes.value){facts.estimated_minutes=Number(fields.estimated_minutes.value);facts.defaults_edited.push('minutes');}if(program.value){facts.oven_program=program.value;facts.defaults_edited.push('program');}void coachCommand('intake',{intake_facts:facts});});edit.append(form);recommendation.append(edit);section.append(recommendation);
 }
 if(state.dish_identity?.status==='recognized')section.append(el('p','זיהוי המנה נשמר בתחילת ההכנה. אפשר לתקן את הפרטים בבחירות למטה.','dish-recognized'));
 const external=el('details');external.append(el('summary','חיפוש מתכון נוסף באינטרנט'));
 for(const item of info.recipe_search_links||[]){const link=el('a',item.label);link.href=item.url;link.target='_blank';link.rel='noopener noreferrer';external.append(link,el('br'));}section.append(external);
 if(!info.recipe_search_links?.length&&info.recipe_search_url?.startsWith('https://www.bbcgoodfood.com/search?')){const link=el('a','חפש מתכון דומה ב־Good Food (אנגלית)');link.href=info.recipe_search_url;link.target='_blank';link.rel='noopener noreferrer';section.append(link);}
 if(info.missing.length)section.append(el('p',info.missing[0].label));
 if(active){
   const form=el('form','','intake-form');form.id='cooking-intake-form';
   const draft=supportDrafts.get(state.id)||{...state.intake_facts};const controls={};
   function add(key,choices){
     const label=el('label',intakeLabels[key]);label.htmlFor='intake-'+key;
     const control=choices?el('select'):key==='recipe_text'?el('textarea'):el('input');control.id='intake-'+key;
     if(choices){const blank=el('option','בחר');blank.value='';control.append(blank);for(const [value,title]of Object.entries(choices)){const option=el('option',title);option.value=value;control.append(option);}}
     else{control.maxLength=key==='recipe_text'?10000:key==='recipe_url'?2000:160;if(key==='recipe_url')control.type='url';if(key==='quantity')control.placeholder='למשל: 500 גרם או 2 כוסות יבשות';if(key==='cut')control.placeholder=`${state.dish_title}: סוג הנתח ועובי בס״מ`;}
     const current=draft[key]||((key==='family')?info.family:'');if(choices&&current&&![...control.options].some(option=>option.value===current)){const existing=el('option',current+' (נשמר קודם)');existing.value=current;control.append(existing);}control.value=current;controls[key]=control;control.addEventListener('input',()=>{draft[key]=control.value;supportDrafts.set(state.id,draft);});
     form.append(label,control);return control;
   }
   const family=add('family',intakeChoices.family),protein=add('protein',intakeChoices.protein);
   function showProtein(){protein.hidden=family.value!=='meat';form.querySelector('label[for="intake-protein"]').hidden=protein.hidden;if(protein.hidden){protein.value='';draft.protein='';}}
   family.addEventListener('change',showProtein);showProtein();
   if(info.main_ingredient_needed){intakeLabels.main_ingredient='מה המרכיב העיקרי? (רק כשהמנה לא זוהתה)';add('main_ingredient',{'עוף':'עוף','חזה עוף':'חזה עוף','כרעיים':'כרעיים','בקר':'בקר','סלמון':'סלמון','גזר':'גזר','תפוח אדמה':'תפוח אדמה','אורז':'אורז','עדשים':'עדשים'});form.append(el('small','הבחירה עוזרת להתאים את ההכוונה כששם המנה אינו מציין את המרכיב. אין צורך להזין רשימת קניות.'));}
   add('cut');add('quantity',{'250 גרם':'250 גרם','500 גרם':'500 גרם','750 גרם':'750 גרם','1 ק״ג':'1 ק״ג','2 ק״ג':'2 ק״ג','1 כוס':'1 כוס','2 כוסות':'2 כוסות','4 יחידות':'4 יחידות'});
   add('goal',info.goal_choices||intakeChoices.goal);add('equipment',{...intakeChoices.equipment,grill:'גריל'});
   const methods=Object.fromEntries((state.method_recommendations?.allowed||[]).map(item=>[item.id,item.label]));
   const method=add('method',methods);if(!draft.method){const option=[...method.options].find(option=>option.textContent===state.method||option.value===state.method);method.value=option?.value||'';}
   add('recipe_url');const recipe=add('recipe_text');recipe.rows=4;recipe.placeholder='הדבק רשימת מרכיבים, כמויות, סדר פעולות וסימני בדיקה, או תאר למה המנה דומה.';
   const source=el('details');source.id='intake-source';source.append(el('summary','שמירת מתכון לעיון בלבד'),el('p','קישור נשמר כקיצור דרך לפתיחה. טקסט נשמר כפי שנכתב. אין כאן קריאה אוטומטית של האתר או פענוח טקסט לשלבי בישול; הבחירות המובנות למעלה הן שמשנות את ההכוונה.'));
   for(const key of ['recipe_url','recipe_text'])source.append(form.querySelector('label[for="intake-'+key+'"]'),controls[key]);form.append(source);
   const save=el('button','שמור פרטים וקבל הכוונה');save.type='submit';form.append(save);
   form.addEventListener('submit',event=>{event.preventDefault();const facts={...state.intake_facts,...Object.fromEntries(Object.entries(controls).map(([key,control])=>[key,control.value.trim()]))};supportDrafts.set(state.id,facts);save.disabled=true;save.textContent='מעדכן את ההכוונה…';void coachCommand('intake',{intake_facts:facts}).then(result=>{if(result){supportDrafts.delete(state.id);renderCoach();const saved=el('p','הפרטים נשמרו. ההנחיה עודכנה בצד.','intake-save-status');saved.id='intake-save-result';saved.setAttribute('role','status');$('cooking-intake')?.prepend(saved);}else{save.disabled=false;save.textContent='שמור פרטים וקבל הכוונה';}});});
   const next=info.missing[0];if(next&&Object.keys(next.choices).length&&controls[next.key]){const interview=el('fieldset','','intake-interview');interview.append(el('legend',next.label));for(const [key,title]of Object.entries(next.choices)){interview.append(actionButton('intake-choice-'+next.key+'-'+key,title,()=>{controls[next.key].value=key;controls[next.key].dispatchEvent(new Event('change'));form.requestSubmit();}));}section.append(interview);}
   section.append(form);
 }
 journey.prepend(section);const questions=$('status-question')||statusQuestion;for(const group of [...questions.querySelectorAll('.decision-question')])section.append(group);
 if(!active)return;
 const box=el('details','','operation-picker');box.id='operation-picker';box.open=operationOpen;box.addEventListener('toggle',()=>{operationOpen=box.open;});box.append(el('summary','בחר פעולה ודווח מה קרה — ללא פענוח טקסט'));
 box.append(el('p','בחר פעולה, קבל הוראות וסמן את המצב שמצאת. המאגר מציג את הפעולות הנתמכות כרגע.'));
 const search=el('input');search.type='search';search.id='operation-search';search.placeholder='חפש פעולה, למשל חיתוך או רתיחה';search.setAttribute('aria-label','חיפוש במאגר הפעולות');search.value=operationSearch;
 const group=el('select');group.id='operation-group';group.setAttribute('aria-label','קבוצת פעולות');for(const value of ['',...new Set((state.operation_catalog||[]).map(item=>item.group))]){const option=el('option',value||'כל הקבוצות');option.value=value;group.append(option);}group.value=operationGroup;
 const items=el('div','','operation-options');
 function draw(){items.replaceChildren();const visible=(state.operation_catalog||[]).filter(item=>(!group.value||item.group===group.value)&&(!search.value.trim()||(item.label+' '+item.instruction).includes(search.value.trim())));for(const item of visible){const card=el('article');const button=actionButton('operation-'+item.id,item.label,()=>coachCommand('select_operation',{operation_id:item.id}));button.disabled=!item.available;if(item.id===state.selected_operation_id)button.setAttribute('aria-pressed','true');card.append(button);if(item.reason)card.append(el('small',item.reason));items.append(card);}if(!visible.length)items.append(el('p','לא נמצאה פעולה נתמכת. אפשר לתאר אותה בדיווח כדי לזהות איזה כלל חסר.'));}
 search.addEventListener('input',()=>{operationSearch=search.value;draw();});group.addEventListener('change',()=>{operationGroup=group.value;draw();});box.append(search,group,items);draw();
 const selected=(state.operation_catalog||[]).find(item=>item.id===state.selected_operation_id);
 if(selected){const panel=el('section','','selected-operation');panel.id='selected-operation';panel.append(el('h3',selected.label),el('p',selected.instruction));const checks=el('ul');for(const check of selected.checks)checks.append(el('li',check));panel.append(checks,el('h4','מה מצאת?'));for(const outcome of selected.outcomes){const button=actionButton('outcome-'+selected.id+'-'+outcome.id,outcome.label,()=>coachCommand('report_operation',{operation_id:selected.id,outcome_id:outcome.id}));button.disabled=!selected.available;panel.append(button);}if(!selected.available)panel.append(el('p',selected.reason));const latest=(state.operation_events||[]).at(-1);if(latest?.operation_id===selected.id){const reply=el('p',latest.reply,'operation-reply');reply.setAttribute('role','status');panel.append(reply);}box.append(panel);box.open=true;}
 const missing=el('details');missing.append(el('summary','חסרה פעולה במאגר?'));
 const request=el('form');const name=el('input');name.required=true;name.maxLength=160;name.setAttribute('aria-label','שם הפעולה החסרה');name.placeholder='איזו פעולה חסרה?';
 const detail=el('input');detail.maxLength=2000;detail.setAttribute('aria-label','פרטי הפעולה החסרה');detail.placeholder='חומר גלם, כלי, תוצאה רצויה ומקור אם יש';
 const send=el('button','רשום מה חסר');send.type='submit';request.append(name,detail,send);request.addEventListener('submit',event=>{event.preventDefault();void coachCommand('request_operation',{step_title:name.value.trim(),message:detail.value.trim()});});missing.append(request);
 if(state.operation_gaps?.length){const list=el('ul');for(const item of state.operation_gaps)list.append(el('li',item.title+' — ממתין להוספת הוראות ובדיקות'));missing.append(list);}box.append(missing);
 journey.append(box);
}
window.addEventListener('message',event=>{const frame=window.chefReportFrame;if(event.origin!==location.origin||!frame||event.source!==frame.contentWindow)return;if(event.data?.type==='chef-report-ready'&&identityUser&&token)frame.contentWindow.postMessage({type:'chef-report-auth',token},location.origin);if(event.data?.type==='chef-report-height'&&Number.isFinite(event.data.height))frame.height=String(Math.min(6000,Math.max(400,event.data.height)));});
document.addEventListener('chef-auth-changed',()=>{const frame=window.chefReportFrame;if(frame)frame.contentWindow.postMessage(identityUser&&token?{type:'chef-report-auth',token}:{type:'chef-report-logout'},location.origin);});
const renderBeforeReportPanel=renderCoach;renderCoach=function(){renderBeforeReportPanel();const reporter=$('inline-action-reporter');if(reporter)reporter.hidden=mentor.state?.workflow!=='user'||mentor.state.status!=='active';};
renderCoach();
