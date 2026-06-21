"""Probe Philadelphia Fed Excel files: sheet names, columns, dtypes, head rows."""
import io
import pandas as pd
from subsets_utils import get

BASE = "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data"

FILES = {
    "ads": f"{BASE}/ads/ADS_Index_Most_Current_Vintage.xlsx",
    "spf_meanLevel": f"{BASE}/survey-of-professional-forecasters/historical-data/meanLevel.xlsx",
    "spf_dispersion": f"{BASE}/survey-of-professional-forecasters/historical-data/dispersion.xlsx",
    "anxious": f"{BASE}/anxious-index/anxious_index_chart.xlsx",
    "mbos": f"{BASE}/MBOS/historical-data/diffusion-indexes-historical.xlsx",
    "nbos": f"{BASE}/NBOS/nboshistory.xlsx",
    "gdpplus": f"{BASE}/gdpplus/GDPplus_Vintages.xlsx",
    "atsix": f"{BASE}/atsix/ATSIX_Vintages.xlsx",
    "coincident": f"{BASE}/coincident/coincident-revised.xls",
    "livingston": f"{BASE}/livingston-survey/historical-data/Mean_Forecasts.xlsx",
    "partisan": f"{BASE}/partisan-conflict/partisan_conflict_index.xlsx",
}


def probe(name, url):
    print(f"\n{'='*70}\n{name}: {url}")
    try:
        r = get(url, timeout=120)
        r.raise_for_status()
        content = r.content
        print(f"  bytes={len(content):,}  ctype={r.headers.get('content-type')}")
        engine = "xlrd" if url.endswith(".xls") else "openpyxl"
        xl = pd.ExcelFile(io.BytesIO(content), engine=engine)
        print(f"  sheets ({len(xl.sheet_names)}): {xl.sheet_names[:20]}")
        for sn in xl.sheet_names[:3]:
            df = pd.read_excel(xl, sheet_name=sn, nrows=8)
            print(f"  --- sheet '{sn}' shape(head)={df.shape}")
            print(f"      cols: {list(df.columns)[:25]}")
            print(df.head(6).to_string()[:1500])
    except Exception as e:
        print(f"  ERROR {type(e).__name__}: {e}")


if __name__ == "__main__":
    import sys
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for name, url in FILES.items():
        if only and only != name:
            continue
        probe(name, url)
