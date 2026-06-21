import sys, os; sys.path.insert(0,"src")
import re
from subsets_utils import get, configure_http
configure_http(headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"})
BASE="https://www.caa.co.uk"
LINK=re.compile(r'<a class="c-document__link"[^>]*href="(/Documents/Download/[^"]+)">\s*<span>([^<]+)</span>')
def links(u):
    h=get(u,timeout=(10,120)).text
    return [(BASE+a, s.strip()) for a,s in LINK.findall(h) if "(CSV" in s]
pl=links(f"{BASE}/data-and-analysis/uk-aviation-market/flight-punctuality/uk-flight-punctuality-statistics/2024/")
print("ALL annual-prefixed labels:")
for u,l in pl:
    if re.match(r'^\d{4}\b', l):
        print("  ",repr(l))
