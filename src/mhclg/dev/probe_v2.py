import sys, os, time, resource
sys.path.insert(0, os.path.abspath("src"))
from subsets_utils import get
from nodes.mhclg import _rows_for, _get_json, CONTENT_API

def content(bp): return _get_json(CONTENT_API+bp)

def test(bp, fname):
    d=content(bp)
    a=next(x for x in d["details"]["attachments"] if x.get("filename")==fname)
    raw=get(a["url"], timeout=(10,300)).content
    t0=time.time(); n=0; sample=None
    for sheet,ri,cells in _rows_for(a["content_type"], raw):
        n+=1
        if sample is None: sample=(sheet,ri,cells[:6])
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6
    print(f"{fname:<42} {len(raw)/1e6:6.1f}MB rows={n:>8} {time.time()-t0:6.1f}s peakRSS={peak:7.0f}MB")
    print("   sample:", sample)

test("government/statistical-data-sets/fire-statistics-data-tables","dwelling-fires-dataset.ods")
test("government/statistical-data-sets/fire-statistics-data-tables","FIRE1204.xlsx")
test("government/statistical-data-sets/live-tables-on-planning-application-statistics","PS2_data_-_open_data_table__202603_.csv")
