from subsets_utils import get
import io, pandas as pd

def content(bp):
    r = get(f"https://www.gov.uk/api/content/{bp}", timeout=(10,120)); r.raise_for_status(); return r.json()

# clean CSV open-data
d = content("government/statistical-data-sets/local-authority-housing-statistics-open-data")
for a in d["details"]["attachments"]:
    if a.get("content_type")=="text/csv":
        rb = get(a["url"], timeout=(10,180)); rb.raise_for_status()
        df = pd.read_csv(io.BytesIO(rb.content), nrows=5)
        print("CSV open-data shape sample:", df.shape, "cols:", list(df.columns)[:10]); print(df.head(3).to_string()[:600])
        break

# a messy homelessness xls
d = content("government/statistical-data-sets/live-tables-on-homelessness")
a = next(x for x in d["details"]["attachments"] if x.get("filename","").endswith(".xlsx"))
print("\n--- XLSX:", a["filename"])
rb = get(a["url"], timeout=(10,180)); rb.raise_for_status()
xl = pd.ExcelFile(io.BytesIO(rb.content))
print("sheets:", xl.sheet_names)
raw = xl.parse(xl.sheet_names[0], header=None, nrows=14)
print("raw top-left 14x6:")
print(raw.iloc[:14,:6].to_string())
