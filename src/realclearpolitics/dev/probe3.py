import sys, json, tempfile, os
sys.path.insert(0, "src"); sys.path.insert(0, "src/nodes")
import importlib, duckdb
m = importlib.import_module("realclearpolitics")
races = dict(list(m._enumerate_races().items())[:3])
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
f=tempfile.mktemp(suffix=".ndjson")
open(f,"w").write("\n".join(json.dumps(r) for r in rows))
con=duckdb.connect()
print(con.execute(f"DESCRIBE SELECT * FROM read_json_auto('{f}')").fetchall())
os.remove(f)
