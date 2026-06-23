import os, sys, json, ssl, httpx, duckdb
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils.http_client as hc
ctx=ssl.create_default_context(); ctx.set_ciphers("DEFAULT")
hc._client=httpx.Client(timeout=60, headers=hc._client_config["headers"], follow_redirects=True, verify=ctx)

import importlib.util
spec=importlib.util.spec_from_file_location("ctg","src/nodes/clinicaltrials_gov.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

from subsets_utils import get
con=duckdb.connect()
TMAP={t.deps[0]: t.sql for t in m.TRANSFORM_SPECS}
for entity, fields in m.ENTITY_FIELDS.items():
    r=get(m.BASE, params={"pageSize":300,"fields":",".join(fields),"countTotal":"false"}, timeout=(10,90))
    r.raise_for_status()
    studies=r.json()["studies"]
    rows=[row for s in studies for row in m.EXTRACTORS[entity](s)]
    asset=f"clinicaltrials-gov-{entity}"
    # write rows to a temp ndjson and run the transform SQL via a view
    path=f"dev/_smoke_{entity}.ndjson"
    with open(path,"w") as fh:
        for row in rows: fh.write(json.dumps(row)+"\n")
    con.execute(f'CREATE OR REPLACE VIEW "{asset}" AS SELECT * FROM read_json_auto(?)',[path])
    out=con.execute(TMAP[asset]).fetchdf()
    print(f"\n=== {entity}: {len(studies)} studies -> {len(rows)} raw rows -> {len(out)} transform rows")
    print("cols:", list(out.columns))
    print(out.head(2).to_dict("records"))
    os.remove(path)
