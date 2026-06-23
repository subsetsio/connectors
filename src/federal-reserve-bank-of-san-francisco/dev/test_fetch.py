import sys
sys.path.insert(0, "src"); sys.path.insert(0, "src/nodes")
import federal_reserve_bank_of_san_francisco as m
from subsets_utils import load_raw_parquet
for slug in ["proxy-funds-rate","total-factor-productivity-tfp","treasury-yield-premiums","twelfth-district-business-sentiment"]:
    sid = f"{m.SLUG}-{slug}"
    m.fetch_one(sid)
    t = load_raw_parquet(sid)
    import pyarrow.compute as pc
    nd = pc.sum(pc.is_valid(t.column("date"))).as_py()
    print(f"{slug}: rows={t.num_rows} dated={nd} schema={t.schema.types}")
