import io
import pyarrow as pa, pyarrow.csv as pacsv
from subsets_utils import get

# adm1 with explicit types: confirm quoted "Moldova, Republic of" parses correctly
types = {"year": pa.int64(), "ADM0_NAME": pa.string(), "ADM1_NAME": pa.string(),
         "ADM0_CODE": pa.int64(), "ADM1_CODE": pa.int64(),
         "permanent": pa.float64(), "projectedPermanent": pa.float64(), "5yr_Permanent": pa.float64(),
         "seasonal": pa.float64(), "projectedSeasonal": pa.float64(), "5yr_Seasonal": pa.float64()}
r = get("https://storage.googleapis.com/global-surface-water-stats/gaul1-all-2018.csv", timeout=(10,300))
t = pacsv.read_csv(io.BytesIO(r.content), convert_options=pacsv.ConvertOptions(column_types=types))
print("cols", t.column_names)
print("rows", t.num_rows)
# find Moldova rows
import pyarrow.compute as pc
mask = pc.equal(t.column("ADM0_NAME"), "Moldova, Republic of")
md = t.filter(mask)
print("moldova rows", md.num_rows)
print(md.slice(0,2).to_pylist())
