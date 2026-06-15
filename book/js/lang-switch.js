// Inject an EN/TH language toggle into the mdBook top menu bar.
// Thai book is served at <base>/, English at <base>/en/.
(function () {
  var BASE = '/open-knowledge-format-starter/';
  function counterpart() {
    var p = location.pathname;
    if (p.indexOf(BASE + 'en/') === 0)
      return { href: BASE + p.slice((BASE + 'en/').length), label: 'ไทย', title: 'อ่านภาษาไทย' };
    if (p.indexOf(BASE) === 0)
      return { href: BASE + 'en/' + p.slice(BASE.length), label: 'EN', title: 'Read in English' };
    // local/dev fallback (no known base path)
    if (p.indexOf('/en/') !== -1)
      return { href: p.replace('/en/', '/'), label: 'ไทย', title: 'อ่านภาษาไทย' };
    return { href: p.replace(/\/(?=[^\/]*$)/, '/en/'), label: 'EN', title: 'Read in English' };
  }
  function add() {
    var rb = document.querySelector('#menu-bar .right-buttons');
    if (!rb || document.getElementById('okf-lang')) return;
    var c = counterpart();
    var a = document.createElement('a');
    a.id = 'okf-lang';
    a.href = c.href;
    a.title = c.title;
    a.className = 'icon-button';
    a.setAttribute('aria-label', c.title);
    a.textContent = c.label;
    rb.insertBefore(a, rb.firstChild);
  }
  if (document.readyState !== 'loading') add();
  else document.addEventListener('DOMContentLoaded', add);
})();

// Fill the cover's "updated" date (ISO, language-neutral) on web and when printing to PDF.
(function () {
  function setDate() {
    var el = document.getElementById('okf-date');
    if (!el) return;
    try { el.textContent = new Date().toISOString().slice(0, 10); } catch (e) {}
  }
  if (document.readyState !== 'loading') setDate();
  else document.addEventListener('DOMContentLoaded', setDate);
})();
