import duckdb, tempfile, os
from subsets_utils import get
DROP="DATAFLOW, INDICADOR, DECIMALS, MULT, NOTAS, NOTAS_INDICADOR, FUENTE"
for did in ["DF_ICL2023","DF_NMIC_SEXO","DF_OCUCIUO_CIUO88_SEXO","DF_HRS_TNR_SEXO"]:
    txt=get(f"https://sdmx.ine.gob.cl/rest/data/CL01,{did},1.0?format=csv",
            headers={"Accept":"application/vnd.sdmx.data+csv"},timeout=(10,120)).text
    f=tempfile.NamedTemporaryFile("w",suffix=".csv",delete=False); f.write(txt); f.close()
    duckdb.sql(f"CREATE OR REPLACE TEMP VIEW v AS SELECT * FROM read_csv_auto(['{f.name}'])")
    try:
        cols=duckdb.sql(f"SELECT * EXCLUDE ({DROP}) FROM v LIMIT 0").columns
        n=duckdb.sql(f"SELECT COUNT(*) FROM (SELECT * EXCLUDE ({DROP}) FROM v)").fetchone()[0]
        print(f"{did}: OK rows={n} kept_cols={cols}")
    except Exception as e:
        print(f"{did}: ERROR {e}")
    os.unlink(f.name)
