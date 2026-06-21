import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, zipfile, csv
from collections import Counter
from subsets_utils import get
url="https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/anual/Brasil_todos_sats/focos_br_todos-sats_2023.zip"
r=get(url, timeout=(10,180)); print("bytes", len(r.content))
zf=zipfile.ZipFile(io.BytesIO(r.content)); n=zf.namelist()[0]
sats=Counter(); frp_nonempty=Counter(); total=0
with zf.open(n) as f:
    t=io.TextIOWrapper(f, encoding="utf-8"); rdr=csv.DictReader(t)
    for row in rdr:
        total+=1
        s=row["satelite"]; sats[s]+=1
        if row.get("frp","")!="": frp_nonempty[s]+=1
print("total rows", total)
print("top satellites:", sats.most_common(12))
print("AQUA_M-T count:", sats.get("AQUA_M-T"))
print("frp nonempty for AQUA_M-T:", frp_nonempty.get("AQUA_M-T"))
