/* atrakcjeegiptu.pl shared interactions */
(function () {
  var header = document.querySelector('.site-header');
  var hasHero = !!document.querySelector('.hero');
  function onScroll() {
    if (!header) return;
    header.classList.toggle('solid', !hasHero || window.scrollY > 40);
  }
  onScroll();
  addEventListener('scroll', onScroll, { passive: true });

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });

  // reveal fallback where CSS scroll-driven animations are unsupported
  if (!CSS.supports('animation-timeline: view()')) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.rv').forEach(function (el) { el.classList.add('in'); });
  }

  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // horizontal rails
  document.querySelectorAll('.rail-wrap').forEach(function (w) {
    var rail = w.querySelector('.rail');
    w.querySelectorAll('.rail-nav button').forEach(function (b) {
      b.addEventListener('click', function () {
        rail.scrollBy({ left: (b.dataset.dir === 'next' ? 1 : -1) * (rail.clientWidth * 0.85), behavior: reduce ? 'auto' : 'smooth' });
      });
    });
  });

  // count-up stats
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var target = parseInt(el.dataset.count, 10);
    if (reduce) return; // HTML already shows the final value
    el.textContent = '0';
    var done = false;
    new IntersectionObserver(function (es, obs) {
      if (!es[0].isIntersecting || done) return;
      done = true; obs.disconnect();
      var t0 = performance.now(), dur = 1400;
      (function tick(t) {
        var p = Math.min((t - t0) / dur, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
    }, { threshold: 0.6 }).observe(el);
  });
})();
