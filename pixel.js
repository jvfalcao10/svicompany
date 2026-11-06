// Meta Pixel da SVI (conta Falcao, "Raio-X Conversions"). PageView nas páginas sem o pixel do config.js e Contact em todo clique no WhatsApp.
(function () {
  var ID = '1010100498078285';
  if (!window.fbq) {
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, 'script', 'https://connect.facebook.net/pt_BR/fbevents.js');
    fbq('init', ID);
    fbq('track', 'PageView');
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="wa.me"],a[href*="api.whatsapp.com"]');
    if (a && window.fbq) fbq('track', 'Contact');
  }, true);
})();
