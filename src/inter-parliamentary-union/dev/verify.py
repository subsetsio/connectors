import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]/"src"))
import json
import nodes.inter_parliamentary_union as m

# Verify flattening for a wrapped entity, a flat entity, and a report — small slices.
for suffix in ["chambers","political-parties","report-women-ranking"]:
    if suffix in m.WRAPPED:
        api,keys=m.WRAPPED[suffix]
        rows=m._fetch_all_list(api)
        out=[{k:m._scalar(m._unwrap(r.get('attributes',{}).get(k))) for k in keys} for r in rows]
    elif suffix in m.FLAT:
        api,keys=m.FLAT[suffix]
        rows=m._fetch_all_list(api)
        out=[{k:m._scalar(r.get(k)) for k in keys} for r in rows]
    else:
        p=m._get_json(f"{m.BASE}/reports/{m.REPORTS[suffix]}")
        rows=m._rows_of(p)
        keys=[]; seen=set()
        for r in rows:
            for k in r:
                if k not in seen and k not in m._REPORT_DROP: seen.add(k); keys.append(k)
        out=[{k:m._scalar(r.get(k)) for k in keys} for r in rows]
    print(f"\n== {suffix}: {len(out)} rows ==")
    print(json.dumps(out[0], ensure_ascii=False, indent=1))
    # type sanity: count non-null per col
    cols=out[0].keys()
    nn={c:sum(1 for r in out if r.get(c) not in (None,'')) for c in cols}
    print("nonnull:", {c:nn[c] for c in list(cols)[:8]})
