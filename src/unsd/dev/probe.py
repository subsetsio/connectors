import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from subsets_utils import get

BASE = "https://unstats.un.org/SDGAPI/v1/sdg"
r = get(f"{BASE}/Series/List", timeout=(10,180))
print("status:", r.status_code)
print("content-type:", r.headers.get("content-type"))
print("len bytes:", len(r.content))
print("head:", r.text[:300])
