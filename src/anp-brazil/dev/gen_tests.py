import sys, os
sys.path.insert(0,"src"); sys.path.insert(0,"src/nodes")
import anp_brazil as M
from constants import ENTITY_IDS
os.makedirs("tests", exist_ok=True)

KEY = {
 "monthly": ("ano", r"^[0-9]{4}$"),
 "annual":  ("ano", r"^[0-9]{4}$"),
 "periodo": ("periodo", r"^[0-9]{4}/[0-9]{1,2}$"),
 "mesano":  ("mes_ano", r"^[0-9]{1,2}/[0-9]{4}$"),
 "coleta":  ("data_da_coleta", r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$"),
}
MIN = {
 "shpc-dsas-ca-ca": 100000,
 "vdpb-vaehdpm-asfalto-vendas-anuais-de-asfalto-por-municipio": 20000,
 "vdpb-vaehdpm-glp-vendas-anuais-de-glp-por-municipio": 2000,
 "vdpb-vaehdpm-oleo-combustivel-vendas-anuais-de-oleo-combustivel-por-municipio": 2000,
 "vdpb-vendas-derivados-petroleo-e-etanol-vendas-combustiveis-m3": 1000,
 "ppgn-el-producao-petroleo-m3": 1000,
 "arquivos-vendas-anuais-de-etanol-hidratado-e-derivados-de-petroleo-por-estado-ve": 200,
}
def rmin(eid): return MIN.get(eid, 300)

def yam(eid):
    kind = M.TRANSFORMS[eid][0]
    key, pat = KEY[kind]
    sid = f"anp-brazil-{eid}"
    L = [f"spec_id: {sid}", "status: active", "tests:"]
    L += [f"  - row_count: {{min: {rmin(eid)}}}",
          f"    reason: ANP publishes the full history for this series; a tiny table means a download/parse break or a renamed file path.",
          f"    certainty: 80"]
    L += [f"  - not_null: {key}",
          f"    reason: every row is stamped with its period; nulls here mean header misalignment or wrong delimiter/encoding.",
          f"    certainty: 90"]
    L += [f"  - matches: {{col: {key}, pattern: '{pat}'}}",
          f"    reason: raw period column must match the source's documented format ({pat}); a mismatch flags an encoding/delimiter regression.",
          f"    certainty: 85"]
    return "\n".join(L)+"\n"

for eid in ENTITY_IDS:
    open(f"tests/anp-brazil-{eid}.yaml","w").write(yam(eid))
print("wrote", len(ENTITY_IDS), "yaml files")
