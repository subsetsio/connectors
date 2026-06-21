import io, csv
from subsets_utils import get

def head(url, nbytes=200000):
    r = get(url, timeout=(10,120))
    r.raise_for_status()
    return r

# small file: bas_cs
r = get("https://www.qogdata.pol.gu.se/data/qog_bas_cs_jan26.csv", timeout=(10,120))
r.raise_for_status()
text = r.content.decode("utf-8", "replace")
lines = text.splitlines()
print("bas_cs total lines:", len(lines))
reader = csv.reader(io.StringIO(text))
header = next(reader)
print("bas_cs ncols:", len(header))
print("first 15 cols:", header[:15])
row1 = next(reader)
print("row1 first 15:", row1[:15])
# check eqi_long header (different schema)
r2 = get("https://www.qogdata.pol.gu.se/data/qog_eqi_long_24.csv", timeout=(10,120))
r2.raise_for_status()
t2 = r2.content.decode("utf-8","replace")
h2 = next(csv.reader(io.StringIO(t2)))
print("eqi_long ncols:", len(h2), "cols:", h2[:20])
