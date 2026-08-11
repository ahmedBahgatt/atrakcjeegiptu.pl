#!/usr/bin/env python3
"""Static site generator for atrakcjeegiptu.pl - tours, hubs, blog from data/*.json."""
import json, os, re, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
D = lambda *p: os.path.join(ROOT, *p)

tours = json.load(open(D("data/tours.json")))
posts = json.load(open(D("data/blog.json")))
copy = json.load(open(D("data/copy.json")))

SITE = "https://atrakcjeegiptu.pl"
WA_DIGITS = re.sub(r"\D", "", copy["footer"]["contact"]["whatsapp"])
CAT_LABEL = {c["id"]: c["label"] for c in copy["categories"]}
CAT_IMG = {c["id"]: c["img"] for c in copy["categories"]}
BASES = [(d["id"], d["label"], d["gen"]) for d in copy["destinations"]]
BASE_GEN = {d["label"]: d["gen"] for d in copy["destinations"]}


def usd(n):
    return f"{n} USD"


def wa_link(msg):
    return f"https://wa.me/{WA_DIGITS}?text={urllib.parse.quote(msg)}"


def trunc(s, n=155):
    s = str(s)
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def hero_img(t):
    if t.get("photos"):
        return f"/assets/img/tours/{t['slug']}/0.webp"
    return f"/assets/img/{CAT_IMG.get(t['category'], 'scene_giza')}.webp"


def card_img(t):
    if t.get("photos"):
        return f"/assets/img/tours/{t['slug']}/0-s.webp"
    return f"/assets/img/{CAT_IMG.get(t['category'], 'scene_giza')}-s.webp"


NAV = [("Strona główna", "/"), ("Wycieczki", "/wycieczki/"), ("Hurghada", "/hurghada/"),
       ("Marsa Alam", "/marsa-alam/"), ("Sharm el-Sheikh", "/sharm-el-sheikh/"), ("Blog", "/blog/")]

WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.4 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.2-.7-2.7-1.1-4.4-3.8-4.6-4-.1-.2-1.1-1.4-1.1-2.7s.7-1.9.9-2.2c.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.4l.9 2.1c.1.2.1.4 0 .6l-.4.6-.4.5c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1.1 2.2 1.4 2.5 1.5.3.1.5.1.7-.1l1-1.2c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.6.4 0 .1 0 .7-.2 1.3Z"/></svg>'


def shell(title, desc, body, canonical, active="", jsonld=None, og_img=None, noindex=False, og_type="website", wa_float=True, preload=None):
    act = ' class="active"'
    nav = "".join(f'<a href="{h}"{act if l == active else ""}>{l}</a>' for l, h in NAV)
    lds = ""
    if jsonld:
        blocks = jsonld if isinstance(jsonld, list) else [jsonld]
        lds = "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False).replace("</", chr(60) + chr(92) + "/")}</script>' for b in blocks)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else f'<link rel="canonical" href="{canonical}">'
    og_img = og_img or f"{SITE}/assets/img/hero_poster.webp"
    fl = f'<a class="wa-float" href="{wa_link(copy["waDefault"])}" target="_blank" rel="noopener" aria-label="Napisz na WhatsApp">{WA_SVG}</a>' if wa_float else ""
    pre = f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    return f"""<!doctype html>
<html lang="pl" class="no-js">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.replace('no-js','js')</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
{pre}
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="Atrakcje Egiptu">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" type="image/svg+xml" href="/assets/img/logo.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">
{lds}
</head>
<body>
<header class="site-header"><div class="container">
<a class="brand" href="/"><img src="/assets/img/logo.svg" alt="" width="36" height="36">Atrakcje Egiptu</a>
<button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="main-nav">☰</button>
<nav class="main-nav" id="main-nav">{nav}</nav>
<a class="btn btn-wa header-cta" href="{wa_link(copy['waDefault'])}" target="_blank" rel="noopener">WhatsApp</a>
</div></header>
<main>
{body}
</main>
<footer class="site-footer">
<div class="container">
<div><div class="footer-brand"><img src="/assets/img/logo.svg" alt="" width="32" height="32">Atrakcje Egiptu</div><p class="about">{esc(copy['footer']['about'])}</p></div>
<div><h4>Kierunki</h4><ul><li><a href="/hurghada/">Wycieczki z Hurghady</a></li><li><a href="/marsa-alam/">Wycieczki z Marsa Alam</a></li><li><a href="/sharm-el-sheikh/">Wycieczki z Sharm el-Sheikh</a></li></ul></div>
<div><h4>Na skróty</h4><ul><li><a href="/wycieczki/">Wszystkie wycieczki</a></li><li><a href="/blog/">Blog</a></li><li><a href="/wycieczki/#faq">Częste pytania</a></li><li><a href="/polityka-prywatnosci/">Polityka prywatności</a></li></ul></div>
<div><h4>Kontakt</h4><ul>
<li><a href="{wa_link('Dzień dobry!')}" target="_blank" rel="noopener">WhatsApp: {copy['footer']['contact']['whatsapp']}</a></li>
<li><a href="mailto:{copy['footer']['contact']['email']}">{copy['footer']['contact']['email']}</a></li>
</ul></div>
</div>
<div class="footer-legal">© 2026 {esc(copy['footer']['legalNote'])}</div>
</footer>
{fl}
<script src="/js/site.js" defer></script>
</body>
</html>"""


def tour_card(t, lazy=True):
    dur = t.get("duration") or "1 dzień"
    old = f'<s style="color:var(--ink-soft);font-size:.9rem;font-weight:500">{usd(t["priceOld"])}</s> ' if t.get("priceOld") else ""
    badge = '<span class="badge">Promocja</span>' if t.get("priceOld") else ""
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return f"""<article class="card rv" data-cat="{t['category']}" data-base="{t['base']}">
<div class="card-img"><a href="/wycieczki/{t['slug']}/"><img src="{card_img(t)}" alt="{esc(t['shortTitle'])}" width="560" height="350"{load} style="view-transition-name:t-{t['slug'][:40]}"></a>{badge}<span class="badge-dur">{esc(dur)}</span></div>
<div class="card-body">
<div class="card-meta"><span>z {esc(BASE_GEN.get(t['base'], t['base']))}</span><span>·</span><span>{esc(CAT_LABEL.get(t['category'], ''))}</span></div>
<h3><a href="/wycieczki/{t['slug']}/">{esc(t['shortTitle'])}</a></h3>
<div class="card-foot"><div class="price"><span class="from">od</span> {old}{usd(t['price'])}<small>za osobę</small></div>
<a class="btn btn-gold" href="/wycieczki/{t['slug']}/">Zobacz</a></div>
</div></article>"""


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": f["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]}


def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                                for i, (n, u) in enumerate(items)]}


def build_home():
    feat = [t for t in tours if t.get("photos") and t.get("priceOld")][:4] + \
           [t for t in tours if t.get("photos") and not t.get("priceOld")]
    feat = (feat or tours)[:8]
    rail = "".join(tour_card(t) for t in feat)
    dests = "".join(f"""<a class="dest-tile rv" href="/{d['id']}/">
<img src="/assets/img/{d['img']}.webp" alt="Wycieczki z {esc(d['gen'])}" width="640" height="800" loading="lazy">
<div><h3>{esc(d['label'])}</h3><p>{esc(d['desc'])}</p>
<span class="count">{sum(1 for t in tours if t['base'] == d['label'])} wycieczek →</span></div></a>""" for d in copy["destinations"])
    cats = "".join(f"""<a class="dest-tile rv" href="/wycieczki/#{c['id']}" style="aspect-ratio:4/3">
<img src="/assets/img/{c['img']}-s.webp" alt="{esc(c['label'])}" width="560" height="420" loading="lazy">
<div><h3 style="font-size:1.2rem">{esc(c['label'])}</h3>
<span class="count">{sum(1 for t in tours if t['category'] == c['id'])} ofert →</span></div></a>""" for c in copy["categories"])
    marq = "".join(f"<span>{esc(m)}</span>" for m in copy["marquee"]) * 2
    steps = "".join(f'<div class="feature rv"><span class="num">{i+1}</span><h3>{esc(s["title"])}</h3><p>{esc(s["body"])}</p></div>'
                    for i, s in enumerate(copy["howItWorks"]))
    usps = "".join(f'<div class="feature rv"><h3>{esc(u["title"])}</h3><p>{esc(u["body"])}</p></div>' for u in copy["usp"])
    revs = "".join(f"""<div class="review rv"><div class="stars">★★★★★</div><p>{esc(r['text'])}</p>
<footer>{esc(r['name'])}<span>{esc(r['city'])} · {esc(r['tour'])}</span></footer></div>""" for r in copy["reviews"])
    faqs = "".join(f'<details><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>' for f in copy["faq"][:6])
    stats = "".join(f'<div><b data-count="{s["value"]}">0</b><span>{esc(s["label"])}</span></div>' for s in copy["stats"])
    latest = "".join(post_card(p) for p in sorted(posts, key=lambda p: p["date"], reverse=True)[:3])
    body = f"""
<section class="hero">
<div class="hero-media plx">
<video autoplay muted loop playsinline preload="none" poster="/assets/img/hero_poster.webp" id="herovid">
</video>
<img src="/assets/img/hero_poster.webp" alt="Piramidy w Gizie o zachodzie słońca" fetchpriority="high" width="1600" height="900" id="heroimg">
</div>
<div class="hero-inner container">
<span class="eyebrow stagger">{esc(copy['tagline'])}</span>
<h1 class="stagger">{esc(copy['hero']['h1'])}</h1>
<p class="sub stagger">{esc(copy['hero']['sub'])}</p>
<div class="hero-ctas stagger">
<a class="btn btn-gold" href="/wycieczki/">{esc(copy['hero']['ctaMain'])}</a>
<a class="btn btn-ghost" href="{wa_link(copy['waDefault'])}" target="_blank" rel="noopener">{esc(copy['hero']['ctaWa'])}</a>
</div>
<div class="hero-stats">{stats}</div>
</div>
<div class="hero-scroll" aria-hidden="true"></div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{marq}</div></div>
<section class="section"><div class="container">
<span class="eyebrow">Skąd wyruszasz?</span>
<h2>Trzy kurorty, jeden Egipt</h2>
<p class="lead">Odbieramy z hotelu w każdym z trzech głównych kurortów Morza Czerwonego - i z ich okolic.</p>
<div class="dest-tiles">{dests}</div>
</div></section>
<section class="section section-alt">
<div class="container"><span class="eyebrow">Bestsellery</span>
<h2>Najchętniej wybierane wycieczki</h2>
<p class="lead">Sprawdzone przez setki polskich turystów. Ceny w USD za osobę, bez ukrytych dopłat.</p></div>
<div class="rail-wrap"><div class="rail">{rail}</div>
<div class="rail-nav"><button data-dir="prev" aria-label="Poprzednie">←</button><button data-dir="next" aria-label="Następne">→</button></div></div>
<div class="container" style="padding-top:20px"><a class="btn btn-ghost" href="/wycieczki/">Zobacz wszystkie {len(tours)} wycieczek →</a></div>
</section>
<section class="section"><div class="container">
<span class="eyebrow">Kategorie</span>
<h2>Co Cię ciągnie?</h2>
<div class="dest-tiles" style="grid-template-columns:repeat(auto-fit,minmax(210px,1fr))">{cats}</div>
</div></section>
<section class="section section-dark"><div class="container">
<span class="eyebrow">Jak to działa</span>
<h2>Trzy kroki do rezerwacji</h2>
<p class="lead">Bez formularzy, logowania i przedpłat - cała rezerwacja to jedna rozmowa na WhatsApp.</p>
<div class="cols-3">{steps}</div>
</div></section>
<section class="section"><div class="container">
<span class="eyebrow">Dlaczego my</span>
<h2>Egipt bez ściemy</h2>
<div class="cols-3" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">{usps}</div>
</div></section>
<section class="section section-alt"><div class="container">
<span class="eyebrow">Opinie</span>
<h2>Co mówią nasi turyści</h2>
<div class="cols-3">{revs}</div>
</div></section>
<section class="section"><div class="container">
<span class="eyebrow">FAQ</span>
<h2>Częste pytania</h2>
<div class="faq">{faqs}</div>
</div></section>
<section class="section section-alt"><div class="container">
<span class="eyebrow">Blog</span>
<h2>Praktycznie o Egipcie</h2>
<div class="grid">{latest}</div>
</div></section>
<div class="container"><div class="cta-band rv">
<div><h2>Nie wiesz, co wybrać?</h2><p>Napisz, co lubisz - doradzimy szczerze i bez wciskania.</p></div>
<a class="btn btn-wa" href="{wa_link('Dzień dobry! Proszę o pomoc w wyborze wycieczki.')}" target="_blank" rel="noopener">Napisz na WhatsApp</a>
</div></div>
<script>
(function(){{var v=document.getElementById('herovid'),i=document.getElementById('heroimg');
if(matchMedia('(min-width:768px) and (prefers-reduced-motion: no-preference)').matches){{
var s=document.createElement('source');s.src='/assets/vid/hero.mp4';s.type='video/mp4';
v.appendChild(s);v.load();v.addEventListener('playing',function(){{i.style.display='none'}});v.play().catch(function(){{}});
}}else{{v.remove()}}}})();
</script>"""
    ld = [
        {"@context": "https://schema.org", "@type": "TravelAgency", "name": copy["brand"],
         "url": SITE, "logo": f"{SITE}/assets/img/logo.svg",
         "description": copy["footer"]["about"],
         "areaServed": ["Hurghada", "Marsa Alam", "Sharm el-Sheikh"],
         "address": {"@type": "PostalAddress", "addressLocality": "Hurghada", "addressCountry": "EG"},
         "telephone": "+" + WA_DIGITS,
         "email": copy["footer"]["contact"]["email"],
         "priceRange": "$5 - $345"},
        faq_ld(copy["faq"][:6]),
    ]
    write("index.html", shell(
        "Atrakcje Egiptu - wycieczki fakultatywne z Hurghady, Marsa Alam i Sharm",
        "Ponad 100 wycieczek fakultatywnych w Egipcie po polsku: Kair, Luksor, rejsy, safari i nurkowanie. Ceny w USD, odbiór z hotelu, rezerwacja przez WhatsApp.",
        body, f"{SITE}/", active="Strona główna", jsonld=ld,
        preload="/assets/img/hero_poster.webp"))


def build_listing():
    cats = '<a href="#lista" data-cat="all" class="active">Wszystkie</a>' + \
           "".join(f'<a href="#lista" data-cat="{c["id"]}" id="{c["id"]}">{esc(c["label"])}</a>' for c in copy["categories"])
    base_nav = "".join(f'<a href="#z-{bid}">z {esc(gen)} ({sum(1 for t in tours if t["base"] == lbl)})</a>' for bid, lbl, gen in BASES)
    dest_sections = ""
    for bid, lbl, gen in BASES:
        bt = [t for t in tours if t["base"] == lbl]
        if not bt:
            continue
        bcards = "".join(tour_card(t) for t in bt)
        dest_sections += f"""<section id="z-{bid}" class="container dest-section" style="padding-top:34px">
<h2>Wycieczki z {esc(gen)}</h2>
<div class="grid">{bcards}</div>
</section>"""
    faqs = "".join(f'<details><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>' for f in copy["faq"])
    body = f"""
<section class="page-hero container">
<span class="eyebrow">Katalog</span>
<h1>Wycieczki fakultatywne w Egipcie</h1>
<p>{len(tours)} wycieczek i kursów z odbiorem z hotelu. Stałe ceny w dolarach, polska obsługa, rezerwacja przez WhatsApp bez przedpłaty.</p>
<div class="cats">{base_nav}</div>
<div class="cats">{cats}</div>
</section>
<div id="lista">{dest_sections}</div>
<section id="faq" class="section section-alt"><div class="container">
<h2>Częste pytania</h2>
<div class="faq">{faqs}</div>
</div></section>
<script>
function applyCat(c){{
  document.querySelectorAll('.cats a[data-cat]').forEach(x => x.classList.toggle('active', x.dataset.cat === c));
  document.querySelectorAll('#lista .card[data-cat]').forEach(card => {{
    card.style.display = (c === 'all' || card.dataset.cat === c) ? '' : 'none';
  }});
}}
document.querySelectorAll('.cats a[data-cat]').forEach(a => a.addEventListener('click', () => applyCat(a.dataset.cat)));
if (location.hash) {{
  const h = location.hash.slice(1);
  if (document.querySelector(`.cats a[data-cat="${{h}}"]`)) applyCat(h);
}}
</script>"""
    ld = [{"@context": "https://schema.org", "@type": "ItemList",
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t["shortTitle"],
                                "url": f"{SITE}/wycieczki/{t['slug']}/"}
                               for i, t in enumerate(tours)]},
          breadcrumb_ld([("Strona główna", SITE + "/"), ("Wycieczki", f"{SITE}/wycieczki/")]),
          faq_ld(copy["faq"])]
    write("wycieczki/index.html", shell(
        f"Wycieczki po Egipcie - katalog {len(tours)} wycieczek | Atrakcje Egiptu",
        "Wycieczki fakultatywne z Hurghady, Marsa Alam i Sharm el-Sheikh: Kair, Luksor, rejsy na rafy, safari. Polski przewodnik, ceny w USD, rezerwacja WhatsApp.",
        body, f"{SITE}/wycieczki/", active="Wycieczki", jsonld=ld))


def build_tour(t):
    n = t.get("photos", 0)
    gallery = ""
    if n > 1:
        gitems = "".join(
            f'<img src="/assets/img/tours/{t["slug"]}/{i}-s.webp" data-full="/assets/img/tours/{t["slug"]}/{i}.webp" alt="{esc(t["shortTitle"])} - zdjęcie {i+1}" width="560" height="373" loading="lazy" tabindex="0">'
            for i in range(1, n))
        gallery = f'<h2>Zdjęcia z wycieczki</h2><div class="gallery" id="gal">{gitems}</div>'
    dur = t.get("duration") or "1 dzień"
    chips = f'<div class="chips"><span>{esc(CAT_LABEL.get(t["category"], t["category"]))}</span><span>z {esc(BASE_GEN.get(t["base"], t["base"]))}</span><span>{esc(dur)}</span><span>Bezpłatne odwołanie do 24 h</span></div>'
    desc = "".join(f"<p>{esc(p)}</p>" for p in t["description"])
    incl = "".join(f"<li>{esc(x)}</li>" for x in t["included"])
    nincl = "".join(f"<li>{esc(x)}</li>" for x in t["notIncluded"])
    incl_section = ""
    if incl or nincl:
        cols = (f'<div><h3>W cenie</h3><ul class="incl">{incl}</ul></div>' if incl else "") + \
               (f'<div><h3>We własnym zakresie</h3><ul class="nincl">{nincl}</ul></div>' if nincl else "")
        incl_section = f'<h2>Co jest w cenie</h2><div class="incl-grid">{cols}</div>'
    tiers = ""
    if t.get("tiers"):
        rows = "".join(f"<li>{esc(x['label'])} - <b>{usd(x['usd'])}</b></li>" for x in t["tiers"])
        tiers = f'<h2>Cennik</h2><ul class="incl" style="margin-bottom:30px">{rows}</ul>'
    old = f'<s style="font-size:1.1rem;color:var(--ink-soft);font-weight:500">{usd(t["priceOld"])}</s> ' if t.get("priceOld") else ""
    wa = wa_link(f"""Dzień dobry! Chcę zarezerwować wycieczkę:
{t['shortTitle']} (z {BASE_GEN.get(t['base'], t['base'])})
Data: (do ustalenia)
Hotel: (do podania)
Dorośli: 2 | Dzieci: 0
{SITE}/wycieczki/{t['slug']}/
Proszę o potwierdzenie dostępności, godziny odbioru i ceny.""")
    body = f"""
<div class="container">
<div class="tour-hero plx"><img src="{hero_img(t)}" alt="{esc(t['shortTitle'])}" width="1400" height="600" fetchpriority="high" style="view-transition-name:t-{t['slug'][:40]}"></div>
<div class="tour-layout">
<div class="tour-main">
<span class="eyebrow">z {esc(BASE_GEN.get(t['base'], t['base']))} · {esc(dur)}</span>
<h1>{esc(t['title'])}</h1>
{chips}
<div class="tour-desc">{desc}</div>
{gallery}
{tiers}
{incl_section}
</div>
<aside class="book-box">
<div class="price"><span class="from">od</span> {old}{usd(t['price'])}<small>za osobę</small></div>
<div class="meta">
<span>Wyjazd z: <b>{esc(t['base'])}</b></span>
<span>Czas trwania: <b>{esc(dur)}</b></span>
<span>Język: <b>polski</b></span>
<span>Płatność: <b>na miejscu, bez przedpłat</b></span>
<span>Odpowiadamy: <b>zwykle w 15 minut</b></span>
</div>
<a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">Rezerwuj przez WhatsApp</a>
<a class="btn btn-ghost" style="margin-top:10px;width:100%;justify-content:center" href="/wycieczki/">Inne wycieczki</a>
<p class="book-note">Bezpłatne odwołanie do 24 h przed wyjazdem. Cena w USD za osobę dorosłą{' - ceny dla dzieci w cenniku powyżej' if t.get('tiers') else ' - o ceny dla dzieci zapytaj przy rezerwacji'}.</p>
</aside>
</div></div>
<div class="stickybar"><div class="price">{usd(t['price'])}</div><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">Rezerwuj</a></div>
<dialog id="lb" aria-label="Powiększone zdjęcie" style="max-width:92vw;border:0;border-radius:12px;padding:0;background:transparent">
<button id="lbx" aria-label="Zamknij" style="position:absolute;top:8px;right:8px;z-index:2;width:38px;height:38px;border-radius:50%;border:0;background:rgba(11,18,38,.75);color:#fff;font-size:1.2rem;cursor:pointer">×</button>
<img alt="" style="max-height:86vh;border-radius:12px"></dialog>
<script>
document.body.classList.add('has-stickybar');
const lb=document.getElementById('lb');
if(lb){{document.querySelectorAll('#gal img').forEach(im=>{{const open=()=>{{lb.querySelector('img').src=im.dataset.full;lb.showModal()}};im.addEventListener('click',open);im.addEventListener('keydown',e=>{{if(e.key==='Enter'||e.key===' '){{e.preventDefault();open()}}}})}});
document.getElementById('lbx').addEventListener('click',()=>lb.close());
lb.addEventListener('click',e=>{{if(e.target===lb)lb.close()}});}}
</script>"""
    ld = [{"@context": "https://schema.org", "@type": "TouristTrip", "name": t["title"],
           "description": trunc(t["description"][0] if t["description"] else t["title"], 300),
           "touristType": "Polscy turyści", "image": f"{SITE}{hero_img(t)}",
           "provider": {"@type": "TravelAgency", "name": copy["brand"], "url": SITE},
           "offers": {"@type": "Offer", "price": t["price"], "priceCurrency": "USD",
                      "url": f"{SITE}/wycieczki/{t['slug']}/"}},
          breadcrumb_ld([("Strona główna", SITE + "/"), ("Wycieczki", f"{SITE}/wycieczki/"),
                         (t["title"], f"{SITE}/wycieczki/{t['slug']}/")])]
    write(f"wycieczki/{t['slug']}/index.html",
          shell(f"{t['shortTitle']} - od {usd(t['price'])} | Atrakcje Egiptu",
                trunc(t["description"][0] if t["description"] else t.get("teaser", t["title"])), body,
                f"{SITE}/wycieczki/{t['slug']}/", active="Wycieczki", jsonld=ld,
                og_img=f"{SITE}{hero_img(t)}", preload=hero_img(t), wa_float=False))


DEST_INTRO = {
    "hurghada": {
        "h1": "Wycieczki fakultatywne z Hurghady",
        "title": "Hurghada - wycieczki fakultatywne po polsku (ceny w USD)",
        "desc": "Wycieczki fakultatywne z Hurghady: Kair i piramidy, Luksor, rejsy na Orange Bay, safari na pustyni. Polski przewodnik, odbiór z hotelu, ceny w USD.",
        "intro": ["Hurghada to najlepsza baza wypadowa nad Morzem Czerwonym - stąd jest najbliżej i do Kairu, i do Luksoru, a rejsowe rafy Giftun czy Orange Bay leżą tuż za portem. Odbieramy z hoteli w całej Hurghadzie oraz z El Gouny, Makadi Bay, Soma Bay, Sahl Hasheesh i Safagi.",
                  "Poniżej pełna lista naszych wycieczek z Hurghady - od całodniowych wypraw do piramid po popołudniowe safari na quadach. Każdą rezerwujesz przez WhatsApp, płacisz na miejscu w dniu wyjazdu."]},
    "marsa-alam": {
        "h1": "Wycieczki fakultatywne z Marsa Alam",
        "title": "Marsa Alam - wycieczki fakultatywne po polsku (ceny w USD)",
        "desc": "Wycieczki z Marsa Alam: delfiny w Sataya, żółwie w Marsa Mubarak, Luksor, Kair i egipskie Malediwy Hamata. Polski przewodnik, odbiór z hotelu.",
        "intro": ["Marsa Alam to najdziksze rafy Egiptu: delfiny w zatoce Sataya, diugonie i żółwie w Marsa Mubarak i Abu Dabbab oraz rajskie wyspy Hamata, zwane egipskimi Malediwami. Stąd też wygodnie dojechać do Luksoru i Abu Simbel.",
                  "Odbieramy z hoteli w Marsa Alam, Port Ghalib i El Quseir. Wszystkie ceny w USD za osobę, rezerwacja przez WhatsApp bez przedpłaty."]},
    "sharm-el-sheikh": {
        "h1": "Wycieczki fakultatywne z Sharm el-Sheikh",
        "title": "Sharm el-Sheikh - wycieczki fakultatywne po polsku (ceny w USD)",
        "desc": "Wycieczki z Sharm el-Sheikh: Ras Mohammed, Góra Mojżesza, klasztor św. Katarzyny, rejsy i safari na Synaju. Polski przewodnik, ceny w USD.",
        "intro": ["Sharm el-Sheikh leży na styku pustyni Synaju i najsłynniejszego parku morskiego Egiptu - Ras Mohammed. To stąd wchodzi się nocą na Górę Mojżesza, by zobaczyć wschód słońca, i stąd najbliżej do klasztoru św. Katarzyny.",
                  "Odbieramy z hoteli w całym Sharm el-Sheikh, od Naama Bay po Nabq. Rezerwacja przez WhatsApp, płatność na miejscu."]},
}


def build_dest(bid, lbl, gen):
    meta = DEST_INTRO[bid]
    bt = [t for t in tours if t["base"] == lbl]
    cards = "".join(tour_card(t) for t in bt)
    intro = "".join(f"<p>{esc(p)}</p>" for p in meta["intro"])
    faqs = [f for f in copy["faq"] if "odbiór" in f["q"].lower() or "zarezerwować" in f["q"].lower() or "zapłacić" in f["q"].lower()]
    faq_html = "".join(f'<details><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>' for f in copy["faq"][:5])
    body = f"""
<section class="page-hero container">
<span class="eyebrow">Kierunek</span>
<h1>{esc(meta['h1'])}</h1>
{intro}
</section>
<section class="container"><div class="grid">{cards}</div></section>
<section class="section section-alt" style="margin-top:50px"><div class="container">
<h2>Częste pytania</h2><div class="faq">{faq_html}</div>
</div></section>
<div class="container"><div class="cta-band rv">
<div><h2>Twojego hotelu nie ma na liście?</h2><p>Napisz - obsługujemy także okoliczne kurorty i miejscowości.</p></div>
<a class="btn btn-wa" href="{wa_link(f'Dzień dobry! Pytanie o wycieczki z {lbl}.')}" target="_blank" rel="noopener">Zapytaj na WhatsApp</a>
</div></div>"""
    ld = [{"@context": "https://schema.org", "@type": "ItemList",
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/wycieczki/{t['slug']}/"}
                               for i, t in enumerate(bt)]},
          breadcrumb_ld([("Strona główna", SITE + "/"), (lbl, f"{SITE}/{bid}/")])]
    write(f"{bid}/index.html", shell(meta["title"], meta["desc"], body, f"{SITE}/{bid}/", active=lbl, jsonld=ld))


def post_card(p):
    return f"""<article class="card post-card rv">
<div class="card-img"><a href="/blog/{p['slug']}/" aria-label="{esc(p['title'])}"><img src="/assets/img/{p['img']}-s.webp" alt="{esc(p['title'])}" width="560" height="350" loading="lazy"></a></div>
<div class="card-body">
<span class="post-meta">{p['date']} · {p['readMinutes']} min czytania · {esc(p['category'])}</span>
<h3><a href="/blog/{p['slug']}/">{esc(p['title'])}</a></h3>
<p style="margin:0;color:var(--ink-soft);font-size:.92rem">{esc(p['excerpt'])}</p>
</div></article>"""


def build_blog():
    cards = "".join(post_card(p) for p in sorted(posts, key=lambda p: p["date"], reverse=True))
    body = f"""
<section class="page-hero container">
<span class="eyebrow">Blog</span>
<h1>Praktycznie o Egipcie</h1>
<p>Pogoda, wiza, waluta, zdrowie i bezpieczeństwo - piszemy o tym, o co naprawdę pytają polscy turyści, z perspektywy ludzi mieszkających w Egipcie.</p>
</section>
<section class="container"><div class="grid">{cards}</div></section>"""
    write("blog/index.html", shell("Blog o Egipcie - praktyczne porady | Atrakcje Egiptu",
          "Praktyczny blog o wakacjach w Egipcie: pogoda w Hurghadzie, wiza, waluta, zemsta faraona, bezpieczeństwo i pamiątki.",
          body, f"{SITE}/blog/", active="Blog"))


def build_post(p):
    related = [t for t in tours if t["category"] in p.get("relatedCategories", []) and t.get("photos")][:2] or tours[:2]
    rel = "".join(tour_card(t) for t in related)
    faq_html = ""
    if p.get("faq"):
        items = "".join(f'<details><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>' for f in p["faq"])
        faq_html = f'<h2>Najczęstsze pytania</h2><div class="faq">{items}</div>'
    body = f"""
<article class="article">
<span class="eyebrow">{esc(p['category'])}</span>
<h1>{esc(p['title'])}</h1>
<p class="post-meta">{p['date']} · {p['readMinutes']} min czytania</p>
<div class="article-hero plx"><img src="/assets/img/{p['img']}.webp" alt="{esc(p['title'])}" width="1600" height="900"></div>
{p['bodyHtml']}
{faq_html}
</article>
<section class="container" style="max-width:1180px">
<h2 style="font-family:var(--font-display)">Wycieczki, które pasują do tematu</h2>
<div class="grid" style="padding-top:12px">{rel}</div>
</section>"""
    ld = [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
           "datePublished": p["date"], "dateModified": p["date"], "inLanguage": "pl",
           "mainEntityOfPage": f"{SITE}/blog/{p['slug']}/",
           "author": {"@type": "Organization", "name": copy["brand"]},
           "publisher": {"@type": "Organization", "name": copy["brand"],
                         "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/logo.svg"}},
           "image": f"{SITE}/assets/img/{p['img']}.webp"}]
    if p.get("faq"):
        ld.append(faq_ld(p["faq"]))
    write(f"blog/{p['slug']}/index.html",
          shell(f"{p.get('metaTitle', p['title'])} | Atrakcje Egiptu", trunc(p["excerpt"]), body,
                f"{SITE}/blog/{p['slug']}/", active="Blog", jsonld=ld,
                og_img=f"{SITE}/assets/img/{p['img']}.webp", og_type="article"))


def build_privacy():
    body = f"""<section class="page-hero container" style="max-width:820px">
<span class="eyebrow">Formalności</span>
<h1>Polityka prywatności</h1>
<p>Ostatnia aktualizacja: sierpień 2026</p>
</section>
<article class="article" style="padding-top:0">
<h2>Kto przetwarza Twoje dane</h2>
<p>Administratorem danych jest Atrakcje Egiptu, agencja wycieczek fakultatywnych działająca w Hurghadzie (Egipt). Kontakt: {esc(copy['footer']['contact']['email'])}.</p>
<h2>Jakie dane zbieramy i po co</h2>
<p>Strona atrakcjeegiptu.pl nie używa formularzy, kont użytkowników ani plików cookies do śledzenia. Nie prowadzimy analityki reklamowej.</p>
<p>Gdy piszesz do nas na WhatsApp lub e-mail, otrzymujemy dane, które sam podasz (imię, numer telefonu, hotel, termin, liczba osób). Używamy ich wyłącznie do obsługi Twojej rezerwacji: potwierdzenia dostępności, organizacji odbioru z hotelu i kontaktu w sprawie wycieczki.</p>
<h2>Komu przekazujemy dane</h2>
<p>Dane rezerwacji trafiają tylko do osób realizujących wycieczkę (kierowca, przewodnik). Nie sprzedajemy ich i nie udostępniamy nikomu innemu. Komunikacja przez WhatsApp podlega także polityce prywatności Meta.</p>
<h2>Jak długo przechowujemy dane</h2>
<p>Historię rozmów przechowujemy do 12 miesięcy od wycieczki, na wypadek reklamacji, potem ją usuwamy.</p>
<h2>Twoje prawa</h2>
<p>Masz prawo do wglądu, poprawienia i usunięcia swoich danych oraz do ograniczenia ich przetwarzania. Wystarczy wiadomość na {esc(copy['footer']['contact']['email'])}.</p>
</article>"""
    write("polityka-prywatnosci/index.html",
          shell("Polityka prywatności | Atrakcje Egiptu",
                "Zasady przetwarzania danych osobowych na atrakcjeegiptu.pl - bez cookies, bez formularzy, dane tylko do obsługi rezerwacji.",
                body, f"{SITE}/polityka-prywatnosci/"))


def build_404():
    body = """<section class="page-hero container" style="min-height:50vh">
<span class="eyebrow">404</span><h1>Ta strona zaginęła na pustyni</h1>
<p>Nie ma takiego adresu. Wróć na stronę główną albo przejrzyj wycieczki.</p>
<p style="margin-top:24px"><a class="btn btn-gold" href="/">Strona główna</a>
<a class="btn btn-ghost" href="/wycieczki/" style="margin-left:10px">Wycieczki</a></p>
</section>"""
    write("404.html", shell("404 - Atrakcje Egiptu", "Strona nie istnieje.", body, f"{SITE}/404.html", noindex=True))


def build_meta_files():
    urls = [f"{SITE}/", f"{SITE}/wycieczki/", f"{SITE}/blog/"] + \
           [f"{SITE}/{bid}/" for bid, _, _ in BASES] + \
           [f"{SITE}/wycieczki/{t['slug']}/" for t in tours] + \
           [f"{SITE}/blog/{p['slug']}/" for p in posts] + \
           [f"{SITE}/polityka-prywatnosci/"]
    import datetime
    today = datetime.date.today().isoformat()
    items = "".join(f"<url><loc>{u.replace('&', '&amp;')}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    open(D("sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>')
    open(D("robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    top = [t for t in tours if t.get("photos")][:15]
    tour_lines = "\n".join(f"- [{t['title']}]({SITE}/wycieczki/{t['slug']}/): od {t['price']} USD, wyjazd z {t['base']}, {t.get('duration', '1 dzień')}" for t in top)
    post_lines = "\n".join(f"- [{p['title']}]({SITE}/blog/{p['slug']}/): {p['excerpt']}" for p in posts)
    open(D("llms.txt"), "w").write(f"""# Atrakcje Egiptu (atrakcjeegiptu.pl)

> Polskojęzyczna agencja wycieczek fakultatywnych w Egipcie. {len(tours)} wycieczek i kursów z odbiorem z hotelu w Hurghadzie, Marsa Alam i Sharm el-Sheikh. Wszystkie ceny w USD za osobę. Rezerwacja przez WhatsApp ({copy['footer']['contact']['whatsapp']}), płatność na miejscu bez przedpłat, bezpłatne odwołanie do 24 h przed wyjazdem.

## Kierunki
- [Wycieczki z Hurghady]({SITE}/hurghada/): {sum(1 for t in tours if t['base'] == 'Hurghada')} ofert - Kair, Luksor, Orange Bay, safari
- [Wycieczki z Marsa Alam]({SITE}/marsa-alam/): {sum(1 for t in tours if t['base'] == 'Marsa Alam')} ofert - delfiny Sataya, Abu Dabbab, Hamata
- [Wycieczki z Sharm el-Sheikh]({SITE}/sharm-el-sheikh/): {sum(1 for t in tours if t['base'] == 'Sharm el-Sheikh')} ofert - Ras Mohammed, Góra Mojżesza

## Popularne wycieczki
{tour_lines}

## Poradniki
{post_lines}
""")


def write(rel, html):
    path = D(rel)
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    open(path, "w").write(html)


if __name__ == "__main__":
    build_home()
    build_listing()
    for t in tours:
        build_tour(t)
    for bid, lbl, gen in BASES:
        build_dest(bid, lbl, gen)
    build_blog()
    for p in posts:
        build_post(p)
    build_privacy()
    build_404()
    build_meta_files()
    print("DONE:", 4 + len(BASES) + len(tours) + len(posts), "pages")
