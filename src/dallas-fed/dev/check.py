import subsets_utils as su
captured={}
def fake_save(table, asset): captured[asset]=table; return asset
su.save_raw_parquet = fake_save
import nodes.dallas_fed as m
m.save_raw_parquet = fake_save

for nid,fn in [("dallas-fed-tmos",m.fetch_diffusion),("dallas-fed-bcs",m.fetch_diffusion),
               ("dallas-fed-des",m.fetch_diffusion),("dallas-fed-agsurvey",m.fetch_agsurvey),
               ("dallas-fed-pce",m.fetch_pce),("dallas-fed-wei",m.fetch_wei),
               ("dallas-fed-houseprice",m.fetch_houseprice)]:
    try:
        fn(nid)
        t=captured[nid]
        print(f"\n### {nid}: {t.num_rows} rows, cols={t.column_names}")
        d=t.to_pylist()
        print("   first:",d[0])
        print("   last :",d[-1])
        # quick distinct checks
        if "component" in t.column_names:
            import collections
            print("   components:",collections.Counter(r['component'] for r in d))
            print("   bases:",set(r['basis'] for r in d))
            print("   segments:",sorted(set(r['segment'] for r in d))[:6])
        if "country" in t.column_names:
            print("   countries:",sorted(set(r['country'] for r in d))[:8],"...n=",len(set(r['country'] for r in d)))
            print("   metrics:",set(r['metric'] for r in d))
        if "horizon" in t.column_names:
            print("   horizons:",set(r['horizon'] for r in d))
        if "topic" in t.column_names:
            print("   topics:",set(r['topic'] for r in d))
        print("   date range:",min(r['date'] for r in d),"->",max(r['date'] for r in d))
    except Exception as e:
        import traceback; traceback.print_exc()
