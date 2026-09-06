const urls=['app-00.txt','app-01.txt','app-02.txt','app-03.txt','app-04.txt','app-05.txt'];
try{
  const parts=await Promise.all(urls.map(async u=>{const r=await fetch(u,{cache:'no-store'});if(!r.ok)throw new Error(`${u}: HTTP ${r.status}`);return r.text();}));
  let code=parts.join('\n');

  // Visual quality: clearer atmosphere, brighter filmic exposure, sharper aerial imagery.
  code=code.replace('renderer.toneMappingExposure=1.05;','renderer.toneMappingExposure=1.12;');
  code=code.replace('scene.background=new THREE.Color(0xaecbe2);','scene.background=new THREE.Color(0xb7d0e4);');
  code=code.replace('scene.fog=new THREE.FogExp2(0xc5d4dc,0.0017);','scene.fog=new THREE.FogExp2(0xc7d3da,0.00105);');
  code=code.replace('const z=16,lats=routeLL.map(p=>p.lat),lons=routeLL.map(p=>p.lon),pad=.004;','const z=17,lats=routeLL.map(p=>p.lat),lons=routeLL.map(p=>p.lon),pad=.0038;');
  code=code.replace('const maxTiles=MOBILE?42:65;','const maxTiles=MOBILE?54:96;');

  // More plausible carriageway proportions.
  code=code.replace('roadGroup.add(makeRoadStrip(routeWorld,12,.01,sidewalkMat));','roadGroup.add(makeRoadStrip(routeWorld,13.2,.012,sidewalkMat));');
  code=code.replace('roadGroup.add(makeRoadStrip(routeWorld,7.4,.035,asphalt));','roadGroup.add(makeRoadStrip(routeWorld,8.2,.038,asphalt));');
  code=code.replace('const outer=makeRoadStrip(routeWorld,18,-.01,vergeMat);','const outer=makeRoadStrip(routeWorld,18.8,-.01,vergeMat);');

  // Critical geometry fix: OSM returns several independent way segments. The old version
  // sorted all vertices by latitude, which can create false diagonals. Chain segments by
  // matching their real endpoints instead.
  const oldRoute=`    let pts=[];\n    for(const e of data.elements||[]) if(e.geometry) for(const p of e.geometry) if(p?.lat&&p?.lon) pts.push({lat:p.lat,lon:p.lon});\n    pts.sort((a,b)=>a.lat-b.lat || a.lon-b.lon);\n    const ded=[];for(const p of pts){if(!ded.length||hav(ded[ded.length-1],p)>2.0) ded.push(p);}\n    if(ded.length<8) throw new Error('zu wenige Straßenpunkte');\n    routeLL=ded;state.routeSource='OpenStreetMap';`;
  const newRoute=`    const segs=(data.elements||[]).filter(e=>Array.isArray(e.geometry)&&e.geometry.length>1).map(e=>e.geometry.filter(p=>p?.lat&&p?.lon).map(p=>({lat:p.lat,lon:p.lon}))).filter(s=>s.length>1);\n    if(!segs.length) throw new Error('zu wenige Straßenpunkte');\n    let start=0,flip=false,best=Infinity;\n    for(let i=0;i<segs.length;i++){for(const f of [false,true]){const p=f?segs[i][segs[i].length-1]:segs[i][0];const score=p.lat*1000+p.lon;if(score<best){best=score;start=i;flip=f;}}}\n    const used=new Set([start]);let chain=flip?[...segs[start]].reverse():[...segs[start]];\n    while(used.size<segs.length){const anchor=chain[chain.length-1];let pick=-1,rev=false,dist=Infinity;for(let i=0;i<segs.length;i++)if(!used.has(i)){const d0=hav(anchor,segs[i][0]),d1=hav(anchor,segs[i][segs[i].length-1]);if(Math.min(d0,d1)<dist){dist=Math.min(d0,d1);pick=i;rev=d1<d0;}}if(pick<0||dist>120)break;used.add(pick);const s=rev?[...segs[pick]].reverse():segs[pick];for(const p of s){if(!chain.length||hav(chain[chain.length-1],p)>1.2)chain.push(p);}}\n    if(chain.length<8) throw new Error('zu wenige Straßenpunkte');\n    routeLL=chain;state.routeSource='OpenStreetMap';`;
  if(code.includes(oldRoute)) code=code.replace(oldRoute,newRoute);
  else console.warn('Straßenachsen-Patch konnte nicht exakt angewendet werden.');

  const blob=new Blob([code],{type:'text/javascript'});
  const moduleUrl=URL.createObjectURL(blob);
  await import(moduleUrl);
}catch(e){
  console.error(e);
  const t=document.getElementById('loadingText');
  if(t)t.textContent='3D-Code konnte nicht geladen werden: '+(e?.message||e);
}
