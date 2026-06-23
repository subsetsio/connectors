import io, csv
from collections import defaultdict
from subsets_utils import get

URL = "https://media.githubusercontent.com/media/stvno/stvno.github.io/master/page/cliwoc/CLIWOC21.tsv"

# Stream just enough lines to understand shape without pulling all 167MB.
resp = get(URL, timeout=(10.0, 300.0))
resp.raise_for_status()
text = resp.text
print("total bytes:", len(resp.content))

reader = csv.reader(io.StringIO(text), delimiter="\t")
header = next(reader)
print("num columns:", len(header))

rows = []
for i, r in enumerate(reader):
    rows.append(r)
    if i >= 50000:
        break
print("sampled rows:", len(rows))

# non-empty fraction per column
nonempty = defaultdict(int)
samples = defaultdict(list)
for r in rows:
    for j, col in enumerate(header):
        v = r[j].strip() if j < len(r) else ""
        if v:
            nonempty[col] += 1
            if len(samples[col]) < 4:
                samples[col].append(v)

n = len(rows)
print("\n=== columns of interest (populated %) ===")
interest = ["YR","MO","DY","HR","LAT","LON","latitude","longitude","SLP","AT","SST","WD","WP","WW","W",
            "Year","Month","Day","ShipName","Nationality","ShipType","Company","VoyageFrom","VoyageTo",
            "LogbookIdent","LogbookLanguage","DASnumber","Weather","AllWindDirections","AllWindForces",
            "PrecipitationDescriptor","ZeroMeridian","Calendar","Release","InstName","ArchivePart"]
for c in interest:
    if c in header:
        print(f"{c:22} {100*nonempty[c]//n:3d}%  {samples[c][:3]}")
    else:
        print(f"{c:22} NOT IN HEADER")
