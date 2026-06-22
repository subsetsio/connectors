import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
def show(url, accept):
    r=get(url, headers={"Accept":accept}, timeout=(15,120))
    print(f"[{r.status_code}] {url}  (Accept={accept})")
    print("   ", r.text[:280].replace("\n"," "))
# 400 detail body
show("https://api.statistiken.bundesbank.de/rest/data/BBBK7?detail=serieskeysonly","application/vnd.sdmx.data+csv;version=1.0.0")
# try SDMX-ML structurespecific with serieskeysonly
show("https://api.statistiken.bundesbank.de/rest/data/BBBK7?detail=serieskeysonly","application/vnd.sdmx.structurespecificdata+xml;version=2.1")
# try nodata
show("https://api.statistiken.bundesbank.de/rest/data/BBBK7?detail=nodata","application/vnd.sdmx.data+csv;version=1.0.0")
# try generic + lastN with firstN
show("https://api.statistiken.bundesbank.de/rest/data/BBBK7/Q.?firstNObservations=1","application/vnd.sdmx.data+csv;version=1.0.0")
