#!/usr/bin/env python3
"""Regenerate sitemap.xml from posts.json for this site. Run from repo root: python3 scripts/regen_sitemap.py"""
import json
import subprocess
import os

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL_FILE = os.path.join(REPO_DIR, ".site_url")


def git_last_date(relpath):
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", relpath],
            cwd=REPO_DIR, stderr=subprocess.DEVNULL
        ).decode().strip()
        return out or None
    except subprocess.CalledProcessError:
        return None


def main():
    with open(os.path.join(REPO_DIR, "posts.json"), encoding="utf-8") as f:
        posts = json.load(f)

    repo_name = os.path.basename(REPO_DIR)
    base_url = f"https://laykim829.github.io/{repo_name}/"

    dates = [p["date"] for p in posts if p.get("date")]
    latest_post_date = max(dates) if dates else None
    about_date = git_last_date("about.html") or latest_post_date
    privacy_date = git_last_date("privacy.html") or latest_post_date

    entries = [
        (base_url, "daily", "1.0", latest_post_date),
        (base_url + "about.html", "monthly", "0.5", about_date),
        (base_url + "privacy.html", "monthly", "0.3", privacy_date),
    ]
    for p in sorted(posts, key=lambda p: p.get("date", ""), reverse=True):
        entries.append((base_url + p["url"], "monthly", "0.8", p.get("date")))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, changefreq, priority, lastmod in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        if lastmod:
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")

    with open(os.path.join(REPO_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"{repo_name}: {len(posts)} posts -> sitemap.xml with {len(entries)} urls")


if __name__ == "__main__":
    main()
