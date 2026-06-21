import pandas as pd, datetime

PATH = "dev/russian.xlsx"
# Standard-layout Figure sheets: header row where col0 == 'direction of trade'
STD_SHEETS = ["Figure 1","Figure 2","Figure 3","Figure 4","Figure 5","Figure 8&9","Figure 10"]

def parse_sheet(xls, sheet):
    raw = pd.read_excel(xls, sheet_name=sheet, header=None)
    # find header row
    hdr = None
    for i in range(min(10, len(raw))):
        if str(raw.iloc[i,0]).strip().lower() == "direction of trade":
            hdr = i; break
    if hdr is None:
        return pd.DataFrame()
    header = raw.iloc[hdr].tolist()
    # dim columns = leading cells that are non-date text; date columns = datetime cells
    date_cols, dim_cols = [], []
    for ci, h in enumerate(header):
        if isinstance(h, (datetime.datetime, pd.Timestamp)):
            date_cols.append(ci)
        elif pd.notna(h) and not date_cols:  # text dim before first date
            dim_cols.append(ci)
    dim_names = [str(header[ci]).strip() for ci in dim_cols]
    body = raw.iloc[hdr+1:].copy()
    # drop fully-empty rows (separators) -> require col0 non-empty
    body = body[body.iloc[:,0].notna() & (body.iloc[:,0].astype(str).str.strip()!="")]
    records = []
    for _, row in body.iterrows():
        # stop if we hit another 'Source:'/'Figure' title block
        if str(row.iloc[0]).strip().lower().startswith(("source:","figure")):
            continue
        dims = {dim_names[k]: row.iloc[dim_cols[k]] for k in range(len(dim_cols))}
        for dc in date_cols:
            val = row.iloc[dc]
            if pd.isna(val): continue
            try: v = float(val)
            except (ValueError, TypeError): continue
            d = header[dc]
            records.append({
                "figure": sheet,
                "date": pd.Timestamp(d).date().isoformat(),
                "direction_of_trade": dims.get("direction of trade"),
                "country": dims.get("country"),
                "unit": dims.get("unit"),
                "sitc_code": dims.get("SITC 1-digit code") or dims.get("SITC 2-digit code"),
                "sitc_category": dims.get("SITC category description"),
                "value": v,
            })
    return pd.DataFrame(records)

xls = pd.ExcelFile(PATH, engine="openpyxl")
frames = [parse_sheet(xls, s) for s in STD_SHEETS]
out = pd.concat(frames, ignore_index=True)
print("dim columns seen per sheet:")
for s in STD_SHEETS:
    raw = pd.read_excel(xls, sheet_name=s, header=None)
    for i in range(10):
        if str(raw.iloc[i,0]).strip().lower()=="direction of trade":
            hdr=raw.iloc[i].tolist()
            dims=[str(h) for h in hdr if pd.notna(h) and not isinstance(h,(datetime.datetime,pd.Timestamp))]
            print(f"  {s}: {dims}")
            break
print("\nTOTAL ROWS:", len(out))
print("rows per figure:\n", out.groupby("figure").size())
print("\ndate range:", out.date.min(), "->", out.date.max())
print("\nSAMPLE:")
print(out.head(5).to_string())
print("nulls in sitc_code:", out.sitc_code.isna().sum())
