# -*- coding: utf-8 -*-
"""Gerador do blog e das páginas de serviço do svicompany.com.br.

Lê blog.json e paginas.json (nesta pasta) e escreve os HTML na raiz do site:
  /gestor-de-trafego-pago-em-redencao.html, /agente-de-ia-e-crm-no-whatsapp.html,
  /onde-a-svi-atende-no-sul-do-para.html, /blog/index.html e /blog/<slug>.html

Uso:  python3 _gerador/gen.py
Regras que o gerador força: zero travessão, meia-risca e hífen duplo na saída;
JSON-LD com json.dumps; todo link interno conferido no fim.
"""
import io, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
BASE = "https://svicompany.com.br"
WA = "https://wa.me/5594992404033"
MAPS = "https://www.google.com/maps/place/?q=place_id:ChIJgUFCUBwJ4JIRxGxrGYLAPyo"
AUTOR = "João Vitor Falcão"
IG_AUTOR = "https://www.instagram.com/joaofalcao.svi"
IG_SVI = "https://www.instagram.com/svicompanyy"

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro"]

CSS = u"""
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'DM Sans',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;background:#0A0608;color:#F7F2E7;line-height:1.6;font-size:17px;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit}
img{max-width:100%;height:auto}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
.narrow{max-width:760px;margin:0 auto;padding:0 20px}
nav{border-bottom:1px solid rgba(245,241,232,.12);position:sticky;top:0;background:rgba(10,6,8,.94);backdrop-filter:blur(8px);z-index:10}
nav .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;height:64px}
nav img{height:36px;width:auto;display:block}
.nl{display:flex;gap:20px;align-items:center;font-size:15px}
.nl a{color:#DCD1B8;text-decoration:none}
.nl a:hover{color:#F0C744}
.btn{display:inline-block;white-space:nowrap;background:#D4A82C;color:#1A1218;font-weight:700;text-decoration:none;padding:12px 22px;border-radius:999px;font-size:15px}
.btn:hover{background:#F0C744}
.btn-o{background:transparent;color:#F7F2E7;border:1px solid rgba(245,241,232,.12);margin-left:8px;font-weight:500}
.btn-o:hover{background:#241820}
.eyebrow{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#D4A82C;margin-bottom:14px}
header.hero{padding:72px 0 56px}
h1{font-size:clamp(32px,5vw,52px);line-height:1.1;letter-spacing:-.025em;font-weight:700;max-width:22ch;overflow-wrap:break-word}
h1 .hl{color:#F0C744}
.lead{font-size:clamp(18px,1.6vw,21px);color:#DCD1B8;max-width:62ch;margin:22px 0 30px}
section{padding:56px 0;border-top:1px solid rgba(245,241,232,.12)}
h2{font-size:clamp(24px,3vw,34px);line-height:1.18;letter-spacing:-.02em;margin-bottom:14px;overflow-wrap:break-word}
h3{overflow-wrap:break-word}
.sub{color:#DCD1B8;max-width:64ch;margin-bottom:28px}
.sub a,.txt a,.art a,.card p a,.faqb a{color:#F0C744}
.txt p{color:#DCD1B8;max-width:66ch;margin-bottom:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.card{background:#1A1218;border:1px solid rgba(245,241,232,.12);border-radius:14px;padding:22px;min-width:0}
.card h3{font-size:19px;margin-bottom:8px;color:#F0C744}
.card p{color:#DCD1B8;font-size:16px}
.card .loc{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#A89B82;margin-bottom:10px}
ol.passos{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;counter-reset:c}
ol.passos li{counter-increment:c;background:#1A1218;border:1px solid rgba(245,241,232,.12);border-radius:12px;padding:16px;min-width:0}
ol.passos li:before{content:counter(c,decimal-leading-zero);display:block;font-size:13px;color:#D4A82C;margin-bottom:6px}
ol.passos b{display:block;margin-bottom:4px}
ol.passos span{font-size:15px;color:#DCD1B8}
address{font-style:normal;background:#1A1218;border:1px solid rgba(245,241,232,.12);border-radius:14px;padding:24px;max-width:540px;overflow-wrap:anywhere}
address strong{display:block;font-size:20px;margin-bottom:8px}
address a{color:#F0C744}
details{border-bottom:1px solid rgba(245,241,232,.12);padding:16px 0}
summary{cursor:pointer;font-weight:600;font-size:18px}
details p{color:#DCD1B8;margin-top:10px;max-width:66ch}
.lk{list-style:none;display:grid;gap:10px}
.lk a{display:block;background:#1A1218;border:1px solid rgba(245,241,232,.12);border-radius:12px;padding:16px 18px;text-decoration:none;color:#F7F2E7;font-weight:600;overflow-wrap:break-word}
.lk a:hover{border-color:#D4A82C}
.lk small{display:block;color:#A89B82;font-weight:400;font-size:14px;margin-top:2px}
.crumb{font-size:14px;color:#A89B82;margin-bottom:22px}
.crumb a{color:#DCD1B8}
.art{padding:48px 0 24px}
.art h1{max-width:none;font-size:clamp(28px,4.4vw,42px)}
.meta{color:#A89B82;font-size:14px;margin:16px 0 26px}
.tag{display:inline-block;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#D4A82C;margin-bottom:12px}
.resposta{background:#1A1218;border:1px solid rgba(212,168,44,.45);border-left:4px solid #D4A82C;border-radius:12px;padding:20px 22px;font-size:19px;color:#F7F2E7;margin-bottom:34px}
.art h2{margin-top:40px;font-size:clamp(22px,2.6vw,28px)}
.art p{color:#DCD1B8;margin-bottom:16px}
.art ul{margin:0 0 18px 22px;color:#DCD1B8}
.art li{margin-bottom:8px}
.fontes{margin-top:44px;padding-top:24px;border-top:1px solid rgba(245,241,232,.12)}
.fontes h2{font-size:22px;margin-top:0}
.fontes ul{margin-left:20px}
.fontes a{color:#F0C744;overflow-wrap:anywhere}
.faqb{margin-top:40px}
.faqb h2{margin-top:0}
.cta{margin:44px 0 8px;background:#1A1218;border:1px solid rgba(245,241,232,.12);border-radius:16px;padding:26px}
.cta h2{margin:0 0 10px;font-size:24px}
.cta p{margin-bottom:16px}
.cta .btn{margin:0 8px 10px 0}
.cta .btn-o{margin-left:0}
.cards-art{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.cards-art a{display:block;text-decoration:none;background:#1A1218;border:1px solid rgba(245,241,232,.12);border-radius:12px;padding:16px;min-width:0}
.cards-art a:hover{border-color:#D4A82C}
.cards-art b{display:block;color:#F7F2E7;font-size:16px;line-height:1.35;overflow-wrap:break-word}
.cards-art span{display:block;color:#A89B82;font-size:13px;margin-top:6px;text-transform:uppercase;letter-spacing:.08em}
.idx{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.idx a{display:block;text-decoration:none;background:#1A1218;border:1px solid rgba(245,241,232,.12);border-radius:14px;padding:22px;min-width:0}
.idx a:hover{border-color:#D4A82C}
.idx .tg{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#D4A82C}
.idx b{display:block;font-size:19px;line-height:1.3;margin:8px 0;color:#F7F2E7;overflow-wrap:break-word}
.idx p{color:#DCD1B8;font-size:15px}
footer{border-top:1px solid rgba(245,241,232,.12);padding:32px 0 40px;color:#A89B82;font-size:15px}
footer a{color:#DCD1B8}
footer p{overflow-wrap:anywhere}
@media(max-width:700px){.nl a.hide{display:none}}
@media(max-width:480px){.nl a:not(.btn){display:none}}
@media(max-width:560px){.btn-o{margin:10px 0 0}header.hero{padding:48px 0 40px}.nl{gap:12px;font-size:14px}.btn{padding:11px 16px}}
"""

LINKS_NAV = [("/gestor-de-trafego-pago-em-redencao", "Tráfego pago", False),
             ("/agente-de-ia-e-crm-no-whatsapp", "Agente de IA e CRM", True),
             ("/blog", "Blog", False)]


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def attr(t):
    return esc(t).replace('"', "&quot;")


def plain(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()


def ld(obj):
    return u'  <script type="application/ld+json">\n  %s\n  </script>\n' % json.dumps(obj, ensure_ascii=False, indent=2).replace("\n", "\n  ")


def wa(msg):
    return WA + u"?text=" + re.sub(r"[^A-Za-z0-9_.~-]", lambda m: "".join("%%%02X" % b for b in m.group(0).encode("utf-8")), msg)


ORG = {
    "@type": ["ProfessionalService", "LocalBusiness"],
    "@id": BASE + "/#org",
    "name": "SVI Company",
    "alternateName": ["Svi Company | Agência de marketing médico em Redenção", "SVI Company Agência de Marketing"],
    "description": "Agência de marketing em Redenção, no Pará. Tráfego pago, agente de IA, CRM no WhatsApp, Google Meu Negócio e conteúdo para empresas, comércio e clínicas, com acompanhamento diário.",
    "url": BASE + "/",
    "logo": BASE + "/images/logo-svi-company.png",
    "image": BASE + "/images/og-image.jpg",
    "telephone": "+55-94-99240-4033",
    "email": "svicompanyy@gmail.com",
    "foundingDate": "2021-05",
    "address": {"@type": "PostalAddress", "streetAddress": "Av. Santa Tereza, 110, 2º Piso, Sala 02",
                "addressLocality": "Redenção", "addressRegion": "PA", "postalCode": "68553-075", "addressCountry": "BR"},
    "geo": {"@type": "GeoCoordinates", "latitude": -8.0303168, "longitude": -50.0326338},
    "hasMap": MAPS,
    "areaServed": [{"@type": "City", "name": n, "containedInPlace": {"@type": "State", "name": "Pará"}}
                   for n in ("Redenção", "Xinguara", "Rio Maria", "Santana do Araguaia")] + [{"@type": "State", "name": "Pará"}],
    "sameAs": [IG_SVI, MAPS],
}


def breadcrumb(itens):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(itens)]}


def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faq]}


def head(title, desc, path, ogdesc=None, ldblocks=(), tipo="website", geo=False):
    url = BASE + path
    h = [u'<!DOCTYPE html>', u'<html lang="pt-BR">', u'<head>', u'  <meta charset="UTF-8">',
         u'  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5">',
         u'  <title>%s</title>' % esc(title),
         u'  <meta name="description" content="%s">' % attr(desc),
         u'  <meta name="theme-color" content="#0A0608">',
         u'  <meta name="author" content="SVI Company">']
    if geo:
        h += [u'  <meta name="geo.region" content="BR-PA">', u'  <meta name="geo.placename" content="Redenção">',
              u'  <meta name="geo.position" content="-8.0303168;-50.0326338">', u'  <meta name="ICBM" content="-8.0303168, -50.0326338">']
    h += [u'  <link rel="canonical" href="%s">' % url,
          u'  <meta property="og:type" content="%s">' % tipo,
          u'  <meta property="og:url" content="%s">' % url,
          u'  <meta property="og:title" content="%s">' % attr(title),
          u'  <meta property="og:description" content="%s">' % attr(ogdesc or desc),
          u'  <meta property="og:locale" content="pt_BR">',
          u'  <meta property="og:site_name" content="SVI Company">',
          u'  <meta property="og:image" content="%s/images/og-image.jpg?v=2">' % BASE,
          u'  <meta property="og:image:width" content="1200">', u'  <meta property="og:image:height" content="630">',
          u'  <meta name="twitter:card" content="summary_large_image">',
          u'  <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">',
          u'  <link rel="icon" type="image/png" sizes="64x64" href="/images/favicon-64.png">',
          u'  <link rel="apple-touch-icon" sizes="192x192" href="/images/favicon-192.png">']
    out = u"\n".join(h) + u"\n" + u"".join(ld(b) for b in ldblocks)
    out += u"  <style>%s  </style>\n</head>\n<body>\n" % CSS
    return out


def nav():
    links = u"".join(u'<a href="%s"%s>%s</a>' % (h, u' class="hide"' if hide else u"", t) for h, t, hide in LINKS_NAV)
    return (u'  <nav>\n    <div class="wrap">\n      <a href="/" aria-label="SVI Company"><img src="/images/logo-svi-company-white.png" alt="SVI Company" width="62" height="44"></a>\n'
            u'      <div class="nl">%s<a class="btn" href="%s" target="_blank" rel="noopener">Pedir diagnóstico</a></div>\n    </div>\n  </nav>\n'
            % (links, wa("Quero o diagnóstico de marketing da SVI")))


def footer():
    return (u'  <footer>\n    <div class="wrap">\n'
            u'      <p>© 2026 SVI Company · Av. Santa Tereza, 110, 2º Piso, Sala 02, Núcleo Urbano, Redenção, PA, 68553-075 · <a href="%s" target="_blank" rel="noopener">(94) 99240-4033</a></p>\n'
            u'      <p style="margin-top:8px"><a href="/">Página inicial</a> · <a href="/gestor-de-trafego-pago-em-redencao">Gestor de tráfego pago</a> · <a href="/agente-de-ia-e-crm-no-whatsapp">Agente de IA e CRM</a> · <a href="/onde-a-svi-atende-no-sul-do-para">Onde a SVI atende</a> · <a href="/agencia-de-marketing-em-redencao">Agência em Redenção</a> · <a href="/blog">Blog</a> · <a href="https://medicos.svicompany.com.br">Marketing médico</a> · <a href="/politica-de-privacidade">Privacidade</a> · <a href="/termos-de-uso">Termos de uso</a></p>\n'
            u'    </div>\n  </footer>\n</body>\n</html>\n' % WA)


def nap_block():
    return (u'<address>\n        <strong>SVI Company</strong>\n        Av. Santa Tereza, 110, 2º Piso, Sala 02<br>\n'
            u'        Núcleo Urbano, Redenção, PA, 68553-075<br>\n'
            u'        WhatsApp: <a href="%s" target="_blank" rel="noopener">(94) 99240-4033</a><br>\n'
            u'        E-mail: <a href="mailto:svicompanyy@gmail.com">svicompanyy@gmail.com</a><br>\n'
            u'        Instagram: <a href="%s" target="_blank" rel="noopener">@svicompanyy</a><br>\n'
            u'        <a href="%s" target="_blank" rel="noopener">Ver no Google Maps e nas avaliações</a>\n      </address>' % (WA, IG_SVI, MAPS))


def faq_html(faq, classe=u""):
    return u"".join(u"<details><summary>%s</summary><p>%s</p></details>\n      " % (esc(q), a) for q, a in faq)


def lista(txt):
    return u"<ul>" + u"".join(u"<li>%s</li>" % i for i in txt[5:].split("|")) + u"</ul>"


# secao: páginas de serviço
def secao_html(s, artigos):
    t = s["tipo"]
    out = [u'  <section>\n    <div class="wrap">\n      <h2>%s</h2>' % s["h2"]]
    if s.get("sub"):
        out.append(u'      <p class="sub">%s</p>' % s["sub"])
    if t == "cards":
        out.append(u'      <div class="grid">')
        for h, p in s["itens"]:
            out.append(u'        <div class="card"><h3>%s</h3><p>%s</p></div>' % (h, p))
        out.append(u'      </div>')
    elif t == "cidades":
        out.append(u'      <div class="grid">')
        for nome, loc, p in s["itens"]:
            out.append(u'        <div class="card"><p class="loc">%s</p><h3>%s</h3><p>%s</p></div>' % (loc, nome, p))
        out.append(u'      </div>')
    elif t == "texto":
        out.append(u'      <div class="txt">' + u"".join(u"<p>%s</p>" % p for p in s["paras"]) + u"</div>")
    elif t == "passos":
        out.append(u'      <ol class="passos">' + u"".join(u"<li><b>%s</b><span>%s</span></li>" % (h, p) for h, p in s["itens"]) + u"</ol>")
    elif t == "artigos":
        out.append(u'      <ul class="lk">' + u"".join(
            u'<li><a href="/blog/%s">%s<small>%s</small></a></li>' % (sl, esc(artigos[sl]["h1"]), esc(artigos[sl]["tag"])) for sl in s["slugs"]) + u"</ul>")
    elif t == "nap":
        out.append(u"      " + nap_block())
    out.append(u'    </div>\n  </section>\n')
    return u"\n".join(out)


def gerar_pagina(p, artigos):
    slug = p["slug"]
    path = "/" + slug
    sch = p["schema"]
    cidades_area = [{"@type": "City", "name": n, "containedInPlace": {"@type": "State", "name": "Pará"}}
                    for n in ("Redenção", "Xinguara", "Rio Maria", "Santana do Araguaia")]
    blocos = []
    if sch.get("tipo") == "regional":
        regional = dict(ORG)
        regional["@context"] = "https://schema.org"
        regional["url"] = BASE + path
        regional["description"] = "A SVI Company atende empresas, comércio e clínicas em Redenção, Xinguara, Rio Maria e Santana do Araguaia, no Sul do Pará. Base na Av. Santa Tereza, 110, Redenção."
        blocos.append(regional)
    else:
        org = dict(ORG)
        servico = {"@context": "https://schema.org", "@type": "Service", "@id": BASE + path + "#servico",
                   "name": sch["serviceName"], "serviceType": sch["serviceType"], "description": sch["serviceDesc"],
                   "url": BASE + path, "provider": org, "areaServed": cidades_area + [{"@type": "State", "name": "Pará"}],
                   "audience": {"@type": "BusinessAudience", "audienceType": "Empresas, comércio e clínicas"},
                   "availableChannel": {"@type": "ServiceChannel", "serviceUrl": wa(p["ctaMsg"]),
                                        "servicePhone": {"@type": "ContactPoint", "telephone": "+55-94-99240-4033", "contactType": "customer service", "availableLanguage": "pt-BR"}}}
        blocos.append(servico)
    blocos.append(faq_ld(p["faq"]))
    blocos.append(breadcrumb([("Início", BASE + "/"), (plain(p["h1"]), BASE + path)]))
    h = head(p["title"], p["desc"], path, p.get("ogDesc"), blocos, geo=True)
    corpo = [nav(), u'  <header class="hero">\n    <div class="wrap">\n      <p class="eyebrow">%s</p>\n      <h1>%s</h1>\n      <p class="lead">%s</p>\n'
             u'      <a class="btn" href="%s" target="_blank" rel="noopener">%s</a>\n'
             u'      <a class="btn btn-o" href="#perguntas">Ver perguntas frequentes</a>\n    </div>\n  </header>\n'
             % (p["eyebrow"], p["h1"], p["lead"], wa(p["ctaMsg"]), p["cta"])]
    for s in p["secoes"]:
        corpo.append(secao_html(s, artigos))
    corpo.append(u'  <section id="perguntas">\n    <div class="wrap">\n      <h2>Perguntas frequentes</h2>\n      %s'
                 u'<p style="margin-top:28px"><a class="btn" href="%s" target="_blank" rel="noopener">%s</a></p>\n    </div>\n  </section>\n'
                 % (faq_html(p["faq"]), wa(p["ctaMsg"]), p["cta"]))
    corpo.append(footer())
    return path, h + u"".join(corpo)


# secao: blog
def data_extenso(iso):
    a, m, d = iso.split("-")
    return u"%d de %s de %s" % (int(d), MESES[int(m) - 1], a)


def gerar_artigo(a, dados, todos):
    slug = a["slug"]
    path = "/blog/" + slug
    iso = dados["dataPublicacao"]
    titulo = a["metaTitle"] + u" | SVI Company"
    artigo = {"@context": "https://schema.org", "@type": "Article", "headline": plain(a["h1"]), "description": a["desc"],
              "inLanguage": "pt-BR", "datePublished": iso, "dateModified": iso, "articleSection": a["tag"],
              "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + path},
              "image": BASE + "/images/og-image.jpg",
              "author": {"@type": "Person", "name": AUTOR, "sameAs": [IG_AUTOR], "jobTitle": "Fundador da SVI Company",
                         "worksFor": {"@type": "Organization", "name": "SVI Company", "url": BASE + "/"}},
              "publisher": {"@type": "Organization", "name": "SVI Company", "url": BASE + "/",
                            "logo": {"@type": "ImageObject", "url": BASE + "/images/logo-svi-company.png"}},
              "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".resposta"]},
              "citation": [{"@type": "CreativeWork", "name": n, "url": u} for n, u in a["fontes"]]}
    blocos = [artigo, faq_ld(a["faq"]), breadcrumb([("Início", BASE + "/"), ("Blog", BASE + "/blog"), (plain(a["h1"]), BASE + path)])]
    h = head(titulo, a["desc"], path, None, blocos, tipo="article")
    corpo = [nav()]
    corpo.append(u'  <main class="art">\n    <div class="narrow">\n      <p class="crumb"><a href="/">Início</a> / <a href="/blog">Blog</a> / %s</p>\n'
                 u'      <span class="tag">%s</span>\n      <h1>%s</h1>\n'
                 u'      <p class="meta">Por %s, fundador da SVI Company · %s · %s de leitura</p>\n'
                 u'      <div class="resposta">%s</div>\n' % (esc(a["tag"]), esc(a["tag"]), a["h1"], AUTOR, data_extenso(iso), a["leitura"], a["resposta"]))
    for h2, paras in a["secoes"]:
        corpo.append(u"      <h2>%s</h2>" % h2)
        for p in paras:
            corpo.append(lista(p) if p.startswith("LIST:") else u"      <p>%s</p>" % p)
    corpo.append(u'      <div class="fontes"><h2>Fontes oficiais</h2><ul>%s</ul></div>' %
                 u"".join(u'<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, esc(n)) for n, u in a["fontes"]))
    corpo.append(u'      <div class="faqb"><h2>Perguntas frequentes</h2>\n      %s</div>' % faq_html(a["faq"]))
    corpo.append(u'      <div class="cta"><h2>Quer isso funcionando na sua empresa?</h2>'
                 u'<p>A SVI Company, de Redenção, cuida do <a href="/gestor-de-trafego-pago-em-redencao">tráfego pago</a> e do <a href="/agente-de-ia-e-crm-no-whatsapp">agente de IA e do CRM no WhatsApp</a>, com acompanhamento diário. O primeiro passo é um diagnóstico gratuito.</p>'
                 u'<a class="btn" href="%s" target="_blank" rel="noopener">Pedir o diagnóstico gratuito</a>'
                 u'<a class="btn btn-o" href="/onde-a-svi-atende-no-sul-do-para">Onde a SVI atende</a></div>' % wa("Li o artigo %s no blog da SVI e quero o diagnóstico" % plain(a["h1"])[:60]))
    rel = u"".join(u'<a href="/blog/%s"><b>%s</b><span>%s</span></a>' % (r, esc(todos[r]["h1"]), esc(todos[r]["tag"])) for r in a["rel"])
    corpo.append(u'      <div class="faqb"><h2>Continue lendo</h2><div class="cards-art">%s</div></div>\n    </div>\n  </main>\n' % rel)
    corpo.append(footer())
    return path, h + u"\n".join(corpo)


def gerar_indice(dados, todos):
    path = "/blog"
    titulo = "Blog da SVI Company: Tráfego Pago, IA e Vendas"
    desc = "Artigos da SVI Company sobre tráfego pago, agente de IA, CRM no WhatsApp e funil de vendas para empresas e negócios locais, com fontes oficiais."
    itens = dados["artigos"]
    colecao = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Blog da SVI Company", "url": BASE + path,
               "description": desc, "inLanguage": "pt-BR", "publisher": {"@type": "Organization", "name": "SVI Company", "url": BASE + "/"},
               "mainEntity": {"@type": "ItemList", "itemListElement": [
                   {"@type": "ListItem", "position": i + 1, "url": BASE + "/blog/" + a["slug"], "name": plain(a["h1"])} for i, a in enumerate(itens)]}}
    h = head(titulo, desc, path, None, [colecao, breadcrumb([("Início", BASE + "/"), ("Blog", BASE + path)])])
    cards = u"".join(u'<a href="/blog/%s"><span class="tg">%s</span><b>%s</b><p>%s</p></a>\n        ' % (a["slug"], esc(a["tag"]), a["h1"], esc(a["desc"])) for a in itens)
    corpo = [nav(),
             u'  <header class="hero">\n    <div class="wrap">\n      <p class="eyebrow">Blog</p>\n      <h1>Tráfego pago, IA e vendas para <span class="hl">negócios locais</span></h1>\n'
             u'      <p class="lead">Respostas diretas, com fonte oficial quando o assunto é regra. Escritas pela SVI Company, de Redenção, para quem vende no Sul do Pará e quer entender o que contratar.</p>\n'
             u'      <a class="btn" href="/gestor-de-trafego-pago-em-redencao">Gestor de tráfego pago</a>\n'
             u'      <a class="btn btn-o" href="/agente-de-ia-e-crm-no-whatsapp">Agente de IA e CRM</a>\n    </div>\n  </header>\n'
             u'  <section>\n    <div class="wrap">\n      <h2>Todos os artigos</h2>\n      <div class="idx">\n        %s</div>\n    </div>\n  </section>\n' % cards,
             footer()]
    return path, h + u"".join(corpo)


def checar(arquivos):
    ok = True
    for rel, html in arquivos.items():
        for blk in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, flags=re.S):
            try:
                json.loads(blk)
            except Exception as e:
                print("JSON-LD inválido em", rel, e); ok = False
        if re.search(u"[%s%s]|%s" % (chr(0x2014), chr(0x2013), "-" * 2), html):
            print("travessão/meia-risca/hífen duplo em", rel); ok = False
        if re.search(r"\ba gente\b", html, flags=re.I):
            print("a gente em", rel); ok = False
    internos = set()
    for rel, html in arquivos.items():
        for href in re.findall(r'href="(/[^"#?]*)', html):
            internos.add(href)
    existentes = {("/" + r[:-5]) if not r.endswith("index.html") else ("/" + r[:-11]) for r in arquivos}
    for href in sorted(internos):
        if href == "/":
            continue
        alvo = href.rstrip("/")
        if alvo in existentes:
            continue
        if os.path.exists(os.path.join(RAIZ, alvo.lstrip("/") + ".html")) or os.path.exists(os.path.join(RAIZ, alvo.lstrip("/"))):
            continue
        print("link interno sem destino:", href); ok = False
    return ok


def main():
    blog = json.load(io.open(os.path.join(AQUI, "blog.json"), encoding="utf-8"))
    pag = json.load(io.open(os.path.join(AQUI, "paginas.json"), encoding="utf-8"))
    todos = {a["slug"]: a for a in blog["artigos"]}
    saida = {}
    for p in pag["paginas"]:
        path, html = gerar_pagina(p, todos)
        saida[p["slug"] + ".html"] = html
    for a in blog["artigos"]:
        path, html = gerar_artigo(a, blog, todos)
        saida["blog/%s.html" % a["slug"]] = html
    path, html = gerar_indice(blog, todos)
    saida["blog/index.html"] = html
    if not checar(saida):
        sys.exit("falhou na checagem; nada foi escrito")
    os.makedirs(os.path.join(RAIZ, "blog"), exist_ok=True)
    for rel, html in saida.items():
        io.open(os.path.join(RAIZ, rel), "w", encoding="utf-8").write(html)
    print("escritos:", len(saida))
    for rel in sorted(saida):
        print(" ", rel)


if __name__ == "__main__":
    main()
