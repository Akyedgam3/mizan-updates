// وزن — حركات الموقع بدون مكتبات.
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

  // ───── 3D مع التمرير والماوس (بس transform، وكل شي بينطفى مع «تقليل الحركة») ─────
  if (!still) {
    const fine = matchMedia('(pointer: fine)').matches;
    const clamp = (v) => Math.max(0, Math.min(1, v));
    const dev = $('.hero .device');
    const scr = dev && $('.screen', dev);
    const floats = dev ? $$('.float', dev) : [];
    const stage = $('.stage3d');
    const ring = stage && $('.ring', stage);
    const faces = stage ? $$('.face', stage) : [];
    const cap = stage && $('.stage-cap', stage);
    const bar = stage && $('.stage-bar', stage);
    let mx = 0;
    let my = 0;
    let active = -1;
    let ticking = false;
    const frame = () => {
      ticking = false;
      // الشاشة بالواجهة: مع النزول بتميل لورا وبتبعد، والبطاقات العايمة بتطير بسرعات مختلفة (عمق)
      if (scr) {
        const h = clamp(scrollY / (innerHeight * 0.9));
        scr.style.transform = 'translateZ(' + -160 * h + 'px) rotateX(' + (4 + 22 * h - my * 5) + 'deg) rotateY(' + (-8 + 8 * h + mx * 7) + 'deg) scale(' + (1 - 0.06 * h) + ')';
        floats.forEach((f, i) => {
          const depth = [1.4, 0.9, 1.9][i % 3];
          f.style.transform = 'translate3d(' + mx * 14 * depth + 'px, ' + (-120 * h * depth + my * 10 * depth) + 'px, ' + 60 * depth + 'px) rotate(' + (i - 1) * 6 * h + 'deg)';
          f.style.opacity = String(1 - h * 0.85);
        });
      }
      // حلقة الشاشات: كل ما تنزل بتلفّ، والشاشة اللي قدام بتنضوي
      if (ring && faces.length) {
        const r = stage.getBoundingClientRect();
        const p = clamp(-r.top / (r.height - innerHeight));
        const n = faces.length;
        ring.style.setProperty('--rot', -p * 360 * ((n - 1) / n) + 'deg');
        ring.style.setProperty('--rx', -6 + my * 4 + 'deg');
        if (bar) bar.style.setProperty('--p', String(p));
        const i = Math.round(p * (n - 1));
        if (i !== active) {
          active = i;
          faces.forEach((f, j) => f.classList.toggle('dim', j !== i));
          const c = $('figcaption', faces[i]);
          if (cap && c) cap.textContent = c.textContent;
        }
      }
    };
    const kick = () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(frame);
      }
    };
    addEventListener('scroll', kick, { passive: true });
    addEventListener('resize', kick);
    if (fine) {
      addEventListener(
        'mousemove',
        (e) => {
          mx = e.clientX / innerWidth - 0.5;
          my = e.clientY / innerHeight - 0.5;
          kick();
        },
        { passive: true },
      );
      // البطاقات بتميل باتجاه الماوس
      $$('.sector').forEach((c) => {
        c.addEventListener('mousemove', (e) => {
          const b = c.getBoundingClientRect();
          const x = (e.clientX - b.left) / b.width - 0.5;
          const y = (e.clientY - b.top) / b.height - 0.5;
          c.classList.add('tilting');
          c.style.transform = 'perspective(700px) rotateX(' + -y * 10 + 'deg) rotateY(' + x * 12 + 'deg) translateY(-4px)';
        });
        c.addEventListener('mouseleave', () => {
          c.classList.remove('tilting');
          c.style.transform = '';
        });
      });
    }
    if (dev) dev.classList.add('tilt');
    frame();
  }

  // سنة حقوق النشر
  $$('[data-year]').forEach((el) => (el.textContent = new Date().getFullYear()));

  // زر التحميل: اختيار ويندوز 64 بت (الأغلب) أو 32 بت (الأجهزة القديمة)
  const SETUP = /\/(Wazn|Mizan|Miyar)-Setup\.exe$/i;
  const URL32 = 'https://waznsy.com/dl/Wazn-Setup-32bit.exe';
  let dl = null;
  const pick = (url64) => {
    if (!dl) {
      dl = document.createElement('dialog');
      dl.className = 'dl-pick';
      dl.innerHTML =
        '<form method="dialog">' +
        '<button class="dl-x" aria-label="إغلاق">×</button>' +
        '<h3>اختار نسخة ويندوز</h3>' +
        '<a class="dl-opt main" data-arch="64"><b>ويندوز 64 بت</b><small>لأغلب الأجهزة. إذا مو متأكد اختار هي</small></a>' +
        '<a class="dl-opt" data-arch="32" href="' + URL32 + '"><b>ويندوز 32 بت</b><small>للأجهزة القديمة (ويندوز 10 بنظام 32 بت)</small></a>' +
        '<p class="dl-how">كيف بعرف؟ من <b>الإعدادات ← النظام ← حول</b>، شوف «نوع النظام». إذا نزّلت 64 بت وطلعتلك رسالة إنو ما بيشتغل على هالجهاز، نزّل 32 بت.</p>' +
        '</form>';
      document.body.append(dl);
      dl.addEventListener('click', (e) => { if (e.target === dl) dl.close(); });
      $$('.dl-opt', dl).forEach((a) => a.addEventListener('click', () => setTimeout(() => dl.close(), 300)));
    }
    $('.dl-opt.main', dl).href = url64;
    dl.showModal();
  };
  document.addEventListener('click', (e) => {
    const a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.closest('.dl-pick') || !SETUP.test(a.getAttribute('href')) || typeof HTMLDialogElement !== 'function') return;
    e.preventDefault();
    pick(a.href);
  });
})();
