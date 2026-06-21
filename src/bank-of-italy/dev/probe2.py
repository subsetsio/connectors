import time, nodes.bank_of_italy as m
for eid in ["RTIT0100", "AGGM0100"]:
    nid = "bank-of-italy-" + eid.lower().replace("_","-")
    t0=time.time()
    m._seed_session()
    mem = m._member_series(eid, m.ENTITIES[eid])
    chunks=[mem[i:i+m.CHUNK_SIZE] for i in range(0,len(mem),m.CHUNK_SIZE)]
    from concurrent.futures import ThreadPoolExecutor
    rows=[]
    with ThreadPoolExecutor(max_workers=min(m._MAX_WORKERS,len(chunks))) as p:
        for obs in p.map(m._chunk_observations, chunks):
            rows += [o["values"] for o in obs if o.get("values")]
    print(f"{eid}: members={len(mem)} obs={len(rows)} in {time.time()-t0:.0f}s")
