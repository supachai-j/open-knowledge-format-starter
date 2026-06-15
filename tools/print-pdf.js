// Render an mdBook print page to a PDF with a running header + "page / total" footer.
// Uses puppeteer-core driving the system Chrome (the --print-to-pdf CLI can't add
// header/footer; only the DevTools protocol can). The cover page is full-bleed via
// CSS @page :first { margin: 0 }, which leaves no room for header/footer there — so
// the header/footer appear only on the content pages, exactly as we want.
//
// Usage: node tools/print-pdf.js <input.html> <output.pdf> [headerTitle]
const puppeteer = require('puppeteer-core');
const fs = require('fs');

const [, , input, output, headerTitle] = process.argv;
if (!input || !output) {
  console.error('usage: print-pdf.js <input.html> <output.pdf> [headerTitle]');
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
    const s = "font-family:'Noto Sans Thai','Loma','TLwg Typo',sans-serif;font-size:8px;color:#9aa3af;width:100%;padding:0 15mm;text-align:center;";
    await page.pdf({
      path: output,
      printBackground: true,
      preferCSSPageSize: true,          // honor CSS @page size + per-page margins (incl. :first)
      displayHeaderFooter: true,
      headerTemplate: `<div style="${s}">${headerTitle || ''}</div>`,
      footerTemplate: `<div style="${s}"><span class="pageNumber"></span> / <span class="totalPages"></span></div>`,
    });
    console.log('wrote', output);
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error('PDF generation failed:', e.message); process.exit(1); });
