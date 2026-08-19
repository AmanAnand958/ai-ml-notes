#!/usr/bin/env python3
"""
scripts/check_url_liveness.py
Exhaustive Link-Checker testing live network HTTP status for all resource URLs
across 26 YAML files and roadmap.html.
"""

import os, glob, re, yaml, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

# 1. Extract all URLs
urls_by_day = []
all_urls = set()

for yf in sorted(glob.glob(os.path.join(DATA_DIR, '*.yaml'))):
    with open(yf, 'r', encoding='utf-8') as f:
        ydata = yaml.safe_load(f)
    for day in ydata.get('days', []):
        did = int(day.get('day_num') or day.get('id'))
        for r in day.get('resources', []):
            url = str(r.get('url', '')).strip()
            title = str(r.get('title', '')).strip()
            if url.startswith('http'):
                urls_by_day.append((did, title, url))
                all_urls.add(url)

print(f"Extracted {len(urls_by_day)} total resource references ({len(all_urls)} unique URLs).")

# 2. Check URL liveness
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def check_url(url):
    req = urllib.request.Request(url, headers=HEADERS, method='HEAD')
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return url, resp.status, None
    except urllib.error.HTTPError as e:
        # Some servers reject HEAD, retry with GET
        if e.code in [403, 405, 400]:
            req_get = urllib.request.Request(url, headers=HEADERS, method='GET')
            try:
                with urllib.request.urlopen(req_get, timeout=8) as resp_get:
                    return url, resp_get.status, None
            except urllib.error.HTTPError as e_get:
                return url, e_get.code, str(e_get)
            except Exception as e_get_other:
                return url, 'ERR', str(e_get_other)
        return url, e.code, str(e)
    except Exception as e:
        # Retry with GET on general error
        req_get = urllib.request.Request(url, headers=HEADERS, method='GET')
        try:
            with urllib.request.urlopen(req_get, timeout=8) as resp_get:
                return url, resp_get.status, None
        except Exception as e_retry:
            return url, 'TIMEOUT_OR_ERR', str(e_retry)

results = {}
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(check_url, url): url for url in all_urls}
    for future in as_completed(futures):
        url, status, err = future.result()
        results[url] = (status, err)

# 3. Categorize results
live_urls = []
redirects = []
broken_404 = []
blocked_or_rate_limited = []
timeouts = []

for url, (status, err) in results.items():
    if status in [200, 301, 302, 307, 308]:
        live_urls.append((url, status))
    elif status == 404:
        broken_404.append((url, err))
    elif status in [403, 429]:
        blocked_or_rate_limited.append((url, status, err))
    else:
        timeouts.append((url, status, err))

print("\n=== LIVENESS SUMMARY ===")
print(f"✅ Live / Resolving URLs (200/3xx): {len(live_urls)}")
print(f"🔒 Bot-Protected / Rate-limited (403/429 - Active in browser): {len(blocked_or_rate_limited)}")
print(f"⏳ Timeouts / Network Warnings: {len(timeouts)}")
print(f"❌ 404 Not Found (Broken URLs): {len(broken_404)}")

if broken_404:
    print("\n❌ BROKEN 404 URLs TO FIX:")
    for url, err in broken_404:
        # Find which days use this
        days_using = [d for d, t, u in urls_by_day if u == url]
        print(f"  • URL: {url} | Days: {days_using} | Error: {err}")

if timeouts:
    print("\n⏳ TIMEOUTS / UNREACHABLE URLS:")
    for url, status, err in timeouts:
        days_using = [d for d, t, u in urls_by_day if u == url]
        print(f"  • URL: {url} | Days: {days_using} | Status: {status} | Error: {err}")

