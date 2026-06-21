import io
import pyarrow as pa
import pyarrow.csv as pacsv
from subsets_utils import get
content = get("https://raw.githubusercontent.com/fivethirtyeight/data/master/star-wars-survey/StarWars.csv", timeout=(10.0,120.0)).content
print("bytes:", len(content))
try:
    content.decode("utf-8"); print("decodes as utf-8: YES")
except UnicodeDecodeError as e:
    print("decodes as utf-8: NO ->", e)
# default (utf8) parse
t = pacsv.read_csv(io.BytesIO(content))
# check a string column for invalid utf8 by re-encoding via to_pylist
col = t.column(1).to_pylist()[:3]
print("default parse sample:", col)
# cp1252 transcode
t2 = pacsv.read_csv(io.BytesIO(content), read_options=pacsv.ReadOptions(encoding="cp1252"))
print("cp1252 sample:", t2.column(1).to_pylist()[:3])
print("rows/cols:", t2.num_rows, t2.num_columns)
