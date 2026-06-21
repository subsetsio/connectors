import sys, os; sys.path.insert(0, "src")
import nodes.civil_aviation_authority as m
for eid in ["airport-09", "airline-0-1-6", "airport-04a", "punctuality-summary-analysis"]:
    nid = f"civil-aviation-authority-{eid}"
    family, key = eid.split("-",1)
    if family in m._TABLE_FAMILIES:
        recs = m._fetch_annual_table(family, key)
    else:
        recs = m._fetch_punctuality(key)
    recs = m._coerce(recs)
    yrs = sorted({r["release_period"] for r in recs})
    print(f"{eid}: {len(recs)} rows, years {yrs[0]}..{yrs[-1]} ({len(yrs)})")
    print("   sample keys:", list(recs[0].keys())[:8])
