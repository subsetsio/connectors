import io, zipfile
import pyarrow as pa
import pyarrow.csv as pacsv
from subsets_utils import get

OBS_COLUMNS = ["LOC_ID","LATITUDE","LONGITUDE","SUBNATIONAL1_CODE","ENTRY_TECHNIQUE","SUB_ID","OBS_ID","Month","Day","Year","PROJ_PERIOD_ID","SPECIES_CODE","alt_full_spp_code","HOW_MANY","PLUS_CODE","VALID","REVIEWED","DAY1_AM","DAY1_PM","DAY2_AM","DAY2_PM","EFFORT_HRS_ATLEAST","SNOW_DEP_ATLEAST","Data_Entry_Method"]

url = "https://cdn.feederwatch.org/data/202406/PFW_all_1988_1995_May2024_Public.csv.zip"
resp = get(url, timeout=(10.0, 300.0))
resp.raise_for_status()
zf = zipfile.ZipFile(io.BytesIO(resp.content))
name = [n for n in zf.namelist() if n.lower().endswith(".csv")][0]
print("inner:", name)

col_types = {c: pa.string() for c in OBS_COLUMNS}
ro = pacsv.ReadOptions(block_size=8*1024*1024)
co = pacsv.ConvertOptions(column_types=col_types, null_values=["NA",""], strings_can_be_null=True)
with zf.open(name) as f:
    reader = pacsv.open_csv(f, read_options=ro, convert_options=co)
    total = 0
    nbatch = 0
    first_schema = None
    for batch in reader:
        if first_schema is None:
            first_schema = batch.schema
        total += batch.num_rows
        nbatch += 1
    print("schema names match header:", first_schema.names == OBS_COLUMNS)
    print("all string:", all(str(first_schema.field(c).type)=="string" for c in OBS_COLUMNS))
    print("rows:", total, "batches:", nbatch)
