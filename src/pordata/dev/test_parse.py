import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))
from subsets_utils import get
from parser import parse_indicator
import collections
for url in [
  "https://www.pordata.pt/en/portugal/resident+population+total+and+by+age+group-10",
  "https://www.pordata.pt/en/portugal/gross+domestic+product+(gdp)-130",
  "https://www.pordata.pt/en/portugal/unemployment+rate+total+and+by+sex+(percentage)-550",
  "https://www.pordata.pt/en/portugal/gross+domestic+product+(gdp)+annual+growth+rate-2298",
]:
    r = get(url, timeout=(10,60))
    recs = parse_indicator(r.text)
    nn = [x for x in recs if x["value"] is not None]
    series = collections.Counter(x["series"] for x in recs)
    periods = sorted({x["period"] for x in recs if x["period"]})
    print(f"\n{url.split('/')[-1]}")
    print(f"  recs={len(recs)} non_null={len(nn)} distinct_series={len(series)} periods[{len(periods)}]={periods[:3]}..{periods[-2:]}")
    for x in recs[:2]+recs[-2:]:
        print("   ", {k:x[k] for k in ('period','series','series_group','value','value_text')})
