import duckdb, tempfile, os
from subsets_utils import get
for did in ["DF_ICL2023","DF_NMIC_SEXO"]:
    txt=get(f"https://sdmx.ine.gob.cl/rest/data/CL01,{did},1.0?format=csv",
            headers={"Accept":"application/vnd.sdmx.data+csv"},timeout=(10,120)).text
    f=tempfile.NamedTemporaryFile("w",suffix=".csv",delete=False); f.write(txt); f.close()
    duckdb.sql(f"CREATE OR REPLACE TEMP VIEW v AS SELECT * FROM read_csv_auto(['{f.name}'])")
    res=duckdb.sql('SELECT * FROM "v"'.replace('"v"','v'))
    df=duckdb.sql("SELECT COUNT(*) n FROM v").fetchone()
    print(did,"rows",df[0])
    print("  schema:", duckdb.sql("DESCRIBE SELECT * FROM v").df()[["column_name","column_type"]].values.tolist()[:8])
    os.unlink(f.name)
