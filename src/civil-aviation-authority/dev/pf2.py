import sys, os; sys.path.insert(0,"src")
import re
from subsets_utils import get, configure_http
import nodes.civil_aviation_authority as m
configure_http(headers={"User-Agent":m._BROWSER_UA})
BASE="https://www.caa.co.uk"
for u,l in m._csv_links(f"{BASE}/data-and-analysis/uk-aviation-market/flight-punctuality/uk-flight-punctuality-statistics/2024/"):
    if l in ("2024 Annual Punctuality Statistics Full Analysis","2024 Annual Punctuality Statistics Full Analysis Arrival Departure"):
        txt=get(u,timeout=(10,120)).text
        print("==",l)
        for i,ln in enumerate(txt.splitlines()[:5]):
            print(f"  [{i}]",repr(ln[:200]))
        recs=m._parse_csv(txt)
        print("  parsed rows:",len(recs))
