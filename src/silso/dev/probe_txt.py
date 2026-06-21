from subsets_utils import get
URLS = {
    "daily-total": "https://www.sidc.be/SILSO/DATA/SN_d_tot_V2.0.txt",
    "monthly-total": "https://www.sidc.be/SILSO/DATA/SN_m_tot_V2.0.txt",
    "monthly-smoothed-total": "https://www.sidc.be/SILSO/DATA/SN_ms_tot_V2.0.txt",
    "yearly-total": "https://www.sidc.be/SILSO/DATA/SN_y_tot_V2.0.txt",
    "daily-hemispheric": "https://www.sidc.be/SILSO/DATA/SN_d_hem_V2.0.txt",
    "monthly-hemispheric": "https://www.sidc.be/SILSO/DATA/SN_m_hem_V2.0.txt",
    "monthly-smoothed-hemispheric": "https://www.sidc.be/SILSO/DATA/SN_ms_hem_V2.0.txt",
}
for name, url in URLS.items():
    try:
        r = get(url, timeout=(30.0, 180.0)); r.raise_for_status()
        lines = r.text.strip().splitlines()
        ncol = len(lines[0].split())
        print(f"=== {name} ({len(lines)} rows, whitespace ncol={ncol}) ===")
        print("  FIRST:", repr(lines[0]))
        print("  LAST :", repr(lines[-1]))
    except Exception as e:
        print(f"=== {name} ERROR {type(e).__name__}: {e}")
