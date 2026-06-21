import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from nodes.wipo import _get_json

kdata = _get_json("keyindicator/keysearch-json/201", {})
print("columns:", json.dumps(kdata["columns"])[:600])
print("\nrecord[0]:", json.dumps(kdata["records"][0]))
print("\nrecord[1]:", json.dumps(kdata["records"][1]))

print("\n--- IPS patent ind10 rt11 first 3 records ---")
data = _get_json("ips-search/table-result",
                 {"selectedTab": "patent", "indicator": 10, "reportType": "11", "fromYear": 2022, "toYear": 2023})
for r in data["records"][:3]:
    print(json.dumps(r))
