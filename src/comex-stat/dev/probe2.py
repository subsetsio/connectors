import certifi, tempfile, os, io
import httpx, pyarrow as pa, pyarrow.csv as pacsv
inter = open("/tmp/inter.pem").read()
bundle = certifi.contents() + "\n" + inter
fd, path = tempfile.mkstemp(suffix=".pem"); os.write(fd, bundle.encode()); os.close(fd)
url = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_1997.csv"
with httpx.Client(verify=path, timeout=120, follow_redirects=True) as c:
    r = c.get(url)
print("status", r.status_code, "bytes", len(r.content))
raw = r.content
try: raw.decode("utf-8"); print("utf8 ok")
except Exception as e: print("utf8 fail", e)
header = raw.split(b"\n",1)[0].decode("utf-8").replace('"','').strip()
cols=[x for x in header.split(";") if x]
t = pacsv.read_csv(io.BytesIO(raw),
  read_options=pacsv.ReadOptions(encoding="utf-8"),
  parse_options=pacsv.ParseOptions(delimiter=";"),
  convert_options=pacsv.ConvertOptions(column_types={x:pa.string() for x in cols}, strings_can_be_null=True))
print("rows", t.num_rows, "cols", t.column_names)
print(t.slice(0,2).to_pylist())
