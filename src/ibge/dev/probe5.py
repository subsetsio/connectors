from subsets_utils import get
import time
PREF=["N3","N2","N1"]
for aid in ["19","20","22"]:
    t0=time.time()
    meta=get(f"https://servicodados.ibge.gov.br/api/v3/agregados/{aid}/metadados",timeout=120).json()
    adm=meta["nivelTerritorial"]["Administrativo"]
    level=next((L for L in PREF if L in adm),adm[0])
    varids="|".join(str(v["id"]) for v in meta["variaveis"])
    nper=len(get(f"https://servicodados.ibge.gov.br/api/v3/agregados/{aid}/periodos",timeout=120).json())
    print(f"{aid}: '{meta['nome'][:45]}' lvl={level} adm={adm} nvars={len(meta['variaveis'])} nperiods={nper} nclassif={len(meta.get('classificacoes',[]))} freq={meta['periodicidade']}")
    t1=time.time()
    url=f"https://servicodados.ibge.gov.br/api/v3/agregados/{aid}/periodos/all/variaveis/{varids}?localidades={level}[all]"
    try:
        r=get(url,timeout=120); data=r.json()
        rows=sum(len(s['serie']) for res in data for rr in res['resultados'] for s in rr['series'])
        print(f"   data fetch {time.time()-t1:.1f}s status={r.status_code} rows={rows} bytes={len(r.content)}")
    except Exception as e:
        print(f"   FETCH ERR after {time.time()-t1:.1f}s: {type(e).__name__} {e}")
