// Word editável de download da página /formula-atendimento (mesmo conteúdo do PDF).
// Conteúdo: _gerador/formula_atendimento.json. Uso: NODE_PATH=$(npm root -g) node _gerador/formula_atendimento_docx.js
const fs = require('fs'), path = require('path'), os = require('os');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Footer, AlignmentType,
        ExternalHyperlink, HeadingLevel, BorderStyle, WidthType, ShadingType } = require('docx');

const AQUI = __dirname, SITE = path.dirname(AQUI);
const D = JSON.parse(fs.readFileSync(path.join(AQUI, 'formula_atendimento.json'), 'utf8'));
const [f1, f2, f3, f4] = D.secoes;
const SAIDA = path.join(SITE, 'downloads', 'formula-da-primeira-resposta-svi.docx');
const OURO = 'A07F2E', OURO_CLARO = 'C9A44C', TINTA = '15110A';
const LARG = 9638;  // A4 com margens de 2 cm
const semBorda = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const bordaBranca = { style: BorderStyle.SINGLE, size: 6, color: 'FFFFFF' };
const tabBordas = (b) => ({ top: b, bottom: b, left: b, right: b, insideHorizontal: b, insideVertical: b });

const p = (runs, opt = {}) => new Paragraph({ spacing: { after: 120, line: 300 }, ...opt, children: runs });
const r = (text, opt = {}) => new TextRun({ text, font: 'Arial', ...opt });
const titulo = (s) => new Paragraph({
  heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: OURO_CLARO, space: 4 } },
  children: s.h2_em ? [r(s.h2.slice(0, s.h2.lastIndexOf(s.h2_em))), r(s.h2_em, { color: OURO })] : [r(s.h2)],
});
const sub = (n, t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 200, after: 80 },
  children: [r(String(n).padStart(2, '0') + '  ', { color: OURO }), r(t)] });
const paras = (ps) => ps.map(([b, resto]) => p(b ? [r(b + ' ', { bold: true }), r(resto)] : [r(resto)]));
const caixa = (fill, filhos, borda) => new Table({
  width: { size: LARG, type: WidthType.DXA }, columnWidths: [LARG], borders: tabBordas(semBorda),
  rows: [new TableRow({ children: [new TableCell({
    width: { size: LARG, type: WidthType.DXA }, shading: { fill, type: ShadingType.CLEAR },
    margins: { top: 160, bottom: 120, left: 220, right: 220 },
    borders: { top: semBorda, bottom: semBorda, right: semBorda, left: borda || semBorda },
    children: filhos })] })],
});
const espaco = () => new Paragraph({ spacing: { after: 120 }, children: [] });
const rotulo = (t, cor) => p([r(t.toUpperCase(), { bold: true, size: 17, color: cor, characterSpacing: 40 })], { spacing: { after: 80 } });

const logo = fs.readFileSync(path.join(os.homedir(), 'Dev/felipe-roteiros/gravacao/logo-svi-preto.png'));
const filhos = [
  new Paragraph({ spacing: { after: 360 }, children: [new ImageRun({ type: 'png', data: logo, transformation: { width: 110, height: 75 },
    altText: { title: 'SVI Company', description: 'Logo da SVI Company', name: 'logo' } })] }),
  rotulo(D.kicker, OURO),
  new Paragraph({ spacing: { after: 200 }, children: [r('A fórmula da ', { bold: true, size: 52 }), r('primeira resposta', { bold: true, size: 52, color: OURO })] }),
  caixa('FAF5E9', [p([r(D.intro)], { spacing: { after: 40, line: 300 } })], { style: BorderStyle.SINGLE, size: 24, color: OURO_CLARO }),

  titulo(f1),
  p([r(f1.ps[0])]),
  p([r('O que a pessoa pediu', { bold: true }), r('  +  ', { bold: true, color: OURO }), r('O valor', { bold: true }),
     r('  +  ', { bold: true, color: OURO }), r('Duas opções de dia e hora', { bold: true })], { spacing: { before: 120, after: 200 } }),
  ...f1.movs.flatMap((m, i) => [sub(i + 1, m.t), ...paras(m.ps)]),
  espaco(),
  new Table({
    width: { size: LARG, type: WidthType.DXA }, columnWidths: [LARG / 2, LARG / 2], borders: tabBordas(bordaBranca),
    rows: [new TableRow({ children: [
      ['Assim não', f1.nao, 'F6ECE8', '9A4A37'], ['Assim sim', f1.sim, 'F0E7D2', '6B5520'],
    ].map(([t, itens, fill, cor]) => new TableCell({
      width: { size: LARG / 2, type: WidthType.DXA }, shading: { fill, type: ShadingType.CLEAR },
      margins: { top: 140, bottom: 120, left: 200, right: 200 },
      borders: { top: { style: BorderStyle.SINGLE, size: 6, color: 'FFFFFF' }, bottom: { style: BorderStyle.SINGLE, size: 6, color: 'FFFFFF' },
                 left: { style: BorderStyle.SINGLE, size: 6, color: 'FFFFFF' }, right: { style: BorderStyle.SINGLE, size: 6, color: 'FFFFFF' } },
      children: [rotulo(t, cor), ...itens.map((x) => p([r(x)], { spacing: { after: 60 } }))],
    })) })],
  }),

  new Paragraph({ pageBreakBefore: true, children: [] }),
  titulo(f2),
  ...f2.movs.flatMap((m, i) => [sub(i + 1, m.t), ...paras(m.ps)]),

  new Paragraph({ pageBreakBefore: true, children: [] }),
  titulo(f3),
  p([r(f3.ps[0])]),
  ...f3.modelos.flatMap((m) => [espaco(), caixa('F7F1E3', [rotulo(m.tag, OURO),
    ...m.msg.split('\n\n').map((t) => p([r(t, { size: 24 })], { spacing: { after: 120, line: 320 } }))])]),
  p([r(f3.nota, { italics: true, color: '5D5444' })], { spacing: { before: 200, after: 240 } }),
  caixa('0A0808', [
    p([r(f4.cta.h, { bold: true, size: 28, color: OURO_CLARO })]),
    p([r(f4.cta.p, { color: 'EFE7D4' })]),
    p([new ExternalHyperlink({ link: f4.cta.href, children: [r(f4.cta.btn + ': ' + f4.cta.href.replace(/\/$/, ''), { bold: true, color: OURO_CLARO, underline: {} })] })]),
  ]),
];

const doc = new Document({
  creator: 'SVI Company', title: 'A fórmula da primeira resposta', description: 'SVI Company · svicompany.com.br/formula-atendimento',
  styles: {
    default: { document: { run: { font: 'Arial', size: 22, color: TINTA } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 32, bold: true, font: 'Arial', color: TINTA }, paragraph: { outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 25, bold: true, font: 'Arial', color: TINTA }, paragraph: { outlineLevel: 1, keepNext: true } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [r('SVI Company · svicompany.com.br/formula-atendimento', { size: 16, color: '8A8070' })] })] }) },
    children: filhos,
  }],
});
fs.mkdirSync(path.dirname(SAIDA), { recursive: true });
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(SAIDA, b); console.log('DOCX:', SAIDA, b.length, 'bytes'); });
