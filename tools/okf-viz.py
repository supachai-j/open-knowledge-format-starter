#!/usr/bin/env python3
"""okf-viz.py — render an OKF bundle as a self-contained interactive HTML graph.

Inspired by the visualizer in GoogleCloudPlatform/knowledge-catalog. Zero
dependencies (stdlib only). Walks the bundle, embeds it as a JSON blob, and
renders a force-directed concept graph using Cytoscape.js + marked (from CDN).
No data leaves the page; everything is serialized at generation time.

Usage:
  python3 tools/okf-viz.py [bundle_dir] [-o out.html] [--name "Display Name"]

Defaults: bundle_dir=../wiki, out=<bundle>/viz.html
"""
import argparse
import html
import json
import os
import re

RESERVED = {"index.md", "log.md"}
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
LINK_RE = re.compile(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)")


def parse_frontmatter(text):
    """Return (meta_dict, body). YAML-lite — handles scalars and simple lists."""
    meta, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end]
            body = text[end + 4:].lstrip("\n")
            key = None
            for line in block.splitlines():
                if re.match(r"\s*-\s+", line) and key:           # list item
                    meta.setdefault(key, [])
                    if isinstance(meta[key], list):
                        meta[key].append(line.split("-", 1)[1].strip().strip("'\""))
                    continue
                m = re.match(r"([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
                if m:
                    key, val = m.group(1), m.group(2).strip()
                    if val == "":
                        meta[key] = []                            # block list follows
                    elif val.startswith("[") and val.endswith("]"):
                        meta[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
                    else:
                        meta[key] = val.strip().strip("'\"")
    return meta, body


def resolve(concept_dir, target, ids):
    """Resolve a link target to a concept id within the bundle, or None."""
    t = target.split("#")[0]
    if not t or t.startswith(("http://", "https://", "mailto:")):
        return None
    if not t.endswith(".md"):
        return None
    if t.startswith("/"):                       # bundle-root-absolute
        rid = t[1:]
    else:                                       # file-relative
        rid = os.path.normpath(os.path.join(concept_dir, t))
    rid = rid[:-3] if rid.endswith(".md") else rid
    rid = rid.replace(os.sep, "/").lstrip("./")
    return rid


def collect(bundle):
    paths, ids = [], set()
    for root, _, files in os.walk(bundle):
        for fn in files:
            if fn.endswith(".md") and fn not in RESERVED:
                rel = os.path.relpath(os.path.join(root, fn), bundle).replace(os.sep, "/")
                paths.append(rel)
                ids.add(rel[:-3])
    concepts = []
    for rel in sorted(paths):
        cid = rel[:-3]
        cdir = os.path.dirname(rel)
        with open(os.path.join(bundle, rel), encoding="utf-8") as fh:
            meta, body = parse_frontmatter(fh.read())
        # extract + rewrite internal links so the viewer can intercept them
        links, broken = [], []

        def repl(m, _cdir=cdir):
            label, tgt = m.group(1), m.group(2)
            rid = resolve(_cdir, tgt, ids)
            if rid is None:
                return m.group(0)
            if rid in ids:
                links.append(rid)
                return f"[{label}](okf:{rid})"
            broken.append(rid)
            return f"[{label}](okf-missing:{rid})"

        # only rewrite outside fenced code blocks
        parts, last, out = [], 0, []
        for fm in FENCE_RE.finditer(body):
            out.append(LINK_RE.sub(repl, body[last:fm.start()]))
            out.append(fm.group(0))
            last = fm.end()
        out.append(LINK_RE.sub(repl, body[last:]))
        body = "".join(out)

        tags = meta.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        concepts.append({
            "id": cid,
            "type": meta.get("type", "Concept"),
            "title": meta.get("title", cid.split("/")[-1]),
            "description": meta.get("description", ""),
            "resource": meta.get("resource", ""),
            "tags": tags,
            "timestamp": meta.get("timestamp", ""),
            "body": body,
            "links": sorted(set(links)),
            "broken": sorted(set(broken)),
        })
    return concepts


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__NAME__ — OKF Viewer</title>
<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.30.2/dist/cytoscape.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<style>
:root{--bg:#0f1115;--panel:#181b22;--ink:#e6e8ec;--mut:#9aa3af;--line:#2a2f3a;--acc:#4f86c6}
*{box-sizing:border-box}body{margin:0;font:14px/1.55 system-ui,sans-serif;background:var(--bg);color:var(--ink);height:100vh;display:flex;flex-direction:column}
header{padding:10px 16px;border-bottom:1px solid var(--line);display:flex;gap:12px;align-items:center;flex-wrap:wrap}
header h1{font-size:15px;margin:0;font-weight:600}header .sp{flex:1}
input,select{background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:6px 9px;font-size:13px}
#main{flex:1;display:flex;min-height:0}#cy{flex:1;min-width:0}
#side{width:380px;border-left:1px solid var(--line);overflow:auto;padding:16px;background:var(--panel)}
#side h2{font-size:16px;margin:0 0 2px}#side .type{display:inline-block;font-size:11px;color:#fff;border-radius:4px;padding:1px 7px;margin-bottom:8px}
#side .desc{color:var(--mut);margin:0 0 10px}#side .meta{font-size:12px;color:var(--mut);margin-bottom:10px}
#side .tag{display:inline-block;background:#222834;border:1px solid var(--line);border-radius:10px;padding:0 8px;margin:0 4px 4px 0;font-size:11px}
#body{border-top:1px solid var(--line);margin-top:10px;padding-top:10px}
#body table{border-collapse:collapse;width:100%}#body th,#body td{border:1px solid var(--line);padding:4px 7px;text-align:left;font-size:12px}
#body pre{background:#0c0e12;padding:10px;border-radius:6px;overflow:auto}#body code{font-family:ui-monospace,monospace}
#body a{color:var(--acc);cursor:pointer}#body a.broken{color:#c0504d;text-decoration:line-through}
.back a{display:block;color:var(--acc);cursor:pointer;font-size:12px;margin:2px 0}
.legend{font-size:11px;color:var(--mut);display:flex;gap:10px;flex-wrap:wrap}.legend span{display:flex;align-items:center;gap:4px}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block}.empty{color:var(--mut);padding:24px}
</style></head><body>
<header>
  <h1>__NAME__</h1>
  <span id="legend" class="legend"></span><span class="sp"></span>
  <input id="search" placeholder="Search title / id / tag…">
  <select id="typeFilter"><option value="">All types</option></select>
  <select id="layout"><option value="cose">cose</option><option value="concentric">concentric</option><option value="breadthfirst">breadthfirst</option><option value="circle">circle</option><option value="grid">grid</option></select>
</header>
<div id="main"><div id="cy"></div>
  <div id="side"><div class="empty">Click a concept node to inspect it.</div></div></div>
<script>
const DATA = __BUNDLE_JSON__;
const byId={}; DATA.concepts.forEach(c=>byId[c.id]=c);
const types=[...new Set(DATA.concepts.map(c=>c.type))].sort();
const palette=['#4f86c6','#6cc24a','#e8a33d','#c0504d','#8064a2','#4bacc6','#f06292','#90a4ae','#a3be8c','#d08770'];
const typeColor={}; types.forEach((t,i)=>typeColor[t]=palette[i%palette.length]);
const nodes=DATA.concepts.map(c=>({data:{id:c.id,label:c.title||c.id,type:c.type}}));
const edges=[]; DATA.concepts.forEach(c=>(c.links||[]).forEach(t=>{if(byId[t])edges.push({data:{id:c.id+' -> '+t,source:c.id,target:t}});}));
const backlinks={}; edges.forEach(e=>{(backlinks[e.data.target]=backlinks[e.data.target]||[]).push(e.data.source);});
const cy=cytoscape({container:document.getElementById('cy'),elements:[...nodes,...edges],
  style:[
    {selector:'node',style:{'background-color':e=>typeColor[e.data('type')]||'#90a4ae','label':'data(label)','color':'#cfd4dc','font-size':9,'text-wrap':'wrap','text-max-width':110,'text-valign':'bottom','text-margin-y':3,'width':18,'height':18}},
    {selector:'edge',style:{'width':1,'line-color':'#3a4250','target-arrow-color':'#3a4250','target-arrow-shape':'triangle','curve-style':'bezier','arrow-scale':0.8}},
    {selector:'node:selected',style:{'border-width':3,'border-color':'#fff'}},
    {selector:'.dim',style:{'opacity':0.12}}
  ],layout:{name:'cose',animate:false,padding:40}});
const legend=document.getElementById('legend'); types.forEach(t=>{const s=document.createElement('span');s.innerHTML=`<span class="dot" style="background:${typeColor[t]}"></span>${t}`;legend.appendChild(s);});
const tf=document.getElementById('typeFilter'); types.forEach(t=>{const o=document.createElement('option');o.value=t;o.textContent=t;tf.appendChild(o);});
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function show(id){const c=byId[id];if(!c)return;const side=document.getElementById('side');
  let h=`<h2>${esc(c.title)}</h2><span class="type" style="background:${typeColor[c.type]||'#90a4ae'}">${esc(c.type)}</span>`;
  h+=`<div class="meta"><code>${esc(c.id)}</code></div>`;
  if(c.description)h+=`<p class="desc">${esc(c.description)}</p>`;
  if(c.resource)h+=`<div class="meta">🔗 <a href="${esc(c.resource)}" target="_blank" rel="noopener">${esc(c.resource)}</a></div>`;
  if(c.tags&&c.tags.length)h+=`<div>${c.tags.map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div>`;
  const bl=backlinks[c.id]||[]; if(bl.length)h+=`<div class="meta back" style="margin-top:10px"><b>Cited by</b>${bl.map(b=>`<a data-go="${esc(b)}">${esc((byId[b]||{}).title||b)}</a>`).join('')}</div>`;
  h+=`<div id="body">${marked.parse(c.body||'')}</div>`;
  side.innerHTML=h;
  side.querySelectorAll('a[href^="okf:"]').forEach(a=>{const id=a.getAttribute('href').slice(4);a.removeAttribute('href');a.onclick=()=>select(id);});
  side.querySelectorAll('a[href^="okf-missing:"]').forEach(a=>{a.classList.add('broken');a.removeAttribute('href');a.title='not-yet-written concept';});
  side.querySelectorAll('a[data-go]').forEach(a=>{a.onclick=()=>select(a.getAttribute('data-go'));});
}
function select(id){const n=cy.getElementById(id);if(n.empty())return;cy.elements().unselect();n.select();cy.animate({center:{eles:n},zoom:1.2},{duration:250});show(id);}
cy.on('tap','node',e=>select(e.target.id()));
document.getElementById('search').addEventListener('input',e=>{const q=e.target.value.toLowerCase();cy.nodes().forEach(n=>{const c=byId[n.id()];const hit=!q||(c.title+ ' '+c.id+' '+(c.tags||[]).join(' ')).toLowerCase().includes(q);n.toggleClass('dim',!hit);});});
document.getElementById('typeFilter').addEventListener('change',e=>{const t=e.target.value;cy.nodes().forEach(n=>n.toggleClass('dim',t&&byId[n.id()].type!==t));});
document.getElementById('layout').addEventListener('change',e=>cy.layout({name:e.target.value,animate:false,padding:40}).run());
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("bundle", nargs="?", default=os.path.join(here, "..", "wiki"))
    ap.add_argument("-o", "--out")
    ap.add_argument("--name")
    a = ap.parse_args()
    bundle = os.path.abspath(a.bundle)
    if not os.path.isdir(bundle):
        print(f"✗ bundle dir not found: {bundle}")
        return 1
    name = a.name or os.path.basename(bundle.rstrip("/"))
    out = a.out or os.path.join(bundle, "viz.html")
    concepts = collect(bundle)
    blob = json.dumps({"name": name, "concepts": concepts}, ensure_ascii=False)
    page = (TEMPLATE
            .replace("__BUNDLE_JSON__", blob)
            .replace("__NAME__", html.escape(name)))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    edges = sum(len(c["links"]) for c in concepts)
    print(f"✓ wrote {out}\n  {len(concepts)} concepts, {edges} links, {len(set(t['type'] for t in concepts))} types")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
