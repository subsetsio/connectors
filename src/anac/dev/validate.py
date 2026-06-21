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
    print("  rows:", len(rows), "cols:", list(rows[0].keys())[:6] if rows else None)
    if rows:
        print("  first:", {k: rows[0][k] for k in list(rows[0])[:3]})

print("=== file-match: AerodromosPrivados ===")
u = m._pick_file("Aerodromos/Aeródromos Privados/Lista de aeródromos privados", "aerodromosprivados")
print(" picked:", u.rsplit("/",1)[-1]); sample_parse(u)

print("=== file-match: Ocorrencias V2 (accented filename) ===")
u = m._pick_file("Seguranca Operacional/Ocorrências de Dificuldades em Serviço em Aeronaves", "v2")
print(" picked:", u.rsplit("/",1)[-1]); sample_parse(u)
u2 = m._pick_file("Seguranca Operacional/Ocorrências de Dificuldades em Serviço em Aeronaves", "historico")
print(" picked hist:", u2.rsplit("/",1)[-1])

print("=== dir multi: drones Historico (n_files) ===")
fs = m._dir_csvs("Aeronaves/drones cadastrados/Historico")
print("  csv count:", len(fs), "sample:", [x.rsplit('/',1)[-1] for x in fs[:3]])

print("=== dir single but has subdir: Aeronaves/RAB ===")
fs = m._dir_csvs("Aeronaves/RAB")
print("  direct csvs:", [x.rsplit('/',1)[-1] for x in fs])

print("=== dir: dados consumidor (must exclude Estrutura_Antiga subdir) ===")
fs = m._dir_csvs("Voos e operações aéreas/Dados do consumidor.gov")
print("  direct csvs:", [x.rsplit('/',1)[-1] for x in fs])

print("=== tree: percentuais (count leaves, sample) ===")
fs = m._tree_csvs("Voos e operações aéreas/Percentuais de atrasos e cancelamentos")
print("  leaf csv count:", len(fs))
print("  samples:", [x.rsplit('/',1)[-1] for x in fs[:3]])
if fs:
    sample_parse(fs[0])

print("=== airfares existence: domestic 2023-01 and a likely-missing 2002-01 ===")
print("  2023-01:", m._http_get_optional(f"{m.SAS_BASE}tarifadomestica/2023/202301.csv") is not None)
print("  2002-01:", m._http_get_optional(f"{m.SAS_BASE}tarifadomestica/2002/200201.csv") is not None)
ur = f"{m.SAS_BASE}tarifadomestica/2023/202301.csv"
sample_parse(ur)
