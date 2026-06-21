import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import pyarrow as pa, duckdb
from nodes.swiss_national_bank import _cube_for, _cube_url, _fetch_json, SCHEMA, _spec_id, ENTITY_IDS

# pick a topic cube and a deep warehouse cube
samples = ["gdppr", "BSTA@SNB.Z.MONA_US", "ddumfxd", ENTITY_IDS[-1]]
for cube in samples:
    sid=_spec_id(cube)
    assert _cube_for(sid)==cube, (sid, _cube_for(sid))
    payload=_fetch_json(_cube_url(cube))
    rows=[]
    for s in payload.get("timeseries",[]):
        meta=s.get("metadata",{}) or {}
        label=" | ".join((h.get("dimItem") or "") for h in (s.get("header") or []))
        for p in s.get("values",[]) or []:
            v=p.get("value")
            rows.append({"cube_id":cube,"series_key":meta.get("key",""),"series_label":label,
                "frequency":meta.get("frequency"),"unit":meta.get("unit"),"scale":meta.get("scale"),
                "period":p.get("date"),"value":float(v) if v is not None else None})
    t=pa.Table.from_pylist(rows, schema=SCHEMA)
    con=duckdb.connect()
    con.register("v", t)
    res=con.execute(f'''SELECT cube_id, series_key, series_label, frequency, unit, scale, period,
        CAST(value AS DOUBLE) AS value FROM v WHERE value IS NOT NULL''').fetch_arrow_table()
    print(f"{cube}: raw_rows={t.num_rows} transform_rows={res.num_rows} cols={res.column_names}")
    print("   sample:", res.slice(0,1).to_pylist())
