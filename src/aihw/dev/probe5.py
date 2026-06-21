from subsets_utils import get
import json
MYH="https://myhospitalsapi.aihw.gov.au/api/v1"
H={"Accept":"application/json"}
for path in ["measure-downloads/measure-download-codes","simple-downloads/download-codes","reporting-units-downloads/datasheet-codes"]:
    try:
        d=get(f"{MYH}/{path}", headers=H, timeout=(10,60)).json()
        print(path, "->", json.dumps(d.get("result"))[:300])
    except Exception as e:
        print(path,"ERR",e)
