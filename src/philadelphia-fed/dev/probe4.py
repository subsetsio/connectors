import io, re, zipfile
import pandas as pd
from subsets_utils import get

BASE = "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data"

_CLEAN_CORE = (
    b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    b'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    b'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
    b'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    b'</cp:coreProperties>'
)


def sanitize_xlsx(content: bytes) -> bytes:
    """Rebuild the xlsx zip with a clean docProps/core.xml — SAS writes a malformed
    W3CDTF timestamp ('T 2:56' instead of 'T02:56') that openpyxl refuses to parse."""
    src = zipfile.ZipFile(io.BytesIO(content))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "docProps/core.xml":
                data = _CLEAN_CORE
            dst.writestr(item, data)
    return out.getvalue()


URLS = {
    "meanLevel": f"{BASE}/survey-of-professional-forecasters/historical-data/meanLevel.xlsx",
    "routput_fst": f"{BASE}/real-time-data/data-files/xlsx/routput_first_second_third.xlsx",
    "dispersion1": f"{BASE}/survey-of-professional-forecasters/historical-data/Dispersion_1.xlsx",
}

for name, url in URLS.items():
    print(f"\n{'='*70}\n{name}")
    content = sanitize_xlsx(get(url, timeout=120).content)
    xl = pd.ExcelFile(io.BytesIO(content), engine="openpyxl")
    print(f"  sheets({len(xl.sheet_names)}): {xl.sheet_names[:15]}")
    for sn in xl.sheet_names[:2]:
        df = pd.read_excel(xl, sheet_name=sn, nrows=8)
        print(f"  -- '{sn}' cols({len(df.columns)}): {list(df.columns)[:20]}")
        print(df.head(5).to_string()[:900])
