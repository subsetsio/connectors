import sys, os, io, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import pandas as pd

# 1) a quarterly active-travel count CSV
url = "https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/2015%20Q2%20spring%20(Apr-Jun)-Central.csv"
r = get(url, timeout=(10,120)); r.raise_for_status()
txt = r.content.decode("utf-8","replace")
rows = list(csv.reader(io.StringIO(txt)))
print("ATC CSV rows:", len(rows))
print("ATC header:", rows[0])
print("ATC row1:", rows[1] if len(rows)>1 else None)
print("ATC row2:", rows[2] if len(rows)>2 else None)

# 2) a cycle-counter xls
xurl = "https://cycling.data.tfl.gov.uk/CycleCounters/Blackfriars/July/Friday,%20Jul%2013%202018.xls"
r2 = get(xurl, timeout=(10,120)); r2.raise_for_status()
print("\nXLS bytes:", len(r2.content), "head:", r2.content[:8])
try:
    xl = pd.ExcelFile(io.BytesIO(r2.content))
    print("XLS sheets:", xl.sheet_names)
    df = xl.parse(xl.sheet_names[0], header=None, nrows=12)
    print(df.to_string())
except Exception as e:
    print("XLS parse err:", type(e).__name__, e)
