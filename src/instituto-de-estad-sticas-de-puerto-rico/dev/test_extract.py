import itertools
import nodes.instituto_de_estad_sticas_de_puerto_rico as m

m._ensure_http()

def probe(pkg):
    res = m._api("package_show", id=pkg).get("resources", [])
    fmts = {}
    for r in res: fmts[(r.get('format') or '').upper()] = fmts.get((r.get('format') or '').upper(),0)+1
    tables = []
    for r in res:
        try:
            tables.extend(t for t in m._expand_resource(r) if t)
        except Exception as e:
            print(f"   expand err {r.get('name')}: {type(e).__name__}: {e}")
    groups = {}
    for t in tables: groups.setdefault(m._norm_sig(t.columns), []).append(t)
    print(f"\n=== {pkg}: {len(res)} res {fmts} -> {len(tables)} tables, {len(groups)} schema-groups")
    if not tables:
        print("   !!! NO TABLES"); return
    dom = max(groups, key=lambda s:(len(groups[s]),len(s)))
    chosen = groups[dom]
    cols = chosen[0].columns
    # count rows in first chosen table (capped) to confirm data flows
    sample_rows = list(itertools.islice(chosen[0].rows_iter, 3))
    print(f"   dominant: {len(chosen)} tables, {len(cols)} cols: {cols[:8]}")
    print(f"   sample row0 keys-vals: {list(sample_rows[0].items())[:5] if sample_rows else 'EMPTY'}")

for p in ["datos-del-tablero-indice-agricolas-resumen-censos-agricolas-2018-y-2022-por-regiones",
          "mortalidad-infantil-cohortes","hipotecas-home-mortgage-disclosure-act-hmda",
          "commuting-flow-2009-2015","nacimientos","calendario"]:
    try: probe(p)
    except Exception as e: print(f"=== {p}: TOP ERR {type(e).__name__}: {e}")
