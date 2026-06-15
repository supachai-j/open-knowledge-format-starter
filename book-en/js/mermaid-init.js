// Render Mermaid diagrams written as <pre class="mermaid">…</pre> (no preprocessor needed).
// Sets window.__okfMermaidDone so the PDF renderer can wait for diagrams to finish.
(function () {
  window.__okfMermaidDone = false;
  async function run() {
    if (!window.mermaid) { window.__okfMermaidDone = true; return; }
    try {
      window.mermaid.initialize({
        startOnLoad: false,
        theme: 'neutral',
        securityLevel: 'loose',
        fontFamily: "'Noto Sans Thai','Loma',sans-serif",
        flowchart: { htmlLabels: true, curve: 'basis', useMaxWidth: true },
        themeVariables: { primaryColor: '#ede9fe', primaryBorderColor: '#8b5cf6', lineColor: '#8b5cf6' },
      });
      await window.mermaid.run({ querySelector: 'pre.mermaid' });
    } catch (e) { console.error('mermaid', e); }
    window.__okfMermaidDone = true;
  }
  if (document.readyState !== 'loading') run();
  else document.addEventListener('DOMContentLoaded', run);
})();
