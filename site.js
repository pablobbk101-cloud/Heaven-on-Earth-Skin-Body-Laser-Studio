/* Heaven On Earth concept: navigation, dropdown, tabs, demo contact form and motion. No dependencies. */
(function () {
  var root = document.documentElement;
  root.classList.add('js');

  /* page-to-page transitions are a nicety: if the browser skips one, do not report it as an error */
  function quiet(e) {
    var vt = e && e.viewTransition;
    if (!vt) return;
    ['ready', 'finished', 'updateCallbackDone'].forEach(function (k) { if (vt[k] && vt[k].catch) vt[k].catch(function () {}); });
  }
  window.addEventListener('pageswap', quiet);
  window.addEventListener('pagereveal', quiet);
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- mobile menu (animated open and close) ---------------- */
  var menuBtn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  function closeMenu() {
    if (!nav.classList.contains('open')) return;
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.textContent = 'Menu';
    if (reduce) { nav.classList.remove('open'); return; }
    nav.classList.add('closing');
    var done = function () { nav.classList.remove('open', 'closing'); nav.removeEventListener('animationend', done); };
    nav.addEventListener('animationend', done);
    setTimeout(done, 400); /* safety net if animationend never fires */
  }
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      if (nav.classList.contains('open') && !nav.classList.contains('closing')) { closeMenu(); return; }
      nav.classList.remove('closing');
      nav.classList.add('open');
      menuBtn.setAttribute('aria-expanded', 'true');
      menuBtn.textContent = 'Close';
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  }

  /* ---------------- services dropdown: hover and focus in CSS, button for touch and keyboard ---------------- */
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

  /* ---------------- tabs on treatment pages (panels fade in when switched) ---------------- */
  document.querySelectorAll('[data-tabs]').forEach(function (tabRoot) {
    var tabs = Array.prototype.slice.call(tabRoot.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
    var current = -1;
    function select(i, focus) {
      var changed = current !== -1 && current !== i;
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
      });
      if (changed && !reduce) {
        var p = panels[i];
        p.classList.remove('panel-in', 'panel-in-back');
        void p.offsetWidth;
        p.classList.add(i > current ? 'panel-in' : 'panel-in-back');
      }
      current = i;
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

  /* ---------------- demo contact form: nothing is sent ---------------- */
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

  /* ---------------- header: soft shadow once the page scrolls ---------------- */
  var header = document.querySelector('.site-header');
  var ticking = false;
  var parallax = reduce ? [] : Array.prototype.slice.call(document.querySelectorAll('.arch img, .page-head .orb-main img'));
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle('scrolled', y > 8);
    parallax.forEach(function (img) {
      var r = img.parentNode.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var shift = Math.max(-40, Math.min(40, -r.top * 0.08));
      img.style.setProperty('--py', shift.toFixed(1) + 'px');
    });
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  if (reduce) return;

  /* ---------------- images below the fold fade in as they load ---------------- */
  document.querySelectorAll('img[loading="lazy"]').forEach(function (img) {
    if (img.complete && img.naturalWidth) return;
    img.classList.add('img-wait');
    var show = function () { img.classList.remove('img-wait'); };
    img.addEventListener('load', show, { once: true });
    img.addEventListener('error', show, { once: true });
  });

  /* ---------------- scroll reveal: content glides in as it reaches the screen ---------------- */
  if (!('IntersectionObserver' in window)) return;
  var vh = window.innerHeight;
  function belowFold(el) { return el.getBoundingClientRect().top > vh * 0.92; }

  var singles = '.h2-head, .section-head, .team-intro, .swipe-hint, .split > *, .visit-grid > *, .cta .wrap > *, .contact-grid > .card, .menu-wrap > .wrap, .section-tint .wrap > *, .book-grid > *, .site-footer .legal';
  var groups = '.cards, .specs, .mini-team, .team, .svc-list, .others, .foot-grid, .amenities';
  var targets = [];

  /* groups first: their children glide in one after another */
  document.querySelectorAll(groups).forEach(function (g) {
    if (!belowFold(g)) return;
    g.setAttribute('data-rv-group', '');
    Array.prototype.forEach.call(g.children, function (child, i) {
      child.classList.add('rv');
      child.style.setProperty('--d', Math.min(i, 7));
    });
    targets.push(g);
  });
  /* single blocks, skipping anything already handled as a group or inside one */
  document.querySelectorAll(singles).forEach(function (el) {
    if (!belowFold(el) || el.hasAttribute('data-rv-group') || el.closest('[data-rv-group]')) return;
    el.classList.add('rv');
    targets.push(el);
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      var items = el.hasAttribute('data-rv-group') ? Array.prototype.slice.call(el.children) : [el];
      items.forEach(function (it) {
        it.classList.add('in');
        /* hand control back to normal hover transitions once the reveal is over */
        setTimeout(function () { it.classList.remove('rv', 'in'); it.style.removeProperty('--d'); }, 1500);
      });
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  targets.forEach(function (t) { io.observe(t); });
})();
