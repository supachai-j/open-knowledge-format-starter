// Render an mdBook print page to PDF with puppeteer-core (the --print-to-pdf CLI
// can't add header/footer; only the DevTools protocol can).
//
// displayHeaderFooter forces the header/footer onto EVERY page, including the
// full-bleed cover. So we render in two modes and the workflow stitches them:
//   mode=cover : page 1 only, NO header/footer  -> the clean full-bleed cover
//   mode=body  : all pages, WITH running header + "page / total" footer
// The workflow keeps cover page 1 + body pages 2..N.
//
// Usage: node tools/print-pdf.js <input.html> <output.pdf> <headerTitle> <cover|body>
const puppeteer = require('puppeteer-core');
const fs = require('fs');

const [, , input, output, headerTitle, mode = 'body'] = process.argv;
if (!input || !output) {
  console.error('usage: print-pdf.js <input.html> <output.pdf> <headerTitle> <cover|body>');
  process.exit(2);
}

function findChrome() {
  const cands = [process.env.CHROME_PATH, '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium-browser', '/usr/bin/chromium', '/snap/bin/chromium'].filter(Boolean);
  for (const c of cands) { try { if (fs.existsSync(c)) return c; } catch (e) {} }
  throw new Error('No Chrome/Chromium found (set CHROME_PATH)');
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: findChrome(),
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'],
  });
  try {
    const page = await browser.newPage();
    await page.goto('file://' + input, { waitUntil: 'networkidle0', timeout: 120000 });
    try { await page.evaluate(() => document.fonts && document.fonts.ready); } catch (e) {}

    const opts = { path: output, printBackground: true, preferCSSPageSize: true };
    if (mode === 'cover') {
      opts.pageRanges = '1';
      opts.displayHeaderFooter = false;
    } else {
      const s = "font-family:'Noto Sans Thai','Loma','TLwg Typo',sans-serif;font-size:8px;color:#9aa3af;width:100%;padding:0 15mm;text-align:center;";
      opts.displayHeaderFooter = true;
      opts.headerTemplate = `<div style="${s}">${headerTitle || ''}</div>`;
      opts.footerTemplate = `<div style="${s}"><span class="pageNumber"></span> / <span class="totalPages"></span></div>`;
    }
    await page.pdf(opts);
    console.log('wrote', output, '(' + mode + ')');
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error('PDF generation failed:', e.message); process.exit(1); });
