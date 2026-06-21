import sys; sys.path.insert(0,"src")
import duckdb, glob, os
import nodes.observatory_of_economic_complexity as M
from constants import CUBES

# 1. small whole cube
M.fetch_one("observatory-of-economic-complexity-complexity-eci-a-hs22-hs4")
# 2. one partition leaf of a large bilateral cube (seed the exporter cut)
cube="bilateral_relatedness"; sid=M._spec_id(cube); cfg=CUBES[cube]
ms={M._snake(m) for m in cfg["measures"]}
n=M._fetch_partition(sid, cube, cfg["drilldowns"], cfg["measures"], cfg["split_order"], ms,
                     cuts={"Exporter Country Official":"aus"}, applied=["Exporter Country Official"])
print("bilat leaf rows:", n)

# find raw dir
from subsets_utils.io import raw_uri
base=raw_uri("__p__","__").rsplit("/",1)[0]
print("raw base:", base)
for sid_test in ["observatory-of-economic-complexity-complexity-eci-a-hs22-hs4", sid]:
    files=[f for f in os.listdir(base) if f.startswith(os.path.basename(sid_test))]
    print(sid_test, "->", files[:3], "(", len(files), "files )")

# 3. run a transform SQL over each
for cube_t, dep in [("complexity_eci_a_hs22_hs4","observatory-of-economic-complexity-complexity-eci-a-hs22-hs4"),
                    ("bilateral_relatedness", sid)]:
    files=glob.glob(f"{base}/{dep}.parquet") or glob.glob(f"{base}/{dep}-*.parquet")
    duckdb.sql(f"CREATE OR REPLACE TEMP VIEW \"{dep}\" AS SELECT * FROM read_parquet({files})")
    sql=M._transform_sql(dep, CUBES[cube_t]["measures"])
    res=duckdb.sql(sql)
    cols=res.columns
    cnt=duckdb.sql(f"SELECT count(*) c FROM ({sql})").fetchone()[0]
    print(f"\n{cube_t}: transform rows={cnt}, cols={cols}")
    print(duckdb.sql(sql+" LIMIT 2").fetchall())
