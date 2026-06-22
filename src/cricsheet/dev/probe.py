import io, zipfile, csv, collections
from subsets_utils import get

# Use a small competition zip to inspect structure (proxy for all_csv2.zip layout)
r = get("https://cricsheet.org/downloads/mlc_csv2.zip", timeout=(10,120))
r.raise_for_status()
z = zipfile.ZipFile(io.BytesIO(r.content))
names = z.namelist()
ball = [n for n in names if n.endswith(".csv") and not n.endswith("_info.csv")]
info = [n for n in names if n.endswith("_info.csv")]
print("members:", len(names), "ball:", len(ball), "info:", len(info), "non-csv:", [n for n in names if not n.endswith('.csv')])

# header stability across ball files
headers = set()
for n in ball:
    with z.open(n) as f:
        first = io.TextIOWrapper(f, encoding="utf-8").readline().strip()
        headers.add(first)
print("distinct ball headers:", len(headers))
print("header:", list(headers)[0])

# info key inventory: which keys appear, and multiplicity per match
key_counts = collections.Counter()
multi = collections.Counter()
sample_rows = None
for n in info:
    perfile = collections.Counter()
    with z.open(n) as f:
        rdr = csv.reader(io.TextIOWrapper(f, encoding="utf-8"))
        for row in rdr:
            if not row: continue
            if row[0] == "info" and len(row) >= 3:
                perfile[row[1]] += 1
    for k,c in perfile.items():
        key_counts[k]+=1
        if c>1: multi[k]+=1
print("\ninfo keys (appears in N of %d matches; multivalued in M):" % len(info))
for k,c in key_counts.most_common():
    print(f"  {k:24s} present={c:3d} multi={multi.get(k,0)}")
