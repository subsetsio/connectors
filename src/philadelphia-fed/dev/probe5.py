import io, zipfile
import pandas as pd
from subsets_utils import get

BASE = "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data"
_CLEAN = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          b'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
          b'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
          b'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"></cp:coreProperties>')

def san(c):
    src = zipfile.ZipFile(io.BytesIO(c)); out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as d:
        for it in src.infolist():
            d.writestr(it, _CLEAN if it.filename == "docProps/core.xml" else src.read(it.filename))
    return out.getvalue()

# dispersion: raw rows of NGDP sheet with no header
print("=== Dispersion_1 NGDP raw (header=None) ===")
c = san(get(f"{BASE}/survey-of-professional-forecasters/historical-data/Dispersion_1.xlsx", timeout=120).content)
df = pd.read_excel(io.BytesIO(c), sheet_name="NGDP", header=None, nrows=16, engine="openpyxl")
print(df.to_string()[:1600])

print("\n=== routput DATA raw (header=None) ===")
c = san(get(f"{BASE}/real-time-data/data-files/xlsx/routput_first_second_third.xlsx", timeout=120).content)
df = pd.read_excel(io.BytesIO(c), sheet_name="DATA", header=None, nrows=8, engine="openpyxl")
print(df.to_string()[:900])
nt = pd.read_excel(io.BytesIO(c), sheet_name="NOTES", header=None, nrows=4, engine="openpyxl")
print("NOTES:", nt.to_string()[:400])

print("\n=== anxious Data raw (header=None) ===")
c = get(f"{BASE}/survey-of-professional-forecasters/anxious-index/anxious_index_chart.xlsx", timeout=120).content
df = pd.read_excel(io.BytesIO(c), sheet_name="Data", header=None, nrows=8, engine="openpyxl")
print(df.to_string()[:700])

print("\n=== meanGrowth sheets ===")
c = san(get(f"{BASE}/survey-of-professional-forecasters/historical-data/meanGrowth.xlsx", timeout=120).content)
xl = pd.ExcelFile(io.BytesIO(c), engine="openpyxl")
print("n sheets:", len(xl.sheet_names), xl.sheet_names[:6])
print(pd.read_excel(xl, sheet_name=xl.sheet_names[0], nrows=3).to_string()[:500])
