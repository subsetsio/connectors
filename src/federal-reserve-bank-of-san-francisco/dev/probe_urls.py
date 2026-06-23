import re, sys
from subsets_utils import get

SLUGS = [
 "china-cyclical-activity-tracker","cpi-inflation-contributions-from-goods-and-services",
 "cyclical-and-acyclical-core-pce-inflation","daily-news-sentiment-index",
 "interest-rate-probability-distributions","labor-market-stress-indicator",
 "market-based-monetary-policy-uncertainty","monetary-policy-surprises",
 "pandemic-era-excess-savings","pce-inflation-contributions-from-goods-and-services",
 "pce-personal-consumption-expenditure-price-index-pcepi","proxy-funds-rate",
 "regional-indicators-for-labor-markets-and-prices","supply-and-demand-driven-pce-inflation",
 "total-factor-productivity-tfp","treasury-yield-premiums","treasury-yield-skewness",
 "twelfth-district-business-sentiment","us-monetary-policy-event-study-database",
 "weather-adjusted-employment-change","zero-lower-bound-probabilities-at-different-time-horizons",
 "revisions-to-payroll-employment-gains",
]
base="https://www.frbsf.org/research-and-insights/data-and-indicators/"
linkpat = re.compile(r'href="([^"]*wp-content/uploads/[^"]+?\.(?:xlsx|xls|csv))(?:\?[^"]*)?"', re.I)
for s in SLUGS:
    try:
        r = get(base+s+"/", timeout=(10,60))
        links = []
        for m in linkpat.finditer(r.text):
            u = m.group(1)
            if not u.startswith("http"): u = "https://www.frbsf.org"+u
            if u not in links: links.append(u)
        print(f"{s}  [{r.status_code}]  {len(links)} file(s)")
        for u in links: print("    ", u.split('/wp-content/uploads/')[-1])
    except Exception as e:
        print(f"{s}  ERROR {type(e).__name__}: {e}")
