import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent/"src"))
import io, json
import pyarrow as pa
import pyarrow.csv as pacsv
from subsets_utils import get

PPD_COLS = ["transaction_id","price","date_of_transfer","postcode","property_type",
            "old_new","duration","paon","saon","street","locality","town_city",
            "district","county","ppd_category_type","record_status"]

# --- PPD: parse the small 2026 partial year file ---
url = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2026.csv"
r = get(url, timeout=(10.0,120.0))
print("PPD http:", r.status_code, "bytes:", len(r.content))
read_opts = pacsv.ReadOptions(column_names=PPD_COLS, autogenerate_column_names=False, block_size=8<<20)
conv_opts = pacsv.ConvertOptions(column_types={c: pa.string() for c in PPD_COLS})
tbl = pacsv.read_csv(io.BytesIO(r.content), read_options=read_opts, convert_options=conv_opts)
print("PPD rows:", tbl.num_rows, "cols:", tbl.num_columns)
print("PPD sample row:", {k: tbl.column(k)[0].as_py() for k in ["transaction_id","price","date_of_transfer","property_type","county"]})

# --- UKHPI: pagination + flat extraction for one region ---
base = "https://landregistry.data.gov.uk/data/ukhpi/region/aberdeenshire.json"
got=[]; page=0
while True:
    rr = get(base, params={"_view":"all","_pageSize":500,"_page":page}, headers={"Accept":"application/json"}, timeout=(10.0,120.0))
    res = rr.json()["result"]
    items = res.get("items", [])
    got += items
    total = res.get("totalResults")
    page += 1
    if not items or len(got) >= (total or 0) or page>5:
        break
print("UKHPI aberdeenshire total:", total, "fetched:", len(got))
it = got[0]
rr_region = it.get("refRegion", {})
label = rr_region.get("label")
print("refRegion._about:", rr_region.get("_about"))
print("label:", label)
measure_keys = sorted(k for k in it if k not in ("refRegion","refMonth","refPeriodStart","refPeriodDuration","_about","type","dataSet"))
print("num measure keys:", len(measure_keys))
print("sample measures:", {k: it.get(k) for k in ["averagePrice","housePriceIndex","percentageAnnualChange","salesVolume"]})
print("refMonth:", it.get("refMonth"))
