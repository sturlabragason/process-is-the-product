#!/usr/bin/env python3
"""Build index.html: inline the brand (tokens, fonts, logos, motif) and the prose in prose/*.md, so the page works from any location."""
import base64, html, json, pathlib, re, sys
here = pathlib.Path(__file__).resolve().parent
brand = here.parents[2] / "claude-for-small-business/business/brand"
sys.path.insert(0, str(brand))
from build_motif import untangle  # the brand's own generator; the motif is never drawn by hand

def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()

def motif(**kw):
    """Brand motif with pathLength=1 on each line and a draw order (--k), for the line-drawing motion."""
    svg = untangle(**kw)
    k = iter(range(100))
    return re.sub(r"<path ", lambda _: f'<path pathLength="1" style="--k:{next(k)}" ', svg)

src = (here / "post.src.html").read_text()
css = re.sub(r'url\("fonts/([^"]+)"\)', lambda m: f'url("{b64(brand / "fonts" / m[1], "font/woff2")}")',
             (brand / "tokens.css").read_text())
presets = {  # same presets as build_motif.py's library: slide-title, slide-band, close-band
    "MOTIF_TITLE": dict(seed=11, w=1920, h=520, lines=11, split=0.44, accent=5),
    "MOTIF_HERO": dict(seed=11, w=1920, h=330, lines=11, accent=5),
    "MOTIF_CLOSE": dict(seed=23, w=1440, h=220, lines=7, split=0.36, accent=3, ends=False),
}
out = src.replace('<link rel="stylesheet" href="../../../claude-for-small-business/business/brand/tokens.css">',
                  f"<style>\n{css}\n</style>")
for name in ("icon.svg", "lockup.svg"):
    out = out.replace(f"'../../../claude-for-small-business/business/brand/logo/{name}'",
                      f"'{b64(brand / 'logo' / name, 'image/svg+xml')}'")
for key, kw in presets.items():
    out = out.replace(f"'%%{key}%%'", json.dumps(motif(**kw)))
assert "claude-for-small-business" not in out and "%%MOTIF" not in out and 'url("fonts/' not in out, "unresolved brand asset"
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"<em>\1</em>", t)

prose = {}
for f in sorted((here / "prose").glob("*.md")):
    for block in re.split(r"^## ", f.read_text(), flags=re.M)[1:]:
        sid, _, body = block.partition("\n")
        paras = [p.strip().replace("\n", " ") for p in re.split(r"\n\s*\n", body) if p.strip()]
        prose[sid.strip()] = "".join(f"<p>{inline(p)}</p>" for p in paras)
GH = "https://github.com/sturlabragason/process-is-the-product/blob/main/"
prose = {k: v.replace('href="../../', 'href="' + GH) for k, v in prose.items()}
out = out.replace("'%%PROSE%%'", json.dumps(prose))
ids = re.findall(r"\{id:'([a-z0-9]+)'", src)
missing = [i for i in ids if i not in prose]
assert "%%" not in out, "unresolved placeholder"
(here / "index.html").write_text(out)
print("wrote", here / "index.html", f"{len(out)//1024} KB", f"prose {len(ids)-len(missing)}/{len(ids)}", "missing: " + " ".join(missing) if missing else "")
