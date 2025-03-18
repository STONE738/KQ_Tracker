self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('ai-tracker-v1').then((cache) => {
      return cache.addAll([
        '/',
        '/static/css/bootstrap.min.css',
        '/static/css/styles.css',
        '/static/images/Ai_tracker-logo.jpg'
      ]);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});