import sys; sys.path.insert(0,"src")
from nodes.ons import _resolve_csv_url
for did in ["trade","TS058","TS009","retail-sales-index"]:
    print(did, "->", _resolve_csv_url(did))
