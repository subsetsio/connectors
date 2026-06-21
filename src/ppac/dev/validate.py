import sys, types
import subsets_utils as su
CAP={}
def fake_save(table, asset):
    CAP[asset]=table; return f"/fake/{asset}.parquet"
su.save_raw_parquet=fake_save
# also patch the name imported into the node module after import
import importlib
sys.path.insert(0,"src")
mod=importlib.import_module("nodes.ppac")
mod.save_raw_parquet=fake_save

print("DOWNLOAD_SPECS:",len(mod.DOWNLOAD_SPECS),"TRANSFORM_SPECS:",len(mod.TRANSFORM_SPECS))
ids=[s.id for s in mod.DOWNLOAD_SPECS]
print("ids ok:", all(i.startswith("ppac-") for i in ids))
# run each fetch
import traceback
for s in mod.DOWNLOAD_SPECS:
    try:
        s.fn(s.id)
        t=CAP.get(s.id)
        cols=t.column_names if t is not None else None
        print(f"  OK   {s.id:52s} rows={len(t) if t is not None else 'NONE':>6} cols={cols}")
    except Exception as e:
        print(f"  FAIL {s.id:52s} {type(e).__name__}: {e}")
        traceback.print_exc()

print("\n==== TRANSFORM CHECK (duckdb) ====")
import duckdb
con=duckdb.connect()
tmap={t.id:t for t in mod.TRANSFORM_SPECS}
for s in mod.DOWNLOAD_SPECS:
    t=CAP.get(s.id)
    if t is None: continue
    con.register(s.id, t.to_pandas())
    sql=tmap[f"{s.id}-transform"].sql
    try:
        out=con.execute(sql).fetch_df()
        nnull=out.isnull().mean().round(2).to_dict()
        print(f"  {s.id:50s} -> {len(out):>5} rows, cols={list(out.columns)}")
        print(f"       null_frac={nnull}")
    except Exception as e:
        print(f"  {s.id:50s} TRANSFORM FAIL {type(e).__name__}: {e}")

print("\n==== SPOT CHECKS ====")
ic=CAP["ppac-prices/international-prices-of-crude-oil"].to_pandas()
print("intl crude items:", sorted(ic['item'].unique()), "| periods:", sorted(ic['period'].unique()))
sn=CAP["ppac-consumption/active-domestic-customers"].to_pandas()
print("active-domestic as_of sample:", sn['as_of'].unique()[:3], "| states:", len(sn))
gp=CAP["ppac-natural-gas/production"].to_pandas()
print("gas-prod sections:", sorted(gp['section'].unique())[:8])
ie=CAP["ppac-import-export"].to_pandas()
print("import-export sections:", sorted(ie['section'].unique()))
