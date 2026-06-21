import sys; sys.path.insert(0,"src")
from nodes.berkeley_earth import _fetch_text, _parse_trend, BASE_S3, BASE_AUTO
# Land+Ocean: should now be one section (~2100 months), not 4200
g=_parse_trend(_fetch_text(BASE_S3+"Global/Land_and_Ocean_complete.txt"))
yk=list(zip(g[0],g[1]))
print("L+O rows:", len(g[0]), "unique (yr,mo):", len(set(yk)), "dup:", len(yk)-len(set(yk)), "range", g[0][0], g[0][-1])
# regional single-section unaffected
f=_parse_trend(_fetch_text(BASE_AUTO+"Regional/TAVG/Text/france-TAVG-Trend.txt"))
print("france rows:", len(f[0]), "unique:", len(set(zip(f[0],f[1]))))
# land-only global single section
t=_parse_trend(_fetch_text(BASE_S3+"Global/Complete_TAVG_complete.txt"))
print("global TAVG rows:", len(t[0]), "unique:", len(set(zip(t[0],t[1]))))
