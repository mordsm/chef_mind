'use strict';
(() => {
 const panel=el('details','','panel');panel.id='culinary-engine-editor';
 const select=el('select'), rules=el('option','משפחות, שיטות וסיבות לחסימה'),registry=el('option','חומרי גלם ושיוך למשפחות');
 rules.value='rules';registry.value='registry';select.append(rules,registry);select.setAttribute('aria-label','קובץ מנוע קולינרי');
 const area=el('textarea');area.rows=22;area.dir='ltr';area.id='culinary-engine-yaml';area.setAttribute('aria-label','קובץ המקור של המנוע');
 const status=el('p'),path=el('p'),load=el('button','טען מקור'),save=el('button','שמור קובץ מקור משותף'),check=el('input'),label=el('label');
 status.setAttribute('role','status');load.type=save.type='button';check.type='checkbox';label.append(check,document.createTextNode('בדקתי ומאשר שינוי שישפיע על ברירת המחדל לכל המשתמשים'));
 panel.append(el('summary','מנוע קולינרי — משפחות וחומרי גלם'),el('p','הקטלוג משייך כל חומר גלם למשפחה. קובץ החוקים מגדיר שיטות מותרות והסברים לחסימות. שיטה שלא הותרה חסומה. ההגדרות משותפות; קונפיגורציית שיטות פרטית מאושרת מקבלת קדימות. התאמת שיטה אינה מחליפה בדיקות בטיחות או תהליך מאומת.'),select,path,load,area,label,save,status);
 $('knowledge').append(panel);let data=null;
 function permissions(){const allowed=!!identityUser&&role==='reviewer';area.readOnly=!allowed;save.disabled=!allowed;label.hidden=!allowed;}
 function render(){if(!data)return;area.value=data[select.value+'_yaml'];path.textContent='מקור: '+data.source_paths[select.value];check.checked=false;permissions();}
 async function refresh(){try{data=await publicApi('/v1/culinary/engine');render();status.textContent='קובץ המקור נטען. שינויים תקינים חלים בבחירת השיטה הבאה.';}catch{status.textContent='טעינת קובצי המנוע נכשלה.';}}
 select.addEventListener('change',render);load.addEventListener('click',()=>void refresh());
 save.addEventListener('click',async()=>{if(!check.checked){status.textContent='נדרש אישור לשינוי המשותף.';return;}save.disabled=true;try{data=await api('/v1/culinary/engine/sources/'+select.value,'PUT',{expected_revision:data.revision,yaml_text:area.value,reviewed:true});render();status.textContent='קובץ המקור נשמר והופעל.';document.dispatchEvent(new Event('chef-method-policy-changed'));}catch(error){status.textContent='השמירה נכשלה: '+(error.message||'בדוק מבנה, הפניות והרשאות; במקרה של שינוי מקביל טען מחדש.');}finally{permissions();}});
 panel.addEventListener('toggle',()=>{if(panel.open&&!data)void refresh();});document.addEventListener('chef-auth-changed',()=>{check.checked=false;permissions();});permissions();
})();
