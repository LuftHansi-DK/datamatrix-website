#!/usr/bin/env python3
"""Copy dist/ to a folder that works by double-clicking index.html (file://).
Rewrites root-absolute links to relative ones and points folder links at index.html.
Demo only — production uses dist/ as-is."""
import os, re, shutil, sys
src, dst = "dist", sys.argv[1]
if os.path.exists(dst): shutil.rmtree(dst)
shutil.copytree(src, dst)
def rel(path_from_root, depth, html):
    p = path_from_root.split("#")[0].split("?")[0]
    frag = path_from_root[len(p):]
    if html and (p.endswith("/") or p == ""): p += "index.html"
    return ("../" * depth or "./") + p.lstrip("/") + frag
for root, _, files in os.walk(dst):
    for f in files:
        full = os.path.join(root, f)
        depth = os.path.relpath(full, dst).count(os.sep)
        if f.endswith(".html"):
            s = open(full, encoding="utf-8").read()
            s = re.sub(r'((?:href|src)=")(/(?!/)[^"]*)"', lambda m: m.group(1) + rel(m.group(2), depth, not re.search(r'\.\w{2,5}($|[?#])', m.group(2).split("#")[0])) + '"', s)
            open(full, "w", encoding="utf-8").write(s)
        elif f.endswith(".css"):
            s = open(full, encoding="utf-8").read()
            s = re.sub(r'url\((["\']?)/(?!/)', lambda m: "url(" + m.group(1) + ("../" * depth or "./"), s)
            open(full, "w", encoding="utf-8").write(s)
print("offline demo:", dst)
