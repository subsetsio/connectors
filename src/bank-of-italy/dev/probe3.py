import time, nodes.bank_of_italy as m
for eid in ["RTIT0100","BMK0200","AGGM0100"]:
    t0=time.time()
    m._seed_session()
    mem=m._member_series(eid,m.ENTITIES[eid])
    groups=[mem[i:i+m.CHUNK_SIZE] for i in range(0,len(mem),m.CHUNK_SIZE)]
    from concurrent.futures import ThreadPoolExecutor
    rows=[]
    with ThreadPoolExecutor(max_workers=min(m._MAX_WORKERS,len(groups))) as p:
        for obs in p.map(m._fetch_group,groups):
            rows+=[o["values"] for o in obs if o.get("values")]
    ser=len(set(r["CUBEID"] for r in rows))
    print(f"{eid}: members={len(mem)} obs={len(rows)} series_with_data={ser} in {time.time()-t0:.0f}s")
