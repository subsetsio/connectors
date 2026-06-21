import io, csv, json, re, zipfile
import pyarrow as pa

FOG="/tmp/wgms_probe/fog.zip"
AMCE="/tmp/wgms_probe/amce.zip"

# FoG streaming to all-string record batches (logic mirror)
zf=zipfile.ZipFile(FOG)
with zf.open("data/glacier.csv") as fh:
    text=io.TextIOWrapper(fh,encoding="utf-8",newline="")
    r=csv.reader(text); header=next(r); ncol=len(header)
    schema=pa.schema([(c,pa.string()) for c in header])
    rows=[next(r) for _ in range(3)]
    cols=[[None]*len(rows) for _ in range(ncol)]
    for ri,row in enumerate(rows):
        for ci in range(ncol):
            if ci<len(row): cols[ci][ri]=row[ci] if row[ci]!="" else None
    batch=pa.RecordBatch.from_arrays([pa.array(c,type=pa.string()) for c in cols],schema=schema)
    print("FoG glacier cols:",header[:5],"... n=",ncol,"batch rows:",batch.num_rows)

# AMCE region unpivot mirror
zf2=zipfile.ZipFile(AMCE)
regions=sorted(m.group(1) for n in zf2.namelist() if (m:=re.fullmatch(r"glacier/([A-Za-z0-9]+)_mwe\.csv",n)))
print("AMCE regions:",len(regions),regions)
# one region glacier unpivot sample
R=regions[0]
meta={}
for rec in csv.DictReader(io.TextIOWrapper(zf2.open(f"glacier/{R}_metadata.csv"),encoding="utf-8",newline="")):
    meta[rec["outline_id"]]=rec
rd=csv.reader(io.TextIOWrapper(zf2.open(f"glacier/{R}_mwe.csv"),encoding="utf-8",newline=""))
h=next(rd); years=h[1:]
row=next(rd)
out=[]
for yi,year in enumerate(years,start=1):
    if yi>=len(row): break
    if row[yi]=="" : continue
    m=meta.get(row[0],{})
    out.append({"region":R,"outline_id":row[0],"glacier_id":m.get("glacier_id"),"year":year,"mwe":row[yi]})
print("region",R,"sample long rows:",len(out),"first:",out[0] if out else None)

# region csv unpivot
region_files=sorted(n for n in zf2.namelist() if re.fullmatch(r"region/[A-Za-z0-9]+\.csv",n))
print("region files:",len(region_files))
rec=next(csv.DictReader(io.TextIOWrapper(zf2.open(region_files[0]),encoding="utf-8",newline="")))
print("region row sample:",rec)
