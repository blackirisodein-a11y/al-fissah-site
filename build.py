# -*- coding: utf-8 -*-
"""Génère le site Al-Fissah dans toutes les langues.

Usage :
  python3 build.py                              toutes les langues
  python3 build.py fr en                        langues choisies
  python3 build.py --site https://exemple.fr    change l'adresse du site
  python3 build.py --preview                    version d'essai : demande à Google
                                                de ne PAS indexer (à utiliser tant que
                                                le site n'est pas sur son adresse finale)

L'adresse est mémorisée dans site.conf : elle sert aux balises canoniques,
au sitemap et au partage sur les réseaux sociaux.
Contenu : lang/fr.py, lang/en.py, lang/ar.py, lang/es.py, lang/de.py
"""
import os, sys, json, re, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGO_ABS = 'https://al-fissah.com/assets/images/Logo.png'   # utilisé pour le partage social et Schema.org
LOGO_FILE = 'assets/logo.svg'                               # fichier local affiché sur le site
LOGIN = 'https://al-fissah.com/fr/login'
REGISTER = 'https://al-fissah.com/fr/register'
SITE = 'https://al-fissah.com'
PREVIEW = False
YEAR = '2026'

# --- adresse du site : site.conf, puis --site / --preview en ligne de commande ---
_conf = os.path.join(ROOT, 'site.conf')
if os.path.exists(_conf):
    for _l in open(_conf, encoding='utf-8'):
        _l = _l.strip()
        if _l.startswith('site='):
            SITE = _l[5:].strip().rstrip('/')
        elif _l.startswith('preview='):
            PREVIEW = _l[8:].strip().lower() in ('1', 'true', 'oui', 'yes')
if '--site' in sys.argv:
    SITE = sys.argv[sys.argv.index('--site') + 1].rstrip('/')
if '--preview' in sys.argv:
    PREVIEW = True
if '--public' in sys.argv:
    PREVIEW = False
LANGS = [c for c in ['fr', 'en', 'ar', 'ru', 'es', 'de'] if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lang', c + '.py'))]
LANG_NAMES = {'fr': 'Français', 'en': 'English', 'ar': 'العربية', 'ru': 'Русский', 'es': 'Español', 'de': 'Deutsch'}
FONTS = {
  'default': "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Karla:wght@400;500;700;800&family=Amiri:wght@400;700&display=swap",
  'ar': "https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&family=Amiri:wght@400;700&display=swap",
  'ru': "https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Amiri:wght@400;700&display=swap",
}
PAGES = ['index', 'programmes', 'tarifs', 'faq', 'temoignages', 'reglement', 'a-propos', 'contact', 'mentions-legales', '404']

PICS = json.load(open(os.path.join(ROOT, 'pics.json')))
CLASSROOM_RAW = open(os.path.join(ROOT, 'part_classroom.html'), encoding='utf-8').read()
sys.path.insert(0, os.path.join(ROOT, 'lang'))
from testimonials import TESTI  # témoignages réels, en français

def load_lang(code):
    spec = importlib.util.spec_from_file_location(code, os.path.join(ROOT, 'lang', code + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.L

def strip(s): return re.sub('<[^>]+>', ' ', s).strip()

class Builder:
    def __init__(self, code, L):
        self.c, self.L = code, L
        self.out = ROOT if code == 'fr' else os.path.join(ROOT, code)
        self.rel = '' if code == 'fr' else '../'
        os.makedirs(self.out, exist_ok=True)

    def url(self, page):
        p = '' if page == 'index' else page + '.html'
        return f"{SITE}/{p}" if self.c == 'fr' else f"{SITE}/{self.c}/{p}"

    def head(self, title, desc, page, extra=''):
        L = self.L; m = L['meta']
        fonts = FONTS.get(self.c, FONTS['default'])
        noindex = '\n<meta name="robots" content="noindex, nofollow">' if PREVIEW else ''
        pp = '' if page == 'index' else page + '.html'
        hreflang = '\n'.join(f'<link rel="alternate" hreflang="{c}" href="{SITE}/{"" if c=="fr" else c+"/"}{pp}">' for c in LANGS)
        org = json.dumps({"@context":"https://schema.org","@type":"EducationalOrganization","name":"Al-Fissah","url":SITE,"logo":LOGO_ABS,
                          "description":m['org_desc'],"email":"c.alfissah@gmail.com",
                          "sameAs":["http://www.facebook.com/Ecole.al.fissah1","https://www.instagram.com/ecolealfissah/","https://twitter.com/AlFissah","https://blog.al-fissah.com"]}, ensure_ascii=False)
        return f'''<!DOCTYPE html>
<html lang="{m['html_lang']}" dir="{m.get('dir','ltr')}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0D204E">{noindex}
<link rel="icon" type="image/svg+xml" href="{self.rel}assets/logo.svg">
<link rel="canonical" href="{self.url(page)}">
{hreflang}
<link rel="alternate" hreflang="x-default" href="{SITE}/{pp}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{LOGO_ABS}">
<meta property="og:type" content="website">
<meta property="og:url" content="{self.url(page)}">
<meta property="og:locale" content="{m['og_locale']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts}" rel="stylesheet">
<link rel="stylesheet" href="{self.rel}assets/style.css">
<script type="application/ld+json">{org}</script>
<script>window.I18N={json.dumps(L['js'], ensure_ascii=False)};</script>
{extra}
</head>
<body class="lang-{self.c}">
'''

    def langswitch(self, page):
        p = 'index.html' if page == 'index' else page + '.html'
        items = ''.join(f'<a href="{self.rel}{"" if c=="fr" else c+"/"}{p}" hreflang="{c}" lang="{c}"{" class=\"on\"" if c==self.c else ""}>{LANG_NAMES[c]}</a>' for c in LANGS)
        return f'<div class="langsw"><button type="button" class="langbtn" aria-haspopup="true" aria-expanded="false" aria-label="{self.L["nav"]["language"]}">{self.c.upper()} ▾</button><div class="langmenu">{items}</div></div>'

    def chrome(self, page, home=False):
        L = self.L; n = L['nav']
        loader = f'''<div id="loader">
  <div class="ld-box">
    <img class="ld-logo" src="{self.rel}{LOGO_FILE}" alt="" onerror="this.style.display='none'">
    <div class="word"><span id="typew"></span><span class="caret"></span></div>
  </div>
</div>
''' if home else ''
        nav = [('index.html', n['accueil'], 'index'), ('programmes.html', n['programmes'], 'programmes'), ('tarifs.html', n['tarifs'], 'tarifs'),
               ('faq.html', n['faq'], 'faq'), ('temoignages.html', n['temoignages'], 'temoignages'), ('a-propos.html', n['apropos'], 'a-propos'), ('contact.html', n['contact'], 'contact')]
        menu = '\n      '.join(f'<li><a href="{h}"{" class=\"active\"" if k == page else ""}>{l}</a></li>' for h, l, k in nav)
        mob = '\n    '.join(f'<a href="{h}">{l}</a>' for h, l, k in nav) + f'\n    <a href="reglement.html">{n["reglement"]}</a>'
        return loader + f'''<div id="progress" aria-hidden="true"></div>
<button class="totop" id="totop" aria-label="{n['totop']}">↑</button>
<a class="btn btn-orange cta-float" id="ctafloat" href="index.html#inscription">{n['cta_float']}</a>

<div class="dots" aria-hidden="true"></div>
<div class="aur a1" aria-hidden="true"></div>
<div class="aur a2" aria-hidden="true"></div>
<div class="blob b1" aria-hidden="true"></div>
<div class="blob b2" aria-hidden="true"></div>
<div class="blob b3" aria-hidden="true"></div>
<canvas id="floatsyms" aria-hidden="true"></canvas>

<header id="hd">
  <div class="wrap nav">
    <a class="logo" href="index.html"><img class="logomark" src="{self.rel}{LOGO_FILE}" alt="Al-Fissah" onerror="this.style.display='none';this.nextElementSibling.style.display='grid'"><span class="mark" style="display:none">A</span> <span class="logo-txt">AL-FISSAH<small>{self.L["meta"].get("tagline","")}</small></span></a>
    <ul class="menu">
      {menu}
    </ul>
    <div class="nav-right">
      {self.langswitch(page)}
      <a class="hd-login" href="{LOGIN}">{n['login']}</a>
      <a class="btn btn-orange login" href="index.html#inscription">{n['essai']} <span class="login-sub">{n['essai_sub']}</span></a>
      <button class="burger" id="burger" aria-label="{n['menu']}" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>

<div class="mobmenu" id="mobmenu" aria-hidden="true">
  <nav>
    {mob}
    <a href="https://livres.al-fissah.com">{n['livres']}</a>
    <a href="https://blog.al-fissah.com">{n['blog']}</a>
    <a class="btn btn-orange" href="index.html#inscription">{n['essai_mob']}</a>
    <a class="btn btn-navy" href="{LOGIN}">{n['login_full']}</a>
  </nav>
</div>

'''

    def footer(self):
        L = self.L; f = L['footer']; n = L['nav']
        return f'''
<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="logo" href="index.html" style="color:#fff"><img class="logomark" src="{self.rel}{LOGO_FILE}" alt="Al-Fissah" onerror="this.style.display='none';this.nextElementSibling.style.display='grid'"><span class="mark" style="display:none;background:#fff;color:var(--navy)">A</span> <span class="logo-txt">AL-FISSAH<small>{self.L["meta"].get("tagline","")}</small></span></a>
        <p style="margin-top:.9rem;max-width:26rem">{f['desc']}</p>
        <div class="socials">
          <a href="http://www.facebook.com/Ecole.al.fissah1" aria-label="Facebook" target="_blank" rel="noopener"><svg viewBox="0 0 24 24"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H7v4h3v6h4v-6h3l1-4h-4V8z"/></svg></a>
          <a href="https://www.instagram.com/ecolealfissah/" aria-label="Instagram" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></a>
          <a href="https://twitter.com/AlFissah" aria-label="X / Twitter" target="_blank" rel="noopener"><svg viewBox="0 0 24 24"><path d="M4 4l6.5 8.5L4 20h2.2l5.3-6.1L16 20h4l-6.8-9L19.5 4h-2.2l-4.9 5.6L8 4z"/></svg></a>
          <a href="https://www.youtube.com/watch?v=MNiWkEPoGNw" aria-label="YouTube" target="_blank" rel="noopener"><svg viewBox="0 0 24 24"><path d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12 31 31 0 0 0 2 15.8a3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-3.8 31 31 0 0 0-.4-3.8zM10 15V9l5.2 3z"/></svg></a>
        </div>
      </div>
      <div>
        <h4>{f['col1']}</h4>
        <ul>
          <li><a href="a-propos.html">{n['apropos']}</a></li>
          <li><a href="programmes.html">{f['prog_ind']}</a></li>
          <li><a href="programmes.html#collectifs">{f['prog_col']}</a></li>
          <li><a href="tarifs.html">{n['tarifs']}</a></li>
          <li><a href="temoignages.html">{n['temoignages']}</a></li>
          <li><a href="index.html#inscription">{f['essai']}</a></li>
        </ul>
      </div>
      <div>
        <h4>{f['col2']}</h4>
        <ul>
          <li><a href="faq.html">{f['faq']}</a></li>
          <li><a href="reglement.html">{n['reglement']}</a></li>
          <li><a href="https://livres.al-fissah.com">{n['livres']}</a></li>
          <li><a href="https://blog.al-fissah.com">{n['blog']}</a></li>
          <li><a href="contact.html">{f['contact']}</a></li>
          <li><a href="mentions-legales.html">{n['mentions']}</a></li>
        </ul>
      </div>
    </div>
    <div class="base">
      <span>© 2020–{YEAR} Al-Fissah — {f['copy']}</span>
      <span><a href="{LOGIN}">{n['login']}</a> · <a href="{REGISTER}">{f['register']}</a></span>
    </div>
  </div>
</footer>

<script src="{self.rel}assets/main.js"></script>
</body>
</html>
'''

    def page_hero(self, crumb, h1, lead, updated=None):
        u = f'<span class="updated">{self.L["common"]["updated"]} {updated}</span>' if updated else ''
        return f'''<div class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">{self.L['nav']['accueil']}</a> › {crumb}</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    {u}
  </div>
</div>
'''

    def write(self, name, html):
        with open(os.path.join(self.out, name), 'w', encoding='utf-8') as f: f.write(html)

    def qa(self, q, a, cls=''):
        return f'<div class="qa"><button aria-expanded="false">{q}<span class="chev">▾</span></button><div class="ans"><div class="{cls}">{a}</div></div></div>'

    # ------------------------------------------------------------ pages
    def build_index(self):
        L = self.L; H = L['home']; F = L['form']; P = L['progs']; c = L['common']
        cr = CLASSROOM_RAW
        for a, b in H['classroom'].items(): cr = cr.replace(a, b)
        ios = ['io io-l', 'io d1', 'io io-r d2', 'io io-l d1', 'io d2', 'io io-r d3']
        cards = ''.join(f'''      <article class="prog tilt io {ios[i]}">
        {PICS[i]}
        <div class="num">{i+1:02d}</div>
        <h3>{p['titre']}</h3>
        <div class="facts">{''.join(f'<span>{x}</span>' for x in p['facts'])}</div>
        <p>{p['court']}</p>
        <a class="more" href="programmes.html#{p['id']}">{c['discover']} →</a>
      </article>
''' for i, p in enumerate(P['items']))
        steps = ''.join(f'<div class="jstep"><span class="n">{i+1}</span><b>{t}</b><span>{d}</span></div>' for i, (t, d) in enumerate(H['journey']))
        pillars = ''.join(f'<div class="pillar io {x}"><div class="ar">{ar}</div><h3>{t}</h3>{body}</div>' for (ar, t, body), x in zip(H['pillars'], ['io-l', 'd1', 'io-r d2']))
        checks_ad = ''.join(f'<li>{x}</li>' for x in H['adultes_checks'])
        checks_app = ''.join(f'<li>{x}</li>' for x in H['app_checks'])
        phone = ''.join(f'<div class="item"><b>{a}</b><span>{b}</span></div>' for a, b in H['phone'])
        plans = ''
        for (t, price, per, feats), x, bt in zip(H['plans'], ['io io-l', 'featured io d1', 'io io-r d2'], ['btn-navy', 'btn-orange', 'btn-navy']):
            plans += f'<div class="plan {x}"><h3>{t}</h3><div class="price">{price}<small>/{c["session"]}</small></div><div class="per">{per}</div><ul>{"".join(f"<li>{f}</li>" for f in feats)}</ul><a class="btn {bt}" href="tarifs.html">{c["details"]}</a></div>'
        posts = ''.join(f'<a class="post" href="{u}" target="_blank" rel="noopener"><span class="post-tag">{tag}</span><b>{t}</b><span class="post-meta">Blog Al-Fissah · {d}</span></a>' for u, tag, t, d in H['posts'])
        vids = [('Nqwj4BfOaSg', 12, 12), ('_TVQsB01a5o', 12, 9), ('67vD_tLzQt4', 12, 8), ('q-NHRbJhJwU', 11, 7), ('pTpY0QsvLIw', 10, 4), ('7i9LYB64RZA', 9, 4)]
        videos = ''.join(f'<a class="vid" href="https://www.youtube.com/watch?v={v}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="" loading="lazy"><span>{H["book"]} {b} · {H["unit"]} {u}</span></a>' for v, b, u in vids)
        quotes = ''.join(f'<blockquote class="quote io {x}"><span class="stars">★★★★★</span><p>{q}</p><footer>{w}</footer></blockquote>' for (q, w), x in zip(H['quotes'], ['io-l', 'io-z d1', 'io-r d2']))
        faq = ''.join(self.qa(q, a) for q, a in H['faq'])
        ages = ''.join(f'<option>{a}</option>' for a in range(5, 18))
        progopts = ''.join(f'<option>{o}</option>' for o in F['programmes'])
        nivopts = ''.join(f'<option>{o}</option>' for o in F['niveaux'])
        html = f'''<div class="hero">
  <div class="wrap hero-grid">
    <div class="reveal-seq">
      <span class="badge"><span class="dot"></span> {H['badge']}</span>
      <h1>{H['h1_pre']} <span class="hl">{H['h1_hl']}<svg viewBox="0 0 300 14" preserveAspectRatio="none"><path d="M4 10 C 60 3, 120 12, 180 7 S 270 4, 296 9"/></svg></span>{H['h1_post']}</h1>
      <p class="lead">{H['lead']}</p>
      <div class="hero-cta">
        <a class="btn btn-orange" href="#inscription">{H['cta1']} <span class="arr">→</span></a>
        <a class="btn btn-ghost" href="programmes.html">{H['cta2']} ▸</a>
      </div>
      <p class="hero-note">{' &nbsp;·&nbsp; '.join(f'<b>✓</b> {x}' for x in H['note'])}</p>
    </div>
    {cr}
  </div>
</div>

<div class="journey"><div class="wrap"><div class="jgrid io" id="jgrid"><div class="jline" aria-hidden="true"><i></i></div>{steps}</div></div></div>

<section id="methode"><div class="wrap">
  <div class="head center io"><span class="kick">{H['methode_kick']}</span><h2>{H['methode_h2']}</h2><p>{H['methode_p']}</p></div>
  <div class="pillars">{pillars}</div>
</div></section>

<section id="programmes"><div class="wrap">
  <div class="head io"><span class="kick">{H['prog_kick']}</span><h2>{H['prog_h2']}</h2><p>{H['prog_p']}</p></div>
  <div class="progs">
{cards}  </div>
</div></section>

<section id="video"><div class="wrap"><div class="videowrap io io-z">
  <div class="head center"><span class="kick">{H['video_kick']}</span><h2>{H['video_h2']}</h2><p>{H['video_p']}</p></div>
  <div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/MNiWkEPoGNw" title="{H['video_h2']}" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe></div>
  <p class="video-more"><a href="https://www.youtube.com/watch?v=MNiWkEPoGNw" target="_blank" rel="noopener">{H['video_more']} →</a></p>
</div></div></section>

<section id="adultes"><div class="wrap split">
  <div class="io io-l">
    <div class="head" style="margin-bottom:0"><span class="kick">{H['adultes_kick']}</span><h2>{H['adultes_h2']}</h2><p>{H['adultes_p']}</p></div>
    <ul class="checks">{checks_ad}</ul>
  </div>
  <div class="panel io io-r d1"><p class="big">{' · '.join(f'<span>{w}</span>' for w in H['big'])}</p><p class="trad">{H['big_sub']}</p></div>
</div></section>

<section id="app"><div class="wrap split">
  <div class="io io-l"><div class="phone" aria-label="App"><div class="screen"><div class="bar">AL-FISSAH</div>{phone}</div></div></div>
  <div class="io io-r d1">
    <div class="head" style="margin-bottom:0"><span class="kick">{H['app_kick']}</span><h2>{H['app_h2']}</h2><p>{H['app_p']}</p></div>
    <ul class="checks">{checks_app}</ul>
    <div class="store-btns">
      <a class="store" href="https://apps.apple.com/fr/app/al-fissah/id6476883231"><small>{H['store_ios']}</small><b>App Store</b></a>
      <a class="store" href="https://play.google.com/store/apps/details?id=com.alfissah.dev"><small>{H['store_android']}</small><b>Google Play</b></a>
    </div>
  </div>
</div></section>

<section id="tarifs"><div class="wrap">
  <div class="head center io"><span class="kick">{L['nav']['tarifs']}</span><h2>{H['tarifs_h2']}</h2><p>{H['tarifs_p']}</p></div>
  <div class="plans">{plans}</div>
  <p class="tarif-note">{H['tarifs_note']} <a href="tarifs.html">{H['tarifs_all']} →</a></p>
</div></section>

<section id="blog"><div class="wrap">
  <div class="head center io"><span class="kick">{H['blog_kick']}</span><h2>{H['blog_h2']}</h2><p>{H['blog_p']}</p></div>
  <div class="posts io d1">{posts}</div>
  <div class="videos io d2">{videos}</div>
  <p class="tarif-note">{H['blog_note']} <a href="https://blog.al-fissah.com" target="_blank" rel="noopener">{H['blog_all']}</a> · <a href="https://www.youtube.com/watch?v=MNiWkEPoGNw" target="_blank" rel="noopener">{H['yt']}</a></p>
</div></section>

<section id="avis"><div class="wrap">
  <div class="head center io"><span class="kick">{L['nav']['temoignages']}</span><h2>{H['avis_h2']}</h2></div>
  <div class="quotes">{quotes}</div>
  <p class="tarif-note"><a href="temoignages.html">{H['avis_all']} →</a></p>
</div></section>

<section id="faq"><div class="wrap">
  <div class="head center io"><span class="kick">FAQ</span><h2>{H['faq_h2']}</h2></div>
  <div class="faq io d1">{faq}</div>
  <p class="tarif-note"><a href="faq.html">{H['faq_all']} →</a></p>
</div></section>

<section id="inscription" class="formsec"><div class="wrap form-grid">
  <div class="form-aside io io-l">
    <div class="head"><span class="kick">{F['kick']}</span><h2>{F['h2']}</h2><p>{F['p']}</p></div>
    <ul class="checks">{''.join(f'<li>{x}</li>' for x in F['checks'])}</ul>
    <div class="assur"><span class="ar">بِسْمِ اللهِ</span><b>{F['next_t']}</b><p>{F['next_p']}</p></div>
  </div>
  <form id="trial-form" class="card-form io io-r d1" novalidate>
    <fieldset>
      <legend><i>1</i> {F['who']}</legend>
      <div class="seg" role="radiogroup"><label><input type="radio" name="profil" value="adulte" checked><span>{F['adult']}</span></label><label><input type="radio" name="profil" value="enfant"><span>{F['child']}</span></label></div>
      <div id="enfant-fields" hidden><div class="row2">
        <div class="field"><label for="f-enfant">{F['child_name']}</label><input id="f-enfant" name="enfant_prenom" type="text" autocomplete="off"></div>
        <div class="field"><label for="f-age">{F['age']}</label><select id="f-age" name="enfant_age"><option value="">—</option>{ages}</select></div>
      </div></div>
      <div class="row2">
        <div class="field"><label for="f-programme">{F['programme']}</label><select id="f-programme" name="programme" required><option value="">{F['choose']}</option>{progopts}</select></div>
        <div class="field"><label for="f-niveau">{F['niveau']}</label><select id="f-niveau" name="niveau" required><option value="">{F['choose']}</option>{nivopts}</select></div>
      </div>
    </fieldset>
    <fieldset>
      <legend><i>2</i> {F['coords']}</legend>
      <div class="row2">
        <div class="field"><label for="f-nom">{F['name']}</label><input id="f-nom" name="nom" type="text" required autocomplete="name"></div>
        <div class="field"><label for="f-email">{F.get("email","E-mail")}</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-tel">{F['tel']} <small>({F['optional']})</small></label><input id="f-tel" name="tel" type="tel" autocomplete="tel" placeholder="+33 6 …"></div>
        <div class="field"><label for="f-pays">{F['country']}</label><input id="f-pays" name="pays" type="text" autocomplete="country-name" required></div>
      </div>
    </fieldset>
    <fieldset>
      <legend><i>3</i> {F['dispo_t']}</legend>
      <div class="field"><label for="f-dispo">{F['dispo']} <small>({F['dispo_hint']})</small></label><input id="f-dispo" name="dispo" type="text" placeholder="{F['dispo_ph']}"></div>
      <div class="field"><label for="f-msg">{F['message']} <small>({F['optional']})</small></label><textarea id="f-msg" name="message" placeholder="{F['msg_ph']}"></textarea></div>
      <label class="consent"><input type="checkbox" name="consent" required><span>{F['consent']} <a href="mentions-legales.html#confidentialite">{F['privacy']}</a>.</span></label>
      <div class="hp" aria-hidden="true"><label>Website <input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
    </fieldset>
    <div class="form-actions">
      <button type="submit" class="btn btn-orange">{F['submit']} <span class="arr">→</span></button>
      <span class="alt">{F['or']} <a id="wa-link" href="#" target="_blank" rel="noopener">{F['whatsapp']}</a></span>
    </div>
    <p id="form-status" class="form-status" hidden role="status" aria-live="polite"></p>
  </form>
</div></section>
'''
        self.write('index.html', self.head(L['meta']['title_home'], L['meta']['desc_home'], 'index') + self.chrome('index', home=True) + html + self.footer())

    def build_programmes(self):
        L = self.L; P = L['progs']; c = L['common']
        toc = ''.join(f'<li><a href="#{p["id"]}">{p["titre"]}</a></li>' for p in P['items'])
        secs = ''
        for i, p in enumerate(P['items']):
            secs += f'''<article class="pdetail io {'io-l' if i % 2 == 0 else 'io-r'}" id="{p['id']}">
  <div class="pd-head"><div class="pd-ar">{p['ar']}</div><div><span class="kick">{p['tag']}</span><h2>{p['titre']}</h2><div class="facts">{''.join(f'<span>{x}</span>' for x in p['facts'])}</div></div></div>
  <div class="prose">{p['long']}</div>
  <div class="pd-actions"><a class="btn btn-orange" href="index.html#inscription">{p['cta']} <span class="arr">→</span></a><a class="btn btn-ghost" href="tarifs.html">{c['see_prices']}</a></div>
</article>
'''
        html = self.page_hero(L['nav']['programmes'], P['h1'], P['lead']) + f'''<div class="page"><div class="wrap">
  <aside class="toc"><b>{L['nav']['programmes']}</b><ol>{toc}</ol><p class="toc-note">{P['toc_note']}</p></aside>
  <div class="pd-list">{secs}</div>
</div></div>
'''
        self.write('programmes.html', self.head(P['title'], P['desc'], 'programmes') + self.chrome('programmes') + html + self.footer())

    def build_tarifs(self):
        L = self.L; T = L['tarifs']; c = L['common']
        def grid(duo):
            rows = [(1, 28), (2, 48), (3, 72), (4, 96), (5, 120), (6, 144), (7, 168)]
            s = ''.join(f'<div class="tcard{" featured" if h == 2 else ""}"{f' data-badge="{T.get("badge","")}"' if h == 2 else ""}><span class="tf">{T["formule"]} {h}</span><div class="price">{e}&nbsp;€</div><div class="per">{T["per"].format(h=h)}</div><a class="btn {"btn-orange" if h == 2 else "btn-navy"}" href="index.html#inscription">{T["choose"]}</a></div>' for h, e in rows)
            if duo: s += f'<div class="tcard duo"><span class="tf">{T["duo"]}</span><div class="price">36&nbsp;€</div><div class="per">{T["duo_per"]}</div><a class="btn btn-navy" href="contact.html">{T["ask"]}</a></div>'
            return s
        values = ''.join(f'<div class="value"><div class="ar">{a}</div><b>{b}</b><p>{p}</p></div>' for a, b, p in T['values'])
        html = self.page_hero(L['nav']['tarifs'], T['h1'], T['lead']) + f'''<div class="page"><div class="wrap single tarifs-page">
  <div class="head io"><span class="kick">{T['arabe_kick']}</span><h2>{T['arabe_h2']}</h2><p>{T['arabe_p']}</p></div>
  <div class="tgrid io d1">{grid(True)}</div>
  <div class="head io" style="margin-top:4rem"><span class="kick">{T['coran_kick']}</span><h2>{T['coran_h2']}</h2><p>{T['coran_p']}</p></div>
  <div class="tgrid io d1">{grid(False)}</div>
  <article class="prose" style="margin-top:4rem">
    <h2>{T['good_h2']}</h2><div class="values">{values}</div>
    <h2>{T['pay_h2']}</h2>{T['pay_body']}
    <div class="note"><b>{T['note_b']}</b> {T['note_p']} <a href="index.html#inscription">{c['request']}</a></div>
  </article>
</div></div>
'''
        self.write('tarifs.html', self.head(T['title'], T['desc'], 'tarifs') + self.chrome('tarifs') + html + self.footer())

    def build_faq(self):
        L = self.L; Q = L['faq']
        ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q, a in Q['items']]}, ensure_ascii=False)
        html = self.page_hero('FAQ', Q['h1'], Q['lead']) + f'''<div class="page"><div class="wrap single">
  <div class="faq wide io">{''.join(self.qa(q, a, 'prose-lite') for q, a in Q['items'])}</div>
  <div class="prose" style="margin-top:3rem"><div class="note"><b>{Q['note_b']}</b> <a href="contact.html">{Q['note_a']}</a>{Q['note_p']}</div></div>
</div></div>
'''
        self.write('faq.html', self.head(Q['title'], Q['desc'], 'faq', f'<script type="application/ld+json">{ld}</script>') + self.chrome('faq') + html + self.footer())

    def build_temoignages(self):
        L = self.L; T = L['temoignages']; M = L['common']['months']
        def fdate(d):
            y, m, dd = d.split('-'); return T['date_fmt'].format(d=int(dd), m=M[int(m) - 1], y=y)
        tags = T['tags']
        cards = ''.join(f'''<blockquote class="tcard-t io {'io-l' if i % 2 == 0 else 'io-r'}" lang="fr" dir="ltr">
  <div class="tt-top"><span class="stars">★★★★★</span><span class="tt-tag">{tags.get(tag, tag)}</span></div>{body}
  <footer><b>{n}</b><time datetime="{d}">{fdate(d)}</time></footer>
</blockquote>''' for i, (n, d, tag, body) in enumerate(TESTI))
        ld = json.dumps({"@context":"https://schema.org","@type":"EducationalOrganization","name":"Al-Fissah","url":SITE,
              "aggregateRating":{"@type":"AggregateRating","ratingValue":"5","bestRating":"5","reviewCount":str(len(TESTI))},
              "review":[{"@type":"Review","author":{"@type":"Person","name":n},"datePublished":d,"inLanguage":"fr","reviewRating":{"@type":"Rating","ratingValue":"5"},"reviewBody":strip(b)[:500]} for n, d, _, b in TESTI]}, ensure_ascii=False)
        kids = sum(1 for x in TESTI if x[2] == 'Enfants')
        note_lang = f'<p class="lang-note">{T["lang_note"]}</p>' if self.c != 'fr' else ''
        html = self.page_hero(L['nav']['temoignages'], T['h1'], T['lead'].format(n=len(TESTI))) + f'''<div class="page"><div class="wrap single tpage">
  <div class="stats io">
    <div class="stat"><div class="n">{len(TESTI)}</div><span>{T['s1']}</span></div>
    <div class="stat"><div class="n">★ 5/5</div><span>{T['s2']}</span></div>
    <div class="stat"><div class="n">{kids}</div><span>{T['s3']}</span></div>
    <div class="stat"><div class="n">2021</div><span>{T['s4']}</span></div>
  </div>
  {note_lang}
  <div class="tcols">{cards}</div>
  <div class="prose"><div class="note"><b>{T['note_b']}</b> {T['note_p']} <a href="{LOGIN}">{T['note_a']}</a>.</div></div>
</div></div>
'''
        self.write('temoignages.html', self.head(T['title'], T['desc'], 'temoignages', f'<script type="application/ld+json">{ld}</script>') + self.chrome('temoignages') + html + self.footer())

    def build_reglement(self):
        L = self.L; R = L['reglement']
        toc = ''.join(f'<li><a href="#art-{i+1}">{t}</a></li>' for i, (t, _) in enumerate(R['articles']))
        arts = ''.join(f'<h2 id="art-{i+1}"><span class="art">{R["article"]} {i+1}</span>{t}</h2>{b}' for i, (t, b) in enumerate(R['articles']))
        html = self.page_hero(L['nav']['reglement'], R['h1'], R['lead'], R['updated']) + f'''<div class="page"><div class="wrap">
  <aside class="toc"><b>{L['common']['toc']}</b><ol>{toc}</ol></aside>
  <article class="prose">{arts}</article>
</div></div>
'''
        self.write('reglement.html', self.head(R['title'], R['desc'], 'reglement') + self.chrome('reglement') + html + self.footer())

    def build_apropos(self):
        L = self.L; A = L['apropos']
        stats = ''.join(f'<div class="stat"><div class="n">{n}</div><span>{s}</span></div>' for n, s in A['stats'])
        values = ''.join(f'<div class="value"><div class="ar">{a}</div><b>{b}</b><p>{p}</p></div>' for a, b, p in A['values'])
        links = ''.join(f'<li><b>{t}</b><a href="{u}" target="_blank" rel="noopener">{A["read"]} →</a></li>' for u, t in A['links'])
        html = self.page_hero(L['nav']['apropos'], A['h1'], A['lead']) + f'''<div class="page"><div class="wrap single"><article class="prose">
  <div class="stats">{stats}</div>
  <h2>{A['prog_h2']}</h2>{A['prog_body']}
  <h2>{A['is_h2']}</h2><div class="values">{values}</div>
  <h2>{A['coran_h2']}</h2>{A['coran_body']}
  <h2>{A['more_h2']}</h2><ul class="timeline">{links}</ul>
  <div class="note"><b>{A['note_b']}</b> {A['note_p']} <a href="index.html#inscription">{L['common']['request']}</a></div>
</article></div></div>
'''
        self.write('a-propos.html', self.head(A['title'], A['desc'], 'a-propos') + self.chrome('a-propos') + html + self.footer())

    def build_contact(self):
        L = self.L; C = L['contact']
        subj = ''.join(f'<option>{s}</option>' for s in C['subjects'])
        html = self.page_hero(L['nav']['contact'], C['h1'], C['lead']) + f'''<div class="page"><div class="wrap form-grid contact-grid">
  <div class="form-aside io io-l"><div class="support-grid one">
    <div class="sup"><div class="ico">✉</div><b>{C['mail_t']}</b><p>{C['mail_p']}</p><a class="btn btn-navy" href="mailto:c.alfissah@gmail.com">c.alfissah@gmail.com</a></div>
    <div class="sup"><div class="ico">🕘</div><b>{C['hours_t']}</b><p>{C['hours_p']}</p></div>
    <div class="sup"><div class="ico">▶</div><b>{C['new_t']}</b><p>{C['new_p']}</p><a class="btn btn-orange" href="index.html#inscription">{L['nav']['cta_float']}</a></div>
  </div></div>
  <form id="contact-form" class="card-form io io-r d1" novalidate>
    <fieldset>
      <legend><i>✉</i> {C['form_t']}</legend>
      <div class="row2">
        <div class="field"><label for="c-nom">{C['nom']}</label><input id="c-nom" name="nom" type="text" required autocomplete="family-name"></div>
        <div class="field"><label for="c-prenom">{C['prenom']}</label><input id="c-prenom" name="prenom" type="text" required autocomplete="given-name"></div>
      </div>
      <div class="field"><label for="c-email">{L['form'].get("email","E-mail")}</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
      <div class="field"><label for="c-sujet">{C['sujet']}</label><select id="c-sujet" name="sujet" required><option value="">{L['form']['choose']}</option>{subj}</select></div>
      <div class="field"><label for="c-msg">{C['message']}</label><textarea id="c-msg" name="message" required></textarea></div>
      <div class="hp" aria-hidden="true"><label>Website <input id="c-website" name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
    </fieldset>
    <div class="form-actions"><button type="submit" class="btn btn-orange">{C['send']} <span class="arr">→</span></button></div>
    <p id="contact-status" class="form-status" hidden role="status" aria-live="polite"></p>
  </form>
</div></div>
'''
        self.write('contact.html', self.head(C['title'], C['desc'], 'contact') + self.chrome('contact') + html + self.footer())

    def build_mentions(self):
        L = self.L; M = L['mentions']
        toc = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in M['toc'])
        html = self.page_hero(L['nav']['mentions'], M['h1'], M['lead'], M['updated']) + f'''<div class="page"><div class="wrap">
  <aside class="toc"><b>{L['common']['toc']}</b><ol>{toc}</ol></aside>
  <article class="prose">{M['body']}</article>
</div></div>
'''
        self.write('mentions-legales.html', self.head(M['title'], M['desc'], 'mentions-legales') + self.chrome('mentions-legales') + html + self.footer())

    def build_404(self):
        L = self.L; N = L['nf']
        html = f'''<div class="page-hero notfound"><div class="wrap">
  <div class="nf-ar">٤٠٤</div><h1>{N['h1']}</h1><p class="lead">{N['p']}</p>
  <div class="hero-cta" style="margin-top:1.6rem"><a class="btn btn-orange" href="index.html">{N['home']} <span class="arr">→</span></a><a class="btn btn-ghost" href="programmes.html">{L['nav']['programmes']}</a><a class="btn btn-ghost" href="contact.html">{L['nav']['contact']}</a></div>
</div></div><div style="height:4rem"></div>
'''
        self.write('404.html', self.head(N['title'], N['p'], '404', '<meta name="robots" content="noindex">') + self.chrome('404') + html + self.footer())

    def build(self):
        for f in [self.build_index, self.build_programmes, self.build_tarifs, self.build_faq, self.build_temoignages,
                  self.build_reglement, self.build_apropos, self.build_contact, self.build_mentions, self.build_404]:
            f()
        print('✓', self.c, '→', os.path.relpath(self.out, ROOT) or '.')

def sitemap(codes):
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
        for p in PAGES:
            if p == '404': continue
            for c in codes:
                loc = f"{SITE}/{'' if c == 'fr' else c + '/'}{'' if p == 'index' else p + '.html'}"
                alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{a}" href="{SITE}/{"" if a == "fr" else a + "/"}{"" if p == "index" else p + ".html"}"/>' for a in codes)
                pr = '1.0' if p == 'index' else ('0.8' if p in ('programmes', 'tarifs') else '0.6')
                f.write(f'  <url><loc>{loc}</loc>{alts}<changefreq>monthly</changefreq><priority>{pr}</priority></url>\n')
        f.write('</urlset>\n')
    with open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8') as f:
        if PREVIEW:
            f.write('User-agent: *\nDisallow: /\n')
        else:
            f.write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')

if __name__ == '__main__':
    _args = sys.argv[1:]
    if '--site' in _args:
        _i = _args.index('--site'); del _args[_i:_i + 2]
    _args = [a for a in _args if not a.startswith('--')]
    codes = _args or LANGS
    for c in codes:
        Builder(c, load_lang(c)).build()
    sitemap(LANGS)
    print('✓ sitemap.xml, robots.txt')
    print(f'✓ adresse du site : {SITE}' + ('   [APERÇU — non indexable par Google]' if PREVIEW else ''))
