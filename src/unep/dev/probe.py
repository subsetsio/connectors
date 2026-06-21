import io, csv
from subsets_utils import get

urls = {
    "national": "https://storage.googleapis.com/global-surface-water-stats/gaul0-all-2018.csv",
    "adm1": "https://storage.googleapis.com/global-surface-water-stats/gaul1-all-2018.csv",
    "basins3": "https://storage.googleapis.com/global-surface-water-stats/hydrobasins3-all-2018.csv",
}
for name, url in urls.items():
    r = get(url, timeout=(10,120))
    print("==", name, r.status_code, "len", len(r.content))
    text = r.text
    lines = text.splitlines()
    print("header:", lines[0])
    for ln in lines[1:4]:
        print("  ", ln)
    print("nrows approx:", len(lines)-1)
