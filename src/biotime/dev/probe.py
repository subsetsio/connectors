import io, zipfile, csv
from subsets_utils import get

# Metadata CSV (small)
r = get("https://zenodo.org/api/records/5026943/files/BioTIMEMetadata_24_06_2021.csv/content", timeout=(10, 120))
print("META status", r.status_code, "bytes", len(r.content))
reader = csv.reader(io.StringIO(r.content.decode("utf-8", "replace")))
mhead = next(reader)
print("META cols", len(mhead), mhead)
mrows = list(reader)
print("META nrows", len(mrows))
print("META row0", mrows[0][:6])

# Query zip — stream just the header + a couple rows
rz = get("https://zenodo.org/api/records/5026943/files/BioTIMEQuery_24_06_2021.zip/content", timeout=(10, 300))
print("QUERY zip status", rz.status_code, "bytes", len(rz.content))
zf = zipfile.ZipFile(io.BytesIO(rz.content))
print("zip members", zf.namelist())
member = zf.namelist()[0]
with zf.open(member) as fh:
    txt = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
    qr = csv.reader(txt)
    qhead = next(qr)
    print("QUERY cols", len(qhead), qhead)
    for i, row in enumerate(qr):
        if i >= 3: break
        print("QUERY row", i, row)
