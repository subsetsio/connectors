import csv, io, re
from subsets_utils import get

URL = "https://www.ghsindex.org/wp-content/uploads/2022/04/2021-GHS-Index-April-2022.csv"
resp = get(URL, timeout=(10.0, 120.0))
resp.raise_for_status()
text = resp.content.decode("utf-8-sig")  # strip BOM
reader = csv.reader(io.StringIO(text))
header = next(reader)
rows = list(reader)
print("n cols:", len(header))
print("n data rows:", len(rows))
print("first 8 headers:", header[:8])
print("Country/Year cols:", header[0], "|", header[1], "|", header[2])

def parse_code(h):
    if h.strip().upper() == "OVERALL SCORE":
        return "OVERALL", "Overall score"
    if ")" in h:
        code, label = h.split(")", 1)
        return code.strip(), label.strip()
    return h.strip(), h.strip()

# show code parsing on a sample
for h in [header[2], header[3], header[4], header[6], header[-1]]:
    print(parse_code(h), "  <=", h[:60])

years = set(r[1] for r in rows)
countries = set(r[0] for r in rows)
print("years:", sorted(years))
print("n countries:", len(countries))

# value sampling: blanks?
blanks = 0; nonnum = 0; total = 0
for r in rows:
    for v in r[2:]:
        total += 1
        if v.strip() == "":
            blanks += 1
        else:
            try: float(v)
            except: nonnum += 1
print(f"value cells total={total} blanks={blanks} nonnumeric={nonnum}")
# show some nonnumeric examples
ex = []
for r in rows:
    for i,v in enumerate(r[2:], start=2):
        if v.strip() and not _is_num(v) if (_is_num:=lambda x: __import__('re').match(r'^-?\d+(\.\d+)?$', x.strip())) else False:
            pass
