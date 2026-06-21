import io
import pandas as pd
from subsets_utils import get

BASE = "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data"

FILES = {
    "spf_meanLevel": f"{BASE}/survey-of-professional-forecasters/historical-data/meanLevel.xlsx",
    "anxious": f"{BASE}/survey-of-professional-forecasters/anxious-index/anxious_index_chart.xlsx",
    "dispersion1": f"{BASE}/survey-of-professional-forecasters/historical-data/Dispersion_1.xlsx",
    "livingston_means": f"{BASE}/livingston-survey/historical-data/means.xlsx",
    "partisan": "https://www.philadelphiafed.org/-/media/FRBP/Assets/Data-Visualizations/partisan-conflict.xlsx",
    "mbos_dif_csv": f"{BASE}/MBOS/Historical-Data/Diffusion-Indexes/bos_dif.csv",
    "rtdsm_routput": f"{BASE}/real-time-data/data-files/xlsx/routput_first_second_third.xlsx",
}


def probe(name, url):
    print(f"\n{'='*70}\n{name}: {url}")
    r = get(url, timeout=120)
    r.raise_for_status()
    content = r.content
    print(f"  bytes={len(content):,} ctype={r.headers.get('content-type')}")
    if url.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content), nrows=8)
        print(f"  cols({len(df.columns)}): {list(df.columns)[:30]}")
        print(df.head(6).to_string()[:1200])
        return
    engine = "xlrd" if url.endswith(".xls") else "openpyxl"
    xl = pd.ExcelFile(io.BytesIO(content), engine=engine)
    print(f"  sheets({len(xl.sheet_names)}): {xl.sheet_names[:12]}")
    for sn in xl.sheet_names[:3]:
        try:
            df = pd.read_excel(xl, sheet_name=sn, nrows=8)
            print(f"  -- '{sn}' cols({len(df.columns)}): {list(df.columns)[:30]}")
            print(df.head(5).to_string()[:1000])
        except Exception as e:
            print(f"  -- '{sn}' read error {type(e).__name__}: {e}")


if __name__ == "__main__":
    for n, u in FILES.items():
        try:
            probe(n, u)
        except Exception as e:
            print(f"  ERROR {type(e).__name__}: {e}")
