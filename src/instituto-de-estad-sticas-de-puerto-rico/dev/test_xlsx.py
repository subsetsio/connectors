import itertools
import nodes.instituto_de_estad_sticas_de_puerto_rico as m
m._ensure_http()
def probe(pkg):
    res = m._api("package_show", id=pkg)["resources"]
    tables=[]
    for r in res:
        try: tables.extend(t for t in m._expand_resource(r) if t)
        except Exception as e: print("  err",r.get('name'),e)
    groups={}
    for t in tables: groups.setdefault(m._norm_sig(t.columns),[]).append(t)
    if not tables: print(f"=== {pkg}: NO TABLES"); return
    dom=max(groups,key=lambda s:(len(groups[s]),len(s)))
    cols=groups[dom][0].columns
    sample=list(itertools.islice(groups[dom][0].rows_iter,2))
    unnamed=sum(1 for c in cols if c.startswith('col_') or 'Unnamed' in c)
    print(f"=== {pkg}: dom {len(groups[dom])}t {len(cols)}c, {unnamed} unnamed")
    print(f"   cols[:8]={cols[:8]}")
    print(f"   row0={list(sample[0].items())[:4] if sample else 'EMPTY'}")
for p in ["ghgrp","directorio-de-instituciones-de-educacion-superior-puerto-rico","lmop",
          "matriz-insumo-producto-mip","datos-del-tablero-indice-agricolas-resumen-censos-agricolas-2018-y-2022-por-regiones",
          "directorio-de-escuelas-publicas-puerto-rico-2020-2021"]:
    try: probe(p)
    except Exception as e: print(f"=== {p}: ERR {type(e).__name__}: {e}")
