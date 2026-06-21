import io
from subsets_utils import get
import pyarrow as pa
import pyarrow.csv as pacsv

url = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_1997.csv"
r = get(url, timeout=(10,120))
print("status", r.status_code, "bytes", len(r.content))
raw = r.content
try:
    raw.decode("utf-8"); print("utf8 ok: yes")
except Exception as e:
    print("utf8 ok: no ->", e)
header = raw.split(b"\n",1)[0].decode("utf-8").replace('"','').strip()
cols = [x for x in header.split(";") if x]
ro = pacsv.ReadOptions(encoding="utf-8")
po = pacsv.ParseOptions(delimiter=";")
co = pacsv.ConvertOptions(column_types={x: pa.string() for x in cols}, strings_can_be_null=True)
t = pacsv.read_csv(io.BytesIO(raw), read_options=ro, parse_options=po, convert_options=co)
print("rows", t.num_rows, "cols", t.column_names)
print(t.slice(0,2).to_pylist())
