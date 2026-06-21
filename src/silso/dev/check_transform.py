import duckdb
from nodes.silso import _fetch_text, _parse, SERIES, _TRANSFORM_SQL

for eid in SERIES:
    url, cols = SERIES[eid]
    t = _parse(_fetch_text(url), cols)
    con = duckdb.connect()
    con.register(f"silso-{eid}", t)
    res = con.execute(_TRANSFORM_SQL[f"silso-{eid}"]).to_arrow_table()
    ndef = sum(t.column("definitive").to_pylist())
    print(f"=== {eid}: raw {t.num_rows} (definitive={ndef}) -> transform {res.num_rows} rows; cols={res.column_names}")
    print("   tail:", res.slice(res.num_rows - 1, 1).to_pylist())
