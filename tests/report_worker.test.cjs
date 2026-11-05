const test=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const path=require('node:path');

test('push is handled by the worker without any open page and links only to the report app',async()=>{
  const handlers={},notifications=[],opened=[];
  const self={addEventListener:(name,fn)=>handlers[name]=fn,registration:{showNotification:async(title,options)=>notifications.push({title,...options})},clients:{matchAll:async()=>[],openWindow:async url=>opened.push(url)}};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../backend/app/static/report/sw.js'),'utf8'),{self,URL});
  let completion;
  handlers.push({data:{json:()=>({title:'Timer elapsed',body:'Check the dish',tag:'stable-delivery-id',url:'https://untrusted.example/'})},waitUntil:promise=>completion=promise});
  await completion;
  assert.equal(notifications.length,1);
  assert.equal(notifications[0].tag,'stable-delivery-id');
  assert.equal(notifications[0].data.url,'/report/');
  handlers.notificationclick({notification:{close(){}},waitUntil:promise=>completion=promise});
  await completion;
  assert.equal(opened[0],'/report/');
});
