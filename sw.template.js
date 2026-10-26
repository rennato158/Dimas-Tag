/* DIMAS Tag — service worker: deixa o app disponível offline. Gerado por build.py. */
const VERSION = "__VERSION__";
const CACHE = "dimas-tag-" + VERSION;
const SHELL = [
  "./", "index.html", "manifest.webmanifest", "sw.js",
  "vendor/jszip.min.js", "vendor/xlsx.full.min.js",
  "icons/icon-32.png", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-192-maskable.png", "icons/icon-512-maskable.png", "icons/apple-touch-icon.png"
];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
/* Arquivos do app: cache primeiro, atualiza em segundo plano.
   Fontes do Google: cache quando houver rede, sem bloquear quando não houver. */
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const sameOrigin = url.origin === self.location.origin;
  const isFont = /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if (!sameOrigin && !isFont) return;
  /* elenco.json: sempre tenta a rede primeiro (é a lista de atletas publicada); cache só como reserva offline. */
  if (sameOrigin && /\/elenco\.json$/.test(url.pathname)) {
    e.respondWith(fetch(req).then(res => { if (res.ok) caches.open(CACHE).then(c => c.put(req, res.clone())); return res; }).catch(() => caches.match(req, { ignoreSearch: true })));
    return;
  }
  e.respondWith(
    caches.match(req, { ignoreSearch: sameOrigin }).then(cached => {
      const net = fetch(req).then(res => {
        if (res && (res.ok || res.type === "opaque")) caches.open(CACHE).then(c => c.put(req, res.clone()));
        return res;
      }).catch(() => cached);
      return cached || net;
    })
  );
});
