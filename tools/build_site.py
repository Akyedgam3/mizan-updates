# يولّد صفحات الموقع من قوالب مشتركة (الشريط العلوي والتذييل).
# الاستعمال: python3 tools/build_site.py   (من جذر المستودع)
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'pages')

SITE = 'https://waznsy.com/'
DOWNLOAD = 'https://github.com/Akyedgam3/mizan-updates/releases/latest/download/Wazn-Setup.exe'
APK = 'https://github.com/Akyedgam3/mizan-updates/releases/latest/download/Wazn.apk'
WA1, WA2 = '963968037609', '963980072891'
PH1, PH2 = '+963 968 037 609', '+963 980 072 891'
EMAIL = 'info@waznsy.com'
# رقم آخر نسخة: بيتحدّث لحالو من scripts/publish-release.sh بمستودع البرنامج
VERSION = open(os.path.join(ROOT, 'tools', 'version.txt'), encoding='utf8').read().strip()


def icon(name, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} aria-hidden="true"><use href="assets/img/icons.svg#{name}"/></svg>'


NAV = [('index.html', 'الرئيسية'), ('index.html#sectors', 'المجالات'), ('index.html#features', 'المزايا'), ('index.html#pricing', 'الاشتراك'), ('index.html#videos', 'فيديوهات'), ('reviews.html', 'التقييمات'), ('agents.html', 'كن وكيلاً'), ('index.html#faq', 'أسئلة')]


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
<link rel="stylesheet" href="assets/css/site.css?v=10" />
</head>
<body>
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/img/logo-256.png" alt="" width="40" height="40" />وزن</a>
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
        <a class="brand" href="index.html"><img src="assets/img/logo-256.png" alt="" width="40" height="40" />وزن</a>
        <p>برنامج محاسبة وإدارة محلات عربي لويندوز، بيشتغل بدون إنترنت. صُنع في سوريا لمحلات بلاد الشام.</p>
      </div>
      <div>
        <h4>البرنامج</h4>
        <a href="{DOWNLOAD}">تحميل وزن للكمبيوتر</a>
        <a href="{APK}">تطبيق وزن لأندرويد</a>
        <a href="index.html#sectors">مجالات العمل</a>
        <a href="reviews.html">تقييمات الزباين</a>
        <a href="index.html#pricing">الاشتراك</a>
        <a href="index.html#faq">الأسئلة الشائعة</a>
      </div>
      <div>
        <h4>الشركة</h4>
        <a href="agents.html">كن وكيلاً لوزن</a>
        <a href="terms.html">الشروط والأحكام</a>
        <a href="privacy.html">سياسة الخصوصية</a>
      </div>
      <div>
        <h4>تواصل معنا</h4>
        <a href="https://wa.me/{WA1}" rel="noopener"><span class="ltr">{PH1}</span></a>
        <a href="https://wa.me/{WA2}" rel="noopener"><span class="ltr">{PH2}</span></a>
        <a href="mailto:{EMAIL}"><span class="ltr">{EMAIL}</span></a>
      </div>
    </div>
    <div class="copy"><span>© <span data-year>2026</span> وزن. جميع الحقوق محفوظة.</span><span class="team">مدير فريق تطبيق وزن: أغيد بهلول</span><span>كل شي بوزنه</span></div>
  </div>
</footer>
<a class="wa-float" href="https://wa.me/{WA1}" rel="noopener" aria-label="راسلنا واتساب">{icon('message-circle')}</a>
<script src="assets/js/site.js?v=2" defer></script>
</body>
</html>
'''


def render(name):
    raw = open(os.path.join(SRC, name), encoding='utf8').read()
    meta, body = raw.split('\n---\n', 1)
    m = dict(line.split(': ', 1) for line in meta.strip().splitlines())
    for k, v in {'DOWNLOAD': DOWNLOAD, 'APK': APK, 'WA1': WA1, 'WA2': WA2, 'PH1': PH1, 'PH2': PH2, 'EMAIL': EMAIL, 'VERSION': VERSION}.items():
        body = body.replace('{{' + k + '}}', v)
    import re
    body = re.sub(r'\{\{icon:([a-z0-9-]+)\}\}', lambda x: icon(x.group(1)), body)
    # صفحة 404 بتنفتح من أي مسار، فروابطها لازم تكون من جذر الموقع
    fill = lambda t: t.replace('{{VERSION}}', VERSION)
    out = page(name, fill(m['title']), fill(m['description']), body, m.get('active', ''), m.get('base', ''))
    if name == 'index.html':
        out = out.replace('</head>', LD_JSON + '\n</head>', 1)
    open(os.path.join(ROOT, name), 'w', encoding='utf8').write(out)
    print('built', name)


# بيانات منظّمة لمحركات البحث (غوغل بيفهم إنو هاد برنامج، وبيعرض اسمه وشعاره صح)
import json as _json
LD_JSON = '<script type="application/ld+json">' + _json.dumps([
    {
        '@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': 'وزن', 'alternateName': ['Wazn', 'برنامج وزن للمحاسبة'],
        'url': SITE, 'image': SITE + 'assets/img/logo-256.png', 'inLanguage': 'ar',
        'applicationCategory': 'BusinessApplication', 'applicationSubCategory': 'برنامج محاسبة وإدارة محلات',
        'operatingSystem': 'Windows, Android', 'softwareVersion': VERSION, 'downloadUrl': DOWNLOAD,
        'description': 'برنامج محاسبة وإدارة محلات عربي يشتغل بدون إنترنت: فواتير، مخزون، ديون، نقطة بيع، مطاعم، ورش، صيدليات، بالليرة والدولار.',
    },
    {
        '@context': 'https://schema.org', '@type': 'Organization', 'name': 'وزن', 'url': SITE, 'logo': SITE + 'assets/img/logo-256.png', 'email': EMAIL,
        'contactPoint': [{'@type': 'ContactPoint', 'telephone': PH1.replace(' ', ''), 'contactType': 'customer service', 'areaServed': 'SY', 'availableLanguage': 'ar'}],
    },
], ensure_ascii=False) + '</script>'

# الصفحات اللي بدنا غوغل يلاقيها (404 وget ما بتنفهرس)
SITEMAP_PAGES = [('', '1.0', 'weekly'), ('agents.html', '0.8', 'monthly'), ('reviews.html', '0.7', 'weekly'), ('update.html', '0.6', 'weekly'), ('terms.html', '0.3', 'yearly'), ('privacy.html', '0.3', 'yearly')]


def seo_files():
    import datetime
    today = datetime.date.today().isoformat()
    urls = ''.join(f'  <url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n' for p, pr, c in SITEMAP_PAGES)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf8').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf8').write(f'User-agent: *\nAllow: /\nDisallow: /release/\nDisallow: /get.html\n\nSitemap: {SITE}sitemap.xml\n')
    print('built sitemap.xml, robots.txt')


if __name__ == '__main__':
    for f in sorted(os.listdir(SRC)):
        if f.endswith('.html'):
            render(f)
    seo_files()
