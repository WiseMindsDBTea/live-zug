(() => {
"use strict";
const BIRDS = window.BIRDS, HAB = window.HABITATS;
const MONTHS = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"];
const M1 = ["J","F","M","A","M","J","J","A","S","O","N","D"];
const NOW = new Date().getMonth() + 1;
const CACHE_KEY = "vsm-meta-v3";
const CACHE_TTL = 14 * 864e5;
const COMMONS = "https://commons.wikimedia.org/w/api.php";
// Synonyme, unter denen Wikidata die Art führen könnte
const SYN = {
  "Coloeus monedula":["Corvus monedula"], "Chloris chloris":["Carduelis chloris"],
  "Cyanistes caeruleus":["Parus caeruleus"], "Dendrocopos major":["Picoides major"],
  "Carduelis carduelis":[], "Sylvia atricapilla":[]
};

const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const strip = html => { const d = document.createElement("div"); d.innerHTML = html || ""; return (d.textContent || "").replace(/\s+/g," ").trim(); };
const store = {
  get(k){ try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
  set(k,v){ try { localStorage.setItem(k, JSON.stringify(v)); } catch {} }
};

// meta[id] = { audio:[fileInfo], image:fileInfo }
let meta = {};
const searchCache = {};

/* ---------- Status pro Monat ---------- */
function stateOf(b, m = NOW){
  if (!b.present.includes(m)) return "away";
  return b.sings.includes(m) ? "sing" : "call";
}
const BADGE = {
  sing:'<span class="badge b-sing">♪ singt jetzt</span>',
  call:'<span class="badge b-call">· Rufe zu hören</span>',
  away:'<span class="badge b-away">derzeit nicht hier</span>'
};

/* ---------- Kopfzeile ---------- */
function renderNow(){
  const present = BIRDS.filter(b => stateOf(b) !== "away").length;
  const sing = BIRDS.filter(b => stateOf(b) === "sing").length;
  $("#now").innerHTML =
    `<span class="pill">Im <b>${MONTHS[NOW-1]}</b> zu hören: <b>${present}</b> von ${BIRDS.length}</span>` +
    `<span class="pill">davon singend: <b>${sing}</b></span>`;
}

/* ---------- Filter ---------- */
let filter = "all", query = "";
function renderChips(){
  const chips = [["all","Alle"],["now","Jetzt hörbar"],...Object.entries(HAB).map(([k,v]) => [k, `${v.icon} ${v.label}`])];
  $("#chips").innerHTML = chips.map(([k,l]) => `<button class="chip" type="button" data-f="${k}" aria-pressed="${k===filter}">${l}</button>`).join("");
}
$("#chips").addEventListener("click", e => {
  const b = e.target.closest(".chip"); if (!b) return;
  filter = b.dataset.f; renderChips(); renderGrid();
});
$("#q").addEventListener("input", e => { query = e.target.value.trim().toLowerCase(); renderGrid(); });

function matches(b){
  if (filter === "now" && stateOf(b) === "away") return false;
  if (HAB[filter] && !b.hab.includes(filter)) return false;
  if (!query) return true;
  return [b.de,b.lat,b.lautbild,b.gesang,b.ruf,b.merk,b.wo].join(" ").toLowerCase().includes(query);
}

/* ---------- Karten ---------- */
const ICON_PLAY = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
const ICON_PAUSE = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>';
const ICON_LOAD = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 3a9 9 0 1 0 9 9"/></svg>';

function thumbHTML(b){
  const img = meta[b.id]?.image;
  return img?.thumb ? `<img src="${esc(img.thumb)}" alt="" loading="lazy">` : esc(b.de[0]);
}
function renderGrid(){
  const list = BIRDS.filter(matches);
  $("#empty").hidden = list.length > 0;
  $("#grid").innerHTML = list.map(b => {
    const st = stateOf(b);
    return `<article class="card${st==="away"?" absent":""}" data-id="${b.id}" tabindex="0" role="button" aria-label="${esc(b.de)} – Details">
      <div class="thumb" data-thumb="${b.id}">${thumbHTML(b)}</div>
      <div class="cbody">
        <h2 class="cname">${esc(b.de)}</h2>
        <div class="clat">${esc(b.lat)}</div>
        <p class="claut">${esc(b.lautbild)}</p>
        ${BADGE[st]}
      </div>
      <button class="play" type="button" data-play="${b.id}" aria-label="${esc(b.de)} anhören">${ICON_PLAY}</button>
    </article>`;
  }).join("");
  syncPlayButtons();
}
$("#grid").addEventListener("click", e => {
  const p = e.target.closest("[data-play]");
  if (p){ e.stopPropagation(); togglePlay(p.dataset.play); return; }
  const c = e.target.closest(".card"); if (c) openDetail(c.dataset.id);
});
$("#grid").addEventListener("keydown", e => {
  if ((e.key === "Enter" || e.key === " ") && e.target.classList.contains("card")){ e.preventDefault(); openDetail(e.target.dataset.id); }
});

/* ---------- Audio ---------- */
const player = new Audio();
player.preload = "none";
let playingKey = null, loadingKey = null;

function pickSrc(info){
  if (!info) return null;
  const a = document.createElement("audio");
  const derivs = (info.derivatives || []).filter(d => d.src);
  const mp3 = derivs.find(d => /mpeg|mp3/i.test(d.type || d.src));
  if (/mpeg|mp3|wav|x-wav/i.test(info.mime || "") ) return info.url;
  if (mp3) return mp3.src;
  if (info.mime && a.canPlayType(info.mime)) return info.url;
  const any = derivs.find(d => d.type && a.canPlayType(d.type));
  return any ? any.src : info.url;
}

async function mainAudio(id){
  const m = meta[id];
  if (m?.audio?.length) return m.audio[0];
  const list = await searchAudio(id);
  return list[0] || null;
}

async function togglePlay(id, info){
  const key = info ? info.url : id;
  if (playingKey === key && !player.paused){ player.pause(); return; }
  loadingKey = key; syncPlayButtons();
  try {
    info = info || await mainAudio(id);
    if (!info){ setStatus(`Für ${birdById(id).de} gerade keine Aufnahme verfügbar – siehe xeno-canto-Link im Detail.`); return; }
    const src = pickSrc(info);
    if (player.src !== src) player.src = src;
    playingKey = key;
    await player.play();
  } catch (err){
    setStatus("Abspielen nicht möglich – Internetverbindung prüfen.");
    playingKey = null;
  } finally { loadingKey = null; syncPlayButtons(); }
}
["play","pause","ended","error"].forEach(ev => player.addEventListener(ev, () => {
  if (ev === "ended" || ev === "error") { if (ev==="error") setStatus("Diese Aufnahme ließ sich nicht laden."); playingKey = null; }
  syncPlayButtons();
}));
function syncPlayButtons(){
  document.querySelectorAll("[data-play]").forEach(b => {
    const k = b.dataset.play;
    const on = playingKey === k && !player.paused;
    const ld = loadingKey === k;
    b.classList.toggle("playing", on); b.classList.toggle("loading", ld);
    b.innerHTML = ld ? ICON_LOAD : on ? ICON_PAUSE : ICON_PLAY;
  });
  document.querySelectorAll("[data-more]").forEach(b => {
    const on = playingKey === b.dataset.more && !player.paused;
    b.classList.toggle("playing", on);
    b.querySelector(".mini").innerHTML = loadingKey === b.dataset.more ? ICON_LOAD : on ? ICON_PAUSE : ICON_PLAY;
  });
  const qp = $("#qplay");
  if (qp){ const on = playingKey === "quiz" && !player.paused; qp.classList.toggle("playing", on); qp.innerHTML = (on ? ICON_PAUSE : ICON_PLAY).replace(/20/g,"40"); }
}
let statusTimer;
function setStatus(t){ $("#status").textContent = t; clearTimeout(statusTimer); statusTimer = setTimeout(() => $("#status").textContent = "", 6000); }
const birdById = id => BIRDS.find(b => b.id === id);

/* ---------- Metadaten: Wikidata + Commons ---------- */
function fileName(u){ return decodeURIComponent(String(u).split("/").pop()).replace(/_/g," "); }

async function fetchJSON(url, opts){
  const r = await fetch(url, opts);
  if (!r.ok) throw new Error(r.status);
  return r.json();
}

async function commonsInfo(titles){
  const out = {};
  for (let i = 0; i < titles.length; i += 40){
    const chunk = titles.slice(i, i + 40);
    const p = new URLSearchParams({
      action:"query", format:"json", origin:"*", prop:"imageinfo|videoinfo",
      iiprop:"url|mime|extmetadata", iiurlwidth:"480", iiextmetadatafilter:"Artist|LicenseShortName",
      viprop:"derivatives",
      titles: chunk.map(t => "File:" + t).join("|")
    });
    const d = await fetchJSON(COMMONS + "?" + p);
    const norm = {};
    (d.query?.normalized || []).forEach(n => norm[n.from] = n.to);
    const pages = Object.values(d.query?.pages || {});
    chunk.forEach(t => {
      const want = norm["File:" + t] || "File:" + t;
      const pg = pages.find(x => x.title === want);
      if (pg && (pg.imageinfo || pg.videoinfo)) out[t] = toInfo(pg);
    });
  }
  return out;
}
function toInfo(pg){
  const ii = pg.imageinfo?.[0] || {}, vi = pg.videoinfo?.[0] || {};
  const em = ii.extmetadata || vi.extmetadata || {};
  return {
    title: pg.title.replace(/^File:/, ""),
    url: ii.url || vi.url, thumb: ii.thumburl || vi.thumburl || null, mime: ii.mime || vi.mime,
    derivatives: (vi.derivatives || []).map(d => ({src:d.src, type:d.type})),
    page: ii.descriptionurl || vi.descriptionurl,
    artist: strip(em.Artist?.value), license: strip(em.LicenseShortName?.value)
  };
}

async function loadMeta(force){
  const cached = store.get(CACHE_KEY);
  if (cached && cached.data){
    meta = cached.data; refreshThumbs();
    if (!force && Date.now() - cached.ts < CACHE_TTL) return;
  }
  try {
    const nameToId = {};
    BIRDS.forEach(b => { nameToId[b.lat] = b.id; (SYN[b.lat] || []).forEach(s => nameToId[s] = b.id); });
    const values = Object.keys(nameToId).map(n => `"${n}"`).join(" ");
    const sparql = `SELECT ?n ?a ?i WHERE { VALUES ?n { ${values} } ?x wdt:P225 ?n ; wdt:P105 wd:Q7432 . OPTIONAL { ?x wdt:P51 ?a } OPTIONAL { ?x wdt:P18 ?i } }`;
    const d = await fetchJSON("https://query.wikidata.org/sparql?format=json&query=" + encodeURIComponent(sparql),
      { headers:{ Accept:"application/sparql-results+json" } });
    const raw = {};
    d.results.bindings.forEach(r => {
      const id = nameToId[r.n.value]; if (!id) return;
      raw[id] = raw[id] || { audio:new Set(), image:null };
      if (r.a) raw[id].audio.add(fileName(r.a.value));
      if (r.i && !raw[id].image) raw[id].image = fileName(r.i.value);
    });
    const titles = [];
    Object.values(raw).forEach(v => { [...v.audio].slice(0,2).forEach(t => titles.push(t)); if (v.image) titles.push(v.image); });
    const info = await commonsInfo([...new Set(titles)]);
    const next = {};
    Object.entries(raw).forEach(([id, v]) => {
      next[id] = {
        audio: [...v.audio].slice(0,2).map(t => info[t]).filter(Boolean),
        image: v.image ? info[v.image] || null : null
      };
    });
    meta = next;
    if (Object.keys(next).length) store.set(CACHE_KEY, { ts: Date.now(), data: next });
    refreshThumbs();
  } catch (err){
    if (!Object.keys(meta).length) setStatus("Fotos/Aufnahmen konnten nicht vorgeladen werden – Abspielen versucht es erneut.");
  }
}
function refreshThumbs(){
  BIRDS.forEach(b => {
    const el = document.querySelector(`[data-thumb="${b.id}"]`);
    if (el && meta[b.id]?.image?.thumb && !el.querySelector("img")) el.innerHTML = thumbHTML(b);
  });
}

/* Weitere Aufnahmen über die Commons-Suche */
async function searchAudio(id){
  if (searchCache[id]) return searchCache[id];
  const b = birdById(id);
  const p = new URLSearchParams({
    action:"query", format:"json", origin:"*", generator:"search",
    gsrsearch:`filetype:audio "${b.lat}"`, gsrnamespace:"6", gsrlimit:"8",
    prop:"imageinfo|videoinfo", iiprop:"url|mime|extmetadata", iiextmetadatafilter:"Artist|LicenseShortName",
    viprop:"derivatives"
  });
  try {
    const d = await fetchJSON(COMMONS + "?" + p);
    const pages = Object.values(d.query?.pages || {}).sort((a,b) => (a.index||0) - (b.index||0));
    const list = pages.filter(pg => pg.imageinfo?.[0]?.url).map(toInfo);
    searchCache[id] = list;
    return list;
  } catch { return []; }
}
function labelFor(info){
  const t = (info.title || "").toLowerCase();
  const tags = [];
  if (/song|gesang|singing|chant/.test(t)) tags.push("Gesang");
  if (/alarm|warn/.test(t)) tags.push("Warnruf");
  else if (/flight/.test(t)) tags.push("Flugruf");
  else if (/call|ruf|calls/.test(t)) tags.push("Ruf");
  if (/drum/.test(t)) tags.push("Trommeln");
  if (/begg|juvenile|chick|young/.test(t)) tags.push("Jungvögel");
  if (/duet/.test(t)) tags.push("Duett");
  if (/female|weibchen/.test(t)) tags.push("Weibchen");
  const xc = (info.title || "").match(/XC\s?\d+/i);
  return (tags.join(" · ") || "Aufnahme") + (xc ? ` (${xc[0].replace(/\s/,"")})` : "");
}
const credit = i => [i.artist && `© ${esc(i.artist)}`, i.license && esc(i.license)].filter(Boolean).join(" · ");

/* ---------- Detail ---------- */
const detail = $("#detail");
async function openDetail(id){
  const b = birdById(id), m = meta[id] || {}, img = m.image;
  const st = stateOf(b);
  const season = M1.map((l,i) => {
    const mo = i + 1; const c = b.sings.includes(mo) && b.present.includes(mo) ? "s" : b.present.includes(mo) ? "p" : "";
    return `<span class="${c}${mo===NOW?" cur":""}" title="${MONTHS[i]}">${l}</span>`;
  }).join("");
  const hab = b.hab.map(h => HAB[h].icon + " " + HAB[h].label).join(" · ");
  $("#sheet").innerHTML = `
    <div class="hero-img">
      <button class="close" type="button" aria-label="Schließen">×</button>
      ${img ? `<img src="${esc(img.thumb || img.url)}" alt="${esc(b.de)}"><div class="credit">Foto: <a href="${esc(img.page)}" target="_blank" rel="noopener">${credit(img) || "Wikimedia Commons"}</a></div>`
            : `<div style="height:100%;display:grid;place-items:center;font-family:Fraunces,serif;font-size:80px;color:var(--moss)">${esc(b.de[0])}</div>`}
    </div>
    <div class="sheet-inner">
      <h2>${esc(b.de)}</h2>
      <div class="lat">${esc(b.lat)} · ${hab}</div>
      <div style="margin-top:8px">${BADGE[st]}</div>
      <div class="lautbild">${esc(b.lautbild)}</div>
      <div class="player" id="mainplayer"><div class="audiocredit">Aufnahme wird geladen …</div></div>
      <div class="sec"><h3>Gesang</h3><p>${esc(b.gesang)}</p></div>
      <div class="sec"><h3>Rufe</h3><p>${esc(b.ruf)}</p></div>
      <div class="sec"><h3>Merkspruch</h3><p><i>${esc(b.merk)}</i></p></div>
      <div class="sec"><h3>Verwechslungsgefahr</h3><p>${esc(b.verw)}</p></div>
      <div class="sec"><h3>Wo in München</h3><p>${esc(b.wo)}</p></div>
      <div class="sec"><h3>Wann zu hören</h3><div class="season">${season}</div>
        <div class="legend"><span><i style="background:var(--moss)"></i>Gesangszeit</span><span><i style="background:var(--sky-2)"></i>anwesend, Rufe</span><span><i style="background:var(--absent)"></i>abwesend</span></div></div>
      <div class="sec"><h3>Wissenswert</h3><p>${esc(b.fakt)}</p></div>
      <div class="sec"><h3>Weitere Aufnahmen</h3><div class="more" id="more"><small>werden gesucht …</small></div></div>
      <a class="extlink" href="https://xeno-canto.org/explore?query=${encodeURIComponent(b.lat)}" target="_blank" rel="noopener">Hunderte weitere Aufnahmen auf xeno-canto ↗</a>
    </div>`;
  $("#sheet").scrollTop = 0;
  detail.showModal();
  if (!player.paused) player.pause();

  // Hauptaufnahme
  const main = await mainAudio(id);
  if (!detail.open || $("#sheet h2")?.textContent !== b.de) return;
  $("#mainplayer").innerHTML = main
    ? `<audio controls preload="none" src="${esc(pickSrc(main))}"></audio><div class="audiocredit">${labelFor(main)} – <a href="${esc(main.page)}" target="_blank" rel="noopener">${credit(main) || "Wikimedia Commons"}</a></div>`
    : `<div class="audiocredit">Keine Aufnahme gefunden – nutze den xeno-canto-Link unten.</div>`;
  const ma = $("#mainplayer audio");
  if (ma) ma.addEventListener("play", () => { if (!player.paused) player.pause(); });

  // Weitere
  const list = (await searchAudio(id)).filter(i => !main || i.url !== main.url).slice(0, 6);
  if (!detail.open || $("#sheet h2")?.textContent !== b.de) return;
  $("#more").innerHTML = list.length ? list.map((i, n) =>
    `<button type="button" data-more="${esc(i.url)}" data-n="${n}"><span class="mini">${ICON_PLAY}</span><span>${esc(labelFor(i))}<small>${credit(i)}</small></span></button>`).join("")
    : "<small>Keine weiteren Aufnahmen auf Commons gefunden.</small>";
  $("#more").onclick = e => {
    const btn = e.target.closest("[data-more]"); if (!btn) return;
    if (ma && !ma.paused) ma.pause();
    togglePlay(id, list[+btn.dataset.n]);
  };
}
detail.addEventListener("click", e => {
  if (e.target === detail || e.target.closest(".close")) closeDialog(detail);
});
detail.addEventListener("close", () => {
  player.pause();
  document.querySelectorAll("#sheet audio").forEach(a => a.pause());
});
function closeDialog(d){ d.close(); }

/* ---------- Ohr-Training ---------- */
const quiz = $("#quiz");
let q = { score:0, total:0, nowOnly:false, current:null, answered:false };
function quizPool(){ return BIRDS.filter(b => !q.nowOnly || stateOf(b) !== "away"); }
function shuffle(a){ for (let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

async function nextQuestion(tries = 0){
  const pool = quizPool();
  const prev = q.current?.id;
  let bird = shuffle(pool.filter(b => b.id !== prev))[0];
  q.current = bird; q.answered = false;
  const others = shuffle(BIRDS.filter(b => b.id !== bird.id)).slice(0, 3);
  q.options = shuffle([bird, ...others]);
  renderQuiz();
  q.audio = await mainAudio(bird.id);
  if (q.current !== bird) return;
  if (!q.audio){
    if (tries < 4) { nextQuestion(tries + 1); return; }
    $("#qresult").textContent = "Gerade lassen sich keine Aufnahmen laden – bitte Internetverbindung prüfen.";
    return;
  }
  playQuiz();
}
function playQuiz(){
  if (!q.audio) return;
  if (playingKey === "quiz" && !player.paused){ player.pause(); return; }
  const src = pickSrc(q.audio);
  if (player.src !== src) player.src = src;
  playingKey = "quiz";
  player.play().catch(() => setStatus("Abspielen nicht möglich.")).finally(syncPlayButtons);
}
function renderQuiz(){
  const b = q.current;
  $("#quizsheet").innerHTML = `
    <div class="quiz">
      <button class="close" type="button" aria-label="Schließen" style="background:var(--absent);color:var(--ink)">×</button>
      <div class="kicker">Ohr-Training</div>
      <h2 style="font-family:Fraunces,serif;margin:4px 0 0">Wer singt da?</h2>
      <button class="qplay" id="qplay" type="button" aria-label="Aufnahme abspielen">${ICON_LOAD.replace(/20/g,"40")}</button>
      <div class="opts">${q.options.map(o => `<button type="button" data-ans="${o.id}">${esc(o.de)}</button>`).join("")}</div>
      <div id="qresult" class="qmeta"></div>
      <div class="qmeta" id="qscore">Punkte: <b>${q.score}</b> / ${q.total}</div>
      <label class="qtoggle"><input type="checkbox" id="qnow" ${q.nowOnly?"checked":""}> nur Vögel, die im ${MONTHS[NOW-1]} zu hören sind</label>
    </div>`;
  syncPlayButtons();
}
$("#quizsheet").addEventListener("click", e => {
  if (e.target.closest(".close")){ closeDialog(quiz); return; }
  if (e.target.closest("#qplay")){ playQuiz(); return; }
  if (e.target.closest(".qnext")){ nextQuestion(); return; }
  const a = e.target.closest("[data-ans]");
  if (a && !q.answered){
    q.answered = true; q.total++;
    const right = a.dataset.ans === q.current.id;
    if (right) q.score++;
    document.querySelectorAll("[data-ans]").forEach(btn => {
      if (btn.dataset.ans === q.current.id) btn.classList.add("right");
      else if (btn === a) btn.classList.add("wrong");
    });
    $("#qresult").innerHTML = (right ? "✓ Richtig! " : "✗ Das war ") + `<b>${esc(q.current.de)}</b> – <i>${esc(q.current.merk)}</i><br><button class="qnext" type="button">Nächster Vogel →</button>`;
    $("#qscore").innerHTML = `Punkte: <b>${q.score}</b> / ${q.total}`;
  }
});
$("#quizsheet").addEventListener("change", e => { if (e.target.id === "qnow") q.nowOnly = e.target.checked; });
quiz.addEventListener("click", e => { if (e.target === quiz) closeDialog(quiz); });
quiz.addEventListener("close", () => { player.pause(); });
$("#quizbtn").addEventListener("click", () => { quiz.showModal(); nextQuestion(); });

/* ---------- Sticky-Schatten ---------- */
const ctr = $("#controls");
new IntersectionObserver(([e]) => ctr.classList.toggle("stuck", e.intersectionRatio < 1), { threshold:[1], rootMargin:"-1px 0px 0px 0px" }).observe(ctr);

/* ---------- Start ---------- */
renderNow(); renderChips(); renderGrid(); loadMeta();
})();
