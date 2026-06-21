import nodes.itu as m
cids = m._country_ids()
for cid in [38968, 8965]:  # 38968 = no-data/500, 8965 = real data
    r = m._download_indicator_csv(cid, cids)
    print(f"code {cid}: {'None (skipped)' if r is None else str(len(r))+' rows'}")
