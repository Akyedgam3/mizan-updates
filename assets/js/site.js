// وزن — سكربت الموقع: القائمة عالجوال، تبويبات صور الميزات، واختيار نسخة ويندوز. بدون حركات.
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // قائمة الجوال
  const btn = $('.menu-btn');
  const links = $('.links');
  if (btn && links) {
    btn.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });
    $$('a', links).forEach((a) => a.addEventListener('click', () => links.classList.remove('open')));
  }

  // تبويبات الصور ضمن الميزة
  $$('[data-tabs]').forEach((box) => {
    const img = $('img', box.closest('.feature'));
    $$('button', box).forEach((b) =>
      b.addEventListener('click', () => {
        $$('button', box).forEach((x) => {
          x.classList.toggle('on', x === b);
          x.setAttribute('aria-pressed', String(x === b));
        });
        img.style.opacity = '0';
        img.onload = () => (img.style.opacity = '1');
        img.src = b.dataset.src;
        img.alt = b.textContent;
      }),
    );
  });

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
        '<h3>اختار نسختك</h3>' +
        '<a class="dl-opt main" data-arch="64"><b>ويندوز 64 بت</b><small>لأغلب الأجهزة. إذا مو متأكد اختار هي</small></a>' +
        '<a class="dl-opt" data-arch="32" href="' + URL32 + '"><b>ويندوز 32 بت</b><small>للأجهزة القديمة (ويندوز 10 بنظام 32 بت)</small></a>' +
        '<p class="dl-sep">أو على الجوال</p>' +
        '<a class="dl-opt" href="https://waznsy.com/dl/Wazn.apk"><b>أندرويد</b><small>تطبيق وزن الكامل (أندرويد 7 وأحدث)</small></a>' +
        '<a class="dl-opt" href="https://waznsy.com/app/"><b>آيفون</b><small>افتحه بسفاري وضيفه عالشاشة الرئيسية</small></a>' +
        '<p class="dl-how">كيف بعرف؟ من <b>الإعدادات ← النظام ← حول</b>، شوف «نوع النظام». إذا نزّلت 64 بت وطلعتلك رسالة إنو ما بيشتغل على هالجهاز، نزّل 32 بت.</p>' +
        '</form>';
      document.body.append(dl);
      dl.addEventListener('click', (e) => {
        if (e.target === dl) dl.close();
      });
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
