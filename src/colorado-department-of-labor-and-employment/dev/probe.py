from subsets_utils import get

# Check a few datasets in the union for shape, types, nested fields, row counts.
for rid in ["4e3w-qire", "busm-qa5b", "bynd-i2hj", "gyeb-jc69"]:
    r = get(f"https://data.colorado.gov/resource/{rid}.json",
            params={"$limit": 3, "$offset": 0}, timeout=(10.0, 60.0))
    r.raise_for_status()
    rows = r.json()
    print("===", rid, "rows:", len(rows))
    if rows:
        for k, v in rows[0].items():
            print(f"   {k!r:20} -> {type(v).__name__:6} {str(v)[:30]!r}")
    # count
    c = get(f"https://data.colorado.gov/resource/{rid}.json",
            params={"$select": "count(*)"}, timeout=(10.0, 60.0))
    print("   count:", c.json())
