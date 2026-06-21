import itertools
import nodes.instituto_de_estad_sticas_de_puerto_rico as m
m._ensure_http()
def probe(pkg):
    res=m._api("package_show",id=pkg)["resources"]; tables=[]
    for r in res:
        try: tables.extend(t for t in m._expand_resource(r) if t)
        except Exception as e: print("  err",e)
    groups={}
    for t in tables: groups.setdefault(m._norm_sig(t.columns),[]).append(t)
    if not tables: print(pkg,"NO TABLES"); return
    def q(s):
        rep=groups[s][0].columns; synth=sum(1 for c in rep if c.startswith('col_'))
        return (len(groups[s]), len(rep)-synth, -synth)
    dom=max(groups,key=q); cols=groups[dom][0].columns
    s=list(itertools.islice(groups[dom][0].rows_iter,2))
    synth=sum(1 for c in cols if c.startswith('col_'))
    print(f"{pkg}: {len(cols)}c {synth}synth cols[:6]={cols[:6]} row0={list(s[0].items())[:3] if s else 'E'}")
for p in ["ghgrp","directorio-de-instituciones-de-educacion-superior-puerto-rico"]:
    try: probe(p)
    except Exception as e: print(p,"ERR",e)
