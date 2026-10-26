# -*- coding: utf-8 -*-
# PDF de download da página /formula-atendimento, no padrão de documento da SVI
# (capa preta com logo branca, dourado #c9a44c, papel claro, Helvetica).
# Conteúdo: _gerador/formula_atendimento.json (o mesmo que alimenta o .docx).
# Uso: python3 _gerador/formula_atendimento_pdf.py
import base64, html, json, os, asyncio

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
D = json.load(open(os.path.join(AQUI, 'formula_atendimento.json'), encoding='utf-8'))
LOGO = base64.b64encode(open(os.path.expanduser('~/Dev/exatta-reuniao/logo-svi-white.png'), 'rb').read()).decode()
SAIDA = os.path.join(SITE, 'downloads', 'formula-da-primeira-resposta-svi.pdf')
e = html.escape
f1, f2, f3, f4 = D['secoes']


def h2(s):
    t = e(s['h2'])
    return t.replace(e(s['h2_em']), '<span>%s</span>' % e(s['h2_em'])) if s['h2_em'] else t


def paras(ps):
    return ''.join('<p>%s%s</p>' % (('<b>%s</b> ' % e(b)) if b else '', e(r)) for b, r in ps)


def cards(movs):
    return ''.join('<div class="card"><div class="num">%02d</div><div><h3>%s</h3>%s</div></div>' % (i, e(m['t']), paras(m['ps']))
                   for i, m in enumerate(movs, 1))


modelos = ''.join('<div class="modelo"><div class="lbl">%s</div><div class="msg">%s</div></div>' % (e(m['tag']), e(m['msg']).replace('\n\n', '<br><br>'))
                  for m in f3['modelos'])

CSS = """
@page{size:A4;margin:18mm 18mm 18mm}
@page:first{margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Helvetica Neue',Arial,sans-serif;color:#15110a;font-size:12pt;line-height:1.48;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.cover{background:#0a0808;color:#fff;height:297mm;padding:34mm 24mm 26mm;display:flex;flex-direction:column;page-break-after:always}
.cover img{width:130px;margin-bottom:auto}
.cover .kicker{color:#c9a44c;font-size:10pt;font-weight:700;letter-spacing:.18em;text-transform:uppercase;margin-bottom:14px}
.cover h1{font-size:52px;line-height:1.05;font-weight:800;letter-spacing:-.02em;margin-bottom:22px}
.cover h1 span{color:#c9a44c}
.cover .lead{font-size:13pt;color:#e9e1cf;max-width:150mm;line-height:1.55;margin-bottom:34px}
.cover .rod{border-top:1px solid rgba(201,164,76,.45);padding-top:14px;font-size:9.5pt;color:#b9ad92;display:flex;justify-content:space-between}
.section-title{text-wrap:balance;font-size:24px;font-weight:800;line-height:1.2;padding-bottom:8px;border-bottom:3px solid #c9a44c;margin:0 0 14px}
.section-title span{color:#8a6d22}
.intro{background:#faf5e9;border-left:4px solid #c9a44c;padding:14px 18px;margin-bottom:18px;font-size:12.5pt}
.formula{display:flex;align-items:stretch;gap:8px;margin:0 0 18px}
.formula div{flex:1;background:#0a0808;color:#fff;border-radius:10px;padding:14px 10px;text-align:center;font-weight:700;font-size:12pt;text-wrap:balance;display:flex;flex-direction:column;justify-content:center}
.formula div small{display:block;color:#c9a44c;font-size:8.5pt;letter-spacing:.12em;margin-bottom:3px}
.formula b{color:#c9a44c;font-size:18pt;align-self:center}
.card{display:flex;gap:16px;background:#fffdf8;border:1px solid #e7ddc4;border-radius:12px;padding:13px 18px;margin-bottom:10px;page-break-inside:avoid}
.num{flex:0 0 34px;height:34px;border-radius:50%;background:#0a0808;color:#c9a44c;font-weight:800;font-size:11pt;display:flex;align-items:center;justify-content:center}
.card h3{font-size:14pt;margin-bottom:4px}
.card p{margin-bottom:4px;font-size:11.5pt;line-height:1.45}
.card p:last-child{margin-bottom:0}
.vs{display:flex;gap:10px;margin-top:6px;page-break-inside:avoid}
.vs div{flex:1;border-radius:12px;padding:12px 14px}
.vs .nao{background:#f6ece8;border:1px solid #e8cfc6}
.vs .sim{background:#f0e7d2;border:1px solid #e0d1ab}
.vs h4{font-size:8.5pt;letter-spacing:.14em;text-transform:uppercase;margin-bottom:6px}
.vs .nao h4{color:#9a4a37}.vs .sim h4{color:#6b5520}
.vs li{list-style:none;padding:3px 0}
.quebra{page-break-before:always}
.modelo{background:#f7f1e3;border-radius:12px;padding:16px 18px;margin-bottom:12px;page-break-inside:avoid}
.lbl{color:#a08540;font-size:8.5pt;font-weight:800;letter-spacing:.14em;text-transform:uppercase;margin-bottom:6px}
.msg{font-size:13pt;line-height:1.55}
.nota{font-size:11pt;color:#5d5444;margin:4px 0 18px}
.plan{background:#0a0808;color:#efe7d4;border-radius:14px;padding:18px 20px;page-break-inside:avoid}
.plan h3{color:#c9a44c;font-size:16pt;margin-bottom:6px}
.plan a{display:inline-block;margin-top:10px;background:#c9a44c;color:#0a0808;font-weight:800;text-decoration:none;padding:9px 16px;border-radius:999px;font-size:10.5pt}
.fim{margin-top:14px;font-size:9pt;color:#8a8070;text-align:center}
"""

partes = ''.join('<div><small>%02d</small>%s</div>%s' % (i, e(m['t']), '<b>+</b>' if i < 3 else '') for i, m in enumerate(f1['movs'], 1))
corpo = f"""
<div class="cover">
  <img src="data:image/png;base64,{LOGO}" alt="SVI Company">
  <div class="kicker">{e(D['kicker'])}</div>
  <h1>A fórmula da<br><span>primeira resposta</span></h1>
  <p class="lead">{e(D['intro'])}</p>
  <div class="rod"><span>SVI Company · svicompany.com.br</span><span>@joaofalcao.svi</span></div>
</div>

<div class="section-title">{h2(f1)}</div>
<div class="intro">{e(f1['ps'][0])}</div>
<div class="formula">{partes}</div>
{cards(f1['movs'])}
<div class="vs">
  <div class="nao"><h4>Assim não</h4><ul>{''.join('<li>%s</li>' % e(x) for x in f1['nao'])}</ul></div>
  <div class="sim"><h4>Assim sim</h4><ul>{''.join('<li>%s</li>' % e(x) for x in f1['sim'])}</ul></div>
</div>

<div class="section-title quebra">{h2(f2)}</div>
{cards(f2['movs'])}

<div class="section-title quebra">{h2(f3)}</div>
<div class="intro">{e(f3['ps'][0])}</div>
{modelos}
<p class="nota">{e(f3['nota'])}</p>
<div class="plan"><h3>{e(f4['cta']['h'])}</h3><p>{e(f4['cta']['p'])}</p><a href="{e(f4['cta']['href'])}">{e(f4['cta']['btn'])}</a></div>
<p class="fim">SVI Company · svicompany.com.br/formula-atendimento</p>
"""
doc = '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>A fórmula da primeira resposta · SVI Company</title><style>%s</style></head><body>%s</body></html>' % (CSS, corpo)
open(os.path.join(AQUI, 'formula_atendimento_pdf.html'), 'w', encoding='utf-8').write(doc)


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.set_content(doc, wait_until='load')
        os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
        await pg.pdf(path=SAIDA, format='A4', print_background=True, prefer_css_page_size=True)
        await b.close()

asyncio.run(main())
print('PDF:', SAIDA, os.path.getsize(SAIDA), 'bytes')
