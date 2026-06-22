import sys; sys.path.insert(0,'src')
import nodes.cbn as c, time
tid=48
info=c._indicators_for_table(tid); ids=[i for i,_ in info]
for sd,ed in [("2020-06-01","2020-06-30"),("2024-02-01","2027-12-31"),("2024-02-01","2024-02-29"),("2023-01-01","2026-12-31"),("2020-06-01","2020-06-30")]:
    j=c._post_search_raw(tid,ids,sd,ed)
    print(f"{sd}..{ed}: ok={j.get('IsSuccessful')} err={j.get('Error')!r} tvlen={len(j.get('TableView') or '')}")
    time.sleep(1)
