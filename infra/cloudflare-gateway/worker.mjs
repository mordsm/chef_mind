// Fixed workers.dev address in front of the existing Chef origin.
// CHEF_ORIGIN is controlled by the deployment script, never by incoming requests.
export function originURL(value) {
  const origin = new URL(value);
  if (origin.protocol !== 'https:' || origin.username || origin.password || origin.port ||
      origin.pathname !== '/' || origin.search || origin.hash ||
      !/^[a-z0-9-]+\.trycloudflare\.com$/.test(origin.hostname)) {
    throw new Error('Configure an HTTPS Chef tunnel origin');
  }
  return origin;
}

export function gateway(fetchOrigin = fetch) {
  return {async fetch(request, env) {
    let origin;
    try { origin = originURL(env.CHEF_ORIGIN); }
    catch {
      return new Response('The kitchen connection has not been configured yet.', {
        status: 503, headers: {'Content-Type':'text/plain; charset=utf-8','Cache-Control':'no-store'}
      });
    }
    const incoming = new URL(request.url);
    const target = new URL(incoming.pathname + incoming.search, origin);
    // A path starting // must not be interpreted as an alternate network host.
    target.protocol = origin.protocol;
    target.host = origin.host;
    const headers = new Headers(request.headers);
    headers.delete('host');
    headers.delete('cookie'); // Chef uses explicit account Bearer tokens, not ambient cookies.
    const upstreamRequest = new Request(target, {
      method: request.method, headers, redirect:'manual',
      duplex:'half',
      body: ['GET','HEAD'].includes(request.method) ? undefined : request.body
    });
    let response;
    try { response = await fetchOrigin(upstreamRequest); }
    catch { return unavailable(request); }
    // Do not expose Cloudflare's DNS/tunnel error document as if it were the app.
    if ([502,503,504,530].includes(response.status)) return unavailable(request);
    const outgoing = new Headers(response.headers);
    outgoing.set('Cache-Control','no-store');
    outgoing.set('X-Chef-Gateway','permanent');
    outgoing.delete('Set-Cookie');
    const location = outgoing.get('Location');
    if (location) {
      const redirect = new URL(location, origin);
      if (redirect.origin === origin.origin) {
        outgoing.set('Location', incoming.origin + redirect.pathname + redirect.search + redirect.hash);
      }
    }
    return new Response(response.body, {status:response.status, statusText:response.statusText, headers:outgoing});
  }};
}
function unavailable(request) {
  const headers={'Cache-Control':'no-store','Retry-After':'15','X-Chef-Gateway':'permanent'};
  if(request.method==='GET'&&(request.headers.get('Accept')||'').includes('text/html')) {
    headers['Content-Type']='text/html; charset=utf-8';
    return new Response('<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="15"><title>המטבח מתחבר מחדש</title><body style="font:22px system-ui;line-height:1.7;max-width:650px;margin:12vh auto;padding:24px;color:#173b30"><h1>המטבח מתחבר מחדש</h1><p>החיבור למחשב המטבח אינו זמין כרגע. הדף ינסה להתחבר שוב בעוד 15 שניות.</p><p>אין צורך לשנות כתובת. אם המחשב כבוי או ללא רשת, יש לחבר אותו כדי להמשיך.</p><a href="">נסה שוב עכשיו</a></body></html>',{status:503,headers});
  }
  headers['Content-Type']='application/json; charset=utf-8';
  return new Response(JSON.stringify({error:'kitchen_unavailable',message:'החיבור למטבח אינו זמין כרגע. נסה שוב לאחר חידוש החיבור.'}),{status:503,headers});
}
export default gateway();
