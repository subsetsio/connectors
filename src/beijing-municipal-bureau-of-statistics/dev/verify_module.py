import sys; sys.path.insert(0,"src")
import nodes.beijing_municipal_bureau_of_statistics as M

captured={}
M.save_raw_ndjson = lambda rows, asset: captured.__setitem__(asset, rows)

print("n DOWNLOAD_SPECS", len(M.DOWNLOAD_SPECS))
print("n TRANSFORM_SPECS", len(M.TRANSFORM_SPECS))
print("sample spec id", M.DOWNLOAD_SPECS[0].id)

# annual: 01-60Y-1-03-N ; monthly: 05-DBW-A01
for eid in ["01-60Y-1-03-N","05-DBW-A01"]:
    sid=M._spec_id(eid)
    M.fetch_one(sid)
    rows=captured[sid]
    print(f"\n=== {sid}: {len(rows)} rows")
    for r in rows[:4]: print("   ", r)
    # distinct periods/cols
    print("   distinct mask:", sorted(set(r['mask'] for r in rows))[:6], "...n=",len(set(r['mask'] for r in rows)))
    print("   distinct col_label:", sorted(set(r['col_label'] for r in rows))[:6])
