import io, csv, json, gzip, os, tempfile
import duckdb
from subsets_utils import get
import nodes.california_edd as M

BASE = "https://data.ca.gov/api/3"

def first_csv_url(pkg_id):
    r = get(f"{BASE}/action/package_show", params={"id": pkg_id}, timeout=(10, 120))
    r.raise_for_status()
    for res in r.json()["result"]["resources"]:
        if (res.get("format") or "").upper() == "CSV" and res.get("url"):
            return res["url"]

def sample_rows(url, n=200):
    # Range-fetch only the head of the (possibly 70MB) file — enough for a sample.
    r = get(url, timeout=(10, 180), headers={"Range": "bytes=0-300000"})
    r.raise_for_status()
    text = r.text.lstrip("﻿")
    # drop a possibly-truncated final line
    text = text[: text.rfind("\n")]
    rdr = csv.DictReader(io.StringIO(text))
    out = []
    for row in rdr:
        out.append({k.lstrip("﻿").strip(): (v if v not in ("", None) else None) for k, v in row.items() if k is not None})
        if len(out) >= n:
            break
    return out

for spec in M.DOWNLOAD_SPECS:
    eid = spec.id[len(M.PREFIX):]
    sql = M._build_sql(spec.id)
    try:
        url = first_csv_url(eid)
        rows = sample_rows(url)
    except Exception as e:
        print(f"NET  {eid}: {type(e).__name__}: {e}")
        continue
    tmp = tempfile.NamedTemporaryFile(suffix=".ndjson", delete=False, mode="w")
    for row in rows:
        tmp.write(json.dumps(row) + "\n")
    tmp.close()
    con = duckdb.connect()
    con.sql(f'CREATE TEMP VIEW "{spec.id}" AS SELECT * FROM read_json_auto(\'{tmp.name}\')')
    try:
        res = con.sql(sql).fetchall()
        cols = [d[0] for d in con.sql(sql).description]
        # count non-null per numeric-ish column on the sample
        print(f"OK  {eid}: {len(res)} rows, {len(cols)} cols")
    except Exception as e:
        print(f"FAIL {eid}: {type(e).__name__}: {e}")
    finally:
        con.close()
        os.unlink(tmp.name)
