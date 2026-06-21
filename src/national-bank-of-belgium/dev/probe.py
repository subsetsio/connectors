import gzip, json, csv, duckdb, httpx
from subsets_utils import get_client

BASE="https://nsidisseminate-stat.nbb.be/rest"
CSV="application/vnd.sdmx.data+csv;version=1.0.0"

def dl_ndjson(flow, path):
    c=get_client()
    with c.stream("GET", f"{BASE}/data/{flow}/all", headers={"Accept":CSV}, timeout=httpx.Timeout(300.0, connect=30.0)) as r:
        r.raise_for_status()
        rd=csv.reader(r.iter_lines())
        header=next(rd)
        header[0]=header[0].lstrip("﻿")
        n=0
        with gzip.open(path,"wt") as out:
            for row in rd:
                out.write(json.dumps(dict(zip(header,row)))+"\n"); n+=1
        return n

for flow in ["DF_EXTTRADEBENAT_Overview","CPI","DF_QNA_DISS"]:
    p=f"/tmp/{flow}.ndjson.gz"
    n=dl_ndjson(flow,p)
    sql=f'''SELECT * EXCLUDE (OBS_VALUE), TRY_CAST(OBS_VALUE AS DOUBLE) AS obs_value
            FROM read_json_auto('{p}') WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL'''
    cols=duckdb.sql(sql).columns
    cnt=duckdb.sql(f"SELECT count(*) FROM ({sql})").fetchone()[0]
    tp=duckdb.sql(f"SELECT first(typeof(TIME_PERIOD)) t, min(TIME_PERIOD) lo, max(TIME_PERIOD) hi FROM read_json_auto('{p}')").fetchone()
    print(f"{flow}: rawrows={n} outrows={cnt} TIME_PERIOD_type={tp[0]} range={tp[1]}..{tp[2]} obs_value_in={'obs_value' in cols}")
