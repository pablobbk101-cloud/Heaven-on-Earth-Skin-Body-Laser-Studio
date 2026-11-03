/* Heaven On Earth concept: navigation, dropdown, tabs, demo contact form. No dependencies. */
(function () {
  document.documentElement.classList.add('js');

  /* mobile menu */
  var menuBtn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuBtn.textContent = open ? 'Close' : 'Menu';
    });
  }

  /* services dropdown: hover and focus are handled in CSS, the button serves touch and keyboard */
  var sub = document.querySelector('.has-sub');
  if (sub) {
    var toggle = sub.querySelector('.sub-toggle');
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = sub.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (!sub.contains(e.target)) {
        sub.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && sub.classList.contains('open')) {
        sub.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* tabs on treatment pages */
  document.querySelectorAll('[data-tabs]').forEach(function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
    function select(i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
      });
      if (focus) tabs[i].focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () {
        select(i, false);
        if (history.replaceState) history.replaceState(null, '', '#' + t.getAttribute('aria-controls'));
      });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = tabs.length;
        if (k === 'ArrowRight') { e.preventDefault(); select((i + 1) % n, true); }
        else if (k === 'ArrowLeft') { e.preventDefault(); select((i - 1 + n) % n, true); }
        else if (k === 'Home') { e.preventDefault(); select(0, true); }
        else if (k === 'End') { e.preventDefault(); select(n - 1, true); }
      });
    });
    function fromHash() {
      var hash = location.hash.replace('#', '');
      var start = 0;
      panels.forEach(function (p, i) { if (p.id === hash) start = i; });
      select(start, false);
    }
    window.addEventListener('hashchange', fromHash);
    fromHash();
  });

  /* demo contact form: nothing is sent */
  var cf = document.getElementById('contact-form');
  if (cf) {
    cf.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      ['cf-email', 'cf-message'].forEach(function (id) {
        var f = document.getElementById(id);
        var err = document.getElementById(id + '-err');
        var bad = !f.value.trim() || (id === 'cf-email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value.trim()));
        f.setAttribute('aria-invalid', bad ? 'true' : 'false');
        err.textContent = bad ? (id === 'cf-email' ? 'Enter a valid email address.' : 'Write a short message.') : '';
        if (bad && ok) { f.focus(); }
        if (bad) ok = false;
      });
      if (ok) {
        var n = document.getElementById('cf-notice');
        n.hidden = false;
        n.focus();
        cf.reset();
      }
    });
  }
})();
