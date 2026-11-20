#!/usr/bin/env python3
"""Rewrite root-absolute paths to the /drsamaragi project base for GitHub Pages.

The repository source keeps root-absolute paths (correct for Cloudflare Pages,
which serves at the domain root). GitHub Pages serves this project repo under
/drsamaragi/, so this build step prefixes asset and internal-page paths with
that base. It runs ONLY in CI against the copied _site/ folder and never
touches the committed source.
"""
import pathlib

BASE = "/drsamaragi"
site = pathlib.Path("_site")

# Order matters only in that none of these overlap destructively; source never
# already contains "/drsamaragi/", so each replacement is idempotent per run.
replacements = [
    ("/wp-content", BASE + "/wp-content"),   # assets + uploads; no trailing slash so escaped \/wp-content\/ also matches
    ("/wp-includes", BASE + "/wp-includes"),  # core scripts/styles (plain and escaped forms)
    ('href="/"', 'href="' + BASE + '/"'),       # homepage / logo links
    ('href="/serv/"', 'href="' + BASE + '/serv/"'),
    ('href="/contact/"', 'href="' + BASE + '/contact/"'),
    ('href="/glossary/"', 'href="' + BASE + '/glossary/"'),
    ('href="/privacy-policy/"', 'href="' + BASE + '/privacy-policy/"'),
]

count = 0
for f in site.rglob("*.html"):
    s = f.read_text(encoding="utf-8")
    for a, b in replacements:
        s = s.replace(a, b)
    f.write_text(s, encoding="utf-8", newline="")
    count += 1

print(f"Rewrote {count} HTML files for base {BASE}")
