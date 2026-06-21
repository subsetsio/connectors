import io, os, re, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get, configure_http

configure_http(headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Referer": "https://www.ifo.de/en/ifo-time-series",
    "Accept-Language": "en-US,en;q=0.9",
})

INDEX = "https://www.ifo.de/en/ifo-time-series"

def fetch(url):
    r = get(url, timeout=(10.0, 120.0))
    ct = r.headers.get("content-type", "")
    print(f"  GET {url}\n    -> {r.status_code} {ct} {len(r.content)}B")
    return r

print("=== index page ===")
r = fetch(INDEX)
html = r.text
hrefs = re.findall(r'href="([^"]+\.xlsx)"', html)
print("xlsx hrefs found:", len(hrefs))
for h in sorted(set(hrefs)):
    print("   ", h)
