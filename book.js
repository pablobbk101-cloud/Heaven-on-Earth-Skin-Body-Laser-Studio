/* Heaven On Earth concept: online booking demo.
   Nothing is stored or sent. Times shown are sample availability only. */
(function () {
  var catalog = JSON.parse(document.getElementById('catalog').textContent);
  var state = { cat: catalog[0].slug, item: null, date: null, time: null };
  var byId = {};
  catalog.forEach(function (c) { c.items.forEach(function (it) { it.cat = c.slug; it.catName = c.name; byId[it.id] = it; }); });

  var steps = ['treatment', 'when', 'details', 'review'];
  var current = 0;
  var el = function (id) { return document.getElementById(id); };
  var stepEls = steps.map(function (s) { return el('step-' + s); });
  var stepperItems = Array.prototype.slice.call(document.querySelectorAll('.stepper li'));

  /* ---------- step 1: treatment ---------- */
  var catTabs = el('cat-tabs');
  var pickList = el('pick-list');

  function renderCats() {
    catTabs.innerHTML = '';
    catalog.forEach(function (c) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'tab';
      b.textContent = c.name;
      b.setAttribute('aria-pressed', c.slug === state.cat ? 'true' : 'false');
      b.addEventListener('click', function () { state.cat = c.slug; renderCats(); renderItems(); animateIn(pickList, false); });
      catTabs.appendChild(b);
    });
  }

  function renderItems() {
    var cat = catalog.filter(function (c) { return c.slug === state.cat; })[0];
    pickList.innerHTML = '';
    var lastGroup = null;
    cat.items.forEach(function (it) {
      if (it.group !== lastGroup) {
        lastGroup = it.group;
        var h = document.createElement('h3');
        h.className = 'pick-group';
        h.textContent = it.group;
        pickList.appendChild(h);
      }
      var li = document.createElement('div');
      var label = document.createElement('label');
      var input = document.createElement('input');
      input.type = 'radio';
      input.name = 'treatment';
      input.value = it.id;
      input.checked = state.item === it.id;
      input.addEventListener('change', function () { state.item = it.id; update(); });
      var nm = document.createElement('span');
      nm.textContent = it.name;
      var du = document.createElement('span');
      du.className = 'du';
      du.textContent = it.dur || '';
      var pr = document.createElement('span');
      pr.className = 'pr';
      pr.textContent = it.price;
      label.appendChild(input); label.appendChild(nm); label.appendChild(du); label.appendChild(pr);
      li.appendChild(label);
      li.className = 'pick-row';
      pickList.appendChild(li);
    });
  }

  /* ---------- step 2: date and time ---------- */
  var dateWrap = el('dates');
  var slotWrap = el('slots');
  var days = [];
  var today = new Date();
  for (var i = 1; i <= 14; i++) { var d = new Date(today.getFullYear(), today.getMonth(), today.getDate() + i); days.push(d); }
  var wdNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  var moNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var times = [];
  for (var h = 9; h <= 16; h++) { times.push(('0' + h).slice(-2) + ':00'); times.push(('0' + h).slice(-2) + ':30'); }

  function dateKey(d) { return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate(); }
  function dateLabel(d) { return wdNames[d.getDay()] + ' ' + d.getDate() + ' ' + moNames[d.getMonth()]; }

  function renderDates() {
    dateWrap.innerHTML = '';
    days.forEach(function (d) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'date';
      b.setAttribute('aria-pressed', state.date === dateKey(d) ? 'true' : 'false');
      b.innerHTML = '<span class="wd">' + wdNames[d.getDay()] + '</span><span class="dn">' + d.getDate() + '</span><span class="mo">' + moNames[d.getMonth()] + '</span>';
      b.setAttribute('aria-label', dateLabel(d));
      b.addEventListener('click', function () { state.date = dateKey(d); state.time = null; renderDates(); renderSlots(); update(); animateIn(slotWrap, false); });
      dateWrap.appendChild(b);
    });
  }

  function renderSlots() {
    slotWrap.innerHTML = '';
    if (!state.date) {
      slotWrap.innerHTML = '<p class="form-note">Choose a date to see sample times.</p>';
      return;
    }
    var di = 0;
    days.forEach(function (d, idx) { if (dateKey(d) === state.date) di = idx; });
    times.forEach(function (t, ti) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'slot';
      b.textContent = t;
      var taken = (di * 7 + ti * 3) % 5 === 0;
      if (taken) { b.disabled = true; b.setAttribute('aria-label', t + ', taken'); }
      b.setAttribute('aria-pressed', state.time === t ? 'true' : 'false');
      b.addEventListener('click', function () { state.time = t; renderSlots(); update(); });
      slotWrap.appendChild(b);
    });
  }

  /* ---------- step 3: details ---------- */
  var form = el('details-form');
  var fields = ['bk-name', 'bk-phone', 'bk-email'];
  function validDetails(focusFirst) {
    var ok = true;
    fields.forEach(function (id) {
      var f = el(id), err = el(id + '-err'), v = f.value.trim(), msg = '';
      if (id === 'bk-name' && !v) msg = 'Enter your name.';
      if (id === 'bk-phone' && v.replace(/\D/g, '').length < 9) msg = 'Enter a phone number with at least 9 digits.';
      if (id === 'bk-email' && v && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) msg = 'Enter a valid email address, or leave it blank.';
      f.setAttribute('aria-invalid', msg ? 'true' : 'false');
      err.textContent = msg;
      if (msg) { if (ok && focusFirst) f.focus(); ok = false; }
    });
    return ok;
  }

  /* ---------- summary + review ---------- */
  function priceNote(it) {
    return it.price === 'Varies' ? 'Price confirmed by the studio' : it.price;
  }
  var lastSummary = {};
  function setSum(id, text) {
    var el = document.getElementById(id);
    if (el.textContent !== text) { el.textContent = text; if (lastSummary[id] !== undefined) flash(el); }
    lastSummary[id] = text;
  }
  function update() {
    var it = state.item ? byId[state.item] : null;
    setSum('sum-treatment', it ? it.name : 'Not chosen yet');
    setSum('sum-cat', it ? it.catName : '');
    setSum('sum-when', state.date && state.time ? dateLabel(days.filter(function (d) { return dateKey(d) === state.date; })[0]) + ' at ' + state.time : 'Not chosen yet');
    setSum('sum-price', it ? priceNote(it) + (it.dur ? ', ' + it.dur : '') : '');
    el('next-treatment').disabled = !it;
    el('next-when').disabled = !(state.date && state.time);
  }

  function renderReview() {
    var it = byId[state.item];
    var d = days.filter(function (x) { return dateKey(x) === state.date; })[0];
    var rows = [
      ['Treatment', it.name + ' (' + it.catName + ')'],
      ['Duration', it.dur || 'To be confirmed'],
      ['Price', priceNote(it)],
      ['Date and time', dateLabel(d) + ' at ' + state.time],
      ['Name', el('bk-name').value.trim()],
      ['Phone', el('bk-phone').value.trim()],
      ['Email', el('bk-email').value.trim() || 'Not given']
    ];
    var ul = el('review-list');
    ul.innerHTML = '';
    rows.forEach(function (r) {
      var li = document.createElement('li');
      var k = document.createElement('span'); k.className = 'k'; k.textContent = r[0];
      var v = document.createElement('span'); v.className = 'v'; v.textContent = r[1];
      li.appendChild(k); li.appendChild(v); ul.appendChild(li);
    });
  }

  /* ---------- navigation between steps ---------- */
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function animateIn(el, back) {
    if (reduceMotion || !el) return;
    el.classList.remove('step-in', 'step-in-back');
    void el.offsetWidth;
    el.classList.add(back ? 'step-in-back' : 'step-in');
  }
  function flash(el) {
    if (reduceMotion || !el) return;
    el.classList.remove('flash');
    void el.offsetWidth;
    el.classList.add('flash');
  }
  function go(n) {
    var back = n < current;
    current = n;
    stepEls.forEach(function (s, i) { s.hidden = i !== n; });
    animateIn(stepEls[n], back);
    stepperItems.forEach(function (li, i) {
      li.classList.toggle('done', i < n);
      if (i === n) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current');
    });
    if (n === 3) renderReview();
    var h = stepEls[n].querySelector('h2');
    if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
    window.scrollTo({ top: Math.max(0, el('book-top').offsetTop - 20), behavior: 'smooth' });
  }

  el('next-treatment').addEventListener('click', function () { go(1); });
  el('back-when').addEventListener('click', function () { go(0); });
  el('next-when').addEventListener('click', function () { go(2); });
  el('back-details').addEventListener('click', function () { go(1); });
  form.addEventListener('submit', function (e) { e.preventDefault(); if (validDetails(true)) go(3); });
  el('back-review').addEventListener('click', function () { go(2); });
  el('confirm').addEventListener('click', function () {
    el('review-wrap').hidden = true;
    el('done').hidden = false;
    animateIn(el('done'), false);
    el('done').focus();
  });
  el('restart').addEventListener('click', function () {
    state.item = null; state.date = null; state.time = null;
    form.reset();
    el('done').hidden = true;
    el('review-wrap').hidden = false;
    renderItems(); renderDates(); renderSlots(); update(); go(0);
  });

  /* ---------- start (supports ?t=<treatment id> or ?c=<category slug>) ---------- */
  var q = new URLSearchParams(location.search);
  if (q.get('t') && byId[q.get('t')]) { state.item = q.get('t'); state.cat = byId[q.get('t')].cat; }
  else if (q.get('c') && catalog.some(function (c) { return c.slug === q.get('c'); })) { state.cat = q.get('c'); }
  renderCats(); renderItems(); renderDates(); renderSlots(); update();
  stepEls.forEach(function (s, i) { s.hidden = i !== 0; });
  stepperItems[0].setAttribute('aria-current', 'step');
})();
