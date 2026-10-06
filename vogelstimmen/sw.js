/* Vogelohr Service Worker
   – Medien (Fotos, Stimmbilder, Aufnahmen) aus dem Cache, inkl. Range-Anfragen für Audio
   – alles andere zuerst aus dem Netz, bei Funkloch aus dem Cache */
const SHELL = "vogelohr-shell-v2", MEDIA = "vogelohr-media-v1";
const CORE = ["./", "index.html", "app.css", "app.js", "data/birds.js", "media.json", "icon.svg", "manifest.webmanifest"];
self.addEventListener("install", e => { e.waitUntil(caches.open(SHELL).then(c => c.addAll(CORE)).catch(() => {})); self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("vogelohr") && ![SHELL, MEDIA].includes(k)).map(k => caches.delete(k))))); self.clients.claim(); });

async function ranged(req, full){
  const range = req.headers.get("range");
  if (!range) return full;
  const buf = await full.arrayBuffer();
  const m = /bytes=(\d*)-(\d*)/.exec(range) || [];
  const size = buf.byteLength;
  let start = m[1] ? +m[1] : 0, end = m[2] ? +m[2] : size - 1;
  if (!m[1] && m[2]) { start = size - +m[2]; end = size - 1; }
  end = Math.min(end, size - 1);
  return new Response(buf.slice(start, end + 1), { status: 206, statusText: "Partial Content", headers: {
    "Content-Type": full.headers.get("Content-Type") || "audio/mpeg",
    "Content-Range": `bytes ${start}-${end}/${size}`, "Content-Length": String(end - start + 1), "Accept-Ranges": "bytes" } });
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin === location.origin && url.pathname.includes("/media/")) {
    e.respondWith((async () => {
      const cache = await caches.open(MEDIA);
      const hit = await cache.match(url.href);
      if (hit) return ranged(req, hit);
      if (req.headers.has("range")) {
        e.waitUntil(cache.add(url.href).catch(() => {}));
        return fetch(req);
      }
      const res = await fetch(req);
      if (res.ok && res.status === 200) cache.put(url.href, res.clone());
      return res;
    })());
    return;
  }
  if (url.origin === location.origin || url.host.endsWith("fonts.googleapis.com") || url.host.endsWith("fonts.gstatic.com")) {
    e.respondWith(fetch(req).then(res => {
      if (res.ok && res.status === 200) { const copy = res.clone(); caches.open(SHELL).then(c => c.put(req, copy)); }
      return res;
    }).catch(() => caches.match(req, { ignoreSearch: true }).then(r => r || caches.match("index.html"))));
  }
});
