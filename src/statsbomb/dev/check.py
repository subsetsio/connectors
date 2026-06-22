import duckdb
import pyarrow as pa
import sys
sys.path.insert(0, "src/nodes")
import statsbomb as sb

RAW = sb.RAW

# competitions: build table + run transform SQL
comps = sb._get_json(f"{RAW}/competitions.json")
ct = pa.Table.from_pylist(
    [dict(zip(sb.COMP_SCHEMA.names,
              [c.get(n) for n in sb.COMP_SCHEMA.names])) for c in comps],
    schema=sb.COMP_SCHEMA)
duckdb.sql('CREATE VIEW "statsbomb-competitions" AS SELECT * FROM ct')
r = duckdb.sql(sb.TRANSFORM_SPECS[0].sql)
print("competitions transform rows:", len(r.fetchall()), "cols:", r.columns)

# matches
mid_seen = None
mrows = []
for cid, sid in sb._competition_seasons()[:2]:
    for m in sb._get_json(f"{RAW}/matches/{cid}/{sid}.json"):
        mrows.append(sb._match_row(m))
        mid_seen = mid_seen or m["match_id"]
mt = pa.Table.from_pylist(mrows, schema=sb.MATCH_SCHEMA)
duckdb.sql('CREATE VIEW "statsbomb-matches" AS SELECT * FROM mt')
r = duckdb.sql(sb.TRANSFORM_SPECS[1].sql)
print("matches transform rows:", len(r.fetchall()))

# events flatten + schema coercion on a real match
ev = sb._get_json(f"{RAW}/events/{mid_seen}.json")
et = pa.Table.from_pylist([sb._event_row(e, mid_seen) for e in ev], schema=sb.EVENT_SCHEMA)
print("events rows:", et.num_rows, "| sample types:",
      duckdb.sql('SELECT DISTINCT type_name FROM et LIMIT 5').fetchall())
duckdb.sql('CREATE VIEW "statsbomb-events" AS SELECT * FROM et')
r = duckdb.sql(sb.TRANSFORM_SPECS[2].sql)
print("events transform rows:", len(r.fetchall()))

# lineups
lu = sb._get_json(f"{RAW}/lineups/{mid_seen}.json")
lt = pa.Table.from_pylist(sb._lineup_rows(lu, mid_seen), schema=sb.LINEUP_SCHEMA)
print("lineup rows:", lt.num_rows)

# three sixty
t360 = sb._match_ids_with_360()
print("matches with 360:", len(t360))
fr = sb._get_json(f"{RAW}/three-sixty/{t360[0]}.json")
tt = pa.Table.from_pylist(sb._threesixty_rows(fr, t360[0]), schema=sb.THREESIXTY_SCHEMA)
print("360 rows for one match:", tt.num_rows,
      "| x range:", duckdb.sql("SELECT min(x), max(x), min(y), max(y) FROM tt").fetchall())
print("ALL OK")
