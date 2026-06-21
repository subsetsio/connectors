from subsets_utils import get
import csv, io

ACCEPT = {"Accept":"application/vnd.sdmx.data+csv;version=1.0.0"}

def fetch(flow):
    url = f"https://api.statistiken.bundesbank.de/rest/data/{flow}"
    r = get(url, headers=ACCEPT, timeout=(10,180))
    return r

for flow in ["BBDA1","BBBK1","BBSIS","BBNZ1","BBDE1"]:
    r = fetch(flow)
    text = r.text
    if text and text[0]=="﻿": text = text[1:]
    rdr = csv.DictReader(io.StringIO(text), delimiter=";")
    rows = list(rdr)
    cols = rdr.fieldnames
    common = [c for c in cols if c in ("DATAFLOW","TIME_PERIOD","OBS_VALUE","BBK_ID","BBK_TITLE","BBK_UNIT","TIME_FORMAT","BBK_UNIT_MULT","BBK_DECIMALS")]
    tfmts = set(row.get("TIME_FORMAT") for row in rows[:5000])
    tps = set(row.get("TIME_PERIOD") for row in rows[:3])
    print(f"{flow}: status={r.status_code} bytes={len(r.content)} nrows={len(rows)} ncols={len(cols)}")
    print("   common cols present:", common)
    print("   TIME_FORMAT sample:", tfmts, "| TIME_PERIOD sample:", tps)
    print("   has BBK_ID:", "BBK_ID" in cols, "| has BBK_TITLE:", "BBK_TITLE" in cols)
