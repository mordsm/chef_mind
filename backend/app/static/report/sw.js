'use strict';
const CACHE='chef-report-shell-v13';
const SHELL=['/report/','/assets/report/style.css','/assets/report/app.js','/assets/report/storage.js','/assets/report/actions.json','/assets/report/manifest.webmanifest','/assets/report/icon-192.png','/assets/report/icon-512.png'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(SHELL)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil((async()=>{for(const key of await caches.keys())if(key.startsWith('chef-report-shell-')&&key!==CACHE)await caches.delete(key);await self.clients.claim();})()));
self.addEventListener('fetch',event=>{
 const url=new URL(event.request.url);
 // Never cache credentials, private API responses, mutations or unrelated pages.
 if(event.request.method!=='GET'||url.origin!==self.location.origin||url.pathname.startsWith('/v1/'))return;
 if(event.request.mode==='navigate'&&url.pathname==='/report/'){
   event.respondWith(fetch(event.request).catch(()=>caches.match('/report/')));return;
 }
 if(SHELL.includes(url.pathname))event.respondWith((async()=>{try{const response=await fetch(event.request);if(!response.ok)throw Error('Shell unavailable');const cache=await caches.open(CACHE);await cache.put(url.pathname,response.clone());return response;}catch(error){const saved=await caches.match(url.pathname);if(saved)return saved;throw error;}})());
});
self.addEventListener('push',event=>event.waitUntil((async()=>{let data={};try{data=event.data.json();}catch{}await self.registration.showNotification(data.title||'הגיע זמן לבדוק את הבישול',{body:data.body||'פתח את המטבח ובדוק את המנה.',tag:data.tag||'chef-timer',icon:'/assets/report/icon-192.png',badge:'/assets/report/icon-192.png',data:{url:'/report/'},requireInteraction:true});})()));
self.addEventListener('notificationclick',event=>{event.notification.close();event.waitUntil((async()=>{for(const client of await self.clients.matchAll({type:'window',includeUncontrolled:true})){if(new URL(client.url).pathname==='/report/')return client.focus();}return self.clients.openWindow('/report/');})());});
