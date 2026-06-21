import json
from subsets_utils import get

KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; subsets-bot/1.0)"}

# a few of the accepted entity ids spanning different table types
ids = [
    "067fea29-928e-493c-b576-df5154b3661a",  # Gender Budget 2019-20 to 2021-22
    "0e2c4496-4c33-4f13-86c8-ed297773702e",  # Exports, Imports and Trade Balance till 2012-13
    "01daa0df-0621-41ef-bddf-e6255b343c68",  # IIFCL snapshot
]
for rid in ids:
    r = get(
        f"https://api.data.gov.in/resource/{rid}",
        params={"api-key": KEY, "format": "json", "limit": 1000, "offset": 0},
        headers=HEADERS,
        timeout=(10.0, 120.0),
    )
    d = r.json()
    recs = d.get("records") or []
    print("=" * 70)
    print(rid, "| status", r.status_code, "| total", d.get("total"), "| count", len(recs))
    print("has document_id in every rec:", all("document_id" in x for x in recs) if recs else "n/a")
    if recs:
        print("keys:", list(recs[0].keys()))
        print("first record:", json.dumps(recs[0]))
        print("value types:", {k: type(v).__name__ for k, v in recs[0].items()})
