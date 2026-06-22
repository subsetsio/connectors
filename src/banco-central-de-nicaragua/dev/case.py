from subsets_utils import get
BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
for code in ["4.IMAE","4.imae","Mon_3_60_5_1","mon_3_60_5_1","4.V.01.01.02","4.v.01.01.02"]:
    try:
        r=get(BASE+code+".xls",timeout=(10,60))
        print(code, r.status_code, len(r.content), r.content[:4].hex())
    except Exception as e:
        print(code,"ERR",str(e)[:60])
