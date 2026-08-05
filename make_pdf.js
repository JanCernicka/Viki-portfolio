/**
 * Vyrobí PDF-ká z tlačových strán.
 *
 *     node make_pdf.js
 *
 * Predtým treba spustiť `python3 build_docs.py`, aby boli HTML strany aktuálne.
 * Renderuje sa cez lokálny server — z file:// by sa nenačítali fonty ani obrázky.
 */
const path = require('path');
const fs = require('fs');
const http = require('http');
const { spawnSync } = require('child_process');
const { chromium } = require(process.env.PW_PATH ||
  '/opt/node22/lib/node_modules/playwright');

const ROOT = __dirname;
const PORT = 8123;

const DOCS = [
  { html: 'cv.html',                out: 'assets/cv/Viktoria-Mikuskova-CV.pdf' },
  { html: 'cv-en.html',             out: 'assets/cv/Viktoria-Mikuskova-CV-EN.pdf' },
  { html: 'portfolio-dokument.html', out: 'assets/dokumenty/Viktoria-Mikuskova-portfolio.pdf' },
];

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2',
  '.pdf': 'application/pdf',
};

function serve() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      const file = path.join(ROOT, rel || 'index.html');
      if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        res.writeHead(404).end('not found');
        return;
      }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
      fs.createReadStream(file).pipe(res);
    });
    server.listen(PORT, () => resolve(server));
  });
}

(async () => {
  const server = await serve();
  const browser = await chromium.launch();
  const page = await browser.newPage();

  for (const doc of DOCS) {
    if (!fs.existsSync(path.join(ROOT, doc.html))) {
      console.log(`  ! ${doc.html} neexistuje — preskočené`);
      continue;
    }
    const out = path.join(ROOT, doc.out);
    fs.mkdirSync(path.dirname(out), { recursive: true });

    await page.goto(`http://127.0.0.1:${PORT}/${doc.html}`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: out, format: 'A4', printBackground: true });

    const kb = Math.round(fs.statSync(out).size / 1024);
    console.log(`  ${doc.out} — ${kb} kB`);
  }

  await browser.close();
  server.close();

  // Chromium vkladá obrázky v pôvodnej veľkosti, takže portfólio vyjde cez
  // 11 MB a ako e-mailová príloha je nepoužiteľné. Prevzorkovanie na 200 dpi
  // ho zmenší na polovicu bez viditeľného rozdielu.
  const big = DOCS.map((d) => d.out).filter(
    (o) => fs.existsSync(path.join(ROOT, o)) &&
           fs.statSync(path.join(ROOT, o)).size > 2 * 1024 * 1024);
  if (big.length) {
    const r = spawnSync('python3', [path.join(ROOT, 'optimize_pdf.py'), ...big],
      { cwd: ROOT, encoding: 'utf8' });
    process.stdout.write(r.stdout || '');
    if (r.status !== 0) console.log('  ! optimize_pdf.py zlyhalo — PDF ostáva veľké');
  }

  console.log('Hotovo.');
})();
