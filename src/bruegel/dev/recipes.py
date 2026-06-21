"""Test parsers for the 7 well-understood datasets end-to-end."""
import io, re, sys, os, zipfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import pandas as pd
import numpy as np

BASE = "https://www.bruegel.org"
FILE_RE = re.compile(r'href="((?:https?://[^"]+)?/(?:sites/default|system)/files/[^"]+\.(?:xlsx|xls|csv|zip))"', re.I)

def resolve(path):
    html = get(BASE + path, timeout=(10, 60)).text
    out = []
    for m in FILE_RE.finditer(html):
        u = m.group(1)
        if not u.startswith("http"): u = BASE + u
        if u not in out: out.append(u)
    return out

def dl(u): return get(u, timeout=(10, 180)).content

def _clean(v):
    if v is None: return None
    if isinstance(v, float) and (pd.isna(v) or np.isinf(v)): return None
    if isinstance(v, (np.floating,)): return float(v)
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, (pd.Timestamp,)): return v.date().isoformat()
    return v

def rows_from_df(df):
    return [{k: _clean(v) for k, v in r.items()} for r in df.to_dict("records")]

# ---- parsers ----
def parse_energy_crisis(links):
    data = dl([u for u in links if u.lower().endswith(".xlsx")][0])
    df = pd.read_excel(io.BytesIO(data), sheet_name="Measures", header=0)
    df = df.dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]
    return rows_from_df(df)

def parse_renewables(links):
    data = dl([u for u in links if u.lower().endswith(".xlsx")][0])
    df = pd.read_excel(io.BytesIO(data), sheet_name="Data", header=0)
    df = df.dropna(how="all")
    df["zone"] = df["zone"].astype(str).str.strip()
    return rows_from_df(df)

def parse_fms(links):
    data = dl([u for u in links if u.lower().endswith(".xlsx")][0])
    df = pd.read_excel(io.BytesIO(data), sheet_name="MAINDATA", header=0)
    df = df.dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]
    return rows_from_df(df)

def parse_gas_imports(links):
    z = zipfile.ZipFile(io.BytesIO(dl(links[0])))
    name = [n for n in z.namelist() if "daily_data" in n.lower() and n.lower().endswith(".csv")][0]
    df = pd.read_csv(io.BytesIO(z.read(name)))
    df = df.rename(columns={df.columns[0]: "date"})
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce").dt.date.astype(str)
    long = df.melt(id_vars=["date"], var_name="source", value_name="flow_gwh_d")
    long = long.dropna(subset=["flow_gwh_d"])
    return rows_from_df(long)

def parse_gini(links):
    z = zipfile.ZipFile(io.BytesIO(dl(links[0])))
    name = [n for n in z.namelist() if n.lower().endswith((".xls", ".xlsx"))][0]
    df = pd.read_excel(io.BytesIO(z.read(name)), sheet_name="Database", header=0)
    id_cols = ["Type", "Mean income", "Method", "Group", "Variable name"]
    year_cols = [c for c in df.columns if isinstance(c, (int, float)) or str(c).strip().isdigit()]
    long = df.melt(id_vars=id_cols, value_vars=year_cols, var_name="year", value_name="gini")
    long = long.dropna(subset=["gini"])
    long["year"] = long["year"].astype(float).astype(int)
    long = long.rename(columns={"Type": "income_type", "Mean income": "mean_income",
                                "Method": "method", "Group": "group", "Variable name": "variable_name"})
    return rows_from_df(long)

def parse_trade(links):
    data = dl([u for u in links if u.lower().endswith(".xlsx")][0])
    xl = pd.ExcelFile(io.BytesIO(data))
    out = []
    for sh in xl.sheet_names:
        if sh.strip().upper().startswith("READ"): continue
        parts = [p.strip() for p in sh.split(",")]
        commodity = parts[0] if parts else sh
        unit = parts[1] if len(parts) > 1 else None
        sa = parts[2] if len(parts) > 2 else None
        raw = xl.parse(sh, header=None)
        flow_row = raw.iloc[0].ffill()
        country_row = raw.iloc[1]
        body = raw.iloc[2:]
        for _, r in body.iterrows():
            dt = r.iloc[0]
            if pd.isna(dt): continue
            d = pd.Timestamp(dt).date().isoformat()
            for j in range(1, raw.shape[1]):
                val = r.iloc[j]
                if pd.isna(val): continue
                out.append({"date": d, "commodity": commodity, "unit": unit,
                            "seasonal_adj": sa, "flow": _clean(flow_row.iloc[j]),
                            "partner": _clean(country_row.iloc[j]), "value": _clean(val)})
    return out

def parse_reer(links):
    z = zipfile.ZipFile(io.BytesIO(dl(links[0])))
    name = [n for n in z.namelist() if n.lower().endswith((".xls", ".xlsx"))][0]
    xl = pd.ExcelFile(io.BytesIO(z.read(name)))
    out = []
    for sh in xl.sheet_names:
        m = re.match(r"(REER|NEER)_(MONTHLY|ANNUAL)_(\d+)$", sh.strip())
        if not m: continue
        measure, freq, cset = m.group(1), m.group(2).lower(), m.group(3)
        raw = xl.parse(sh, header=None)
        codes = raw.iloc[0]
        body = raw.iloc[1:]
        for _, r in body.iterrows():
            period = r.iloc[0]
            if pd.isna(period): continue
            period = str(period).strip()
            for j in range(1, raw.shape[1]):
                val = r.iloc[j]
                if pd.isna(val): continue
                code = str(codes.iloc[j]).strip()
                cc = code.split("_")[-1] if "_" in code else code
                out.append({"period": period, "measure": measure, "frequency": freq,
                            "country_set": cset, "country_code": cc, "value": _clean(val)})
    return out

REG = {
    "2026-european-energy-crisis-fiscal-response-tracker": ("/dataset/2026-european-energy-crisis-fiscal-response-tracker", parse_energy_crisis),
    "eu-renewables-value-tracker": ("/dataset/eu-renewables-value-tracker", parse_renewables),
    "us-foreign-military-sales": ("/dataset/us-foreign-military-sales", parse_fms),
    "european-natural-gas-imports": ("/dataset/european-natural-gas-imports", parse_gas_imports),
    "global-and-regional-gini-coefficients-income-inequality": ("/dataset/global-and-regional-gini-coefficients-income-inequality", parse_gini),
    "global-trade-tracker": ("/dataset/global-trade-tracker", parse_trade),
    "real-effective-exchange-rates-for-178-countries-a-new-database": ("/publications/datasets/real-effective-exchange-rates-for-178-countries-a-new-database", parse_reer),
}

only = sys.argv[1] if len(sys.argv) > 1 else None
for eid, (path, fn) in REG.items():
    if only and only not in eid: continue
    try:
        links = resolve(path)
        rows = fn(links)
        print(f"OK  {eid}: {len(rows)} rows")
        for r in rows[:2]:
            print("     ", {k: (str(v)[:30] if v is not None else None) for k, v in list(r.items())[:9]})
    except Exception as e:
        import traceback; traceback.print_exc()
        print(f"ERR {eid}: {type(e).__name__}: {e}")
