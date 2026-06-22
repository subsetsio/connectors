import io, csv, sys
sys.path.insert(0, "src")
from subsets_utils import get
from nodes.leaderboards import _LEADERBOARDS

def hdr(url):
    try:
        r = get(url, timeout=(10,120))
        ct = r.headers.get("Content-Type","")[:16]
        t = r.text
        if t and t[0]=="﻿": t=t[1:]
        rdr=list(csv.reader(io.StringIO(t)))
        h=[c.strip() for c in (rdr[0] if rdr else [])]
        return len(rdr)-1, ct, h
    except Exception as e:
        return -1, f"ERR {e}", []

y = 2024
for slug,(tmpl,types,tag) in _LEADERBOARDS.items():
    tval = types[0] if types[0] is not None else ""
    q = tmpl.format(y=y, type=tval)
    url = f"https://baseballsavant.mlb.com/leaderboard/{slug}?{q}&csv=true"
    n,ct,h = hdr(url)
    print(f"### {slug}  rows={n} ct={ct}")
    print("   cols:", h)
