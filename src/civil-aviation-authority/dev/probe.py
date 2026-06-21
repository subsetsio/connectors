import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import re, csv, io
from subsets_utils import get

BASE="https://www.caa.co.uk"
def html(url):
    r=get(url, timeout=(10,120)); r.raise_for_status(); return r.text
LINK=re.compile(r'<a class="c-document__link"[^>]*href="(/Documents/Download/[^"]+)">\s*<span>([^<]+)</span>')
SIZE=re.compile(r"\s*\((CSV|PDF)[^)]*\)\s*$", re.I)

def csv_links(url):
    out=[]
    for href,span in LINK.findall(html(url)):
        span=span.strip()
        if "(CSV" not in span: continue
        out.append((href, SIZE.sub("", span).strip()))
    return out

# AIRPORT table 09 from annual 2024
links=csv_links(f"{BASE}/data-and-analysis/uk-aviation-market/airports/uk-airport-data/uk-airport-data-2024/annual-2024/")
t09=[(h,l) for h,l in links if l.startswith("Table 09")][0]
print("AIRPORT t09 label:",t09[1])
txt=get(BASE+t09[0], timeout=(10,120)).text
print("---- first 6 lines ----")
for ln in txt.splitlines()[:6]: print(repr(ln))
print("---- last 3 lines ----")
for ln in txt.splitlines()[-3:]: print(repr(ln))

# AIRLINE 0.1.6 annual 2024
al=csv_links(f"{BASE}/data-and-analysis/uk-aviation-market/airlines/uk-airline-data/uk-airline-data-2024/annual-2024/")
a016=[(h,l) for h,l in al if re.match(r'Table 0 1 6\b',l)][0]
print("\nAIRLINE 0.1.6 label:",a016[1])
atxt=get(BASE+a016[0], timeout=(10,120)).text
for ln in atxt.splitlines()[:6]: print(repr(ln))

# PUNCTUALITY summary annual 2024
pl=csv_links(f"{BASE}/data-and-analysis/uk-aviation-market/flight-punctuality/uk-flight-punctuality-statistics/2024/")
psum=[(h,l) for h,l in pl if l.startswith("2024 Annual") and "Summary" in l][0]
print("\nPUNCT summary label:",psum[1])
ptxt=get(BASE+psum[0], timeout=(10,120)).text
for ln in ptxt.splitlines()[:4]: print(repr(ln))
