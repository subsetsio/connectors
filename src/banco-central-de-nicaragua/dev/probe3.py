from subsets_utils import get
BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
for code in ["4.IMAE","1.1"]:
    r=get(BASE+code+".xls", timeout=(10,60))
    h=r.content.decode("iso-8859-1","replace")
    print("="*60,code,"len",len(h))
    for y in ["1994","1995","2000","2020","2024","2025"]:
        print(y, h.count(y))
    print("tr count", h.lower().count("<tr"))
    print("td count", h.lower().count("<td"))
    print("table count", h.lower().count("<table"))
