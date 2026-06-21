"""Local smoke test: fetch small windows, write ndjson, run each transform SQL
via DuckDB read_json_auto to verify column refs / casts resolve and yield rows."""
import json, tempfile, os, duckdb
import nodes.ny_fed as m

tmp = tempfile.mkdtemp()

def write(asset, rows):
    p = os.path.join(tmp, f"{asset}.ndjson")
    with open(p, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return p

# Build tiny raw samples by calling the internal helpers with narrow windows.
from datetime import date, timedelta
def search_small(template, *kp, start, end=None):
    # one ~80-day chunk only (under the API's per-request range cap)
    end = end or (start + timedelta(days=80))
    from nodes.ny_fed import _get_json
    path = template.format(startDate=start.isoformat(), endDate=end.isoformat())
    payload = _get_json(path)
    node = payload
    for k in kp:
        node = node.get(k, {}) if isinstance(node, dict) else {}
    return node if isinstance(node, list) else []

samples = {}

# rates
samples["ny-fed-reference-rates-unsecured"] = [m._project(r, m._RATE_FIELDS) for r in search_small("rates/all/search.json?startDate={startDate}&endDate={endDate}","refRates",start=date(2026,5,1)) if r.get("type") in ("EFFR","OBFR")]
samples["ny-fed-reference-rates-secured"] = [m._project(r, m._RATE_FIELDS) for r in search_small("rates/secured/all/search.json?startDate={startDate}&endDate={endDate}","refRates",start=date(2026,5,1)) if r.get("type") in ("SOFR","BGCR","TGCR","SOFRAI")]
# operations
samples["ny-fed-repo-operations"] = list(m._flatten_operations(search_small("rp/results/search.json?startDate={startDate}&endDate={endDate}","repo","operations",start=date(2026,5,1)), m._REPO_PARENT, m._REPO_DETAIL))
samples["ny-fed-ambs-operations"] = list(m._flatten_operations(search_small("ambs/all/results/details/search.json?startDate={startDate}&endDate={endDate}","ambs","auctions",start=date(2026,4,1)), m._AMBS_PARENT, m._AMBS_DETAIL))
samples["ny-fed-treasury-operations"] = list(m._flatten_operations(search_small("tsy/all/results/details/search.json?startDate={startDate}&endDate={endDate}","treasury","auctions",start=date(2024,1,1)), m._TSY_PARENT, m._TSY_DETAIL))
samples["ny-fed-securities-lending"] = list(m._flatten_operations(search_small("seclending/all/results/details/search.json?startDate={startDate}&endDate={endDate}","seclending","operations",start=date(2026,5,1)), m._SECLEND_PARENT, m._SECLEND_DETAIL))
samples["ny-fed-fx-swaps"] = [m._project(r, m._FXS_FIELDS) for r in search_small("fxs/all/search.json?startDate={startDate}&endDate={endDate}","fxSwaps","operations",start=date(2020,3,1))]
# soma summary
from nodes.ny_fed import _get_json
summ = _get_json("soma/summary.json").get("soma",{}).get("summary",[])
samples["ny-fed-soma-summary"] = [m._project(r, m._SUMMARY_FIELDS) for r in summ]
# soma holdings latest
asof = max(s["asOfDate"] for s in summ if s.get("asOfDate"))
hold=[]
for grp,p in (("Treasury",f"soma/tsy/get/all/asof/{asof}.json"),("Agency",f"soma/agency/get/asof/{asof}.json")):
    h=_get_json(p).get("soma",{}).get("holdings",[])
    hold.extend(m._project(x,m._HOLDING_FIELDS,extra={"instrumentGroup":grp}) for x in h)
samples["ny-fed-soma-holdings"]=hold
# pd: just two series
listing=_get_json("pd/list/timeseries.json").get("pd",{}).get("timeseries",[])[:3]
pdrows=[]
for s in listing:
    ts=m._get_series(s["keyid"]) or []
    for o in ts:
        pdrows.append({"asofdate":o.get("asofdate"),"keyid":o.get("keyid"),"value":o.get("value"),"seriesbreak":s.get("seriesbreak"),"description":s.get("description")})
samples["ny-fed-primary-dealer-values"]=pdrows

paths={a:write(a,rows) for a,rows in samples.items()}
for a,rows in samples.items():
    print(f"{a}: {len(rows)} raw rows")

con=duckdb.connect()
for spec in m.TRANSFORM_SPECS:
    dep=spec.deps[0]
    sql=spec.sql.replace(f'"{dep}"', f"read_json_auto('{paths[dep]}')")
    try:
        res=con.execute(sql).fetchall()
        cols=[d[0] for d in con.execute(sql).description]
        print(f"OK  {spec.id}: {len(res)} rows, {len(cols)} cols -> {cols}")
    except Exception as e:
        print(f"FAIL {spec.id}: {type(e).__name__}: {e}")
