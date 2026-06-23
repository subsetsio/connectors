import sys; sys.path.insert(0,"src")
from nodes import eskom as E

for eid in ["station-build-up-last-7-days","weekly-peak-demand","renewable-statistics",
            "financial-year-load-factor-eskom-ocgt","weekly-uclf-oclf-frequency","total-monthly-ocgt-energy-utilization"]:
    try:
        rk=E._resource_key(eid)
        me=E._models_and_exploration(rk)
        model=me["models"][0]; rid=me["exploration"].get("reportId")
        merged={}; vc=0
        for pq in E._data_visuals(me["exploration"]):
            vc+=1
            data=E._query_visual(rk,model,rid,pq)
            for r in E._rows_from_visual(data):
                merged[(r["period_label"],r["series"])]=r
        rows=list(merged.values())
        sers=sorted({r["series"] for r in rows})
        print(f"\n{eid}: visuals={vc} rows={len(rows)} series={len(sers)}")
        print("  series sample:", sers[:6])
        print("  row sample:", rows[0] if rows else None)
        print("  has period_ms:", any(r['period_ms'] for r in rows))
    except Exception as ex:
        print(f"\n{eid}: ERROR {type(ex).__name__}: {ex}")
