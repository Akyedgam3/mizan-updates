# يولّد صفحات الموقع من قوالب مشتركة (الشريط العلوي والتذييل).
# الاستعمال: python3 tools/build_site.py   (من جذر المستودع)
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'pages')

SITE = 'https://akyedgam3.github.io/mizan-updates/'
DOWNLOAD = 'https://github.com/Akyedgam3/mizan-updates/releases/latest/download/Mizan-Setup.exe'
WA1, WA2 = '963968037609', '963980072891'
PH1, PH2 = '+963 968 037 609', '+963 980 072 891'


def icon(name, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} aria-hidden="true"><use href="assets/img/icons.svg#{name}"/></svg>'


NAV = [('index.html', 'الرئيسية'), ('index.html#sectors', 'المجالات'), ('index.html#features', 'المزايا'), ('index.html#videos', 'الفيديوهات'), ('agents.html', 'كن وكيلاً'), ('index.html#faq', 'أسئلة')]


def page(file, title, desc, body, active='', base=''):
    links = ''.join(f'<a href="{h}"{" class=on" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8" />
{f'<base href="{base}" />' if base else ''}
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<meta name="theme-color" content="#071a17" />
<link rel="icon" type="image/png" href="assets/img/favicon.png" />
<link rel="apple-touch-icon" href="assets/img/logo-256.png" />
<meta property="og:type" content="website" />
<meta property="og:locale" content="ar_SY" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{SITE}{file if file != 'index.html' else ''}" />
<meta property="og:image" content="{SITE}assets/img/og.jpg" />
<link rel="canonical" href="{SITE}{file if file != 'index.html' else ''}" />
<link rel="preload" href="assets/fonts/cairo-arabic-900-normal.woff2" as="font" type="font/woff2" crossorigin />
<link rel="stylesheet" href="assets/css/site.css?v=1" />
</head>
<body>
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/img/logo-256.png" alt="" width="40" height="40" />ميزان</a>
    <nav class="links" aria-label="القائمة">{links}</nav>
    <button class="menu-btn" aria-label="القائمة" aria-expanded="false">☰</button>
    <a class="btn primary sm" href="{DOWNLOAD}">{icon('download')}تحميل</a>
  </div>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="index.html"><img src="assets/img/logo-256.png" alt="" width="40" height="40" />ميزان</a>
        <p>برنامج محاسبة وإدارة محلات عربي لويندوز، بيشتغل بدون إنترنت. صُنع في سوريا لمحلات بلاد الشام.</p>
      </div>
      <div>
        <h4>البرنامج</h4>
        <a href="{DOWNLOAD}">تحميل ميزان</a>
        <a href="index.html#sectors">مجالات العمل</a>
        <a href="index.html#videos">فيديوهات الشرح</a>
        <a href="index.html#faq">الأسئلة الشائعة</a>
      </div>
      <div>
        <h4>الشركة</h4>
        <a href="agents.html">كن وكيلاً لميزان</a>
        <a href="terms.html">الشروط والأحكام</a>
        <a href="privacy.html">سياسة الخصوصية</a>
      </div>
      <div>
        <h4>تواصل معنا (واتساب)</h4>
        <a href="https://wa.me/{WA1}" rel="noopener"><span class="ltr">{PH1}</span></a>
        <a href="https://wa.me/{WA2}" rel="noopener"><span class="ltr">{PH2}</span></a>
      </div>
    </div>
    <div class="copy"><span>© <span data-year>2026</span> ميزان. جميع الحقوق محفوظة.</span><span>حساباتك صارت بميزان</span></div>
  </div>
</footer>
<a class="wa-float" href="https://wa.me/{WA1}" rel="noopener" aria-label="راسلنا واتساب">{icon('message-circle')}</a>
<script src="assets/js/site.js?v=1" defer></script>
</body>
</html>
'''


def render(name):
    raw = open(os.path.join(SRC, name), encoding='utf8').read()
    meta, body = raw.split('\n---\n', 1)
    m = dict(line.split(': ', 1) for line in meta.strip().splitlines())
    for k, v in {'DOWNLOAD': DOWNLOAD, 'WA1': WA1, 'WA2': WA2, 'PH1': PH1, 'PH2': PH2}.items():
        body = body.replace('{{' + k + '}}', v)
    import re
    body = re.sub(r'\{\{icon:([a-z0-9-]+)\}\}', lambda x: icon(x.group(1)), body)
    # صفحة 404 بتنفتح من أي مسار، فروابطها لازم تكون من جذر الموقع
    out = page(name, m['title'], m['description'], body, m.get('active', ''), m.get('base', ''))
    open(os.path.join(ROOT, name), 'w', encoding='utf8').write(out)
    print('built', name)


if __name__ == '__main__':
    for f in sorted(os.listdir(SRC)):
        if f.endswith('.html'):
            render(f)
