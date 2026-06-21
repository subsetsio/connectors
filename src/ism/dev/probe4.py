from datetime import date
import re, pyarrow as pa
from subsets_utils import get

_SCHEMA = pa.schema([("date",pa.date32()),("metric",pa.string()),
    ("series_code",pa.string()),("series_name",pa.string()),("value",pa.float64())])

def slug(name):
    s=(name or "").strip().lower().replace("%","pct").replace("&","and")
    return re.sub(r"[^a-z0-9]+","_",s).strip("_") or "value"

def coerce(v):
    return None if (v is None or isinstance(v,str)) else float(v)

def build(code):
    d=get(f"https://api.db.nomics.world/v22/series/ISM/{code}?observations=1&limit=1000",timeout=(10,120)).json()
    rows=[]
    for s in d["series"]["docs"]:
        for day,rv in zip(s.get("period_start_day",[]),s.get("value",[])):
            val=coerce(rv)
            if val is None: continue
            rows.append({"date":date.fromisoformat(day),"metric":slug(s.get("series_name")),
                "series_code":s.get("series_code"),"series_name":s.get("series_name"),"value":val})
    t=pa.Table.from_pylist(rows,schema=_SCHEMA)
    print(f"{code}: {len(t)} rows, metrics={sorted(set(t.column('metric').to_pylist()))}")
    return t

for c in ("bacord","pmi","buypol","nm-supdel"):
    build(c)
