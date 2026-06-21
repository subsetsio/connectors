import pandas as pd, re

# ============ DIVISIA ============
print("########## DIVISIA ##########")
DPATH = "dev/divisia_extract/Divisia_database_ver12Jun2026.xls"
raw = pd.read_excel(DPATH, engine="xlrd", sheet_name="Data", header=None)
cat   = raw.iloc[1].ffill()      # merged category headers (row 1)
subcat= raw.iloc[2].ffill()      # merged subcategory text  (row 2)
codes = raw.iloc[3]              # unique series codes       (row 3)
data  = raw.iloc[4:].reset_index(drop=True)

def parse_divisia_date(s):
    m = re.match(r"^(\d{4})M(\d{2})$", str(s).strip())
    if not m: return None
    return f"{m.group(1)}-{m.group(2)}-01"

recs = []
for _, row in data.iterrows():
    d = parse_divisia_date(row.iloc[0])
    if d is None: continue
    for ci in range(1, raw.shape[1]):
        code = codes.iloc[ci]
        if pd.isna(code): continue
        val = row.iloc[ci]
        if pd.isna(val): continue
        recs.append({
            "date": d,
            "series_name": str(code).strip(),
            "category": None if pd.isna(cat.iloc[ci]) else str(cat.iloc[ci]).strip(),
            "subcategory": None if pd.isna(subcat.iloc[ci]) else str(subcat.iloc[ci]).strip(),
            "value": float(val),
        })
div = pd.DataFrame(recs)
print("TOTAL ROWS:", len(div))
print("n series:", div.series_name.nunique(), "| date range:", div.date.min(),"->",div.date.max())
print(div.head(5).to_string())

# ============ SOVEREIGN ============
print("\n########## SOVEREIGN ##########")
SPATH = "dev/sovereign.xlsx"

def parse_cross(sheet, freq):
    raw = pd.read_excel(SPATH, engine="openpyxl", sheet_name=sheet, header=None)
    countries = raw.iloc[1].ffill()     # row1 country (merged across pairs)
    holders   = raw.iloc[2]             # row2 holder type, col0='Date'
    body = raw.iloc[3:]
    recs=[]
    for _, row in body.iterrows():
        dval = row.iloc[0]
        # data row only if col0 is a date or year (skip footnote text rows)
        if isinstance(dval, str): continue
        if pd.isna(dval): continue
        if freq=="quarterly":
            ts = pd.Timestamp(dval); date = ts.date().isoformat()
        else:
            date = f"{int(dval)}-01-01"
        for ci in range(1, raw.shape[1]):
            ctry = countries.iloc[ci]; hold = holders.iloc[ci]
            if pd.isna(ctry) or pd.isna(hold): continue
            val = row.iloc[ci]
            if pd.isna(val): continue
            holder_type = re.sub(r"\*+$","",str(hold).strip()).strip()  # strip trailing asterisks
            recs.append({
                "date": date, "country": str(ctry).strip(),
                "holder_type": holder_type, "value": float(val),
                "frequency": freq})
    return pd.DataFrame(recs)

q = parse_cross("cross countries QUARTERLY","quarterly")
a = parse_cross("cross countries ANNUAL","annual")
sov = pd.concat([q,a], ignore_index=True)
print("QUARTERLY rows:", len(q), "| ANNUAL rows:", len(a), "| TOTAL:", len(sov))
print("countries (Q):", sorted(q.country.unique()))
print("holder_types:", sorted(sov.holder_type.unique()))
print("Q date range:", q.date.min(),"->",q.date.max(),"| A:", a.date.min(),"->",a.date.max())
print(sov.head(5).to_string())
