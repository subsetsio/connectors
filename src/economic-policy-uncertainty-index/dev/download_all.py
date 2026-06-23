import json, os, sys
sys.path.insert(0, "src")
from subsets_utils import get
mapping=json.load(open("dev/mapping.json"))
os.makedirs("dev/files", exist_ok=True)
import urllib.parse
for eid, fn in mapping.items():
    url="https://www.policyuncertainty.com/media/"+urllib.parse.quote(fn)
    dest="dev/files/"+fn
    if os.path.exists(dest): continue
    try:
        r=get(url, timeout=(10,120))
        r.raise_for_status()
        open(dest,"wb").write(r.content)
        print("OK", len(r.content), fn)
    except Exception as e:
        print("FAIL", fn, type(e).__name__, e)
