from subsets_utils import get
import csv, io

url = "https://ssh.datastations.nl/api/access/datafile/183974?format=original"
r = get(url, timeout=(10,120))
print("status", r.status_code, "ctype", r.headers.get("content-type"), "len", len(r.content))
text = r.content.decode("utf-8", errors="replace")
# detect delimiter
first = text.splitlines()[0]
print("FIRST LINE:", repr(first[:300]))
delim = "\t" if "\t" in first else ","
rdr = csv.reader(io.StringIO(text), delimiter=delim)
rows = []
for i, row in enumerate(rdr):
    rows.append(row)
    if i >= 6: break
hdr = rows[0]
print("NCOLS", len(hdr))
print("HEADER", hdr)
for row in rows[1:]:
    print(row)
