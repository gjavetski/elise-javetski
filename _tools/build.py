"""Build the four public pages from _src/site.html.

_src/site.html holds every page section in one file (that's where edits go).
This script writes one HTML file per page so each gets its own address, title,
description and search data:

    /                index.html
    /coaching/       coaching/index.html
    /training-tips/  training-tips/index.html
    /get-started/    get-started/index.html

Run from the repo root:  python3 _tools/build.py
"""
import datetime
import json
import os
import re

SITE = 'https://elisejavetski.com'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = {
    'home': {
        'path': '/', 'out': 'index.html',
        'title': 'Prenatal & Postpartum Trainer in Jersey City',
        'desc': 'Strength training for pregnancy and after baby in Jersey City: 1-on-1 coaching in person or online, weekly group classes for moms, and assisted stretching.',
        'schema': lambda g: g.get('@type') != 'FAQPage',
    },
    'services': {
        'path': '/coaching/', 'out': 'coaching/index.html',
        'title': 'Group Classes & 1-on-1 Coaching for Moms',
        'desc': 'Group strength classes and 1-on-1 private coaching for pregnant and postpartum moms with Elise Javetski in Jersey City, in person or online. See the weekly class schedule.',
        'schema': lambda g: g.get('@id', '').endswith('#business'),
    },
    'action': {
        'path': '/training-tips/', 'out': 'training-tips/index.html',
        'title': 'Prenatal & Postpartum Training Tips',
        'desc': 'Free prenatal and postpartum training tips from Jersey City strength coach Elise Javetski: core and pelvic floor, breathing, stretching and strength basics.',
        'schema': lambda g: False,
    },
    'book': {
        'path': '/get-started/', 'out': 'get-started/index.html',
        'title': 'Book Prenatal & Postpartum Coaching',
        'desc': 'Get started with Elise Javetski, prenatal and postpartum strength coach in Jersey City. Send a message, see 1-on-1 pricing and read common questions.',
        'schema': lambda g: g.get('@type') == 'FAQPage',
    },
}
HASH_TO_PATH = {'#home': '/', '#services': '/coaching/', '#action': '/training-tips/', '#book': '/get-started/'}


def page_block(html, key):
    m = re.search(r'<div class="page" data-page="%s">.*?\n</div>\n' % key, html, re.S)
    assert m, key
    return m.group(0)


def set_meta(html, attr, name, value):
    pat = r'<meta %s="%s" content="[^"]*">' % (attr, re.escape(name))
    new = '<meta %s="%s" content="%s">' % (attr, name, value)
    assert re.search(pat, html), name
    return re.sub(pat, lambda _: new, html, count=1)


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')


def build():
    src = open(os.path.join(ROOT, '_src/site.html'), encoding='utf-8').read()
    main_start = src.index('<main id="main">') + len('<main id="main">')
    main_end = src.index('</main>')
    blocks = {k: page_block(src, k) for k in PAGES}
    shared = dict((k, v) for v, k in re.findall(r'<img[^>]* src="([^"]+)" data-src0="([^"]+)"', src))

    ld_start = src.index('<script type="application/ld+json">') + len('<script type="application/ld+json">')
    ld_end = src.index('</script>', ld_start)
    graph = json.loads(src[ld_start:ld_end])['@graph']

    for key, cfg in PAGES.items():
        h = src[:main_start] + '\n' + blocks[key] + src[main_end:]
        url = SITE + cfg['path']

        # head: title, description, canonical, share tags
        h = re.sub(r'<title>.*?</title>', lambda _: '<title>%s</title>' % esc(cfg['title']), h, count=1)
        if cfg['desc']:
            h = set_meta(h, 'name', 'description', esc(cfg['desc']))
            h = set_meta(h, 'property', 'og:description', esc(cfg['desc']))
        h = set_meta(h, 'property', 'og:title', esc(cfg['title']))
        h = set_meta(h, 'property', 'og:url', url)
        h = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, h, count=1)

        # structured data relevant to this page only
        nodes = [g for g in graph if cfg['schema'](g)]
        ld = '<script type="application/ld+json">%s</script>' % json.dumps({'@context': 'https://schema.org', '@graph': nodes}, ensure_ascii=False) if nodes else ''
        s = h.index('<script type="application/ld+json">')
        e = h.index('</script>', s) + len('</script>')
        h = h[:s] + ld + h[e:]

        # links between pages become real addresses; assets use absolute paths
        for frag, path in HASH_TO_PATH.items():
            h = h.replace('href="%s"' % frag, 'href="%s"' % path)
        # reused photos (data-k) point at a data-src0 image that may sit on another page now
        h = re.sub(r'<img src="data:," data-k="([^"]+)"',
                   lambda m: '<img src="%s" data-k="%s"' % (shared[m.group(1)], m.group(1)), h)
        h = h.replace('src="img/', 'src="/img/')

        # router: each file holds one page, so show it and mark its menu link
        h = h.replace("if(names.indexOf(h)<0)h='home';", "if(names.indexOf(h)<0)h=names[0];")
        h = h.replace("if(titles[h])document.title=titles[h];", "")
        h = h.replace("if(a.getAttribute('href')==='#'+h)",
                      "if(a.getAttribute('href')===({home:'/',services:'/coaching/',action:'/training-tips/',book:'/get-started/'})[h])")
        h = h.replace("menu.hidden=true;btn.setAttribute('aria-expanded','false');window.scrollTo(0,0);",
                      "menu.hidden=true;btn.setAttribute('aria-expanded','false');var jt=location.hash&&document.getElementById(location.hash.slice(1));if(jt)setTimeout(function(){jt.scrollIntoView({block:'start'})},60);else window.scrollTo(0,0);")
        h = h.replace("if(location.hash!=='#services')location.hash='services';",
                      "if(!document.querySelector('[data-page=\"services\"]')){location.href='/coaching/#'+id;return}")

        if key == 'home':
            # old one-page links like elisejavetski.com/#services still land on the right page
            redirect = ("<script>(function(){var m={'#services':'/coaching/','#action':'/training-tips/','#book':'/get-started/'};"
                        "if(m[location.hash])location.replace(m[location.hash]);})();</script>\n")
            h = h.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + redirect, 1)

        out = os.path.join(ROOT, cfg['out'])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(h)
        print('wrote', cfg['out'], round(len(h.encode()) / 1024), 'KB')

    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    today = datetime.date.today().isoformat()
    sm += ['  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>' % (SITE, c['path'], today) for c in PAGES.values()]
    sm.append('</urlset>')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
    print('wrote sitemap.xml')


if __name__ == '__main__':
    build()
