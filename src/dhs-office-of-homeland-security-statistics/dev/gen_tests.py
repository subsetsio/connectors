import os, json
from utils import (install_browser_client, yearbook_workbook_url,
                   enforcement_workbook_url, download_workbook, parse_sheet)
from constants import ENTITY_META

SLUG="dhs-office-of-homeland-security-statistics"
install_browser_client()
cache={}
def wb(meta):
    url=enforcement_workbook_url() if meta["section_kw"] is None else yearbook_workbook_url(meta["section_kw"])
    if url not in cache: cache[url]=download_workbook(url)
    return cache[url]

os.makedirs("tests", exist_ok=True)
counts={}
for eid,meta in ENTITY_META.items():
    _,rows=parse_sheet(wb(meta), meta["sheet"])
    counts[eid]=len(rows)

for eid,n in counts.items():
    spec_id=f"{SLUG}-{eid.lower().replace('_','-')}"
    floor=max(1, n//2)
    sheet=ENTITY_META[eid]["sheet"]
    y=f"""spec_id: {spec_id}
status: active
tests:
  - row_count: {{min: {floor}}}
    reason: parsed sheet {sheet!r} yielded {n} rows on probe; a run materially below half that means the point-in-time workbook rotated, the Akamai TLS block returned (empty), or header detection failed.
    certainty: 80
    severity: block
"""
    open(f"tests/{spec_id}.yaml","w").write(y)
print("wrote", len(counts), "yaml specs; min count", min(counts.values()), "max", max(counts.values()))
