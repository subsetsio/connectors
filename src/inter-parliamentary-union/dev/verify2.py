import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]/"src"))
import importlib, nodes.inter_parliamentary_union as m
for suffix in ["report-age-brackets","report-women-ranking","report-women-speakers","report-secretaries-general"]:
    p=m._get_json(f"{m.BASE}/reports/{m.REPORTS[suffix]}")
    rows=m._rows_of(p); keys=[];seen=set()
    for r in rows:
        for k in r:
            if k not in seen and k not in m._REPORT_DROP: seen.add(k);keys.append(k)
    out=[{k:m._scalar(r.get(k)) for k in keys} for r in rows]
    empty=[k for k in keys if all(r.get(k) in (None,"") for r in out)]
    kept=[k for k in keys if k not in empty]
    print(f"{suffix}: dropped={empty}")
    print(f"   kept={kept}")
