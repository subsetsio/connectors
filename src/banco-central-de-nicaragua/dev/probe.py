import pandas as pd, io
from subsets_utils import get

BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
for code in ["4.IMAE","1.23.1","1a.2.1.04","4.ipcn.1","Mon_3_60_5_1","1.1","4.V.01.01.02"]:
    url=BASE+code+".xls"
    r=get(url, timeout=(10,60))
    print("="*70)
    print(code, r.status_code, r.headers.get("content-type"), len(r.content))
    html=r.content.decode("iso-8859-1","replace")
    try:
        tables=pd.read_html(io.StringIO(html))
    except Exception as e:
        print("read_html err",e); continue
    print("num tables",len(tables))
    t=max(tables,key=lambda d:d.shape[0]*d.shape[1])
    print("shape",t.shape)
    print(t.head(12).to_string()[:2000])
