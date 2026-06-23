import re, gzip, io
from subsets_utils import get
import pyarrow as pa
import pyarrow.csv as pacsv

BASE = "https://files.data.gouv.fr/geo-dvf/latest/csv/"

# 1) years
html = get(BASE, timeout=(10,60)).text
years = sorted(set(re.findall(r'href="[^"]*?/(\d{4})/"', html)))
print("years:", years)

# 2) departements listing for latest year
y = years[-1]
dhtml = get(f"{BASE}{y}/departements/", timeout=(10,60)).text
depts = sorted(set(re.findall(r'href="[^"]*?/([0-9AB]{2,3})\.csv\.gz"', dhtml)))
print("n_depts:", len(depts), "sample:", depts[:6], depts[-4:])

# 3) parse one small dept with pyarrow forcing types
import time
url = f"{BASE}{y}/departements/48.csv.gz"
t0=time.time()
raw = get(url, timeout=(10,120)).content
print("dept48 gz bytes:", len(raw), "dl s:", round(time.time()-t0,2))
csv_bytes = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
header = csv_bytes.split(b"\n",1)[0].decode().split(",")
print("ncols:", len(header))
NUMERIC_FLOAT = {"valeur_fonciere","lot1_surface_carrez","lot2_surface_carrez","lot3_surface_carrez","lot4_surface_carrez","lot5_surface_carrez","surface_reelle_bati","surface_terrain","longitude","latitude"}
NUMERIC_INT = {"nombre_lots","nombre_pieces_principales"}
col_types = {}
for c in header:
    if c in NUMERIC_FLOAT: col_types[c]=pa.float64()
    elif c in NUMERIC_INT: col_types[c]=pa.int64()
    else: col_types[c]=pa.string()
tbl = pacsv.read_csv(io.BytesIO(csv_bytes), convert_options=pacsv.ConvertOptions(column_types=col_types))
print("rows:", tbl.num_rows, "schema ok")
print(tbl.slice(0,2).to_pydict()["valeur_fonciere"], tbl.slice(0,2).to_pydict()["date_mutation"])

# 4) size check a big dept (Bouches-du-Rhone 13)
import time
t0=time.time()
raw13 = get(f"{BASE}{y}/departements/13.csv.gz", timeout=(10,180)).content
csv13 = gzip.GzipFile(fileobj=io.BytesIO(raw13)).read()
print("dept13 gz:", len(raw13), "uncompressed:", len(csv13), "dl s:", round(time.time()-t0,2))
