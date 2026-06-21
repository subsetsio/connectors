"""Fetch a small sample per family, run each transform SQL via duckdb to confir
column names, the DATE cast, and CIT mixed-case quoting all resolve."""
import json
import tempfile
import os
import duckdb
from subsets_utils import get
import nodes.cftc as m

SAMPLE = {
    "cftc-legacy": ["6dca-aqww", "jun7-fc8e"],
    "cftc-disaggregated": ["72hh-3qpy", "kh3c-gbw2"],
    "cftc-tff": ["gpe5-46if", "yw9f-hn96"],
    "cftc-supplemental-cit": ["4zgm-a668"],
}

for node_id, rids in SAMPLE.items():
    rows = []
    for rid in rids:
        r = get(f"https://publicreporting.cftc.gov/resource/{rid}.json",
                params={"$limit": 200, "$order": ":id"}, timeout=(10.0, 60.0))
        r.raise_for_status()
        rows.extend(r.json())
    tmp = tempfile.NamedTemporaryFile("w", suffix=".ndjson", delete=False)
    for row in rows:
        tmp.write(json.dumps(row) + "\n")
    tmp.close()
    duckdb.sql(f'CREATE OR REPLACE TEMP VIEW "{node_id}" AS SELECT * FROM read_json_auto(\'{tmp.name}\')')
    sql = m._SQL_BY_ID[node_id]
    res = duckdb.sql(sql)
    df = res.df()
    print(f"\n=== {node_id}: {len(df)} rows, {len(df.columns)} cols ===")
    print("columns:", list(df.columns))
    print(df[["report_date", "market", "report_type", "open_interest"]].head(3).to_string())
    print("nulls in open_interest:", int(df["open_interest"].isna().sum()))
    os.unlink(tmp.name)
print("\nALL SQL OK")
