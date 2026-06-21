import sys, os, json, base64
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

base="https://gamma-api.polymarket.com/markets/keyset"
j0 = get(base, params={"limit":3}, timeout=(10,60)).json()
nc = j0["next_cursor"]
# decode cursor — it looked like prefix + base64 json
print("cursor:", nc)
# try splitting: maybe first chars are a token, rest base64
for cut in [0, 11, 12, 43]:
    try:
        dec = base64.urlsafe_b64decode(nc[cut:]+"==")
        print(f"cut {cut}: {dec[:120]}")
    except Exception as e:
        print(f"cut {cut}: err {e}")
