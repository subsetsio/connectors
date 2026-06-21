import sys
sys.path.insert(0, "src")
from nodes.atlanta_fed import (_download_workbook, _read_sheet, _date_str, _num,
                               TRACK_RECORD_SHEET, EVOLUTION_SHEETS)

content = _download_workbook()
print("workbook bytes:", len(content))

# track record
tr = []
col_q="Quarter being forecasted"; col_f="Model Forecast Right Before BEA's Advance Estimate"; col_a="BEA's Advance Estimate"
for r in _read_sheet(content, TRACK_RECORD_SHEET):
    q=_date_str(r.get(col_q)); f=_num(r.get(col_f)); a=_num(r.get(col_a))
    if q and f is not None and a is not None:
        tr.append((q,f,a))
print("track_record rows:", len(tr))
if tr:
    print("  first:", tr[0], "last:", tr[-1])
    fc=[x[1] for x in tr]; print("  forecast min/max:", min(fc), max(fc))
    qs=[x[0] for x in tr]; print("  unique quarters:", len(set(qs)), "==", len(qs))

# evolution
ev=[]
col_fd="Forecast Date"; col_gdp="GDP Nowcast"
for sheet in EVOLUTION_SHEETS:
    for r in _read_sheet(content, sheet):
        fd=_date_str(r.get(col_fd)); q=_date_str(r.get(col_q)); g=_num(r.get(col_gdp))
        if fd and q and g is not None:
            ev.append((fd,q,g))
print("evolution rows:", len(ev))
if ev:
    print("  first:", ev[0], "last:", ev[-1])
    gc=[x[2] for x in ev]; print("  nowcast min/max:", min(gc), max(gc))
    pairs=[(x[0],x[1]) for x in ev]; print("  unique (fdate,quarter):", len(set(pairs)), "of", len(pairs))
