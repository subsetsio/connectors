import csv, io
from subsets_utils import get

def parse_anomaly(s):
    s = (s or "").strip()
    if not s or set(s) <= {"*"} or s == "-":
        return None
    return float(s)

txt = get("https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv", timeout=(10,120)).text
rows = list(csv.reader(io.StringIO(txt)))
hi = next(i for i,r in enumerate(rows) if r and r[0].strip()=="Year")
print("header_idx", hi, "header:", rows[hi])
last = [r for r in rows[hi+1:] if r and r[0].strip().isdigit()][-1]
print("last data row:", last)
hdr = [h.strip() for h in rows[hi]]
rec = dict(zip(hdr, last))
print("J-D=", rec["J-D"], "-> parsed", parse_anomaly(rec["J-D"]))
print("Jan=", rec["Jan"], "-> parsed", parse_anomaly(rec["Jan"]))
print("Dec=", rec["Dec"], "-> parsed", parse_anomaly(rec["Dec"]))

z = get("https://data.giss.nasa.gov/gistemp/tabledata_v4/ZonAnn.Ts+dSST.csv", timeout=(10,120)).text
zrows = list(csv.reader(io.StringIO(z)))
zhi = next(i for i,r in enumerate(zrows) if r and r[0].strip()=="Year")
print("zonal header:", zrows[zhi])
print("zonal last:", [r for r in zrows[zhi+1:] if r and r[0].strip().isdigit()][-1])
