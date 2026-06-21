import json, datetime as dt
from urllib.parse import quote
import duckdb
from subsets_utils import get
HDRS={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36","Accept":"application/json"}
BASE="https://api.nasdaq.com/api"
def gj(u): 
    r=get(u,headers=HDRS,timeout=(10,60)); r.raise_for_status(); return r.json()
def s(v): return None if v is None else str(v)

con=duckdb.connect()

# stocks sample
d=gj(f"{BASE}/screener/stocks?limit=20&offset=0")["data"]["table"]["rows"]
stocks=[{k:s(r.get(k)) for k in ("symbol","name","lastsale","netchange","pctchange","marketCap")} for r in d]
# etfs
d=gj(f"{BASE}/screener/etf?limit=20&offset=0")["data"]["records"]["data"]["rows"]
etfs=[{k:s(r.get(k)) for k in ("symbol","companyName","lastSalePrice","netChange","percentageChange","oneYearPercentage")} for r in d]
# historical
hp=[]
for sym,ac in [("AAPL","stocks"),("QQQ","etf")]:
    rows=gj(f"{BASE}/quote/{quote(sym)}/historical?assetclass={ac}&fromdate=2024-01-01&todate=2026-06-18&limit=99999")["data"]["tradesTable"]["rows"]
    for r in rows[:30]:
        hp.append({"symbol":sym,"assetclass":ac,"date":s(r.get("date")),"open":s(r.get("open")),"high":s(r.get("high")),"low":s(r.get("low")),"close":s(r.get("close")),"volume":s(r.get("volume"))})
# dividends
dv=[]
day=dt.date(2026,6,15).isoformat()
for r in gj(f"{BASE}/calendar/dividends?date={day}")["data"]["calendar"]["rows"][:20]:
    dv.append({k:s(r.get(k)) for k in ("symbol","companyName","dividend_Ex_Date","payment_Date","record_Date","dividend_Rate","indicated_Annual_Dividend","announcement_Date")})
# earnings
ern=[]
for r in gj(f"{BASE}/calendar/earnings?date=2026-06-18")["data"]["rows"][:20]:
    row={"report_date":"2026-06-18"}; row.update({k:s(r.get(k)) for k in ("symbol","name","time","marketCap","fiscalQuarterEnding","epsForecast","noOfEsts","lastYearRptDt","lastYearEPS")}); ern.append(row)
# ipos
ip=[]
for r in gj(f"{BASE}/ipo/calendar?date=2026-05")["data"]["priced"]["rows"][:20]:
    ip.append({k:s(r.get(k)) for k in ("proposedTickerSymbol","companyName","proposedExchange","proposedSharePrice","sharesOffered","pricedDate","dollarValueOfSharesOffered","dealID")})
# splits
sp=[]
for r in gj(f"{BASE}/calendar/splits")["data"]["rows"][:20]:
    sp.append({k:s(r.get(k)) for k in ("symbol","name","ratio","executionDate")})

reg={"nasdaq-stocks":stocks,"nasdaq-etfs":etfs,"nasdaq-historical-prices":hp,"nasdaq-dividends":dv,"nasdaq-earnings":ern,"nasdaq-ipos":ip,"nasdaq-splits":sp}
import pyarrow as pa
for name,rows in reg.items():
    t=pa.Table.from_pylist(rows)
    con.register(name, t)

# import the actual TRANSFORM_SPECS from the node module
import importlib.util, sys
sys.path.insert(0,"src")
mod=importlib.import_module("nodes.nasdaq")
for sp_ in mod.TRANSFORM_SPECS:
    try:
        res=con.execute(sp_.sql).fetchdf()
        print(f"OK  {sp_.id}: {len(res)} rows, cols={list(res.columns)}")
        print("    sample:", res.head(1).to_dict('records'))
    except Exception as e:
        print(f"FAIL {sp_.id}: {type(e).__name__}: {e}")
