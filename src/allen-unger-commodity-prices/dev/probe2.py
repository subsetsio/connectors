from subsets_utils import get
import csv, io, re
from collections import Counter

# ingested .tab (default, tab-separated)
url = "https://ssh.datastations.nl/api/access/datafile/183974"
r = get(url, timeout=(10,180))
raw = r.content
print("ingested ctype", r.headers.get("content-type"), "len", len(raw))
# try decodings on a sample byte slice that had the accented name
for enc in ("utf-8","latin-1","cp1252"):
    try:
        t = raw.decode(enc)
        print(enc, "OK; sample:", repr(t[400:520]))
    except Exception as e:
        print(enc, "FAIL", e)

text = raw.decode("utf-8", errors="replace")
rdr = csv.reader(io.StringIO(text), delimiter="\t")
hdr = next(rdr)
idx = {c:i for i,c in enumerate(hdr)}
n=0
years_nonint=Counter(); val_orig_bad=0; val_std_bad=0; year_min=9999; year_max=0
commodities=set(); markets=set()
empties=Counter()
for row in rdr:
    if len(row)!=len(hdr): 
        empties['ragged']+=1; continue
    n+=1
    y=row[idx['Item_Years']].strip()
    if not re.fullmatch(r'-?\d+', y):
        years_nonint[y]+=1
    else:
        yi=int(y); year_min=min(year_min,yi); year_max=max(year_max,yi)
    vo=row[idx['Item_Value_Original']].strip()
    vs=row[idx['Item_Value_Standardized']].strip()
    if vo and not re.fullmatch(r'-?\d+(\.\d+)?([eE]-?\d+)?', vo): val_orig_bad+=1
    if vs and not re.fullmatch(r'-?\d+(\.\d+)?([eE]-?\d+)?', vs): val_std_bad+=1
    if not vo: empties['val_orig_empty']+=1
    if not vs: empties['val_std_empty']+=1
    commodities.add(row[idx['Commodity']]); markets.add(row[idx['Market']])
print("rows", n)
print("year range", year_min, year_max)
print("commodities", len(commodities), "markets", len(markets))
print("val_orig_nonnumeric", val_orig_bad, "val_std_nonnumeric", val_std_bad)
print("empties", dict(empties))
print("years_nonint top", years_nonint.most_common(10), "distinct nonint", len(years_nonint))
