import sys, json, re, tempfile, os
sys.path.insert(0,'src')
import duckdb
from nodes.cedefop import _discover, _melt, _get_json, _slug, _transform_sql
from constants import SUBSETS

base, static, templ, iso = _discover()
# test two entities: a country panel (with eu) and templated sector-occupations (1 country only for speed)
for ent in ["country-sectors", "sector-occupations"]:
    cfg = SUBSETS[ent]
    if ent == "sector-occupations":
        prefix = next(t for t in templ if _slug(t.rstrip('-')+'.json.gz')==ent)
        rows = list(_melt(_get_json(base+prefix+iso[0]+".json.gz")))
    else:
        m=[p for p in static if _slug(p)==ent][0]
        rows=list(_melt(_get_json(base+m)))
        for eu in [p for p in static if _slug(p)==ent+"-eu"]:
            rows+=list(_melt(_get_json(base+eu)))
    f=tempfile.NamedTemporaryFile(suffix=".ndjson",delete=False,mode="w")
    for r in rows: f.write(json.dumps(r)+"\n")
    f.close()
    did=f"cedefop-{ent}"
    sql=_transform_sql(did,cfg["dims"],cfg["value_col"])
    con=duckdb.connect()
    con.execute(f'CREATE VIEW "{did}" AS SELECT * FROM read_json_auto(\'{f.name}\')')
    res=con.execute(sql).fetch_arrow_table()
    print(f"\n=== {ent} === raw {len(rows)} -> transform {res.num_rows} cols {res.column_names}")
    print(res.slice(0,2).to_pylist())
    os.unlink(f.name)
