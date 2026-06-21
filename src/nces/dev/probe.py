import io, zipfile, csv
from subsets_utils import get

def look(table):
    url=f"https://nces.ed.gov/ipeds/datacenter/data/{table}.zip"
    r=get(url, timeout=(10,120))
    print(f"\n== {table}  HTTP {r.status_code}  zip {len(r.content)} bytes")
    if r.status_code!=200: return
    z=zipfile.ZipFile(io.BytesIO(r.content))
    names=z.namelist(); print("  members:", names)
    # pick the csv (skip _rv revised? there may be two)
    csvname=[n for n in names if n.lower().endswith('.csv')][0]
    raw=z.read(csvname)
    text=raw.decode('latin-1')
    rdr=csv.reader(io.StringIO(text))
    header=next(rdr)
    nrows=sum(1 for _ in rdr)
    print(f"  csv={csvname} cols={len(header)} rows={nrows}")
    print("  header[:25]:", header[:25])

for t in ["HD2022","EFFY2022","EF2022A","C2022_A","SAL2022_IS","F2122_F1A","GR2022","SFA2122","DRVEF2022"]:
    try: look(t)
    except Exception as e: print(t,"ERR",type(e).__name__,e)
