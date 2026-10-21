'use strict';
(() => {
 const panel=$('problem-rules-editor'),button=el('button','הוסף טיפולים חסרים מברירת המחדל לטיוטה','secondary');
 button.type='button';button.id='problem-rule-import-defaults';
 $('problem-rules-yaml').insertAdjacentElement('beforebegin',button);
 function permissions(){button.hidden=!identityUser||role!=='reviewer';}
 button.addEventListener('click',async()=>{
   const epoch=authEpoch;button.disabled=true;
   try{
     const result=await api('/v1/coach/problem-rules/with-defaults','POST',{yaml_text:$('problem-rules-yaml').value});
     if(epoch!==authEpoch)return;
     $('problem-rules-yaml').value=result.yaml_text;
     panel.querySelector('input[type="checkbox"]').checked=false;
     $('problem-rules-status').textContent=result.added_ids.length?'נוספו לטיוטה טיפולים חסרים. יש לבדוק ולאשר לפני שמירה. חוקים קיימים נשמרו.':'כל סוגי הבעיות המוגדרים כבר נמצאים בטיוטה. לא הוחלף חוק קיים.';
   }catch{if(epoch===authEpoch)$('problem-rules-status').textContent='הוספת הטיפולים נכשלה. בדוק את תקינות הטיוטה וההרשאות.';}
   finally{button.disabled=false;permissions();}
 });
 document.addEventListener('chef-auth-changed',permissions);permissions();
})();
