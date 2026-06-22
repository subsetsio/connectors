import io, urllib.parse, pandas as pd, pyarrow as pa
from subsets_utils import get
BASE="https://www.systemicpeace.org/inscr/"
FILES={
 "coups-list":"CSPCoupsListv2021.xls",
 "pitf-adverse-regime-change":"PITF Adverse Regime Change 2018.xls",
 "pitf-revolutionary-war":"PITF Revolutionary War 2018.xls",
 "mepv-episodes":"MEPV2012ex.xls",
}
for eid,fn in FILES.items():
    r=get(BASE+urllib.parse.quote(fn),timeout=(10,120)); r.raise_for_status()
    df=pd.read_excel(io.BytesIO(r.content))
    # normalize column names
    df.columns=[str(c).strip() for c in df.columns]
    try:
        t=pa.Table.from_pandas(df, preserve_index=False)
        print(f"{eid}: pa.from_pandas OK rows={t.num_rows}")
        for f in t.schema:
            print("   ", f.name, f.type)
    except Exception as e:
        print(f"{eid}: pa.from_pandas FAIL {type(e).__name__}: {e}")
    print()
