import csv, io, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
from constants import ANON_API_KEY, CONFIG

BASE = "https://api.dataplatform.knmi.nl/open-data/v1"
KEY = os.environ.get("KNMI_API_KEY") or ANON_API_KEY

def aj(url, params=None):
    r = get(url, params=params, headers={"Authorization": KEY}, timeout=(10, 120)); r.raise_for_status(); return r.json()
def dl(name, ver, fn):
    u = aj(f"{BASE}/datasets/{name}/versions/{ver}/files/{fn}/url")["temporaryDownloadUrl"]
    r = get(u, timeout=(10, 120)); r.raise_for_status(); return r.content

def num(v):
    if v is None: return None
    s = str(v).strip().replace(",", ".")
    if s in ("", "-", ".", "NaN", "nan"): return None
    try: return float(s)
    except ValueError: return None

def parse_matrix(text, loc):
    rows=[]; periods=None
    for line in text.splitlines():
        line=line.strip()
        if not line or line.startswith("#"): continue
        cells=[c.strip() for c in line.split(",")]
        if cells[0].lower()=="metric": periods=cells[1:]; continue
        if periods is None: continue
        m=cells[0]
        if not m: continue
        for p,raw in zip(periods,cells[1:]): rows.append({"location":loc,"metric":m,"period":p,"value":num(raw)})
    return rows

# matrix sample
for eid in ["climate-normals-1991-2020-climate-normals-by-station-1","climate-normals-1991-2020-day-normals-by-station-1","climate-normals-1991-2020-precipitation-normals-by-district-1"]:
    c=CONFIG[eid]; files=[f["filename"] for f in aj(f"{BASE}/datasets/{c['name']}/versions/{c['version']}/files",{"maxKeys":1000})["files"] if f["filename"].startswith(c["prefix"]) and f["filename"].endswith(".csv")]
    fn=files[0]; loc=fn[:-4].split("_",1)[1]
    rows=parse_matrix(dl(c["name"],c["version"],fn).decode("utf-8-sig"),loc)
    nn=[r for r in rows if r["value"] is not None]
    print(f"\n[matrix] {eid}: {len(files)} files; sample {fn} -> {len(rows)} rows, {len(nn)} non-null; ex:",rows[:2])

# earthquakes
c=CONFIG["aardbevingen-cijfers-1"]; files=aj(f"{BASE}/datasets/{c['name']}/versions/{c['version']}/files",{"maxKeys":1000,"orderBy":"created","sorting":"desc"})["files"]
counts=[f["filename"] for f in files if f["filename"].startswith("aantal-aardbevingen-")]; latest=max(counts)
doc=json.loads(dl(c["name"],c["version"],latest));
erows=[{"year":int(y),"magnitude":num(m),"earthquake_count":int(ct)} for y,b in doc["data"].items() for m,ct in b.items() if m!="max"]
print(f"\n[earthquakes] latest={latest} -> {len(erows)} rows; ex:",erows[:3])

# ice
c=CONFIG["ice-thickness-observations-1-0"]; files=[f["filename"] for f in aj(f"{BASE}/datasets/{c['name']}/versions/{c['version']}/files",{"maxKeys":1000})["files"] if f["filename"].endswith(".csv")]
fn=files[0]; text=dl(c["name"],c["version"],fn).decode("utf-8-sig")
irows=[]
for r in csv.DictReader(io.StringIO(text)):
    r={(k or "").strip():v for k,v in r.items()}
    irows.append({"location":fn[:-4].split("_")[0],"water_depth_m":num(r.get("water_depth[m]")),"ice_depth_cm":num(r.get("ice_depth[cm]")),"date":r.get("date")})
print(f"\n[ice] {fn} -> {len(irows)} rows; ex:",irows[:2])

# homogenization
c=CONFIG["homogenization-daily-temperature-principal-stations-netherlands-1-0"]; files=[f["filename"] for f in aj(f"{BASE}/datasets/{c['name']}/versions/{c['version']}/files",{"maxKeys":1000})["files"] if f["filename"].endswith(".csv")]
fn=files[0]; text=dl(c["name"],c["version"],fn).decode("utf-8-sig"); parts=fn[:-4].split("-")
hrows=[{"station":parts[0],"variable":parts[1],"date":(r.get("date") or "").strip(),"original":num(r.get("original"))} for r in csv.DictReader(io.StringIO(text))]
print(f"\n[homog] {fn} station={parts[0]} var={parts[1]} -> {len(hrows)} rows; ex:",hrows[:2])

# stations
c=CONFIG["waarneemstations-csv-1-0"]; files=aj(f"{BASE}/datasets/{c['name']}/versions/{c['version']}/files",{"maxKeys":1,"orderBy":"lastModified","sorting":"desc"})["files"]
text=dl(c["name"],c["version"],files[0]["filename"]).decode("utf-8-sig")
srows=list(csv.DictReader(io.StringIO(text)))
print(f"\n[stations] {files[0]['filename']} -> {len(srows)} rows; cols:",list(srows[0].keys()) if srows else None)
