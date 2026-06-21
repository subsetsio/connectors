import io, csv, json, os, tempfile
import duckdb
from subsets_utils import get
from constants import CKAN_RESOURCE_IDS
import nodes.aihw as M

CKAN="https://data.gov.au/data/api/3/action"
tmp=tempfile.mkdtemp()

def fetch_ckan_ndjson(rid):
    url=get(f"{CKAN}/resource_show",params={"id":rid},timeout=(10,60)).json()["result"]["url"]
    raw=get(url,timeout=(10,300)).content
    try: text=raw.decode("utf-8-sig")
    except UnicodeDecodeError: text=raw.decode("cp1252")
    rows=list(csv.DictReader(io.StringIO(text)))
    p=os.path.join(tmp,f"aihw-{rid}.ndjson")
    with open(p,"w") as f:
        for r in rows: f.write(json.dumps(r)+"\n")
    return p,len(rows)

def fetch_ru():
    units=json.loads(get("https://myhospitalsapi.aihw.gov.au/api/v1/reporting-units",headers={"Accept":"application/json"},timeout=(10,120)).content.decode("utf-8-sig"))["result"]
    rows=[]
    for u in units:
        rut=u.get("reporting_unit_type") or {}
        rows.append({"reporting_unit_code":u.get("reporting_unit_code"),"reporting_unit_name":u.get("reporting_unit_name"),"reporting_unit_type_code":rut.get("reporting_unit_type_code"),"reporting_unit_type_name":rut.get("reporting_unit_type_name"),"latitude":u.get("latitude"),"longitude":u.get("longitude"),"closed":u.get("closed"),"private":u.get("private")})
    p=os.path.join(tmp,"aihw-reporting-units.ndjson")
    with open(p,"w") as f:
        for r in rows: f.write(json.dumps(r)+"\n")
    return p,len(rows)

con=duckdb.connect()

def run_transform(spec):
    dep=spec.deps[0]
    # find file for dep
    fname=os.path.join(tmp,f"{dep}.ndjson")
    con.execute(f"CREATE OR REPLACE VIEW \"{dep}\" AS SELECT * FROM read_json_auto('{fname}')")
    res=con.execute(spec.sql).fetchall()
    cols=[d[0] for d in con.description]
    return len(res),cols

# map download id -> transform spec
tf={s.deps[0]:s for s in M.TRANSFORM_SPECS}

# CKAN
for rid in CKAN_RESOURCE_IDS:
    did=f"aihw-{rid}"
    p,n=fetch_ckan_ndjson(rid)
    try:
        rc,cols=run_transform(tf[did])
        print(f"OK  {did[:18]} raw={n} out={rc} ncols={len(cols)}")
    except Exception as e:
        print(f"ERR {did} -> {type(e).__name__}: {e}")
# reporting units
p,n=fetch_ru()
try:
    rc,cols=run_transform(tf["aihw-reporting-units"])
    print(f"OK  aihw-reporting-units raw={n} out={rc} cols={cols}")
except Exception as e:
    print(f"ERR aihw-reporting-units -> {type(e).__name__}: {e}")
