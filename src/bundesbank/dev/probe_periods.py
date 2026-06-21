from subsets_utils import get
import csv, io, re, json

ACCEPT = {"Accept":"application/vnd.sdmx.data+csv;version=1.0.0"}
flows = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/bundesbank/work/entity_union.json"))

def pat(tp):
    if re.match(r'^\d{4}$', tp): return "YYYY"
    if re.match(r'^\d{4}-\d{2}$', tp): return "YYYY-MM"
    if re.match(r'^\d{4}-\d{2}-\d{2}$', tp): return "YYYY-MM-DD"
    if re.match(r'^\d{4}-Q[1-4]$', tp): return "YYYY-Qn"
    if re.match(r'^\d{4}-S[12]$', tp): return "YYYY-Sn"
    if re.match(r'^\d{4}-W\d{2}$', tp): return "YYYY-Wnn"
    return "OTHER:"+tp

fmts=set(); pats=set(); bad=[]
for flow in flows:
    url=f"https://api.statistiken.bundesbank.de/rest/data/{flow}?lastNObservations=1"
    try:
        r=get(url, headers=ACCEPT, timeout=(10,120))
        if r.status_code!=200:
            bad.append((flow,r.status_code)); continue
        t=r.text
        if t and t[0]=="﻿": t=t[1:]
        rdr=csv.DictReader(io.StringIO(t), delimiter=";")
        n=0
        for row in rdr:
            fmts.add(row.get("TIME_FORMAT")); pats.add(pat(row.get("TIME_PERIOD",""))); n+=1
        if n==0: bad.append((flow,"empty"))
    except Exception as e:
        bad.append((flow,str(e)[:60]))
print("TIME_FORMAT values:", sorted(f for f in fmts if f))
print("TIME_PERIOD patterns:", sorted(pats))
print("bad/non-200:", bad)
