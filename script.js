(function(){
  const q=document.querySelector("#q"); if(q){const p=new URLSearchParams(location.search).get("q")||""; q.value=p;
    q.addEventListener("input",e=>{const v=e.target.value; const u=new URL(location); v?u.searchParams.set("q",v):u.searchParams.delete("q"); history.replaceState({}, "", u);});}
  document.querySelectorAll("[data-copy]").forEach(b=>b.addEventListener("click",()=>{navigator.clipboard.writeText(b.dataset.copy).then(()=>{b.innerText="Zkopírováno"; setTimeout(()=>b.innerText="Kopírovat odkaz",1400);});}));
  const utm="utm_source=magazin&utm_medium=referral&utm_campaign=content";
  document.querySelectorAll("a[href^=\"https://\"]").forEach(a=>{try{const u=new URL(a.href);
    ["utm_source","utm_medium","utm_campaign"].forEach(k=>{ if(!u.searchParams.has(k)){ const t=utm.split("&").find(x=>x.startsWith(k)).split("="); u.searchParams.set(t[0],t[1]); }}); a.href=u.toString(); }catch(_){ }});
})();
