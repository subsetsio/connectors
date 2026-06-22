import io, zipfile, csv
from subsets_utils import get

for url in [
    "https://www150.statcan.gc.ca/n1/tbl/csv/34100097-eng.zip",  # housing starts SAAR
    "https://www150.statcan.gc.ca/n1/tbl/csv/34100133-eng.zip",  # average rents
]:
    print("="*90)
    print(url)
    r = get(url, timeout=(10,120))
    print("status", r.status_code, "bytes", len(r.content), "ctype", r.headers.get("content-type"))
    z = zipfile.ZipFile(io.BytesIO(r.content))
    print("names:", z.namelist())
    # the main data CSV is <pid>.csv ; there's also a _MetaData.csv
    main = [n for n in z.namelist() if not n.lower().endswith("metadata.csv")][0]
    with z.open(main) as f:
        text = io.TextIOWrapper(f, encoding="utf-8-sig")
        rdr = csv.reader(text)
        header = next(rdr)
        print("HEADER (%d cols):" % len(header), header)
        for i, row in enumerate(rdr):
            print("ROW:", row)
            if i >= 2: break
