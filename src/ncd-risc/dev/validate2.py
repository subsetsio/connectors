import io, json, tempfile, os, sys
import duckdb
from subsets_utils import get
sys.path.insert(0, "src")
from nodes.ncd_risc import _melt_csv, _csv_texts, BASE, ENTITY_PATHS, DOWNLOAD_SPECS, TRANSFORM_SPECS

byid = {t.deps[0]: t for t in TRANSFORM_SPECS}
cases = [
 "ncd-risc-lancet-2017-men-agespecific-mean-sbp-by-country",
 "ncd-risc-nature-2026-bmi-age-standardised-country",
 "ncd-risc-lancet-2020-height-child-adolescent-country",
 "ncd-risc-lancet-2024-diabetes-crude-world",
]
for eid in cases:
    sid = f"ncd-risc-{eid}"
    path = ENTITY_PATHS[eid]
    content = get(BASE+path, timeout=(10,180)).content
    rows=[r for text in _csv_texts(content, path) for r in _melt_csv(text, eid)]
    nn=sum(1 for r in rows if r["value"] is not None)
    print(f"== {eid}: rows={len(rows)} nonnull={nn} sample={rows[0]}")
    fd,p=tempfile.mkstemp(suffix=".ndjson")
    with os.fdopen(fd,"w") as f:
        for r in rows[:3000]: f.write(json.dumps(r)+"\n")
    con=duckdb.connect()
    con.execute(f'CREATE VIEW "{sid}" AS SELECT * FROM read_json_auto(\'{p}\')')
    sql = byid[sid].sql
    res = con.execute(sql).fetch_arrow_table()
    print(f"   transform OK rows={res.num_rows} schema={[ (f.name,str(f.type)) for f in res.schema ]}")
    os.remove(p)
