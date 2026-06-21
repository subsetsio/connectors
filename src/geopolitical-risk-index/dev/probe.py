import io, re
import pandas as pd
from subsets_utils import get

def load(url):
    r = get(url, timeout=(10.0,120.0))
    r.raise_for_status()
    return pd.read_excel(io.BytesIO(r.content), sheet_name=0, engine="xlrd")

m = load("https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls")
print("monthly shape", m.shape)
meta = {"var_name","var_label"}
gc = [c for c in m.columns if c.startswith("GPRC_")]
ghc = [c for c in m.columns if c.startswith("GPRHC_")]
glob = [c for c in m.columns if c not in meta and not c.startswith("GPRC_") and not c.startswith("GPRHC_") and c!="month"]
print("global cols", len(glob), glob[:8])
print("countries", len(gc), [c[5:] for c in gc][:5])
print("month dtype", m["month"].dtype, m["month"].iloc[0], m["month"].iloc[-1])
print("GPR dtype", m["GPR"].dtype)
# reshape probe
iso = sorted({c[5:] for c in gc} | {c[6:] for c in ghc})
print("iso union", len(iso))
rec = m[["month"]+gc].melt(id_vars="month", var_name="country", value_name="gprc")
rec["country"]=rec["country"].str[5:]
print("recent melt", rec.shape, rec.dropna(subset=["gprc"]).shape)

d = load("https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.xls")
print("daily shape", d.shape, list(d.columns))
print("DAY", d["DAY"].dtype, d["DAY"].iloc[0], d["DAY"].iloc[-1])
print("event non-null", d["event"].notna().sum())
