import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import json

BASE="https://ckan.publishing.service.gov.uk/api/3/action/"
families=["firm-complaints","general-insurance-value-measures","mortgage-lending-statistics",
          "product-sales","retail-intermediary-market","retirement-income-market"]

r=get(BASE+"package_search", params={"q":"organization:financial-conduct-authority","rows":1000}, timeout=60)
pkgs=r.json()["result"]["results"]

import re
MONTHS="january|february|march|april|may|june|july|august|september|october|november|december"
def fam(slug):
    s=re.sub(r'^fca-','',slug); s=re.sub(r'-data$','',s); prev=None
    while prev!=s:
        prev=s
        s=re.sub(r'-(19|20)\d{2}(-\d{2})?$','',s); s=re.sub(r'-q[1-4]$','',s); s=re.sub(r'-h[12]$','',s)
        s=re.sub(r'-('+MONTHS+r')$','',s); s=re.sub(r'-(19|20)\d{2}$','',s); s=re.sub(r'-\d{1,2}$','',s)
        s=re.sub(r'-(to|and|ending|year-ending)$','',s)
    s=re.sub(r'-data$','',s); s=re.sub(r'-quarterly$','',s); s=re.sub(r'^the-','',s)
    return s.strip('-') or slug

groups={}
for p in pkgs: groups.setdefault(fam(p["name"]),[]).append(p)

for f in families:
    ms=sorted(groups[f], key=lambda p:p.get("metadata_modified") or "")
    latest=ms[-1]
    print("="*80)
    print(f"FAMILY {f}  ({len(ms)} packages)  latest={latest['name']}")
    for res in latest.get("resources",[]):
        fmt=(res.get("format") or "").upper().lstrip(".")
        if fmt in ("XLSX","XLS","CSV"):
            print(f"  [{fmt}] {res.get('name')!r}  -> {res.get('url')}")
