from subsets_utils import get

URLS = {
    "daily-total": "https://www.sidc.be/SILSO/INFO/sndtotcsv.php",
    "monthly-total": "https://www.sidc.be/SILSO/INFO/snmtotcsv.php",
    "monthly-smoothed-total": "https://www.sidc.be/SILSO/INFO/snmstotcsv.php",
    "yearly-total": "https://www.sidc.be/SILSO/INFO/snytotcsv.php",
    "daily-hemispheric": "https://www.sidc.be/SILSO/INFO/sndhemcsv.php",
    "monthly-hemispheric": "https://www.sidc.be/SILSO/INFO/snmhemcsv.php",
    "monthly-smoothed-hemispheric": "https://www.sidc.be/SILSO/INFO/snmshemcsv.php",
}

for name, url in URLS.items():
    r = get(url, timeout=(10.0, 120.0))
    r.raise_for_status()
    lines = r.text.strip().splitlines()
    first = lines[0]
    last = lines[-1]
    sep = ";" if ";" in first else ","
    ncol = len(first.split(sep))
    print(f"=== {name} ({len(lines)} rows, sep={sep!r}, ncol={ncol}) ===")
    print("  FIRST:", repr(first))
    print("  LAST :", repr(last))
