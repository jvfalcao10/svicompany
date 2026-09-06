# Carrosséis SVI Médicos — Gerador

Sistema pra gerar carrosséis de Instagram (1080×1350) na identidade visual dos posts do @joaofalcao.svi (referência: `ig/setembro-bd/`).

## Identidade visual

- **Fundos**: dark cinematic (preto `#0B0A08` + brilho dourado) pra capa, storytelling e frases de impacto; creme `#F0EBDF` pros slides de conteúdo.
- **Cores**: preto `#141311`, creme `#F0EBDF`, dourado `#A8863F` / `#D0B870`, gradiente dourado `#E8D49A → #8A6D22`.
- **Tipografia**: Archivo 800/900 (títulos, caps, tracking apertado) + DM Sans (corpo). Fontes locais em `fonts/` (não depende de rede).
- **Header fixo**: "Movido pela SVI" (esq) + "@joaofalcao.svi" (dir) em todos os slides.
- **Recursos**: destaque dourado com `*asteriscos*` no texto, divider dourado, números gigantes em gradiente, caixas pretas de label, comparativo com VS, pill de CTA.

## Como gerar um carrossel novo

1. Copie um `content.json` existente (ex.: `ig/relogio-whatsapp/content.json`) pra uma pasta nova em `ig/<slug>/`.
2. Edite os slides. Tipos disponíveis:

| Tipo | Fundo | Uso |
|---|---|---|
| `cover` | dark | Capa: avatar + headline com `*destaque*` + kicker |
| `story` | dark | Storytelling em 1ª pessoa (lead + parágrafos) |
| `text` | creme | Título + subtítulo + stat gigante opcional + corpo |
| `compare` | creme | Duas colunas com VS, conclusões e notas de rodapé |
| `step` | creme | Passo numerado (num + label + título sublinhado + corpo) |
| `punch` | dark | Frase de impacto ("Anota o que eu tô falando...") |
| `final` | creme | Fechamento + pill de CTA ("Comente X...") |

3. Renderize:

```bash
cd ig/templates
node render.mjs ../<slug>/content.json ../<slug>
```

Sai um `slide-NN.jpg` por slide, pronto pra subir no Instagram.

Pra conferir no navegador antes de renderizar, abra `carrossel-medicos.html` direto (mostra um exemplo) ou rode o render e olhe os JPGs.

## Linha editorial (informa + entretém)

Ângulos que funcionam pro público (médicos donos de consultório):

- **Vendas/comercial**: WhatsApp, secretária, tempo de resposta, no-show, follow-up.
- **Marketing**: custo por paciente, Meta Ads, criativos, funil do consultório.
- **Notícias/em alta**: eventos que mexem no leilão do Meta (eleição, Black Friday, datas), mudanças de plataforma, regras do CFM.
- **Bastidor com número**: "eu opero R$X por mês e vejo isso" — dado interno + opinião forte.

Estrutura que o formato pede: capa provocativa (dor + curiosidade) → storytelling 1ª pessoa → dado que educa → comparativo → 3 passos práticos → punch → CTA de comentário pra DM.
