(function(){
  const q = document.querySelector("#q");
  if(q){ const param=new URLSearchParams(location.search).get("q")||""; q.value=param; q.addEventListener("input",e=>{const v=e.target.value; const u=new URL(location); v?u.searchParams.set("q",v):u.searchParams.delete("q"); history.replaceState({}, "", u);});}
  document.querySelectorAll("[data-copy]").forEach(b=>b.addEventListener("click",()=>{navigator.clipboard.writeText(b.dataset.copy).then(()=>{b.innerText="Zkopírováno"; setTimeout(()=>b.innerText="Kopírovat odkaz",1400);});}));
  document.querySelectorAll("[data-share]").forEach(a=>a.addEventListener("click",(e)=>{e.preventDefault(); const u=a.getAttribute("href"); if(navigator.share){navigator.share({url:u,title:document.title});} else { window.open(u,"_blank"); }}));
  const form = document.querySelector("#news-form");
  if(form){ form.addEventListener("submit",async(e)=>{e.preventDefault(); const email=form.querySelector("input[type=email]").value.trim(); if(!email) return;
    try{ const endpoint=form.dataset.endpoint||""; if(endpoint.startsWith("https://")){ await fetch(endpoint,{method:"POST",headers:{'Content-Type':'application/json'},body:JSON.stringify({email})});}
      form.innerHTML="<small>Děkujeme, potvrďte prosím odběr v e-mailu.</small>";
    }catch(_){ form.innerHTML="<small>Odesláno. Pokud nic nedorazí, napište na info@tvojehnizdo.com.</small>";}
  });}
  // UTM self-tagging (přidá utm_* do odchozích odkazů)
  const utm="utm_source=magazin&utm_medium=referral&utm_campaign=content";
  document.querySelectorAll("a[href^='https://']").forEach(a=>{try{const u=new URL(a.href); ["utm_source","utm_medium","utm_campaign"].forEach(k=>{if(!u.searchParams.has(k)){ const [k2,v]=utm.split("&").find(p=>p.startsWith(k)).split("="); u.searchParams.set(k2,v);} }); a.href=u.toString(); }catch(_){} });
})();