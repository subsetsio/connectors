import re
from subsets_utils import get, configure_http

DISCOVERY = "https://au.seek.com/about/news/seek-employment-data"
configure_http(headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"})
html = get(DISCOVERY, timeout=(10,120)).text
print("page bytes:", len(html))
# find graphassets links near anchor text
links = re.findall(r'href="(https://[^"]*graphassets\.com/[^"]+)"', html)
print("graphassets hrefs found:", len(links))
for l in sorted(set(links)):
    print("  ", l)
# anchor-text based
for label in ["Employment data", "Advertised Salary"]:
    idx = html.find(label)
    print(f"label {label!r} at idx", idx)
