import sys; sys.path.insert(0,"src")
import duckdb
from nodes.california_iso_oasis import TRANSFORM_SQL, _spec_id
con = duckdb.connect()
for eid, fname in [("PRC_LMP","prc_lmp"),("PRC_INTVL_LMP","prc_intvl_lmp"),("PRC_FUEL","prc_fuel"),("AS_RESULTS","as_results")]:
    view = _spec_id(eid)
    con.execute(f"CREATE VIEW \"{view}\" AS SELECT * FROM read_ndjson_auto('dev/{fname}.ndjson')")
    try:
        rel = con.sql(TRANSFORM_SQL[eid])
        df = rel.df()
        print(f"\n### {eid}: {len(df)} rows")
        print(rel.types[:6], "...")
        print(df.head(2).to_string())
    except Exception as e:
        print(f"\n### {eid} FAILED: {type(e).__name__}: {e}")
