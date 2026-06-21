import sys; sys.path.insert(0,'src')
from nodes import national_records_of_scotland as M
from subsets_utils import load_raw_parquet
for eid in ["household-type","infant-deaths","weekly-deaths"]:
    sid=f"national-records-of-scotland-{eid}"
    M.fetch_one(sid)
    t=load_raw_parquet(sid)
    print(f"{eid}: {t.num_rows} rows, cols={t.column_names}")
    print("   first:", {k:t.column(k)[0].as_py() for k in t.column_names})
