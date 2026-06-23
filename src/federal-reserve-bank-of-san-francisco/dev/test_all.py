import re, sys
sys.path.insert(0, "dev")
from subsets_utils import get
from parser import parse_workbook

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
xlsxpat = re.compile(r'href="([^"]*wp-content/uploads/[^"]+?\.xlsx)(?:\?[^"]*)?"', re.I)

tot=0
for s in SLUGS:
    r=get(base+s+"/",timeout=(10,60)); 
    urls=[]
    for m in xlsxpat.finditer(r.text):
        u=m.group(1)
        if not u.startswith("http"): u="https://www.frbsf.org"+u
        if u not in urls: urls.append(u)
    rows=[]
    for u in urls:
        rr=get(u,timeout=(10,120)); rr.raise_for_status()
        stem=u.split("/")[-1].rsplit(".",1)[0]
        try:
            rows += parse_workbook(rr.content, stem)
        except Exception as e:
            print(f"  !! parse error {s} {stem}: {type(e).__name__}: {e}")
    tot+=len(rows)
    if not rows:
        print(f"{s}: 0 ROWS  (xlsx={[u.split('/')[-1] for u in urls]})"); continue
    sheets=sorted(set(x['sheet'] for x in rows))
    nseries=len(set((x['sheet'],x['series']) for x in rows))
    dates=[x['date'] for x in rows if x['date']]
    ndim=len(set(x['dimension'] for x in rows if x['dimension']))
    nullperiod=sum(1 for x in rows if not x['date'])
    dr = f"{min(dates)}..{max(dates)}" if dates else "NO-DATES"
    print(f"{s}: {len(rows):>7} rows | {len(sheets)} sheets | {nseries} series | dims={ndim} | {dr} | nodate={nullperiod}")
print("TOTAL ROWS", tot)
