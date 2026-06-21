import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "nodes"))
import national_health_mission_hmis as N
import pyarrow as pa

def check(rid, title, npages=1):
    fy, fyy = N._parse_fy(title); geo = N._parse_geo(title)
    # fetch just 1 page for probe
    doc = N._get_json(N._RESOURCE.format(rid), {"api-key": N._api_key(), "format":"json","offset":"0","limit":"1000"})
    rows = doc.get("records", [])
    long = N._melt(rows, rid, fy, fyy, geo)
    print(f"\n{title[:55]} | fy={fy} geo={geo} | wide={len(rows)} -> long={len(long)}")
    # build table to verify schema coercion
    t = pa.Table.from_pylist(long[:5000], schema=N.SCHEMA)
    print("  schema ok, sample long rows:")
    for r in long[:3]:
        print("   ", {k: r[k] for k in ("level","state","district","s_no","parameter","month","total","public","rural")})
    months = collections.Counter(r["month"] for r in long)
    print("  month dist:", dict(months))
    lv = collections.Counter(r["level"] for r in long)
    print("  level:", dict(lv))

# All-India 69-col, All-India 17-col, a per-state report
check("e086e5ef-03ef-42ce-8302-d93d1fc7d30b", "Item-wise HMIS report of All India for 2019-20")
check("8074b2f2-a366-42b8-acd8-500f0768ca00", "Item-wise HMIS report of All India for 2008-09")
check("9da7b8a9-ea07-486c-a7ed-dda6885b45e9", "Item-wise HMIS report of Maharashtra for 2018-19")

# also verify the family selector count
res = N._list_item_wise_resources()
print("\nitem-wise family resource count:", len(res))
