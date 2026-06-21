import sys, io
sys.path.insert(0, "src")
sys.path.insert(0, "src/nodes")
import anp_brazil as M
from constants import ENTITY_IDS
import pyarrow as pa, duckdb

# 1. coverage
miss=[e for e in ENTITY_IDS if e not in M.TRANSFORMS]
print("transforms missing:", miss)
print("download specs:", len(M.DOWNLOAD_SPECS), "transform specs:", len(M.TRANSFORM_SPECS))

def sample_table(url, limit_rows=5000):
    # build a small arrow table from the first batch of a file
    gen = M._iter_file_records(url)
    header, batch = next(gen)
    batch = batch[:limit_rows]
    cols=[[r[i] for r in batch] for i in range(len(header))]
    return pa.table([pa.array(c, type=pa.string()) for c in cols], names=header)

B="https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos"
cases = {
 "vdpb-vendas-derivados-petroleo-e-etanol-vendas-combustiveis-m3": B+"/vdpb/vendas-derivados-petroleo-e-etanol/vendas-combustiveis-m3-1990-2025.csv",
 "ie-petroleo-importacoes-exportacoes-petroleo": B+"/ie/petroleo/importacoes-exportacoes-petroleo-2000-2025.csv",
 "mdpg-glp": B+"/mdpg/glp.zip",
 "mdpg-movimentacaologistica": B+"/mdpg/movimentacaologistica.zip",
 "mdpg-lubrificante": B+"/mdpg/lubrificante.zip",
 "vdpb-vendas-de-biodiesel-vendas-biodiesel-b100-m3": B+"/vdpb/vendas-de-biodiesel/vendas-biodiesel-b100-m3.csv",
 "vdpb-vaehdpm-asfalto-vendas-anuais-de-asfalto-por-municipio": B+"/vdpb/vaehdpm/asfalto/vendas-anuais-de-asfalto-por-municipio.csv",
 "vdpb-vaehdpm-glp-vendas-anuais-de-glp-por-municipio": B+"/vdpb/vaehdpm/glp/vendas-anuais-de-glp-por-municipio.csv",
 "shpc-dsas-ca-ca": B+"/shpc/dsan/2025/precos-diesel-gnv-01.csv",
 "vdpb-vendas-por-produtor-vendas-oleo-diesel-produtores-m3": B+"/vdpb/vendas-por-produtor/vendas-oleo-diesel-produtores-m3-2025-2026.csv",
}
con=duckdb.connect()
for eid,url in cases.items():
    asset=f"anp-brazil-{eid}"
    try:
        t=sample_table(url)
        con.register(asset, t)
        sql=M._build_sql(asset, *M.TRANSFORMS[eid])
        r=con.execute(sql).fetch_arrow_table()
        n=r.num_rows
        # show schema + sample of date/year + first value
        sch={f.name:str(f.type) for f in r.schema}
        print(f"\n[{eid}] in={t.num_rows} out={n}")
        print("   header:", t.column_names)
        print("   out schema:", sch)
        if n: print("   sample:", {k:r.column(k)[0].as_py() for k in list(sch)[:6]})
        con.unregister(asset)
    except Exception as e:
        import traceback; print(f"\n[{eid}] ERROR {type(e).__name__}: {e}")
