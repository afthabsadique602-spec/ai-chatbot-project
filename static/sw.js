const CACHE_NAME = 'bookstore-ai-v2';
const urlsToCache = [
  '/',
  '/manifest.json',
  '/static/icon.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  // Only handle GET requests for caching
  if (event.request.method !== 'GET') {
    return;
  }
  
  event.respondWith(
    fetch(event.request)
      .catch(() => caches.match(event.request))
  );
});
