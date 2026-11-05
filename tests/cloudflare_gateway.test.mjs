import test from 'node:test';
import assert from 'node:assert/strict';
import {gateway, originURL} from '../infra/cloudflare-gateway/worker.mjs';

test('passes authenticated API mutations to the configured origin without caching', async()=>{
  let sent;
  const worker=gateway(async request=>{sent=request;return new Response('{"saved":true}',{headers:{'Content-Type':'application/json'}});});
  const response=await worker.fetch(new Request('https://chef.example.workers.dev/v1/action-log/mutations?q=1',{method:'POST',headers:{Authorization:'Bearer test-token',Cookie:'unrelated=cookie'},body:'{"value":1}'}),{CHEF_ORIGIN:'https://test-origin.trycloudflare.com'});
  assert.equal(sent.url,'https://test-origin.trycloudflare.com/v1/action-log/mutations?q=1');
  assert.equal(sent.headers.get('Authorization'),'Bearer test-token');
  assert.equal(sent.headers.get('Cookie'),null);
  assert.equal(await sent.text(),'{"value":1}');
  assert.equal(response.headers.get('Cache-Control'),'no-store');
});

test('does not permit a request path to override the configured origin',async()=>{
  let sent;
  const worker=gateway(async request=>{sent=request;return new Response('ok');});
  await worker.fetch(new Request('https://chef.example.workers.dev//evil.example/secret'),{CHEF_ORIGIN:'https://test-origin.trycloudflare.com'});
  assert.equal(new URL(sent.url).host,'test-origin.trycloudflare.com');
});

test('rewrites origin redirects back to the permanent address and preserves SW responses',async()=>{
  const worker=gateway(async()=>new Response('',{status:307,headers:{Location:'https://test-origin.trycloudflare.com/report/'}}));
  const response=await worker.fetch(new Request('https://chef.example.workers.dev/report'),{CHEF_ORIGIN:'https://test-origin.trycloudflare.com'});
  assert.equal(response.headers.get('Location'),'https://chef.example.workers.dev/report/');
});

test('unconfigured or unsafe origins fail closed',async()=>{
  for(const origin of ['http://localhost:8800','https://example.com','https://a.trycloudflare.com/path','https://secret@a.trycloudflare.com'])assert.throws(()=>originURL(origin));
  const worker=gateway(()=>{throw Error('must not fetch');});
  assert.equal((await worker.fetch(new Request('https://chef.example.workers.dev'),{})).status,503);
});

test('tunnel DNS failure shows a recoverable page without retrying writes',async()=>{
  const worker=gateway(async()=>new Response('Origin DNS error 1016',{status:530}));
  const env={CHEF_ORIGIN:'https://test-origin.trycloudflare.com'};
  const page=await worker.fetch(new Request('https://chef.example.workers.dev/',{headers:{Accept:'text/html'}}),env);
  assert.equal(page.status,503);
  assert.equal(page.headers.get('Cache-Control'),'no-store');
  assert.match(await page.text(),/http-equiv="refresh"/);
  const write=await worker.fetch(new Request('https://chef.example.workers.dev/v1/action-log/mutations',{method:'POST',body:'{}'}),env);
  assert.equal((await write.json()).error,'kitchen_unavailable');
});
