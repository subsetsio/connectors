from urllib.parse import quote
from subsets_utils import get

BASE = "https://sistemas.anac.gov.br/dadosabertos/"

def enc(path):
    # percent-encode each segment, keep slashes
    return "/".join(quote(seg) for seg in path.split("/"))

def head(url):
    r = get(url, timeout=60)
    return r.status_code, r.headers.get("content-type"), r.headers.get("content-length")

def show_dir(path):
    url = BASE + enc(path) + "/"
    r = get(url, timeout=60)
    print("DIR", url, r.status_code, r.headers.get("content-type"))
    txt = r.text
    print(txt[:1500])
    print("..." )

def show_csv_head(path, nbytes=2000):
    url = BASE + enc(path)
    r = get(url, timeout=120)
    print("CSV", url, r.status_code, r.headers.get("content-type"), "len=", r.headers.get("content-length"))
    raw = r.content[:nbytes]
    for encname in ("utf-8-sig", "latin-1"):
        try:
            txt = raw.decode(encname)
            print(f"--- decoded {encname} ---")
            print(txt[:1200])
            break
        except Exception as e:
            print("decode fail", encname, e)

print("=== autoindex dir: VRA series root ===")
show_dir("Voos e operações aéreas/Voo Regular Ativo (VRA)")
print("\n=== autoindex dir: VRA 2024 ===")
show_dir("Voos e operações aéreas/Voo Regular Ativo (VRA)/2024")
print("\n=== single-file: AerodromosPublicos ===")
show_csv_head("Aerodromos/Aeródromos Públicos/Lista de aeródromos públicos/AerodromosPublicos.csv")
print("\n=== Dados Estatisticos (preamble risk) ===")
show_csv_head("Voos e operações aéreas/Dados Estatísticos do Transporte Aéreo/Dados_Estatisticos_parte.csv")
print("\n=== airfares domestic head ===")
print(head("https://sas.anac.gov.br/sas/tarifadomestica/2023/202301.csv"))
