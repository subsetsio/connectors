import io, pyarrow.csv as pacsv, pyarrow.compute as pc
from subsets_utils import get
URL="https://www.cato.org/sites/cato.org/files/human-freedom-index-files/2025-human-freedom-index-data.csv"
t=pacsv.read_csv(io.BytesIO(get(URL,timeout=(10,120)).content))
for c in ["hf_score","ef_score","pf_score","hf_rank"]:
    col=t.column(c)
    print(c,"min",pc.min(col).as_py(),"max",pc.max(col).as_py(),"nulls",pc.sum(pc.is_null(col)).as_py())
print("regions:", set(t.column("region").to_pylist()))
