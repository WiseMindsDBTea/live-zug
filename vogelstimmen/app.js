/* Vogelohr – App */
(() => {
"use strict";

/* ================================================================ Grundlagen */
const BIRDS = window.BIRDS || [];
BIRDS.forEach(b => { ["present","sings","verw","hab","snd"].forEach(k => { b[k] = b[k] || []; }); });
const BY = Object.fromEntries(BIRDS.map(b => [b.id, b]));
let MEDIA = {};
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const MONTHS = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"];
const M1 = ["J","F","M","A","M","J","J","A","S","O","N","D"];
const NOW = new Date().getMonth() + 1;
const store = {
  get(k, d){ try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v){ try { localStorage.setItem(k, JSON.stringify(v)); } catch {} }
};
const fold = s => String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ß/g, "ss");
const HAB = {
  garten:{label:"Siedlung & Garten"}, wald:{label:"Wald & Park"}, wasser:{label:"Am Wasser"},
  feld:{label:"Feld & Wiese"}, berge:{label:"Berge"}, kueste:{label:"Küste"}
};
const FREQ = ["", "sehr häufig", "häufig", "verbreitet", "selten"];
const KIND = { song:"Gesang", call:"Ruf", drum:"Trommeln", crow:"Krähen", clatter:"Klappern", wings:"Flügel", primary:"Aufnahme", secondary:"Aufnahme 2" };
const SHAPES = {
  floete:  {label:"flötet melodisch", svg:'<path d="M4 20c6-9 10-9 16-3s10 6 16-4M44 18c4-6 8-6 12 0" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'},
  zwitscher:{label:"zwitschert, trillert", svg:[...Array(14)].map((_,i)=>`<path d="M${4+i*4} ${10+(i%3)*4}l2 -5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>`).join("")},
  motiv:   {label:"wiederholt kurze Motive", svg:[0,1,2,3].map(i=>`<rect x="${3+i*15}" y="9" width="4" height="12" rx="1.5" fill="currentColor"/><rect x="${9+i*15}" y="15" width="4" height="7" rx="1.5" fill="currentColor"/>`).join("")},
  name:    {label:"ruft seinen Namen", svg:'<rect x="6" y="8" width="16" height="6" rx="3" fill="currentColor"/><rect x="28" y="16" width="20" height="6" rx="3" fill="currentColor"/><path d="M54 10l4-3M54 16h5M54 22l4 3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'},
  kraechz: {label:"krächzt, schimpft", svg:[0,1,2].map(i=>`<path d="M${4+i*20} 24V8M${7+i*20} 24V6M${10+i*20} 24V9M${13+i*20} 24V7" stroke="currentColor" stroke-width="2.2"/>`).join("")},
  tief:    {label:"tief, gurrend, huhu", svg:'<rect x="4" y="22" width="14" height="5" rx="2.5" fill="currentColor"/><rect x="22" y="21" width="22" height="6" rx="3" fill="currentColor"/><rect x="48" y="22" width="10" height="5" rx="2.5" fill="currentColor"/>'},
  wasser:  {label:"quakt, schnattert", svg:[0,1,2,3].map(i=>`<path d="M${4+i*15} 22c2-8 6-8 8 0" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>`).join("")},
  trommel: {label:"klopft, trommelt, klappert", svg:[...Array(16)].map((_,i)=>`<path d="M${6+i*3.2} 26V6" stroke="currentColor" stroke-width="1.6"/>`).join("")},
  schrill: {label:"hoch und schrill", svg:'<path d="M4 6h12M22 5h10M38 6h14" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'},
  lach:    {label:"lacht, kichert", svg:[0,1,2,3,4,5].map(i=>`<circle cx="${6+i*9}" cy="${8+i*2.6}" r="3" fill="currentColor"/>`).join("")}
};
const shapeSVG = k => `<svg viewBox="0 0 62 30" aria-hidden="true">${SHAPES[k].svg}</svg>`;

const presentNow = b => b.present.includes(NOW);
const singsNow = b => presentNow(b) && b.sings.includes(NOW);
const clipsOf = b => (MEDIA[b.id]?.clips || []);
const imgOf = b => MEDIA[b.id]?.img || null;
const thumb = b => imgOf(b)?.thumb || "";
const photoHTML = (b, cls = "") => thumb(b)
  ? `<img class="${cls}" src="${esc(thumb(b))}" alt="" loading="lazy" decoding="async">`
  : `<span class="${cls} ph">${esc(b.de[0])}</span>`;

/* ================================================================ Logbuch & Training */
let heard = store.get("vo-heard", {});
const isHeard = id => !!heard[id];
function toggleHeard(id){
  if (heard[id]) delete heard[id]; else heard[id] = new Date().toISOString().slice(0,10);
  store.set("vo-heard", heard);
}
let train = store.get("vo-train", {});

/* ================================================================ Toast */
let toastT;
function toast(msg){
  const t = $("#toast"); t.textContent = msg; t.classList.add("show");
  clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove("show"), 3200);
}

/* ================================================================ Audio */
const audio = new Audio();
audio.preload = "auto";
const A = { key:null, bird:null, idx:0, rate:1, loop:false };
function setPreserve(on){ audio.preservesPitch = on; audio.webkitPreservesPitch = on; audio.mozPreservesPitch = on; }

/* Wichtig für iOS: play() muss synchron im Tipp-Ereignis passieren – deshalb kein await davor. */
function play(bird, idx = 0, from = 0){
  const clip = clipsOf(bird)[idx];
  if (!clip){ toast(`Für „${bird.de}“ gibt es noch keine Aufnahme.`); return Promise.resolve(); }
  stopChorus();
  const key = `${bird.id}:${idx}`;
  if (audio.dataset.src !== clip.src){ audio.src = clip.src; audio.dataset.src = clip.src; }
  A.key = key; A.bird = bird; A.idx = idx;
  audio.loop = A.loop; audio.playbackRate = A.rate; setPreserve(true);
  const seekTo = () => { const d = audio.duration || clip.dur; try { audio.currentTime = Math.max(0, Math.min(from * d, d - 0.05)); } catch {} };
  if (from > 0){ if (audio.readyState >= 1) seekTo(); else audio.addEventListener("loadedmetadata", seekTo, { once:true }); }
  else if (audio.readyState >= 1) { try { audio.currentTime = 0; } catch {} }
  markLoading(key, true);
  const p = audio.play();
  showBar(); syncButtons(); frame();
  return (p || Promise.resolve()).catch(e => {
    if (e && e.name !== "AbortError") toast("Abspielen nicht möglich – Verbindung prüfen.");
  }).finally(() => markLoading(key, false));
}
function toggle(bird, idx = 0, from = null){
  const key = `${bird.id}:${idx}`;
  if (A.key === key && audio.src){
    if (from != null){ try { audio.currentTime = from * (audio.duration || 0); } catch {} if (audio.paused) audio.play(); return; }
    if (audio.paused) audio.play(); else audio.pause();
    return;
  }
  play(bird, idx, from || 0);
}
function markLoading(key, on){ $$(`[data-play="${CSS.escape(key)}"]`).forEach(b => b.classList.toggle("loading", on)); }

/* ================================================================ Lautschrift synchron */
const ONO_CACHE = new Map();
function onoText(b, c){
  const [song, call] = b.ono || [];
  if (c.kind === "call" || c.kind === "secondary") return call || song || "";
  return song || call || "";
}
function tokenize(t){ const out = []; t.replace(/([^\s-]+)([\s-]*)/g, (m, s, sep) => { out.push({ s, sep }); return m; }); return out; }
function onoModel(key){
  if (ONO_CACHE.has(key)) return ONO_CACHE.get(key);
  const [id, i] = key.split(":"); const b = BY[id]; const c = clipsOf(b)[+i];
  if (!b || !c || !c.ev || !c.ev.length){ ONO_CACHE.set(key, null); return null; }
  const toks = tokenize(onoText(b, c)); const n = toks.length;
  if (!n){ ONO_CACHE.set(key, null); return null; }
  const ev = []; for (let k = 0; k + 1 < c.ev.length; k += 2) ev.push([c.ev[k] / 100, c.ev[k + 1] / 100]);
  const gap = b.pg || 0.35, ph = [];
  ev.forEach(e => { const last = ph[ph.length - 1]; if (last && e[0] - last.t1 < gap){ last.t1 = e[1]; last.ev.push(e); } else ph.push({ t0:e[0], t1:e[1], ev:[e] }); });
  ph.forEach(p => { const m = p.ev.length; p.mode = m >= 2 * n ? "cyc" : m >= n ? "prop" : "time"; });
  const model = { toks, n, ph };
  ONO_CACHE.set(key, model);
  return model;
}
function onoAt(model, t){
  const ph = model.ph;
  let i = -1;
  for (let k = 0; k < ph.length; k++){ if (ph[k].t0 - 0.03 <= t) i = k; else break; }
  if (i < 0) return { i:-1, s:-1, live:false };
  const p = ph[i], live = t <= p.t1 + 0.15;
  let s;
  if (p.mode === "time") s = Math.min(model.n - 1, Math.floor(Math.max(0, t - p.t0) / Math.max(0.05, p.t1 - p.t0) * model.n));
  else {
    let j = 0; for (let k = 0; k < p.ev.length; k++){ if (p.ev[k][0] - 0.02 <= t) j = k; else break; }
    s = p.mode === "cyc" ? j % model.n : Math.min(model.n - 1, Math.floor(j * model.n / p.ev.length));
  }
  return { i, s, live };
}
const tokHTML = toks => toks.map((x, k) => `<i data-s="${k}">${esc(x.s)}</i>${esc(x.sep)}`).join("");
function onoTrackHTML(bird, idx = 0, win = 0){
  const c = clipsOf(bird)[idx]; if (!c) return "";
  const key = `${bird.id}:${idx}`, model = onoModel(key); if (!model) return "";
  const span = win && c.dur > win ? win : c.dur;
  const words = model.ph.map((p, k) => p.t0 < span - 0.2 ? `<span class="ow" data-w="${k}" style="left:${(p.t0 / span * 100).toFixed(2)}%">${tokHTML(model.toks)}</span>` : "").join("");
  return `<div class="ono-track" data-okey="${key}" aria-hidden="true">${words}</div>`;
}
function onoNowHTML(bird, idx = 0, cls = ""){
  const c = clipsOf(bird)[idx]; if (!c) return "";
  const key = `${bird.id}:${idx}`, model = onoModel(key);
  const toks = model ? model.toks : tokenize(onoText(bird, c)); if (!toks.length) return "";
  return `<div class="ono-now idle ${cls}" data-onow="${key}" aria-live="off"><span class="w">${tokHTML(toks)}</span></div>`;
}
function layoutTracks(root = document){
  $$(".ono-track", root).forEach(tr => {
    const W = tr.clientWidth; if (!W) return;
    const right = [-1e9, -1e9];
    $$(".ow", tr).forEach(w => {
      w.classList.remove("r1", "mini");
      w.style.removeProperty("margin-left"); w.style.removeProperty("--tick");
      const l = w.offsetLeft, wd = w.offsetWidth;
      const el = l + wd > W ? Math.max(0, W - wd) : l;           // am rechten Rand nach links schieben
      if (el >= right[0] + 6) right[0] = el + wd;
      else if (el >= right[1] + 6){ w.classList.add("r1"); right[1] = el + wd; }
      else { w.classList.add("mini"); return; }
      if (el !== l){ w.style.marginLeft = (el - l) + "px"; w.style.setProperty("--tick", (l - el) + "px"); }
    });
  });
}
let layoutT; window.addEventListener("resize", () => { clearTimeout(layoutT); layoutT = setTimeout(() => layoutTracks(), 150); });
const onoState = new Map();
function syncOno(key, t, playing){
  const model = key && onoModel(key);
  // alte Spuren zurücksetzen
  onoState.forEach((st, k) => { if (k !== key){ $$(`[data-okey="${CSS.escape(k)}"] .ow`).forEach(w => w.classList.remove("on", "past")); $$(`[data-onow="${CSS.escape(k)}"]`).forEach(n => { n.classList.add("idle"); $$("i", n).forEach(x => x.className = ""); }); onoState.delete(k); } });
  if (!model) return;
  const st = onoAt(model, t);
  const prev = onoState.get(key) || {};
  const sig = `${st.i}|${st.s}|${st.live}`;
  if (prev.sig === sig && prev.n === document.querySelectorAll(`[data-okey="${CSS.escape(key)}"],[data-onow="${CSS.escape(key)}"]`).length) return;
  onoState.set(key, { sig, n: document.querySelectorAll(`[data-okey="${CSS.escape(key)}"],[data-onow="${CSS.escape(key)}"]`).length });
  $$(`[data-okey="${CSS.escape(key)}"]`).forEach(tr => {
    $$(".ow", tr).forEach(w => {
      const k = +w.dataset.w;
      w.classList.toggle("past", k < st.i || (k === st.i && !st.live));
      w.classList.toggle("on", k === st.i && st.live);
      $$("i", w).forEach(x => { const sI = +x.dataset.s; x.className = k === st.i && st.live ? (sI < st.s ? "past" : sI === st.s ? "on" : "") : ""; });
    });
  });
  $$(`[data-onow="${CSS.escape(key)}"]`).forEach(n => {
    const newPhrase = prev.i !== st.i && st.i >= 0;
    n.classList.toggle("idle", st.i < 0);
    n.classList.toggle("rest", st.i >= 0 && !st.live);
    $$("i", n).forEach(x => { const sI = +x.dataset.s; x.className = st.live ? (sI < st.s ? "past" : sI === st.s ? "on" : "") : ""; });
    if (newPhrase && playing){ n.classList.remove("pop"); void n.offsetWidth; n.classList.add("pop"); }
  });
  onoState.get(key).i = st.i;
}

let lastKey = null;
function frame(){
  const p = audio.duration ? audio.currentTime / audio.duration : 0;
  const playing = !audio.paused && !audio.ended;
  if (lastKey && lastKey !== A.key) $$(`.spec[data-key="${CSS.escape(lastKey)}"]`).forEach(el => { el.style.setProperty("--p", 0); el.classList.remove("playing"); });
  lastKey = A.key;
  if (A.key) $$(`.spec[data-key="${CSS.escape(A.key)}"]`).forEach(el => {
    const w = +el.dataset.win || 0;
    const pp = w ? Math.min(1, audio.currentTime / w) : p;
    el.style.setProperty("--p", pp.toFixed(4)); el.classList.toggle("playing", playing && pp < 1);
  });
  const bs = $("#pbSpec"); bs.style.setProperty("--p", p.toFixed(4)); bs.classList.toggle("playing", playing);
  syncOno(A.key, audio.currentTime, playing);
  if (playing) requestAnimationFrame(frame);
}
function syncButtons(){
  const playing = !audio.paused && !audio.ended;
  $$("[data-play]").forEach(b => {
    const on = b.dataset.play === A.key && playing;
    b.innerHTML = `<svg aria-hidden="true"><use href="#i-${on ? "pause" : "play"}"/></svg>`;
    b.setAttribute("aria-label", (on ? "Pause: " : "Anhören: ") + (b.dataset.label || ""));
  });
  $("#pbPlay").innerHTML = `<svg aria-hidden="true"><use href="#i-${playing ? "pause" : "play"}"/></svg>`;
  $("#pbPlay").setAttribute("aria-label", playing ? "Pause" : "Weiter abspielen");
  if (kidActive) kidSync(playing);
}
["play","playing"].forEach(ev => audio.addEventListener(ev, () => { syncButtons(); requestAnimationFrame(frame); }));
["pause","ended","seeked"].forEach(ev => audio.addEventListener(ev, () => { syncButtons(); frame(); }));
audio.addEventListener("error", () => { if (audio.dataset.src) toast("Diese Aufnahme ließ sich nicht laden."); syncButtons(); });

function showBar(){
  if (!A.bird) return;
  const c = clipsOf(A.bird)[A.idx];
  $("#pbName").textContent = A.bird.de;
  $("#pbKind").textContent = KIND[c?.kind] || "Aufnahme";
  const s = $("#pbSpec"); s.style.setProperty("--spec", `url("${c.spec}")`); s.classList.add("has");
  $("#pbar").hidden = (route.view === "kinder" || route.view === "ueben");
}
$("#pbPlay").onclick = () => { if (audio.paused) audio.play(); else audio.pause(); };
$("#pbClose").onclick = () => { audio.pause(); $("#pbar").hidden = true; };
$("#pbInfo").onclick = () => { if (A.bird) go(`#/vogel/${A.bird.id}`); };
$("#pbSpec").onclick = e => { const r = e.currentTarget.getBoundingClientRect(); if (audio.duration) audio.currentTime = (e.clientX - r.left) / r.width * audio.duration; };

function specHTML(bird, idx = 0, cls = "", win = 0){
  const c = clipsOf(bird)[idx];
  const key = `${bird.id}:${idx}`;
  if (!c) return `<div class="spec ${cls}" aria-hidden="true"></div>`;
  const w = win && c.dur > win ? win : 0;
  return `<div class="spec has ${cls}" data-key="${key}" data-spec="${bird.id}:${idx}" ${w ? `data-win="${w}"` : ""} style='--spec:url("${esc(c.spec)}");--zoom:${w ? (c.dur / w).toFixed(3) : 1}' role="button" tabindex="-1" aria-label="${esc(bird.de)}: ${KIND[c.kind] || "Aufnahme"} abspielen"><i class="spec-ink"></i><i class="spec-done"></i><i class="spec-head"></i></div>`;
}
function playBtn(bird, idx = 0, cls = ""){
  const has = !!clipsOf(bird)[idx];
  return `<button class="play-b ${cls}" type="button" data-play="${bird.id}:${idx}" data-label="${esc(bird.de)}" aria-label="Anhören: ${esc(bird.de)}" ${has ? "" : "disabled"}><svg aria-hidden="true"><use href="#i-play"/></svg></button>`;
}
// Globale Klicks auf Sonagramme und Play-Knöpfe
document.addEventListener("click", e => {
  const pb = e.target.closest("[data-play]");
  if (pb){ e.preventDefault(); e.stopPropagation(); const [id, i] = pb.dataset.play.split(":"); toggle(BY[id], +i); return; }
  const sp = e.target.closest("[data-spec]");
  if (sp){
    e.preventDefault(); e.stopPropagation();
    const [id, i] = sp.dataset.spec.split(":");
    const r = sp.getBoundingClientRect();
    let f = Math.max(0, Math.min(.98, (e.clientX - r.left) / r.width));
    const w = +sp.dataset.win || 0, c = clipsOf(BY[id])[+i];
    if (w && c) f = f * w / c.dur;
    const key = `${id}:${i}`;
    if (A.key === key) toggle(BY[id], +i, f); else play(BY[id], +i, f < .12 ? 0 : f);
  }
}, true);

/* ================================================================ Router */
const route = { view:"lexikon", base:"#/" };
function go(h){ if (location.hash === h) onRoute(); else location.hash = h; }
window.addEventListener("hashchange", onRoute);

function onRoute(){
  const h = location.hash || "#/";
  const parts = h.replace(/^#\/?/, "").split("/").filter(Boolean);
  if (parts[0] === "vogel" && BY[parts[1]]){
    if (!$("#main").firstChild) renderView("lexikon");
    openDetail(BY[parts[1]]); return;
  }
  if (parts[0] === "vergleich" && BY[parts[1]] && BY[parts[2]]){
    if (!$("#main").firstChild) renderView("lexikon");
    openCompare(BY[parts[1]], BY[parts[2]]); return;
  }
  closeSheet();
  const v = ({ bestimmen:"bestimmen", ueben:"ueben", kinder:"kinder", morgen:"morgen" })[parts[0]] || "lexikon";
  route.base = h;
  if (v !== route.view || !$("#main").firstChild) renderView(v);
}
function renderView(v){
  if (route.view === "kinder" && v !== "kinder") kidStop();
  if (route.view === "bestimmen" && v !== "bestimmen") micStop();
  if (route.view === "morgen" && v !== "morgen") stopChorus();
  route.view = v;
  $$(".tabs a").forEach(a => { if (a.dataset.tab === v) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current"); });
  const m = $("#main");
  m.innerHTML = `<div class="view">${VIEWS[v]()}</div>`;
  AFTER[v]?.();
  window.scrollTo(0, 0);
  requestAnimationFrame(() => layoutTracks($("#main")));
  if (A.bird && !audio.paused) $("#pbar").hidden = (v === "kinder" || v === "ueben");
  else if (v === "kinder" || v === "ueben") $("#pbar").hidden = true;
  syncButtons(); frame();
  document.title = ({ lexikon:"Vogelohr – Vogelstimmen in D-A-CH", bestimmen:"Bestimmen – Vogelohr", ueben:"Üben – Vogelohr", kinder:"Kinder – Vogelohr", morgen:"Morgenchor – Vogelohr" })[v];
}

/* ================================================================ Lexikon */
const LX = { q:"", chip:"alle", sort:"gruppe" };
function dayBird(){
  const pool = BIRDS.filter(b => b.freq <= 2 && presentNow(b) && !b.night && clipsOf(b).length && b.snd.some(x => ["floete","zwitscher","motiv","name","lach"].includes(x)));
  const list = pool.length ? pool : BIRDS;
  const d = new Date(); const seed = d.getFullYear() * 400 + d.getMonth() * 31 + d.getDate();
  const singing = list.filter(singsNow);
  const from = singing.length >= 5 ? singing : list;
  return from[(seed * 7919) % from.length];
}
function lxMatches(b){
  const c = LX.chip;
  if (c === "jetzt" && !presentNow(b)) return false;
  if (c === "gehoert" && !isHeard(b.id)) return false;
  if (c === "geschichten" && !(b.kultur || b.kid)) return false;
  if (c === "nacht" && !b.night) return false;
  if (HAB[c] && !b.hab.includes(c)) return false;
  if (!LX.q) return true;
  const q = fold(LX.q);
  return fold([b.de, b.lat, (b.alias || []).join(" "), b.grp, b.laut, b.gesang, b.ruf, b.merk, b.wo, b.kultur, b.fakt].join(" ")).includes(q);
}
function rowHTML(b){
  const away = !presentNow(b);
  const sub = LX.q && !fold(b.de).includes(fold(LX.q)) && !fold(b.lat).includes(fold(LX.q)) && (b.alias||[]).find(a => fold(a).includes(fold(LX.q)));
  return `<a class="row${away ? " away" : ""}" href="#/vogel/${b.id}" data-id="${b.id}">
    <span class="row-ph">${photoHTML(b)}</span>
    ${isHeard(b.id) ? '<span class="heard-dot" title="Schon gehört"><svg><use href="#i-check"/></svg></span>' : ""}
    <span><span class="row-name">${esc(b.de)}${singsNow(b) ? '<span class="row-tag" title="singt jetzt" aria-label="singt jetzt">♪</span>' : ""}</span>
    <span class="row-sub">${sub ? `auch „${esc(sub)}“` : `<span class="lat">${esc(b.lat)}</span>`}</span></span>
    ${specHTML(b, 0, "", 9)}
  </a>`;
}
function groupsFor(list){
  const s = LX.sort;
  if (s === "az") return [["", list.slice().sort((a, b) => a.de.localeCompare(b.de, "de"))]];
  if (s === "haeufig"){
    return [1,2,3,4].map(f => [FREQ[f][0].toUpperCase() + FREQ[f].slice(1), list.filter(b => b.freq === f)]).filter(g => g[1].length);
  }
  if (s === "lebensraum"){
    return Object.entries(HAB).map(([k, v]) => [v.label, list.filter(b => b.hab[0] === k)]).filter(g => g[1].length);
  }
  const order = []; const map = {};
  list.forEach(b => { if (!map[b.grp]){ map[b.grp] = []; order.push(b.grp); } map[b.grp].push(b); });
  return order.map(g => [g, map[g]]);
}
function registerHTML(){
  const list = BIRDS.filter(lxMatches);
  if (!list.length) return `<p class="empty">Kein Vogel passt dazu. Versuch es mit einem Laut wie „quak“ oder „huhu“.</p>`;
  return groupsFor(list).map(([g, arr]) => `<section class="group">${g ? `<h2 class="group-h">${esc(g)} <small>${arr.length}</small></h2>` : ""}
    <div class="register">${arr.map(rowHTML).join("")}</div></section>`).join("");
}
function chipsHTML(){
  const n = f => BIRDS.filter(f).length;
  const chips = [
    ["alle", "Alle", BIRDS.length], ["jetzt", `Im ${MONTHS[NOW-1]} da`, n(presentNow)],
    ["geschichten", "Aus Liedern & Märchen", n(b => b.kultur || b.kid)], ["nacht", "Nachts", n(b => b.night)],
    ...Object.entries(HAB).map(([k, v]) => [k, v.label, n(b => b.hab.includes(k))]),
    ["gehoert", "Schon gehört", Object.keys(heard).length]
  ];
  return chips.map(([k, l, c]) => `<button class="chip" type="button" data-chip="${k}" aria-pressed="${LX.chip === k}">${esc(l)} <span class="n">${c}</span></button>`).join("");
}
const VIEWS = {};
const AFTER = {};
VIEWS.lexikon = () => {
  const b = dayBird();
  const present = BIRDS.filter(presentNow).length, sing = BIRDS.filter(singsNow).length;
  const hc = Object.keys(heard).length;
  return `
  <section class="today" aria-label="Stimme des Tages">
    <div>
      <div class="today-top">
        ${thumb(b) ? `<img class="today-photo" src="${esc(imgOf(b).src)}" alt="">` : ""}
        <div><p class="today-kicker">Stimme des Tages</p>
          <h1><a href="#/vogel/${b.id}" style="color:inherit;text-decoration:none">${esc(b.de)}</a></h1>
          <div class="lat">${esc(b.lat)}</div></div>
      </div>
      <p class="today-laut" style="margin-top:14px">${esc(b.laut)}</p>
    </div>
    <div>
      <div class="today-row">${playBtn(b, 0, "big")}<div class="today-spec">${specHTML(b, 0, "", 12)}${onoTrackHTML(b, 0, 12)}</div></div>
      <div class="today-meta" style="margin-top:12px">
        <span>Im ${MONTHS[NOW-1]} zu hören: <b>${present}</b> von ${BIRDS.length} Arten</span>
        <span>Singen gerade: <b>${sing}</b></span>
        <span>Schon gehört: <b>${hc}</b></span>
      </div>
    </div>
  </section>
  <div class="finder">
    <label class="search"><svg aria-hidden="true"><use href="#i-search"/></svg><span class="sr">Suchen</span>
      <input id="q" type="search" placeholder="Name, Laut, Ort …" value="${esc(LX.q)}" autocomplete="off" enterkeyhint="search">
      <select id="sort" aria-label="Ordnen nach">
        <option value="gruppe">nach Familie</option><option value="az">A–Z</option>
        <option value="lebensraum">nach Lebensraum</option><option value="haeufig">nach Häufigkeit</option>
      </select></label>
    <div class="chips" id="chips">${chipsHTML()}</div>
  </div>
  <div id="reg">${registerHTML()}</div>
  <footer class="foot">
    <h2>Hören lernen</h2>
    <p>Jede Aufnahme steht neben ihrem <b>Stimmbild</b> (Sonagramm): links nach rechts die Zeit, unten nach oben die Tonhöhe. So sieht man, ob ein Vogel Motive wiederholt, trillert oder flötet – und erkennt die Form wieder.</p>
    <p><b>Gesang</b> ist die Reviermelodie (meist Männchen, vor allem im Frühjahr). <b>Rufe</b> sind kurze Alltagslaute – Kontakt, Warnung, Flug – und das ganze Jahr zu hören.</p>
    <h2 style="margin-top:18px">Für unterwegs</h2>
    <p>Alle Aufnahmen auf dem Gerät speichern (etwa 40 MB), damit Vogelohr auch im Wald ohne Netz funktioniert.</p>
    <button class="btn" id="offline" type="button"><svg aria-hidden="true"><use href="#i-down"/></svg>Offline speichern</button>
    <div class="offline-box" id="offbox" hidden><div class="progress"><i id="offbar"></i></div><span id="offtxt"></span></div>
    <h2 style="margin-top:22px">Quellen</h2>
    <p>Aufnahmen und Fotos stammen von <a href="https://commons.wikimedia.org" target="_blank" rel="noopener">Wikimedia Commons</a>, viele davon ursprünglich von <a href="https://xeno-canto.org" target="_blank" rel="noopener">xeno-canto</a>; Urheber und Lizenz stehen bei jedem Vogel. Die Aufnahmen wurden gekürzt und in der Lautstärke angeglichen. Monatsangaben sind Richtwerte für Mitteleuropa.</p>
  </footer>`;
};
AFTER.lexikon = () => {
  $("#sort").value = LX.sort;
  $("#q").addEventListener("input", e => { LX.q = e.target.value.trim(); $("#reg").innerHTML = registerHTML(); frame(); });
  $("#sort").addEventListener("change", e => { LX.sort = e.target.value; $("#reg").innerHTML = registerHTML(); frame(); });
  $("#chips").addEventListener("click", e => {
    const c = e.target.closest("[data-chip]"); if (!c) return;
    LX.chip = LX.chip === c.dataset.chip && c.dataset.chip !== "alle" ? "alle" : c.dataset.chip;
    $("#chips").innerHTML = chipsHTML(); $("#reg").innerHTML = registerHTML(); frame();
  });
  $("#offline").addEventListener("click", saveOffline);
};

/* ================================================================ Detail */
const sheet = $("#sheet");
let sheetBird = null, sheetIdx = 0;
function openSheet(html){
  $("#sheetBody").innerHTML = html;
  if (!sheet.open){ sheet.showModal(); document.documentElement.style.overflow = "hidden"; }
  $("#sheetBody").scrollTop = 0;
  syncButtons(); frame();
  requestAnimationFrame(() => layoutTracks($("#sheetBody")));
}
function closeSheet(){
  if (!sheet.open) return;
  sheet.close(); document.documentElement.style.overflow = "";
}
$("#sheetBody").addEventListener("scroll", e => { const bar = $("#dbar"); const hero = $(".d-hero"); if (bar && hero) bar.classList.toggle("solid", e.target.scrollTop > hero.offsetHeight - 70); }, { passive:true });
sheet.addEventListener("cancel", e => { e.preventDefault(); go(route.base); });
sheet.addEventListener("click", e => {
  if (e.target === sheet) go(route.base);
  if (e.target.closest("[data-close]")) go(route.base);
});

function monthsHTML(b){
  return `<div class="months">${M1.map((l, i) => {
    const m = i + 1; const c = b.sings.includes(m) && b.present.includes(m) ? "s" : b.present.includes(m) ? "p" : "";
    return `<span class="${c}${m === NOW ? " cur" : ""}" title="${MONTHS[i]}">${l}</span>`;
  }).join("")}</div>
  <div class="legend"><span><i style="background:var(--accent)"></i>singt</span><span><i style="background:var(--accent-soft)"></i>da, ruft</span><span><i style="background:var(--sunk)"></i>nicht hier</span></div>`;
}
function credit(o){ return [o?.artist && `© ${esc(o.artist)}`, o?.license && esc(o.license)].filter(Boolean).join(", "); }
function listenHTML(b, idx){
  const cl = clipsOf(b);
  if (!cl.length) return `<div class="listen"><p class="clip-credit">Für diese Art ist noch keine Aufnahme hinterlegt. <a href="https://xeno-canto.org/explore?query=${encodeURIComponent(b.lat)}" target="_blank" rel="noopener">Aufnahmen auf xeno-canto</a></p></div>`;
  const c = cl[idx] || cl[0];
  const khz = [c.fmax, (c.fmax + c.fmin) / 2, c.fmin].map(v => (v / 1000).toFixed(v % 1000 ? 1 : 0).replace(".", ","));
  return `<div class="listen" id="listen">
    ${cl.length > 1 ? `<div class="seg" role="group" aria-label="Aufnahme wählen">${cl.map((x, i) => `<button type="button" data-clip="${i}" aria-pressed="${i === idx}">${KIND[x.kind] || "Aufnahme " + (i + 1)}</button>`).join("")}</div>` : ""}
    ${onoNowHTML(b, idx)}
    <div class="big-spec"><div class="spec-wrap"><div class="khz" aria-hidden="true"><span>${khz[0]}</span><span>${khz[1]}</span><span>${khz[2]} kHz</span></div>
      ${specHTML(b, idx)}</div>
      ${onoTrackHTML(b, idx)}
      <div class="tline" aria-hidden="true"><span>0 s</span><span>${Math.round(c.dur / 2)} s</span><span>${Math.round(c.dur)} s</span></div></div>
    <div class="ctrl">${playBtn(b, idx, "big")}
      <span class="grow"></span>
      <button class="btn" type="button" id="slow" aria-pressed="${A.rate < 1}"><svg aria-hidden="true"><use href="#i-slow"/></svg>Zeitlupe</button>
      <button class="btn" type="button" id="loop" aria-pressed="${A.loop}"><svg aria-hidden="true"><use href="#i-loop"/></svg>Schleife</button>
    </div>
    <p class="clip-credit">Aufnahme: <a href="${esc(c.page)}" target="_blank" rel="noopener">${credit(c) || "Wikimedia Commons"}</a></p>
  </div>`;
}
function openDetail(b, idx = 0){
  sheetBird = b; sheetIdx = idx;
  const img = imgOf(b);
  const st = singsNow(b) ? '<span class="badge sing">♪ singt gerade</span>' : presentNow(b) ? '<span class="badge now">jetzt zu hören</span>' : `<span class="badge">im ${MONTHS[NOW-1]} nicht hier</span>`;
  const verw = (b.verw || []).map(id => BY[id]).filter(Boolean);
  openSheet(`
    <div class="d-bar" id="dbar"><button class="d-close" type="button" data-close aria-label="Schließen"><svg aria-hidden="true"><use href="#i-x"/></svg></button><span class="d-bar-name">${esc(b.de)}</span></div>
    <div class="d-hero" style="--tint:${esc(img?.tint || "")}">
      ${img ? `<img src="${esc(img.src)}" alt="${esc(b.de)}"><a class="d-credit" href="${esc(img.page)}" target="_blank" rel="noopener">Foto: ${credit(img) || "Wikimedia Commons"}</a>` : ""}
    </div>
    <article class="d-body">
      <h1 class="d-name" id="sheetTitle">${esc(b.de)}</h1>
      <div class="d-lat lat">${esc(b.lat)}</div>
      ${b.alias ? `<div class="d-alias">auch: ${b.alias.map(esc).join(", ")}</div>` : ""}
      <div class="d-badges">${st}<span class="badge">${FREQ[b.freq]}</span>${b.reg ? `<span class="badge">${esc(b.reg)}</span>` : ""}${b.night ? '<span class="badge"><svg><use href="#i-moon"/></svg>auch nachts</span>' : ""}<span class="badge">${esc(b.grp)}</span></div>
      <div id="listenWrap">${listenHTML(b, idx)}</div>
      <p class="laut">${esc(b.laut)}</p>
      <section class="sec"><h2>Gesang</h2><p>${esc(b.gesang)}</p></section>
      <section class="sec"><h2>Rufe</h2><p>${esc(b.ruf)}</p></section>
      <section class="sec merk"><h2>Merkhilfe</h2><p>${esc(b.merk)}</p></section>
      ${verw.length ? `<section class="sec"><h2>Leicht zu verwechseln mit</h2><div class="verw">${verw.map(v => `
        <a class="verw-item" href="#/vergleich/${b.id}/${v.id}">${photoHTML(v)}<span><b>${esc(v.de)}</b><small>${esc(v.laut)}</small></span><svg style="width:22px;height:22px;color:var(--accent)" aria-label="Vergleichen"><use href="#i-swap"/></svg></a>`).join("")}</div></section>` : ""}
      <section class="sec"><h2>Wo man ihn hört</h2><p>${esc(b.wo)}</p></section>
      <section class="sec"><h2>Wann</h2>${monthsHTML(b)}</section>
      ${b.kultur ? `<section class="sec kultur"><h2>In Liedern & Geschichten</h2><p>${esc(b.kultur)}</p></section>` : ""}
      <section class="sec"><h2>Gut zu wissen</h2><p>${esc(b.fakt)}</p></section>
      <div class="d-actions">
        <button class="btn ${isHeard(b.id) ? "accent" : ""}" type="button" id="heard" aria-pressed="${isHeard(b.id)}"><svg aria-hidden="true"><use href="#i-check"/></svg>${isHeard(b.id) ? `Gehört am ${new Date(heard[b.id]).toLocaleDateString("de-DE")}` : "Hab ich gehört"}</button>
        <button class="btn" type="button" id="share"><svg aria-hidden="true"><use href="#i-share"/></svg>Teilen</button>
      </div>
      <p class="ext">Mehr Aufnahmen: <a href="https://xeno-canto.org/explore?query=${encodeURIComponent(b.lat)}" target="_blank" rel="noopener">xeno-canto</a></p>
    </article>`);
  wireListen(b);
  $("#heard").onclick = () => { toggleHeard(b.id); openDetail(b, sheetIdx); toast(isHeard(b.id) ? `${b.de} ins Logbuch eingetragen.` : `${b.de} aus dem Logbuch entfernt.`); refreshRegister(); };
  $("#share").onclick = async () => {
    const url = location.href.split("#")[0] + `#/vogel/${b.id}`;
    try { if (navigator.share) await navigator.share({ title:`${b.de} – Vogelohr`, text:b.laut, url }); else { await navigator.clipboard.writeText(url); toast("Link kopiert."); } } catch {}
  };
}
function wireListen(b){
  const w = $("#listenWrap"); if (!w) return;
  w.onclick = e => {
    const c = e.target.closest("[data-clip]");
    if (c){ sheetIdx = +c.dataset.clip; w.innerHTML = listenHTML(b, sheetIdx); layoutTracks(w); syncButtons(); frame(); play(b, sheetIdx); return; }
    if (e.target.closest("#slow")){ A.rate = A.rate < 1 ? 1 : 0.5; audio.playbackRate = A.rate; e.target.closest("#slow").setAttribute("aria-pressed", A.rate < 1); toast(A.rate < 1 ? "Zeitlupe: halbe Geschwindigkeit, gleiche Tonhöhe." : "Normale Geschwindigkeit."); }
    if (e.target.closest("#loop")){ A.loop = !A.loop; audio.loop = A.loop; e.target.closest("#loop").setAttribute("aria-pressed", A.loop); }
  };
}
function refreshRegister(){ if (route.view === "lexikon" && $("#reg")){ $("#reg").innerHTML = registerHTML(); $("#chips").innerHTML = chipsHTML(); frame(); } }

function openCompare(a, b){
  const item = x => `<div class="cmp-item"><div class="cmp-head">${photoHTML(x)}<a href="#/vogel/${x.id}" style="color:inherit;text-decoration:none"><b>${esc(x.de)}</b></a>${playBtn(x, 0)}</div>
    ${specHTML(x, 0)}${onoTrackHTML(x, 0)}<p class="cmp-laut">${esc(x.laut)}</p></div>`;
  openSheet(`<div class="d-bar solid" id="dbar"><button class="d-close" type="button" data-close aria-label="Schließen"><svg aria-hidden="true"><use href="#i-x"/></svg></button><span class="d-bar-name">Hörvergleich</span></div>
    <article class="d-body" style="margin-top:0;padding-top:calc(var(--safe-t) + 70px)">
      <h1 class="d-name" id="sheetTitle" style="font-size:clamp(30px,7vw,44px)">${esc(a.de)} oder ${esc(b.de)}?</h1>
      <p class="page-lead" style="margin-top:8px">Hör abwechselnd hin und vergleiche die Stimmbilder: Wo liegen die Töne, wie lang sind die Silben, wiederholt sich etwas?</p>
      <div class="cmp">${item(a)}${item(b)}</div>
      <div class="sec merk"><h2>Merkhilfen</h2><p><b>${esc(a.de)}:</b> ${esc(a.merk)}<br><b>${esc(b.de)}:</b> ${esc(b.merk)}</p></div>
      <div class="d-actions"><button class="btn primary" type="button" id="abplay"><svg aria-hidden="true"><use href="#i-swap"/></svg>Abwechselnd abspielen</button></div>
    </article>`);
  $("#abplay").onclick = async () => {
    if (!clipsOf(a).length || !clipsOf(b).length) return;
    for (const x of [a, b]){
      await play(x, 0);
      await new Promise(res => { const t = setTimeout(res, 8000); audio.addEventListener("pause", () => { clearTimeout(t); res(); }, { once:true }); });
      if (!sheet.open) return;
      audio.pause();
    }
  };
}

/* ================================================================ Bestimmen */
const BS = { hab:new Set(), snd:new Set(), night:false };
let micState = null;
function bestScore(b){
  if (!presentNow(b)) return -99;
  let s = (4 - b.freq) * 0.8;
  if (BS.hab.size){ const hit = b.hab.filter(h => BS.hab.has(h)).length; s += hit ? 2 + hit : -3; }
  if (BS.snd.size){ const hit = b.snd.filter(x => BS.snd.has(x)).length; s += hit ? 4 * hit : -6; }
  if (BS.night) s += b.night ? 5 : (["rotkehlchen","kranich","singdrossel","stockente","blaesshuhn","teichhuhn","graugans"].includes(b.id) ? 0 : -8);
  else if (b.night && !["kuckuck"].includes(b.id)) s -= 1.5;
  if (singsNow(b) && BS.snd.size && !BS.snd.has("kraechz")) s += 1;
  return s;
}
function bestResults(){
  const ranked = BIRDS.map(b => [b, bestScore(b)]).filter(x => x[1] > -1).sort((a, b) => b[1] - a[1]);
  return ranked.slice(0, BS.hab.size || BS.snd.size || BS.night ? 12 : 8).map(x => x[0]);
}
function bestResultsHTML(){
  const r = bestResults();
  const any = BS.hab.size || BS.snd.size || BS.night;
  return `<div class="result-h"><h2>${any ? "Am ehesten" : "Häufig im " + MONTHS[NOW-1]}</h2><small>${r.length} Vorschläge</small></div>
    <div class="register" style="--x:1">${r.map(rowHTML).join("") || '<p class="empty">Nichts gefunden – nimm eine Angabe weg.</p>'}</div>`;
}
VIEWS.bestimmen = () => `
  <h1 class="page-title">Was singt da?</h1>
  <p class="page-lead">Beschreib, was du hörst – Vogelohr schlägt passende Arten vor, die im ${MONTHS[NOW-1]} da sind. Dann vergleichst du Stimme und Stimmbild.</p>
  <div class="step"><h2>Wo bist du?</h2><div class="chips" id="bsHab">${Object.entries(HAB).map(([k, v]) => `<button class="chip" type="button" data-h="${k}" aria-pressed="${BS.hab.has(k)}">${v.label}</button>`).join("")}
    <button class="chip" type="button" id="bsNight" aria-pressed="${BS.night}"><svg aria-hidden="true"><use href="#i-moon"/></svg>Es ist Nacht</button></div></div>
  <div class="step"><h2>Wie klingt es?</h2><div class="shapes" id="bsSnd">${Object.entries(SHAPES).map(([k, v]) => `<button class="shape" type="button" data-s="${k}" aria-pressed="${BS.snd.has(k)}">${shapeSVG(k)}<span>${v.label}</span></button>`).join("")}</div></div>
  <div id="bsRes">${bestResultsHTML()}</div>
  <section class="step">
    <div class="mirror">
      <h2>Stimmbild-Spiegel</h2>
      <p>Halte das Handy Richtung Vogel: Vogelohr zeichnet live das Stimmbild dessen, was das Mikrofon hört. Vergleiche die Form mit den Vorschlägen oben. Die Aufnahme bleibt auf deinem Gerät.</p>
      <canvas id="mic" width="900" height="300" aria-label="Live-Stimmbild des Mikrofons"></canvas>
      <div class="ctrl"><button class="btn accent" type="button" id="micBtn"><svg aria-hidden="true"><use href="#i-mic"/></svg>Zuhören</button>
        <button class="btn" type="button" id="micPlay" hidden><svg aria-hidden="true"><use href="#i-play"/></svg>Aufnahme anhören</button></div>
      <p class="note" id="micNote">Stoppt automatisch nach 20 Sekunden.</p>
    </div>
  </section>
  <section class="step"><h2>Automatisch erkennen lassen</h2>
    <p class="page-lead" style="margin-bottom:6px">Für die vollautomatische Erkennung gibt es zwei hervorragende, kostenlose Apps. Tipp zum Lernen: erst selbst raten, dann prüfen – und den Vogel hier nachschlagen.</p>
    <div class="apps">
      <div class="app-card"><b>Merlin Bird ID</b><p>Vom Cornell Lab of Ornithology. „Sound ID“ hört live mit und zeigt laufend, wer gerade singt.</p><a class="btn" href="https://merlin.allaboutbirds.org/" target="_blank" rel="noopener">Zu Merlin</a></div>
      <div class="app-card"><b>BirdNET</b><p>Von Cornell und TU Chemnitz. Aufnahme machen, Abschnitt wählen, Vorschlag mit Wahrscheinlichkeit erhalten.</p><a class="btn" href="https://birdnet.cornell.edu/" target="_blank" rel="noopener">Zu BirdNET</a></div>
    </div>
  </section>`;
AFTER.bestimmen = () => {
  const upd = () => { $("#bsRes").innerHTML = bestResultsHTML(); syncButtons(); frame(); };
  $("#bsHab").onclick = e => {
    const c = e.target.closest("[data-h]");
    if (c){ const k = c.dataset.h; BS.hab.has(k) ? BS.hab.delete(k) : BS.hab.add(k); c.setAttribute("aria-pressed", BS.hab.has(k)); upd(); }
    if (e.target.closest("#bsNight")){ BS.night = !BS.night; $("#bsNight").setAttribute("aria-pressed", BS.night); upd(); }
  };
  $("#bsSnd").onclick = e => {
    const c = e.target.closest("[data-s]"); if (!c) return;
    const k = c.dataset.s; BS.snd.has(k) ? BS.snd.delete(k) : BS.snd.add(k); c.setAttribute("aria-pressed", BS.snd.has(k)); upd();
  };
  $("#micBtn").onclick = () => micState ? micStop() : micStart();
  $("#micPlay").onclick = () => { if (micState?.url || micUrl){ audio.pause(); const a = new Audio(micUrl); a.play(); } };
  drawMicIdle();
};
let micUrl = null;
function cssVar(n){ return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); }
function drawMicIdle(){
  const cv = $("#mic"); if (!cv) return;
  const g = cv.getContext("2d"); g.clearRect(0, 0, cv.width, cv.height);
  g.fillStyle = "rgba(255,255,255,.08)";
  for (let k = 1; k < 5; k++) g.fillRect(0, cv.height * k / 5, cv.width, 1);
}
async function micStart(){
  if (!navigator.mediaDevices?.getUserMedia){ toast("Dieses Gerät erlaubt hier keinen Mikrofonzugriff."); return; }
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  try { ctx.resume(); } catch {}
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio:{ echoCancellation:false, noiseSuppression:false, autoGainControl:false } });
    audio.pause();
    const src = ctx.createMediaStreamSource(stream);
    const an = ctx.createAnalyser(); an.fftSize = 1024; an.smoothingTimeConstant = 0; an.minDecibels = -95; an.maxDecibels = -25;
    src.connect(an);
    let rec = null, chunks = [];
    try { rec = new MediaRecorder(stream); rec.ondataavailable = e => chunks.push(e.data); rec.onstop = () => { if (micUrl) URL.revokeObjectURL(micUrl); micUrl = URL.createObjectURL(new Blob(chunks, { type:rec.mimeType })); $("#micPlay") && ($("#micPlay").hidden = false); }; rec.start(); } catch {}
    micState = { stream, ctx, an, rec, t0:performance.now(), raf:0 };
    $("#micBtn").innerHTML = `<svg aria-hidden="true"><use href="#i-pause"/></svg>Stopp`;
    $("#micNote").textContent = "Hört zu …";
    const cv = $("#mic"), g = cv.getContext("2d");
    const data = new Uint8Array(an.frequencyBinCount);
    const nyq = ctx.sampleRate / 2, fmax = 11000, bins = Math.floor(an.frequencyBinCount * fmax / nyq);
    g.clearRect(0, 0, cv.width, cv.height);
    const step = 3;
    const loop = () => {
      if (!micState) return;
      an.getByteFrequencyData(data);
      g.drawImage(cv, -step, 0);
      g.clearRect(cv.width - step, 0, step, cv.height);
      for (let y = 0; y < cv.height; y++){
        const bin = Math.floor((1 - y / cv.height) * bins);
        const v = data[bin] / 255;
        if (v < 0.18) continue;
        const a = Math.min(1, (v - 0.18) / 0.6);
        g.fillStyle = a > .75 ? `rgba(245,200,66,${a})` : `rgba(230,240,242,${a})`;
        g.fillRect(cv.width - step, y, step, 1);
      }
      if (performance.now() - micState.t0 > 20000){ micStop(); return; }
      micState.raf = requestAnimationFrame(loop);
    };
    loop();
  } catch (e) {
    try { ctx.close(); } catch {}
    toast("Kein Zugriff aufs Mikrofon – bitte in den Einstellungen erlauben.");
  }
}
function micStop(){
  if (!micState) return;
  cancelAnimationFrame(micState.raf);
  try { micState.rec && micState.rec.state !== "inactive" && micState.rec.stop(); } catch {}
  micState.stream.getTracks().forEach(t => t.stop());
  micState.ctx.close();
  micState = null;
  if ($("#micBtn")){ $("#micBtn").innerHTML = `<svg aria-hidden="true"><use href="#i-mic"/></svg>Noch einmal zuhören`; $("#micNote").textContent = "Gestoppt. Das Stimmbild bleibt stehen – vergleiche es mit den Vorschlägen."; }
}

/* ================================================================ Üben */
const Q = { mode:"alle", cur:null, opts:[], idx:0, done:false, round:0, ok:0, streak:0 };
const MODES = [["alle","Alle"],["jetzt",`Im ${MONTHS[NOW-1]}`],["haeufig","Die Häufigsten"],["paare","Verwechslungspaare"],["gehoert","Meine gehörten"]];
function qPool(){
  let p = BIRDS.filter(b => clipsOf(b).length);
  if (Q.mode === "jetzt") p = p.filter(presentNow);
  if (Q.mode === "haeufig") p = p.filter(b => b.freq <= 2);
  if (Q.mode === "paare") p = p.filter(b => (b.verw || []).some(v => clipsOf(BY[v]).length));
  if (Q.mode === "gehoert") p = p.filter(b => isHeard(b.id));
  return p.length >= 4 ? p : BIRDS.filter(b => clipsOf(b).length);
}
const boxOf = id => train[id]?.box || 0;
function qPick(){
  const pool = qPool();
  const w = pool.map(b => (b.id === Q.cur?.id ? 0 : 5 - boxOf(b.id)) * (Q.mode === "alle" ? (5 - b.freq) : 1));
  let r = Math.random() * w.reduce((a, b) => a + b, 0);
  for (let i = 0; i < pool.length; i++){ r -= w[i]; if (r <= 0) return pool[i]; }
  return pool[0];
}
const shuffle = a => { for (let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
function qNext(){
  const b = qPick();
  Q.cur = b; Q.done = false; Q.idx = Math.floor(Math.random() * clipsOf(b).length);
  const verw = shuffle((b.verw || []).map(id => BY[id]).filter(x => x && x.id !== b.id));
  let others = Q.mode === "paare" ? verw.slice(0, 3) : verw.slice(0, 1);
  const rest = shuffle(BIRDS.filter(x => x.id !== b.id && !others.includes(x)));
  while (others.length < 3) others.push(rest.pop());
  Q.opts = shuffle([b, ...others]);
  $("#quiz").innerHTML = qHTML();
  play(b, Q.idx);
}
function qHTML(){
  const b = Q.cur;
  if (!b) return "";
  const pool = qPool();
  const sure = pool.filter(x => boxOf(x.id) >= 3).length;
  return `<div class="q-card">
    <div class="q-top">${playBtn(b, Q.idx, "big")}<div><h2>Wer ist das?</h2><p>Tippe aufs Stimmbild, um an eine Stelle zu springen.</p></div></div>
    ${specHTML(b, Q.idx)}
    <div class="q-opts">${Q.opts.map(o => `<button class="q-opt${Q.done ? (o.id === b.id ? " right" : o.id === Q.picked ? " wrong" : "") : ""}" type="button" data-ans="${o.id}" ${Q.done ? "disabled" : ""}>${photoHTML(o)}<span>${esc(o.de)}</span></button>`).join("")}</div>
    ${Q.done ? `<div class="q-fb">${Q.picked === b.id ? "<b>Richtig.</b>" : `<b>Das war ${esc(b.de)}.</b>`} <i>${esc(b.merk)}</i></div>
      <div class="ctrl q-next"><button class="btn primary" type="button" id="qNext">Nächster Vogel</button><a class="btn" href="#/vogel/${b.id}">Mehr über ${esc(b.de)}</a></div>` : ""}
    <div class="stats"><span><b>${Q.ok}/${Q.round}</b>richtig</span><span><b>${Q.streak}</b>in Folge</span><span><b>${sure}/${pool.length}</b>sicher erkannt</span></div>
    <div class="boxes" title="Lernstand: je dunkler, desto sicherer">${pool.map(x => `<i class="b${Math.min(4, boxOf(x.id))}"></i>`).join("")}</div>
  </div>`;
}
VIEWS.ueben = () => `
  <div class="quiz">
    <h1 class="page-title">Ohr-Training</h1>
    <p class="page-lead">Hör zu und tippe auf den richtigen Vogel. Vogelohr merkt sich, welche Stimmen dir noch schwerfallen, und spielt sie öfter.</p>
    <div class="chips" id="qModes">${MODES.map(([k, l]) => `<button class="chip" type="button" data-m="${k}" aria-pressed="${Q.mode === k}">${l}</button>`).join("")}</div>
    <div id="quiz">${Q.cur ? qHTML() : `<div class="q-card"><div class="q-top"><button class="play-b big" type="button" id="qStart" aria-label="Training starten"><svg aria-hidden="true"><use href="#i-play"/></svg></button><div><h2>Bereit?</h2><p>Ton an, dann los.</p></div></div></div>`}</div>
  </div>`;
AFTER.ueben = () => {
  $("#qModes").onclick = e => {
    const c = e.target.closest("[data-m]"); if (!c) return;
    Q.mode = c.dataset.m; $$("#qModes .chip").forEach(x => x.setAttribute("aria-pressed", x.dataset.m === Q.mode)); qNext();
  };
  $("#quiz").onclick = e => {
    if (e.target.closest("#qStart")) { qNext(); return; }
    if (e.target.closest("#qNext")) { qNext(); return; }
    const a = e.target.closest("[data-ans]");
    if (a && !Q.done){
      Q.done = true; Q.picked = a.dataset.ans; Q.round++;
      const t = train[Q.cur.id] || { box:0, n:0 };
      t.n++;
      if (Q.picked === Q.cur.id){ Q.ok++; Q.streak++; t.box = Math.min(4, t.box + 1); }
      else { Q.streak = 0; t.box = 0; const w = train[Q.picked] || { box:0, n:0 }; w.box = Math.max(0, w.box - 1); train[Q.picked] = w; }
      train[Q.cur.id] = t; store.set("vo-train", train);
      $("#quiz").innerHTML = qHTML(); syncButtons(); frame();
    }
  };
};

/* ================================================================ Kinder */
let kidActive = null;
const KID_ORDER = ["kuckuck","haushuhn","stockente","waldkauz","uhu","graugans","rabenkraehe","haussperling","buntspecht","weissstorch","amsel","kohlmeise","rotkehlchen","strassentaube","ringeltaube","silbermoewe","elster","kolkrabe","zaunkoenig","hoeckerschwan","pfau","kranich","nachtigall","feldlerche","rauchschwalbe","eisvogel","wiedehopf","maeusebussard","steinadler","gruenspecht","kiebitz","stieglitz","blaumeise","buchfink","zilpzalp","mauersegler"];
function kidBirds(){ const k = BIRDS.filter(b => b.kid); return k.sort((a, b) => (KID_ORDER.indexOf(a.id) + 1 || 99) - (KID_ORDER.indexOf(b.id) + 1 || 99)); }
VIEWS.kinder = () => `
  <div class="kids">
    <h1 class="page-title">Wie macht der Vogel?</h1>
    <p class="page-lead">Tippe auf einen Vogel und hör, wie er klingt.</p>
    <div class="kids-grid" id="kids">${kidBirds().map(b => `<button class="kid" type="button" data-kid="${b.id}" aria-label="${esc(b.de)} anhören">
      <span class="kid-ph" style="--tint:${esc(imgOf(b)?.tint || "")}">${thumb(b) ? `<img src="${esc(thumb(b))}" alt="" loading="lazy">` : ""}</span><b>${esc(b.de.replace(/^Haus(huhn)$/, "Hahn & Huhn"))}</b></button>`).join("")}</div>
    <h2 class="group-h" style="margin-top:30px">Aus Liedern und Märchen</h2>
    <div class="stories">${BIRDS.filter(b => b.kultur).map(b => `<a class="story" href="#/vogel/${b.id}"><b>${esc(b.de)}</b><p>${esc(b.kultur)}</p></a>`).join("")}</div>
  </div>`;
AFTER.kinder = () => {
  $("#kids").onclick = e => {
    const k = e.target.closest("[data-kid]"); if (!k) return;
    const b = BY[k.dataset.kid];
    if (kidActive === b.id && !audio.paused){ audio.pause(); return; }
    kidActive = b.id;
    $("#kidSay").innerHTML = `${onoNowHTML(b, 0, "kidword") || `<b>${esc(b.kid[0])}</b>`}<span>${esc(b.kid[1])}</span>`;
    $("#kidSay").hidden = false;
    play(b, 0);
  };
};
function kidSync(playing){
  $$(".kid").forEach(k => k.classList.toggle("on", playing && k.dataset.kid === kidActive && A.bird?.id === kidActive));
  const done = () => audio.ended || (audio.paused && audio.currentTime > 0.3);
  if (!playing && done() && $("#kidSay")) setTimeout(() => { if (done() && $("#kidSay")) $("#kidSay").hidden = true; }, 1800);
}
function kidStop(){ kidActive = null; const k = $("#kidSay"); if (k) k.hidden = true; }

/* ================================================================ Morgenchor */
const CITIES = [["München",48.137,11.575],["Berlin",52.52,13.405],["Hamburg",53.55,9.99],["Köln",50.94,6.96],["Frankfurt",50.11,8.68],["Stuttgart",48.78,9.18],["Leipzig",51.34,12.37],["Nürnberg",49.45,11.08],["Wien",48.21,16.37],["Graz",47.07,15.44],["Salzburg",47.81,13.04],["Innsbruck",47.27,11.39],["Zürich",47.37,8.54],["Bern",46.95,7.45],["Basel",47.56,7.59]];
let dawnCity = store.get("vo-city", 0);
function sunrise(date, lat, lng){
  const r = Math.PI / 180;
  const jd0 = Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), 12) / 864e5 + 2440587.5;
  const n = Math.round(jd0 - 2451545.0 + 0.0008);
  const Js = n - lng / 360;
  const M = (357.5291 + 0.98560028 * Js) % 360;
  const C = 1.9148 * Math.sin(M * r) + 0.02 * Math.sin(2 * M * r) + 0.0003 * Math.sin(3 * M * r);
  const L = (M + C + 180 + 102.9372) % 360;
  const Jt = 2451545.0 + Js + 0.0053 * Math.sin(M * r) - 0.0069 * Math.sin(2 * L * r);
  const sd = Math.sin(L * r) * Math.sin(23.4397 * r);
  const cd = Math.cos(Math.asin(sd));
  const cw = (Math.sin(-0.833 * r) - Math.sin(lat * r) * sd) / (Math.cos(lat * r) * cd);
  if (cw < -1 || cw > 1) return null;
  const w = Math.acos(cw) / r;
  return new Date((Jt - w / 360 - 2440587.5) * 864e5);
}
const hm = d => d.toLocaleTimeString("de-DE", { hour:"2-digit", minute:"2-digit" });
function dawnData(){
  const [name, lat, lng] = CITIES[dawnCity] || CITIES[0];
  const tm = new Date(); tm.setDate(tm.getDate() + 1);
  const sr = sunrise(tm, lat, lng);
  const birds = BIRDS.filter(b => b.dawn).sort((a, b) => b.dawn - a.dawn);
  return { name, sr, birds };
}
VIEWS.morgen = () => {
  const { sr, birds } = dawnData();
  return `
  <section class="dawn-sky">
    <h1>Wer weckt dich morgen?</h1>
    <p>Vögel beginnen in einer recht festen Reihenfolge zu singen – gemessen am Sonnenaufgang. Diese „Vogeluhr“ gilt vor allem im Frühjahr; die Zeiten sind Richtwerte.</p>
    <div class="dawn-controls">
      <select id="city" aria-label="Ort">${CITIES.map((c, i) => `<option value="${i}" ${i === dawnCity ? "selected" : ""}>${c[0]}</option>`).join("")}</select>
      <button class="btn accent" type="button" id="chorus"><svg aria-hidden="true"><use href="#i-play"/></svg>Morgenchor im Zeitraffer</button>
    </div>
    <div class="sunrise">Sonnenaufgang morgen: ${sr ? hm(sr) : "–"} Uhr</div>
  </section>
  <div class="timeline" id="tl">
    ${birds.map(b => {
      const t = sr ? new Date(sr.getTime() - b.dawn * 60000) : null;
      const now = singsNow(b);
      return `<div class="t-item${now ? "" : " off"}" data-t="${b.id}"><span class="t-time">${t ? hm(t) : ""}</span><span class="t-dot"></span>
        ${photoHTML(b)}<a href="#/vogel/${b.id}" style="color:inherit;text-decoration:none;min-width:0"><b>${esc(b.de)}</b><small>${b.dawn} Minuten vorher${now ? "" : `, singt im ${MONTHS[NOW-1]} kaum`}</small></a>${specHTML(b, 0)}</div>`;
    }).join("")}
    <div class="t-item t-sun"><span class="t-time">${sr ? hm(sr) : ""}</span><span class="t-dot" style="border-color:var(--gold);background:var(--gold)"></span>Sonnenaufgang</div>
  </div>
  <p class="foot" style="border:0;margin-top:10px">Der Zeitraffer legt die Stimmen nacheinander übereinander, wie sie im Frühling vor Sonnenaufgang einsetzen – mit Kopfhörern räumlich verteilt.</p>`;
};
AFTER.morgen = () => {
  $("#city").onchange = e => { dawnCity = +e.target.value; store.set("vo-city", dawnCity); renderView("morgen"); };
  $("#chorus").onclick = () => chorus ? stopChorus() : startChorus();
};
let chorus = null;
function startChorus(){ startChorusAsync(); }
async function startChorusAsync(){
  audio.pause();
  const { birds } = dawnData();
  const list = birds.filter(b => clipsOf(b).length);
  const Ctx = window.AudioContext || window.webkitAudioContext;
  const ctx = new Ctx();
  try { ctx.resume(); } catch {}
  chorus = { ctx, nodes:[], timers:[] };
  $("#chorus").innerHTML = `<svg aria-hidden="true"><use href="#i-pause"/></svg>Lädt …`;
  const bufs = await Promise.all(list.map(async b => {
    try { const r = await fetch(clipsOf(b)[0].src); return await ctx.decodeAudioData(await r.arrayBuffer()); } catch { return null; }
  }));
  if (!chorus || chorus.ctx !== ctx) return;
  $("#chorus").innerHTML = `<svg aria-hidden="true"><use href="#i-pause"/></svg>Anhalten`;
  const master = ctx.createGain(); master.gain.value = 0.9; master.connect(ctx.destination);
  const t0 = ctx.currentTime + 0.3, gap = 2.6;
  list.forEach((b, i) => {
    const buf = bufs[i]; if (!buf) return;
    const s = ctx.createBufferSource(); s.buffer = buf;
    const g = ctx.createGain();
    const p = ctx.createStereoPanner ? ctx.createStereoPanner() : null;
    const at = t0 + i * gap;
    g.gain.setValueAtTime(0, at); g.gain.linearRampToValueAtTime(0.5, at + 0.6);
    g.gain.setValueAtTime(0.5, at + buf.duration - 1.2); g.gain.linearRampToValueAtTime(0, at + buf.duration);
    if (p){ p.pan.value = ((i * 0.618) % 1) * 1.4 - 0.7; s.connect(g).connect(p).connect(master); } else s.connect(g).connect(master);
    s.start(at); chorus.nodes.push(s);
    chorus.timers.push(setTimeout(() => { const el = $(`[data-t="${b.id}"]`); el?.classList.add("on"); el?.scrollIntoView({ block:"center", behavior:"smooth" }); }, (at - ctx.currentTime) * 1000));
  });
  const end = (list.length - 1) * gap + 24;
  chorus.timers.push(setTimeout(stopChorus, end * 1000));
}
function stopChorus(){
  if (!chorus) return;
  chorus.timers.forEach(clearTimeout);
  chorus.nodes.forEach(n => { try { n.stop(); } catch {} });
  chorus.ctx.close();
  chorus = null;
  $$(".t-item.on").forEach(e => e.classList.remove("on"));
  if ($("#chorus")) $("#chorus").innerHTML = `<svg aria-hidden="true"><use href="#i-play"/></svg>Morgenchor im Zeitraffer`;
}

/* ================================================================ Offline */
async function saveOffline(){
  if (!("caches" in window)){ toast("Dieser Browser kann nichts offline speichern."); return; }
  const urls = [];
  BIRDS.forEach(b => { clipsOf(b).forEach(c => urls.push(c.src, c.spec)); const i = imgOf(b); if (i) urls.push(i.thumb, i.src); });
  $("#offbox").hidden = false;
  const cache = await caches.open("vogelohr-media-v1");
  let done = 0, fail = 0;
  const q = urls.slice();
  const worker = async () => { while (q.length){ const u = q.shift(); try { if (!(await cache.match(u))) await cache.add(u); } catch { fail++; } done++; $("#offbar").style.width = (done / urls.length * 100) + "%"; $("#offtxt").textContent = `${done} von ${urls.length} Dateien`; } };
  await Promise.all([1,2,3,4].map(worker));
  $("#offtxt").textContent = fail ? `Fertig – ${fail} Dateien fehlen noch. Später erneut versuchen.` : "Fertig. Vogelohr funktioniert jetzt auch ohne Netz.";
}

/* ================================================================ Start */
window.addEventListener("scroll", () => { $("#top").classList.toggle("scrolled", scrollY > 4); const f = $(".finder"); if (f) f.classList.toggle("stuck", f.getBoundingClientRect().top <= parseFloat(getComputedStyle(f).top) + 1 && scrollY > 200); }, { passive:true });
fetch("media.json").then(r => r.ok ? r.json() : {}).catch(() => ({})).then(m => { MEDIA = m || {}; onRoute(); });
if ("serviceWorker" in navigator && location.protocol === "https:") navigator.serviceWorker.register("sw.js").catch(() => {});
})();
