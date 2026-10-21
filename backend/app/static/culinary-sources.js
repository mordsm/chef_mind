'use strict';
(() => {
 const host=document.getElementById('culinary-sources');
 const copy={
  en:['Culinary YAML sources','Private source drafts. Saving does not change live coaching; new advice needs editorial review.','Source','Load / reload','YAML document','Save draft','Add an entry','Section','Entry ID (leave empty for recipe paths)','Entry YAML','Add entry','Saved source draft. Live coaching is unchanged.','Unsaved edits will be replaced. Continue?','Revision'],
  he:['מקורות הידע ב־YAML','טיוטות מקור פרטיות. שמירה אינה משנה את ההדרכה הפעילה; הנחיות חדשות דורשות סקירה ועריכה.','מקור','טעינה / רענון','מסמך YAML','שמירת טיוטה','הוספת רשומה','מקטע','מזהה רשומה (ריק למתווה מתכון)','רשומה ב־YAML','הוספת רשומה','טיוטת המקור נשמרה. ההדרכה הפעילה לא השתנתה.','שינויים שלא נשמרו יוחלפו. להמשיך?','גרסה']
 };
 let loaded=null, epoch=authEpoch, dirty=false, editable=false, request=0;
 const tr=i=>copy[language][i];
 function label(text,node){const wrap=el('label');wrap.append(el('span',text),node);return wrap;}
 const heading=el('h3'),help=el('p'),status=el('p'),difference=el('p');status.setAttribute('role','status');status.id='culinary-source-status';
 const select=el('select');select.id='culinary-source-select';for(const key of ['graph','domain']){const option=el('option',key);option.value=key;select.append(option);}
 const load=el('button');load.type='button';
 const text=el('textarea');text.id='culinary-source-yaml';text.rows=20;text.dir='ltr';text.spellcheck=false;
 const save=el('button');save.type='button';save.hidden=true;
 const entryTitle=el('h4'),section=el('select'),id=el('input'),entry=el('textarea');entry.rows=6;entry.dir='ltr';entry.spellcheck=false;id.dir='ltr';
 const add=el('button');add.type='button';
 const controls=el('div');controls.hidden=true;
 const sourceLabel=label('',select),textLabel=label('',text),sectionLabel=label('',section),idLabel=label('',id),entryLabel=label('',entry);
 controls.append(entryTitle,sectionLabel,idLabel,entryLabel,add);
 host.append(heading,help,difference,sourceLabel,load,textLabel,status,save,controls);
 function localizeEditor(){heading.textContent=tr(0);help.textContent=tr(1);sourceLabel.firstChild.textContent=tr(2);load.textContent=tr(3);textLabel.firstChild.textContent=tr(4);save.textContent=tr(5);entryTitle.textContent=tr(6);sectionLabel.firstChild.textContent=tr(7);idLabel.firstChild.textContent=tr(8);entryLabel.firstChild.textContent=tr(9);add.textContent=tr(10);}
 function permissions(){text.readOnly=!editable;save.hidden=!editable;controls.hidden=!editable;}
 function clear(){request++;loaded=null;editable=false;text.value='';entry.value='';id.value='';status.textContent='';status.className='';section.replaceChildren();dirty=false;epoch=authEpoch;permissions();}
 function showSource(result,privateCopy=true){loaded=result;text.value=result.yaml_text;dirty=false;editable=privateCopy&&role==='reviewer';section.replaceChildren();for(const key of Object.keys(result.sections)){const option=el('option',key);option.value=key;section.append(option);}status.className='';status.textContent=tr(13)+' '+result.revision+' · '+(privateCopy?(language==='he'?'הטיוטה הפרטית שלך':'Your private draft'):(language==='he'?'המקור המקורי. לשמירת שינויים יש להתחבר עם הרשאת סקירה.':'Original source. Sign in with review permission to save edits.'));permissions();}
 async function loadSource(ask=true){if(ask&&dirty&&!confirm(tr(12)))return;const ticket=++request,key=select.value,auth=authEpoch;editable=false;permissions();load.disabled=true;status.className='';status.textContent=language==='he'?'טוען את המקור…':'Loading source…';try{let result,privateCopy=!!identityUser,failed=false;if(privateCopy){try{result=await api('/v1/culinary/sources/'+key);}catch{failed=true;privateCopy=false;}}if(!result)result=await publicApi('/v1/culinary/templates/'+key);if(ticket!==request||auth!==authEpoch)return;showSource(result,privateCopy);if(failed){status.className='error';status.textContent=language==='he'?'לא ניתן לטעון טיוטה פרטית. מוצג המקור המקורי והשמירה חסומה. בדוק את מסד הנתונים והתחבר מחדש.':'Private draft unavailable. Showing the original; saving is disabled. Check the database and sign in again.';}}catch(error){if(ticket===request){text.value='';status.className='error';status.textContent=t(error.message);}}finally{if(ticket===request)load.disabled=false;}}
 async function run(button,action){button.disabled=true;try{await action();}catch(error){status.textContent=t(error.message);status.className='error';}finally{button.disabled=false;}}
 text.addEventListener('input',()=>dirty=true);
 load.addEventListener('click',()=>void loadSource());
 select.addEventListener('change',()=>{if(dirty&&!confirm(tr(12))){select.value=loaded.source_key;return;}dirty=false;void loadSource(false);});
 save.addEventListener('click',()=>run(save,async()=>{if(!loaded||loaded.source_key!==select.value)throw new Error('sourceLoadFirst');const result=await api('/v1/culinary/sources/'+loaded.source_key,'PUT',{expected_revision:loaded.revision,yaml_text:text.value});showSource(result);status.textContent=tr(11);}));
 add.addEventListener('click',()=>run(add,async()=>{if(!loaded||loaded.source_key!==select.value)throw new Error('sourceLoadFirst');if(dirty)throw new Error('sourceSaveFirst');const result=await api('/v1/culinary/sources/'+loaded.source_key+'/entries','POST',{expected_revision:loaded.revision,section:section.value,entry_id:id.value.trim()||null,yaml_text:entry.value});showSource(result);entry.value='';id.value='';status.textContent=tr(11);}));
 document.addEventListener('chef-auth-changed',()=>{clear();void loadSource(false);});
 function explain(){help.textContent=language==='he'?'שני מקורות משלימים. השף כבר משתמש בהתאמות שנבדקו מתוך שניהם. שינויים חדשים נשמרים כטיוטות ודורשים סקירה לפני שילוב בהדרכה.':'The coach already uses reviewed adaptations of both sources. New edits remain drafts until reviewed.';difference.textContent=language==='he'?'graph מקשר רכיבים להכנות, שיטות בישול ומתווים. domain מוסיף משפחות רכיבים, ירושה ושלבי עבודה מפורטים.':'graph links ingredients, preparations, methods and paths. domain adds ingredient families, inheritance and detailed steps.';select.options[0].textContent=language==='he'?'רכיבים, הכנות ושיטות (graph)':'Ingredients, preparations and methods (graph)';select.options[1].textContent=language==='he'?'משפחות רכיבים ושלבים מפורטים (domain)':'Ingredient families and detailed steps (domain)';}
 new MutationObserver(()=>{localizeEditor();explain();}).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
 localizeEditor();explain();permissions();void loadSource(false);
})();
