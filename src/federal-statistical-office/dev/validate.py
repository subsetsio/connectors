import json, sys
sys.path.insert(0,"src")
import importlib.util
spec=importlib.util.spec_from_file_location("mod","src/nodes/federal_statistical_office.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

col=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/federal-statistical-office/assets/collect/entities/current.json"))
union=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/federal-statistical-office/work/entity_union.json"))
# pick a small single-chunk cube and a multi-chunk cube
sizes=[(col[e]["source_metadata"]["n_cells"],e) for e in union]
sizes.sort()
small=sizes[0][1]
multi=[e for c,e in sizes if 200000<c<600000][0]
for cube,label in [(small,"SMALL"),(multi,"MULTI")]:
    lang,url,meta=mod._fetch_meta(cube)
    colmap=mod._column_map(meta)
    dim_codes=[v["code"] for v in meta["variables"]]
    value_lists=[list(v["values"]) for v in meta["variables"]]
    chunks=list(mod._plan_chunks(dim_codes,value_lists))
    import math
    total=math.prod(len(v) for v in value_lists)
    # verify chunks partition the full product (sum of chunk cells == total, rectangular non-overlap)
    csum=sum(math.prod(len(sel[c]) for c in dim_codes) for sel in chunks)
    maxcells=max(math.prod(len(sel[c]) for c in dim_codes) for sel in chunks)
    print(f"\n=== {label} {cube} lang={lang} total_cells={total} chunks={len(chunks)} sum_chunk_cells={csum} max_chunk={maxcells}")
    print("columns:",list(colmap.values()))
    # fetch first chunk, reshape, show sample
    js=mod._post_jsonstat(url, [{"code":c,"selection":{"filter":"item","values":chunks[0][c]}} for c in dim_codes])
    rows=list(mod._reshape(js,colmap,cube,meta.get("updated")))
    print("first-chunk rows:",len(rows),"| sample:",json.dumps(rows[0],ensure_ascii=False) if rows else "none")
    assert csum==total, "chunk cells do not sum to total!"
    assert maxcells<=mod.SAFE_CELLS_PER_QUERY, "chunk exceeds cap!"
print("\nALL OK")
