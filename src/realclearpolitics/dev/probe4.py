import sys, json, tempfile, os
sys.path.insert(0, "src"); sys.path.insert(0, "src/nodes")
import importlib, duckdb
m = importlib.import_module("realclearpolitics")
races = dict(list(m._enumerate_races().items())[:4])

def readings(races):
    rows=[]
    for rid,href in races.items():
        d=m._race_json(rid)
        if not d: continue
        mi=d.get("moduleInfo",{}); year,office=m._classify(href)
        for poll in d.get("poll",[]):
            rt="rcp_average" if poll.get("type")=="rcp_average" else "poll"
            sp=poll.get("spread") or {}
            for c in poll.get("candidate") or []:
                rows.append({"race_id":int(rid),"race_title":mi.get("title"),"office":office,"year":year,
                 "state":mi.get("state"),"country":mi.get("country"),"category":mi.get("category"),
                 "reading_type":rt,"poll_id":poll.get("id"),"pollster":poll.get("pollster"),
                 "date_label":poll.get("date"),"data_start_date":poll.get("data_start_date") or None,
                 "data_end_date":poll.get("data_end_date") or None,"sample_size_raw":poll.get("sampleSize") or None,
                 "margin_error":poll.get("marginError") or None,"partisan":poll.get("partisan") or None,
                 "candidate":c.get("name"),"affiliation":c.get("affiliation") or None,"value":c.get("value") or None,
                 "spread_candidate":sp.get("name") or None,"spread_value":sp.get("value") or None,
                 "last_build_date":mi.get("lastBuildDate")})
    return rows

def racecat(races):
    rows=[]
    for rid,href in races.items():
        d=m._race_json(rid)
        if not d: continue
        mi=d.get("moduleInfo",{}); pr=d.get("poll",[]); year,office=m._classify(href)
        names=m._candidate_names(pr)
        rows.append({"race_id":int(rid),"title":mi.get("title"),"office":office,"year":year,
         "state":mi.get("state") or None,"country":mi.get("country") or None,"category":mi.get("category") or None,
         "slug":mi.get("poll_contentful_slug") or None,"fullpath":mi.get("poll_contentful_fullpath") or None,
         "link":mi.get("link") or None,"num_candidates":len(names),
         "candidate_names":", ".join(names) if names else None,
         "num_polls":sum(1 for p in pr if p.get("type")!="rcp_average"),"last_build_date":mi.get("lastBuildDate")})
    return rows

def run(view, rows, sql):
    f=tempfile.mktemp(suffix=".ndjson"); open(f,"w").write("\n".join(json.dumps(r) for r in rows))
    con=duckdb.connect()
    con.execute(f'CREATE VIEW "{view}" AS SELECT * FROM read_json_auto(\'{f}\')')
    res=con.execute(sql).fetch_arrow_table(); os.remove(f); return con,res

rr=readings(races)
sql1=[t.sql for t in m.TRANSFORM_SPECS if "poll-readings" in t.id][0]
con1,res1=run("realclearpolitics-poll-readings", rr, sql1)
print("READINGS in/out:", len(rr), res1.num_rows)
print("schema:", [(f.name,str(f.type)) for f in res1.schema])
con1.register("o", res1)
print("type counts:", con1.execute("SELECT reading_type,count(*) FROM o GROUP BY 1").fetchall())
print("sample poll row:", con1.execute("SELECT race_id,pollster,sample_size,sample_population,margin_error,candidate,value,poll_end_date FROM o WHERE reading_type='poll' AND sample_size IS NOT NULL LIMIT 2").fetchall())

rc=racecat(races)
sql2=[t.sql for t in m.TRANSFORM_SPECS if "races-transform" in t.id][0]
con2,res2=run("realclearpolitics-races", rc, sql2)
print("RACES in/out:", len(rc), res2.num_rows)
print("races schema:", [(f.name,str(f.type)) for f in res2.schema])
print("sample race:", res2.slice(0,1).to_pylist())
