/* Mobile navigation toggle + tap-friendly dropdown */
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.main-nav');

    if (toggle && nav) {
      toggle.addEventListener('click', function () {
        var open = nav.classList.toggle('open');
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      });

      // Close the drawer after tapping any link
      nav.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () {
          nav.classList.remove('open');
          toggle.setAttribute('aria-expanded', 'false');
        });
      });
    }

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav) {
        nav.classList.remove('open');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      }
    });
  });
})();

/* Lupa na obrázky projektu.
   Náhľady sú zmenšené a neorezané, detail sa pozerá kliknutím. Odkazy vedú
   priamo na súbor s obrázkom, takže bez JavaScriptu sa obrázok otvorí sám
   a stránka ostane použiteľná. */
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var links = Array.prototype.slice.call(document.querySelectorAll('a.zoom'));
    if (!links.length) return;

    var box = document.createElement('div');
    box.className = 'lbx';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Zväčšený obrázok');
    box.innerHTML =
      '<button class="lbx-btn lbx-close" type="button" aria-label="Zavrieť">&#10005;</button>' +
      '<button class="lbx-btn lbx-prev" type="button" aria-label="Predchádzajúci obrázok">&#8249;</button>' +
      '<button class="lbx-btn lbx-next" type="button" aria-label="Ďalší obrázok">&#8250;</button>' +
      '<figure class="lbx-fig"><img alt=""><figcaption class="lbx-cap"></figcaption></figure>';
    document.body.appendChild(box);

    var img = box.querySelector('img');
    var cap = box.querySelector('.lbx-cap');
    var fig = box.querySelector('.lbx-fig');
    var btnClose = box.querySelector('.lbx-close');
    var btnPrev = box.querySelector('.lbx-prev');
    var btnNext = box.querySelector('.lbx-next');
    var many = links.length > 1;
    var at = 0;
    var lastFocus = null;

    btnPrev.hidden = !many;
    btnNext.hidden = !many;

    function show(i) {
      at = (i + links.length) % links.length;
      var a = links[at];
      img.src = a.getAttribute('href');
      img.alt = a.getAttribute('data-cap') || '';
      cap.textContent = a.getAttribute('data-cap') || '';
    }

    function open(i) {
      lastFocus = document.activeElement;
      show(i);
      box.classList.add('open');
      document.body.classList.add('lbx-lock');
      btnClose.focus();
    }

    function close() {
      box.classList.remove('open');
      document.body.classList.remove('lbx-lock');
      img.removeAttribute('src');
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    links.forEach(function (a, i) {
      a.addEventListener('click', function (e) {
        // Otvorenie v novom paneli necháme prehliadaču.
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
        e.preventDefault();
        open(i);
      });
    });

    btnClose.addEventListener('click', close);
    btnPrev.addEventListener('click', function () { show(at - 1); });
    btnNext.addEventListener('click', function () { show(at + 1); });
    box.addEventListener('click', function (e) {
      if (e.target === box || e.target === fig) close();
    });

    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('open')) return;
      if (e.key === 'Escape') { e.stopPropagation(); close(); }
      else if (e.key === 'ArrowLeft' && many) show(at - 1);
      else if (e.key === 'ArrowRight' && many) show(at + 1);
      else if (e.key === 'Tab') {
        // Kým je dialóg otvorený, fokus z neho nesmie vypadnúť.
        var f = Array.prototype.filter.call(box.querySelectorAll('.lbx-btn'),
                                            function (b) { return !b.hidden; });
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    }, true);
  });
})();
