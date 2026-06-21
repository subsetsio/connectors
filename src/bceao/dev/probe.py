import re, os, tempfile, certifi
bundle = open(certifi.where()).read() + "\n" + open("/tmp/thawte.crt").read()
f = tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False); f.write(bundle); f.close()
os.environ["SSL_CERT_FILE"] = f.name
from subsets_utils import post, configure_http
configure_http()

BASE = "https://edenpub.bceao.int"
def P(path, data=None):
    return post(f"{BASE}/{path}", data=data or {}, timeout=90).text

idx = post(f"{BASE}/index.php", timeout=60).text
years = {}
for m in re.finditer(r"case '([A-Z])'\s*:\s*idAnnee\s*=\s*'([^']*)'", idx):
    arr = [y for y in m.group(2).split(';') if y]
    years[m.group(1)] = (arr[0], arr[-1]) if arr else None
print("freq year-ranges:", years)

SECT = ["SR","SF","FP","SE","SS"]
subs = {}
for s in SECT:
    html = P("secteursDAO.php", {"idSecteur": s})
    subs[s] = re.findall(r"value='([A-Z]{2}[0-9]+)'[^>]*name='groupe_soussecteurs'", html)
print("subsectors:", subs)

OPT = re.compile(r"<option value='([A-Z0-9]+)'>\[[^\]]*\]\s*\[([^\]]*)\]\s*(?:\[([^\]]*)\])?")
for sub in ["SR1","SF1","SE1"]:
    for c in ["A","Z"]:
        for fr in ["A","M","T","H","J","D","S"]:
            try:
                html = P("variablesDAO.php", {"idSousSecteur": sub, "idLocalite": ";"+c, "idFrequence": fr})
            except Exception as e:
                print(f"{sub} {c} {fr}: ERR {e}"); continue
            opts = OPT.findall(html)
            if opts:
                print(f"{sub} c={c} f={fr}: {len(opts)} e.g. {opts[0][0]} | {opts[0][1][:30]} | unit={opts[0][2]!r}")

print("=== export monthly CPI Burkina metadonnee=1 serie=l ===")
print(P("exportRapport.php", {"paysUemoa":"C","frequence":"M","export":"xcl",
        "parametre":"M*CCCSR3017M0BP*1;2023*6;2023*1*l"})[:700])
print("=== export annual batch (2 series) Cote d'Ivoire ===")
print(P("exportRapport.php", {"paysUemoa":"A","frequence":"A","export":"xcl",
        "parametre":"A*AAASR1011A0BP;AAASR1012A0BP*2018*2023*0*l"})[:500])
