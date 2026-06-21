import subsets_utils as su
captured = {}
def fake_ndjson(rows, asset, **kw):
    rows=list(rows); captured[asset]=rows; print(f"  {asset}: {len(rows)} rows; sample={rows[0] if rows else None}")
    return asset
su.save_raw_ndjson = fake_ndjson
import sys; sys.path.insert(0,"src")
import nodes.nasa as n
n.save_raw_ndjson = fake_ndjson  # patch the imported binding

print("== gistemp monthly =="); n.fetch_gistemp("nasa-gistemp-monthly-anomalies")
print("== gistemp zonal =="); n.fetch_gistemp("nasa-gistemp-zonal-annual")
print("== eonet =="); n.fetch_eonet("nasa-events")
print("== jpl fireball =="); n.fetch_jpl("nasa-fireball")
print("== jpl nhats =="); n.fetch_jpl("nasa-nhats")
# quick distinct checks
mr=captured["nasa-gistemp-monthly-anomalies"]
print("monthly regions:", set(r["region"] for r in mr), "years:", min(r["year"] for r in mr),"-",max(r["year"] for r in mr))
print("monthly periods:", sorted(set(r["period"] for r in mr)))
zr=captured["nasa-gistemp-zonal-annual"]; print("zonal zones:", sorted(set(r["zone"] for r in zr)))
nh=captured["nasa-nhats"][0]; print("nhats keys:", sorted(nh.keys()))
