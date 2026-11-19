# -*- coding: utf-8 -*-
"""Génère les sept versions du site à partir de content.py (texte) et themes (mise en forme).

Usage : python _build/build.py
Chaque version suit la forme et le texte de la maquette des frères ; seules couleurs, polices,
en-tête et petites variations de mise en page changent (classes sur <body> + theme.css).
"""
import html, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import *  # noqa
import content_en as EN
import time
ASSET_V = time.strftime("%Y%m%d%H%M")  # numéro de version des CSS/JS : les navigateurs rechargent après chaque mise à jour

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = "../assets/img/"

# ------------------------------------------------------------------ les sept thèmes
# menu : "mega" (rubrique « L'abbaye » qui ouvre un panneau), "utility" (barre discrète au-dessus), "simple" (consignes seules)
THEMES = [
    dict(folder="1-maquette-des-freres", name="La maquette des frères", menu="maquette", tagline=False, color="#f7f4ee",
         fonts="family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400",
         cls="maquette", desc="La première version, telle qu’elle était : application fidèle des consignes, avec le formulaire et le choix de la langue en plus."),
    dict(folder="2-sept-fons", name="Sept-Fons", menu="utility", tagline=False, color="#ffffff",
         fonts="family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Source+Sans+3:wght@400;500;600",
         cls="light hero-center faq-plus page-banner quote-center",
         desc="Dans la continuité du site actuel : Playfair, noir, blanc et un rouge liturgique."),
    dict(folder="3-noir-et-blanc", name="Noir et blanc", menu="drawer", tagline=True, color="#ffffff",
         fonts="family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600",
         cls="light hero-center hero-inset faq-plus page-plain quote-center",
         desc="Le blanc et le noir de l’habit, rien d’autre. Sous-titre « Abbaye cistercienne fondée en 1132 »."),
    dict(folder="4-nocturne", name="Nocturne", menu="mega", tagline=False, color="#0f0e0c",
         fonts="family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Spectral:ital,wght@0,300;0,400;1,300",
         cls="dark dawn numerals anim hero-center faq-chevron page-banner quote-center",
         desc="De la nuit de l’office à la lumière du jour. Menu « L’abbaye » qui ouvre un panneau."),
    dict(folder="5-matines", name="Matines", menu="drawer", tagline=False, color="#eef1f3",
         fonts="family=Marcellus&family=Lora:ital,wght@0,400;0,500;1,400",
         cls="light hero-center faq-circle page-banner quote-left",
         desc="La lumière froide du petit matin."),
    dict(folder="6-terre", name="Terre", menu="mega", tagline=False, color="#f4f2ea",
         fonts="family=Literata:ital,opsz,wght@0,7..72,300;0,7..72,400;0,7..72,500;1,7..72,300&family=Work+Sans:wght@400;500;600",
         cls="light hero-left hero-inset faq-circle page-plain quote-left journee-stagger",
         desc="Le travail bien fait, les champs, le vert olive. Titres alignés à gauche."),
    dict(folder="7-ivoire", name="Ivoire", menu="utility", tagline=False, color="#f7f4ee",
         fonts="family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400",
         cls="light hero-center faq-plus page-plain quote-center",
         desc="La maquette des frères au plus près : fond clair, Garamond, barre discrète d’accès direct."),
    dict(folder="8-silence", name="Silence", menu="drawer", tagline=False, color="#f3f3f1",
         fonts="family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=IBM+Plex+Sans:wght@400;500",
         cls="light numerals anim hero-left hero-inset faq-chevron page-plain quote-left",
         desc="Très épuré, gris pierre, beaucoup d’espace. Sections numérotées."),
]


# ------------------------------------------------------------------ helpers
def inl(t):
    t = html.escape(t, quote=False)
    def lk(m):
        attrs = ' target="_blank" rel="noopener"' if m.group(2).startswith("http") else ""
        return f'<a href="{m.group(2)}"{attrs}>{m.group(1)}</a>'
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lk, t)
    t = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)
    # Typographie française : espaces insécables (le texte lui-même est inchangé)
    t = re.sub(r" ([?!:;»])", " \\1", t)
    t = t.replace("« ", "« ")
    return t.replace("\n", "<br>")


def slug(t):
    t = t.lower()
    for a, b in [("à", "a"), ("â", "a"), ("é", "e"), ("è", "e"), ("ê", "e"), ("î", "i"), ("ô", "o"),
                 ("û", "u"), ("ù", "u"), ("ç", "c"), ("’", "-"), ("'", "-")]:
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def ext(href):
    return ' target="_blank" rel="noopener"' if href.startswith("http") else ""


def img(key, alt, cls="", loading="lazy"):
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{IMG}{key}.jpg" alt="{html.escape(alt)}" loading="{loading}" decoding="async">'


def paras(ps):
    return "".join(f"<p>{inl(p)}</p>" for p in ps)


def faq(items):
    out = ['<div class="faq">']
    for q, answer in items:
        out.append('<details class="faq-item"><summary><span class="faq-icon" aria-hidden="true"></span>'
                   f'<span class="faq-q">{inl(q)}</span></summary><div class="faq-a">{paras(answer)}</div></details>')
    out.append("</div>")
    return "".join(out)


def more(label, href, soon="bientôt"):
    if href is None:
        return f'<span class="more is-soon" aria-disabled="true">{inl(label)} <small>{soon}</small></span>'
    return f'<a class="more" href="{href}"{ext(href)}>{inl(label)}</a>'


def btn(label, href, cls="btn"):
    return f'<a class="{cls}" href="{href}"{ext(href)}>{inl(label)}</a>'


# ------------------------------------------------------------------ blocs des pages intérieures
def render_blocks(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == "lead":
            out.append(f'<p class="lead">{inl(b[1])}</p>')
        elif k == "p":
            out.append(f"<p>{inl(b[1])}</p>")
        elif k == "h2":
            out.append(f'<h2 id="{slug(b[1])}">{inl(b[1])}</h2>')
        elif k == "h3":
            out.append(f"<h3>{inl(b[1])}</h3>")
        elif k == "anchor":
            out.append(f'<span id="{b[1]}" class="anchor"></span>')
        elif k == "quote":
            cite = f"<cite>{inl(b[2])}</cite>" if b[2] else ""
            out.append(f'<blockquote class="pull"><p>{inl(b[1])}</p>{cite}</blockquote>')
        elif k == "box":
            out.append(f'<aside class="box"><p class="box-title">{inl(b[1])}</p>{paras(b[2])}</aside>')
        elif k == "signs":
            out.append(f'<aside class="box signs"><p class="box-title">{inl(b[1])}</p><ol>' +
                       "".join(f"<li>{inl(p)}</li>" for p in b[2]) + "</ol></aside>")
        elif k == "img":
            cap = f"<figcaption>{inl(b[3])}</figcaption>" if b[3] else ""
            out.append(f'<figure class="wide">{img(b[1], b[2])}{cap}</figure>')
        elif k == "figure":
            cap = f"<figcaption>{inl(b[3])}</figcaption>" if b[3] else ""
            out.append(f'<figure class="portrait">{img(b[1], b[2])}{cap}</figure>')
        elif k == "imgs":
            out.append(f'<div class="duo n{len(b[1])}">' + "".join(f"<figure>{img(a, al)}</figure>" for a, al in b[1]) + "</div>")
        elif k == "btn":
            out.append(f'<p class="btn-row">{btn(b[1], b[2])}</p>')
        elif k == "lines":
            out.append('<p class="lines">' + "<br>".join(inl(l) for l in b[1]) + "</p>")
        elif k == "linkrow":
            out.append('<ul class="linkrow">' + "".join(f'<li><a href="{h}"{ext(h)}>{inl(l)}</a></li>' for l, h in b[1]) + "</ul>")
        elif k == "cta":
            out.append(f'<p class="btn-row">{btn(*HOME["contact"]["button"])}</p>')
        elif k == "tables":
            out.append('<div class="tables">')
            for title, sub, head, rows in b[1]:
                cap = f"<caption><span>{inl(title)}</span>" + (f" <small>{inl(sub)}</small>" if sub else "") + "</caption>"
                th = "".join(f'<th scope="col">{inl(h)}</th>' for h in head)
                body = "".join("<tr>" + f'<th scope="row">{inl(r[0])}</th>' + "".join(f"<td>{inl(c)}</td>" for c in r[1:]) + "</tr>" for r in rows)
                out.append(f'<table>{cap}<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>')
            out.append("</div>")
        elif k == "house":
            _, name, key, text, (lbl, href) = b
            out.append(f'<article class="house" id="{slug(name)}"><figure>{img(key, name)}</figure>'
                       f'<div class="house-body"><h2>{inl(name)}</h2><p>{inl(text)}</p>{more(lbl, href)}</div></article>')
        elif k == "contacts":
            out.append('<div class="contacts">')
            for title, lines, links in b[1]:
                out.append(f'<section class="contact-card"><h2>{inl(title)}</h2><p>' + "<br>".join(inl(l) for l in lines) + "</p>" +
                           "".join(f"<p>{more(l, h)}</p>" for l, h in links) + "</section>")
            out.append("</div>")
        else:
            raise ValueError(k)
    return "\n".join(out)


# ------------------------------------------------------------------ en-tête, langue, pied de page
def lang_switch(lang):
    items = []
    for code, name in LANGS:
        if code == lang:
            items.append(f'<li><span class="lang-cur" aria-current="true">{name}</span></li>')
        elif code == "fr":
            items.append(f'<li><a href="index.html" lang="fr" hreflang="fr">{name}</a></li>')
        elif code == "en":
            items.append(f'<li><a href="index-en.html" lang="en" hreflang="en">{name}</a></li>')
        else:
            items.append(f'<li><span class="lang-soon" lang="{code}">{name} <small>{"soon" if lang == "en" else "bientôt"}</small></span></li>')
    label = "Langue" if lang == "fr" else "Language"
    return (f'<div class="lang"><button class="lang-btn" type="button" aria-expanded="false" aria-haspopup="true" '
            f'aria-label="{label}" data-lang><span class="globe" aria-hidden="true"></span>{lang.upper()}</button>'
            f'<ul class="lang-list" hidden>{"".join(items)}</ul></div>')


def header(t, current, lang):
    L = lang == "en"
    nav = EN.NAV_EN if L else NAV
    cta_l, cta_h = EN.CTA_EN if L else CTA
    more_label = EN.MORE_LABEL_EN if L else MORE_LABEL
    groups = EN.MORE_EN if L else MORE
    util = EN.UTILITY_EN if L else UTILITY
    tag = (EN.TAGLINE_EN if L else "Abbaye cistercienne fondée en 1132") if t["tagline"] else ""
    brand_href = "index-en.html" if L else "index.html"

    items = []
    for label, href, sub in nav:
        cur = ' aria-current="page"' if current == label else ""
        if sub:
            subs = "".join(f'<li><a href="{h}">{inl(l)}</a></li>' for l, h in sub)
            items.append(f'<li class="has-sub"><a href="{href}"{cur}>{inl(label)}</a><ul class="sub">{subs}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cur}>{inl(label)}</a></li>')
    mega = ""
    if t["menu"] == "mega":
        items.append(f'<li class="more-li"><button class="more-btn" type="button" aria-expanded="false" aria-controls="mega" data-more>'
                     f'{inl(more_label)}<span class="caret" aria-hidden="true"></span></button></li>')
        cols = "".join(f'<div class="mega-col"><p class="mega-title">{inl(g)}</p><ul>' +
                       "".join(f'<li><a href="{h}"{ext(h)}>{inl(l)}</a></li>' for l, h in links) + "</ul></div>"
                       for g, links in groups)
        mega = (f'<div class="mega" id="mega" hidden data-mega><div class="mega-inner">'
                f'<figure class="mega-fig">{img("wa-clocher", "Le clocher de l’abbaye")}</figure>{cols}'
                f'<button class="mega-close" type="button" data-mega-close aria-label="Fermer">×</button></div></div>')
    utilbar = ""
    if t["menu"] == "utility":
        utilbar = ('<div class="util"><ul>' + "".join(f'<li><a href="{h}"{ext(h)}>{inl(l)}</a></li>' for l, h in util) + "</ul></div>")
    tag_html = f'<span class="tagline">{inl(tag)}</span>' if tag else ""
    left, right, drawer = lang_switch(lang), "", ""
    if t["menu"] == "drawer":
        cols = "".join(f'<div class="drawer-group"><p class="mega-title">{inl(g)}</p><ul>' +
                       "".join(f'<li><a href="{h}"{ext(h)}>{inl(l)}</a></li>' for l, h in links) + "</ul></div>"
                       for g, links in groups)
        left = (f'<button class="drawer-btn" type="button" aria-expanded="false" aria-controls="drawer" data-drawer>'
                f'<span class="bars" aria-hidden="true"></span><span class="drawer-label">{"Menu"}</span></button>')
        right = lang_switch(lang)
        drawer = (f'<div class="drawer" id="drawer" hidden data-drawer-panel><div class="drawer-backdrop" data-drawer-close></div>'
                  f'<aside class="drawer-panel" aria-label="{more_label}"><button class="drawer-close" type="button" data-drawer-close aria-label="{"Close" if L else "Fermer"}">×</button>'
                  f'<p class="drawer-brand">Abbaye de Sept-Fons</p>{cols}'
                  f'<p class="drawer-cta">{btn(cta_l, cta_h)}</p></aside></div>')
    return f"""<header class="site-header" data-header>
  {utilbar}
  <div class="h-top">
    <div class="h-left">{left}</div>
    <a class="brand" href="{brand_href}"><span class="brand-name">Abbaye de Sept-Fons</span>{tag_html}</a>
    <div class="h-right">{right}<a class="cta" href="{cta_h}">{inl(cta_l)}</a></div>
  </div>
  <nav class="main-nav" aria-label="{'Main navigation' if L else 'Navigation principale'}"><ul>{"".join(items)}</ul></nav>
  {mega}
</header>
{drawer}"""


def footer(lang):
    L = lang == "en"
    titles = EN.FOOTER_TITLES_EN if L else [g for g, _ in FOOTER_LINKS]
    cols = "".join(
        f'<div class="f-col"><p class="f-title">{inl(titles[i])}</p><ul>' +
        "".join(f'<li><a href="{h}"{ext(h)}>{inl(l)}</a></li>' for l, h in links) + "</ul></div>"
        for i, (_, links) in enumerate(FOOTER_LINKS))
    text = EN.FOOTER_TEXT_EN if L else FOOTER_TEXT
    q = EN.FOOTER_QUOTE_EN if L else FOOTER_QUOTE
    note = f'<p class="f-note">{EN.NOTE_EN}</p>' if L else ""
    return f"""<footer class="site-footer">
  <div class="f-inner">
    <div class="f-about">
      <p class="f-brand"><a href="{'index-en.html' if L else 'index.html'}">Abbaye de Sept-Fons</a></p>
      <p class="f-text">{inl(text)}</p>
      <blockquote class="f-quote"><p>{inl(q[0])}</p><cite>{inl(q[1])}</cite></blockquote>
      <p class="f-address">{"<br>".join(inl(l) for l in FOOTER_ADDRESS)}</p>
      {note}
    </div>
    {cols}
  </div>
  <p class="f-bottom"><span>© Abbaye Notre-Dame de Sept-Fons</span> <a href="../index.html">← {'Other versions' if L else 'Autres versions de la maquette'}</a></p>
</footer>"""


def shell(t, title, desc, body, current=None, body_cls="", lang="fr", extra_js=""):
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="{t['color']}">
<link rel="alternate" hreflang="fr" href="index.html">
<link rel="alternate" hreflang="en" href="index-en.html">
<link rel="icon" href="../assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{t['fonts']}&display=swap">
<link rel="stylesheet" href="../assets/css/base.css?v={ASSET_V}">
<link rel="stylesheet" href="theme.css?v={ASSET_V}">
<script>document.documentElement.classList.add("js")</script>
</head>
<body class="{t['cls']} menu-{t['menu']} {body_cls}">
<a class="skip" href="#contenu">{'Skip to content' if lang == 'en' else 'Aller au contenu'}</a>
{header(t, current, lang)}
<main id="contenu">
{body}
</main>
{footer(lang)}
<script src="../assets/js/site.js?v={ASSET_V}" defer></script>{extra_js}
{review_tags("../")}
</body>
</html>
"""


# ------------------------------------------------------------------ accueil (forme de la maquette des frères)
def home(H, lang="fr"):
    a, f, j, vo, c = H["ami"], H["freres"], H["journee"], H["vocation"], H["contact"]
    soon = "soon" if lang == "en" else "bientôt"
    return f"""
<section class="hero" aria-label="Ouverture">
  <div class="hero-media">{img(H["hero_img"][0], H["hero_img"][1], "", "eager")}</div>
  <h1 class="hero-title"><span>{inl(H["hero_title"][0])}</span> <span>{inl(H["hero_title"][1])}</span></h1>
</section>

<section class="s intro" data-n="I">
  <div class="narrow reveal">
    {paras(H["intro"])}
    {faq(H["intro_faq"])}
  </div>
</section>

<section class="s split" id="ami" data-n="II">
  <figure class="split-img">{img(*a["img"])}</figure>
  <div class="split-text reveal">
    <h2>{inl(a["title"])}</h2>
    {paras(a["paras"])}
    {faq(a["faq"])}
  </div>
</section>

<section class="quote-band" aria-label="Une parole pour s’arrêter">
  <blockquote class="reveal"><p><span>{inl(H["quote"][0])}</span> <span>{inl(H["quote"][1])}</span></p></blockquote>
</section>

<section class="s freres" id="freres" data-n="III">
  <figure class="big-img">{img(*f["img"])}</figure>
  <div class="narrow reveal">
    <h2>{inl(f["title"])}</h2>
    {paras(f["paras"])}
    {faq(f["faq"])}
    {more(*f["link"], soon=soon)}
  </div>
</section>

<section class="s journee" id="journee" data-n="IV">
  <div class="pair">{"".join(f"<figure>{img(k, al)}</figure>" for k, al in j["imgs"])}</div>
  <div class="narrow reveal">
    <h2>{inl(j["title"])}</h2>
    {paras(j["paras"])}
    {more(*j["link"], soon=soon)}
  </div>
</section>

<section class="s vocation" id="vocation" data-n="V">
  <div class="narrow reveal">
    <h2>{inl(vo["title"])}</h2>
    {paras(vo["paras"])}
    {faq(vo["faq"])}
    {more(*vo["link"], soon=soon)}
  </div>
</section>

<section class="s contact" id="ecrire" data-n="VI">
  <div class="narrow center reveal">
    <h2>{inl(c["title"])}</h2>
    {paras(c["paras"])}
    <p class="btn-row">{btn(*c["button"])}</p>
  </div>
</section>
"""


def gallery(p):
    if not p.get("gallery"):
        return ""
    out = ['<section class="gallery" aria-label="Photographies">']
    for title, photos in p["gallery"]:
        out.append(f'<h2 class="g-title">{inl(title)}</h2><div class="g-grid">')
        for key, alt in photos:
            out.append(f'<a class="g-item" href="{IMG}{key}.jpg" data-lightbox>{img(key, alt)}</a>')
        out.append("</div>")
    out.append("</section>")
    return "".join(out)


def page(p):
    nxt = "".join(f'<a href="{h}"><small>Pour continuer</small><span>{inl(l)}</span></a>' for l, h in p["next"])
    return f"""
<section class="page-hero">
  <figure class="ph-img">{img(p["hero"][0], p["hero"][1], "", "eager")}</figure>
  <div class="ph-title">
    <p class="kicker">{inl(p["kicker"])}</p>
    <h1>{inl(p["title"])}</h1>
  </div>
</section>
<article class="prose">
{render_blocks(p["blocks"])}
</article>
{gallery(p)}
<nav class="next" aria-label="Pour continuer">{nxt}</nav>
"""


# ------------------------------------------------------------------ formulaire « Nous écrire »
def form_page():
    def field(name, label, typ="text", req=False, extra="", hint=""):
        r = " required" if req else ""
        h = f'<small class="hint">{hint}</small>' if hint else ""
        return (f'<label class="fld"><span>{label}{" <i>*</i>" if req else ""}</span>'
                f'<input type="{typ}" name="{name}"{r}{extra}>{h}</label>')
    return f"""
<section class="page-hero form-hero">
  <div class="ph-title">
    <p class="kicker">Nous écrire</p>
    <h1>{inl(HOME["contact"]["title"])}</h1>
  </div>
</section>
<div class="form-wrap">
  <p class="form-intro">Choisissez l’objet de votre message et remplissez quelques champs : le message se rédige tout seul. Vous pouvez ensuite le relire et le modifier avant de l’envoyer.</p>
  <form class="smart-form" id="smart-form" novalidate>
    <fieldset class="objets">
      <legend>Objet</legend>
      <label class="objet"><input type="radio" name="objet" value="question" checked><span><b>Une question</b><small>Vie monastique, vocation, discernement</small></span></label>
      <label class="objet"><input type="radio" name="objet" value="sejour"><span><b>Un séjour ou une retraite</b><small>Hôtellerie — Père Hôtelier</small></span></label>
      <label class="objet"><input type="radio" name="objet" value="commande"><span><b>Une commande</b><small>Moulin de la Trappe, confitures, album</small></span></label>
    </fieldset>

    <div class="form-grid">
      <div class="form-fields">
        <div class="row2">
          {field("prenom", "Prénom", req=True, extra=' autocomplete="given-name"')}
          {field("nom", "Nom", req=True, extra=' autocomplete="family-name"')}
        </div>
        <div class="row2">
          {field("tel", "Téléphone", "tel", True, ' autocomplete="tel"')}
          {field("email", "E-mail", "email", True, ' autocomplete="email"')}
        </div>

        <div class="grp" data-for="question">
          <label class="fld"><span>Où en êtes-vous ?</span>
            <select name="situation">
              <option value="questions">Je me pose des questions sur la vie monastique</option>
              <option value="rencontre">J’aimerais rencontrer un frère pour en parler</option>
              <option value="decouvrir">J’aimerais venir quelques jours découvrir la vie de la communauté</option>
            </select></label>
          <div class="row2">
            {field("age", "Âge", "number", extra=' min="15" max="99" inputmode="numeric"', hint="facultatif")}
            <label class="fld"><span>Langue de réponse</span>
              <select name="langue"><option>Français</option><option>English</option><option>Deutsch</option><option>Español</option><option>Italiano</option><option>Čeština</option><option>Polski</option></select></label>
          </div>
          <label class="fld"><span>Votre question</span><textarea name="question" rows="3" placeholder="En quelques mots…"></textarea></label>
        </div>

        <div class="grp" data-for="sejour" hidden>
          <div class="row2">
            {field("arrivee", "Arrivée", "date", True)}
            {field("depart", "Départ", "date", True)}
          </div>
          <div class="row2">
            <label class="fld"><span>Type de séjour</span>
              <select name="type_sejour">
                <option value="retraite">Retraite individuelle</option>
                <option value="premiere">Première visite (3 ou 4 jours conseillés)</option>
                <option value="groupe">Séjour en groupe</option>
                <option value="jeunes">Groupe de jeunes</option>
              </select></label>
            {field("personnes", "Nombre de personnes", "number", extra=' min="1" max="60" value="1" inputmode="numeric"')}
          </div>
          <label class="chk"><input type="checkbox" name="vocation"><span>Je m’interroge sur la vie monastique et j’aimerais pouvoir parler avec un frère pendant mon séjour</span></label>
          <label class="fld"><span>Précisions</span><textarea name="precisions" rows="3" placeholder="Heure d’arrivée, régime alimentaire, besoin particulier…"></textarea></label>
        </div>

        <div class="grp" data-for="commande" hidden>
          <div class="lines-edit" data-lines>
            <div class="line"><label class="fld"><span>Produit</span><input name="produit" list="produits" placeholder="Ex. : Germalyne"></label>
              <label class="fld qty"><span>Quantité</span><input name="quantite" type="number" min="1" value="1" inputmode="numeric"></label></div>
          </div>
          <datalist id="produits"><option value="Germalyne"><option value="Confitures de l’abbaye"><option value="Album « Possibilités et mélodies »"></datalist>
          <button class="add-line" type="button" data-add-line>+ Ajouter un produit</button>
          <label class="fld"><span>Adresse de livraison <i>*</i></span><textarea name="adresse" rows="3" required autocomplete="street-address"></textarea></label>
          <p class="aside-note">Vous pouvez aussi commander directement sur la <a href="{SHOP_URL}" target="_blank" rel="noopener">boutique en ligne</a>.</p>
        </div>
      </div>

      <div class="form-preview">
        <p class="pv-to">Destinataire : <b data-to>La communauté</b></p>
        <label class="fld"><span>Sujet</span><input name="sujet" data-subject></label>
        <label class="fld"><span>Votre message <small>rédigé automatiquement, modifiable</small></span>
          <textarea name="message" rows="15" data-message></textarea></label>
        <button class="reset-msg" type="button" data-reset hidden>Rétablir le message automatique</button>
        <p class="form-errors" role="alert" data-errors></p>
        <p class="btn-row"><button class="btn" type="submit">Envoyer</button></p>
        <p class="form-status" role="status" data-status></p>
      </div>
    </div>
  </form>
  <p class="form-alt">Vous préférez téléphoner ? Standard : 04 70 48 14 90 · Produits : 04 70 48 14 70</p>
</div>
"""


# ------------------------------------------------------------------ VERSION 1 — la maquette des frères (rendu d'origine)
def mq_header(current, lang):
    L = lang == "en"
    nav = EN.NAV_EN if L else NAV
    cta_l, cta_h = EN.CTA_EN if L else CTA
    items = []
    for label, href, sub in nav:
        cur = ' aria-current="page"' if current == label else ""
        if sub:
            subs = "".join(f'<li><a href="{h}">{inl(l)}</a></li>' for l, h in sub)
            items.append(f'<li class="has-sub"><a href="{href}"{cur}>{inl(label)}</a><ul class="sub">{subs}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cur}>{inl(label)}</a></li>')
    return f"""<header class="site-header" data-header>
  <div class="h-inner">
    <a class="brand" href="{'index-en.html' if L else 'index.html'}">Abbaye de Sept-Fons</a>
    <nav class="main-nav" id="main-nav" aria-label="Navigation principale" data-nav>
      <ul>{"".join(items)}</ul>
      <a class="cta cta-mobile" href="{cta_h}">{inl(cta_l)}</a>
    </nav>
    {lang_switch(lang)}
    <a class="cta" href="{cta_h}">{inl(cta_l)}</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="main-nav" data-menu><span class="bars" aria-hidden="true"></span><span class="sr">Menu</span></button>
  </div>
</header>"""


# ------------------------------------------------------------------ VERSION 1 bis — maquette des frères V2 (notre proposition)
# Les quatre rubriques des consignes, puis « Menu » juste à droite d'« Une vocation ? » : tout le reste du site et « Nous écrire ».
V2 = dict(folder="maquette-des-freres-v2", name="La maquette des frères — V2", menu="v2", tagline=False, color="#f7f4ee",
          fonts=THEMES[0]["fonts"], cls="maquette v2",
          desc="La maquette des frères, gardée telle quelle, avec un menu plus calme : les quatre rubriques essentielles, "
               "puis « Menu » pour tout le reste du site et « Nous écrire ».")
V2_MORE = [   # menu volontairement court ; un lien peut porter des sous-liens (3e élément)
    ("Venir à Sept-Fons", [
        ("Horaires des offices", "horaires.html"),
        ("Hôtellerie", "hotellerie.html"),
        ("Horaires du magasin", "horaires.html#magasin"),
        ("Contacts et accès", "contact.html"),
    ]),
    ("L’abbaye", [
        ("Histoire de l’Abbaye", "histoire.html", [
            ("La croix de nos martyrs", "martyrs.html"),
            ("L’Ordre cistercien", "ocso.html"),
            ("Nos maisons-filles", "filiation.html"),
        ]),
    ]),
    ("Actualités", [
        ("SOURCE – Le Magazine", SOURCE_URL),
        ("Homélies", OLD + "/homelies/"),
        ("Album « Possibilités et mélodies »", "cd.html"),
        ("L’abbaye en images", "photos.html"),
    ]),
]
V2_MORE_EN = [
    ("Visiting Sept-Fons", [("Times of the Offices", "horaires.html"), ("Guesthouse", "hotellerie.html"),
                            ("Shop opening hours", "horaires.html#magasin"), ("Contacts and directions", "contact.html")]),
    ("The abbey", [("History of the Abbey", "histoire.html", [
        ("The cross of our martyrs", "martyrs.html"), ("The Cistercian Order", "ocso.html"), ("Daughter houses", "filiation.html")])]),
    ("News", [("SOURCE – The Magazine", SOURCE_URL), ("Homilies", OLD + "/homelies/"),
              ("Album “Possibilités et mélodies”", "cd.html"), ("The abbey in pictures", "photos.html")]),
]


def v2_link(e):
    l, h = e[0], e[1]
    sub = e[2] if len(e) > 2 else []
    subs = ('<ul class="drawer-sub">' + "".join(f'<li><a href="{sh}"{ext(sh)}>{inl(sl)}</a></li>' for sl, sh in sub) + "</ul>") if sub else ""
    return f'<li><a href="{h}"{ext(h)}>{inl(l)}</a>{subs}</li>'


def v2_header(current, lang):
    L = lang == "en"
    nav = EN.NAV_EN if L else NAV
    cta_l, cta_h = EN.CTA_EN if L else CTA
    groups = V2_MORE_EN if L else V2_MORE
    shop_l, don_l = ("Online shop", "Donate") if L else ("Boutique", "Faire un don")
    items, main_groups = [], []
    for label, href, sub in nav:
        cur = ' aria-current="page"' if current == label else ""
        if sub:
            subs = "".join(f'<li><a href="{h}">{inl(l)}</a></li>' for l, h in sub)
            items.append(f'<li class="has-sub"><a href="{href}"{cur}>{inl(label)}</a><ul class="sub">{subs}</ul></li>')
            main_groups.append(f'<li><a href="{href}"{cur}>{inl(label)}</a><ul class="drawer-sub">{subs}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cur}>{inl(label)}</a></li>')
            main_groups.append(f'<li><a href="{href}"{cur}>{inl(label)}</a></li>')
    cols = "".join(f'<div class="drawer-group"><p class="drawer-title">{inl(g)}</p><ul>' +
                   "".join(v2_link(e) for e in links) + "</ul></div>"
                   for g, links in groups)
    close = "Close" if L else "Fermer"
    actions = (f'<div class="drawer-actions"><a class="v2-write" href="{cta_h}">{inl(cta_l)}</a>'
               f'<a class="v2-act" href="{SHOP_URL}" target="_blank" rel="noopener">{shop_l}</a>'
               f'<a class="v2-act" href="don.html">{don_l}</a></div>')
    drawer = (f'<div class="drawer" id="drawer" hidden data-drawer-panel><div class="drawer-backdrop" data-drawer-close></div>'
              f'<aside class="drawer-panel" aria-label="Menu"><button class="drawer-close" type="button" data-drawer-close aria-label="{close}">×</button>'
              f'{actions}<div class="drawer-group drawer-main"><ul>{"".join(main_groups)}</ul></div>'
              f'<div class="drawer-cols">{cols}</div></aside></div>')
    return f"""<header class="site-header" data-header>
  <div class="h-inner">
    <a class="brand" href="{'index-en.html' if L else 'index.html'}">Abbaye de Sept-Fons</a>
    <nav class="main-nav" aria-label="{'Main navigation' if L else 'Navigation principale'}">
      <ul>{"".join(items)}</ul>
    </nav>
    <div class="h-end">
      <button class="v2-menu" type="button" aria-expanded="false" aria-controls="drawer" data-drawer><span class="bars" aria-hidden="true"></span><span>Menu</span></button>
      {lang_switch(lang)}
    </div>
  </div>
</header>
{drawer}"""


def mq_home(H, lang="fr"):
    a, f, j, vo, c = H["ami"], H["freres"], H["journee"], H["vocation"], H["contact"]
    soon = "soon" if lang == "en" else "bientôt"
    return f"""
<section class="hero" aria-label="Ouverture">
  {img(H["hero_img"][0], H["hero_img"][1], "hero-img", "eager")}
  <h1 class="hero-title"><span>{inl(H["hero_title"][0])}</span> <span>{inl(H["hero_title"][1])}</span></h1>
</section>
<section class="intro"><div class="narrow">{paras(H["intro"])}{faq(H["intro_faq"])}</div></section>
<section class="split" id="ami">
  <figure class="split-img">{img(*a["img"])}</figure>
  <div class="split-text"><h2>{inl(a["title"])}</h2>{paras(a["paras"])}{faq(a["faq"])}</div>
</section>
<section class="quote-band" aria-label="Une parole pour s’arrêter">
  <blockquote><p><span>{inl(H["quote"][0])}</span> <span>{inl(H["quote"][1])}</span></p></blockquote>
</section>
<section class="freres" id="freres">
  <figure class="big-img">{img(*f["img"])}</figure>
  <div class="narrow"><h2>{inl(f["title"])}</h2>{paras(f["paras"])}{faq(f["faq"])}{more(*f["link"], soon=soon)}</div>
</section>
<section class="journee" id="journee">
  <div class="pair">{"".join(f"<figure>{img(k, al)}</figure>" for k, al in j["imgs"])}</div>
  <div class="narrow"><h2>{inl(j["title"])}</h2>{paras(j["paras"])}{more(*j["link"], soon=soon)}</div>
</section>
<section class="vocation" id="vocation">
  <div class="narrow"><h2>{inl(vo["title"])}</h2>{paras(vo["paras"])}{faq(vo["faq"])}{more(*vo["link"], soon=soon)}</div>
</section>
<section class="contact" id="ecrire">
  <div class="narrow center"><h2>{inl(c["title"])}</h2>{paras(c["paras"])}<p class="btn-row">{btn(*c["button"])}</p></div>
</section>
"""


def mq_page(p):
    nxt = "".join(f'<a href="{h}">{inl(l)} →</a>' for l, h in p["next"])
    return f"""
<header class="page-head">
  <p class="kicker">{inl(p["kicker"])}</p>
  <h1>{inl(p["title"])}</h1>
</header>
<figure class="page-hero">{img(p["hero"][0], p["hero"][1], "", "eager")}</figure>
<article class="prose">
{render_blocks(p["blocks"])}
</article>
{gallery(p)}
<nav class="next" aria-label="Pour continuer"><p>Pour continuer</p>{nxt}</nav>
"""


def mq_shell(t, title, desc, body, current=None, body_cls="", lang="fr", extra_js=""):
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="{t['color']}">
<link rel="icon" href="../assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{t['fonts']}&display=swap">
<link rel="stylesheet" href="style.css?v={ASSET_V}">
<script>document.documentElement.classList.add("js")</script>
</head>
<body class="{'v2 ' if t['menu'] == 'v2' else ''}{body_cls}">
<a class="skip" href="#contenu">{'Skip to content' if lang == 'en' else 'Aller au contenu'}</a>
{v2_header(current, lang) if t['menu'] == 'v2' else mq_header(current, lang)}
<main id="contenu">
{body}
</main>
{footer(lang)}
<script src="../assets/js/site.js?v={ASSET_V}" defer></script>{extra_js}
{review_tags("../")}
</body>
</html>
"""


# ------------------------------------------------------------------ écriture
HOME_DESC = "Abbaye cistercienne trappiste de Sept-Fons (Allier) : chercher Dieu, prier et vivre chaque jour avec des frères. Et si Dieu m’appelait ?"


def main():
    for old in ["version-1-maquette", "version-2-clarte", "version-3-nocturne", "1-nocturne"]:
        shutil.rmtree(os.path.join(ROOT, old), ignore_errors=True)
    for t in [V2] + THEMES:
        d = os.path.join(ROOT, t["folder"])
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            if f.endswith(".html"):
                os.remove(os.path.join(d, f))
        w = lambda name, s: open(os.path.join(d, name), "w", encoding="utf-8").write(s)
        if t is V2:  # feuille de style de la version 1, plus le menu de la V2
            base = open(os.path.join(ROOT, THEMES[0]["folder"], "style.css"), encoding="utf-8").read()
            extra = open(os.path.join(ROOT, "_build", "v2.css"), encoding="utf-8").read()
            w("style.css", base + "\n" + extra)
        if t["menu"] in ("maquette", "v2"):
            sh, hm, pg = mq_shell, mq_home, mq_page
        else:
            sh, hm, pg = shell, home, page
        w("index.html", sh(t, "Abbaye de Sept-Fons", HOME_DESC, hm(HOME), None, "home"))
        w("index-en.html", sh(t, "Abbey of Sept-Fons", "Cistercian Trappist abbey of Sept-Fons (France).", hm(EN.HOME_EN, "en"), None, "home", "en"))
        for key in PAGE_ORDER:
            p = PAGES[key]
            desc = next((b[1] for b in p["blocks"] if b[0] in ("lead", "p")), p["title"])[:155]
            desc = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", desc)
            w(key + ".html", sh(t, f'{p["title"]} — Abbaye de Sept-Fons', desc, pg(p), p["nav"], "page page-" + key))
        w("ecrire.html", sh(t, "Nous écrire — Abbaye de Sept-Fons", "Écrire à l’abbaye de Sept-Fons : question, séjour à l’hôtellerie, commande.",
                               form_page(), None, "page page-ecrire", extra_js='\n<script src="../assets/js/form.js" defer></script>'))
        print("ok", t["folder"], len(PAGE_ORDER) + 3, "pages")
    chooser()


THUMBS = {"1-maquette-des-freres": "vaisselle", "4-nocturne": "bro-office", "3-noir-et-blanc": "bro-cloitre", "7-ivoire": "bro-livre",
          "5-matines": "wa-eglise", "6-terre": "bro-fourche", "2-sept-fons": "eglise-choeur", "8-silence": "wa-couchant"}
MENU_LABEL = {"mega": "Menu des consignes + rubrique « L’abbaye »", "utility": "Menu des consignes + barre d’accès direct",
              "simple": "Menu des consignes uniquement",
              "drawer": "Menu des consignes + menu à gauche pour tout le reste",
              "maquette": "Menu des consignes (regroupé sur téléphone)"}


# Destinataire du courriel préparé par « Envoyer mes remarques » (vide : seul le fichier est téléchargé)
REVIEW_EMAIL = ""
# Adresse de l'application Web Google Apps Script (_build/google-apps-script.gs) : remarques partagées en ligne
REVIEW_ENDPOINT = "https://script.google.com/macros/s/AKfycbyyz0rJNnj8nXJaCfWtXvzXwDhnYf72NvwK5JnJURjYThUWoz17hJ59n1WgfeZoBYOn/exec"


def review_tags(prefix):
    return (f'<link rel="stylesheet" href="{prefix}assets/css/review.css?v={ASSET_V}">\n'
            f'<script src="{prefix}assets/js/review.js?v={ASSET_V}" data-email="{html.escape(REVIEW_EMAIL)}" data-endpoint="{html.escape(REVIEW_ENDPOINT)}" defer></script>')


def chooser():
    HOWTO_END = ("<li>C’est tout : vos remarques s’enregistrent aussitôt dans le site, signées de votre prénom.</li></ol>\n"
                 "<p class=\"small\">Chaque frère voit les remarques des autres (pastilles sur la page, liste sous <b>☰</b>). "
                 "Le bouton <b>◉</b> masque ou affiche les remarques. "
                 "<a href=\"remarques.html\">Voir toutes les remarques, par version et par page →</a></p>")
    cards = "".join(
        f'<a class="card" href="{t["folder"]}/index.html" target="_blank" rel="noopener"><div class="thumb" style="background-image:url(assets/img/{THUMBS[t["folder"]]}.jpg)"></div>'
        f'<div class="body"><span class="n">Version {i}</span><h2>{t["name"]}</h2><p>{html.escape(t["desc"])}</p>'
        f'<p class="m">{MENU_LABEL[t["menu"]]}</p></div></a>' for i, t in enumerate(THEMES, 1))
    feat = (f'<a class="feat" href="{V2["folder"]}/index.html" target="_blank" rel="noopener">'
            f'<div class="feat-img" style="background-image:url(assets/img/bro-champs.jpg)"></div>'
            f'<div class="feat-body"><span class="n">Notre proposition</span><h2>{V2["name"]}</h2>'
            f'<p>{html.escape(V2["desc"])}</p>'
            f'<ul class="feat-list"><li>Le texte, les photos et la mise en page de la maquette des frères</li>'
            f'<li>Quatre rubriques au centre de la page : Chercher Dieu · Prier et vivre chaque jour · Avec des frères · Une vocation ?</li>'
            f'<li>À droite, « Menu » : Nous écrire, Boutique et Faire un don d’emblée, puis trois rubriques courtes : venir à Sept-Fons, l’abbaye, actualités</li></ul>'
            f'<span class="go">Ouvrir la proposition →</span></div></a>')
    s = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sept-Fons — maquettes du site</title><link rel="icon" href="assets/favicon.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600&display=swap">
<style>
:root{{--bg:#f5f2eb;--ink:#1f1c18;--ink-2:#655d52;--line:#ddd5c7;--accent:#8a6a3b}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:400 1rem/1.6 Inter,system-ui,sans-serif}}
header,main,footer{{max-width:76rem;margin:0 auto;padding-left:1.25rem;padding-right:1.25rem}}
header{{padding-top:4rem;padding-bottom:2rem}}
h1{{font:400 clamp(2.2rem,1.4rem + 3vw,3.6rem)/1.1 "Cormorant Garamond",serif;margin:0 0 .8rem}}
.howto{{max-width:48rem;color:var(--ink-2)}}.howto ol{{margin:.4rem 0 .6rem;padding-left:1.3rem}}.howto li{{margin:.25rem 0}}.howto b{{color:var(--ink);font-weight:600}}.small{{font-size:.88rem}}.lede{{margin:0}}
main{{padding-bottom:4rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(20rem,1fr));gap:1.25rem}}
a.card{{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:#fff;border:1px solid var(--line);border-radius:6px;overflow:hidden;transition:transform .25s,box-shadow .25s}}
a.card:hover{{transform:translateY(-3px);box-shadow:0 14px 40px rgba(0,0,0,.08)}}
.thumb{{aspect-ratio:16/10;background-size:cover;background-position:center}}
.body{{padding:1.1rem 1.3rem 1.4rem}}.n{{font-size:.72rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}}
h2{{font:500 1.7rem/1.2 "Cormorant Garamond",serif;margin:.2rem 0 .4rem}}.body p{{margin:0 0 .5rem;color:var(--ink-2);font-size:.93rem}}
.m{{font-size:.8rem!important;border-top:1px solid var(--line);padding-top:.6rem;margin-top:.8rem!important}}
a.feat{{display:grid;grid-template-columns:1.1fr 1fr;text-decoration:none;color:inherit;background:#fff;border:1px solid var(--ink);border-radius:6px;overflow:hidden;transition:box-shadow .25s}}
a.feat:hover{{box-shadow:0 18px 50px rgba(0,0,0,.1)}}
.feat-img{{min-height:22rem;background-size:cover;background-position:center}}
.feat-body{{padding:2rem 2.2rem 2.2rem}}.feat-body h2{{font-size:2.3rem}}.feat-body p{{color:var(--ink-2);margin:0 0 .8rem}}
.feat-list{{margin:0 0 1.2rem;padding-left:1.1rem;color:var(--ink-2);font-size:.93rem}}.feat-list li{{margin:.3rem 0}}
.go{{display:inline-block;background:var(--ink);color:#fff;padding:.6rem 1.2rem;border-radius:999px;font-weight:500;font-size:.95rem}}
a.feat:hover .go{{background:var(--accent)}}
.lead-in{{color:var(--ink-2);max-width:44rem;margin:0}}
.howto{{margin-top:2rem}}
.block{{max-width:76rem;margin:0 auto;padding:0 1.25rem}}
.others{{max-width:76rem;margin:3rem auto 0;padding:2.5rem 1.25rem 0;border-top:1px solid var(--line)}}.others h2{{font-size:2rem;margin:0}}.others p{{color:var(--ink-2);margin:.2rem 0 1.2rem;max-width:44rem}}
@media (max-width:820px){{a.feat{{grid-template-columns:1fr}}.feat-img{{min-height:0;aspect-ratio:16/10}}.feat-body{{padding:1.4rem 1.3rem 1.6rem}}.feat-body h2{{font-size:1.9rem}}}}
footer{{padding-top:2rem;padding-bottom:4rem;border-top:1px solid var(--line);color:var(--ink-2);font-size:.9rem}}footer ul{{padding-left:1.1rem}}
</style></head><body>
<header><h1>Abbaye de Sept-Fons — le nouveau site</h1>
<p class="lead-in">Voici la version que nous vous proposons. Les autres pistes explorées restent visibles plus bas : une couleur, une photo ou une idée peut y être reprise.</p></header>
<div class="block">{feat}
<div class="howto"><p class="lede">Ouvrez une version, puis donnez votre avis directement sur la page :</p>
<ol><li>Cliquez sur <b>✎ Commenter</b>, en bas à droite.</li>
<li>Cliquez sur l’élément de votre choix (titre, photo, menu, bouton…) : <b>👍 J’aime</b> ou <b>👎 Je n’aime pas</b>, et ajoutez une remarque si vous le souhaitez.</li>
{HOWTO_END}</div></div>
<section class="others"><h2>Autres pistes explorées</h2>
<p>Huit variations sur la même base : couleurs, polices et menus différents.</p></section>
<main>{cards}</main>
{review_tags("")}
</body></html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(s)
    remarques_page()


def remarques_page():
    """Page « Toutes les remarques » : lecture du recueil en ligne, classée par version puis par page."""
    pages = {"index.html": "Accueil", "index-en.html": "Accueil (anglais)", "ecrire.html": "Nous écrire"}
    pages.update({k + ".html": PAGES[k]["title"] for k in PAGE_ORDER})
    cfg = {"endpoint": REVIEW_ENDPOINT,
           "order": ["choix", V2["folder"]] + [t["folder"] for t in THEMES],
           "versions": {V2["folder"]: "Notre proposition · " + V2["name"],
                        **{t["folder"]: f"Version {i} · {t['name']}" for i, t in enumerate(THEMES, 1)}},
           "pages": pages,
           "pageOrder": ["index.html"] + [k + ".html" for k in PAGE_ORDER] + ["ecrire.html", "index-en.html"]}
    cfg_json = json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/")
    s = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Toutes les remarques — maquettes de Sept-Fons</title><link rel="icon" href="assets/favicon.png">
<meta name="robots" content="noindex">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&family=Inter:wght@400;500;600&display=swap">
<style>
:root{{--bg:#f5f2eb;--ink:#1f1c18;--ink-2:#655d52;--line:#ddd5c7;--accent:#8a6a3b;--like:#2f7d4f;--dis:#b23a3a;--note:#6b655c}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:400 1rem/1.55 Inter,system-ui,sans-serif}}
.wrap{{max-width:64rem;margin:0 auto;padding:2.5rem 1.25rem 5rem}}
.back{{color:var(--ink-2);font-size:.9rem;text-decoration:none}}.back:hover{{color:var(--ink)}}
h1{{font:400 clamp(2rem,1.4rem + 2.4vw,3rem)/1.1 "Cormorant Garamond",serif;margin:.6rem 0 .4rem}}
.meta{{color:var(--ink-2);font-size:.9rem;display:flex;flex-wrap:wrap;gap:.4rem 1rem;align-items:center;margin-bottom:1.6rem}}
button{{font:inherit;cursor:pointer;border:1px solid var(--line);background:#fff;border-radius:999px;padding:.35rem .9rem;color:var(--ink)}}button:hover{{border-color:var(--ink)}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);font-size:.92rem;margin-bottom:2rem}}
th,td{{padding:.55rem .8rem;border-bottom:1px solid var(--line);text-align:left}}td{{font-variant-numeric:tabular-nums}}
thead th{{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--ink-2);font-weight:600}}
tbody th{{font-weight:500}}tbody th a{{color:inherit}}tr.none{{color:#aaa49a}}
.summary-wrap{{overflow-x:auto}}
.filters{{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 1.5rem;position:sticky;top:0;background:var(--bg);padding:.7rem 0;z-index:2;border-bottom:1px solid var(--line)}}
select,input{{font:inherit;padding:.4rem .6rem;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--ink);min-width:0}}
input{{flex:1 1 12rem}}
#count{{align-self:center;color:var(--ink-2);font-size:.9rem;margin-left:auto}}
.version{{margin:2.4rem 0 0}}
.version h2{{font:500 1.8rem/1.2 "Cormorant Garamond",serif;margin:0 0 .4rem;padding-bottom:.4rem;border-bottom:2px solid var(--ink);display:flex;flex-wrap:wrap;justify-content:space-between;gap:.5rem;align-items:baseline}}
.version h3{{font-size:1rem;font-weight:600;margin:1.4rem 0 .6rem;display:flex;flex-wrap:wrap;justify-content:space-between;gap:.5rem}}
.version h3 a{{color:var(--ink)}}
.tally{{display:inline-flex;gap:.7rem;font:400 .85rem Inter,system-ui,sans-serif;color:var(--ink-2)}}
.items{{list-style:none;margin:0;padding:0;display:grid;gap:.6rem}}
.it{{background:#fff;border:1px solid var(--line);border-left:4px solid var(--note);border-radius:6px;padding:.8rem 1rem}}
.it.like{{border-left-color:var(--like)}}.it.dislike{{border-left-color:var(--dis)}}
.ih{{display:flex;flex-wrap:wrap;gap:.3rem .9rem;align-items:baseline;font-size:.9rem}}
.verdict{{font-weight:600}}.who{{font-weight:500}}.when{{color:var(--ink-2);font-size:.82rem}}
.el{{color:var(--ink-2);font-size:.88rem;margin-top:.2rem}}
.txt{{margin:.45rem 0 0;white-space:pre-wrap}}
.see{{display:inline-block;font-size:.85rem;color:var(--accent)}}
.acts{{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem 1rem;margin-top:.4rem}}
.edit{{padding:.2rem .7rem;font-size:.82rem}}
.ed{{margin:.5rem 0 0;display:grid;gap:.5rem}}
.ed-row{{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center}}
.ed-t{{width:100%;font:inherit;padding:.5rem .6rem;border:1px solid var(--line);border-radius:6px;resize:vertical}}
.ed-v{{font-size:.88rem;padding:.3rem .8rem}}.ed-v[aria-pressed=true]{{background:var(--ink);border-color:var(--ink);color:#fff}}
.ed-s{{background:var(--ink);color:#fff;border-color:var(--ink)}}.ed-s:hover{{background:var(--accent);border-color:var(--accent)}}
.ed-m{{font-size:.85rem;color:var(--dis)}}
.empty{{color:var(--ink-2);padding:2rem 0}}
.help{{background:#fff;border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:6px;padding:.8rem 1rem;margin:0 0 1.4rem;font-size:.93rem;color:var(--ink-2)}}.help b{{color:var(--ink)}}
.dec{{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem .5rem;margin-top:.7rem;padding-top:.6rem;border-top:1px dashed var(--line);font-size:.88rem}}
.dec-l{{color:var(--ink-2)}}.dec-s{{color:var(--ink-2);font-style:italic}}
.dec-b{{padding:.3rem .8rem;font-size:.88rem}}
.dec-b.garder[aria-pressed=true]{{background:var(--like);border-color:var(--like);color:#fff}}
.dec-b.ecarter[aria-pressed=true]{{background:var(--dis);border-color:var(--dis);color:#fff}}
.it.d-garder{{background:#f3f9f5}}.it.d-ecarter{{background:#f7f3f2;opacity:.75}}
</style></head><body>
<div class="wrap">
<a class="back" href="index.html">← Les versions du site</a>
<h1>Toutes les remarques</h1>
<div class="meta"><span id="status">Chargement…</span><button type="button" id="refresh">Actualiser</button><button type="button" id="csv">Exporter vers un tableur</button></div>
<p class="help">Pour préparer la version suivante, faites le point ensemble : sous chaque remarque, choisissez <b>✓ On garde</b> ou <b>✗ On écarte</b>. Le choix s’enregistre aussitôt et tous les frères le voient ; un second clic l’annule. Seules les remarques gardées seront prises en compte.</p>
<div class="summary-wrap" id="summary"></div>
<div class="filters" role="search">
<select id="f-version" aria-label="Version"></select>
<select id="f-verdict" aria-label="Avis"><option value="">Tous les avis</option><option value="like">👍 J’aime</option><option value="dislike">👎 Je n’aime pas</option><option value="note">💬 Remarque seule</option></select>
<select id="f-auteur" aria-label="Frère"></select>
<select id="f-decision" aria-label="Pour la V3"><option value="">Pour la V3 : tout</option><option value="atrancher">À trancher</option><option value="garder">✓ On garde</option><option value="ecarter">✗ On écarte</option></select>
<input id="f-q" type="search" placeholder="Rechercher dans les remarques" aria-label="Rechercher">
<span id="count"></span>
</div>
<div id="list"></div>
</div>
<script type="application/json" id="rv-config">{cfg_json}</script>
<script src="assets/js/remarques.js?v={ASSET_V}" defer></script>
</body></html>
"""
    open(os.path.join(ROOT, "remarques.html"), "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    main()
