import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import duckdb, json

# sample raw rows mimicking what the fetch fns write
ft = [
  {"name1":"A Clinic","name2":"","street1":"1 Main","street2":"","city":"Albany","state":"NY","zip":"12207","phone":"555-1212","intake1":None,"hotline1":None,"website":"https://x.org","latitude":"42.6","longitude":"-73.7","typeFacility":"MH"},
  {"name1":"A Clinic","name2":"","street1":"1 Main","street2":"","city":"Albany","state":"NY","zip":"12207","phone":"555-1212","intake1":None,"hotline1":None,"website":"https://x.org","latitude":"42.6","longitude":"-73.7","typeFacility":"MH"},
  {"name1":"B Center","name2":"Prog","street1":"2 Oak","street2":"","city":"Fargo","state":"ND","zip":"58102","phone":"","intake1":"555-0000","hotline1":None,"website":"","latitude":"","longitude":"","typeFacility":"SA"},
]
sy = [
  {"locationabbr":"AL","locationdesc":"Alabama","ffy_year":"2018","topicdesc":"Synar Report","measuredesc":"Sales to Minors","submeasure":"YTS","data_value":"6.6","data_value_unit":"%","data_value_type":"Percent","geolocation":{"latitude":"32.8"},"source":"SAMHSA"},
  {"locationabbr":"AK","locationdesc":"Alaska","ffy_year":"2017","topicdesc":"Synar Report","measuredesc":"Sales to Minors","submeasure":"YTS","data_value":"","data_value_unit":"%","data_value_type":"Percent","geolocation":None,"source":"SAMHSA"},
]
con = duckdb.connect()
con.execute("CREATE VIEW \"samhsa-findtreatment-facilities\" AS SELECT * FROM read_json_auto(?)", ["/tmp/ft.json"])
open("/tmp/ft.json","w").write("\n".join(json.dumps(r) for r in ft))
open("/tmp/sy.json","w").write("\n".join(json.dumps(r) for r in sy))
con.execute("CREATE OR REPLACE VIEW \"samhsa-findtreatment-facilities\" AS SELECT * FROM read_json_auto('/tmp/ft.json')")
con.execute("CREATE OR REPLACE VIEW \"samhsa-escb-scz6\" AS SELECT * FROM read_json_auto('/tmp/sy.json')")

import re
src = open("src/nodes/samhsa.py").read()
sqls = re.findall(r"sql='''(.*?)'''", src, re.S)
for i,q in enumerate(sqls):
    r = con.execute(q).fetch_arrow_table()
    print(f"--- transform {i}: {r.num_rows} rows, cols={r.column_names}")
    print(r.to_pylist())
