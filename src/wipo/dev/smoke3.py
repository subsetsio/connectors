import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from nodes.wipo import _get_json, _parse_office_table, _parse_key_table, _explode

# KEY 201 should now give millions, not 1.0
kdata = _get_json("keyindicator/keysearch-json/201", {})
krows = _parse_key_table(kdata, 201, "Total applications")
ind_world = [r for r in krows if r["ip_right"].startswith("Patent") and r["year"] == 2024]
print("KEY 201 Patent World 2024:", ind_world)

# Verify ips packing: check a large value office has no thousands comma issue
data = _get_json("ips-search/table-result",
                 {"selectedTab": "patent", "indicator": 10, "reportType": "11", "fromYear": 2023, "toYear": 2023})
for rec in data["records"]:
    if rec.get("selectedOffice") in ("China", "World", "Asia"):
        print(f"IPS {rec['selectedOffice']} 2023 raw={rec.get('2023')!r} SeqOrder={rec.get('2023_SeqOrder')}")

# Verify pmh: large value formatting + SeqOrder relation
sel = _get_json("pmh-search/loadOffOrgClassList", {"indicator": "1001"})
off = list((sel.get("pmhOffList") or {}).keys()); ori = list((sel.get("pmhOriginList") or {}).keys())
pdata = _get_json("pmh-search/table-result",
                  {"selectedTab": "pct", "indicator": "1001", "reportType": "4001",
                   "fromYear": 2023, "toYear": 2023, "pmhOffSelValues": off, "pmhOriSelValues": ori})
big = sorted(pdata["records"], key=lambda r: (r.get("2023_SeqOrder") or 0), reverse=True)[:3]
for rec in big:
    print(f"PMH {rec.get('selectedOffice')}/{rec.get('selectedOrigin')} 2023 raw={rec.get('2023')!r} SeqOrder={rec.get('2023_SeqOrder')}")
