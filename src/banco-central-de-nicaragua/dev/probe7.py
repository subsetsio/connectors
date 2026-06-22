from bs4 import BeautifulSoup
from subsets_utils import get
BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
for code in ["4.IMAE","1.1","3.8.2","1a.2.1.04"]:
    r=get(BASE+code+".xls", timeout=(10,60))
    h=r.content.decode("iso-8859-1","replace")
    soup=BeautifulSoup(h,"html5lib")
    trs=soup.find_all("tr")
    data=[]
    for tr in trs:
        cells=[c.get_text(strip=True) for c in tr.find_all(["td","th"])]
        ne=[c for c in cells if c]
        if ne: data.append(cells)
    print("="*50,code,"trs",len(trs),"datarows",len(data))
    for row in data[:8]:
        print("  ",[c for c in row if c][:16])
    if len(data)>8:
        print("  ... last:",[c for c in data[-1] if c][:16])
