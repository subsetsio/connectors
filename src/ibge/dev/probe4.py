from subsets_utils import get
import json
r=get("https://servicodados.ibge.gov.br/api/v1/localidades/municipios",timeout=90)
d=r.json(); print("n_muni:",len(d)); print(json.dumps(d[0],ensure_ascii=False,indent=1)[:700])
