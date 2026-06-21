import re, io, sys
from subsets_utils import get
import pandas as pd
sys.path.insert(0,"dev")
import parser as P

url=("https://www.statistics.gr/en/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd"
     "&p_p_lifecycle=2&p_p_cacheability=cacheLevelPage&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_javax.faces.resource=document"
     "&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_ln=downloadResources"
     "&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_documentID=225240&_documents_WAR_publicationsportlet_INSTANCE_Mr0GiQJSgPHd_locale=en")
content=get(url,timeout=(10,90)).content
sheets=pd.read_excel(io.BytesIO(content),header=None,dtype=str,sheet_name=None)
df=list(sheets.values())[0]
g=df.where(pd.notna(df),None).values.tolist()
print("dtype sample r2:", g[2])
print("dtype sample r3:", g[3])
print("type of a blank cell r0c1:", repr(g[0][1]), "r3c5:", repr(g[3][5] if len(g[3])>5 else 'NA'))
rows=P.melt_sheet(df,"SDT03","Sheet1")
print("nrows:", len(rows))
from collections import Counter
print("col_label dist:", Counter(r['col_label'] for r in rows))
print("any nan values:", sum(1 for r in rows if r['value']!=r['value']))
print("sample rows:", rows[:3])
