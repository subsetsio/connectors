from subsets_utils import get
import io, csv

def show(name, url, n=6):
    r = get(url, timeout=(10,120))
    print(f"\n===== {name} ({r.status_code}) {url}")
    text = r.content.decode('utf-8-sig', 'replace')
    for i,line in enumerate(text.splitlines()[:n]):
        print(repr(line[:300]))

ID="OGD_krebs_ext_KREBS_1"
B="https://data.statistik.gv.at/data"
show("MAIN", f"{B}/{ID}.csv")
show("HEADER", f"{B}/{ID}_HEADER.csv")
show("CODELIST C-BUNDESLAND", f"{B}/{ID}_C-BUNDESLAND-0.csv")
# a non-coded one
ID2="OGDEXT_AEST_GEMTAB_1"
show("MAIN AEST (plain headers)", f"{B}/{ID2}.csv")
show("HEADER AEST", f"{B}/{ID2}_HEADER.csv")
# one with decimal values - VPI consumer price
ID3="OGD_vpi15_VPIZR_1"
show("MAIN VPI (decimals?)", f"{B}/{ID3}.csv")
