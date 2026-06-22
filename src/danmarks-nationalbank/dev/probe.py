import json
from subsets_utils import get, post

API = "https://api.statbank.dk/v1"

def tableinfo(tid):
    r = get(f"{API}/tableinfo/{tid}", params={"format": "JSON"}, timeout=(10, 120))
    r.raise_for_status()
    return r.json()

def bulk(tid, varcodes):
    body = {"table": tid, "lang": "en", "format": "BULK",
            "variables": [{"code": c, "values": ["*"]} for c in varcodes]}
    r = post(f"{API}/data", json=body, timeout=(10, 300))
    r.raise_for_status()
    return r.text

for tid in ["DNVALD", "DNVPU", "DNMNOGL", "DNRENTD"]:
    info = tableinfo(tid)
    vcodes = [v["id"] for v in info["variables"]]
    timevars = [v["id"] for v in info["variables"] if v.get("time")]
    print(f"\n=== {tid} :: vars={vcodes} time={timevars}")
    txt = bulk(tid, vcodes)
    lines = txt.splitlines()
    print("bytes:", len(txt), "lines:", len(lines))
    print("header:", lines[0])
    print("row1  :", lines[1])
    print("row2  :", lines[2])
