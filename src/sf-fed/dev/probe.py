import re, io
from subsets_utils import get

ENTITY_IDS = [
  "china-cyclical-activity-tracker","cpi-inflation-contributions-from-goods-and-services",
  "cyclical-and-acyclical-core-pce-inflation","daily-news-sentiment-index",
  "interest-rate-probability-distributions","labor-market-stress-indicator",
  "market-based-monetary-policy-uncertainty","monetary-policy-surprises",
  "pandemic-era-excess-savings","pce-inflation-contributions-from-goods-and-services",
  "pce-personal-consumption-expenditure-price-index-pcepi","proxy-funds-rate",
  "regional-indicators-for-labor-markets-and-prices","revisions-to-payroll-employment-gains",
  "supply-and-demand-driven-pce-inflation","total-factor-productivity-tfp",
  "treasury-yield-premiums","treasury-yield-skewness","twelfth-district-business-sentiment",
  "us-monetary-policy-event-study-database","weather-adjusted-employment-change",
  "zero-lower-bound-probabilities-at-different-time-horizons",
]
BASE = "https://www.frbsf.org/research-and-insights/data-and-indicators/"
FILE_RE = re.compile(r'href="([^"]*\.(?:xlsx|xls|csv))(?:\?[^"]*)?"', re.IGNORECASE)

for eid in ENTITY_IDS:
    url = BASE + eid + "/"
    try:
        html = get(url, timeout=(10, 60)).text
    except Exception as e:
        print(f"## {eid}\n  PAGE ERROR {type(e).__name__}: {e}")
        continue
    hrefs = []
    seen = set()
    for m in FILE_RE.finditer(html):
        h = m.group(1)
        if h.startswith("/"):
            h = "https://www.frbsf.org" + h
        if h not in seen:
            seen.add(h); hrefs.append(h)
    print(f"## {eid}")
    print(f"   files: {hrefs if hrefs else 'NONE'}")
