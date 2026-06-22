import sys, os, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import pyarrow.csv as pacsv
# counter file via pyarrow
xurl = "https://cycling.data.tfl.gov.uk/CycleCounters/Blackfriars/July/Friday,%20Jul%2013%202018.xls"
b = get(xurl, timeout=(10,120)).content
try:
    t = pacsv.read_csv(io.BytesIO(b), read_options=pacsv.ReadOptions(block_size=1<<24),
                       parse_options=pacsv.ParseOptions(newlines_in_values=False))
    print("COUNTER cols:", len(t.column_names), "rows:", t.num_rows)
    print("first 16 names:", t.column_names[:16])
    print("CLASS distinct (sample):", set(t.column('CLASS').to_pylist()[:50]) if 'CLASS' in t.column_names else 'NO CLASS')
except Exception as e:
    print("COUNTER pyarrow err:", type(e).__name__, e)
