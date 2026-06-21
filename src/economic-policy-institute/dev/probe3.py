from subsets_utils import get
import io, zipfile, csv

url = "https://github.com/Economic/data/releases/latest/download/epi_swa_data_library.zip"
r = get(url, timeout=(10,300))
zf = zipfile.ZipFile(io.BytesIO(r.content))
mapping = {}
headers_seen = set()
for n in zf.namelist():
    with zf.open(n) as f:
        txt = io.TextIOWrapper(f, encoding="utf-8")
        rd = csv.reader(txt)
        header = next(rd)
        headers_seen.add(tuple(header))
        try:
            row = next(rd)
        except StopIteration:
            row = []
        rec = dict(zip(header, row))
        ind = rec.get("indicator")
        mapping[n] = ind
        print(f"{n:45} indicator={ind!r}  data_version={rec.get('data_version')!r}")
print("\n--- distinct header tuples:", len(headers_seen))
for h in headers_seen:
    print(list(h))
print("\nsample row dict:", rec)
