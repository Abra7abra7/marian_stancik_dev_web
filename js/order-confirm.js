// Order confirmation box (contact page) — reads ?ordered=&email=&url= from the URL
// and fills #orderConfirmationBox. Extracted from an inline <script> for CSP script-src 'self'.
(function () {
  'use strict';
  var box = document.getElementById('orderConfirmationBox');
  if (!box) return;

  var params = new URLSearchParams(window.location.search);
  var ordered = params.get('ordered');
  var email = params.get('email');
  var url = params.get('url');

  if (ordered || email || url) {
    box.style.display = 'block';
    var p = document.getElementById('orderBoxProduct');
    var e = document.getElementById('orderBoxEmail');
    var u = document.getElementById('orderBoxUrl');
    if (p) p.textContent = ordered || 'AI Audit / Agent Service';
    if (e) e.textContent = email || 'Zadaný e-mail';
    if (u) u.textContent = url || 'Zadaná doména';
    box.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
})();
