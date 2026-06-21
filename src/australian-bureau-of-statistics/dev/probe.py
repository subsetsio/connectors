import io
import csv
from subsets_utils import get

# Probe a small dataflow's SDMX-CSV. Use a smaller flow than CPI.
url = "https://data.api.abs.gov.au/rest/data/ABORIGINAL_POP_PROJ/all"
resp = get(url, params={"format": "csv"}, timeout=(10.0, 120.0))
print("status", resp.status_code)
print("content-type", resp.headers.get("content-type"))
text = resp.text
print("len bytes", len(text))
lines = text.splitlines()
print("num lines", len(lines))
print("HEADER:", lines[0])
for l in lines[1:6]:
    print("ROW:", l)

# parse columns
reader = csv.DictReader(io.StringIO(text))
print("FIELDS:", reader.fieldnames)
first = next(reader)
print("FIRST DICT:", first)
