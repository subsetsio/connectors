import sys, os; sys.path.insert(0,"src")
import nodes.civil_aviation_authority as m
from subsets_utils import configure_http
configure_http(headers={"User-Agent":m._BROWSER_UA})
for key in ["full-analysis","full-analysis-arrival-departure","summary-analysis"]:
    recs=m._coerce(m._fetch_punctuality(key))
    yrs=sorted({r["release_period"] for r in recs})
    print(f"punctuality-{key}: {len(recs)} rows, years {yrs[0]}..{yrs[-1]} ({len(yrs)})")
