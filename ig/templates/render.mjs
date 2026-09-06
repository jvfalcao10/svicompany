#!/usr/bin/env node
// Renderiza um carrossel (content.json) em JPGs 1080x1350 prontos pro Instagram.
// Uso: node render.mjs <content.json> <pasta-de-saida>
import { createRequire } from 'node:module';
import { readFileSync, mkdirSync } from 'node:fs';

// usa o playwright local se existir; senão, o instalado globalmente
const { chromium } = await import('playwright').catch(() => {
  const req = createRequire(process.execPath);
  return req(req.resolve('playwright', { paths: [join(dirname(process.execPath), '..', 'lib', 'node_modules')] }));
});
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const [,, contentPath, outDir] = process.argv;
if (!contentPath || !outDir) {
  console.error('Uso: node render.mjs <content.json> <pasta-de-saida>');
  process.exit(1);
}

const content = JSON.parse(readFileSync(resolve(contentPath), 'utf8'));
const templatePath = join(dirname(fileURLToPath(import.meta.url)), 'carrossel-medicos.html');
mkdirSync(resolve(outDir), { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
await page.addInitScript(data => { window.CAROUSEL = data; }, content);
await page.goto(pathToFileURL(templatePath).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(300);

const slides = page.locator('.slide');
const n = await slides.count();
for (let i = 0; i < n; i++) {
  const file = join(resolve(outDir), `slide-${String(i + 1).padStart(2, '0')}.jpg`);
  await slides.nth(i).screenshot({ path: file, type: 'jpeg', quality: 92 });
  console.log('ok', file);
}
await browser.close();
console.log(`${n} slides renderizados em ${resolve(outDir)}`);
