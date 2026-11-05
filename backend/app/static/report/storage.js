// Durable, account-partitioned records and an ordered transactional outbox.
let opening;
export function database(){
 if(!opening)opening=new Promise((resolve,reject)=>{
   const request=indexedDB.open('chef-action-log-v1',1);
   request.onupgradeneeded=()=>{const db=request.result;for(const name of ['entries','sessions']){const store=db.createObjectStore(name,{keyPath:['owner','id']});store.createIndex('owner','owner');}const queue=db.createObjectStore('outbox',{keyPath:'seq',autoIncrement:true});queue.createIndex('owner','owner');db.createObjectStore('meta',{keyPath:'key'});};
   request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error);request.onblocked=()=>reject(new Error('סגור לשוניות ישנות כדי לפתוח את האחסון.'));
 });return opening;
}
export async function read(store,key){const db=await database();return new Promise((resolve,reject)=>{const request=db.transaction(store).objectStore(store).get(key);request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error);});}
export async function all(store,owner){const db=await database();return new Promise((resolve,reject)=>{const request=db.transaction(store).objectStore(store).index('owner').getAll(owner);request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error);});}
export async function write(stores,work){const db=await database();return new Promise((resolve,reject)=>{const tx=db.transaction(stores,'readwrite');tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error||new Error('השמירה המקומית לא הושלמה.'));try{work(tx);}catch(error){tx.abort();reject(error);}});}
export async function put(store,value){return write([store],tx=>tx.objectStore(store).put(value));}
export async function meta(key,value){if(arguments.length===2){await put('meta',{key,value});return value;}return (await read('meta',key))?.value;}
export async function queue(owner,body,local,store='entries'){
 await write([store,'outbox'],tx=>{tx.objectStore(store).put({...local,owner,pending:true});tx.objectStore('outbox').add({owner,body,entity:local.id,store});});
}
export async function pending(owner){return (await all('outbox',owner)).sort((a,b)=>a.seq-b.seq);}
