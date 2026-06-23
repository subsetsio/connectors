import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils as su

ASSET = "clinicaltrials-gov-devtest"
rows = [{"nct_id":"NCT1","condition":"A"},{"nct_id":"NCT2","condition":"B"}]
with su.raw_writer(ASSET, "ndjson.gz", mode="wt", compression="gzip") as fh:
    for r in rows:
        fh.write(json.dumps(r) + "\n")
print("wrote. files:", su.list_raw_files(ASSET))
back = su.load_raw_ndjson(ASSET)
print("loaded:", back)
su.delete_raw_file(ASSET, "ndjson.gz")
print("cleaned. files now:", su.list_raw_files(ASSET))
