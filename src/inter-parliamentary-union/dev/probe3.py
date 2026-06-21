import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]/"src"))
import json
from subsets_utils import get
for rep in ["women-ranking","age-brackets","speakers","secretaries-general","women-speakers","elections"]:
    r=get(f"https://api.data.ipu.org/v1/reports/{rep}",headers={"Accept-Language":"en"},timeout=(10,120))
    d=r.json(); data=d.get("data")
    rows=list(data.values()) if isinstance(data,dict) else data
    row=rows[0] if rows else {}
    print(f"\n===== report {rep}  rows={len(rows)} =====")
    for k in sorted(row):
        print(f"  {k}: {json.dumps(row[k],ensure_ascii=False)[:100]}")
