// تقييمات وزن: تسجيل دخول بغوغل (Firebase Auth) والتقييمات بـ Firestore (مجموعة reviews، مستند لكل مستخدم).
// العنصر #reviews-app بيحدد الشكل: data-mode="summary" (الرئيسية) أو "full" (صفحة التقييمات).
import { firebaseConfig } from './firebase-config.js';

const SDK = 'https://www.gstatic.com/firebasejs/10.12.2';
const root = document.getElementById('reviews-app');
const mode = root?.dataset.mode ?? 'summary';

const h = (tag, attrs = {}, ...kids) => {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') el.className = v;
    else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
    else if (v !== undefined && v !== null && v !== false) el.setAttribute(k, v === true ? '' : v);
  }
  for (const kid of kids.flat()) if (kid !== null && kid !== undefined && kid !== false) el.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
  return el;
};

const starsText = (n) => '★★★★★'.slice(0, n) + '☆☆☆☆☆'.slice(0, 5 - n);
const fmtDate = (ts) => {
  const d = ts?.toDate ? ts.toDate() : null;
  return d ? d.toLocaleDateString('en-GB') : '';
};

function message(text) {
  root.replaceChildren(h('div', { class: 'reviews-empty' }, text));
}

function summaryBlock(list) {
  const n = list.length;
  const avg = n ? list.reduce((s, r) => s + r.stars, 0) / n : 0;
  const dist = [5, 4, 3, 2, 1].map((s) => [s, list.filter((r) => r.stars === s).length]);
  return h(
    'div',
    { class: 'rv-summary' },
    h('div', { class: 'rv-score' }, h('b', {}, n ? avg.toFixed(1) : '—'), h('span', { class: 'rv-stars', 'aria-label': `${avg.toFixed(1)} من 5` }, starsText(Math.round(avg))), h('small', {}, n ? `${n} تقييم` : 'لا توجد تقييمات بعد')),
    h(
      'div',
      { class: 'rv-dist' },
      dist.map(([s, c]) => h('div', { class: 'rv-row' }, h('span', {}, `${s} ★`), h('i', {}, h('em', { style: `width:${n ? (c / n) * 100 : 0}%` })), h('small', {}, c))),
    ),
  );
}

function card(r, mine) {
  return h(
    'article',
    { class: `rv-card${mine ? ' mine' : ''}` },
    h(
      'header',
      {},
      r.photo ? h('img', { src: r.photo, alt: '', referrerpolicy: 'no-referrer', width: 40, height: 40, loading: 'lazy' }) : h('span', { class: 'rv-avatar' }, (r.name || '؟').slice(0, 1)),
      h('div', {}, h('strong', {}, r.name || 'مستخدم'), r.business ? h('small', {}, r.business) : null),
      h('span', { class: 'rv-stars sm' }, starsText(r.stars)),
    ),
    r.text ? h('p', {}, r.text) : null,
    h('time', {}, fmtDate(r.updatedAt || r.createdAt)),
  );
}

async function start() {
  if (!root) return;
  if (!firebaseConfig) {
    message(mode === 'full' ? 'التقييمات رح تنفتح قريباً. تابعنا!' : 'التقييمات رح تنفتح قريباً.');
    return;
  }
  message('جاري تحميل التقييمات...');
  const [{ initializeApp }, auth, fs] = await Promise.all([import(`${SDK}/firebase-app.js`), import(`${SDK}/firebase-auth.js`), import(`${SDK}/firebase-firestore.js`)]);
  const app = initializeApp(firebaseConfig);
  const db = fs.getFirestore(app);
  const au = auth.getAuth(app);
  au.languageCode = 'ar';
  let user = null;
  let list = [];

  const load = async () => {
    const q = fs.query(fs.collection(db, 'reviews'), fs.orderBy('createdAt', 'desc'), fs.limit(mode === 'full' ? 300 : 60));
    const snap = await fs.getDocs(q);
    list = snap.docs.map((d) => ({ id: d.id, ...d.data() })).filter((r) => Number.isInteger(r.stars) && r.stars >= 1 && r.stars <= 5);
  };

  const signIn = async () => {
    const provider = new auth.GoogleAuthProvider();
    try {
      await auth.signInWithPopup(au, provider);
    } catch (e) {
      // الموبايل أحياناً بيمنع النوافذ المنبثقة
      if (e?.code === 'auth/popup-blocked' || e?.code === 'auth/operation-not-supported-in-this-environment') await auth.signInWithRedirect(au, provider);
      else if (e?.code !== 'auth/popup-closed-by-user' && e?.code !== 'auth/cancelled-popup-request') alert('ما قدرنا نسجّل الدخول، جرّب مرة تانية.');
    }
  };

  const form = () => {
    const mine = list.find((r) => r.id === user.uid);
    let stars = mine?.stars ?? 0;
    const starBtns = [1, 2, 3, 4, 5].map((s) =>
      h('button', { type: 'button', class: 'rv-star', 'aria-label': `${s} نجوم`, onclick: () => ((stars = s), paint()) }, '★'),
    );
    const paint = () => starBtns.forEach((b, i) => b.classList.toggle('on', i < stars));
    const text = h('textarea', { maxlength: 600, rows: 4, placeholder: 'شو عجبك بوزن؟ وشو بتحب نضيف؟' });
    text.value = mine?.text ?? '';
    const business = h('input', { maxlength: 60, placeholder: 'نوع محلك والمدينة (اختياري) — مثلاً: سوبرماركت، حلب' });
    business.value = mine?.business ?? '';
    const status = h('small', { class: 'rv-status' });
    const save = async () => {
      if (!stars) return (status.textContent = 'اختار عدد النجوم أولاً');
      status.textContent = 'جاري الحفظ...';
      const data = {
        name: (user.displayName || 'مستخدم').slice(0, 60),
        stars,
        text: text.value.trim().slice(0, 600),
        updatedAt: fs.serverTimestamp(),
        createdAt: mine?.createdAt ?? fs.serverTimestamp(),
        ...(user.photoURL ? { photo: user.photoURL.slice(0, 500) } : {}),
        ...(business.value.trim() ? { business: business.value.trim().slice(0, 60) } : {}),
      };
      try {
        await fs.setDoc(fs.doc(db, 'reviews', user.uid), data);
        await load();
        render();
      } catch {
        status.textContent = 'ما انحفظ التقييم، جرّب مرة تانية.';
      }
    };
    const remove = async () => {
      if (!confirm('بدك تحذف تقييمك؟')) return;
      await fs.deleteDoc(fs.doc(db, 'reviews', user.uid));
      await load();
      render();
    };
    paint();
    return h(
      'div',
      { class: 'rv-form' },
      h('div', { class: 'rv-who' }, user.photoURL ? h('img', { src: user.photoURL, alt: '', referrerpolicy: 'no-referrer', width: 36, height: 36 }) : null, h('span', {}, `أهلاً ${user.displayName || ''}`), h('button', { type: 'button', class: 'link', onclick: () => auth.signOut(au) }, 'تسجيل الخروج')),
      h('h3', {}, mine ? 'عدّل تقييمك' : 'قيّم تجربتك مع وزن'),
      h('div', { class: 'rv-pick' }, starBtns),
      business,
      text,
      h('div', { class: 'rv-actions' }, h('button', { type: 'button', class: 'btn green', onclick: save }, mine ? 'حفظ التعديل' : 'نشر التقييم'), mine ? h('button', { type: 'button', class: 'link danger', onclick: remove }, 'حذف تقييمي') : null, status),
    );
  };

  const render = () => {
    const kids = [summaryBlock(list)];
    if (mode === 'full') {
      kids.push(
        user
          ? form()
          : h('div', { class: 'rv-login' }, h('p', {}, 'سجّل دخول بحساب غوغل لتقيّم وزن. ما منستعمل حسابك لأي شي غير اسمك وصورتك جنب تقييمك.'), h('button', { type: 'button', class: 'btn green', onclick: signIn }, h('span', { class: 'g' }, 'G'), 'تسجيل الدخول بغوغل')),
      );
    }
    const shown = mode === 'full' ? list : list.filter((r) => r.text).slice(0, 3);
    kids.push(shown.length ? h('div', { class: 'rv-list' }, shown.map((r) => card(r, user && r.id === user.uid))) : null);
    root.replaceChildren(...kids.filter(Boolean));
  };

  try {
    await load();
  } catch {
    message('ما قدرنا نحمّل التقييمات هلق.');
    return;
  }
  render();
  auth.onAuthStateChanged(au, (u) => {
    user = u;
    render();
  });
  if (mode === 'full') auth.getRedirectResult(au).catch(() => {});
}

void start();
