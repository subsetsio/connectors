from subsets_utils import get
from bs4 import BeautifulSoup
r=get("https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/4.IMAE.xls",timeout=(10,60))
soup=BeautifulSoup(r.content.decode("iso-8859-1","replace"),"html5lib")
rows=[[c.get_text(strip=True) for c in tr.find_all(["td","th"])] for tr in soup.find_all("tr")]
import re
yrs=[]
for i,row in enumerate(rows):
    cells=[c for c in row if c.strip()]
    if cells and re.match(r"^\d{4}$",cells[0].strip()):
        yrs.append((i,cells[0],len(cells)))
print("num year-rows:",len(yrs))
for y in yrs: print(y)
