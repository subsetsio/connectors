import io, json, zipfile, tempfile, os, gzip
import duckdb
from subsets_utils import get
import sys
sys.path.insert(0, "src")
from nodes.ncd_risc import _melt_csv, _csv_texts, BASE, ENTITY_PATHS

cases = [
 "ncd-risc-lancet-2017-bp-age-standardised-world",      # multi-metric, no age col
 "ncd-risc-lancet-2017-men-agespecific-mean-sbp-by-country",  # no sex col -> infer
 "ncd-risc-nature-2026-bmi-age-standardised-country",   # BOM header, unicode metrics
 "ncd-risc-lancet-2020-height-child-adolescent-country",# zip
 "ncd-risc-lancet-2024-diabetes-crude-world",           # crude variant
]
for eid in cases:
    path = ENTITY_PATHS[eid]
    content = get(BASE+path, timeout=(10,180)).content
    rows=[]
    for text in _csv_texts(content, path):
        for r in _melt_csv(text, eid):
            rows.append(r)
    nn = sum(1 for r in rows if r["value"] is not None)
    print(f"== {eid}: long_rows={len(rows)} nonnull={nn}")
    print("   sample:", rows[0])
    # run the transform SQL via duckdb over an ndjson temp file
    fd, p = tempfile.mkstemp(suffix=".ndjson")
    with os.fdopen(fd,"w") as f:
        for r in rows[:2000]:
            f.write(json.dumps(r)+"\n")
    con = duckdb.connect()
    con.execute(f"CREATE VIEW v AS SELECT * FROM read_json_auto('{p}')")
    res = con.execute('''SELECT area,iso,sex,CAST(year AS INTEGER) AS year,age,metric,CAST(value AS DOUBLE) value FROM v WHERE value IS NOT NULL''').fetchall()
    print(f"   transform rows (of 2000)={len(res)}; e.g. {res[0]}")
    os.remove(p)
