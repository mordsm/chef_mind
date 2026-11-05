'use strict';
// A user reviews the source snapshot before adopting its instructions.
(() => {
 function recipeContext(){const state=mentor.state,recipe=state?.recipe_snapshot;const current=selectedStep();return {type:'chef-recipe-context',recipe:recipe||null,defaults:recipe?null:state?.intake_guidance?.defaults||null,step_id:current?.id||'',legacy_timer:state&&(state.timer_deadline||state.paused_remaining!==null)?{deadline:state.timer_deadline,paused:state.status==='paused',remaining:state.paused_remaining}:null};}
 function sendContext(){const frame=window.chefReportFrame;if(frame)frame.contentWindow.postMessage(recipeContext(),location.origin);}
 function renderRecipeImport(){
   const state=mentor.state,source=$('intake-source');if(!source||!state)return;
   source.querySelector('summary').textContent='צרף מתכון שבחרתי';
   const explanation=source.querySelector('p');if(explanation)explanation.textContent='בחרת מתכון באתר אחר? העתק את הקישור לכאן ולחץ על קליטה. אם לא ניתן לקרוא את האתר, הדבק רק את הוראות ההכנה — שלב בכל שורה. לאחר תצוגה מקדימה אפשר להוסיף את השלבים לתוכנית.';
   const text=$('intake-recipe_text');if(text)text.placeholder='הוראות הכנה בלבד, שלב בכל שורה. שלבי המתכון לא יסומנו אוטומטית כבוצעו.';
   const textLabel=source.querySelector('label[for="intake-recipe_text"]');if(textLabel)textLabel.textContent='הוראות המתכון — שלב בכל שורה';
   const button=actionButton('import-selected-recipe','קלוט מתכון מקישור / מהוראות שהדבקתי',async()=>{
     const status=$('recipe-import-status');button.disabled=true;status.textContent='קורא את המתכון…';
     try{
       const response=await fetch('/v1/coach/recipe-import',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:$('intake-recipe_url').value.trim(),text:text.value.trim(),title:state.dish_title})});
       const recipe=await response.json();if(!response.ok)throw new Error(recipe.message||'לא ניתן לקלוט את המתכון. אפשר להדביק את הוראות ההכנה.');
       const preview=$('recipe-import-preview');preview.replaceChildren(el('h4',recipe.title),el('p',`${recipe.steps.length} שלבי הכנה נקלטו. בדוק שהם שייכים למתכון שבחרת.`));
       const steps=el('ol');for(const step of recipe.steps)steps.append(el('li',step.text));preview.append(steps);
       const adopt=actionButton('adopt-imported-recipe',state.custom_steps.length?'השתמש בשלבי המתכון במקום התוכנית הנוכחית':'הוסף את שלבי המתכון למנה שלי',async()=>{adopt.disabled=true;const result=await coachCommand('attach_recipe',{recipe_snapshot:recipe});if(!result)adopt.disabled=false;});preview.append(adopt);status.textContent='המתכון נקלט לתצוגה מקדימה. אשר להוספת השלבים.';
     }catch(error){status.textContent=error.message;}finally{button.disabled=false;}
   });
   const status=el('p');status.id='recipe-import-status';status.setAttribute('role','status');const preview=el('section');preview.id='recipe-import-preview';source.append(button,status,preview);
   if(state.recipe_snapshot){const recipe=state.recipe_snapshot,attached=el('details','','attached-recipe');attached.id='attached-recipe';attached.append(el('summary','המתכון שלי: '+recipe.title));if(recipe.url){const link=el('a','פתח את המתכון המקורי');link.href=recipe.url;link.target='_blank';link.rel='noopener noreferrer';attached.append(link);}if(recipe.ingredients.length){attached.append(el('h4','מצרכים כפי שנקלטו'));const ingredients=el('ul');for(const item of recipe.ingredients)ingredients.append(el('li',item));attached.append(ingredients);}const steps=el('ol');for(const step of recipe.steps)steps.append(el('li',step.text));attached.append(steps);$('cooking-intake').prepend(attached);}
   sendContext();
 }
 window.addEventListener('message',event=>{const frame=window.chefReportFrame;if(event.origin!==location.origin||!frame||event.source!==frame.contentWindow)return;if(event.data?.type==='chef-report-ready')sendContext();if(event.data?.type==='chef-cancel-legacy-timer')void coachCommand('timer_cancel');});
 const render=renderCoach;renderCoach=function(){render();renderRecipeImport();};renderCoach();
})();
