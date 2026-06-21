import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import pyarrow as pa
from nodes.wipo import (
    _get_json, _parse_office_table, _parse_key_table, IPS_SCHEMA, KEY_SCHEMA,
)

# IPS: patent indicator 10, report type 11 (full range)
fc = _get_json("ips-search/formcontrols", {"selectedTab": "patent"})
fy = min(int(y) for y in fc["ipsFYears"])
ty = max(int(y) for y in fc["ipsToYearList"])
data = _get_json("ips-search/table-result",
                 {"selectedTab": "patent", "indicator": 10, "reportType": "11", "fromYear": fy, "toYear": ty})
rows = _parse_office_table(data, 10, "Total patent applications", "Total count by filing office", packed=True)
print("IPS patent ind10 rt11 rows:", len(rows), "sample:", rows[0])
t = pa.Table.from_pylist(rows, schema=IPS_SCHEMA)
print("  -> table ok, rows", len(t), "years", min(t.column('year').to_pylist()), max(t.column('year').to_pylist()))

# PMH: pct indicator 1001 yearly
sel = _get_json("pmh-search/loadOffOrgClassList", {"indicator": "1001"})
off = list((sel.get("pmhOffList") or {}).keys())
ori = list((sel.get("pmhOriginList") or {}).keys())
pdata = _get_json("pmh-search/table-result",
                  {"selectedTab": "pct", "indicator": "1001", "reportType": "4001",
                   "fromYear": 1995, "toYear": 2026,
                   "pmhOffSelValues": off, "pmhOriSelValues": ori})
prows = _parse_office_table(pdata, 1001, "PCT applications by filing date", "Yearly statistics", packed=False)
print("\nPMH pct ind1001 rows:", len(prows), "sample:", prows[0] if prows else None)
pt = pa.Table.from_pylist(prows, schema=IPS_SCHEMA)
print("  -> table ok, rows", len(pt))

# KEY: indicator 201 and 222 (222 may be packed)
for kid, lbl in [("201", "Total applications"), ("222", "Patent route Direct/PCT")]:
    kdata = _get_json(f"keyindicator/keysearch-json/{kid}", {})
    krows = _parse_key_table(kdata, int(kid), lbl)
    bidx = set(r["breakdown_index"] for r in krows)
    print(f"\nKEY {kid} rows:", len(krows), "breakdown idxs:", sorted(bidx), "sample:", krows[0] if krows else None)
    kt = pa.Table.from_pylist(krows, schema=KEY_SCHEMA)
    print("  -> table ok, rows", len(kt))
