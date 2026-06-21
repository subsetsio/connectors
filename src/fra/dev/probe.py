import csv, io
from subsets_utils import get_client

def probe(view, n=2):
    url = f"https://data.transportation.gov/api/views/{view}/rows.csv?accessType=DOWNLOAD&bom=false"
    c = get_client()
    with c.stream("GET", url, timeout=120.0) as r:
        print(view, "status", r.status_code, "final_url", str(r.url))
        it = r.iter_lines()
        header = next(it)
        reader_header = next(csv.reader([header]))
        print("  ncols", len(reader_header))
        print("  header[:6]", reader_header[:6])
        cnt = 0
        for line in it:
            cnt += 1
            if cnt >= n:
                first_rows = line
                break
        print("  sample row 1st cell:", next(csv.reader([first_rows]))[:3])

probe("m8i6-zdsy")   # narrow 34 cols
probe("85tf-25kj")   # form54 157 cols
