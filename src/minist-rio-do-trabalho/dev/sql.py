import duckdb, json, tempfile, os
td=tempfile.mkdtemp()
# CAGED-like
f=os.path.join(td,"c-202401.ndjson")
open(f,"w").write("\n".join(json.dumps(r) for r in [
 {"competencia":202401,"arquivo_fonte":"CAGEDMOV202401","saldomovimentacao":"1","uf":"35"},
 {"competencia":202401,"arquivo_fonte":"CAGEDMOV202401","saldomovimentacao":"-1","uf":"33"},
])+"\n")
print("CAGED:")
print(duckdb.sql(f"""
SELECT TRY_CAST(competencia AS BIGINT) AS competencia,
       TRY_CAST(competencia AS BIGINT)//100 AS ano,
       TRY_CAST(competencia AS BIGINT)%100 AS mes,
       CAST(try_strptime(CAST(competencia AS VARCHAR)||'01','%Y%m%d') AS DATE) AS data_competencia,
       * EXCLUDE (competencia)
FROM read_json_auto(['{f}'])
""").fetchall())
# RAIS-like, two files different cols
r1=os.path.join(td,"r-1985.ndjson"); r2=os.path.join(td,"r-2023.ndjson")
open(r1,"w").write(json.dumps({"ano":1985,"arquivo_fonte":"AC1985","sexo":"01"})+"\n")
open(r2,"w").write(json.dumps({"ano":2023,"arquivo_fonte":"RAIS_VINC_PUB_SP","sexo_trabalhador":"1","raca_cor":"2"})+"\n")
print("RAIS:")
print(duckdb.sql(f"SELECT TRY_CAST(ano AS INTEGER) AS ano, * EXCLUDE (ano) FROM read_json_auto(['{r1}','{r2}'])").fetchall())
print(duckdb.sql(f"SELECT TRY_CAST(ano AS INTEGER) AS ano, * EXCLUDE (ano) FROM read_json_auto(['{r1}','{r2}'])").columns)
