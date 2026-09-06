const urls=['app-00.txt','app-01.txt','app-02.txt','app-03.txt','app-04.txt','app-05.txt'];
try{
  const parts=await Promise.all(urls.map(async u=>{const r=await fetch(u,{cache:'no-store'});if(!r.ok)throw new Error(`${u}: HTTP ${r.status}`);return r.text();}));
  const blob=new Blob([parts.join('\n')],{type:'text/javascript'});
  const moduleUrl=URL.createObjectURL(blob);
  await import(moduleUrl);
}catch(e){
  console.error(e);
  const t=document.getElementById('loadingText');
  if(t)t.textContent='3D-Code konnte nicht geladen werden: '+(e?.message||e);
}
