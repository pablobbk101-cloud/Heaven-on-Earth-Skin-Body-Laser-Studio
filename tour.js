/* Heaven On Earth concept: guided preview tour.
   Starts with ?tour=1 in the link, or from the "Take the tour" button on any page.
   Walks across pages; the current step is kept in sessionStorage so the tour survives page changes. */
(function () {
  var KEY = 'hoe-tour-step';
  var PABLO_WA = 'https://wa.me/27604521037';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* sel: one selector or a list (the first one that is visible is used); no sel = centred card */
  var STEPS = [
    { page: 'index', title: 'Welcome to your website preview',
      text: 'This short tour shows you around your new website, one part at a time. It takes about two minutes. Use Next to move on, or close it any time and explore on your own.' },
    { page: 'index', sel: '.hero', title: 'Your home page',
      text: 'This is the first thing clients see: your name, a current special, real prices from your menu and a clear Book online button.' },
    { page: 'index', sel: '.hero-top .rating', title: 'Your Booksy rating',
      text: 'Your 4.8 rating from 290 Booksy reviews sits right under the buttons. Tapping it opens your reviews on Booksy.' },
    { page: 'index', sel: ['.has-sub', '.menu-btn'], title: 'The Services menu',
      text: 'Every treatment area has its own page, plus a Specials page, so clients find what they want without scrolling through one long list.' },
    { page: 'index', sel: '.treatments', title: 'Your treatments',
      text: 'Each card opens a treatment area and shows its starting price. On a phone, clients swipe sideways through them.' },
    { page: 'index', sel: '.specials', title: 'Your specials',
      text: 'Your combos and packages from Booksy, each with a Book now button.' },
    { page: 'index', sel: '.crew', title: 'Your team',
      text: 'Your team photos, with your own words about the studio. Tapping a photo opens the About page.' },
    { page: 'index', sel: '.visit', title: 'Finding you',
      text: 'Address, phone, WhatsApp, email, opening hours and a map with directions, so new clients get to you easily.' },
    { page: 'index', sel: ['.dock .dock-main', '.nav-cta'], title: 'Booking stays on Booksy',
      text: 'Every Book button opens your Booksy page, so your bookings, reminders and reviews keep working exactly as they do now.' },
    { page: 'hairless', sel: '.page-head', title: 'A treatment page',
      text: 'Each treatment area gets a page like this one, with your own description at the top.' },
    { page: 'hairless', sel: '[data-tabs] .tablist', title: 'Tabs keep it short',
      text: 'Longer price lists are split into tabs, here laser hair removal and waxing, so clients see one list at a time.' },
    { page: 'hairless', sel: '.tabpanel:not([hidden]) .menu-row', title: 'Prices that match Booksy',
      text: 'Every treatment shows its time and price, the same as your Booksy menu, and its own Book now button that goes to Booksy.' },
    { page: 'about', sel: '.team', title: 'Meet the team',
      text: 'The About page introduces the studio and the whole team, using your own photos.' },
    { page: 'booking-preview', sel: '.book-grid', title: 'Optional: your own booking system',
      text: 'If you ever want clients to book on your own website instead of Booksy, this is how it could work. Try it: pick a treatment, a date and a time. Nothing is booked or sent.' },
    { page: 'index', title: 'That is the tour',
      text: 'Thank you for having a look. Explore any page you like, and message me with questions or changes you would like.', last: true }
  ];

  function pageId() {
    var p = location.pathname.replace(/\/+$/, '').split('/').pop().replace(/\.html$/, '');
    return p === '' ? 'index' : p;
  }
  function pageUrl(id) {
    var onFile = location.protocol === 'file:' || /\.html$/.test(location.pathname);
    if (id === 'index') return onFile ? 'index.html' : './';
    return onFile ? id + '.html' : id;
  }
  function store(v) { try { if (v === null) sessionStorage.removeItem(KEY); else sessionStorage.setItem(KEY, String(v)); } catch (e) {} }
  function stored() { try { var v = sessionStorage.getItem(KEY); return v === null ? null : parseInt(v, 10); } catch (e) { return null; } }

  function visible(el) {
    if (!el) return false;
    var r = el.getBoundingClientRect();
    var s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
  }
  function target(step) {
    if (!step.sel) return null;
    var list = [].concat(step.sel);
    for (var i = 0; i < list.length; i++) {
      var all = document.querySelectorAll(list[i]);
      for (var j = 0; j < all.length; j++) if (visible(all[j])) return all[j];
    }
    return null;
  }

  /* ---------------- UI ---------------- */
  var ui = null, current = -1, el = null, raf = 0;
  function build() {
    if (ui) return ui;
    ui = {};
    ui.shade = document.createElement('div');
    ui.shade.className = 'tour-shade';
    ui.spot = document.createElement('div');
    ui.spot.className = 'tour-spot';
    ui.card = document.createElement('div');
    ui.card.className = 'tour-card';
    ui.card.setAttribute('role', 'dialog');
    ui.card.setAttribute('aria-modal', 'false');
    ui.card.setAttribute('aria-labelledby', 'tour-title');
    ui.card.tabIndex = -1;
    ui.card.innerHTML =
      '<div class="tour-top"><span class="tour-count" id="tour-count"></span>' +
      '<button type="button" class="tour-x" aria-label="Close the tour">×</button></div>' +
      '<div class="tour-bar" aria-hidden="true"><span id="tour-bar"></span></div>' +
      '<h2 class="tour-title" id="tour-title"></h2><p class="tour-text" id="tour-text" aria-live="polite"></p>' +
      '<div class="tour-actions"><button type="button" class="btn btn-line tour-back">Back</button>' +
      '<button type="button" class="btn btn-solid tour-next">Next</button></div>';
    document.body.appendChild(ui.shade);
    document.body.appendChild(ui.spot);
    document.body.appendChild(ui.card);
    ui.card.querySelector('.tour-x').addEventListener('click', end);
    ui.card.querySelector('.tour-back').addEventListener('click', function () { go(current - 1); });
    ui.card.querySelector('.tour-next').addEventListener('click', function () {
      if (STEPS[current].last) { end(); return; }
      go(current + 1);
    });
    ui.shade.addEventListener('click', function () { /* clicking the dimmed page does nothing, to avoid losing the tour by accident */ });
    document.addEventListener('keydown', function (e) {
      if (current < 0) return;
      if (e.key === 'Escape') end();
      else if (e.key === 'ArrowRight' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) { if (!STEPS[current].last) go(current + 1); }
      else if (e.key === 'ArrowLeft' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) go(current - 1);
    });
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule);
    return ui;
  }

  function schedule() { if (current < 0) return; cancelAnimationFrame(raf); raf = requestAnimationFrame(place); }

  function place() {
    if (!ui || current < 0) return;
    var step = STEPS[current];
    var vw = window.innerWidth, vh = window.innerHeight, phone = vw < 700;
    var card = ui.card;
    card.classList.toggle('sheet', phone);
    if (!el) {
      ui.spot.style.opacity = '0';
      ui.shade.classList.add('on');
      card.classList.add('center');
      card.style.left = card.style.top = '';
      return;
    }
    ui.shade.classList.remove('on');
    card.classList.remove('center');
    var r = el.getBoundingClientRect();
    var pad = 8;
    var top = Math.max(r.top - pad, 6), bottom = Math.min(r.bottom + pad, vh - 6);
    var left = Math.max(r.left - pad, 6), right = Math.min(r.right + pad, vw - 6);
    var s = ui.spot.style;
    s.opacity = bottom - top > 4 ? '1' : '0';
    s.transform = 'translate(' + left + 'px,' + top + 'px)';
    s.width = Math.max(0, right - left) + 'px';
    s.height = Math.max(0, bottom - top) + 'px';
    if (phone) { card.style.left = card.style.top = ''; return; }
    var cw = card.offsetWidth, ch = card.offsetHeight, gap = 16, x, y;
    if (vh - bottom >= ch + gap) y = bottom + gap;
    else if (top >= ch + gap) y = top - ch - gap;
    else y = vh - ch - 20;
    x = Math.min(Math.max(left, 16), vw - cw - 16);
    card.style.left = x + 'px';
    card.style.top = Math.max(16, y) + 'px';
  }

  function show(i) {
    build();
    current = i;
    store(i);
    var step = STEPS[i];
    document.documentElement.classList.add('touring');
    ui.card.querySelector('#tour-count').textContent = (i + 1) + ' of ' + STEPS.length;
    ui.card.querySelector('#tour-bar').style.transform = 'scaleX(' + ((i + 1) / STEPS.length).toFixed(3) + ')';
    ui.card.querySelector('#tour-title').textContent = step.title;
    ui.card.querySelector('#tour-text').textContent = step.text;
    var back = ui.card.querySelector('.tour-back');
    back.hidden = i === 0;
    var next = ui.card.querySelector('.tour-next');
    next.textContent = step.last ? 'Explore on my own' : (i === 0 ? 'Start the tour' : 'Next');
    var extra = ui.card.querySelector('.tour-wa');
    if (step.last && !extra) {
      extra = document.createElement('a');
      extra.className = 'btn btn-line tour-wa';
      extra.href = PABLO_WA;
      extra.rel = 'noopener';
      extra.target = '_blank';
      extra.textContent = 'WhatsApp Pablo';
      ui.card.querySelector('.tour-actions').insertBefore(extra, next);
    } else if (!step.last && extra) { extra.remove(); }
    el = target(step);
    /* on phones the quick-action bar steps aside during the tour, unless this step is about it */
    var dockStep = !!(el && el.closest && el.closest('.dock'));
    document.documentElement.classList.toggle('tour-dock', dockStep);
    ui.card.classList.toggle('sheet', window.innerWidth < 700);
    ui.card.classList.remove('in');
    void ui.card.offsetWidth;
    ui.card.classList.add('in');
    if (el) {
      var r = el.getBoundingClientRect();
      var phone = window.innerWidth < 700;
      var room = window.innerHeight - (phone ? ui.card.offsetHeight + (dockStep ? 110 : 30) : 0);
      var wantTop = r.height > room * 0.8 ? 90 : Math.max(80, (room - r.height) / 2);
      var y = window.scrollY + r.top - wantTop;
      window.scrollTo({ top: Math.max(0, y), behavior: reduce ? 'auto' : 'smooth' });
    }
    place();
    setTimeout(place, 450);
    setTimeout(place, 900);
    ui.card.focus({ preventScroll: true });
  }

  function go(i) {
    if (i < 0 || i >= STEPS.length) return;
    var step = STEPS[i];
    if (step.page !== pageId()) {
      store(i);
      location.href = pageUrl(step.page);
      return;
    }
    show(i);
  }

  function end() {
    current = -1;
    el = null;
    store(null);
    document.documentElement.classList.remove('touring', 'tour-dock');
    if (ui) { ui.card.remove(); ui.spot.remove(); ui.shade.remove(); ui = null; }
    try { var u = new URL(location.href); if (u.searchParams.has('tour')) { u.searchParams.delete('tour'); history.replaceState(null, '', u.pathname + u.search + u.hash); } } catch (e) {}
  }

  function start() {
    var first = 0;
    if (STEPS[first].page !== pageId()) { store(first); location.href = pageUrl('index'); return; }
    show(first);
  }

  /* "Take the tour" buttons */
  document.querySelectorAll('[data-tour-start]').forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); start(); });
  });

  /* resume after a page change, or start from ?tour=1 */
  function boot() {
    var s = stored();
    if (s !== null && STEPS[s] && STEPS[s].page === pageId()) { show(s); return; }
    if (s !== null) store(null); /* they wandered off the tour's page: forget it */
    if (/[?&]tour=1\b/.test(location.search)) start();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(boot, 300); });
  else setTimeout(boot, 300);
})();
