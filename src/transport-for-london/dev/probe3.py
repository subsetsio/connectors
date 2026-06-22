import sys, os, io, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
xurl = "https://cycling.data.tfl.gov.uk/CycleCounters/Blackfriars/July/Friday,%20Jul%2013%202018.xls"
r = get(xurl, timeout=(10,120)); r.raise_for_status()
txt = r.content.decode("utf-8","replace")
print("first 400 chars:\n", repr(txt[:400]))
# guess delimiter
first = txt.splitlines()[0]
for d in ['\t',',',';','|']:
    print(f"delim {d!r}: {len(first.split(d))} cols")
print("\n--- as TSV ---")
rows = list(csv.reader(io.StringIO(txt), delimiter='\t'))
print("nrows:", len(rows))
for r_ in rows[:4]:
    print(r_)
