import sys, os, re
sys.path.insert(0, os.path.join("src"))
from subsets_utils import get
BASE="https://www.bruegel.org"
PAGES={
 "energy-crisis":"/dataset/2026-european-energy-crisis-fiscal-response-tracker",
 "divisia":"/dataset/divisia-monetary-aggregates-euro-area",
 "eu-labour":"/dataset/eu-labour-market-outlook-dashboard",
 "eu-renewables":"/dataset/eu-renewables-value-tracker",
 "gas-imports":"/dataset/european-natural-gas-imports",
 "gini":"/dataset/global-and-regional-gini-coefficients-income-inequality",
 "global-trade":"/dataset/global-trade-tracker",
 "reer":"/publications/datasets/real-effective-exchange-rates-for-178-countries-a-new-database",
 "russian":"/dataset/russian-foreign-trade-tracker",
 "sovereign":"/dataset/sovereign-bond-holdings",
 "us-fms":"/dataset/us-foreign-military-sales",
}
RE=re.compile(r'href="((?:https?://[^"]+)?/(?:sites/default|system)/files/[^"]+\.(?:xlsx|xls|csv|zip|7z))"',re.I)
H={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36","Accept":"text/html","Accept-Language":"en-US,en;q=0.9"}
for k,p in PAGES.items():
    try:
        html=get(BASE+p,timeout=(10,60),headers=H).text
        links=[]
        for m in RE.finditer(html):
            u=m.group(1)
            if not u.startswith("http"): u=BASE+u
            if u not in links: links.append(u)
        print(f"{k}\t{len(links)}\t{links[:3]}")
    except Exception as e:
        print(f"{k}\tERR\t{type(e).__name__}: {str(e)[:60]}")
