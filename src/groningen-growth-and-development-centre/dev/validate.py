import sys; sys.path.insert(0,"src")
import io, openpyxl, pandas as pd
from subsets_utils import get

def read_sheet(content, sheet):
    wb=openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    ws=wb[sheet]
    rows=list(ws.iter_rows(values_only=True))
    hdr=list(rows[0])
    data=[r for r in rows[1:] if any(c is not None for c in r)]
    df=pd.DataFrame(data, columns=hdr)
    wb.close()
    return df

def dl(fid):
    r=get(f"https://dataverse.nl/api/access/datafile/{fid}", timeout=600); r.raise_for_status(); return r.content

# PWT 11.0 row count sanity + melt
c=dl(554105); df=read_sheet(c,"Data")
print("PWT11 Data shape:", df.shape, "| cols0-6:", list(df.columns[:7]))
idv=["countrycode","country","currency_unit","year"]
m=df.melt(id_vars=idv, var_name="variable", value_name="value")
m["value"]=pd.to_numeric(m["value"], errors="coerce"); m=m.dropna(subset=["value"])
print("PWT11 long rows:", len(m), "| distinct vars:", m['variable'].nunique())

# EU KLEMS output csv row count
import io as _io
c=dl(357147)
dfe=pd.read_csv(_io.BytesIO(c))
print("EUKLEMS output shape:", dfe.shape, "cols:", list(dfe.columns))
print("EUKLEMS years:", dfe['year'].min(), dfe['year'].max(), "vars:", dfe['var'].nunique())
