import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils as su
from utils import install_ca, parse_census_excel
install_ca()

tests = {
  "PC01_A01_xls": "https://censusindia.gov.in/nada/index.php/catalog/20028/download/23160/PC01_A01.xls",
  "PC11_A01_xlsx": "https://censusindia.gov.in/nada/index.php/catalog/42526/download/46152/A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA.xlsx",
}
for name, url in tests.items():
    r = su.get(url, timeout=(10,120))
    print("===", name, r.status_code, r.headers.get("content-type"), len(r.content), "bytes")
    rows = parse_census_excel(r.content, url)
    print("  parsed rows:", len(rows))
    if rows:
        print("  cols:", list(rows[0].keys()))
        for row in rows[:3]:
            print("   ", row)
