# يولّد صفحات الموقع من قوالب مشتركة (الشريط العلوي والتذييل).
# الاستعمال: python3 tools/build_site.py   (من جذر المستودع)
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'pages')

SITE = 'https://waznsy.com/'
DOWNLOAD = 'https://waznsy.com/dl/Wazn-Setup.exe'
APK = 'https://waznsy.com/dl/Wazn.apk'
WA1, WA2 = '963968037609', '963980072891'
PH1, PH2 = '+963 968 037 609', '+963 980 072 891'
EMAIL = 'info@waznsy.com'
# رقم آخر نسخة: بيتحدّث لحالو من scripts/publish-release.sh بمستودع البرنامج
VERSION = open(os.path.join(ROOT, 'tools', 'version.txt'), encoding='utf8').read().strip()


def icon(name, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} aria-hidden="true"><use href="assets/img/icons.svg#{name}"/></svg>'


NAV = [('index.html', 'الرئيسية'), ('sectors.html', 'المجالات'), ('index.html#features', 'المزايا'), ('index.html#pricing', 'الاشتراك'), ('index.html#videos', 'فيديوهات'), ('reviews.html', 'التقييمات'), ('agents.html', 'كن وكيلاً'), ('index.html#faq', 'أسئلة')]


def page(file, title, desc, body, active='', base='', head=''):
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
<link rel="canonical" href="{SITE}{file if file != 'index.html' else ''}" />{'<meta name="robots" content="noindex" />' if file == '404.html' else ''}{head}
<link rel="preload" href="assets/fonts/cairo-arabic-900-normal.woff2" as="font" type="font/woff2" crossorigin />
<link rel="stylesheet" href="assets/css/site.css?v=13" />
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
        <a href="privacy.html#en" lang="en">Privacy Policy (English)</a>
      </div>
      <div>
        <h4>تواصل معنا</h4>
        <a href="https://wa.me/{WA1}" rel="noopener"><span class="ltr">{PH1}</span></a>
        <a href="https://wa.me/{WA2}" rel="noopener"><span class="ltr">{PH2}</span></a>
        <a href="mailto:{EMAIL}"><span class="ltr">{EMAIL}</span></a>
      </div>
    </div>
    <div class="copy"><span>© <span data-year>2026</span> وزن (Wazn). جميع الحقوق محفوظة.</span><span class="team">مدير فريق تطبيق وزن: أغيد بهلول</span><span>كل شي بوزنه</span></div>
  </div>
</footer>
<a class="wa-float" href="https://wa.me/{WA1}" rel="noopener" aria-label="راسلنا واتساب">{icon('message-circle')}</a>
<script src="assets/js/site.js?v=5" defer></script>
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

from sectors import SECTORS

# الصفحات اللي بدنا غوغل يلاقيها (404 وget ما بتنفهرس)
SITEMAP_PAGES = [('', '1.0', 'weekly'), ('sectors.html', '0.9', 'monthly')] + [(f"{x['slug']}.html", '0.8', 'monthly') for x in SECTORS] + [('agents.html', '0.8', 'monthly'), ('reviews.html', '0.7', 'weekly'), ('update.html', '0.6', 'weekly'), ('terms.html', '0.3', 'yearly'), ('privacy.html', '0.3', 'yearly')]


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def ld(obj):
    return '\n<script type="application/ld+json">' + _json.dumps(obj, ensure_ascii=False) + '</script>'


def crumbs(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(items)]}


def sector_page(x):
    """صفحة مجال: مقدمة، ميزات خاصة بالمجال، كيف بيمشي اليوم، أسئلة، ومجالات تانية."""
    feats = ''.join(f'<div class="sector reveal"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in x['features'])
    steps = ''.join(f'<li>{icon("circle-check-big")}{esc(st)}</li>' for st in x['steps'])
    faq = ''.join(f'<details class="reveal"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in x['faq'])
    others = ''.join(f'<a class="chip" href="{o["slug"]}.html">{icon(o["icon"])}{esc(o["name"])}</a>' for o in SECTORS if o['slug'] != x['slug'])
    img, alt = x['shot']
    body = f'''<div class="dark">
  <div class="blob a"></div><div class="blob b"></div><div class="grid-bg"></div>
  <div class="page-hero">
    <div class="wrap reveal">
      <nav class="crumbs" aria-label="المسار"><a href="index.html">الرئيسية</a> ‹ <a href="sectors.html">المجالات</a> ‹ <span>{esc(x['name'])}</span></nav>
      <h1>{esc(x['h1'])}</h1>
      <p>{esc(x['intro'])}</p>
      <div class="cta"><a class="btn primary" href="{DOWNLOAD}">{icon('download')}تحميل وزن لويندوز</a><a class="btn ghost" href="{APK}">{icon('smartphone')}تطبيق أندرويد</a><a class="btn ghost" href="https://wa.me/{WA1}" rel="noopener">{icon('message-circle')}جرّبه ببلاش، راسلنا</a></div>
    </div>
  </div>
  <div style="height:40px"></div>
</div>

<section>
  <div class="wrap">
    <div class="feature">
      <div class="ftxt reveal">
        <div class="tag">{esc(x['name'])}</div>
        <h2>كيف بيمشي يومك مع وزن</h2>
        <ul class="checks">{steps}</ul>
        <p>وكل شي بيشتغل بدون إنترنت، والبيانات محفوظة على جهازك ومشفّرة. بالليرة والدولار، بفواتير بشعار محلك، وتقارير أرباح وديون وصندوق.</p>
      </div>
      <div class="reveal d2"><div class="shot"><img src="assets/img/{img}" alt="{esc(alt)}" width="1200" height="750" loading="lazy" /></div></div>
    </div>
  </div>
</section>

<section style="background:#fff">
  <div class="wrap">
    <div class="head reveal"><div class="tag">مخصص لـ {esc(x['name'])}</div><h2>شو بيعطيك وزن بالزبط</h2></div>
    <div class="sectors">{feats}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head reveal"><div class="tag">أسئلة</div><h2>أسئلة أصحاب محلات {esc(x['name'])}</h2></div>
    <div class="faq">{faq}<details class="reveal"><summary>بيشتغل بدون إنترنت؟</summary><p>إي، كل الشغل على جهازك. البرنامج بس بيتصل كل كم يوم ليتأكد من الاشتراك ويشوف التحديثات.</p></details><details class="reveal"><summary>كيف بجرّبه؟</summary><p>نزّل البرنامج وراسلنا واتساب، ومنفعّلك نسخة تجريبية مع بيانات تجريبية لمجالك.</p></details></div>
  </div>
</section>

<section style="background:#fff">
  <div class="wrap">
    <div class="head reveal"><div class="tag">برنامج واحد لكل المجالات</div><h2>مجالات تانية بيخدمها وزن</h2></div>
    <div class="chips reveal">{others}</div>
  </div>
</section>'''
    head = ld(crumbs([('الرئيسية', ''), ('المجالات', 'sectors.html'), (x['name'], f"{x['slug']}.html")]))
    head += ld({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in x['faq']]})
    out = page(f"{x['slug']}.html", x['title'], x['description'], body, 'sectors.html', '', head)
    open(os.path.join(ROOT, f"{x['slug']}.html"), 'w', encoding='utf8').write(out)
    print('built', x['slug'] + '.html')


def sectors_hub():
    cards = ''.join(f'<a class="sector reveal" href="{x["slug"]}.html"><div class="ic">{icon(x["icon"])}</div><h3>{esc(x["name"])}</h3><p>{esc(x["description"].split(":")[0])}</p></a>' for x in SECTORS)
    body = f'''<div class="dark">
  <div class="blob a"></div><div class="blob b"></div><div class="grid-bg"></div>
  <div class="page-hero"><div class="wrap reveal">
    <h1>برنامج محاسبة لكل مجال</h1>
    <p>«وزن» برنامج واحد بيتجهّز حسب نوع شغلك: وقت إنشاء الشركة بتختار مجالك، فبتطلعلك الشاشات والميزات اللي بتلزمك. اختار مجالك لتشوف شو بيعطيك بالزبط.</p>
  </div></div>
  <div style="height:40px"></div>
</div>
<section><div class="wrap"><div class="sectors">{cards}</div></div></section>'''
    out = page('sectors.html', 'برنامج محاسبة لكل مجال: سوبرماركت، مطاعم، صيدليات وغيرها — وزن', 'اختار مجال شغلك وشوف كيف بيخدمه برنامج وزن للمحاسبة وإدارة المحلات: سوبرماركت، مطاعم، صيدليات، موبايلات، ألبسة، قطع غيار، مواد بناء، خضار ولحوم، حلويات، جملة، خياطة وكهربائيات.', body, 'sectors.html', '', ld(crumbs([('الرئيسية', ''), ('المجالات', 'sectors.html')])))
    open(os.path.join(ROOT, 'sectors.html'), 'w', encoding='utf8').write(out)
    print('built sectors.html')


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
    for x in SECTORS:
        sector_page(x)
    sectors_hub()
    seo_files()
