import sys, json, tempfile, os
sys.path.insert(0, "src"); sys.path.insert(0, "src/nodes")
import importlib, duckdb
m = importlib.import_module("realclearpolitics")
races = dict(list(m._enumerate_races().items())[:3])

def build_readings(races):
    rows=[]
    for rid,href in races.items():
        d=m._race_json(rid)
        if not d: continue
        mi=d.get("moduleInfo",{}); year,office=m._classify(href)
        for poll in d.get("poll",[]):
            rt="rcp_average" if poll.get("type")=="rcp_average" else "poll"
            spread=poll.get("spread") or {}
            for c in poll.get("candidate") or []:
                rows.append({"race_id":int(rid),"race_title":mi.get("title"),"office":office,"year":year,
                 "state":mi.get("state"),"country":mi.get("country"),"category":mi.get("category"),
                 "reading_type":rt,"poll_id":poll.get("id"),"pollster":poll.get("pollster"),
                 "date_label":poll.get("date"),"data_start_date":poll.get("data_start_date") or None,
                 "data_end_date":poll.get("data_end_date") or None,"sample_size_raw":poll.get("sampleSize") or None,
                 "margin_error":poll.get("marginError") or None,"partisan":poll.get("partisan") or None,
                 "candidate":c.get("name"),"affiliation":c.get("affiliation") or None,"value":c.get("value") or None,
                 "spread_candidate":spread.get("name") or None,"spread_value":spread.get("value") or None,
                 "last_build_date":mi.get("lastBuildDate")})
    return rows

rows=build_readings(races)
f=tempfile.mktemp(suffix=".ndjson")
open(f,"w").write("\n".join(json.dumps(r) for r in rows))
con=duckdb.connect()
con.execute(f"CREATE VIEW \"realclearpolitics-poll-readings\" AS SELECT * FROM read_json_auto('{f}')")
sql=[t.sql for t in m.TRANSFORM_SPECS if "poll-readings" in t.id][0]
res=con.execute(sql).fetch_arrow_table()
print("readings rows in/out:", len(rows), res.num_rows)
print("cols:", res.schema.names)
import pyarrow as pa
print(res.slice(0,3).to_pylist()[0])
# sample size parsing check
con.register("out", res)
print(con.execute("SELECT sample_size, sample_population, value, poll_start_date FROM out WHERE reading_type='poll' AND sample_size IS NOT NULL LIMIT 3").fetchall())
print("reading_type distinct:", con.execute("SELECT reading_type, count(*) FROM out GROUP BY 1").fetchall())
os.remove(f)
