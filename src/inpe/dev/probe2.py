import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, zipfile, csv
from subsets_utils import get
def head(url):
    print("="*60); print(url)
    r = get(url, timeout=(10,120)); print("status", r.status_code, "bytes", len(r.content))
    zf = zipfile.ZipFile(io.BytesIO(r.content)); names = zf.namelist(); print("members", names)
    with zf.open(names[0]) as f:
        t = io.TextIOWrapper(f, encoding="utf-8"); rdr = csv.reader(t)
        print("header", next(rdr))
        for i,row in enumerate(rdr):
            print("row", row); 
            if i>=1: break
head("https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/anual/Brasil_todos_sats/focos_br_todos-sats_2023.zip")
head("https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/anual/Brasil_todos_sats/focos_br_todos-sats_2003.zip")
