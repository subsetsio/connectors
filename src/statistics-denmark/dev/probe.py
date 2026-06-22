import io, time
import pyarrow as pa
import pyarrow.csv as pacsv
from subsets_utils import get, post

BASE = "https://api.statbank.dk/v1"
ROW_BUDGET = 300_000

def fetch(table_id):
    info = get(f"{BASE}/tableinfo/{table_id}", params={"format":"JSON","lang":"en"}).json()
    variables = info["variables"]
    chunk_var = max(variables, key=lambda v: len(v.get("values") or []))
    others = [v for v in variables if v is not chunk_var]
    rpu = 1
    for v in others: rpu *= max(1, len(v.get("values") or []))
    per_req = max(1, ROW_BUDGET // max(1, rpu))
    cvals = [x["id"] for x in (chunk_var.get("values") or [])]
    slices = [cvals[i:i+per_req] for i in range(0,len(cvals),per_req)] or [["*"]]
    print(f"{table_id}: chunk_var={chunk_var['id']} card={len(cvals)} rows/unit={rpu} per_req={per_req} nslices={len(slices)}")
    total=0; cols=None; t0=time.time()
    for sel in slices:
        body={"table":table_id,"format":"BULK","lang":"en",
              "variables":[{"code":chunk_var["id"],"values":sel}]+[{"code":v["id"],"values":["*"]} for v in others]}
        r=post(f"{BASE}/data",json=body,timeout=600); r.raise_for_status()
        content=r.content; nl=content.find(b"\n")
        names=[h.strip() for h in content[:nl].decode("utf-8").rstrip("\r").split(";")]
        tb=pacsv.read_csv(io.BytesIO(content),parse_options=pacsv.ParseOptions(delimiter=";"),
                          convert_options=pacsv.ConvertOptions(column_types={n:pa.string() for n in names}))
        total+=tb.num_rows; cols=tb.column_names
    print(f"  -> {total} rows, cols={cols}, {time.time()-t0:.1f}s")

for t in ["AED21","PRIS01","FOLK1C"]:
    fetch(t)
