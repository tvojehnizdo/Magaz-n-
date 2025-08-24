self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>clients.claim());
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  e.respondWith(caches.open('th-magazin-v1').then(async c=>{
    const k=await c.match(e.request); if(k) return k;
    try{const r=await fetch(e.request); if(r&&r.status===200)c.put(e.request,r.clone()); return r;}
    catch{return k||fetch(e.request);}
  }));
});