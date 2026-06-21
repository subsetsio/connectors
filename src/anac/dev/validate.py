import sys
sys.path.insert(0, "src")
import importlib
m = importlib.import_module("nodes.anac")

def sample_parse(url, n=3):
    r = m._http_get(url)
    rows = []
    for rec in m._parse_csv(r.content):
        rows.append(rec)
        if len(rows) >= n:
            break
    print("  rows>=", len(rows), "ncols:", len(rows[0]) if rows else 0,
          "cols:", list(rows[0].keys())[:5] if rows else None)

print("=== dir: AerodromosPrivados leaf ===")
fs = m._dir_csvs("Aerodromos/Aeródromos Privados/Lista de aeródromos privados/Aerodromos Privados")
print("  csvs:", [x.rsplit('/',1)[-1] for x in fs]);
if fs: sample_parse(fs[0])

print("=== file-match: Ocorrencias V2 + Historico (collision dir) ===")
u = m._pick_file("Seguranca Operacional/Ocorrências de Dificuldades em Serviço em Aeronaves", "v2")
print("  v2 ->", u.rsplit("/",1)[-1])
u2 = m._pick_file("Seguranca Operacional/Ocorrências de Dificuldades em Serviço em Aeronaves", "historico")
print("  historico ->", u2.rsplit("/",1)[-1])
sample_parse(u2)

print("=== dir: dados consumidor (exclude Estrutura_Antiga subdir) ===")
fs = m._dir_csvs("Voos e operações aéreas/Dados do consumidor.gov")
print("  direct csvs:", [x.rsplit('/',1)[-1] for x in fs])

print("=== dir: Aeronaves/RAB (direct only, skip Historico_RAB) ===")
fs = m._dir_csvs("Aeronaves/RAB")
print("  direct csvs:", [x.rsplit('/',1)[-1] for x in fs])

print("=== tree: Slots Alocados (small partitioned) ===")
fs = m._tree_csvs("Voos e operações aéreas/Slots Alocados")
print("  leaves:", len(fs), "sample:", [x.rsplit('/',1)[-1] for x in fs[:3]])
if fs: sample_parse(fs[0])

print("=== airfares head parse ===")
sample_parse(f"{m.SAS_BASE}tarifadomestica/2023/202301.csv")
print("ALL OK")
