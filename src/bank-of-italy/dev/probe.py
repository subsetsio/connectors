import sys
import nodes.bank_of_italy as m

eid = "AGGM0100"
node_id = "bank-of-italy-aggm0100"
print("seeding session...")
m._seed_session()
mem = m._member_series(eid, m.ENTITIES[eid])
print("members:", len(mem))
obs = m._chunk_observations(mem[:min(len(mem), m.CHUNK_SIZE)])
print("observations (first chunk):", len(obs))
if obs:
    print("sample values keys:", sorted(obs[0]["values"].keys()))
    print("sample:", {k: obs[0]["values"][k] for k in ("CUBEID","DATA_OSS","VALORE","DFCUBEID")})
