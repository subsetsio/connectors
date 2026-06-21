import io, zipfile
from subsets_utils import get

def members(url):
    r = get(url, timeout=(10, 120)); r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    out = []
    for i in z.infolist():
        head = b""
        if i.filename.lower().endswith((".csv", ".txt", ".tsv")):
            with z.open(i) as fh:
                head = fh.read(200)
        out.append((i.filename, i.file_size, head))
    return out

for k, u in {
 "geodist": "https://www.cepii.fr/distance/dist_cepii.zip",
 "geodist_geo": "https://www.cepii.fr/distance/geo_cepii.zip",
 "trade_volume": "https://www.cepii.fr/DATA_DOWNLOAD/trade_volume/data/trade_volume_v202507.zip",
}.items():
    print(f"\n== {k}  {u}")
    try:
        for n, s, h in members(u):
            print(f"   {s:>10}  {n}")
            if h:
                print(f"       head: {h[:160]!r}")
    except Exception as e:
        print("   ERR", e)

# macmap .txt delimiter — read first bytes of the member
import io as _io
print("\n== macmap header ==")
r = get("https://www.cepii.fr/DATA_DOWNLOAD/macmap/download/mmhs2_2007.zip", timeout=(10, 180)); r.raise_for_status()
z = zipfile.ZipFile(_io.BytesIO(r.content))
with z.open("mmhs2_2007.txt") as fh:
    print(repr(fh.read(300)))
