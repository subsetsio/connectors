import io, pandas as pd
from subsets_utils import get
BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
for code in ["1.1","3.8.2","1a.2.1.04","2.1"]:
    r=get(BASE+code+".xls", timeout=(10,60))
    c=r.content
    print("="*50,code,"magic",c[:4].hex())
    try:
        df=pd.read_excel(io.BytesIO(c), engine="xlrd", header=None)
    except Exception as e:
        print(" xlrd err",e); continue
    print(" shape",df.shape)
    for i in range(min(10,len(df))):
        row=[str(x) for x in df.iloc[i].tolist()]
        ne=[x for x in row if x and x!='nan']
        if ne: print("  ",i,ne[:16])
