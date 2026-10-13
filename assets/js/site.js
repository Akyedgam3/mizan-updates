// ميزان — حركات خفيفة للموقع بدون مكتبات.
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // الشريط العلوي بيصير معتم مع التمرير
  const nav = $('.nav');
  const onScroll = () => nav && nav.classList.toggle('solid', scrollY > 30);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // قائمة الموبايل
  const btn = $('.menu-btn');
  const links = $('.links');
  if (btn && links) {
    btn.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });
    $$('a', links).forEach((a) => a.addEventListener('click', () => links.classList.remove('open')));
  }

  // الظهور مع التمرير
  if ('IntersectionObserver' in window && !still) {
    const io = new IntersectionObserver(
      (es) => es.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      }),
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' },
    );
    $$('.reveal').forEach((el) => io.observe(el));
  } else {
    $$('.reveal').forEach((el) => el.classList.add('in'));
  }

  // صور البرنامج بالواجهة بتتبدل لحالها
  const shots = $$('.shots img');
  if (shots.length > 1 && !still) {
    let i = 0;
    setInterval(() => {
      shots[i].classList.remove('on');
      i = (i + 1) % shots.length;
      shots[i].classList.add('on');
      const cap = $('.screen .bar b');
      if (cap && shots[i].dataset.cap) cap.textContent = shots[i].dataset.cap;
    }, 3600);
  }

  // عدّادات الأرقام
  const counters = $$('[data-count]');
  const run = (el) => {
    const to = Number(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    if (still) return (el.textContent = to + suffix);
    const t0 = performance.now();
    const step = (t) => {
      const p = Math.min(1, (t - t0) / 1400);
      el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))) + suffix;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if ('IntersectionObserver' in window) {
    const co = new IntersectionObserver((es) => es.forEach((e) => e.isIntersecting && (run(e.target), co.unobserve(e.target))), { threshold: 0.6 });
    counters.forEach((c) => co.observe(c));
  } else counters.forEach(run);

  // تبويبات الصور ضمن الميزة
  $$('[data-tabs]').forEach((box) => {
    const img = $('img', box.closest('.feature'));
    const pill = $('.pill', box.closest('.feature'));
    $$('button', box).forEach((b) =>
      b.addEventListener('click', () => {
        $$('button', box).forEach((x) => x.classList.toggle('on', x === b));
        img.style.opacity = '0';
        setTimeout(() => {
          img.src = b.dataset.src;
          img.alt = b.textContent;
          if (pill) pill.textContent = b.textContent;
          img.onload = () => (img.style.opacity = '1');
        }, 180);
      }),
    );
  });

  // سنة حقوق النشر
  $$('[data-year]').forEach((el) => (el.textContent = new Date().getFullYear()));
})();
